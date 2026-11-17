---
name: translate-to-chn
description: >
  Translate a specific article from ai-thoughts/docs/ into Simplified Chinese,
  writing the output to an exactly-same-filename "-chn.md" file. Use when the
  user names a specific article and asks to translate it (e.g. "translate
  260803-ollama-to-llamacpp", "翻译 xxx", "make a -chn.md version"). Never
  runs automatically; only acts on an explicitly chosen article.
---

# Translate to Chinese (-chn.md)

Translate one article from `ai-thoughts/docs/` into Simplified Chinese and write it to a new file with the same filename plus a `-chn.md` suffix.

## Approval gate — read before anything else

- **Never translate, write, or create anything without explicit user approval.** This skill converts on demand only; it does not run automatically and it does not pick candidate articles on its own.
- **No action if no article is specifically chosen.** The user must point out exactly one article (by filename, slug, or date). If they don't, do nothing except ask which one.
- Before writing the output, confirm the plan with the user: the source file, the exact output path, and whether an existing `-chn.md` should be overwritten.

## Inputs

- `source` — Path to the source article, e.g. `ai-thoughts/docs/260803-ollama-to-llamacpp.md`. Required. If the user only names an article by slug or date, locate it in `ai-thoughts/docs/`.

## Outputs

- `outputPath` — Path to the translated article: `docs/<exact-same-filename>-chn.md` (replace the `.md` suffix with `-chn.md`, keeping the `YYMMDD-slug` prefix and all characters exactly). Example: `260803-ollama-to-llamacpp.md` → `260803-ollama-to-llamacpp-chn.md`.

## Procedure

1. **Wait for the user to point out the article** to translate. Do not start until they name it explicitly.
2. **Confirm the plan** with the user: the source file and the output path. Get their go-ahead before writing anything.
3. **Check for an existing `-chn.md`.** If `docs/<same>-chn.md` already exists, stop and ask whether to overwrite it, diff against it, or skip. Never overwrite silently.
4. **Read the source** article from `source`. Understand the full content before translating.
5. **Translate the body** into Simplified Chinese:
   - Keep the title as an H1 with the key term followed by a Chinese
     translation (match the style of existing `-chn.md` pairs).
   - Right after the H1, add the source link line, using the **absolute GitHub URL** (the `j3ffyang` repo), not a relative link:
     `**原文：** [<source-filename>](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/<source-filename>)`
   - Translate the running text, headings, and bullets faithfully and
     naturally. Do not add, remove, or reorder content.
   - Write Simplified Chinese by default; Traditional Chinese only when the
     source was originally written that way.
   - Apply the bilingual-gloss style below: gloss technical terms and section
     titles, and add plain-language explanations for unfamiliar concepts.
6. **Do not translate specific terms** — leave them verbatim:
   - Product, tool, and agent names: Hermes Agent, OpenCode, OpenClaw, Astro,
     etc.
   - Technical terms, commands, flags, config and file names (`AGENTS.md`,
     `SOUL.md`, `.cursorrules`, `hermes -c`), environment variables, URLs.
   - Code blocks, inline code, CLI keystrokes (`Ctrl+C`, `Alt+Enter`).
   - Existing proper nouns already in Latin script. Only translate the surrounding prose; never translate inside code.
7. **Preserve everything else exactly**: `../imgs/<file>` image references (keep the path verbatim — Chinese files mirror English per AGENTS.md), links, HTML, tables, frontmatter (if any), and Markdown structure.
8. **Write the output** to `docs/<same-filename>-chn.md` with the source link line followed by the translated body.
9. **Arch sign-off**: if the source ends with `btw, i use arch`, append the identical line at the bottom of the `-chn.md`. Keep it verbatim English — do not translate.
10. **Report** `outputPath` to the user. Do not modify the source file, and do not touch `articles.yaml` or the READMEs (out of scope for this skill).

## Bilingual-gloss style (default)

Every `-chn.md` uses this style: Simplified Chinese is the primary text, and English is added as glosses so a Chinese-only reader still gets the technical vocabulary. The source article stays as-is; the glosses and explanations live only in the `-chn.md`.

1. **Gloss technical terms inline.** The first meaningful time a technical term appears, follow it with the English in parentheses: `技能 (skill)`, `无头 (headless)`, `密钥链 (keychain)`, `接口额度 (API quota)`. Don't gloss every repetition or everyday words — only technical or specialized vocabulary.
2. **Gloss section titles.** Add the gloss to headings that contain technical terms: `## 技能 (skill) 是什么`, `## 无头 (headless) 环境下的认证`.
3. **Add plain-language explanations.** For concepts a general reader won't know (e.g. what 无头 (headless) 环境 means), add a short, simple explanation in plain Chinese at the first use. Understanding beats literal fidelity here — the explanation may be a small addition to the source, since the goal is a standalone readable article for a Chinese audience.
4. **Gloss inside tables too.** The same rules apply to table cells — gloss technical terms on first appearance: `| 我——思维流 (thought-flow) | OpenCode + git——工作流 (workflow) |`.

The verbatim exceptions from Procedure step 6 still apply: code, commands, product names, and URLs stay untouched, and glosses never go inside code blocks.

## Quality rules

- **Avoid hallucination.** If a word, reference, or term is unclear, do not guess — ask the user or flag it in the report. Never invent translations, names, dates, or content that is not in the source.
- **Ask if anything is unclear** — about the article, an ambiguous phrase, an unknown acronym, or the intended output. Clarify rather than assume.
- Translate meaning faithfully and naturally in Simplified Chinese; do not perform a word-for-word substitution.

## Verification

- Output is at `docs/<exact-source-filename>-chn.md`; the prefix and slug match the source filename exactly (only the `.md` → `-chn.md` suffix changed).
- The source link line is present right after the H1 and uses the **absolute GitHub URL**: `**原文：** [<source-filename>](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/<source-filename>)`.
- Every `../imgs/<file>` reference in the output matches one in the source (verify with a glob/ls against `ai-thoughts/imgs/`).
- Code blocks, inline code, commands, and specific terms (e.g. Hermes Agent, OpenCode) are preserved verbatim.
- The bilingual-gloss style is applied: technical terms and headings carry English glosses, table cells are glossed on first appearance, and unfamiliar concepts get a plain-language explanation at first use.
- If the source ends with the arch sign-off (`btw, i use arch`), the `-chn.md` carries the identical verbatim line.
- The source file is unmodified (confirm via git status/diff).

## Error Handling

- **No article chosen**: do nothing; ask the user which article to translate.
- **Source not found**: list candidate files in `ai-thoughts/docs/` and ask which to use.
- **Output already exists**: stop and ask whether to overwrite, diff against it, or skip.
- **Ambiguous or untranslatable content**: ask the user instead of guessing.
