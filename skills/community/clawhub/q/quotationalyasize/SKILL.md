---
name: multi-project-quote-board
description: 多项目（同批供应商、同一询价口径）报价对比看板生成器，输出「中英双语可切换的自包含 HTML 看板 + 结构一致的 Excel」。适用于一次询价覆盖 2 个及以上子项目（如葡萄牙 Worten Chafiras & Leiria 两个店、西班牙多处点位），需同时呈现回标状态、逐项目明细、工期门槛判定、条款对比、待澄清清单、分项目价格排序与「满足工期前提下价格最低优先」的定标建议，且**明确不做跨项目合计**的场景。数据层与渲染层严格分离，HTML 与 Excel 共用同一份数据层，口径永不发叉。
agent_created: true
---

# 多项目报价对比看板（Multi-Project Quote Board）

把「一批同口径询价的多家回标」变成「一份可决策的双语看板 + 一张可存档的 Excel」。

本技能**不含任何真实门店/供应商名称**，全部由数据层驱动；换项目、换供应商数量、换货币、换工期门槛都不需要改渲染代码。模板自带可跑的脱敏示例（2 个项目 × 3 家供应商），`python gen_board.py` 即可出图。

---

## 1. 定位与边界

| 场景 | 用本技能 | 改用 |
|---|---|---|
| **同一批供应商、多个子项目**横向比价（报价 + 工期 + 条款 + 定标建议） | ✅ | |
| 单项目、多供应商、需要「分部分项 + 单方造价 + 异常核查 + 历史门店对比」 | ➖ | `bid-quote-cockpit` |
| 只要一份轻量「双方案/多方案价格对比」可视化（成本构成堆叠条 / 周期时间轴 / tradeoff 结论卡） | ➖ | `bilingual-price-compare` |
| 某家澄清/修订后报价回灌既有对比表 | ➖ | `bid-quote-clarification-sync` |
| 两家 Excel/BOQ 逐行机械比对 | ➖ | `excel-quote-compare` |

**与 `bid-quote-cockpit` 的关键区别（选型要点）：**

| 维度 | multi-project-quote-board（本技能） | bid-quote-cockpit |
|---|---|---|
| 项目数 | **多项目并置**（本项目核心） | 单项目为主 |
| 跨项目合计 | **明令禁止**，分项目独立定标 | 不涉及 |
| 定标逻辑 | 内置**工期门槛 + 最低价**判定（7.1–7.5） | 侧重总价排名/异常核查，定标为可选模块 |
| 配置方式 | 直接改 Python 数据层（dict） | 填 `config.json` / `quotes.json` |
| 交付物 | HTML **+ 结构对齐的 Excel（6 sheet）** | HTML（+ 可选） |
| 依赖 | 纯标准库出 HTML；Excel 需 openpyxl | 需内联 echarts |

> 共用红线：**只用报价原文数字，禁止补全/估算/同口径估算**；勾稽 `生产 + 运输 + 安装 == Total` 必须全通过。

---

## 2. 快速开始（3 步）

```bash
SK=~/.workbuddy/skills/multi-project-quote-board

# 1. 复制模板到工作目录
cp $SK/scripts/gen_board.py  ./gen_board.py
cp $SK/scripts/gen_excel.py  ./gen_excel.py

# 2. 改 gen_board.py 顶部 DATA LAYER（只改这一处！）—— 项目/供应商/报价/工期/条款/待澄清
#    然后出 HTML 看板
python gen_board.py            # → board.html（自带中英切换）

# 3. 用同一数据层出 Excel（务必用带 Pillow 的解释器，若含图片）
python gen_excel.py            # → board.xlsx（6 个 sheet）
```

运行成功标志（务必核对）：

```
=== RECON (Unit+Transport+Install==Total): ALL OK ===
WROTE board.html  bytes=...
WROTE board.xlsx  bytes=...
```

> `RECON` 不是 `ALL OK` → **先修数字，不要交付**。每一条 `prod+trans+inst != total` 的明细都会打印 `RECON FAIL: <key> <pid> {...}`。

