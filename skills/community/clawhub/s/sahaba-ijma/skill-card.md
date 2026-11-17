## Description:

Searches Dorar Al-Sunniyah for Sahaba consensus and sayings, returning source, narrator, scholar, page or number, and authenticity status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m7madash](https://clawhub.ai/user/m7madash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to search documented Sahaba consensus and related reports from Dorar Al-Sunniyah, then inspect returned source and authenticity details before relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted search text can lead to local code execution during query encoding.

Mitigation: Install only after the query-encoding bug is fixed; pass query text to Python as data, such as through an argument, or use curl data-urlencode.

Risk: Search terms are sent to dorar.net.

Mitigation: Avoid sensitive or untrusted query strings unless the user accepts that the text will be shared with the external service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m7madash/skills/sahaba-ijma)
- [Dorar API endpoint](https://dorar.net/dorar_api.json?skey=QUERY&callback=?)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with shell command usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include report text, narrator, hadith scholar, source, page or number, grading, and a Dorar search URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
