---
name: wow-daily-news
description: 每日日报自动生成。每天 18:00 自动生成包含魔兽世界新闻、NGA 热帖、今日美图的飞书文档，并推送到飞书和微信。
---

# 每日日报

每天自动生成综合日报，汇总魔兽世界相关资讯，写入飞书文档并推送。

## 触发词

- "今日日报"
- "每日新闻"
- "生成日报"
- "日报"

---

## 📋 日报内容结构

按顺序包含以下 4 个板块：

1. 🎮 **魔兽世界今日新闻** — EXWIND 蓝帖/热修 + 暴雪中国官网（当日无新闻则跳过）
2. 📋 **艾泽拉斯议事厅** — NGA 热门帖子（3 条，无数据则跳过）
3. 🏘️ **晴风村** — NGA 晴风村热门帖子（1 条，无数据则跳过）
4. 🌸 **今日美图** — 小红书真人美女博主（9 张图片，获取失败则降级标记）

---

## ⏱️ 时间日志（必须执行）

**每个 Step 开始和结束时，必须执行以下命令记录时间：**
```bash
echo "[Step N] start $(date '+%H:%M:%S')"
echo "[Step N] end $(date '+%H:%M:%S')"
```

这用于排查超时问题，**不可跳过**。

---

## 🚨 Agent 执行步骤

### Step 1: 运行数据收集脚本

```bash
echo "[Step 1] start $(date '+%H:%M:%S')"
python3 ~/.openclaw/workspace/scripts/daily_report_generator.py
echo "[Step 1] end $(date '+%H:%M:%S')"
```

脚本只负责收集基础数据（标题、链接、URL），**不抓详情**。

### Step 2: 解析 JSON 输出

```bash
echo "[Step 2] start $(date '+%H:%M:%S')"
```

从 Step 1 的输出中解析 JSON：
```json
{
  "success": true,
  "date": "2026-03-18",
  "title": "每日日报 - 2026年03月18日",
  "news": [{"title": "...", "url": "...", "date": "...", "type": "...", "source": "..."}],
  "nga_aiz": [{"title": "...", "url": "...", "tid": "...", "replies": 0}],
  "nga_qfc": [{"title": "...", "url": "...", "tid": "...", "replies": 0}],
  "beauty": {"success": true/false, "error": "...", "blogger": {...}, "images": [...]},
  "news_count": 0,
  "nga_count": 4
}
```

```bash
echo "[Step 2] end $(date '+%H:%M:%S')"
```

### Step 3: 处理美图（优先处理，失败可降级）

```bash
echo "[Step 3] start $(date '+%H:%M:%S')"
```

1. **检查 beauty.success**：
   - `true` → 跳到 Step 4
   - `false` → 进入自动修复流程

2. **自动修复流程**（**最多重试 1 次**）：

   **a. 检查小红书 MCP 服务是否运行：**
   ```bash
   curl -s --connect-timeout 3 http://localhost:18060/mcp
   ```
   - 无响应 → 启动：
     ```bash
     cd ~/xiaohongshu-mcp && nohup ./xiaohongshu-mcp-linux-amd64 >> mcp.log 2>&1 & sleep 10 && curl -s --connect-timeout 3 http://localhost:18060/mcp
     ```

   **b. 重新运行美图脚本：**
   ```bash
   python3 ~/.openclaw/workspace/skills/daily-beauty/daily_beauty.py
   ```
   - 成功 → 更新 beauty 数据，继续 Step 4
   - 失败 → **降级处理**：标记 `beauty_failed = true`，继续生成日报（美图板块显示降级提示），**不要停止执行**

3. **⚠️ 绝对不要因为美图失败而停止日报生成。** 美图只是锦上添花，新闻和 NGA 内容更重要。

> 注：Xvfb 已配置为 systemd 常驻服务（`systemctl status xvfb`），无需手动启动。

```bash
echo "[Step 3] end $(date '+%H:%M:%S')"
```

### Step 4: 抓取 NGA 帖子详情

```bash
echo "[Step 4] start $(date '+%H:%M:%S')"
```

对 nga_aiz + nga_qfc 中的每条帖子，按回复数从高到低依次处理：
1. 用 agent-browser 打开帖子 url
2. 查看帖子发表时间/最后回复时间，超过 7 天则跳过，递推到下一个
3. 在 7 天内 → 提取摘要（100-200字）+ 下载配图到 ~/.openclaw/workspace/img/
4. 处理完后关闭浏览器

如果列表为空，**跳过对应板块**。

