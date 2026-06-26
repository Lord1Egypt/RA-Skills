# Smallest AI — Supported Languages

## TTS (Lightning Model) — 30+ Languages

| Code | Language         | Code | Language         |
|------|------------------|------|------------------|
| en   | English          | hi   | Hindi            |
| es   | Spanish          | fr   | French           |
| de   | German           | it   | Italian          |
| pt   | Portuguese       | nl   | Dutch            |
| pl   | Polish           | ro   | Romanian         |
| sv   | Swedish          | da   | Danish           |
| no   | Norwegian        | fi   | Finnish          |
| cs   | Czech            | sk   | Slovak           |
| hu   | Hungarian        | el   | Greek            |
| tr   | Turkish          | ru   | Russian          |
| uk   | Ukrainian        | ar   | Arabic           |
| ja   | Japanese         | ko   | Korean           |
| zh   | Chinese          | th   | Thai             |
| vi   | Vietnamese       | id   | Indonesian       |
| ms   | Malay            | tl   | Filipino/Tagalog |
| bn   | Bengali          | ta   | Tamil            |
| te   | Telugu           | mr   | Marathi          |
| gu   | Gujarati         | kn   | Kannada          |

## STT (Pulse Model) — 36 Languages

Pulse supports all TTS languages plus additional dialects.

Features per language:
- Word-level timestamps: All languages
- Speaker diarization: All languages
- Emotion detection: English, Hindi (more coming)
- Code-switching: English-Hindi, English-Spanish (more coming)

## Code-Switching

Lightning handles mixed-language text automatically. No special flags needed:

```bash
# Hindi-English mix
tts.sh "Hey, मुझे 5 बजे meeting remind कर दो" --lang hi

# Spanish-English mix
tts.sh "Let's go to the fiesta tonight" --lang es
```

## Usage Notes

- Set `--lang` to the primary language of the text
- For code-switching, use the language of the majority content
- Regional accents are automatically handled based on voice selection
- New languages are added regularly — check waves-docs.smallest.ai
