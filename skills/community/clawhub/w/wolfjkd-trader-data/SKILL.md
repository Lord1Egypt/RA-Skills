# A股数据获取体系 - 快速部署指南
> **Skill名称**：wolfjkd-trader-data
> **当前版本**：**v3.0**（2026-05-22）
> **作者**：wolfjkd
> **开源协议**：MIT

> 本skill记录A股交易员数据获取的完整解决方案，含多源智能路由能力
> **适用场景**：新机器部署、数据源容错、定时任务搭建、AI Agent数据获取集成

---

## 📊 数据获取架构

```
┌──────────────────────────────────────────────────────────────────────┐
│                        A股数据获取体系                                │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────┤
│   行情数据    │    公告数据   │    新闻数据   │   大宗商品   │ 深度数据 │
├──────────────┼──────────────┼──────────────┼──────────────┼─────────┤
│  腾讯接口 ✅  │ ftshare ✅   │ WebSearch ✅ │ 腾讯接口 ✅  │ Wind ✅  │
│  (毫秒级)    │  (无需Key)   │  (兜底)     │  (无需Key)   │(需API Key)│
│  实时快照    │  A股公告     │  财经资讯    │  黄金银油    │财务/资金/ │
│             │             │             │             │板块/宏观/ │
│             │             │             │             │公告RAG/  │
│             │             │             │             │技术指标   │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘
```

---

## 🎯 数据类型与数据源

### 1. 行情数据（腾讯接口，开箱即用）

| 数据类型 | 接口地址 | 示例 |
|---------|---------|------|
| A股指数 | `https://qt.gtimg.cn/q=sh000001,sz399001,sz399006` | 上证/深证/创业板 |
| 自选股 | `https://qt.gtimg.cn/q=sh600170,sh603077,sz000061` | 自定义股票列表 |
| 美股指数 | `https://qt.gtimg.cn/q=usINDU,usIXIC,usINX` | 道指/纳斯达克/标普 |
| 大宗商品 | `https://qt.gtimg.cn/q=hf_GC,hf_SI,hf_CL` | 黄金/白银/原油 |
| 数字货币 | `https://qt.gtimg.cn/q=gb_BTCJPY` | 比特币等 |

**获取方式**：
```bash
# 获取数据（Python）
import subprocess
result = subprocess.run(['curl', '-s', 'https://qt.gtimg.cn/q=sh000001'], capture_output=True, text=True)
```

### 2. 公告数据（ftshare-announcement-data，首选）

**安装**：
```bash
npx openclaw skills install shawn92/ftshare-announcement-data
# 或移动到workbuddy目录
mv ~/.openclaw/workspace/skills/ftshare-announcement-data ~/.workbuddy/skills/
```

**使用**：
```bash
# 单只股票公告历史（示例：贵州茅台）
python <FTSHARE_SKILL_DIR>/run.py \
  stock-announcements-single-stock-all-periods \
  --stock-code 600519.SH \
  --page 1 --page-size 10

# 全市场某日公告
python <FTSHARE_SKILL_DIR>/run.py \
  stock-announcements-all-stocks-specific-date \
  --start-date 20260520 \
  --page 1 --page-size 20
```

**股票代码格式**：
- 上海：`600519.SH`
- 深圳：`000001.SZ`
- 创业板：`300xxx.SZ`
- 科创板：`688xxx.SH`

### 3. 新闻数据（WebSearch，兜底方案）

```bash
# 公告搜索示例
"贵州茅台 600519 公告 今天"
"比亚迪 002594 公告 最新"

# 新闻搜索示例
"XX股票 最新消息 今天"
"今日财经新闻 20260520"
"AI 科技 最新"
```

### 4. 板块/资金数据（WebSearch备选）

> akshare东方财富接口可能被拒，已内置Wind作为稳定替代

```bash
# 搜索关键词
"A股涨幅前5板块"
"北上资金 净流入"
"今日市场异动"
```

### 5. Wind深度数据（万得金融，核心补充）

> **定位**：填补腾讯接口无法覆盖的**财务报表、资金流向、板块行情、技术指标、宏观指标**等深度数据空白

#### 5.1 安装与配置

```bash
# Wind万得金融Skill（Gitee源，推荐国内用户）
npx skills add https://gitee.com/wind_info/wind-skills.git --skill wind-mcp-skill -g -y
npx skills add https://gitee.com/wind_info/wind-skills.git --skill wind-find-finance-skill -g -y

# 配置API Key（需要Wind开发者账号）
node <WIND_SKILL_DIR>/scripts/cli.mjs open-portal
# 拿到Key后配置
node <WIND_SKILL_DIR>/scripts/cli.mjs setup-key <YOUR_KEY> --scope global
```

