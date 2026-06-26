# SEOwlsClaw — SEO Brief Registry
# File: SEO_BRIEFS/_index.md
# Purpose: Index of all generated SEO content briefs.
# Used by: /write and /writehtml with --from-brief <brief-id> flag

---

## Registry Table

| Brief ID | Topic | Type | Brand | Lang | Date | Status | File |
|----------|-------|------|-------|------|------|--------|------|
| _(empty — add rows here as briefs are generated)_ | | | | | | | |

> Briefs are added here automatically when /seobrief generates a new brief.
> Status values: draft | approved | in-production | published

---

## ⚠️ FILE WRITE — CONFIRMATION REQUIRED
Never write files silently or autonomously.
Before saving any SEO Brief files, you must:
1. Show the user the full file content in chat
2. Show the proposed file path
3. Ask: "Save this file? (yes / no / rename)"
4. Only write to disk after explicit "yes"

---

## How Briefs Are Used

### Generating a Brief
```bash
/seobrief Blogpost "Leica M6 Analogfotografie Guide" --lang de --brand jbv-foto
# → Creates SEO_BRIEFS/leica-m6-analogfotografie-guide-de.md
# → Adds row to this index
```

### Writing Content From a Brief
```bash
/persona blogger
/write Blogpost "Leica M6 Guide" --from-brief leica-m6-analogfotografie-guide-de
# → Brain loads brief file at Step 1 (parse)
# → Brief's keyword, outline, and internal links override auto-detected values
# → Persona from command overrides brief's persona suggestion (user choice wins)
```

### What --from-brief Does in the Brain
Step 1 (Parse): Load SEO_BRIEFS/<brief-id>.md → extract:
  - primary_kw, secondary_kw (override auto-detected if not set in command)
  - approved_outline (H1/H2/H3 structure to follow)
  - paa_questions (use as FAQ variables)
  - internal_links (inject as {INTERNAL_LINKS_*} variables)
  - word_count_target (pass to Step 6.5 depth check)
  - competitor_gaps (use as content improvement hints in Step 3)

---

*Last updated: 2026-04-05 (v0.1)*
*Maintainer: Chris — rows are auto-added by /seobrief*
