## Description:

Tracks AI token usage, budgets, and rate-limit context across Anthropic, OpenAI, Gemini, and Manus through a local dashboard and REST API while storing counts rather than prompts or message content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor AI provider token usage, spending, budgets, and local dashboard/API status across multiple services. It is intended for users who can safely manage provider credentials and a localhost service that exposes spend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The localhost API exposes spend and quota data through unauthenticated GET endpoints if the port is reachable.

Mitigation: Keep the service bound to localhost, do not expose the port, and set TOKEN_PANEL_API_TOKEN before enabling write endpoints.

Risk: The skill handles sensitive provider credentials and may fall back to a local plaintext credential file when no OS keychain is available.

Mitigation: Prefer the OS keychain, provide only credentials intended for this tool, and review the fallback warning before use.

Risk: Transcript parsing, generic provider environment variables, live probing, and the systemd service expand what the tool reads or does.

Mitigation: Enable TOKEN_PANEL_READ_TRANSCRIPTS, TOKEN_PANEL_ALLOW_PROVIDER_ENV, live probes, or the service only when those behaviors are intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/token-panel-ultimate)
- [Publisher profile](https://clawhub.ai/user/globalcaos)
- [TinkerClaw project](https://github.com/globalcaos/tinkerclaw)
- [Anthropic Usage and Cost API documentation](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)
- [Gemini API pricing documentation](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini API rate limits documentation](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Manus plans documentation](https://manus.im/docs/introduction/plans)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide setup of local files, credentials, provider API calls, and a localhost REST API; no prompts or message content are intended outputs.]

## Skill Version(s):

2.6.2 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
