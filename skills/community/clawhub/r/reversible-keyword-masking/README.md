# Reversible Keyword Masking

Reversible Keyword Masking (RKM) is an OpenClaw skill for locally masking sensitive document keywords before AI editing, then verifying and restoring them from an encrypted local mapping.

It is designed for workflows where a document needs to be rewritten, translated, polished, summarized, or restructured while names, organizations, project names, contract numbers, phone numbers, email addresses, IDs, amounts, addresses, or other user-provided keywords should not be exposed to the model.

## What It Does

- Replaces sensitive terms with stable placeholders such as `[[ORG_0001]]`.
- Stores placeholder mappings in an AES-256-GCM encrypted local JSON file.
- Supports `.txt`, `.md`, `.markdown`, `.docx`, and legacy `.doc` through local Word or LibreOffice conversion.
- Verifies edited masked documents before restoration.
- Repairs common placeholder damage such as `[ORG_0001]`, `[[ORG-0001]]`, or full-width brackets when the repair is unambiguous.
- Includes a `cn-sensitive` preset for common Chinese business-document fields.

## Quick Start

```bash
python scripts/rkm.py protect input.md --keywords keywords.yml --out input.masked.md --map input.rkm-map.json
python scripts/rkm.py verify input.masked.edited.md --map input.rkm-map.json
python scripts/rkm.py restore input.masked.edited.md --map input.rkm-map.json --out input.restored.md
```

Set the local mapping password through `RKM_KEY` for non-interactive runs:

```bash
export RKM_KEY="long local secret"
```

PowerShell:

```powershell
$env:RKM_KEY = "long local secret"
```

## Example

A fully fictional walkthrough is included under `examples/`:

```bash
python scripts/rkm.py scan examples/sample.md --preset cn-sensitive --keywords examples/keywords.yml
python scripts/rkm.py protect examples/sample.md --preset cn-sensitive --keywords examples/keywords.yml --out sample.masked.md --map sample.map.json
python scripts/rkm.py verify sample.masked.md --map sample.map.json
python scripts/rkm.py restore sample.masked.md --map sample.map.json --out sample.restored.md
```

## Privacy Boundary

RKM protects explicit configured keywords and preset pattern matches. It does not remove indirect context, business logic, document structure, writing style, or background clues. Mapping files, mapping passwords, decrypted mapping data, and raw sensitive keywords should stay local unless the user explicitly asks otherwise.

## Documentation

- Skill instructions: `SKILL.md`
- Keyword configuration: `references/keyword-config.md`
- Plain-text custom keyword template: `references/custom-keywords.txt`
- Fictional sample workflow: `examples/README.md`

## Version

Current release: `v1.0.1`
