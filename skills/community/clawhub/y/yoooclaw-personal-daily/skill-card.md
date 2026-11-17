## Description:

Generates a Chinese personalized daily news digest from configured user topics, using available search tools or fixed RSS fallback and requiring source and publication-date checks before summarizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Hermes or OpenClaw-compatible agents to turn configured interest topics into a current-day Chinese news briefing with linked sources and trend notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured interest topics may be used in search queries or RSS filtering.

Mitigation: Use non-sensitive topic lists and avoid putting private personal, customer, or credential-like data in configured interests.

Risk: The RSS helper fetches external HTTP(S) feed URLs and does not itself block private, loopback, link-local, or metadata-service addresses.

Mitigation: Run the skill with network egress controls that block private, loopback, link-local, and metadata-service address ranges in sensitive environments.

Risk: News summaries can be misleading if source links or same-day publication times are not verified.

Mitigation: Keep the skill's evidence gate enabled: require a usable source, same-day publication time, topic relevance, and independent corroboration for major or disputed claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-personal-daily)
- [Hermes daily generation workflow](references/generate/hermes.md)
- [OpenClaw daily generation workflow](references/generate/openclaw.md)
- [Search acquisition workflow](references/acquisition/search.md)
- [RSS acquisition workflow](references/acquisition/rss.md)
- [Domestic RSS source list](references/rss/domestic.md)
- [International RSS source list](references/rss/international.md)
- [Daily output template](references/output/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown daily news digest with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maximum 6 news items, at most 2 per topic, under 1500 Chinese characters; outputs an empty digest only when retrieval succeeds and no same-day verified events pass the evidence gate.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
