---
name: qr-generator
description: QR code generator. Use when user needs to create QR codes for text, URLs, WiFi, vCards, or any data. Supports custom colors, sizes, logos, and formats (PNG/SVG). 二维码生成、QR码制作。
version: 1.0.1
license: MIT-0
metadata: {"openclaw": {"emoji": "📱", "requires": {"bins": ["python3"]}}}
dependencies: "pip install qrcode pillow"
---

# QR Generator

Professional QR code generator with custom styling and multiple data formats.

## Features

- 📱 **Multiple Formats**: Text, URL, WiFi, vCard, Email, SMS
- 🎨 **Custom Styling**: Colors, size, error correction
- 🖼️ **Logo Embedding**: Add logo to center of QR code
- 📐 **Flexible Output**: PNG, SVG, PDF formats
- 🌍 **Multi-Language**: Supports all Unicode text
- ✅ **Cross-Platform**: Windows, macOS, Linux

## Supported QR Types

| Type | Use Case | Example |
|------|----------|---------|
| **Text** | Simple text | "Hello World" |
| **URL** | Website links | "https://example.com" |
| **WiFi** | Auto-connect | SSID + Password |
| **vCard** | Contact info | Name, Phone, Email |
| **Email** | Send email | mailto:user@example.com |
| **SMS** | Send SMS | sms:+1234567890 |
| **Phone** | Call number | tel:+1234567890 |
| **Geo** | Location | geo:lat,lng |

## Trigger Conditions

- "生成二维码" / "Generate QR code"
- "创建二维码" / "Create QR code"
- "WiFi二维码" / "WiFi QR code"
- "名片二维码" / "vCard QR code"
- "qr-generator"

---

## Step 1: Understand Requirements

```
请提供以下信息：

内容类型：（文本/URL/WiFi/名片/其他）
具体内容：
输出格式：（PNG/SVG）
尺寸要求：（小/中/大/自定义）
颜色要求：（默认/自定义）
是否需要Logo：
```

---

## Step 2: Generate QR Code

### Python Script Template

```python
python3 << 'PYEOF'
import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask
)
from PIL import Image

class QRGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
    
    def generate_text(self, text, output_path, **kwargs):
        """Generate QR code for text"""
        return self._generate(text, output_path, **kwargs)
    
    def generate_url(self, url, output_path, **kwargs):
        """Generate QR code for URL"""
        return self._generate(url, output_path, **kwargs)
    
    def generate_wifi(self, ssid, password, security='WPA', output_path=None, **kwargs):
        """Generate QR code for WiFi"""
        wifi_string = f'WIFI:T:{security};S:{ssid};P:{password};;'
        return self._generate(wifi_string, output_path, **kwargs)
    
    def generate_vcard(self, name, phone='', email='', org='', output_path=None, **kwargs):
        """Generate QR code for vCard"""
        vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{name}
FN:{name}
TEL:{phone}
EMAIL:{email}
ORG:{org}
END:VCARD"""
        return self._generate(vcard, output_path, **kwargs)
    
    def generate_email(self, email, subject='', body='', output_path=None, **kwargs):
        """Generate QR code for email"""
        mailto = f'mailto:{email}'
        if subject or body:
            mailto += '?'
            params = []
            if subject:
                params.append(f'subject={subject}')
            if body:
                params.append(f'body={body}')
            mailto += '&'.join(params)
        return self._generate(mailto, output_path, **kwargs)
    
    def generate_phone(self, phone, output_path=None, **kwargs):
        """Generate QR code for phone call"""
        return self._generate(f'tel:{phone}', output_path, **kwargs)
    
    def generate_sms(self, phone, message='', output_path=None, **kwargs):
        """Generate QR code for SMS"""
        sms = f'sms:{phone}'
        if message:
            sms += f'?body={message}'
        return self._generate(sms, output_path, **kwargs)
    
    def _generate(self, data, output_path, 
                  fill_color='black', 
                  back_color='white',
                  size=10,
                  style='square',
                  logo_path=None):
        """Generate QR code with options"""
        
        # Reset QR code
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        # Set colors
        if isinstance(fill_color, str):
            fill_color = self._hex_to_rgb(fill_color)
        if isinstance(back_color, str):
            back_color = self._hex_to_rgb(back_color)
        
        # Choose module drawer
        drawers = {
            'square': SquareModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer()
        }
        drawer = drawers.get(style, SquareModuleDrawer())
        
        # Generate image
        img = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=fill_color
            )
        )
        
        # Convert to PIL Image
        img = img.convert('RGBA')
        
        # Resize if needed
        if size != 10:
            new_size = img.size[0] * size // 10
            img = img.resize((new_size, new_size), Image.LANCZOS)
        
        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            img = self._add_logo(img, logo_path)
        
        # Save
        img.save(output_path)
        return output_path
    
    def _add_logo(self, qr_img, logo_path, logo_size_ratio=0.2):
        """Add logo to center of QR code"""
        logo = Image.open(logo_path).convert('RGBA')
        
        # Calculate logo size
        qr_width, qr_height = qr_img.size
        logo_size = int(min(qr_width, qr_height) * logo_size_ratio)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # Calculate position
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Create white background for logo
        logo_bg = Image.new('RGBA', (logo_size + 10, logo_size + 10), (255, 255, 255, 255))
        bg_pos = ((qr_width - logo_size - 10) // 2, (qr_height - logo_size - 10) // 2)
        
        # Paste
        qr_img.paste(logo_bg, bg_pos)
        qr_img.paste(logo, logo_pos, logo)
        
        return qr_img
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Example usage
generator = QRGenerator()

output_dir = os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())

# Text QR
generator.generate_text(
    'Hello World!',
    os.path.join(output_dir, 'qr_text.png')
)

# URL QR
generator.generate_url(
    'https://github.com',
    os.path.join(output_dir, 'qr_url.png'),
    fill_color='#1a365d'
)

# WiFi QR
generator.generate_wifi(
    ssid='MyWiFi',
    password='password123',
    output_path=os.path.join(output_dir, 'qr_wifi.png'),
    fill_color='#3182ce'
)

# vCard QR
generator.generate_vcard(
    name='John Doe',
    phone='+1234567890',
    email='john@example.com',
    org='Example Corp',
    output_path=os.path.join(output_dir, 'qr_vcard.png')
)

print(f"✅ QR codes generated in: {output_dir}")
PYEOF
```

