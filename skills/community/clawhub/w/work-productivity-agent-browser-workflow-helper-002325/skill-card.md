## Description:

Helps agent users, skill authors, maintainers, and teams create practical Agent Browser-style workflow support for bug fixes, setup hardening, reliability improvements, and adjacent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, developers, skill authors, maintainers, and teams use this skill to turn Agent Browser-style workflow needs into concrete plans, checklists, code changes, configuration guidance, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as browser, automation, and CLI may activate the skill for adjacent tasks where it is not the best fit.

Mitigation: Explicitly invoke the skill for Agent Browser workflow help and confirm the requested outcome before relying on its guidance.

Risk: Generated browser automation or shell-command suggestions could affect local files, accounts, or web sessions if run without review.

Mitigation: Review proposed automation steps, configuration changes, and commands before execution, especially when authenticated browser sessions or persistent files are involved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-002325)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Popular ClawHub skill demand: Obsidian](https://clawhub.ai/skills/obsidian)
- [Popular ClawHub skill demand: Nano Pdf](https://clawhub.ai/skills/nano-pdf)
- [Popular ClawHub skill demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Super AI Agentic Android App (BYOK)](https://news.ycombinator.com/item?id=48632415)
- [MCP and Playwright browser automation article](https://blog.csdn.net/weixin_28842269/article/details/162255631?ops_request_misc=elastic_search_misc&request_id=297c248b2d1e44178b0fa41633592bb8&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-7-162255631-null-null.142^v102^pc_search_result_base9&utm_term=agent-browser%20browser%20headless%20automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow helper; users should review generated automation steps before running them.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
