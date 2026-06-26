## Description: <br>
Skill Kit helps Claude Code users create, validate, merge, deduplicate, convert, route, upgrade, discover, graph, and review the publish scope of agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent-skill maintainers use Skill Kit to build, reorganize, validate, discover, and publish Claude Code skills. It is intended for normal skill maintenance workflows, including frontmatter linting, topic routing, dependency graph extraction, and hook registration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to persistent agent behavior, including skill directories, hooks, settings, and git workflow. <br>
Mitigation: Install it only when that level of control is intended, review generated hooks and settings changes, and back up settings.json before applying changes. <br>
Risk: Some workflows recommend broad installs, commits, backup cleanup, or destructive shell cleanup without enough safeguards. <br>
Mitigation: Avoid global non-interactive installs by default, run trigger compile in dry-run mode first, and verify exact paths before deleting backups or running rm -rf cleanup commands. <br>


## Reference(s): <br>
- [Skill Kit on ClawHub](https://clawhub.ai/drumrobot/skill-kit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, generated skill files, and review tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent skill, hook, settings, and git workflow changes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and changelog, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
