## Description:

Anonymously fetches Weibo real-time hot search rankings without a Weibo account and saves the results as a Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazemace](https://clawhub.ai/user/kazemace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to collect the current Weibo hot search list without account credentials and generate a dated Markdown table for monitoring, reporting, or downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Chrome or Edge through CDP and may terminate browser debugging processes associated with its profile.

Mitigation: Run it with a dedicated throwaway browser profile and avoid using it on workstations that have other Chrome or Edge automation sessions.

Risk: The scanner reports that the skill may ask for login despite its anonymous-use positioning.

Mitigation: Do not log into a personal Weibo account through this skill; stop execution if a login prompt blocks collection.

Risk: The npx fallback can download and execute a runtime at use time.

Mitigation: Prefer a trusted preinstalled Bun runtime and avoid the unpinned npx fallback in controlled environments.

Risk: Collection depends on Weibo page structure and may fail or produce incomplete results after site changes.

Mitigation: Review generated Markdown for completeness and rerun or update selectors when the page no longer exposes expected hot search elements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kazemace/skills/weibo-hot-search-anonymous)
- [Weibo hot search page](https://weibo.com/newlogin?tabtype=search)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown file with a ranked table of hot search terms, heat values, labels, and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome, Chromium, or Microsoft Edge plus a Bun runtime; supports optional output path and browser profile settings.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
