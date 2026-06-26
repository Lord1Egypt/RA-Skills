## Description: <br>
Xhsfenxi Pro analyzes Xiaohongshu creators by collecting authenticated public-page data, classifying creator archetypes, generating topic formulas, and producing Markdown or Word reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Xiaohongshu bloggers, compare creator patterns, generate viral topic formulas, and prepare structured creator reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses saved Xiaohongshu session cookies and intercepts authenticated browser traffic. <br>
Mitigation: Treat cookie files as secrets, keep them local, refresh them intentionally, and install only when authenticated Xiaohongshu scraping is expected. <br>
Risk: The skill can persist creator profiles, reports, and local blogger data. <br>
Mitigation: Periodically delete local blogger databases and generated reports that are no longer needed. <br>
Risk: The release includes account-writing and optional outbound automation features such as comments, webhooks, cron checks, and update checks. <br>
Mitigation: Review or disable post_comment and onboarding automations unless the user has explicitly opted in and understands what they send or run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosmofang/xhsfenxi-pro) <br>
- [Newrank Xiaohongshu profile reference](https://www.newrank.cn/profile/xiaohongshu/{user_id}) <br>
- [Xiaohongshu note URL format](https://www.xiaohongshu.com/explore/xxx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Word documents, JSON-like analysis objects, Python examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Markdown, DOCX, JSON, and creator profile data during analysis workflows.] <br>

## Skill Version(s): <br>
2.1.4 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
