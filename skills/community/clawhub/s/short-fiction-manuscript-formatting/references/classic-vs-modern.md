# Courier New, modern rules — not Classic

This skill sets **Courier New** because the writer prefers it. That is not Shunn Classic.

Shunn's short-fiction article is one text in two specimens. Classic means the monospaced specimen **and** two spaces after sentences. Modern means one space, italics, and (in the Times New Roman specimen) a real em dash. His note:

> If a publication specifically asks for "Shunn Classic" format, they mean you should use a Courier font, not Times New Roman.

He also says Courier users may want to leave a dash as two hyphens, because in a monospaced font a true em dash is hard to distinguish from a hyphen. This skill does that. It does **not** add the second space.

| Element | This skill | Shunn Classic — do not do this | Shunn's Times specimen — do not "correct" to this |
|---|---|---|---|
| Font | Courier New, 12 pt | Courier, 12 pt | Times New Roman, 12 pt |
| After `.` `?` `!` | One space | Two spaces | One space |
| Dash | `--`, no spaces | `--`, often | Em dash `—` |
| Emphasis | Italics | Italics unless the market wants underline | Italics |
| What it formats | One short story | One short story | One short story |

If the guidelines say "Shunn Classic" or "two spaces," do not run the emitter (`--classic` is the same refusal). Point them at <https://format.ms/classic>.

If the guidelines require Times New Roman, stop and tell the writer. Do not quietly change the font.

"Standard manuscript format" for a short story, with no other instruction, means this skill: Courier New, one space, italics, `--`.

## The article and this skill are separate

The guide is CC BY-NC-ND 4.0: copy, distribute, and display for non-commercial purposes only, with credit, and with no alterations. No part of it belongs in a submission file, and this skill's output must never contain it.

Concretely, this means the emitter refuses, rather than silently reformatting, when the input looks like the guide itself:

- A story paragraph beginning with `Copyright` is a refusal, not a rewrite. Same for any paragraph starting with the license text or the attribution line.
- Chapter, part, book, prologue, and epilogue headings are novel structure and are refused with `_NOVEL_REFUSAL`.
- A `--classic` request is refused with exit code 2 and writes nothing.
- `--self-test` checks all three refusals, so a regression in any of them is visible.

The copyright notice Shunn's article asks writers to avoid is advice about the writer's own manuscript, not a rule about the guide's text. Do not put a copyright line in a submission, and do not copy the guide's license line into one either.
