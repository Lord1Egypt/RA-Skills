---
name: stock-query
description: >
  查询全球股票实时行情（A 股、港股、美股）、ETF、场外基金、指数，支持批量查询、历史K线（含均线）与自选股管理。
  TRIGGER when: 用户查询股价/行情/净值/历史K线/自选盈亏/大盘指数时。NOT for: 加密货币、期货、期权、外汇。
license: MIT
compatibility: Requires curl, iconv, python3. macOS/Linux only.
metadata:
  version: "2.6.0"
  author: asfamilybank
  repo: https://github.com/asfamilybank/stock-query
user-invocable: true
allowed-tools:
  - Bash
---

# 全球股票/ETF/基金/指数 实时价格查询

## 权限与操作范围

| 权限 | 声明用途 | 限制 |
|------|---------|------|
| `network` | `scripts/sq.sh` 内部调用行情 API | 仅限 `qt.gtimg.cn`、`hq.sinajs.cn`、`push2.eastmoney.com`、`web.ifzq.gtimg.cn`、`query1.finance.yahoo.com`、`fundgz.1234567.com.cn`、`api.fund.eastmoney.com` 七个数据源，不发送用户个人数据 |
| `shell` | 执行 `curl`、`iconv`、`grep`、`awk`、`mktemp` | 仅操作 `portfolio.csv`；不执行任意命令 |

**文件访问：** 本 skill 仅在用户**显式指令**下读写 `portfolio.csv` 一个文件，优先查找 `~/.config/stock-query/portfolio.csv`，其次兼容旧版安装目录（`~/.openclaw/workspace/skills/stock-query/`、`~/.claude/skills/stock-query/`、`~/.agents/skills/stock-query/`），无需配置任何环境变量。历史数据通过网络实时获取，不写本地文件。

**自动触发范围：** **文件操作（Command 1）不会自动触发**，仅在用户明确发出增/删/改/查 portfolio 指令时执行。

⚠️ **凭证安全：** `portfolio.csv` 仅应包含股票代码、名称、数量、自选价格。**禁止存放账户密码、API 密钥、Token 或任何认证凭证。**

## 前置依赖

| 工具 | 说明 |
|------|------|
| `scripts/sq.sh` | 行情查询 CLI，内部使用 `curl` + `iconv` |
| `scripts/fmt.sh` | 格式化输出工具，由 `sq.sh --format` 调用，依赖 `python3`，输出人类可读的 Markdown 表格 |

## 支持的市场与标的

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| 沪/深市股票、ETF、指数 | 6 位数字 | `601991`、`510300`、`000001` |
| 港股 | ≤5 位数字（自动补零） | `700`、`00700`、`09988` |
| 美股 | 英文 ticker | `AAPL`、`TSLA`、`BIDU` |
| 美股指数 | `.DJI` / `.IXIC` / `.SPX` | `.DJI` |
| 场外基金 | 6 位数字 | `014978`、`110011` |

---

## 工作流程

### Step 0: 意图识别与 Command 路由

**Meta 命令**（最高优先级）：输入为 `version`、`-v`、`--version`、`help`、`-h`、`--help`（大小写不敏感）
→ 直接输出版本/帮助信息，**不执行后续步骤**

version 输出：
```
stock-query v2.6.0
```

help 输出：
```
stock-query v2.6.0 — 全球股票/ETF/基金/指数实时行情查询

用法：
  /stock-query <代码> [代码2 ...]   查询一个或多个标的实时行情
  /stock-query <代码> 历史          查询个股历史K线（默认近30个交易日）
  /stock-query version              显示版本号
  /stock-query help                 显示本帮助

支持的市场：
  A股（沪/深）  6位数字，如 601991 000001
  港股          5位数字，如 00700 09988
  美股          英文ticker，如 AAPL TSLA NVDA
  美股指数      .DJI  .IXIC  .SPX
  ETF           6位数字，如 510300 159915
  场外基金      6位数字，如 014978

常用示例：
  /stock-query AAPL
  /stock-query 00700 09988
  /stock-query AAPL 00700 601991 510300
  /stock-query 600519 近60天日K
  /stock-query TSLA 周K 最近20周

作者：asfamilybank · https://github.com/asfamilybank/stock-query
```

