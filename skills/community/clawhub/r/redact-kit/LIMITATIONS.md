# RedactKit Limitations

What RedactKit **doesn't** do. Read before using on sensitive data.

---

## What It Doesn't Do

### 1. **Semantic Understanding**
RedactKit uses regex patterns, not AI. It finds text that LOOKS like an email or API key, but doesn't understand context.

**Example:**
- Input: "My favorite color is 123-45-6789"
- RedactKit: Redacts it (looks like SSN)
- Reality: It's not actually an SSN

**Why:** Semantic analysis requires AI models, which would send your data to external APIs (defeating the purpose).

**Workaround:** Review report mode output before batch redaction. Add exclusion patterns for known false positives.

---

### 2. **Non-Text Data**
Text-only. No support for:
- Images (can't detect faces, license plates, etc.)
- Audio (can't detect voices or spoken PII)
- Video
- PDFs (extract text first)
- Binary files

**Why:** OCR, image analysis, audio transcription require heavyweight dependencies or external services.

**Workaround:** Use `pdftotext`, OCR tools, or transcription services FIRST, then redact the text output.

---

### 3. **Guaranteed Detection**
Regex patterns catch common formats, but not everything.

**What might be missed:**
- Obfuscated data (`user AT example DOT com`)
- Non-standard formats
- Context-dependent secrets (e.g., "The answer is 42" where 42 is a secret passcode)
- Encrypted or encoded data (Base64, etc.)

**Why:** No pattern can anticipate every possible format.

**Workaround:** Add custom patterns for your specific formats. Use --report mode to audit.

---

### 4. **Mapping File Encryption**
Mapping files are stored as plain JSON. If someone gets the mapping file, they can restore your redacted data.

**Why:** Encryption adds complexity (key management, passwords). Out of scope for v1.

**Workaround:** 
- Store mapping files in encrypted folders (FileVault, BitLocker, LUKS)
- Manually encrypt JSON files (GPG, openssl)
- Restrict filesystem permissions (chmod 600)

---

### 5. **Cloud Sync**
No automatic cloud backup or sync for mapping files.

**Why:** Local-only tool by design.

**Workaround:** Manually backup mapping files to secure cloud storage or external drives.

---

### 6. **Structured Data Awareness**
RedactKit treats JSON, CSV, YAML, etc. as plain text. It doesn't parse structure.

**Example:**
- Input JSON: `{"email": "user@example.com"}`
- RedactKit output: `{"email": "[EMAIL-1]"}`
- Problem: Still valid JSON, but might not be what you want

**Why:** Structure-aware redaction requires format-specific parsers. Scope creep.

**Workaround:** This behavior is often desirable (preserves structure). If not, preprocess data.

---

### 7. **Real-Time Monitoring**
RedactKit is a **one-shot tool**, not a live filter.

**Why:** Real-time filtering requires background processes and hooks into applications.

**Workaround:** Integrate into workflows manually (redact before paste).

---

### 8. **Compliance Guarantees**
RedactKit is a tool, not a compliance certification.

**GDPR, HIPAA, PCI-DSS:** RedactKit can HELP with data minimization, but doesn't guarantee compliance. You're responsible for validating it meets your requirements.

**Why:** Compliance is context-dependent (legal interpretations, audit requirements).

**Workaround:** Use RedactKit as one layer of a compliance strategy. Audit outputs. Consult legal counsel.

---

### 9. **Collision Handling**
If two different values match the same pattern in one file, they get different placeholders (`[EMAIL-1]`, `[EMAIL-2]`). But if you redact two DIFFERENT files with the same email, they might get different indices.

**Why:** Mapping is per-redaction-session, not global.

**Workaround:** This is usually fine (restoration works per-file). For global consistency, redact all files in one batch operation.

---

### 10. **Performance on Huge Files**
RedactKit loads entire files into memory. Very large files (100MB+) may be slow or cause OOM errors.

**Why:** Simple implementation (regex over full text).

**Workaround:** Split large files, or increase system memory.

---

## Edge Cases

### False Positives
- **Person names:** `"John Smith"` matches, but so does `"North America"` (capitalized words)
- **API keys:** Long hex strings might match, even if they're not secrets
- **IP addresses:** `"1.2.3.4"` might be a version number, not an IP

**Workaround:** Use `--sensitivity low` to reduce false positives, or add exclusion patterns.

---

### Unicode & Special Characters
Patterns are optimized for ASCII. Emails with unicode domains, phone numbers with unusual formatting, etc. may not match.

**Workaround:** Add custom patterns for your specific formats.

---

### Newlines in Secrets
If a secret spans multiple lines (e.g., multi-line private key), detection might fail depending on pattern.

**Workaround:** Patterns include PEM header detection (`-----BEGIN PRIVATE KEY-----`), but check with --report mode.

---

## When NOT to Use RedactKit

- **Legal evidence:** Courts may require certified redaction tools
- **Medical records:** HIPAA compliance may require specialized software
- **Production data pipelines:** Use database-level access controls instead
- **Real-time filtering:** Use network proxies or data loss prevention (DLP) tools

---

## When TO Use RedactKit

- **Ad-hoc sanitization:** Quick redaction before pasting into AI tools
- **Code sharing:** Remove API keys before sending code to consultants
- **Log sanitization:** Strip PII from logs before sharing with support
- **Prototyping:** Fast redaction for testing workflows
- **Local processing:** When you can't or won't use cloud DLP services

---

## Honest Summary

RedactKit is a **lightweight, local, regex-based redaction tool**. It's fast, has zero dependencies, and works offline. But it's not perfect. It will miss some things (obfuscated data, non-standard formats) and flag some false positives (person name heuristic). Use it for ad-hoc sanitization, not as your sole compliance tool.