#### 5.2 核心Server类型（8个）

| server_type | 能力覆盖 | 适用场景 |
|-------------|---------|---------|
| `stock_data` | A股行情+基本面+技术指标+风险 | 个股深度分析 |
| `global_stock_data` | 港股/美股同上 | 海外标的行情 |
| `fund_data` | ETF/基金全维数据 | ETF套利/折溢价监控 |
| `index_data` | 指数/板块行情+PE/PB分位+技术 | 大盘/板块分析 |
| `bond_data` | 债券档案+估值+主体财务 | 宏观对冲参考 |
| `financial_docs` | 公告RAG+财经新闻RAG | 公告/新闻语义搜索 |
| `economic_data` | EDB宏观/行业经济指标 | GDP/CPI/PMI等宏观数据 |
| `analytics_data` | NL通用入口(兜底) | 跨域综合查询 |

#### 5.3 常用查询速查表

**📈 行情快照**
```bash
# 个股最新价+涨跌幅+成交量
node <WIND_SKILL_DIR>/scripts/cli.mjs call stock_data get_stock_price_indicators \
  '{"windcode":"600519.SH","indexes":"中文简称,最新成交价,涨跌幅,成交量,换手率,市盈率(TTM),市净率"}'
```

**📊 K线历史**
```bash
# 日K线（近30个交易日）
node <WIND_SKILL_DIR>/scripts/cli.mjs call stock_data get_stock_kline \
  '{"windcode":"600519.SH","begin_date":"20260418","end_date":"20260522","count":30}'
```

**💰 财务基本面**
```bash
# ROE+净利润增速（自然语言查询）
node <WIND_SKILL_DIR>/scripts/cli.mjs call stock_data get_stock_fundamentals \
  '{"question":"贵州茅台2024年ROE和净利润增速"}'
```

**📐 技术指标**
```bash
# MACD/KDJ/RSI/BOLL
node <WIND_SKILL_DIR>/scripts/cli.mjs call stock_data get_stock_technicals \
  '{"question":"贵州茅台近60日MACD和RSI走势"}'
```

**🏭 板块/指数**
```bash
# 指数PE/PB历史分位
node <WIND_SKILL_DIR>/scripts/cli.mjs call index_data get_index_fundamentals \
  '{"question":"沪深300指数PE/PB历史分位"}'
```

**📰 公告RAG**
```bash
# 个股公告搜索
node <WIND_SKILL_DIR>/scripts/cli.mjs call financial_docs get_company_announcements \
  '{"query":"贵州茅台最新公告","top_k":5}'
```

**🌍 宏观指标**
```bash
# 中国CPI/PPI
node <WIND_SKILL_DIR>/scripts/cli.mjs call economic_data get_economic_data \
  '{"metricIdsStr":"中国CPI同比","freq":"月","beginDate":"20250101","endDate":"20260522"}'
```

#### 5.4 Wind vs 其他数据源分工

| 数据需求 | 首选 | 备选 | 说明 |
|---------|------|------|------|
| 实时价格快照 | **腾讯接口** | Wind `stock_data` | 腾讯毫秒级，Wind字段更丰富但有延迟 |
| 历史K线 | **Wind** | AkShare腾讯K线 | Wind数据质量更高 |
| A股公告 | **ftshare** | **Wind RAG** | ftshare按日期列表，Wind按内容语义搜索 |
| 财经新闻 | WebSearch | **Wind RAG** | Wind新闻RAG质量高 |
| 财务报表/ROE/盈利 | **Wind** | 无 | 只有Wind能取到 |
| 技术指标(MACD/RSI) | **Wind** | 无 | 只有Wind能取到 |
| 板块涨跌/资金流向 | **Wind** `index_data` | WebSearch | Wind可取板块行情+PE分位 |
| 北上资金/资金流 | **Wind** NL | WebSearch | analytics_data或NL工具 |
| 宏观指标(GDP/CPI) | **Wind** | WebSearch | Wind EDB数据库 |

#### 5.5 Wind注意事项

