# Radon Test Interpreter

**A radon number arrived. Now what? Verdicts with real risk arithmetic — EPA/WHO action levels, lifetime lung-cancer risk by smoking status, test-validity gates, mitigation pricing, and the real-estate credit letter.**

## The problem
Radon causes ~21,000 US lung-cancer deaths a year — more than home fires and carbon-monoxide deaths combined — and the only action most families ever take is a $15 test whose result they can't interpret. "3.8" gets read as "passed" because it's under 4.0, even though 4.0 was a 1986 cost compromise, not a safety line, and the WHO acts at 2.7. Winter tests run high and summer tests run low; a single 48-hour charcoal canister has huge variance; smoker status multiplies risk several-fold; and in real-estate deals the number shows up mid-escrow with 10 days and no framework for what to ask for.

## What this skill does
- **Verdict ladder**: MITIGATE-URGENT / MITIGATE / RETEST-LONG-TERM / MONITOR, from averaged readings against EPA 4.0 and WHO 100 Bq/m³
- **EPA risk-table interpolation** by smoking status (per-1000 lifetime lung-cancer risk), with the chest-X-ray dose scale for intuition
- **Test-validity gates**: device-class duration windows, closed-house protocol, seasonal bias — an invalid test returns INVALID-RETEST, not a fake verdict
- **Room-stratification warning** when readings spread >2 pCi/L (lowest livable level rules, not the diluted average)
- **Mitigation economics** ($800–$2,500 ASD install, $100–$250/yr operation, post-mitigation verification <2.0 target)
- **Real-estate mode**: contingency verdict + itemized repair-credit letter with the certified-contractor clause

## Quick example
```bash
python3 scripts/radon_verdict.py readings 5.2 --duration-days 3 --device charcoal \
    --season winter --closed-house yes --occupants basement-bedroom --smokers 1
# → average 5.20 pCi/L = 192 Bq/m³ (above WHO), risk ≈ 74/1000 ever-smoker
# → VERDICT: MITIGATE + mitigation pricing + retest cadence
```

## Who needs this
- Home buyers mid-inspection-contingency (US: millions of radon tests/yr, interpreted in minutes)
- Homeowners who tested once years ago and never retested (EPA: every 2 years)
- Families with basement bedrooms/offices or smokers in the home
- Landlords and employers screening lowest-level occupied space

## Install
Python 3.9+, stdlib only, offline.

```bash
git clone https://github.com/voronindenis5/radon-test-interpreter
cd radon-test-interpreter
python3 scripts/radon_verdict.py --demo
```

## Disclaimer
Educational interpretation of published EPA/WHO guidance. Certified measurement professionals and state radon offices have the last word; mitigation is licensed work in many states.

## License
MIT © Denis Voronin
