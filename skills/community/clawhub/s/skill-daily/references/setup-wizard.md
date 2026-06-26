# 首次安装向导（Setup Wizard）

> 适用版本：clawhub-daily v1.0.0+
> 用户首次安装本技能后必读

## 🎯 选择你的使用模式

ClawHub Daily 提供 **2 种使用模式**，请根据你的需求选择 A 或 B。

---

### 模式 A：常规对话模式 💬

**适合**：每天手动触发、AI 对话中临时调用

**触发词**（在 Agent 对话中输入任一即可）：
- "每日推荐"
- "ClawHub 日报"
- "今天有什么好 Skill"
- "帮我推荐技能"
- "扫描 ClawHub"

**示例对话**：
```
你: 每日推荐
AI: 🦞 ClawHub 每日洞察 | 2026-06-03（质量维度）
    扫描 198 个 Skill → 推荐 10 个新发现...
```

**优点**：
- ✅ 灵活，按需触发
- ✅ 可以临时调整关注点
- ✅ 不需要定时任务

**缺点**：
- ❌ 容易忘记
- ❌ 没有自动推送

---

### 模式 B：Cron 定时任务模式 ⏰

**适合**：每天定时自动推送、长期稳定使用

**支持平台**：
- **qclaw / WorkBuddy / OpenClaw / Hermes** — 使用各平台 Cron 配置
- **Trae SOLO** — 使用 `Schedule` 工具（已为你集成）
- **纯脚本** — Linux/Mac crontab 或 Windows Task Scheduler

**触发节奏**（推荐）：
- **每 2 天一次**：抓取 200 个 Skill，覆盖 10 天滚动窗口
- **每日 1 次**：抓取 200 个 Skill，新发现会更多
- **每周 1 次**：信息密度高但容易错过热点

**预制 Cron 提示词**：见 [prompt-templates.md](prompt-templates.md)

**优点**：
- ✅ 自动化，无需手动触发
- ✅ 飞书/IM 推送主动送达
- ✅ 长期稳定运行

**缺点**：
- ❌ 初次配置稍复杂
- ❌ 故障不易发现（需加监控）

---

## 🔧 通用配置（两种模式都需要）

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置飞书凭证（仅需推送时）

#### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`
4. 权限配置：
   - `im:message` — 发送消息
   - `im:message:send_as_bot` — 以应用身份发消息
   - `docx:document:create` — 创建云文档
   - `docx:document:write` — 编辑云文档
5. 事件订阅：可跳过（不需要接收消息）

#### 步骤 2：填写凭证

编辑 `references/config.json`：

```json
{
  "feishu_app_id": "<your_app_id>",
  "feishu_app_secret": "<your_app_secret>",
  "feishu_user_open_id": "<your_user_open_id>"
}
```

> ⚠️ **请勿将此文件提交到 GitHub**！建议加入 `.gitignore`。

#### 步骤 3：获取 user_open_id

让目标用户**给应用发一条任意消息**，然后在飞书管理后台查看"用户与部门"即可找到对应的 `open_id`。

---

### 3. 测试运行

```bash
# 1. 抓取数据
python scripts/fetch_clawhub.py --date 2026-06-03

# 2. 计算指标
python scripts/compute_metrics.py --input data/snapshots/2026-06-03.json

# 3. 生成推荐
python scripts/daily_recommend.py --date 2026-06-03 --data-dir data

# 4. 推送到飞书
python scripts/push_to_feishu.py --recommendation data/recommended/2026-06-03.json
```

预期：飞书收到一条带 200-400 字摘要的卡片消息 + 一个云文档链接。

---

## 📋 模式选择决策树

```
你希望什么时候看到推荐？
│
├─ "我想每天主动查看"        → 模式 A
│
├─ "我想每天自动收到推送"    → 模式 B（每天 1 次）
│
├─ "我想隔天看一次就够了"    → 模式 B（每 2 天 1 次）⭐ 推荐
│
└─ "我只想周末看"            → 模式 B（每周 1 次）
```

---

## 🔄 模式切换

随时可以切换模式：
- A → B：参考 [prompt-templates.md](prompt-templates.md) 配置 Cron
- B → A：删除 Cron 配置，回到对话触发

---

## ❓ 常见问题

**Q1：必须配置飞书吗？**
A：不必。飞书是可选的，模式 A 完全不需要飞书，模式 B 也可以只生成本地简报不推送（用 `--skip-push`）。

**Q2：每天扫描会不会很慢？**
A：不会。抓取 200 个 Skill 仅需 10-15 秒，**不调大模型**（0 token 消耗）。

**Q3：可以同时用 A 和 B 吗？**
A：可以。模式 B 自动推送后，你仍可以在对话中输入"每日推荐"立即查看最新数据。

**Q4：配置文件被提交到 GitHub 怎么办？**
A：立即在飞书开放平台**重置 App Secret**。`references/config.json` 已加入 `.gitignore` 建议列表。

---

## 📚 下一步

- 模式 A 用户：直接看 [README.md](../README.md) 的"快速开始"
- 模式 B 用户：看 [prompt-templates.md](prompt-templates.md) 配置 Cron
- 双模式用户：两个都看
