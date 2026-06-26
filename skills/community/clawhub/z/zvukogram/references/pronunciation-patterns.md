# Pronunciation & transcription patterns (Zvukogram)

This is a **practical** guide for making names/brands/acronyms sound right in Russian TTS.

Primary sources:
- SSML hub: https://zvukogram.com/node/ssml/
- Phoneme (IPA) doc: https://zvukogram.com/node/mfa/

## 1) Fast path: stress with `+`

Zvukogram supports a simple stress mark: put `+` **before the stressed vowel**.

Examples:

- `з+амок` vs `зам+ок`
- `Ал+ьтман`

Use this when:
- a Russian word is ambiguous
- a foreign surname in Cyrillic needs stress guidance

## 2) Reliable path: `<sub alias="...">` for brands and acronyms

Use `<sub>` to force stable pronunciation, especially when the original token is Latin.

```xml
<sub alias="Оупен Эй Ай">OpenAI</sub>
<sub alias="Джи Пи Ти">GPT</sub>
<sub alias="Эй Пи Ай">API</sub>
<sub alias="Эс Кью Эл">SQL</sub>
```

Pattern tips:
- If the correct pronunciation is “by letters”, alias it in Cyrillic letter names.
- If the correct pronunciation is a known Russian word, alias directly (e.g. `IAEA → Магатэ`).
- Include stress marks inside alias when needed: `Ал+ьтман`.

## 3) When `<say-as interpret-as="spell-out">` is better than `<sub>`

Use `spell-out` when you want *letters of the same script* read out and don’t care about stylistic nuances.

```xml
<say-as interpret-as="spell-out">ООО</say-as>
```

If you need a *very specific* reading, use `<sub>`.

## 4) Expert path: `<phoneme alphabet="ipa">` (precise)

Use this when:
- stress marks aren’t enough
- you need to encode reduced vowels / palatalization
- you want repeatable pronunciation across voices

Example (from official docs):

```xml
<phoneme alphabet="ipa" ph="nʲɪkˈitʲənko">Никитенко</phoneme>
```

Practical notes:
- Primary stress in IPA uses `ˈ`.
- For Russian vowels, the official doc discusses symbols like `ə`, `ɐ` for unstressed variants.

## 5) Podcast-specific pronunciation workflow

When generating daily podcast scripts:

1) Build a short **alias dictionary** of recurring entities:
   - companies, product names, people, abbreviations
2) Apply `<sub alias>` consistently.
3) Only reach for `<phoneme>` for the top 1% of stubborn words.

Example snippet:

```xml
Сегодня <sub alias="Оупен Эй Ай">OpenAI</sub> выпустила обновление.
<break time="300ms"/>
На связи <sub alias="Сэм Ал+ьтман">Sam Altman</sub>.
```

## 6) Things that commonly break pronunciation

- Mixed Latin/Cyrillic in one token: prefer splitting or aliasing.
- Numbers embedded in names (e.g. GPT-4.1): consider `<say-as interpret-as="cardinal">4</say-as>` or alias it fully.
- Very long hyphenated brand strings: alias to a shorter spoken form.
