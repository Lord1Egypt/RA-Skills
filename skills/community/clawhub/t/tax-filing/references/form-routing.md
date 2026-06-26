# Form Routing: Income Types → Required Forms

Use this table to determine which forms and schedules the user needs based on their source documents and income types. Start from the source docs the user has, then follow the chain.

## Income Routing Table

| Source Doc | Income Type | Goes To | Then Flows To |
|-----------|-------------|---------|---------------|
| W-2 | Wages, salary, tips | 1040 Line 1a | — |
| W-2 Box 12 Code W | Employer HSA contributions | Form 8889 Line 9 | Schedule 1 Line 13 → 1040 Line 10 |
| 1099-NEC | Self-employment income | Schedule C Line 1 | Schedule C Line 31 → Schedule 1 Line 3 → 1040 Line 8; also → Schedule SE |
| 1099-INT | Interest income | Schedule B Part I (if total > $1,500) | 1040 Line 2b |
| 1099-DIV | Ordinary dividends | Schedule B Part II (if total > $1,500) | 1040 Line 3b |
| 1099-DIV Box 1a vs 1b | Qualified dividends | — | 1040 Line 3a (qualified portion, taxed at capital gains rates) |
| 1099-B | Stock/crypto sales | Form 8949 | Schedule D → 1040 Line 7 |
| 1099-MISC Box 1 | Rents | Schedule E Part I | Schedule E → Schedule 1 Line 5 → 1040 Line 8 |
| 1099-MISC Box 2 | Royalties | Schedule E Part I | Schedule E → Schedule 1 Line 5 → 1040 Line 8 |
| 1099-SA | HSA distributions | Form 8889 Part II | Taxable amount → Schedule 1 Line 8c → 1040 Line 8 |
| 5498-SA | HSA contributions | Form 8889 Line 2 | Form 8889 Line 13 → Schedule 1 Line 13 → 1040 Line 10 |
| 1098 | Mortgage interest | Schedule A Line 8a | 1040 Line 13 (if itemizing) |
| 1098-T | Tuition | Form 8863 | 1040 Line 29 (AOTC) or Schedule 3 Line 3 (LLC) |
| 1099-G Box 1 | Unemployment compensation | — | 1040 Line 7 |
| 1099-R | Retirement distributions | — | 1040 Lines 4a/4b (IRA) or 5a/5b (pensions) |

## Schedule Trigger Rules

These rules determine when each schedule is required:

### Always Required if Applicable
| Schedule | Required When |
|----------|--------------|
| Schedule 1 | Any additional income (1099-NEC, HSA, etc.) or above-the-line adjustments |
| Schedule 2 | AMT, excess premium tax credit, SE tax, or additional Medicare tax |
| Schedule 3 | Education credits, foreign tax credit, estimated tax payments, excess SS withholding |

### Conditional Schedules
| Schedule | Required When |
|----------|--------------|
| Schedule A | Itemizing deductions (total > standard deduction) |
| Schedule B | Interest or dividends > $1,500 |
| Schedule C | Self-employment / sole proprietor income |
| Schedule D | Capital gains or losses from investments |
| Schedule E | Rental income, royalties, partnership/S-corp income |
| Schedule SE | Net self-employment income ≥ $400 |

### Additional Forms
| Form | Required When |
|------|--------------|
| Form 8949 | Stock/crypto sales (detail behind Schedule D) |
| Form 8889 | HSA contributions, distributions, or employer contributions |
| Form 8863 | Education credits (AOTC or Lifetime Learning) |
| Schedule 8812 | Child tax credit (if children under 17) |
| Form 2441 | Child and dependent care expenses credit |
| Form 8959 | Additional Medicare Tax (wages > $200K single / $250K MFJ) |
| Form 8960 | Net Investment Income Tax (MAGI > $200K single / $250K MFJ) |

## NRA-Specific Forms

If the filer is a nonresident alien, the form set is different. See `references/form-field-maps.md` for field-to-line mappings and the NRA workflow in the main SKILL.md Step 3b.

| Form | Purpose | Key Trigger |
|------|---------|-------------|
| Form 1040-NR | Main NRA return (replaces Form 1040) | Always required for NRA filers |
| Form 8843 | Exempt individual statement | F-1/J-1 students claiming SPT exemption |
| Schedule NEC | Non-effectively connected income | Dividends, capital gains at flat rate (not ECI) |
| Schedule OI | Other information | Visa type, treaty claims, days present |
| Form 8833 | Treaty-based return position disclosure | Claiming any treaty benefit (e.g., Article 20(c)) |
| Schedule 1 | Additional income/adjustments | Contractor income (1099-NEC), HSA deduction |
| Form 8889 | HSA | HSA contributions or distributions |

## Decision Shortcuts

- **Only W-2 income, no other complexity** → Form 1040 only (no schedules needed). Standard deduction.
- **W-2 + bank interest under $1,500** → Form 1040 only. Interest goes directly on Line 2b.
- **W-2 + 1099-NEC** → Form 1040 + Schedule C + Schedule SE + Schedule 1 + Schedule 2
- **W-2 + stock sales** → Form 1040 + Form 8949 + Schedule D
- **W-2 + HSA** → Form 1040 + Form 8889 + Schedule 1
