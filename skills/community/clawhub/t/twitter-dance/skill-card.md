## Description:

Twitter Dance helps agents generate, preview, publish, and manage X/Twitter posts and interactions through apidance.pro and optional Kimi-generated tweet drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan-y25](https://clawhub.ai/user/evan-y25)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and developers use this skill to draft, preview, publish, schedule, and monitor Twitter/X posts and account interactions from command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposed or mishandled credentials may allow unauthorized account or API access.

Mitigation: Remove exposed credentials, rotate affected keys and tokens, and keep secrets in scoped environment variables or a managed secret store.

Risk: Browser-token scraping can create fragile and over-privileged authentication flows.

Mitigation: Replace browser-token extraction guidance with a scoped official authorization flow before installation or use.

Risk: Logs, examples, or diagnostic commands may reveal API keys, auth tokens, or account data.

Mitigation: Redact logs and examples, avoid printing secret values, and remove broad node -e execution permission.

Risk: Automated posting, replies, likes, retweets, follows, or scheduled jobs can perform account actions without adequate review.

Mitigation: Use draft or dry-run modes first, disable scheduled posting by default, and approve account action limits before enabling automation.

## Reference(s):

- [Twitter Dance on ClawHub](https://clawhub.ai/evan-y25/skills/twitter-dance)
- [apidance.pro Documentation](https://doc.apidance.pro)
- [Moonshot Platform](https://platform.moonshot.cn)
- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Auto Reply Guide](AUTO-REPLY-GUIDE.md)
- [GraphQL API Guide](GRAPHQL_API_GUIDE.md)
- [Advanced Features](ADVANCED_FEATURES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce tweet drafts, runnable Node.js commands, environment variable configuration, and operational review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
