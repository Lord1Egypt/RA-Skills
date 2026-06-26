# Configuration Reference

Full details for `expense-config.json`, located in the skill root directory.

---

## Structure

The config file contains three top-level sections:

### categories

Keyword-to-category mappings for auto-categorization. The script checks `vendor` name and `description` against these keywords (case-insensitive).

```json
{
  "categories": {
    "software": ["github", "aws", "azure", "google cloud", "saas"],
    "travel": ["airline", "hotel", "uber", "lyft", "ryanair", "aer lingus"],
    "office": ["amazon", "staples", "ikea", "keyboard", "monitor"],
    "food": ["restaurant", "coffee", "tesco", "supermarket"]
  }
}
```

Users can add new categories or keywords by editing this file. Suggest additions when a vendor doesn't match any existing category.

### defaults

Default values used when fields are missing from extracted data:

```json
{
  "defaults": {
    "currency": "EUR",
    "taxRate": 0.23,
    "dateFormat": "YYYY-MM-DD"
  }
}
```

### ledger

CSV file path and backup settings:

```json
{
  "ledger": {
    "csvPath": "expenses.csv",
    "backupCount": 5
  }
}
```

### xero

Settings for Xero export preset:

```json
{
  "xero": {
    "defaultAccountCode": "200",
    "defaultTaxRate": "23% (VAT on Expenses)"
  }
}
```

### freeagent

Settings for FreeAgent export preset:

```json
{
  "freeagent": {
    "claimantName": ""
  }
}
```

### exportPresets

Custom export format definitions. Each preset maps your ledger fields to a target CSV format:

```json
{
  "exportPresets": {
    "my-accounting": {
      "columns": ["date", "vendor", "amount"],
      "headerRow": true,
      "dateFormat": "%m/%d/%Y",
      "amountHandling": "positive",
      "fieldMapping": {
        "date": "date",
        "vendor": "vendor",
        "amount": "total"
      }
    }
  }
}
```

- `columns` — ordered list of CSV column headers
- `headerRow` — whether to include the header row in the output
- `dateFormat` — Python strftime format for date fields
- `amountHandling` — `positive` (keep as-is) or `negative` (prefix with minus sign for expenses)
- `fieldMapping` — maps each CSV column name to the corresponding ledger field name

---

## Custom Config

Use a custom config file with the `--config` flag:

```bash
python3 scripts/extract.py --config /path/to/config.json <command>
```

---

## View Current Categories

```bash
python3 scripts/extract.py categories
```
