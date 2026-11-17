# stock_data.json 模板

> 这是一个**可直接复制使用**的完整 JSON 模板。  
> 所有字段已用 `占位符` 标记，按需替换。  
> `build.py` 会自动处理 HTML 转义（`esc()`），所以 `<` `>` `&` 都可以直接写，不会破坏布局。

---

## 完整模板（直接复制 → 替换占位符 → 保存为 `${cwd}/stock_data.json`）

```json
{
  "report_date": "YYYY-MM-DD",
  "stock": {
    "name": "股票简称",
    "code": "000000",
    "market": "A股主板 / A股科创板 / A股创业板 / 港股 / 美股",
    "secid": "1.000000 (沪A) / 0.000000 (深A) / 116.000000 (港股) / 105.000000 (美股)",
    "badge": "板块1 · 板块2 · 板块3",
    "company": "公司全称"
  },
  "quote": {
    "price": 0.0,
    "change_pct": 0.0,
    "change_amt": 0.0,
    "mktcap_y": 0,
    "ps": 0.0,
    "pb": 0.0,
    "low_52w": 0.0,
    "high_52w": 0.0,
    "ytd_pct": 0.0,
    "rsi": 0.0
  },
  "fin_items": [
    {"label": "营业收入 (最新季)", "val": "X.XX亿", "sub": "同比 +XX.X%", "note": "2025年报：X.XX亿（同比 +X.X%）", "color": "blue"},
    {"label": "归母净利润 (最新季)", "val": "X.XX亿", "sub": "同比 +XX.X%", "note": "2025年报：X.XX亿", "color": "red"},
    {"label": "毛利率 (最新季)", "val": "XX.X%", "sub": "↑ 修复中", "note": "2025年报：XX.X%", "color": "purple"},
    {"label": "研发费率 (2025)", "val": "XX.X%", "sub": "行业偏高", "note": "研发费用/营收", "color": "amber"},
    {"label": "资产负债率", "val": "XX.X%", "sub": "", "note": "财务稳健", "color": "green"},
    {"label": "每股净资产 (BPS)", "val": "X.XX元", "sub": "", "note": "PB=X.XXx，溢价XX", "color": "blue"}
  ],
  "fin_table": {
    "headers": ["年度", "营收(亿)", "同比", "净利润(亿)", "同比", "毛利率", "ROE", "EPS(元)"],
    "rows": [
      {"cells": ["2023年报", "X.XX", "+X.X%", "X.XX", "+X.X%", "XX.X%", "X.X%", "X.XX"]},
      {"cells": ["2024年报", "X.XX", "+X.X%", "X.XX", "+X.X%", "XX.X%", "X.X%", "X.XX"]},
      {"cells": ["<b>2025Q1</b>", "<b>X.XX</b>", "+X.X%", "X.XX", "+X.X%", "<b>XX.X%</b>", "X.X%", "X.XX"], "highlight": true}
    ],
    "note": "趋势说明文字",
    "trend": [
      {"icon": "📈", "title": "营收趋势", "color": "green", "text": "营收CAGR约XX%；最新季同比+XX.X%"},
      {"icon": "📉", "title": "净利润趋势", "color": "red", "text": "净利润同比变化说明"}
    ]
  },
  "news": [
    {"date": "YYYY-MM-DD", "title": "新闻标题", "sentiment": "positive / neutral / negative", "tag": "正面 / 中性 / 负面"}
  ],
  "news_summary": "近30天情绪总结文字（自动 HTML 转义）",
  "score": {
    "total": 0.0,
    "label": "积极关注 / 观望等待 / 谨慎回避",
    "advice": "投资建议文字",
    "items": [
      {"label": "基本面", "score": 0.0, "color": "amber"},
      {"label": "新闻面", "score": 0.0, "color": "green"},
      {"label": "资金面", "score": 0.0, "color": "red"},
      {"label": "技术面", "score": 0.0, "color": "amber"}
    ]
  },
  "flow": {
    "today_net": 0,
    "bars": [
      {"label": "今日主力净额", "val": 0, "unit": "万", "sign": "流入/流出"},
      {"label": "今日主力净比", "val": 0.0, "unit": "%", "sign": "流入/流出"}
    ],
    "detail": "近5日主力资金说明（可含 <b> / <span class='down'> 标签）"
  },
  "tech": {
    "rsi": 0.0,
    "rsi_note": "超买/中性/超卖说明",
    "macd": "X.XXX 金叉/死叉",
    "macd_note": "DIF vs DEA 说明",
    "kdj": "K=50 D=50 J=50",
    "kdj_note": "K,D,J 位置说明",
    "boll": {"u": 0.0, "m": 0.0, "l": 0.0, "note": "当前价相对布林带位置"},
    "ma": {"ma5": 0.0, "ma20": 0.0, "note": "均线排列说明"},
    "vol_ratio": 1.0,
    "vol_note": "量比说明",
    "alpha_index_name": "沪深300 / 科创板指数 / 恒生科技指数 / 纳斯达克",
    "alpha": [
      {"days": 3, "stock": 0.0, "index": 0.0, "alpha": 0.0},
      {"days": 5, "stock": 0.0, "index": 0.0, "alpha": 0.0},
      {"days": 10, "stock": 0.0, "index": 0.0, "alpha": 0.0},
      {"days": 20, "stock": 0.0, "index": 0.0, "alpha": 0.0}
    ]
  },
  "products": [
    {"name": "产品1", "pct": 50, "color": "blue"},
    {"name": "产品2", "pct": 30, "color": "purple"},
    {"name": "产品3", "pct": 20, "color": "amber"}
  ],
  "products_note": "* 收入占比说明（自动 HTML 转义）",
  "survey": {
    "date": "YYYY-MM-DD",
    "orgs": "机构列表",
    "qas": [
      {"q": "问题1", "a": "回答1"},
      {"q": "问题2", "a": "回答2"}
    ]
  },
  "valuation": {
    "ps": 0.0,
    "ps_pct": 0,
    "pb": 0.0,
    "pb_pct": 0,
    "note": "估值通道说明"
  },
  "index_alpha": {
    "rows": [
      {"label": "近5日 Alpha", "val": 0.0},
      {"label": "近10日 Alpha", "val": 0.0},
      {"label": "近20日 Alpha", "val": 0.0},
      {"label": "近60日 Alpha", "val": 0.0}
    ],
    "warning": "超额收益预警（自动 HTML 转义）"
  },
  "peers": {
    "title": "同行估值与业绩对比（自动取该字段作为标题，避免硬编码行业）",
    "headers": ["公司", "代码", "PE(TTM)", "PB", "PS(TTM)", "营收(最近)", "净利润(最近)"],
    "rows": [
      {"cells": ["本股票", "000000", "XX", "X.Xx", "X.Xx", "XX亿", "X.XX亿"], "highlight": true},
      {"cells": ["同行A", "000000", "XX", "X.Xx", "X.Xx", "XX亿", "X.XX亿"]},
      {"cells": ["同行B", "000000", "XX", "X.Xx", "X.Xx", "XX亿", "X.XX亿"]}
    ],
    "note": "同行对比说明（自动 HTML 转义）"
  },
  "holders": [
    {"rank": 1, "name": "股东名1", "note": "控股股东", "pct": "XX.XX%", "pct_color": "blue", "chg": "不变", "chg_color": "muted"},
    {"rank": 2, "name": "股东名2", "note": "", "pct": "XX.XX%", "pct_color": "blue", "chg": "+0.XX%", "chg_color": "green"}
  ],
  "holders_note": "* 数据来源说明（自动 HTML 转义）",
  "risks": [
    "风险1（自动 HTML 转义）",
    "风险2",
    "风险3"
  ],
  "sources": [
    {"dim": "数据维度", "source": "数据来源", "note": "说明"}
  ],
  "margin": {
    "is_margin_target": true,
    "is_hk_connect": true,
    "margin_balance": "XX.XX亿",
    "margin_balance_chg": "+X.X%",
    "margin_trend": "近5日融资余额变化趋势",
    "short_selling": "XX万股",
    "hk_connect_pct": "X.XX%",
    "hk_connect_chg": "+0.XX%",
    "hk_connect_trend": "北向资金近30日变化趋势"
  },
  "analyst": {
    "rating_count": {"买入": 8, "增持": 3, "中性": 1, "减持": 0},
    "consensus_target": "XX.00",
    "target_high": "XX.00",
    "target_low": "XX.00",
    "recent_ratings": [
      {"date": "YYYY-MM-DD", "org": "机构名", "rating": "买入", "target": "XX.00"}
    ],
    "note": "机构评级说明"
  },
  "corporate_actions": {
    "lockup": [
      {"date": "YYYY-MM-DD", "shares": "XX万股", "pct": "X.X%", "type": "首发原股东限售"}
    ],
    "dividend_history": [
      {"year": "2025", "amount": "10派X.XX元", "yield": "X.X%"}
    ],
    "buyback": "回购进展说明",
    "note": "公司行动风险提示"
  },
  "block_lhb": {
    "block_trades": [
      {"date": "YYYY-MM-DD", "price": "X.XX", "vol": "XX万股", "amount": "XXX万", "premium": "+X.X%", "buyer": "机构专用"}
    ],
    "lhb_records": [
      {"date": "YYYY-MM-DD", "reason": "上榜原因", "net_buy": "XXX万", "main_buyer": "机构专用"}
    ],
    "note": "大宗交易/龙虎榜说明"
  },
  "ai_analysis": {
    "overview": "一句话总评（可含 <b> 标签）",
    "thesis": "核心投资逻辑，2-4 段用 <br> 分行（可含 <b> 标签）",
    "strengths": [
      "优势1（可含 <b> 强调）",
      "优势2",
      "优势3"
    ],
    "weaknesses": [
      "风险1（可含 <b> 强调）",
      "风险2",
      "风险3"
    ],
    "advice_by_profile": [
      {"profile": "🛡️ 保守型投资者", "stance": "建议回避", "tone": "red", "advice": "具体建议（可含 <b>）"},
      {"profile": "⚖️ 稳健型投资者", "stance": "观望等待", "tone": "amber", "advice": "具体建议"},
      {"profile": "🚀 进取型投资者", "stance": "小仓位跟踪", "tone": "green", "advice": "具体建议"}
    ],
    "action_plan": {
      "ideal_entry": "理想买入区间",
      "current_stance": "当前位置态度",
      "target": "目标价 / 上行空间",
      "stop_loss": "止损参考位",
      "position": "仓位建议"
    },
    "triggers": {
      "watch": [
        "🎯 后续跟踪信号1",
        "🎯 后续跟踪信号2",
        "⚠️ 风险信号1"
      ]
    },
    "ending": "结语（可含 <b> 强调）"
  }
}
```

