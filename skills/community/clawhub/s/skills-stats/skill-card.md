## Description:

Query any ClawHub skill's statistics, including stars, downloads, current installs, all-time installs, comments, and versions, via curl and the public ClawHub API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:


## Use Case:

Developers and ClawHub users use this skill to inspect a skill's popularity metrics, compare multiple skill slugs, or search for skills by keyword without opening the ClawHub web UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples contain user-filled slug and search placeholders that are pasted into shell commands.

Mitigation: Use normal ClawHub slugs or URL-encoded search terms and avoid untrusted shell metacharacters in placeholder values.

Risk: The skill depends on public ClawHub API responses and local JSON parsing.

Mitigation: Review terminal output for missing or unexpected fields before relying on the reported popularity metrics.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tjefferson/skills/skills-stats)
- [ClawHub skill API endpoint](https://clawhub.ai/api/skill?slug={slug})
- [ClawHub search API endpoint](https://clawhub.ai/api/search?q=SEARCH_TERM)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces terminal commands that fetch public ClawHub API responses and summarize stats locally.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
