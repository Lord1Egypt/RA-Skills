# Tax Tables & Thresholds — 2026 US (ESTIMATES — VERIFY)

> **Verify-first doctrine.** Every number here is a 2026 estimate compiled from post-OBBBA projections and SSA announcements. Before finalizing any plan, check: IRS Rev. Proc. (current-year inflation adjustments), SSA.gov Medicare Part B IRMAA tables (published each fall for the NEXT year), and IRS Pub 590-B (RMD tables). The script prints the same disclaimer on every run.

## Ordinary brackets (2026 est.)
| Rate | Single top | MFJ top |
|---|---|---|
| 10% | $12,400 | $24,800 |
| 12% | $50,400 | $100,800 |
| 22% | $105,700 | $211,400 |
| 24% | $201,775 | $403,550 |
| 32% | $256,225 | $512,450 |
| 35% | $640,600 | $768,700 |
| 37% | — | — |

Standard deduction (2026 est.): **$15,750 single / $31,500 MFJ** (additional 65+ / blind amounts apply). No personal exemptions.

## Long-term capital gains (2026 est., taxable income)
- 0% up to **$49,250 S / $98,500 MFJ**
- 15% up to ~$600k S / $750k MFJ; 20% above.
- NIIT 3.8% applies over $200k S / $250k MAGI — the model ignores it; flag for high earners.

## IRMAA tiers (2026 est. MAGI → premiums charged in 2028)
| Tier | Single MAGI | MFJ MAGI | Part B+D surcharge (approx., single rates) |
|---|---|---|---|
| 1 (OK) | < $106,000 | < $212,000 | standard premium |
| 2 | $106k–133k | $212k–266k | +~$1,100/yr |
| 3 | $133k–167k | $266k–334k | +~$2,700/yr |
| 4 | $167k–200k | $334k–400k | +~$4,400/yr |
| 5 | $200k–500k | $400k–750k | +~$6,300/yr (3.5×) |
| 6 | ≥ $500k | ≥ $750k | max (4×+ ~$7,600/yr) |

- **Two-year lookback:** 2026 MAGI sets 2028 premiums. New retirees (no MAGI 2 years ago) get standard premiums initially — then get re-priced; file **Form SSA-44** (life-changing event: retirement/work stoppage) to appeal with an income estimate.
- Crossing a tier by $1 costs the whole tier's premium increase on ALL income — the "cliff" behavior that makes a $1,000 Roth conversion a $5,000 mistake.

## RMD rules (SECURE 2.0)
- First RMD year: **age 73** if born 1951–1959; **age 75** if born 1960 or later.
- First RMD can defer to April 1 of the following year — **trap**: that stacks TWO RMDs in one tax year.
- Missed RMD: **25% excise** on the shortfall; reduced to **10%** if corrected within 2 years (Form 5329 Part IX; IRS has been waiving with reasonable cause + correction).
- Uniform Lifetime Table (joint life, 10-yr-younger spouse): 73→26.5, 74→25.5, 75→24.6, 76→23.7, 78→22.0, 80→20.2, 85→16.0, 90→12.2, 95→8.9, 100→6.4. If sole spouse is >10 yrs younger, use the Joint Life table (smaller RMDs).
- Roth IRAs have **no lifetime RMD** (inherited RMDs are a different, crueler system: 10-year rule for most non-spouse heirs post-2019).

## Other 2026 anchors (est.)
- QCD limit: ~$108k–110k (indexed; 70½+, IRA→charity directly, counts for RMD, never touches MAGI).
- Estate/gift exemption: ~$15M per person (post-OBBBA permanent + index) — makes Roth "spend last / leave to heirs" even stronger.
- SS taxation: up to 85% of benefits taxable over $44k MFJ / $34k S combined income (NOT indexed — the eternal stealth bracket).