```bash
echo "[Step 4] end $(date '+%H:%M:%S')"
```

### Step 5: 获取新闻完整内容（如果有今日新闻）

```bash
echo "[Step 5] start $(date '+%H:%M:%S')"
```

从 `~/.openclaw/workspace/data/wow_news_history.json` 的 by_date 字段按 URL 匹配获取 content 字段。

如果 news 为空（今日无新闻），**跳过整个板块**。

```bash
echo "[Step 5] end $(date '+%H:%M:%S')"
```

### Step 6: 生成 Lark-flavored Markdown

```bash
echo "[Step 6] start $(date '+%H:%M:%S')"
```

按各板块格式规则生成完整 Markdown 内容（见下方"各板块详细规则"）。

```bash
echo "[Step 6] end $(date '+%H:%M:%S')"
```

### Step 7: 创建飞书文档

```bash
echo "[Step 7] start $(date '+%H:%M:%S')"
```

使用 `feishu_create_doc`：
- `title`：JSON 中的 title 字段
- `markdown`：生成的 Markdown
- **不要在 markdown 开头加一级标题**

```bash
echo "[Step 7] end $(date '+%H:%M:%S')"
```

### Step 8: 插入美图（仅美图成功时）

```bash
echo "[Step 8] start $(date '+%H:%M:%S')"
```

仅当 `beauty_failed` 不为 true 时执行：
- 使用 `feishu_doc_media` 逐张插入美图到文档末尾
- `action`: insert, `type`: image, `doc_id`: Step 7 的 doc_id
- **图片文件必须先复制到 /tmp/ 目录下**（feishu_doc_media 只允许 /tmp 路径）
- 每张图片间隔 2-3 秒，避免 429 限流

如果美图失败，跳过此步骤。

```bash
echo "[Step 8] end $(date '+%H:%M:%S')"
```

### Step 9: 推送文档链接（必须执行！）

```bash
echo "[Step 9] start $(date '+%H:%M:%S')"
```

使用 Step 7 获取的文档 URL，必须同时发送到两个渠道：
- 飞书：`message action=send channel=feishu target=user:ou_2f7b674673f4020ca4a64deda675ccc9 message="📰 每日日报已生成\n\n{url}"`
- 微信：`message action=send channel=openclaw-weixin target=o9cq80yHzZS7fs4USr2cLP6z53R4@im.wechat accountId=7785501783cf-im-bot message="📰 每日日报已生成\n\n{url}"`

```bash
echo "[Step 9] end $(date '+%H:%M:%S')"
echo "=== 日报生成完成 ==="
```

**🚨 如果不执行 Step 9 推送链接，日报就等于没生成！这一步绝对不能跳过！**

---

## 📐 各板块详细规则

### 🎮 魔兽世界今日新闻

**严格规则：**

1. **只包含今日新闻**：仅展示当天发布的新闻，无今日新闻则**整个板块跳过**
2. **必须包含完整内容**：每条新闻必须读取并展示完整正文
3. **必须包含配图**：每条新闻必须抓取原文中的图片
4. **不降级**：不取旧新闻凑数

**格式示例：**
```markdown
## 🎮 魔兽世界今日新闻

共 X 条资讯

---

### 📘 蓝帖：职业调整即将到来
📅 2026-03-17 09:56
🔗 [查看原文](https://exwind.net/post/blue/xxx)

<image url="配图URL" width="600" align="center"/>

完整新闻正文内容...

---
```

### 📋 艾泽拉斯议事厅

**严格规则：**

1. **时间限制**：只选择发表于一周内的帖子。打开帖子页面后，查看帖子的发表时间或最后回复时间，超过 7 天则跳过，递推到回复数排序的下一个帖子
2. **必须包含 100-200 字摘要**：打开帖子详情页抓取正文
3. **有配图则抓取插入**
4. **数量**：3 条，按回复数排序，一周内不足 3 条则有多少展示多少
5. **无数据则跳过板块**

**时间判断方式**：AI 打开帖子页面时，查看帖子的发表时间或最后回复时间，如果超过 7 天则跳过该帖子。

**格式示例：**
```markdown
## 📋 艾泽拉斯议事厅

---

### 1. 帖子标题
🔗 [查看帖子](https://nga.178.com/read.php?tid=xxx)  💬 回复：782

<image url="帖子配图URL" width="600" align="center"/>

帖子正文摘要（100-200字）...

---
```

### 🏘️ 晴风村

**严格规则：**

