# API Reference — 题材库数据接口

本文档记录题材库 Skill 依赖的 API 接口完整规格，包含爱投顾题材库接口和个股行情补充数据源。

## 服务信息

- **服务名**: `teach-hotspot`
- **Base URL**: `https://group-api.itougu.com`
- **请求方式**: 所有爱投顾接口均为 **POST**
- **Content-Type**: `application/json`
- **响应标准**: `{ code: number, data: any, msg?: string }`，code=20000 表示成功

---

## 1. 题材库列表 — fullList

### 基本信息

| 项 | 值 |
|---|---|
| 端点 | `POST /teach-hotspot/subject/fullList` |
| 认证 | 无需认证 |
| Content-Type | `application/json` |
| 请求体 | `{}`（空对象即可） |

### 调用示例

```bash
curl -X POST 'https://group-api.itougu.com/teach-hotspot/subject/fullList' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### 响应结构

```typescript
interface FullListResponse {
  code: number       // 20000=成功
  data: {
    rows: SubjectItem[]
  }
  msg?: string
}

interface SubjectItem {
  subjectId: string       // 题材唯一标识，如 "90000797"
  name: string            // 题材名称，如 "锂电池"、"光伏"、"ST股"
  driven: string | null   // 驱动因素描述文本
    //   如 "科研团队研制出用于高能量密度与低温电池的氢氟烃电解液"
    //   可能为 null
  squareTag: number       // 方形标签
    //   0 = 无标签
    //   1 = "新" (新题材)
    //   2 = "热" (热门题材)
  rectangleTag: string | null  // 运营自定义标签（无固定范围）
    //   已知值: 龙头出现, 中军出现, 新挖掘题材, 主线,
    //          火热关注, 持续火热, 两天领涨, 今日最热
    //   运营可随时新增或调整，不做枚举限制
  updateTime: string | null    // 最后更新时间, ISO格式
    //   如 "2026-03-19T10:30:00"
    //   注意: 大量题材此字段为 null
  upLimitNum: number      // 涨停家数
    //   0 = 无涨停
    //   >0 = 该题材中有N只股票涨停
  orderNumber: number     // 排序序号（反映热度排名）
    //   值越小越热门，如 1=最热
}
```

### 字段说明

**排名标签 (squareTag)**:

- `squareTag === 1` → 显示"新"标签（新出现的题材）
- `squareTag === 2` → 显示"热"标签（持续热门题材）
- 其他 → 无特殊标签

**排序 (orderNumber)**:

- 该字段由运营/算法决定，反映题材的综合热度排名
- 值越小排名越靠前，如 orderNumber=1 为当前最热题材
- 可作为热度评估的主要参考指标

**驱动因素 (driven)**:

- 可能为 null
- 非空时描述该题材的核心驱动事件或逻辑

---

## 2. 题材详情 — subjectDetail4Free

### 基本信息

| 项 | 值 |
|---|---|
| 端点 | `POST /teach-hotspot/subject/subjectDetail4Free` |
| 认证 | 无需认证 |
| Content-Type | `application/json` |
| 请求体 | `{ "subjectId": "题材ID" }` |

### 调用示例

```bash
curl -X POST 'https://group-api.itougu.com/teach-hotspot/subject/subjectDetail4Free' \
  -H 'Content-Type: application/json' \
  -d '{"subjectId": "90000797"}'
```

### 响应结构

```typescript
interface SubjectDetailResponse {
  code: number       // 20000=成功, 50000=数据不存在
  data: SubjectDetail
  msg?: string
}

interface SubjectDetail {
  // === 导航信息 ===
  navi: NaviNode               // 题材导航树（面包屑）

  // === 核心数据 ===
  tableJson: TableJsonNode     // 树状表格数据（最重要）
  driven: string               // 驱动因素文本

  // === 标志位 ===
  reasonShowFlag: number       // 0=不显示推荐理由, 1=显示
  middleTroopsFlag: number     // 0=无, 1=有"题材中军"分类
  dragonHeadFlag: number       // 0=无, 1=有"题材龙头"分类
  
