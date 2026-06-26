---
name: xlsx
version: 2.0.0
description: Create, read, edit Excel spreadsheets (.xlsx, .xlsm, .csv). Supports formulas, formatting, charts, pivot tables, and data analysis with pandas.
category: document-processing
license: MIT
---

# XLSX Skill v2.0

## Overview

Complete Excel spreadsheet processing using `openpyxl` for creation/editing and `pandas` for data analysis. Supports formulas, formatting, charts, and complex data operations.

## Installation & Dependencies

### Required
```bash
pip install pandas openpyxl xlsxwriter
```

### Optional
```bash
# For chart support
pip install numpy

# For PDF export
brew install --cask libreoffice
```

## Quick Start

### Read Excel File
```python
import pandas as pd

# Read first sheet
df = pd.read_excel('file.xlsx')

# Read specific sheet
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# Read all sheets
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)
```

### Create Excel File
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello'
ws['B1'] = 'World'
wb.save('output.xlsx')
```

### Add Formula
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 10
ws['A2'] = 20
ws['A3'] = '=SUM(A1:A2)'  # Excel formula
wb.save('formula.xlsx')
```

## Complete API Reference

### Reading Data with pandas

```python
import pandas as pd

# Basic read
df = pd.read_excel('data.xlsx')

# Read specific columns
df = pd.read_excel('data.xlsx', usecols=['A', 'B', 'C'])

# Read with header row
df = pd.read_excel('data.xlsx', header=0)

# Read without header
df = pd.read_excel('data.xlsx', header=None)

# Read specific rows
df = pd.read_excel('data.xlsx', skiprows=range(1, 10))  # Skip rows 1-9

# Read multiple sheets
sheets_dict = pd.read_excel('data.xlsx', sheet_name=None)
for sheet_name, df in sheets_dict.items():
    print(f"Sheet: {sheet_name}, Rows: {len(df)}")

# Data exploration
df.head()        # First 5 rows
df.tail()        # Last 5 rows
df.info()        # Column info
df.describe()    # Statistics
df.shape         # (rows, columns)
df.columns       # Column names
df.dtypes        # Data types
```

### Writing Data with pandas

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['NYC', 'LA', 'Chicago']
})

# Write to Excel
df.to_excel('output.xlsx', index=False)

# Write to specific sheet
df.to_excel('output.xlsx', sheet_name='Data', index=False)

# Write multiple sheets
with pd.ExcelWriter('multi-sheet.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
```

### Creating with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Fill, PatternFill, Border, Side, Alignment, Color
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Data"

# Write values
ws['A1'] = 'Header 1'
ws['B1'] = 'Header 2'
ws.append(['Row 1 Col 1', 'Row 1 Col 2'])
ws.append(['Row 2 Col 1', 'Row 2 Col 2'])

# Cell formatting
ws['A1'].font = Font(bold=True, size=14, color='FFFFFF')
ws['A1'].fill = PatternFill('solid', start_color='4472C4')
ws['A1'].alignment = Alignment(horizontal='center')

# Column width
ws.column_dimensions['A'].width = 20
ws.column_dimensions['B'].width = 15

# Row height
ws.row_dimensions[1].height = 25

# Merge cells
ws.merge_cells('A1:B1')

# Save
wb.save('formatted.xlsx')
```

### Formulas

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Basic formulas
ws['A1'] = 10
ws['A2'] = 20
ws['A3'] = '=SUM(A1:A2)'      # Sum
ws['A4'] = '=AVERAGE(A1:A2)'  # Average
ws['A5'] = '=MAX(A1:A2)'      # Maximum
ws['A6'] = '=MIN(A1:A2)'      # Minimum
ws['A7'] = '=COUNT(A1:A2)'    # Count numbers

# Cross-sheet references
wb.create_sheet('Sheet2')
ws2 = wb['Sheet2']
ws2['A1'] = '=Data!A1'  # Reference to Sheet1

# Save and recalculate
wb.save('formulas.xlsx')
```

### Charts

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference, LineChart, PieChart

wb = Workbook()
ws = wb.active

# Add data
data = [
    ['Category', 'Value'],
    ['A', 10],
    ['B', 15],
    ['C', 20],
    ['D', 25]
]
for row in data:
    ws.append(row)

# Create bar chart
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Sales Chart"
chart.y_axis.title = 'Value'
chart.x_axis.title = 'Category'

# Define data range
data_ref = Reference(ws, min_col=2, min_row=1, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)

chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats)
chart.shape = 4
ws.add_chart(chart, "E1")

wb.save('chart.xlsx')
```

### Tables

```python
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = Workbook()
ws = wb.active

# Add data
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'NYC'],
    ['Bob', 30, 'LA'],
    ['Charlie', 35, 'Chicago']
]
for row in data:
    ws.append(row)

# Create table
tab = Table(displayName="Table1", ref="A1:C4")
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True,
                       showColumnStripes=False)
tab.tableStyleInfo = style
ws.add_table(tab)

wb.save('table.xlsx')
```

### Conditional Formatting

```python
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import PatternFill

wb = Workbook()
ws = wb.active

# Add data
for i in range(1, 11):
    ws.cell(row=i, column=1, value=i * 10)

# Highlight cells greater than 50
red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
ws.conditional_formatting.add(
    'A1:A10',
    CellIsRule(operator='greaterThan', formula=['50'], fill=red_fill)
)

# Highlight even numbers with formula
green_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
ws.conditional_formatting.add(
    'A1:A10',
    FormulaRule(formula=['IS EVEN(A1)'], fill=green_fill)
)

wb.save('conditional.xlsx')
```

### Data Validation

```python
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active

# Dropdown list
dv = DataValidation(type="list", formula1='"Yes,No,Maybe'", allow_blank=True)
dv.error = "Please select from the list"
dv.errorTitle = "Invalid Selection"
ws.add_data_validation(dv)
dv.add('A1:A10')

# Number range
dv2 = DataValidation(type="whole", operator="between", formula1=["1", "100"])
dv2.error = "Enter a number between 1 and 100"
ws.add_data_validation(dv2)
dv2.add('B1:B10')

wb.save('validation.xlsx')
```

## Complete Examples

### Example 1: Financial Report

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Financial Report"

# Styles
header_font = Font(bold=True, size=12, color='FFFFFF')
header_fill = PatternFill('solid', start_color='4472C4')
border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
center_align = Alignment(horizontal='center')

# Headers
headers = ['Category', 'Q1', 'Q2', 'Q3', 'Q4', 'Total']
ws.append(headers)

# Style header row
for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.border = border
    cell.alignment = center_align

# Data (blue for inputs, black for formulas)
data = [
    ['Revenue', 100000, 120000, 115000, 130000],
    ['COGS', 40000, 48000, 46000, 52000],
    ['Gross Profit', '=B2-B3', '=C2-C3', '=D2-D3', '=E2-E3'],
    ['Expenses', 30000, 32000, 31000, 33000],
    ['Net Income', '=B4-B5', '=C4-C5', '=D4-D5', '=E4-E5']
]

for row in data:
    ws.append(row)

# Add Total formula for Q1 column
last_row = len(data) + 2
ws[f'B{last_row}'] = '=SUM(B2:B6)'

# Format as currency
for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=2, max_col=6):
    for cell in row:
        cell.number_format = '$#,##0'
        cell.border = border

