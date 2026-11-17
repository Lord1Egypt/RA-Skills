## Description:

Generates WeChat public account article drafts from a topic by helping an agent gather source material, summarize it, format the article, and prepare draft output for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onwalking](https://clawhub.ai/user/onwalking)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and agent users can use this skill to draft WeChat public account articles from a supplied topic and requested style. The workflow is most appropriate when a human will review generated content and any account draft before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests WeChat developer credentials and may read them from the current working directory's .env file.

Mitigation: Use dedicated least-privilege credentials, keep .env out of source control, and run the skill only in directories where that .env file is intentional.

Risk: The release advertises automatic draft creation, while the packaged CLI is mostly placeholder behavior and does not complete the advertised generation or upload flow.

Mitigation: Treat the skill as incomplete until reviewed, and require explicit human review before any future draft-upload path writes to the WeChat account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onwalking/skills/wechat-article-creator)
- [Publisher profile](https://clawhub.ai/user/onwalking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown article preview with CLI status text and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and WeChat developer credentials supplied as environment variables or an intentional .env file.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
