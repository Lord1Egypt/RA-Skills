## Description:

Telegram Web platform skill for SurfAgent, covering chat state, composer flows, send verification, and when to use the Telegram Web adapter over raw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Telegram Web through SurfAgent with reliable chat state checks, composer handling, visible message extraction, and proof-aware send verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect visible Telegram chats and assist with sending messages through a logged-in account.

Mitigation: Use it only with the intended account, confirm the target chat and message content before sending, and avoid exposing private conversations unnecessarily.

Risk: A send action can be misreported if the agent treats a click, keypress, or draft text as proof of delivery.

Mitigation: Require post-send verification that the composer changed and the last visible message, or stronger site-native confirmation, reflects the intended content.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub skill page](https://clawhub.ai/surfagentapp/skills/surfagent-telegram-web)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with operational checklists and verification rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; guides agent behavior for Telegram Web workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
