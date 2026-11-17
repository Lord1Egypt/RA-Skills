# templates/ 输出资源清单

生成资产时的填充模板，全部含占位符，按需复制后替换 `{{...}}` 占位内容。模板不得直接提交——占位符必须全部替换或改为 `${VAR}` 凭证占位。

> 注：本目录按平台两级目录约束与开放平台技能规范命名（原 assets/ 已更名 templates/）；生成的技能包内，产品自带模板同样放 templates/ 且文件直接平铺、不再嵌套子目录。

| 文件 | 用途 | 使用方式 | 对应任务 |
|------|------|---------|---------|
| skill-SKILL-template.md | 技能 SKILL.md 骨架 | 复制→替换占位→对照 D1 字段表核对 | D1-02 |
| expert-plugin.json-template.json | 单专家 plugin.json 骨架 | 复制→替换占位→对照 D3 字段表核对 | D3-02 |
| team-plugin.json-template.json | 专家团 plugin.json 骨架 | 复制→替换占位（含 teamInfo/members） | D4-02 |
| connector-meta.json-template.json | 连接器元信息骨架 | 复制→替换占位 | D2-02 |
| mcp.json-template.json | MCP 接入配置骨架（含远程/stdio 两形态） | 二选一保留→替换 url/command | D2-03 |
| cli.json-template.json | CLI 接入配置骨架 | 替换各平台命令 | D2-03 |
| buddy-app-config-checklist.md | Buddy 应用五模块配置清单 | 填充后供用户在开放平台网页逐项粘贴 | D5-01~03 |
| buddy_oauth_callback_local.py | Buddy 应用 OAuth 回调端点参考实现（本地调试版，Python 标准库零依赖） | 复制到本地→配置 WB_* 环境变量→python 直接运行 | D5-01 |
| buddy_oauth_callback_scf.py | Buddy 应用 OAuth 回调端点参考实现（腾讯云函数 SCF 版） | 全量粘贴到 SCF 事件函数→配 WB_* 环境变量→建 API 网关触发器 | D5-01 |

安全规则：模板中的 `${VAR}` 为凭证占位符，保留并在提交指引中说明由用户填写；`{{...}}` 为内容占位符，生成时必须替换。任何情况下不得写入真实 Token。
