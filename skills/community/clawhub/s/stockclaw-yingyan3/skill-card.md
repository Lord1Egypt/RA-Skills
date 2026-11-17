## Description:

This ClawHub skill helps an agent use OpenClaw stock endpoints to generate quantitative chart links, answer A-share market questions, run natural-language stock screens, query limit-up stocks, and monitor real-time trading signal changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woshixihongtu-cyber](https://clawhub.ai/user/woshixihongtu-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve stock charts, structured market snapshots, concise trend analysis, natural-language stock-screening results, daily limit-up lists, and real-time monitor signal updates through the Yingyan OpenClaw service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable OpenClaw and monitor API keys in a plaintext config.json file.

Mitigation: Install only in trusted workspaces, avoid committing or sharing populated config.json files, and rotate keys if exposure is suspected.

Risk: The skill instructs the agent to use system and user prompts returned by the remote stock service for market analysis.

Mitigation: Treat remote returned prompts as untrusted data; prefer local system instructions and parse only structured stock fields before producing analysis.

Risk: Stock charts, screens, and trend summaries may be interpreted as financial advice.

Mitigation: Present outputs as informational analysis, preserve uncertainty, and include that results are not investment advice when returning market conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woshixihongtu-cyber/skills/stockclaw-yingyan3)
- [Publisher profile](https://clawhub.ai/user/woshixihongtu-cyber)
- [OpenClaw API reference](artifact/reference.md)
- [OpenClaw examples](artifact/examples.md)
- [OpenAPI specification](artifact/openapi.json)
- [Yingyan OpenClaw service](https://yingyan.chatface.com/)
- [Yingyan OpenClaw demo](https://yingyan.chatface.com/web/openclaw_demo.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and structured text, including image links, stock tables, trend summaries, and connection status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied OpenClaw credentials; stock-screening results are capped at 20 rows by the referenced API.]

## Skill Version(s):

1.1.4 (source: ClawHub release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