---

## 字段必填与选填

| 字段 | 必填 | 备注 |
|------|------|------|
| `report_date` | ✅ | YYYY-MM-DD 格式 |
| `stock` | ✅ | 全部必填 |
| `quote` | ✅ | `mktcap_y` 单位**元**（不是亿），如 37410000000 |
| `fin_items` | ✅ | 建议 6 个，`color` ∈ {blue, red, purple, amber, green} |
| `fin_table` | ✅ | `rows[].cells` 8 列；`highlight: true` 高亮整行 |
| `news` | ✅ | 至少 3 条；`sentiment` ∈ {positive, neutral, negative} |
| `score` | ✅ | `total` 0-10，4 个 items |
| `flow` | ✅ | `today_net` 单位**万元** |
| `tech` | ✅ | 6 个指标必填；`alpha_index_name` 必填 |
| `products` | ⚠️ 选填 | 无数据时省略整个字段 |
| `products_note` | ⚠️ | 配合 products |
| `survey` | ⚠️ | 机构调研信息 |
| `valuation` | ✅ | `ps_pct` / `pb_pct` 0-100 |
| `index_alpha` | ✅ | 4 个时间窗口 |
| `peers` | ✅ | 至少 3 行；建议加 `title` 字段避免硬编码 |
| `holders` | ✅ | 至少 5 行；`chg` 四选一：不变 / ±X.XX% / 新进 / 减持 |
| `holders_note` | ⚠️ | |
| `risks` | ✅ | 至少 3 条 |
| `sources` | ✅ | 至少 5 条 |
| `margin` | ⚠️ | 非融资融券 / 非沪深港通时 `is_margin_target: false` |
| `analyst` | ⚠️ | 无评级时省略整个字段 |
| `corporate_actions` | ⚠️ | |
| `block_lhb` | ⚠️ | |
| `ai_analysis` | ⚠️ 强烈推荐 | SEC 17 核心内容 |

