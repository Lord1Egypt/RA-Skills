# StockToday Skill

A 股 / 港股 / 美股 / 基金 / 期货数据 Skill，提供 **241** 个数据接口 (基于 Tushare 协议)。

> **📌 重要提示**:
> - **完整接口列表和参数** → 看 [SKILL.md](./SKILL.md)
> - **每个接口的详细 schema** → AI agent 可直接读 `dist/tool_schemas.js` (运行时自动加载)
> - **安装/集成各智能体 (Claude Code/Desktop/Cursor/Cline)** → 看 [INSTALL.md](./INSTALL.md)

## 一句话安装

```bash
npx clawhub install stocktoday
```

装好之后,只要把 `STOCKTODAY_TOKEN` 配到智能体的 MCP 配置里,重启智能体就能用。详见 [INSTALL.md](./INSTALL.md)。

> ⚠️ **改了 `mcp.json` / `claude_desktop_config.json` 必须完全退出并重启智能体进程** —— 只关闭对话窗口不够, 必须 kill 进程再启动, Claude Code/Desktop/Cursor/Cline 都不例外。

## 5 个最高频的使用场景

| 场景 | 工具 |
|---|---|
| 查某只股票今天的行情 | `pro_bar` / `daily` |
| 查某只股票的财务数据 | `income` / `balancesheet` / `cashflow` |
| 查今天的龙虎榜 / 涨停 | `top_list` / `limit_list_d` |
| 查某只股票的十大股东 | `top10_holders` |
| 自查我的 token 状态 | `token_info` |

## 工具速查 (按分类)

> ⚠️ **共 241 个工具**, 这里只列每个分类的代表性工具,完整列表见 [SKILL.md](./SKILL.md)。

### 股票-基础数据 (16)
| 工具 | 说明 |
|---|---|
| `stock_basic` | 股票基本信息 |
| `stock_company` | 上市公司信息 |
| `trade_cal` | 交易日历 |
| `namechange` | 股票名称变更 |
| `new_share` | 新股发行 |
| ... | 还有 11 个,见 SKILL.md |

### 股票-行情数据 (15)
| 工具 | 说明 |
|---|---|
| `daily` | 日线行情 |
| `weekly` | 周线行情 |
| `monthly` | 月线行情 |
| `pro_bar` | 行情(支持复权) |
| `adj_factor` | 复权因子 |
| `daily_basic` | 每日指标 |
| ... | 还有 9 个,见 SKILL.md |

### 股票-财务数据 (17)
| 工具 | 说明 |
|---|---|
| `income` | 利润表 |
| `balancesheet` | 资产负债表 |
| `cashflow` | 现金流量表 |
| `fina_indicator` | 财务指标 |
| `forecast` | 业绩预告 |
| `dividend` | 分红送股 |
| `fina_mainbz` | 主营业务 |
| ... | 还有 10 个,见 SKILL.md |

### 股票-特色数据 (18)
| 工具 | 说明 |
|---|---|
| `top_list` | 龙虎榜上榜 |
| `top_inst` | 龙虎榜机构 |
| `limit_list_d` | 涨跌停明细 |
| `top10_holders` | 十大股东 |
| `top10_floatholders` | 十大流通股东 |
| `pledge_stat` | 股权质押统计 |
| ... | 还有 12 个,见 SKILL.md |

### 股票-资金流向 (8)
| 工具 | 说明 |
|---|---|
| `moneyflow` | 资金流向 |
| `moneyflow_hsgt` | 沪深港通资金流向 |
| `moneyflow_ths` | 资金流向(同花顺) |
| ... | 还有 5 个,见 SKILL.md |

### 指数 (21)
| 工具 | 说明 |
|---|---|
| `index_basic` | 指数基本信息 |
| `index_daily` | 指数日线 |
| `index_weight` | 指数成分 |
| `index_classify` | 指数分类 |
| ... | 还有 17 个,见 SKILL.md |

