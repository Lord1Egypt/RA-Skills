## Description: <br>
Manage files on remote machines over Tailscale SSH (Tailnet). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xeon0v0](https://clawhub.ai/user/xeon0v0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list, inspect, transfer, modify, and remove files on remote OpenClaw nodes reachable through Tailscale SSH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad remote and local file-control power over Tailnet hosts using the user's SSH privileges. <br>
Mitigation: Verify the exact host, path, and requested operation before execution; use limited SSH identities and Tailscale ACLs where possible. <br>
Risk: Write, delete, move, chmod, push, and pull operations can alter or expose files on local or remote systems. <br>
Mitigation: Treat these actions as high risk, require explicit confirmation, avoid privileged system paths, and review overwrite or deletion targets before running the helper. <br>
Risk: Inline transfer of large or binary file content can exceed invoke payload limits. <br>
Mitigation: Use scp-based push or pull for files of 3KB or larger and for binary content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON helper results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts return JSON; files of 3KB or larger and binary files are handled through scp-based push or pull operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