---

## 3. 核心架构（勿改）

```
gen_board.py
├── ① DATA LAYER  （上半部，标 "DATA LAYER —— 唯一手工维护区"）
│      BOARD_TITLE / PROJECTS / SUPPLIERS / QUOTES / LEAD_* / TERMS / CLAR / TRANS_NOTE
│      ⋮
│   # ============================ DATA LAYER END ============================
└── ② RENDER LAYER （下半部，读数据层出 HTML，一般不动）

gen_excel.py
   读 gen_board.py → split("DATA LAYER END")[0] → exec 复用同一数据层 → 出 6 sheet
```

**为什么这样设计：** HTML 与 Excel 是两份交付物，若各自硬编码数字，迟早「HTML 改了 Excel 没改」。把数据层做成唯一的真源、Excel 生成器 exec 复用，**口径在物理上不可能发叉**。改一个报价只需改 `QUOTES` 一处。

`DATA LAYER END` 这行标记是**契约**：`gen_excel.py` 靠它切分。删掉或改写这行，Excel 生成器会直接 `SystemExit`。

---

## 4. 数据层字段速查

| 变量 | 作用 | 修改要点 |
|---|---|---|
| `BOARD_TITLE` | (中文标题, English title) 二元组 | H1 与 Excel 标题、`<title>` 同步 |
| `TENDER_DATE` / `INVITED_COUNT` | 发标日 / 邀请家数 | 只用于总览副标题，不参与计算 |
| `PROJECTS` | `[{id,name,area,qty}]` 子项目列表 | `id` 是 QUOTES 的键，**一旦定下不要改** |
| `SUPPLIERS` | `[{key,name,color,status,date}]` | `status`: `received` / `pending`（**顺序即条款表列序，见 §6 坑 1**） |
| `QUOTES` | `{key:{pid:{prod,trans,inst,total}}}` | **四值须满足 prod+trans+inst==total**；只有原文数字 |
| `TRANS_NOTE` | `{(key,pid):"已含在运输费用中"}` | 驱动明细表数字格的三态文案（见 §7） |
| `LEAD_START` | 统一起算日（下单日） | 定标工期门槛的基准 |
| `LEAD_DEADLINE` | 安装完成截止日 | `完成日 <= 此日` → 满足工期 |
| `LEAD_SPAN` | `{key:{pid:天数}}` 自起算至完成总天数 | 严格取自报价原文 |
| `LEAD_ABS_END` | `{key:{pid:date}}` 绝对日期排期者 | **绝对日期者不顺延**（见 §8） |
| `LEAD_BASIS` / `LEAD_BASIS_PID` | 工期依据原文（中英） | 进「7.1 工期满足性判定表」的依据列 |
| `TERMS` | `[(中,英, 各供应商取值…)]` | 每条取值个数 == `SUPPLIERS` 个数，顺序对齐 |
| `CLAR` | `[(级别,中,英)]`，级别 P0/P1/P2 | 自动按 P0→P1→P2 排序 |

### 扩容（团队最常问）

- **新增一家供应商**：`SUPPLIERS` 加 dict + `QUOTES` 补该项目条目 + `TERMS` 每行补一列 + `TRANS_NOTE`/`LEAD_SPAN`/`LEAD_BASIS` 补键。渲染层无需动。
- **某家尚未回标**：`status` 保持 `"pending"`，看板自动渲染「待回标」占位行，**不影响任何计算**（`RECV_KEYS` 只含 `received`）。
- **只更新报价**：只改 `QUOTES` 数值 → 最低标高亮、差额、排序、定标结论全部自动重算。

---

## 5. 看板八大板块

