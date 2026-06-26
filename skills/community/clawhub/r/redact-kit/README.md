# RedactKit — AI Privacy Scrubber

**Scan your data before sending it to AI. Detect and redact PII, secrets, and sensitive info. Reversible, local, zero network calls.**

RedactKit scans text and files for sensitive data (emails, phone numbers, API keys, credit cards, etc.), replaces them with placeholders, and saves a mapping file so you can restore the originals later. Perfect for sanitizing data before pasting into AI tools or sharing with teammates.

---

## The Problem

You want to get AI help with a document, but it contains:
- Customer emails
- API keys
- Phone numbers
- Internal project names
- Credit card test data

Pasting it directly into ChatGPT, Claude, or any AI tool means that sensitive data leaves your control. Even if the AI provider promises not to train on it, do you want to risk it?

## What RedactKit Does

### Detect & Redact
- **PII:** Emails, phone numbers, SSNs, person names
- **Secrets:** API keys, passwords, AWS keys, private keys
- **Financial:** Credit card numbers
- **Network:** IP addresses, URLs

### Reversible Redaction
- Replaces sensitive data with placeholders (`[EMAIL-1]`, `[API-KEY-2]`, etc.)
- Saves a mapping file locally
- Restore original values anytime with `redact_restore.py`

### Batch Mode
- Scan entire directories
- Supports `.txt`, `.md`, `.py`, `.json`, `.csv`, `.yaml`, and more
- Preserves directory structure

### Report Mode
- See what WOULD be redacted without changing anything
- Perfect for auditing before processing

### Custom Patterns
- Add your own regex patterns (employee IDs, project codes, etc.)
- Configure sensitivity levels (`low`, `medium`, `high`)

### Zero Network
- Everything runs locally
- No API calls, no cloud uploads
- Your data stays on your machine

---

## Quick Start

```bash
# Scan and redact a file
python3 redact_kit.py document.txt --output document.redacted.txt --mapping mapping.json

# Restore original values
python3 redact_restore.py document.redacted.txt mapping.json --output document.restored.txt

# Report mode (see what would be redacted)
python3 redact_kit.py document.txt --report
```

---

## Usage Guide

### Redact a Single File

```bash
# Basic redaction
python3 redact_kit.py input.txt --output output.txt

# Save mapping for restoration
python3 redact_kit.py input.txt --output output.txt --mapping mapping.json

# Different sensitivity levels
python3 redact_kit.py input.txt --output output.txt --sensitivity high
```

### Redact from Stdin

```bash
# Pipe text through RedactKit
cat sensitive.txt | python3 redact_kit.py > redacted.txt

# Copy-paste workflow
python3 redact_kit.py
# Paste your text, press Ctrl+D
# Redacted output prints to stdout
```

### Batch Mode (Directory)

```bash
# Redact all files in a directory
python3 redact_kit.py input_dir/ --batch --output output_dir/ --mapping mappings/

# Process only specific file types
python3 redact_kit.py input_dir/ --batch --output output_dir/ --extensions .txt,.md,.py
```

### Report Mode

```bash
# See what would be redacted WITHOUT changing anything
python3 redact_kit.py document.txt --report

# Output shows:
# ✅ Found 5 sensitive items:
#    pii: 3
#    secrets: 2
# 
# 🔍 Report mode - showing matches:
#   [email] john.doe@example.com → [EMAIL-1]
#   [phone] 555-123-4567 → [PHONE-1]
#   [api_key] EXAMPLE_KEY_abc... → [API-KEY-1]
```

### Filter by Category

```bash
# Redact only PII (skip secrets, financial, network)
python3 redact_kit.py input.txt --output output.txt --category pii

# Redact only secrets
python3 redact_kit.py input.txt --output output.txt --category secrets

# Multiple categories
python3 redact_kit.py input.txt --output output.txt --category pii --category secrets
```

### Restore Redacted Files

```bash
# Restore single file
python3 redact_restore.py redacted.txt mapping.json --output restored.txt

# Restore directory
python3 redact_restore.py redacted_dir/ mappings/ --batch --output restored_dir/

# Verify restoration matches original
python3 redact_restore.py redacted.txt mapping.json --output restored.txt --verify original.txt
```

---

## Use Cases

### 1. **AI Assistance with Sensitive Docs**
Redact customer data before pasting into ChatGPT for help with code, emails, or documentation.

### 2. **Sharing Logs with Support**
Redact production logs before sending to vendor support. Restore internally after.

### 3. **Code Review with External Consultants**
Redact API keys and internal project names before sharing code. Give consultants clean code without secrets.

### 4. **Testing AI Prompt Safety**
Redact real data from test datasets before using them in AI experiments.

### 5. **Data Minimization for Compliance**
Automatically redact PII from documents before archiving or sharing with third parties.

### 6. **Pre-Flight Check Before Publishing**
Scan blog posts, documentation, or tutorials for accidentally committed secrets or PII.

---

## What Gets Detected

### PII (Personal Identifiable Information)
- **Emails:** `user@example.com`
- **Phone numbers:** US and international formats
- **SSNs:** `123-45-6789`
- **Person names:** Simple heuristic (capitalized names, may have false positives)

### Secrets
- **API keys:** Generic long alphanumeric strings
- **AWS Access Keys:** `AKIA...`
- **Passwords:** `password=secret123`
- **Private keys:** PEM format headers

