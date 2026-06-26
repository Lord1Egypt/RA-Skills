---
name: tax-filing
description: >
  United States federal income tax filing assistant for US citizens, resident aliens,
  and nonresident aliens. Guides users through the entire IRS filing workflow:
  determining filer type and filing status, identifying which forms and schedules are
  needed, calculating amounts from source documents (W-2, 1099s, etc.), and filling
  IRS PDF forms using pypdf. This skill covers US federal taxes only — not state,
  local, or non-US tax systems. Use this skill whenever the user mentions taxes, tax
  returns, 1040, 1040-NR, filing status, "which forms do I need", "help me file my
  taxes", "tax prep", deductions, NRA tax filing, nonresident alien taxes, treaty-based
  returns, "check my tax forms", "review my 1040-NR", or any request related to
  preparing a US federal tax return — even if they don't specify their filer type.
  This skill handles the routing and covers both citizen/RA (Form 1040) and NRA
  (Form 1040-NR) workflows end to end, including PDF form filling and validation.
version: 0.2.0
---

# Tax Filing

A guided workflow for preparing US federal income tax returns. This skill covers all filer types — US citizens, resident aliens (RA), and nonresident aliens (NRA) — by first determining the correct filer type, then routing to the appropriate forms and procedures. Both citizen/RA and NRA workflows are fully self-contained in this skill, including PDF form field mappings, cross-form validation, and the safe `update_form.py` script.

## Step 1: Gather Source Documents

Before anything else, ask the user what documents they have. Common source docs:

| Document | What it tells you |
|----------|-------------------|
| W-2 | Wages, federal/state tax withheld, employer HSA contributions |
| 1099-NEC | Contractor / self-employment income |
| 1099-INT | Bank interest |
| 1099-DIV | Dividends (qualified and ordinary) |
| 1099-B | Stock/crypto sales (proceeds and cost basis) |
| 1099-MISC | Other income (royalties, rents, etc.) |
| 1099-SA / 5498-SA | HSA distributions and contributions |
| 1098 | Mortgage interest paid |
| 1098-T | Tuition paid (education credits) |
| I-94 | Travel history (needed for NRA determination) |

If the user has an I-94 or mentions a visa type, that's a strong signal they may be NRA — proceed to Step 2 with that in mind.

## Step 2: Determine Filer Type

This is the critical routing decision. Read `references/filing-status.md` for the full decision tree. The short version:

1. **US citizen or green card holder** → Resident. File **Form 1040**. Go to Step 3a.
2. **Visa holder (F-1, J-1, H-1B, OPT, etc.)** → Apply the **Substantial Presence Test (SPT)**:
   - Count days present: current year days + (1/3 × prior year days) + (1/6 × two years ago days)
   - If total ≥ 183 → **Resident alien** (unless an exemption applies). File **Form 1040**. Go to Step 3a.
   - F-1 and J-1 students are **exempt from SPT** for their first 5 calendar years. They remain NRA. File **Form 1040-NR**. Go to Step 3b.
   - If total < 183 → **Nonresident alien**. File **Form 1040-NR**. Go to Step 3b.
3. **Dual-status** (changed status mid-year) → complex case. Note it for the user and suggest professional review for the transition period.

Ask the user directly if unclear. Don't assume.

## Step 3a: Citizen / Resident Alien Workflow (Form 1040)

Read `references/form-routing.md` to determine which schedules and forms are needed based on the user's income types. For field-level details on individual schedule lines and common pitfalls, read `references/common-schedules.md` when filling specific forms.

### Workflow

