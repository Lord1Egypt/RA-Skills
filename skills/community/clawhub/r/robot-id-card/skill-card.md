## Description:

Robot Id Card helps agents and developers issue and verify bot identity certificates using RFC 9421-style HTTP message signatures, an Ed25519 registry, CLI tooling, a browser extension, and website SDKs.

This skill is for research and development only.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create bot keys and certificates, run or integrate a bot identity registry, sign bot requests, and verify registered bots in websites or services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports serious gaps that could expose bot identity or allow trust ratings to be manipulated.

Mitigation: Use only for review, experimentation, or tightly controlled local development until the registry signature, admin authentication, report moderation, replay protection, SDK caching, browser-extension scoping, private-key storage, dependency updates, and network binding defaults are fixed.

Risk: Bot identity and trust ratings may be mistaken for a complete access-control system.

Mitigation: Do not rely on this skill alone for production authorization; pair it with independent authentication, authorization, key-management, and monitoring controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cosmofang/skills/robot-id-card)
- [OpenClaw Homepage](https://github.com/Cosmofang/robot-id-card)
- [RIC Protocol Specification v2.0](docs/spec-v2.md)
- [Deployment Guide](docs/deploy.md)
- [CLI README](packages/cli/README.md)
- [SDK README](packages/sdk/README.md)
- [RFC 9421 HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421)
- [Cloudflare Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local key files, registry data, signed request headers, and integration snippets when used by an agent.]

## Skill Version(s):

0.4.0 (source: server release metadata, package.json, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
