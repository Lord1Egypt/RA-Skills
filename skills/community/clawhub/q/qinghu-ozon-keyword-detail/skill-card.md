## Description:

Helps agents retrieve Ozon keyword search, conversion, exposure, supply-demand, and order metrics for up to 10 keyword IDs through Qinghu's qhkit tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to compare keyword demand, competition, and order activity from Qinghu data before making marketplace decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use may install or update Node and qhkit on the user's machine.

Mitigation: Preinstall a reviewed, pinned qhkit version and approve any runtime changes before using the skill.

Risk: Configuring Qinghu credentials on the wrong account region can cause authentication failures or unexpected account access.

Mitigation: Confirm the intended Qinghu account region before storing the token or invoking paid tools.

Risk: Keyword lookups consume paid Qinghu credits, and final charges can exceed the base estimate.

Mitigation: Review estimated credits and obtain consent before paid calls; check actual credits charged afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-keyword-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise narrative with keyword metrics and optional tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the queried platform and period, and discloses credits spent on paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