1. **Determine filing status** — Single, MFJ, MFS, HOH, QSS (see `references/filing-status.md`)
2. **Map income to forms** — Use the routing table in `references/form-routing.md`
3. **Standard vs. itemized deduction** — 2025 standard deduction: $15,000 (Single), $30,000 (MFJ). Itemize only if total Schedule A deductions exceed this.
4. **Calculate key amounts** from source docs:
   - Total wages (sum of all W-2 Box 1)
   - Total interest/dividends (1099-INT/DIV)
   - Net self-employment income (1099-NEC minus expenses → Schedule C → Schedule SE)
   - Capital gains/losses (1099-B → Form 8949 → Schedule D)
   - Above-the-line deductions (HSA, student loan interest, SE tax deduction → Schedule 1)
   - AGI = Total income - Adjustments
   - Taxable income = AGI - Deduction (standard or itemized)
5. **Fill PDF forms** — Use `scripts/update_form.py` (bundled with this skill) or write equivalent code following the three critical rules:
   - Never write to the same path as input
   - Always use `auto_regenerate=False`
   - Iterate all pages
6. **Cross-validate** — Check the validation rules below
7. **Final review** — Re-extract all fields and confirm consistency

### Cross-Form Validation Rules (Form 1040)

1. **W-2 Box 1 (all) → 1040 Line 1a** (total wages)
2. **Schedule 1 Line 11 → 1040 Line 8** (additional income)
3. **Schedule 1 Line 26 → 1040 Line 10** (adjustments)
4. **1040 Line 9 (total income) = Line 1z + Line 8**
5. **1040 Line 11 (AGI) = Line 9 - Line 10**
6. **1040 Line 13 = standard deduction or Schedule A total**
7. **1040 Line 15 (taxable income) = Line 11 - Line 13 - Line 14**
8. **Schedule C Line 31 (net profit) → Schedule SE Line 2**
9. **Schedule SE Line 13 (SE tax) → Schedule 2 Line 4**
10. **Schedule D Line 16 or 21 → 1040 Line 7** (capital gain/loss)
11. **W-2 Box 2 (all) → 1040 Line 25a** (federal tax withheld)
12. **Estimated payments (1040-ES) → 1040 Line 26**

### Common Mistakes (Citizen/RA)

- Forgetting to file **Schedule SE** when you have 1099-NEC income (self-employment tax is separate from income tax)
- Using the wrong **cost basis** from 1099-B (check Box 1e — if blank, you must calculate it yourself via Form 8949)
- Double-counting **employer HSA contributions** (W-2 Box 12 Code W) — these go on Form 8889 Line 9, not Line 2
- Missing the **$3,000 capital loss limit** — net losses over $3,000 carry forward, they don't all deduct in one year
- Filing as **Single** when **Head of Household** applies (HOH has a larger standard deduction and lower tax brackets)

## Step 3b: Nonresident Alien Workflow (Form 1040-NR)

This section covers the complete NRA filing workflow. For NRA-specific field-to-line mappings, see `references/form-field-maps.md`. For PDF recovery procedures, see `references/pypdf-recovery.md`.

### Critical pypdf Rules

These rules prevent data loss. Violating them will corrupt PDF files. The bundled `scripts/update_form.py` enforces all three automatically — use it instead of writing update logic from scratch.

1. **NEVER write output to the same path as input.** PdfReader uses lazy reading — if you write to the same file, you truncate it while the reader still holds references into it. Page annotations (already in memory) may survive, but the AcroForm catalog gets corrupted during the partial read/write overlap. Always write to a temp path first, then copy.

2. **Always use `auto_regenerate=False`** when calling `update_page_form_field_values()`. The default `True` removes `/AP` (appearance stream) entries from each field. Without appearance streams, some PDF viewers render the field as blank even though the `/V` value is correct — the data is there but invisible.

3. **Iterate all pages** when updating fields, even if you think fields are on page 1. Some IRS forms silently split fields across pages — if you only update page 0, fields on page 1 will be silently skipped with no error.

4. **If a PDF gets corrupted** (field tree broken but annotation values survive):
   - Check annotations directly: `page.get("/Annots")` → `annot.get("/V")`
   - Rebuild the AcroForm `/Fields` array from page annotations
   - Read `references/pypdf-recovery.md` when you see this symptom — it has the full step-by-step repair procedure

