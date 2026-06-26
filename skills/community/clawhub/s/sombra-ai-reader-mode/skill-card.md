## Description: <br>
Persistent reader mode for AI. Save web pages, organise into collections, distil to dense context, and serve it all through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dazld](https://clawhub.ai/user/dazld) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Sombra to build a persistent research library of saved web pages, notes, and project collections. The skill helps agents retrieve, search, and distil that library into focused MCP context for research and coding sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to a persistent Sombra library, so saved pages, notes, and distilled collection context may be stored and reused across sessions. <br>
Mitigation: Avoid saving credentials, regulated data, or sensitive private material unless that storage and reuse is acceptable for the user's environment. <br>
Risk: The MCP setup can use a bearer token or personal access token, which grants access to the user's Sombra library. <br>
Mitigation: Treat the Sombra token as a secret, prefer OAuth or safer secret storage when available, and install only if the user trusts Sombra and the sombra-mcp package. <br>
Risk: Agent actions can create, update, archive, restore, and move library items and collections. <br>
Mitigation: Review agent write and delete actions for important collections before relying on the resulting library state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dazld/sombra-ai-reader-mode) <br>
- [Sombra](https://sombra.so) <br>
- [Sombra MCP setup docs](https://sombra.so/mcp) <br>
- [What is Sombra?](https://sombra.so/blog/what-is-sombra) <br>
- [Why context engineering matters](https://sombra.so/blog/context-failures) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and MCP tool descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and a Sombra MCP token or OAuth-capable MCP client.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
