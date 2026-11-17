## Description:

AI browser automation protocol \u2014 run pre-built skills for 41 sites, or forge new ones. MCP native, deterministic, zero AI at runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonting1010](https://clawhub.ai/user/leonting1010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Tap to configure deterministic browser automation through MCP, run pre-built site skills, and create reusable site-specific automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can act inside logged-in accounts and perform sensitive actions.

Mitigation: Confirm posts, purchases, form submissions, destructive navigation, and tab-closing actions before running Tap workflows.

Risk: Community .tap.js scripts may execute behavior the user has not reviewed.

Mitigation: Review community scripts before installing or executing them, especially when they interact with authenticated sites.

Risk: Installing the Tap binary or Chrome extension from an untrusted source could expose the browser session to unwanted automation.

Mitigation: Install only from trusted sources and review the binary or source and Chrome extension before enabling Tap.

## Reference(s):

- [ClawHub Tap skill page](https://clawhub.ai/leonting1010/skills/tap)
- [Tap homepage](https://github.com/LeonTing1010/tap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool names, install commands, browser automation examples, and configuration snippets.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
