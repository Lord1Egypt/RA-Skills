---
name: roofing-estimate-builder
description: Builds a line-item US roofing estimate with tear-off, decking, flashing, waste and labor, plus the notice and deposit terms the state requires. Use when the user asks for roofing estimate template, roof replacement estimate, roofing bid sheet us. For US residential roofing contractors and the production managers who write their bids.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Roofing Estimate Builder

**Builds a line-item US roofing estimate with tear-off, decking, flashing, waste and labor, plus the notice and deposit terms the state requires.** Written for US residential roofing contractors and the production managers who write their bids.

Use this skill when someone asks for:

- roofing estimate template
- roof replacement estimate
- roofing bid sheet us
- roofing line item estimate
- roofing contractor quote

---

## The job

Sales reps price roofs from a per-square habit, so the measurement, the waste factor and the flashing detail never reach the estimate and the change orders start on day two.

## What you get

1. Collect the roof plan, the field measurement, the number of existing layers and the access and staging conditions.
2. Break the scope into tear-off, decking repair, underlayment, shingle, flashing, ventilation, labor and disposal.
3. Add the waste factor, the labor hours and the change-order triggers such as decking replacement or concealed rot.
4. Add the deposit terms, the mechanic's lien notice language and the permit requirement for the job's jurisdiction.

Output contract:

- estimate - line items with material, quantity, unit, unit price, labor hours and line total
- change_order_triggers - the conditions that change the price, each with its unit price
- deposit_terms - deposit amount, what it covers and the balance schedule
- notices - lien notice and permit language for the state the job is in
- open_items - measurements, code items or site conditions the roofer has to confirm

## US specifics that matter

- The FTC Cooling-Off Rule (16 CFR Part 429) gives buyers three business days to cancel a home improvement contract over $50 signed at their home, and roofing contracts written on the kitchen table fall under it.
- Mechanic's lien protection is state-specific: Texas Property Code Chapter 53 requires a notice before payment and a lien affidavit filed within 90 days after the work is performed and within 90 days after payment becomes due.
- Roofing contractor licensing is state-specific; some states license roofers through a state licensing board and others rely on local registration, so the license or registration number belongs on the contract.
- State sales tax on roofing is state-specific and often treats materials and labor differently, so the tax line has to follow the state treatment instead of one blended rate.
- The FTC treats a free estimate as an advertising claim: if a charge is deducted from the contract price, the offer has to say so in the ad.

## Guardrails (hard rules)

- Never invent a measurement, a roof square count, a labor hour or a waste factor; the estimate has to come from the user's own field measurements.
- Never promise a wind rating, a warranty class, an insurance discount or code compliance that the manufacturer or the building department has not confirmed.
- Never collect a deposit, email a homeowner or sign a contract; the contractor does that.
- Never present the estimate as a binding contract until the contractor adds the contract terms, the notices and the signature page.
- Never publish a line item that prices work the contractor has not agreed to perform.

## Quickstart

### 1. Fill in the brief

`templates/roofing-job-brief.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/render_roofing_estimate.py --input roofing-job-brief.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/roofing-contract-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Home improvement contract basics**

- FTC Cooling-Off Rule: a home improvement contract over $50 signed at the home gives the buyer three business days to cancel.
- State whether the document is a proposal or a contract and what happens after the customer accepts it.
- Deposit terms are custom and state-specific, so state what the deposit covers and when the balance comes due.
- Licensing and insurance information belongs on the contract: license number, insurance carrier and coverage.

**Lien notices and deadlines**

- Texas Property Code Chapter 53 sets a prepayment notice and a lien affidavit deadline of 90 days after the work and 90 days after payment is due.
- Other states use different forms and different deadlines, so the notice language is set by state and not by the contractor's template.
- Keep the signed contract, the payment schedule and the notice copies in the job file.
- Payment on a lien is risky for the owner, so the notice is a required step and not a formality.

**Materials, tax and permits**

- The waste factor covers extra material for cuts and overlaps, and the percentage used belongs on the estimate.
- State sales tax on roofing materials and labor is state-specific and the two are often treated differently.
- Many counties require a roofing permit, and some require a disposal or recycling record for the old shingles.
- Flashing, decking and ventilation are the three lines that drive change orders.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/roofing-contract-rules.md` - US roofing estimate and contract rules
- `templates/roofing-job-brief.yaml` - the brief to fill in
- `scripts/render_roofing_estimate.py` - the working script

## Verify the bundle

```bash
python3 scripts/render_roofing_estimate.py --input roofing-job-brief.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
