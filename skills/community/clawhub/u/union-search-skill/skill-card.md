## Description:

Union Search Skill gives agents a unified interface for searching across developer communities, social platforms, web search engines, video services, RSS feeds, and image sources, with structured output, filtering, response archiving, and batch image download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runningz1](https://clawhub.ai/user/runningz1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-oriented agents use this skill to run multi-platform searches, compare results, collect structured search output, and save raw responses or downloaded image assets for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command handling may expose users to unintended command execution when helper scripts receive untrusted queries.

Mitigation: Review the Exa helper before installation and avoid using the Exa mcporter script with untrusted queries.

Risk: Token routing can send API credentials or session-derived access to the wrong service if host configuration is changed.

Mitigation: Keep TIKHUB_HOST set only to the real TikHub API host and use least-privilege API keys.

Risk: Browser cookies, session cookies, raw responses, downloads, search logs, and image metadata can contain sensitive local data.

Mitigation: Avoid browser or session cookies unless needed, and treat generated logs, response archives, downloads, and metadata as sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runningz1/skills/union-search-skill)
- [Skill overview](artifact/README.md)
- [API credential guide](artifact/references/api_credentials.md)
- [Rate limits](artifact/references/rate_limits.md)
- [Platform notes](artifact/references/platform_notes.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Union search module](artifact/scripts/union_search/README.md)
- [Union image search module](artifact/scripts/union_image_search/UNION_IMAGE_SEARCH_README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown tables, JSON responses, saved response files, downloaded image files, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May archive raw API responses, search logs, downloads, and image metadata locally.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
