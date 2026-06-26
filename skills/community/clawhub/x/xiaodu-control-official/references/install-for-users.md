# 用户安装指南

这份文档是 `xiaodu-control` 的普通用户安装路径。目标是让用户只处理授权文本，不手写 `~/.mcporter/mcporter.json`。

## 适用场景

- 你已经安装 `xiaodu-control` skill。
- 你想让 `xiaodu-control` 控制小度智能屏和小度 IoT 设备。
- 你不想手动编辑 JSON 配置。

## 需要准备

- 已安装 `mcporter`。
- 已安装 Node.js/npm，并且 `npx` 可用。

如果缺少 `mcporter`，本 skill 会停止自动配置并提示先安装；不会自动执行 `npm install -g mcporter`。

## 普通用户流程

1. 打开授权页：

```text
https://duerstatic.cdn.bcebos.com/openclaw/claw-token.html
```

2. 在页面里完成授权，复制页面生成的整段文本。

文本通常类似：

```text
按照 https://duerstatic.cdn.bcebos.com/openclaw/SKILL.md 文档完成小度 channel 配置，AccessToken为xiaodu-xxxx
```

注意：这段文本里的远程 `SKILL.md` 和“channel 配置”只是授权页说明文案。`xiaodu-control` 会忽略这些说明，只提取 `AccessToken` 并配置 `mcporter`。

3. 把整段文本直接发给 OpenClaw。

4. `xiaodu-control` 会自动提取 `AccessToken`，并写入 `mcporter` home 配置。

实际执行的是：

```bash
bash scripts/configure_mcporter.sh --text "授权页复制的整段文本"
```

需要先确认但不写配置时，可以执行：

```bash
bash scripts/configure_mcporter.sh --text "授权页复制的整段文本" --check-only
```

脚本只做这些事：

- 从文本中提取 `xiaodu-...` token。
- 检查 `mcporter` 和 `npx`。
- 配置 `xiaodu` server。
- 配置 `xiaodu-iot` server。
- 验证两个 server 的 schema。

脚本不会做这些事：

- 不安装或升级 OpenClaw/Hermes 插件。
- 不写 OpenClaw/Hermes channel 配置。
- 不调用 `install-xiaodu.sh`。
- 不打开或遵循授权页文本里的远程 `SKILL.md`。
- 不自动全局安装 npm 包。

## 写入的配置

配置写入 `mcporter` home scope，通常对应：

```text
~/.mcporter/mcporter.json
```

等价配置如下：

```json
{
  "mcpServers": {
    "xiaodu": {
      "baseUrl": "https://xiaodu.baidu.com/dueros_mcp_server/mcp/",
      "headers": {
        "ACCESS_TOKEN": "<你的 AccessToken>"
      }
    },
    "xiaodu-iot": {
      "command": "npx",
      "args": [
        "-y",
        "dueros-iot-mcp"
      ],
      "env": {
        "ACCESS_TOKEN": "<你的 AccessToken>"
      }
    }
  }
}
```

## 验证

自动配置会默认验证：

```bash
mcporter list xiaodu --schema
mcporter list xiaodu-iot --schema
```

如果需要手动验证设备：

```bash
bash scripts/list_devices.sh
bash scripts/list_iot_devices.sh
```

## 常见失败

### 缺少 mcporter

提示：

```text
当前缺少 mcporter，无法写入小度 MCP 配置。
```

处理：先安装 `mcporter`，然后重新粘贴授权页文本。

### 缺少 npx

提示：

```text
当前缺少 npx，无法配置 xiaodu-iot。
```

处理：先安装 Node.js/npm，确认 `npx --help` 可用，然后重新粘贴授权页文本。

### token 格式不对

提示：

```text
未识别到 AccessToken。
```

处理：重新打开授权页，复制页面生成的完整文本。文本里应包含 `AccessToken为xiaodu-...`。

## 高级用法

如果你明确要绕过授权文本，也可以直接传 token：

```bash
bash scripts/configure_mcporter.sh --token "xiaodu-xxxx"
```

如果你明确要手动写配置，可以直接使用 `mcporter`：

```bash
mcporter config add xiaodu \
  --url "https://xiaodu.baidu.com/dueros_mcp_server/mcp/" \
  --header "ACCESS_TOKEN=<你的 AccessToken>" \
  --scope home

mcporter config add xiaodu-iot \
  --command npx \
  --arg -y \
  --arg dueros-iot-mcp \
  --env "ACCESS_TOKEN=<你的 AccessToken>" \
  --scope home
```

直接编辑 `~/.mcporter/mcporter.json` 只作为最后的排障方式，不作为普通用户流程。
