## Description:

Fetches trending news and articles from Tencent Cloud Online Search API (SearchPro), supporting web-wide or site-specific queries and JSON, CSV, TXT, and Markdown outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search current news, trending topics, and keyword-matched articles through Tencent Cloud SearchPro, then return or save structured results for research, monitoring, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud API credentials, and ClawHub security evidence flags credential handling as needing review.

Mitigation: Use dedicated, least-privileged temporary Tencent Cloud keys, keep config.json out of version control, set restrictive file permissions, and rotate credentials after testing.

Risk: The skill writes search results to user-configured output paths, which can expose data or touch sensitive locations if configured poorly.

Mitigation: Run in an isolated directory or container, use only non-sensitive output directories, and avoid absolute or sensitive output paths.

Risk: The release has a suspicious ClawHub security verdict because credential and file-output handling need review.

Mitigation: Review the source before installation and follow ClawHub security guidance before supplying credentials.

## Reference(s):

- [Tencent Web Search API on ClawHub](https://clawhub.ai/neuhanli/skills/tencenthotsearch-skill)
- [Tencent Cloud Online Search Product Page](https://cloud.tencent.com/product/ais)
- [Tencent Cloud Online Search API Documentation](https://cloud.tencent.com/document/product/1139/46888)
- [Tencent Cloud Access Management Console](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, TXT, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and search results saved or printed as Markdown, JSON, CSV, or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud SecretId and SecretKey in config.json; writes result files to the configured output directory unless printing to console.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
