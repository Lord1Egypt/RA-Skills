## Description:

SkillMarket helps agents find, inspect, and install skills from the Zerone Skill Market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone-agent](https://clawhub.ai/user/zerone-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to browse marketplace skills, check framework compatibility, retrieve installation instructions, and install selected skills after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch changing third-party installation instructions that may alter an agent's installed skills.

Mitigation: Review the exact install instructions and require explicit user approval before executing any installation action.

Risk: Marketplace installation steps may reference untrusted packages, downloads, or commands.

Mitigation: Prefer signed or checksummed packages, verify integrity when evidence is provided, and run installation in a sandbox or restricted environment where possible.

Risk: Install commands may request privileged filesystem or network actions.

Mitigation: Avoid privileged execution unless the marketplace maintainer and selected skill publisher are trusted.

## Reference(s):

- [Zerone Skill Market API](https://api.zerone.market/api)
- [ClawHub SkillMarket page](https://clawhub.ai/zerone-agent/skills/skill-market)
- [Zerone publisher profile](https://clawhub.ai/user/zerone-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON returned by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches marketplace data and install tutorials from the configured Zerone API endpoint.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
