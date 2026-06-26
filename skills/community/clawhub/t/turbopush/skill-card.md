## Description: <br>
Multi-platform content publishing assistant for posting articles, image-text posts, and videos to 20+ platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyc1f](https://clawhub.ai/user/xueyc1f) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use TurboPush to prepare, configure, publish, and review multi-platform social content through the turbo-push MCP server. It helps agents select logged-in accounts, create or reuse content, gather platform-specific publishing settings, publish or save drafts, and inspect publishing records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content publicly through logged-in social accounts without requiring an explicit final confirmation in its instructions. <br>
Mitigation: Require the agent to show the final content, destination accounts, target platforms, and draft-versus-public-publish choice before any publish_article, publish_graph_text, or publish_video call. <br>
Risk: Publishing depends on a local TurboPush application, browser automation, and the turbo-push-mcp binary. <br>
Mitigation: Install only from trusted TurboPush sources and verify the local binary and application before connecting accounts or authorizing publication. <br>
Risk: Platform-specific required settings or desc syntax errors can block publication or cause incorrect publishing metadata. <br>
Mitigation: Call get_platform_setting_schema for the target platform and content type before publishing, validate required fields, and enforce the documented topic and mention syntax for image-text and video descriptions. <br>


## Reference(s): <br>
- [TurboPush ClawHub page](https://clawhub.ai/xueyc1f/turbopush) <br>
- [TurboPush MCP source URL listed by the artifact](https://github.com/xueyc/turbopush-mcp) <br>
- [TurboPush application URL listed by the artifact](https://github.com/xueyc/turbopush) <br>
- [TurboPush MCP releases URL listed by the artifact](https://github.com/xueyc/turbopush-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and MCP tool call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local TurboPush environment variables TURBO_PUSH_PORT and TURBO_PUSH_AUTH and the turbo-push-mcp binary.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
