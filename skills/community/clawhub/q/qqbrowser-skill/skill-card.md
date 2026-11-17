## Description:

Browser automation CLI for AI agents that can open, navigate, interact with websites, extract structured data, analyze already-open tabs, record reusable browser tasks, and replay existing playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqbrowserteam](https://clawhub.ai/user/qqbrowserteam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows, inspect page state, extract web data, manage existing tabs, and create or replay reusable browser playbooks. It is suited to web tasks that require live browser behavior, including pages with login gates, dynamic SPAs, downloads, screenshots, or form interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playbook replay guidance allows variables to be used inside executable page JavaScript, which can be unsafe when values are untrusted or unsanitized.

Mitigation: Do not replay playbooks from untrusted sources; inspect side-effecting playbooks and avoid passing untrusted or unsanitized values into JavaScript variables.

Risk: Installation trusts mutable external browser and package downloads.

Mitigation: Install only from trusted sources, preferably using a pinned reviewed package version and verified browser installer source.

Risk: Browser automation can submit, publish, purchase, delete, message, or otherwise perform side-effecting web actions.

Mitigation: Review side-effecting playbooks before execution and require explicit user confirmation for actions that change external state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qqbrowserteam/skills/qqbrowser-skill)
- [PyPI Package](https://pypi.org/project/qqbrowser-skill/)
- [QQ Browser Homepage](https://browser.qq.com/)
- [Command Extended Reference](references/commands-extended.md)
- [Session Lifecycle](references/session-lifecycle.md)
- [Playbook Guide](references/playbook.md)
- [QQBrowserUse Evaluation Report](https://bak.res.qq.com/nav/qqbrowser_skills/QQBrowserSkillReport.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples, JSON playbook references, browser-state summaries, and file paths for generated artifacts such as downloads or screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to execute browser automation commands that read or mutate live browser state, create playbook JSON, capture screenshots, download files, or interact with web pages.]

## Skill Version(s):

1.0.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
