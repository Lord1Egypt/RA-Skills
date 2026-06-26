---
name: ths-financial-data
description: 该skill用于获取股票市场数据，包括实时行情、中文名称查询、键盘缩写转换、资金流向和日K线数据。使用thsdk库提供同花顺数据接口支持。支持自动将中文、缩写、短代码转换为thsdk所需的完整ths_code格式。当匹配到多只股票时，会返回候选列表供用户选择。如未安装thsdk，会自动安装。
---

# Stock Data Skill

## 概述

此skill提供基于thsdk库的股票市场数据获取功能，支持A股、港股、美股等多市场数据查询。该skill应于用户需要获取金融市场数据、进行股票分析或构建金融应用时使用。

## 自动安装依赖

**此skill会自动处理 thsdk 库的安装**，无需用户手动操作：

```
首次使用时：
        │
        ▼
检查 thsdk 是否安装？
        │
   ┌────┴────┐
  YES        NO
   │          │
   ▼          ▼
检查版本    自动执行
>= 1.7.14?   pip install --upgrade thsdk
   │
   ┌────┴────┐
  YES        NO
   │          │
   ▼          ▼
正常使用    自动升级
```

如果检测到 thsdk 未安装或版本低于 1.7.14，会自动执行：
```bash
pip install --upgrade thsdk
```

## 代码自动解析工作流（核心规则）

**在任何需要股票代码的操作之前，必须先执行以下判断流程：**

```
用户输入的 stock_code
        │
        ▼
是否满足"直通"条件？
  USHA + 6位数字  （如 USHA600519，上交所A股）
  USZA + 6位数字  （如 USZA000001，深交所A股）
        │
   ┌────┴────┐
  YES        NO（短代码/中文/缩写/其他前缀/其他任何格式）
   │          │
   ▼          ▼
直接使用   调用 search_symbols(input) 查询候选列表
              │
              ▼
         获取完整的 ths_code
              │
        ┌─────┴─────┐
      0条           1条          多条
        │             │             │
        ▼             ▼             ▼
    返回错误      自动匹配      筛选A股
  "未找到"        ths_code          │
                               ┌────┴────┐
                           0只A股      1只A股      多只A股
                               │           │           │
                               ▼           ▼           ▼
                           展示全部    自动选择    返回候选列表
                           让用户选择             等待用户选择
```

## 多股票选择交互流程（重要）

当 `search_symbols` 匹配到**多只A股**时，函数会返回一个特殊结构：

```python
{
    'need_selection': True,
    'candidates': [
        {'ths_code': 'USHA600520', 'name': '三佳科技', 'code': '600520', 'market': '沪A'},
        {'ths_code': 'USZA002796', 'name': '世嘉科技', 'code': '002796', 'market': '深A'},
        # ... 更多候选
    ],
    'display': '\n**找到 5 只A股**：\n\n  1. **三佳科技** `USHA600520` (沪A)\n  2. **世嘉科技** `USZA002796` (深A)\n  ...\n\n请输入序号选择（1-5），或输入 0 取消。'
}
```

**AI 助手应该：**
1. 检测返回值是否为 `dict` 且包含 `need_selection: True`
2. 将 `display` 内容展示给用户
3. 等待用户输入序号
4. 使用 `get_candidate_by_index(candidates, index)` 获取用户选择的股票
5. 使用获取到的 `ths_code` 继续后续操作

### 示例交互流程

```python
from thsdk import THS
from stock_utils import search_stock_candidates, get_candidate_by_index, get_kline_data

with THS() as ths:
    # 第一步：搜索股票
    result = search_stock_candidates(ths, "sjkj")
    
    if result['status'] == 'found':
        # 唯一匹配，直接使用
        ths_code = result['ths_code']
        df = ths.klines(ths_code, interval="day", count=30)
        
    elif result['status'] == 'need_selection':
        # 多个候选，需要用户选择
        print(result['display'])  # 展示给用户
        
        # AI 应该在这里等待用户输入序号
        # 假设用户选择了 2
        user_choice = 2
        selected = get_candidate_by_index(result['candidates'], user_choice)
        
        if selected:
            ths_code = selected['ths_code']
            df = ths.klines(ths_code, interval="day", count=30)
    
    elif result['status'] == 'not_found':
        print(result['display'])  # 未找到提示
```

---

