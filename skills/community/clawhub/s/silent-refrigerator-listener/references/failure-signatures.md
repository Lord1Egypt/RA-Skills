# Refrigerator Failure Signatures — What Each Sound Is

## The machine's normal voice

A frost-free refrigerator is a heat pump plus two fans plus a defrost
system, and its healthy acoustic signature is boring:

- **Compressor**: a low hum at mains frequency (50/60 Hz) and its
  harmonics (100/120 Hz dominant). It cycles: runs 30–50% of the time
  in a cool kitchen with healthy seals, more in hot rooms or after
  door openings — but rarely sustained above ~60%.
- **Evaporator fan** (freezer side): a soft broadband whoosh whenever
  the compressor runs, in many units also with doors closed between
  cycles. Slight speed change on door opening is normal.
- **Condenser fan** (near compressor, if present): similar, quieter.
- **Defrost cycle**: every 8–12 h the heater runs ~30 min; you may
   hear ticking/cracking (thermal expansion) and water dripping to the
   drain pan. Intermittent, quiet, normal.
- **One click** at compressor start = the start relay doing its job.
- **Gurgling/swishing** = refrigerant moving; normal, often after a
  long run or a new unit.

## The four failure signatures

### 1. Over-running compressor (duty > 70%)

The compressor removes heat that leaks in. If it runs almost all the
time, heat is arriving too fast or can't be dumped:

| Cause | Cost to fix | Check |
|---|---|---|
| Door seal (gasket) leak | $50–150 DIY | paper test: close the door on a banknote; if it slides freely anywhere, the gasket is shot there. Also: door not tilted back 1–2°, hinges sagging, heavy items on the door |
| Dirty condenser coils | free | pull the unit, vacuum the coil grid (back or bottom). Do this FIRST — it's the most common cause and costs nothing |
| Hot / enclosed installation | free | spec sheet wants inches of clearance; a fridge in a nook behind a radiator can't dump heat |
| Low refrigerant (slow leak) | $200–500, often not worth it on old units | frost pattern on the evaporator plate is patchy; needs a tech |
| Stuck/failed thermostat or control board | $100–300 | fridge section freezing items, or temps drifting regardless of setting |

Note: over-running alone with everything else normal, in a 35 °C
kitchen, after six door openings, is just physics — record in steady
state.

### 2. Rattle / flutter (4–15 Hz envelope modulation)

A hum that wobbles several times a second is mechanical contact or
resonance:

- **Unlevel feet** — the #1 cause and a free fix. Level front-to-back
  with a slight rear tilt so doors swing closed. Check with a spirit
  level app.
- **Worn compressor mount springs** — internal suspension; the whole
  compressor vibrates against the frame. Replaceable mounts, cheap-ish
  labor.
- **Something touching** — a water line against the back, a drip pan
  rattling, a shelf or panel resonating. Press lightly on suspects
  while it rattles; when the rattle stops, you've found it.
- **Iced-over evaporator fan blade** — if the flutter is faster
  (whirring/grinding) and comes from the freezer, defrost first.

### 3. Hiss / broadband noise (fan or airflow)

Sustained hiss without a tonal hum, from the freezer side, is the
evaporator fan:

- **Ice on the blade** — defrost (unplug, doors open, 24–48 h with
  towels; or the manufacturer's forced-defrost mode). If the noise
  returns within days, the defrost system (heater, timer, or
  bi-metal) is failing and ice is building — fix the defrost, not the
  fan.
- **Bearing wear** — the fan motor itself; aftermarket fan motors are
  $20–60 and usually a straightforward swap behind the freezer panel.
- **Rasping/scraping** — blade touching the shroud: reseat or replace
  the blade.

### 4. Clicking (relay/overload chatter)

Rapid clicks (every 1–5 min or faster) with the compressor trying to
start = start relay / overload protector cycling:

- **Weak start capacitor / failed relay** — $15–40 part, often
  plug-on. The compressor hums briefly, clicks off, cools, retries.
  Worth attempting DIY (universal relay kits exist — match by
  compressor pins).
- **Seized compressor** — same clicking but the hum is labored and
  loud; the thermal cutoff keeps killing it. Compressor replacement
  ($500–1000+) — on a unit past ~8–10 years, compare against
  replacement.
- **Low voltage / bad outlet** — rare, but try a different outlet
  before ordering parts.

## Decision tree (cheap-first)

1. Record → duty high? → vacuum coils, paper-test gaskets, check
   clearances → re-record.
2. Rattle? → level feet → press-test panels/lines → mounts.
3. Hiss? → manual defrost → returns in days? → defrost system, not fan.
4. Clicking? → try another outlet → replace start relay (cheap) →
   if laboring hum persists, get a quote on the compressor vs a new
   unit.

## Making the technician call efficient

Read them, in order: the signature (over-run / rattle / hiss /
clicking), the duty-cycle number, whether the hum is tonal, the
flutter rate, and what you already tried (coils vacuumed, gasket
tested, defrosted). That list moves you from "it's loud" (they bring
nothing and charge a diagnosis visit) to a tech who arrives with the
likely parts.

## Recording protocol that survives phone AGC

- Door closed. Nobody in the room. HVAC/fans off if possible.
- Phone 0.5–1 m from the unit, at compressor height (bottom rear) or
  front bottom grille — NOT inside the fridge.
- 3–10 minutes, airplane mode (notifications corrupt frames).
- Convert to WAV: `ffmpeg -i memo.m4a -ar 44100 fridge.wav`.
- Save a healthy baseline recording now, while everything is fine.
  Comparative features (duty delta, new flutter) beat absolutes.
