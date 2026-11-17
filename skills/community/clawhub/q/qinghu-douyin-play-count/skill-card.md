## Description:

Looks up the play count of a Douyin video from its link using Qinghu's data tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting Douyin users retrieve a video's play count from its link and report the result after obtaining approval for a paid lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit and storing a Qinghu access token adds local software and credential exposure.

Mitigation: Use a reviewed, pinned qhkit installation where possible and protect the locally stored token.

Risk: The play-count lookup is paid and may consume Qinghu credits.

Mitigation: Check the estimate and obtain user approval before each authorized set of paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-douyin-play-count)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the Douyin video play count and the Qinghu credits consumed by paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
