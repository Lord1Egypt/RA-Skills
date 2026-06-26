---
name: screen-life
version: 1.0.0
description: "macOS 数字生活日报：自动监控你每天在电脑上做什么，生成可读的行为报告。零配置，一键安装，后台静默运行。当用户想看今天用电脑做了什么、分析效率、查看应用使用时长时触发。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      platform: ["darwin"]
      pip: ["python-dotenv"]
    llm:
      required: false
      purpose: "对日报数据做行为洞察和效率建议"
      env:
        - name: OPENCLAW_LLM_API_KEY
          description: "大模型 API Key（OpenClaw 自动注入）"
        - name: OPENCLAW_LLM_BASE_URL
          description: "大模型 API 地址（OpenClaw 自动注入）"
        - name: OPENCLAW_LLM_MODEL
          description: "大模型名称（OpenClaw 自动注入）"
---

# screen-life

**自动生成你的数字生活日报。后台静默运行，每天一份报告。**

## 快速开始

```bash
cd /path/to/screen-life

# 一键安装（启动后台监控守护进程）
bash install.sh

# 查看今日报告（含 AI 洞察，需配置 LLM）
python3 handler.py

# 不含 AI 分析
python3 handler.py --no-llm
```

## LLM 配置

OpenClaw 运行时自动注入以下环境变量（无需手动配置）：

| 变量 | 说明 |
|------|------|
| `OPENCLAW_LLM_API_KEY` | OpenClaw 当前 LLM 的 API Key |
| `OPENCLAW_LLM_BASE_URL` | API 地址（标准 Chat Completions 格式） |
| `OPENCLAW_LLM_MODEL` | OpenClaw 当前选用的模型标识 |

三个变量均未注入时，跳过 AI 分析，仅输出原始日报。

## 命令

```bash
# 今日报告（含 AI 洞察）
python3 handler.py

# 今日报告（不含 AI）
python3 handler.py --no-llm

# 指定日期
python3 handler.py --date 2026-04-10

# 本周汇总
python3 handler.py --week

# JSON 输出
python3 handler.py --format json

# 推送到飞书
python3 handler.py --push feishu

# 管理守护进程
bash install.sh status    # 查看状态
bash install.sh stop      # 停止监控
bash install.sh restart   # 重启
bash install.sh uninstall # 卸载
```

## 输出示例

```
🖥️ 2026-04-11 数字生活日报

⏱️ 应用使用 TOP 5
  VS Code       4h 23m  ████████████  35%
  Chrome        3h 12m  █████████     26%
  AI 助手        2h 45m  ████████      22%
  微信          0h 48m  ██             6%
  Terminal      0h 32m  █              4%

🔍 浏览器热词（今日搜索 / 访问）
  AI编程 ×12  |  stock-analyzer ×8  |  飞书API ×5

📝 Obsidian 笔记变更
  新增 3 篇  |  修改 12 篇
  最活跃目录: 20_Project/OpenClaw/

💬 AI 工具使用摘要
  对话工具: 23 轮  |  主题: Skill开发、量化交易

📊 专注度评分: 82/100  🟢
  建议: 下午 3-4 点切换频率较高，可尝试设置专注时段
```

## 数据来源

| 来源 | 数据 | 权限要求 |
|------|------|----------|
| macOS NSWorkspace | 应用名称、使用时长 | 无 |
| Chrome 历史 | 搜索词、访问网站 | 无（自动） |
| Safari 历史 | 同上 | 完全磁盘访问（可选） |
| Obsidian git | 笔记新增/修改 | 无 |
| Cursor 对话 | AI 使用摘要 | 无 |

## 文件位置

```
~/.orbitos-monitor/
├── logs/            # 每日 JSONL 原始日志
│   └── 2026-04-11.jsonl
├── daemon.pid       # 守护进程 PID
└── daemon.log       # 运行日志
```

> **隐私说明**: 所有数据仅存储在本地 `~/.orbitos-monitor/`，不上传任何内容。
