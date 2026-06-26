---
name: ZeeLin Twitter/X 运营
description: "ZeeLin 推特运营 — 蓝V互关（认证关注者回关）、回关新粉丝、写深度有趣评论、在需要涨粉的推文下自主打招呼以增加曝光与涨粉。用户自行登录 X 网页版，Agent 负责在账号 https://x.com/Gsdata5566 下执行蓝V互关/回关/评论/涨粉互动。Keywords: Zeelin, ZeeLin, Twitter growth, follow back, 互关, 回关, 蓝V互关, 认证关注者, 涨粉, 打招呼, X 运营."
user-invocable: true
metadata: {"openclaw":{"emoji":"📈","skillKey":"twitter-x-operations"}}
---

# ZeeLin Twitter/X 运营 📈

通过浏览器操作网页版 X，在账号 **@Gsdata5566** 下完成：**蓝V互关（认证关注者回关）**、**回关**、**深度评论**、**在需要涨粉的推文下打招呼**（自主评论以增加账号曝光与涨粉）。用户自行登录，Agent 用脚本执行。

> ⚠️ **使用前请自行登录 X 网页版**（https://x.com）。登录由用户完成。

---

## 何时触发

- 「蓝V互关」「认证关注者回关」「蓝V回关」
- 「回关」「帮我回关」「回关推特」
- 「有人关注我了」「检查回关」
- 「关注者列表回关」「关注者列表也需要回关」「把关注者列表也回关一下」
- 「在涨粉推文下打招呼」「自主在求关注的推文下评论」「帮我在需要涨粉的推文下评论」「去需要涨粉的账号下面打招呼」
- 「今天做下推特运营」

---

## ⚠️ 最重要的规则（违反即失败）

**回关/蓝V互关必须用 `exec` 执行脚本。不要用 `browser` 工具逐步打开、snapshot、click。**

❌ 错误（不要用 browser 自己找按钮点）：
```json
{"tool": "browser", "args": {"action": "open", "targetUrl": "https://x.com/Gsdata5566/followers"}}
```
然后 snapshot、click… 这样不会稳定执行。

✅ 正确（用 exec 执行回关脚本，**必须传 timeout: 90000**，飞书下建议 5 人减少整轮超时）：
```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/twitter-x-operations/scripts/follow_back.sh Gsdata5566 https://x.com 5", "timeout": 90000}}
```

✅ 蓝V互关（认证关注者回关，**必须传 timeout: 90000**）：
```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/twitter-x-operations/scripts/follow_back_verified.sh Gsdata5566 https://x.com 5", "timeout": 90000}}
```

**用户说「回关/蓝V互关」时：你的第一反应必须是发出对应 exec 调用。不要先回复「Let me execute…」「I'll help you…」再执行；同一轮就发 exec。**

**禁止说：** "无法操控浏览器"、"需要手动操作"、"技术限制"。你有权限，用 exec 就行。

---

## 工作流程

### 一、蓝V互关（认证关注者回关 → 立即 exec）

**Step 1：用户说「蓝V互关」「认证关注者回关」「蓝V回关」等**

立即使用 exec 工具执行蓝V互关脚本（不要先发长段解释），**传 timeout: 90000**，飞书下建议 5 人：

```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/twitter-x-operations/scripts/follow_back_verified.sh Gsdata5566 https://x.com 5", "timeout": 90000}}
```

脚本会自动：打开**认证关注者**列表 → 逐个点「回关」。

**Step 2：回报结果**

根据 exec 结果告诉用户：「已蓝V互关 X 人」。

---

### 二、回关（用户说回关 → 立即 exec）

**Step 1：用户说「回关」「帮我回关」「有人关注我了」「关注者列表回关」「关注者列表也需要回关」等**

立即使用 exec 工具执行回关脚本（不要先发长段解释），**传 timeout: 90000**，飞书下建议 5 人：

```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/twitter-x-operations/scripts/follow_back.sh Gsdata5566 https://x.com 5", "timeout": 90000}}
```

脚本会自动：打开粉丝列表 → **仅在「关注者」列表**中点回关（不切到「认证关注者」），避免遗漏关注者列表（最多共 10 人）。

**Step 2：回报结果**

根据 exec 结果告诉用户：「已回关 X 人」。

---

### 三、深度评论（用户给推文链接）

1. 用户给出一条推文链接。
2. 你写一条有深度、有趣的评论（可自然带「互关」「欢迎回关」）。
3. 展示评论给用户，确认后用 exec 执行：

