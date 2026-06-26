---
name: zhuocha
description: 招投标重复项目核实助手。当需要分析同一 reid 下的多条 jy_id 是否为真正重复时激活。数据源：dify_ns_re_readsource（reid分组） + dwd_bid_it_all（明细字段，5200端口） + ods_bid_content（原始正文，5100端口）。典型触发语：「找茬大师」「分析这组重复」「判断是否是重复项目」「去重分析」。
---

# 找茬大师（zhuocha）

招投标重复项目核实：根据 reid 聚类的多条 jy_id，核实是否真的重复，排除同一项目的二次公告/多批次发布/不同标段等情况。

## 数据库查询

**数据表分工**：
- `dify_ns_re_readsource`（6100端口）：只存 reid 分组和 jy_id，**不包含明细字段**
- `dwd_bid_it_all`（**5200端口**）：真正的明细数据表，包含字段
- `ods_bid_content`（5100端口）：原始正文 detail + att_ext
- `result.dify_ns_re_result`（6100端口）：结果写入表

| 用途 | URL | 说明 |
|------|-----|------|
| 查 reid 分组和 jy_id | 6100端口 | `SELECT reid, jy_id FROM public.dify_ns_re_readsource WHERE reid = 'xxx'` |
| 查明细字段（**必须用这个**） | **5200端口** | `SELECT customer_standard_new, title, proj_name, type, area, city FROM zy_dwd_bid.public.dwd_bid_it_all WHERE jy_id = 'xxx'` |
| 查原始正文 | 5100端口 | `SELECT left(detail, N), att_ext FROM public.ods_bid_content WHERE jy_id = 'xxx'` |
| 写入结果 | 6100端口 | POST JSON 格式（见下方） |

**⚠️ 重要：明细字段必须查 dwd_bid_it_all（5200端口），不要查 dify_ns_re_readsource（6100端口），后者只有 reid 和 jy_id 无实际业务字段。**

## 核心判断流程

**核心原则：proj_name 只起辅助参考作用，最终判断必须以 detail 正文中项目编号 + 客户名 + 采购内容为准。**

**⚠️ SQL 写法注意：detail 字段查询时，不要在 SQL 中使用 LEFT() 等函数截取，直接 `SELECT detail` 取完整字段，然后在 Python 中用字符串截取 `[:150]` 代替。这样比 SQL 函数截取更可靠，避免某些端口/驱动兼容性问题。**

```
同一 reid 下的多条 jy_id
    ↓
Step 1: 查 dify_ns_re_readsource，获取该 reid 下所有 jy_id
    SQL: SELECT reid, jy_id FROM public.dify_ns_re_readsource WHERE reid = 'xxx'
    ↓
Step 2: 查 dwd_bid_it_all 明细字段（5200端口），确认字段对比
    SQL: SELECT customer_standard_new, title, proj_name, type, area, city
         FROM zy_dwd_bid.public.dwd_bid_it_all WHERE jy_id = 'jy_id'
    ↓
    ┌─ proj_name 有效 + 只有一个 → 进入 Step 3
    ├─ proj_name 有效 + 多个不同 proj_name → 进入 Step 3（需 detail 确认）
    └─ proj_name 为"无效"或空
         ├─ detail 中项目编号/客户名完全不同 → ❌ 非重复（错误归组）
         └─ detail 中项目编号/客户名相同 → 进入 Step 3
    ↓
Step 3: 查 ods_bid_content.detail + att_ext（5100端口）
    SQL: SELECT detail, att_ext FROM public.ods_bid_content WHERE jy_id = 'xxx'
    · att_ext 附件标题对比（有无"二次"等差异）
    · detail 正文关键字段：项目编号、金额、供应商、时间
    ↓
项目编号相同 + 正文实质相同 → ✅ 重复
项目编号不同 / 金额不同 / 时间明显不同 → ❌ 非重复（不同标段/不同批次）
```

## 写入结果表（重要）

**⚠️ 必须用 Python `urllib` 写入，禁止用 bash curl 循环**：

bash 循环写入时，中文逗号（,）会导致 `cut -d','` 切割字段错位，使 `re_result` 字段变成 NULL。必须始终用 Python：

```python
import urllib.request, json
url = "http://192.168.88.51:6100/insert"
headers = {"Content-Type": "application/json"}
payload = json.dumps({
    "sql": "INSERT INTO result.dify_ns_re_result (reid, reason, rr, rd, re_result) VALUES (:reid, :reason, :rr, :rd, :re_result)",
    "params": {"reid": "...", "reason": "...", "rr": "...", "rd": "...", "re_result": "是"}
})
req = urllib.request.Request(url, data=payload.encode(), headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    print(json.loads(resp.read()))
```

**⚠️ API 不支持 DELETE/UPDATE**：如果同一条 reid 重复写入（re_result 为 NULL 的错误数据），只能通过 `TRUNCATE TABLE result.dify_ns_re_result;` 清空全表后重新写入全部记录。

