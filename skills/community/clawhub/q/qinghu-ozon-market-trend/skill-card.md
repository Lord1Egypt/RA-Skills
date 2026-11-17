## Description:

Retrieves historical daily or monthly market trend snapshots for the Ozon marketplace through Qinghu data tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to review daily or monthly marketplace-wide trends and summarize changes over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading qhkit and Node/npm can change the local runtime or introduce untrusted software.

Mitigation: Use an isolated environment with qhkit preinstalled when possible; review the package and confirm before installing or upgrading.

Risk: Configuring credentials or switching sites can overwrite working tokens or connect to the wrong account.

Mitigation: Confirm the intended site and obtain approval before changing token or site settings; keep credentials private.

Risk: Trend queries and repeated API calls can consume paid credits.

Mitigation: Estimate charges and obtain user consent before paid calls, particularly large or repeated queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-ozon-market-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with optional table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the queried period and reports credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
