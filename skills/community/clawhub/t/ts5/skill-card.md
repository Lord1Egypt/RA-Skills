## Description: <br>
TS5 is a TypeScript full-stack starter skill for monorepo templates with shared types, CI/CD pipelines, and deployment helper commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kleberbaum](https://clawhub.ai/user/kleberbaum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap or inspect a TypeScript full-stack monorepo structure and run helper commands for packages and deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests shell execution permission and exposes deployment-oriented arguments. <br>
Mitigation: Review the disclosed shell script before use and re-check future versions before running --deploy. <br>
Risk: Future releases could replace the current echo-only script with commands that modify files, deploy services, or access the network. <br>
Mitigation: Treat updates as new executable code and review the security scan, changelog, and script behavior before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kleberbaum/ts5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell helper currently prints status messages for init, package, and deploy arguments.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
