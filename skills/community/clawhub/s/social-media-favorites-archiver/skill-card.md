## Description:

Sync a user's Bilibili/B站, Xiaohongshu/小红书/RedNote, and Douyin/抖音 favorites into local Markdown/Obsidian with local ASR/OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvlin-dev](https://clawhub.ai/user/dvlin-dev)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to back up, migrate, and organize their own authorized Bilibili, Xiaohongshu/RedNote, and Douyin favorites into a local Markdown or Obsidian vault. It guides installation, configuration, login, synchronization, local ASR/OCR processing, reporting, retry, cleanup, and optional scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs and runs an external GitHub CLI by tag while using an authenticated browser session.

Mitigation: Install only when the external project and maintainer are trusted, or prefer a reviewed full commit SHA or signed release with a published digest; use a dedicated browser profile and user-owned vault, state, and cache paths.

Risk: Browser cookies, platform tokens, signed media URLs, private responses, or private content could be exposed if copied into configuration, logs, fixtures, or reports.

Mitigation: Keep secrets and live content out of configs, logs, fixtures, and Git; report only sanitized aggregate `smfa status` and `smfa report` output.

Risk: Optional enrichment can send selected archived text to an OpenAI-compatible provider when explicitly enabled.

Mitigation: Keep enrichment disabled unless requested, send only the documented redacted text allowlist, and require schema-validated structured output.

Risk: Platform layout changes, authentication prompts, or ephemeral media URLs can make a partial enumeration look complete.

Mitigation: Pause for user-owned QR, captcha, login, or device confirmation, treat layout drift as a typed adapter failure, and re-enumerate before retrying media failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dvlin-dev/skills/social-media-favorites-archiver)
- [Project homepage](https://github.com/dvlin-dev/social-media-favorites-archiver)
- [Configuration](references/configuration.md)
- [Bilibili](references/platform-bilibili.md)
- [Xiaohongshu / RedNote](references/platform-xiaohongshu.md)
- [Douyin](references/platform-douyin.md)
- [Troubleshooting and scheduling](references/troubleshooting.md)
- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON status/report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown/Obsidian archive content through the external CLI; optional enrichment is text-only and explicitly enabled.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
