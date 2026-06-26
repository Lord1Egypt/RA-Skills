# SignalBot OpenClaw 使用指南

本文档面向使用者，说明如何在 OpenClaw 中安装和使用 signalbot skill。

- GitHub 仓库：https://github.com/shanhuhai5739/signalbot
- ClawHub Skill：`clawhub install signalbot`

---

## 前置条件：安装 signalbot 二进制

### 方式一：go install（推荐，需要 Go 1.21+）

```bash
go install github.com/shanhuhai5739/signalbot@latest
```

安装后二进制自动放入 `$GOPATH/bin`，确保该目录在 PATH 中：

```bash
# 验证
signalbot --help

# 如果找不到命令，将 GOPATH/bin 加入 PATH
echo 'export PATH="$PATH:$(go env GOPATH)/bin"' >> ~/.zshrc
source ~/.zshrc
```

### 方式二：从源码手动编译

```bash
git clone https://github.com/shanhuhai5739/signalbot.git
cd signalbot
go build -o signalbot .
cp signalbot /usr/local/bin/signalbot
```

### 方式三：下载预编译二进制（GitHub Releases）

```bash
# macOS Apple Silicon (arm64)
curl -L https://github.com/shanhuhai5739/signalbot/releases/latest/download/signalbot-darwin-arm64 \
  -o /usr/local/bin/signalbot && chmod +x /usr/local/bin/signalbot

# macOS Intel (amd64)
curl -L https://github.com/shanhuhai5739/signalbot/releases/latest/download/signalbot-darwin-amd64 \
  -o /usr/local/bin/signalbot && chmod +x /usr/local/bin/signalbot

# Linux (amd64)
curl -L https://github.com/shanhuhai5739/signalbot/releases/latest/download/signalbot-linux-amd64 \
  -o /usr/local/bin/signalbot && chmod +x /usr/local/bin/signalbot
```

---

## 安装 Skill

### 方式一：全局安装（推荐，所有 agent 共享）

```bash
mkdir -p ~/.openclaw/skills/signalbot
cp /path/to/signalbot/skills/signalbot/SKILL.md ~/.openclaw/skills/signalbot/
```

### 方式二：Workspace 安装（仅当前 agent）

将 `skills/signalbot/` 目录直接放入 OpenClaw workspace 的 `/skills/` 下：

```bash
cp -r /path/to/signalbot/skills/signalbot /your/openclaw/workspace/skills/
```

### 验证加载

重启 OpenClaw 或新建 session 后，执行：

```bash
openclaw skills list
```

输出中应包含 `signalbot 📊`。

---

## 直接对话调用

安装后，直接在 OpenClaw 聊天窗口中用自然语言提问即可，agent 会自动识别并调用 signalbot：

```
BTC 现在行情怎么样？
```

```
分析一下黄金日线，给出操作建议
```

```
同时分析 BTC 4小时和黄金日线，生成一条行情分析推文
```

```
BTC 和 XAUUSD 当前谁更强势？
```

```
分析 BTC 所有时间周期，判断趋势是否共振
```

```
BTC 的主力成交密集区在哪里？价格现在相对 POC 什么位置？
```

```
顾比均线显示 BTC 机构资金方向如何？
```

---

## Cron Job 配置

### 每日早 8 点 BTC 行情日报

```bash
openclaw cron add --schedule "0 8 * * *" \
  --prompt "运行 signalbot analyze --asset BTC --timeframe 4h 获取行情数据，然后以专业量化交易员视角用中文生成一条行情分析推文，要求：
1. 当前趋势（含顾比均线多空方向）
2. 关键支撑阻力位（含斐波那契水平和 VPVR 的 POC/VAH/VAL）
3. VWAP 偏离度（机构持仓成本参考）
4. 操作建议（BUY/SELL/HOLD）和风险提示
推文长度控制在 280 字以内。" \
  --name "btc-daily-analysis"
```