  // === 以下字段存在于响应中但不应使用 ===
  // serviceEndTime, shareClaim, authorizationOrderId,
  // opStatus, currRoleType, orderInterval
}

// === 导航树 ===
interface NaviNode {
  subjectId: string
  subjectName: string
  children: NaviNode[] | null  // 子题材导航，可能为 null
}

// === 树状表格（核心数据结构）===
interface TableJsonNode {
  subjectId: string | null     // 分类节点有值，个股节点为 null
  nodeType: 1 | 2 | 3
  // nodeType = 1: 分类节点
  //   → 题材本身或子分类，可嵌套
  //   → 有 subjectId, name, children
  // nodeType = 2: 个股节点
  //   → 叶子节点，含 stockCode
  //   → 有 stockCode, name, highlight, recommendReason
  // nodeType = 3: 介绍节点（推荐理由文本）
  //   → 有 content

  name: string                 // 节点名称

  // 个股节点(nodeType=2)相关
  stockCode: string | null     // 股票代码, 格式 "600519.sh" 或 "002230.sz"
    // 含 "***" 表示该数据暂不可用
  highlight: number | null     // 0=普通, 1=核心标的（高亮）
  recommendReason: string | null  // 推荐理由

  // 介绍节点(nodeType=3)相关
  content?: string             // 介绍文本

  // 通用
  children: TableJsonNode[] | null  // 子节点
}
```

### stockCode 格式

题材库 API 返回的 stockCode 格式为 `代码.小写市场后缀`：

```
600519.sh  →  贵州茅台 (上海)
002230.sz  →  科大讯飞 (深圳)
300750.sz  →  宁德时代 (深圳创业板)
688256.sh  →  寒武纪 (上海科创板)
```

**市场字典 (CEMarket)**:

```typescript
const CEMarket: Record<string, number> = {
  sz: 0,  // 深圳
  sh: 1,  // 上海
  hk: 2,  // 香港
  sf: 3,  sc: 4,  dc: 5,  zc: 6,
  bj: 7,  // 北京
}
```

### 树状结构示例

**扁平结构**（当前生产数据主流）:

```
ST股 (nodeType=1, 根节点, subjectId="90000797")
├── [nodeType=2] *ST中润 (000506.sz) highlight=0
│   推荐理由: "公司回复交易所问询函；控股公司斐济瓦图科拉金矿..."
├── [nodeType=2] *ST景峰 (000908.sz) highlight=1 ⭐
│   推荐理由: "法院决定对公司启动预重整"
├── [nodeType=2] ST春天 (600381.sh) highlight=1 ⭐
│   推荐理由: "冬虫夏草产业化龙头企业，回复交易所问询函"
├── [nodeType=2] *ST博信 (600083.sh) highlight=0
│   推荐理由: "苏州国资委旗下..."
└── ... (共37只个股)
```

**嵌套分类结构**（较少见但需支持）:

```
题材 (nodeType=1, 根节点)
├── 个股A (nodeType=2)
├── 分类A (nodeType=1)
│   ├── 个股B (nodeType=2)
│   └── 个股C (nodeType=2)
└── 分类B (nodeType=1)
    ├── 分类C (nodeType=1)
    │   ├── 个股D (nodeType=2)
    │   └── 个股E (nodeType=2)
    └── 分类D (nodeType=1)
        └── 个股F (nodeType=2)
```

> 注: nodeType=1 代表分类节点（可嵌套），nodeType=2 代表个股节点（叶子）。

### 个股分类说明

题材详情中的个股通过标志位区分角色（仅在标志位=1时有效）：

| 分类 | 标志位 | 说明 |
|------|--------|------|
| 题材个股 | 默认存在 | 该题材的所有关联个股 |
| 题材中军 | `middleTroopsFlag=1` | 题材中的中坚力量个股（仅当标志位=1时输出） |
| 题材龙头 | `dragonHeadFlag=1` | 题材中的领军龙头个股（仅当标志位=1时输出） |

---

## 3. 补充数据源 — 个股行情

题材库 API 返回的是题材结构和关联个股列表，但**不包含个股实时行情数据**（最新价、涨幅等）。需通过以下数据源补充。

### ⚠️ 行情获取决策路径（必读）

```
始终使用 Python 获取行情（不要用 curl/bash 循环）
    ↓
