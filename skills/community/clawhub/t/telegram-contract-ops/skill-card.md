## Description:

Telegram Contract Ops supports internal Vietnamese contract workflows by parsing structured Telegram inputs, generating .docx contracts, OCRing Vietnamese eID screenshots, and routing bot behavior by Telegram group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vt-mmm](https://clawhub.ai/user/vt-mmm)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and developers use this skill to set up, migrate, and run a Telegram bot workflow for Vietnamese contract generation and eID intake. It helps convert structured contract blocks or OCR-derived eID fields into contract-ready data and generated .docx files.

### Deployment Geography for Use:

Vietnam

## Known Risks and Mitigations:

Risk: The workflow handles government ID, bank account, contact, and contract data.

Mitigation: Restrict Telegram access to authorized users, return sensitive results only in private or approved channels, and document permissions for every contract and eID artifact.

Risk: Security evidence reports unsafe storage and retention concerns for eID, OCR, and contract artifacts.

Mitigation: Define retention periods, store artifacts only in controlled directories, and add cleanup for temporary images, OCR output, generated inputs, state, and logs.

Risk: Security evidence reports hardcoded personal and banking data in the package.

Mitigation: Sanitize source files and templates before deployment, and treat any packaged hardcoded personal or banking data as exposed.

Risk: Debug OCR can expose raw identity text.

Mitigation: Disable debug OCR in normal operation or restrict it to administrators with explicit handling and cleanup procedures.

## Reference(s):

- [Telegram Contract Ops Architecture](references/architecture.md)
- [Telegram Contract Ops Deployment](references/deployment.md)
- [Canonical Telegram Contract Input](references/input-template.md)
- [Telegram Contract Ops Troubleshooting](references/troubleshooting.md)
- [Telegram Contract Ops on macOS](references/macos.md)
- [Telegram Contract Ops on Windows](references/windows.md)
- [ClawHub Skill Page](https://clawhub.ai/vt-mmm/skills/telegram-contract-ops)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command snippets, configuration examples, and generated workflow files such as contract .docx outputs or OCR-derived input blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles Telegram text blocks, Vietnamese eID image intake, and local bot workflow setup; sensitive artifacts require controlled access and retention.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
