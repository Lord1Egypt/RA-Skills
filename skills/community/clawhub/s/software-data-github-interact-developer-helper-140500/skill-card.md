## Description:

Helps AI-agent users, skill authors, maintainers, and teams produce GitHub-style workflow support for bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to clarify GitHub-style development requests, plan practical implementation steps, produce artifacts such as workflows, checklists, code changes, or decision support, and validate the result against visible success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation wording and may lead an agent toward CLI commands, repository changes, issue or PR interactions, or API actions.

Mitigation: Treat suggestions as advisory and require user confirmation before running commands, changing repositories, or interacting with external services.

Risk: Documentation-only workflow guidance can still produce incorrect or misleading development advice.

Mitigation: Review generated plans, test commands, and scan resulting skills or code before deployment.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-140500)
- [Popular ClawHub Github Skill Demand](https://clawhub.ai/skills/github)
- [Hacker News AI Coding Discussion](https://news.ycombinator.com/item?id=48770319)
- [Hacker News Agent CLI Discussion](https://news.ycombinator.com/item?id=48770691)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output; users should review commands and repository changes before execution.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
