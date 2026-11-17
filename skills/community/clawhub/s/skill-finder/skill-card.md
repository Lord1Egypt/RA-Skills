## Description:

Find, compare, and install agent skills across ClawHub and Skills.sh when the user needs new capabilities, better workflows, stronger tools, or safer alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, compare, and optionally install agent skills when a task would benefit from a stronger specialized workflow or a safer alternative. It supports cross-registry discovery across ClawHub and Skills.sh, candidate evaluation, and source-aware installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can persistently change agent routing by adding steering that loads this skill for future capability-related requests.

Mitigation: Review the steering change before applying it, and decline or edit the routing line unless the future loading behavior is desired.

Risk: Search and install commands run unpinned external CLIs through npx.

Mitigation: Prefer pinned, reviewed versions of the ClawHub and Skills.sh CLIs, inspect candidate skills before installation, and keep installs explicitly opt-in.

Risk: Search queries are sent to external skill registries.

Mitigation: Avoid including secrets, proprietary details, or sensitive task context in registry search queries.

Risk: Recommended skills may come from third-party sources or may be flagged by scanners.

Mitigation: Inspect scanner warnings and candidate files before installing, prefer safer alternatives when available, and do not use force-install or auto-confirm flags.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/skill-finder)
- [Skill Homepage](https://clawic.com/skills/skill-finder)
- [Search Strategies](artifact/search.md)
- [Skill Evaluation Criteria](artifact/evaluate.md)
- [Setup](artifact/setup.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked skill recommendations, exact install commands, setup steps, and local preference updates.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