| # | 板块 | 内容 |
|---|---|---|
| 一 | 回标状态与总览 | KPI 卡（已回标家数 / 各项目「满足工期+报价最低」）+ 供应商状态表 |
| 二 | 逐项目明细对比 | 生产 / 运输 / 安装 / Total / vs 最低；数字格三态（见 §7） |
| 三 | 工期（Lead Time）对比 | 各家所报工期 + 起算推算完成日 + 是否满足 |
| 四 | 条款对比 | 材质工艺 / 运输口径 / VAT / 付款条件… |
| 五 | 待澄清清单 | 按 P0 > P1 > P2 排序 |
| 六 | **各项目价格排序** | 纯价格排序，**每项目独立一行，绝不做跨项目合计** |
| 七 | **定标建议** | 工期判定 + 满足者按价排序 + 推荐结论 + 需澄清 + 前置条件 |
| 八 | 扩容说明 | 数据层改动指引（写进看板，便于团队自查） |

### ⛔ 铁律：不做跨项目合计

本节（及全板）**禁止把两个项目的总价加总**。理由（已写入看板第六节说明）：不同项目的工程量与交付条件不同，合并总价无决策意义。若要表达「打包」，只能单列 what-if，且**必须明确标注为情景假设、不进排名**。

对应地：KPI 按项目拆成独立卡片、第六节删掉「两项目合计」行、7.3 结论按项目独立定标。Excel 侧同样（`01 回标状态` 无合计列、`06 定标建议` 无合计行）。

---

## 6. 数据层三大坑（必读）

### 坑 1 — `TERMS` 取值顺序必须 == `SUPPLIERS` 顺序

`TERMS` 每行是 `(中, 英, v1, v2, v3…)`，`v1…vn` 按 `SUPPLIERS` 顺序一一对应。若顺序错一位，**整列条款错位**且不报错（静默错误，最危险）。

### 坑 2 — 用 `%` 格式化大段 HTML 会炸

渲染层把整页 HTML 拼成一个字符串。若正文里出现 `width:100%`、`%s` 等，与 Python 的 `%` 格式化冲突 → `TypeError: not enough arguments for format string`，且**产物静默为空**。
**模板的解法**：标题用 token 占位 `@@TITLE@@` + `.replace("@@TITLE@@", …)`，不用 `%` 拼标题。你新增含 `%` 的文案时，沿用局部拼接或 `.replace()`，别整段 `%`。

### 坑 3 — 明细表数字格三态不可混

运输/安装列取值只有三种合法形态：**数字** / **`已包含在运输费用中`** / **`未报价待澄清`**。由 `cell_state()` 依据 `QUOTES` 值 + `TRANS_NOTE` 自动派生，**不要在数据格里手写中文**（会把数字列变成文本列，Excel 求和/排序失效）。

---

## 7. 定标模块：工期门槛 + 最低价（本技能灵魂）

判定三原则（看板第七节顶部固定文案）：

1. **起算日统一**：全部按 `LEAD_START`（下单日）起算。
2. **工期门槛**：所报工期自起算日推算，能在 `LEAD_DEADLINE` 前完成安装 → **满足**；不能 → 列入「**需请对方澄清**」（⚠️ 不是直接淘汰）。
3. **定标原则**：**满足工期者中，报价最低优先**（工期是门槛，价格是排序键）。

实现函数（渲染层，Excel 侧同样实现一份）：

```python
def lead_result(k, pid):
    # 绝对日期排期者不顺延；其余 = 起算日 + 总天数
    est = LEAD_ABS_END[k][pid] if (k in LEAD_ABS_END and pid in LEAD_ABS_END[k]) \
          else LEAD_START + dt.timedelta(days=LEAD_SPAN[k][pid])
    return {"days": …, "est": est, "ok": est <= LEAD_DEADLINE, …}

def sched_lowest(pid):
    cand = sorted([k for k in RECV_KEYS if satisfied(k, pid)],
                  key=lambda k: QUOTES[k][pid]["total"])
    if not cand:                          # 无人满足 → 回退纯最低（并须在看板提示）
        cand = sorted(RECV_KEYS, key=lambda k: QUOTES[k][pid]["total"])
    return cand[0], QUOTES[cand[0]][pid]["total"], cand
```

