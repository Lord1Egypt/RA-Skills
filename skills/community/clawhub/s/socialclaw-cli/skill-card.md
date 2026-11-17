## Description:

SocialClaw CLI helps agents plan and propose risk-gated Social Flow CLI commands for Meta operations across auth, insights, ads, Instagram, WhatsApp, ops, Gateway, and Studio workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Developers, operators, and marketing teams use this skill to translate natural-language Meta operations requests into exact Social Flow command sequences. It supports read-first diagnostics, scoped execution planning, and confirmation gates for actions that may affect live spend, publishing, messaging, or production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external Social Flow npm package and CLI.

Mitigation: Install only from the trusted package source, pin a reviewed version when possible, and avoid elevated privileges during installation.

Risk: Generated commands can affect Meta credentials, live spend, publishing, customer messaging, or production automations.

Mitigation: Use narrowly scoped Meta credentials or test workspaces, start with read-only diagnostics, and require explicit confirmation before write or high-risk commands.

Risk: Diagnostics or command examples could expose sensitive tokens or credentials.

Mitigation: Mask secrets in outputs and prefer secure credential prompts over inline plaintext tokens.

## Reference(s):

- [SocialClaw CLI ClawHub page](https://clawhub.ai/vishalgojha/skills/socialclaw-cli)
- [Social Flow GitHub homepage](https://github.com/vishalgojha/social-flow)
- [Social Flow npm package](https://www.npmjs.com/package/@vishalgojha/social-flow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, command ordering, risk classifications, and explicit confirmation prompts before write or high-risk execution.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
