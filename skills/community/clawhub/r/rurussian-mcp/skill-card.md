## Description: <br>
RuRussian MCP connects OpenClaw or MCP-compatible agents to RuRussian tutoring tools for Russian vocabulary, grammar analysis, reading practice, translation, learner memory, and subscription activation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuyuew1991](https://clawhub.ai/user/shuyuew1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to RuRussian tutoring workflows for vocabulary lookup, sentence analysis, reading practice, translation, learner progress tracking, and account activation. It is intended for Russian-learning assistants that can call MCP tools and manage user-approved subscription flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a RuRussian API key and can send learner text or email to the RuRussian backend. <br>
Mitigation: Use a dedicated API key, avoid exposing raw credentials in chat output, and confirm that users understand what learner data is being sent. <br>
Risk: The skill can create hosted checkout sessions for subscription activation. <br>
Mitigation: Do not grant unattended payment authority; require explicit user approval and confirm the plan and account before checkout. <br>
Risk: The skill can keep local learner history in a JSON memory file. <br>
Mitigation: Delete, relocate, or protect the memory file when learner history should not persist on the host. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuyuew1991/rurussian-mcp) <br>
- [RuRussian MCP Homepage](https://github.com/shuyueW1991/rurussian-mcp) <br>
- [OpenClaw Integration Guide](docs/INTEGRATION.md) <br>
- [Tool Examples](examples/tool_examples.json) <br>
- [OpenClaw Configuration Example](examples/openclaw_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON, shell commands, text] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and structured MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool outputs may include tutoring content, learner profile state, checkout session information, and API-key status previews.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and pyproject.toml; SKILL.md frontmatter says 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
