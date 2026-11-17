## Description:

Converts Douyin short links and shared profile links into regular web URLs using Qinghu's service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People who receive Douyin share links can use this skill to obtain direct web links for videos or profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install Node/npm packages and change command paths for a simple link conversion.

Mitigation: Review installation steps first; prefer an already installed, pinned qhkit version.

Risk: Using the service may require Qinghu API credentials on the local machine.

Mitigation: Configure credentials only if needed, and keep them out of shared commands and files.

Risk: Submitted Douyin links are sent to Qinghu's external service.

Mitigation: Submit only links you are comfortable sharing with Qinghu.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-douyin-link-convert)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Short response with the resolved web link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversion depends on the Qinghu service; large results may be delivered as a local file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
