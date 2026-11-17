## Description:

Smooth Browser helps AI agents navigate websites, fill forms, extract web data, test web apps, and automate browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind)

### License/Terms of Use:


## Use Case:

Developers and AI agents use Smooth Browser to run goal-oriented browser automation tasks, including authenticated web workflows, form completion, data extraction, application testing, and structured scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly handles web actions and may operate inside authenticated browser sessions.

Mitigation: Use anonymous or read-only profiles for routine browsing, create separate profiles per service, and restrict allowed URLs when possible.

Risk: Persistent profiles, uploaded files, and saved browser state can retain sensitive account or document data.

Mitigation: Delete profiles and uploaded files after sensitive work, and close sessions when tasks are complete.

Risk: The release depends on the third-party smooth-py package and external Smooth service credentials.

Mitigation: Install only if you trust Smooth, prefer a reviewed pinned version of smooth-py, and use an isolated environment.

## Reference(s):

- [Smooth Browser on ClawHub](https://clawhub.ai/antoniocirclemind/skills/smooth-browser)
- [Smooth App](https://app.smooth.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON outputs from Smooth CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can request structured output schemas, session identifiers, profile identifiers, live-view URLs, recording URLs, download URLs, and uploaded file IDs.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
