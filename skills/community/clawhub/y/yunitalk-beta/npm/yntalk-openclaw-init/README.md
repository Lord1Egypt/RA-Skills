# yntalk-openclaw-init

`yntalk-openclaw-init` 用于生成 Talk Robots OpenClaw 机器人配置页可扫码保存的初始化指令和命令行二维码。

它会读取本机 OpenClaw 的 `openclaw.json`，从 Gateway 配置中获取端口、绑定模式和 `gateway.auth.token`，再探测本机局域网 IPv4 与公网 IP，生成可直接扫码写入机器人 `OpenClaw连接信息` 配置项的 `/openclaw --init <base64-json>` 初始化指令。

该工具没有运行时依赖，二维码使用终端黑白字符块绘制。

## 二维码内容

二维码内容是机器人配置页可识别的初始化指令：

```text
/openclaw --init <base64-json>
```

其中 `<base64-json>` 是下面 JSON 的 UTF-8 Base64 编码：

```json
{"OPENCLAW_URL":"https://your-openclaw-domain","OPENCLAW_TOKEN":"your-openclaw-gateway-token","OPENCLAW_LAN_URL":"http://your-lan-ip:port"}
```

`docs/openclaw-robot.js` 可以识别这个格式。请在机器人配置页的 `OpenClaw连接信息` 字段中扫码保存；保存后回到聊聊会话发送普通消息即可触发自动连通。

## 安装

不安装，直接运行：

```bash
npx yntalk-openclaw-init
```

全局安装后运行：

```bash
npm install -g yntalk-openclaw-init
yntalk-openclaw-init
```

在本仓库中调试本地版本：

```bash
npx ./docs/skills/yunitalk-beta/npm/yntalk-openclaw-init
```

## 使用

默认无参数运行：

```bash
npx yntalk-openclaw-init
```

无参数运行会自动获取当前 OpenClaw 连接信息，并输出：

- 局域网访问地址
- 局域网 OpenAI Base URL
- 公网访问地址
- 公网 OpenAI Base URL
- Gateway 状态
- `/openclaw --init <base64-json>` 初始化指令
- 1x1 scale 命令行二维码

命令行参数只支持：

```bash
npx yntalk-openclaw-init -h
npx yntalk-openclaw-init -v
```

全局安装后也可以这样运行：

```bash
yntalk-openclaw-init
yntalk-openclaw-init -h
yntalk-openclaw-init -v
```

参数说明：

- `-h` / `--help`：显示帮助
- `-v` / `--verbose`：打印配置查找、Gateway 推导和公网 IP 探测日志

## 默认读取逻辑

工具默认会：

- 查找并读取本地 `openclaw.json`
- 从 `gateway.port` 读取 Gateway 端口，缺省为 `18789`
- 从 `gateway.bind` 读取 Gateway 绑定模式
- 从 `gateway.auth.token` 读取 `OPENCLAW_TOKEN`
- 检查 `gateway.http.endpoints.chatCompletions.enabled`
- 探测本机局域网 IPv4 和公网 IP
- 使用公网 Gateway 根地址作为初始化 JSON 中的 `OPENCLAW_URL`
- 使用局域网 Gateway 根地址作为初始化 JSON 中的 `OPENCLAW_LAN_URL`
- 额外打印以 `/v1` 结尾的 OpenAI Base URL，方便核对接口地址

注意：初始化 JSON 中的 `OPENCLAW_URL` 不带 `/v1`。`docs/openclaw-robot.js` 会在请求时自动拼接 `/v1/chat/completions`，同时也兼容扫码内容本身已经带 `/v1` 的情况。

## 配置文件位置

工具会按以下位置查找 `openclaw.json`：

- `OPENCLAW_CONFIG` 环境变量指定的路径
- 当前目录及父目录下的 `openclaw.json`
- 当前目录及父目录下的 `.openclaw/openclaw.json`
- `~/openclaw.json`
- `~/.openclaw/openclaw.json`
- `~/.config/openclaw/openclaw.json`
- macOS: `~/Library/Application Support/OpenClaw/openclaw.json`

## 输出示例

```text
局域网访问地址:
http://192.168.1.10:18789

局域网 OpenAI Base URL:
http://192.168.1.10:18789/v1

公网访问地址:
http://203.0.113.10:18789

公网 OpenAI Base URL:
http://203.0.113.10:18789/v1

Gateway:
bind: all
port: 18789
auth_mode: bearer
chatCompletions: enabled

扫码连接内容:
/openclaw --init eyJPUEVOQ0xBV19VUkw...

二维码(1x1):
████...
```

如果公网 IP 探测失败，工具会回退到局域网地址，并在 stderr 中打印 warning。此时生成的公网访问地址并不是真正的公网地址。

如果 `gateway.bind` 不是 `lan`、`all`、`0.0.0.0` 或 `::`，工具也会打印 warning，提示公网访问可能失败。

## 常见问题

### 找不到 `openclaw.json`

确认 OpenClaw 已在本机初始化，并且配置文件位于默认查找路径之一。也可以用环境变量显式指定：

```bash
OPENCLAW_CONFIG=/path/to/openclaw.json npx yntalk-openclaw-init
```

### Token 为空

确认 `openclaw.json` 中存在：

```json
{
  "gateway": {
    "auth": {
      "token": "your-token"
    }
  }
}
```

### Chat API 未启用

确认配置中开启了 OpenAI 兼容接口：

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": {
          "enabled": true
        }
      }
    }
  }
}
```

### 二维码扫码后机器人仍访问失败

优先检查输出里的 `公网 OpenAI Base URL` 是否能从 Talk Robots 运行环境访问。`OPENCLAW_URL` 最终会请求：

```text
<OPENCLAW_URL>/v1/chat/completions
```

如果你传入的是以 `/v1` 结尾的 OpenAI Base URL，`docs/openclaw-robot.js` 会自动去重，不会拼出重复的 `/v1/v1/chat/completions`。

## 安全提示

`OPENCLAW_TOKEN` 会被编码进扫码初始化指令中。Base64 不是加密，不要把生成的初始化指令、连接内容或二维码发送到不可信渠道。
