## Description:

Web Access Skill guides an agent through web search, page fetching, and Chrome CDP browser automation for logged-in, dynamic, and interactive web tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deardavidzheng](https://clawhub.ai/user/deardavidzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to give an agent a structured approach for web research, page extraction, and browser-backed interactions when static search or fetch tools are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over a logged-in Chrome session.

Mitigation: Use a separate Chrome profile or test account, avoid sensitive sites such as banking, email, and admin consoles, and install only when this level of browser access is acceptable.

Risk: The local browser proxy supports unauthenticated actions such as tab navigation, JavaScript evaluation, clicks, screenshots, and file input setting.

Mitigation: Keep the proxy bound to localhost, stop it when not needed, and require explicit confirmation before uploads, form submissions, posts, purchases, screenshots, or actions on existing tabs.

Risk: Local file interactions can expose or upload files if an agent is directed to use unintended paths.

Mitigation: Confirm exact file paths before upload, use temporary working files for screenshots or extracted media, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deardavidzheng/skills/web-access-skill)
- [CDP Proxy API Reference](references/cdp-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to use local browser-control API calls, screenshots, and file-upload commands when the user approves the task.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