### Core Update Function

A bundled script at `scripts/update_form.py` encodes all three critical rules above plus post-write verification. Use it for all form updates:

```bash
# CLI usage — fix a field
python scripts/update_form.py Form1040NR.pdf /tmp/Form1040NR_fixed.pdf --set "f1_53=5000"

# Fix multiple fields and clear one
python scripts/update_form.py Form8843.pdf /tmp/Form8843_fixed.pdf \
    --set "f1_14=338" "f1_17=338" --clear "f1_15"
```

```python
# Or import as a library in your own script
from scripts.update_form import update_form
import shutil

update_form("Form.pdf", "/tmp/Form_fixed.pdf", {"f1_53": "5000"}, clear_fields=["f1_65"])
shutil.copy("/tmp/Form_fixed.pdf", "Form.pdf")  # only then overwrite original
```

The script automatically verifies that fields survived the write and warns if the output looks corrupted. Ensure pypdf is available: `pip install pypdf --break-system-packages`.

### Field Discovery Workflow

Before modifying any form, always extract and map fields first.

**Step 1: Extract all field names and values**
```python
reader = PdfReader("Form.pdf")
fields = reader.get_form_text_fields()
for name, value in sorted(fields.items()):
    short = name.split(".")[-1].replace("[0]", "")
    print(f"{short} = {value}")
```

**Step 2: Map fields to line numbers via Y-position**
Before this step, read `references/form-field-maps.md` for the expected field-to-line table — it covers 1040-NR, 8843, Schedule NEC, Schedule OI, Form 8833, Form 8889, and Schedule 1. Use it as a reference while verifying the Y-position analysis below.

IRS PDFs use positional layout. Extract annotation rectangles to determine which line a field corresponds to:
```python
page = reader.pages[0]
annots = page.get("/Annots")
field_positions = []
for annot_ref in annots:
    annot = annot_ref.get_object()
    t = str(annot.get("/T", ""))
    v = annot.get("/V", "")
    rect = annot.get("/Rect", [])
    ft = str(annot.get("/FT", ""))
    if ft == "/Tx":  # text fields only
        y = float(rect[1]) if rect else 0
        x = float(rect[0]) if rect else 0
        field_positions.append((y, x, t, v))
# Sort by Y descending = top of page to bottom (matches line order)
for y, x, t, v in sorted(field_positions, reverse=True):
    short = t.split(".")[-1].replace("[0]", "")
    print(f"Y={y:.0f} X={x:.0f} {short} = {v}")
```

Compare the Y-position ordering against the physical form layout to create a definitive field-to-line map.

**Step 3: Check checkboxes and radio buttons**
```python
all_fields = reader.get_fields()
for name, field in sorted(all_fields.items()):
    v = field.get("/V", "")
    ft = field.get("/FT", "")
    if ft == "/Btn":
        short = name.split(".")[-1].replace("[0]", "")
        print(f"{short} = {v} (button)")
```

### NRA Form Suite Overview

A typical NRA (F-1 OPT) filing includes these forms. See `references/form-field-maps.md` for complete field-to-line mappings.

| Form | Purpose | Key Fields |
|------|---------|------------|
| 1040-NR | Main return | Income lines, AGI, tax, withholding, refund |
| Schedule 1 | Additional income/adjustments | Contractor income (Line 8h), HSA deduction |
| Schedule NEC | Tax on non-effectively-connected income | Dividends, capital gains, NEC tax |
| Schedule OI | Other information | Visa type, country, treaty claims, days present |
| Form 8843 | Statement for exempt individuals | Days of presence, visa status, exclusion days |
| Form 8833 | Treaty-based return position | Treaty article, exemption amount |
| Form 8889 | HSA | Contributions, employer contributions, deduction |

### NRA Workflow Steps

