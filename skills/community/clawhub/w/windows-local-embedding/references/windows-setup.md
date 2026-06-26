# Windows 本地 Embedding / 记忆检索部署

## 目标

让 Windows 上的 OpenClaw 使用 **本地 embedding** 做记忆检索，而不是远程 embedding 服务。

## 推荐模型

- 模型名：`nomic-embed-text-v1.5`
- 实际文件名：`nomic-embed-text-v1.5.Q8_0.gguf`
- **正确文件大小：约 139 MB**（注意：不是 496MB，那是另一个不相关的模型文件）
- 下载地址：https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf
- HuggingFace 页面：https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF

下载完之后，验证文件头是否为 `GGUF`（正确的 gguf 文件头部4字节是 ASCII 的 "GGUF"）：

```powershell
$fs = [System.IO.File]::OpenRead("你的文件路径\nomic-embed-text-v1.5.Q8_0.gguf")
$buf = New-Object byte[] 4
$fs.Read($buf, 0, 4) | Out-Null
$fs.Close()
[System.Text.Encoding]::ASCII.GetString($buf)  # 应该输出 GGUF
```

## 推荐放置路径

建议放到 D 盘，避免占用 C 盘空间：

```
D:\Users\Administrator\Documents\openclaw\model_cache\nomic-embed-text-v1.5.Q8_0.gguf
```

## 安装 node-llama-cpp（应用商店版必须做）

**应用商店版 OpenClaw 没有打包 `node-llama-cpp`**，必须手动安装，否则本地 embedding 无法运行，会报错：

```
Local embeddings unavailable.
Reason: optional dependency node-llama-cpp is missing
```

安装方法：

```powershell
cd "D:\Program Files\OpenClaw\resources\openclaw"
npm install node-llama-cpp
```

安装过程较慢（需要下载预编译二进制，约 10-40 分钟），耐心等待。
出现 `added xxx packages` 即为成功，warn 和 vulnerabilities 提示可以忽略。

## 配置 openclaw.json

在 `C:\Users\Administrator\.openclaw\openclaw.json` 中修改 `memorySearch` 部分：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "local",
        "fallback": "none",
        "local": {
          "modelPath": "D:\\Users\\Administrator\\Documents\\openclaw\\model_cache\\nomic-embed-text-v1.5.Q8_0.gguf"
        }
      }
    }
  }
}
```

注意 Windows 路径里反斜杠要转义成 `\\`。

## 重启

**不是点 Dashboard 里的"连接"按钮**——那只是重连 Dashboard，不会重载配置。

需要完全关闭 OpenClaw 应用再重新打开。

## 验证是否生效

因为 `openclaw memory status --deep` CLI 在 Windows 上无输出，用以下脚本代替：

新建文件 `check_memory.mjs`：

```javascript
const base = 'file:///D:/Program%20Files/OpenClaw/resources/openclaw/dist/';
const { n: callGateway } = await import(base + 'call-C5sk0PsH.js');
const result = await callGateway({
  method: 'doctor.memory.status',
  params: { deep: true },
  timeoutMs: 15000
});
console.log(JSON.stringify(result, null, 2));
```

运行：

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

## 装好之后怎么用

装好之后，日常不用额外操作。

- 平时正常聊天就行
- 当龙虾需要回忆旧事时，会通过本地 embedding 去捞记忆
- 偶尔用验证脚本检查状态

## 常见问题

### 1. 报错 node-llama-cpp is missing

应用商店版必须手动安装，见上方"安装 node-llama-cpp"步骤。

### 2. 文件明明下载了，但还是失败

先查：
- 文件大小是否约 139MB（不是 496MB）
- 用验证脚本确认文件头是否为 `GGUF`
- 路径和文件名是否写对
- Windows 路径里的反斜杠是否转义成 `\\`
- 是否完全重启了 OpenClaw（不是点"连接"按钮）

### 3. provider 不是 local

通常是：
- JSON 结构写错
- 改错了配置文件
- 改完没重启

### 4. 检索效果一般

embedding 负责"找记忆"，不负责"发明记忆"。`MEMORY.md` 和 `memory/` 里没内容，再好的 embedding 也没用。

## 更新记录

- 原始版本：小龙虾哥哥编写
- 2026-03-14 虾宝更新：
  - 修正文件大小（139MB，不是 496MB）
  - 补充应用商店版必须手动安装 `node-llama-cpp` 的步骤
  - 补充 Gateway 验证脚本（替代无效的 CLI 命令）
  - 补充重启注意事项（不是点"连接"按钮）
  - 补充文件头验证方法
