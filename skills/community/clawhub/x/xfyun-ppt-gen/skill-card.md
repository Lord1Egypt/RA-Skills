## Description:

Generate professional, structured PowerPoint presentations from optimized topic keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy-1026](https://clawhub.ai/user/dzy-1026)

### License/Terms of Use:


## Use Case:

Employees, developers, and external users can use this skill to generate business, technical, training, strategy, and academic presentation decks from concise optimized topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics, outlines, and document-based inputs may leave the local environment for Xfyun processing.

Mitigation: Do not use sensitive, confidential, regulated, or internal content unless Xfyun processing and credential handling are approved for that use case.

Risk: The skill requires API credentials for an external PPT generation service.

Mitigation: Store XF_PPT_APP_ID and XF_PPT_API_SECRET in a controlled environment and rotate them if they are exposed.

Risk: Generated presentation content may be incomplete, inaccurate, or unsuitable for the intended audience.

Mitigation: Review generated outlines and slides before sharing or using them in business, training, technical, or academic settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dzy-1026/skills/xfyun-ppt-gen)
- [Publisher profile](https://clawhub.ai/user/dzy-1026)
- [iFLYTEK Spark PPT v2 documentation](https://www.xfyun.cn/doc/spark/PPTv2.html)
- [iFLYTEK PPT API base endpoint](https://zwapi.xfyun.cn/api/ppt/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime responses may include JSON strings, task status text, and generated PPT download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python plus XF_PPT_APP_ID and XF_PPT_API_SECRET credentials; normal use submits optimized topics to iFLYTEK/Xfyun services.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
