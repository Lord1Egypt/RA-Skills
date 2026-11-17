## Description:

Provides Chinese-language web search through Bing China with browser-based page retrieval and login handling when a visited site requires it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwq2023qwq](https://clawhub.ai/user/qwq2023qwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an agent needs Chinese-language search results from Bing China and may need to fetch page content through OpenClaw's browser tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented browser configuration can disable browser sandboxing while visiting web pages.

Mitigation: Avoid the noSandbox setting unless an administrator has accepted that risk in a contained environment.

Risk: The skill may open a host browser for third-party login flows.

Mitigation: Enter credentials only when you intentionally initiated the login and trust the destination site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwq2023qwq/skills/web-search-bing-cn)
- [OpenClaw browser tool documentation](https://docs.openclaw.ai/zh-CN/tools/browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with search-result text and browser-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open the host browser only when a site requires login.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
