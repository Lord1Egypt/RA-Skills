# 盘后复盘（Evening Review）

> 生成时间：{{generated_at}}
> 报告日期：{{date}}
> 报告作者：{{author}}
> 今日市场状态：{{market_regime}}

---

## 一、自选股当日表现汇总表

| 代码 | 名称 | 所属行业 | 昨收 | 今收 | 涨跌幅 | 成交额 | 换手率 | 相对大盘 |
|------|------|----------|------|------|--------|--------|--------|----------|
| {{stock_code}} | {{stock_name}} | {{sector}} | {{prev_close}} | {{close}} | {{change_pct}} | {{turnover}} | {{turnover_rate}} | {{relative_market}} |

---

## 二、市场主线还原

### 2.1 大盘综述
- 上证指数：{{sh_close}}（{{sh_change_pct}}）
- 深证成指：{{sz_close}}（{{sz_change_pct}}）
- 创业板指：{{cyb_close}}（{{cyb_change_pct}}）
- 科创 50：{{kc50_close}}（{{kc50_change_pct}}）
- 两市成交额：{{total_turnover}}（环比 {{turnover_mom}}）

### 2.2 主线板块梳理
| 主线方向 | 龙头股 | 板块涨幅 | 涨停家数 | 驱动逻辑 | 持续性判断 |
|----------|--------|----------|----------|----------|------------|
| {{main_theme}} | {{leader_stock}} | {{theme_change_pct}} | {{theme_limit_count}} | {{driver_logic}} | {{sustainability}} |

### 2.3 主线演化路径
1. 早盘：{{morning_session}}
2. 午盘：{{midday_session}}
3. 尾盘：{{afternoon_session}}

---

## 三、资金面复盘

### 3.1 北向资金
- 全天净买入/卖出：{{northbound_net}}
- 沪股通：{{northbound_sh}}
- 深股通：{{northbound_sz}}
- 重点流入个股 Top5：{{northbound_in_top5}}
- 重点流出个股 Top5：{{northbound_out_top5}}

### 3.2 机构席位
- 机构净买入额：{{institution_net_buy}}
- 机构净买入个股：{{institution_buy_stocks}}
- 机构净卖出个股：{{institution_sell_stocks}}

### 3.3 龙虎榜
| 代码 | 名称 | 上榜原因 | 买入额 | 卖出额 | 净额 | 机构席位 | 知名游资 |
|------|------|----------|--------|--------|------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{reason}} | {{buy_amount}} | {{sell_amount}} | {{net_amount}} | {{inst_seat}} | {{hot_money}} |

---

## 四、今日操作记录

| 时间 | 代码 | 名称 | 方向 | 价格 | 数量 | 金额 | 触发原因 | 执行评价 |
|------|------|------|------|------|------|------|----------|----------|
| {{trade_time}} | {{stock_code}} | {{stock_name}} | {{direction}} | {{price}} | {{quantity}} | {{amount}} | {{trigger_reason}} | {{execution_eval}} |

**操作统计：** 买入 {{buy_count}} 笔 / 卖出 {{sell_count}} 笔 / 合计 {{total_trades}} 笔

---

## 五、盈亏统计

### 5.1 当日盈亏
- 当日已实现盈亏：{{realized_pnl}}
- 当日浮动盈亏：{{floating_pnl}}
- 当日总盈亏：{{total_pnl}}（收益率 {{daily_return_pct}}）
- 同期大盘涨跌幅：{{benchmark_change_pct}}
- 超额收益：{{alpha}}

### 5.2 持仓盈亏明细
| 代码 | 名称 | 持仓数量 | 成本价 | 现价 | 浮动盈亏 | 盈亏比例 | 仓位占比 |
|------|------|----------|--------|------|----------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{shares}} | {{cost_price}} | {{current_price}} | {{floating_pnl}} | {{pnl_pct}} | {{position_pct}} |

### 5.3 累计绩效
- 累计收益率：{{cumulative_return}}
- 累计超额收益：{{cumulative_alpha}}
- 最大回撤：{{max_drawdown}}

---

## 六、决策回顾与经验教训

### 6.1 正确决策
1. {{correct_decision_1}}
   - 决策依据：{{correct_basis_1}}
   - 可复用经验：{{reusable_lesson_1}}

2. {{correct_decision_2}}
   - 决策依据：{{correct_basis_2}}
   - 可复用经验：{{reusable_lesson_2}}

### 6.2 错误决策
1. {{wrong_decision_1}}
   - 错误原因：{{wrong_reason_1}}
   - 改进措施：{{improvement_1}}

2. {{wrong_decision_2}}
   - 错误原因：{{wrong_reason_2}}
   - 改进措施：{{improvement_2}}

### 6.3 情绪与纪律检查
- 是否严格遵守交易计划：{{discipline_check}}
- 是否有情绪化交易：{{emotional_trade}}
- 是否触及风控红线：{{risk_control_check}}

---

## 七、次日预判与关注点

### 7.1 市场预判
- 大盘方向预判：{{market_forecast}}
- 主线板块预判：{{theme_forecast}}
- 情绪温度预判：{{sentiment_forecast}}

### 7.2 次日关注标的
| 代码 | 名称 | 关注逻辑 | 关键价位 | 操作预案 |
|------|------|----------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{watch_logic}} | {{key_price}} | {{action_plan}} |

### 7.3 待办事项
- [ ] {{todo_1}}
- [ ] {{todo_2}}
- [ ] {{todo_3}}

---

> 免责声明：本报告仅为个人投资决策辅助记录，不构成任何投资建议。市场有风险，投资需谨慎。