首选: 腾讯行情 API (qt.gtimg.cn) — 最稳定，支持批量，无频率限制
    ↓ 返回空数据（非交易时间或接口异常）
Fallback: 东方财富个股快照 API (push2.eastmoney.com) — 有频率限制
    ↓ 也失败
Fallback: AKShare Python 库 — 需要 pip install
    ↓ 全部失败
标注"行情数据暂无"，基于题材数据继续分析
```

**关键注意事项**:
- **非交易时间**（休市、节假日）：腾讯 API 可能返回空数据，这是正常行为
- **频率限制**：东方财富 push2 接口高频调用（>5次/秒）会返回空数据
- **编码问题**：腾讯 API 返回 GBK 编码，必须用 Python 处理（不要用 curl 管道）
- **始终用 Python**：涉及 GBK 解码、批量处理、JSON 解析，bash/curl 容易出错

### 3.1 数据源字段映射速查

> 完整的获取逻辑见 3.2 节统一脚本。以下仅为字段映射参考。

**腾讯行情 API**（首选，`http://qt.gtimg.cn/q={市场}{代码}`，GBK 编码，`~` 分隔）:

| 索引 | 字段 | 索引 | 字段 |
|:---:|------|:---:|------|
| 1 | 股票名称 | 31 | 涨跌额 |
| 2 | 股票代码 | 32 | 涨跌幅(%) |
| 3 | 最新价 | 33 | 最高价 |
| 4 | 昨收价 | 34 | 最低价 |
| 5 | 开盘价 | 37 | 成交额(万) |
| 6 | 成交量(手) | 38 | 换手率(%) |
| 44 | 流通市值(亿) | 45 | 总市值(亿) |

**东方财富 API**（Fallback，`push2.eastmoney.com`，JSON 格式）:

| 字段 | 含义 | 字段 | 含义 |
|------|------|------|------|
| f2 | 最新价 | f14 | 名称 |
| f3 | 涨跌幅(%) | f12 | 代码 |
| f6 | 成交额 | f8 | 换手率(%) |
| f20 | 总市值 | f21 | 流通市值 |

> ⚠️ 东方财富 push2 接口高频调用（>5次/秒）可能返回空数据。

**AKShare**（最终 Fallback，`pip install akshare`）:
- `ak.stock_zh_a_spot_em()` — A 股实时行情（全部），字段：代码, 名称, 最新价, 涨跌幅, 换手率, 成交额, 流通市值 等
- `ak.stock_board_concept_cons_em(symbol="概念名")` — 概念板块成分股
- `ak.stock_zh_a_hist(symbol="300750", period="daily", adjust="qfq")` — 个股历史K线
- ⚠️ 底层调用东方财富，高频请求触发 IP 限制，建议间隔 ≥ 200ms

### 3.2 完整行情获取脚本（推荐直接使用）

以下 Python 脚本覆盖**批量获取 + 自动 fallback + 格式转换**全流程，可直接复制运行：

