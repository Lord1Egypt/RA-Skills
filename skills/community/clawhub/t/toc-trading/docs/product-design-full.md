# TOC 模拟交易系统 - 完整产品文档

> **别名**：TOC 模拟交易 / 小悟操盘手 🎯
> **版本**：v1.0
> **状态**：产品设计完成

---

## 1. 需求分析

### 1.1 用户故事

| 角色 | 场景 | 痛点 | 期望 |
|------|------|------|------|
| 苍苍子森（老板） | 验证选股思路 | 真金白银试错成本高 | 低成本验证策略 |
| 苍苍子森 | 练习交易纪律 | 手动计算收益麻烦 | 自动算好盈亏 |
| 苍苍子森 | 复盘总结 | 忘了买过什么股票 | 记录可追溯 |
| 苍苍子森 | 挑战自我 | 想验证自己选股能力 | 有排名有统计 |

### 1.2 业务场景

**场景 1：日常选股验证**
- 老板看到某只股票，想加入自选观察
- 告诉小悟"加一只 XXX"
- 小悟自动获取实时行情、行业分类
- 后续持续监控涨跌

**场景 2：模拟买入操作**
- 老板决定买入，记录"买 100 手 @ 15.6 元"
- 小悟记录成本，自动拉取当前市价计算盈亏
- 实时显示持仓状态

**场景 3：假设演练**
- 老板想测试"如果昨天买，现在赚多少"
- 小悟取昨日开盘价 vs 当前价计算收益

**场景 4：挑战比赛**
- 老板开启月度挑战，初始 5 万
- 自主决策买卖，小悟辅助统计
- 月末看排名、收益率曲线

### 1.3 核心需求

| 优先级 | 需求 | 描述 |
|--------|------|------|
| P0 | 股票池管理 | 加/删/查自选股，获取实时行情 |
| P0 | 持仓模拟 | 记录买卖，计算实时盈亏 |
| P0 | 演练假设 | 取历史价格 vs 当前价格计算收益 |
| P0 | **股票推荐** | 消息驱动/分析驱动/定时推送 |
| P1 | 监控推送 | 定时推送 + 异动提醒 |
| P1 | 挑战模式 | 月度模拟赛，统计排名 |
| P1 | 挑战模式 | 月度模拟赛，统计排名 |
| P2 | 数据导出 | 导出持仓/交易记录 |

---

## 2. 功能模块

#### 模块 1：股票池
- 管理自选股列表
- 展示实时行情（价格、涨跌幅）
- 按行业分类、按涨幅排序
- 支持搜索

#### 模块 2：持仓模拟
- 记录买入/卖出
- 实时计算盈亏（单笔 + 总计）
- 查看历史交易记录

#### 模块 3：演练模式
- 假设买入计算收益
- 支持任意历史日期

#### 模块 4：监控推送
- 定时三个时间点推送
- 异动即时提醒（涨跌幅/成交量）

#### 模块 5：AI股神挑战
- 月度模拟赛
- 收益率排名
- 交易统计（胜率/连盈）

#### 模块 6：股票推荐 🤖
- 消息驱动推荐（涨停/资金/公告/新闻）
- 分析驱动筛选（基本面/技术面/资金面）
- 每日金股 / 异动提醒 / 周报

### 2.2 股票推荐模块详细设计

#### 推荐场景

| 类型 | 触发方式 | 推荐逻辑 |
|------|----------|----------|
| **消息驱动** | 每天心跳检查 | 监控涨停板、资金流向、热门板块、重大公告 |
| **分析驱动** | 你问我答 | 按条件筛选（低估值、高增长、资金流入等） |
| **定时推送** | 早/午/收盘 | 每日金股、异动提醒、操作建议周报 |

#### 推荐来源

