# Workflow Guide

PyThesisPlot adopts a complete four-stage workflow: Data Analysis → Chart Recommendations → User Confirmation → Generation.

## Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 1: Data Reception                      │
├─────────────────────────────────────────────────────────────────┤
│  1. User uploads data file (csv/xlsx/txt/md)                   │
│  2. Generate timestamp: YYYYMMDD-HHMMSS                         │
│  3. Rename file: {timestamp}-{original_filename}                │
│  4. Create directory: output/{timestamp}-{filename}/            │
│  5. Save file to working directory                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 2: Data Analysis                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Read data file                                              │
│  2. Analyze data dimensions (rows, columns)                     │
│  3. Analyze column types (numeric/categorical/datetime)         │
│  4. Statistical feature analysis (mean, std, distribution)      │
│  5. Column relationship analysis (correlations)                 │
│  6. Generate analysis_report.md                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 3: Chart Recommendations               │
├─────────────────────────────────────────────────────────────────┤
│  Intelligent chart recommendations based on analysis results:    │
│                                                                  │
│  • Time series → Line plot                                       │
│  • Categorical comparison → Bar chart                            │
│  • Two numeric correlated → Scatter plot                         │
│  • Multiple numeric correlated → Heatmap                         │
│  • Distribution analysis → Box plot                              │
│  • Multi-dimensional data → Comprehensive dashboard              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ⚠️ Stage 4: User Confirmation (Required)        │
├─────────────────────────────────────────────────────────────────┤
│  Display to user:                                               │
│    • Data overview (dimensions, types, statistics)              │
│    • Chart recommendations (types, content, reasons)            │
│                                                                  │
│  Wait for user instruction:                                     │
│    ✅ "Generate schemes 1 and 2" → Generate specified charts    │
│    ✅ "Generate all" → Generate all recommendations             │
│    📝 "Modify scheme X..." → Adjust based on feedback           │
│    💬 "I want to make XXX chart" → Custom according to needs    │
│                                                                  │
│  ⚠️ Important: Must wait for explicit user confirmation         │
│      before entering generation phase                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 5: Generation & Delivery               │
├─────────────────────────────────────────────────────────────────┤
│  1. Generate plot_config.json (chart configuration)            │
│  2. Generate {timestamp}_plot.py (Python code)                  │
│  3. Execute code to generate charts:                            │
│     • {timestamp}_fig1_line.png (PNG image)                     │
│     • {timestamp}_fig2_bar.png                                  │
│  4. All files saved to same working directory                   │
└─────────────────────────────────────────────────────────────────┘
```

## File Naming Conventions

### Directory Naming
```
output/
└── 20250312-143052-sales_data/          # timestamp-original_name
    └── ...
```

### File Naming

| File Type | Naming Format | Example |
|---------|---------|------|
| Raw Data | `{timestamp}-{original}` | `20250312-143052-sales_data.csv` |
| Analysis Report | `analysis_report.md` | `analysis_report.md` |
| Chart Config | `plot_config.json` | `plot_config.json` |
| Python Code | `{timestamp}_plot.py` | `20250312-143052_plot.py` |
| Chart PNG | `{timestamp}_fig{n}_{type}.png` | `20250312-143052_fig1_line.png` |

## User Interaction Examples

### Scenario 1: Standard Workflow

```
[User uploads data.csv]

👤 User: Help me analyze this data and create some charts

🤖 Assistant: Received! Processing your data...

   📁 Working directory: output/20250312-143052-data/
   📄 Data file: 20250312-143052-data.csv
   🔍 Analyzing data...

═══════════════════════════════════════════════════════════════
                        Data Analysis Report
═══════════════════════════════════════════════════════════════

📊 Data Overview
• Dimensions: 120 rows × 5 columns
• Numeric columns: 3
• Categorical columns: 2

📋 Column Details
| Column | Type | Description                    |
|--------|------|--------------------------------|
| date   | 📅 datetime | 2023-01 to 2023-12        |
| sales  | 🔢 numeric | mean=1250, std=320         |
| region | 🏷️ categorical | 4 categories: N/S/E/W |

💡 Chart Recommendations

Scheme 1: Time Trend Analysis ⭐
• Chart Type: Line plot
• Content: Sales trend over time
• Reason: Time series data, best for showing trends

Scheme 2: Regional Comparison
• Chart Type: Grouped bar chart
• Content: Sales comparison by region
• Reason: Categorical data, intuitive for differences

Scheme 3: Comprehensive Dashboard
• Chart Type: 2×2 subplot layout
• Includes: Trend line + Bar chart + Box plot + Heatmap
• Reason: Rich dimensions, comprehensive view

═══════════════════════════════════════════════════════════════

🎯 Next Steps
Please tell me what you want:
• "Generate schemes 1 and 2" - Generate specified charts
• "Generate all" - Generate all recommendations
• "Modify scheme 3..." - Provide your modification suggestions

👤 User: Generate schemes 1 and 2

🤖 Assistant: Okay! Generating schemes 1 and 2...

   ⚙️  Chart config: plot_config.json
   📝 Python code: 20250312-143052_plot.py
   🎨 Generating charts...
   ✅ Generated 4 chart files
      📊 20250312-143052_fig1_line.png
      📊 20250312-143052_fig2_bar.png

═══════════════════════════════════════════════════════════════
✅ All complete!
📁 All files saved to: output/20250312-143052-data/
═══════════════════════════════════════════════════════════════
```

### Scenario 2: User Modifications

```
👤 User: Modify scheme 1, group X-axis by month and show mean values

🤖 Assistant: Received! Adjusting scheme 1 based on your request:

   Modified Scheme 1: Monthly Sales Trend
   • Chart Type: Line plot
   • X-axis: Month (grouped by date)
   • Y-axis: Sales mean
   • Data aggregation: Monthly aggregation

   Confirm generation?

👤 User: Confirm

🤖 Assistant: Generating...
```

## Script Usage Guide

### workflow.py - Complete Workflow

```bash
# Complete workflow (analysis + wait for confirmation + generation)
python scripts/workflow.py --input data.csv

# Analysis only (for displaying report, no chart generation)
python scripts/workflow.py --input data.csv --analyze-only

# Specify output directory
python scripts/workflow.py --input data.csv --output-dir ./my_output
```

### data_analyzer.py - Analysis Only

```bash
# Analyze and output report
python scripts/data_analyzer.py --input data.csv --output report.md

# Print report only
python scripts/data_analyzer.py --input data.csv
```

### plot_generator.py - Generate from Config

```bash
# Generate charts according to configuration file
python scripts/plot_generator.py --config plot_config.json --output-dir ./
```

## Important Notes

1. **Required Confirmation Step**: After analysis, must wait for user confirmation, cannot generate charts directly
2. **Unified File Management**: All related files saved to same directory for easy user access
3. **Publication-Ready Output**: Provide high-resolution PNG (300 DPI) suitable for publication
4. **Code Traceability**: Generated Python code also saved for user modification and reproducibility