```python
import urllib.request
import json
import time

# ========== stockCode 格式转换 ==========
CE_MARKET = {'sz': 0, 'sh': 1, 'hk': 2, 'sf': 3, 'sc': 4, 'dc': 5, 'zc': 6, 'bj': 7}

def convert_stock_code(stock_code):
    """题材库 stockCode 转各平台格式
    输入: '600519.sh' → 输出: {'tencent': 'sh600519', 'eastmoney': '1.600519', 'akshare': '600519'}
    """
    code, market = stock_code.split('.')
    return {
        'tencent': f'{market}{code}',
        'eastmoney': f'{CE_MARKET.get(market, 0)}.{code}',
        'akshare': code,
        'display': code,
    }

# ========== 腾讯 API（首选） ==========
def fetch_quotes_tencent(stock_codes, batch_size=30):
    """批量获取行情（腾讯 API）
    stock_codes: 题材库格式列表，如 ['600519.sh', '002230.sz']
    返回: {stock_code: {name, code, price, change, turnover, amount, cap, total_cap, ...}}
    """
    results = {}
    tencent_codes = []
    code_map = {}  # tencent_code -> original_code

    for sc in stock_codes:
        if '***' in sc:
            continue
        converted = convert_stock_code(sc)
        tencent_codes.append(converted['tencent'])
        code_map[converted['tencent']] = sc

    # 分批请求（每批 ≤ batch_size）
    for i in range(0, len(tencent_codes), batch_size):
        batch = tencent_codes[i:i+batch_size]
        url = f'http://qt.gtimg.cn/q={",".join(batch)}'
        try:
            resp = urllib.request.urlopen(url, timeout=10).read().decode('gbk')
            for line in resp.strip().split('\n'):
                if '=' not in line or '"' not in line:
                    continue
                parts = line.split('"')
                if len(parts) < 2:
                    continue
                data = parts[1].split('~')
                if len(data) < 46 or not data[3]:
                    continue  # 空数据（非交易时间）
                # 找回原始 stock_code
                tc = line.split('=')[0].split('_')[-1].strip()
                orig = code_map.get(tc, tc)
                try:
                    results[orig] = {
                        'name': data[1],
                        'code': data[2],
                        'price': float(data[3]) if data[3] else 0,
                        'change_pct': float(data[32]) if data[32] else 0,
                        'change_amt': float(data[31]) if data[31] else 0,
                        'turnover': float(data[38]) if data[38] else 0,
                        'amount_wan': float(data[37]) if data[37] else 0,  # 万元
                        'high': float(data[33]) if data[33] else 0,
                        'low': float(data[34]) if data[34] else 0,
                        'open': float(data[5]) if data[5] else 0,
                        'prev_close': float(data[4]) if data[4] else 0,
                        'cap': float(data[44]) if data[44] else 0,  # 流通市值(亿)
                        'total_cap': float(data[45]) if data[45] else 0,  # 总市值(亿)
                        'pe': data[39],
                        'source': '腾讯行情',
                    }
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            print(f'腾讯API批次{i//batch_size+1}失败: {e}')
            continue
        if i + batch_size < len(tencent_codes):
            time.sleep(0.1)  # 批次间隔

    return results

# ========== 东方财富 API（Fallback） ==========
def fetch_quotes_eastmoney(stock_codes):
    """批量获取行情（东方财富 API）— 腾讯失败时使用
    stock_codes: 题材库格式列表
    """
    results = {}
    secids = []
    code_map = {}

    for sc in stock_codes:
        if '***' in sc:
            continue
        converted = convert_stock_code(sc)
        secids.append(converted['eastmoney'])
        code_map[converted['eastmoney']] = sc

    url = (f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2'
           f'&fields=f2,f3,f4,f5,f6,f7,f8,f9,f12,f14,f15,f16,f17,f18,f20,f21'
           f'&secids={",".join(secids)}')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        data = json.loads(resp)
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                code = item.get('f12', '')
                name = item.get('f14', '')
                # 找回原始 stock_code
                for secid, orig in code_map.items():
                    if secid.endswith(f'.{code}'):
                        try:
                            results[orig] = {
                                'name': name,
                                'code': code,
                                'price': float(item.get('f2', 0)) if item.get('f2') != '-' else 0,
                                'change_pct': float(item.get('f3', 0)) if item.get('f3') != '-' else 0,
                                'change_amt': float(item.get('f4', 0)) if item.get('f4') != '-' else 0,
                                'turnover': float(item.get('f8', 0)) if item.get('f8') != '-' else 0,
                                'amount_wan': float(item.get('f6', 0)) / 10000 if item.get('f6') not in ['-', None] else 0,
                                'cap': float(item.get('f21', 0)) / 100000000 if item.get('f21') not in ['-', None] else 0,
                                'total_cap': float(item.get('f20', 0)) / 100000000 if item.get('f20') not in ['-', None] else 0,
                                'source': '东方财富',
                            }
                        except (ValueError, TypeError):
                            continue
                        break
    except Exception as e:
        print(f'东方财富API失败: {e}')

    return results

# ========== 统一入口（自动 Fallback） ==========
def fetch_quotes(stock_codes):
    """获取个股行情 — 自动 fallback
    stock_codes: 题材库格式列表，如 ['600519.sh', '002230.sz']
    返回: {stock_code: {name, code, price, change_pct, turnover, amount_wan, cap, source, ...}}
    """
    if not stock_codes:
        return {}

    # 1. 首选腾讯
    results = fetch_quotes_tencent(stock_codes)
    if results:
        return results

    print('腾讯API无数据（可能非交易时间），尝试东方财富...')

    # 2. Fallback 东方财富
    results = fetch_quotes_eastmoney(stock_codes)
    if results:
        return results

    print('东方财富也无数据，尝试 AKShare...')

    # 3. 最终 Fallback: AKShare
    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        target_codes = [convert_stock_code(sc)['akshare'] for sc in stock_codes if '***' not in sc]
        filtered = df[df['代码'].isin(target_codes)]
        for _, row in filtered.iterrows():
            for sc in stock_codes:
                if sc.split('.')[0] == row['代码']:
                    results[sc] = {
                        'name': row['名称'],
                        'code': row['代码'],
                        'price': float(row['最新价']) if row['最新价'] else 0,
                        'change_pct': float(row['涨跌幅']) if row['涨跌幅'] else 0,
                        'turnover': float(row['换手率']) if row['换手率'] else 0,
                        'amount_wan': float(row['成交额']) / 10000 if row['成交额'] else 0,
                        'cap': float(row['流通市值']) / 100000000 if row['流通市值'] else 0,
                        'source': 'AKShare',
                    }
                    break
    except ImportError:
        print('AKShare 未安装 (pip install akshare)')
    except Exception as e:
        print(f'AKShare失败: {e}')

    return results

# ========== 使用示例 ==========
if __name__ == '__main__':
    # 从题材详情提取的 stockCode 列表
    codes = ['600519.sh', '002230.sz', '300750.sz', '688256.sh']
    quotes = fetch_quotes(codes)
    for sc, q in quotes.items():
        print(f'{q["name"]}({q["code"]}): {q["price"]}元 {q["change_pct"]:+.2f}% '
              f'换手{q["turnover"]:.2f}% 成交{q["amount_wan"]:.0f}万 [{q["source"]}]')
```

