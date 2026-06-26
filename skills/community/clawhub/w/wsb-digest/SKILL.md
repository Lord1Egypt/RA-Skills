---
name: wsb-digest
description: 自动抓取 r/wallstreetbets 热股数据，生成每日报告推送到 Discord。使用 ApeWisdom API，支持分片发送避免 Discord 2000 字符限制。
version: "1.0.0"
author: mingkko
homepage: https://github.com/mingkko/wsb-digest
---

# WSB Digest Skill

自动监控 WallStreetBets (WSB) 热门股票，每日生成热股报告并推送到 Discord。

## 功能特点

- 📊 **自动抓取**: 从 ApeWisdom API 获取 WSB 热股数据
- 📈 **多维度分析**: 提及次数、排名变化、情绪分数
- 🚀 **趋势识别**: 自动识别快速上升股票
- 🆕 **新上榜**: 追踪首次进入榜单的股票  
- ✂️ **智能分片**: 超长内容自动分片发送，避免 Discord 截断
- ⏰ **定时推送**: 支持 cron 定时任务

## 数据来源

- **ApeWisdom API**: https://apewisdom.io/api/v1.0/filter/wallstreetbets
- 覆盖: 股票代码、提及次数、排名变化、Upvotes 数据

## 安装步骤

### 1. 安装 Skill

```bash
# 在你的 OpenClaw workspace 中
cd ~/.openclaw/workspace/skills
git clone https://github.com/mingkko/wsb-digest.git
# 或者手动复制本文件夹到 skills/wsb-digest/
```

### 2. 安装依赖

本 skill 仅依赖 Node.js (v18+)，无需额外 npm 包。

### 3. 配置 Discord 频道

编辑 `scripts/wsb-digest-trigger.sh`，修改以下变量：

```bash
# Discord 频道 ID（必须修改！）
TARGET_CHANNEL_ID="你的频道ID"

# OpenClaw 可执行文件路径（根据你的安装调整）
OPENCLAW_BIN=/root/.local/share/pnpm/openclaw
```

获取 Discord 频道 ID：
1. Discord 设置 → 高级 → 开启开发者模式
2. 右键点击频道 → 复制频道 ID

### 4. 设置定时任务

```bash
crontab -e

# 添加以下行（每天北京时间 9:00 和 21:00 推送）
0 9,21 * * * /root/.openclaw/workspace/skills/wsb-digest/scripts/wsb-digest-trigger.sh
```

### 5. 测试运行

```bash
# 手动运行测试
/root/.openclaw/workspace/skills/wsb-digest/scripts/wsb-digest-trigger.sh
```

## 输出格式示例

```
📊 **WSB 每日热股报告**

⏰ 2026/03/04 09:00 (北京时间)
📈 数据来源: ApeWisdom (r/wallstreetbets)
📊 总提及股票: 643 只

## 🔥 TOP 15 热门股票

1. **$SPY** 🟢🟢🟢
   📊 200 次提及 (+29.0%)
   👍 2301 upvotes
   📈 ➡️ 持平
   🏢 SPDR S&P 500 ETF Trust

2. **$NVDA** 🟢🟢🟢
   📊 65 次提及 (-17.7%)
   👍 296 upvotes
   📈 ➡️ 持平
   🏢 NVIDIA

## 🚀 快速上升股票

↗️ **$UAE**: 上升 42 位 (从 #45 → #3) 🔥
↗️ **$USO**: 上升 51 位 (从 #59 → #8) 🔥

---
📝 数据来自 ApeWisdom API | ⏰ 每日 9:00 & 21:00 更新
⚠️ 仅供参考，不构成投资建议
```

## 文件结构

```
wsb-digest/
├── SKILL.md                     # 本文件
├── scripts/
│   ├── apewisdom-wsb.js        # 核心抓取脚本
│   └── wsb-digest-trigger.sh   # Discord 推送脚本
└── references/
    └── install-guide.md        # 详细安装指南
```

## 配置说明

### 修改推送时间

编辑 crontab：
```bash
crontab -e
```

Cron 格式说明：
```
# 每天 9:00 和 21:00（北京时间）
0 9,21 * * * /path/to/wsb-digest-trigger.sh

# 每天 12:00 一次
0 12 * * * /path/to/wsb-digest-trigger.sh

# 每 6 小时一次
0 */6 * * * /path/to/wsb-digest-trigger.sh
```

### 调整显示数量

编辑 `scripts/apewisdom-wsb.js`：

```javascript
// 修改 TOP N 数量（默认 15）
const stocks = data.results.slice(0, 15);

// 修改快速上升股票数量（默认 5）
const trending = data.results.filter(...).slice(0, 5);
```

### 自定义模板

在 `apewisdom-wsb.js` 中修改 `generateDigest()` 函数的 output 拼接部分。

## 故障排除

### 问题：脚本提示 "node: command not found"

**解决**: 确保 Node.js 已安装，并在脚本中正确设置 PATH：
```bash
export PATH="/usr/bin:/usr/local/bin:$PATH"
```

### 问题：Discord 消息发送失败

**解决**: 
1. 检查 `TARGET_CHANNEL_ID` 是否正确
2. 确保 OpenClaw 有该频道的发送权限
3. 检查 `openclaw` 命令路径是否正确

### 问题：抓取返回空数据

**解决**:
- ApeWisdom API 偶尔会有波动，脚本会自动重试 3 次
- 检查网络连接是否正常
- 查看日志：`tail -f /tmp/wsb-digest.log`

## 日志查看

```bash
# 实时查看日志
tail -f /tmp/wsb-digest.log

# 查看最近 50 行
tail -n 50 /tmp/wsb-digest.log
```

## 更新

```bash
cd ~/.openclaw/workspace/skills/wsb-digest
git pull
```

## License

MIT

## 致谢

- 数据来源: [ApeWisdom](https://apewisdom.io/)
- 原始社区: r/wallstreetbets
