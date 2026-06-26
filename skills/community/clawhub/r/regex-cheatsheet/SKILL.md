---
name: regex-patterns
description: Comprehensive regex pattern library for common use cases including emails, URLs, phone numbers, dates, passwords, HTML, and more. Use when needing quick copy-paste regex patterns for validation, extraction, or text processing.
---

# Regex Pattern Library

Copy-paste ready regular expressions for common use cases. Test before production use.

---

## 📧 Email & Contact Patterns

### Email Address
```regex
# Basic validation
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

# More permissive (real-world)
^[^\s@]+@[^\s@]+\.[^\s@]{2,}$
```

### Phone Numbers
```regex
# US phone (123) 456-7890 or 123-456-7890
^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$

# International E.164 format (+1234567890)
^\+?[1-9]\d{1,14}$
```

### URLs
```regex
# URL with protocol
https?://[^\s/$.?#].[^\s]*

# URL (optional protocol)
(https?://)?[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+[^\s]*

# Domain name
^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$
```

### IP Addresses
```regex
# IPv4
^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$

# IPv6 (simplified)
^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$
```

---

## 📅 Date & Time Patterns

### Dates
```regex
# YYYY-MM-DD (ISO 8601)
^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$

# MM/DD/YYYY
^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$

# DD/MM/YYYY
^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$
```

### Times
```regex
# 24-hour format (HH:MM)
^([01]\d|2[0-3]):[0-5]\d$

# 24-hour with seconds
^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$

# 12-hour format (HH:MM AM/PM)
^(0?[1-9]|1[0-2]):[0-5]\d\s?(AM|PM|am|pm)$
```

### Timestamps
```regex
# ISO 8601 with timezone
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$
```

---

## 🔐 Password & Security Patterns

### Password Strength
```regex
# Minimum 8 chars, at least one letter and one number
^(?=.*[A-Za-z])(?=.*\d).{8,}$

# Minimum 8 chars, uppercase, lowercase, number
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$

# Strong: 8+ chars, upper, lower, number, special
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$
```

### Common Identifiers
```regex
# UUID v4
^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$

# US Social Security Number (SSN)
^\d{3}-\d{2}-\d{4}$

# US ZIP Code
^\d{5}(-\d{4})?$

# UK Postcode
^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$
```

---

## 📝 Text Processing Patterns

### Whitespace
```regex
# Leading whitespace
^\s+

# Trailing whitespace
\s+$

# Multiple spaces (replace with single space)
\s{2,}

# Empty lines
^\s*$
```

### Numbers
```regex
# Integer (positive/negative)
^-?\d+$

# Decimal number
^-?\d+(\.\d+)?$

# Currency ($123.45)
^\$?\d{1,3}(,\d{3})*(\.\d{2})?$

# Percentage (12.5%)
^\d+(\.\d+)?%$
```

### Hex Colors
```regex
# Hex color (#fff or #ffffff)
^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$

# Hex with alpha
^#([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$
```

---

## 🌐 HTML & Web Patterns

### HTML Tags
```regex
# Opening tag
<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>

# Closing tag
</([a-zA-Z][a-zA-Z0-9]*)>

# Self-closing tag
<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*/>
```

### HTML Comments
```regex
<!--[\s\S]*?-->
```

### CSS Classes/IDs
```regex
# Class selector
class="([^"]*)"

# ID selector
id="([^"]*)"
```

### Markdown
```regex
# Heading level 1-6
^#{1,6}\s.+$

# Bold text
\*\*([^*]+)\*\*

# Italic text
\*([^*]+)\*

# Link
\[([^\]]*)\]\(([^)]*)\)
```

---

## 📂 File & Path Patterns

### File Extensions
```regex
# Image files
\.(jpg|jpeg|png|gif|bmp|webp|svg)$

# Document files
\.(pdf|doc|docx|txt|xls|xlsx|ppt|pptx)$

# Code files
\.(js|ts|py|java|cpp|c|h|go|rs|rb|php)$
```

### File Paths
```regex
# Unix path
^(/[^/]+)+/?$

# Windows path
^[A-Za-z]:\\([^\\]+\\)*[^\\]*$

# Filename (no path)
[^/\\]+$
```

---

## 🔍 Useful Regex Constructs

### Lookarounds
```regex
# Positive lookahead
foo(?=bar)       # "foo" followed by "bar"

# Negative lookahead
foo(?!bar)       # "foo" NOT followed by "bar"

# Positive lookbehind
(?<=foo)bar      # "bar" preceded by "foo"

# Negative lookbehind
(?<!foo)bar      # "bar" NOT preceded by "foo"
```

### Groups & Capture
```regex
# Capture group
(foo|bar)

# Non-capturing group
(?:foo|bar)

# Named group (Python/JS)
(?P<name>pattern)

# Backreference
(["'])\w+\1      # Matches quoted text with same quotes
```

---

## 💡 Quick Reference Table

| Pattern | Regex |
|---------|-------|
| Email | `^[^\s@]+@[^\s@]+\.[^\s@]{2,}$` |
| URL | `https?://[^\s/$.?#].[^\s]*` |
| IPv4 | `^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$` |
| UUID | `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
| YYYY-MM-DD | `^\d{4}-\d{2}-\d{2}$` |
| Hex color | `^#([A-Fa-f0-9]{6}\|[A-Fa-f0-9]{3})$` |

---

## ⚠️ Important Notes

1. **Test thoroughly**: Always test regex patterns with your specific data
2. **Escape properly**: Different languages/engines may require different escaping
3. **Performance**: Complex regex can be slow on large inputs
4. **HTML parsing**: Regex cannot fully parse HTML - use proper parsers when possible
5. **Email validation**: No perfect email regex exists - send verification emails instead
6. **Security**: Regex denial-of-service (ReDoS) is possible with certain patterns

### Testing Tools
- https://regex101.com - Interactive testing with explanation
- https://regexr.com - Visual regex builder
- https://www.debuggex.com - Visualize regex state machines
