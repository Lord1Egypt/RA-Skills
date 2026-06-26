## Description: <br>
Manage TinyTalkingTodos lists and items via the ttt CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshuacrowley](https://clawhub.ai/user/joshuacrowley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create, inspect, update, delete, and batch-manage TinyTalkingTodos lists and todo items through the ttt CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can log in to a TinyTalkingTodos account and export credentials for scripts. <br>
Mitigation: Install only if you trust the external @ojschwa/ttt-cli package, avoid credential export unless necessary, and do not print or log exported credentials. <br>
Risk: The skill supports todo and list mutations, including deletes and batch changes. <br>
Mitigation: Confirm destructive or batch operations before running them and use the CLI undo capability when a supported operation needs to be reverted. <br>
Risk: The daemon can maintain a background connection for faster commands. <br>
Mitigation: Stop the daemon when a persistent background connection is not wanted. <br>


## Reference(s): <br>
- [TinyTalkingTodos homepage](https://tinytalkingtodos.com) <br>
- [ClawHub skill page](https://clawhub.ai/joshuacrowley/ttt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ttt CLI and an authenticated TinyTalkingTodos account for account-backed operations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
