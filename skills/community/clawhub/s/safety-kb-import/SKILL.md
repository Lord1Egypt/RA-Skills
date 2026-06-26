---
name: safety-kb-import
description: "安全生产法规标准导入工具。当用户需要导入新法规或标准到知识库、PDF文本提取、条款拆分、批量导入、数据质量验证时使用。触发词：导入法规、添加标准、入库、导入知识库、补充标准、PDF提取文本、拆分条款、KB导入、safety-review import"
version: "1.0.0"
author: WorkBuddy Agent
license: MIT
tags:
  - safety
  - regulation
  - knowledge-base
  - import
  - compliance
  - mining-safety
---

# Safety KB Import — 安全生产法规标准导入工具

## Overview

This skill provides **standardized, safe import workflows** for adding regulations, standards, and policy documents into the `safety-review` knowledge base (SQLite). It handles multi-source text extraction, smart clause splitting, conflict detection, and three-table atomic writes (regulations + clauses + std_registry).

**Database location**: `~/.openclaw-autoclaw/skills/safety-review/db/knowledge.db`

## When to Use This Skill

- User wants to add new standards/regulations to the knowledge base
- User has PDF files that need text extraction before import
- User needs to batch-import multiple standards at once
- User asks about importing courseware-referenced standards that are missing
- Any **write** operation on the `safety-review` database

**Trigger phrases (Chinese)**: 导入法规、入库、添加标准、补充知识库、PDF提取、拆分条款、批量导入

**Companion skill**: Use `safety-kb-query` first to check what's already in the database before importing.

## Prerequisites

1. Detect Python command:
   ```bash
   python --version
   ```

2. Required packages for PDF extraction:
   ```bash
   pip install pdfplumber
   ```
   For OCR of scanned PDFs:
   ```bash
   pip install pdf2image pytesseract
   # Also requires Tesseract OCR engine installed on system
   ```

## Import Workflow (Complete)

### Phase 1: Preparation — Check What's Needed ⭐ Always Do This First

Before importing anything, use `safety-kb-query` to identify gaps:

```bash
python <kb_query_path>/kb_query.py check "GB 16423" "AQ/T 2033" "AQ 2034"
```

This prevents duplicates and identifies data quality issues.

### Phase 2: Text Extraction

#### Option A: From PDF Files

```bash
python scripts/kb_import.py extract-pdf /path/to/document.pdf
```

**Response fields:**
- `success`: boolean
- `text`: extracted full text (empty if scan-only)
- `char_count`: number of characters extracted
- `page_count`: total pages
- `is_scan_only`: true if PDF is image-based (needs OCR)

**If `is_scan_only` is true**, the PDF is a scanned/image-based document:
1. Try installing and using tesseract OCR
2. If OCR unavailable, extract content from PPT lecture materials or web sources as fallback
3. Document the source as "PPT整理" or "网络来源" rather than official text

#### Option B: From Web Sources

Use `web_fetch` to get full text from government websites, wikisource, etc.
Common reliable sources:
- **维基文库** (wikisource.org) — full text of laws/policies
- **政府公报** (gov.cn/gongbao) — official gazette versions
- **部委官网** — original standard publications

#### Option C: From Existing Documents (.docx, .pptx)

Extract text from these formats using appropriate libraries (`python-docx`, `python-pptx`) or the respective skills.

### Phase 3: Create Import Manifest

Create a JSON manifest file listing all items to import:

```json
{
  "items": [
    {
      "title": "金属非金属矿山安全规程",
      "document_number": "GB 16423—2020",
      "issuing_authority": "国家市场监督管理总局",
      "authority_level": "national",
      "effective_date": "2021-09-01",
      "status": "current",
      "domains": "矿山安全",
      "category": "国标",
      "full_text": "<complete extracted text here>",
      "source_url": "",
      "page_count": 70,
      "clause_split_pattern": "standard"
    },
    {
      "title": "国务院关于进一步加强企业安全生产工作的通知",
      "document_number": "国发〔2010〕23号",
      "issuing_authority": "国务院",
      "authority_level": "national",
      "effective_date": "2010-07-23",
      "status": "current",
      "domains": "安全生产",
      "category": "政策文件",
      "full_text": "<complete text>",
      "source_url": "https://zh.wikisource.org/...",
      "page_count": 5,
      "clause_split_pattern": "policy"
    }
  ]
}
```

### Manifest Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `title` | ✅ | Full title of the regulation/standard |
| `document_number` | ✅ | Standard number (GB XXXX, AQ/T XXXX, 国发[X]X号) |
| `issuing_authority` | ❌ | Issuing agency (default: "") |
| `authority_level` | ❌ | One of: `national`, `ministerial`, `local` |
| `effective_date` | ❌ | ISO date format YYYY-MM-DD |
| `status` | ❌ | `current` (default), `superseded`, `draft`, `repealed` |
| `domains` | ❌ | Domain category (e.g., "矿山安全") |
| `category` | ❌ | Type: "国标", "行标", "政策文件", "地方文件" |
| `full_text` | ✅ | **Complete** text content for clause splitting |
| `source_url` | ❌ | Original source URL for attribution |
| `page_count` | ❌ | Number of pages (for reference) |
| `clause_split_pattern` | ❌ | `standard` (default), `policy`, `raw_lines` |

### Clause Splitting Patterns

