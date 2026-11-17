## Description:

Social Publisher formats Markdown content for WeChat, Xiaohongshu, Zhihu, and Douyin and provides preview and simulated publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and teams use this skill to convert one Markdown draft into platform-specific text for major Chinese social platforms and preview the formatted result before publishing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect real publishing because credentials and publish commands are documented, but the current artifact implements simulated publishing.

Mitigation: Treat publish output as preview or simulation unless the platform API implementation is separately reviewed and enabled.

Risk: The simulated publish path may still read configured platform credentials from environment variables or local config files.

Mitigation: Use the format preview mode for credential-free testing, and keep any platform credentials in protected environment or config storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/social-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces platform-specific formatted content for preview or simulated publish flows; real platform API publishing is not implemented in the current artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
