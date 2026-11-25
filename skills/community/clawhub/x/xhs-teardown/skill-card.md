## Description:

Read-only Xiaohongshu skill that searches public notes, retrieves note details and comments, and lists creator posts and engagement metrics as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, and analysts use this skill to search public Xiaohongshu notes, review individual posts and comments, and inspect creator activity for topic research, competitor monitoring, KOL screening, and feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and note or creator links are sent to a third-party API; the security assessment has medium confidence and partial code coverage.

Mitigation: Use queries and links suitable for sharing with the API provider, and review the skill before execution because some behavior was not fully assessed.

## Reference(s):

- [GuaiKei API service](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON containing public Xiaohongshu note, comment, or creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; result counts depend on the API plan.]

## Skill Version(s):

1.2.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
