# Voiceover worked recipes

Three end-to-end recipes for the `voiceover` skill. Each shows the scenario, the real `audioInference` request, and the result shape. Adapt the script, voice, and tags. Confirm field names and ranges against the live schema (`runware-run`) before sending, and run every request asynchronously, then poll `getResponse` and read `audioURL`.

Field reminders verified against the live schema:

- Fish S2.1 Pro `speech.voice` is a voice model ID (a hex string like `933563129e564b19a115bedd57b7406a`), not a name. Paralanguage `(cues)` and `<|phoneme|>` overrides need `settings.normalize: false`.
- Inworld TTS-2 `speech.voice` is a named preset from the enum (`Sarah`, `Ashley`, `Mark`, and so on) and is required. `settings.textNormalization: true` expands numbers, dates, and abbreviations.
- Response is `audioInference` returning `audioUUID` and `audioURL`.

## Recipe 1: Emotional ad read (Fish S2.1 Pro, inline delivery tags)

Scenario: a 15-second product ad. Open warm and inviting, lift into excitement on the offer, land on a confident close. Tags carry the delivery forward and shift only at each emotional beat. Paralanguage `(break)` paces the read, so normalization is off.

Request:

```json
[
  {
    "taskType": "audioInference",
    "model": "fishaudio:s2.1@pro",
    "speech": {
      "text": "[with gentle warmth] Picture your morning, but quieter. [excited] Introducing Aria, the smart mug that keeps your coffee at the perfect temperature all day long! (break) [confident, slowing down] Aria. Your coffee, exactly how you like it.",
      "voice": "933563129e564b19a115bedd57b7406a"
    },
    "settings": {
      "normalize": false
    }
  }
]
```

Notes:

- The first tag applies from the start until `[excited]`, which applies until `[confident, slowing down]`. No tag is closed or reset.
- `(break)` inserts a paced pause before the tagline. It only works with `settings.normalize: false`.
- Keep one or two compatible tags per beat. Give each beat a full sentence so the delivery lands.

Result:

```json
{
  "data": [
    {
      "taskType": "audioInference",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "audioUUID": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
      "audioURL": "https://am.runware.ai/audio/os/a14d18/ws/2/ai/f1e2d3c4-b5a6-7890-1234-567890abcdef.mp3"
    }
  ]
}
```

## Recipe 2: Calm explainer with text normalization (Inworld TTS-2)

Scenario: a product explainer line piped from raw text full of numbers, a price, and a date. Read it calm and measured. Let normalization speak the digits cleanly so the script stays readable.

Request:

```json
[
  {
    "taskType": "audioInference",
    "model": "inworld:tts@2",
    "speech": {
      "text": "[calm and steady, with a warm tone and measured pace] Your plan covers up to 250 GB per month. Renewal is on 03/15/2026, and the total is $1,249.99.",
      "voice": "Sarah"
    },
    "settings": {
      "textNormalization": true
    }
  }
]
```

Notes:

- With `textNormalization: true`, the model expands `250 GB`, `$1,249.99`, and `03/15/2026` into spoken form. Without it, write those in spoken form yourself.
- Dates are ambiguous under normalization (`03/15/2026` is unambiguous, but `01/02/2026` is not). For application-handled dates, pre-expand them in the text and leave normalization for the rest.
- One calm tag at the start carries the whole line. Do not tag every sentence.
- `speech.voice` is required for Inworld and must be a name from the preset enum.

Result:

```json
{
  "data": [
    {
      "taskType": "audioInference",
      "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "audioUUID": "e2d3c4b5-a6f7-8901-2345-67890abcdef1",
      "audioURL": "https://am.runware.ai/audio/os/a14d18/ws/2/ai/e2d3c4b5-a6f7-8901-2345-67890abcdef1.mp3"
    }
  ]
}
```

## Recipe 3: Branded IVR greeting (Inworld TTS-2, no fillers)

Scenario: a phone-system greeting for a brand. Professional and friendly, no filler words, account and option numbers spoken digit by digit. Normalization on for the menu numbers, capitalization to stress the key option.

Request:

```json
[
  {
    "taskType": "audioInference",
    "model": "inworld:tts@2",
    "speech": {
      "text": "[warm and professional, clear and unhurried] Thank you for calling Northwind Bank. For account balances, press 1. To report a lost card, press 2. For everything else, stay on the line and the NEXT available agent will help you.",
      "voice": "Mark"
    },
    "settings": {
      "textNormalization": true
    }
  }
]
```

Notes:

- No filler words. "Uh" or "um" make an IVR sound broken. Keep the read clean and professional.
- `NEXT` in caps stresses one word. Use emphasis on one or two words at most.
- `textNormalization: true` speaks `1` and `2` as menu numbers. For account numbers read digit by digit, write them spaced in the text (`one two three four`) so they are not collapsed into a single number.
- One steering tag sets the tone for the whole greeting.

Result:

```json
{
  "data": [
    {
      "taskType": "audioInference",
      "taskUUID": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "audioUUID": "d3c4b5a6-f7e8-9012-3456-7890abcdef12",
      "audioURL": "https://am.runware.ai/audio/os/a14d18/ws/2/ai/d3c4b5a6-f7e8-9012-3456-7890abcdef12.mp3"
    }
  ]
}
```
