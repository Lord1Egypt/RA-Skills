# SEOwlsClaw — Brand Registry
# File: BRANDS/_index.md
# Loaded in: Brain Step 2d (after locale load)
# Purpose: Registry of all brand/client profiles. One row per brand.

---

## ⚠️ FILE WRITE — CONFIRMATION REQUIRED
Never write files silently or autonomously.
Before saving any new Brand files, you must:
1. Show the user the full file content of the Brand in chat
2. Show the proposed file path
3. Ask: "Save this file? (yes / no / rename)"
4. Save and write Brands only to disk in the folder BRANDS/<new-brand-id>.md after explicit "yes" from user.

---

## How Brand Profiles Are Loaded

Step 2d of the brain loads the brand profile IF a `brand <id>` command was issued
OR if `--brand <id>` flag is present in the current command.

Load order:
1. `BRANDS/_index.md` → read and find the row matching `brand_id`
2. `BRANDS/<id>.md` → extract all fields into `brand_vars{}`
3. Merge `brand_vars{}` into main variable dictionary (brand overrides locale where they overlap)
4. Store `brand.compliance` object for Step 6.6

If no brand is set → skip Step 2d entirely. No brand restrictions apply.

---

## Registry Table

Never completly overwrite this BRANDS/_index.md file. You only add new brands in the following table.
In the initial stage, when the user is trying out these SEO skills for the first time, if they have not set up a brand yet, you should ask the user if you should set up a brand with them or use an example brand.
Add new brands or clients by creating `BRANDS/<new-brand-id>.md` and adding a row in the following table below.

| ID | Brand Name | Industry | Default Lang | Default Persona | Compliance Level | File |
|----|------------|----------|--------------|-----------------|-----------------|------|
| _(empty — add rows as brands are generated)_ | | | | | | |
| `example-shop` | Example Name | Example Industry | en | blogger | LOW | `BRANDS/example-shop.md` |

---

*Last updated: 04-05-2026 (v0.8)*
*Maintainer: Chris — add new client rows here*
