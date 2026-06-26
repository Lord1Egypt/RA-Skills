# IRS Form Field-to-Line Mappings

Field names extracted from 2025 IRS fillable PDFs. Field name pattern is typically `topmostSubform[0].PageN[0].f{page}_{seq}[0]`.

> **Important**: These mappings were determined by Y-position analysis of annotation Rect coordinates. Always verify against the actual PDF if using a different tax year — field numbering can change between years.

## Form 1040-NR

### Page 1 (Key Income Lines)

| Field | Y-pos | Line | Description |
|-------|-------|------|-------------|
| f1_42 | ~384 | 1a | Wages, salaries, tips (W-2 Box 1) |
| f1_43 | ~372 | 1b | Household employee income |
| f1_44 | ~360 | 1c | Tip income not on 1a |
| f1_45 | ~348 | 1d | Medicaid waiver |
| f1_46 | ~336 | 1e | Dependent care benefits |
| f1_47 | ~324 | 1f | Adoption benefits |
| f1_48 | ~312 | 1g | Form 8919 wages |
| f1_50 | ~300 | 1h | Other earned income |
| f1_53 | ~252 | 1k | Treaty-exempt income (e.g. $5000 Art. 20(c)) |
| f1_54 | ~240 | 1z | Total (sum of 1a through 1h, or 1a minus 1k depending on instruction) |
| f1_55 | ~228 | 2a | Tax-exempt interest |
| f1_56 | ~216 | 2b | Taxable interest |
| f1_57 | ~204 | 3a | Qualified dividends |
| f1_58 | ~192 | 3b | Ordinary dividends |
| f1_62 | ~168 | 5a | Pensions/annuities |
| f1_63 | ~168 | 5b | Pensions taxable (different X from 5a) |
| f1_65 | ~144 | 6 | Reserved for future use — LEAVE EMPTY |
| f1_66 | ~132 | 7a | Capital gain/loss |
| f1_68 | ~108 | 8 | Additional income from Schedule 1 |
| f1_69 | ~96 | 9 | Total effectively connected income |
| f1_70 | ~72 | 10 | Adjustments from Schedule 1 |
| f1_71 | ~60 | 11a | Adjusted gross income |

### Page 2 (Tax Computation and Payments)

| Field | Line | Description |
|-------|------|-------------|
| f2_01 | 11b | AGI from page 1 |
| f2_03 | 12 | Itemized deductions |
| f2_07 | 15 | Taxable income |
| f2_09 | 16 | Tax |
| f2_11 | 18 | Tax after credits |
| f2_15 | 22 | Other taxes |
| f2_16 | 23a | Tax on income not effectively connected (Schedule NEC) |
| f2_19 | 23d | Total NEC tax |
| f2_20 | 24 | Total tax (Line 22 + Line 23d) |
| f2_21 | 25a | Federal tax withheld (W-2 Box 2) |
| f2_35 | 33 | Total payments |
| f2_36 | 34 | Overpayment |
| f2_37 | 35a | Refund amount |

### Common Errors to Watch

- **f1_50 (Line 1h)**: Often gets a duplicate of wages. Should only have "other earned income" not reported elsewhere.
- **f1_63 (Line 5b)**: Contractor income sometimes lands here. Contractor income goes on Schedule 1 → Line 8.
- **f1_65 (Line 6)**: Reserved line. Must be empty. AGI sometimes gets placed here by mistake.
- **f1_53 (Line 1k)**: Often left blank when treaty exemption applies. Must show treaty amount if Form 8833 is filed.
- **f1_71 (Line 11a)**: Often left blank. Must have AGI.

## Form 8843

Field name pattern: `topmostSubform[0].Page1[0].f1_XX[0]`

| Field | Line | Description |
|-------|------|-------------|
| f1_04 | 1a (First) | First name |
| f1_05 | 1a (Last) | Last name |
| f1_06 | 1b | SSN or ITIN |
| f1_07 | - | Country of nationality |
| f1_08 | - | US address |
| f1_09 | - | Date of entry (MM/DD/YYYY) |
| f1_10 | 2 | Visa type and status |
| f1_11 | 3a | Country of tax residence |
| f1_12 | 3a | Country of citizenship |
| f1_13 | 3b | Passport number |
| f1_14 | 4a (current) | Days present current year |
| f1_15 | 4a (prior 1) | Days present 1st prior year |
| f1_16 | 4a (prior 2) | Days present 2nd prior year |
| f1_17 | 4b | Days of current year to exclude from substantial presence test |
| f1_26 | Part III, 8a | University/institution name and location |
| f1_27 | Part III, 8b | Director of academic program name and address |
| f1_28 | Part III, 9a | Current nonimmigrant status |
| f1_32 | Part III, 10a | Prior year 1 status |
| f1_33 | Part III, 10a | Prior year 2 status |

### Checkboxes
| Field | Value | Meaning |
|-------|-------|---------|
| c1_2[1] | /2 | "Yes" for question about immigration status change |
| c1_3[1] | /2 | "Yes" for teacher/trainee question (varies by form version) |

### Critical Rule
**Line 4b must equal the days in Line 4a (current year)**. Common error: setting 4b to 365 when the person was only present for fewer days (e.g., 338 if they departed before year-end).

## Schedule NEC

Field name pattern: `form1040-NR[0].Page1[0].Table_NatureOfIncome[0].LineXX[0].f1_XX[0]`

Organized by income type rows and columns (nature, country, rate, amount, tax):

| Income Type | Line | Amount Field | Rate Field | Tax Field |
|-------------|------|-------------|------------|-----------|
| Dividends | 2 | amount column | rate column | tax column |
| Capital gains | 7 | amount column | rate column | tax column |
| Total | 12 | - | - | total NEC tax |

Rates for US-China Treaty:
- Dividends: 10% (Article 9(2))
- Capital gains: 30% (IRC 871(a)(2), no treaty reduction)
- Interest from bank deposits: EXEMPT (IRC 871(i)(2)(A)) — do not report

## Schedule OI (Other Information)

Key fields for days-of-presence and treaty claims. Field names vary but critical data:

| Question | Content |
|----------|---------|
| Visa type | Current nonimmigrant visa (e.g., F-1) |
| Country | Country of citizenship and tax residence |
| Days present | Current year, 1st prior, 2nd prior (must match Form 8843) |
| Treaty claim | Article number and country |
| Departure date | Date of last departure if applicable |

## Form 8833 (Treaty-Based Return Position)

Key fields:
- Treaty country (e.g., China)
- Treaty article (e.g., Article 20(c))
- IRC provision (e.g., IRC 871(b))
- Exemption amount (e.g., $5,000)
- Explanation of treaty position

## Form 8889 (HSA)

Key fields:
- Line 2: HSA contributions (from 5498-SA Box 2 minus employer contributions)
- Line 9: Employer contributions (W-2 Code W)
- Line 13: HSA deduction (Line 2 minus Line 9, or limited amount)

Note: For NRA filers, HSA rules can be complex if presence spans multiple countries. Verify eligibility for months of US residency.

## Schedule 1 (Additional Income and Adjustments)

Key fields for NRA:
- Part I, Line 8h (or appropriate sub-line): Other income (contractor/1099-NEC income)
- Part I, Line 10: Total additional income → flows to 1040-NR Line 8
- Part II, Line 13: HSA deduction (from Form 8889)
- Part II, Line 26: Total adjustments → flows to 1040-NR Line 10
