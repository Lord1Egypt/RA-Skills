## Description:

Render structured table data as high-quality PNG images using Headless Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[con2000us](https://clawhub.ai/user/con2000us)

### License/Terms of Use:


## Use Case:

Developers and agents use zenTable to convert messy table-like text, structured JSON, or OCR-assisted screenshot data into readable visual table outputs for chat interfaces, reports, and social sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Python and Chrome rendering code and may use local OCR services.

Mitigation: Review the pinned release scripts before execution and install or run the runtime in a controlled environment.

Risk: OCR or rendering workflows may process sensitive table screenshots or photos.

Mitigation: Use a sandbox, virtual machine, or container for sensitive data and keep OCR endpoints bound to localhost or a private network unless intentional exposure is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/con2000us/skills/zentable)
- [Pinned runtime release](https://github.com/con2000us/zenTable/releases/tag/skillhub-zentable-beta-2026-03-01)
- [Source repository](https://github.com/con2000us/zenTable)
- [GitHub Issues](https://github.com/con2000us/zenTable/issues)

## Skill Output:

**Output Type(s):** [image files, text, shell commands, configuration, guidance]

**Output Format:** [PNG images with optional TXT side output and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rendering depends on python3 and google-chrome; OCR deployment may use local Docker/FastAPI services.]

## Skill Version(s):

0.9.2 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
