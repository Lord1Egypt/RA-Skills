# Smoker Pitmaster Planner — Reference

## 1. The real problem
Low-and-slow barbecue is the only common cooking task measured in **half-days
with a plateau in the middle**. A 6–7 kg brisket at 110 °C takes 14–20 h,
crosses an evaporative stall that can freeze the thermometer for 2–6 h, and
still has to land on a dinner time. Home cooks routinely:
- start too late and serve at 21:40 ("it's done when it's done" is physics,
  not a schedule);
- panic at hour 12 when the temp has not moved for 3 h and crank the pit,
  ruining the bark;
- run out of charcoal at 4 AM because nobody multiplied burn-rate × duration;
- pull meat at a quality temp for one species applied to another
  (chicken pulled at brisket temps = danger; brisket pulled at chicken-safe
  temps = shoe leather).

## 2. The physics

### 2.1 Newton-law heating
A cold mass in a hot environment heats on an exponential:

    T(t) = T_pit − (T_pit − T_0) · e^(−k·t)

- `T_0` = start temp (fridge-cold ≈ 5 °C).
- `k` = effective heat transfer coefficient per meat class, in 1/h.
- Mass scaling: surface area grows ~ m^(2/3), thermal mass ~ m, so
  `k(m) = k_ref · (m_ref / m)^(1/3)`.

Calibration anchors (pitmaster rules of thumb at 110 °C / 225 °F):
- brisket ~1.5 h/lb → 6.5 kg ≈ 21.5 h
- pork shoulder ~1.25 h/lb → 4.5 kg ≈ 12.4 h
- baby backs ~4 h at 1.4 kg racks, spare ribs ~5–6 h

These anchors fix `k_ref` per class; the model then interpolates sensibly
across weights and pit temps (higher ΔT = faster early climb, same asymptote).

### 2.2 The stall
Between ~65 °C and ~75 °C the meat surface sweats; evaporation consumes the
incoming heat and the internal temp plateaus. Model:
- stall duration ≈ `stall_h_per_kg × mass`, scaled by airflow (more draft =
  longer) and shortened by water pans / humidity.
- wrapping in foil/butcher paper ("Texas crutch") blocks evaporation:
  stall × ~0.35, and post-wrap `k × 1.6` (foil) / `× 1.3` (paper).
- thin cuts (ribs, tri-tip, chicken) barely stall — encoded as
  `stall_h_per_kg ≈ 0`.

### 2.3 Pull temps — quality vs safety (non-negotiable)
| Meat | Quality pull | Safety floor |
|---|---|---|
| brisket | 92–96 °C probe-tender | 71 °C (whole-muscle) |
| pork shoulder | 90–95 °C (shreds) | 63 °C whole pork (rested) |
| poultry | 74 °C breast 74–79 °C thigh | **74 °C hard floor** |
| ribs | 88–92 °C (bend test) | 63 °C |
| tri-tip | 54–57 °C medium-rare | 63 °C ground-composite only |

The script prints both and always shows the safety floor; quality targets
above the floor are allowed, below is blocked with a warning.

### 2.4 Carryover and rest
- Carryover: +2–4 °C after pulling (bigger cuts, higher pit temps → more).
- Rest: redistributes juices; 1 h minimum foil-towel-cooler for big cuts,
  which can safely extend to 2–4 h. **The rest is the schedule buffer** —
  plan to finish early and hold, never to finish late.

### 2.5 Fuel budget
Approximate steady-state charcoal consumption at 110–120 °C:
- kettle (snake/minion): 0.6–0.8 kg/h briquettes
- offset smoker: 0.9–1.3 kg/h lump (more airflow)
- ceramic (Kamado): 0.3–0.5 kg/h (insulated)
- pellet: quoted in kg pellets (0.5–0.9 kg/h), not charcoal

Always +25 % reserve; a 16 h offset cook realistically eats a full 10 kg
bag + starters.

## 3. Probe mode (mid-cook ETA)
Given elapsed `t1` and internal `T1`:

    k_fit = −ln((T_pit − T1) / (T_pit − T0)) / t1

Recompute remaining time to pull temp with `k_fit`, detect stall
(`T1` inside band AND `k_fit` collapsed vs class norm), and report:
- ON TRACK / STALLED (normal, expected N more hours) / RUNNING FAST /
  BEHIND (raise pit 10–15 °C now, do not open the lid).

## 4. Decision doctrine
1. Back-plan from serve: serve − rest − carryover − cook × 1.25 = put-on.
2. If put-on lands in the middle of the night, that is normal; set two alarms
   (fuel top-up, stall check).
3. Late protocol: +10–15 °C pit and wrap if not already — a hotter-and-
   faster brisket at 130 °C is still good; a rushed undercooked one is not.
4. Early protocol: hold in cooler with towels; brisket held 3–4 h is *better*.
5. Never judge doneness by clock alone — probe tender (slides in like
   butter) or bend test for ribs; time models get you to the window.

## 5. Limitations (honesty)
- Model is 1-D lumped-capacitance; real cookers have gradients. Treat
  outputs as a planning window (±15 %), not a promise.
- Ambient cold/wind extends cooks (offset in winter: +10–20 %) — the
  uncertainty factor exists for this.
- Altitude lowers boiling point: high-elevation stalls happen ~1 °C lower
  per 300 m.
