## Description:

Retrieves Bilibili creator profile metrics, including account name, biography, followers, likes, and views, from a creator's profile URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to check a Bilibili creator's public profile and engagement metrics from a profile URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Bilibili session cookies can expose account access.

Mitigation: Avoid supplying cookies unless necessary; treat any provided cookie as an account secret.

Risk: The skill may install or update an external qhkit CLI using unpinned versions.

Mitigation: Prefer an approved, pinned or preinstalled qhkit version over ad hoc latest or npx installation.

Risk: Queries use paid Qinghu credits, and actual charges can vary with returned data.

Mitigation: Check the current estimate and obtain user consent before paid calls; disclose actual credits used.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-bilibili-creator-profile)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written summary of creator metrics; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report Qinghu credits consumed for paid queries.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
