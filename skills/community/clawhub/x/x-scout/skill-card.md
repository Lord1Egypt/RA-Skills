## Description:

X-Scout is a CLI skill for searching X/Twitter, scraping profiles and replies, transcribing embedded videos, and classifying tweets as replicable methods or general content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aces1up](https://clawhub.ai/user/aces1up)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content research teams use X-Scout to gather X/Twitter posts, profile activity, replies, and video transcripts for social intelligence and method discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage telemetry is reported to clawagents.dev during setup and normal CLI runs.

Mitigation: Review telemetry acceptability before installation and run only where this reporting is approved.

Risk: API keys may be stored in plaintext config files in the project directory and home directory.

Mitigation: Use isolated credentials, restrict file access, and rotate keys if generated config files may have been exposed.

Risk: Tweet content, queries, media audio, and classification prompts may be processed by external services.

Mitigation: Avoid submitting confidential or regulated data and review the service terms for TwitterAPI.io, OpenRouter, Cerebras, and Deepgram.

Risk: The setup script has an input handling flaw reported by the security evidence.

Mitigation: Review setup.sh before execution and avoid running setup with privileged accounts.

## Reference(s):

- [X-Scout homepage](https://clawagents.dev/x-scout)
- [ClawHub X-Scout listing](https://clawhub.ai/aces1up/skills/x-scout)
- [TwitterAPI.io](https://twitterapi.io)
- [OpenRouter](https://openrouter.ai)
- [Cerebras API](https://api.cerebras.ai/v1/chat/completions)
- [Deepgram](https://deepgram.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Terminal table text or structured JSON from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWITTERAPI_KEY; optional OPENROUTER_API_KEY, CEREBRAS_API_KEYS, and DEEPGRAM_API_KEY enable classification, query optimization, and transcription.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
