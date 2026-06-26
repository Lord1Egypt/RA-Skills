# Supertonic Voices

10 voices total: 5 female, 5 male.

| Voice | Gender | Description | Best For |
|-------|--------|-------------|----------|
| F1 | Female | Warm, mature | Professional narration, audiobooks |
| F2 | Female | Bright, clear | General purpose, announcements |
| F3 | Female | Soft, gentle | Japanese language, ASMR-like content |
| F4 | Female | Energetic, youthful | Gaming, casual content |
| F5 | Female | Deep, authoritative | News, documentaries |
| M1 | Male | Neutral, clear | Default voice, general use |
| M2 | Male | Warm, conversational | Blogs, casual narration |
| M3 | Male | Deep, serious | Trailers, dramatic content, briefings |
| M4 | Male | Bright, young | Gaming, tech content |
| M5 | Male | Energetic, expressive | Ads, high-energy narration |

## Selection Tips

- **For Japanese**: F3 and M2 work particularly well. F3 has a natural softness that fits Japanese prosody.
- **For Hindi**: F2 and M1 are clear and articulate with Indo-Aryan phonetics.
- **For Korean**: F1 and M3 handle Hangul cleanly.
- **For multilingual scripts**: Stick with one voice per language. Switching voices mid-sentence can sound disjointed.
- **For expression tags**: M5 and F4 are most responsive to tags like `<happy>`, `<excited>`, `<sarcastic>`.
- **For dramatic/briefing content**: M3 is the deepest, most authoritative male voice.

## Language-Agnostic Mode

Pass `lang="na"` to let Supertonic auto-detect the input language. Good for:
- Mixed-language text
- Unknown input language
- Quick prototyping without looking up ISO codes

Trade-off: slightly less accurate prosody than explicit language tagging.

## Voice Cloning (Voice Builder)

Supertonic supports zero-shot voice cloning via [Voice Builder](https://supertonic.supertone.ai/voice_builder).

### Workflow

1. **Record** a short reference clip (~10–30 seconds of clear speech)
2. **Upload** to Voice Builder (https://supertonic.supertone.ai/voice_builder)
3. **Export** the voice style as a JSON file
4. **Load** it locally:

```python
from supertonic import TTS

tts = TTS(auto_download=True)
style = tts.get_voice_style_from_path("voices/my_voice.json")

wav, _ = tts.synthesize(
    "Hello in my own cloned voice.",
    voice_style=style,
    lang="en",
)
tts.save_audio(wav, "output.wav")
```

### Properties

- **Permanent ownership** — Once cloned, the voice JSON is yours forever. No subscription, no expiring credits.
- **Offline deployment after cloning** — The exported voice style JSON runs entirely on-device alongside the base model. No cloud calls are made during synthesis.
- **Privacy note** — The initial voice cloning step requires uploading a reference audio clip to Supertone's online Voice Builder service (https://supertonic.supertone.ai/voice_builder). Biometric voice data is transmitted to a third party during this step. Do not use this feature if your environment is air-gapped, regulated, or requires keeping voice samples fully offline. Built-in voices require no upload and are fully offline.

### CLI with Custom Voice

```bash
supertonic tts "Hello in my voice." -o output.wav \
  --custom-style-path voices/my_voice.json
```

### Limitations

- Quality depends on the reference recording. Quiet, clean audio with minimal background noise works best.
- Very short clips (<5s) may not capture vocal characteristics well.
- Extreme pitch shifts or heavy accents outside the training distribution may produce artifacts.
