import qrcode

url = "http://192.168.1.8:5000"

qr = qrcode.make(url)

qr.save("restaurant_qr.png")

print("QR code created successfully!")