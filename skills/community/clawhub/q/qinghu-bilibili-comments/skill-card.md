## Description:

Collects comments from a Bilibili video link through the Qinghu data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content analysts and other users collect Bilibili video comments to review audience feedback. The agent summarizes findings and can deliver larger result sets as a table file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node/npm tooling or an unpinned qhkit package and change the host environment.

Mitigation: Review the installation steps and package source before allowing setup; use a controlled environment if needed.

Risk: A Qinghu API token may be persisted in local qhkit configuration.

Mitigation: Confirm the account and site before providing a token; protect local configuration and credentials.

Risk: Comment collection incurs variable Qinghu credit charges, especially for large results.

Mitigation: Check the current estimate and obtain user approval before paid calls or large collections.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-bilibili-comments)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary; tabular file for 10 or more comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual Qinghu credit usage for paid calls; large results may be saved locally.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
