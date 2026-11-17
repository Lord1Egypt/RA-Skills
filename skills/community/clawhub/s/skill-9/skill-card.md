## Description:

Give your AI agent eyes to see the entire internet by installing and configuring upstream tools for Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss直聘, WeChat, RSS, and web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ma-star](https://clawhub.ai/user/ma-star)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to install, check, and configure platform access tools, then call those upstream tools for web, social, video, repository, job, and feed retrieval or publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable remote tools for broad internet access.

Mitigation: Review the upstream package source before installation and run the skill in an isolated environment.

Risk: Some supported channels require sensitive account cookies or browser-derived session data.

Mitigation: Avoid pasting real account cookies into chat or shell history, prefer throwaway accounts, and use dedicated cookie handling workflows.

Risk: Several upstream tools can post, like, comment, publish, or otherwise change account state.

Mitigation: Require explicit user confirmation before any account-changing action.

Risk: Server IPs may be blocked by social or media platforms, and proxy use can affect privacy and account safety.

Mitigation: Use trusted proxy infrastructure only when necessary and keep platform credentials separated from general agent workspaces.

## Reference(s):

- [Agent Reach upstream package](https://github.com/Panniantong/agent-reach/archive/main.zip)
- [Cookie-Editor Chrome extension](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
- [ClawHub skill page](https://clawhub.ai/ma-star/skills/skill-9)
- [ClawHub publisher profile](https://clawhub.ai/user/ma-star)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install or invoke third-party upstream tools and may require user-provided cookies, proxies, or local browser access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