**断点续跑保护**：每次重新写入前，先查询 `result.dify_ns_re_result` 中已有 reid，从原始数据中排除，确保已分析过的数据不会丢失。

**表**：`result.dify_ns_re_result`（schema: `result`）

**接口**：`POST http://192.168.88.51:6100/insert`

```json
{
  "sql": "INSERT INTO result.dify_ns_re_result (reid, reason, rr, rd, re_result) VALUES (:reid, :reason, :rr, :rd, :re_result)",
  "params": {
    "reid": "xxxxxx",
    "reason": "判断理由",
    "rr": "保留的jy_id",
    "rd": "删除的jy_id（多值用英文逗号分隔）",
    "re_result": "是"
  }
}
```

**字段说明**

| 字段 | 含义 |
|------|------|
| `re_result = "是"` | 重复：rr 保留，rd 内所有 jy_id 删除 |
| `re_result = "否"` | 非重复：该 reid 下所有 jy_id 均保留，rr/rd 任意填两条即可 |

**⚠️ RD 字段必须完整**：多 jy_id 组（如 40 条）的 re_result="是"时，rd 要填入**所有待删除的 jy_id**（除 rr 外），用英文逗号分隔。

**⚠️ 必须用 Python 写入**：bash 循环写入时，中文逗号会导致字段错位使 re_result 变成 NULL。始终用 Python `urllib` + `json` 写入。

## 常见判断模式

### ✅ 判定重复

- 标题仅标注差异（二次/重发/第二次/第X批/合同公示），proj_name 和正文实质相同
- att_ext 一个有完整附件一个无，正文实质相同
- 不同批次发布同一采购意向（如第1批、第2批、第3批均有同一项目）
- 多条同一采购意向的重复收录
- detail 正文项目编号相同 + 采购内容相同 + 时间一致
- 第一次询比采购失败后第二次询比（正文明确提到"第一次失败"/"供应商不足3家"），实质相同
- 同项目不同次变更公告（如第一次变更、第二次变更），实质相同

### ❌ 判定非重复

- detail 正文项目编号不同（不同标段/不同项目）
- detail 正文金额/供应商/项目编号不同（不同采购记录）
- 验收单编号/采购记录编号不同（不同采购记录）
- att_ext 附件内容实质不同（如一个是采购公告，一个是中标结果）
- **proj_name 为"无效"且 dwd_bid_it_all 中项目编号/客户名完全不同 → 错误归组产生同一个 reid，非重复**
- **proj_name 解析失败时，即使 proj_name 相同也不能直接判定为重复，必须查 detail**
- **同一项目不同包（A包 vs B包 vs C包）的中标/变更公告，虽同招标编号但属不同标段，非重复**

## ⚠️ 二次招标陷阱

标题出现"二次"时，极易误判为重复（实为同一项目的二次公告）。必须同时查 detail 正文中：

1. **项目编号**——两次公告编号是否完全一致
2. **获取文件时间**——时间不同则是二次公告（非重复）
3. **`att_ext` 附件标题**——是否明确标注"二次采购公告"

**判断逻辑**：
- 项目编号相同 + 获取文件时间不同 = 二次公告 → **非重复**
- 项目编号相同 + 正文实质无差异 = 同一来源重复抓取 → **重复**

**实操案例（reid=3c50e926）**：两记录 att_ext 一个写"采购公告"，一个写"二次采购公告"，项目编号一致，获取文件时间相差7天 → 判定为"否"（二次公告，非重复）

## 多 jy_id 组处理

当同一 reid 含有 >2 条 jy_id 时，必须逐一查 detail 确认：

1. **proj_name 都有效且只有一个** → 大概率重复，查 detail 确认项目编号/金额/时间是否一致
2. **proj_name 为"无效"或空** → 切勿凭 proj_name 判断，必须全部查 detail 确认项目编号是否相同
3. 若为重复：rr = 任意一条，rd = **其余所有 jy_id**（英文逗号分隔）
4. 若为非重复：所有 jy_id 均保留，rr/rd 任意

**⚠️ 重要**：proj_name 为"无效"的多 jy_id 组（如 34 条、31 条），极大概率是错误归组，实际混着完全不同项目，dwd_bid_it_all 中项目编号/客户名会有明显差异。dif y_ns_re_readsource 中表现为"proj_name 种类 = 1"（因为全是同一个无效值），容易误判为重复，**必须逐条查 dwd_bid_it_all + detail**。

## 断点续跑

每次分析前，先查 `result.dify_ns_re_result` 中已存在的 reid，从 dify_ns_re_readsource 中排除：

```python
done = set(row['reid'] for row in result['data'])
# 新分析时加 WHERE reid NOT IN ('done_reids')
```

## 输出格式

每批分析完成后，给用户汇总：

```
本批 N 组结果：
  ✅ 重复（是）：X 条
  ❌ 非重复（否）：X 条

结果表最新状态：
  重复（是）：XX 条
  非重复（否）：XX 条
  总计：XX 条
```

确认无误后写入结果表，写入完成后汇报写入数量和表当前总量。