### 每日早 8 点 BTC + 黄金双标的报告

```bash
openclaw cron add --schedule "0 8 * * *" \
  --prompt "依次运行以下两条命令：
1. signalbot analyze --asset BTC --timeframe 4h
2. signalbot analyze --asset XAUUSD --timeframe 1d

综合两份 JSON 数据，用中文生成一份「早间行情简报」，格式如下：
- 📊 市场概览（1句话）
- ₿ BTC 分析（趋势 + 顾比均线信号 + POC价位 + 操作建议）
- 🥇 黄金分析（趋势 + Fib支撑阻力 + VWAP偏离 + 操作建议）
- ⚠️ 风险提示（1句话）" \
  --name "morning-market-briefing"
```

### 每 4 小时行情监控

```bash
openclaw cron add --schedule "0 */4 * * *" \
  --prompt "运行 signalbot analyze --asset BTC --timeframe 4h，如果满足以下任一条件则生成预警推文；否则回复「当前无明显信号，无需推送」：
- analysis.signal 为 BUY 且 confidence >= 60
- analysis.signal 为 SELL 且 confidence >= 60
- indicators.guppy.alignment 从 crossing 变为 above_long 或 below_long（趋势确认）
- indicators.vpvr.signal 为 above_vah 或 below_val（突破价值区）
- indicators.vwap.position 为 above_band2 或 below_band2（极端偏离）" \
  --name "btc-4h-alert"
```

### 每周一多周期综合分析

```bash
openclaw cron add --schedule "0 9 * * 1" \
  --prompt "运行 signalbot multi --asset BTC 获取五周期综合数据，生成本周行情展望：
1. 多周期趋势共振情况（summary.alignment）
2. 各周期顾比均线信号汇总
3. 日线斐波那契关键水平和 VPVR 主力区间
4. 本周操作建议和止损止盈参考位" \
  --name "btc-weekly-multi"
```

### 查看和管理 Cron Job

```bash
# 查看所有 job
openclaw cron list

# 查看运行历史
openclaw cron history btc-daily-analysis

# 手动触发一次
openclaw cron run btc-daily-analysis

# 删除
openclaw cron remove btc-daily-analysis
```

---

## 常用 Prompt 模板

### 标准行情分析推文

```
分析 BTC 4小时行情，生成一条专业的中文行情分析推文，要求：
1. 包含 RSI、MACD、布林带、EMA 的信号解读
2. 顾比均线：短期组 vs 长期组位置关系（机构资金方向）
3. 斐波那契：最近关键水平和当前价格距离
4. VPVR：POC / VAH / VAL 价位及当前价格位置
5. VWAP：偏离程度（是否超买超卖）
6. 给出明确的操作建议（BUY/SELL/HOLD）和置信度
7. 末尾加上相关话题标签（#BTC #行情分析 等）
总长度 280 字以内
```

### 多周期趋势共振分析

```
运行 signalbot multi --asset BTC，分析多周期趋势共振情况：
1. summary.alignment 总体方向
2. 哪些周期趋势一致？哪些出现背离？
3. 顾比均线在各周期的信号是否同步？
4. 结合多周期分析给出最优入场时机建议
```

### 主力资金意图分析（顾比均线 + VPVR）

```
获取 BTC 日线行情，重点分析主力资金动向：
1. 顾比均线：短期组和长期组的相对位置（机构是否在接筹/出货）
   - above_long → 机构已入场，短线跟多
   - crossing → 机构观望，警惕方向转变
   - below_long → 机构主导下行
2. VPVR：POC（主力成交密集区）价位，价格是否在价值区内
   - above_vah → 价格高于主力均价，上方阻力较小
   - at_poc → 主力博弈区，可能大幅波动
   - below_val → 价格低于价值区，下方支撑弱
3. 综合判断当前是否为机构主导的趋势行情
```

### 斐波那契支撑/阻力位分析

