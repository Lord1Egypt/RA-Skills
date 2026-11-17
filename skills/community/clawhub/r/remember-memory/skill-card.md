## Description:

Provides a category-based persistent memory service that lets Claude store, retrieve, and delete memory data across chat sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to add, retrieve, and delete categorized memories through a XiaoBenYang-backed persistent memory service. It is intended for workflows that need remembered context across Claude chat sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory contents and retrieval requests are sent to a configurable remote XiaoBenYang endpoint.

Mitigation: Use the skill only when the XiaoBenYang service is trusted, and avoid storing sensitive secrets or private data as memories.

Risk: The API key is saved in plaintext in a local .env file.

Mitigation: Use a limited API key, keep .env out of shared artifacts, and review local file permissions before use.

Risk: Delete-category and wildcard operations can remove broad sets of memories.

Mitigation: Confirm category, wildcard, and partial-match delete requests with the user before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/remember-memory)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, API calls]

**Output Format:** [Markdown or structured text summarizing JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided XiaoBenYang API key; tool calls may return raw JSON response data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
