# SSML `say-as` in Zvukogram — patterns and examples

Source (official hub): https://zvukogram.com/node/ssml/

Use `say-as` when plain text is ambiguous (numbers, dates, money, phone numbers) or when you want a deliberate speaking style (spelling out).

General syntax:

```xml
<say-as interpret-as="MODE" [format="..."] [detail="..."]>VALUE</say-as>
```

Below are the **modes agents should know** with copy-paste examples and common pitfalls.

## 1) spell-out / characters / verbatim

Spell a word/abbr out letter-by-letter.

```xml
<say-as interpret-as="spell-out">ООО</say-as>
<say-as interpret-as="spell-out">банан</say-as>
```

Use cases:
- abbreviations (API, LLM)
- serials / codes where reading as a word is wrong

## 2) cardinal (quantity)

For “сколько?” (5 → “пять”).

```xml
У нас <say-as interpret-as="cardinal">5</say-as> сервисов.
```

If you need grammatical control (some “advanced” voices support it), see the official `/node/cardinal/` examples.

## 3) ordinal (order)

For “который по счёту?” (3 → “третий”).

```xml
Возьми <say-as interpret-as="ordinal">3</say-as> пункт.
```

## 4) fraction

Fractions like 1/2.

```xml
<say-as interpret-as="fraction">1/2</say-as>
<say-as interpret-as="fraction">3+1/2</say-as>
```

Important:
- `3+1/2` means “три целых и одна вторая” (no spaces).
- Not all voices support `fraction` (see `references/SSML.md` for the voice support list).

## 5) date

### A) Basic W3C-style (format dmy/mdy/ymd… + detail=1)

```xml
<say-as interpret-as="date" format="dmy" detail="1">5/7/24</say-as>
<say-as interpret-as="date" format="ymd" detail="1">1945.05.09</say-as>
```

Rules:
- separators: `-`, `/`, `.`
- `format`: `dmy`, `mdy`, `ymd`, `ym`, `my`, `md`, `dm`, `d`, `m`, `y`

### B) Advanced case-aware style (some voices)

```xml
<say-as interpret-as="date" format="accusative" detail="d-m-y">25-1-2000</say-as>
<say-as interpret-as="date" format="accusative" detail="m-yw">02-2000</say-as>
```

Notes:
- Here `format` becomes grammatical case (`nominative|genitive|dative|accusative|ablative|prepositional`).
- `detail` becomes a template, and the value uses `-` separators.
- `y` adds “год/года”, `yw` suppresses it.

## 6) time

```xml
<say-as interpret-as="time">13:45</say-as>
<say-as interpret-as="time" format="hms12">4:50</say-as>
<say-as interpret-as="time" format="hms12">4:50am</say-as>
<say-as interpret-as="time" format="hms24">04:50</say-as>
```

## 7) telephone

```xml
<say-as interpret-as="telephone">88005557778</say-as>
<say-as interpret-as="telephone" detail="use-round-word">+7 (495) 600-35-56</say-as>
```

Pitfalls:
- If you insert separators, keep digit groups small (<= 3) or the voice may error.
- Some voices do not support `telephone` (see `references/SSML.md`).

## 8) currency (simple)

Use when the value contains amount + currency code.

```xml
<say-as interpret-as="currency">99.9 USD</say-as>
<say-as interpret-as="currency">99 CHF</say-as>
```

Support is voice-dependent.

## 9) money (advanced)

Some “advanced” voices support `money` with grammatical cases and currency variants.

```xml
<say-as interpret-as="money" detail="USD">21</say-as>
<say-as interpret-as="money" detail="USD_full-form">21,15</say-as>
<say-as interpret-as="money" detail="USD_short-form_say-null-cents">10</say-as>
```

Notes:
- `detail` encodes currency and output form.
- Some voices support `format` for grammatical case (see official currency docs for `money`).

## 10) spell-out vs `sub alias` for acronyms

- Use `spell-out` when you want “read letters”.
- Use `<sub alias="...">` when you want a **specific** pronunciation (e.g. “Магатэ” for IAEA).

Examples:

```xml
<say-as interpret-as="spell-out">IAEA</say-as>
<sub alias="Магатэ">IAEA</sub>
```
