import io
import re
import requests
from pdfminer.high_level import extract_pages


def process_pdf_from_url(pdf_url):
    # Faz o download do PDF
    response = requests.get(pdf_url)
    response.raise_for_status()  # Verifica se o download foi bem-sucedido

    # Converte o conteúdo baixado em um arquivo em memória
    pdf_memory_file = io.BytesIO(response.content)

    barcode = None

    # Processa o PDF da mesma forma que no seu código original
    for page_layout in extract_pages(pdf_memory_file):
        for element in page_layout:
            try:
                element_text = element.get_text().strip()
                barcode_match = re.search(r'(\d{11}-\d{1} \d{11}-\d{1} \d{11}-\d{1} \d{11}-\d{1})', element_text)
                print('*', element_text, '*')
                if barcode_match:
                    print(element_text)
                    barcode = re.sub(r'\D', '', barcode_match.group(1))  # Remove todos os caracteres que não são números
                    print("resultadooo")
                    print(barcode)

            except Exception as e:
                print(f"Erro ao processar elemento: {e}")
                continue

    return barcode

# Exemplo de uso
pdf_url = "https://d3mc5mwbv01en1.cloudfront.net/2d8d5264-b220-468f-84f0-997686f5b3f5.pdf"
barcode = process_pdf_from_url(pdf_url)
print(f"Código de barras encontrado: {barcode}")
