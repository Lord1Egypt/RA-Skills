# Common Schedules — Key Fields and Pitfalls

Field-level guidance for the most frequently used citizen/RA schedules. This is not exhaustive — it covers the fields where mistakes most commonly happen.

For NRA-specific form fields (1040-NR, 8843, Schedule NEC/OI, 8833), see `references/form-field-maps.md` in this skill.

## Form 1040 — Key Lines

| Line | Description | Source |
|------|-------------|--------|
| 1a | Wages, salaries, tips | Sum of all W-2 Box 1 |
| 2a | Tax-exempt interest | 1099-INT Box 8 |
| 2b | Taxable interest | 1099-INT Box 1 |
| 3a | Qualified dividends | 1099-DIV Box 1b |
| 3b | Ordinary dividends | 1099-DIV Box 1a |
| 7 | Capital gain or loss | Schedule D Line 16 (or Line 21 if using worksheet) |
| 8 | Other income from Schedule 1 | Schedule 1 Line 11 |
| 9 | Total income | Sum of Lines 1z through 8 |
| 10 | Adjustments from Schedule 1 | Schedule 1 Line 26 |
| 11 | AGI | Line 9 - Line 10 |
| 13 | Deductions | Standard deduction or Schedule A Line 17 |
| 15 | Taxable income | Line 11 - Line 13 - Line 14 |
| 16 | Tax | From tax table, Qualified Dividends worksheet, or Schedule D worksheet |
| 24 | Total tax | After credits and other taxes |
| 25a | Federal tax withheld from W-2s | Sum of all W-2 Box 2 |
| 33 | Total payments | |
| 34 | Overpayment (refund) | Line 33 - Line 24 |
| 37 | Amount owed | Line 24 - Line 33 |

**Common errors**: Forgetting to sum multiple W-2s for Line 1a. Missing Line 7 when Schedule D applies. Putting adjustments on Line 8 instead of Line 10.

## Schedule C — Profit or Loss from Business

| Line | Description | Notes |
|------|-------------|-------|
| 1 | Gross receipts | Sum of 1099-NEC amounts |
| 7 | Gross income | Line 1 - returns/allowances - COGS |
| 8-27 | Expenses | Business expenses (categorized) |
| 28 | Total expenses | |
| 31 | Net profit or loss | Line 7 - Line 28 → goes to Schedule 1 Line 3 |

**Common errors**:
- Including personal expenses as business expenses
- Forgetting the home office deduction (simplified: $5/sq ft, max 300 sq ft = $1,500)
- Not separating meals (50% deductible) from other expenses

## Schedule SE — Self-Employment Tax

| Line | Description | Notes |
|------|-------------|-------|
| 2 | Net earnings | From Schedule C Line 31 (or combined if multiple Sch C's) |
| 4 | 92.35% of Line 2 | Only 92.35% of net earnings are subject to SE tax |
| 12 | SE tax | 15.3% of Line 4 (12.4% Social Security up to $176,100 for 2025 + 2.9% Medicare) |
| 13 | Deductible part of SE tax | 50% of Line 12 → Schedule 1 Line 15 |

**Critical**: SE tax applies when net self-employment income ≥ $400. This is separate from income tax — many first-time freelancers miss it entirely.

**Common errors**:
- Forgetting to file Schedule SE at all
- Not taking the 50% SE tax deduction on Schedule 1 (it's above the line, reducing AGI)
- Applying the Social Security wage cap incorrectly when the filer also has W-2 wages

## Schedule D — Capital Gains and Losses

| Line | Description | Notes |
|------|-------------|-------|
| 1b | Short-term from Form 8949 Box A | Reported to IRS, basis reported |
| 2 | Short-term from Form 8949 Box B | Reported to IRS, basis NOT reported |
| 3 | Short-term from Form 8949 Box C | NOT reported to IRS |
| 7 | Net short-term gain/loss | Sum of Lines 1-6 |
| 8b | Long-term from Form 8949 Box D | Reported, basis reported |
| 9 | Long-term from Form 8949 Box E | Reported, basis NOT reported |
| 10 | Long-term from Form 8949 Box F | NOT reported |
| 15 | Net long-term gain/loss | Sum of Lines 8-14 |
| 16 | Combined | Line 7 + Line 15 → 1040 Line 7 |

**Common errors**:
- Using proceeds as gain (forgetting to subtract cost basis)
- Not adjusting for wash sales (1099-B Box 1g)
- Ignoring the **$3,000 loss limit** — net losses over $3,000 carry forward to next year
- Mixing short-term and long-term transactions in the wrong Form 8949 box

## Schedule A — Itemized Deductions

Only file if total exceeds the standard deduction.

| Line | Description | Cap/Limit |
|------|-------------|-----------|
| 1-4 | Medical expenses | Only amount exceeding 7.5% of AGI |
| 5a | State/local income tax | SALT cap: $10,000 total ($5,000 MFS) |
| 5b | State/local sales tax | Alternative to 5a (choose one) |
| 5c | Real estate taxes | Included in SALT cap |
| 8a | Home mortgage interest | On up to $750K of debt ($375K MFS) |
| 11-14 | Gifts to charity | Cash: up to 60% of AGI. Property: up to 30% of AGI. |
| 17 | Total itemized deductions | → 1040 Line 13 |

**Common errors**:
- Exceeding the $10,000 SALT cap without realizing it
- Deducting mortgage interest on a home equity loan used for non-home purposes (not deductible post-TCJA)
- Claiming charitable contributions without proper documentation (receipts for $250+)

## Schedule B — Interest and Dividends

Required when interest or dividends exceed $1,500.

| Part | Lines | Source |
|------|-------|--------|
| I | Lines 1-4 | List each payer and interest amount from 1099-INT |
| II | Lines 5-6 | List each payer and dividend amount from 1099-DIV |

**Common errors**: Forgetting to include interest from multiple bank accounts. Not reporting tax-exempt interest separately (it goes on 1040 Line 2a, not Schedule B).

## Form 8889 — HSA

| Line | Description | Source |
|------|-------------|--------|
| 2 | HSA contributions you made | 5498-SA Box 2 minus employer contributions |
| 9 | Employer contributions | W-2 Box 12 Code W |
| 13 | HSA deduction | Line 2 - excess over limit → Schedule 1 Line 13 |
| 14a | Total distributions | 1099-SA Box 1 |
| 15 | Distributions for medical expenses | (user must track this) |
| 17a | Taxable HSA distributions | If 14a > 15 |

**2025 contribution limits**: $4,300 (self-only), $8,550 (family). Add $1,000 if 55+.

**Common errors**:
- Double-counting employer contributions (W-2 Code W already includes them — don't add again on Line 2)
- Not filing Form 8889 when you have an HSA — it's required even if you made no contributions, as long as you had a balance
- Forgetting the 20% penalty on non-medical distributions under age 65
