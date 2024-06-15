import requests
import pandas as pd
from io import BytesIO

# Fungsi untuk mengirim data ke API
def send_data_to_api(data, image_data):
    url = 'http://34.101.239.167/product'
    headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRmOGIxNTFiY2Q5MGQ1YjMwMjBlNTNhMzYyZTRiMzA3NTYzMzdhNjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcmVudHN0eWxlIiwiYXVkIjoicmVudHN0eWxlIiwiYXV0aF90aW1lIjoxNzE4NDY0MDUzLCJ1c2VyX2lkIjoiNDJ2UmVycEFjNVF2ZnljemxoWGI4U1EyWmFuMiIsInN1YiI6IjQydlJlcnBBYzVRdmZ5Y3psaFhiOFNRMlphbjIiLCJpYXQiOjE3MTg0NjQwNTMsImV4cCI6MTcxODQ2NzY1MywiZW1haWwiOiJkaHlvZ2FAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImRoeW9nYUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.WZIfm_tMoZq0kVtTpV0samIobK03YJW4P8pHIo0YQoLewYTl5x4j6-WmyENh0_p9QTU2_f1QcUO9t94reDO-HP3wskW3vd0mkdcyvV7qJEW4qVc9W9kCxkT6cNo_-cgOWq5E6z3Iz5gr6VKExuyZN6sNBYa27fRw0Xq7Tkc6--_FJYwv3_OVo8OktbDqMJPV_LmHC8dh80jDeg5YYWv3q9_NLjtaBo1pMN84JN2UOlTBSZu4OLPSn4F0ygLMElKtjpoA1dkgNSfmjfFnBGVu62TL96aDweKT4zftiSj8bCj1EjMjm4YNaBd0lEHqVgH-vgl5tMaiWTRAKIkPUjK3nQ'}

    # Data produk yang akan dikirim
    product_data = {
        'seller_id': data['seller_id'],
        'product_name': data['product_name'],
        'category': data['category'],
        'color': data['color'],
        'size': data['size'],
        'product_price': data['product_price'],
        'rent_price': data['rent_price'],
        'desc': data['desc']
    }

    try:
        # Membuat form-data multipart untuk mengirim gambar dan data produk
        files = {'image': ('product_image.jpg', image_data, 'image/jpeg')}
        response = requests.post(url, headers=headers, data=product_data, files=files)

        # Tampilkan hasil atau respon dari API
        print(f"Response from API: {response.status_code}")
        print(response.json())  # Jika API mengembalikan JSON response

    except Exception as e:
        print(f"Error sending data to API: {e}")

# Fungsi untuk mengambil gambar dari URL
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download image from {url}")
            return None
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None

# Fungsi untuk membaca CSV dan mengolah setiap baris
def process_csv(filename):
    try:
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            # Konversi rent_price dan product_price ke format angka
            try:
                row['rent_price'] = float(row['rent_price'].replace('Rp', '').replace('.', '').replace(',', ''))
            except ValueError:
                print(f"Invalid rent_price format for row {index + 1}: {row['rent_price']}")
                continue

            try:
                row['product_price'] = float(row['product_price'].replace('Rp', '').replace('.', '').replace(',', ''))
            except ValueError:
                print(f"Invalid product_price format for row {index + 1}: {row['product_price']}")
                continue

            image_url = row['image']
            image_data = download_image(image_url)

            if image_data:
                send_data_to_api(row, image_data)
            else:
                print(f"Failed to download image from {image_url}")

    except Exception as e:
        print(f"Error processing CSV: {e}")

# Panggil fungsi untuk memulai proses
process_csv('product.csv')
