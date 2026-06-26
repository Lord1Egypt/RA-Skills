# Sheet Agent

Transform natural language into spreadsheet comprehension, anomaly detection, business insights, and safe rewrite suggestions.

## Quick Start

```bash
# Install dependencies
pip install pandas openpyxl

# View spreadsheet info
python scripts/sheet_agent.py ~/Desktop/orders.csv

# Query overdue leads
python scripts/sheet_agent.py ~/Desktop/leads.csv "Which leads haven't been followed up for more than 3 days?"

# Check for anomalies
python scripts/sheet_agent.py ~/Desktop/inventory.xlsx "Check for any issues"

# Generate weekly report
python scripts/sheet_agent.py ~/Desktop/orders.csv "Generate last week's weekly report"

# Change preview (no write)
python scripts/sheet_agent.py ~/Desktop/customers.csv "Change the customer tier in row 8 to VIP"
```

## Run Tests

```bash
cd /Users/jianghaidong/.openclaw/skills/sheet-agent
python tests/test_sheet_agent.py
```

## Core Principles

- **Read-only by default**: Operations do not modify files by default
- **Preview before confirm**: Show diff before changing data; execute only on user confirmation
- **Backup before write**: Original file automatically backed up to `backup/` directory
- **Ask when uncertain**: If column meaning is unclear, proactively ask the user

## Directory Structure

```
sheet-agent/
├── SKILL.md              # Skill definition
├── skill.json            # Metadata
├── scripts/
│   └── sheet_agent.py    # Core logic (Python)
├── templates/            # Report templates
├── tests/
│   └── test_sheet_agent.py  # Test suite
├── backup/               # Auto backup directory
└── README.md
```

## Feature Checklist

| Feature | Status |
|---------|--------|
| CSV reading | ✅ |
| Excel reading | ✅ |
| Spreadsheet type inference | ✅ |
| Empty value detection | ✅ |
| Negative number detection | ✅ |
| Duplicate ID detection | ✅ |
| Date anomaly detection | ✅ |
| Large value anomaly detection | ✅ |
| Natural language query parsing | ✅ |
| Overdue lead queries | ✅ |
| Change preview | ✅ |
| Daily/weekly report generation | ✅ |
| Write execution (on confirm) | ✅ |
