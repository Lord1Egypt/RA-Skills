# 同花顺 Skill（ClawHub 兼容版）

此目录提供同花顺个人交易的全流程自动化组件（不包含 `.ahk` / `.ps1` 文件）：

- `SKILL.md`：Agent 指令与行为规范
- `scripts/ths-hotkeys.mjs`：Windows GUI 自动化（Node 调用 PowerShell SendKeys）
- `scripts/risk-calc.mjs`：风控仓位计算
- `scripts/run-all.mjs`：一体化计划执行入口
- `scripts/trade-journal.mjs`：交易日志工具
- `scripts/watchlist.txt`：默认批量巡检清单
- `scripts/trading-plan.sample.json`：计划模板

## 快速开始

1. Windows 环境
2. 安装 Node.js
3. 打开同花顺客户端
4. 运行：

```bash
node "./scripts/ths-hotkeys.mjs" --action morning_check
```

## 一体化执行

```bash
node "./scripts/run-all.mjs" --mode short --batch kline
```

## 风控计算

```bash
node "./scripts/risk-calc.mjs" --capital 200000 --riskPct 1 --entry 25.8 --stop 24.9 --target 28 --side long
```

## 交易日志

```bash
node "./scripts/trade-journal.mjs" add --symbol 600519 --side buy --entry 1688 --stop 1650 --target 1760 --shares 100 --strategy short --note "回踩均线"
```

```bash
node "./scripts/trade-journal.mjs" list --limit 20
```
