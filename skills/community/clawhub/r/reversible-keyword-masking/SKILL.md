---
name: reversible-keyword-masking
description: Reversible Keyword Masking (RKM) for locally masking sensitive document keywords with stable placeholders before AI editing, then verifying and restoring them from an encrypted local mapping. Use when the user needs to edit, rewrite, translate, summarize, polish, or restructure documents while protecting names, organizations, project names, contract numbers, phone numbers, email addresses, IDs, amounts, addresses, or other user-provided keywords from being exposed to the LLM.
---

# Reversible Keyword Masking

Use this skill to protect sensitive keywords before sending document content to an AI model. Replace each sensitive term locally with stable placeholders such as `[[ORG_0001]]`, keep the placeholder-to-original mapping encrypted on disk, ask the AI to edit only the masked document, then verify and restore the placeholders locally.

Chinese name: 可逆关键词脱敏  
Short name: RKM  
Command: `rkm`

## Core Rules

- Never send raw sensitive keywords, mapping files, passwords, or decrypted mapping data to a remote model unless the user explicitly asks.
- Prefer stable placeholders over ciphertext in the editable document. Models preserve `[[ORG_0001]]` more reliably than long encrypted strings.
- Always verify an AI-edited masked document before restoring it.
- Treat missing, malformed, or unknown placeholders as restoration risks and report them before continuing.
- Keep mapping files local and out of Git.

## Quick Start

Run the bundled CLI from the skill directory:

```bash
python scripts/rkm.py protect input.md --keywords keywords.yml --out input.masked.md --map input.rkm-map.json
python scripts/rkm.py verify input.masked.edited.md --map input.rkm-map.json
python scripts/rkm.py restore input.masked.edited.md --map input.rkm-map.json --out input.restored.md
```

For Chinese business documents, add the built-in preset:

```bash
python scripts/rkm.py protect input.docx --preset cn-sensitive --keywords keywords.yml --out input.masked.docx --map input.rkm-map.json
```

Use neutral output names when the source title is sensitive:

```bash
python scripts/rkm.py protect input.docx --safe-name --preset cn-sensitive --keywords keywords.yml --out ./masked.docx --map ./map.json
```

`--safe-name` ignores the sensitive basename in `--out` and `--map`, preserves their directories, and writes neutral names such as `rkm-masked-1a2b3c4d.docx` and `rkm-map-1a2b3c4d.json`.

Set the encryption password through `RKM_KEY` for non-interactive runs:

```bash
RKM_KEY="long local secret" python scripts/rkm.py protect input.md --keywords keywords.yml --out input.masked.md --map input.rkm-map.json
```

On PowerShell:

```powershell
$env:RKM_KEY = "long local secret"
python scripts/rkm.py protect input.md --keywords keywords.yml --out input.masked.md --map input.rkm-map.json
```

On Windows, you can avoid keeping the password in an environment variable by sealing it once with DPAPI, then passing the sealed file:

```bash
python scripts/rkm.py seal-password --out rkm.key
python scripts/rkm.py --dpapi-password-file rkm.key protect input.md --keywords keywords.yml --out input.masked.md --map input.rkm-map.json
```

The sealed file can only be unsealed by the current Windows user account on that machine. The mapping file itself is still AES-256-GCM encrypted with a PBKDF2-derived key, so it stays portable; DPAPI only protects the password at rest. Keep `*.key` files out of Git.

A runnable, fully fictional walkthrough lives in `examples/` (`sample.md`, `keywords.yml`, `README.md`).

## Workflow

1. Collect sensitive keywords from a YAML keyword file, command-line `--term` values, and optional regex patterns.
2. Optionally run `scan` (or `protect --dry-run`) to preview which terms would be masked before committing.
3. Run `protect` locally to create a masked document and encrypted mapping file.
4. Ask the AI to edit the masked document only. Instruct it to preserve all `[[TYPE_0001]]` placeholders exactly.
5. Run `verify` on the edited masked document. If the AI mangled placeholder brackets, run `verify --repair` to fix them.
6. If verification passes, run `restore` locally to create the final document.

## Preview before masking

Use `scan` to see candidate masks without writing any file or mapping (no password needed):

```bash
python scripts/rkm.py scan input.md --preset cn-sensitive
```

Candidate values are redacted by default (first and last character shown). Add `--show-values` to reveal full values on a local terminal, `--json` for machine-readable output, or `--report scan.json` to save the report. `protect --dry-run` prints the same preview and writes nothing.

## Reports

`protect`, `verify`, and `scan` accept `--report <path>` to write a structured JSON report. Reports never contain raw sensitive values: they list placeholders, categories, counts, and `under_masking`/verification status only.

## Command Details

### Protect

Use `protect` before AI editing:

```bash
python scripts/rkm.py protect <input_file> --keywords <keywords.yml> --out <masked_file> --map <mapping_file>
```

Supported input/output formats:

- `.txt`
- `.md`
- `.markdown`
- `.doc` through local conversion with Microsoft Word or LibreOffice/soffice
- `.docx` with best-effort XML text replacement across the main document, tables, headers, footers, text boxes, and visible watermark/textpath attributes

For `.docx`, replacement is run-aware at the WordprocessingML text-node level: the placeholder is written into the text node where the match begins and the matched characters are cleared from any other text nodes they spanned, so surrounding run formatting (bold, italic, color, font) is preserved. Matches whose value is split across runs or sits in a separate table cell from its label are still handled. Header/footer text, text boxes, and visible VML watermark text attributes are included. After masking, `protect` re-scans the masked output with the same rules and warns if any sensitive span is still detectable (possible under-masking).