## 快速开始

### AI 助手使用此 Skill 时

1. **自动安装检查**：首次调用时会自动检查并安装 thsdk
2. **获取 THS 实例**：可使用 `get_ths_instance()` 或直接 `from thsdk import THS`
3. **调用查询函数**：使用 `search_stock_candidates` 等函数获取数据

```python
# 方式1：使用便捷函数（推荐）
from stock_utils import get_ths_instance, get_kline_data

ths = get_ths_instance()
if ths:
    df = get_kline_data(ths, "平安银行", interval="day", count=30)

# 方式2：标准方式
from thsdk import THS
from stock_utils import search_stock_candidates, get_kline_data

with THS() as ths:
    result = search_stock_candidates(ths, "平安银行")
    if result['status'] == 'found':
        df = ths.klines(result['ths_code'], interval="day", count=30)
```

### 股票代码格式说明

thsdk 要求使用**完整 ths_code**，格式为市场前缀 + 代码：

| 市场      | 前缀   | 示例           |
|-----------|--------|----------------|
| 深交所A股 | `USZA` | `USZA000001`   |
| 上交所A股 | `USHA` | `USHA600519`   |
| 港股      | `HKHK` | `HKHK00700`    |
| 美股      | `USUS` | `USUSAAPL`     |

> **不需要手动记忆前缀**，使用 `search_stock_candidates()` 自动处理一切格式。

## 核心函数

### 1. ensure_thsdk() - 自动安装检查

```python
from stock_utils import ensure_thsdk, get_ths_instance

# 确保 thsdk 已安装
if ensure_thsdk():
    print("thsdk 已就绪")

# 或直接获取实例（内部会自动检查安装）
ths = get_ths_instance()
```

### 2. search_stock_candidates（推荐）

搜索股票并返回结构化结果，支持优雅的用户选择流程：

```python
from thsdk import THS
from stock_utils import search_stock_candidates

with THS() as ths:
    result = search_stock_candidates(ths, "ndsd")
    
    # result['status'] 可能的值：
    # - 'found': 唯一匹配，result['ths_code'] 可直接使用
    # - 'need_selection': 多个候选，需要用户选择
    # - 'not_found': 未找到匹配
    
    # result['ths_code']: 唯一匹配时的 ths_code
    # result['candidates']: 候选列表
    # result['display']: 格式化的展示文本（直接展示给用户）
```

### 3. get_candidate_by_index

根据序号获取用户选择的股票：

```python
from stock_utils import get_candidate_by_index

# candidates 是 search_stock_candidates 返回的候选列表
# index 是用户输入的序号（1-based）
selected = get_candidate_by_index(candidates, 2)

if selected:
    print(f"用户选择: {selected['name']} ({selected['ths_code']})")
```

### 4. get_kline_data

获取K线数据，支持自动解析股票代码：

```python
from thsdk import THS
from stock_utils import get_kline_data

with THS() as ths:
    result = get_kline_data(ths, "平安银行", interval="day", count=30)
    
    # 检查是否需要用户选择
    if isinstance(result, dict) and result.get('need_selection'):
        print(result['display'])  # 展示候选列表给用户
        # 等待用户选择...
    elif isinstance(result, pd.DataFrame):
        print(result)  # 成功获取数据
    else:
        print("获取失败")
```

### 5. get_realtime_data

获取实时行情：

```python
from thsdk import THS
from stock_utils import get_realtime_data

with THS() as ths:
    result = get_realtime_data(ths, "000001")
    
    if isinstance(result, dict):
        if result.get('need_selection'):
            print(result['display'])  # 需要选择
        else:
            print(f"股票：{result['name']}")
            print(f"最新价：{result['price']}")
            print(f"涨跌幅：{result['change_pct']}%")
```

### 6. get_fund_flow

获取资金流向：

```python
from thsdk import THS
from stock_utils import get_fund_flow

with THS() as ths:
    result = get_fund_flow(ths, "贵州茅台")
    
    if isinstance(result, dict) and not result.get('need_selection'):
        print(f"主力净流入：{result['main_net_inflow']}")
        print(f"散户净流入：{result['retail_net_inflow']}")
```

### 7. wencai_query

使用问财自然语言查询：

```python
from thsdk import THS
from stock_utils import wencai_query

with THS() as ths:
    df = wencai_query(ths, "最近热度前50的行业和涨停原因归类")
    if df is not None:
        print(df.head())
```

