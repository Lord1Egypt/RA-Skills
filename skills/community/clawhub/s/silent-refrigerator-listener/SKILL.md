---
name: silent-refrigerator-listener
description: Use when a fridge or freezer sounds wrong (rattling, humming louder, clicking, running constantly) or food spoils early — analyzes a phone recording of the appliance with pure-Python DSP (duty cycle, mains-hum autocorrelation, envelope flutter, click counting) to name the likely failure: over-running compressor, worn mounts, iced fan, or hard-starting relay, with causes and a technician brief.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [refrigerator, appliance-repair, sound-analysis, diagnostics, home-maintenance, dsp]
---

# Silent Refrigerator Listener

A fridge announces its failures acoustically before anything measurable
happens to the temperature. The compressor that runs 70% of the time
instead of 35% is telling you about a leaking door seal, dirty coils,
or low refrigerant; the 8 Hz flutter in the hum is worn mount springs
or unlevel feet; sustained broadband hiss is an evaporator fan blade
hitting ice; rapid clicking is the start relay fighting a dying
capacitor or a seized compressor. Most people hear "it's louder" and
can't say more — and by the time milk spoils, the repair bill includes
a full compressor instead of a $15 relay.

This skill turns a phone voice memo into a structured verdict. Record
the fridge for a few minutes (door closed, phone within a meter, room
quiet), run the analyzer, get the failure signature named with ranked
causes and what-to-try-first.

## When to Use

- "The fridge is louder / making a weird noise" — rattle vs hiss vs
  click vs over-run, each pointing at different parts
- Food spoiling early or milk going off — check whether the compressor
  is over-cycling (duty cycle is the headline number)
- Before calling a technician — the verdict + features make the phone
  call precise ("compressor runs constantly, relay isn't clicking")
- After a repair — record again, compare feature tables objectively
- Buying a used fridge — a 5-minute recording is the cheapest
  mechanical inspection you can do without tools

**Don't use for:** electrical burning smell, visible smoke, or water
flooding — unplug now, this is not a pre-call triage situation.

## How It Works — the four signatures

| Signature | Detected as | Means |
|---|---|---|
| **Over-running** | duty cycle >70% (healthy 30–50%) | door seal leak, dirty condenser coils, low refrigerant, hot/enclosed install, stuck thermostat |
| **Rattle/flutter** | envelope modulation 4–15 Hz, >6 dB depth | worn compressor mounts, unlevel feet, panel or line touching frame — level feet first, it's free |
| **Hiss** | >30% of active frames broadband (high zero-crossing, no hum) | evaporator/condenser fan: blade hitting ice or bearing wear — defrost first, if it returns it's the fan |
| **Clicking** | isolated spikes, >6/min | relay/overload chattering: weak start capacitor (cheap fix) or seized compressor (expensive) |

The chain: WAV → mono mixdown → downsample to ~11 kHz → 10 ms frames
→ RMS levels (dB, relative — phone mics aren't calibrated; the
diagnostic value is pattern, not absolute loudness) → noise-floor
percentile → activity mask → duty cycle, click detection, hum
fundamental via normalized autocorrelation on the loudest 200 ms
window (expect 50/60 Hz mains and 100/120 Hz harmonics), and envelope
modulation spectrum for flutter rate.

## Commands

```bash
# record: phone voice memo, door CLOSED, <1 m away, 3-10 min,
# quiet room, no one talking. Convert to WAV (e.g. ffmpeg -i memo.m4a out.wav)

python3 scripts/fridge_sound_analyzer.py analyze fridge.wav

# no fridge handy? built-in synthetic demo (generates, analyzes, removes):
python3 scripts/fridge_sound_analyzer.py demo
```

Zero dependencies — stdlib `wave` + `array` only. Mono/stereo, 8/16/32-bit.

## Interpreting the output

```
=== fridge.wav — 240.0s @ 11025 Hz ===
  duty             0.73        ← headline: fraction of time compressor-quiet machine is loud
  hum_f0           119.8       ← mains harmonic present = real compressor voice
  am_rate_hz       9.8         ← flutter rate in the rattle band (4-15 Hz)
  am_depth_db      11.3        ← how deep the flutter is (>6 dB = mechanical)
  hiss_frac        0.05        ← broadband fraction (fan noise)
  clicks_per_min   0.4         ← relay chatter
 • COMPRESSOR OVER-RUNNING: ... Causes: door seal leak, dirty coils, ...
 • RATTLE DETECTED: ... Level the feet first (free), then check mounts.
```

## Common Pitfalls

1. **Recording too short.** Under 60 s you'll likely capture one long
   run and read "over-running" from a normal cycle. 3–10 minutes
   covers several cycles.
2. **Door open or people talking.** The mic must hear only the fridge.
   Speech and door alarms destroy the duty-cycle math.
3. **Recording during/after defrost.** Defrost heaters and defrost
   fans run on their own schedule — a normal unit can hiss for 30 min.
   Record in steady state, ideally morning.
3. **Trusting absolute loudness.** Phone AGC and distance vary; only
   relative patterns (duty, modulation rate, hum presence) carry over
   between recordings. Compare recordings taken the same way.
4. **Missing the freezer fan.** In many units the evaporator fan runs
   whenever the compressor is off is wrong — it runs with the door
   closed continuously in frost-free models; a hiss that NEVER stops
   while the compressor cycles normally is the fan, and that's normal
   unless loud or rasping.
5. **Clicking once.** One click per compressor start is normal
   (relay). The failure signature is rapid repeated clicks —
   start-fail-thermal-cutoff loops.

## Verification Checklist

- [ ] Recording ≥3 min, door closed, quiet room, <1 m distance
- [ ] Duty cycle compared against 30–50% healthy band
- [ ] If over-running: door-seal paper test + coil cleaning BEFORE calling anyone
- [ ] If rattle: feet leveled, then re-record to compare am_depth_db
- [ ] If clicking: unplug 30 s, replug once; if the pattern repeats, technician time
- [ ] Baseline recording saved when the fridge is healthy — comparisons beat absolutes

## References

- `references/failure-signatures.md` — the physics of each signature,
  what each part sounds like, cheap-fix-first decision tree, and the
  questions that make the technician call efficient.
