# OpenClaw 与 Talk Robots 集成指南

本 Skill 用于将 OpenClaw 接入与你聊聊 (Talk Robots)。初始化流程通过 Talk Robots 机器人配置页的 `OpenClaw连接信息` 扫码项完成，不需要用户在聊聊会话输入任何命令。

二维码内容是初始化指令，格式为：

```text
/openclaw --init <base64-json>
```

其中 `<base64-json>` 是对 JSON 做 UTF-8 Base64 编码后的内容，JSON 包含：

```json
{"OPENCLAW_URL":"https://your-openclaw-domain","OPENCLAW_TOKEN":"your-openclaw-gateway-token","OPENCLAW_LAN_URL":"http://your-lan-ip:port"}
```

Talk Robots 机器人配置页扫码保存后，机器人会 Base64 decode 并保存 OpenClaw 连接信息。用户随后在聊聊会话中发送普通消息，即可通过 OpenClaw 进行对话。

## 功能概述

- **双向通信**：用户可以通过聊聊与 OpenClaw 对话。
- **自动初始化**：通过机器人配置页 `OpenClaw连接信息` 扫码导入 OpenClaw URL/Token。
- **连接自检**：将同一条 `/openclaw --init <base64-json>` 发送到会话时，Talk Robots 机器人会向 OpenClaw 发送“我发送 ping，你帮我回复 pong”验证配置。
- **事件投递**：OpenClaw 可调用 `/robot/send` 将文本或文件事件投递给指定机器人。

## 快速开始

### 1. 安装 Skill

使用 `clawhub` 安装：

```bash
clawhub install yunitalk-beta
```

`shell/robot_send.sh` 依赖 `curl`、`openssl` 和 `python3`。如果 OpenClaw 运行环境是容器，请确认镜像内已安装这些命令。

本地开发调试未发布版本时，才需要使用本仓库中的 `docs/skills/yunitalk-beta/` 目录。

### 2. 生成扫码连接内容

推荐使用 npm CLI 直接读取本机 OpenClaw 连接信息并生成可扫码的连接内容：

```bash
npx yntalk-openclaw-init
```

也可以先全局安装后运行：

```bash
npm install -g yntalk-openclaw-init
yntalk-openclaw-init
```

在本仓库内调试未发布版本时，可以直接运行本地包：

```bash
npx ./docs/skills/yunitalk-beta/npm/yntalk-openclaw-init
```

本仓库内的 CLI 源码位于 `npm/yntalk-openclaw-init/`；发布到 npm 后即可直接通过上面的 `npx` 命令使用。CLI 默认读取本机 `openclaw.json` 的 `gateway.port`、`gateway.bind`、`gateway.auth.token` 和 `gateway.http.endpoints.chatCompletions.enabled`，使用本机局域网 IPv4 生成局域网访问地址，并探测公网 IP 生成公网访问地址，最后输出完整 `/openclaw --init <base64-json>` 初始化指令和 1x1 scale 命令行二维码。
CLI 只支持 `-h/--help` 和 `-v/--verbose` 两个参数；默认无参数运行即可输出局域网访问地址、公网访问地址、初始化指令和 1x1 scale 二维码。生成的初始化 JSON 中 `OPENCLAW_URL` 使用公网访问地址，`OPENCLAW_LAN_URL` 保存局域网访问地址。
提交 `docs/openclaw-robot.js` 后，在机器人配置页的 `OpenClaw连接信息` 参数中扫码保存该二维码内容，脚本会自动解析并写入 `OPENCLAW_URL` 和 `OPENCLAW_TOKEN`。

输出示例：

```text
局域网访问地址:
http://192.168.1.10:3000

公网访问地址:
http://203.0.113.10:3000

扫码连接内容:
/openclaw --init eyJPUEVOQ0xBV19VUkw...

二维码(1x1):
████...
```

npx CLI 默认会自动读取本地 `openclaw.json` 的 Gateway 配置，探测公网 IP 生成公网访问地址，并从 `gateway.auth.token` 获取 Token，不需要手动传入这些配置。Base64 不是加密，不要把 `OPENCLAW_TOKEN` 明文、初始化指令、扫码连接内容或二维码发送到不可信渠道。

### 3. 在机器人配置页扫码保存

打开 Talk Robots 机器人配置页，找到 `OpenClaw连接信息` 参数，扫描或粘贴上一步生成的 `/openclaw --init <base64-json>` 并保存。保存后回到聊聊会话，发送任意普通消息即可开始对话。

机器人会自动执行：

1. 从扫码保存的初始化指令中提取 `<base64-json>` 并执行 Base64 decode，得到包含 `OPENCLAW_URL`、`OPENCLAW_TOKEN` 和可选 `OPENCLAW_LAN_URL` 的 JSON。
2. 写入 `OPENCLAW_URL`、`OPENCLAW_TOKEN` 和可选 `OPENCLAW_LAN_URL`。

