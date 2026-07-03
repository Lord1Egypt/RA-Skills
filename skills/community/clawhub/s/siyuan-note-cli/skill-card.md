## Description: <br>
Connects an agent to a local SiYuan Note workspace through the siyuan-note-cli command-line tool for querying, creating, and modifying notes, notebooks, documents, blocks, and databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agilebuilder](https://clawhub.ai/user/agilebuilder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-work agents use this skill to search, read, create, and update SiYuan notes while preserving Markdown formatting and verifying write operations. It is intended for workflows where a user explicitly wants an agent to use a local SiYuan workspace as task context or as a destination for saved results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to local SiYuan notes, including note creation, modification, deletion, and database operations. <br>
Mitigation: Install it only when local SiYuan access is intended, keep the API token private, prefer read-only or query-limited workflows unless writes are requested, confirm destructive operations, and verify write results. <br>
Risk: The skill directs agents to read a persistent "AI Assistant Guide" note before operations, which could influence later behavior if that note contains unsafe or adversarial instructions. <br>
Mitigation: Review the guide note before use, avoid storing adversarial or sensitive instructions there, and treat its contents as user-managed context that should not override higher-priority safety or system requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/siyuan-note-cli) <br>
- [Server-resolved GitHub provenance](https://github.com/agilebuilder/work-skills/tree/master/skills/siyuan-note-cli) <br>
- [Command reference](references/commands.md) <br>
- [Workflow examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples and optional JSON, YAML, or table output from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running local SiYuan client and a configured API token; write workflows should verify results after creation or modification.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
