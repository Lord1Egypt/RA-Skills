## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, analyses, and implementation support for Skill Vetter-style reliability, safety, setup-hardening, bug-fixing, and adjacent skill-development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, skill authors, maintainers, and teams use this skill to turn skill-vetting, hardening, reliability, onboarding, bug-fix, or adjacent-skill requests into concise plans, templates, checklists, analyses, code changes, and validation notes. It is especially suited to local-hardware friendly workflows that avoid unnecessary cloud-only or large-training dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be selected too broadly because it allows implicit invocation and lists common trigger words such as GitHub, security, and bug fix.

Mitigation: Prefer explicit invocation for skill-vetting or skill-hardening tasks, and confirm the request is about vetting, hardening, reliability, or adjacent skill workflow support before applying it.

Risk: The skill produces workflow guidance, checklists, scripts, templates, analyses, or code changes that could be incomplete or incorrect for a specific environment.

Mitigation: Review outputs against the user's stated success criteria, scan or test any generated code or shell commands before deployment, and keep assumptions and remaining risks visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-005353)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [HN: Newer macOS runs slower on Intel](https://news.ycombinator.com/item?id=48545230)
- [HN: Atlassian Data Contribution](https://news.ycombinator.com/item?id=48540151)
- [HN: Ask HN: Why are Spec-kit specs like that](https://news.ycombinator.com/item?id=48539057)
- [HN: Active GitHub accounts delivering malware](https://news.ycombinator.com/item?id=48548530)
- [GitHub issue: interactive onboarding tour for first-time users](https://github.com/Veritas-Vaults-Network/Soroban-Guard-web/issues/387)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, configuration snippets, checklists, and decision-support notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
