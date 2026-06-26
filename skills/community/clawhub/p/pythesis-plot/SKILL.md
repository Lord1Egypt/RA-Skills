---
name: pythesis-plot
description: >
  Python scientific plotting tool for thesis/dissertation scenarios.
  Workflow: data upload → analysis → recommendations → confirmation → generation.
  Triggers when users upload data files (CSV/Excel/TXT) and ask for plots,
  charts, figures, or data visualization for academic publications.
---

# PyThesisPlot

Python scientific plotting workflow tool supporting the complete process from data upload to figure generation for academic publications.

## Workflow

```
[User Uploads Data] → [Auto-save to output dir] → [Data Analysis]
                                           ↓
[Generate Images to output dir] ← [Code Generation] ← [User Confirms Scheme]
```

### Required Steps

1. **Data Reception**: User uploads data file (txt/md/xlsx/csv)
2. **Auto-save**: Rename to `timestamp-original_filename`, save to `output/YYYYMMDD-filename/`
3. **Data Analysis**: Analyze dimensions, types, statistical features, column relationships
4. **Chart Recommendations**: Recommend chart schemes based on data characteristics (type, quantity, layout)
5. **User Confirmation**: Display analysis report, **must wait for user confirmation before generation**
6. **Generation & Delivery**: Python code + chart images, save to same output directory

## Core Scripts

### 1. Main Workflow Script

```bash
python scripts/workflow.py --input data.csv --output-dir output/
```

### 2. Data Analysis

```bash
python scripts/data_analyzer.py --input data.csv
```

Output: Data characteristics report + chart recommendation scheme

### 3. Chart Generation

```bash
python scripts/plot_generator.py --config plot_config.json --output-dir output/
```

## File Management Standards

### Directory Structure

```
output/
└── 20250312-145230-data.csv/          # Named with timestamp + filename
    ├── 20250312-145230-data.csv       # Original data file (renamed)
    ├── analysis_report.md             # Data analysis report
    ├── plot_config.json               # Chart configuration (generated after user confirmation)
    ├── 20250312-145230_plot.py        # Generated Python code
    ├── 20250312-145230_fig1_line.png  # Chart (PNG image)
    └── 20250312-145230_fig2_bar.png
```

### Naming Conventions

| File Type | Naming Format | Example |
|---------|---------|------|
| Data File | `{timestamp}-{original}` | `20250312-145230-data.csv` |
| Analysis Report | `analysis_report.md` | `analysis_report.md` |
| Python Code | `{timestamp}_plot.py` | `20250312-145230_plot.py` |
| Chart PNG | `{timestamp}_fig{n}_{type}.png` | `20250312-145230_fig1_line.png` |

## Usage

### Scenario 1: Complete Workflow

When user uploads a data file:

1. **Auto-save File**
   ```python
   # Rename and save to output/{timestamp}-{filename}/
   save_uploaded_file(input_file, output_base="output/")
   ```

2. **Execute Data Analysis**
   ```python
   # Analyze data characteristics, generate report
   python scripts/data_analyzer.py --input output/20250312-data/data.csv
   ```

3. **Display Analysis Report to User**
   ```markdown
   ## Data Analysis Report
   
   ### Data Overview
   - File: data.csv
   - Dimensions: 120 rows × 5 columns
   - Types: 3 numeric + 2 categorical columns
   
   ### Column Details
   | Column | Type | Description |
   |-----|------|-----|
   | date | datetime | 2023-01 to 2023-12 |
   | sales | numeric | mean=1250, std=320 |
   | region | categorical | 4 categories: N/S/E/W |
   
   ### Chart Recommendations
   Based on data characteristics, the following schemes are recommended:
   
   **Scheme 1: Time Trend Analysis** ⭐Recommended
   - Chart Type: Line plot
   - Content: Sales trend over time
   - Reason: Time series data, most intuitive for showing trends
   
   **Scheme 2: Regional Comparison**
   - Chart Type: Grouped bar chart
   - Content: Sales comparison across regions
   - Reason: Categorical comparison, suitable for showing differences
   
   **Scheme 3: Comprehensive Dashboard**
   - Chart Type: 2×2 subplot layout
   - Includes: Trend line + Bar chart + Box plot + Correlation heatmap
   - Reason: Rich data dimensions, comprehensive display
   
   Please tell me what you want:
   - "Generate schemes 1 and 2"
   - "Generate all"
   - "Modify scheme 3..." (provide your modification suggestions)
   ```

4. **Wait for User Confirmation** ⚠️ **Critical Step**
   - User may say: "Generate scheme 1" / "Generate all" / "Modify XX..."
   - **Must wait for explicit instruction before entering generation phase**

5. **Generate and Save**
   ```python
   # Generate Python code
   python scripts/plot_generator.py --config plot_config.json
   
   # Output to same directory
   output/20250312-data/
   ├── 20250312-145230_plot.py        # Code
   ├── 20250312-145230_fig1_line.png  # Chart
   └── 20250312-145230_fig2_bar.png
   ```

### Scenario 2: Data Analysis Only

```bash
python scripts/data_analyzer.py --input data.csv --output report.md
```

### Scenario 3: Generate from Config

```bash
python scripts/plot_generator.py --config config.json --output-dir ./
```

## Chart Recommendation Logic

| Data Characteristics | Recommended Chart | Application |
|---------|---------|---------|
| Time series + Numeric | Line plot | Trend display |
| Categorical + Single numeric | Bar chart | Category comparison |
| Categorical + Distribution | Box/Violin plot | Distribution display |
| Two numeric (correlated) | Scatter (+regression) | Correlation analysis |
| Multiple numeric (correlated) | Heatmap | Correlation matrix |
| Single numeric distribution | Histogram/Density | Distribution characteristics |
| Multi-dimensional rich data | 2×2 subplots | Comprehensive display |

## Supported File Formats

- **CSV**: `.csv` (Recommended)
- **Excel**: `.xlsx`, `.xls`
- **Text**: `.txt`, `.md` (table format)

## Dependencies

```
pandas >= 1.3.0
matplotlib >= 3.5.0
seaborn >= 0.11.0
openpyxl >= 3.0.0  # Excel support
numpy >= 1.20.0
scipy >= 1.7.0
```

## Reference Documents

- [Workflow Guide](references/workflow_guide.md) - Complete workflow instructions
- [Chart Types](references/chart_types.md) - Detailed chart type descriptions
- [Style Guide](references/style_guide.md) - Color schemes, fonts, size standards
- [Examples](references/examples.md) - Complete code examples

## Important Notes

1. **User confirmation is mandatory**: Must wait for user confirmation after analysis, cannot generate directly
2. **Unified file management**: All output files saved to same output/{timestamp}-{filename}/ directory
3. **High-resolution output**: Generate PNG at 300 DPI (suitable for publication)
4. **Code traceability**: Generated Python code also saved to same directory for user modification
5. **Academic style**: Charts follow top journal standards (Nature/Science/Lancet style)
