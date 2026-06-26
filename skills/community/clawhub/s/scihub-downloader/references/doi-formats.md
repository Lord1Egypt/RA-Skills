# DOI Format Reference

## Standard DOI Format

A DOI (Digital Object Identifier) has the format:

```
10.prefix/suffix
```

Where:
- `10.` is the DOI directory indicator
- `prefix` is assigned by the DOI Registration Agency
- `suffix` is assigned by the publisher

## Examples

### Standard DOIs

```
10.1038/nature12373
10.1016/j.enggeo.2023.107123
10.1029/2023GL010345
10.1007/s00466-023-02234-5
```

### DOI with URL Prefix

```
https://doi.org/10.1038/nature12373
http://doi.org/10.1038/nature12373
```

### DOI with dx.doi.org

```
https://dx.doi.org/10.1038/nature12373
http://dx.doi.org/10.1038/nature12373
```

## Acceptable Input Formats

The `scihub-dl` tool accepts these DOI formats:

| Format | Example | Notes |
|--------|---------|-------|
| Bare DOI | `10.1038/nature12373` | Recommended |
| doi.org URL | `https://doi.org/10.1038/nature12373` | Auto-stripped |
| dx.doi.org | `https://dx.doi.org/10.1038/nature12373` | Auto-stripped |
| doi: prefix | `doi:10.1038/nature12373` | Auto-stripped |
| DOI: prefix | `DOI:10.1038/nature12373` | Auto-stripped |

## PMID Format

PMID (PubMed ID) is a numeric identifier:

| Format | Example |
|--------|---------|
| Bare number | `36871234` |
| PMID prefix | `PMID:36871234` |
| PMID space | `PMID 36871234` |

## Finding DOIs

### From Paper

1. **Title page** - Usually near the journal name
2. **Abstract page** - On publisher's website
3. **PDF header/footer** - First or last page
4. **CrossRef** - https://search.crossref.org

### From Citation

```
Smith, J. et al. (2023). Paper Title. Journal Name, 10(2), 123-145. 
doi: 10.1038/nature12373
```

### From URL

Many publisher URLs contain the DOI:

```
https://www.nature.com/articles/nature12373
→ DOI: 10.1038/nature12373
```

## DOI Resolution

DOIs resolve to the publisher's page:

```bash
# Open DOI in browser
open "https://doi.org/10.1038/nature12373"

# Get metadata
curl "https://api.crossref.org/works/10.1038/nature12373"
```

## Common DOI Prefixes

| Prefix | Publisher |
|--------|-----------|
| 10.1038 | Nature |
| 10.1016 | Elsevier |
| 10.1007 | Springer |
| 10.1029 | AGU |
| 10.1021 | ACS |
| 10.1103 | APS |
| 10.1111 | Wiley |
| 10.1126 | Science |
| 10.1371 | PLOS |
| 10.2139 | SSRN |

## Validation

To validate a DOI:

```bash
# Check if DOI exists
curl -s "https://doi.org/10.1038/nature12373" -I | grep "HTTP"

# Get metadata
curl -s "https://api.crossref.org/works/10.1038/nature12373" | jq .
```