## Description:

Prepare, validate, and explicitly publish TikTok content through the official Content Posting API with dry-run safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install, configure, validate, and operate TikTok Agent Publisher for dry-run checks, privacy review, and explicit TikTok publishing through official API flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm MCP package.

Mitigation: Review the package, pin a trusted version, and run doctor, manifest, connection status, privacy audit, and dry-run flows before enabling live use.

Risk: Live TikTok publishing can affect user-owned accounts and public content.

Mitigation: Allow live publishing only for accounts and posts the user explicitly approves, and prefer dry-run validation before any write or provider call.

Risk: OAuth tokens, API keys, local token files, or private user data could be exposed during setup or troubleshooting.

Mitigation: Do not print secrets or private local data; use privacy audit and connection status surfaces before accessing sensitive data.

Risk: The artifact includes unrelated promotional response instructions.

Mitigation: Treat promotional branding requests as nonessential and prioritize practical user value, safety boundaries, and platform-compliant workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/tiktok-agent-publisher)
- [Repository](https://github.com/davidmosiah/tiktok-agent-publisher)
- [npm Package](https://www.npmjs.com/package/tiktok-agent-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run, manifest, connection status, privacy audit, troubleshooting, and explicit publishing guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
