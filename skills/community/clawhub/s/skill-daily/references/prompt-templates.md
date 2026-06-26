# Cron 提示词模板

> 适用版本：clawhub-daily v1.0.0+
> 使用方法：复制下面的 JSON 配置到你的 Cron 平台，**替换痛点列表**为你自己的关注点

---

## 📌 通用结构

所有 Cron 配置都遵循：

```json
{
  "schedule": { "kind": "cron", "expr": "<cron 表达式>", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "<提示词内容>"
  },
  "delivery": { "mode": "announce", "channel": "<推送渠道>" }
}
```

---

## 🎯 模板 1：Trae SOLO（推荐）

**频率**：每 2 天 1 次（北京时间 21:00）  
**痛点**：默认 7 大类（按需修改）

```json
{
  "schedule": { "kind": "cron", "expr": "0 13 */2 * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "请执行 clawhub-daily Skill，按 SKILL.md 步骤 1-4 完成每日推荐。\n\n# 痛点（请直接使用，按优先级排序）\n- 🤖 自动化办公：gmail、calendar、slack、notion、sheets\n- 🛠️ 开发工具：github、mcp、browser、code、git、api\n- ✍️ 内容创作：youtube、video、image、pdf、writing\n- 🕷️ 数据采集：search、scraping、apify、firecrawl、google\n- 🧠 AI 增强：self-improving、proactive、memory、agent、reasoning\n- 🇨🇳 中文支持：chinese、baidu、wechat、taobao、bilibili\n- 💰 金融分析：polymarket、financial、stock、trading、market\n\n# 数据源\nClawHub Convex API（https://wry-manatee-359.convex.cloud/api/query）\n扫描数量：200 个 Skill（4 页 × 50/页）\n\n# 存储\n飞书云文档（feishu_app_id / feishu_app_secret 从 references/config.json 读取）\n\n# 输出\n- 简报 Markdown：data/recommended/{date}.md\n- 飞书云文档：包含所有推荐详情\n- 飞书卡片消息：250-400 字摘要 + Top 3 详细解读 + 完整简报链接\n\n# 完成后\n输出 200 字以内的对话摘要，包含：\n- 扫描数量、推荐数量、去重数量\n- 推荐维度（trending / quality / newcomers / panorama）\n- 命中场景（前 3 个）\n- 今日 TOP 1 Skill 名 + 一句话理由"
  },
  "delivery": { "mode": "announce", "channel": "feishu" }
}
```

---

## 🎯 模板 2：qclaw / WorkBuddy

**频率**：每日 1 次（北京时间 09:00）  
**痛点**：精简 3 大类（最常用）

```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行 clawhub-daily Skill。\n\n# 痛点（精简版）\n- 开发工具\n- 内容创作\n- AI 增强\n\n# 任务\n1. 抓取 ClawHub 200 个 Skill\n2. 按当前日期自动选维度（trending/quality/newcomers/panorama）\n3. 痛点匹配 + 10 天去重\n4. 生成简报 + 飞书推送\n\n# 输出\n简报 Markdown + 飞书卡片（200-400 字）"
  },
  "delivery": { "mode": "announce", "channel": "feishu" }
}
```

---

## 🎯 模板 3：纯 Linux/Mac crontab

**频率**：每 2 天 1 次（北京时间 21:00）  
**特点**：完全独立，无 Agent 依赖

```cron
# 编辑 crontab
0 13 */2 * * /bin/bash -c 'cd <your_clawhub_daily_path> && python clawhub_daily_executor.py >> logs/cron.log 2>&1'
```

**`<your_clawhub_daily_path>`** 替换为实际路径（如 `~/projects/clawhub-daily`）。

**建议**：
- 创建 `logs/` 目录用于 cron 日志
- 用 `>>` 追加而非 `>` 覆盖
- 加 `2>&1` 重定向错误输出

---

## 🎯 模板 4：Windows Task Scheduler

**频率**：每 2 天 1 次（北京时间 21:00）

**步骤**：
1. 打开"任务计划程序" → "创建基本任务"
2. 名称：ClawHub Daily
3. 触发器：每天 → 高级设置 → 勾选"重复任务间隔：2 天"
4. 操作：启动程序
   - 程序：`python`
   - 参数：`clawhub_daily_executor.py`
   - 起始于：`<your_clawhub_daily_path>`
5. 条件：勾选"唤醒计算机运行此任务"

---

## 🎯 模板 5：Hermes

**频率**：每日 1 次（北京时间 08:00）

```yaml
schedule:
  cron: "0 8 * * *"
  timezone: "Asia/Shanghai"
task:
  type: "agent"
  message: |
    请执行 clawhub-daily Skill：
    1. 抓取 ClawHub 200 个 Skill
    2. 计算指标 + 4 维度轮换
    3. 7 大痛点匹配 + 10 天去重
    4. 生成简报 + 飞书推送
  delivery:
    channel: "feishu"
    template: "card"
```

---

## 🔧 痛点列表定制指南

默认痛点库在 [`references/pain-points.md`](pain-points.md) 维护，**复制到 Cron 提示词里时请按需删减**：

### 7 大类全部使用（信息量最大）

```
🤖 自动化办公 / 🛠️ 开发工具 / ✍️ 内容创作 / 🕷️ 数据采集
🧠 AI 增强 / 🇨🇳 中文支持 / 💰 金融分析
```

### 精简 3 大类（聚焦核心）

```
🛠️ 开发工具 / ✍️ 内容创作 / 🧠 AI 增强
```

### 自定义（按你的职业/兴趣）

```
# 程序员
🛠️ 开发工具 / 🕷️ 数据采集 / 🧠 AI 增强

# 创作者
✍️ 内容创作 / 🤖 自动化办公 / 🇨🇳 中文支持

# 投资者
💰 金融分析 / 🕷️ 数据采集 / 🤖 自动化办公

# 运营/产品
🤖 自动化办公 / ✍️ 内容创作 / 🕷️ 数据采集
```

---

## 📊 频率选择指南

| 频率 | 适合场景 | 优缺点 |
|------|---------|--------|
| **每日 1 次** | 重度用户、跟热点 | 信息量大、推送频繁 |
| **每 2 天 1 次** ⭐ | 通用推荐（默认） | 平衡点、不打扰 |
| **每周 1 次** | 周末回顾、深度阅读 | 信息密度高 |
| **每月 1 次** | 长尾发现、避免打扰 | 易错过热点 |

**推荐**：每 2 天 1 次（与 10 天去重窗口完美匹配 → 5 个独立周期全覆盖 200 个 Skill）。

---

## ⚙️ Cron 表达式速查

```
0 13 */2 * *   →  每 2 天 13:00（北京时间 21:00）
0 9 * * *      →  每天 9:00
0 8 * * 1      →  每周一 8:00
0 0 1 * *      →  每月 1 日 0:00
```

字段：`分 时 日 月 周`

---

## 🐛 故障排查

**Cron 跑了但没飞书消息？**
1. 检查 `references/config.json` 凭证是否正确
2. 看 cron 日志（`logs/cron.log` 或任务计划程序历史）
3. 手动跑一次 `python clawhub_daily_executor.py` 排查

**推送重复了？**
- 检查 10 天去重是否生效（`data/recommended/` 是否有最近 10 天的 JSON）
- 减小 cron 频率（每 2 天 → 每 3 天）

**想换推送时间？**
- 修改 `cron` 表达式
- 用 https://crontab.guru 验证
