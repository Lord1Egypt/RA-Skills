## Description: <br>
Skill Reader helps users understand how to use an agent skill from a skill name, install URL, or SKILL.md by producing a structured usage guide with core functions, usage scenarios, dependencies, version details, and cautions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenwang-dev](https://clawhub.ai/user/kenwang-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, team members, and skill users use this skill to turn a skill name, ClawHub or GitHub install address, or local SKILL.md file into a practical usage manual. The output helps evaluate whether a skill is worth installing and explains how to use it in plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious and the security summary reports that related helper artifacts may launch nested review tooling with approval and sandbox bypass enabled. <br>
Mitigation: Review the skill and any helper behavior before use; prefer non-bypass execution settings and run moderation, PR commenting, publishing, or deployment commands only when those external changes are intended. <br>
Risk: Generated usage manuals may be incomplete or misleading when a source skill's documentation is ambiguous or differs from actual behavior. <br>
Mitigation: Treat the generated manual as a starting point and verify dependency, cost, command, and API-key claims against the target skill before relying on the guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kenwang-dev/skill-reader) <br>
- [Publisher profile](https://clawhub.ai/user/kenwang-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown usage guide with quick-summary and full-instructions sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include decision tables, dependency notes, estimated cost notes, and cautions derived from the inspected skill documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
