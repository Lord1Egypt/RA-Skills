## Description: <br>
Structured software development workflow for AI-assisted codebases: gated requirement intake with test cases, change impact analysis, typed implementation boundaries, verified delivery, full regression testing, and experience accumulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morelapai](https://clawhub.ai/user/morelapai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use ShipGuard to add a gated workflow around AI-assisted software changes, including requirement intake, impact analysis, implementation boundaries, feature QA, regression checks, and lessons capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update persistent project workflow files that influence future agent behavior. <br>
Mitigation: Review the generated `.dev-workflow/` changes before relying on them, especially permanent rules, lessons, cumulative test cases, and changelog entries. <br>
Risk: Automatic activation on code-change requests may apply the workflow more broadly than intended. <br>
Mitigation: Narrow the activation criteria during installation or require explicit approval before ShipGuard updates persistent project memory. <br>


## Reference(s): <br>
- [ShipGuard repository homepage](https://github.com/morelapAI/shipguard) <br>
- [ShipGuard ClawHub page](https://clawhub.ai/morelapai/shipguard) <br>
- [Hard rules](references/hard-rules.md) <br>
- [Lessons template](references/lessons.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured workflow cards, checklists, code blocks, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent project workflow files under .dev-workflow/ when used in a project.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
