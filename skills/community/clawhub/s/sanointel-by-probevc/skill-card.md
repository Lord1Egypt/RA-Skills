## Description:

中国医疗产业情报 agent skill for querying Chinese healthcare and biotech company intelligence, financing events, clinical trials, patents, sector trends, daily digests, and A/HK/US market data through the Sano Intel API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanjj-cmd](https://clawhub.ai/user/yanjj-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to answer Chinese healthcare industry research questions about companies, financing, clinical trials, patents, sector momentum, daily intelligence, and listed-market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to send an API token and healthcare or investment research queries over plaintext HTTP.

Mitigation: Use the skill only when comfortable sharing those credentials and queries with the listed service; prefer encrypted transport if the provider makes it available.

Risk: Persisting the API token in a shell profile can expose the token to other local processes, backups, or shared environments.

Mitigation: Use a temporary environment variable or secure secret store, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanjj-cmd/skills/sanointel-by-probevc)
- [Sano Intel API base](http://47.102.196.1:8081)
- [Sano Intel token application](http://47.102.196.1:5005/apply)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline curl commands and concise Chinese summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SANO_TOKEN API key; API responses depend on the external Sano Intel service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
