## Description:

Browser automation via SLBrow MCP and HTTP API for navigating pages, analyzing content, managing tabs, searching history, extracting text, and controlling the browser when the SLBrow server and browser extension are installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeted](https://clawhub.ai/user/adeted)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and browser-automation users use this skill to guide agents through SLBrow browser control workflows, including page navigation, content extraction, tab management, browser history search, and Seelink player AI actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to access browser history and page content.

Mitigation: Require explicit user approval before history searches or page extraction, and use a separate browser profile for agent-driven browsing.

Risk: The skill can guide an agent to navigate pages, close tabs, or manipulate active browser sessions.

Mitigation: Confirm target tabs and URLs before navigation or tab changes, and avoid using the skill in browser profiles with sensitive active sessions.

Risk: The skill relies on a local SLBrow server package and browser extension.

Mitigation: Pin and verify the SLBrow server package and extension, and keep the server bound to localhost.

Risk: Seelink/VAI player actions can alter media presentation on web pages.

Mitigation: Require explicit user approval before applying Seelink/VAI player actions and verify selected player IDs or positions before execution.

## Reference(s):

- [SLBrow REST API Reference](references/api-reference.md)
- [SLBrow Workflow Checklist](SKILL_COMPACT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool names, JSON request examples, curl commands, and JavaScript CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on a local SLBrow server, connected browser extension, and selected browser or VAI tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
