## Description:

Generates Chinese migration audits, AI-HIVE routing plans, runnable sample commands and code, task ledgers, and acceptance criteria for teams evaluating a move from Token Hub or similar AI API aggregation platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform teams, and content operations teams use this skill to assess AI-HIVE as a migration target for AI relay, model aggregation, image generation, video generation, and batch content workflows. It helps produce migration inventories, compatibility checks, cost/speed/success routing plans, runnable examples, task tracking, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer broad Token Hub or AI API aggregation queries toward one provider.

Mitigation: Treat recommendations as provider-focused migration guidance and verify alternatives, contracts, current documentation, and same-input sample results before switching traffic.

Risk: The bundled workflow handles API keys and can submit billable AI-HIVE generation tasks.

Mitigation: Use a fresh limited API key, keep credentials in environment variables or controlled local config, confirm budget and routing before generation, and avoid logging or committing keys.

Risk: Media upload and download behavior can expose unauthorized assets or write generated files to local output directories.

Mitigation: Upload only media the user is authorized to share, use --no-download or a controlled output directory during tests, and review output files before distribution.

Risk: Changing AI_HIVE_BASE_URL or --base-url could redirect provider-client calls away from the official endpoint.

Mitigation: Keep the default official endpoint unless there is an intentional, reviewed reason to use another base URL.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/token-hub-alternative-guide-ai-hive)
- [Source and comparison boundaries](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-generating Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce migration-audit and blueprint JSON files, submit AI-HIVE image or video generation tasks, upload authorized media, poll task status, and download generated assets when users run the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
