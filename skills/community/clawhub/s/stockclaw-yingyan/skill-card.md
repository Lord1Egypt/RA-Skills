## Description:

stockClaw-yingyan helps agents use OpenClaw stock APIs to return quantitative chart links, A-share market analysis, natural-language stock screening results, limit-up stock lists, and WebSocket monitor signal updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woshixihongtu-cyber](https://clawhub.ai/user/woshixihongtu-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and developers use this skill to connect an agent to Yingyan/OpenClaw stock endpoints for chart generation, market Q&A, natural-language stock screening, limit-up stock lists, and real-time monitor signals. It requires user-provided OpenClaw credentials for HTTP requests and a separate monitor key for WebSocket subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are stored in local config.json and may be exposed if the file is committed, uploaded, or shared.

Mitigation: Use limited or disposable keys where possible, keep config.json private after credentials are added, and avoid sharing logs that include keys or full WebSocket URLs.

Risk: Some market analysis prompt content may be supplied by the remote service.

Mitigation: Review the skill before installation and independently verify stock analysis; present outputs as non-advisory analysis rather than investment instructions.

Risk: WebSocket monitoring uses a separate monitor API key that can be confused with the HTTP OpenClaw key.

Mitigation: Keep HTTP and monitor credentials separate, validate the intended key before connecting, and avoid exposing full monitor URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/woshixihongtu-cyber/skills/stockclaw-yingyan)
- [API Reference](artifact/reference.md)
- [Examples](artifact/examples.md)
- [OpenAPI Specification](artifact/openapi.json)
- [Yingyan OpenClaw Service](https://yingyan.chatface.com/)
- [OpenClaw Demo Page](https://yingyan.chatface.com/web/openclaw_demo.html)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured JSON-derived text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image URLs or rendered Markdown, stock tables, market analysis sections, credential setup prompts, and real-time signal summaries.]

## Skill Version(s):

1.1.4 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
