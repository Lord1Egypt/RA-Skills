## Description:

Tavily Quota Router helps agents route Tavily searches across multiple API keys with failover, rate-limit cooldowns, usage synchronization, and key-status visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangtang0206](https://clawhub.ai/user/fangtang0206)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they have multiple Tavily API keys and need quota-aware search routing, per-key status checks, and controlled recovery from rate-limit or auth failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Tavily API keys may be stored locally in config/keys.json and exposed through backups, shared skill directories, or missing ignore rules.

Mitigation: Keep real keys outside published artifacts, prefer environment variables or a secret manager, verify config/keys.json and state/quota.json are ignored, restrict file permissions, and rotate keys after suspected exposure.

Risk: Rate-limit safety guidance may not fully match runtime failover behavior, so bursts can still consume quota or cool down multiple keys.

Mitigation: Review the router before deployment, use controlled request rates, stop on the first 429, honor Retry-After cooldowns, and test behavior with non-production or low-risk keys.

Risk: The scanner marked the release suspicious because local key storage and safety-rule conflicts require review.

Mitigation: Install only after confirming the multi-key Tavily router is intended for the environment and after scanning the packaged files for secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fangtang0206/skills/tavily-quota-router)
- [README](README.md)
- [Quickstart](QUICKSTART.md)
- [Security Hardening](references/security-hardening.md)
- [State Machine Walkthrough](references/state-machine-2026-07-08.md)
- [Tavily 401/403 Recovery Pattern](references/tavily-401-403-recovery-pattern.md)
- [Tavily 429 Retry-After Handling](references/tavily-429-retry-after-2026-07-17.md)
- [Tavily Search API Endpoint](https://api.tavily.com/search)
- [Tavily API Keys Dashboard](https://app.tavily.com/keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and JSON router responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Router commands require locally configured Tavily API keys; status and search commands produce single-stream command output.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
