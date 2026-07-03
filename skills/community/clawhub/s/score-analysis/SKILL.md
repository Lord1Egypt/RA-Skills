---
name: score-analysis
description: "分析班级考试成绩，生成可视化图表和分析报告，支持多次成绩纵向对比和同层次班级横向对比。"
version: "1.0.0"
author: "OpenClaw Community"
license: "MIT"
tags:
  - education
  - score-analysis
  - data-visualization
  - report-generation
---

# Score Analysis Skill

AI-powered class score analysis tool that generates visualized charts and professional reports. Supports longitudinal comparison across multiple exams and horizontal comparison with peer classes.

## Features

- 📊 Auto-detect Excel/CSV headers (supports merged cells, mixed Chinese/English)
- 📈 Multi-dimensional analysis (horizontal & vertical comparison)
- 🎯 Critical student identification (near pass lines)
- 📉 Subject imbalance diagnosis
- 📋 Grouped radar charts by student type
- 📄 Professional Word report with charts
- 🎨 Customizable school branding

## Workflow

### 1. Data Reading & Validation
- Auto-detect header structure
- Extract fields: student ID, name, class, total score, subject scores, rankings
- Output standardized JSON

### 2. Data Verification (Required)
After reading data, **must send to user for verification** before analysis:

Submit verification content:
- Average score per subject per class
- Number of students per class
- Total score average
- Special notes (absences, anomalies)

⚠️ Analysis can only proceed after user confirmation!

### 3. Analysis Dimensions

#### Horizontal Comparison (Peer Classes)
- Total score average comparison
- Subject average comparison
- Score segment distribution
- Special control line / undergraduate line pass rates
- Top student distribution

#### Vertical Comparison (Time Dimension)
- Class average score trends
- Pass count changes
- Student ranking fluctuations
- Subject score changes

#### Individual Analysis
- Student score volatility (stability)
- Subject imbalance diagnosis
- Progress/regression attribution
- Critical student identification (within X points of pass line)

### 4. Chart Generation

#### Grouped Radar Charts (by student type)
- **Special control line critical students** → radar chart (within 10 points, max 5)
- **Undergraduate line critical students** → radar chart (max 5)
- **Subject-imbalanced students** → radar chart (highest imbalance index, max 5)

#### Other Charts
- Subject average score bar chart
- Class average comparison chart
- Score segment distribution chart

### 5. Report Output
Generate Word format analysis report including:
- School logo, header/footer
- Three-line tables (research style)
- Embedded charts
- Highlight boxes (emphasize conclusions)

### 6. Presentation PPT (Optional)
Call pptx-master skill to create presentation PPT.

## Subject Score Rules

### Default Rules
- **Chinese, Math, English, Physics**: Use **raw scores**
- **Chemistry, Biology, Politics, Geography**: Use **adjusted scores**
- **Total score**: Default to **adjusted total score**

### Special Cases
- When adjusted/raw scores are in same column (e.g., `85(92)` format), ask user to confirm
- If table only has raw scores, use raw scores

## Data Processing Rules

### Absence/Makeup Handling
- Marks like `/`, `缺`, `缓`, `缓考`, `0`, blank are treated as absence
- Absent students excluded from average calculation

### Score Lines
- Special control line, undergraduate line provided by user (may be image)
- May vary per exam, needs individual confirmation

### Peer Classes
- Specified by user during analysis
- Must ask if not specified

### Student Mobility
- Transferred students excluded from individual analysis

## Output Files
- `*_standardized.json` - Standardized data
- `*_analysis.json` - Analysis results
- `charts/` - Charts directory
- `*_report.docx` - Analysis report
- `*_presentation.pptx` - Presentation PPT (optional)

## Directory Structure
```
score-analysis/
  SKILL.md                        # Skill description
  scripts/
    create_template.py            # Template generator
    generate_report_from_template.py  # Report from template
    generate_radar_charts.py      # Grouped radar charts
    generate_report.py            # Direct report generation
  references/
    analysis_framework.md         # Analysis framework
  assets/
    report_template.docx          # Word report template
  examples/
    sample_data.json              # Sample data for testing
```

## Requirements

```bash
pip install python-docx matplotlib pandas numpy openpyxl
```

## License

MIT
