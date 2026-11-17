## Description:

Automate web browser interactions using natural language via CLI commands for browsing websites, navigating pages, extracting data, taking screenshots, filling forms, clicking buttons, and interacting with web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peytoncasper](https://clawhub.ai/user/peytoncasper)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to drive a browser from natural language CLI commands for web navigation, page interaction, structured extraction, screenshots, and form workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad browser control that may interact with sensitive accounts, admin consoles, internal services, or private data.

Mitigation: Use isolated browser profiles, avoid sensitive sites unless explicitly approved, and clear cookies and saved passwords after use.

Risk: Browserbase mode may be selected automatically when configured API keys are present.

Mitigation: Review environment variables and .env configuration before running browser commands so local or remote execution is intentional.

Risk: Persistent browser sessions can retain cookies and passwords between runs.

Mitigation: Use a dedicated profile for automation and remove or reset the profile when handling private or regulated workflows.

Risk: Automatic downloads can save unreviewed files to the workspace.

Mitigation: Inspect downloaded files before opening or executing them and clear the downloads directory after tasks.

Risk: The submitted artifact references implementation files that are not included for review.

Mitigation: Review the installed implementation and dependencies before deploying the skill in a shared or production environment.

## Reference(s):

- [Stagehand Browser CLI on ClawHub](https://clawhub.ai/peytoncasper/skills/stagehand-browser-cli)
- [Browser Automation CLI Reference](artifact/REFERENCE.md)
- [Browser Automation Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands, JSON command outputs, screenshots, and downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser commands can produce screenshots under ./agent/browser_screenshots/ and downloads under ./agent/downloads/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
