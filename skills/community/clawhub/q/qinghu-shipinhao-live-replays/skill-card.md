## Description:

Queries WeChat Channels account live replay history to support broadcast-frequency and replay-content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and creators use this skill to retrieve a WeChat Channels account's live replay list and assess broadcast frequency and available replay material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external qhkit package and configuring a Qinghu API token may expose credentials or introduce dependency risk.

Mitigation: Approve installation and token setup first; use a pinned qhkit version or disposable environment when supply-chain stability matters.

Risk: Live replay queries spend Qinghu credits, and failed server calls may still incur charges.

Mitigation: Check the current credit estimate and get user consent before paid calls; limit repeated calls and report actual credits spent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-live-replays)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary; tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits spent on paid calls and supports paginated replay results.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
