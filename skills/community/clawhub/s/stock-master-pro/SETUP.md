# Stock Master Pro 安装指南

## 前置依赖

### 1. 安装 QVeris AI Skill

Stock Master Pro 依赖 QVeris AI 提供股票数据。

#### 步骤 1：注册 QVeris AI

访问：https://qveris.ai/?ref=y9d7PKgdPcPC-A

- 免费注册账号
- 登录后进入控制台
- 复制你的 API Key（格式：`sk-xxxxxxxx`）

#### 步骤 2：安装 QVeris Skill

```bash
# 创建目录
mkdir -p ~/.openclaw/skills/qveris-official/scripts

# 下载技能文件
curl -fSL https://qveris.ai/skill/SKILL.md -o ~/.openclaw/skills/qveris-official/SKILL.md
curl -fSL https://qveris.ai/skill/scripts/qveris_tool.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs
curl -fSL https://qveris.ai/skill/scripts/qveris_client.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_client.mjs
curl -fSL https://qveris.ai/skill/scripts/qveris_env.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_env.mjs

# 验证安装
ls -la ~/.openclaw/skills/qveris-official/
```

#### 步骤 3：设置 API Key

**方法 A：临时设置（当前会话有效）**

```bash
export QVERIS_API_KEY="sk-你的 API Key"
```

**方法 B：永久设置（推荐）**

编辑 `~/.bashrc` 或 `~/.zshrc`，添加：

```bash
export QVERIS_API_KEY="sk-你的 API Key"
```

然后执行：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

**方法 C：通过 OpenClaw 配置**

在 OpenClaw 的配置文件中设置环境变量（如果支持）。

#### 步骤 4：验证安装

```bash
# 检查 API Key
echo $QVERIS_API_KEY

# 测试 QVeris CLI
node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs --help

# 测试获取股票数据
export QVERIS_API_KEY="sk-你的 API Key"
node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs call ths_ifind.real_time_quotation.v1 --discovery-id 81d10584-cf1b-4229-afa2-54b9c84b7342 --params '{"codes":"000531.SZ"}'
```

---

### 2. 安装 Stock Master Pro

#### 步骤 1：检查依赖

```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_dependency.mjs
```

应该显示：

```
✅ QVeris AI 依赖已就绪

✨ 所有依赖已就绪，可以开始使用 Stock Master Pro！
```

#### 步骤 2：配置持仓

```bash
# 创建持仓配置文件
cp ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.example.json \
   ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json

# 编辑持仓配置
nano ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json
```

示例配置：

```json
{
  "holdings": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.2572,
      "shares": 700,
      "buy_date": "2026-03-20",
      "notes": "趋势票，电力概念",
      "alerts": {
        "target_price": 8.20,
        "stop_loss": 7.00,
        "change_pct": 5
      }
    }
  ],
  "watchlist": [
    {
      "code": "603259.SH",
      "name": "药明康德",
      "reason": "趋势突破，关注回踩"
    }
  ],
  "settings": {
    "check_interval_minutes": 10,
    "review_times": ["12:30", "15:30", "16:00"],
    "exclude_st": true,
    "exclude_kcb": true
  }
}
```

---

## 开始使用

### 检查持仓

```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs
```

### 选股

```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/stock_screener.mjs
```

---

## 设置定时任务（可选）

### 使用 Cron 设置 10 分钟检查

```bash
crontab -e
```

添加：

```bash
# Stock Master Pro - 每 10 分钟检查持仓
*/10 * 9-15 * * 1-5 export QVERIS_API_KEY="sk-你的 API Key" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs >> /tmp/stock_check.log 2>&1

# 午盘复盘 - 每天 12:30
30 12 * * 1-5 export QVERIS_API_KEY="sk-你的 API Key" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/market_review.mjs --session=noon >> /tmp/stock_review.log 2>&1

# 尾盘复盘 - 每天 15:30
30 15 * * 1-5 export QVERIS_API_KEY="sk-你的 API Key" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/market_review.mjs --session=close >> /tmp/stock_review.log 2>&1
```

---

## 故障排查

### 问题 1：API Key 未设置

**错误信息**：
```
❌ QVERIS_API_KEY 环境变量未设置或格式不正确
```

**解决方法**：
```bash
export QVERIS_API_KEY="sk-你的 API Key"
```

### 问题 2：QVeris Skill 未安装

**错误信息**：
```
❌ QVeris AI 技能未安装
```

**解决方法**：按照上面的步骤 1 安装 QVeris Skill。

### 问题 3：持仓配置文件不存在

**错误信息**：
```
❌ 持仓配置文件不存在
```

**解决方法**：
```bash
cp ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.example.json \
   ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json
```

### 问题 4：QVeris API 调用失败

**错误信息**：
```
QVeris API error: no data
```

**可能原因**：
- 股票代码格式错误（需要带后缀，如 `000531.SZ`）
- 非交易时间
- API Key 无效

**解决方法**：
1. 检查股票代码格式
2. 确认在交易时间（9:30-11:30, 13:00-15:00）
3. 重新获取 API Key

---

## 获取帮助

- 查看 README.md 了解详细功能
- 查看 SKILL.md 了解使用说明
- 检查日志文件：`/tmp/stock_check.log`

---

## 版本

v1.0.0 (2026-03-24)
