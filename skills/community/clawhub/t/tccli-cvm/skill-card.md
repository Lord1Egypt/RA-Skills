## Description: <br>
Manage Tencent Cloud CVM instances with the TCCLI command-line tool, including instance creation, querying, deletion, launch template management, price inquiry, and related resource cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agilebuilder](https://clawhub.ai/user/agilebuilder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Tencent Cloud CVM instances through TCCLI, including provisioning, querying, operating, pricing, and cleanup workflows. It is also useful when an agent needs to prepare directly executable shell commands and workspace-local default configuration for repeated CVM operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Tencent Cloud CVM resources and run shell commands on instances. <br>
Mitigation: Install it only for intended Tencent Cloud administration, use a least-privilege Tencent Cloud role, avoid broad production credentials, and confirm every remote command before it runs. <br>
Risk: Workspace defaults may store passwords in plaintext in .claude/tccli-cvm-defaults.json. <br>
Mitigation: Prefer environment variables or runtime input for passwords, exclude the defaults file from Git, and delete it when persistent defaults are no longer needed. <br>
Risk: Destructive operations can terminate instances or release related EIPs and disks, affecting availability or billing. <br>
Mitigation: Confirm destructive actions with the user, query attached resources before termination, and verify cleanup results after releasing resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/tccli-cvm) <br>
- [Server-resolved GitHub source](https://github.com/agilebuilder/dev-skills/tree/master/skills/tccli-cvm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce TCCLI commands, JSON parameter examples, workspace-local defaults, confirmation prompts, and operational guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
