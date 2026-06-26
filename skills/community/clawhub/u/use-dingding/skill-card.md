## Description: <br>
Interact with DingTalk enterprise workspace using the dws CLI for contacts, chat, calendar, todo, approvals, attendance, reports, and AITable workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhu888](https://clawhub.ai/user/brucezhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and enterprise operators use this skill to let an agent prepare and execute DingTalk workspace actions such as searching contacts, scheduling meetings, creating todos, handling approvals, reading reports, and importing AITable records. Developers can also use the bundled scripts and references to standardize dws CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad DingTalk workspace authority, including messaging, approvals, employee data access, calendar changes, todo creation, reports, and AITable mutations. <br>
Mitigation: Use least-privilege OAuth credentials, test in a sandbox enterprise first, preview mutations with --dry-run, and require human verification before --yes or --execute commands. <br>
Risk: Installer examples include curl|sh and irm|iex paths for the dws CLI. <br>
Mitigation: Prefer verified releases or building from source, and independently inspect any installer script before running it. <br>
Risk: DingTalk OAuth credentials may be exposed if stored in environment variables or logged by tooling. <br>
Mitigation: Prefer interactive dws auth login with encrypted keychain storage, keep credentials out of logs and repositories, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucezhu888/use-dingding) <br>
- [DingTalk Workspace CLI Releases](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases) <br>
- [DingTalk Open Platform App Console](https://open-dev.dingtalk.com/fe/app) <br>
- [Global Reference](references/global-reference.md) <br>
- [Intent Guide](references/intent-guide.md) <br>
- [Error Codes Reference](references/error-codes.md) <br>
- [AITable Commands](references/products/aitable.md) <br>
- [Calendar Commands](references/products/calendar.md) <br>
- [Chat Commands](references/products/chat.md) <br>
- [Contact Commands](references/products/contact.md) <br>
- [OA Approval Commands](references/products/oa.md) <br>
- [Todo Commands](references/products/todo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or invoke JSON, table, raw, and jq-filtered dws CLI outputs depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
