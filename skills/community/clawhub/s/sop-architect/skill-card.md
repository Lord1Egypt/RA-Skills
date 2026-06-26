## Description: <br>
Automatically generates detailed Standard Operating Procedures (SOPs) for recurring digital tasks. Ideal for scaling agency operations or documenting internal AI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operations teams, agency teams, and agent developers use this skill to turn recurring digital tasks into repeatable SOPs with prerequisites, numbered workflow steps, failure modes, and success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can overwrite markdown files outside the advertised SOPs folder when given a path-like task name. <br>
Mitigation: Review before installing if an agent may run the helper script; use simple task names without slashes or '..', check for existing output files, and prefer a fixed version that sanitizes task names, verifies the resolved path stays inside SOPs/, and refuses to overwrite without explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/sop-architect) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown SOP files with numbered steps and success criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script writes SOPs to the SOPs directory using a task-name-derived markdown filename.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
