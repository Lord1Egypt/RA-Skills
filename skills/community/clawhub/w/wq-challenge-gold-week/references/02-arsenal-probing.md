# 第②章 数据与算子:先摸清你的武器库

> 本文是《用 AI 辅助冲刺 WorldQuant BRAIN Challenge》的一章,完整章节地图见上层 SKILL.md。

**本章目录**

- 2.1 先认门:两个探测端点
- 2.2 拉字段:`/data-fields`
- 2.3 字段七大类别:你的"原料"
- 2.4 拉算子:`/operators`
- 2.5 tier-gating:低等级会被锁,先认锁再绕锁
- 2.6 落地:把武器库存成本地清单
- 2.7 复用提示词模板:让 AI 帮你探武器库

---

## ② 数据与算子:先摸清你的武器库

> 核心原则:**别猜,实测。** 你能用哪些字段、哪些算子、哪些地区,完全由你账号当前 tier 决定,而且随等级解锁在变。写因子前,先用 API 把"武器库"拉一遍,存成本地清单——这比背任何"网红因子列表"都值钱。

---

### 2.1 先认门:两个探测端点

摸清武器库只靠两个 GET 接口:

| 端点 | 作用 | 关键返回 |
|---|---|---|
| `GET /data-fields` | 拉某地区/universe 下所有可用**字段** | `id` / `description` / `category` / `coverage` / `type` |
| `GET /operators` | 拉你账号当前可用**算子** | `name` / `category` / `scope` / `definition` / `level` |

两者都是"当前账号视角"的结果:tier 锁掉的东西,要么根本不返回,要么在 simulation 时报错(见 2.5)。所以**这份清单是你自己的,不是别人的**。

#### 认证(不含真凭证)

```python
import os, requests

BASE = "https://api.worldquantbrain.com"

sess = requests.Session()
# HTTP Basic:账号密码从环境变量/密钥文件读,绝不硬编码进代码
sess.auth = (os.environ["BRAIN_EMAIL"], os.environ["BRAIN_PASSWORD"])
r = sess.post(f"{BASE}/authentication")
r.raise_for_status()          # 成功后 session cookie 已就位,后续请求复用 sess
```

> 安全提醒:凭证走环境变量或 `.env`(加进 `.gitignore`),**永远不要**写进代码或提交到仓库。

---

### 2.2 拉字段:`/data-fields`

字段接口按 `region / delay / universe / dataset` 过滤,并且**分页**(一次几十条,用 `offset` 翻页)。

```python
def fetch_fields(sess, region="USA", delay=1, universe="TOP3000",
                 dataset_id=None, limit=50):
    fields, offset = [], 0
    while True:
        params = {
            "instrumentType": "EQUITY",
            "region": region,
            "delay": delay,
            "universe": universe,
            "limit": limit,
            "offset": offset,
        }
        if dataset_id:
            params["dataset.id"] = dataset_id      # 按数据集过滤(可选)
        resp = sess.get(f"{BASE}/data-fields", params=params).json()
        batch = resp.get("results", [])
        fields += batch
        offset += limit
        if offset >= resp.get("count", 0):
            break
    return fields
```

单条字段返回大致长这样(字段名示意,以你实际返回为准):

```json
{
  "id": "close",
  "description": "Daily close price",
  "dataset": {"id": "pv1", "name": "Price Volume"},
  "category": "pv",
  "type": "MATRIX",
  "coverage": 0.99,        // 覆盖率:越高越好,低覆盖率因子容易 Sharpe 虚高
  "delay": 1,
  "region": "USA"
}
```

**看字段先看两件事**:`coverage`(覆盖率,太低的字段慎用,回测容易失真)和 `type`(`MATRIX` 是每股每日一个值的常规字段,`GROUP` 是分组字段如 industry,`VECTOR` 是每股多值的向量字段——向量字段常需向量算子,而那些算子往往被 tier 锁,见 2.5)。

---

### 2.3 字段七大类别:你的"原料"

`category` 把字段分成七大类。开局(USA + 低 tier)时,`pv`(几乎全解锁)和 `fundamental`/`analyst` 是主力矿脉。

