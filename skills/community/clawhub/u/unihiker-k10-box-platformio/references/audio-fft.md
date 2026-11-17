# K10 Box Audio FFT and Reactive Lights

## Hardware boundary

The PCM microphone is K10-native I2S hardware. The red/yellow/green traffic
lights belong to the experiment-box IO controller at `0x20`. The box
`getSoundVolume()` value is an amplitude-style ADC reading, not PCM suitable
for FFT analysis.

Call `k10.begin()` before capturing audio. Reuse the BSP-initialized I2S port;
do not install a second driver over it. Keep motor and actuator modes mutually
exclusive with sound-reactive lights, and clear every LED when leaving the
audio screen.

## Tested capture format

The tested K10 BSP configures I2S port 0 as 16 kHz, stereo, 16-bit. Each frame
contains two native little-endian signed 16-bit words. The microphone signal is
in the second/right word. Treating it as big-endian can produce false
near-full-scale audio.

Drain stale DMA data after startup before judging the microphone. A bounded
drain is especially important when initialization took hundreds of
milliseconds and old silent buffers accumulated.

## FFT pipeline

Use this tested baseline:

1. Capture 512 microphone samples.
2. Remove the frame mean (DC offset).
3. Calculate RMS and `20 * log10(rms / 32768)` dBFS.
4. Apply a Hann window.
5. Run a 512-point radix-2 FFT.
6. Search roughly 94 Hz through 6 kHz for the dominant peak.
7. Use parabolic interpolation around the strongest bin.
8. Downsample PCM to 64 waveform points and FFT bins to 16 display bands.

At 16 kHz, a 512-point transform gives a 31.25 Hz bin width. Label loudness as
**dBFS**, not dB SPL; it is not acoustically calibrated.

## Quiet gating and LEDs

Track the quiet noise floor and require both sufficient level and spectral
prominence. A working starting point is:

```text
activity threshold = max(-44 dBFS, tracked noise floor + 8 dB)
peak magnitude      > average searched-bin magnitude * 4
```

Map normalized low-, mid-, and high-band energy to red, green, and blue. Apply
fast attack and slower release (for example, retain about 68% per update) to
avoid harsh flicker. On the K10 RGB strip, dedicate one pixel to each band; on
the box, drive red/yellow/green analog brightness with the same three levels.

Update the audio LVGL objects about every 50 ms. Refresh only the waveform,
spectrum, level label, and status indicator; do not clear the full screen.

## Verification

Serial diagnostics should report FFT activity, dominant frequency, dBFS, and
the three LED levels. Verify both states:

- Quiet input eventually reports inactive FFT and LEDs decay to zero.
- A real tone or box-buzzer diagnostic produces active FFT and a corresponding
  frequency-band LED response.

A buzzer driven with `setBuzzer(1000)` can have a stronger acoustic resonance
or harmonic near another frequency. Report what the microphone actually hears;
do not force the FFT result to equal the drive setting.
