---
name: shared-cost-pack-free
slug: shared-cost-pack-free
displayName: 公共费用与分摊技能包（免费版）
display_name: 公共费用与分摊技能包（免费版）
display_name_en: Shared Cost & Allocation Pack (Free)
version: 1.0.21
summary: 把一家门店的一套费用材料按 6 项公共费用核对逐门店核一遍，每家门店一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description: 把一家门店的一套费用材料按 6 项公共费用核对逐门店核一遍，每家门店一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description_zh: 把一家门店的一套费用材料按 6 项公共费用核对逐门店核一遍，每家门店一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description_en: A local checker for shared-cost and allocation worksheets. It runs 6 built-in checks per store directory and prints one conclusion line per store, each finding citing the source file and line. Fully local, no network, no API key, no call limit.
category: business-ops
tags: [公共费用,水电分摊,仓储费,手续费,代理佣金,废料处置,门店核对]
license: Proprietary
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 公共费用与分摊技能包（免费版）

> **完全本地运行**：引擎已经打包在本技能里（`scripts/engine/`）。
> 核对过程不需要联网、不需要 API Key、**没有调用次数上限**、**不写任何文件**，材料不出本机。

## 什么时候用

**多门店 / 多项目公司的费用会计与成本岗**，在**每月费用结算与分摊入账之前**。

典型场景：月度/季度复核前，把一类检查一次跑完所有门店

## 这个免费版查什么

**一次跑完所有门店，每家门店一行结论**（免费版的核心产出，完整可用）：

1. **水电表抄见与计费核对** —— 复用 `parts/utility-meter-reading-check/`（逐字节来自免费包 `utility-meter-reading-check-free`）
2. **公共能耗费分摊核对** —— 复用 `parts/utility-allocation-check/`（逐字节来自免费包 `utility-allocation-check-free`）
3. **仓储费与超期费核对** —— 复用 `parts/warehouse-fee-check/`（逐字节来自免费包 `warehouse-fee-check-free`）
4. **支付手续费与结算金额核对** —— 复用 `parts/payment-fee-check/`（逐字节来自免费包 `payment-fee-check-free`）
5. **保险代理手续费与佣金核对** —— 复用 `parts/insurance-agency-fee-check/`（逐字节来自免费包 `insurance-agency-fee-check-free`）
6. **废料与边角料处置核对** —— 复用 `parts/scrap-sale-check/`（逐字节来自免费包 `scrap-sale-check-free`）

> 每一项的实际规则在 `scripts/engine/parts/<检查项>/` 里（**逐字节复用**仓库里已有的免费引擎，
> 一行规则都没有改）。本包只做"目录 → 门店 → 逐项派发"的编排。

## 怎么用

```bash
node scripts/run.mjs --sample                 # 单门店样例（内置，6 项全跑）
node scripts/run.mjs --sample-batch           # 3 家门店的批量样例（干净 / 有硬伤 / 未交材料）
node scripts/run.mjs --input <门店目录>     # 批量：每个子目录 = 一家门店
node scripts/run.mjs --input <材料.json>        # 单门店：JSON 或纯文本
```

门店目录怎么放（每个子目录里放这家门店的一套材料，每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）：

```
门店目录/
  豫州国贸店（2026-04 费用结算）/费用材料.txt
  中岳朝阳店（2026-04 费用结算）/费用材料.txt
```

## 结论怎么读

- 每家门店一行：`[结论] 门店名｜问题 N 项（P0/P1/P2）｜每一项:通过 / 有问题(n) / 未执行`；
- 有价值的是**问题明细**：每条都带 `门店 + 检查项 + 来源文件:行号 + 类别 + 具体数字`；
- 「未执行」与「通过」是两件事：**没交材料 / 材料认不出表 = 未执行**，不是"没问题"。

## 常见错法

- **把几家门店的材料放进同一个子目录**：`--input` 指向的目录里，**每个子目录 = 一家门店**。混在一起时结论里就没有门店名，跨门店台账也就分不出是谁。
- **抄见数与计费数只填一个**：这两列必须都在，且差额要能解释（倍率/线损/公摊）；只填一个时该店这一项会落进「未执行」，**不是"通过"**。
- **分摊基数与分摊金额对不上**：分摊金额 = 基数 × 单价（或占比 × 总额），把总额直接按"感觉"拆开会被逐户相加校验抓出来。
- **把押金/预付款当成当期费用**：这类款项要单独列，混进费用合计会让分摊结果整体偏大。
- **拿 `--sample` 的输出当自己的结论**：样例数字是虚构的，必须换成你自己的材料再跑。

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- 跨门店汇总台账（全部门店 × 全部 6 项核对合并成一张总表）
- 费用风险排序清单（按 P0/P1/P2 排序，带门店名与原文文件行号）
- 跨门店共性问题归类（同一个问题命中 2 家及以上门店时合并成一条共性项）
- 分摊台账导出（Markdown 与 CSV 文本，直接用于月度费用复核说明）

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界（请务必知道）

- **不做**：判断分摊口径该选哪一个（面积 / 人数 / 工时 / 收入占比属于**管理决策与会计政策**，请按公司制度执行）；
- **不做**：代替成本核算或出具鉴证意见（只做表内/表间的算术与勾稽核对）；
- **不做**：核对电费发票、银行回单、保单与支付凭证的**真伪**，或比对电力 / 银行 / 保险系统的逐行明细；
- **不做**：读取电表系统 / 银行流水 / 保险系统的导出文件（需要你先导出成文本，每家门店一个目录）；
- **不做**：判断各类费用的**税前扣除**是否成立（属于税务判断，请咨询税务师）；