**Command 1：Portfolio 文件管理**：含操作词（添加/新增/删除/移除/修改/查看/列出）＋ 对象词（自选股/持仓/portfolio/watchlist），或明确指令如"把 AAPL 加到自选股"
→ 直接执行 Command 1，**不进入 Command 2/3 流程**

**Command 3：历史行情查询**：含关键词（历史/历史数据/历史行情/历史价格/历史走势/K线/日K/周K/月K）
→ 直接执行 Command 3，**不进入 Command 2 流程**

**Command 2：行情查询**（默认）：其余所有输入 → 进入 Command 2 流程（执行 Step 1–6）

---

## 静默执行原则（Claude 对话输出约束）

**⛔ 严禁向用户输出任何中间推理或过程信息。** 这是最高优先级约束，覆盖所有步骤。

> 本约束仅适用于 Claude 的对话文本输出。`scripts/sq.sh` stdout 仅输出结构化数据供 Claude 内部消费：行情/基金命令输出 JSON 数组，`pfile` 命令输出文件绝对路径或控制令牌 `NOT_FOUND`；stderr 输出错误/用法提示。`scripts/fmt.sh` 是格式化渲染层，接收 `sq.sh` 的 JSON 输出，输出供用户直接查看的 Markdown 表格（含涨跌 emoji、CJK 对齐、均线列）；其 stdout 为最终展示内容，非过程日志。两个脚本均不向用户界面打印任何过程信息。

以下内容**绝对禁止出现**在回复中：
- 市场/类型判断（如"014978 是场外基金"）
- 数据源切换说明（如"腾讯接口返回空，切换至东方财富："）
- 文件路径查找过程
- 任何形式的"正在..."、"切换..."、"尝试..."等过程性文字

**唯一允许的输出：** 最终结果表格，或无法查询时的错误提示。

---

## Command 1: Portfolio 文件管理

**所有增删改查操作必须通过 Bash 工具执行实际命令，禁止依赖会话记忆。未执行命令不得声称操作已完成。**

### 文件定位（每次进入 Command 1 必须首先执行）

```bash
PFILE=$(bash scripts/sq.sh pfile)
echo "$PFILE"
```

- 输出 `NOT_FOUND` → 立即向用户输出下方创建引导，停止执行，**不得创建任何替代文件**
- 否则将 `$PFILE` 用于所有后续操作

**portfolio.csv 不存在时**，引导用户创建：
```
未找到自选股文件。请执行以下步骤创建：

1. 创建配置目录并复制模板：
   mkdir -p ~/.config/stock-query
   cp <skill安装目录>/assets/portfolio.csv ~/.config/stock-query/portfolio.csv

2. 编辑文件，填入你的自选股信息。
```

**CSV 文件格式**（参考 `assets/portfolio.csv`）：

```
代码,名称,数量,自选价格
601991,大唐发电,1000,4.00   # 含数量与参考价，输出浮盈亏
014978,华安纳指100C,10000,  # 自选价格留空：只查行情
AAPL,,50,220.00             # 名称留空：自动从接口获取
000300,,0,                  # 数量为 0：纯自选
```

### 查

```bash
grep -v '^#' "$PFILE" | tail -n +2
```

格式化为表格展示，不查询实时行情。如需实时价格，使用 Command 2。

### 增

1. 用 `bash scripts/sq.sh get <code>` 获取标的名称
2. 执行：
```bash
if grep -q "^{code}," "$PFILE" 2>/dev/null; then
  echo "DUPLICATE:{code}"
else
  echo "{code},{name},{shares},{cost}" >> "$PFILE" && echo "ADDED:{code},{name},{shares},{cost}"
fi
```
3. `ADDED:...` → 展示添加结果；`DUPLICATE:{code}` → 询问是否改为修改操作

### 改

1. 用 `bash scripts/sq.sh get <code>` 获取最新名称
2. 执行：
```bash
OLD=$(grep "^{code}," "$PFILE")
if [ -z "$OLD" ]; then
  echo "NOT_FOUND:{code}"
else
  NEW="{code},{name},{shares},{cost}"
  tmp=$(mktemp)
  awk -F',' -v c="{code}" -v n="$NEW" \
    'BEGIN{OFS=","} $1==c{print n;next}{print}' "$PFILE" > "$tmp" && mv "$tmp" "$PFILE"
  echo "BEFORE:$OLD"
  echo "AFTER:$NEW"
fi
```
3. 展示修改前后 diff；`NOT_FOUND:{code}` → 提示未找到

