## Description:

Zeelin Social Watch monitors social media sentiment, trending events, platform rankings, and account data through the GSData open platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thu-nmrc](https://clawhub.ai/user/thu-nmrc)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to query GSData-backed social media monitoring data, including public sentiment searches, hot events, platform rankings, account metrics, and related NLP endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use GSData credentials to make broad API calls, including remote state-changing account and warning-rule actions.

Mitigation: Use only an intended GSData account, run dry-run checks before new requests, and require explicit user confirmation plus the write-enable flag before state-changing actions.

Risk: The default GSData endpoint is plaintext HTTP.

Mitigation: Prefer an HTTPS GSDATA_BASE_URL when GSData supports it and review network exposure before installation.

Risk: The raw command can call arbitrary GSData routes.

Mitigation: Avoid raw calls unless the endpoint and parameters are understood and approved for the task.

Risk: Social media searches can return large JSON payloads.

Mitigation: Use small page sizes, paginate deliberately, and summarize key fields before returning results to users.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thu-nmrc/skills/zeelin-social-watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown summaries with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GSData credentials; large result sets should be paginated and summarized.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
