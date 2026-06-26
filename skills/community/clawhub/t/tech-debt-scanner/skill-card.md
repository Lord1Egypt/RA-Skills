## Description: <br>
Scan codebases for technical debt — TODO/FIXME comments, deprecated APIs, complexity hotspots, outdated patterns, missing tests, large files — then prioritize with AI reasoning and generate remediation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit repositories for technical debt, complexity hotspots, stale patterns, dependency health issues, and test gaps before refactoring or sprint planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository contents, git metadata, and dependency metadata, which may expose sensitive project information to the agent session. <br>
Mitigation: Run it only when a repository audit is intended and review the target scope before scanning. <br>
Risk: Dependency checks may query package registries or other networked sources when allowed. <br>
Mitigation: Review proposed commands before permitting networked dependency checks, especially in restricted environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable text or Markdown reports, with optional structured JSON for CI/CD integration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include prioritized findings, severity, effort estimates, risk reasoning, remediation steps, metrics, and CI exit-code guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