# Column widths
ws.column_dimensions['A'].width = 15
for col in range(2, 7):
    ws.column_dimensions[get_column_letter(col)].width = 12

wb.save('financial-report.xlsx')
print("✓ Financial report created!")
```

### Example 2: Sales Dashboard with pandas

```python
import pandas as pd
import numpy as np

# Create sample sales data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')
products = ['Product A', 'Product B', 'Product C']
regions = ['North', 'South', 'East', 'West']

data = {
    'Date': np.random.choice(dates, 100),
    'Product': np.random.choice(products, 100),
    'Region': np.random.choice(regions, 100),
    'Units': np.random.randint(1, 100, 100),
    'Price': np.random.uniform(10, 100, 100)
}

df = pd.DataFrame(data)
df['Revenue'] = df['Units'] * df['Price']

# Analysis
summary = df.groupby('Product').agg({
    'Units': 'sum',
    'Revenue': 'sum'
}).round(2)

region_summary = df.groupby('Region').agg({
    'Units': 'sum',
    'Revenue': ['sum', 'mean']
}).round(2)

# Write to Excel with multiple sheets
with pd.ExcelWriter('sales-dashboard.xlsx', engine='openpyxl') as writer:
    # Raw data
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    
    # Product summary
    summary.to_excel(writer, sheet_name='Product Summary')
    
    # Region summary
    region_summary.to_excel(writer, sheet_name='Region Summary')
    
    # Pivot table
    pivot = pd.pivot_table(df, values='Revenue', index='Product', 
                          columns='Region', aggfunc='sum')
    pivot.to_excel(writer, sheet_name='Pivot Table')

