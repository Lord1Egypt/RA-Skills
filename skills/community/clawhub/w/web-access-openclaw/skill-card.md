## Description:

Enables OpenClaw agents to search, read, and interact with dynamic or logged-in websites through a user's existing Chrome session via CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysyyrps777](https://clawhub.ai/user/ysyyrps777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when an agent needs browser-backed web access, including dynamic pages, authenticated sessions, UI interaction, media inspection, file upload flows, and sites that do not work through static fetching alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real logged-in Chrome session through a long-lived unauthenticated local proxy.

Mitigation: Install it only when browser-session automation is needed, avoid running it while sensitive tabs are open, and stop the proxy when finished.

Risk: Browser actions can upload files, submit forms, post or publish content, delete data, make purchases, or save screenshots.

Mitigation: Require explicit user review before state-changing actions or screenshot/file capture, and prefer read-only inspection before write actions.

Risk: Private, internal, signed, or token-bearing URLs can expose sensitive access context if sent to third-party preprocessors.

Mitigation: Do not send those URLs to Jina or similar third-party preprocessors; use direct browser inspection instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysyyrps777/skills/web-access-openclaw)
- [CDP Proxy API reference](references/cdp-api.md)
- [Upstream project attribution](https://github.com/eze-is/web-access)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, curl examples, JavaScript snippets, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct browser actions through Chrome CDP and may save screenshots or files when the user explicitly requests those actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