---

## ⚠️ 文本字段安全规则（2026-07 经验教训）

`build.py` 内部对所有文本字段调用 `esc()` 转义 `& < >`，所以**直接写 `<` `>` `&` 是安全的**（会被转义为 `&lt;` `&gt;` `&amp;`，用户看到的是字面字符，不会破坏 HTML）。

### ✅ 允许的 HTML 标签（保留）

| 标签 | 用途 | 字段示例 |
|------|------|----------|
| `<b>...</b>` | 加粗 | `ai_analysis.overview`, `thesis`, `advice`, `triggers.watch[]`, `ending`, `fin_table.rows[].cells[]` |
| `<br>` | 换行 | `ai_analysis.thesis` |
| `<span class="up">` | 红色文字 | `flow.detail` |
| `<span class="down">` | 绿色文字 | `flow.detail` |
| `<i>...</i>` | 斜体 | 任意文本 |

### ❌ 绝对禁止

1. **未配对的 HTML 标签** —— 文本中类似 `<MA20=445` 这种伪标签会被浏览器解析，破坏布局
   - ✅ 正确：使用文字"MA5 小于 MA20"或保留全角符号
   - ❌ 错误：保留原始半角 `<` `>` 描述比较关系
2. **手动写 `&amp;` 转义** —— `build.py` 会自动转义，写了反而双重转义
3. **在 `news[].title` 中写完整 HTML** —— title 字段只显示文本，加 HTML 标签会显示成字面字符

