# Major Items Reference

Use these canonical `major_items` keys when normalizing returns before running the script.

| Key | Typical Source | Notes |
|---|---|---|
| `wages` | Form 1040 line 1z | Wages, salaries, tips from Forms W-2.
| `wages_subject_to_social_security` | W-2 box 3 total | Optional; improves Schedule SE cross-check.
| `taxable_interest` | Form 1040 line 2b | Taxable interest only.
| `ordinary_dividends` | Form 1040 line 3b | Ordinary dividends.
| `qualified_dividends` | Form 1040 line 3a | Presence implies preferential tax computation.
| `capital_gain_or_loss` | Form 1040 line 7 | Net capital gain/loss.
| `business_income` | Schedule 1 line 3 | Optional high-level business-income marker.
| `self_employment_net_earnings` | Schedule SE net earnings | Use positive net earnings for tax approximation.
| `schedule_se_tax` | Schedule 2 / Schedule SE result | SE tax amount carried to 1040 total tax flow.
| `unemployment_compensation` | Schedule 1 line 7 | Taxable unemployment income.
| `other_income` | Schedule 1, other items | Any other taxable income not split elsewhere.
| `total_income` | Form 1040 line 9 | Total income.
| `adjustments_to_income` | Form 1040 line 10 | Schedule 1 adjustments.
| `agi` | Form 1040 line 11 | Adjusted gross income.
| `deduction_amount` | Form 1040 line 12 | Standard or itemized deduction amount.
| `qbi_deduction` | Form 1040 line 13 | Qualified business income deduction.
| `taxable_income` | Form 1040 line 15 | Taxable income.
| `tax_before_credits` | Form 1040 line 16 | Computed tax before credits.
| `nonrefundable_credits` | Form 1040 line 20 | Nonrefundable credits total.
| `ctc_claimed` | Schedule 8812 nonrefundable portion | Claimed CTC used as nonrefundable credit.
| `actc_claimed` | Schedule 8812 refundable portion | Additional child tax credit.
| `other_taxes` | Form 1040 line 23 | Other taxes.
| `additional_medicare_tax` | Form 8959 result | Additional Medicare tax component.
| `total_tax` | Form 1040 line 24 | Total tax.
| `withholding` | Form 1040 line 25d | Federal withholding total.
| `estimated_tax_payments` | Form 1040 line 26 | Estimated payments and prior-year overpayment applied.
| `refundable_credits` | Form 1040 line 31 total | Refundable credits total.
| `other_payments` | Payment line items not above | Optional catch-all payment bucket.
| `total_payments` | Form 1040 line 33 | Total payments.
| `refund` | Form 1040 line 35a | Refund amount.
| `amount_owed` | Form 1040 line 37 | Amount you owe.
| `earned_income` | Earned-income figure for ACTC tests | Usually wage + SE earned income.

## Normalization Tips

- Keep currency values as numbers (no `$` signs) when possible.
- Preserve one record per tax year.
- Include historical years only if they are complete enough for year-over-year comparison.
- If a key is unknown, omit it; the checker skips missing-key tests rather than forcing zero.