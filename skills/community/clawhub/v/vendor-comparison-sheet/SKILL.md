---
name: vendor-comparison-sheet
description: Scores vendors against weighted criteria and builds a total-cost comparison sheet for US purchasing and operations teams. Use when the user asks for vendor comparison sheet, supplier evaluation scorecard, procurement comparison table. For US purchasing agents, operations managers and small business owners choosing a service or supply vendor.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Vendor Comparison Sheet

**Scores vendors against weighted criteria and builds a total-cost comparison sheet for US purchasing and operations teams.** Written for US purchasing agents, operations managers and small business owners choosing a service or supply vendor.

Use this skill when someone asks for:

- vendor comparison sheet
- supplier evaluation scorecard
- procurement comparison table
- total cost of ownership vendor
- vendor bid comparison template

---

## The job

Purchasers compare vendors on the headline price alone, so setup fees, minimum order quantities, lead times and warranty terms only surface after the contract is signed.

## What you get

1. Collect the requirement, the budget range, the decision date and the name of each vendor on the shortlist.
2. Normalize every quote into the same columns: unit price, setup fee, recurring fee, minimum order, lead time, warranty and returns window.
3. Set the weights with the buyer before anything is scored, so the ranking reflects the buyer's priorities and not the template's.
4. Score each vendor against the weighted criteria and show the ranking with the raw numbers next to every score.
5. List the open items that still block the decision, such as a missing quote, an unconfirmed warranty term or a sample that has not been tested.

Output contract:

- comparison_table - one row per vendor with the normalized cost, lead time, warranty and returns columns
- ranking - the weighted score for each vendor and the criteria that drove it
- twelve_month_cost - the total cost of each option including setup, recurring fees and the expected volume
- open_items - the missing data points that still block the decision, each with an owner and a due date
- decision_note - a short note on what the ranking settles and what it does not, for the buyer's sign-off

## US specifics that matter

- Section 5 of the FTC Act (15 USC 45) treats unfair or deceptive acts or practices as unlawful, so a performance or savings claim a vendor makes has to be true and documented before the sheet repeats it.
- The Magnuson-Moss rules in 16 CFR part 702 require a seller or warrantor to make written warranty terms available before the sale of a consumer product priced over $15, so warranty terms belong in the comparison and not in a footnote.
- There is no federal 30-day return right for general retail purchases, a 30-day window is a store policy, and state law can set different rules, for example California Civil Code 1723 for unopened merchandise.
- US postal addresses use a five-digit ZIP code with an optional ZIP+4 extension and US phone numbers in the North American Numbering Plan are ten digits with a three-digit area code, so quote data should be normalized to those formats before it is compared.
- Services paid to a vendor of $600 or more in a year are reported on Form 1099-NEC, and a Form W-9 collects the vendor's taxpayer identification number, so a service comparison tracks the paperwork finance needs.
- FTC guidance treats an offer of free shipping or free setup as deceptive unless the components that normally carry the price are genuinely free, so a free row in the sheet needs its terms attached.

## Guardrails (hard rules)

- Never fill a blank cell with an estimated price, lead time or warranty term; leave it unknown and move it to the open items.
- Never share one vendor's quoted pricing, proposal or contract terms with another vendor.
- Never send the sheet to a vendor, accept a quote, sign an agreement or place an order; the buyer does those steps.
- Never call a vendor the best, the cheapest or the safest in customer-facing copy; the sheet ranks the criteria the buyer set.

## Quickstart

### 1. Fill in the brief

`templates/vendor-comparison.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_vendors.py --input vendor-comparison.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/vendor-comparison-us.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**What the comparison has to prove**

- Section 5 of the FTC Act (15 USC 45) is the standard for any claim the sheet repeats to a customer.
- Keep each vendor's claim attached to the document it came from, with the date it was captured.
- A price that excludes shipping, setup or restocking is not a total cost, and the sheet has to say so.
- A 30-day return window is a store policy and not a federal right, so record the seller's own terms.

**Warranty terms and pre-sale availability**

- 16 CFR part 702 requires written warranty terms to be available to a buyer before the sale of a consumer product priced over $15.
- 16 CFR part 239 is the FTC's guide to advertising warranties, and misrepresenting warranty terms violates Section 5.
- A service contract sold alongside the product is a separate line in the comparison.
- Compare the exclusion list and the claim process, not only the length of the warranty.

**Formats to normalize before scoring**

- US postal addresses: street, city, two-letter state, five-digit ZIP and ZIP+4 when it is known.
- US phone numbers: ten digits with a three-digit area code, with any extension in a separate field.
- Money in USD, with the tax treatment and the payment terms on a different line from the unit price.
- Lead times in business days and warranty lengths in months, so the columns compare like with like.

**Where the state layer changes the answer**

- Sales tax nexus and rates differ by state, so a comparison states the state it assumes.
- Certificate of insurance and workers compensation requirements vary by state and by buyer.
- A service vendor paid $600 or more in a year needs a Form W-9 and appears on Form 1099-NEC.
- Flag any vendor term that the buyer's own attorney has to review before the sheet circulates.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/vendor-comparison-us.md` - US vendor comparison rules and data formats
- `templates/vendor-comparison.csv` - the brief to fill in
- `scripts/score_vendors.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_vendors.py --input vendor-comparison.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
