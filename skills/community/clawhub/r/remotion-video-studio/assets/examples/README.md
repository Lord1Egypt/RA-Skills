# Examples

This directory contains complete example projects for reference.

## fourier-transform/

A Fourier Transform explainer video with 9 custom animated scenes.

### Files

- `subtitles.json` — Content script (9 slides in Chinese)
- `sceneMap.ts` — Scene registry mapping slide IDs to components
- `scenes/` — 9 custom React scene components:
  - `FourierScene01.tsx` — Sine wave decomposition
  - `FourierScene02.tsx` — Frequency spectrum
  - `FourierScene03.tsx` — Signal reconstruction
  - `FourierScene04.tsx` — DFT algorithm
  - `FourierScene05.tsx` — FFT butterfly diagram
  - `FourierScene06.tsx` — Spectral leakage
  - `FourierScene07.tsx` — Windowing functions
  - `FourierScene08.tsx` — Applications
  - `FourierScene09.tsx` — Summary timeline

### How to Use

Copy the scene files to your project as a starting point:

```bash
cp -r assets/examples/fourier-transform/scenes/*.tsx your-project/src/components/scenes/
```

Then adapt the scene components for your topic.
