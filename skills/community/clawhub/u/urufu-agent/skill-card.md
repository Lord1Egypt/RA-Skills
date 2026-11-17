## Description:

Urufu Agent helps AI agents monitor a urufu wallet on Base, check portfolio and yield, and perform approved claim and mint actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urufu-labs](https://clawhub.ai/user/urufu-labs)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an AI agent monitor their Urufu game wallet on Base, review portfolio, yield, and mint eligibility, and run approved steward CLI actions for claims, mints, and game play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet signing authority for claim and mint flows.

Mitigation: Use only a dedicated low-fund wallet or enforceably limited session key, keep private keys out of shell startup files, and inspect each transaction or signature before approval.

Risk: The server security guidance flags paid mint use before a cooldown bug is fixed.

Mitigation: Avoid mint-paid flows until that issue is fixed and reviewed.

Risk: The server security guidance flags a vulnerable dependency lock for long-running network use.

Mitigation: Update the dependency lock before relying on the skill for long-running network activity.

## Reference(s):

- [ClawHub Urufu Agent listing](https://clawhub.ai/urufu-labs/skills/urufu-agent)
- [Urufu Agent homepage](https://github.com/urufu-labs/urufu-agent)
- [Urufu agent play guide](https://www.urufu.xyz/play/agent)
- [Agent play documentation](docs/agent-play.md)
- [OpenAPI documentation](docs/api/README.md)
- [OpenAPI specification](docs/api/openapi.yaml)
- [Agent policy](references/agent-policy.json)
- [Bootstrap reference](references/BOOTSTRAP.md)
- [Onboarding reference](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run CLI commands that read wallet state and, after user approval, initiate Base claim or mint flows.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