1. **时间限制**：同议事厅，超过 7 天则递推到下一个帖子
2. **必须包含 100-200 字摘要**：同议事厅
3. **有配图则抓取插入**
4. **数量**：1 条，按回复数排序，一周内不足 1 条则跳过板块
5. **无数据则跳过板块**

**格式示例：**
```markdown
## 🏘️ 晴风村

---

### 帖子标题
🔗 [查看帖子](https://nga.178.com/read.php?tid=xxx)  💬 回复：7086

<image url="帖子配图URL" width="600" align="center"/>

帖子正文摘要（100-200字）...

---
```

### 🌸 今日美图

**正常情况**：
- 1 位小红书真人美女博主的 9 张全身照
- 博主信息：昵称、粉丝数、获赞数

**降级处理**（美图获取失败时）：
```markdown
## 🌸 今日美图

> 今日美图服务暂时不可用，明日恢复 🌟
```

**⚠️ 美图失败不影响日报生成！** 日报以新闻和 NGA 内容为核心，美图为加分项。

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/workspace/scripts/daily_report_generator.py` | 数据收集脚本（纯数据，不抓详情） |
| `~/.openclaw/workspace/scripts/wow_news_monitor.py` | 新闻监控脚本（实时推送用） |
| `~/.openclaw/workspace/data/wow_news_history.json` | 新闻历史数据 |
| `~/.openclaw/workspace/data/daily_report_history.json` | 日报历史记录 |
| `/tmp/nga_history_multi.json` | NGA 帖子历史数据 |
| `~/.openclaw/workspace/skills/daily-beauty/daily_beauty.py` | 美图获取脚本 |
| `~/.openclaw/workspace/skills/wow-daily-news/scripts/wow_daily_news.py` | 魔兽新闻详情抓取脚本 |
| `~/.openclaw/workspace/img/` | 图片保存目录 |
| `~/xiaohongshu-mcp/` | 小红书 MCP 服务目录 |

---

## 🔗 数据源

### EXWIND 魔兽数据挖掘
- **URL**: https://exwind.net/
- **历史文件**: `data/wow_news_history.json`
- **详情获取**: 从 history JSON 的 by_date 字段按 URL 匹配 content

### 暴雪中国官网
- **URL**: https://wow.blizzard.cn/news/

### NGA 论坛
- **艾泽拉斯议事厅**: fid=7 | **晴风村**: fid=-7955747
- **历史文件**: `/tmp/nga_history_multi.json`
- **详情获取**: agent-browser 抓取摘要和配图

### 小红书（美图）
- **脚本**: `daily_beauty.py`
- **MCP 服务**: localhost:18060
- **依赖**: Xvfb 虚拟显示 (DISPLAY=:99)

---

## 📐 飞书文档格式要求

- **标题**: `##`、`###`，不重复文档标题
- **分割线**: 板块之间用 `---`
- **加粗**: 新闻/帖子标题用 `**加粗**`
- **链接**: `[文字](URL)` 语法
- **图片**: `<image url="..."/>` 语法
- **图标**: 📘蓝帖 🔧热修 📰新闻 📋议事厅 🏘晴风村 🌸美图

---

## ⚙️ Cron 配置

- **任务名**: `wow-daily-news`
- **调度**: `cron 0 18 * * *`（每天 18:00 北京时间）
- **超时**: 1200 秒（20 分钟）
- **会话**: isolated agentTurn
- **投递**: none（AI 通过 message tool 主动推送）
- **推送**: 飞书 + 微信双渠道

---

## 📝 更新记录

| 日期 | 变更 |
|------|------|
| 2026-03-31 | 超时从 600s 增大到 1200s（20分钟） |
| 2026-03-31 | 美图失败降级处理：不再阻塞日报生成，显示"暂时不可用" |
| 2026-03-31 | 每步添加时间日志（echo start/end），方便排查卡点 |
| 2026-03-31 | Xvfb 改为 systemd 常驻服务，移除手动启动逻辑 |
| 2026-03-31 | 推送渠道从 LightClaw 改为微信（openclaw-weixin） |
| 2026-03-18 | 美图失败自动修复（启动 MCP），失败则降级处理 |
| 2026-03-18 | 脚本重构：只输出基础数据，详情抓取由 AI 完成 |
| 2026-03-18 | 新增：NGA 必须摘要+配图 |
| 2026-03-18 | 新增：新闻仅今日+完整内容+配图 |
| 2026-03-18 | 新增：美图强制板块 |
| 2026-03-18 | 支持飞书+LightClaw 双渠道 |
| 2026-03-12 | 初始创建 |