初始化完成后，用户在聊聊里直接发送普通消息即可开始对话。

## OpenClaw Skill 环境变量

如需让 OpenClaw 通过本 Skill 主动调用 `/robot/send` 发送文本或文件，需要在 OpenClaw 中配置以下变量：

| 环境变量 | 对应配置项 | 必填 | 说明 |
|----------|-----------|------|------|
| `TALK_ROBOT_ENDPOINT` | `robot_endpoint` | 是 | Talk Robots `/v1/robot/send` 服务端点 |
| `TALK_ROBOT_ID` | `robot_id` | 是 | 机器人 ID，用于签名鉴权 |
| `TALK_ROBOT_KEY` | `robot_key` | 是 | 机器人密钥，用于签名鉴权 |
| `TALK_ROBOT_CVS_ID` | `cvs_id` | 否 | 可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话 |

也可以在 OpenClaw 配置文件 `openclaw.json` 的 `skills.entries` 中持久化：

```json
{
  "skills": {
    "entries": {
      "yunitalk-beta": {
        "enabled": true,
        "env": {
          "TALK_ROBOT_ENDPOINT": "https://api-talk.yuniapp.cn/v1/robot/send",
          "TALK_ROBOT_ID": "your-robot-id",
          "TALK_ROBOT_KEY": "your-robot-key",
          "TALK_ROBOT_CVS_ID": "optional-cvs-id"
        }
      }
    }
  }
}
```

这些变量需要由 OpenClaw 运行环境或管理员配置。不要在普通回复中回显 `TALK_ROBOT_KEY`。

## Talk Robots 机器人脚本配置

将 `docs/openclaw-robot.js` 提交到 Talk Robots。脚本会在机器人配置页扫码保存 `OpenClaw连接信息` 后写入以下 KV：

| 配置项 | 必填 | 说明 |
|--------|------|------|
| `OPENCLAW_URL` | 是 | OpenClaw Gateway 地址，例如 `https://your-openclaw-domain`；也兼容以 `/v1` 结尾的 OpenAI Base URL |
| `OPENCLAW_TOKEN` | 是 | OpenClaw Gateway Token |
| `TALK_ROBOT_ENDPOINT` | 否 | `/v1/robot/send` 地址，默认 `https://api-talk.yuniapp.cn/v1/robot/send` |

## 机器人消息发送接口

OpenClaw 可以调用 Talk Robots `/robot/send` 将文本或文件事件投递给指定机器人。发送消息时推荐优先使用本 Skill 内置脚本 `shell/robot_send.sh`，它会自动生成 `msg_id`、`noncestr`、`timestamp` 和 HMAC-SHA256 `sign`。

完整的文本消息、文件消息、签名规则和 `curl` 示例见独立文档：

- [ROBOT_SEND_API.md](./ROBOT_SEND_API.md) - 机器人消息发送接口

## 故障排查

### 问题：无法生成扫码连接内容

- 确认本机可以读取 OpenClaw 配置文件 `openclaw.json`。
- 确认配置中存在 `gateway.auth.token`。
- 使用 `npx yntalk-openclaw-init -v` 查看运行日志，或使用 `npx yntalk-openclaw-init -h` 查看帮助。

### 问题：初始化 ping/pong 失败

- 检查 `OPENCLAW_URL` 是否能访问 `/v1/chat/completions`。
- 检查 `OPENCLAW_TOKEN` 是否有效。
- 确认 OpenClaw 模型收到 ping 时能只回复 `pong`。

### 问题：无法发送消息

1. 检查 `TALK_ROBOT_ENDPOINT`、`TALK_ROBOT_ID`、`TALK_ROBOT_KEY` 是否完整。
2. 如需投递到指定会话，确认 `cvs_id` 使用当前目标会话 ID，且大小写未被改变；不传时默认投递到机器人与创建者的点对点会话。
3. 使用 `shell/robot_send.sh --dry-run` 检查签名 URL 和请求体。
4. 确认 `/robot/send` 的返回状态和错误信息。

## 注意事项

1. **安全性**：`OPENCLAW_TOKEN` 和 `TALK_ROBOT_KEY` 是敏感信息，请勿提交到代码仓库或普通聊天回复。
2. **会话 ID 可选**：`cvs_id` 用于指定目标会话；不传时默认投递到机器人与创建者的点对点会话。
3. **投递语义**：`/robot/send` 只表示事件已投递给机器人；是否最终回消息由机器人脚本决定。
4. **会话隔离**：每个用户的会话是独立的，OpenClaw 不应跨会话共享上下文。

## 参考文档

- [SKILL.md](./SKILL.md) - OpenClaw 技能详细说明
- [ROBOT_SEND_API.md](./ROBOT_SEND_API.md) - 机器人消息发送接口
- [ROBOT_SEND_CURL_API.md](./ROBOT_SEND_CURL_API.md) - 机器人消息 curl 调用示例
- [config.yaml](./config.yaml) - 技能配置文件
