## Description:

Extracts learner questions from Enterprise WeChat group messages, classifies them by course stage, and generates a structured table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackzhenguo](https://clawhub.ai/user/jackzhenguo)

### License/Terms of Use:

MIT-0

## Use Case:

Course operators and instructors use this skill to collect learner questions from Enterprise WeChat groups, organize them by beginner, advanced, or sprint course stage, and maintain a markdown Q&A record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save learner nicknames, question content, timestamps, and course-stage labels in a local markdown record.

Mitigation: Confirm group consent before use and treat the generated Q&A records file as sensitive data.

Risk: The bot reads relevant Enterprise WeChat group messages when collecting questions.

Mitigation: Limit deployment to groups where participants understand that mentioned questions may be read, categorized, and recorded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackzhenguo/skills/wechat-group-qa)
- [ClawHub publisher profile](https://clawhub.ai/user/jackzhenguo)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown table saved as a Q&A records file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records include learner nickname, question content, question time, and course stage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
