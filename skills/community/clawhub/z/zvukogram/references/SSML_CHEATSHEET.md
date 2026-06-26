# SSML Cheatsheet

## Quick Reference

### Stress Marks
```
З+амок     → stress on "a"
зам+ок     → stress on "o"
```

### Aliases (Transcription)
| Original | SSML | Result |
|----------|------|--------|
| OpenAI | `<sub alias="Оупен Эй Ай">OpenAI</sub>` | Оупен Эй Ай |
| Samsung | `<sub alias="Самсунг">Samsung</sub>` | Самсунг |
| SK Hynix | `<sub alias="Эс Кей Хайникс">SK Hynix</sub>` | Эс Кей Хайникс |
| Altman | `<sub alias="Ал+ьтман">Altman</sub>` | Ал+ьтман |
| GPT | `<sub alias="Джи Пи Ти">GPT</sub>` | Джи Пи Ти |
| API | `<sub alias="Эй Пи Ай">API</sub>` | Эй Пи Ай |
| AI | `<sub alias="Эй Ай">AI</sub>` | Эй Ай |
| IAEA | `<sub alias="Магатэ">IAEA</sub>` | Магатэ |

### Speed
```xml
<prosody rate="1.2">20% faster</prosody>
<prosody rate="fast">Fast text</prosody>
<prosody rate="slow">Slow text</prosody>
```

### Pauses
```xml
<break time="300ms"/>  <!-- 0.3 sec -->
<break time="1s"/>     <!-- 1 sec -->
<break time="2s"/>     <!-- 2 sec -->
```

### Volume and Pitch
```xml
<prosody volume="+6dB">Louder</prosody>
<prosody volume="-6dB">Quieter</prosody>
<prosody pitch="+2st">Higher pitch</prosody>
<prosody pitch="-2st">Lower pitch</prosody>
```

### Multi-voice Podcast Pattern (API-safe)

Zvukogram API multi-voice is typically done by **separate requests per voice** and then merging audio fragments.

Example SSML snippet (content only, per fragment):
```xml
Доброе утро! Вы слушаете <sub alias="Эй Ай Дейли">AI Daily</sub>.
<break time="300ms"/>
Сегодня обсудим <sub alias="Оупен Эй Ай">OpenAI</sub>.
```

## Tags by Category

### Pauses
- `<break time="..."/>` — pause

### Prosody (Intonation)
- `<prosody rate="...">` — speed
- `<prosody pitch="...">` — pitch
- `<prosody volume="...">` — volume

### Pronunciation
- `<sub alias="...">` — alias
- Stress marks with `+` — put `+` before stressed vowel (quick + robust)
- `<phoneme alphabet="ipa" ph="...">` — phonetic transcription (expert)

### Formatting (`say-as`)
- `<say-as interpret-as="spell-out">` — spell out letters
- `<say-as interpret-as="cardinal">` — cardinal number (quantity)
- `<say-as interpret-as="ordinal">` — ordinal number (order)
- `<say-as interpret-as="fraction">` — fractions
- `<say-as interpret-as="date">` — dates
- `<say-as interpret-as="time">` — time
- `<say-as interpret-as="telephone">` — phone numbers
- `<say-as interpret-as="currency">` — currency (limited voices)
- `<say-as interpret-as="money">` — money (advanced voices)
- `<say-as interpret-as="bleep">` — censorship
