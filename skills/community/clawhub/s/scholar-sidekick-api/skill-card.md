## Description:

Resolve scholarly identifiers into formatted citations, bibliography exports, and retraction, open-access, or citation-verification checks through Scholar Sidekick's documented REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlava](https://clawhub.ai/user/mlava)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, librarians, and developers use this skill to resolve known scholarly identifiers into citations or bibliography exports and to check retraction, open-access, and citation-verification status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation references or text sent to the REST API may include confidential, unpublished, or proprietary research information.

Mitigation: Use the REST examples only for references approved to be sent to scholar-sidekick.com, and avoid sensitive citation text unless there is approval.

Risk: The optional MCP command runs unpinned third-party npm code on the user's machine.

Mitigation: Prefer the REST workflow for zero-install use; if MCP is needed, use a pinned reviewed package version and avoid exposing sensitive environment variables.

Risk: Failed API calls or uncertain verification results can mislead users if the agent fabricates fallback citation, retraction, open-access, or match status.

Mitigation: Report failed or ambiguous API responses as returned, and do not invent citations, verdicts, or status values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlava/skills/scholar-sidekick-api)
- [Publisher profile](https://clawhub.ai/user/mlava)
- [Scholar Sidekick homepage](https://scholar-sidekick.com)
- [Agent surfaces index](https://scholar-sidekick.com/llms.txt)
- [REST and MCP guide](https://scholar-sidekick.com/AGENTS.md)
- [OpenAPI specification](https://scholar-sidekick.com/openapi/openapi.yml)
- [RapidAPI listing](https://rapidapi.com/scholar-sidekick-scholar-sidekick-api/api/scholar-sidekick)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples plus API text, JSON, and bibliography file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; anonymous REST use is rate limited, with optional RapidAPI use for higher volume.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