---

## QR Code Types (二维码类型)

### WiFi QR Code

```python
# Format: WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;

# WPA/WPA2
WIFI:T:WPA;S:MyNetwork;P:MyPassword;;

# WEP
WIFI:T:WEP;S:MyNetwork;P:MyPassword;;

# No password
WIFI:T:nopass;S:MyNetwork;;
```

### vCard QR Code

```python
# Format: vCard 3.0
BEGIN:VCARD
VERSION:3.0
N:Lastname;Firstname
FN:Firstname Lastname
TEL:+1234567890
EMAIL:email@example.com
ORG:Company Name
TITLE:Job Title
URL:https://example.com
ADR:;;Street;City;State;Zip;Country
END:VCARD
```

### Email QR Code

```python
# Format: mailto:{email}?subject={subject}&body={body}
mailto:contact@example.com?subject=Hello&body=Message
```

---

## Styling Options (样式选项)

### Colors

```python
# Solid colors
fill_color='#000000'  # Black
fill_color='#1a365d'  # Dark blue
fill_color='#3182ce'  # Blue

# Gradients (advanced)
color_mask=RadialGradiantColorMask(
    back_color=(255, 255, 255),
    center_color=(0, 0, 0),
    edge_color=(100, 100, 100)
)
```

### Module Styles

```python
# Square (default)
style='square'

# Circle
style='circle'

# Rounded
style='rounded'
```

### Sizes

```python
# Small (for mobile)
size=5

# Medium (default)
size=10

# Large (for print)
size=20

# Custom pixels
box_size=15  # Each module = 15 pixels
```

---

## Security Notes

- ✅ No network calls or external endpoints
- ✅ No credentials or API keys required
- ✅ Local file processing only
- ✅ Open source dependencies (qrcode, pillow)
- ✅ No data uploaded to external servers

---

## Notes

- QR codes support up to 4,296 alphanumeric characters
- Error correction levels: L(7%), M(15%), Q(25%), H(30%)
- Higher error correction = more reliable but larger size
- Logo embedding reduces error correction capacity
