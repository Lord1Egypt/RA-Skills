## Description:

Build and query a searchable FAQ knowledge base from markdown files for WhatsApp business bot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

External business teams and developers use this skill to build a local FAQ knowledge base, search customer questions, and return likely answers for WhatsApp assistant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported FAQ content is stored locally on disk by default.

Mitigation: Set FAQ_BOT_DIR to an approved storage location and avoid importing confidential content unless local storage is acceptable.

Risk: Removing an FAQ entry deletes it immediately.

Mitigation: Export or back up the knowledge base before removing entries that may need to be restored.

Risk: Export can overwrite the selected output file.

Mitigation: Choose a new output path or verify the target file before running export with an output argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/whatsapp-faq-bot)
- [Publisher profile](https://clawhub.ai/user/mariusfit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search commands return JSON matches with confidence scores; export can produce Markdown or JSON files.]

## Skill Version(s):

1.0.0 (source: _meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
