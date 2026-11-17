# Silent Refrigerator Listener

**The problem:** a fridge announces failures acoustically before food spoils — but "it's louder" is all most people can articulate. The compressor running 70% of the time instead of 35% means a leaking door seal, dirty coils, or low refrigerant. An 8 Hz flutter in the hum means worn mounts or unlevel feet. Sustained hiss means an iced fan blade. Rapid clicking means a $15 start relay fighting a compressor that will die of thermal abuse if ignored. Each sound is a different part with a price tag spanning $0–$1000 — and the diagnosis needs no tools, just listening correctly.

**What this does:** pure-Python DSP (stdlib only — no numpy, no dependencies) on a phone recording of the running appliance:

- **Duty cycle** — fraction of time the compressor is audible; >70% = over-running (headline symptom)
- **Hum detection** — autocorrelation finds the 50/60 Hz + harmonic compressor voice; its presence separates real compressor noise from fan hiss
- **Envelope flutter** — 4–15 Hz loudness modulation with depth >6 dB = mechanical rattle signature
- **Click counting** — relay/overload chatter per minute (start-fail cycles)
- **Hiss fraction** — broadband frames without tonal hum = evaporator fan trouble

Each signature maps to ranked causes with a cheap-fix-first order (vacuum the coils before anyone looks at refrigerant), and the output doubles as a technician brief.

```bash
# phone memo → wav: ffmpeg -i memo.m4a fridge.wav
python3 scripts/fridge_sound_analyzer.py analyze fridge.wav
# → duty 0.73, am_rate 9.8 Hz → "COMPRESSOR OVER-RUNNING..." + "RATTLE DETECTED..."

# no fridge handy? synthetic demo of two failure signatures:
python3 scripts/fridge_sound_analyzer.py demo
```

## Who needs this

Every household owns a refrigerator; compressor-driven appliances fail by degradation, not suddenly, and the acoustic phase lasts weeks. Also: anyone buying a used fridge (a 5-minute recording is the cheapest mechanical inspection available), landlords triaging tenant complaints, and anyone deciding repair-vs-replace.

## Why patterns, not decibels

Phone mics are uncalibrated and AGC-affected, so absolute loudness is meaningless across recordings. Duty cycle, modulation rate, hum presence, and click rate are **invariant** — they carry over between any two recordings taken the same way, which also makes before/after repair comparisons objective.

## License

MIT