The tool supports three splitting strategies — choose based on document type:

| Pattern | Best For | How It Works |
|---------|----------|-------------|
| `standard` | GB/AQ national/industry standards | Recognizes chapters (第X章), sections (N.N), sub-sections (N.N.N), appendixes |
| `policy` | Government notices, State Council documents | Recognizes Chinese numbering (一、二、(一)、1.) |
| `raw_lines` | Unstructured text, fallback | Splits by non-empty lines |

**Test splitting before full import:**
```bash
python scripts/kb_import.py split-clauses --text "$SAMPLE_TEXT" --pattern standard
```

### Phase 4: Execute Import

```bash
python scripts/kb_import.py import --json manifest.json
```

**What happens during import:**

1. **For each item** in the manifest:
   - Searches existing regulations by `document_number`
   - If found → **UPDATE** (overwrite existing data)
   - If not found → **INSERT** (create new record)
   
2. **Clause processing**:
   - Deletes old clauses (if updating)
   - Re-splits `full_text` using specified pattern
   - Inserts new clause records linked to regulation ID

3. **std_registry registration** (automatic):
   - If `document_number` starts with GB/AQ → auto-registers in std_registry table
   - Skips if already registered

**Output includes per-item status:**
- `created` — New record inserted
- `updated` — Existing record overwritten
- `skipped` — (reserved for future skip logic)
- `error` — Database error with message

### Phase 5: Post-Import Validation

Always validate after importing:

```bash
# Validate specific imported records
python scripts/kb_import.py validate <regulation_id>

# Check overall data quality
python <kb_query_path>/kb_query.py conflicts

# Verify it's findable
python <kb_query_path>/kb_query.py search "<document_number>"
```

## Handling Special Cases

### Scanned/Image-Based PDFs (No Extractable Text)

When `extract-pdf` returns `"is_scan_only": true`:

1. **First choice**: Install tesseract and run OCR
2. **Second choice**: Find text version from web sources (government sites, wikisource)
3. **Third choice**: Extract from related PPT/lecture materials (document as "PPT整理")
4. **Last resort**: Skip or note as "待补充官方全文"

**Important**: When using non-official sources (PPT, web scraping), always note this in the `source_url` field so data provenance is tracked.

### Large Standards (e.g., GB 16423 with 80K+ characters)

No special handling needed — the tool processes them normally. Clause count may be high (2000+). Consider using `--pattern standard` for best results.

### Batch Imports (10+ Items)

Split manifests into batches of 5-10 items each. Run sequentially. This makes error isolation easier.

### Conflict: Existing Record Has Wrong Data

The tool will overwrite any existing record matching the `document_number`. Before overwriting:

1. Use `safety-kb-query info <id>` to check current data
2. If current data looks correct (different standard sharing similar number?), abort and investigate
3. The `conflicts` command in `safety-kb-query` can help identify mismatched records proactively

## Complete Example: Importing Courseware-Referenced Standards

This is the canonical workflow when a user says "the standards referenced in my training material aren't in the database":

```
Step 1: Extract references from user's document
        → List: [GB 16423-2020, AQ/T 2033-2023, AQ 2034, 国发[2010]23号]

Step 2: Gap analysis
        $ python kb_query.py check GB16423 AQ2033 AQ2034 "国发[2010]23号"
        → Found: 1, Missing: 3, Issues: 1 (ID:94 has wrong data)

Step 3: Extract text for missing items
        $ python kb_import.py extract-pdf GB16423-2020.pdf
        → { success: true, text: "...", char_count: 80357 }

Step 4: Create manifest.json with all items

Step 5: Execute import
        $ python kb_import.py import --json manifest.json
        → { imported: 3, updated: 2, skipped: 0 }

Step 6: Validate
        $ python kb_import.py validate 94
        → { is_valid: true, issues: [] }

Step 7: Verify
        $ python kb_query.py check GB16423 AQ2033 AQ2034 "国发[2010]23号"
        → All found ✓
```

## Relationship with Other Skills

| Skill | Role |
|-------|------|
| `safety-kb-query` | Query/read operations; must use BEFORE import for gap detection |
| `safety-kb-import` (**this one**) | Import/write operations into the database |
| `pdf` | Advanced PDF handling (merge, split, watermark) — use for complex PDF prep work |
| `standard-update-courseware` | Update courseware after standards change — uses both query & import |

## Known Limitations

- **No rollback**: Import commits immediately. Validate before importing bulk data.
- **OCR dependency**: Scanned PDF handling requires external tesseract installation.
- **Clause granularity**: Split patterns are heuristic-based; review output for edge cases.
- **Single-user**: No locking mechanism for concurrent access.

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Database not found` | Wrong path | Set `KB_PATH` env var or update `DEFAULT_DB_PATH` |
| `no such column: X` | Schema changed | Run `schema` command to verify columns |
| `UNIQUE constraint failed` | Duplicate insert attempt | Tool should handle updates; check manifest has unique doc numbers |
| `clause_count: 0` after import | Text empty or pattern mismatched | Try different `clause_split_pattern`; verify `full_text` field isn't empty |
| Garbled Chinese in output | Encoding issue | Ensure script runs with UTF-8 locale; Windows: `chcp 65001` |

## Version History

- **1.0.0** (2026-04-25): Initial release with import, extract-pdf, split-clauses, validate, schema commands