### Financial
- **Credit cards:** Visa, MasterCard, Amex, Discover, JCB

### Network
- **IP addresses:** IPv4 (e.g., `192.168.1.1`)
- **URLs:** `https://example.com/path`

---

## Configuration

Copy `config_example.py` to `config.py` and customize:

```python
# Set default sensitivity
SENSITIVITY_LEVEL = 'medium'

# Enable/disable categories
ENABLED_CATEGORIES = {
    'pii': True,
    'secrets': True,
    'financial': True,
    'network': False  # Disable URL/IP redaction
}

# Add custom patterns
CUSTOM_PATTERNS = [
    {
        'name': 'employee_id',
        'regex': r'EMP-\d{6}',
        'category': 'custom',
        'sensitivity': 'medium',
        'description': 'Employee IDs',
        'placeholder_template': '[EMPLOYEE-{index}]'
    }
]

# File types for batch mode
SUPPORTED_EXTENSIONS = ['.txt', '.md', '.py', '.json', '.csv']
```

See `config_example.py` for full options.

---

## Examples

### Example 1: Sanitize for AI Help

```bash
# Before: document.txt contains customer emails and API keys
cat document.txt
# "Contact support@acme.com for help. API key: EXAMPLE_KEY_not_real_abc123"

# Redact
python3 redact_kit.py document.txt --output safe.txt --mapping restore.json

# After: safe.txt
cat safe.txt
# "Contact [EMAIL-1] for help. API key: [API-KEY-1]"

# Paste safe.txt into ChatGPT, get help

# Restore original after
python3 redact_restore.py safe.txt restore.json --output recovered.txt
```

### Example 2: Report Mode Audit

```bash
python3 redact_kit.py production.log --report

# Output:
# ✅ Found 23 sensitive items:
#    pii: 15
#    secrets: 5
#    network: 3
# 
# 🔍 Report mode - showing matches:
#   [email] admin@internal.com → [EMAIL-1]
#   [ip_address] 10.0.1.50 → [IP-1]
#   [api_key] Bearer abc123... → [API-KEY-1]
#   ...
```

### Example 3: Custom Pattern

```python
# config.py
CUSTOM_PATTERNS = [
    {
        'name': 'ticket_id',
        'regex': r'TICKET-\d{8}',
        'category': 'custom',
        'sensitivity': 'low',
        'description': 'Internal ticket IDs',
        'placeholder_template': '[TICKET-{index}]'
    }
]
```

```bash
python3 redact_kit.py tickets.txt --output redacted.txt
# Input: "See TICKET-12345678 for details"
# Output: "See [TICKET-1] for details"
```

---

## What's Included

| File | Purpose |
|------|---------|
| `redact_kit.py` | Main redaction engine (CLI + library) |
| `redact_restore.py` | Restoration tool |
| `redact_patterns.py` | Built-in pattern library + custom pattern manager |
| `config_example.py` | Configuration template |
| `README.md` | This file |
| `LIMITATIONS.md` | What it doesn't do |
| `LICENSE` | MIT License |

---

## Requirements

- Python 3.7+
- **Zero external dependencies** (stdlib only)
- Works on Linux, macOS, Windows

---

## Python API

Use RedactKit in your own scripts:

```python
from redact_kit import RedactionEngine
from redact_restore import RestorationEngine

# Redact text
engine = RedactionEngine(sensitivity_level='medium')
result = engine.redact("Contact support@acme.com")

print(result.redacted_text)
# "Contact [EMAIL-1]"

print(f"Found {len(result.matches)} sensitive items")

# Save mapping
engine.save_mapping(result.mapping_id, 'mapping.json')

# Restore later
restore_engine = RestorationEngine()
restore_engine.load_mapping('mapping.json')
restored = restore_engine.restore(result.redacted_text, result.mapping_id)

print(restored)
# "Contact support@acme.com"
```

---

## FAQ

**Q: Does it send my data anywhere?**  
A: **No.** Everything runs locally. Zero network calls.

**Q: How accurate is the detection?**  
A: Regex-based, so it catches patterns, not semantic meaning. Low false negatives (good at finding things), but may have false positives (names heuristic, generic API key patterns).

**Q: Can I use it on non-English text?**  
A: Patterns are mostly language-agnostic (emails, IPs, credit cards work fine). Person name detection is optimized for English.

**Q: What if I lose the mapping file?**  
A: You can't restore without it. **Backup mapping files carefully.** Treat them like encryption keys.

**Q: Can I encrypt mapping files?**  
A: Not built-in. Use filesystem encryption (LUKS, BitLocker, FileVault) or encrypt the JSON manually.

**Q: Does it work on images or PDFs?**  
A: Text-only. Extract text first (OCR, pdftotext) then redact.

---

## License

MIT — See `LICENSE` file.

---

## Author

**Shadow Rose**

Built for people who want to use AI tools without leaking sensitive data.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**SECURITY DISCLAIMER:** This software provides supplementary security measures and 
is NOT a replacement for professional security auditing, penetration testing, or 
compliance frameworks. No software can guarantee complete protection against all 
threats. Users operating in regulated industries (healthcare, finance, legal) should 
consult qualified security professionals and verify compliance with applicable 
regulations (GDPR, HIPAA, SOC2, etc.) independently.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at . If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
