---
name: stock-monitor-skill
description: "自动监控股票价格，突破阈值时自动发送飞书语音提醒。支持多只股票、自定义阈值、交易时间判断。"
---

# Stock Monitor Skill - 股票自动监控技能

自动监控股票价格，突破阈值时自动发送语音提醒！

## 🎯 功能特点

- ✅ **实时监控**：支持 A 股/港股/美股
- ✅ **语音提醒**：突破阈值自动发飞书语音条
- ✅ **多股票支持**：同时监控多只股票
- ✅ **自定义阈值**：每只股票独立设置涨跌阈值
- ✅ **交易时间判断**：自动跳过非交易时间
- ✅ **智能防打扰**：午休时间不提醒

## 📋 使用场景

- 📈 短线交易：监控关键价位突破
- 💼 上班族：没空看盘，自动提醒
- 🎯 止盈止损：到达目标价自动通知
- 🔔 异动提醒：大涨大跌不错过

## 🔧 前置要求

### 1. Feishu 应用配置

同 Feishu Voice Skill

### 2. 股票数据源

使用新浪财经免费 API（无需 key）

### 3. 系统依赖

```bash
# 安装 jq（JSON 处理）
yum install -y jq  # CentOS/OpenCloudOS
apt-get install -y jq  # Ubuntu/Debian
```

## 🚀 快速开始

### 步骤 1：配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
export NOIZ_API_KEY="xxx"
```

### 步骤 2：添加监控股票

编辑 `stocks.conf`：

```bash
# 格式：股票代码，股票名称，涨阈值%，跌阈值%
sh600519,贵州茅台，3,3
sz000858,五粮液，4,4
sh601318,中国平安，5,5
```

### 步骤 3：运行监控

```bash
# 手动运行一次
bash scripts/monitor.sh

# 加入定时任务（每 5 分钟检查一次）
crontab -e
*/5 9-11,13-15 * * 1-5 bash /path/to/monitor.sh  # 交易日交易时间
```

## 📖 命令参数

```bash
bash scripts/monitor.sh [选项]

选项:
  -c, --config <file>     配置文件路径（默认：stocks.conf）
  -o, --once              只运行一次，不监控
  -v, --verbose           详细输出
  -h, --help              显示帮助
```

## 💡 使用示例

### 1. 监控贵州茅台

```bash
# 添加股票
echo "sh600519，贵州茅台，3,3" >> stocks.conf

# 运行监控
bash scripts/monitor.sh
```

### 2. 设置止盈止损

```bash
# 涨 5% 止盈提醒，跌 3% 止损提醒
echo "sz000858，五粮液，5,3" >> stocks.conf
```

### 3. 多股票监控

```bash
# 批量添加
cat >> stocks.conf << EOF
sh600519，贵州茅台，3,3
sz000858，五粮液，4,4
sh601318，中国平安，5,5
sz002415，海康威视，4,4
EOF

bash scripts/monitor.sh
```

## 📊 提醒内容

当股票突破阈值时，司幼会发送语音：

> "主人～ 贵州茅台现价 1850 元，涨了 3.2%，突破您设置的 3% 阈值啦！要不要看看？"

## ⚙️ 高级配置

### 1. 自定义监控时间

编辑 `config.sh`：

```bash
# 监控时间段（24 小时制）
START_HOUR=9
END_HOUR=15

# 午休时间不监控
LUNCH_START=11:30
LUNCH_END=13:00

# 周末不监控
WEEKEND_SKIP=true
```

### 2. 自定义提醒方式

```bash
# 语音 + 文字
NOTIFY_TYPE="both"

# 只发文字
NOTIFY_TYPE="text"

# 只发语音
NOTIFY_TYPE="voice"
```

### 3. 价格缓存

避免频繁请求 API：

```bash
# 缓存时间（秒）
CACHE_TTL=60
```

## 🐛 故障排除

### 问题 1：获取不到股价

**解决**：检查网络连接，新浪财经 API 可能需要代理

### 问题 2：重复提醒

**解决**：检查缓存配置，避免同一阈值反复触发

### 问题 3：非交易时间也提醒

**解决**：检查交易时间判断逻辑

## 📦 文件结构

```
stock-monitor-skill/
├── SKILL.md
├── README.md
├── reference.md
├── scripts/
│   ├── monitor.sh        # 主监控脚本
│   ├── get_price.sh      # 获取股价
│   ├── notify.sh         # 发送提醒
│   └── config.sh         # 配置文件
├── examples/
│   ├── stocks.conf       # 股票配置示例
│   └── crontab.txt       # 定时任务示例
└── stocks.conf           # 用户配置
```

## 💰 商业授权

- **个人使用**：免费
- **商业使用**：请联系作者获取授权

---

**Made with ❤️ by 司幼 (SiYou)**
