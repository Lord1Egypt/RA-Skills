## Description:

提取微信公众号文章内容，支持任意公众号文章链接的内容抓取和结构化输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nalin3166-collab](https://clawhub.ai/user/nalin3166-collab)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to extract public WeChat article metadata, body text, image information, and reading statistics from mp.weixin.qq.com article links. The package should be reviewed before deployment because the release evidence flags broader scraping and capture utilities beyond the advertised WeChat reader scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broader scraping, search, Notion/Zhihu tooling, and local capture utilities beyond the advertised WeChat reader scope.

Mitigation: Review the package before installation, remove unrelated scripts for production use, and deploy only the WeChat extraction path that is needed.

Risk: Arbitrary URL handling and local screenshot or HTML retention can expose private or internal content if used outside public article workflows.

Mitigation: Run the skill in an isolated environment, avoid private or internal URLs, and enforce a strict mp.weixin.qq.com allowlist.

Risk: Stealth browser automation can conflict with target-site terms or operational expectations.

Mitigation: Disable stealth automation unless explicitly approved for the deployment context and target site.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nalin3166-collab/skills/weixin-reader)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [JSON containing article metadata, extracted text or HTML, image entries, and statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success or error status; intended for public article extraction.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
