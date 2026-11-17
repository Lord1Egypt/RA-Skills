## Description:

Connects websites to the local-mcp browser bridge through fixed UXC links for native WebMCP sites, adapter-backed sites, site-scoped browser profiles, and explicit bridge presentation modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or refresh fixed UXC commands for WebMCP/local-mcp sites, inspect tool schemas, manage per-site browser profiles, and recover sessions when site tools are not attached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent site links and browser profiles that may retain logged-in sessions on disk.

Mitigation: Use separate site-scoped profiles, avoid sensitive accounts unless persistence is acceptable, and remove profiles when the session should no longer be retained.

Risk: The default launcher uses npm-launched local-mcp code, which evidence flags as unpinned.

Mitigation: Prefer pinned or locally installed local-mcp and Playwright versions before using the skill in trusted workflows.

Risk: Browser automation can act through authenticated sessions on trusted sites or adapters.

Mitigation: Inspect tool help before writes, require explicit user intent for destructive actions, and use only trusted sites and adapters.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Source Modes](references/source-modes.md)
- [Link Patterns](references/link-patterns.md)
- [Troubleshooting](references/troubleshooting.md)
- [Ensure Links Script](scripts/ensure-links.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fixed UXC link workflows and browser-session recovery guidance for agent execution.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
