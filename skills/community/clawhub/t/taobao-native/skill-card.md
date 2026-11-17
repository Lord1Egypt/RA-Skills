## Description:

Shopping assistant via Taobao Desktop client for searching products, viewing details, adding items to cart, placing orders, checking orders, requesting shipping, and performing Taobao or Tmall shopping operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flappymonkey](https://clawhub.ai/user/flappymonkey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to operate a local Taobao Desktop client for Taobao and Tmall shopping workflows, including product search, SKU inspection, cart and order management, seller chat, and product reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent control over a logged-in Taobao desktop session and account-affecting shopping actions.

Mitigation: Require explicit user confirmation before deleting cart items, submitting reviews, sending seller messages, placing orders, or taking any purchase-related step.

Risk: The skill includes an installation path for a desktop client whose installer source and publisher must be trusted outside the skill.

Mitigation: Verify the installer source and publisher before installation, and install only after the user has approved that setup.

Risk: Incorrect SKU or price handling can lead to misleading shopping recommendations or unintended cart contents.

Mitigation: Follow the documented SKU workflow: retrieve available SKUs, use exact element indexes for SKU selection, wait for price refresh, and confirm purchase-related actions with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flappymonkey/skills/taobao-native)
- [Install download reference](artifact/references/install-download.md)
- [Taobao Desktop installer CDN](https://tblifecdn.taobao.com/taobaopc/ai/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to write CLI results to workspace JSON files when command output is large.]

## Skill Version(s):

1.0.41 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
