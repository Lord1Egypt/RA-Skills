## Description:

Helps AI-agent users and skill maintainers create practical weather-workflow plans, checklists, analysis, code changes, and validation notes for bugs, setup hardening, reliability, or adjacent skill work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn weather-style workflow needs into practical plans, templates, checklists, implementation support, and validation notes. It is aimed at improving bug fixes, setup hardening, safety, and reliability for workflows that should remain feasible on local hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation language may select this skill for generic weather, API, or bug-fix prompts where a more specific skill would be better.

Mitigation: Review or narrow the trigger terms when precise routing matters, and confirm the user's concrete weather-workflow goal before producing artifacts.

Risk: The skill produces guidance, plans, code, commands, and configuration suggestions that may be incorrect for a user's environment.

Mitigation: Validate outputs against the stated success criteria and have users review commands, code, and configuration before applying them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-weather-current-workflow-helper-005353)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Popular ClawHub skill demand: Proactive Agent](https://clawhub.ai/skills/proactive-agent)
- [Popular ClawHub skill demand: Weather](https://clawhub.ai/skills/weather)
- [Ask HN: What does your local LLM setup looks like?](https://news.ycombinator.com/item?id=48536531)
- [Are we asking the right questions?](https://news.ycombinator.com/item?id=48539681)
- [GitHub issue: interactive onboarding tour for first-time users](https://github.com/Veritas-Vaults-Network/Soroban-Guard-web/issues/387)
- [GitHub issue: respect OS color-scheme preference for initial theme](https://github.com/Veritas-Vaults-Network/Soroban-Guard-web/issues/386)
- [GitHub issue: stale route version recovery](https://github.com/jackson-simionato/sombreado-floripa/issues/7)
- [GitHub issue: API key input focus outline](https://github.com/unicef/adt-studio/issues/510)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, code snippets, shell commands, configuration snippets, or locally executable workflow artifacts depending on the user request.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, limits, success criteria, and a short verification note when useful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
