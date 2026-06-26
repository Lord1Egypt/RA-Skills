---
name: qr-code-generator
description: Generate QR codes for URLs, text, WiFi credentials, contact cards, and more. Use when creating scannable links for marketing materials, sharing WiFi passwords, generating business cards, or creating quick access to digital content. Supports custom styling, error correction levels, and multiple export formats.
---

# QR Code Generator

Create QR codes for URLs, WiFi, contacts, and more.

## When to Use

- Creating scannable links for print materials
- Sharing WiFi credentials securely
- Generating digital business cards
- Creating quick app download links
- Sharing locations or maps
- Event check-in codes

## Quick Start

### Basic URL QR Code

```python
import qrcode

def generate_qr(data, output_path='qr_code.png'):
    """Generate simple QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path

# Usage
generate_qr('https://example.com', 'website_qr.png')
```

### WiFi QR Code

```python
def generate_wifi_qr(ssid, password, security='WPA', output='wifi_qr.png'):
    """
    Generate WiFi connection QR code
    Format: WIFI:S:ssid;T:security;P:password;;
    """
    wifi_string = f"WIFI:S:{ssid};T:{security};P:{password};;"
    return generate_qr(wifi_string, output)

# Usage
generate_wifi_qr('MyHomeNetwork', 'secret123', 'WPA')
# Scan to auto-connect to WiFi
```

### Contact Card (vCard)

```python
def generate_vcard_qr(name, phone, email, output='contact_qr.png'):
    """Generate vCard QR code"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}
END:VCARD"""
    return generate_qr(vcard, output)

# Usage
generate_vcard_qr('John Doe', '+1234567890', 'john@example.com')
```

### Styled QR Code

```python
def generate_styled_qr(data, output='styled_qr.png', **kwargs):
    """Generate QR with custom styling"""
    qr = qrcode.QRCode(
        version=kwargs.get('version', 1),
        error_correction=getattr(
            qrcode.constants, 
            f"ERROR_CORRECT_{kwargs.get('error_correction', 'M')}"
        ),
        box_size=kwargs.get('box_size', 10),
        border=kwargs.get('border', 4),
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Custom colors
    fill_color = kwargs.get('fill_color', 'black')
    back_color = kwargs.get('back_color', 'white')
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output)
    return output

# Styled examples
generate_styled_qr('https://mysite.com', 'blue_qr.png', 
                   fill_color='blue', back_color='lightblue')
```

## Error Correction Levels

| Level | Correction | Use Case |
|-------|-----------|----------|
| L | ~7% | Clean environments |
| M | ~15% | Default, good balance |
| Q | ~25% | Dirty/damaged possible |
| H | ~30% | Logos/overlays on QR |

## Advanced Features

### Batch Generate

```python
def batch_generate(urls, output_dir='./qr_codes'):
    """Generate QR codes for multiple URLs"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    generated = []
    for i, url in enumerate(urls, 1):
        output = f"{output_dir}/qr_{i:03d}.png"
        generate_qr(url, output)
        generated.append(output)
    
    return generated

# Usage
urls = [
    'https://product1.com',
    'https://product2.com',
    'https://product3.com'
]
batch_generate(urls)
```

### Add Logo to Center

```python
from PIL import Image

def add_logo_to_qr(qr_path, logo_path, output_path):
    """Add logo to center of QR code"""
    qr_img = Image.open(qr_path)
    logo_img = Image.open(logo_path)
    
    # Resize logo to fit in center
    box_size = min(qr_img.size) // 5
    logo_img = logo_img.resize((box_size, box_size))
    
    # Calculate position
    pos = ((qr_img.size[0] - box_size) // 2,
           (qr_img.size[1] - box_size) // 2)
    
    # Paste logo
    qr_img.paste(logo_img, pos, logo_img if logo_img.mode == 'RGBA' else None)
    qr_img.save(output_path)
```

## Dependencies

```bash
pip install qrcode[pil]
```
