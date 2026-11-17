## Description:

Semantic Scholar Search helps agents find academic papers and related metadata through Semantic Scholar while preserving compatibility with the older scholar entry point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search Semantic Scholar for papers or authors and review titles, authors, abstracts, citation counts, venues, years, and source URLs. It is also maintained as a compatibility path for older scholar-style calls while recommending the newer search scholar entry point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency metadata declares the Python requests package as an npm dependency, which may fail during installation or resolve an unintended package.

Mitigation: Review or correct dependency metadata before installing, and ensure requests is provided through an appropriate Python dependency mechanism.

Risk: Search terms are sent to Semantic Scholar.

Mitigation: Avoid submitting sensitive or confidential research queries unless that external disclosure is acceptable.

Risk: The visible skill instructions are primarily in Chinese.

Mitigation: Confirm that operators and reviewers can understand the instructions or provide an approved translation before deployment.

## Reference(s):

- [Semantic Scholar API](https://api.semanticscholar.org/)
- [Semantic Scholar Graph API v1](https://api.semanticscholar.org/graph/v1)
- [ClawHub skill page](https://clawhub.ai/jirboy/skills/semantic-scholar-search)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text search results with paper or author metadata and error messages when requests fail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search terms are sent to Semantic Scholar; paper output is limited to 10 results by the script.]

## Skill Version(s):

1.0.0 (source: package.json and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