### 删

```bash
DEL=$(grep "^{code}," "$PFILE")
if [ -z "$DEL" ]; then
  echo "NOT_FOUND:{code}"
else
  tmp=$(mktemp)
  grep -v "^{code}," "$PFILE" > "$tmp" && mv "$tmp" "$PFILE"
  echo "DELETED:$DEL"
fi
```

`DELETED:...` → 展示删除结果；`NOT_FOUND:{code}` → 提示未找到

---

## Command 2: 行情查询

### Step 1: 解析用户输入

**detail_mode 检测：** 若用户消息含以下关键词，设 `detail_mode = true`，在 Step 3 输出详细表格：
- 中文：详细、详情、详细信息、更多信息、全部信息、完整信息
- 英文：detail、details、verbose、full

从用户消息中提取标的代码，支持以下形式：
- **6 位纯数字** → A 股（股票/ETF/指数/基金）
- **≤5 位纯数字** → 港股，自动补零（700 → 00700）
- **英文字母或英文+数字** → 美股 ticker
- **中文/英文名称** → 匹配下表常见标的；无法确定时向用户确认

常见标的速查：

**A 股：**
- 黄金ETF → 518880 / 红利低波ETF → 512890 / 沪深300ETF → 510300
- 卫星ETF → 563230 / 创业板ETF → 159915 / 中证500ETF → 510500
- 上证指数 → 000001 / 深证成指 → 399001 / 创业板指 → 399006
- 沪深300 → 000300 / 上证50 → 000016 / 中证500 → 000905 / 中证1000 → 000852

**港股：**
- 腾讯 → 00700 / 阿里巴巴 → 09988 / 美团 → 03690 / 小米 → 01810
- 比亚迪 → 01211 / 恒生指数 → HSI

**美股：**
- 苹果 → AAPL / 谷歌 → GOOG / 特斯拉 → TSLA / 英伟达 → NVDA
- 微软 → MSFT / 亚马逊 → AMZN / 百度 → BIDU / 阿里巴巴 → BABA
- 哔哩哔哩 → BILI / 拼多多 → PDD
- 道琼斯 → .DJI / 纳斯达克 → .IXIC / 标普500 → .SPX

### Step 2: 查询并格式化输出

```
Step 2A: 执行命令（不得省略 --format 参数，单支/批量/任意市场均适用）
  detail_mode = false → bash scripts/sq.sh get <code1> [code2 ...] --format table
  detail_mode = true  → bash scripts/sq.sh get <code1> [code2 ...] --format table --detail

Step 2B: 将命令的 stdout 原样作为回复返回
  ⛔ 不得解析 JSON 自行构建表格
  ⛔ 不得修改 emoji 字符（A股/港股：涨🔴跌🟢；美股：涨🟩跌🟥）
  ⛔ 不得添加、删除或重排列
```

**⛔ 特别注意：港股跌幅用 🟢（非 🔴）。** A股、港股均遵循中国市场惯例：上涨 🔴，下跌 🟢，平盘 ⚪。命令输出已正确处理，勿覆盖。

### Step 4: 自选市值计算（可选）

#### 4a. 从 portfolio 文件加载

当用户指令涉及自选股（如"查我的自选股""看下自选股"），先定位文件再批量查询：

```bash
PFILE=$(bash scripts/sq.sh pfile)
```

- 输出 `NOT_FOUND` → 立即输出创建引导（见 Command 1），停止执行
- 否则读取文件，提取所有代码后用 `sq get` 批量查询

执行步骤（严格按序）：

```
Step A: 读取全部条目
  codes_all      = 文件中所有非注释、非表头行
  codes_position = codes_all 中数量 > 0 的条目
  codes_watch    = codes_all 中数量 = 0 或空的条目

Step B: 批量查询
  bash scripts/sq.sh get <codes_all 中所有代码>

Step C: 输出自选市值表（若 codes_position 非空）
  横向宽表格：代码/名称/数量/自选价格/现价/市值/浮盈亏/盈亏比

Step D: 输出自选行情表（若 codes_watch 非空）← 必须执行，不得省略
  标题"自选行情"，简表：代码/名称/现价/涨跌幅
```

