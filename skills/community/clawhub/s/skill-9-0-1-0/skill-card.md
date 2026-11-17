## Description:

Installs and configures upstream tools that let an agent access Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss Zhipin, WeChat public accounts, RSS, and general web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiyi-9](https://clawhub.ai/user/yiyi-9)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to set up and manage internet platform access tools, then call those upstream tools for search, reading, media metadata, RSS, and selected platform actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned third-party tooling and remote code.

Mitigation: Inspect the upstream package and installation commands before running setup, and install only in an environment where third-party tooling is acceptable.

Risk: The skill can handle authenticated platform sessions and sensitive cookies.

Mitigation: Use dedicated low-privilege accounts, avoid sharing primary-account cookies in chat, and review any browser cookie extraction flow before use.

Risk: Some configured upstream tools can perform account-changing actions such as posting, liking, commenting, or publishing content.

Mitigation: Require explicit user approval before any posting, liking, commenting, publishing, or other account-changing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiyi-9/skills/skill-9-0-1-0)
- [agent-reach installation package](https://github.com/Panniantong/agent-reach/archive/main.zip)
- [Cookie-Editor Chrome Web Store listing](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup commands, configuration steps, platform-specific tool invocations, and safety guidance for handling authenticated platform access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
