## Description: <br>
Skill Validator tests newly installed OpenClaw skills for functional completeness, edge cases, potential problems, UX quality, and improvement opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate OpenClaw skills after installation, checking required files, dependencies, normal behavior, edge cases, UX characteristics, and actionable remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator can automatically run scripts from other skills, which may execute untrusted code without sandboxing or clear per-run consent. <br>
Mitigation: Use it only on trusted skills or inside a disposable sandbox, inspect target scripts before running validation, and gate execution with explicit confirmation. <br>
Risk: Validation checks for empty parameters or diagnostic behavior may trigger unexpected behavior in target scripts. <br>
Mitigation: Prefer static analysis for unknown skills and apply execution timeouts, resource limits, and read-only isolation when dynamic checks are required. <br>


## Reference(s): <br>
- [Skill Validator on ClawHub](https://clawhub.ai/dongrebeccahhh-boop/xiaosanwan-skill-validator) <br>
- [Security hardening notes](SECURITY.md) <br>
- [Validation report template](templates/report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal text and Markdown validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports pass, warning, failure, skip, score, grade, and improvement recommendation summaries for a selected skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
