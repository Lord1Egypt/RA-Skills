## Description:

配套搭子路书（Trek）微信旅行小程序的自动化 Skill，主要面向 WorkBuddy，也兼容 Codex、Claude、OpenClaw、Hermes 等 Agent。通过认证的远程 MCP 研究国内外目的地、读取或修改行程，并把日程、地点、预订、住宿、费用、清单、待办、附件和协作提案安全同步回小程序。

This skill is ready for commercial/non-commercial use.

## Publisher:

[super21-bat](https://clawhub.ai/user/super21-bat)

### License/Terms of Use:

MIT-0

## Use Case:

面向希望使用 WorkBuddy 或其他兼容 Agent 的旅行者，用于研究目的地、维护 Trek 行程，并整理预订、住宿、费用、清单和待办。Agent 可在用户授权后通过远程 MCP 或 CLI 同步结构化行程数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation, updates, or synchronization can replace agent instructions from changing remote sources.

Mitigation: Review and pin installation sources before global installation, updates, or cross-agent synchronization.

Risk: Direct MCP calls can bypass the CLI batch safeguards for high-impact changes.

Mitigation: Require explicit user approval for destructive, financial, and membership changes, including direct calls.

Risk: A Trek Agent Key or an unintended attachment could expose account access or private travel documents.

Mitigation: Use a separate revocable key stored securely, never echo credentials, and upload only intended documents.

## Reference(s):

- [Trek skill release](https://clawhub.ai/super21-bat/skills/trek-agent-control)
- [Configuration guide](references/configuration.md)
- [Planning and synchronization workflows](references/workflows.md)
- [Field guide](references/field-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Text and Markdown, API Calls, Shell commands, Configuration, Files]

**Output Format:** [Text or Markdown guidance, structured MCP operations, CLI commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The resulting itinerary changes and supporting outputs depend on the user's request and connected Trek tools.]

## Skill Version(s):

1.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
