## Description: <br>
Generates Xiaohongshu-style posts by combining topic discovery, reference-post style analysis, opinionated draft generation, and Chinese prose refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to draft Xiaohongshu posts from a chosen topic, a 36kr RSS trend, or a supplied reference post, while preserving a high-engagement social writing style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch public RSS topics from 36kr when trend discovery is used. <br>
Mitigation: Install and run it only in environments where outbound access to the disclosed public RSS source is acceptable. <br>
Risk: The skill depends on the separate humanizer-zh skill for prose refinement. <br>
Mitigation: Review the installed humanizer-zh dependency before using this skill in production workflows. <br>
Risk: Generated posts are designed to include strong viewpoints and controversy, which can produce misleading or overconfident claims. <br>
Mitigation: Fact-check and edit drafts before publishing, especially when the content makes strong, controversial, or current-event claims. <br>


## Reference(s): <br>
- [XHS Content Generate on ClawHub](https://clawhub.ai/lifei68801/xhs-content-generate) <br>
- [36kr RSS Feed](https://36kr.com/feed) <br>
- [Style Analysis Method](references/style-analysis.md) <br>
- [Xiaohongshu Writing Templates](references/writing-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text social post drafts with optional shell command output for trend selection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May incorporate public 36kr RSS topics and may call the humanizer-zh skill for Chinese writing style refinement.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
