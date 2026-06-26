## Description: <br>
Skill Creator Pro helps agents create, edit, test, benchmark, package, and improve skills through eval-driven iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to draft new skills, improve existing skills, run evaluation loops, compare outputs, optimize trigger descriptions, and package skill releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation tooling can start local browser or server processes and may affect unrelated local processes. <br>
Mitigation: Prefer static viewer mode, check for port conflicts before using a live review server, and review running processes before cleanup. <br>
Risk: Automated evaluation and description optimization can send skill and evaluation content through the Claude CLI. <br>
Mitigation: Use these flows only in repositories where the content is appropriate for the configured Claude CLI account, and avoid sensitive repositories unless that data sharing is acceptable. <br>
Risk: The skill edits and packages other skills, so incorrect guidance can propagate into released artifacts. <br>
Mitigation: Review generated diffs, run focused evaluations, and scan packaged skills before deployment. <br>


## Reference(s): <br>
- [Skill Creator Pro ClawHub page](https://clawhub.ai/zihaofeng2001/skill-creator-pro) <br>
- [Anthropic official skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) <br>
- [Skill Creator JSON schemas](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, code, and shell command snippets; may also produce or update files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files, evaluation workspaces, benchmark reports, packaged skill archives, and static HTML review reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
