# Renewal traps (snapshot)

Domain endings whose renewal is at least 2x the first-year price at the cheapest registrar we found (year one plus renewal).
405 endings qualify. This file is a dated snapshot; for live numbers call
`GET https://tld.expert/api/prices?tld=<ending>` (true cost block, every row with `sourceUrl` and `checkedAt`) or see https://tld.expert/trap.

When a user asks why a renewal jumped, or what a domain costs to keep: quote year one, the renewal next to it,
and the five-year total, never year one alone.

## Well-known endings

| Ending | Year one | Renewal | Multiple | Cheapest 5 years we found |
|---|---|---|---|---|
| [.bar](https://tld.expert/bar) | $1.53 at Porkbun | $52.01/yr | 34x | $209.57 (Porkbun) |
| [.health](https://tld.expert/health) | $3.00 at Dynadot | $64.42/yr | 21.5x | $252.24 (Dynadot, then Porkbun) |
| [.store](https://tld.expert/store) | $2.50 at Dynadot | $43.02/yr | 17.2x | $174.58 (Dynadot) |
| [.lol](https://tld.expert/lol) | $1.54 at Porkbun | $26.26/yr | 17.1x | $106.58 (Porkbun) |
| [.design](https://tld.expert/design) | $3.00 at Dynadot | $48.37/yr | 16.1x | $190.44 (Dynadot, then Porkbun) |
| [.shop](https://tld.expert/shop) | $2.06 at Porkbun | $31.41/yr | 15.2x | $127.70 (Porkbun) |
| [.online](https://tld.expert/online) | $1.96 at Porkbun | $28.84/yr | 14.7x | $117.32 (Porkbun) |
| [.world](https://tld.expert/world) | $2.57 at Porkbun | $37.59/yr | 14.6x | $152.93 (Porkbun) |
| [.co](https://tld.expert/co) | $2.37 at Porkbun | $31.20/yr | 13.2x | $127.17 (Porkbun) |
| [.fit](https://tld.expert/fit) | $2.06 at Porkbun | $26.26/yr | 12.7x | $107.10 (Porkbun) |
| [.wtf](https://tld.expert/wtf) | $2.57 at Porkbun | $32.44/yr | 12.6x | $132.33 (Porkbun) |
| [.fun](https://tld.expert/fun) | $2.57 at Porkbun | $31.41/yr | 12.2x | $128.21 (Porkbun) |

## Worst ratios

| Ending | Year one | Renewal | Multiple | Cheapest 5 years we found |
|---|---|---|---|---|
| [.bar](https://tld.expert/bar) | $1.53 at Porkbun | $52.01/yr | 34x | $209.57 (Porkbun) |
| [.feedback](https://tld.expert/feedback) | $9.27 at Porkbun | $309.47/yr | 33.4x | $1247.15 (Porkbun) |
| [.sa.com](https://tld.expert/sa.com) | $10.08 at Porkbun | $308.24/yr | 30.6x | $1243.04 (Porkbun) |
| [.za.com](https://tld.expert/za.com) | $10.08 at Porkbun | $308.24/yr | 30.6x | $1243.04 (Porkbun) |
| [.realty](https://tld.expert/realty) | $10.80 at Porkbun | $288.88/yr | 26.7x | $1166.32 (Porkbun) |
| [.creditcard](https://tld.expert/creditcard) | $5.66 at Porkbun | $129.25/yr | 22.8x | $522.66 (Porkbun) |
| [.health](https://tld.expert/health) | $3.00 at Dynadot | $64.42/yr | 21.5x | $252.24 (Dynadot, then Porkbun) |
| [.courses](https://tld.expert/courses) | $1.54 at Porkbun | $31.41/yr | 20.4x | $127.18 (Porkbun) |
| [.forum](https://tld.expert/forum) | $1.54 at Porkbun | $31.41/yr | 20.4x | $127.18 (Porkbun) |
| [.study](https://tld.expert/study) | $1.54 at Porkbun | $31.41/yr | 20.4x | $127.18 (Porkbun) |

## Renewal at or below year one, per registrar

- Porkbun: 218 of 636
- Dynadot: 413 of 823
- Name.com: 204 of 601
- gandi: 4 of 123

## Sources

- Dynadot: https://www.dynadot.com/domain/price-list (read 2026-11-27)
- gandi: https://www.gandi.net/en-US/domain/tld (read 2026-11-27)
- Name.com: https://www.name.com/pricing (read 2026-11-27)
- Porkbun: https://api.porkbun.com/api/json/v3/pricing/get (read 2026-11-27)
