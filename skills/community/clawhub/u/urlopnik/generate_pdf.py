#!/usr/bin/env python3
"""
Urlopnik — Generator PDF wniosków urlopowych
Wymaga: reportlab (pip install reportlab)
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph
    from reportlab.lib.colors import HexColor
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def generate_pdf(employee, start_date, end_date, leave_type_name, filename="wniosek_urlopowy.pdf"):
    """Generuje PDF wniosku urlopowego."""
    
    if not HAS_REPORTLAB:
        print("⚠️  reportlab nie jest zainstalowany. Instaluję...")
        import subprocess
        subprocess.run(["pip", "install", "reportlab"], check=True)
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Kolory
    blue = HexColor('#2563eb')
    dark = HexColor('#1e293b')
    gray = HexColor('#64748b')
    light_gray = HexColor('#f1f5f9')
    
    # Header
    c.setFillColor(blue)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 40, "WNIOSEK O URLOP WYPOCZYNKOWY")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 60, "Formularz urlopowy - pracownik")
    
    # Info o dokumencie
    c.setFillColor(dark)
    c.setFont("Helvetica", 9)
    c.drawString(2*cm, height - 100, f"Data: {start_date.strftime('%d.%m.%Y')}")
    c.drawRightString(width - 2*cm, height - 100, f"Nr: WR/{start_date.strftime('%Y%m%d')}/{employee.get('initials', 'XX')}")
    
    # Sekcja: Dane pracownika
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, height - 130, "DANE PRACOWNIKA")
    
    c.setStrokeColor(light_gray)
    c.line(2*cm, height - 135, width - 2*cm, height - 135)
    
    y = height - 155
    c.setFillColor(dark)
    c.setFont("Helvetica", 10)
    
    fields = [
        ("Imię i nazwisko:", employee.get('name', 'Jan Kowalski')),
        ("Stanowisko:", employee.get('position', 'Specjalista')),
        ("Dział:", employee.get('department', 'Sprzedaż')),
        ("Lokalizacja:", employee.get('location', 'Zamość')),
        ("Tel.:", employee.get('phone', '500 123 456')),
        ("E-mail:", employee.get('email', 'jan.kowalski@firma.pl')),
    ]
    
    for label, value in fields:
        c.setFillColor(gray)
        c.drawString(2*cm, y, label)
        c.setFillColor(dark)
        c.drawString(7*cm, y, value)
        y -= 15
    
    # Sekcja: Informacje o urlopie
    y -= 15
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "INFORMACJE O URLOPIE")
    c.setStrokeColor(light_gray)
    c.line(2*cm, y - 5, width - 2*cm, y - 5)
    
    y -= 25
    c.setFillColor(dark)
    c.setFont("Helvetica", 10)
    
    days_diff = (end_date - start_date).days + 1
    # Count business days
    from datetime import timedelta
    business_days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            business_days += 1
        current += timedelta(days=1)
    
    leave_info = [
        ("Rodzaj urlopu:", leave_type_name),
        ("Data od:", start_date.strftime('%d.%m.%Y')),
        ("Data do:", end_date.strftime('%d.%m.%Y')),
        ("Liczba dni kalendarzowych:", str(days_diff)),
        ("Liczba dni roboczych:", str(business_days)),
    ]
    
    for label, value in leave_info:
        c.setFillColor(gray)
        c.drawString(2*cm, y, label)
        c.setFillColor(dark)
        c.drawString(7*cm, y, value)
        y -= 15
    
    # Sekcja: Do wypełnienia
    y -= 15
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "DO WYPEŁNIENIA PRZEZ PRACOWNIKA")
    c.setStrokeColor(light_gray)
    c.line(2*cm, y - 5, width - 2*cm, y - 5)
    
    y -= 25
    c.setFillColor(dark)
    c.setFont("Helvetica", 10)
    
    # Fill-in fields
    fill_fields = [
        "Data od delegacji / spotkania:",
        "Środek transportu:",
        "Adres w czasie urlopu:",
        "Tel. w czasie urlopu:",
    ]
    
    for field in fill_fields:
        c.setFillColor(gray)
        c.drawString(2*cm, y, field)
        c.setStrokeColor(gray)
        c.line(7*cm, y - 2, width - 2*cm, y - 2)
        y -= 20
    
    # Uzasadnienie
    y -= 10
    c.setFillColor(gray)
    c.drawString(2*cm, y, "Uzasadnienie (opcjonalnie):")
    c.setStrokeColor(gray)
    c.rect(2*cm, y - 40, width - 4*cm, 35, fill=False, stroke=True)
    
    # Podpisy
    y -= 60
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "PODPISY I AKCEPTACJA")
    c.setStrokeColor(light_gray)
    c.line(2*cm, y - 5, width - 2*cm, y - 5)
    
    y -= 30
    c.setFillColor(dark)
    c.setFont("Helvetica", 10)
    
    # Podpis pracownika
    c.drawString(2*cm, y, "Pracownik:")
    c.line(3.5*cm, y - 2, 9*cm, y - 2)
    c.drawString(10*cm, y, "Data:")
    c.line(11*cm, y - 2, 15*cm, y - 2)
    
    y -= 25
    c.drawString(2*cm, y, "Bezpośredni przełożony:")
    c.line(5.5*cm, y - 2, 9*cm, y - 2)
    c.drawString(10*cm, y, "Data:")
    c.line(11*cm, y - 2, 15*cm, y - 2)
    
    y -= 25
    c.drawString(2*cm, y, "Dział HR / Kasa:")
    c.line(4.5*cm, y - 2, 9*cm, y - 2)
    c.drawString(10*cm, y, "Data:")
    c.line(11*cm, y - 2, 15*cm, y - 2)
    
    # Footer
    c.setFillColor(gray)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 1.5*cm, f"Wygenerowano przez Urlopnik v1.0 | ClawLabs / Infinity Tech | {employee.get('email', '')}")
    
    c.save()
    print(f"✅ PDF zapisany: {filename}")

if __name__ == "__main__":
    from datetime import datetime
    employee = {
        'name': 'Jan Kowalski',
        'position': 'Specjalista ds. Sprzedaży',
        'department': 'Dział Handlowy',
        'location': 'Zamość',
        'phone': '500 123 456',
        'email': 'jan.kowalski@firm.pl',
        'initials': 'JK',
    }
    
    generate_pdf(employee, datetime(2026, 7, 15).date(), datetime(2026, 7, 19).date(), "urlop wypoczynkowy")