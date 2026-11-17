## Description:

Helps agents retrieve and summarize up to 90 days of historical Ozon shop-trend snapshots by shop name or ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to review a single shop's historical trend, assess growth, and share a concise, supported summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use may install external qhkit or Node tooling and change the user's environment.

Mitigation: Prefer an existing, version-pinned installation and review any proposed installation or configuration changes first.

Risk: The skill requires a qhkit token and may incur usage-based charges for shop-trend queries.

Mitigation: Configure the token through the intended account, check the current cost estimate, and obtain consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-shop-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend summary with supporting figures; tabular file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the platform, period, sample size, and credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
