---
name: smartpi
description: SmartPi 设备绑定、扫码、设备管理与连接故障排查。Use when the user mentions binding SmartPi, SmartPi QR code, 9002, SmartPi connection failure, listing SmartPi devices, or removing a SmartPi device.
allowed-tools: terminal, read_file, grep, find_path
context: local-first
---

# SmartPi 

帮助用户完成 SmartPi 插件安装检查、设备扫码绑定、设备列表查看、设备删除，以及 `9002` / 连接失败等常见问题排查。

## 设计原则

- **元信息负责触发**：`description` 必须直接覆盖用户常见说法，例如 SmartPi 绑定、二维码、9002、连接失败、查看设备、删除设备。
- **正文负责执行**：按任务给出明确步骤、成功判定、失败分支和用户输出。
- **本地优先**：优先使用本机 `openclaw` 命令、Gateway 配置和日志，不假设外部服务可用。
- **最小副作用**：删除设备、安装插件、重启 Gateway、修改配置前必须说明影响并征得用户确认。

## 触发条件

当用户提出以下请求时使用本 Skill：

- **绑定设备**：绑定 SmartPi、添加 SmartPi、生成 SmartPi 二维码、扫码绑定。
- **设备管理**：查看 SmartPi 设备、列出已绑定设备、删除 SmartPi 设备。
- **连接故障**：SmartPi 连接失败、设备不在线、WebSocket 断开。
- **9002 故障**：用户看到 `9002`、`AI response timeout`、语音请求无响应或超时。
- **插件配置**：安装 `openclaw-smartpi`、检查插件是否启用、修复 `channels.openclaw-smartpi`。

## 不适用场景

- 用户问题与 SmartPi、OpenClaw Gateway、`openclaw-smartpi` 插件无关。
- 用户要求开发新功能、改插件源码或调试非 SmartPi 通道时，应转入代码分析/开发类流程。
- 用户只询问泛化 IoT、语音识别或硬件设计知识时，不应直接执行 OpenClaw 命令。

## 快速路由

