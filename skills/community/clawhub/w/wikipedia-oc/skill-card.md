## Description:

Searches, retrieves, and summarizes content from English Wikipedia using the `wikipedia` Python module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachmann-alexander](https://clawhub.ai/user/rachmann-alexander)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search English Wikipedia, retrieve a relevant page, and return concise structured information with attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves from English Wikipedia even when the user's question is in another language, so translated answers may miss local-language article details.

Mitigation: Disclose Wikipedia as the source, preserve factual accuracy during translation, and tell users that lookup was performed against English Wikipedia.

Risk: The `wikipedia` Python dependency is installed from PyPI and may change over time.

Mitigation: Install it in a virtual environment and pin a reviewed version before deployment.

Risk: Wikipedia content can be incomplete, rate-limited, or ambiguous for broad queries.

Mitigation: Prefer concise summaries, include the page URL, limit search candidates, and handle disambiguation or page-not-found errors explicitly.

## Reference(s):

- [wikipedia Python module](https://pypi.org/project/wikipedia/)
- [ClawHub skill page](https://clawhub.ai/rachmann-alexander/skills/wikipedia-oc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell code blocks; retrieved results are structured as title, summary, and URL fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses English Wikipedia for lookup and instructs agents to disclose Wikipedia as the source.]

## Skill Version(s):

0.1.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
