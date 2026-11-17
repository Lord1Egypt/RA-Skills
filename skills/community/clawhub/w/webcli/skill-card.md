## Description:

webcli lets agents browse websites, read page content, click buttons, fill forms, take screenshots, and inspect accessibility snapshots through a headless browser CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdinccurebal](https://clawhub.ai/user/erdinccurebal)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to navigate web pages, inspect page content, interact with forms and controls, capture screenshots or PDFs, and manage browser state during web automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes browser interactions, form submission, uploads, cookie import/export, storage changes, and browser-state save/load.

Mitigation: Use it in an isolated environment and require explicit approval before submissions, uploads, cookie export/import, storage changes, or browser-state save/load on sensitive sites.

Risk: The security verdict is suspicious because the skill uses a mutable global install and provides limited user-control guidance for sensitive browser actions.

Mitigation: Review before installing, prefer a reviewed and pinned package version, and stop the daemon when finished.

## Reference(s):

- [webcli homepage](https://webcli.erdinc.curebal.dev/)
- [webcli repository](https://github.com/erdinccurebal/webcli)
- [ClawHub skill page](https://clawhub.ai/erdinccurebal/skills/webcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce paths to screenshots, PDFs, exported cookies, or saved browser-state files when those commands are used.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
