## Description:

Weflow Group Summarizer helps agents configure WeFlow API access, monitor WeChat group chats, and summarize new group messages on a heartbeat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusining](https://clawhub.ai/user/liusining)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up WeFlow connectivity, choose WeChat groups, configure prompts and member tracking, and run periodic fetches that an agent turns into group summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and summarize private WeChat group messages and images.

Mitigation: Use it only for groups the user intentionally selects, treat chat and media content as sensitive untrusted input, and avoid sharing generated summaries beyond the intended audience.

Risk: The included proxy can expose the local WeFlow API to a network without authentication.

Mitigation: Do not run the proxy on untrusted networks; bind it to localhost or add authentication, route limits, and firewall restrictions before use.

Risk: Python dependencies are listed without pinned versions.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before production deployment.

## Reference(s):

- [WeFlow HTTP API](reference/HTTP-API.md)
- [WeFlow](https://github.com/hicccc77/WeFlow)
- [ChatLab Format](https://github.com/nichuanfang/chatlab-format)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and setup guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local image paths when new WeChat messages contain images.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