| 来源 | 数据接口 | 用途 |
|------|----------|------|
| 涨停异动 | `limit_list_d` | 挖掘涨停原因，跟踪持续性 |
| 资金流向 | `moneyflow` / `moneyflow_hsgt` | 北向/主力资金买入信号 |
| 板块轮动 | `sw_daily` / `ths_hot` | 热门板块切换 |
| 业绩预增 | `express` / `forecast` | 业绩拐点/高增长 |
| 研报推荐 | `research_report` | 机构看好 |
| 消息催化 | `news` / `anns_d` | 政策/事件驱动 |

#### 推荐输出

```json
{
  "id": "rec-001",
  "type": "资金流入推荐",
  "stock_code": "300750.SZ",
  "stock_name": "宁德时代",
  "price": 192.30,
  "change_pct": 3.56,
  "reason": "北向资金连续3日净买入，累计超5亿",
  "industry": "新能源车",
  "tags": ["北向资金", "业绩预增"],
  "signal_strength": "强",
  "created_at": "2026-03-29T10:00:00Z"
}
```

#### 推荐命令

| 命令 | 说明 |
|------|------|
| 推荐一只股票 | 基于当前市场推荐 |
| 有什么消息吗 | 今日热点梳理 |
| 最近资金在买什么 | 资金流向分析 |
| 推荐低估值股票 | 按估值筛选 |
| 今日金股 | 每天推荐一只 |

#### 推荐的分类标签

| 标签 | 含义 | 推荐场景 |
|------|------|----------|
| 🟢 北向资金 | 港股通净买入 | 资金面推荐 |
| 🔥 涨停 | 今日涨停 | 异动推荐 |
| 📈 突破 | 突破新高/均线 | 技术面推荐 |
| 💰 资金流入 | 主力/北向买入 | 资金面推荐 |
| 📊 业绩预增 | 业绩超预期 | 基本面推荐 |
| 🏭 政策利好 | 政策推动 | 消息面推荐 |

### 2.2 交互流程

```
用户输入 → 命令解析 → 业务处理 → 数据存储 → 结果呈现
              ↓
         Tushare API 获取行情
```

### 2.3 命令体系

| 命令类型 | 示例 | 处理逻辑 |
|----------|------|----------|
| 添加 | 加一只 宁德时代 | 查代码 → 取行情 → 存入股票池 |
| 删除 | 去掉 茅台 | 从股票池移除 |
| 买入 | 买 100 手 @ 15.6 招商银行 | 存入持仓记录 |
| 卖出 | 卖 50 手 招商银行 | 更新持仓数量 |
| 查询 | 持仓 | 拉取持仓 + 实时行情计算盈亏 |
| 演练 | 如果昨天开盘买入招商银行 | 取昨日开盘价 → 计算收益 |
| 挑战 | 开启挑战 | 初始化挑战数据 |

---

## 3. 架构设计

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     表现层 (Presentation)                 │
│  飞书消息 / 命令输入 ←→ 结果输出 (Markdown/表格)        │
└─────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────┐
│                    业务层 (Business)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ 命令解析  │ │ 股票池   │ │ 持仓管理  │ │ 挑战引擎  │   │
│  │ Parser   │ │ Service  │ │ Service  │ │ Service  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↓↑
┌─────────────────────────────────────────────────────────┐
│                    数据层 (Data)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ JSON存储 │ │ 缓存管理 │ │ Tushare  │ │ 推送服务  │   │
│  │ Storage │ │ Cache   │ │ Client  │ │ Notifier │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3.2 模块职责

| 模块 | 职责 | 对外接口 |
|------|------|----------|
| **Parser** | 解析用户命令，提取标的/参数/意图 | `parse(input) → Command` |
| **StockPoolService** | 股票池 CRUD + 行情拉取 | `add/remove/list/search` |
| **PositionService** | 持仓管理 + 盈亏计算 | `buy/sell/holdings/profit` |
| **DrillService** | 假设交易收益计算 | `calculate(scenario)` |
| **RecommendationService** | 股票推荐 + 信号挖掘 | `recommend/daily/analysis` |
| **ChallengeService** | 挑战周期/排名/统计 | `start/rank/stats` |
| **Storage** | JSON 文件读写 | `get/set` |
| **TushareClient** | 行情数据封装 | `quote/history/industry` |
| **Notifier** | 飞书消息推送 | `send(message)` |

