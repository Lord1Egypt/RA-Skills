---
name: validator-tool
description: Validate data formats including JSON, email, URL, file paths, IP addresses, and phone numbers with detailed error reporting and batch processing.
---

# Validator Tool — Multi-Format Data Validation

Validate, lint, and report errors across common data formats. Designed for input sanitization pipelines, CI checks, and API request validation.

## Quick Start

```bash
# Validate a JSON string
validator-tool --json '{"name":"Alice","age":30}'

# Validate an email address
validator-tool --email "user@example.com"

# Validate a URL
validator-tool --url "https://example.com/path?q=1"
```

## Usage

```bash
validator-tool [TYPE] [INPUT] [OPTIONS]

Types:
  --json      Validate JSON syntax and optional schema
  --email     Validate email format (RFC 5321/5322)
  --url       Validate URL format and scheme
  --path      Validate file/directory path (exists, readable, writable)
  --ip        Validate IPv4 or IPv6 address
  --phone     Validate phone number format (E.164 or regional)

Options:
  --schema FILE   JSON Schema file for --json validation
  --strict        Strict mode (reject warnings as errors)
  --batch FILE    Validate multiple inputs from a file (one per line)
  --json-output   Output results as JSON
  --verbose       Show detailed error reasons
```

## Examples

```bash
# Validate JSON with schema
validator-tool --json '{"id":1,"name":"Test"}' --schema schema.json

# Batch validate emails from file
validator-tool --email --batch emails.txt --json-output

# Validate an IP address
validator-tool --ip "192.168.1.1"

# Check if a file path exists and is writable
validator-tool --path "/tmp/log.txt" --strict
```

## Features

- **Multiple formats:** JSON, email, URL, path, IP, phone
- **JSON Schema support:** Validate against draft-07 schemas
- **Batch mode:** Process hundreds of inputs from a file
- **Exit codes:** 0 = all valid, 1 = any invalid, 2 = error
- **Machine-readable:** `--json-output` for pipeline integration
- **Strict mode:** Surface warnings as errors
- **i18n emails:** Supports internationalized email addresses
