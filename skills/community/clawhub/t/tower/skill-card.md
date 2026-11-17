## Description:

Tower helps agents extract and summarize information from public Tower project and announcement pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to summarize public Tower announcements, count visible project task groups and statuses, and organize public document or resource links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for public Tower pages only; using it on private workspace or logged-in content may expose non-public information.

Mitigation: Use only publicly accessible Tower links unless a separate review approves private or authenticated content handling.

Risk: Dynamic Tower pages may not be fully rendered when parsed, which can lead to incomplete summaries or counts.

Mitigation: Wait for page rendering to complete and verify extracted task counts, timestamps, and document links against the visible page.

Risk: Repeated access to public Tower pages can create unnecessary traffic.

Mitigation: Apply rate limits and avoid repeated fetches of the same page.

## Reference(s):

- [Tower homepage](https://tower.im/)
- [ClawHub Tower skill page](https://clawhub.ai/codenova58/skills/tower)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on publicly accessible Tower pages and should include source links when available.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