第七节固定结构（老板认可的清晰版式，勿改顺序）：

```
7.0 判定规则三条（灰底 info 卡）
7.1 工期满足性判定表（项目 × 供应商：所报工期 / 依据原文 / 完成日 / 是否满足）
7.2 满足工期的候选 —— 按报价排序（首位绿底 rec-row）
7.3 定标推荐结论（逐项目卡片：推荐 + 报价 + 备选）
7.4 需请对方澄清（工期不满足）—— 列出超出天数
7.5 定标前置条件（P0 未闭环不按当前价定标；起算日需各家认可）
```

**KPI / chip 口径必须与定标口径一致**：项目卡右上角「✓ 当前报价最低（工期满足+报价最低）」、KPI 卡取值都走 `sched_lowest`，**不能显示纯最低价那家**（否则会出现「KPI 说 A 最低，第七节却推 B」的自相矛盾）。

**绝对日期特例（`LEAD_ABS_END`）**：某些供应商给的是绝对排期（如「X 月 X 日完成」），不随统一起算日顺延。这类必须放进 `LEAD_ABS_END`，否则会被错误地按「起算日 + 天数」平移。

---

## 8. 双语切换机制（CSS-only，禁用脚本也能用）

- 正文每段用 `<span class="zh">中文</span><span class="en">English</span>`（模板封装为 `Z()` / `E()` / `BI(zh,en)`）。
- 有两个隐藏 radio `#lzh` / `#len` + `body:has(#lzh:checked) .en{display:none}` 等 CSS 规则实现切换。
- JS **只用于 localStorage 记忆语言偏好**，不承担切换逻辑 —— 因此断网/禁脚本时切换仍可用。
- 默认中文。

**自检**：`zh` span 数应等于 `en` span 数（模板示例 134 = 134）。不等 → 有段落漏了英文或漏了中文。

---

## 9. 环境要求

| 用途 | 要求 |
|---|---|
| 出 HTML | 任意 Python 3（**纯标准库**：os / datetime / html，无第三方依赖） |
| 出 Excel | `openpyxl` |
| Excel 嵌图（可选） | **必须用带 Pillow 的解释器**，否则图片**静默跳过**（产物 media=0） |

本机固定用 venv 解释器（Pillow 10.4.0 + openpyxl 3.1.5）：

```bash
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe gen_excel.py
```

> 托管的基础解释器 3.13.12 **无 PIL**：`openpyxl.drawing.image.Image` 会全部静默跳过，xlsx 体积明显偏小（如 18KB）且无图片。出图必须走上面这个 venv 解释器。

---

## 10. 交付前检查清单

- [ ] 运行日志 `=== RECON … ALL OK ===`（每条明细勾稽通过）
- [ ] `board.html` 已生成，浏览器打开：中/英切换正常，两语字数相等
- [ ] **全板无跨项目合计**（KPI 分项目、第六节无合计行、7.3 分项目独立、Excel 同）
- [ ] KPI/chip 的「最低」= 满足工期者中的最低（与第七节结论一致）
- [ ] `LEAD_START` / `LEAD_DEADLINE` 全文一致，无残留旧日期
- [ ] 待澄清 P0 项已在看板第五节列全
- [ ] 所有数字与报价原文逐条可对（禁止补全/估算）
- [ ] `board.xlsx` 6 个 sheet 齐全，条款表列顺序 == 供应商顺序

---

## 11. 参考

- `scripts/gen_board.py` —— 数据层 + 渲染层模板（可直接改，含脱敏示例）
- `scripts/gen_excel.py` —— 复用数据层出 6 sheet Excel
- `references/pitfalls.md` —— 踩坑与修复记录（`%` 格式化、条款错位、图片静默跳过、双语不等长等）

**关联技能**：`bid-quote-cockpit`（单项目重看板）、`bilingual-price-compare`（轻量双方案对比）、`bid-quote-clarification-sync`（澄清回灌）、`excel-quote-compare`（机械比对）、`bid-price-analysis`（商务标分析表）。
