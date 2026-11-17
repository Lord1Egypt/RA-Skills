# MCP 本地证据检查

服务技能/插件推荐操作；配置、调用、进程运行与工具成功分开。

| 维度 | 当前 CLI 证据 | 状态边界 |
|---|---|---|
| config | 指定配置的 command/args 或 URL | 仅结构，不是连接测试 |
| startup | 未启动 MCP | unavailable，command 存在不证明成功 |
| permissions | 敏感字段名称及传输方式 | 待核验线索，不代表已泄漏 |
| schema | 未实时请求工具列表 | unavailable，缓存计数只用于估算 |
| usage | 可归因调用记录 | 调用不等于成功，无记录为 unavailable |
| consistency | 未逐客户端对比 | unavailable |

健康分仅对已知维度加权，展示局部分数及覆盖；存在未知时 partial，不称正常。
报告披露配置路径，不把 ZCode 配置称为所有客户端 MCP；读取失败不等于未安装。
凭据存在既不自动判泄漏，也不自动判安全。只输出字段名，不含值或前缀；核验实际权限、版本控制跟踪和日志暴露后再判断。
真实 initialize/list_tools/无副作用工具测试由执行 Agent 在授权范围内进行，不主动启动服务。
建议绑定具体失败维度；不输出“处理 0 个问题”。Firecrawl 配置存在不能称未安装，仍需区分 Skill 与 MCP。
