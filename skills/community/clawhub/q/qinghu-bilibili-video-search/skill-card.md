## Description:

Searches Bilibili videos by keyword and reports video details such as titles, duration, engagement metrics, and collaboration status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can find Bilibili videos matching a keyword and review video metadata, engagement, and potential collaboration content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or upgrade tooling and change the local PATH or account configuration.

Mitigation: Require explicit approval before installations, PATH changes, or account and site configuration; prefer preinstalled, pinned tooling.

Risk: Service tokens may be handled during account setup.

Mitigation: Require explicit approval before token configuration and keep tokens out of shared outputs.

Risk: Video searches are paid and larger results may increase charges.

Mitigation: Estimate credits first and obtain explicit consent before each authorized set of paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-bilibili-video-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise narrative with video details and optional table file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report credits consumed for paid searches.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
