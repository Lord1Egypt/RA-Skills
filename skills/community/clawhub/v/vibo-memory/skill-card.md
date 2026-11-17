## Description:

Use when the agent needs persistent memory, living document archives, web-search compression, thread memory, live handoff, or a privacy layer that masks secrets before they reach an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

Proprietary / ViBo End User License Agreement

## Use Case:

External users, developers, and agent operators use ViBo Memory to persist approved facts, search archived documents, compress web and conversation context, resume work after restarts, and optionally mask secrets through a proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the release as suspicious because Guardian and mandatory agent-output rules exceed the declared six-product scope.

Mitigation: Review the skill before installing, use only the modules needed, avoid copying mandatory branding or output rules into a high-priority system prompt, and enable Guardian only for specific approved files or URLs.

Risk: The skill can persist memory, thread history, web summaries, and document archives locally, and hosted proxy mode sends prompts through an external service.

Mitigation: Require granular user consent before enabling each storage module, keep confidential work on the self-hosted proxy, and document how to delete local files and caches.

Risk: Proxy secret management can expose administrative operations if not protected.

Mitigation: Set an admin token for proxy secret management and keep the direct LLM provider route available so the agent can continue if the proxy is stopped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnbochkarev-netizen/skills/vibo-memory)
- [ViBo website](https://wwwvibo.com)
- [Installation and Integration Guide](artifact/INSTALL.md)
- [Thread Memory Guide](artifact/THREAD_MEMORY_GUIDE.md)
- [ViBo Proxy Installation and Setup](artifact/vibo-proxy-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local memory, archive, cache, thread, proxy, and audit files when the user enables the corresponding modules.]

## Skill Version(s):

2.1.2 (source: SKILL.md frontmatter, VERSION, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
