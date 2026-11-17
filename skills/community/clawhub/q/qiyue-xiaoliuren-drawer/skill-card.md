## Description:

Qiyue Xiaoliuren Drawer calls QiyueAstro's public Xiao Liu Ren API to cast one of six palaces by time and return the original verse and sequence path without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for entertainment and self-exploration when they want a quick Xiao Liu Ren cast for a current question or decision. It returns the cast palace, source verse, and month/day/hour sequence from QiyueAstro rather than independently interpreting the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Question text and date values used for a cast may be sent to qiyueastro.com.

Mitigation: Avoid sending secrets, sensitive personal details, or confidential business information in the question or date parameters.

Risk: Generated results include a QiyueAstro promotional link.

Mitigation: Review the required link behavior before deployment and disclose the external destination to users.

Risk: Users may mistake divination output for factual or professional advice.

Mitigation: Frame results as entertainment or self-exploration and avoid adding independent interpretations beyond the API response.

## Reference(s):

- [QiyueAstro](https://qiyueastro.com)
- [QiyueAstro Xiao Liu Ren Public API](https://qiyueastro.com/api/v1/openclaw/xiaoliuren)
- [ClawHub Skill Page](https://clawhub.ai/bloodymarygg/skills/qiyue-xiaoliuren-drawer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text containing returned API fields, the cast palace, original verse, sequence path, and a QiyueAstro link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make unauthenticated HTTPS GET requests to qiyueastro.com; user question text and optional date can be sent to the service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