| 类别 | 中文 | 讲的是什么 | 代表字段(示意) |
|---|---|---|---|
| `pv` | 量价 | 价格与成交量,几乎必解锁,做反转/动量 | `close` `open` `high` `low` `volume` `returns` |
| `fundamental` | 基本面 | 财报科目,做质量/估值比率的核心 | 净利润、股东权益、总资产、营收、现金流类科目 |
| `analyst` | 分析师一致预期 | 卖方对未来的估计,做预期修正 | `est_eps` `est_sales` `est_fcf`(一致预期 EPS/营收/自由现金流) |
| `news` | 新闻 | 新闻数量/情绪信号 | 新闻计数、新闻情绪分 |
| `option` | 期权 | 隐含波动率等,做正交的"另类通道" | `implied_volatility_*`(如看涨/看跌 IV) |
| `model` | 模型 | 平台预构建的复合/风险模型输出 | 各类风险因子暴露、模型打分 |
| `sentiment` | 情绪 | 社媒/文本情绪聚合 | 情绪强度、情绪极性 |

> 用法预告:基本面比率是最高产的"SIGNAL 原料"。经典构造是 `分子/分母杠杆`——如 `净利润/股东权益`(≈ROE)、`盈利/close`(盈利收益率)。分母换成 `equity/assets/sales/cap/enterprise_value` 就是一整族因子。第 ③ 章展开。

---

### 2.4 拉算子:`/operators`

```python
def fetch_operators(sess):
    ops = sess.get(f"{BASE}/operators").json()
    # 返回是列表;整理成 name -> 元信息
    return {o["name"]: o for o in ops}
```

单个算子返回示意:

```json
{
  "name": "ts_rank",
  "category": "Time Series",
  "scope": ["REGULAR"],        // 可用范围:REGULAR/COMBO/SELECTION 等
  "definition": "ts_rank(x, d)",
  "description": "过去 d 天里 x 当前值的时序分位",
  "level": "CONSULTANT"        // 或标注解锁所需 tier(锁住的算子可能压根不返回)
}
```

`scope` 告诉你算子能用在什么模式;`level` 提示解锁门槛。**以实际返回为准**——某算子不在你的返回列表里,或 `level` 高于你,就是暂时用不了。

#### 常用算子清单(开局够用)

| 算子 | 一句话含义 |
|---|---|
| `ts_rank(x, d)` | 过去 `d` 天里,当前 `x` 排第几分位(0~1),做时序相对强弱 |
| `ts_zscore(x, d)` | 过去 `d` 天的 z-score:`(x - 均值) / 标准差`,标准化偏离 |
| `ts_delta(x, d)` | `x - d 天前的 x`,做变化量/动量 |
| `ts_mean(x, d)` | 过去 `d` 天均值,平滑 |
| `ts_std_dev(x, d)` | 过去 `d` 天标准差,度量波动 |
| `ts_decay_linear(x, d)` | 过去 `d` 天线性加权衰减平均(越近权重越大),**降 turnover 利器** |
| `rank(x)` | 当天全 universe 横截面排序分位(0~1),几乎所有因子最外层都套它 |
| `group_rank(x, group)` | 在 `group`(如同行业)内部做横截面排序,剔除组间差异 |
| `group_neutralize(x, group)` | 在 `group` 内去均值,**中性化**,剔除行业/板块 beta,聚焦个股 alpha |
| `-x`(负号) | 取反,反转信号方向(反转类因子/翻正 Sharpe 常用) |

#### 分组层级(`group` 参数常用取值)

由细到粗:`subindustry`(子行业)→ `industry`(行业)→ `sector`(板块)→ `market`(全市场)。
经验:**中性化用 `industry`/`subindustry`** 最常见——粒度太粗(market)剔不干净行业 beta,粒度太细(subindustry)每组样本太少、结果不稳。两个都试,看哪个 Sharpe/Fitness 更稳。

> 高产模板(公开常识):`group_rank(ts_rank(SIGNAL, 窗口), industry)`。把基本面比率当 `SIGNAL`,时序分位捕捉趋势,再行业内横截面排序去 beta。

---

### 2.5 tier-gating:低等级会被锁,先认锁再绕锁

**现象**:平台按账号 tier 逐级解锁算子、地区、universe。低等级账号实测会撞到两类报错——

- 用了锁住的算子 → simulation 返回类似 **`inaccessible operator: <name>`**(常见于向量统计算子,如 `vec_stddev`、`vec_avg` 等 `VECTOR`-scope 算子)。
- 选了锁住的地区 → 类似 **`Region not available`**(低等级往往只开 **USA**;EUR/ASI/CHN 等需升级)。

