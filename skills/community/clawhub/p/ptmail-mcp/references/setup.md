# 连接 PTMail 邮箱聚合 的本地 MCP

本仓库提供 Skill 文档及配置示例，运行时由官方安装包另行提供。安装 Skill 不会自动安装或连接产品。

1. 从[产品官网](https://ptmail.qique.cn/)安装支持 MCP 的 Windows 客户端，再下载[官方 MCP 包](https://res.qique.cn/system/skill/ptmail-mcp-453cd07d1045.zip)，解压到用户选定的运行目录；保留官方包内的脚本与其他文件。不要覆盖此仓库安装的文档目录。
2. 使用 Windows 10/11，Node.js 22+ recommended，以及已运行并登录的产品客户端。不把 Windows 客户端的本地服务视为云端或其他系统上的服务。
3. 参考 [mcp.example.json](../examples/mcp.example.json)，将所有 REPLACE_WITH 占位符替换为自己的官方运行目录，再导入支持 stdio MCP 的 AI 软件。示例不是可直接运行的配置；无需在配置中输入产品登录令牌。
4. 如安装 Cursor 插件，将变量 PTMAIL_RUNTIME_DIR 设置为包含 scripts/ptmail-mcp.js 的官方包根目录。变量只保存本机路径，不放入凭据。
5. 重启对应 MCP 服务，先用 tools/list 和 ptmail_session 做只读检查。工具及权限以当前客户端实际返回为准；连接未验证时不声称可用。

客户端会话文件和安装后的配对/凭据文件仅留在本机，不上传到 GitHub、不发给 AI 对话。修改/删除/发送等业务动作必须按 SKILL.md 的授权与确认要求执行。产品官网是说明和下载页面，不是远程 MCP endpoint。

升级时从官网重新取得匹配的官方包，并核对版本与发布哈希；不要混用缓存旧包。卸载先按产品说明断开连接，再移除 AI 软件 MCP 配置和用户安装的运行时。
