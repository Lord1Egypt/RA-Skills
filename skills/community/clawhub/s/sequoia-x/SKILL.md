---
name: sequoia-x
description: A股量化选股系统 Sequoia-X V2 的安装、配置与使用。当用户要求安装 Sequoia-X、使用 Sequoia-X 选股、运行量化策略、配置飞书推送时激活。
---

# Sequoia-X V2 · A股量化选股系统

> 数据源：akshare（免费开源）| 数据库：SQLite | 推送：飞书群机器人

## 安装（一键）

```bash
SKILL_DIR=$(find ~/.openclaw/skills -name "install.sh" -path "*/sequoia-x/*" -exec dirname {} \; | head -1)
bash "${SKILL_DIR}/scripts/install.sh
```

安装到 `~/sequoia-x`，包含：clone 仓库 + pip 依赖 + 生成 .env 配置。

**安装后必须编辑** `~/sequoia-x/.env`，填入飞书 Webhook URL：

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-token-here
```

## 运行

```bash
SKILL_DIR=$(find ~/.openclaw/skills -name "run.sh" -path "*/sequoia-x/*" -exec dirname {} \; | head -1)
bash "${SKILL_DIR}/scripts/run.sh
```

- **工作日**：增量同步行情 → 执行全部策略 → 推送飞书
- **周末/节假日**：跳过网络拉取，用本地数据调试

## 策略一览

详见 `references/strategies.md`（含参数调整建议）

| 策略 | 逻辑 |
|------|------|
| MaVolumeStrategy | MA5 金叉 MA20 + 成交量放大 |
| TurtleTradeStrategy | 20日新高突破 + 成交额过亿 |
| HighTightFlagStrategy | 强动量后极度收敛缩量 |
| LimitUpShakeoutStrategy | 涨停洗盘 |
| UptrendLimitDownStrategy | 趋势中跌停 |
| RpsBreakoutStrategy | RPS突破 |

## 调参路径

- 策略源码：`~/sequoia-x/sequoia_x/strategy/<策略名>.py`
- 详细参数说明：`references/strategies.md`
- 注册新策略：编辑 `~/sequoia-x/main.py`，在 `strategies` 列表追加类名

## 数据位置

```
~/sequoia-x/
├── .env                    # 配置文件（需手动填写 Webhook）
├── data/sequoia_v2.db     # SQLite 数据库
└── sequoia_x/strategy/    # 策略源码
```

## 调试命令

```bash
# 查看数据库已有数据
sqlite3 ~/sequoia-x/data/sequoia_v2.db ".tables"

# 强制全量重新同步
rm ~/sequoia-x/data/sequoia_v2.db
SKILL_DIR=$(find ~/.openclaw/skills -name "run.sh" -path "*/sequoia-x/*" -exec dirname {} \; | head -1)
bash "${SKILL_DIR}/scripts/run.sh"
```
