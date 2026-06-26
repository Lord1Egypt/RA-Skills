## Description: <br>
AI-powered QA for Strykr trading platform. Pre-built tests for crypto, stocks, news, AI chat. CI/CD ready. Works with Cursor, Claude, ChatGPT, Copilot. Vibe-coding enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and QA engineers use this skill to run Strykr-focused regression, smoke, API health, and AI response quality checks after deployments or during site monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated browser tests may run against environments the user is not authorized to test. <br>
Mitigation: Run the skill only against Strykr or another explicitly authorized test environment. <br>
Risk: Screenshots, console logs, timing data, and reports may capture sensitive application or user information. <br>
Mitigation: Review, redact, or secure generated artifacts before storing or sharing them. <br>
Risk: Unpinned QA dependencies can make CI results difficult to reproduce. <br>
Mitigation: Pin the web-qa-bot dependency and review dependency changes before CI rollout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NextFrontierBuilds/strykr-qa-bot) <br>
- [Publisher Profile](https://clawhub.ai/user/NextFrontierBuilds) <br>
- [Strykr Application](https://app.strykr.ai) <br>
- [web-qa-bot Dependency](https://github.com/NextFrontierBuilds/web-qa-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, shell commands, TypeScript APIs, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, console logs, timing metrics, and local test reports.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