For legacy `.doc`, RKM converts the document locally to a temporary `.docx`, applies the same WordprocessingML masking pipeline, and then writes the requested output. If `--out` ends in `.doc`, RKM converts the masked/restored result back to `.doc`; otherwise it can write `.docx`. This requires Microsoft Word on Windows or LibreOffice/soffice installed locally. If neither converter is available, convert the file to `.docx` first.

`protect` refuses to run on an input that already contains `[[...]]` placeholders (it is probably already masked, and re-masking would nest placeholders and break restoration). Pass `--force` to override.

Use `--preset cn-sensitive` for common Chinese business-document patterns: organization names, labeled person names including table labels such as `姓····名`, labeled and standalone Chinese addresses, bank account fields that preserve labels such as `开户行` and mask the value, tax numbers, dates, form-style bracketed date/duration values such as `【 4 】月` or `期限为【/】年` where only the middle value is masked, amounts with units, bare decimal/table amounts such as `320.9`, phone numbers including landlines, email addresses, ID-card-like values, and bank-card-like values.

### Verify

Use `verify` after AI editing and before restoration:

```bash
python scripts/rkm.py verify <edited_masked_file> --map <mapping_file>
```

Verification checks:

- expected placeholders missing from the edited document
- unknown placeholders not present in the encrypted mapping
- malformed placeholder-like tokens such as `[ORG_0001]`
- residual original values: a mapped keyword (4+ characters, matched as a standalone token rather than a substring) reappearing in the edited document, which usually means the AI un-masked a placeholder. Raw values are never printed; only the affected placeholder and category are shown.
- unmapped sensitive spans: for mapping files created by this version, the encrypted mapping stores the masking rules used by `protect`, and `verify` re-scans the edited masked document with those rules. This catches sensitive values that were introduced or left unmasked but are not present in the placeholder mapping. Raw values are never printed; only categories and sources are shown.

Any of these conditions sets the status to `WARNING`, and `restore` refuses to run unless you pass `--allow-warnings`.

To auto-fix malformed placeholders, run `verify` with `--repair --out <file>`:

```bash
python scripts/rkm.py verify input.masked.edited.md --map input.rkm-map.json --repair --out input.repaired.md
```

Repair is conservative: it normalizes malformed tokens (single brackets like `[ORG_0001]`, hyphens like `[[ORG-0001]]`, full-width brackets like `【【ORG_0001】】`, or zero-pad differences like `[PHONE_001]`) and rewrites them only when they map unambiguously to an expected placeholder. Tokens with no matching placeholder are reported as unrepaired and left untouched. Word repairs preserve run formatting where the local conversion pipeline preserves it. After repairing, `verify` re-runs automatically and prints the updated report.

### Restore

Use `restore` only after verification:

```bash
python scripts/rkm.py restore <edited_masked_file> --map <mapping_file> --out <restored_file>
```

Restoration replaces mapped placeholders with original keywords locally.

## Keyword Configuration

Read `references/keyword-config.md` when creating or debugging keyword YAML files.

Minimal example:

```yaml
keywords:
  organizations:
    - Shenzhen Green Carbon Energy Co., Ltd.
  custom:
    - Any exact phrase that must be masked
  projects:
    - Duku Highway Project
patterns:
  phone: "\\b1[3-9]\\d{9}\\b"
  email: "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
```

Manual keywords and regex matches are replaced longest-first to avoid shorter terms breaking longer terms.

### Plain-text custom keyword file

For a simple, maintainable list of exact phrases without writing YAML, pass `--custom-keywords <file.txt>`:

```bash
python scripts/rkm.py protect input.docx --preset cn-sensitive --custom-keywords references/custom-keywords.txt --out masked.docx --map map.json
```

In the file, put one keyword per line, or several on one line separated by `、` or `；`. Lines beginning with `#` are comments, and blank lines and duplicates are ignored. Each keyword is masked with a dedicated `[[CUSTOM_0001]]` placeholder. The flag composes with `--preset`, `--keywords`, and `--term`, and also works with `scan`. A ready-to-edit template lives at `references/custom-keywords.txt`.

When a regex contains capture groups, RKM masks the first non-empty captured group instead of the full match. Use this for label-preserving rules such as `(?:联系人及电话|联系人|经办人)[:： \t　]+([\u4e00-\u9fff]{2,4})` or `(?:开户行|开户银行)[:： \t　]+(.+支行)`. Require at least one delimiter after labels so label text such as `联系人及电话` or `开户行` is not mistaken for a sensitive value. For DOCX tables, allow a newline between the label cell and value cell only when a delimiter is still required. Avoid broad `\s*` rules because extracted table cells may be separated by newlines.

## AI Editing Guard

When asking an AI model to edit masked text, include a short preservation rule:

```text
This document has been masked. All tokens shaped like [[ORG_0001]], [[PERSON_0002]], or [[K_0003]] are immutable placeholders. Do not delete, rewrite, translate, explain, split, merge, or change any placeholder. Edit only the surrounding text.
```

## Failure Handling

- If `verify` reports missing placeholders, inspect whether the AI deleted relevant content or modified the token.
- If `verify` reports malformed placeholders, repair the edited masked document first when the intended placeholder is obvious.
- If the encrypted mapping cannot be opened, do not attempt restoration from memory or conversation context. Ask the user for the correct mapping file and local key.
- If the user needs stronger privacy, remind them this protects explicit keywords but not indirect context, business logic, document structure, or background clues.
