# 盘前报告（Morning Report）

> 生成时间：{{generated_at}}
> 报告日期：{{date}}
> 报告作者：{{author}}
> 市场状态：{{market_regime}}

---

## 一、隔夜市场概览

### 1.1 美股市场
- 三大指数收盘：
  - 道琼斯工业指数：{{dow_close}}（{{dow_change_pct}}）
  - 标普 500 指数：{{spx_close}}（{{spx_change_pct}}）
  - 纳斯达克综合指数：{{ndx_close}}（{{ndx_change_pct}}）
- 中概股表现：{{chinaADR_summary}}
- 美债收益率：10Y {{us_10y}}% / 2Y {{us_2y}}% / 利差 {{us_yield_spread}}%
- VIX 恐慌指数：{{vix_value}}

### 1.2 港股市场
- 恒生指数：{{hsi_close}}（{{hsi_change_pct}}）
- 恒生科技指数：{{hstech_close}}（{{hstech_change_pct}}）
- 南向资金：{{southbound_flow}}

### 1.3 大宗商品与外汇
- 原油（WTI / 布伦特）：{{wti_price}} / {{brent_price}}
- 黄金 / 白银：{{gold_price}} / {{silver_price}}
- 伦敦基本金属（铜/铝/锌）：{{lme_copper}} / {{lme_aluminum}} / {{lme_zinc}}
- 美元指数 DXY：{{dxy_value}}
- 离岸人民币 USD/CNH：{{usdcnh_value}}

---

## 二、重大新闻与公告

### 2.1 隔夜重要新闻
| 序号 | 时间 | 来源 | 事件 | 影响评估 |
|------|------|------|------|----------|
| 1 | {{news_time_1}} | {{news_source_1}} | {{news_event_1}} | {{news_impact_1}} |
| 2 | {{news_time_2}} | {{news_source_2}} | {{news_event_2}} | {{news_impact_2}} |
| 3 | {{news_time_3}} | {{news_source_3}} | {{news_event_3}} | {{news_impact_3}} |

### 2.2 自选股相关公告
| 代码 | 名称 | 公告类型 | 公告摘要 | 影响判断 |
|------|------|----------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{announce_type}} | {{announce_summary}} | {{announce_impact}} |

### 2.3 今日新股申购 / 解禁 / 分红
- 新股申购：{{ipo_list}}
- 限售解禁：{{unlock_list}}
- 除权除息：{{dividend_list}}

---

## 三、宏观与政策扫描

### 3.1 国内宏观
- 央行公开市场操作：{{cmo_operation}}（净投放/回笼 {{cmo_net}}）
- 关键利率：DR007 {{dr007}}% / SHIBOR 1W {{shibor_1w}}%
- 经济数据：{{economic_data_cn}}
- 政策动态：{{policy_news_cn}}

### 3.2 海外宏观
- 美联储动态：{{fed_news}}
- 欧央行动态：{{ecb_news}}
- 地缘政治：{{geopolitics_news}}

### 3.3 重要事件日历
| 时间 | 事件 | 预期 | 前值 | 重要性 |
|------|------|------|------|--------|
| {{event_time}} | {{event_name}} | {{event_forecast}} | {{event_previous}} | {{event_importance}} |

---

## 四、市场状态研判

- **当前研判结论：{{market_regime}}**
  - [ ] 进攻（Risk-On）
  - [ ] 防守（Risk-Off）
  - [ ] 震荡（Range）
  - [ ] 切换（Transition）

**研判依据：**
1. 趋势信号：{{trend_signal}}
2. 资金信号：{{capital_signal}}
3. 情绪信号：{{sentiment_signal}}
4. 结构信号：{{structure_signal}}

**对应策略建议：** {{regime_strategy}}

---

## 五、情绪温度计读数

| 指标 | 当前值 | 阈值（低/高） | 状态 | 信号 |
|------|--------|---------------|------|------|
| 两市成交额 | {{turnover_value}} | {{turnover_threshold}} | {{turnover_status}} | {{turnover_signal}} |
| 涨停/跌停比 | {{limit_ratio}} | {{limit_threshold}} | {{limit_status}} | {{limit_signal}} |
| 涨跌家数比 | {{ad_ratio}} | {{ad_threshold}} | {{ad_status}} | {{ad_signal}} |
| 换手率分位 | {{turnover_pctile}} | {{turnover_pctile_threshold}} | {{turnover_pctile_status}} | {{turnover_pctile_signal}} |
| 融资余额变化 | {{margin_change}} | {{margin_threshold}} | {{margin_status}} | {{margin_signal}} |

**综合情绪温度：{{sentiment_score}} / 100（{{sentiment_level}}）**

---

## 六、资金面预判

### 6.1 北向资金
- 昨日净流入/流出：{{northbound_yesterday}}
- 近 5 日累计：{{northbound_5d}}
- 重点流入行业：{{northbound_industry_in}}
- 重点流出行业：{{northbound_industry_out}}
- 今日预判：{{northbound_forecast}}

### 6.2 机构席位
- 昨日机构净买卖：{{institution_net}}
- 重点个股：{{institution_stocks}}

### 6.3 龙虎榜
- 昨日上榜个股：{{dragon_list}}
- 游资动向：{{hot_money_flow}}
- 机构专用席位：{{dragon_institution}}

---

## 七、今日关注标的清单

| 代码 | 名称 | 所属行业 | 关注逻辑 | 触发条件 | 计划仓位 | 优先级 |
|------|------|----------|----------|----------|----------|--------|
| {{stock_code}} | {{stock_name}} | {{sector}} | {{watch_logic}} | {{trigger_condition}} | {{plan_position}} | {{priority}} |

---

## 八、盘前执行单

### 8.1 买入计划
| 代码 | 名称 | 买入价区间 | 目标仓位 | 止损位 | 止盈位 | 买入理由 |
|------|------|-----------|----------|--------|--------|----------|
| {{stock_code}} | {{stock_name}} | {{buy_price_range}} | {{target_position}} | {{stop_loss}} | {{take_profit}} | {{buy_reason}} |

### 8.2 卖出计划
| 代码 | 名称 | 卖出价区间 | 减仓比例 | 卖出理由 |
|------|------|-----------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{sell_price_range}} | {{reduce_ratio}} | {{sell_reason}} |

### 8.3 关键价位监控
| 代码 | 名称 | 支撑位 1 | 支撑位 2 | 压力位 1 | 压力位 2 | 关注时段 |
|------|------|----------|----------|----------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{support_1}} | {{support_2}} | {{resistance_1}} | {{resistance_2}} | {{focus_session}} |

---

## 九、风险提示

1. {{risk_warning_1}}
2. {{risk_warning_2}}
3. {{risk_warning_3}}

**最大可承受单日亏损：{{max_daily_loss}}**
**组合止损线：{{portfolio_stop_loss}}**

---

> 免责声明：本报告仅为个人投资决策辅助记录，不构成任何投资建议。市场有风险，投资需谨慎。
