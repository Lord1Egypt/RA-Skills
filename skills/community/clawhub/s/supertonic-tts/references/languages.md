# Supported Languages

Supertonic supports 31 languages. Pass the ISO 639-1 code to `lang=` or use `"na"` for automatic language detection.

## Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| ar | Arabic | lt | Lithuanian |
| bg | Bulgarian | pl | Polish |
| hr | Croatian | pt | Portuguese |
| cs | Czech | ro | Romanian |
| da | Danish | ru | Russian |
| nl | Dutch | sk | Slovak |
| en | English | sl | Slovenian |
| et | Estonian | es | Spanish |
| fi | Finnish | sv | Swedish |
| fr | French | tr | Turkish |
| de | German | uk | Ukrainian |
| el | Greek | vi | Vietnamese |
| hi | Hindi | | |
| hu | Hungarian | | |
| id | Indonesian | | |
| it | Italian | | |
| ja | Japanese | | |
| ko | Korean | | |
| lv | Latvian | | |

## Language-Agnostic Mode

```python
wav, duration = tts.synthesize(
    text="Text of unknown language",
    lang="na",  # "na" = language-agnostic
    voice_style=style,
)
```

When to use `na`:
- Mixed-language input
- Unknown source language
- Quick prototyping

When to use explicit codes:
- Known single-language text
- Best prosody accuracy
- Production use
