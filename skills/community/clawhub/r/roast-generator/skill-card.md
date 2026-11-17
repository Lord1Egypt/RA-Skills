## Description:

Generates playful roast text in gentle, savage, friend, celebrity, self, and battle styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for humorous roast text or Markdown-ready joke output in several modes. Reviewers should account for the shipped local utility behavior described in the security evidence before deploying it in environments that handle sensitive text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package may create local roast-generator data files and retain command arguments or added text.

Mitigation: Avoid passing secrets, private names, confidential workplace text, or sensitive search terms, and review local storage behavior before installation.

Risk: The advertised roast generator is accompanied by an additional utility that stores and logs user-provided text locally.

Mitigation: Review the shipped scripts and deploy only in environments where local data retention is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/roast-generator)
- [BytesAgain Homepage](https://bytesagain.com)
- [Source link declared in skill metadata](https://github.com/bytesagain/ai-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and stdout text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Roast output is single-stream text; the additional utility may create local data and history logs.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
