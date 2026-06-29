## Description: <br>
X.com (Twitter) 全量推文采集技能。支持三种采集方案：自动搜索模式、GraphQL API 模式、DOM 滚动模式。Complete X.com tweet scraping skill with three strategies: auto-search, GraphQL API, and DOM scrolling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media analysts use this skill to collect public tweet history from X.com accounts through Playwright-based auto-search, GraphQL, or DOM scrolling workflows for archiving and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported live X.com cookies can expose account access if stored or shared carelessly. <br>
Mitigation: Use a dedicated low-privilege account, keep cookie files out of version control and shared folders, and delete or rotate cookies after use. <br>
Risk: Authenticated X.com scraping may trigger platform enforcement, rate limits, or account restrictions. <br>
Mitigation: Install and run the skill only when account-backed X.com scraping is intentional, expect rate limits, and stop or reduce activity if X.com applies limits. <br>
Risk: Collected tweet JSON can contain sensitive or valuable datasets depending on the target and seed files. <br>
Mitigation: Review the scripts and target accounts before execution, and avoid pointing the skill at valuable accounts or sensitive datasets without an appropriate review. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/kooui/skills/x-tweet-scraper) <br>
- [Workflow reference](references/workflow.md) <br>
- [English README](README_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON files] <br>
**Output Format:** [Markdown instructions with Python and PowerShell command examples, plus JSON tweet output files from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, Playwright with Chromium, exported X.com cookies, and a target username.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
