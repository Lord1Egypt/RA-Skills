## 🖥️ 平台兼容性

### ✅ **完整支持：OpenClaw**
- ✅ 多人在线（Telegram群聊）
- ✅ 自动获取玩家ID（Telegram ID）
- ✅ 自动发送配图（`message` tool）
- ✅ PvP和组队功能
- ✅ 共享世界状态

**推荐使用OpenClaw获得最佳体验。**

---

### ⚠️ **部分支持：Claude Code / Codex / 原生Claude**

**可以玩，但有限制**：

#### 限制1：单人模式
- ❌ 无法多人PvP/组队
- ✅ 可以单人探索、修炼、战斗NPC
- ✅ 可以完成单人剧情线

#### 限制2：手动存档管理
由于无法自动获取用户ID，需要手动指定：
```
/yumfu start --user myname
```
存档保存为 `user-myname.json`

#### 限制3：手动查看图片
配图会生成但不会自动发送，需要手动查看：
```
图片已生成: ~/.openclaw/media/outbound/yumfu/20260402-203045-scene.png
```
可用 `open` 或 `eog` 命令查看。

#### 限制4：无共享世界
每个用户独立运行，无法影响其他玩家的世界。

---

### 🛠️ **如何在非OpenClaw环境运行**

#### 方法A：单人模式（推荐）
1. 设置环境变量：
   ```bash
   export GEMINI_API_KEY="your-key"
   export YUMFU_USER_ID="myname"  # 自定义用户名
   ```

2. 开始游戏：
   ```
   /yumfu start
   ```

3. 查看配图（需手动）：
   ```bash
   open ~/.openclaw/media/outbound/yumfu/*.png
   ```

#### 方法B：纯文本模式（无配图）
如果没有`GEMINI_API_KEY`，可以禁用配图：
```bash
export YUMFU_NO_IMAGES=1
```
游戏将跳过图片生成，只输出文字剧情。

---

### 📋 **功能对比表**

| 功能 | OpenClaw | Claude Code | 原生Claude |
|------|----------|-------------|-----------|
| 单人游戏 | ✅ | ✅ | ✅ |
| 多人PvP/组队 | ✅ | ❌ | ❌ |
| 自动发送配图 | ✅ | ❌ | ❌ |
| 共享世界状态 | ✅ | ❌ | ❌ |
| Telegram群聊 | ✅ | ❌ | ❌ |
| 本地存档 | ✅ | ✅ | ✅ |
| 水墨风配图生成 | ✅ | ✅¹ | ✅¹ |

¹ 需要 `GEMINI_API_KEY` 和手动查看图片

---

### 💡 **最佳实践建议**

**推荐配置**：
- 🥇 **OpenClaw + Telegram群** → 完整多人体验
- 🥈 **OpenClaw + 私聊** → 单人体验 + 自动配图
- 🥉 **Claude Code** → 单人纯文本体验（适合快速测试）

**不推荐**：
- ❌ 在非OpenClaw环境玩多人模式（无法实现）
