## Description:

Feishu Card helps agents send international Feishu interactive card messages with titles, Markdown content, and color themes using Feishu schema 2.0 and double JSON serialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to compose and send rich Feishu interactive card messages to a user or chat, including Markdown bodies, color-themed headers, and troubleshooting guidance for schema 2.0 rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local Feishu app secret and sends messages through the configured Feishu app.

Mitigation: Install only when Feishu message sending is intended, verify the app_id and recipients match the tenant, and prefer managed message tooling or a secret manager to avoid exposing secrets in shell commands or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/skills/xiaolongxia-feishu-card)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Send Message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu interactive message payload guidance and may execute a helper script that sends messages through the configured Feishu app.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
