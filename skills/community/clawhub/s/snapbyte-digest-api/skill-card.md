## Description:

Fetch personalized developer news digests from Snapbyte External API with API-key auth. Use for Hacker News digest, Reddit digest, Lobsters digest, and DEV.to digest workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onatm](https://clawhub.ai/user/onatm)

### License/Terms of Use:


## Use Case:

Developers use this skill to fetch Snapbyte digest configurations, latest digests, digest history, individual digests, and digest items, then present the results as Markdown or raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send SNAPBYTE_API_KEY to a non-default endpoint when SNAPBYTE_BASE_URL is set.

Mitigation: Use the default https://api.snapbyte.dev endpoint unless you fully control the override, and review environment configuration before running the skill.

Risk: The quickstart cron example creates persistent scheduled use of the configured API key.

Mitigation: Review the cron command, destination channel, session isolation, and schedule before enabling it; disable the job when routine digest delivery is no longer needed.

## Reference(s):

- [Snapbyte Digest API Quickstart](references/quickstart.md)
- [Snapbyte API Documentation](https://api.snapbyte.dev/docs)
- [Snapbyte API Base URL](https://api.snapbyte.dev)
- [ClawHub Skill Page](https://clawhub.ai/onatm/skills/snapbyte-digest-api)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown by default, with optional raw JSON payloads and inline shell or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SNAPBYTE_API_KEY; supports optional SNAPBYTE_BASE_URL override.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
