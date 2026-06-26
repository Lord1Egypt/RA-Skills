# Rohoon Six Sigma Professional Support

[![ClawHub](https://img.shields.io/badge/ClawHub-rohoon--6sigma-blue)](https://clawhub.ai/williamhyzhu/rohoon-6sigma)
![Version](https://img.shields.io/badge/version-1.8.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Comprehensive Six Sigma and Lean quality management toolkit for AI agents. Based on **AIAG-VDA SPC Manual (Yellow Volume)**, **AIAG MSA Manual 4th Ed.**, **ISO 13053**, and **GB/T 36077-2025**.

## Features

- **SPC Control Charts**: Xbar-R, Xbar-S, I-MR, CUSUM, EWMA, p/np, c/u, MAMR, Hotelling T²
- **Out-of-Control Detection**: 8 AIAG-VDA rules + 7 Western Electric rules
- **Process Capability**: Cp, Cpk, Pp, Ppk, Pm, Pmk (Geometric Method) with confidence intervals
- **MSA Analysis**: GR&R (ANOVA method), Bias, Linearity, Stability studies
- **DOE**: Full Factorial (2^k), Response Surface (CCD/Box-Behnken), Taguchi S/N Ratios, Factor Effects
- **AIAG-VDA Standard Reports**: PDF reports strictly following Figure 12-1/12-2/12-3 formats (bilingual)
- **Sigma Estimation**: Range (R̄/d₂), Std Dev (s̄/c₄), Pooled Std Dev (s_p)
- **Excel Reports**: Professional multi-worksheet reports
- **GB/T 36077-2025**: Complete China national standard evaluation framework (7 dimensions, 1000 points)

## Installation

```bash
# Install via ClawHub
clawhub install rohoon-6sigma

# Install Python dependencies
cd skills/rohoon-6sigma
pip install -r requirements.txt
```

## Quick Start

### Process Capability Analysis

```bash
python scripts/calculate_capability.py \
  --data "10.1,10.2,10.15,10.18,10.12,10.05,10.22,10.08,10.14,10.19" \
  --usl 10.5 --lsl 9.5 --json
```

### Control Charts

```bash
# Xbar-R chart (subgroup n=5)
python scripts/control_chart.py \
  --data "[10.1,10.2,10.15,10.18,10.12, 10.05,10.22,10.08,10.14,10.19]" \
  --chart-type Xbar-R --subgroup-size 5 --json

# I-MR chart (individual values)
python scripts/control_chart.py \
  --data "10.1,10.2,10.15,10.18,10.12" \
  --chart-type I-MR --json
```

### MSA GR&R Study

```bash
python scripts/msa_grr_analysis.py \
  --data "[10.1,10.15,10.12, ...]" \
  --parts 10 --operators 3 --trials 3 \
  --tolerance 0.5 --json
```

### DOE Full Factorial

```bash
python scripts/doe_full_factorial.py \
  --factors 2 --responses "[40,50,45,55]" --analyze --json
```

### AIAG-VDA Standard PDF Reports

```bash
# Figure 12-1: Normal distribution report (Chinese)
python scripts/aiagvda_unified_report.py -o report.pdf -f 12-1 -l zh

# Figure 12-1: Normal distribution report (English)
python scripts/aiagvda_unified_report.py -o report.pdf -f 12-1 -l en

# Figure 12-2: Non-normal / mixed distribution
python scripts/aiagvda_unified_report.py -o report.pdf -f 12-2 -l zh

# Figure 12-3: Standard statistical summary table
python scripts/aiagvda_unified_report.py -o report.pdf -f 12-3 -l zh
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Standards

| Standard | Description |
|----------|-------------|
| **AIAG-VDA SPC Manual** | Yellow Volume, 1st Ed., February 2026 |
| **AIAG MSA Manual** | 4th Edition |
| **ISO 13053** | Six Sigma Methodology (DMAIC/DMADV) |
| **ISO 22514** | Statistical Methods in Process Management |
| **ISO 7870** | Control Charts |
| **GB/T 36077-2025** | 精益六西格玛管理评价准则 (replaces 2018) |
| **IATF 16949** | Automotive Quality Management |
| **ISO 9001** | Quality Management Systems |

## Use Cases

- **Automotive Quality Management**: IATF 16949 compliance, PPAP documentation
- **Process Capability Studies**: Cp/Cpk analysis for customer audits
- **Measurement System Analysis**: GR&R studies before production launches
- **Design of Experiments**: Process optimization, parameter screening
- **Supplier Assessment**: Evaluate incoming material quality
- **Continuous Improvement**: DMAIC project support
- **China National Standard**: GB/T 36077-2025 self-evaluation

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `calculate_capability.py` | Process capability indices |
| `control_chart.py` | Xbar-R, Xbar-S, I-MR charts |
| `attribute_control_charts.py` | p/np/c/u/Z attribute charts |
| `advanced_control_charts.py` | CUSUM, EWMA, MAMR, Hotelling T² |
| `pooled_std.py` | Sigma estimation methods |
| `western_electric_rules.py` | Out-of-control rule detection |
| `msa_grr_analysis.py` | GR&R study (ANOVA) |
| `msa_other_studies.py` | Bias, Linearity, Stability |
| `doe_full_factorial.py` | 2^k factorial designs |
| `doe_response_surface.py` | CCD, Box-Behnken |
| `doe_factor_effects.py` | Main & interaction effects |
| `doe_sn_ratio.py` | Taguchi S/N ratios |
| `aiagvda_unified_report.py` | Standard PDF report generator |
| `excel_report.py` | Excel report generation |
| `batch_generate_reports_v2.py` | Batch PDF report generation |
| `generate_test_data.py` | Generate test datasets |

## Evaluation Criteria

### Process Capability
| Index | Rating | Action |
|-------|--------|--------|
| ≥ 2.0 | 🟢 Six Sigma | Maintain |
| 1.67–2.0 | 🟢 Excellent | Maintain |
| 1.33–1.67 | 🟡 Good | Improve |
| 1.0–1.33 | 🟡 Marginal | Plan improvement |
| < 1.0 | 🔴 Insufficient | Must improve |

### MSA GR&R
| %GR&R | Rating | Action |
|-------|--------|--------|
| < 10% | 🟢 Acceptable | OK |
| 10–30% | 🟡 Conditional | Evaluate risk |
| ≥ 30% | 🔴 Unacceptable | Improve system |

## Dependencies

Requires Python 3.10+ with: `numpy`, `scipy`, `reportlab`, `openpyxl`, `matplotlib`, `pandas`

## License

MIT

## Author

William (WilliamHYZhu on ClawHub)
