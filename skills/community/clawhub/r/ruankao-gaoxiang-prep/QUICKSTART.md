# 软考高项备考助手 - 快速上手指南 🚀

## 📦 技能已就绪！

技能位置：`/root/.openclaw/workspace/skills/ruankao-gaoxiang-prep/`

OpenClaw 会自动从 `workspace/skills/` 目录加载技能，无需额外配置。

---

## ⚡ 30秒快速设置（推荐）

### 步骤 1：运行自动配置脚本

```bash
cd ~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/scripts/
bash setup.sh
```

脚本会提示你输入：
1. **QQ openid**（你的QQ号对应的唯一标识）
2. **推送时间**（默认 09:00，可自定义）

### 步骤 2：在QQ中测试

发送以下消息给机器人：

```
今天的复习内容
```

如果看到推送内容，说明配置成功！✅

---

## 📱 手动配置方法

如果自动脚本无法使用，可以手动配置：

### 1. 获取你的 QQ openid

在 QQ 中与机器人对话，机器人会在日志中显示你的 openid。
格式类似：`55DE97983076AF00410248091457E495`

### 2. 创建定时任务

创建文件 `/tmp/ruankao-cron.json`：

```json
{
  "action": "add",
  "job": {
    "name": "软考高项每日推送",
    "schedule": {
      "kind": "cron",
      "expr": "0 9 * * *",
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "请执行以下任务：(1) 调用 scripts/daily_push.py 获取今天的推送内容 (2) 输出格式：'📚 软考高项每日复习 {日期}\\\\n\\\\n📖 今日重点（第X章）：\\\\n{10条重点内容}\\\\n\\\\n📝 今日英语单词：\\\\n{10个单词}\\\\n\\\\n🎯 历年真题精选（10题）：\\\\n{10道题目}\\\\n\\\\n💪 加油，坚持就是胜利！' (3) 不要回复HEARTBEAT_OK (4) 用emoji点缀让内容更生动",
      "deliver": true,
      "channel": "qqbot",
      "to": "YOUR_QQ_OPENID"
    }
  }
}
```

**重要**：将 `YOUR_QQ_OPENID` 替换为你的实际 openid。

### 3. 提交定时任务

```bash
openclaw cron create /tmp/ruankao-cron.json
```

### 4. 验证任务

```bash
# 查看所有定时任务
openclaw cron list

# 应该能看到「软考高项每日推送」任务
```

---

## 🕐 修改推送时间

### 修改 Cron 表达式

Cron 表达式格式：`分钟 小时 * * *`

| 推送时间 | Cron 表达式 |
|---------|-------------|
| 每天 8:00 | `"0 8 * * *"` |
| 每天 9:00 | `"0 9 * * *"` |
| 每天 12:00 | `"0 12 * * *"` |
| 每天 20:00 | `"0 20 * * *"` |

### 更新现有任务

```bash
# 删除旧任务
openclaw cron delete <JOB_ID>

# 创建新任务（使用新的 cron 表达式）
openclaw cron create /tmp/ruankao-cron.json
```

---

## 💬 常用命令

### 在 QQ 中使用

| 命令 | 说明 |
|------|------|
| `今天的复习内容` | 查看今日推送 |
| `今天的重点` | 查看今日章节重点 |
| `今天的英语单词` | 查看今日单词 |
| `第一章重点` | 查看第1章重点 |
| `成本管理重点` | 查看成本管理章节重点 |
| `有哪些章节` | 查看完整章节目录 |
| `软考英语单词` | 查询英语单词 |
| `设置软考备考推送` | 创建每日推送 |
| `取消软考备考推送` | 取消每日推送 |

### 命令行使用

```bash
# 查看所有定时任务
openclaw cron list

# 查看任务详情
openclaw cron get <JOB_ID>

# 删除任务
openclaw cron delete <JOB_ID>

# 测试推送脚本
cd ~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/scripts/
python3 daily_push.py
```

---

## ✅ 验证清单

配置完成后，请确认以下项目：

- [ ] 技能位于 `~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/`
- [ ] SKILL.md 文件存在
- [ ] `scripts/daily_push.py` 脚本可执行
- [ ] 定时任务已创建（`openclaw cron list`）
- [ ] 在 QQ 中发送「今天的复习内容」收到回复
- [ ] 推送时间正确（每天 09:00 或自定义时间）

---

## 🐛 故障排除

### 问题1：找不到技能

**症状**：在 QQ 中发送消息无响应

**解决**：
```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/SKILL.md

# 重启 OpenClaw Gateway
openclaw gateway restart
```

### 问题2：定时任务未执行

**症状**：到点没有收到推送

**解决**：
```bash
# 查看任务状态
openclaw cron list

# 查看 OpenClaw 日志
tail -f ~/.openclaw/logs/openclaw.log
```

### 问题3：推送内容不完整

**症状**：只收到部分内容

**解决**：
```bash
# 检查章节文件
ls -la ~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/references/

# 手动测试脚本
cd ~/.openclaw/workspace/skills/ruankao-gaoxiang-prep/scripts/
python3 daily_push.py
```

### 问题4：找不到 openclaw 命令

**症状**：`command not found: openclaw`

**解决**：
```bash
# 检查 OpenClaw 安装
which openclaw

# 如果未安装，安装 OpenClaw
npm install -g @openclaw/cli
```

---

## 📚 完整使用说明

详细使用说明请查看 [README.md](./README.md)

---

## 💡 提示

1. **首次使用**：建议先发送「今天的复习内容」测试
2. **自定义时间**：可以根据个人习惯调整推送时间
3. **章节轮询**：24章按日期循环，一年会覆盖所有章节
4. **重点记忆**：每天10条重点，长期坚持效果显著
5. **单词积累**：每天10个单词，一年积累3650个专业术语
6. **真题练习**：每天10道真题，熟悉考试题型

---

**祝你考试顺利！** 💪

如有问题，请查看 [README.md](./README.md) 或提交 Issue。