print("✓ Sales dashboard created!")
```

### Example 3: Invoice Generator

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

def create_invoice(invoice_num, client_name, items, output_file):
    """
    items: list of dicts with 'description', 'quantity', 'unit_price'
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"
    
    # Styles
    title_font = Font(bold=True, size=18)
    header_font = Font(bold=True, size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Header
    ws['A1'] = "INVOICE"
    ws['A1'].font = title_font
    ws.merge_cells('A1:C1')
    
    # Invoice details
    ws['A3'] = f"Invoice #: {invoice_num}"
    ws['A4'] = f"Date: {datetime.now().strftime('%Y-%m-%d')}"
    ws['A6'] = f"Bill To: {client_name}"
    
    # Table headers
    headers = ['Description', 'Quantity', 'Unit Price', 'Amount']
    start_row = 8
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col, value=header)
        cell.font = header_font
        cell.border = border
    
    # Items
    row = start_row + 1
    for item in items:
        ws.cell(row=row, column=1, value=item['description'])
        ws.cell(row=row, column=2, value=item['quantity'])
        ws.cell(row=row, column=3, value=item['unit_price'])
        amount = item['quantity'] * item['unit_price']
        ws.cell(row=row, column=4, value=amount)
        
        for col in range(1, 5):
            ws.cell(row=row, column=col).border = border
        row += 1
    
    # Total row
    total_row = row
    ws.cell(row=total_row, column=3, value="Total:")
    ws.cell(row=total_row, column=3).font = Font(bold=True)
    total_formula = f"=SUM(D{start_row+1}:D{total_row-1})"
    ws.cell(row=total_row, column=4, value=total_formula)
    ws.cell(row=total_row, column=4).font = Font(bold=True)
    ws.cell(row=total_row, column=4).border = border
    
    # Column widths
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    
    wb.save(output_file)
    print(f"✓ Invoice created: {output_file}")

# Usage
items = [
    {'description': 'Web Development', 'quantity': 40, 'unit_price': 100},
    {'description': 'Design', 'quantity': 20, 'unit_price': 80},
    {'description': 'Consulting', 'quantity': 10, 'unit_price': 150}
]
create_invoice("INV-2024-001", "ABC Corporation", items, "invoice.xlsx")
```

### Example 4: Data Cleaning Pipeline

```python
import pandas as pd
from openpyxl import load_workbook

def clean_and_export(input_file, output_file):
    """Clean messy Excel data and export formatted version"""
    
    # Read raw data
    df = pd.read_excel(input_file)
    
    # Cleaning operations
    # 1. Remove duplicates
    df = df.drop_duplicates()
    
    # 2. Handle missing values
    df = df.fillna('N/A')
    
    # 3. Standardize text
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].str.strip().str.title()
    
    # 4. Remove invalid rows
    df = df[df['Status'] != 'Cancelled']  # Example filter
    
    # 5. Add calculated columns
    if 'Quantity' in df.columns and 'Price' in df.columns:
        df['Total'] = df['Quantity'] * df['Price']
    
    # Export with formatting
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        # Format the output
        wb = writer.book
        ws = writer.sheets['Cleaned Data']
        
        # Header formatting
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill('solid', start_color='4472C4')
            cell.font = Font(color='FFFFFF', bold=True)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✓ Cleaned data exported to {output_file}")
    return df

# Usage
# clean_and_export('raw_data.xlsx', 'cleaned_data.xlsx')
```

## Financial Modeling Best Practices

### Color Coding Standards

| Color | RGB | Meaning |
|-------|-----|---------|
| Blue | 0, 0, 255 | Hardcoded inputs |
| Black | 0, 0, 0 | Formulas |
| Green | 0, 128, 0 | Internal links |
| Red | 255, 0, 0 | External links |
| Yellow BG | 255, 255, 0 | Key assumptions |

### Implementation
```python
from openpyxl.styles import Font

# Blue for inputs
input_font = Font(color='0000FF')
ws['B2'].font = input_font  # Hardcoded value

# Black for formulas (default)
ws['B3'] = '=B2*1.1'  # Formula stays black

# Green for internal references
# (When linking between sheets)
ws['Sheet2!B2'] = '=Sheet1!B2'
```

### Number Formatting

```python
# Currency
ws['A1'].number_format = '$#,##0'

# Currency with thousands separator
ws['A2'].number_format = '$#,##0;($#,##0);-'

# Percentage with one decimal
ws['A3'].number_format = '0.0%'

# Date
ws['A4'].number_format = 'YYYY-MM-DD'

# Thousands with K suffix
ws['A5'].number_format = '#,##0,"K"'

# Millions with M suffix
ws['A6'].number_format = '#,##0,,"M"'
```

## Error Handling

### Common Errors

#### Error: "Formula not calculating"
```python
# Solution: Recalculate after saving
wb.save('file.xlsx')

# Then use LibreOffice to recalculate
# python scripts/recalc.py file.xlsx
```

#### Error: "Chart not displaying"
```python
# Solution: Ensure data range is correct
data_ref = Reference(ws, min_col=2, min_row=1, max_row=5)  # Check row numbers
```

#### Error: "File corrupted"
```python
# Solution: Use data_only=True when reading
wb = load_workbook('file.xlsx', data_only=True)
```

## Testing Your Setup

```python
# test-xlsx.py
import pandas as pd
from openpyxl import Workbook

print("Testing xlsx setup...")

# Test 1: pandas read/write
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df.to_excel('test-output.xlsx', index=False)
df_read = pd.read_excel('test-output.xlsx')
assert len(df_read) == 3
print("✓ pandas test passed")

# Test 2: openpyxl with formula
wb = Workbook()
ws = wb.active
ws['A1'] = 10
ws['A2'] = 20
ws['A3'] = '=SUM(A1:A2)'
wb.save('test-formula.xlsx')
print("✓ openpyxl test passed")

print("✓ All tests passed!")
```

Run test:
```bash
python test-xlsx.py
```

## License

MIT License - See LICENSE file for details.
