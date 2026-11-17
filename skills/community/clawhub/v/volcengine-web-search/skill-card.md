## Description:

Uses the Volcengine web_search.py script to search public web pages for a clear query and return up to five result summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-wm](https://clawhub.ai/user/warm-wm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to answer web-search questions by running the bundled Volcengine search script and organizing the returned summaries without adding unsupported content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Volcengine and may expose confidential text, secrets, or private internal content if users include them in a query.

Mitigation: Use only non-confidential search queries and avoid submitting secrets or private internal content.

Risk: The skill authenticates with Volcengine credentials or VeFaaS IAM temporary credentials from the agent environment.

Mitigation: Use scoped credentials where possible and prefer tool-specific environment variables for this search workflow.

Risk: Returned search summaries may be incomplete or fail with an error response.

Mitigation: Base the final answer only on returned summaries, report failures clearly, and avoid adding unsupported claims.

## Reference(s):

- [Volcengine Web Search Documentation](https://www.volcengine.com/docs/85508/1650263)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with an inline shell command and console text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 5 summary items from Volcengine web search results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
