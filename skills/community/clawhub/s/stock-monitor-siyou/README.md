# 📊 Stock Monitor Skill - 股票自动监控

自动监控股票价格，突破阈值时自动发送飞书语音提醒！

## ✨ 功能特点

- ✅ **实时监控**：支持 A 股/港股/美股
- ✅ **语音提醒**：突破阈值自动发飞书语音条
- ✅ **多股票支持**：同时监控多只股票
- ✅ **自定义阈值**：每只股票独立设置
- ✅ **交易时间判断**：自动跳过非交易时间

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 jq 和 bc
yum install -y jq bc  # CentOS/OpenCloudOS
apt-get install -y jq bc  # Ubuntu/Debian
```

### 2. 配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
export NOIZ_API_KEY="xxx"
```

### 3. 添加监控股票

编辑 `stocks.conf`：

```
sh600519，贵州茅台，3,3
sz000858，五粮液，4,4
```

### 4. 运行监控

```bash
bash scripts/monitor.sh
```

### 5. 设置定时任务

```bash
crontab -e
*/5 9-11,13-15 * * 1-5 bash /path/to/monitor.sh
```

## 💡 使用场景

- 📈 短线交易：监控关键价位突破
- 💼 上班族：没空看盘，自动提醒
- 🎯 止盈止损：到达目标价自动通知
- 🔔 异动提醒：大涨大跌不错过

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

## 💰 商业授权

- **个人使用**：免费
- **商业使用**：请联系作者获取授权

---

**Made with ❤️ by 司幼 (SiYou)**
