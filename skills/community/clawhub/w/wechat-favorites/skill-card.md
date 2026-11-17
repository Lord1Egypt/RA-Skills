## Description:

微信收藏夹导出、智能分类与知识库管理。支持从解析后的 favorite.db 导出收藏记录、自动归纳分类（从用户内容发现自然类别）、LLM 智能增强（可选）、批量导入 IMA 知识库（可选）、多平台导出（Obsidian/Notion，可选）、增量分类。核心功能支持离线使用，网络功能默认关闭。

This skill is ready for commercial/non-commercial use.

## Publisher:

[geosun](https://clawhub.ai/user/geosun)

### License/Terms of Use:

MIT

## Use Case:

Developers and individual knowledge workers use this skill to export parsed WeChat Favorites records, classify them locally or with optional LLM assistance, and organize the results into CSV, Obsidian, Notion, or IMA knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled decryption script can produce plaintext from encrypted WeChat databases beyond the intended favorite.db workflow.

Mitigation: Run decrypt_db.py only when you intend to decrypt the selected database, review its target paths before execution, and protect decrypted outputs and exported CSV files.

Risk: Optional LLM, IMA, and Notion workflows can send favorite titles, summaries, URLs, or credentials to external services.

Mitigation: Use SAFE_MODE for local-only workflows and enable each network integration only after confirming the data and credentials it will transmit.

## Reference(s):

- [Classification algorithm](references/classification.md)
- [favorite.db schema](references/schema.md)
- [ClawHub skill page](https://clawhub.ai/geosun/skills/wechat-favorites)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; scripts produce CSV, JSON, Markdown, and external knowledge-base entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline export and keyword classification are supported; optional LLM, IMA, and Notion workflows require user-provided credentials and network access.]

## Skill Version(s):

1.2.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
