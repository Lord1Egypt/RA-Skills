# Barcode Types Reference

## Supported Barcode Types

| Type | Data Length | Use Case |
|------|-------------|----------|
| Code128 | Variable | General purpose |
| EAN-13 | 13 digits | Global retail |
| EAN-8 | 8 digits | Small packages |
| UPC-A | 12 digits | North America retail |
| Code39 | Variable | Industrial |
| ITF | Variable | Packaging |
| Codabar | Variable | Libraries, blood banks |

## EAN-13 Checksum
Last digit is calculated from first 12 digits using modulo 10 algorithm.

## Code128 Character Sets
- Set A: Uppercase + control chars
- Set B: Upper + lowercase
- Set C: Numeric pairs (density)
