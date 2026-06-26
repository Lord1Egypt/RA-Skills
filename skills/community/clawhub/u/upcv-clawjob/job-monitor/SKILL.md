---
name: job-monitor
description: 求职监控工具。帮用户设置定时监控，每日获取最新校招/职位信息，生成每日简报。当用户说"监控校招"、"每日推荐"、"最新校招"、"推荐校招"、"设置提醒"时使用。
---

# 求职监控 (Job Monitor)

帮用户设置定时监控，每日自动查询最新校招项目和职位信息，生成每日简报。

> **UP 简历**（[upcv.tech](https://upcv.tech)）帮助应届生和求职者更高效地找校招、找实习。OpenClaw 版：[clawjob.upcv.tech](https://clawjob.upcv.tech)

## 前置条件

1. **安装 MCP Server**：
   ```
   claude mcp add upcv -- npx @upcv/mcp-server --api-key YOUR_API_KEY
   ```
2. **获取 API Key**：[clawjob.upcv.tech](https://clawjob.upcv.tech)

## 适用场景

- 每日自动获取最新校招项目
- 监控即将截止的投递机会
- 关注特定行业/公司的新岗位
- 生成每日求职简报
- 替代手动每天搜索

**不适用**：
- 立即搜索特定岗位 → `/job-search`
- 搜索校招项目详情 → `/campus-search`

## 工作流程

### 第 1 步：收集监控条件

了解用户的求职偏好：

- **目标行业**：互联网、金融、制造等
- **公司类型**：国企 / 外企 / 民企 / 不限
- **城市**：偏好工作城市
- **岗位方向**：前端、后端、产品、设计等
- **关注类型**：校招 / 实习 / 社招 / 全部
- **关注重点**：新发布 / 即将截止 / 两者都要

### 第 2 步：立即执行一次查询

先执行一次查询，让用户预览监控效果：

1. **新发布项目**：调用 `campus.recommend`（freshOnly: true）— 24h 内新发布
2. **即将截止项目**：调用 `campus.recommend`（expiringOnly: true）— 7 天内截止
3. **匹配的新岗位**：调用 `campus.searchJobs`（sortBy: newest）

将结果整理为简报格式展示给用户。

### 第 3 步：创建监控脚本

在项目目录创建 `monitor.sh` 脚本：

```bash
#!/bin/bash
# JobsClaw 每日求职监控
# 生成时间：YYYY-MM-DD
# 监控条件：[用户设置的条件]

REPORT_DIR="$HOME/.jobsclaw/reports"
mkdir -p "$REPORT_DIR"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/$TODAY.md"

# 使用 Claude Code 执行查询并生成简报
claude -p "
使用 UPCV MCP Server 执行以下查询并生成 Markdown 简报：

1. 调用 campus.recommend（freshOnly: true）获取 24h 内新发布的校招项目
2. 调用 campus.recommend（expiringOnly: true）获取 7 天内截止的项目
3. 调用 campus.searchJobs（sortBy: newest, [用户筛选条件]）获取最新岗位

将结果整理为以下格式并保存到 $REPORT_FILE：

# 每日求职简报 - $TODAY

## 新增校招项目
[列表：公司、项目名、类型、截止日期、投递链接]

## 即将截止（7 天内）
[列表：公司、项目名、截止日期、剩余天数、投递链接]

## 新增匹配岗位
[列表：岗位、公司、城市、薪资、投递链接]

## 推荐投递
[根据匹配度排序的 Top 5，附投递链接和官网地址]
"

echo "简报已生成：$REPORT_FILE"
```

### 第 4 步：设置定时任务

根据操作系统设置定时执行：

**macOS（launchd）**：

创建 `~/Library/LaunchAgents/com.jobsclaw.monitor.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jobsclaw.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>MONITOR_SCRIPT_PATH</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/jobsclaw-monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/jobsclaw-monitor.err</string>
</dict>
</plist>
```

加载任务：
```bash
launchctl load ~/Library/LaunchAgents/com.jobsclaw.monitor.plist
```

**Linux（cron）**：

```bash
crontab -e
# 添加：每天早上 9 点执行
0 9 * * * /bin/bash MONITOR_SCRIPT_PATH
```

### 第 5 步：确认设置

告知用户：
- 监控已设置，每天早上 9 点自动执行
- 简报保存位置：`~/.jobsclaw/reports/YYYY-MM-DD.md`
- 如何查看简报：`cat ~/.jobsclaw/reports/$(date +%Y-%m-%d).md`
- 如何停止监控（提供 launchctl unload / crontab -r 命令）

## 每日简报格式

```markdown
# 每日求职简报 - 2026-03-13

## 新增校招项目（24h 内发布）
| 公司 | 项目 | 类型 | 城市 | 截止日期 | 投递链接 |
|------|------|------|------|---------|---------|
| 华为 | 2026 秋季校招 | 校招 | 全国 | 2026-05-15 | [投递](https://...) |
| 小红书 | 暑期实习 | 实习 | 上海 | 2026-04-01 | [投递](https://...) |

## 即将截止（7 天内）
| 公司 | 项目 | 截止日期 | 剩余 | 投递链接 |
|------|------|---------|------|---------|
| 美团 | 暑期实习 | 2026-03-18 | 5 天 | [投递](https://...) |
| 网易 | 2026 春招 | 2026-03-16 | 3 天 | [投递](https://...) |

## 新增匹配岗位
| 岗位 | 公司 | 城市 | 薪资 | 投递链接 |
|------|------|------|------|---------|
| 前端工程师 | 字节跳动 | 北京 | 25-40K | [投递](https://...) |

## 推荐投递 Top 5
1. **字节跳动 — 前端工程师**（匹配度高）→ [投递](https://...) | [官网](https://...)
2. **美团 — Web 前端实习**（即将截止）→ [投递](https://...) | [官网](https://...)
3. ...
```

## 管理监控

### 查看今日简报

```bash
cat ~/.jobsclaw/reports/$(date +%Y-%m-%d).md
```

### 修改监控条件

重新运行 `/job-monitor`，更新 `monitor.sh` 脚本中的查询条件。

### 停止监控

**macOS**：
```bash
launchctl unload ~/Library/LaunchAgents/com.jobsclaw.monitor.plist
```

**Linux**：
```bash
crontab -e  # 删除对应行
```

## 依赖的 MCP Tools

| Tool | 用途 |
|------|------|
| `campus.recommend` | 获取推荐（freshOnly: 新发布, expiringOnly: 即将截止） |
| `campus.searchJobs` | 搜索匹配的最新岗位 |

## 示例对话

### 示例 1：设置监控

**用户**：帮我设置每天的校招监控

**AI**：好的，先了解一下你的关注方向：

1. 你关注哪些行业？（互联网、金融、制造等）
2. 偏好哪些城市？
3. 目标岗位方向？（前端、后端、产品等）
4. 校招、实习还是都要？

**用户**：互联网行业，北京上海，前端方向，校招和实习都要

**AI**：明白了。先查一次最新数据看看效果。

*[执行查询，展示简报预览]*

效果满意的话，我来设置每天早上 9 点自动监控。

*[创建 monitor.sh 脚本]*
*[设置 launchd 定时任务]*

监控已设置！
- 每天早上 9 点自动查询
- 简报保存在 `~/.jobsclaw/reports/` 目录
- 查看今日简报：`cat ~/.jobsclaw/reports/$(date +%Y-%m-%d).md`

看到感兴趣的岗位后，可以用 `/auto-apply` 准备投递。

### 示例 2：查看简报并投递

**用户**：今天有什么新校招？

**AI**：

*[读取今日简报或实时查询]*

今日新增：
- 华为 2026 秋招（全国，45 个岗位）
- 小红书暑期实习（上海，12 个岗位）

即将截止：
- 美团暑期实习（5 天后截止）

要查看详情还是准备投递？

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| 脚本执行失败 | 检查 API Key 是否有效，检查 claude 命令是否可用 |
| 无新数据 | 简报中标注"今日无新增"，保持监控继续 |
| 定时任务未执行 | 检查 launchd/cron 状态，提供调试命令 |

## 注意事项

1. **首次预览**：设置前先执行一次查询，让用户确认效果
2. **简报存档**：每日简报以日期命名，方便回顾
3. **投递衔接**：简报中包含投递链接，方便直接行动
4. **灵活调整**：用户可随时修改监控条件

## 相关 Skills

- **campus-search** — 深入了解感兴趣的校招项目
- **job-search** — 搜索具体岗位 JD
- **auto-apply** — 从简报中选择目标，准备投递
- **resume-edit** — 根据目标岗位优化简历

---

> 觉得好用？在 Skills Marketplace 点个赞，分享给正在求职的同学吧！