| 用户意图 | 首选流程 | 主要成功判定 |
| --- | --- | --- |
| 绑定/添加 SmartPi | [流程：绑定设备](#流程绑定设备) | 日志出现 `WebSocket connected: <deviceKey>` |
| 查看/列出设备 | [流程：查看设备](#流程查看设备) | `accounts list` 返回设备列表 |
| 查询设备连接状态 | [流程：查询设备连接状态](#流程查询设备连接状态) | `accounts status` 返回设备在线/离线状态 |
| 删除设备 | [流程：删除设备](#流程删除设备) | 删除命令成功且列表不再包含该设备 |
| 安装/启用插件 | [流程：首次安装或修复插件](#流程首次安装或修复插件) | `plugins list` 显示 `openclaw-smartpi: enabled` |
| 9002/超时 | [流程：9002 排查](#流程9002-排查) | 定位为连接、路由或 AI 响应链路问题 |

## 执行前检查

在执行会改变状态的动作前，先确认用户意图是否明确。

1. 检查 OpenClaw CLI 是否可用：`openclaw --help`
2. 检查插件状态：`openclaw plugins list`
3. 检查已绑定设备：`openclaw smartpi accounts list`
4. 若需要修改配置，先读取完整配置，再构造完整 patch。

## 流程：绑定设备

### 目标

生成 SmartPi 绑定二维码，让用户扫码绑定，并确认设备通过 WebSocket 上线。

### 执行步骤

1. 执行绑定命令：

```bash
openclaw smartpi accounts bind
```

2. 从输出中提取 `绑定ID:` 后的 `bindingId`。
3. 使用 `bindingId` 生成 `smartpi_qr.png`。
4. 把二维码图片发给用户，并提示：`请用微信扫一扫，绑定成功后我会继续确认设备连接状态。`
5. 等待 30-120 秒，检查日志中是否出现 `WebSocket connected: <deviceKey>`。
6. 连接成功后告知用户：`设备已连接，可以对着 SmartPi 说话了。`

### 二维码生成方式

优先使用当前环境已经安装的二维码工具，不要为了生成二维码自动安装依赖。

Python：

```python
import qrcode
binding_id = "REPLACE_WITH_ACTUAL_BINDING_ID"
qrcode.make(binding_id).save("smartpi_qr.png")
```

Node.js：

```bash
node -e "const id=process.argv[1]; require('qrcode').toFile('smartpi_qr.png',id,{type:'png'},e=>e&&console.error(e))" "REPLACE_WITH_ACTUAL_BINDING_ID"
```

### 成功判定

- 已生成二维码并发送给用户。
- 日志出现 `WebSocket connected: <deviceKey>`。
- `openclaw smartpi accounts list` 能看到新设备。

### 失败分支

- **未提取到 `bindingId`**：反馈绑定命令输出异常，并展示关键输出让用户确认。
- **二维码生成失败**：说明当前环境缺少二维码依赖，询问用户是否允许安装依赖或改用其他方式生成。
- **120 秒内未连接**：转入 [流程：连接失败排查](#流程连接失败排查)。
- **连接后仍不可用**：转入 [流程：9002 排查](#流程9002-排查)。

## 流程：查看设备

### 执行步骤

```bash
openclaw smartpi accounts list
```

### 输出要求

- 如果有设备，列出 `deviceKey`、在线状态或命令输出中的关键字段。
- 如果没有设备，提示用户可以执行绑定流程。
- 不要伪造设备状态；只根据命令输出和日志判断。

## 流程：查询设备连接状态

### 目标

通过设备号查询指定设备的在线/离线连接状态。

### 执行步骤

1. 如果用户未提供设备号，先执行 `openclaw smartpi accounts list` 列出所有设备供用户选择。
2. 获取设备号后，执行：

```bash
openclaw smartpi accounts status <device_number>
```

### 输出要求

- 根据命令输出，展示该设备的连接状态（在线/离线/未找到等）。
- 如果设备未找到，提醒用户检查设备号是否正确。
- 不要伪造状态；只根据命令输出和日志判断。

### 成功判定

- 命令返回设备连接状态（connected / disconnected / unknown 等）。
- 结合日志关键字进一步判断设备是否正常通信。

### 失败分支

- **设备未找到**：提示用户检查设备号是否正确，可重新执行 `accounts list` 确认。
- **命令执行失败**：展示错误信息，询问用户是否继续排查。

## 流程：删除设备

### 执行步骤

1. 先列出现有设备：

```bash
openclaw smartpi accounts list
```

2. 确认要删除的 `deviceKey`。
3. 明确提醒用户：删除会解绑本地记录，并可能同步解绑云端。
4. 用户确认后执行：

```bash
openclaw smartpi accounts remove <deviceKey>
```

5. 再次执行 `accounts list` 验证设备已删除。

### 安全规则

- 删除设备前必须获得用户明确确认。
- 如果用户没有提供 `deviceKey`，必须先列出设备并让用户选择。
- 不要批量删除设备，除非用户明确要求并逐项确认。

## 流程：首次安装或修复插件

### 目标

安装并启用 `openclaw-smartpi` 插件，确保 Gateway 能加载 SmartPi channel。

### 执行步骤

1. 检查插件状态：

```bash
openclaw plugins list
```

2. 若插件未安装，征得用户确认后执行：

```bash
openclaw plugins install openclaw-smartpi
```

3. 修改配置前，必须先读取完整配置。
4. 保留已有 `plugins.allow` 和 `channels` 内容，只追加 openclaw-smartpi 所需项。
5. 重启 Gateway 前说明影响，用户确认后执行：

```bash
openclaw gateway restart
```

6. 重启后再次检查 `plugins list` 和日志。

### 成功判定

- `openclaw plugins list` 显示 `openclaw-smartpi: enabled`。
- 配置中存在 `channels.openclaw-smartpi`。
- 日志中没有 `cannot resolve agentId`。

## 流程：连接失败排查

### 排查顺序

1. 检查插件是否启用：`openclaw plugins list`
2. 检查账号是否存在：`openclaw smartpi accounts list`
3. 检查日志是否出现 `WebSocket connected`
4. 检查日志是否出现 `WebSocket disconnected`
5. 检查网络、设备扫码是否完成、绑定是否过期。
6. 若日志出现 `cannot resolve agentId`，检查 `channels.openclaw-smartpi`。

### 输出要求

- 先说明当前卡在哪一层：插件、账号、WebSocket、路由、AI 响应。
- 每次只给用户一个明确下一步，不要同时抛出大量可能原因。

## 流程：9002 排查

`9002` 表示 AI 未在限定时间内回复。不要直接假设是设备坏了，应按链路排查。

### 排查顺序

1. 插件状态：`openclaw plugins list`，确认 `openclaw-smartpi: enabled`。
2. 设备绑定：`openclaw smartpi accounts list`，确认存在设备。
3. 设备连接：查日志 `WebSocket connected`，确认设备在线。
4. 路由配置：查日志 `cannot resolve agentId`，确认 `channels.openclaw-smartpi` 存在。
5. AI 响应：向 OpenClaw 发一条文本，确认本地模型、MCP、Tools 是否响应过慢。
6. 超时日志：查 `AI response timeout`，判断是否由模型慢、MCP 阻塞或工具调用卡住导致。

### 常见结论

- **插件未启用**：修复插件安装或配置。
- **没有绑定设备**：引导用户走绑定流程。
- **WebSocket 未连接**：检查扫码、网络和绑定状态。
- **`cannot resolve agentId`**：修复 `channels.openclaw-smartpi`。
- **文本请求也慢**：优先排查本地模型、MCP、Tools，而不是 SmartPi 设备。

## 硬性规则

### `plugins.allow` 是整体替换

`config.patch` 对数组是整体替换，不是追加。修改前必须先读取当前完整配置，构造包含原有插件和 `openclaw-smartpi` 的完整数组后再 patch。

### `channels` 是整体替换

不要只 patch `channels.openclaw-smartpi`。这可能覆盖掉已有 channel，例如 `discord`、`telegram`。必须保留所有已有 `channels`，再追加 `openclaw-smartpi`。

### `channel.id` 必须匹配

插件内部 `channel.id = "openclaw-smartpi"`，配置中必须是 `channels.openclaw-smartpi`，一字不差。否则消息无法路由，常见日志为 `cannot resolve agentId`。

### 配置示例

```json
{
  "channels": {
    "openclaw-smartpi": {
      "enabled": true,
      "defaultAgentId": "main"
    }
  }
}
```

## 用户沟通规范

- **先说明动作**：执行命令前，用一句话说明要检查什么。
- **展示关键结果**：只摘取插件状态、设备 ID、日志关键字等必要信息。
- **区分事实和推测**：没有日志证据时，不要断言设备在线或离线。
- **需要确认时暂停**：安装、删除、重启、配置修改前必须等待用户确认。
- **失败时给下一步**：不要只说失败，要说明下一步检查命令或需要用户提供的信息。

## 常用命令

| 命令 | 用途 | 风险 |
| --- | --- | --- |
| `openclaw --help` | 检查 CLI 是否可用 | 只读 |
| `openclaw plugins list` | 确认插件状态 | 只读 |
| `openclaw smartpi accounts list` | 查看已绑定设备 | 只读 |
| `openclaw smartpi accounts status <device_number>` | 查询指定设备连接状态 | 只读 |
| `openclaw smartpi accounts bind` | 扫码绑定新设备 | 创建绑定 |
| `openclaw smartpi accounts remove <deviceKey>` | 删除设备并解绑 | 高风险 |
| `openclaw plugins install openclaw-smartpi` | 安装插件 | 修改环境 |
| `openclaw gateway restart` | 重启 Gateway | 中断服务 |

## 日志关键字

| 关键字 | 含义 | 下一步 |
| --- | --- | --- |
| `WebSocket connected` | 设备已上线 | 验证设备列表和语音交互 |
| `WebSocket disconnected` | 设备断开 | 检查网络、设备状态、绑定状态 |
| `cannot resolve agentId` | 缺少或错误配置 `channels.openclaw-smartpi` | 修复 channels 配置 |
| `AI response timeout` | AI 响应超时，可能导致 `9002` | 排查模型、MCP、Tools 响应链路 |

## 最小完成标准

每次使用本 Skill 后，最终回复必须包含：

- **当前状态**：已绑定、已连接、未连接、未安装、配置异常或超时。
- **证据来源**：命令输出、日志关键字或用户提供的信息。
- **下一步**：如果未解决，明确下一条建议动作。

# SmartPi Skill 增强说明

## 触发条件新增

当用户出现以下描述时，自动进入设备无响应排查流程：

* SmartPi 没反应
* SmartPi 不回复
* 对设备说话没反应
* 按键后没反应
* 设备在线但没有回复
* 语音请求没有响应
* SmartPi 无响应
* 设备不说话
* SmartPi 没有声音
* SmartPi 不工作了

---

## 快速路由新增

| 用户意图  | 首选流程       | 主要成功判定             |
| ----- | ---------- | ------------------ |
| 设备没反应 | 流程：设备无响应排查 | 定位到绑定、连接、路由或 AI 问题 |

---

## 流程：设备无响应排查

### 目标

当用户反馈设备没有任何响应时，快速判断问题位于：

* 未绑定设备
* WebSocket 未连接
* 连接后断开
* 路由配置异常
* AI 响应超时
* 设备侧异常

不要直接假设设备损坏。

---

### 排查顺序

#### 1. 检查本地是否存在已绑定设备

执行：

```bash
openclaw smartpi accounts list
```

判定：

* 返回设备列表 → 继续下一步
* 返回空列表 → 引导用户执行绑定流程

输出要求：

```text
当前未发现已绑定的 SmartPi 设备，请先完成设备绑定。
```

---

#### 2. 检查设备连接状态

查看 Gateway 日志。

重点查找：

```text
WebSocket connected
```

或：

```text
WebSocket connected: <deviceKey>
```

判定：

* 出现 connected → 设备已连接
* 未出现 connected → 设备未连接

输出要求：

```text
设备已绑定，但尚未连接到 Gateway，请检查网络连接或重新扫码绑定。
```

---

#### 3. 检查是否发生断线

查看日志：

```text
WebSocket disconnected
```

判定：

* 存在 disconnected → 设备连接后断开
* 不存在 disconnected → 继续下一步

输出要求：

```text
设备曾成功连接，但后续发生断线，请检查设备网络状态。
```

---

#### 4. 检查消息路由

查看日志：

```text
cannot resolve agentId
```

判定：

* 出现该日志 → channels.openclaw-smartpi 配置异常
* 未出现 → 继续下一步

输出要求：

```text
Gateway 无法找到目标 Agent，请检查 channels.openclaw-smartpi 配置。
```

---

#### 5. 检查 AI 响应链路

查看日志：

```text
AI response timeout
```

或者执行一次普通文本请求验证。

判定：

* 文本请求正常 → 设备链路问题
* 文本请求也超时 → AI 链路问题

输出要求：

```text
设备连接正常，但 AI 响应超时，请优先检查模型、MCP 或 Tool 响应情况。
```

---

### 常见结论

| 现象                        | 结论      |
| ------------------------- | ------- |
| accounts list 为空          | 未绑定设备   |
| 无 WebSocket connected     | 未建立连接   |
| 出现 WebSocket disconnected | 连接后断开   |
| cannot resolve agentId    | 路由配置异常  |
| AI response timeout       | AI 响应超时 |
| 以上均正常                     | 检查设备侧日志 |

---

### 最终输出格式

每次排查结束后必须返回：

当前状态：

* 已绑定 / 未绑定
* 已连接 / 未连接
* 路由正常 / 异常
* AI 正常 / 超时

证据来源：

* accounts list
* WebSocket connected
* WebSocket disconnected
* cannot resolve agentId
* AI response timeout

下一步：

* 给出唯一明确的下一步动作，不同时列出多个方向。

