---
name: secn
description: 这是 StockEarningCN 的 OpenClaw 技能/Skill插件入口说明。安装本目录后，你将获得一组可组合使用的技能
user-invocable: true
---
# StockEarningCN Skills介绍(StockEarning Assistant)

这是 StockEarningCN 的 OpenClaw 技能插件入口说明。安装本目录后，你将获得一组可组合使用的技能，用于：

- 查询A股行情、股票信息、股票搜索
- 查询与管理持仓、计算盈亏、刷新持仓现价
- 记录买入/卖出交易

## 开始之前：

您需要去`https://www.mystockearning.cn注册一个账号，并等待审核通过后获取api key。`

## 认证与基础配置

- 环境变量: `STOCK_API_KEY`
- Base URL: 从 `config.sh` 中读取 `$STOCK_BASE_URL`（默认 `https://www.mystockearning.cn`，也可通过环境变量 `STOCK_BASE_URL` 覆盖）

所有请求均使用 HTTP Header：`X-API-Key: $STOCK_API_KEY`

推荐安全保存（OpenClaw/Hermes 通用）：使用 `./scripts/setup_api_key.sh` 生成本地密钥文件（默认写入 `~/.config/stockearning/stockearning.env`，权限 600）。

## 推荐使用方式

通常直接使用主入口技能：

- `/secn`：主入口，覆盖最常用的查询/记账场景

若你希望更可控、更聚焦的行为，可以按需调用下列技能：

| 技能名称                  | 功能                 | 目录                       |
| --------------------- | ------------------ | ------------------------ |
| `secn`               | 主入口：综合查询、记录交易        | `./stock-master/`        |
| `portfolio-assistant` | 仅查询持仓/收益摘要/历史交易    | `./portfolio-assistant/` |
| `market-data`         | 仅查询实时价格、股票信息、搜索代码  | `./market-data/`         |
| `trade-execution`     | 仅用于记录买入/卖出交易       | `./trade-execution/`     |

## 安装方式

### Openclaw:

```
openclaw skills install secn
```

<br />

### Hermes:

```
hermes skills install clawhub:secn
```
