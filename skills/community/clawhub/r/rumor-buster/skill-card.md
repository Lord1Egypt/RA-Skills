## Description:

Dual-engine fact-checking skill for verifying news, claims, and messages through Chinese + English cross-verification and source tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry720320](https://clawhub.ai/user/harry720320)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess whether claims, news, or messages are credible by comparing Chinese and English search results, tracing sources, and producing a short or detailed verification report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security scan reports unsafe Tavily credential handling, including embedded or plaintext-stored API credentials.

Mitigation: Review before installing, do not use the bundled Tavily fallback key, and only provide a Tavily API key if plaintext storage in ~/.rumor-buster-config is acceptable.

Risk: Verification text may be sent to third-party search services during claim checking.

Mitigation: Do not submit private messages, internal business content, personal data, or other sensitive text unless third-party search disclosure and handling are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harry720320/skills/rumor-buster)
- [Architecture & Sub-Skill Integration](references/architecture.md)
- [Verification Workflow Guide](references/verification-guide.md)
- [Output Templates](references/output-templates.md)
- [Sogou Search](https://sogou.com)
- [Sogou WeChat Search](https://wx.sogou.com)
- [Toutiao Search](https://so.toutiao.com)
- [DuckDuckGo](https://duckduckgo.com)
- [Startpage](https://startpage.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown verification summaries and detailed reports, with optional configuration prompts and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credibility scores, cross-language comparison tables, source timelines, spread paths, and search engine configuration details.]

## Skill Version(s):

0.5.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
