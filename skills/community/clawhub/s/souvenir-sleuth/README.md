# souvenir-sleuth 🎁

**Find authentic local souvenirs — dodge the tourist traps.**

Every travel destination has two souvenir economies. One sells fridge magnets,
"snow globes, and "handmade" scarves shipped from a factory. The other sells
what that place is actually famous for — often for less money, one street over.
Telling them apart requires local knowledge most travelers don't have on day
one. `souvenir-sleuth` is that knowledge, packaged.

## The real-world problem

- Travelers routinely overpay 2-5x for fake "local" crafts (bonded leather,
  machine-printed "handwoven" textiles, reproduction "antiques")
- People accidentally buy **illegal** souvenirs (ivory, coral, tortoiseshell,
  rosewood) and get them seized — or fined — at customs
- Food gifts get confiscated because nobody told them honey can't enter
  Australia or cured sausage can't enter the US
- Shopping hours get wasted in commission-driven "artisan" stores

## What it does

Give it a destination and get a dossier of genuinely local specialties:

- **Fair local price ranges** so you know when you're being quoted tourist price
- **Where locals actually buy** — named markets, districts, workshop streets
- **Authenticity tells per material** — hand-thrown vs mold ceramics,
  vegetable-tanned vs bonded leather, hand-knotted vs machine carpets,
  real saffron vs dyed corn silk
- **Customs flags** (🟢🟡🔴) per item + a full guide for US/EU/AU/UK/CA imports
- **Trap check** — "is a Colosseum snow globe a good Rome souvenir?" (no;
  here's what to buy instead)
- **Haggling index** per culture — where negotiating is expected vs insulting
- **Avoid list** per destination — counterfeits, CITES violations, scams

13 destinations in the offline knowledge base (Kyoto, Fez, Marrakech, Oaxaca,
Mexico City, Lisbon, Florence, Istanbul, Prague, Chiang Mai, Hanoi, Cusco,
Cape Town, New Orleans); the agent enriches any destination with live research
using the same structure.

## Quick start

```bash
python3 scripts/souvenir_sleuth.py --list
python3 scripts/souvenir_sleuth.py --destination Fez
python3 scripts/souvenir_sleuth.py --destination "Mexico City" --budget 500
python3 scripts/souvenir_sleuth.py --destination Rome --item "Colosseum snow globe"
python3 scripts/souvenir_sleuth.py --destination Kyoto --json kyoto.json
```

## Example output

```
 SOUVENIR DOSSIER — Fez, Morocco
 Currency: MAD   Haggling index: ●●●●● (sticker price is theater)

 ▸ Vegetable-tanned leather goods  [leather]
    Chouara tannery leather, pigeon-lime and vegetable-dyed for centuries
    Fair price : 80–900 MAD
    Buy at     : Shops around Chouara tannery terraces; Souk Henna
    Real tell  : Vegetal smell, pore grain visible, fibrous cut edges
    Customs    : 🟡 declare / check liquids & quantity

 AVOID
  ✗ Tortoiseshell-pattern combs — can be real hawksbill turtle — CITES violation
```

## License

MIT © Denis Voronin
