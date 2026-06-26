## Description: <br>
Skill Guard helps agents check OpenClaw skills before installation, scan installed skill files for risky patterns, and verify user-created integrity baselines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skill Guard to review OpenClaw skills before installation, audit installed skills for dangerous text patterns, and compare skill files against user-approved baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner findings are advisory and can require context to interpret correctly. <br>
Mitigation: Review reported patterns and the underlying skill files before installing or keeping a skill. <br>
Risk: Integrity baselines can make a changed or compromised skill appear expected if accepted without review. <br>
Mitigation: Create baselines only on explicit user request and review the baseline contents before keeping them. <br>
Risk: Related skills promoted by the artifact are separate installs with their own risk profiles. <br>
Mitigation: Review and scan each optional related skill before installing it. <br>


## Reference(s): <br>
- [Skill Guard on ClawHub](https://clawhub.ai/tommot2/tommo-skill-guard) <br>
- [Security Pattern Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown reports with file, line, pattern, and risk summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-approved integrity baseline summaries stored under memory/skill-guard/.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
