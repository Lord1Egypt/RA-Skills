## Description:

Fetches YouTube video transcripts through the APIFY API using residential proxies, with plain-text and JSON output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inaor](https://clawhub.ai/user/inaor)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve YouTube transcripts from environments where direct transcript access may be blocked. It supports transcript capture as text or timestamped JSON, optional file output, and language preference selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the requested YouTube video URL and related request metadata to APIFY.

Mitigation: Install only when sharing that data with APIFY is acceptable for the intended workflow.

Risk: The APIFY token is used by the transcript script and may appear in logs because the script sends it as a query parameter.

Mitigation: Use a dedicated, least-privileged APIFY token, keep it out of source control, avoid permanent shell startup storage when possible, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inaor/skills/some-other-youtube)
- [APIFY Pricing](https://apify.com/pricing)
- [APIFY API token setup](https://console.apify.com/account/integrations)
- [YouTube Transcripts Actor](https://apify.com/karamelo/youtube-transcripts)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text or JSON transcript output, optionally written to a file; setup and usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_API_TOKEN and sends the requested YouTube video URL and related request metadata to APIFY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