**⚠️ Step D 不得跳过。** 数量=0 的条目不进市值表，但必须出现在 Step D。

输出示例：

```
| 代码   | 名称     | 数量    | 自选价格 | 现价    | 市值      | 浮盈/亏      | 盈亏比      |
|--------|---------|--------|---------|--------|----------|------------|------------|
| 601991 | 大唐发电 | 1000股 | 4.00    | 4.08   | 4,080    | 🔴 +80     | 🔴 +2.00% |
| AAPL   | 苹果     | 50股   | 220.00  | 246.63 | 12,332   | 🟩 +1,332  | 🟩 +12.10%|

自选行情
| 代码   | 名称    | 现价     | 涨跌幅      |
|--------|--------|---------|------------|
| 000300 | 沪深300 | 4509.24 | 🔴 +0.38% |
| .DJI   | 道琼斯  | 45216.14| 🟩 +0.11% |
```

#### 4b. 用户手动提供自选信息

用 `sq get` 查询后，**必须使用横向宽表格，禁止使用竖向键值对格式**：

```
| 代码   | 名称      | 数量   | 自选价格 | 最新价  | 市值       | 浮盈/亏        | 盈亏比         |
|--------|----------|--------|---------|--------|-----------|--------------|--------------|
| 600519 | 贵州茅台  | 100股  | 1680.0  | 1725.0 | 172,500   | 🔴 +4,500    | 🔴 +2.68%   |
| AAPL   | 苹果      | 50股   | 220.0   | 251.49 | 12,574.50 | 🟩 +1,574.50 | 🟩 +14.31%  |
```

汇总行：
```
📊 自选合计：市值 185,074.50 | 总参考成本 179,000 | 浮盈 +6,074.50（+3.39%）
```

浮盈亏 emoji 遵循市场规则（A股/港股：盈利🔴亏损🟢；美股：盈利🟩亏损🟥）。跨市场汇总时提示用户各币种分开统计。

CSV 解析规则：`#` 开头为注释，第一个非注释行为表头，名称列为空时从查询结果自动填充，自选价格为空时浮盈亏显示 `—`。

---

## Command 3: 历史行情查询

### 意图解析

从用户输入中提取以下参数（均可省略，使用默认值）：

**标的代码**：同 Step 1 规则。

**周期**（默认 day）：
| 用户表述 | 参数 |
|---------|------|
| 日/天/日K/daily | `--period day` |
| 周/周K/weekly | `--period week` |
| 月/月K/monthly | `--period month` |

**数量/区间**：
- "近N天/周/月"、"最近N条"、"过去N" → `--count N`
- "从 YYYY-MM-DD 到 YYYY-MM-DD"、"2024年1月到3月" → `--start ... --end ...`（转为 YYYY-MM-DD 格式）
- 未指定 → 默认 30 条

**复权**（默认前复权）：
| 用户表述 | 参数 |
|---------|------|
| 前复权（默认） | `--fq pre` |
| 后复权 | `--fq post` |
| 不复权/原始价格 | `--fq none` |

### 数据获取与格式化输出

```bash
bash scripts/sq.sh hist <code> [--period day|week|month] [--count N] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--fq pre|post|none] --format table
```

直接执行上述命令，将输出原样呈现给用户。`--format table` 已内置所有格式化逻辑：倒序 K 线表格、标题行（标的/周期/复权/条数）、区间统计、emoji 涨跌规则、成交量单位换算。

---

## 交易时间参考

| 市场 | 交易时段（当地时间） | 时区 |
|------|-------------------|------|
| A 股/ETF | 工作日 09:30-11:30, 13:00-15:00 | UTC+8 |
| 场外基金估值 | 工作日 09:30-15:00 | UTC+8 |
| 港股 | 工作日 09:30-12:00, 13:00-16:00 | UTC+8 |
| 美股 | 工作日 09:30-16:00（北京时间 夏令时 21:30-04:00） | UTC-4/-5 |
| QDII 基金 | 净值 T+2 至 T+7 公布 | — |
