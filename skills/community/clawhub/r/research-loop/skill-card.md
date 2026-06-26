## Description: <br>
Claude Code compatibility mirror for the Codex-native 10000 Mentors Research Workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research engineers use this skill in Claude Code to run a source-gated research workflow that reads a target repository, plans one bounded micro-step per cycle, produces runnable research artifacts, and gates completion on advisor, executor, and delivery checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create workflow files and publish sanitized artifacts to a target GitHub repository. <br>
Mitigation: Use --no-push or a local-only run for dry runs, then review generated .autonomous-research-workflow and source_changes artifacts before publishing. <br>
Risk: Publishing behavior may use GitHub CLI credentials. <br>
Mitigation: Use appropriately scoped GitHub credentials and avoid running the workflow against private or sensitive repositories unless those credentials and outputs have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/research-loop) <br>
- [Publisher profile](https://clawhub.ai/user/wd041216-bit) <br>
- [Homepage](https://github.com/wd041216-bit/10000-mentors-research-workflow) <br>
- [Advisor Rubric](references/advisor-rubric.md) <br>
- [Executor Template](references/executor-template.md) <br>
- [Innovation Frontier](references/innovation-frontier.md) <br>
- [Phases](references/phases.md) <br>
- [Protocol Hygiene](references/protocol-hygiene.md) <br>
- [State Schema](references/state-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with JSON manifests, source-change files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bounded workflow artifacts under the research run state tree and source_changes mirror; publishing may be local-only or pushed through GitHub CLI credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
