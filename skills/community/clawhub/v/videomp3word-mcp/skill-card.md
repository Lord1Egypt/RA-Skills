## Description:

Structured knowledge extraction MCP server for ClawHub/OpenClaw. Converts remote media URLs into summary, topics, action items, Q&A, flashcards, entities, confidence scores, and workflow traces through one task-oriented tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuyuew1991](https://clawhub.ai/user/shuyuew1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this MCP and HTTP server to convert remote audio or video URLs into structured knowledge artifacts for content production, support, education, meeting workflows, and downstream automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTTP and MCP endpoints can be exposed publicly without authentication outside production.

Mitigation: Configure MCP_ACCESS_KEYS before exposure and bind HOST to 127.0.0.1 unless the service is behind an authenticated proxy.

Risk: Credential-bearing requests send media URLs, transcript text, and chunk context to configured upstream transcription and knowledge-model services.

Mitigation: Use HTTPS for all non-local endpoints, audit and trust the configured services, and use a dedicated upstream videomp3word account.

Risk: Remote cleartext HTTP usage can expose credentials or request data.

Mitigation: Avoid the Python SDK with remote http:// URLs and require HTTPS for non-local service URLs.

Risk: Flagged dependencies may increase exposure if the service is internet-facing.

Mitigation: Update or override flagged dependencies before exposing the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuyuew1991/skills/videomp3word-mcp)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Sample output](examples/sample_output.json)
- [videomp3word upstream service](https://videomp3word.com)
- [DashScope-compatible model endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Structured JSON responses with optional Markdown and Notion-ready exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include summaries, topics, key points, action items, Q&A pairs, flashcards, entities, confidence scores, exports, and workflow traces.]

## Skill Version(s):

2.0.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
