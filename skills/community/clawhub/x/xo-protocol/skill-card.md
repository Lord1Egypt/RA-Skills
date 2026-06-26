## Description: <br>
XO Protocol gives agents and applications user-authorized access to dating trust signals, including identity verification, compatibility scoring, reputation, profile context, and social signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pbjhsu](https://clawhub.ai/user/pbjhsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent builders use this skill to integrate XO Protocol's dating intelligence API, OAuth flow, SDK, and MCP tools into dating, trust-badge, compatibility, reputation, and scam-review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive dating-related trust, profile, and newsfeed data through user-authorized scopes. <br>
Mitigation: Request only the minimum OAuth scopes needed, avoid storing or logging raw profile and newsfeed data, and require user review before using the data for consequential decisions. <br>
Risk: API keys and OAuth access tokens are required for runtime use and could expose authorized data if mishandled. <br>
Mitigation: Store credentials in protected environment variables or a secret manager, rotate them when exposed, and do not embed real credentials in shared examples or agent prompts. <br>
Risk: Agents may overstate compatibility, reputation, or social-signal scores when summarizing dating trust information. <br>
Mitigation: Present scores as advisory signals, include confidence where available, and avoid automated blocking, ranking, or outreach decisions without human oversight. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pbjhsu/xo-protocol) <br>
- [XO Protocol landing page](https://xoxo.space/en/protocol) <br>
- [XO Protocol API docs](https://protocol.xoxo.space/protocol/docs) <br>
- [OpenAPI specification](openapi.yaml) <br>
- [SDK package metadata](sdk/package.json) <br>
- [MCP server example](examples/mcp-server.js) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, shell, JSON configuration examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XO Protocol API key and user-authorized OAuth access token; access should be limited to approved scopes.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
