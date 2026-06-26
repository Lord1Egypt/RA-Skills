## Description: <br>
Safely triage and remediate GitHub dependency hygiene issues with explicit guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrummler17](https://clawhub.ai/user/mrummler17) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use RepoMedic to triage failing Dependabot updates, dependency vulnerabilities, lockfile drift, and CI or Vercel failures caused by dependency resolution. It emphasizes conservative remediation, explicit approval gates, branch-based changes, and plain-English risk communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect and modify dependency-related files in a target repository. <br>
Mitigation: Keep work on a non-default branch, review planned file and version changes before execution, and validate with install, build, test, lint, and audit checks where available. <br>
Risk: Major upgrades or medium/high-risk dependency changes can introduce runtime or tooling regressions. <br>
Mitigation: Require explicit approval for major upgrades or non-trivial changes, prefer targeted patch or minor remediation, and stop for confirmation when risk is unclear. <br>


## Reference(s): <br>
- [RepoMedic on ClawHub](https://clawhub.ai/mrummler17/repomedic) <br>
- [mrummler17 publisher profile](https://clawhub.ai/user/mrummler17) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with structured sections and inline commands or file/version details when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes issue summary, recommended action, risk level, changes made, validation results, plain-English summary, and next step.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
