from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import random
import os

# Function to generate a random EAN-13 barcode number
def generate_random_ean13():
    # EAN-13 requires a 12-digit number, the 13th digit is a checksum calculated by the library
    return ''.join(str(random.randint(0, 9)) for _ in range(12))

# Create a new PDF document
pdf_filename = "ean13_barcodes.pdf"
c = canvas.Canvas(pdf_filename, pagesize=A4)
width, height = A4

# Set dimensions for barcodes on the PDF
barcode_width = 2 * inch
barcode_height = 1 * inch
margin = 0.5 * inch
barcodes_per_row = int((width - 2 * margin) / barcode_width)
barcodes_per_column = int((height - 2 * margin) / barcode_height)

# Generate and add 20 EAN-13 barcodes to the PDF
for i in range(20):
    ean = generate_random_ean13()
    ean13 = EAN13(ean, writer=ImageWriter())
    filename = f'temp_barcode_{i}'

    # Save the barcode image without the '.png' extension
    ean13.save(filename)

    row = i // barcodes_per_row
    col = i % barcodes_per_row
    x = margin + col * barcode_width
    y = height - margin - (row + 1) * barcode_height

    if y < margin:
        c.showPage()
        y = height - margin - barcode_height
        row = 0

    # Draw the barcode image on the PDF
    c.drawImage(f'{filename}.png', x, y, barcode_width, barcode_height)

    # Remove the temporary barcode image file
    os.remove(f'{filename}.png')

c.save()

print(f"PDF with 20 EAN-13 barcodes saved as {pdf_filename}")
