# Podcast-oriented SSML & API patterns (Zvukogram)

This file is for **agents generating spoken podcasts**: rhythm, intelligibility, and stability over long runs.

Key sources:
- SSML hub: https://zvukogram.com/node/ssml/
- API: https://zvukogram.com/node/api/

## 1) Episode skeleton (single voice)

Use short paragraphs, and add pauses at semantic boundaries.

```xml
Доброе утро. Вы слушаете «Нейродисседент».
<break time="300ms"/>
Сегодня три сюжета: безопасность, регуляторика и деньги.
<break time="500ms"/>

Сюжет первый.
<break time="200ms"/>
...
```

Notes:
- Use `<break>` sparingly; too many micro-pauses sound “robotic”.
- Prefer **paragraph breaks** + API `pause_paragraph` for consistent cadence.

## 2) Two-host pattern (API-safe)

Zvukogram API multi-voice is easiest as **one request per voice**, then merge.

Fragment A (voice: Алена):

```xml
Доброе утро! Это новости ИИ.
<break time="250ms"/>
Привет, Андрей.
```

Fragment B (voice: Андрей):

```xml
Привет. Сегодня будет жарко.
<break time="200ms"/>
Начнём с утечки.
```

Merge the generated mp3s (see `chunking-and-method-choice.md`).

## 3) Numbers, dates, and money in news scripts

Example:

```xml
Сделка на <say-as interpret-as="currency">99.9 USD</say-as> закрылась
<say-as interpret-as="date" format="dmy" detail="1">5/7/24</say-as>
в <say-as interpret-as="time">13:45</say-as>.
```

See `references/say-as.md` for more.

## 4) Prosody that doesn’t glitch

Official note: `<prosody>` works best on a **whole sentence**.

Good:

```xml
<prosody rate="fast">Сейчас коротко пройдёмся по фактам.</prosody>
```

Risky (may insert weird pauses around the tag):

```xml
Мы видели <prosody rate="fast">очень</prosody> странный патч.
```

If you need emphasis on a single word, try:
- rewrite the sentence
- use `<emphasis>` on the whole sentence

## 5) Using API-level pauses instead of `<break>` everywhere

For consistent pacing across many chunks, prefer API params:

- `pause_sentence=250`
- `pause_paragraph=450`

Then only use `<break>` for special “beat” moments.

## 6) Background music

If you add music (`music`, `musik_volume`, `musik_loop`), keep it subtle:

- `musik_volume` ~ 30–80 often works better than 100+
- loop music for long episodes: `musik_loop=1`

Tip: if music makes speech less intelligible, reduce music volume before increasing voice volume.

## 7) Intro/outro reusable blocks (with aliases)

```xml
Вы слушаете «Нейродисседент».
<break time="250ms"/>
Сегодня: <sub alias="Оупен Эй Ай">OpenAI</sub>, регуляторы и рынок.
```

Outro:

```xml
Это были новости ИИ. Спасибо, что слушали.
<break time="250ms"/>
Подписывайтесь и делитесь выпуском.
```

## 8) Practical defaults for podcasts

From experience, a sane starting set:

- voice: one of the stable “neutral” voices (e.g. Алена/Андрей)
- `speed`: `1.15–1.25`
- `format`: `mp3`
- `channels`: `1` (mono) is often fine for voice-only podcasts
- `sample_rate`: `24000` or `44100`

Then adjust per publishing pipeline.
