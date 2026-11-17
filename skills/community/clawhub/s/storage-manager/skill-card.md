## Description:

Storage Manager helps agents manage Feishu Bitable-backed inventory records with item storage, smart location matching, location photo labels, item lookup, and location updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruoruochen](https://clawhub.ai/user/ruoruochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to record personal or household item locations, attach item and location images, search stored items, and update storage locations through Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes hardcoded Feishu credentials and fixed table identifiers.

Mitigation: Remove bundled credentials and table IDs, rotate the exposed Feishu secret, and require FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BITABLE_TOKEN, and FEISHU_TABLE_ID to be explicitly configured before use.

Risk: If default Feishu values remain, the skill can read, write, or upload to a preset Feishu table.

Mitigation: Verify the tool fails closed without user-owned Feishu configuration and test it only against an isolated Feishu app and table.

## Reference(s):

- [ClawHub Storage Manager Skill Page](https://clawhub.ai/ruoruochen/skills/storage-manager)
- [Artifact README](README.md)
- [Feishu Tenant Access Token API Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Feishu Bitable read, write, and upload actions when configured with Feishu credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
