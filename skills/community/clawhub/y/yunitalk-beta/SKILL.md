---
name: yunitalk-beta
description: 该技能用于 OpenClaw 接入与你聊聊，实现聊聊与 OpenClaw 的对话
version: 0.9.5
build: 20261015
---

# OpenClaw 会话技能

你可以通过 Talk Robots `/robot/send` 把文本或文件事件投递给当前聊聊机器人。`cvs_id` 是可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话。

## 初始化流程

本集成通过 Talk Robots 机器人配置页完成初始化。

请让用户在机器人配置页找到 `OpenClaw连接信息` 参数，扫描或粘贴 OpenClaw 生成的初始化指令。初始化指令格式为：

```text
/openclaw --init <base64-json>
```

其中 `<base64-json>` 是对下面 JSON 做 UTF-8 Base64 编码后的内容：

```json
{"OPENCLAW_URL":"https://your-openclaw-domain","OPENCLAW_TOKEN":"your-openclaw-gateway-token","OPENCLAW_LAN_URL":"http://your-lan-ip:port"}
```

安装完成后，请提示用户通过 npm CLI 读取本机 OpenClaw 配置并生成连接信息二维码，然后在 Talk Robots 机器人配置页的 `OpenClaw连接信息` 中扫码保存。推荐使用：

```bash
npx yntalk-openclaw-init
```

`yntalk-openclaw-init` 默认无参数运行即可输出可扫码保存到 `OpenClaw连接信息` 的 `/openclaw --init <base64-json>` 和命令行二维码。

不要明文展示 `OPENCLAW_TOKEN`。Base64 不是加密，不要把连接信息或二维码发送到不可信渠道。

## 连接信息保存

Talk Robots 机器人在配置页扫码保存连接信息后，会：

1. 从 `/openclaw --init <base64-json>` 中提取 `<base64-json>`。
2. Base64 decode 连接 JSON，保存 `OPENCLAW_URL`、`OPENCLAW_TOKEN` 和可选 `OPENCLAW_LAN_URL`。

如需使用本 skill 主动发送文本或文件，以下配置必须由 OpenClaw 运行环境或管理员提供：

| 字段 | 环境变量 | 说明 |
|------|----------|------|
| `robot_endpoint` | `TALK_ROBOT_ENDPOINT` | Talk Robots `/v1/robot/send` 地址 |
| `robot_id` | `TALK_ROBOT_ID` | 机器人 ID |
| `robot_key` | `TALK_ROBOT_KEY` | 机器人签名密钥 |
| `cvs_id` | `TALK_ROBOT_CVS_ID` | 可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话 |

不要回显 `robot_key`。

## 发送消息

按运行形态选择发送方式，不要手写签名：

**方式一（推荐）：`bin/bot-cli`**。如果 Skill 目录下存在 `bin/bot-cli` 启动器和 `bin/*.dat` 平台二进制（talk-robots 仓库 / skills.git 分发形态），优先使用它（基于 Talk Robots Go SDK 自动完成签名，无需 curl/openssl/python3）：

```bash
./bin/bot-cli text --content "hello"
```

`bin/bot-cli` 启动器按 `uname -s`/`uname -m` 自动选择当前平台（darwin/linux × amd64/arm64）并在首次运行时自动解压，无需安装 Go。

**方式二：`shell/robot_send.sh`**。clawhub 发布包因大小限制不包含 `bin/`；如果没有 `bin/bot-cli`，使用内置 shell 脚本（依赖 `curl`、`openssl` 和 `python3`，同样自动完成签名）：

```bash
./shell/robot_send.sh text --content "hello"
```

文本：

```bash
./shell/robot_send.sh text \
  --base-url "{{robot_endpoint}}" \
  --robot-id "{{robot_id}}" \
  --robot-key "{{robot_key}}" \
  --content "你好，任务已经处理完成。"
```

文件：

```bash
./shell/robot_send.sh file \
  --base-url "{{robot_endpoint}}" \
  --robot-id "{{robot_id}}" \
  --robot-key "{{robot_key}}" \
  --content "请查看附件" \
  --file "./report.pdf"
```

不确定参数是否正确时先加 `--dry-run` 预检（两种方式都支持）；`./bin/bot-cli version` 可查看内置二进制版本。

## Rules

1. 只引导用户在 Talk Robots 机器人配置页的 `OpenClaw连接信息` 中扫码保存 `/openclaw --init <base64-json>`。
2. 发送前必须确认 `robot_endpoint`、`robot_id`、`robot_key` 都存在。
3. 发送消息按形态选择：存在 `bin/bot-cli` 和 `bin/*.dat` 时用 `./bin/bot-cli`；否则用 `./shell/robot_send.sh`。两种方式都会自动生成签名，不要改用 curl 手写签名。
3. `cvs_id` 是可选参数；只有明确要投递到指定会话时才传入，并保持大小写原样。不传时默认投递到机器人与创建者的点对点会话。
4. 文本消息使用完整 `imx.Msg` JSON，`cmd=msg`，文本放 `body.content`。
5. 文件消息使用 `multipart/form-data`，通过 `file` 字段上传。
6. `/robot/send` 只是把事件投递给目标 robot，最终是否回发由机器人脚本决定。
7. 不要明文展示 `OPENCLAW_TOKEN` 或 `robot_key`，不要虚构配置或用户资料。
