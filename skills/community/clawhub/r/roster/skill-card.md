## Description: <br>
Creates weekly shift rosters (KW-JSON) from CSV availability data and pushes them to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kleberbaum](https://clawhub.ai/user/kleberbaum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Roster operators and scheduling teams use this skill to turn Google Forms CSV availability data into validated weekly shift rosters, update employee records, and prepare PDF or email distribution workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change roster files and employee records in the configured repository. <br>
Mitigation: Use a private repository, a fine-grained single-repository GitHub token, explicit operator confirmation for changes, and dummy-data testing before production use. <br>
Risk: Triggered workflows can distribute roster PDFs through Telegram or email. <br>
Mitigation: Review build-roster.yml and publish-roster.yml before installation and require explicit confirmation before PDF preview or publish actions. <br>
Risk: Employee records can contain personal data such as names, emails, minor status, hour limits, notes, and roster assignments. <br>
Mitigation: Minimize stored data, restrict repository and token access, keep the repository private, and align operation with applicable data protection requirements. <br>


## Reference(s): <br>
- [ClawHub Roster listing](https://clawhub.ai/kleberbaum/roster) <br>
- [README](artifact/README.md) <br>
- [Basic usage example](artifact/examples/basic.md) <br>
- [Command examples](artifact/examples/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or plain-text guidance with JSON roster payloads and bash command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITHUB_TOKEN and ROSTER_REPO; can update roster and employee JSON files and trigger PDF, Telegram, or email delivery workflows through the configured repository.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
