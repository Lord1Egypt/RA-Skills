---
name: validator
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [validator, tool, utility]
description: "Validate emails, URLs, phones, dates, and custom patterns. Use when sanitizing input, verifying form fields, checking formats, or enforcing rules."
---

# validator

Input validator.

## Commands

### `email`

Validate email format

```bash
scripts/script.sh email <address>
```

### `url`

Validate URL (+ HTTP check if curl available)

```bash
scripts/script.sh url <url>
```

### `ip`

Validate IPv4/IPv6 address

```bash
scripts/script.sh ip <address>
```

### `phone`

Validate phone number (7-15 digits)

```bash
scripts/script.sh phone <number>
```

### `date`

Validate and parse date string

```bash
scripts/script.sh date <string>
```

### `domain`

Validate domain (+ DNS lookup if dig available)

```bash
scripts/script.sh domain <name>
```

### `credit-card`

Luhn algorithm check + card type detection

```bash
scripts/script.sh credit-card <number>
```

### `json`

Validate JSON syntax

```bash
scripts/script.sh json <file>
```

### `yaml`

Validate YAML syntax

```bash
scripts/script.sh yaml <file>
```

### `csv`

Validate CSV structure (column consistency)

```bash
scripts/script.sh csv <file>
```

## Requirements

- python3
- curl
- dig (optional)

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