### 3.3 目录结构

```
toc-trading/
├── src/
│   ├── __init__.py
│   ├── parser.py          # 命令解析器
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_pool.py # 股票池服务
│   │   ├── position.py   # 持仓服务
│   │   ├── drill.py      # 演练服务
│   │   └── challenge.py  # 挑战服务
│   ├── data/
│   │   ├── __init__.py
│   │   └── storage.py    # 存储抽象
│   ├── tushare_client.py # Tushare 封装
│   └── notifier.py       # 推送服务
├── data/                  # 数据文件目录
│   ├── stock_pool.json
│   ├── positions.json
│   ├── trades.json
│   └── challenge.json
├── config/
│   └── config.yaml       # 配置文件
├── tests/                # 单元测试
├── docs/                 # 文档
│   ├── product-design.md
│   └── api-design.md
└── main.py              # 入口
```

---

## 4. 数据表单

### 4.1 股票池 (stock_pool.json)

```json
{
  "version": "1.0",
  "last_update": "2026-03-29T10:00:00Z",
  "stocks": [
    {
      "id": "uuid-001",
      "code": "600519.SH",
      "name": "贵州茅台",
      "industry": "白酒",
      "added_at": "2026-03-28T09:00:00Z",
      "reason": "龙头稳健，业绩确定性强",
      "remark": "目标价1800",
      "tags": ["龙头", "消费"],
      "enabled": true
    }
  ]
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 UUID |
| code | string | 是 | 股票代码（格式：600519.SH） |
| name | string | 是 | 股票名称 |
| industry | string | 否 | 所属行业（从 Tushare 自动获取） |
| added_at | datetime | 是 | 添加时间 |
| reason | string | 否 | 推荐理由 |
| remark | string | 否 | 备注/目标价 |
| tags | array | 否 | 自定义标签 |
| enabled | boolean | 是 | 是否启用（删除时置 false） |

### 4.2 持仓记录 (positions.json)

```json
{
  "version": "1.0",
  "last_update": "2026-03-29T10:30:00Z",
  "positions": [
    {
      "id": "pos-001",
      "stock_code": "600036.SH",
      "stock_name": "招商银行",
      "buy_date": "2026-03-20",
      "buy_price": 15.60,
      "quantity": 10000,
      "quantity_unit": "手",
      "remark": "测试仓",
      "created_at": "2026-03-20T14:30:00Z"
    }
  ]
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 |
| stock_code | string | 是 | 股票代码 |
| stock_name | string | 是 | 股票名称 |
| buy_date | date | 是 | 买入日期 |
| buy_price | float | 是 | 买入价格 |
| quantity | int | 是 | 数量（股） |
| quantity_unit | string | 是 | 数量单位（手/股） |
| remark | string | 否 | 备注 |
| created_at | datetime | 是 | 记录创建时间 |

### 4.3 交易记录 (trades.json)

```json
{
  "version": "1.0",
  "trades": [
    {
      "id": "trade-001",
      "type": "buy",
      "stock_code": "600036.SH",
      "stock_name": "招商银行",
      "trade_date": "2026-03-20",
      "price": 15.60,
      "quantity": 10000,
      "amount": 156000,
      "fee": 0,
      "created_at": "2026-03-20T14:30:00Z"
    },
    {
      "id": "trade-002",
      "type": "sell",
      "stock_code": "600036.SH",
      "stock_name": "招商银行",
      "trade_date": "2026-03-25",
      "price": 16.50,
      "quantity": 5000,
      "amount": 82500,
      "fee": 0,
      "profit": 4500,
      "profit_rate": 5.77,
      "created_at": "2026-03-25T10:00:00Z"
    }
  ]
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 |
| type | enum | 是 | buy/sell |
| stock_code | string | 是 | 股票代码 |
| stock_name | string | 是 | 股票名称 |
| trade_date | date | 是 | 交易日期 |
| price | float | 是 | 成交价格 |
| quantity | int | 是 | 成交数量 |
| amount | float | 是 | 成交金额 |
| fee | float | 否 | 手续费 |
| profit | float | 否 | 卖出时计算的收益 |
| profit_rate | float | 否 | 卖出时的收益率(%) |
| created_at | datetime | 是 | 记录创建时间 |

### 4.4 挑战数据 (challenge.json)

```json
{
  "version": "1.0",
  "active": true,
  "period": "2026-03",
  "start_date": "2026-03-01",
  "end_date": "2026-03-31",
  "initial_capital": 50000,
  "current_capital": 52300,
  "max_daily_trades": 3,
  "stop_loss_pct": -7,
  "trades_count": 15,
  "win_count": 10,
  "loss_count": 5,
  "win_rate": 66.67,
  "max_profit_trade": 3500,
  "max_loss_trade": -2100,
  "max_consecutive_wins": 4,
  "max_consecutive_losses": 2,
  "daily_trades": [
    {
      "date": "2026-03-20",
      "count": 2,
      "trades": ["trade-001", "trade-002"]
    }
  ],
  "equity_curve": [
    {"date": "2026-03-01", "capital": 50000},
    {"date": "2026-03-20", "capital": 52300}
  ],
  "created_at": "2026-03-01T00:00:00Z"
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| active | boolean | 是 | 是否正在进行 |
| period | string | 是 | 周期（YYYY-MM） |
| start_date | date | 是 | 开始日期 |
| end_date | date | 是 | 结束日期 |
| initial_capital | float | 是 | 初始资金 |
| current_capital | float | 是 | 当前资金 |
| max_daily_trades | int | 是 | 每日最大交易次数 |
| stop_loss_pct | float | 是 | 止损线(%) |
| trades_count | int | 是 | 总交易次数 |
| win_count | int | 是 | 盈利次数 |
| loss_count | int | 是 | 亏损次数 |
| win_rate | float | 是 | 胜率(%) |
| max_profit_trade | float | 是 | 单笔最大盈利 |
| max_loss_trade | float | 是 | 单笔最大亏损 |
| max_consecutive_wins | int | 是 | 最大连盈天数 |
| max_consecutive_losses | int | 是 | 最大连亏天数 |
| daily_trades | array | 是 | 每日交易记录 |
| equity_curve | array | 是 | 资金曲线 |
| created_at | datetime | 是 | 创建时间 |

### 4.5 系统配置 (config.json)

```json
{
  "version": "1.0",
  "notification": {
    "enabled": true,
    "morning_time": "09:30",
    "noon_time": "13:00",
    "evening_time": "15:30",
    "channels": ["feishu"]
  },
  "alert": {
    "price_change_threshold": 5,
    "volume_spike_ratio": 2,
    "enabled": true
  },
  "tushare": {
    "cache_minutes": 5,
    "retry_times": 3
  },
  "recommendation": {
    "daily_stock_enabled": true,
    "daily_stock_time": "09:00",
    "signal_filters": {
      "min_change_pct": 3,
      "min_volume_ratio": 1.5,
      "min_moneyflow": 100000000
    }
  }
}
```

### 4.6 推荐记录 (recommendations.json)

```json
{
  "version": "1.0",
  "last_update": "2026-03-29T10:00:00Z",
  "daily_stocks": [
    {
      "date": "2026-03-29",
      "stocks": [
        {
          "id": "rec-001",
          "stock_code": "300750.SZ",
          "stock_name": "宁德时代",
          "type": "资金流入",
          "price": 192.30,
          "change_pct": 3.56,
          "reason": "北向资金连续3日净买入，累计超5亿",
          "industry": "新能源车",
          "tags": ["北向资金", "业绩预增"],
          "signal_strength": "强"
        }
      ]
    }
  ],
  "historical_recommendations": [
    {
      "id": "hist-001",
      "stock_code": "600519.SH",
      "stock_name": "贵州茅台",
      "type": "分析驱动",
      "reason": "PE估值低于近三年均值，ROE持续高于25%",
      "recommended_at": "2026-03-20T10:00:00Z",
      "result": "pending",
      "current_price": 1680.50,
      "recommended_price": 1650.00
    }
  ]
}
```

---

## 5. 接口关系

### 5.1 外部接口

| 接口 | 来源 | 用途 |
|------|------|------|
| `pro_bar` | Tushare | 实时行情、日K线 |
| `daily` | Tushare | 历史行情 |
| `stock_basic` | Tushare | 股票基本信息 |
| `index_classify` | Tushare | 行业分类 |
| `limit_list_d` | Tushare | 涨停列表 |
| `moneyflow` | Tushare | 资金流向 |
| 飞书消息 API | OpenClaw | 推送通知 |

### 5.2 内部接口

```
┌────────────┐      ┌─────────────┐      ┌────────────┐
│   Parser   │ ───▶ │   Service   │ ───▶ │  Storage   │
│  (命令解析) │      │  (业务逻辑)  │      │  (数据持久) │
└────────────┘      └─────────────┘      └────────────┘
       │                    │
       ↓                    ↓
┌────────────┐      ┌─────────────┐
│  Tushare   │      │  Notifier   │
│  (外部数据)  │      │  (消息推送)  │
└────────────┘      └─────────────┘
```

### 5.3 服务间调用

| 调用方 | 被调方 | 方法 | 说明 |
|--------|--------|------|------|
| Parser | StockPoolService.add() | 添加股票 | 解析"加一只"命令 |
| Parser | PositionService.buy() | 记录买入 | 解析"买 XXX"命令 |
| Parser | DrillService.calculate() | 计算演练 | 解析"如果..."命令 |
| Parser | RecommendationService.recommend() | 股票推荐 | 解析"推荐一只"命令 |
| Parser | ChallengeService.start() | 开启挑战 | 解析"开启挑战"命令 |
| StockPoolService | TushareClient.quote() | 获取行情 | 实时价格 |
| StockPoolService | TushareClient.industry() | 获取行业 | 行业分类 |
| PositionService | TushareClient.quote() | 实时价格 | 盈亏计算 |
| PositionService | Storage.positions | 读写持仓 | 持久化 |
| RecommendationService | TushareClient.limit_list() | 涨停监控 | 获取今日涨停 |
| RecommendationService | TushareClient.moneyflow() | 资金流向 | 资金信号挖掘 |
| RecommendationService | TushareClient.news() | 新闻催化 | 消息面推荐 |
| ChallengeService | PositionService | 持仓数据 | 统计收益 |
| Notifier | 飞书 API | 推送消息 | 监控提醒 |

---

## 6. 非功能性需求

### 6.1 性能

| 指标 | 要求 |
|------|------|
| 行情响应 | < 2 秒 |
| 命令解析 | < 500ms |
| 数据存储 | < 100ms |

### 6.2 可用性

| 指标 | 要求 |
|------|------|
| 日间服务 | 7×24 小时 |
| 数据备份 | 每日自动备份 |
| 故障恢复 | < 5 分钟 |

### 6.3 安全

| 措施 | 说明 |
|------|------|
| Token 存储 | 环境变量，不写入代码 |
| 文件权限 | 600，仅 owner 读写 |
| 日志脱敏 | 不记录股票代码外的敏感信息 |

---

## 7. 演进路线

| 阶段 | 功能 | 优先级 |
|------|------|--------|
| **Phase 1** | 股票池 + 持仓模拟 + 股票推荐 | P0 |
| **Phase 2** | 演练模式 + 监控推送 + 挑战模式 | P1 |
| **Phase 3** | 数据导出 + 微信小程序 | P2 |

---

_持续迭代，越用越好用_