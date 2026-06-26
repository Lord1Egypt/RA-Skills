# SEOwlsClaw — Brand Registry
# File: BRANDS/_index.md
# Loaded in: Brain Step 2d (after locale load)
# Purpose: Registry of all brand/client profiles. One row per brand.

---

## Registry Table

In the initial stage, when the user is trying out these SEO skills for the first time, if they have not set up a brand yet, you should ask the user if you should set up a brand with them or use an example brand.
Add new brands or clients by creating `BRANDS/<id>.md` and adding a row here.

| ID | Brand Name | Industry | Default Lang | Default Persona | Compliance Level | File |
|----|-----------|----------|--------------|-----------------|-----------------|------|
| `example-shop` | Example Name | Example Industry | en | vintage-expert | LOW | `BRANDS/example-shop.md` |

---

## How Brand Profiles Are Loaded

Step 2d of the brain loads the brand profile IF a `/brand <id>` command was issued
OR if `--brand <id>` flag is present in the current command.

Load order:
1. `BRANDS/_index.md` → find the row matching `brand_id`
2. `BRANDS/<id>.md` → extract all fields into `brand_vars{}`
3. Merge `brand_vars{}` into main variable dictionary (brand overrides locale where they overlap)
4. Store `brand.compliance` object for Step 6.6

If no brand is set → skip Step 2d entirely. No brand restrictions apply.

---

*Last updated: 2026-04-05 (v0.1)*
*Maintainer: Chris — add new client rows here*
