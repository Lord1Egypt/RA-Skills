---
name: radon-test-interpreter
description: Use when a radon test result came back (home purchase, basement apartment, kid's room, workplace), when you're deciding between retesting and mitigation, or pricing radon negotiation in a real-estate deal — converts pCi/L↔Bq/m³, interprets single or multiple readings against EPA 4.0 pCi/L and WHO 100 Bq/m³ action levels, estimates lifetime lung-cancer risk by smoking status from the EPA risk tables, flags invalid test conditions (short duration, wrong season, no closed-house protocol), and prices mitigation vs retest vs monitor with the real-estate contingency play included.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [radon, home-safety, air-quality, lung-cancer-risk, epa, real-estate]
---

# Radon Test Interpreter

## Overview
Radon is the second-leading cause of lung cancer (~21,000 deaths/yr in the US), every home should be tested, and yet the result — a single number in pCi/L — arrives with no interpretation people can act on. Is 3.8 safe because it's "under 4"? Is a winter charcoal test trustworthy? Does the smoker in the house change the answer? Real-estate deals compress this further: a 48-hour charcoal canister during closing, a seller saying "basement's unfinished, nobody's down there," and a buyer with 10 days to decide.

This skill turns readings into verdicts with the actual risk arithmetic: EPA action levels (4.0 pCi/L mitigate, 2.0–3.9 consider), WHO's stricter 100 Bq/m³ (~2.7 pCi/L) reference, unit conversion (1 pCi/L = 37 Bq/m³), the EPA lifetime lung-cancer risk tables by smoking status, and test-validity checks (duration vs device class, closed-house conditions, seasonal bias). It then prices the decision: mitigation ($800–$2,500 install, $100–$250/yr operation) vs long-term retest vs monitor, and the real-estate move — asking for a credit at least equal to mitigation cost, with the retest protocol that survives escrow.

## When to Use
- A radon number came back from a home test, lab, or inspection contingency and "what does it mean" needs a real answer
- Basement/ground-floor bedroom, child's playroom, or home office — occupancy changes the urgency read
- A smoker or ex-smoker lives in the home (risk multiplies several-fold)
- Real-estate transaction: interpreting a 48-hour test and negotiating mitigation
- Post-mitigation verification or the 2-year retest cycle

**Don't use for:** workplace regulated-worker exposure programs (different guidance), radon in water (needs water testing), or DIY mitigation design beyond the references' overview — active soil depressurization is licensed-territory in many states and always worth a pro quote.

## Quick Start
```bash
# A single charcoal canister result, winter, tested properly
python3 scripts/radon_verdict.py readings 5.2 --duration-days 3 --device charcoal \
    --season winter --closed-house yes --occupants basement-bedroom --smokers 1

# Two devices in different rooms, averaged
python3 scripts/radon_verdict.py readings 4.4 3.9 5.6 --duration-days 2 --device charcoal --closed-house yes

# Real-estate mode: 6.1 pCi/L on the inspection contingency
python3 scripts/radon_verdict.py realestate --reading 6.1 --mitigation-cost 1400

# Unit conversions and risk lookup alone
python3 scripts/radon_verdict.py convert 4.0
python3 scripts/radon_verdict.py risk --pci 3.5 --smoker

python3 scripts/radon_verdict.py --demo
```

## The Interpretation Ladder
| Average | Verdict | Action |
|---|---|---|
| ≥ 8.0 pCi/L | MITIGATE-URGENT | fix now; if smoker in home, treat as urgent health issue, consider relocating sleeping arrangements off the lowest level until post-mitigation retest |
| 4.0–7.9 | MITIGATE | EPA action level; get bids (ASD $800–$2,500); retest 10 days–2 yr after install |
| 2.0–3.9 | RETEST-LONG-TERM, CONSIDER MITIGATING | WHO reference (~2.7) sits here; run a 91+ day alpha-track/LAB test to confirm |
| < 2.0 | MONITOR | retest every 2 yr and after renovations/HVAC changes |
| any short-term result with invalid conditions | INVALID-RETEST | see validity gates below |

## Test-Validity Gates (checked before any verdict)
1. **Duration vs device**: charcoal/liquid scintillation 2–7 days; continuous monitor ≥ 48 h; alpha-track/E-perm long-term 91–365 days. A "48-hour" result outside its device window is noise.
2. **Closed-house conditions**: 12 h before + during short-term tests (windows closed, normal entry/exit). A "we aired the house out" test reads artificially low.
3. **Season**: short-term winter results run 1–2 pCi/L high (stack effect), summer low. Winter short-term ≥ 4 → assume real; summer short-term < 4 → don't clear the house, confirm long-term.
4. **Lowest livable level tested** — the basement that isn't finished today is the bedroom someone finishes in 3 years.

## Common Pitfalls
1. **"Under 4 is safe."** 4.0 pCi/L carries ~7/1000 lifetime lung-cancer risk for a never-smoker — more than many regulated carcinogens. WHO acts at ~2.7.
2. **Averaging away a high room.** Two basement readings plus a first-floor reading produce a diluted average; interpret the lowest livable level, not the whole-house mean. The script flags spread > 2 pCi/L as stratification.
3. **Trusting one 48-hour charcoal canister in July.** Seasonal + weather variance is real; short-term results are screening tools, long-term tests are the confirmation.
4. **Post-mitigation trust without retest.** Verify < 4.0 (ideally < 2.0) 10 days–2 yr after install; systems fail (fan death, crawlspace bypass).
5. **Real-estate: seller's "we'll credit $500."** Mitigation is $800–$2,500 plus post-test verification; the ask is itemized in the script's letter.

## Verification Checklist
- [ ] Units confirmed (pCi/L vs Bq/m³) — conversions in output
- [ ] Device/duration/season/closed-house answers gathered before trusting the verdict
- [ ] Lowest livable level identified and used for the verdict
- [ ] Smoker status captured — changes the urgency framing, not the EPA action level
- [ ] Post-mitigation retest scheduled (2-yr cadence after that)

## Example
Winter charcoal canister: 5.2 pCi/L, 3 days, closed-house honored, basement bedroom occupied, one smoker in the home. Verdict: **MITIGATE** (EPA ≥ 4.0), risk ≈ 64/1000 lifetime for the smoker (vs ~7/1000 never-smoker at this level) — and the real-estate variant asks for a $1,400 credit with a licensed-mitigator retest clause. Summer result of 2.9 → RETEST-LONG-TERM, not "clear."
