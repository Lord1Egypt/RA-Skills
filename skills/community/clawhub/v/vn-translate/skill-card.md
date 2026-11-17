## Description:

Translates long-form fiction from a source language into Vietnamese through a sequential workflow that preserves names, forms of address, chapter structure, and final Markdown or EPUB outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaibazax-dev](https://clawhub.ai/user/kaibazax-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and translation-focused developers use this skill to translate fiction into Vietnamese in manageable sequential chunks, maintain terminology and address-form consistency, and assemble the translated work as Markdown or EPUB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: EPUB export can unintentionally package local files outside the intended assets folder if crafted Markdown image paths are supplied.

Mitigation: Install only for trusted Markdown inputs or review and constrain EPUB image path handling before use; run the workflow in a dedicated project folder and preview cleanup deletes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaibazax-dev/skills/vn-translate)
- [Worked translation-session example](references/session-worked-example.md)
- [Vietnamese idioms and terminology reference](references/thanh-ngu-va-tu-ngu.md)
- [Token usage diagnostics](references/token-usage-diagnostics.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, Python helper usage, JSON checkpoint data, translated Markdown files, and optional EPUB output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses sequential chunk processing and checkpoint files; EPUB export should be used only with trusted or reviewed Markdown inputs.]

## Skill Version(s):

1.1.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
