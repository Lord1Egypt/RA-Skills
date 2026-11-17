## Description:

Universal Translate translates text, files, and conversations between languages with automatic source language detection while preserving formatting, tone, and technical terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate ad hoc text, documentation files, batches, and interpreter-style conversations across languages while keeping structure and technical content intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File translation may create translated copies in the workspace, which can matter when similar output filenames already exist.

Mitigation: Check expected output filenames and use an explicit target language or suffix before translating files.

Risk: If no target language is supplied, non-English text defaults to English translation.

Mitigation: Specify the desired target language when English is not intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanthienha199/skills/universal-translate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown or translated file content with preserved formatting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create translated copies using language-code filename suffixes for file translation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
