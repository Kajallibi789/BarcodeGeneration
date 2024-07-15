import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from qrcode.image.pil import PilImage
import random
import string
from io import BytesIO

# Function to generate a random string
def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Create a new PDF document
pdf_filename = "qr_codes.pdf"
c = canvas.Canvas(pdf_filename, pagesize=A4)
width, height = A4

# Set dimensions for QR codes on the PDF
qr_size = 2 * inch
margin = 0.5 * inch
qr_per_row = int((width - 2 * margin) / qr_size)
qr_per_column = int((height - 2 * margin) / qr_size)

# Generate and add QR codes to the PDF
for i in range(60):
    data = f"https://example.com/{generate_random_string()}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="blue", back_color="red", image_factory=PilImage)

    # Convert the PIL image to a BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    row = i // qr_per_row
    col = i % qr_per_row
    x = margin + col * qr_size
    y = height - margin - (row + 1) * qr_size

    if y < margin:
        c.showPage()
        y = height - margin - qr_size
        row = 0

    # Use ImageReader to read the BytesIO object
    img_reader = ImageReader(img_byte_arr)
    c.drawImage(img_reader, x, y, qr_size, qr_size)

c.save()

print(f"PDF with 60 QR codes saved as {pdf_filename}")
