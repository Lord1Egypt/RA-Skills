# NCBI Entrez Query Syntax Reference

## Boolean Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `AND` | Both terms required | `cancer AND immunotherapy` |
| `OR` | Either term | `mouse OR rat` |
| `NOT` | Exclude term | `CRISPR NOT Cas9` |

Operators must be UPPERCASE. Implicit AND is applied between adjacent terms:
`cancer immunotherapy` → `cancer AND immunotherapy`

## Grouping

Use parentheses for complex logic:
```text
(cancer OR tumor) AND (immunotherapy OR "immune checkpoint")
```

## Phrase Search

Double-quote multi-word terms:
```text
"Sinorhizobium meliloti"
"cyclic di-GMP"
```

## Field Qualifiers

Restrict searches to specific fields with `[FIELD]` notation:

| Qualifier | Searches | Example |
|-----------|----------|---------|
| `[Title/Abstract]` | Title + abstract text | `hopanoid[Title/Abstract]` |
| `[Title]` | Title only | `biofilm[Title]` |
| `[Author]` | Author name | `Newman DK[Author]` |
| `[Date - Publication]` | Publication date | `2024[Date - Publication]` |
| `[Journal]` | Journal name | `Nature[Journal]` |
| `[MeSH Terms]` | MeSH headings | `Biofilms[MeSH Terms]` |
| `[All Fields]` | All indexed fields | `CRISPR[All Fields]` |
| `[Organism]` | Organism name | `Sinorhizobium[Organism]` |

## Date Ranges

```text
# Specific year
2024[Date - Publication]

# Range (inclusive)
2020:2026[Date - Publication]

# Relative (past N years)
("2023"[Date - Publication] : "3000"[Date - Publication])
```

## Combined Examples

```text
# Organism + topic + recent
Sinorhizobium meliloti[Organism] AND biofilm[Title/Abstract] AND 2020:2026[Date - Publication]

# Author + topic
Newman DK[Author] AND hopanoid

# Multiple organisms
(Sinorhizobium OR Ensifer OR Bradyrhizobium) AND biofilm
```
