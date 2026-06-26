# QR Code Standards

## QR Code Versions
- Version 1: 21x21 modules, 152 bits
- Version 40: 177x177 modules, 23,648 bits
- Auto-version: Let library choose based on data

## Error Correction Levels
| Level | Recovery | Use Case |
|-------|----------|----------|
| L | ~7% | Clean environment |
| M | ~15% | Default |
| Q | ~25% | Slightly dirty |
| H | ~30% | With logo overlay |

## Common QR Code Types
- URL: Direct link
- WiFi: `WIFI:S:ssid;T:WPA;P:pass;;`
- vCard: Contact information
- Email: `mailto:addr`
- Phone: `tel:number`
- SMS: `sms:number`

## Capacity (Version 1, M correction)
- Numeric: 34 characters
- Alphanumeric: 20 characters
- Binary: 14 bytes
