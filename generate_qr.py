import qrcode
import json

def generate_qr(fitting_id):
    data = {"fitting_id": fitting_id}
    data_str = json.dumps(data)

    qr = qrcode.make(data_str)
    filename = f"{fitting_id}_qr.png"
    qr.save(filename)

    print(f"QR code generated and saved as {filename}")

if __name__ == '__main__':
    generate_qr("FLINER-987654")
