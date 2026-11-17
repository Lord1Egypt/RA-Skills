# SEOwlsClaw — SEO Brief Registry
# File: SEO_BRIEFS/_index.md
# Purpose: Index of all generated SEO content briefs.
# Used by: `write` and `writehtml` with --from-brief <brief-id> flag

---

## ⚠️ FILE WRITE — CONFIRMATION REQUIRED
Never write files silently or autonomously.
Before saving any SEO Brief files, you must:
1. Show the user the full file content in chat
2. Show the proposed file path
3. Ask: "Save this file? (yes / no / rename)"
4. Save and write SEO Briefs only to disk in the folder SEO_BRIEFS/<new-seo-brief-id>.md after explicit "yes" from user.

---

## How Briefs Are Used

### Generating a Brief
```text
seobrief Blogpost "Leica M6 Analogfotografie Guide" --lang de --brand example-brand
# → Creates in the folder SEO_BRIEFS/ a new file `leica-m6-analogfotografie-guide-de.md`
# → Adds a new row to at the end of this file to the index of `## Registry Table for new SEO Briefs`
```

### Writing Content From a Brief
```text
persona blogger
write Blogpost "Leica M6 Guide" --from-brief leica-m6-analogfotografie-guide-de
# → Brain loads brief file at Step 1 (parse)
# → Brief's keyword, outline, and internal links override auto-detected values
# → Persona from command overrides brief's persona suggestion (user choice wins)
```

### What --from-brief Does in the Brain
Step 1 (Parse): Load SEO_BRIEFS/<new-seo-brief-id>.md → extract:
  - primary_kw, secondary_kw (override auto-detected if not set in command)
  - approved_outline (H1/H2/H3 structure to follow)
  - paa_questions (use as FAQ variables)
  - internal_links (inject as {INTERNAL_LINKS_*} variables)
  - word_count_target (pass to Step 6.5 depth check)
  - competitor_gaps (use as content improvement hints in Step 3)

---

## Registry Table for new SEO Briefs
Never completly overwrite this SEO_BRIEFS/_index.md file. You only add new SEO Briefs in the following table:
> Briefs are added here automatically when `seobrief` generates a new brief.
> Status values: draft | approved | in-production | published

| Brief ID | Topic | Type | Brand | Lang | Date | Status | File |
|----------|-------|------|-------|------|------|--------|------|
| _(empty — add rows here as briefs are generated)_ | | | | | | | |


---

*Last updated: 05-05-2026 (v0.8)*
*Maintainer: Chris — rows are auto-added by seobrief*
