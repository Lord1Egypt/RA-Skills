## Description:

Fetches WeChat public-account articles from mp.weixin.qq.com links and saves article metadata, content, and image references as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to capture WeChat public-account articles from provided mp.weixin.qq.com URLs and convert them into local Markdown files for review, archiving, or downstream editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Chromium against a user-provided URL with host network access.

Mitigation: Use only trusted https://mp.weixin.qq.com links and run the skill in an isolated environment when possible.

Risk: Fetched article content and generated Markdown files are saved locally.

Mitigation: Specify an intended output directory and review saved content before sharing or publishing it.

Risk: Dependencies are installed from unpinned package names in the artifact documentation.

Mitigation: Pin Playwright and BeautifulSoup dependency versions before installation in managed environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hunkguo/skills/wechat-articles-skill)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with YAML frontmatter and local image references, plus terminal status text from the fetch script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an images/ subdirectory when image handling is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
