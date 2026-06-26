import os
import io
import re
import json
import base64
from typing import Union, Optional, Dict, List, Any

_MISSING_DEPENDENCIES = []

try:
    from PIL import Image
except ImportError:
    _MISSING_DEPENDENCIES.append("Pillow")

try:
    import qrcode
except ImportError:
    _MISSING_DEPENDENCIES.append("qrcode")

try:
    from pyzbar import pyzbar
except ImportError:
    _MISSING_DEPENDENCIES.append("pyzbar")

try:
    import urllib.request
    from urllib.parse import urlparse
except ImportError:
    pass


def check_dependencies() -> None:
    if _MISSING_DEPENDENCIES:
        missing = ", ".join(_MISSING_DEPENDENCIES)
        raise ImportError(
            f"Missing required dependencies: {missing}\n"
            f"Please install them with: pip install {' '.join(_MISSING_DEPENDENCIES)}"
        )


def _is_url(text: str) -> bool:
    try:
        result = urlparse(text)
        return result.scheme in ('http', 'https')
    except Exception:
        return False


def _is_base64(text: str) -> bool:
    if text.startswith('data:image'):
        return True
    try:
        if re.match(r'^[A-Za-z0-9+/]+=*$', text):
            base64.b64decode(text, validate=True)
            return True
    except Exception:
        pass
    return False


def _extract_base64(text: str) -> bytes:
    if text.startswith('data:image'):
        base64_data = text.split(',', 1)[1]
    else:
        base64_data = text
    return base64.b64decode(base64_data)


class QRCodeScanner:
    def __init__(self):
        check_dependencies()
    
    def scan_from_file(self, file_path: str, format_json: bool = False) -> Union[str, List[str], Dict]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with Image.open(file_path) as img:
            return self._scan_image(img, format_json)
    
    def scan_from_url(self, url: str, format_json: bool = False) -> Union[str, List[str], Dict]:
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
            img = Image.open(io.BytesIO(data))
            return self._scan_image(img, format_json)
        except Exception as e:
            raise ValueError(f"Failed to fetch image from URL: {e}")
    
    def scan_from_base64(self, base64_data: str, format_json: bool = False) -> Union[str, List[str], Dict]:
        try:
            data = _extract_base64(base64_data)
            img = Image.open(io.BytesIO(data))
            return self._scan_image(img, format_json)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 image: {e}")
    
    def scan_from_bytes(self, data: bytes, format_json: bool = False) -> Union[str, List[str], Dict]:
        img = Image.open(io.BytesIO(data))
        return self._scan_image(img, format_json)
    
    def _scan_image(self, img: 'Image.Image', format_json: bool = False) -> Union[str, List[str], Dict]:
        decoded_objects = pyzbar.decode(img)
        
        if not decoded_objects:
            raise ValueError("No QR code found in the image")
        
        results = [obj.data.decode('utf-8', errors='ignore') for obj in decoded_objects]
        
        if format_json:
            if len(results) == 1:
                return {
                    "success": True,
                    "count": 1,
                    "data": results[0],
                    "type": self._detect_qr_type(results[0])
                }
            return {
                "success": True,
                "count": len(results),
                "data": results,
                "types": [self._detect_qr_type(r) for r in results]
            }
        
        return results[0] if len(results) == 1 else results
    
    def _detect_qr_type(self, content: str) -> str:
        if content.startswith('WIFI:'):
            return 'wifi'
        elif content.startswith(('http://', 'https://')):
            return 'url'
        else:
            return 'text'