## 完整使用示例

### 场景：用户输入模糊查询

```python
from thsdk import THS
from stock_utils import search_stock_candidates, get_candidate_by_index, get_kline_data

with THS() as ths:
    # 用户输入：sjkj
    result = search_stock_candidates(ths, "sjkj")
    
    if result['status'] == 'need_selection':
        # 展示候选给用户
        print(result['display'])
        # 输出示例：
        # **找到 5 只A股**：
        # 
        #   1. **三佳科技** `USHA600520` (沪A)
        #   2. **盛剑科技** `USHA603324` (沪A)
        #   3. **世嘉科技** `USZA002796` (深A)
        #   4. **仕净科技** `USZA301030` (深A)
        #   5. **熵基科技** `USZA301330` (深A)
        # 
        # 请输入序号选择（1-5），或输入 0 取消。
        
        # 等待用户选择序号
        # user_choice = int(input("请选择: "))  # 假设用户输入 3
        
        selected = get_candidate_by_index(result['candidates'], user_choice)
        if selected:
            ths_code = selected['ths_code']
            df = ths.klines(ths_code, interval="day", count=30)
            print(f"已获取 {selected['name']} 的日K线数据")
```

### 场景：唯一匹配（自动处理）

```python
from thsdk import THS
from stock_utils import search_stock_candidates, get_kline_data

with THS() as ths:
    result = search_stock_candidates(ths, "ndsd")
    
    if result['status'] == 'found':
        # 自动匹配，无需用户选择
        print(result['display'])  # ✅ 已自动匹配：**宁德时代** `USZA300750` (深A)
        
        df = ths.klines(result['ths_code'], interval="day", count=30)
        print(df.head())
```

## 返回值说明

### search_stock_candidates 返回结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | str | `found` / `need_selection` / `not_found` |
| `ths_code` | str | 唯一匹配时的股票代码 |
| `candidates` | list | 候选股票列表 |
| `message` | str | 简短提示信息 |
| `display` | str | 格式化的展示文本（Markdown格式） |

### get_candidate_by_index 返回结构

```python
{
    'ths_code': 'USZA002796',
    'name': '世嘉科技',
    'code': '002796',
    'market': '深A'
}
```

## 输出格式

所有数据以表格形式输出，使用 Markdown 表格格式：

### 实时行情表格示例

| 代码 | 名称 | 最新价 | 涨跌幅 | 涨跌额 | 成交量 | 成交额 |
|------|------|--------|--------|--------|--------|--------|
| USZA000001 | 平安银行 | 15.20 | +1.23% | +0.18 | 12.5万 | 1.89亿 |

### 日K数据表格示例

| 日期 | 开盘 | 收盘 | 最高 | 最低 | 成交量 | 成交额 | 涨跌幅 |
|------|------|------|------|------|--------|--------|--------|
| 2026-03-13 | 27.34 | 27.02 | 27.80 | 26.90 | 372.9万 | 1.02亿 | -1.75% |

## 注意事项

1. **自动安装**：首次使用时会自动检查并安装 thsdk，无需手动操作
2. **数据延迟**：数据来源于同花顺，实时数据可能存在短暂延迟
3. **请求频率**：避免短时间内大量请求，每次查询间隔建议 > 100ms
4. **股票代码格式**：只有 `USHA/USZA + 6位数字` 可以直通，其他格式都会先查询
5. **用户选择**：多只A股时必须等待用户选择，不能自动选择第一只
6. **港股/美股**：港股和美股代码会通过 `search_symbols` 查询确认

## 工具函数

### 安装检查函数

```python
from stock_utils import check_thsdk_installed, get_thsdk_version, ensure_thsdk

# 检查是否已安装
is_installed = check_thsdk_installed()  # True/False

# 获取当前版本
version = get_thsdk_version()  # "1.7.14" 或 "not installed"

# 确保已安装（未安装则自动安装）
ensure_thsdk()  # 返回 True/False
```

## 资源文件

- `scripts/stock_utils.py` — 核心工具函数，包含自动安装、search_stock_candidates 自动解析及所有数据获取封装
- `references/api_reference.md` — thsdk 原始 API 完整参考文档
- `assets/stock_template.py` — 含可视化的股票分析完整模板
