## Description:

Generates, formats, validates, and optionally pushes WeChat Official Account article drafts with configurable themes and cover generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onegrown](https://clawhub.ai/user/onegrown)

### License/Terms of Use:

MIT

## Use Case:

External users and content teams use this skill to turn a topic or reference material into a WeChat Official Account article draft, apply an appropriate visual theme, generate supporting cover assets, and prepare or push the result for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push or modify WeChat Official Account drafts when credentials are configured.

Mitigation: Use guided or local generation by default and review every article, cover, author, digest, and draft in WeChat before publication.

Risk: Generated output may include fixed creator branding or digest text that was not explicitly approved for a given run.

Mitigation: Check and edit branding, author, footer, and digest fields before accepting or publishing generated drafts.

Risk: Automatic mode and mock or incomplete verification can leave factual claims or publishing actions under-reviewed.

Mitigation: Avoid relying on automatic mode for production workflows and manually verify factual claims and sources before publication.

Risk: WeChat and Tavily credentials may grant external API access beyond local file generation.

Mitigation: Run the skill in a dedicated low-privilege environment with separate credentials and rotate secrets if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onegrown/skills/tsmf-wechat-oa)
- [Publisher profile](https://clawhub.ai/user/onegrown)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [WeChat token API](https://api.weixin.qq.com/cgi-bin/token)
- [WeChat image upload API](https://api.weixin.qq.com/cgi-bin/media/uploadimg)
- [WeChat draft add API](https://api.weixin.qq.com/cgi-bin/draft/add)
- [SKILL_OVERVIEW](references/SKILL_OVERVIEW.md)
- [WORKFLOW_DESIGN](references/WORKFLOW_DESIGN.md)
- [THEMES_GUIDE](references/THEMES_GUIDE.md)
- [CONTENT_PIPELINE_ANALYSIS](references/CONTENT_PIPELINE_ANALYSIS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article, cover, and draft metadata files and may call WeChat APIs when credentials and push mode are configured.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
