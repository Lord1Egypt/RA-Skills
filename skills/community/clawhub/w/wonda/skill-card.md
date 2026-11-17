## Description:

Wonda CLI helps terminal-based agents generate and edit images, videos, music, and audio, plus research and automate activity across LinkedIn, Reddit, and X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[degausai](https://clawhub.ai/user/degausai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route Wonda CLI commands for media generation, editing, social research, social publishing, and local finishing workflows. It is intended for agents that need concise command guidance for producing media assets or interacting with connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through broad external social actions, including publishing, messaging, following, deleting, and account workflows.

Mitigation: Require explicit human confirmation before posting, messaging, following, deleting, accepting terms, granting permissions, or making other externally visible account changes.

Risk: The security summary flags stealthy social-account automation and the guidance calls out disposable signup, internal API, and detection-avoidance workflows.

Mitigation: Avoid stealth, disposable signup, internal API, and detection-avoidance workflows; prefer official account APIs and hand off rate-limit or verification challenges to a human.

Risk: Use requires Wonda credentials and may operate on connected social accounts.

Mitigation: Run in an isolated environment, protect WONDERCAT_API_KEY as a secret, pin dependencies where practical, and grant only the account access needed for the task.

## Reference(s):

- [Wonda homepage](https://wonda.sh)
- [ClawHub skill page](https://clawhub.ai/degausai/skills/wonda)
- [Publisher profile](https://clawhub.ai/user/degausai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create media files, social posts, messages, account actions, and local analysis artifacts when executed.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
