## Description: <br>
Monitors a coding session for drift from the stated task and surfaces off-scope work before unrelated changes accumulate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill during focused implementation, bug fixes, and review preparation to keep file changes aligned with a task anchor and make off-scope work visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scope monitoring can interrupt open-ended exploration when the task anchor or drift tolerance is too strict. <br>
Mitigation: Set a clear task anchor and use Off or Exploratory mode for open-ended work. <br>
Risk: Session summaries may include sensitive project details. <br>
Mitigation: Avoid saving or sharing summaries that include confidential code, filenames, business logic, or project context. <br>
Risk: Suggested stash, commit, or scope expansion actions can affect the user's workflow state. <br>
Mitigation: Require explicit confirmation before any stash, commit, or scope expansion action. <br>


## Reference(s): <br>
- [Scope Sentinel on ClawHub](https://clawhub.ai/jcools1977/scope-sentinel) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance with structured alerts, options, and session summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, network access, or hidden install behavior reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
