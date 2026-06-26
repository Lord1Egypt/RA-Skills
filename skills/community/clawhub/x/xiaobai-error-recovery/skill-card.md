## Description: <br>
4R error recovery framework for recognizing failures, attempting bounded recovery, reporting unresolved issues, and remembering fixes so agent work is not lost silently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make agents stop on errors, diagnose common failures, retry only when appropriate, and report clear recovery status to the human user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recovery may touch authentication, permissions, workflow files, or other sensitive state. <br>
Mitigation: Require human approval before using tokens, changing authentication, running privileged fixes, or modifying workflow files. <br>
Risk: Error reports or saved recovery logs may contain credentials, paths, or other sensitive details. <br>
Mitigation: Redact secrets and sensitive identifiers before reporting or storing error records. <br>
Risk: Repeated retries can make a failure worse or obscure the original cause. <br>
Mitigation: Limit retries to the documented maximum of three attempts and escalate to the human user when recovery fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/xiaobai-error-recovery) <br>
- [README](artifact/README.md) <br>
- [README_EN](artifact/README_EN.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with diagnostic text and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bounded retry plans, error reports, recovery status, and suggested follow-up actions.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
