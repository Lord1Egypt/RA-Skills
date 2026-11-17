## Description:

Analyzes Amazon category price ranges, sales share, sales efficiency, and ratings to identify promising entry price bands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market analysts use this skill to compare prices, sales share, sales efficiency, and ratings within a category and assess potential entry price bands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrades of qhkit and Node tooling can change the local environment.

Mitigation: Review installation steps and preinstall a vetted qhkit version instead of allowing automatic setup.

Risk: Persisting a Qinghu API token may expose credentials if the environment is not controlled.

Mitigation: Provide the token through a controlled, revocable method and review how credentials are stored before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-amazon-price-band)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes category price bands, sales share, sales efficiency, ratings, and potential entry prices.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
