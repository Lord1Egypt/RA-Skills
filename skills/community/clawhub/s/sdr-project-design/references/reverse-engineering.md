# Reverse Engineering / Signal Analysis SDR Projects

## Core references

### URH (Universal Radio Hacker)
- Repo: `jopohl/urh`
- Best entry point for protocol reverse-engineering workflows
- Strong for demodulation, parameter inference, decodings, fuzzing, and simulation
- Great when the user wants to move from "I captured something" to "I think I understand the frame structure"

### inspectrum
- Repo: `miek/inspectrum`
- Best for deep offline analysis of recorded captures
- Great for symbol timing, burst structure, period measurement, and extracting frames from captures
- Use when time-domain detail matters more than live interactivity

### SigDigger
- Repo: `BatchDrake/SigDigger`
- Real-time signal analysis tool for unknown signals
- Strong for FSK/PSK/ASK-style signal inspection and live hunting
- Good first stop when the user needs to locate and characterize signals quickly

### GNU Radio
- Repo: `gnuradio/gnuradio`
- Heavyweight DSP construction kit
- Use when custom blocks/flowgraphs are required
- Best for:
  - custom demod chains
  - experiments beyond packaged decoders
  - simulation and controlled test pipelines

### SoapySDR
- Repo: `pothosware/SoapySDR`
- Hardware abstraction layer, not an end-user app
- Critical for portable SDR application design
- Common source of plugin/runtime/vendor mismatch pain

### gr-osmosdr
- Important classic hardware integration layer in many GNU Radio / GQRX style stacks

## Starting from scratch

### If the user has an unknown digital signal
Recommend this order:
1. capture a clean sample
2. inspect it in SigDigger or a live spectrum tool
3. save IQ/baseband
4. inspect offline with inspectrum
5. infer framing/modulation in URH
6. only build custom GNU Radio flowgraphs if the simpler tools stop short

### If the user wants replay / fuzzing style work
Recommend:
- URH first for protocol understanding and controlled generation
- clear legal/safety boundaries
- transmit-capable hardware only if the project actually requires it

### If the user keeps jumping straight into GNU Radio
Slow them down unless custom DSP is clearly required. Many unknown-signal tasks are solved faster with:
- a simple live receiver
- IQ capture
- inspectrum
- URH

## Reverse-engineering workflow notes

Good unknown-signal work usually means documenting:
- center frequency
- sample rate
- bandwidth estimate
- observed modulation guess
- burst length / periodicity
- symbol timing guesses
- preamble/sync patterns
- known-good captures and failed captures

## Best-fit guidance

### If you want unknown RF protocol work
Use:
- `SigDigger` for live hunting
- `inspectrum` for offline captures
- `URH` for protocol inference and fuzzing
- `GNU Radio` only when existing tools stop short

### If you want architecture guidance
Prefer:
- save raw captures early
- keep notes on every successful decode clue
- separate discovery, analysis, and synthesis into distinct phases instead of one giant tool workflow

## Common traps

- trying to reverse engineer from bad captures
- not logging sample rate / center frequency / gain
- over-trusting waterfall visuals without offline inspection
- building custom flowgraphs before understanding the signal basics
- ignoring clock drift / symbol-rate mismatch / front-end overload
