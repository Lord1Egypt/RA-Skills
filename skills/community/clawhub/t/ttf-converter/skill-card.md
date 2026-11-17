## Description:

Local-only skill for converting horizontal Chinese fonts into high-quality vertical-reading TTF fonts with a preview-first workflow, grouped glyph rules, and local audit/test artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aster-copilot](https://clawhub.ai/user/aster-copilot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert horizontal Chinese font files into local vertical-reading font deliverables. It guides source-font checks, preview-first validation, grouped glyph conversion, and generation of reader test artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A poor source font can produce misleading or low-quality vertical output.

Mitigation: Open the source font and review the horizontal preview before building the vertical font.

Risk: Generated punctuation, quotes, Latin text, or digits may be misplaced for a specific font.

Mitigation: Review the vertical preview and use the audit script for representative glyph placement before accepting the final font.

Risk: The workflow writes generated files to user-selected local paths.

Mitigation: Choose input and output paths deliberately and keep the workflow local-only.

Risk: The source font may have license restrictions for modification or use.

Mitigation: Confirm rights to modify and use the source font before converting or distributing the generated font.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aster-copilot/skills/ttf-converter)
- [Workflow](artifact/references/workflow.md)
- [Rules](artifact/references/rules.md)
- [Implementation notes](artifact/references/implementation-notes.md)
- [Default configuration](artifact/references/default-config.json)
- [Examples](artifact/references/examples.md)
- [Real cases - Zihun Songkekaiti](artifact/references/cases-zihun-songkekaiti.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated local files, including preview PNGs, a vertical font file, reader TXT, and optional audit JSON or terminal output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only workflow; output should be previewed before final font delivery.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
