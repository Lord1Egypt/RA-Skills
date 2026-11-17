## Description:

TaskTime Pro is a free, open-source, local-first work manager for freelancers, covering tasks, timers, expenses, invoices, and reports; this first-party TaskTime Pro skill lets same-device agents operate the app through scoped access and approval controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tasktimepro](https://clawhub.ai/user/tasktimepro)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, developers, and agent users use this skill to let a same-device agent manage TaskTime Pro work records through the supported local bridge. Common workflows include planning tasks, tracking time, reviewing expenses and reports, preparing invoice data, opening review screens, and recovering agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an external bridge package can create supply-chain exposure if the package or publisher is not trusted.

Mitigation: Install only when TaskTime Pro is an acceptable trusted publisher and prefer a pinned or verified bridge or plugin release when available.

Risk: Granted scopes can permit high-impact billing, export, email, restore, deletion, or destructive record changes.

Mitigation: Review granted scopes after pairing and reserve high-impact actions for explicit user approval in TaskTime Pro.

Risk: Using storage, sync files, or invoice state outside the supported bridge can corrupt or bypass TaskTime Pro validation.

Mitigation: Operate through the TaskTime Pro MCP bridge and visible app session; do not directly mutate browser storage, Yjs documents, Google Drive sync files, invoice state, or billing state.

## Reference(s):

- [TaskTime Pro Agent Docs](https://tasktime.pro/agents/)
- [TaskTime Pro Agent Quickstart](https://tasktime.pro/agents/quickstart/)
- [TaskTime Pro Agent Security Model](https://tasktime.pro/agents/security/)
- [TaskTime Pro MCP Tool Reference](https://tasktime.pro/agents/tools/)
- [Machine-readable MCP Tools](https://tasktime.pro/agents/mcp-tools.json)
- [Bridge Discovery Manifest](https://tasktime.pro/.well-known/tasktime-agent.json)
- [OpenClaw Setup](https://tasktime.pro/agents/openclaw/)
- [TaskTime Pro Debugging Guide](https://tasktime.pro/agents/debugging/)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, markdown]

**Output Format:** [Markdown with JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance is scoped to TaskTime Pro MCP tools and same-device browser approval workflows.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
