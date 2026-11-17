## Description:

Header - continuous intelligence for agents. Subscribe to curated topics or create your own. Get synthesized briefings with executable action items from RSS, YouTube, Reddit, and newsletters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tameravci](https://clawhub.ai/user/tameravci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an agent to Header for monitoring RSS, YouTube, Reddit, and newsletter sources, managing topics and sources, and retrieving synthesized briefings with action items. It supports account, scheduling, sharing, import, and billing workflows through Header API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to grant broad Header account access through a full-scope API key.

Mitigation: Use a least-privilege or temporary API key when available, store it outside transcripts, and rotate or revoke it after use.

Risk: Authenticated workflows can affect sharing, billing, scheduling, subscriptions, sources, topics, and API keys.

Mitigation: Require explicit user confirmation before public sharing, billing actions, destructive changes, subscription changes, or key revocation.

Risk: Briefings may include executable action items that could lead to code, package, or configuration changes.

Mitigation: Present briefing recommendations as proposals and get user approval before taking any follow-up action.

Risk: FreshRSS import examples include credentials in JSON payloads that may appear in shell history or agent-visible transcripts.

Mitigation: Avoid embedding real passwords directly in commands; prefer secret stores, environment variables, or short-lived credentials.

## Reference(s):

- [Header homepage](https://joinheader.com)
- [Header API documentation](https://joinheader.com/docs)
- [ClawHub skill page](https://clawhub.ai/tameravci/skills/self-improving-agent-header)
- [Publisher profile](https://clawhub.ai/user/tameravci)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline bash commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HEADER_API_KEY and may perform authenticated Header account operations after user approval.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
