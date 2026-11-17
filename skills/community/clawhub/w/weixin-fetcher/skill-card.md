## Description:

Fetches WeChat Official Account article content from mp.weixin.qq.com links and extracts the article body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaozs-com](https://clawhub.ai/user/xiaozs-com)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve the visible title and body of WeChat Official Account articles from trusted mp.weixin.qq.com links and save the result for downstream reading or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can browse and save content from any supplied URL, not only WeChat links.

Mitigation: Use only trusted mp.weixin.qq.com article URLs and reject or review non-WeChat URLs before running.

Risk: Browser automation saves article text and a full-page screenshot in the chosen output directory or current working directory.

Mitigation: Run the skill in an isolated browser and network environment, and choose an output directory appropriate for captured article content.

Risk: First use can install browser automation dependencies and download a matching ChromeDriver.

Mitigation: Review and install dependencies in a controlled environment before deployment.

## Reference(s):

- [WeChat Article Fetcher on ClawHub](https://clawhub.ai/xiaozs-com/skills/weixin-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown file, PNG screenshot, and stdout text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome and DrissionPage; writes article_content_weixin.md and article_screenshot_weixin.png to the selected output directory or current working directory.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
