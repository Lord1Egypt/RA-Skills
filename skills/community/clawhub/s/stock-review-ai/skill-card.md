## Description:

A-share market automated review and analysis system, generating daily market insights with Gemini AI, supporting publishing to Hugo blog and WeChat Official Account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donvink](https://clawhub.ai/user/donvink)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users use this skill to automate daily A-share data collection, generate Markdown market summaries, optionally add Gemini-based analysis, and publish reports to Hugo or WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Gemini and WeChat credentials.

Mitigation: Use scoped credentials in a trusted workspace and verify or fix secret redaction in logs before using real WeChat credentials.

Risk: The skill can publish generated reports to Hugo output paths or create WeChat drafts.

Mitigation: Review publishing platform settings before execution and inspect generated posts or drafts before making them public.

Risk: The skill writes market data and report files to local data and content directories.

Mitigation: Run it in a workspace where writing data and content/posts is expected, and set output paths deliberately.

Risk: Generated market analysis may contain incomplete or misleading trading guidance.

Mitigation: Treat reports as informational analysis, keep the investment-risk disclaimer, and require human review before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donvink/skills/stock-review-ai)
- [Project homepage from metadata](https://github.com/donvink/stock-review)
- [Live demo blog](https://donvink.github.io/stock-review/)
- [AkShare Documentation](https://akshare.akfamily.xyz/index.html)
- [Google AI Studio](https://aistudio.google.com/)
- [WeChat Official Account Platform](https://developers.weixin.qq.com/platform/)
- [Hugo Documentation](https://gohugo.io/)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CSV data files, shell commands, configuration snippets, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local data and blog-post files, optionally call Gemini for analysis, and optionally create WeChat drafts when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
