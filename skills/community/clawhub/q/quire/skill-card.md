## Description: <br>
Read and modify Quire tasks, projects, comments, statuses, and tags via the quire CLI: list, search, get, create, update, complete or uncomplete, set dates, and comment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quire](https://clawhub.ai/user/quire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Quire workspaces, summarize tasks and projects, and perform limited task updates through the authenticated quire CLI. It is suited for task lookup, project status review, URL resolution, and explicitly confirmed writes such as creating tasks, setting dates, completing tasks, and adding comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the logged-in Quire account and can read workspace task, project, comment, status, and tag data. <br>
Mitigation: Install it only for agents that should access that Quire account, and avoid using it in conversations where workspace data should not be exposed. <br>
Risk: Approved write actions can create or update tasks, change dates or completion state, and post comments visible to other Quire users. <br>
Mitigation: Require explicit confirmation for each write and review the proposed task, field changes, dates, completion state, and comment text before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quire/quire) <br>
- [Quire homepage](https://quire.io) <br>
- [Quire CLI](https://github.com/quire-io/quire-cli) <br>
- [Quire API documentation](https://quire.io/dev/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-aware guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses quire CLI JSON output; write actions require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter, changelog, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