```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/twitter-x-operations/scripts/comment.sh \"评论内容\" \"推文URL\" https://x.com"}}
```

---

### 四、涨粉推文下打招呼（自主评论，增加曝光与涨粉）

**目的**：在「需要涨粉 / 求关注 / 互关」类推文下主动发友好评论，吸引对方回关或路人关注，提升自己账号涨粉。

**Step 1：发现目标推文**

- **方式 A（推荐）**：用 `browser` 打开 X 搜索页，搜索关键词如 `follow for follow`、`f4f`、`互关`、`求关注`、`follow back`、`新号求关注` 等，用 snapshot 获取当前时间线中的几条推文，从页面中解析出推文 URL（形如 `https://x.com/用户名/status/123456`）；每次选 3～5 条即可。
- **方式 B**：用户直接提供几条「需要涨粉」的推文链接，你按链接逐条评论。

**Step 2：撰写打招呼评论**

每条推文下写一条**简短、友好、不营销**的评论，可自然带互关/回关暗示，例如：

- 「说得在理，已关，欢迎回关～」
- 「刚看到，已 fo，互关呀」
- 「有同感，关注了，常互动」

避免纯广告、复制粘贴感过重；每条可略有不同。

**Step 3：用 exec 逐条发评论**

对 Step 1 得到的每条推文 URL，用 exec 执行 comment 脚本（同一轮可连续多次 exec）。**务必传入较长 timeout（如 60000 或 90000 毫秒）**，否则容易 request timed out：

```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/twitter-x-operations/scripts/comment.sh \"评论内容\" \"https://x.com/xxx/status/123\" https://x.com", "timeout": 60000}}
```

**Step 4：回报结果**

汇总：「已在 N 条涨粉推文下打招呼」并列出推文链接或作者（若方便）。

**注意**：不要一次评论过多（建议单次 3～5 条），避免被平台限流；评论内容要像真人，不要重复同一句。

---

## exec 命令速查表

| 操作 | exec 命令 |
|------|-----------|
| **蓝V互关**（认证关注者回关，飞书下建议 5 人，timeout 90000） | `bash .../follow_back_verified.sh Gsdata5566 https://x.com 5`，exec 加 `"timeout": 90000` |
| **回关**（飞书下建议 5 人，timeout 90000） | `bash .../follow_back.sh Gsdata5566 https://x.com 5`，exec 加 `"timeout": 90000` |
| 回关（指定人数） | `bash .../follow_back.sh Gsdata5566 https://x.com 10` 或 20，同样加 timeout |
| 在推文下评论 | `bash .../comment.sh "评论内容" "https://x.com/xxx/status/123" https://x.com` |
| 涨粉推文下打招呼 | 先搜索/拿到推文 URL，再对每条执行上面评论命令（评论内容为友好打招呼，可带互关暗示） |
| 打开粉丝页 | `openclaw browser open https://x.com/Gsdata5566/followers` |
| 打开认证关注者页 | `openclaw browser open https://x.com/Gsdata5566/verified_followers` |
| 打开搜索页（找涨粉推文） | `openclaw browser open "https://x.com/search?q=follow%20for%20follow"` 或换关键词 互关/f4f/求关注 |

所有命令都通过 exec 工具执行，格式：
```json
{"tool": "exec", "args": {"command": "上面的命令"}}
```

---

## 示例

**用户**：蓝V互关  
**Agent**：直接发出 exec（蓝V互关脚本），然后根据结果回复「已蓝V互关 X 人」。

**用户**：回关  
**Agent**：直接发出 exec（回关脚本），然后根据结果回复「已回关 X 人」。

**用户**：有人关注我了，帮我回关一下  
**Agent**：直接发出 exec（回关脚本），然后汇报结果。

**用户**：关注者列表也需要回关  
**Agent**：直接发出 exec（回关脚本），脚本会处理关注者列表，然后汇报结果。

**用户**：在涨粉推文下打个招呼呗 / 自主去求关注的推文下面评论  
**Agent**：用 browser 打开 X 搜索「follow for follow」或「互关」等，snapshot 取 3～5 条推文 URL；对每条写一句友好打招呼评论（可带互关暗示），再逐条 exec comment.sh；最后汇报「已在 N 条涨粉推文下打招呼」。

---

**TL;DR**：
- 用户说「蓝V互关」→ **立刻** exec `follow_back_verified.sh`（timeout 90000）
- 用户说「回关」→ **立刻** exec `follow_back.sh`（timeout 90000）
- 用户说「打招呼」→ 找 3～5 条求关注推文 + exec 评论脚本
