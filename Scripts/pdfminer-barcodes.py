import io
import base64
import re
import requests
from pdfminer.high_level import extract_pages


def base64_to_bytes(base64_str):
    byte_data = base64.b64decode(base64_str)
    return byte_data

def process_pdf_from_url(pdf_url_or_byte: str | bytes):
    if isinstance(pdf_url_or_byte, str):
        response = requests.get(pdf_url_or_byte)
        pdf = io.BytesIO(response.content)
    elif isinstance(pdf_url_or_byte, bytes):
        pdf_bytes = base64_to_bytes(pdf_url_or_byte)
        pdf = io.BytesIO(pdf_bytes)
    else:
        raise ValueError("O parâmetro pdf_url deve ser uma string ou bytes.")

    barcode = None
    match_regex = None

    regex_attempt_list = [
        r'(\d{11}-\d{1} \d{11}-\d{1} \d{11}-\d{1} \d{11}-\d{1})',
        r'(\d{12} \d{12} \d{12} \d{12})',
        r'(\d{5}\.\d{5} \d{5}\.\d{6} \d{5}\.\d{6} \d{1} \d{14})',
        r'(\d{44})',
        r'(\d{5}-\d{5} \d{5}-\d{6} \d{5}-\d{6} \d{1} \d{14})',
        r'(\d{47})',
        r'(\d{12}-\d{12}-\d{12}-\d{12})',
        r'(\d{12}\.\d{12}\.\d{12}\.\d{1}\s\d{14})',
        r'(\d{10} \d{10} \d{10} \d{14})',
        r'(\d{10}-\d{10}-\d{10}-\d{14})',
        r'(\d{13}\s\d{13}\s\d{13}\s\d{13})',
        r'(\d{5} \d{6} \d{5} \d{6} \d{5} \d{6} \d{5} \d{6})',
        r'(\d{50})',
        r'([A-Z0-9]{15,50})',
        r'(\d{5}[-\.]\d{5} \d{5}[-\.]\d{6} \d{5}[-\.]\d{6} \d{1} \d{14})',
        r'(\d{5} \d{5} \d{5} \d{5} \d{5} \d{5})',
        r'(\d{5}-\d{5}-\d{5}-\d{5}-\d{5})'
    ]

    pdf_lines = []
    for page_layout in extract_pages(pdf):
        for element in page_layout:
            try:
                element_text = element.get_text().strip()
                pdf_lines.append(element_text)
                for regex in regex_attempt_list:
                    barcode_match = re.search(regex, element_text)

                    if barcode_match:
                        barcode = re.sub(r'\D', '', barcode_match.group(1))
                        match_regex = regex
                        break
            except:
                continue

    print(pdf_lines)

    return barcode, match_regex

pdf_url_or_byte = 'https://d3mc5mwbv01en1.cloudfront.net/74df892e-f22c-4334-a050-3cfdfcfdc2de.pdf'
barcode_regex = process_pdf_from_url(pdf_url_or_byte)
print(f"\nCódigo de barras encontrado: \n{barcode_regex}")
