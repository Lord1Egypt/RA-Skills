# 连接 企雀 AI 助手 的本地 MCP

本仓库提供 Skill 文档及配置示例，运行时由官方安装包另行提供。安装 Skill 不会自动安装或连接产品。

1. 下载同次发布的[企雀员工 Skill 包](https://res.qique.cn/system/skill/qique-employee-skill.zip)和[企雀AI助手 Chrome 包](https://res.qique.cn/system/skill/qique-ai-assistant-chrome.zip)，解压到同一父目录。阅读官方包的 INSTALL.md 后再按其中的安装步骤操作。Chrome 扩展首次加载及员工登录由用户完成；管理员须开启员工的 AI MCP操控。扩展有全站访问和 debugger 等权限，安装前查看官方 manifest 与说明。安装器会写用户安装目录及 AI 软件 MCP 配置，并启动本机桥接。
2. 使用 Windows 10/11，Chrome 120+ 和官方包自带的 Node（MCP engines 要求 Node 22+）。此包使用 Windows 凭据保护机制，不能直接作为 Linux/macOS 服务运行。
3. 参考 [mcp.example.json](../examples/mcp.example.json)，将所有 REPLACE_WITH 占位符替换为自己的官方运行目录及自带 Node 程序路径，再导入支持 stdio MCP 的 AI 软件。示例不是可直接运行的配置；无需在配置中输入产品登录令牌。
4. 如安装 Cursor 插件，将变量 QIQUE_EMPLOYEE_RUNTIME_DIR 设置为包含 mcp/server.cjs 的官方包根目录。同时设置 QIQUE_NODE_EXECUTABLE 为安装包自带 Node 的完整路径。变量只保存本机路径，不放入凭据。
5. 重启对应 MCP 服务，先用 tools/list 和 qique_tabs / qique_status 做只读检查。工具及权限以当前客户端实际返回为准；连接未验证时不声称可用。

客户端会话文件和安装后的配对/凭据文件仅留在本机，不上传到 GitHub、不发给 AI 对话。修改/删除/发送等业务动作必须按 SKILL.md 的授权与确认要求执行。产品官网是说明和下载页面，不是远程 MCP endpoint。

升级时从官网重新取得匹配的官方包，并核对版本与发布哈希；不要混用缓存旧包。卸载先按产品说明断开连接，再移除 AI 软件 MCP 配置和用户安装的运行时。