### 基金/期货/期权/可转债 (37)
| 工具 | 说明 |
|---|---|
| `fund_basic` / `fund_nav` / `fund_daily` | 基金基本信息/净值/日线 |
| `fut_basic` / `fut_daily` | 期货基本信息/日线 |
| `opt_basic` / `opt_daily` | 期权基本信息/日线 |
| `cb_basic` / `cb_daily` | 可转债基本信息/日线 |
| ... | 还有 30 个,见 SKILL.md |

### 港股 / 美股 (19)
| 工具 | 说明 |
|---|---|
| `hk_basic` / `hk_daily` | 港股基本信息/日线 |
| `hk_income` / `hk_balancesheet` / `hk_cashflow` | 港股三大财务报表 |
| `us_basic` / `us_daily` | 美股基本信息/日线 |
| `us_income` / `us_balancesheet` / `us_cashflow` | 美股三大财务报表 |
| ... | 还有 11 个,见 SKILL.md |

### 实时数据 (18)
| 工具 | 说明 |
|---|---|
| `rt_k` | 股票实时日线 |
| `rt_tick` | 股票实时 Tick |
| `rt_min` | 股票实时分钟 |
| `rt_idx_k` / `rt_idx_tick` | 指数实时日线/Tick |
| `rt_etf_k` / `rt_etf_tick` | ETF 实时日线/Tick |
| ... | 还有 11 个,见 SKILL.md |

### 其他 (10)
| 工具 | 说明 |
|---|---|
| `token_info` | **自查 token 状态** (有效期/权限/可用接口) |
| `major_news` / `news` | 资讯 |
| `eco_cal` | 经济日历 |
| `shibor` / `shibor_lpr` | SHIBOR/LPR 利率 |
| ... | 还有 5 个,见 SKILL.md |

---

## 5 个使用示例 (新手必看)

```
User: 查一下茅台今天的行情
→ pro_bar { "ts_code": "600519.SH", "start_date": "20260618", "end_date": "20260618", "adj": "qfq", "freq": "D" }

User: 上证指数今天怎么样?
→ index_daily { "ts_code": "000001.SH", "start_date": "20260618", "end_date": "20260618" }

User: 今天龙虎榜有哪些?
→ top_list { "trade_date": "20260618" }

User: 茅台的财务数据
→ income { "ts_code": "600519.SH", "period": "20251231" }

User: 我的 token 什么时候到期?
→ token_info { }
```

> 💡 **小贴士**:
> - 日期格式统一是 `YYYYMMDD` (8 位无横杠),例如 `20260618`
> - 股票代码格式: A 股 `600519.SH` / 港股 `00700.HK` / 美股 `AAPL.US`
> - 财务接口建议传 `period` (报告期, YYYYMMDD),不传会返回 100+ 条历史记录

## ⚙️ 配置 Token

### 方式 A: 在智能体 MCP 配置里 (推荐)

**Claude Code** (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["~/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["~/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

完整配置 (Claude Desktop / Cline / 其他智能体) 见 [INSTALL.md](./INSTALL.md)。

### 方式 B: 环境变量
```bash
export STOCKTODAY_TOKEN="your_token_here"
```

## 🔄 更新

```bash
npx clawhub update stocktoday
```

更新后**不需要**改 MCP 配置,重启智能体即生效。

## 🆘 故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| 智能体里看不到 stocktoday skill | MCP 配置没生效 | 重启智能体, 检查 JSON 路径 |
| 调工具返 `code:1 TOKEN无效` | token 错/失效 | 调 `token_info` 自查 |
| 调工具超时 | 网络问题 | 检查 `https://tushare.citydata.club/` 通不通 |
| 调工具返 `请求超限` | token 当日额度用完 | 明日 0 点重置, 或换 token |
| 问"今天"返空 | 今天休市 (周末/节假日) | 改问"最近一个交易日" |

## 📞 反馈

- ClawHub: `stocktoday` skill 页面
- 接口详细 schema 文档 (开发/调试用): [INTERFACE.md (GitHub)](https://github.com/stocktoday/stocktoday-skill/blob/main/INTERFACE.md)
- 安装说明: [INSTALL.md](./INSTALL.md)
- 接口速查: [SKILL.md](./SKILL.md)

## License

MIT
