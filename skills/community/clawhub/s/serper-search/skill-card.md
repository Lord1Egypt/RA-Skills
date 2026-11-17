## Description:

Fetches real Google search or news results with links, snippets, knowledge graph data, and related questions via the Serper.dev API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samoppakiks](https://clawhub.ai/user/samoppakiks)

### License/Terms of Use:


## Use Case:

Developers and ClawHub agents use this skill to issue Google web or news searches through Serper.dev and receive structured results for retrieval, monitoring, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Serper.dev and Google-backed search infrastructure.

Mitigation: Avoid secrets, private customer data, credentials, and sensitive internal project names in queries.

Risk: The skill requires a Serper.dev API key.

Mitigation: Store the API key in environment or plugin configuration and avoid placing it in prompts, logs, or source files.

Risk: External service behavior and plugin dependencies can change over time.

Mitigation: Keep Clawdbot and dependencies updated and review Serper.dev behavior before using the skill in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samoppakiks/skills/serper-search)
- [Publisher profile](https://clawhub.ai/user/samoppakiks)
- [Serper.dev](https://serper.dev)

## Skill Output:

**Output Type(s):** [text, JSON, configuration]

**Output Format:** [Text content containing formatted JSON search or news results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Serper.dev API key and supports query, result count, and web/news search mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
