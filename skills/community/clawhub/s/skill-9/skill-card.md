## Description: <br>
Agent Reach helps an AI agent install, configure, and use upstream tools for Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss Zhipin, WeChat articles, RSS, and general web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ma-star](https://clawhub.ai/user/Ma-star) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up platform access tools, check available channels, configure credentials or proxies, and call the installed upstream tools directly for web and social content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a remote package and broad upstream tooling for internet and account automation. <br>
Mitigation: Install in an isolated environment after inspecting the remote package or pinning it to a reviewed commit. <br>
Risk: Cookie-based login can expose account sessions or trigger account enforcement on social platforms. <br>
Mitigation: Use disposable or dedicated accounts where possible, avoid primary-account browser cookies, and revoke sessions after use. <br>
Risk: Some upstream tools can publish, like, comment, favorite, or otherwise change account state. <br>
Mitigation: Require explicit user confirmation before any account-changing action. <br>


## Reference(s): <br>
- [Agent Reach ClawHub release page](https://clawhub.ai/Ma-star/skill-9) <br>
- [agent-reach package archive referenced by the skill](https://github.com/Panniantong/agent-reach/archive/main.zip) <br>
- [Cookie-Editor Chrome extension referenced by the skill](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for installing dependencies, configuring cookies or proxies, running diagnostics, and invoking upstream tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
