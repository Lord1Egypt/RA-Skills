## Description: <br>
AI-driven acceptance execution that autonomously runs [A] steps and asks humans only for [H] steps with precise micro-instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to run SDD acceptance checklists, automate machine-verifiable steps, and request focused yes/no human verification for manual observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands from acceptance checklists and start local services. <br>
Mitigation: Use it only in trusted, version-controlled workspaces and review all backticked checklist commands and service ports before execution. <br>
Risk: The skill may modify code, spec-human-verify.md, and .env files while trying to repair failed checks. <br>
Mitigation: Review resulting file changes after each run and keep source control available to inspect or undo unintended edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/sdd-start-human-verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text prompts with inline shell commands and checklist status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update spec-human-verify.md, code, and local configuration files while executing acceptance checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
