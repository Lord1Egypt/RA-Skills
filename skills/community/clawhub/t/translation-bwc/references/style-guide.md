# BWC Technical Translation Style Guide

Applies to BWC technical and API documentation (中文 ↔ English). Rules here are
mandatory unless the glossary or source overrides them.

## 1. Register & Voice

- API/developer docs: neutral, direct, imperative when the source is imperative.
  - ZH→EN: "调用该接口" → "Call the endpoint."
  - EN→ZH: "Call the endpoint." → "调用该接口。"
- Avoid marketing language inside API docs (no "powerful", "seamless", "轻松").
- Keep sentence length moderate; split long EN sentences rather than force a
  literal 中文 calque.

## 2. Code & Identifiers (never translate)

- API paths, query params, JSON keys, class/method names, enum values, error
  codes: leave verbatim, wrap in backticks.
- Example payloads, code blocks, and curl commands: leave untouched.
- Placeholders `{userId}`, `<region>` stay as-is; do not translate their contents.

## 3. Capitalization

- EN headings: sentence case ("Create a webhook"), not Title Case.
- ZH: no capitalization rules; use full-width punctuation where appropriate.
- Product/brand "BWC" stays uppercase in both languages.

## 4. Units & Formats

- Localize to target locale:
  - Dates: EN → `YYYY-MM-DD` or `MM/DD/YYYY` per doc convention; ZH → `YYYY年MM月DD日` or `YYYY-MM-DD`.
  - Numbers: EN uses commas as thousands separators; ZH uses no separator or
    spaces per convention. Keep consistent within a doc.
  - Timezones: keep `UTC`/`GMT`; add offset if source specifies.

## 5. Lists & Tables

- Preserve ordered/unordered structure. Translate list item text only.
- Table headers: translate, but keep code/identifier headers verbatim.
- Enum/status tables: translate the human label, keep the raw value.

## 6. Terminology Consistency

- One concept → one term. Do not alternate ("租户" vs "客户") for the same idea.
- Prefer glossary term over a literal alternative.
- On first use of an acronym in ZH, give the EN form once: "限流(rate limit)".
- Glossary verbs inflect by tense: a verb entry (e.g. 采集 → offload) must
  agree in tense/number with the sentence (offloads / offloaded / offloading),
  not stay in bare infinitive.

## 7. Untranslatable Items

- Trademarks, third-party product names, protocol names (OAuth2, JWT, REST):
  keep original.
- "Webhook", "token", "endpoint", "payload" commonly stay English even in ZH docs
  unless the glossary localizes them.

## 8. Review Flag

- Any term not in the glossary: append `[NEEDS-GLOSSARY]` and surface it in the
  summary so the user can approve and add it.
