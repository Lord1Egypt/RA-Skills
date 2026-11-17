## Description:

Cross-border compliance and trade reference assistant for certification checklists (CE/FCC/GPSR), tariff estimates, labeling requirements, and platform rule checks, returning structured JSON suggestions that require human verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce teams, cross-border sellers, and developers use this skill to gather product and market context and request reference guidance for certifications, tariffs, labeling, and marketplace restrictions before expert review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured API endpoint can receive the user's API token and business data, including if TOKENAPI_BASE_URL points to a non-HTTPS or untrusted URL.

Mitigation: Use only trusted HTTPS endpoints, control TOKENAPI_BASE_URL centrally, and keep TOKENAPI_KEY scoped, revocable, and out of shared environments.

Risk: Compliance, customs, tax, certification, and marketplace outputs may be incomplete, outdated, or unsuitable for a specific product or jurisdiction.

Mitigation: Treat outputs as references and verify them with official sources or qualified legal, tax, customs, or certification professionals before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-compliance-guard)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with structured JSON guidance from the cloud skill endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are compliance references only and require human verification against official sources and current regulations.]

## Skill Version(s):

1.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
