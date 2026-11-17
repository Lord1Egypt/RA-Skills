## Description:

Summarize URLs or files with the summarize CLI (x86_64 infrastructure supported).

This skill is ready for commercial/non-commercial use.

## Publisher:

[speechybubble](https://clawhub.ai/user/speechybubble)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to invoke the summarize CLI for concise summaries of URLs, local files, and YouTube links, with optional JSON output and provider-specific model configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends URL, file, or YouTube content to configured AI or extraction providers.

Mitigation: Use it only with providers approved for the content being summarized, and avoid secrets, regulated data, or proprietary files unless that transfer is authorized.

Risk: The skill depends on a third-party CLI distributed through npm or Homebrew.

Mitigation: Install only from the documented speechybubble package or formula after confirming the publisher and package are trusted for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/speechybubble/skills/summarizerx64)
- [summarize GitHub repository](https://github.com/speechybubble/summarize)
- [npm package @speechybubble/summarize](https://www.npmjs.com/package/@speechybubble/summarize)
- [Homebrew formula speechybubble/tap/summarize](https://github.com/speechybubble/homebrew-tap)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text, Markdown, or JSON produced by the summarize CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports length and token-limit controls, extraction-only mode for URLs, and optional provider configuration through environment variables or ~/.summarize/config.json.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
