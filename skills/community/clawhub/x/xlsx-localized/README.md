# XLSX Skill (Localized)

Professional Excel (.xlsx) creation, editing, and analysis skill for WorkBuddy.

Localized from [Anthropic official xlsx skill](https://github.com/anthropics/skills/tree/main/skills/xlsx), adapted for Windows environment.

## Features

- **Read & Analyze**: pandas-powered data analysis and visualization
- **Create**: Build formatted spreadsheets with openpyxl (styles, formulas, charts)
- **Edit**: Modify existing .xlsx files while preserving formulas and formatting
- **Formula Engine**: Enforces Excel native formulas over Python hardcoding
- **Formula Recalculation**: LibreOffice-powered formula recalculation with error detection
- **Financial Model Standards**: Industry-standard color coding (blue=inputs, black=formulas, green=cross-sheet, red=external)
- **Number Formatting**: Professional currency (¥/$), percentage, multiple, and date formats
- **Formula QA**: Automatic scanning for #REF!, #DIV/0!, #VALUE!, #NAME?, #NULL!, #NUM!, #N/A errors

## File Structure

```
xlsx/
├── SKILL.md              # Skill metadata & full workflow guide
├── README.md             # This file
└── scripts/
    ├── recalc.py         # Formula recalculation via LibreOffice
    └── office/
        ├── __init__.py   # Package init
        └── soffice.py    # LibreOffice runner (Windows-compatible)
```

## Dependencies

### Required Python Packages
- `openpyxl` - reading/writing .xlsx with formula and formatting support
- `pandas` - data analysis and bulk operations
- `xlrd` - reading older .xls files (optional)

### External
- **LibreOffice** - required for formula recalculation
  - Download: https://www.libreoffice.org/download/download-libreoffice/
  - Or set `SOFFICE_PATH` environment variable

## Usage

```python
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create new spreadsheet
wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Revenue'
sheet['B1'] = 1000000
sheet['B2'] = '=SUM(B1:B10)'

# Format
sheet['A1'].font = Font(bold=True)
sheet.column_dimensions['A'].width = 20
wb.save('output.xlsx')
```

```bash
# Recalculate formulas after save
python scripts/recalc.py output.xlsx
```

## Windows Localization Notes

- Removed Linux-only AF_UNIX socket shim (LD_PRELOAD)
- Added Windows LibreOffice path detection (Program Files)
- Added SOFFICE_PATH environment variable support
- Currency defaults changed to CNY (¥)
- Macro directory uses %APPDATA% on Windows

## Author

yinfeihaaaaaaaaaaa

## License

MIT-0
