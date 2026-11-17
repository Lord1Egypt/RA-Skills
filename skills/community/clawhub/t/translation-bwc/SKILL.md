---
name: translation-bwc
description: "This skill should be used when translating BWC product materials, especially technical and API documentation, in either direction (中文 / English). It applies BWC-specific terminology, preserves code and identifiers, and enforces a consistent technical-writing style. Trigger on requests containing BWC, 翻译, translate, or any BWC product or API doc needing bidirectional EN-ZH conversion."
agent_created: true
---

# BWC Product Translation

## Overview

Translate BWC product content — with emphasis on technical and API documentation —
between 中文 and English while keeping terminology, code, and structure intact.
This skill enforces a single source of truth for BWC terms (the glossary) and a
consistent technical-writing register, so repeated translations stay coherent
across docs, SDK references, and release notes.

## When to Use

- Translating any BWC product material that mentions "BWC" or BWC-specific terms.
- Converting BWC **technical / API documentation** (endpoints, fields, error
  codes, SDK docs, guides) between 中文 and English.
- Localizing release notes, changelogs, or developer-facing copy for BWC.
- Validating that a translated BWC doc uses the approved term for each concept.

If the request is generic translation with no BWC context, this skill does not apply.

## BWC Product Context

BWC is the product family this skill specializes in. Its concrete domain, module
names, and component terms live in `references/glossary.md`. Before translating,
confirm whether the glossary has been populated; if it is still a template, ask
the user to supply the BWC term list or translate using the safest literal
equivalent and flag uncertain terms for review.

## Translation Workflow

1. **Identify scope** — Determine source and target language and whether the
   content is technical/API doc (preserve code) or lighter copy.
2. **Scan for glossary terms** — Extract product names, module names, API
   resource/field names, error codes, and UI labels. Look each up in
   `references/glossary.md`.
3. **Lock approved terms** — Use the glossary's English/中文 term exactly; never
   re-translate an approved term. Mark any term missing from the glossary as
   `[NEEDS-GLOSSARY]` inline.
4. **Translate with conventions** — Follow `references/style-guide.md`:
   preserve identifiers/code, keep sentence case for headings, use consistent
   voice, and localize units/date formats per target language.
5. **Self-check** — Run the Quality Checklist below. Fix terminology drift and
   code corruption before delivering.

## Core Conventions

- **Code is sacred.** API paths, field names, class/method names, error code
  strings, and code blocks are never translated. Wrap them in backticks.
- **Terminology is locked.** Glossary terms override generic translation.
- **BWC acronym.** In source text, "BWC"/"bwc" renders per target language: into
  Chinese → "执法记录仪" (no number inflection); into English → "Body Camera" /
  "Body Cameras" with singular/plural by context. Never leave the bare acronym
  in translated prose.
- **One concept, one term.** Do not use two different translations for the same
  BWC concept within or across docs.
- **Tone.** Developer/technical docs: direct, neutral, imperative where the
  source is imperative ("Call the endpoint" / "调用该接口"). No marketing flourish
  in API docs.
- **Placeholders.** Keep `{curly}` and `<angle>` placeholders intact and untranslated.

## Quality Checklist

- [ ] Every BWC term matches `references/glossary.md` (or is flagged `[NEEDS-GLOSSARY]`).
- [ ] Source "BWC"/"bwc" rendered per target language: 中文→执法记录仪, 英文→Body Camera (singular/plural).
- [ ] No API path, field name, class/method name, or error code was altered.
- [ ] Code blocks, JSON, and example payloads are untouched.
- [ ] Placeholders (`{...}`, `<...>`) preserved.
- [ ] Headings use consistent case; units/date formats localized to target language.
- [ ] No glossary term was silently re-translated.

## Resources

### references/glossary.md
BWC-specific terminology source of truth. Bilingual term table plus sections for
product/module names, API concepts, error codes, and UI labels. Populate before
production use — currently a fill-in template.

### references/style-guide.md
Detailed technical-translation conventions: register, capitalization, units,
dates, lists, tables, and code-handling rules for BWC docs.
