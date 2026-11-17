## Description:

Operate the saizeriya.js command-line interface on behalf of a user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakasyou](https://clawhub.ai/user/nakasyou)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent operate Saizeriya mobile-ordering sessions through the saizeriya.js CLI, including starting or resuming sessions, checking state, managing carts, and viewing account or receipt details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run third-party npm packages with the local agent's permissions.

Mitigation: Use reviewed, pinned, preinstalled versions of saizeriya.js and the QR scanner where possible, and run the agent in a restricted environment.

Risk: Some CLI actions can affect a real restaurant order or reveal account and receipt details.

Mitigation: Require explicit confirmation before submitting orders, changing carts, calling staff, or showing sensitive session information.

Risk: QR photo scanning introduces untrusted input into the ordering workflow.

Mitigation: Treat scanned QR values as untrusted and pass them only to the requested Saizeriya CLI start command after user intent is clear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nakasyou/skills/saizeriya)
- [qr-scanner-cli](https://github.com/victorperin/qr-scanner-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request explicit user confirmation before actions that submit orders, change carts, call staff, or expose account and receipt details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