> **使用方式**: 直接将上述脚本复制到 Python 环境执行，或拆取 `fetch_quotes()` 函数在分析流程中调用。
> 传入题材库格式的 stockCode 列表，自动处理格式转换、批量请求、fallback 和异常。

### 3.3 stockCode 格式转换（快速参考）

> 完整转换逻辑已包含在 3.2 节脚本的 `convert_stock_code()` 函数中。以下为快速参考表：

| 题材库格式 | 腾讯格式 | 东方财富 secid | AKShare 格式 |
|-----------|----------|---------------|-------------|
| `600519.sh` | `sh600519` | `1.600519` | `600519` |
| `002230.sz` | `sz002230` | `0.002230` | `002230` |
| `300750.sz` | `sz300750` | `0.300750` | `300750` |
| `688256.sh` | `sh688256` | `1.688256` | `688256` |
| `301118.sz` | `sz301118` | `0.301118` | `301118` |

---

## 4. 错误码

| code | 含义 |
|------|------|
| 20000 | 成功 |
| 50000 | 数据不存在 |
| 其他 | 业务错误 |

> 注: 以上错误码仅适用于爱投顾接口。东方财富、腾讯、AKShare 等第三方数据源的错误码以各自文档为准。

### 特殊数据说明

| 数据特征 | 含义 |
|---------|------|
| `stockCode` 含 `***` | 该个股数据暂不可用 |
| `updateTime` 为 null | 该题材暂无更新时间记录，以 orderNumber 判断热度 |
| `driven` 为 null | 该题材暂无驱动因素描述 |
| `navi.children` 为 null | 该题材无子题材导航 |
| `highlight` 为 null 或 0 | 非核心标的；highlight=1 为核心标的 |