### 颜色语义（advice_by_profile.tone）

| tone | 含义 | 适用场景 |
|------|------|----------|
| `red` | 保守/谨慎/回避 | 估值过高、风险大、观望为主 |
| `amber` | 稳健/中性/等待 | 估值合理、需要催化剂 |
| `green` | 进取/积极/机会 | 估值底部、催化剂临近 |

### color 字段（多个位置）

取值范围：`blue`, `red`, `green`, `amber`, `purple`, `muted`  
- `muted` = 灰色（用于"不变"等中性变化）
- 涨红跌绿（A股惯例），但 `pct_color` 用于持股比例，`chg_color` 用于变化

---

## 板块标签 (stock.badge) 写法

格式：`板块1 · 板块2 · 板块3`（用 ` · ` 中圆点分隔，2-4 个）

示例：
- 安凯微: `"科创板 · 半导体 · AI芯片"`
- 腾讯控股: `"港股 · 互联网 · 社交媒体"`

---

## SEC 17 AI 综合点评结构（重点）

5 个独立块，**每个块独占一行**（5x1 布局）：

1. **一句话总评** (overview)：`<b>` 加粗核心结论
2. **核心逻辑** (thesis)：`<br>` 分段，每段 1-2 句
3. **优势 / 风险** (strengths / weaknesses)：各 3-5 条
4. **分类型投资者建议** (advice_by_profile)：3 类投资者
5. **操作策略参考** (action_plan)：5 个字段
6. **后续关键跟踪信号** (triggers.watch)：3-6 条
7. **结语** (ending)：1-3 句总结

⚠️ **不要在 strengths/weaknesses 里写类似 `MA5<MA20` 的描述**，会被 `esc()` 转义为字面字符 `MA5&lt;MA20`，影响可读性。用"MA5 小于 MA20"代替。

---

## 完整使用流程

> **路径规范**：所有中间文件必须落在 `${cwd}`（当前工作目录）之下，**禁止**使用 `/tmp/...` 硬编码——Windows 无 `/tmp`，且易造成路径逃逸。`build.py` 已内置 `${cwd}` 校验，越界会被拒绝。

```bash
# 0. 假设当前工作目录为 $PWD（Windows PowerShell 用 $PWD，cmd 用 %CD%）
cd /Users/songxf/WorkBuddy/YYYY-MM-DD   # 或用户自己的项目目录

# 1. 复制 JSON 模板到 ${cwd}/stock_data.json
cp stock_data_template.json "$PWD/stock_data.json"

# 2. 用 Python 脚本分块填充数据（避免 Write 工具超过 5KB 限制）
python3 "$PWD/build_json.py"            # 脚本内部用 os.getcwd() 拼接文件名

# 3. 运行 build.py 生成 HTML（两个路径都必须位于 ${cwd} 之内）
python3 ~/.workbuddy/skills/stock-deep-report/references/build.py \
    "$PWD/stock_data.json" \
    "$PWD/000000_股票名_三维深度分析报告_YYYYMMDD.html"
```
