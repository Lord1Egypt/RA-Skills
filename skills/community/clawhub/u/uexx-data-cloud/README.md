# UEXX Data Cloud Skill

UEXX Data Cloud 是一个面向量化研究、行情监控和交易系统的加密货币市场数据缓存服务。它把多类市场数据同步到本地缓存，提供历史回补、实时更新、权限控制和统一 API 访问。

这个 Skill 的目标不是教用户怎么写 API，而是让用户直接用自然语言查询数据。

## 我们是做什么的

UEXX Data Cloud 提供加密货币市场缓存数据 API，包括：

- 市场情绪数据，例如恐慌贪婪指数
- 市场周期数据，例如山寨季指数
- 核心币种合约数据，例如资金费率、OI、多空比
- ETF、期权、宏观和链上相关数据
- 白名单币种历史数据回补和增量更新
- Free / PRO 会员权限控制

服务端负责：

- 自动同步数据
- 自动历史回补
- 本地缓存
- API Key 鉴权
- 限速
- Free Key 生命周期管理

用户只需要提问。

## 能帮助用户做什么

安装这个 Skill 后，用户可以直接问：

- 今日恐慌指数多少？
- 现在是山寨季吗？
- BTC 最新资金费率是多少？
- ETH 当前 OI 怎么样？
- BTC 多空比偏多还是偏空？
- Free 会员能查哪些数据？
- 给我 BTC 资金费率的 API 调用示例

默认情况下，Skill 会自动申请或复用 Free Key，调用 UEXX Data Cloud，然后直接返回答案。

## 用户体验

用户：

> 今日恐慌指数多少？

Skill：

> 今日恐慌贪婪指数为 72，处于 Greed 区间。数据更新时间为 2026-05-19，缓存约 2 分钟前刷新。市场情绪偏乐观，但这不是单独的买入信号。

用户不需要知道：

- API Base URL
- Header 怎么写
- dataset 是什么
- curl 怎么调用

除非用户明确要求“给我 API 调用方式”。

## 自动 Free Key

Skill 会调用：

```http
POST https://bbs.uexx.com/api/v1/free-key
```

返回 Free 等级 API Key。

限制：

- 同 IP 每天最多申请 3 个 Free Key
- Free Key 连续 7 天未使用会自动失效
- 失效后再次使用时可以重新申请
- Free 权限只开放基础功能和部分数据

Key 会保存在本机：

```text
~/.uexx-data-cloud/free_key.json
```

## 当前支持的直接查询

| 用户意图 | 命令 | 数据 |
|---|---|---|
| 恐慌贪婪指数 | `fear-greed` | `market_fear_greed_history` |
| 山寨季指数 | `altcoin-season` | `market_altcoin_season` |
| 资金费率 | `funding-rate --symbol BTC` | `futures_funding_rate_history` |
| 持仓量 / OI | `oi --symbol BTC` | `futures_oi_aggregated_history` |
| 多空比 | `long-short --symbol BTC` | `futures_global_long_short_account_ratio` |

## 脚本用法

```bash
python scripts/query.py fear-greed
python scripts/query.py altcoin-season
python scripts/query.py funding-rate --symbol BTC
python scripts/query.py oi --symbol ETH
python scripts/query.py long-short --symbol BTCUSDT
python scripts/list_catalog.py
```

## 目录结构

```text
uexx-data-cloud/
  SKILL.md
  README.md
  agents/
    openai.yaml
  scripts/
    uexx_client.py
    query.py
    list_catalog.py
  references/
    api_catalog.md
```

## 后续可扩展

后续 UEXX Data Cloud 会继续接入：

- 自研因子库
- 更多交易所行情数据
- 链上指标
- 量化信号
- 策略研究数据
- PRO 权限专属数据

Skill 不需要硬编码全部数据。它可以通过：

```http
GET https://bbs.uexx.com/api/v1/public/api-guide
```

读取 `data_catalog`，动态了解当前可用数据。
