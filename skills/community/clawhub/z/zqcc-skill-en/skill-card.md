## Description:

zqcc Qichacha Relay helps agents query Qichacha-backed Chinese enterprise data through an authenticated MCP endpoint and natural-language Chat API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shijingyu](https://clawhub.ai/user/shijingyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for company due diligence, risk checks, registration lookups, intellectual property searches, executive research, and related Chinese enterprise-data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company, executive, and related query data to the zqcc service and successful calls may consume paid credits.

Mitigation: Use the skill only for intended zqcc workflows, review data before sending it, and check the zqcc console for balance and billing details.

Risk: The helper script can send the paid ZQCC_APP_KEY to a different destination if ZQCC_BASE_URL is changed.

Mitigation: Leave ZQCC_BASE_URL unset unless the destination is fully trusted, and keep ZQCC_APP_KEY out of prompts, logs, source files, screenshots, and URLs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/shijingyu/skills/zqcc-skill-en)
- [zqcc service homepage](https://zqcc.mkstone.club)
- [zqcc Public API Reference](references/api.md)
- [zqcc Tool Catalog](references/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP JSON-RPC requests, Chat API prompts, client configuration, and guidance for handling enterprise-data results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
