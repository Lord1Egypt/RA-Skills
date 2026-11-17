## Description:

One-time installation and initialization of Chromium, browser dependencies, Chinese fonts, and a Chrome CDP launcher in a fresh OpenClaw environment without root access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyin717](https://clawhub.ai/user/wangyin717)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to initialize browser automation support in a fresh OpenClaw environment, including Chromium/CDP setup, Chinese font support, Playwright MCP registration, and optional browser-use tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill weakens browser and network safeguards through no-sandbox CDP launch options and SSRF allowlist guidance.

Mitigation: Use only in an isolated test container and require explicit authorization before direct CDP is used to work around network policy.

Risk: The setup scripts install mutable third-party tooling and assets from external URLs.

Mitigation: Review, pin, and verify third-party installers and downloads before deployment.

Risk: The optional browser-use workflow can reuse local Chrome profiles or real credentials.

Mitigation: Do not reuse personal browser profiles or production credentials; use disposable test accounts and isolated browser state.

Risk: Security evidence marks the release suspicious and recommends review before use.

Mitigation: Perform security review and scanner review before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyin717/skills/testagent-browser-setup)
- [browser-use repository](https://github.com/browser-use/browser-use)
- [WenQuanYi Micro Hei font source](https://github.com/anthonyfok/fonts-wqy-microhei/raw/master/wqy-microhei.ttc)
- [browser-use CLI installer](https://browser-use.com/cli/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript CDP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and testing guidance for an agent; setup scripts may install browser tooling and create local configuration files.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter reports 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
