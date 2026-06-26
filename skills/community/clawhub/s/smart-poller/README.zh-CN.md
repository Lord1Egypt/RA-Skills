# Smart Poller - 智能轮询技能包

> 定时轮询飞书任务看板，自动执行分配给当前 AI 的任务。

**版本**: v1.0 | **作者**: socneo | **分类**: automation

📖 [English README](README.md)

---

## ✨ 功能特性

- ✅ **定时轮询** — 支持自定义轮询间隔（默认 15 分钟）
- ✅ **飞书集成** — 完整飞书文档 API 支持
- ✅ **静默模式** — 无任务时不发送通知，节省约 95% Token
- ✅ **任务解析** — 自动识别分配给当前 AI 的 pending 任务
- ✅ **自动反馈** — 任务完成后自动写入飞书文档
- ✅ **双语言支持** — Node.js / Python 版本均可用

---

## 📦 安装

```bash
# 方式 1: 通过 ClawHub 安装（推荐）
clawhub install smart-poller

# 方式 2: 手动复制
cp -r smart_poller /your/workspace/
cd /your/workspace/smart_poller
cp config.example.json config.json
```

---

## 🔧 配置

编辑 `config.json`:

```json
{
  "app_id": "cli_xxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "doc_token": "xxxxxxxxxxxxxxxxxxxxxxxxx",
  "assignee": "your_agent_id",
  "poll_interval_minutes": 15,
  "silent_mode": true
}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `app_id` | 飞书应用 ID | `cli_xxxxxxxxxxxxx` |
| `app_secret` | 飞书应用密钥 | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `doc_token` | 任务看板文档 ID（从 URL 获取） | `xxxxxxxxxxxxxxxxxxxxxxxxx` |
| `assignee` | 当前 AI 标识符 | `agent1` / `agent2` |
| `poll_interval_minutes` | 轮询间隔（分钟） | `15` |
| `silent_mode` | 静默模式 | `true` |

> 🔑 `app_id` 和 `app_secret` 请在 [飞书开放平台](https://open.feishu.cn/app) 获取。

---

## 🚀 使用方法

### Python 版本

```bash
# 单次执行（测试）
python3 poller.py config.json --once

# 持续轮询（生产）
python3 poller.py config.json
```

### Node.js 版本

```bash
# 单次执行（测试）
node poller.js --once

# 持续轮询（生产）
node poller.js
```

### Cron 定时（推荐生产环境）

```bash
crontab -e
# 每 15 分钟执行一次
*/15 * * * * cd /path/to/smart_poller && python3 poller.py config.json --once
```

---

## 📊 任务看板格式

Smart Poller 识别以下格式的任务：

```
[TASK-XXX-001] 【测试】验证任务看板写入功能
Assign: agent_a → agent_b  |  Priority: medium  |  Status: pending
Due: 2026-03-16  |  Created: 2026-03-16 11:30
Description: 请验证轮询机制是否正常工作。
```

**完成反馈格式：**
```
[agent_b completed] TASK-XXX-001 | Time: 2026/3/16 12:28:14 | Result: 验证成功
```

---

## 📄 许可证

MIT License

---

*最后更新: 2026-03-18*
