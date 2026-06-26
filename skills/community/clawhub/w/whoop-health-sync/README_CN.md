# WHOOP → AI 健康日报 🏋️

[English README](README.md)

把 WHOOP 手环数据变成每日 AI 健康报告。5 步搞定，10 分钟。

## 工作原理

```
WHOOP 手环 → WHOOP API → Markdown 文件 → AI 读取并生成报告
```

AI 助手每天自动同步你的恢复、睡眠、负荷和运动数据，然后发给你一份通俗易懂的健康简报。

## 快速开始

### 第 1 步：安装

```bash
# OpenClaw 用户（一键）
clawhub install whoop

# 或手动安装
git clone https://github.com/aikong-cmd/whoop-openclaw.git
cp -r whoop-openclaw ~/.openclaw/workspace/skills/whoop
```

### 第 2 步：创建 WHOOP 开发者应用

打开 **https://developer-dashboard.whoop.com** → Create Application：

| 字段 | 填什么 |
|------|--------|
| Name | 随便填，比如 "AI Health Sync" |
| Redirect URI | `http://localhost:9527/callback` |
| Scopes | ✅ 勾选所有 `read:*` + `offline` |

保存你的 **Client ID** 和 **Client Secret**。

### 第 3 步：配置凭证

```bash
export WHOOP_CLIENT_ID="你的-client-id"
export WHOOP_CLIENT_SECRET="你的-client-secret"
```

### 第 4 步：授权（只需一次）

**本地电脑（有浏览器）：**

```bash
cd ~/.openclaw/workspace/skills/whoop
python3 scripts/auth.py
# 自动打开浏览器 → 登录 WHOOP → 点授权 → 搞定 ✅
```

**远程服务器（没浏览器）：**

```bash
python3 scripts/auth.py --print-url
# 1. 在你电脑浏览器打开这个链接
# 2. 登录 WHOOP，点授权
# 3. 浏览器会跳到一个打不开的页面（正常！）
# 4. 复制地址栏完整 URL，然后：
python3 scripts/auth.py --callback-url "粘贴完整URL"
```

看到 `✅ Tokens saved` 就成功了。这一步只需做一次，Token 永久自动续期。

### 第 5 步：同步数据

```bash
python3 scripts/sync.py           # 同步今天
python3 scripts/sync.py --days 7  # 最近 7 天
python3 scripts/sync.py --weekly  # 周报
```

数据保存在 `~/.openclaw/workspace/health/whoop-YYYY-MM-DD.md`

**搞定。** AI 助手现在可以读取这些文件，回答你的健康问题。

---

## 可选：每日自动推送

设置定时任务，让 AI 每天早上给你发健康简报：

```bash
openclaw cron add \
  --name whoop-daily \
  --schedule "30 10 * * *" \
  --timezone Asia/Shanghai \
  --task "Run: python3 ~/.openclaw/workspace/skills/whoop/scripts/sync.py --days 2. Read the latest health file and send me a report with insights."
```

> ⏰ 建议 10:30 — WHOOP 的睡眠数据要等起床后才能最终确认。

## 输出示例

```markdown
# WHOOP — 2026-03-09

## 恢复 🟢
- 恢复分数: 66%
- HRV: 41.4 ms | 静息心率: 62 bpm
- 血氧: 96.3% | 皮肤温度: 33.7°C

## 睡眠 🟡
- 表现: 61% | 在床时间: 5h47m
- 深睡 1h25m | REM 1h38m | 浅睡 2h08m | 清醒 35m
- 睡眠需求: 9h41m → 欠债: 4h29m

## 日间负荷
- 负荷: 0.1 / 21.0 | 消耗: 534 kcal

## 运动
- 步行 · 16分钟 · 负荷 4.9 · 平均心率 114 bpm
```

## 常见问题

| 问题 | 解决 |
|------|------|
| `No tokens found` | 先做第 4 步（auth.py） |
| `Token refresh failed` | 重新跑 auth.py |
| `No data for date` | WHOOP 要等起床后才有数据，稍后再试 |
| 端口 9527 被占用 | `kill $(lsof -ti:9527)` 后重试 |

## 系统要求

- Python 3.10+ 和 curl（大多数系统自带）
- WHOOP 会员 + 在用的手环

## License

MIT
