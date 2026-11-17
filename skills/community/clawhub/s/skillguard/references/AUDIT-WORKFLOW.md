# 审计工作流

## 1. 收集范围

优先提交 `SKILL.md`，再提交它直接引用的脚本、配置与关键 references。API 只读取请求体，
`sourceUrl` 仅作为来源元数据保存，平台不会替你下载 URL 内容。

提交 JSON 可包含：

| 字段 | 约束 |
|---|---|
| `skillName` | 可选，最多 180 字符 |
| `skillMd` | 可选，最多 16000 字符 |
| `content` | 可选，最多 16000 字符 |
| `sourceUrl` | 可选，HTTP/HTTPS URL，最多 2048 字符 |
| `files` | 可选，最多 80 项 |
| `files[].path` | 使用 `files` 时必填，最多 180 字符 |
| `files[].content` | 可选，最多 16000 字符 |

`files` 内容合计不得超过 5 MB。必须至少提供有实际内容的审计输入。

## 2. 提交前脱敏

删除或替换 API 密钥、令牌、Cookie、私钥、数据库口令、个人信息和私有仓库凭据。不要读取
`.env`、密钥链或用户主目录中的无关文件来扩大审计范围。

## 3. 解读结果

- `pass`：结果完整且没有阻断风险时，才可继续后续自动化。
- `review`：暂停自动安装，向用户展示需要人工判断的发现项。
- `block`：停止安装或启用，说明关键风险和修复建议。

检查 `score`、`riskLevel`、`summary`、`findings`、`nextActions` 以及
`evaluationSource`。响应字段缺失、内容截断或无法解析时按 `block` 等级处理并失败关闭，
不得把“未检查到”解释为“安全”。