- ⚠️ **有日调用额度**：不要在循环中无节制调用，优先腾讯接口做实时快照
- ⚠️ **单工具单标的**：批量查询需循环调用，不要传逗号分隔多代码
- ⚠️ **命令必须在skill目录下执行**：CLI用相对路径加载资源
- ⚠️ **结果标注合规要求**：使用Wind数据时必须标注「数据来源于万得Wind金融数据服务」
- ✅ **indexes字段只接中文名**：从 `wind-mcp-skill/references/indicators.md` 复制
- ✅ **NL question/query禁止空格**：用标点符号或直接连接替代空格

---

## 📚 AkShare可用接口（v1.18.63实测）

> ⚠️ 注意：东方财富接口（push2.eastmoney.com）可能被拒，但部分腾讯/新浪接口可用

### ✅ 可用接口

| 接口 | 数据类型 | 代码示例 |
|------|---------|---------|
| `stock_zh_a_hist_tx` | 腾讯历史K线 | 见下方 |
| `stock_news_em` | 财经早餐新闻 | 见下方 |

```python
import akshare as ak

# 1. 腾讯历史K线（推荐，无需代理）
df = ak.stock_zh_a_hist_tx(
    symbol='sz000001',      # 股票代码（sz/sz000001格式）
    start_date='20260518',
    end_date='20260520',
    adjust=''               # ''不复权, 'qfq'前复权
)

# 2. 财经早餐新闻
df = ak.stock_news_em()

# 3. 巨潮资讯个股公告
df = ak.stock_zodiac_em(symbol='000001')
```

### ❌ 不可用接口（东方财富被拒）

| 接口 | 原因 | 替代方案 |
|------|------|---------|
| `stock_zh_a_spot_em` | 东方财富被拒 | 腾讯接口curl |
| `stock_zh_index_spot_em` | 东方财富被拒 | 腾讯接口curl |
| `stock_hsgt_*` | 北上资金接口 | WebSearch / Wind |

### 🔧 AkShare安装命令

```bash
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade
```

---

## 🔄 多源数据智能路由（data_router.py）

> **定位**：自动检测数据源健康状态，评分择优，解决免费接口临时失效问题
>
> **依赖**：Python 3.x 标准库（**无需额外安装任何包**）

### 6.1 核心架构

```
请求 → probe_sources(数据类型)
    │
    ├── ThreadPoolExecutor 并行探测（最多4线程）
    │     ├── TencentAdapter  (行情/指数/大宗商品)
    │     ├── WindAdapter      (深度数据/个股)
    │     └── FtShareAdapter   (公告)
    │
    ↓ 每个适配器独立返回 DataSourceResult
    │
    select_best(results) → 按score降序，≥50分使用，接近时选更快
```

### 6.2 评分模型

| 维度 | 权重 | 腾讯标准 | Wind标准 | ftshare标准 |
|------|------|---------|---------|------------|
| 可用性 | 40% | 连通且有数据=100 | 连通=100 | 连通=100 |
| 及时性 | 25~30% | <500ms=100, >5s=10 | <1.5s=100, >10s=10 | <2s=100, >15s=20 |
| 质量 | 30~35% | 数据完整度+数值合理 | 有内容且无error=95 | 返回条数≥5=95 |

**等级**：A级≥85 / B级≥70 / C级≥50 / D级<50

### 6.3 CLI命令

```bash
python data_router.py health                              # 健康检测
python data_router.py quote --codes sh000001 --json        # 行情(JSON)
python data_router.py watchlist --json                     # 自选股(JSON)
python data_router.py compare --code 600519.SH --type quote # 多源对比
```

### 6.4 定时任务集成

晚间报告推荐流程：
1. `python data_router.py health` — 确认哪些源活着
2. `python data_router.py quote --json` — 行情JSON
3. `python data_router.py watchlist --json` — 自选股JSON
4. 公告/新闻根据health结果选源，报告标注来源和评分

### 6.5 已知限制

| 限制 | 状态 | 改进方向 |
|------|------|---------|
| Wind一致性检查嵌套JSON | 解析不完美 | 优化envelope提取 |
| 无缓存机制 | 每次实时探测 | 加短时间缓存 |
| 仅3个数据源 | 覆盖主场景 | 可扩展WebSearch |

### 6.6 配置自选股

编辑 `data_router.py` 中的 `WATCHLIST` 列表即可自定义你的自选股：

```python
WATCHLIST = [
    ("sh600519", "贵州茅台"),   # 示例：修改为你的持仓
    ("sz000001", "平安银行"),
    ("sh600036", "招商银行"),
    # ... 继续添加
]
```