```
获取 BTC 4小时行情，进行斐波那契分析：
1. 当前摆动高低点（swing_high / swing_low）
2. 各斐波那契水平对应的价格
3. 当前价格最接近哪个水平（nearest_level 和 distance_pct）
4. 结合 VPVR 的 POC，判断最强的支撑/阻力位重叠区域
5. 给出具体的止损和止盈目标位
```

### VWAP 背离与均值回归

```
获取 BTC 4小时行情，分析 VWAP 偏离情况：
1. 当前价格偏离 VWAP 的百分比（deviation_pct）
2. 是否处于超买（above_band2）或超卖（below_band2）区域
3. 结合 RSI 和布林带判断是否存在均值回归机会
4. 若价格严重偏离，给出均值回归目标位（VWAP ± 1σ）
```

### 突破预警

```
分析 BTC 4小时行情，判断是否存在以下信号：
- 价格突破布林带上轨（position = above_upper）且成交量放大（ratio > 1.5）
- MACD 金叉（cross = golden_cross）
- EMA 多头排列（alignment 含 bullish）
- 顾比均线短期组突破长期组（alignment = above_long）
- 价格突破 VPVR 价值区高点（vpvr.signal = above_vah）

如果同时满足 2 个以上条件，生成一条突破预警推文；否则不输出任何内容。
```

### 多标的趋势对比

```
分别获取 BTC（4h）和 XAUUSD（1d）的行情数据，对比分析：
1. 哪个标的趋势更强？（对比 analysis.trend + guppy.alignment）
2. 两者相关性如何（同涨同跌 or 背离）？
3. 各自的 VWAP 偏离情况
4. 基于当前指标，哪个更值得关注？
用简洁的中文表格或要点列表呈现。
```

### 周度行情总结

```
获取 BTC 日线行情（--timeframe 1d），结合指标数据生成本周行情总结：
- 本周价格区间和主要趋势
- 顾比均线周线信号（机构资金状态）
- 斐波那契关键水平和 VPVR 主力区间
- 下周重要支撑阻力位
- 综合操作建议
```

### 风险评估报告

```
获取 BTC 4小时行情，重点分析风险指标：
1. ATR 波动率（atr.regime）和具体数值
2. 布林带宽度（bollinger.width）是否异常收窄或扩张
3. RSI 是否处于超买/超卖极端区域
4. VWAP 偏离是否超过 ±2σ（vwap.position = above/below_band2）
5. 成交量是否异常（volume.ratio 极高或极低）
6. 顾比均线是否处于压缩状态（guppy.alignment = crossing）—— 压缩往往是大波动前兆
基于以上数据给出当前市场风险等级（低/中/高）和风险提示。
```

---

## 环境变量（可选）

如需在 OpenClaw 环境中配置，在 `~/.openclaw/openclaw.json` 中添加：

```json5
{
  "skills": {
    "entries": {
      "signalbot": {
        "enabled": true,
        "env": {
          "BINANCE_BASE_URL": "https://your-proxy.com",
          "HTTP_TIMEOUT_SEC": "20",
          "DEFAULT_LIMIT": "300"
        }
      }
    }
  }
}
```

---

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `zsh: command not found: signalbot` | 二进制不在 PATH | 编译后 `cp signalbot /usr/local/bin/` |
| Skill 未被 OpenClaw 识别 | 未重启 session | 执行 `/new` 新建 session 或 `openclaw gateway restart` |
| 请求超时 | Binance 网络不通 | 设置 `BINANCE_BASE_URL` 为代理地址 |
| XAUUSD 数据异常 | 短周期流动性不足 | 改用 `--timeframe 1d` |
| 数据不足（< 50 根） | 标的名称错误 | 检查 `--asset` 参数是否正确 |
| `ema233`/`ema377` 为 0 | K 线数量不足（默认 200 根） | 用 `--limit 400` 拉取更多 K 线 |