**别把这当 bug**,这是设计:等级上去,`/operators` 和 `/data-fields` 返回的清单会自动变长,之前锁的就解锁了。

**开局策略(务实)**:
1. **地区**只用 `USA`,**universe** 从 `TOP3000` 起步(小 universe 质量分往往更高,后面章节细讲)。
2. **算子**只用 `/operators` 实测返回、且 `level` 不高于你的那些——上面清单 2.4 基本都属此列。
3. 撞到 `inaccessible operator` / `Region not available`,不要硬刚:**记进"待解锁清单"**,等级上去再回来用。可以在代码里维护一张本地表,自动跳过锁住的算子。

```python
# 把锁住的算子记下来,构造因子时自动过滤
LOCKED = set()

def is_usable(op_name, ops_meta, my_level_rank):
    o = ops_meta.get(op_name)
    if o is None:
        LOCKED.add(op_name); return False        # 清单里没有 = 用不了
    if o.get("_level_rank", 0) > my_level_rank:   # level 高于我 = 锁住
        LOCKED.add(op_name); return False
    return True
```

---

### 2.6 落地:把武器库存成本地清单

探测一次,存成 JSON,后面所有因子生成都读这份清单——**保证只用得着能用的**。

```python
import json

fields = fetch_fields(sess, region="USA", universe="TOP3000")
ops    = fetch_operators(sess)

arsenal = {
    "region": "USA",
    "universe": "TOP3000",
    "fields_by_category": {},     # category -> [field ids]
    "operators": list(ops.keys()),
}
for f in fields:
    arsenal["fields_by_category"].setdefault(f["category"], []).append(f["id"])

with open("arsenal_usa.json", "w") as fp:
    json.dump(arsenal, fp, ensure_ascii=False, indent=2)

# 快速体检
for cat, ids in arsenal["fields_by_category"].items():
    print(f"{cat:12s}: {len(ids)} 个字段")
print("可用算子:", len(arsenal["operators"]), "个")
```

> 升级纪律:每次 tier 变化后**重跑一次探测**,覆盖旧清单。别拿着旧的 `arsenal_usa.json` 一直用——新解锁的算子/地区不会自己跳进你的旧文件里。

---

### 2.7 复用提示词模板:让 AI 帮你探武器库

把下面这段丢给你的 AI 助手(Claude Code 之类),让它替你查、跑、整理成清单。**填空处按你情况改**:

```text
你是我的 WorldQuant BRAIN API 助手。目标:摸清我账号当前 tier 下的可用武器库,
输出一份本地 JSON 清单,供后续因子生成使用。凭证从环境变量 BRAIN_EMAIL/BRAIN_PASSWORD 读,
绝不打印或硬编码。

请写并运行 Python(requests)脚本,完成:
1. POST /authentication 建立 session(HTTP Basic)。
2. GET /data-fields 分页拉全:instrumentType=EQUITY, region=USA, delay=1, universe=TOP3000。
   按 category(pv/fundamental/analyst/news/option/model/sentiment)分组统计数量,
   每类列出 coverage 最高的 10 个 field id + 一句话 description。
3. GET /operators 拉全,按 category 分组,标出每个算子的 name / scope / level / definition。
4. 交叉核对:用一个最简单的 alpha(如 rank(close))发一次 /simulations 冒烟测试,
   确认认证与地区可用;若报 "Region not available" 或 "inaccessible operator",
   把报错原样记进 locked 列表,不要重试硬刚。
5. 汇总成 arsenal_usa.json:{region, universe, fields_by_category, operators, locked}。

约束:
- 只用 USA + 返回清单里实测可用的算子,锁住的一律跳过并记录。
- 尊重并发上限(低 tier 通常 K=2),simulation 轮询 status 到 COMPLETE 再取结果。
- 不要编造字段/算子;凡是清单里没有的,视为不可用。
最后给我:七大类别字段数量表 + 可用算子数量 + locked 列表。
```

这个模板的价值在于:**它逼 AI 用"实测返回"而不是"训练记忆"来回答你有什么武器**——记忆会过时、会幻觉,`/operators` 和 `/data-fields` 的实时返回不会。


---

