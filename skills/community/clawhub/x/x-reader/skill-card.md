## Description:

Fetches, transcribes, and analyzes content from URLs, files, or transcripts across supported web, social, RSS, Telegram, and video platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifecn](https://clawhub.ai/user/lifecn)

### License/Terms of Use:

MIT

## Use Case:

Developers and content-focused agent users use X Reader to turn URLs, local files, or transcripts into structured content, summaries, sourced insights, and action-oriented analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary URL fetching could expose private network resources or authenticated content if used on untrusted links.

Mitigation: Use the skill only with trusted URLs, avoid running it in sensitive cloud or corporate networks, and add network egress controls or URL allowlists before broad deployment.

Risk: Saved browser sessions can retain cookies or login state for supported platforms.

Mitigation: Avoid saved sessions unless required, use low-privilege dedicated accounts, restrict access to session files, and delete stored sessions when no longer needed.

Risk: Fetched content may be saved locally as JSON or Markdown.

Mitigation: Set inbox and output paths deliberately, review stored content before syncing it to shared locations, and disable optional Markdown output when persistence is not needed.

Risk: External MCP exposure can make URL-reading tools reachable over the network.

Mitigation: Prefer stdio or localhost operation; require authentication and a trusted reverse proxy before enabling external access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lifecn/skills/x-reader)
- [Source Repository](https://github.com/runesleo/x-reader)
- [Issue Tracker](https://github.com/runesleo/x-reader/issues)
- [Groq API Keys](https://console.groq.com/keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and structured JSON/text results, with inline shell commands and configuration snippets where setup is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save fetched content to a JSON inbox or optional Markdown output when configured.]

## Skill Version(s):

0.2.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
