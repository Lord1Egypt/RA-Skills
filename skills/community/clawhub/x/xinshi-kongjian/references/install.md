# 安装与连接

使用解压后的完整技能包；不需要克隆原开发项目。先运行 `node <技能目录>/scripts/reflection.mjs doctor`。数据目录默认 `~/.private-reflection`，可用 `PRIVATE_REFLECTION_DATA_DIR` 为不同本人身份设置独立目录；不要放到技能包内部。

对外名称为“心事空间”，技能标识为 `xinshi-kongjian`。升级沿用已有数据目录、环境变量、Keychain 服务和 `/private-reflection` 命令，不需要迁移档案。已有旧技能目录请先备份后移出宿主的技能发现目录，避免同时加载两份规则。

## 秘密配置

- macOS 默认复用情感支持档案的 Keychain 服务；写入 Keychain 的辅助源文件是 [../scripts/keychain-set.c](../scripts/keychain-set.c)。
- Linux 通过宿主秘密管理注入 `PRIVATE_REFLECTION_KEY`，内容为安全生成的 32 字节密钥的 base64。每个本地实例保存自己的密钥，重新安装需保留它，程序不会生成明文密钥文件。
- FlowUs 通过 `FLOWUS_TOKEN` 或 macOS 已有 Keychain 凭据连接，不把 Token 放在聊天、命令参数、技能文件和安装包里。
- 初次初始化运行 `init --legacy-root <原项目>` 复用已配置的私有根页面；新用户运行 `init --root-page <私有页面UUID>`，不指定页面则创建专用私有根页面。重复初始化复用现有配置。
- FlowUs 中含可读全文，获得库权限的账号与集成可以读取。先确认目标私有页面与访问权限，再初始化。

## 安装技能

```sh
node <包>/scripts/reflection.mjs install --agent openclaw --workspace <目标agent工作区>
node <包>/scripts/reflection.mjs install --agent hermes --workspace <Hermes配置或profile目录>
node <包>/scripts/reflection.mjs install --agent deepseek --workspace <目标项目目录>
```

安装会验证 [../bundle-manifest.json](../bundle-manifest.json) 并只复制列明文件。已有同名技能不会被覆盖。Hermes 目标为 `<profile>/skills/xinshi-kongjian`，DeepSeek Harness 为 `<project>/.agents/skills/xinshi-kongjian`，OpenClaw 为 `<workspace>/skills/xinshi-kongjian`。安装不修改宿主其他配置、不安装智能体本身，也不删除数据。

## OpenClaw 自动采集

技能管对话，配套插件管采集与本人命令；两者需要分别安装。插件文件完整位于 [../assets/openclaw/package.json](../assets/openclaw/package.json)、[../assets/openclaw/openclaw.plugin.json](../assets/openclaw/openclaw.plugin.json)、[../assets/openclaw/openclaw.mjs](../assets/openclaw/openclaw.mjs) 和 [../assets/openclaw/keychain-set.c](../assets/openclaw/keychain-set.c)。

在运行 Gateway 的宿主上，按当前官方 CLI 安装该插件目录并启用 `private-reflection`。合并以下插件配置；绑定实际的本人身份与私聊，不能照搬占位值：

```json
{
  "plugins": {
    "entries": {
      "private-reflection": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },
        "config": {
          "agentId": "个人agent的ID",
          "ownerId": "本人发送者ID",
          "chatId": "专用私聊的ID",
          "channel": "聊天渠道ID",
          "privateChat": true,
          "syncIntervalSeconds": 60,
          "dataDir": "/宿主上的独立数据目录"
        }
      }
    }
  }
}
```

使用宿主已有的秘密注入方式。插件与该 agent 的 CLI/MCP 必须使用同一数据目录和密钥。不要把其他用户加入同一个私有 profile。Gateway 必须在线才能承接手机消息；Mac 不必保持在线，下次运行同步会拉取云库。

默认每 60 秒补同步；消息先落本地持久队列，队列恢复后再同步。发送一段虚构私聊，核对本人和助手文本、FlowUs 与第二本地实例，并确认 `status` 没有采集缺口。缺少稳定消息 ID、媒体没有转写、宿主未暴露所需字段时会报告缺口，不把缺失标成完整。

真实宿主未测试前不能宣称“完整自动采集已兼容”。参考 [OpenClaw hooks](https://docs.openclaw.ai/plugins/hooks/reference)、[Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)、[DeepSeek Harness skills](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。

## 审核与迁移

手机命令：`/private-reflection pending` → `show <ID>` → 复制该版本对应的 `confirm` 或 `reject` 命令。内容变化后旧命令失效。`pause`、`resume` 控制本系统记录；`forget` 停止引用；`delete` 建立同步删除标记。物理清理云平台及宿主副本需另行处理。

FlowUs 人工审核需在本地 `cloud.json` 的 `reviewerIds` 配置允许的 FlowUs 用户 ID（或使用 `init --reviewer-ids <ID,...>`）。未绑定身份时不会接受云端状态提升；集成账号的修改不能冒充用户确认。

`migrate --legacy-root <项目>` 先备份旧加密库、索引、原配置及授权索引，再导入所有结构化状态。旧原文不上传、原文件不移动。保留旧密钥与原项目，旧的单次授权原文读取仍在那里进行。迁移后运行 `sync`；备份路径与导入数量由命令返回。

旧 CLI/MCP 使用 v2 时，设置 `PRIVATE_REFLECTION_DATA_DIR` 指向同一档案；未切换的旧配置沿用原行为，避免隐式迁移。可选新 MCP 用 `node <技能目录>/scripts/reflection.mjs mcp` 启动。
