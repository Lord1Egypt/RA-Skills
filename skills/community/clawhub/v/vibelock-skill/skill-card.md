## Description:

VibeLock guides AI developers through code protection, packaging, licensing, distribution, VibeLock platform API integration, and attack/defense testing using a conversation-driven workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandleeai](https://clawhub.ai/user/pandleeai)

### License/Terms of Use:

MIT

## Use Case:

Developers and small software teams use this skill to choose and execute code obfuscation, packaging, license activation, heartbeat verification, telemetry, and marketplace setup workflows for commercializing AI-built software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags automatic self-update behavior as unsafe.

Mitigation: Disable or remove automatic self-update instructions and require users to review update sources before replacing skill files.

Risk: The security evidence flags persistent reuse of API tokens.

Mitigation: Store API tokens in a secret manager or protected local configuration, keep them out of source control and client packages, and rotate them if exposure is suspected.

Risk: The security evidence flags broad activation and high-impact merchant API actions.

Mitigation: Require explicit user confirmation before every write or delete API call, especially product, package, license, tier, feature, SKU, and telemetry schema changes.

Risk: The security evidence flags telemetry and report payload review as necessary.

Mitigation: Ask for consent before adding telemetry, inspect payload fields before sending data, and avoid collecting secrets, source code, or unnecessary personal data.

## Reference(s):

- [ClawHub VibeLock Skill Page](https://clawhub.ai/pandleeai/skills/vibelock-skill)
- [Server-Resolved GitHub Provenance](https://github.com/PandLeeAI/VibeLock-Skill)
- [VibeLock Product Website](https://lock.pandlee.cn/)
- [VibeLock Merchant Console and API Base](https://lock.pandlee.cn:8088)
- [VibeLock Skill Operation Guide](https://my.feishu.cn/docx/N2wtdQ0Xuo2G0XxvztFc2Y7KnRh?from=from_copylink)
- [VibeLock OpenAPI Documentation](https://my.feishu.cn/docx/PSBsdct5wong8txDuO6c94mRnVc?from=from_copylink)
- [Node.js Single Executable Applications](https://nodejs.org/api/single-executable-applications.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, JSON configuration examples, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation-only guidance; credential handling, browser operations, telemetry payloads, and merchant API write or delete actions require explicit user review.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; bundled VibeLock prompt version: 2.5.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
