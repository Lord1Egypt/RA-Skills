## Description: <br>
微信收藏夹导出、智能分类与知识库管理。支持从解析后的 favorite.db 导出收藏记录、自动归纳分类（从用户内容发现自然类别）、LLM 智能增强（可选）、批量导入 IMA 知识库（可选）、多平台导出（Obsidian/Notion，可选）、增量分类。核心功能支持离线使用，网络功能默认关闭。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geosun](https://clawhub.ai/user/geosun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and knowledge workers use this skill to export WeChat favorites from a parsed favorite.db, classify saved articles, and organize the results into local files or external knowledge-base destinations. Optional workflows support LLM-assisted category discovery, incremental classification, Obsidian Markdown export, Notion export, and IMA import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can locate WeChat database storage, consume memory-extracted database keys, decrypt local WeChat databases, and persist decrypted copies. <br>
Mitigation: Prefer supplying an explicit already-parsed favorite.db, avoid running decrypt_db.py unless broad local decryption is intended, and review generated local files before reuse. <br>
Risk: Optional LLM, Notion, and IMA workflows can send favorite metadata, article titles, summaries, URLs, or import payloads to external services. <br>
Mitigation: Use SAFE_MODE or offline workflows for local-only processing, enable network integrations only after reviewing payloads, and provide API credentials only for the services you intend to use. <br>
Risk: The release is security-scanner flagged as suspicious because bulk decryption behavior is under-disclosed relative to the stated WeChat favorites purpose. <br>
Mitigation: Treat the skill as sensitive tooling, run it in a controlled local workspace, and inspect the decryption and export commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geosun/wechat-favorites) <br>
- [Release changelog](CHANGELOG.md) <br>
- [Classification algorithm reference](references/classification.md) <br>
- [favorite.db schema reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with bash commands and configuration examples; companion scripts can produce CSV, JSON, and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional integrations require user-supplied credentials and can send selected favorite metadata to LLM, Notion, or IMA services.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, SKILL.md frontmatter, and CHANGELOG.md; released 2026-06-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
