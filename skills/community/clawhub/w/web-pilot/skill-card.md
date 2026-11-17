## Description:

Web Pilot lets agents search the web, extract readable page text, run persistent browser sessions, download files and PDFs, dismiss cookie banners, and return JSON, markdown, or text without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liranudi](https://clawhub.ai/user/liranudi)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and agent users use this skill to search the web, extract readable page text, run stateful browser actions, capture screenshots, and download files without external API keys. It can support accessibility workflows where an agent reads, navigates, and interacts with webpages on a user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can interact with websites, click controls, fill forms, execute JavaScript, and preserve session state.

Mitigation: Use the skill only in isolated environments or for trusted tasks, supervise authenticated or sensitive browsing, and review actions before form submission.

Risk: Search queries, page interactions, and downloaded content can expose sensitive information or introduce untrusted files.

Mitigation: Avoid secrets in search queries, treat downloaded files as untrusted, and scan or sandbox downloaded artifacts before opening them.

Risk: Persistent browser and download behavior has weak local controls according to the security summary.

Mitigation: Avoid shared or high-trust environments unless the persistent-browser and download handling are hardened.

## Reference(s):

- [Web Pilot ClawHub Skill Page](https://clawhub.ai/liranudi/skills/web-pilot)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON by default, with markdown and plain text options for page extraction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write downloaded files, screenshots, and PDF exports to local paths when those actions are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
