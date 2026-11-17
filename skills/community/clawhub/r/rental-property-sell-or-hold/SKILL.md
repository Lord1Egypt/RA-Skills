---
name: rental-property-sell-or-hold
description: >
  Review and analyze a personal sell-or-hold decision for rental property
  against a stock or fixed-income alternative. Use when the user asks whether
  to sell rental condos or houses and move the money into investments, when
  comparing rent yield with fixed income, when modeling a 3-year sell-or-hold
  scenario with break-even returns, or when checking a personal investment
  assessment document. Covers Canadian tax concepts (Capital Cost Allowance (CCA), terminal loss,
  principal residence, personal-use losses) where the owner is a Canadian
  resident. Triggers: sell or hold, rental yield, net yield, cash flow,
  break-even, condo, strata fee, property tax, CCA, fixed income, ETF,
  concentration, 售房, 持有, 租金收益率, 固定收益.
---

# Rental property sell-or-hold review

Disclaimer (just for fun): this skill is a thinking toy. It is not financial, tax, or legal advice. Verify every number with a real appraisal, a real tax adviser, and a real market source before you act on it.

This skill turns a personal sell-or-hold question into a clear, checkable document. It never invents numbers. Every figure comes from the owner, a named source, or a stated assumption.

## Privacy rule (applies first)

This skill is generic. Never write the owner's real figures, names, addresses, unit numbers, account sizes, or tax identifiers into this skill or into any shared file. Use placeholders such as `<unit A purchase price>`. The owner's real values belong only in their own private document. Ask for the values in the session, use them in that document only, and never copy them here.

## Step 1: Gather facts and label each one

Build a facts table. For each row, record the value, the unit or asset it belongs to, and the source (owner, agent, appraisal, calculated).

