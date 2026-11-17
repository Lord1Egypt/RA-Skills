## Description:

Query and manage Sanity CMS content via GROQ queries and the Sanity HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwhite-oss](https://clawhub.ai/user/dwhite-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to query Sanity datasets, inspect GROQ results, and prepare Sanity Content Lake create, update, publish, delete, and asset-management operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes direct create, update, publish, and delete operations for CMS content without explicit confirmation or rollback safeguards.

Mitigation: Require explicit confirmation before mutation operations and review planned changes before applying them.

Risk: Using an Editor token against a production dataset can modify or delete live content.

Mitigation: Use least-privilege Sanity tokens, prefer Viewer tokens for read-only work, and test changes against non-production datasets before using production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwhite-oss/skills/sanity)
- [Publisher profile](https://clawhub.ai/user/dwhite-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, and GROQ code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Sanity environment variable guidance and HTTP API request examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
