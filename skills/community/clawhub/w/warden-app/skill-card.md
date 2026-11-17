## Description:

Guides an agent through safe browser automation for Warden App wallet tasks including portfolio review, swaps, deposits and withdrawals, perps, and repeatable workflow documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deiu](https://clawhub.ai/user/deiu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to navigate a logged-in Warden App wallet session, inspect balances or positions, and carry out explicitly approved crypto actions with confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through a logged-in crypto wallet UI where mistakes may move assets or change positions.

Mitigation: Keep final signing or confirmation under user control and verify token, amount, chain, slippage, fees, leverage, and destination before every transaction.

Risk: Wallet secrets or private information could be exposed if requested, stored, or repeated in conversation.

Mitigation: Never request seed phrases or private keys, and avoid revealing local files, credentials, IPs, internal logs, or other private information.

## Reference(s):

- [Warden App](https://app.wardenprotocol.org/)
- [Warden App UI Notes](references/warden-ui-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/deiu/skills/warden-app)
- [Publisher Profile](https://clawhub.ai/user/deiu)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists and browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction summaries, approval prompts, post-action verification notes, and repeatable workflow documentation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
