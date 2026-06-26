# ElevenLabs Voice Catalog — Dark Motivation

## Top Voices for Dark Motivation Content

| Voice Name | Voice ID | Gender | Accent | Best For |
|---|---|---|---|---|
| Adam | pNInz6obpgDQGcFmaJgB | Male | American | Deep stoic, authoritative |
| Antoni | ErXwobaYiN019PkySvjV | Male | American | Warm intensity |
| Josh | TxGEqnHWrfWFTfGW9XjX | Male | American | Cinematic, dramatic |
| Arnold | VR6AewLTigWG4xSOukaG | Male | American | Villain arc, gravelly |
| Daniel | onwK4e9ZLuTAKqWW03F9 | Male | British | Sophisticated, poetic |
| Clyde | 2EiwWnXFnvU5JabPnv8n | Male | American | Rugged, serious |
| Fin | D38z5RcWu1voky8WS1ja | Male | Irish | Storytelling, poetic |
| Harry | SOYHLrjzK2X1ezoPC6cr | Male | American | Intense, aggressive |

## Voice Settings Guide

### Dark & Stoic (default for motivation)
```python
{
    "stability": 0.75,
    "similarity_boost": 0.85,
    "style": 0.25,
    "use_speaker_boost": True
}
```

### Dark & Aggressive (villain arc content)
```python
{
    "stability": 0.55,
    "similarity_boost": 0.80,
    "style": 0.55,
    "use_speaker_boost": True
}
```

### Dark & Poetic (emotional, philosophical)
```python
{
    "stability": 0.65,
    "similarity_boost": 0.80,
    "style": 0.40,
    "use_speaker_boost": True
}
```

## Model Recommendations

- `eleven_multilingual_v2` — Best quality, supports Vietnamese/English/multilingual
- `eleven_monolingual_v1` — Faster, English only
- `eleven_turbo_v2_5` — Fastest, use when speed matters

## Vietnamese Content

For Vietnamese motivation videos use `eleven_multilingual_v2` model.
Voice "Daniel" (British English) actually renders Vietnamese surprisingly well.
Test custom voice cloning for authentic Vietnamese accent.

## Tips

- Lower stability (0.4-0.6) = more expressive, emotional delivery
- Higher stability (0.7-0.9) = consistent, controlled, robotic
- Style > 0.5 = exaggerated emotion (can sound unnatural)
- Always use `use_speaker_boost: True` for clarity
