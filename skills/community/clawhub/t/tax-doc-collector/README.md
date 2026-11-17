# Tax Doc Collector 🧾💰

Stop the April panic. Track deductible expenses year-round with smart IRS
categorization, real-time tax savings estimates, audit risk flags, and
one-command export to Schedule C / Schedule A format.

## The Problem

Every year, the same nightmare:
- **"Where are my receipts?"** — a shoebox, a email folder, a vague memory
- **"Was that deductible?"** — you forgot what counts
- **"How much did I spend on X?"** — no running total
- **"My accountant charges $500/hr to sort this"** — because you didn't
- **"Did I miss deductions?"** — you probably did, losing real money
- **Audit fear** — no documentation, no mileage log, no proof

## The Solution

A year-round expense tracker purpose-built for tax deductions:

1. Log expenses the moment they happen (30 seconds)
2. Automatic IRS category matching (Schedule C and Schedule A)
3. Real-time savings estimate: "That $45 receipt saves you $10.80 in taxes"
4. Audit risk scoring: flagged before the IRS flags them
5. One-command export for your accountant or tax software

## Features

- 🧾 **Expense logging** — amount, merchant, category, date, notes
- 🏷️ **IRS categories** — pre-mapped to Schedule C and Schedule A line items
- 🚗 **Mileage tracking** — current IRS standard mileage rates
- 🏠 **Home office** — simplified or detailed method calculation
- 💰 **Real-time savings** — see tax impact of every deduction
- ⚠️ **Audit risk** — flags statistically risky deductions
- 📊 **Year-to-date summary** — running totals by category
- 📤 **Export** — Schedule C, Schedule A, or CSV format
- 🔍 **Searchable** — find any expense by category, merchant, or date
- 📅 **Multi-year** — separate tracking per tax year

## Quick Start

```bash
# Set up (once per year)
python3 scripts/tax_docs.py setup --bracket 24

# Log expenses as they happen
python3 scripts/tax_docs.py add --amount 45.99 --category "office supplies" --merchant "Staples"
python3 scripts/tax_docs.py add --amount 120.00 --category "meals" --merchant "Olive Garden" --note "client lunch"
python3 scripts/tax_docs.py add-mileage --miles 32 --purpose "client meeting"

# Check progress
python3 scripts/tax_docs.py summary

# At tax time
python3 scripts/tax_docs.py export schedule-c
```

## IRS Categories Included

### Schedule C (Business)
Advertising, Car/Truck, Commissions, Contract Labor, Depreciation,
Employee Benefits, Insurance, Interest, Legal/Professional, Office Expense,
Pension, Rent/Lease, Repairs, Supplies, Taxes/Licenses, Travel, Meals,
Utilities, Wages

### Schedule A (Personal Itemized)
Medical/Dental, State/Local Taxes, Property Tax, Mortgage Interest,
Charity (Cash), Charity (Non-Cash), Casualty Loss, Miscellaneous

See [`references/irs-categories.md`](references/irs-categories.md) for details.

## Requirements

- Python 3.6+ (stdlib only)

## License

MIT © Denis Voronin
