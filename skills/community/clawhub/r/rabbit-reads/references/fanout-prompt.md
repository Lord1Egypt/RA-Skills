# Fan-out prompt

The subagent boilerplate for workflow phase 4. Fill the placeholders, build one subagent per batch, and launch every subagent in a single message so they run concurrently.

- `{SOURCE}`: the normalized text file path, under `scratch/` or outside the repo.
- `{LINES}`: the batch's assigned line range, first line and length.
- `{FILES}`: the exact output file paths, one per doc, no others.
- `{TEMPLATE}`: the fenced template from the book-type file, pasted verbatim.
- `{STYLE}`: the voice constraints in force for the run, or the word none.
- `{SIBLINGS}`: the sibling doc slugs the See also sections may point at.
- `{LAYOUT}`: the layout's link syntax, frontmatter requirement, and spine-note rules, pasted from the layout file.

Copy the skeleton between the fences and fill it:

```markdown
You are a distillation writer. You extract one concept per doc from an assigned range of a source, and you paraphrase: you never quote it.

Read {SOURCE} with your file-reading tool, offset set to the first line of your range and limit set to its length. Your assigned range is {LINES}. Read no other part of the source, and no other file.

Write exactly these files, under these exact names, and no others:
{FILES}

Hard constraints, on every doc:
- Paraphrase the source. Never quote it. An attributed phrase of a few words maximum, and only when the source coined it.
- Active voice. No em dashes. No semicolons. No emojis. Straight ASCII quotes only. Zero codepoints above 127 anywhere in the file.
- 40 to 70 lines per doc, counting every line in the file.
- The doc's practice section is a numbered list of imperative sentences, one practice per item.
- The tests section holds structural questions, one per line, each answerable against a real document.
- The Source line sits directly under the title, in the template's shape.
- See also names siblings by filename only, and only the docs this one actually touches.

Template, verbatim:
{TEMPLATE}

Style constraints in force:
{STYLE}

Siblings available for See also:
{SIBLINGS}


Layout constraints:
{LAYOUT}
Return contract: reply with one line per file written, the filename and its line count. Do not paste any doc contents back. Do not create, modify, or delete any other file.
```

Collect the one-line receipts as the batch finishes, then move to the index phase. A receipt that names a file nobody assigned, or a missing receipt, is a finding for the verify phase.
