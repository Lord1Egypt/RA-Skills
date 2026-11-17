# Warranty Vault

**When the dishwasher dies at month 20, know exactly what still covers it — manufacturer warranty, extended plan, credit-card perk, or statutory consumer rights — and get the claim letter drafted.**

People forfeit recoverable money constantly: an appliance fails inside the UK's 6-year Consumer Rights Act window, or inside an Amex +12-month perk, or inside an extended plan they forgot buying — and they bin it and buy new, because the purchase date, price, receipt location, and terms were un-marshalable at the moment of failure. Warranty Vault is the filing system that survives that moment.

## The real-world problem

- **Coverage is layered and invisible**: manufacturer (1–2 yr) + statutory rights (UK 6 yr / EU 2 yr / US state-dependent) + paid extended plans + credit-card extended-warranty perks (Visa Infinite +24 mo, Amex +12 mo). Nobody holds all that in their head for 40 purchases.
- **Evidence evaporates**: the receipt email is in one of five accounts, the serial is on a sticker on the back, the plan number came on a card you filed somewhere.
- **Timing is exploitable**: a fault you've tolerated for months is still a claim — until coverage lapses. Expiry alerts turn tolerated annoyances into money.
- **Claims fail on form**: statutory claims go against the *retailer* (not the manufacturer) in the UK/EU; the right citation and enclosures decide first-pass outcomes.

## What it does

```bash
# Record purchases as you make them (30 seconds each)
python3 scripts/warranty_vault.py add --id dishwasher --name "Bosch dishwasher" \
  --price 749 --purchased 2024-11-03 --warranty-mo 12 \
  --receipt "email order #3391" --card "Amex Gold" --jurisdiction UK

# The question that matters when something breaks
python3 scripts/warranty_vault.py covered dishwasher --jurisdiction UK
#   [LIVE] statutory rights (UK)        ends 2030-11-03
#          claim vs: RETAILER; bring: proof of purchase + fault inherent (presumed)

# Draft the claim letter with citations and enclosures checklist
python3 scripts/warranty_vault.py claim dishwasher --fault "Won't drain; E25" \
  --jurisdiction UK > claim.txt

# Quarterly audit: coverage table, expiring windows, unregistered items
python3 scripts/warranty_vault.py report
python3 scripts/warranty_vault.py expiring --days 90
```

The vault is plain JSON (`~/.warranty-vault.json`), fully exportable. `references/warranty-rights.md` carries the full layer model: jurisdiction rules (CRA 2015 burden-reversal at 6 months, EU 2019/771, US Magnuson-Moss + UCC), the card-perk table with eligibility caps, the filing workflow, letter templates, and category-by-category "is an extended plan worth it" math.

## Who needs this

- **Every household** — the vault pays for itself the first time one appliance claim succeeds
- **UK/EU consumers** with strong statutory rights they've never once invoked
- **Card perk holders** (premium Visas/Amex) leaving +12–24 months of coverage on the table
- **Landlords & property managers** tracking appliance coverage across units
- **Anyone selling used gear** — transferable remaining warranty is resale value

## Install

Python 3.8+ standard library only.

```bash
python3 scripts/test_warranty_vault.py   # verify the build
```

## License

MIT © Denis Voronin