1. **Gather source docs** (W-2, 1099s, 5498-SA, I-94)
2. **Extract all fields** from all filled PDFs
3. **Build field-to-line maps** using Y-position analysis and `references/form-field-maps.md`
4. **Calculate key NRA amounts**:
   - Total wages (W-2 Box 1) → 1040-NR Line 1a
   - Treaty-exempt income → Line 1k (requires Form 8833)
   - Net wages = Line 1a minus Line 1k → Line 1z
   - Contractor income (1099-NEC) → Schedule 1 Line 8h → 1040-NR Line 8
   - HSA deduction → Form 8889 → Schedule 1 → 1040-NR Line 10
   - AGI = Line 9 (total ECI) - Line 10 (adjustments)
   - NRA cannot take standard deduction (must itemize or take $0)
   - Non-effectively connected income (dividends, capital gains) → Schedule NEC at flat rates
5. **Fill PDF forms** using `scripts/update_form.py` (different output path!)
6. **Cross-validate** every number against source docs and between forms (see rules below)
7. **Apply fixes** using the safe update function
8. **Re-extract and verify** all fields after each fix
9. **Final verification**: read every form one more time and confirm consistency

### Cross-Form Validation Rules (NRA / Form 1040-NR)

After filling, validate these consistency checks:

1. **W-2 Box 1 → 1040-NR Line 1a** (wages)
2. **Schedule 1 Line 10 → 1040-NR Line 8** (additional income from Sch 1)
3. **1040-NR Line 1a minus treaty exempt = Line 1z** (if treaty applies)
4. **1040-NR Line 9 (total ECI) = Line 1z + Line 8** (or sum of all income lines)
5. **1040-NR Line 11a (AGI) = Line 9 - Line 10** (adjustments)
6. **Schedule NEC total tax → 1040-NR Line 23a**
7. **Form 8843 Line 4b = Schedule OI current year days** (days to exclude)
8. **Form 8843 Lines 4a days must match Schedule OI** for each year
9. **W-2 Box 2 → 1040-NR Line 25a** (federal tax withheld)
10. **Form 8833 exemption amount → 1040-NR Line 1k** (treaty exempt income)

### Common NRA Mapping Errors

Watch for these — they are the most frequent mistakes when auto-filling:

- **Contractor income on Line 5b** (pensions) instead of **Line 8** (additional income from Schedule 1)
- **Wages duplicated** on both Line 1a and Line 1h (Line 1h is "other earned income", not a repeat)
- **AGI placed on Line 6** (reserved/future use) instead of Line 11a
- **Treaty exempt amount missing** from Line 1k when Form 8833 is filed
- **Line 1z left empty** — should equal total of Lines 1a through 1h minus exempt
- **Days of presence wrong on Form 8843** — must match I-94 travel history exactly, not assume 365

### US-China Tax Treaty Quick Reference

This section covers the US-China treaty as a concrete example. Similar treaties exist for other countries (e.g., India Article 21(2), South Korea Article 21(1)) — verify article numbers and rates against the specific treaty if your country differs.

For Chinese nationals on F-1 visa:

- **Article 20(c)**: $5,000 exemption on wages/scholarship for students — reported on Line 1k of 1040-NR, requires Form 8833
- **Article 9(2)**: 10% rate on dividends (vs 30% default) — reported on Schedule NEC
- **IRC 871(i)(2)(A)**: Bank deposit interest is exempt for NRAs — do NOT report on any form
- **IRC 871(a)(2)**: Capital gains taxed at 30% flat if present 183+ days — reported on Schedule NEC

## Workflow Summary

1. Gather source documents from the user
2. Determine filer type (citizen / RA / NRA) and filing status
3. Route to the correct workflow (3a for 1040, 3b for 1040-NR)
4. Identify required forms and schedules
5. Calculate amounts from source documents
6. Fill PDF forms safely (different output path, `auto_regenerate=False`, iterate all pages)
7. Cross-validate all numbers between forms
8. Final review — re-extract every form and confirm consistency