class QRCodeGenerator:
    def __init__(self, default_size: int = 10, default_border: int = 4):
        check_dependencies()
        self.default_size = default_size
        self.default_border = default_border
    
    def generate(
        self,
        content: str,
        output_path: Optional[str] = None,
        size: Optional[int] = None,
        border: Optional[int] = None
    ) -> Optional[str]:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=size or self.default_size,
            border=border or self.default_border,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if output_path:
            img.save(output_path)
            return None
        else:
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode('utf-8')
    
    def generate_url(
        self,
        url: str,
        output_path: Optional[str] = None,
        size: Optional[int] = None,
        border: Optional[int] = None
    ) -> Optional[str]:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return self.generate(url, output_path, size, border)
    
    def generate_wifi(
        self,
        ssid: str,
        password: str,
        security: str = 'WPA',
        output_path: Optional[str] = None,
        hidden: bool = False,
        size: Optional[int] = None,
        border: Optional[int] = None
    ) -> Optional[str]:
        security = security.upper()
        if security not in ('WPA', 'WEP', 'NONE'):
            raise ValueError(f"Invalid security type: {security}. Must be WPA, WEP, or NONE")
        
        escaped_ssid = self._escape_wifi_value(ssid)
        escaped_password = self._escape_wifi_value(password)
        
        wifi_string = f"WIFI:T:{security};S:{escaped_ssid};P:{escaped_password};"
        if hidden:
            wifi_string += "H:true;"
        wifi_string += ";"
        
        return self.generate(wifi_string, output_path, size, border)
    
    def _escape_wifi_value(self, value: str) -> str:
        value = value.replace('\\', '\\\\')
        value = value.replace(';', '\\;')
        value = value.replace(',', '\\,')
        value = value.replace(':', '\\:')
        return value


_scanner: Optional[QRCodeScanner] = None
_generator: Optional[QRCodeGenerator] = None


def get_scanner() -> QRCodeScanner:
    global _scanner
    if _scanner is None:
        _scanner = QRCodeScanner()
    return _scanner


def get_generator(default_size: int = 10, default_border: int = 4) -> QRCodeGenerator:
    global _generator
    if _generator is None:
        _generator = QRCodeGenerator(default_size, default_border)
    return _generator


def scan_qrcode(
    input_data: Union[str, bytes],
    input_type: Optional[str] = None,
    format_json: bool = False
) -> Union[str, List[str], Dict]:
    scanner = get_scanner()
    
    if isinstance(input_data, bytes):
        return scanner.scan_from_bytes(input_data, format_json)
    
    if input_type == 'file':
        return scanner.scan_from_file(input_data, format_json)
    elif input_type == 'url':
        return scanner.scan_from_url(input_data, format_json)
    elif input_type == 'base64':
        return scanner.scan_from_base64(input_data, format_json)
    
    if _is_url(input_data):
        return scanner.scan_from_url(input_data, format_json)
    elif _is_base64(input_data):
        return scanner.scan_from_base64(input_data, format_json)
    else:
        return scanner.scan_from_file(input_data, format_json)


def generate_qrcode(
    content: str,
    output_path: Optional[str] = None,
    qr_type: str = 'text',
    size: int = 10,
    border: int = 4
) -> Optional[str]:
    generator = get_generator(size, border)
    
    if qr_type == 'url':
        return generator.generate_url(content, output_path, size, border)
    else:
        return generator.generate(content, output_path, size, border)


def generate_wifi_qrcode(
    ssid: str,
    password: str,
    security: str = 'WPA',
    output_path: Optional[str] = None,
    hidden: bool = False,
    size: int = 10,
    border: int = 4
) -> Optional[str]:
    generator = get_generator(size, border)
    return generator.generate_wifi(ssid, password, security, output_path, hidden, size, border)


def parse_wifi_qrcode(content: str) -> Optional[Dict[str, str]]:
    if not content.startswith('WIFI:'):
        return None
    
    result = {'ssid': '', 'password': '', 'security': 'WPA', 'hidden': False}
    
    content = content[5:]
    if content.endswith(';;'):
        content = content[:-2]
    
    parts = content.split(';')
    
    for part in parts:
        if not part:
            continue
        
        if ':' not in part:
            continue
        
        key, value = part.split(':', 1)
        key = key.upper()
        value = _unescape_wifi_value(value)
        
        if key == 'T':
            result['security'] = value
        elif key == 'S':
            result['ssid'] = value
        elif key == 'P':
            result['password'] = value
        elif key == 'H':
            result['hidden'] = value.lower() == 'true'
    
    return result


