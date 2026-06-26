# 招聘邮件监控系统 - 安装配置指南

## 🚀 快速安装（5 分钟搞定）

### 步骤 1: 下载 Skill

```bash
# 从 ClawHub 安装（如果已发布）
clawhub install recruit-email-monitor

# 或手动下载后复制到 skills 目录
cp -r /path/to/recruit-email-monitor ~/.openclaw/workspace/skills/
```

### 步骤 2: 安装依赖

```bash
pip3 install openpyxl
```

### 步骤 3: 配置邮箱账号

编辑 `scripts/email-heartbeat-check.py`，修改第 16-30 行：

```python
EMAIL_ACCOUNTS = [
    {
        'name': 'QQ 邮箱',
        'user': '你的 QQ 号@qq.com',
        'password': '你的授权码',  # ⚠️ 不是登录密码！
        'host': 'pop.qq.com',
        'port': 995,
    },
    {
        'name': '163 邮箱',
        'user': '你的账号@163.com',
        'password': '你的授权码',
        'host': 'pop.163.com',
        'port': 995,
    }
]
```

**获取授权码：**
- **QQ 邮箱**: 设置 → 账户 → 开启 POP3/SMTP 服务 → 生成授权码
- **163 邮箱**: 设置 → POP3/SMTP/IMAP → 开启服务 → 获取授权码

### 步骤 4: 配置飞书通知

编辑 `scripts/email-heartbeat-check.py` 和 `scripts/email-daily-briefing.py`，找到飞书发送命令：

```python
# 修改这一行中的用户 ID 为你的飞书 ID
'--target', 'user:ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

**获取飞书 ID：**
- 方法 1: 在飞书中查看自己的个人资料，复制用户 ID
- 方法 2: 使用 OpenClaw 命令：`openclaw message whoami --channel feishu`

### 步骤 5: 配置定时任务

```bash
# 进入 OpenClaw 目录
cd ~/.openclaw

# 导入定时任务配置
openclaw cron import /path/to/recruit-email-monitor/cron-jobs.json
```

**或手动添加 crontab：**

```bash
crontab -e

# 添加以下两行
0 * * * * python3 /path/to/scripts/email-heartbeat-check.py
0 9 * * * python3 /path/to/scripts/email-daily-briefing.py
```

### 步骤 6: 创建 Excel 表格（可选）

首次运行时会自动创建表格，你也可以手动创建：

```bash
# 复制示例表格（如果有）
cp /path/to/招聘邮件汇总.xlsx /your/preferred/path/

# 或在脚本中修改路径
# 编辑 email-heartbeat-check.py 第 51 行
EXCEL_PATH = '/your/path/招聘邮件汇总.xlsx'
```

### 步骤 7: 测试运行

```bash
# 测试邮箱检查
python3 scripts/email-heartbeat-check.py

# 测试简报生成
python3 scripts/email-daily-briefing.py
```

---

## ✅ 验证安装

### 检查定时任务

```bash
# 查看 OpenClaw cron 任务
cat ~/.openclaw/cron/jobs.json | grep -A 5 "recruit-email"
```

### 检查日志

```bash
# 查看最近的运行记录
cat ~/.openclaw/cron/runs/*.jsonl | grep "recruit-email" | tail -10
```

### 手动触发测试

```bash
# 运行一次检查
python3 scripts/email-heartbeat-check.py

# 你应该看到类似输出：
# 🔍 心跳检查：招聘邮件监控
# ✅ 没有新的招聘邮件
# 或
# 📧 发现新招聘邮件 [QQ 邮箱]:
#    主题：【xxx】...
# ✅ Feishu 通知已发送
```

---

## 📁 完整目录结构

```
recruit-email-monitor/
├── SKILL.md                      # 技能说明文档
├── _meta.json                    # 技能元数据
├── cron-jobs.json                # 定时任务配置（可导入）
├── INSTALL.md                    # 本文件
└── scripts/
    ├── email-heartbeat-check.py  # 心跳检查脚本
    └── email-daily-briefing.py   # 每日简报脚本
```

---

## 🔧 配置项清单

| 配置项 | 文件 | 位置 | 说明 |
|--------|------|------|------|
| 邮箱账号 | `email-heartbeat-check.py` | 第 16-30 行 | QQ/163 等邮箱配置 |
| 邮箱授权码 | `email-heartbeat-check.py` | 第 16-30 行 | 必须是授权码，不是登录密码 |
| 飞书用户 ID | 两个脚本 | 约第 155 行 | 接收通知的飞书 ID |
| Excel 路径 | `email-heartbeat-check.py` | 第 51 行 | 邮件汇总表格路径 |
| 简报路径 | `email-daily-briefing.py` | 第 15 行 | 简报输出文件路径 |
| 检查频率 | `cron-jobs.json` | 第 10 行 | 默认每小时 (`0 * * * *`) |
| 简报时间 | `cron-jobs.json` | 第 26 行 | 默认每天 9 点 (`0 9 * * *`) |

---

## 🎯 预期效果

安装配置完成后，系统会：

1. **每小时自动检查邮箱**
   - 扫描 QQ 邮箱、163 邮箱
   - 识别招聘相关邮件（笔试、面试、Offer 等）
   - 自动记录到 Excel 表格
   - 发现新邮件时立即发送飞书通知

2. **每天早上 9:00 发送简报**
   - 汇总所有待处理邮件
   - 标记即将截止的任务
   - 发送飞书消息

3. **自动化运行**
   - 无需手动干预
   - 出错时会在日志中记录

---

## ❓ 常见问题

### Q: 授权码在哪里获取？
**A:** 
- QQ 邮箱：设置 → 账户 → POP3/SMTP 服务 → 生成授权码
- 163 邮箱：设置 → POP3/SMTP/IMAP → 开启服务 → 获取授权码

### Q: 飞书通知没收到？
**A:**
1. 检查飞书用户 ID 是否正确
2. 确认 OpenClaw 已配置飞书插件
3. 查看脚本运行日志是否有错误

### Q: 定时任务不执行？
**A:**
1. 检查 cron 配置是否正确导入：`openclaw cron list`
2. 确认 OpenClaw Gateway 正在运行
3. 查看 cron 日志：`cat ~/.openclaw/cron/runs/*.jsonl`

### Q: 表格无法写入？
**A:**
1. 检查文件路径权限：`ls -l /path/to/招聘邮件汇总.xlsx`
2. 确保 Excel 文件未被其他程序打开
3. 首次运行会自动创建表格

### Q: 想修改邮件分类规则？
**A:** 编辑 `email-heartbeat-check.py` 中的关键词列表：
```python
RECRUITMENT_KEYWORDS = [...]  # 招聘相关关键词
HIGH_PRIORITY_KEYWORDS = [...]  # 高优先级关键词
```

---

## 📞 获取帮助

- 查看完整文档：`cat SKILL.md`
- 检查技能元数据：`cat _meta.json`
- 查看运行日志：`cat ~/.openclaw/cron/runs/*.jsonl | tail -20`

---

**祝你使用愉快！如有问题欢迎反馈！** 🍊
