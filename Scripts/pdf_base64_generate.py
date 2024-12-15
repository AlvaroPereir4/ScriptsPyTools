import base64


def encode_bytes_to_base64(data: bytes) -> str:
    encoded_data = base64.b64encode(data)
    return encoded_data.decode('utf-8')


data = 'byteshere'
encoded_string = encode_bytes_to_base64(data)
print("Encoded String:", encoded_string)
