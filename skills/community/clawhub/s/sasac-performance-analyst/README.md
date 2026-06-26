# SASAC Performance Analyst v2.0

> 🇨🇳 Enterprise Performance Evaluation Skill based on SASAC 2025 Standards
> 基于2025年版《企业绩效评价标准值》的企业绩效对标评价智能分析系统

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-green.svg)](https://clawhub.ai/yjkj999999/sasac-performance-analyst)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://github.com/yjkj999999/sasac-performance-analyst)

## 🌟 Overview

**SASAC Performance Analyst** is a professional AI skill for enterprise performance benchmarking and evaluation, built on the authoritative **"Enterprise Performance Evaluation Standard Values (2025)"** published by the Performance Assessment Bureau of the State-owned Assets Supervision and Administration Commission (SASAC) of the State Council.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Precision Benchmarking** | Input indicator values, auto-classify into 5 tiers (Excellent/Good/Medium/Low/Poor) |
| 📊 **4-Dimensional Diagnosis** | Profitability, Operations, Risk, Growth radar chart analysis |
| 📈 **Scoring Engine** | 5-tier linear interpolation scoring with configurable weights |
| 📋 **Report Generation** | Comprehensive evaluation reports (HTML/PDF/Tencent Docs) |
| 🌍 **International Benchmarking** | 19 industries with international standard values (2024) |
| 📄 **Prospectus Parsing** | Automated financial data extraction from HKEX IPO prospectuses |
| 🔗 **Cross-listing Assessment** | Feasibility evaluation for SOE Hong Kong listings |

## 📊 Data Coverage

- **332 Standard Value Tables** (314 domestic + 18 international)
- **10 Major Industry Categories**, 48 sub-categories, 107 minor categories
- **24 Evaluation Indicators** (16 core + 8 supplementary)
- **5 Evaluation Tiers**: Excellent, Good, Medium, Low, Poor
- **4 Size Classifications**: All sizes, Large, Medium, Small enterprises

## 🚀 Quick Start

### Installation

```bash
# Via SkillHub (recommended)
skillon install sasac-performance-analyst

# Via ClawHub
openclaw skills install sasac-performance-analyst

# Manual
git clone https://github.com/yjkj999999/sasac-performance-analyst.git ~/.qclaw/skills/sasac-performance-analyst/
```

### Usage Example

```
User: I'm a large pharmaceutical enterprise with ROE of 15% and R&D intensity of 4%.

AI Assistant:
📊 Benchmarking Results:
  ROE (15%): [Good] tier (Excellent: 17.1%, gap: 12%)
  R&D Intensity (4%): [Medium] tier (Excellent: 7.9%, gap: 49%)

💡 Diagnosis:
  Strong profitability but insufficient R&D investment — risk of "profit today, decline tomorrow."

📋 Recommendations:
  1. Increase R&D intensity to ≥7.9% (Excellent tier)
  2. Establish R&D investment KPI mechanism
  3. Reference CRRC's "Innovation Performance Evaluation" case study
```

## 🏗️ Architecture

```
Data Acquisition → Indicator Calculation → Benchmark Evaluation → Report Generation
  ├─ CnInfo API        ├─ 24 Formulas      ├─ Industry Matching     ├─ HTML Report
  ├─ HKEX Prospectus   ├─ IFRS↔CAS Adj.    ├─ Size Classification   ├─ Radar Chart
  └─ Manual Input      └─ Auto-calc         └─ 5-tier Interpolation  └─ CSV Export
```

## 📁 File Structure

```
sasac-performance-analyst/
├── SKILL.md                          # Skill definition
├── README.md                         # This file
├── README_ZH.md                     # Chinese documentation
├── package.json                     # Metadata
├── system_prompt.md                  # AI system prompt
├── data/
│   ├── sasac_2025_standards.json   # Full 314 domestic tables
│   ├── international_standards.json # 18 international tables
│   ├── industry_mapping.json        # Industry classification mapping
│   ├── case_studies.json           # 5 core case studies
│   ├── hk_ipo_db.json              # HK IPO financial database
│   └── cross_listing_db.json       # Cross-listing evaluation database
├── tools/
│   ├── performance_calculator.py    # Performance calculation engine
│   ├── visualization.py             # Chart & report generation
│   ├── financial_data_extractor.py # PDF financial data extraction
│   ├── hk_ipo_integration.py       # HKEX IPO integration
│   └── report_generator.py         # Report generation
├── templates/
│   └── report_template.html        # Report HTML template
└── html/
    └── sasac_performance_query_2025.html  # Interactive query system
```

## 📊 Evaluation Dimensions & Weights

| Dimension | Weight | Core Indicators |
|-----------|--------|----------------|
| 💰 Profitability | 30% | ROE, Operating Profit Margin, ROA, Cash Coverage |
| ⚙️ Operations | 20% | Asset Turnover, AR Turnover, Current Asset Turnover, Two-gold Ratio |
| 🛡️ Risk Control | 25% | Debt Ratio, Cash-to-Debt, Interest-bearing Debt, Interest Coverage |
| 🌱 Growth | 25% | R&D Intensity, Labor Productivity, EVA Rate, Capital Preservation |

## 📜 License

MIT License — see [LICENSE](LICENSE)

## 👤 Author

**Wang Dongjie (王东杰)**
- CFO | Senior Strategic Finance Expert | CGMA Holder
- Email: Wdj_@163.com
- GitHub: [@yjkj999999](https://github.com/yjkj999999)

## 🙏 Acknowledgments

- SASAC Performance Assessment Bureau (data source)
- Economic Science Press (publisher)
- AICPA & CIMA (CGMA competency framework)
- Hong Kong Exchanges and Clearing (IPO data)
