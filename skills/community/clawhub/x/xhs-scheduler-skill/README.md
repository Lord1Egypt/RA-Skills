# 📝 小红书智能排期发布器 (XHS Smart Scheduler)

一个基于 OpenClaw 的 Skill，帮助内容创作者实现小红书内容的自动化排期和定时发布。

## ✨ 核心功能

- 📅 **内容队列管理** - 批量添加、编辑、删除待发布内容
- 🎯 **智能排期推荐** - 基于粉丝活跃时间推荐最佳发布时段
- ⏰ **定时自动发布** - 按计划自动发布，无需人工值守
- 📊 **发布状态追踪** - 实时查看发布进度和历史记录
- 🔔 **多渠道通知** - 支持飞书、钉钉、Telegram通知

## 🚀 快速开始

### 前置要求

1. **安装 OpenClaw** - 确保 OpenClaw 已正确安装并运行
2. **安装小红书 MCP 服务**
   ```bash
   # 下载 xiaohongshu-mcp
   git clone https://github.com/xpzouying/xiaohongshu-mcp.git
   cd xiaohongshu-mcp
   
   # 启动 MCP 服务
   go run . server
   # 服务将运行在 http://localhost:18060
   ```
3. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

### 安装 Skill

1. 将本 Skill 复制到 OpenClaw 的 skills 目录
   ```bash
   cp -r xhs-scheduler-skill ~/.openclaw/workspace/skills/
   ```

2. 重启 OpenClaw 网关
   ```bash
   openclaw gateway restart
   ```

3. 验证安装
   ```
   检查小红书登录状态
   ```

## 📖 使用指南

### 1. 检查登录状态

```
检查小红书登录状态
```

首次使用需要扫码登录小红书账号。

### 2. 添加内容到队列

```
添加小红书内容到发布队列
标题：春季护肤的5个误区
内容：春天到了，很多姐妹开始换护肤品...
图片：/path/to/image1.jpg, /path/to/image2.jpg
标签：护肤,春季,美妆
建议发布时间：明天上午10点
```

### 3. 查看发布队列

```
查看我的小红书发布队列
```

### 4. 智能排期推荐

```
为队列中的内容推荐最佳发布时间
```

### 5. 启动定时发布

```
启动小红书定时发布任务
```

### 6. 查看发布统计

```
查看本周小红书发布统计
```

## ⚙️ 配置说明

编辑 `config.yaml` 文件进行自定义配置：

```yaml
# MCP服务地址
mcp_server_url: "http://localhost:18060/mcp"

# 检查间隔（秒）
check_interval: 300

# 通知配置
feishu_webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

## 💰 定价策略

| 版本 | 功能 | 价格 |
|:---|:---|:---:|
| **免费版** | 5篇/天，基础定时 | Free |
| **基础版** | 20篇/天，智能排期，飞书通知 | $29/月 |
| **专业版** | 无限篇，多账号，数据分析 | $49/月 |

## 📁 项目结构

```
xhs-scheduler-skill/
├── SKILL.md              # OpenClaw Skill 定义文件
├── README.md             # 项目说明
├── config.yaml           # 配置文件
├── requirements.txt      # Python依赖
├── scripts/
│   ├── queue_manager.py  # 队列管理
│   ├── scheduler.py      # 定时调度
│   ├── smart_timing.py   # 智能排期算法
│   ├── publisher.py      # 发布执行
│   └── notifier.py       # 通知模块
└── data/                 # 数据存储目录
```

## 🔧 命令行工具

### 队列管理

```bash
# 添加任务
python scripts/queue_manager.py add \
  --title "测试标题" \
  --content "测试内容" \
  --images "/path/img1.jpg,/path/img2.jpg" \
  --tags "标签1,标签2" \
  --schedule "2026-03-30T10:00:00"

# 列出任务
python scripts/queue_manager.py list

# 查看待发布
python scripts/queue_manager.py pending

# 删除任务
python scripts/queue_manager.py delete <task_id>

# 查看统计
python scripts/queue_manager.py stats
```

### 智能排期

```bash
# 获取推荐时间
python scripts/smart_timing.py --type fashion --count 3

# 批量排期
python scripts/smart_timing.py --batch 10 --type beauty
```

### 发布测试

```bash
# 检查登录
python scripts/publisher.py check-login

# 发布图文
python scripts/publisher.py publish \
  --title "测试" \
  --content "内容" \
  --images "/path/img.jpg"
```

### 启动调度器

```bash
# 持续运行
python scripts/scheduler.py

# 只执行一次
python scripts/scheduler.py --once

# 查看状态
python scripts/scheduler.py --status
```

## ⚠️ 注意事项

1. **发布频率限制** - 建议单账号每天不超过 10 篇，避免触发风控
2. **内容合规** - 确保发布内容符合小红书社区规范
3. **网络稳定** - 发布时需要保持网络连接稳定
4. **Cookie 有效期** - 登录状态通常保持 30 天，过期需重新登录

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License

## 💬 支持

如有问题，请通过以下方式联系：

- GitHub Issues: [your-repo]/xhs-scheduler-skill
- 邮箱: sxzxlj@163.com

---

**免责声明**：本工具仅供学习研究使用，请遵守小红书平台规则和相关法律法规。