---

## 🔄 备用方案（容错策略）

| 数据类型 | 首选 | 备用1 | 备用2 |
|---------|------|-------|-------|
| 行情快照 | 腾讯接口 | Wind stock_data | - |
| 历史K线 | Wind stock_data | AkShare腾讯K线 | - |
| 公告 | ftshare | Wind financial_docs RAG | WebSearch |
| 新闻 | WebSearch | Wind financial_docs RAG | - |
| 财务/技术指标 | **Wind** | 无 | - |
| 板块/资金/宏观 | **Wind** (index_data/economic_data) | WebSearch | - |

**自动切换逻辑**（两种模式）：

**模式1：智能路由（推荐，使用data_router.py）**
```
并行探测所有候选源 → 评分排序 → 选最优(≥50分) → 接近时选更快
命令: python data_router.py health / quote / watchlist
```

**模式2：链式降级（手动/脚本）**

---

## 🚀 快速部署步骤

### 新机器部署清单

1. **安装基础依赖**
```bash
pip install akshare
```

2. **安装核心Skills**
```bash
# ftshare公告（来自clawhub.ai）
npx openclaw skills install shawn92/ftshare-announcement-data

# Wind万得金融（Gitee源，推荐国内）
npx skills add https://gitee.com/wind_info/wind-skills.git --skill wind-mcp-skill -g -y
npx skills add https://gitee.com/wind_info/wind-skills.git --skill wind-find-finance-skill -g -y

# 其他推荐Skills（按需）
npx openclaw skills install openclaw/skills/tencent-finance
npx openclaw skills install sugarforever/01coder-agent-skills/china-stock-analysis
```

3. **配置Wind API Key**（可选，有Wind账号的话）
```bash
node <WIND_SKILL_DIR>/scripts/cli.mjs open-portal
node <WIND_SKILL_DIR>/scripts/cli.mjs setup-key <YOUR_KEY> --scope global
```

4. **测试数据源**
```bash
# 测试腾讯接口
curl -s "https://qt.gtimg.cn/q=sh000001"

# 测试智能路由
python data_router.py health
```

---

## ⚠️ 已知限制

| 限制项 | 说明 | 解决方案 |
|-------|------|---------|
| akshare东方财富 | 连接可能被拒 | 腾讯接口/Wind替代 |
| Wind日调用额度 | 有上限，省着用 | 实时快照优先腾讯接口，深度分析才用Wind |
| Wind单工具单标的 | 批量需循环 | 写for循环逐只调用 |
| 港股/美股数据 | 腾讯接口字段有限 | Wind global_stock_data |

---

## 🔧 故障排除

### 腾讯接口失败
- 检查网络连接
- 可能是临时故障，5分钟后重试

### ftshare返回空
- 检查日期格式（YYYYMMDD）
- 确认股票代码格式正确（600519.SH）
- 切换Wind financial_docs RAG或WebSearch备用方案

### WebSearch无结果
- 换用不同关键词
- 检查日期是否正确（今天是工作日？）
- 尝试英文关键词

### Wind调用失败
- **KEY_MISSING**：执行 `node <WIND_SKILL_DIR>/scripts/cli.mjs open-portal` 重新配置
- **RATE_LIMIT_DAILY**：日额度用完，切换腾讯接口/WebSearch
- **INVALID_PARAMS_JSON**：检查shell转义（Bash单引号/PowerShell反斜杠）
- **NETWORK_ERROR**：等3-5秒后重试
- 确认命令在wind-mcp-skill目录下执行

### data_router.py报错
- **"Wind CLI不存在"** → 未安装wind-mcp-skill，忽略即可（自动降级为腾讯接口）
- **"ftshare run.py不存在"** → 未安装ftshare-announcement-data，公告功能暂不可用
- **超时** → 检查网络连接，增加TIMEOUTS配置

---

## 📋 版本变更日志

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| **v3.0** | 2026-05-22 | 新增 `data_router.py` 多源智能路由；SKILL.md新增第6节；容错策略升级为智能路由模式 |
| **v2.0** | 2026-05-22 | 整合Wind万得金融能力：8个server_type、速查表、分工对照表；架构从4列扩展为5列 |
| **v1.0** | 2026-05-20 | 初始版本：腾讯接口+ftshare公告+WebSearch+AkShare数据源体系 |

---

*本skill由 wolfjkd 开源维护，当前版本：**v3.0** | MIT License*
