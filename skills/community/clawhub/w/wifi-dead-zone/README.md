# Wi-Fi Dead Zone Solver

**The problem.** Nearly everyone lives with a room where Wi-Fi is miserable —
the bedroom that drops calls, the office that buffers at 4pm, the balcony
that may as well be a Faraday cage. The standard responses are superstition
(reboot it), waste (buy a $300 mesh kit that fixes the wrong wall), or
resignation. Almost nobody does the one thing that actually works: model the
home's geometry and place radios where physics wants them.

**What this is.** A planning tool that turns a 10-minute paper sketch of your
home — rooms as points, walls as line segments with materials — into:

- **Per-room signal estimates** using standard indoor RF models
  (log-distance path loss with band-specific exponents, plus per-material
  wall attenuation: drywall 3 dB, brick 6, concrete 10, a fridge 18).
- **An ASCII heatmap** of your floor plan showing where signal lives and
  dies, with walls and rooms marked.
- **Optimal router placement**, found by grid-searching 676 candidate spots
  to maximize your *weakest important room*, not the average — the corner
  router by the ISP socket is usually 10-20 dB worse than the spot 4 meters
  away, and the model tells you exactly where.
- **Mesh node guidance that's actually correct**: never inside the dead room
  (that just extends the dead zone); where the node still hears the router
  at ≥ −60 dBm, one wall maximum, Ethernet backhaul if possible.
- **Calibration against reality**: record real dBm readings from your phone
  (`survey`), and `compare` tells you whether to trust the model or fix the
  wall materials — with the direction of the error.
- **Channel selection** given your neighbors' networks: the 1/6/11 rule on
  2.4 GHz, DFS trade-offs on 5 GHz, PSC preference on 6 GHz.

**Why it matters.** Router placement is the highest-leverage, zero-cost fix
in home networking, and mesh kits are massively oversold: a node placed
badly performs *worse* than the router alone. This tool gives you the
physics answer before you spend money or drag furniture.

## Quick start

```bash
python3 scripts/wifi_heatmap.py example      # see it work on a sample home
python3 scripts/wifi_heatmap.py materials    # 21 wall materials + dB costs
```

Then sketch your home (see `references/home-file-guide.md`) and:

```bash
python3 scripts/wifi_heatmap.py plan --home myhome.json
python3 scripts/wifi_heatmap.py survey --home myhome.json --room office --rssi -74 --band 5
python3 scripts/wifi_heatmap.py compare --home myhome.json
python3 scripts/wifi_heatmap.py channels --band 2.4 --neighbors 1,6,6,11
```

## Tests

```bash
python3 scripts/test_wifi_heatmap.py   # 28 assertions, pure stdlib
```

## Honest limits

Planning-grade model (±4-8 dB), can't see furniture, bodies, or the
neighbor's microwave. That's why `survey`/`compare` exist: the model tells
you where to measure and what to expect; measurements keep it honest.

MIT License — see LICENSE. No network calls, no dependencies, nothing leaves
your machine.