Required facts for each property:
- Purchase price, including purchase costs and tax
- Current estimated value and who estimated it (agent estimate is not an appraisal)
- Monthly rent and whether parking or other items are included
- Annual property tax, for the current year and an earlier year (to measure the trend)
- Monthly strata or management fee (ask whether it is monthly or annual)
- Annual maintenance estimate
- Agency or leasing fee and its frequency (for example, half a month's rent, once a year)
- Mortgage balance (zero is a valid answer; confirm it)
- Vacancy history over the last 12 months
- Occupancy: rented, self-occupied, or vacant

Ask the owner to confirm each uncertain value. Never silently fix a value that conflicts with another value in the same document. Flag it and ask.

## Step 2: Compute cash flow

Use this structure for each property and for the combined total:

| Item | Unit A | Unit B | Combined |
|---|---|---|---|
| Gross rent (monthly × 12) | | | |
| Strata (monthly × 12) | | | |
| Property tax (annual) | | | |
| Maintenance (annual, estimate) | | | |
| Agency fee (annual) | | | |
| Net before income tax | | | |

Gross yield = annual gross rent ÷ current estimated value. Net yield = net before income tax ÷ current estimated value. Compare the net yield with the pre-tax fixed-income rate the owner supplies.

Income tax on rent uses the owner's marginal rate, with Capital Cost Allowance (CCA, the tax depreciation deduction) applied. Leave tax out of the main figures unless you calculate it. Say so.

## Step 3: Model sell-or-hold over a fixed horizon

Default horizon: 3 years. The owner may hold one or more properties, and may sell one or more of them. The sell case covers the properties being sold. The hold case covers every property the owner keeps. Assumptions to state in the document:
- Selling cost, as a percentage of the sale price (default placeholder 5%, not checked against current fees)
- Split of the sale proceeds between fixed income and equity ETF (use the owner's split)
- Fixed-income rate (owner's figure, pre-tax)
- Rent held flat, or a stated growth rate. State whether growth in rent, strata, property tax, and maintenance is included.
- Tax excluded unless calculated

For each scenario, compute:
- Hold: net rent over the horizon for every property kept, plus each kept property's value after selling cost.
- Sell now: fixed-income part grown at its rate, plus the equity part grown at the scenario return.

Then compute the break-even equity return: the return the equity part must reach so that selling equals holding, for each property scenario (flat, up, down). Show it in a table, not only in prose.

Break-even formula (horizon of 3 years):

Break-even annual return = ((Hold end value − Fixed-income end value) ÷ Equity starting value)^(1/3) − 1

Where:
- Fixed-income end value = Fixed-income starting value × (1 + fixed-income rate)^3
- Hold end value = net rent over the horizon for all kept properties + sum of each kept property's value × (1 − selling cost)
- Equity starting value = the ETF part of the sale proceeds

Example with placeholders: if Hold end value is H, fixed-income end value is F, and equity starting value is E, the break-even return is ((H − F) ÷ E)^(1/3) − 1. Recompute this for each property scenario.

Write one plain-language reading sentence after the table: which scenario wins, and what must be true for it to win.

## Step 4: Check equity concentration

Liquid assets include cash, fixed income, and stocks or ETFs. Exclude the owner's own residence and any non-liquid property.

Show a table with one row per option:
- Today (no sale)
- Each sell option
- Hold

Columns: liquid assets, equity (stocks and ETFs only), fixed income. Do not add an "equity share" column when it is the same in every row. Put that fact in one note under the table.

If the split keeps the mix unchanged, say so. Selling then moves wealth, it does not reduce risk. Only a different split changes the risk.

## Step 5: Check the stock holdings

Ask what the equity part holds: a broad index ETF, a sector ETF, or individual stocks. Do not assume sector concentration. Record the owner's answer.

For past returns, ask whether the stated return is for the whole portfolio or for one part. If it is for a blended portfolio, compute what the equity part must have earned, given the fixed-income assumption. Say that this is an implied figure, not a measured one.

For historical drawdowns, use a table with a source and a date for every number. Use calendar-year and peak-to-end figures separately. Note when sources disagree. Do not state a range from memory.

Do not present a past return as a forecast.

## Step 6: Tax checks (Canadian resident)

Check these points and mark each as "to confirm with a tax adviser":
- Whether CCA was claimed on the rental property. If so, a sale at a loss may create a terminal loss that is treated differently from a capital loss. If CCA was not claimed, the loss may be a capital loss.
- Whether a capital loss offsets only capital gains, and whether it carries forward.
- Whether a self-occupied home qualifies for the principal residence exemption.
- Whether a loss on personal-use property is deductible. In Canada it generally is not.
- Whether rent income is taxed at the marginal rate, and how interest is taxed.

Do not state a tax result as final. State the question and who should answer it.

## Step 7: Name the open items

End with a list of open items. Mark each one "Resolved" with the owner's confirmation, or leave it open. Do not drop an open item unless the owner resolves it.

Typical open items:
- Appraisal or realtor comparative market analysis for each property
- Floor area or size, if the document uses it
- Tax advice on loss treatment
- Confirmation of any value the owner marked uncertain

## Step 8: Write the document in both languages when asked

Use the same numbers in English and Chinese. Put the Chinese summary directly under the English paragraph it summarizes. Keep the Chinese short.

Use `\$` to escape dollar signs in markdown, so they do not render as math or emoji.

Write in one paragraph per line, no hard wrap, when the repo requires it.

## Step 9: Present options, then recommend one

Present at least three options with pros and cons. Include a "do nothing" option. Recommend one, and say which constraint decided it. Keep the recommendation tied to the owner's stated preferences (for example, keep a specific unit, avoid aggressive investment).

Do not present a single path as the only option.

## Step 10: Verify before finishing

- Recompute every table total from its inputs.
- Check that every number in the prose matches its table.
- Check that every percentage and break-even is consistent with its scenario table.
- Check that no personal data from the owner is present in any shared file.
- Confirm that open items match what the owner has resolved.

## Output checklist

- Facts table with a source for each row
- Cash flow table, with gross and net yield
- Scenario table, with a reading sentence
- Break-even table
- Concentration table, with one note on equity share
- Stock holdings note (what the equity part holds, with a placeholder until confirmed)
- Historical drawdown table with sources, if used
- Tax checks, marked for an adviser
- Options with pros and cons, and one recommendation
- Open items list
- Disclaimer
