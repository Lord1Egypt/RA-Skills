## Description:

YouOS is a local-first personal email copilot that learns writing style from Gmail, Google Docs, and WhatsApp exports, then drafts replies in the user's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drbaher](https://clawhub.ai/user/drbaher)

### License/Terms of Use:

MIT-0

## Use Case:

External users run YouOS locally to draft, review, and improve personal email replies using their own communication history. The skill supports setup, ingestion, retrieval-grounded drafting, feedback collection, and local model improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private email and retrieved context may be sent to Claude when external fallback paths are configured or used.

Mitigation: For strict local-only operation, do not configure Claude credentials, set fallback behavior to local-only, and review the streaming draft and fact-extraction paths before using the web UI.

Risk: The local web server and optional background service process a sensitive personal email corpus.

Mitigation: Keep the service bound to localhost, use a PIN or API token where available, and enable background ingestion or nightly self-improvement only deliberately.

Risk: Manual installation executes local package code before the app ingests private account data.

Mitigation: Review the install script, package metadata, and app source before running installation or connecting Gmail, Docs, or WhatsApp data.

## Reference(s):

- [YouOS ClawHub skill page](https://clawhub.ai/drbaher/skills/youos)
- [YouOS privacy notes](PRIVACY.md)
- [gog CLI](https://github.com/openclaw/gog)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text email drafts, CLI output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be grounded in locally indexed email, document, and chat data; optional external model fallback can affect data egress.]

## Skill Version(s):

0.1.22 (source: server release evidence, created 2026-05-28T09:36:02Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
