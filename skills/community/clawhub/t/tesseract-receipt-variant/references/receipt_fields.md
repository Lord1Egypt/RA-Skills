# Receipt Extraction Fields

## Core Fields
- date: Transaction date
- vendor: Merchant/store name
- total: Final amount
- tax: Sales tax amount
- items: List of purchased items

## Receipt Specific
- mileage: Odometer or km (for mileage/travel)
- category: expense category
- notes: Additional info

## Example JSON
```json
{
  "date": "03/28/2026",
  "vendor": "Gas Station",
  "total": "45.67",
  "category": "receipt"
}
```
