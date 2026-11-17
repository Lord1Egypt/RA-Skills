## Description:

Cheap first-pass web discovery without launching Chrome: fetch SSR pages, run bounded JS, find routes, forms, and API endpoints, extract structured data, and detect bot-wall or browser-only escalation points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[protostatis](https://clawhub.ai/user/protostatis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform inexpensive first-pass web discovery, structured extraction, route/form/API discovery, and simple form workflows before escalating browser-only pages to a managed browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local browsing binary that makes outbound requests from the user's machine.

Mitigation: Install only from trusted pyunbrowser sources and prefer pinned or reviewed package versions in sensitive environments.

Risk: Cookies supplied to the tool can act as login credentials for the exporting user.

Mitigation: Treat cookies as credentials, scope them to the authorized host, clear them after authenticated use, and require explicit approval before account-changing actions.

Risk: Local challenge-cookie services can expose browser cookies if bound or allowed too broadly.

Mitigation: Keep cookie services loopback-bound, use host allowlists for private or internal targets, and avoid public interfaces.

## Reference(s):

- [unbrowser project homepage](https://github.com/protostatis/unbrowser)
- [unbrowser RPC methods](https://github.com/protostatis/unbrowser#rpc-methods)
- [ClawHub skill page](https://clawhub.ai/protostatis/skills/unbrowser)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell, JSON-RPC, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes escalation guidance, host-scoped cookie handling, and no declared environment-variable credentials.]

## Skill Version(s):

0.0.21 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
