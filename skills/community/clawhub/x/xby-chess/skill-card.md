## Description:

Validates chess FEN strings and returns ASCII chessboard visualizations through the XiaoBenYang service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chess-focused agent users can use this skill to submit a FEN position and receive a readable ASCII board visualization. It is useful when an agent needs to inspect or present chess positions in text-only workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a project .env file in plaintext.

Mitigation: Use a controlled working directory, restrict file access, avoid sharing the .env file, and rotate the key if it is exposed.

Risk: FEN input and the API key are sent to a configurable remote XiaoBenYang MCP service.

Mitigation: Install only if the publisher and XiaoBenYang service are trusted, and avoid using uncontrolled environments for requests.

Risk: The security verdict is suspicious because the skill requires and persists an unrelated API key for a chess FEN visualizer.

Mitigation: Review the skill and network destination before deployment, and approve it only for environments where that dependency is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-chess)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration guidance]

**Output Format:** [Text or Markdown summary of a JSON service response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FEN string and a XiaoBenYang API key; the raw service response is returned for agent summarization.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
