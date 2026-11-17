# Veterinary Abbreviation Glossary

How vet notes are written and what the shorthand means. The script's decoder maps each term to a plain-language expansion plus a "why the vet mentions it" note.

## The Structure of a Vet Note

```
Patient: name, age, sex/neuter status ("12y MC DSH" = 12-year-old male-castrated domestic shorthair)
Subjective: owner complaints ("Hx V/D x2d" = vomiting/diarrhea for 2 days)
Objective: exam findings ("BAR, MM pink/moist, BCS 7/9")
Assessment: diagnoses ("r/o pancreatitis" = considering pancreatitis)
Plan: treatment + rechecks ("Cerenia 16mg SID x3d, recheck PRN")
```

## Frequency & Route Shorthand

| Term | Meaning |
|---|---|
| SID / q24h | once daily |
| BID / q12h | twice daily |
| TID / q8h | three times daily |
| QID / q6h | four times daily |
| PRN | as needed |
| PO | by mouth |
| SC / SQ | subcutaneous injection (also at-home fluid therapy) |
| IV / IM | intravenous / intramuscular |
| NPO | nothing by mouth (pre-anesthesia etc.) |

## Exam & Status Shorthand

| Term | Meaning |
|---|---|
| BAR | bright, alert, responsive |
| QAR | quiet, alert, responsive |
| MM pink/moist | gum color/hydration normal |
| BCS n/9 | body condition score (4–5 ideal) |
| MCS | muscle condition score |
| TPR | temperature, pulse, respiration |
| WNL / NSF | within normal limits / no significant findings |
| ADR | "ain't doin' right" — real veterinary shorthand for vague illness |

## History & Diagnosis Shorthand

| Term | Meaning |
|---|---|
| Hx | history |
| s/p | status post (already had) |
| r/o | rule out (considering) |
| Dx / Ddx | diagnosis / differential list |
| Tx / Rx | treatment / prescription |
| Px / GP | prognosis / good prognosis |
| MC / MN / FS | male castrated / male neutered / female spayed |
| V/D | vomiting and diarrhea |
| AN / anorexia | not eating (veterinary sense) |
| CKD / CRF | chronic kidney disease / chronic renal failure (older term) |
| DM | diabetes mellitus |
| IBD | inflammatory bowel disease |
| FLUTD / FUS | feline urinary disease |
| FeLV / FIV | feline leukemia / immunodeficiency virus |
| PKD | polycystic kidney disease (Persians) |
| mets | metastases |

## Lab Shorthand

| Term | Meaning |
|---|---|
| CBC | complete blood count |
| chem / CMP | chemistry panel |
| CREA / BUN / SDMA | kidney markers |
| ALT / ALP / AST / GGT | liver enzymes |
| USG | urine specific gravity |
| UPC | urine protein:creatinine ratio |
| T4 / fT4 / TSH | thyroid tests |
| cPL / fPL | pancreatitis tests (canine/feline pancreatic lipase) |

## Decoding Tips for Agents

1. **Tokenize on whitespace, not slashes** — "r/o", "s/p", "v/d" contain punctuation that naive splitters destroy.
2. **Units may be attached** — "CREA2.8" or "28µg/dL" — extract numbers with adjacent markers, tolerate missing separators.
3. **Ages read "12y MC DSH"** — number + y + sex code + breed abbreviation.
4. **Recheck instructions are the question generator's fuel** — "recheck SDMA in 4 wks" tells you exactly what the vet is watching.
5. **When a term isn't in the glossary**, say so honestly and suggest asking the vet — do not invent an expansion.
