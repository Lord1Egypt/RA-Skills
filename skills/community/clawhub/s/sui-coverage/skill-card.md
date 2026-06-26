## Description: <br>
Analyze Sui Move test coverage, identify untested code, write missing tests, and perform security audits. Includes Python tools for parsing coverage output and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Sui Move coverage, identify untested functions, assertions, and branches, write missing tests, and document security concerns found during test work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to stage and commit repository changes without an explicit approval step. <br>
Mitigation: Require explicit user approval before staging or committing, and review generated diffs before accepting test changes. <br>
Risk: The workflow runs local Sui coverage commands and may edit test files in the target package. <br>
Mitigation: Run it only in the intended Sui Move repository, keep unrelated changes separate, and review coverage reports and generated tests before use. <br>
Risk: Security observations produced during coverage work may be incomplete or incorrect. <br>
Mitigation: Treat security findings as review inputs and validate them with project maintainers or a dedicated security review before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EasonC13/sui-coverage) <br>
- [Sui Coverage GitHub homepage](https://github.com/EasonC13-agent/sui-coverage-demo) <br>
- [Sui Coverage source tree](https://github.com/EasonC13-agent/sui-skills/tree/main/sui-coverage) <br>
- [Sui install documentation](https://docs.sui.io/guides/developer/getting-started/sui-install) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and Move code blocks; helper scripts can emit JSON or Markdown coverage reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the Sui CLI; may propose or create test changes in a local Sui Move package.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
