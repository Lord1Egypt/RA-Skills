## Description:

Manage Linux applications by searching, installing, uninstalling, and updating software via Spark Store on Debian-based systems or APM across Linux distributions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmomenv](https://clawhub.ai/user/vmomenv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux users can use this skill to have an agent search app catalogs and prepare package install, removal, or update actions for Spark Store or APM. It is most relevant when users want package-management help across Debian-based and non-Debian Linux systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent toward root-level package install, uninstall, or update actions.

Mitigation: Require the agent to show the exact package name, source, and command before any package-management action is executed.

Risk: Broad update requests may trigger wider system-level package changes than the user intended.

Mitigation: Avoid broad update requests unless the user is prepared to review and approve system package changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmomenv/skills/spark-store-skill)
- [Publisher profile](https://clawhub.ai/user/vmomenv)
- [Spark Store category API](https://d.spark-app.store/store/categories.json)
- [Spark APM category API](https://d.spark-app.store/amd64-apm/categories.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with package search results, source choices, confirmation prompts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package names, package sources, and commands that require root privileges.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
