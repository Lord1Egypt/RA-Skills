## Description: <br>
Agent Skills builder, auditor, and improver for cross-platform LLM agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent-skill maintainers use this skill to scaffold new Agent Skills, audit existing SKILL.md packages, propose improvements, and run static or runtime checks for cross-platform compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Healthcheck mode can inspect local agent configs, environment-variable names, session logs, and discovered URLs in the active session. <br>
Mitigation: Use create, scan, and improve on explicit paths; run healthcheck-all only when broader local inspection is acceptable. <br>
Risk: The skill may propose edits to skill files that affect future agent behavior. <br>
Mitigation: Review diffs and rerun the scan before accepting or deploying generated changes. <br>


## Reference(s): <br>
- [Agent Skills open standard](https://agentskills.io) <br>
- [Advanced patterns](references/advanced-patterns.md) <br>
- [Anti-patterns in Agent Skills](references/anti-patterns.md) <br>
- [Health Check Reference](references/healthcheck.md) <br>
- [Scoring methodology](references/scoring.md) <br>
- [SKILL.md template](references/template.md) <br>
- [Testing your skill](references/testing.md) <br>
- [ClawHub skill page](https://clawhub.ai/dorukardahan/skeall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline text, code blocks, shell commands, checklists, and edit proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, scan, or improve skill files when the user authorizes edits to an explicit path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
