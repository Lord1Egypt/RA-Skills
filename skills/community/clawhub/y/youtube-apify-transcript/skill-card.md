## Description:

Fetch YouTube transcripts via the Apify API. Works from cloud IPs (Hetzner, AWS, etc.) by bypassing YouTube's bot detection. Features local caching (free repeat requests) and batch mode. Requires APIFY_API_TOKEN and the Python requests library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch YouTube video transcripts from environments where direct transcript access may be blocked, then process the returned transcript text or JSON for downstream summarization, analysis, or archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A URL-handling flaw can let the local cache read or write JSON files outside the intended cache folder.

Mitigation: Use only trusted YouTube URLs, keep the cache directory away from important JSON files, and fix cache path validation before using the skill in workflows that process untrusted URLs.

Risk: The skill requires an Apify API token for external API access.

Mitigation: Keep the token out of repositories and shared shell history, and prefer a temporary environment variable or secret manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/youtube-apify-transcript)
- [Apify API token setup](https://console.apify.com/account/integrations)
- [Apify YouTube Transcripts Actor](https://apify.com/topaz_sharingan/youtube-transcript-scraper-1)
- [Apify Pricing](https://apify.com/pricing)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text or JSON transcript output, with optional saved files and batch status lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses APIFY_API_TOKEN for authenticated Apify requests and can cache transcripts locally in the configured cache directory.]

## Skill Version(s):

1.4.0 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
