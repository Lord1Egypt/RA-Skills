# water-heater-tuner

One dial, three risks: scald (kids burn in seconds at 55°C+), legionella
(the tank is a bacterial reactor below 60°C), and standby energy (every
5.6°C of setpoint ≈ 3–5% of water-heating energy). This skill computes the
trade for your household — who uses the water, tank size, fuel, install
location — and returns a setpoint verdict with the WHY, a pasteurization
protocol for low-storage operation, vacation/return plans, and
morning-shower recovery math.

## The real-world problem

Water heater temperature is the most consequential dial nobody sets
deliberately. Set it high and a toddler at the bath faucet gets
full-thickness burns in seconds (60°C ≈ 3 s for adult skin, less for
children); set it low without a plan and the tank cultures Legionella —
rare but a ~10% fatality disease; set it anywhere and standby loss quietly
eats 3–5% of heating energy per 10°F. The correct strategy differs by
household (infant? elder? mixing valve? garage tank?) — this tool runs the
actual decision, not a generic "120°F is fine" pamphlet answer.

## Quick start

```bash
cd scripts
python3 heater_tuner.py profile --tank-gal 40 --fuel gas --users adult,adult,child2 \
  --location basement --setpoint 140
python3 heater_tuner.py setpoint            # verdict + why
python3 heater_tuner.py energy --to 120 --bill 180
python3 heater_tuner.py recovery --showers 3 --inlet-c 9
python3 heater_tuner.py pasteurize          # thermal disinfection card
python3 heater_tuner.py vacation --days 14
```

Python 3.9+, stdlib only. Store: `heater_profile.json` next to the script.

## Verdict logic

- Immunocompromised resident → storage ≥ 60°C mandatory + mixing valve 49°C
- Child < 5 / elder + valve → **store 60°C, deliver 49°C** (best of both)
- Child/elder, no valve → 49°C setpoint + weekly pasteurize protocol
  (scald time at 49°C ≈ minutes, not seconds)
- Adults only → 55–58°C band, printed with the burn-time context

Every verdict names the binding constraint and the tap temperatures to
verify (nearest tap for scald, farthest for delivery).

## What else it computes

- **energy** — % saved for a setpoint move, $/yr from your bill, tank
  blanket / pipe insulation / heat-pump upgrade deltas, cold-space notes
- **recovery** — mixing multiplier (how much shower-temp water the tank
  yields), back-to-back shower count, minutes-of-reheat per shower, winter
  inlet penalty ("fine in summer, cold by February" explained)
- **pasteurize** — the WHO-based 60°C/30-min hold + flush-every-outlet
  card with scald warnings sized to your household
- **vacation** — away plan by duration and fuel, and the return protocol
  that keeps a stagnant tank from becoming a biology experiment

## Safety notes

The tool prints burn times from the Moritz & Henriques data (the basis of
CPSC/UL guidance) and legionella kill windows from WHO guidance. It is
decision support, not a substitute for a plumber where pressure/temperature
relief valves, gas work, or recirculation systems are involved.

## License

MIT © Denis Voronin
