# PTMail 邮箱聚合助手 · Email Management MCP

PTMail 邮箱聚合与邮件管理 AI Skill。通过已登录 Windows 客户端的本机 MCP 查看邮箱、读取邮件、同步、导出附件，并在用户授权后发送邮件。Use for PTMail multi-mailbox email assistance and local MCP setup.

企雀官方发布的独立 Agent Skill。这个仓库只有 **ptmail-mcp** 一个 Skill，导入时无需选择其他产品。

[官网](https://ptmail.qique.cn/) · [Skill](SKILL.md) · [连接说明](references/setup.md) · [MCP 配置示例](examples/mcp.example.json)

## 单独安装

使用 skills CLI 将这个 Skill 安装到支持的 AI 软件：

```sh
npx skills add Edmon/ptmail-mcp
```

先查看可发现的 Skill，不执行安装：

```sh
npx skills add Edmon/ptmail-mcp --list
```

也可下载 [本仓库 ZIP](https://github.com/Edmon/ptmail-mcp/archive/refs/heads/main.zip)，解压后将含根目录 `SKILL.md` 的文件夹导入支持本地 Skill 的 AI 软件。此 ZIP 仅包含一个 Skill。

## Cursor 插件

本仓库的 `.cursor-plugin/marketplace.json` 只登记一个插件，插件根目录提供一个 `SKILL.md`。在 Cursor 的 GitHub 仓库导入入口使用：

```text
https://github.com/Edmon/ptmail-mcp
```

MCP 配置中的运行目录变量须指向另行安装的官方运行包；安装 Skill 不会自动安装或登录产品客户端。公共市场的收录与审核状态以各市场页面为准。

## 使用与连接

PTMail Windows 邮箱聚合客户端的本地 MCP 使用说明：查看邮箱、读信、授权后发送、同步及导出附件。

[官网](https://ptmail.qique.cn/) · [连接说明](references/setup.md) · [Skill](SKILL.md) · [配置示例](examples/mcp.example.json)

本目录包含操作文档与 Cursor 配置，产品客户端、MCP 脚本及二进制均通过官方链接另行取得。需用户已登录的本机 Windows 客户端。本仓库版本为文档版本，不代表产品运行时版本。

本仓库内的 Skill 文档和配置示例采用 MIT-0 许可。官网产品与运行包不在本许可范围内，见 [LICENSE](LICENSE) 和 [LICENSE-NOTICE.txt](LICENSE-NOTICE.txt)。问题请在本仓库 Issues 中提供版本与脱敏错误；不要上传邮箱授权码、客户资料或会话文件。


## 搜索名称与用途

ptmail · 邮箱聚合 · 邮件管理 · email · mail · multi-mailbox · email assistant · attachments · mcp · agent skills

## 分发范围

这里分发 Skill 文档和配置示例。产品客户端、MCP 运行脚本、Chrome 扩展和依赖均从官网另行下载；现有员工权限、发送授权及批量任务确认规则继续适用。官方运行包的来源快照见 [official-downloads.json](distribution/official-downloads.json)，许可说明见 [LICENSE-NOTICE.txt](LICENSE-NOTICE.txt)。
