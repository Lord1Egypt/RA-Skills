# Singapore SME Compliance Assistant 🇸🇬

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.ai)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-green)](https://github.com/openclaw/openclaw)

Help Singapore SMEs automate compliance tasks: GST calculation, PEPPOL invoice validation, tax report generation, and regulatory checklist.

## Features

- **GST Registration Checker** - Check if your business needs GST registration (S$1M threshold)
- **GST Calculator** - Calculate 9% GST for invoices
- **PEPPOL Invoice Validator** - Validate invoices against InvoiceNow requirements
- **GST F5 Return Helper** - Monthly/quarterly GST return preparation
- **Compliance Calendar** - Track IRAS deadlines and filing requirements

## Installation

```bash
# Via ClawHub
openclaw skills install singapore-sme-compliance
```

## Usage

### Calculate GST

```bash
# Calculate GST for S$5,000 invoice
./scripts/gst_calculator.sh 5000

# Output:
# Amount (excl. GST): S$ 5000.00
# GST Rate: 9.0%
# GST Amount: S$ 450.00
# Total (incl. GST): S$ 5450.00
```

### Check GST Registration

Ask the agent:
```
"Check if I need to register for GST with S$1.2M annual turnover"
```

### Generate Monthly GST Report

Ask the agent:
```
"Generate GST F5 report for March 2026"
```

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.iras.gov.sg/api/* | None (reference only) | GST registration info |
| https://api.gstcalculator.sg/* | Amount, rate | GST calculation |

## Security & Privacy

- **No sensitive data leaves your machine** - All calculations are local
- **No API keys required** - Uses public IRAS reference data
- **Scripts are open source** - Review before installing

## Model Invocation

This skill may autonomously invoke API calls to calculate GST and validate compliance. You can opt-out by configuring model routing rules.

## Trust Statement

By using this skill, no external data is sent. All GST calculations are performed locally using Singapore IRAS published rates. Only install if you trust the skill author.

## Requirements

- OpenClaw v1.0+
- bash, bc (for calculator script)

## Support

- Documentation: https://github.com/openclaw/openclaw
- IRAS Helpline: +65 1800 356 8300
- InvoiceNow: +65 6248 0909

## License

MIT License - See LICENSE file in GitHub repository
