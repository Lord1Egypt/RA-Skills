**Skill**: [Pandoc PDF Generation](../SKILL.md)

## Bibliography and Citations Management

### The Problem with Manual References

Duplicating footnote references is error-prone:

```markdown
In the main text[^ref1]

## References
[^ref1]: Source citation here    ← Footnote definition

1. Source citation here           ← Manual duplication for References section
```

**Problems:**
- Must maintain two copies of each citation
- Updates require changing multiple locations
- Risk of inconsistencies between footnotes and References

### Automated Solution: Pandoc --citeproc

**Step 1: Create a bibliography file (references.bib)**

```bibtex
@misc{nsw-law-2025,
  title = {How to Prepare for the 2025 NSW Strata Law Changes},
  url = {https://netstrata.com.au/how-to-prepare-for-the-2025-nsw-strata-law-changes/},
  year = {2025},
  month = {October}
}

@misc{mcgrathnicol-2025,
  title = {McGrathNicol Review: Key Updates & Improvements},
  url = {https://netstrata.com.au/mcgrathnicol-review-key-updates-improvements/},
  year = {2025},
  month = {May}
}
```

**Step 2: Use citations in Markdown**

```markdown
New reforms came into effect October 27, 2025 [@nsw-law-2025].
The McGrathNicol review shows progress [@mcgrathnicol-2025].
```

**Step 3: Build with --citeproc**

```bash
pandoc document.md \
  -o document.pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --bibliography=references.bib \
  --csl=chicago-author-date.csl
```

**Result:**
- Citations automatically formatted in text
- Bibliography automatically generated at end
- Single source of truth for all references
- Change citation style by swapping CSL file

### CSL Citation Styles

Download styles from:
- [Zotero Style Repository](https://www.zotero.org/styles)
- [Citation Styles Project](https://citationstyles.org/)

Common styles:
- `chicago-author-date.csl` (default if not specified)
- `apa.csl`
- `mla.csl`
- `ieee.csl`

### Alternative: YAML References

For smaller documents, embed references in YAML:

```yaml
---
title: Document Title
references:
- id: nsw-law-2025
  title: How to Prepare for the 2025 NSW Strata Law Changes
  URL: https://netstrata.com.au/...
  issued:
    year: 2025
    month: 10
---
```
