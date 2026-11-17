## Description:

Query-Skills helps agents search, inspect, and recommend OpenClaw and ClawHub skills across bilingual and multi-source queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find relevant OpenClaw skills, inspect skill details, discover popular or related skills, and get install commands from search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may include private project names, customer data, vulnerability details, or internal technology names and may be sent to ClawHub and an undisclosed mirror.

Mitigation: Use non-sensitive, generalized search terms and avoid confidential identifiers when running searches.

Risk: Mirror results may be displayed as verified even though the artifact does not verify them.

Mitigation: Treat verification flags on mirror-derived results as untrusted and confirm the skill publisher, source page, and package contents before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/query-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [CLI text and Markdown guidance with skill result lists, details, recommendations, source labels, and install commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include translated query text, source labels, quality scores, verification flags, and source URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json and SKILL.md list 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
