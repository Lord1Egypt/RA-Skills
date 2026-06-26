---
name: windows-local-embedding
description: 在 Windows 上为 OpenClaw 配置本地 embedding / 本地记忆检索时使用。适用于：下载并接入 `nomic-embed-text-v1.5.Q8_0.gguf`、把 `memorySearch.provider` 改成 `local`、检查 `openclaw memory status --deep`、以及排查"模型下了但不生效""路径写错""provider 不是 local""本地依赖没通"这类问题。对虾宝或其他 Windows 环境的龙虾尤其适用。
---

# Windows Local Embedding

处理 **Windows 环境下的 OpenClaw 本地 embedding / 本地记忆检索**。

## 为什么先做成 Windows 专用？

不是因为本地 embedding 只能在 Windows 上用，而是因为这次最真实、最紧急的使用场景就是：

- **虾宝是 Windows 环境**
- 之前一直没配成功
- Windows 最容易卡在路径、转义、重启是否生效这些细节上

所以先把它做成 **Windows 定向 skill**，是为了先解决最容易卡住的真实问题。

## 快速判断

- 用户说"本地 embedding 怎么配" → 用本 skill
- 用户说"虾宝 Windows 上本地 embedding 没成功" → 用本 skill
- 用户要下载 `nomic-embed-text-v1.5.Q8_0.gguf` 并接到 OpenClaw → 用本 skill
- 用户已经改了配置，但 `provider` 不是 `local` / 不生效 → 用本 skill

## 推荐流程

### 1. 先确认目标

默认目标不是 QMD，也不是复杂的外部向量数据库，而是：

- OpenClaw 自带 `memorySearch`
- `provider = local`
- 本地 GGUF embedding 模型可用

### 2. 模型文件

- 模型名：`nomic-embed-text-v1.5`
- 实际文件名：`nomic-embed-text-v1.5.Q8_0.gguf`
- **正确文件大小：约 139 MB**（注意：不是 496MB，那是另一个模型文件）
- 下载地址：https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf

下载完之后验证文件头是否为 `GGUF`（正确的 gguf 文件头部4字节是 ASCII 的 "GGUF"）：

```powershell
$fs = [System.IO.File]::OpenRead("你的文件路径\nomic-embed-text-v1.5.Q8_0.gguf")
$buf = New-Object byte[] 4
$fs.Read($buf, 0, 4) | Out-Null
$fs.Close()
[System.Text.Encoding]::ASCII.GetString($buf)  # 应该输出 GGUF
```

### 3. 安装 node-llama-cpp（应用商店版 OpenClaw 必须做这步）

**应用商店版 OpenClaw 没有打包 `node-llama-cpp`**，必须手动安装，否则本地 embedding 无法运行。

```powershell
cd "D:\Program Files\OpenClaw\resources\openclaw"
npm install node-llama-cpp
```

安装过程较慢（需要下载预编译二进制，约 10-40 分钟），耐心等待。
出现 `added xxx packages` 即为成功，warn 和 vulnerabilities 提示可以忽略。

### 4. 配置 openclaw.json

在 `C:\Users\Administrator\.openclaw\openclaw.json` 中确认以下配置：

```json
"memorySearch": {
  "provider": "local",
  "fallback": "none",
  "local": {
    "modelPath": "D:\\你的路径\\nomic-embed-text-v1.5.Q8_0.gguf"
  }
}
```

注意 Windows 路径里反斜杠要转义成 `\\`。

### 5. 重启 OpenClaw

**不是点 Dashboard 里的"连接"按钮**——那只是重连 Dashboard，不会重载配置。

需要完全关闭 OpenClaw 应用再重新打开。

### 6. 验证是否生效

重启后用以下脚本验证（因为 `openclaw memory status --deep` CLI 在 Windows 上无输出，用这个代替）：

```javascript
// check_memory.mjs
const base = 'file:///D:/Program%20Files/OpenClaw/resources/openclaw/dist/';
const { n: callGateway } = await import(base + 'call-C5sk0PsH.js');
const result = await callGateway({
  method: 'doctor.memory.status',
  params: { deep: true },
  timeoutMs: 15000
});
console.log(JSON.stringify(result, null, 2));
```

```powershell
node check_memory.mjs
```

成功的输出：
```json
{
  "agentId": "main",
  "provider": "local",
  "embedding": {
    "ok": true
  }
}
```

## 装好之后怎么使用？

装好之后，它不会自动让记忆"变聪明"，而是让 **记忆检索底层改为本地运行**。

1. 确保 `MEMORY.md` 和 `memory/` 里本来就有内容
2. 正常和龙虾对话
3. 当龙虾需要回忆旧事时，会通过本地 embedding 去捞记忆

## 最常见问题

### 1. 报错 `node-llama-cpp is missing`

应用商店版 OpenClaw 必须手动安装：

```powershell
cd "D:\Program Files\OpenClaw\resources\openclaw"
npm install node-llama-cpp
```

### 2. 模型下载了，但没生效

优先排查：
- 文件是否真的是 GGUF 格式（验证文件头）
- 文件大小是否约 139MB（不是 496MB）
- 路径和文件名是否写对
- Windows 反斜杠是否转义成 `\\`
- 改完是否完全重启了 OpenClaw（不是点"连接"按钮）

### 3. `provider` 不是 `local`

优先排查：
- JSON 结构写错位置
- 改错配置文件
- 改完没重启

### 4. 效果一般

embedding 负责"找记忆"，不负责"发明记忆"。`MEMORY.md` 和 `memory/` 里没内容，再好的 embedding 也没用。

## 经验原则

- 先跑通最小可用链路，再追求更花哨的方案
- 先看验证脚本输出，再讨论"是不是模型有问题"
- Windows 问题经常不是模型坏了，而是路径、配置、重启或缺依赖

## 来源说明

- 原始 skill 由小龙虾哥哥编写
- 2026-03-14 由虾宝根据实战经验更新：修正文件大小（139MB 非 496MB）、补充 node-llama-cpp 安装步骤、补充验证脚本、补充重启注意事项
