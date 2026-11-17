## Description:

Manage YouTube Super Chat events by listing Super Chat events for a channel through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare yutu authentication and list YouTube Super Chat events for a channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The yutu CLI installation may introduce supply-chain risk if installed without a pinned or verified version.

Mitigation: Install yutu only from trusted sources and prefer a pinned or verified version where possible.

Risk: OAuth client secrets and cached YouTube tokens can expose account access if mishandled.

Mitigation: Keep client_secret.json and youtube.token.json private and avoid sharing them in prompts, logs, or repositories.

Risk: YouTube OAuth access may grant more permission than needed for listing Super Chat events.

Mitigation: Grant only the YouTube permissions needed for the intended listing workflow.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Super Chat Event List](references/superChatEvent-list.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [ClawHub skill page](https://clawhub.ai/openwaygate/skills/youtube-super-chat-event)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose yutu commands that return table, JSON, or YAML output depending on selected CLI flags.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
