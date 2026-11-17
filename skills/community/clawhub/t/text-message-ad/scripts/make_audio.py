"""Synthesizes iMessage-style UI sounds for a text-message ad.

Usage: python3 make_audio.py config.json
Reads the same config as render.js. Sound events are derived from the timeline:
  - each row in `rowKinds` gets a sound at its `shows` time:
      "send"  -> rising swoosh (outgoing message)
      "recv"  -> glassy two-note ding (incoming bubble or link card)
      "typ"   -> soft low pop (typing indicator)
      "none"  -> silent
  - `endcard` time gets a warm chime.
Writes <framesDir>.wav next to the frames directory (see `audioOut` override).
"""
import json, sys, wave
import numpy as np

SR = 44100

def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def sine(f, n): return np.sin(2 * np.pi * f * np.arange(n) / SR)

def send_swoosh():
    n = int(0.32 * SR)
    t = np.arange(n) / SR
    f = 340 + 700 * (t / t[-1]) ** 1.6
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
    noise = np.random.randn(n)
    noise = np.convolve(np.diff(noise, prepend=0), np.ones(6) / 6, 'same')
    body = tone * 0.55 + noise * 0.5
    e = np.minimum(np.arange(n) / (0.03 * SR), 1) * env_exp(n, 0.12)
    return body * e * 0.55

def receive_ding():
    n = int(0.5 * SR)
    out = np.zeros(n)
    for start, f, amp in [(0.0, 987.8, .9), (0.085, 1318.5, 1.0)]:
        s = int(start * SR); m = n - s
        note = sine(f, m) + sine(f * 2, m) * 0.28 + sine(f * 3.01, m) * 0.08
        out[s:] += note * env_exp(m, 0.10) * amp
    return out * np.minimum(np.arange(n) / (0.004 * SR), 1) * 0.34

def typing_pop():
    n = int(0.07 * SR)
    return sine(300, n) * env_exp(n, 0.02) * 0.16

def end_chime():
    n = int(1.4 * SR)
    out = np.zeros(n)
    for f, amp in [(1046.5, 1.0), (1318.5, .8), (1568.0, .7), (2093.0, .25)]:
        out += sine(f, n) * env_exp(n, 0.35) * amp
    return out * np.minimum(np.arange(n) / (0.01 * SR), 1) * 0.20

LIB = {'send': send_swoosh, 'recv': receive_ding, 'typ': typing_pop, 'chime': end_chime}

def main():
    cfg = json.load(open(sys.argv[1]))
    dur = cfg['durationMs'] / 1000
    total = np.zeros(int(dur * SR))
    events = [(cfg['shows'][i] / 1000, kind)
              for i, kind in enumerate(cfg['rowKinds']) if kind != 'none']
    events.append((cfg['endcard'] / 1000, 'chime'))
    for t, kind in events:
        np.random.seed(7)
        s = LIB[kind]()
        i = int(t * SR)
        end = min(i + len(s), len(total))
        total[i:end] += s[:end - i]
    peak = np.abs(total).max()
    if peak > 0.85:
        total *= 0.85 / peak
    pcm = (total * 32767).astype(np.int16)
    out = cfg.get('audioOut', cfg['framesDir'] + '.wav')
    with wave.open(out, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('audio ->', out)

if __name__ == '__main__':
    main()