def _unescape_wifi_value(value: str) -> str:
    value = value.replace('\\:', ':')
    value = value.replace('\\,', ',')
    value = value.replace('\\;', ';')
    value = value.replace('\\\\', '\\')
    return value


if __name__ == "__main__":
    import sys
    
    try:
        check_dependencies()
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("QR Code Scanner & Generator")
        print("")
        print("Usage:")
        print("  Scan QR code:")
        print("    python main.py scan <input> [--format json]")
        print("    input: image file path, URL, or base64 data")
        print("")
        print("  Generate QR code:")
        print("    python main.py generate <content> [--output path] [--type text|url]")
        print("")
        print("  Generate WiFi QR code:")
        print("    python main.py wifi --ssid <SSID> --password <PASSWORD> [--security WPA|WEP|NONE] [--output path]")
        print("")
        print("Examples:")
        print("  python main.py scan qrcode.png")
        print("  python main.py scan https://example.com/qr.png --format json")
        print("  python main.py generate \"Hello World\" --output output.png")
        print("  python main.py generate https://github.com --type url --output url_qr.png")
        print("  python main.py wifi --ssid MyWiFi --password mypassword --output wifi.png")
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    try:
        if command == 'scan':
            if len(sys.argv) < 3:
                print("Error: Missing input for scan command")
                sys.exit(1)
            
            input_data = sys.argv[2]
            format_json = '--format' in sys.argv
            
            result = scan_qrcode(input_data, format_json=format_json)
            
            if isinstance(result, dict):
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Result: {result}")
        
        elif command == 'generate':
            if len(sys.argv) < 3:
                print("Error: Missing content for generate command")
                sys.exit(1)
            
            content = sys.argv[2]
            output_path = None
            qr_type = 'text'
            
            for i, arg in enumerate(sys.argv[3:], 3):
                if arg == '--output' and i + 1 < len(sys.argv):
                    output_path = sys.argv[i + 1]
                elif arg == '--type' and i + 1 < len(sys.argv):
                    qr_type = sys.argv[i + 1]
            
            result = generate_qrcode(content, output_path=output_path, qr_type=qr_type)
            
            if output_path:
                print(f"QR code saved to: {output_path}")
            else:
                print(f"Base64 QR code: {result[:100]}..." if len(result) > 100 else f"Base64 QR code: {result}")
        
        elif command == 'wifi':
            ssid = None
            password = None
            security = 'WPA'
            output_path = None
            
            i = 2
            while i < len(sys.argv):
                arg = sys.argv[i]
                if arg == '--ssid' and i + 1 < len(sys.argv):
                    ssid = sys.argv[i + 1]
                    i += 2
                elif arg == '--password' and i + 1 < len(sys.argv):
                    password = sys.argv[i + 1]
                    i += 2
                elif arg == '--security' and i + 1 < len(sys.argv):
                    security = sys.argv[i + 1]
                    i += 2
                elif arg == '--output' and i + 1 < len(sys.argv):
                    output_path = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1
            
            if not ssid or not password:
                print("Error: --ssid and --password are required for WiFi QR code")
                sys.exit(1)
            
            result = generate_wifi_qrcode(ssid, password, security, output_path)
            
            if output_path:
                print(f"WiFi QR code saved to: {output_path}")
            else:
                print(f"Base64 WiFi QR code: {result[:100]}..." if len(result) > 100 else f"Base64 WiFi QR code: {result}")
        
        else:
            print(f"Error: Unknown command '{command}'")
            print("Available commands: scan, generate, wifi")
            sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
