## Description:

$SKILL is a Solana memecoin experiment that asks an agent to summarize the project for its human operator and leave all participation decisions to the human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notking0](https://clawhub.ai/user/notking0)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to summarize a Solana memecoin experiment for a human operator. It also provides optional participation, wallet, token swap, and discovery-reporting details that require explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to promote or facilitate real cryptocurrency purchases.

Mitigation: Require manual human review for any cryptocurrency decision and prevent the skill from initiating purchases, swaps, or funding requests.

Risk: Wallet creation and token swaps may expose users to custody mistakes or total loss of funds.

Mitigation: Use independent verification and the human operator's own wallet custody practices; never share secret keys or send funds automatically.

Risk: Discovery reporting sends telemetry to an external API and may involve public tracking with unspecified retention.

Mitigation: Decline telemetry unless the user explicitly accepts public tracking and the available retention information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/notking0/skills/readtheskill)
- [Read The Skill Website](https://readtheskill.com)
- [Skill File](https://readtheskill.com/skill.md)
- [Read The Skill on X](https://x.com/readtheskill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, API calls, guidance]

**Output Format:** [Markdown prose with inline code blocks and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cryptocurrency participation guidance and optional public discovery-reporting instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
