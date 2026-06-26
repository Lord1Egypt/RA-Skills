## Description: <br>
Todo Sync is intended to help address unsynchronized to-dos between WeCom and Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neutronstar238](https://clawhub.ai/user/neutronstar238) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers using OpenClaw can invoke `/todo_sync` for assistance with coordinating task items between WeCom and Feishu. The artifact indicates the core implementation, tests, and documentation are still planned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review describes the skill as unfinished and requesting broad local file and shell access without documenting how access is scoped or controlled. <br>
Mitigation: Review the skill before installation and avoid granting broad Read, Write, Edit, or Bash access until permissions, data access, and confirmation behavior are documented. <br>
Risk: The intended WeCom and Feishu synchronization behavior may read or modify task data without documented permission boundaries. <br>
Mitigation: Confirm the exact WeCom and Feishu permissions, data touched, and user confirmation steps before using the skill with real task data. <br>


## Reference(s): <br>
- [Todo Sync ClawHub release](https://clawhub.ai/neutronstar238/todo-sync) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline command text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-invoked through `/todo_sync`; no completed synchronization behavior is documented in the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
