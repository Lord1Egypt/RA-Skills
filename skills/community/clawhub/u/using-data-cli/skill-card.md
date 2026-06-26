## Description: <br>
Use when the user wants to discover, track, sync, or query news, RSS, social, financial, or other external sources through agent-data-cli and any configured source workspace such as agent-data-hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[severinzhong](https://clawhub.ai/user/severinzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate agent-data-cli for source discovery, channel subscription, remote sync, local content queries, and explicit content interactions across configured data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide remote interactions such as likes, comments, source installation, or source uninstallation. <br>
Mitigation: Require explicit source, verb, and content refs before running content interaction commands, and report remote side effects clearly. <br>
Risk: Sync, subscription, scheduled jobs, and shell redirection can create or modify local databases, logs, source workspaces, and output files. <br>
Mitigation: Confirm persistence-oriented intent, keep paths explicit, and distinguish remote discovery from local writes in the final report. <br>
Risk: The skill depends on an external agent-data-cli repository and configured source workspace. <br>
Mitigation: Verify trust in the external repository and workspace location before installation or ongoing use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/severinzhong/using-data-cli) <br>
- [agent-data-cli repository](https://github.com/severinzhong/agent-data-cli) <br>
- [Command Semantics](references/command-semantics.md) <br>
- [Task Patterns](references/task-patterns.md) <br>
- [Result Reporting](references/result-reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and concise execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSONL-oriented command pipelines and local file redirection when the user requests machine-readable filtering or saved snapshots.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
