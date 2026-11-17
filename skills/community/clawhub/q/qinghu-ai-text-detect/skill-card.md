## Description:

Assesses whether submitted text is AI-generated using Qinghu's text detection service, reporting confidence, category proportions, and segment-level results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People assessing written content use this skill to request an AI-versus-human text assessment, including overall confidence, category proportions, and segment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install software or change the local environment during setup.

Mitigation: Preinstall a reviewed, pinned qhkit version; require explicit approval before global installs or PATH changes.

Risk: Using the paid external detection service involves API credentials and submitted text.

Mitigation: Obtain consent before paid calls, review text before submitting it, and provide the token through a secure secret manager rather than storing it locally.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-ai-text-detect)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown assessment with confidence, category proportions, and segment details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits charged for paid calls; labels manual assessments separately from service results.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
