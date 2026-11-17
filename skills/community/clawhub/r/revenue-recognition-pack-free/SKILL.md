---
name: revenue-recognition-pack-free
slug: revenue-recognition-pack-free
displayName: 收入确认与结算技能包（免费版）
display_name: 收入确认与结算技能包（免费版）
display_name_en: Revenue Recognition & Settlement Pack (Free)
version: 1.0.21
summary: 把一个项目的一套收入材料按 7 项收入确认与结算核对逐项目核一遍，每个项目一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description: 把一个项目的一套收入材料按 7 项收入确认与结算核对逐项目核一遍，每个项目一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description_zh: 把一个项目的一套收入材料按 7 项收入确认与结算核对逐项目核一遍，每个项目一行结论，结论都带原文文件与行号，不需要付款、不需要注册。
description_en: A local checker for revenue recognition and settlement worksheets. It runs 7 built-in checks per project directory and prints one conclusion line per project, each finding citing the source file and line. Fully local, no network, no API key, no call limit.
category: business-ops
tags: [收入确认,SaaS,版税结算,软件许可,门店销售,租金,应收催收]
license: Proprietary
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 收入确认与结算技能包（免费版）

> **完全本地运行**：引擎已经打包在本技能里（`scripts/engine/`）。
> 核对过程不需要联网、不需要 API Key、**没有调用次数上限**、**不写任何文件**，材料不出本机。

## 什么时候用

**软件 / 内容 / 服务型公司的收入会计与项目财务**，在**每月收入确认与结算之前**。

典型场景：月度/季度复核前，把一类检查一次跑完所有项目

## 这个免费版查什么

**一次跑完所有项目，每家项目一行结论**（免费版的核心产出，完整可用）：

1. **SaaS 订阅收入确认核对** —— 复用 `parts/saas-revenue-recognition-check/`（逐字节来自免费包 `saas-revenue-recognition-check-free`）
2. **版税与保底分成结算核对** —— 复用 `parts/royalty-settlement-check/`（逐字节来自免费包 `royalty-settlement-check-free`）
3. **软件许可与授权期摊销核对** —— 复用 `parts/software-license-check/`（逐字节来自免费包 `software-license-check-free`）
4. **门店销售报表与收款方式核对** —— 复用 `parts/store-sales-report-check/`（逐字节来自免费包 `store-sales-report-check-free`）
5. **租金账单与免租期核对** —— 复用 `parts/rent-collection-check/`（逐字节来自免费包 `rent-collection-check-free`）
6. **分期收款本金与利息拆分核对** —— 复用 `parts/installment-rate-check/`（逐字节来自免费包 `installment-rate-check-free`）
7. **应收催收计划与账龄核对** —— 复用 `parts/receivable-collection-plan-check/`（逐字节来自免费包 `receivable-collection-plan-check-free`）

> 每一项的实际规则在 `scripts/engine/parts/<检查项>/` 里（**逐字节复用**仓库里已有的免费引擎，
> 一行规则都没有改）。本包只做"目录 → 项目 → 逐项派发"的编排。

## 怎么用

```bash
node scripts/run.mjs --sample                 # 单项目样例（内置，7 项全跑）
node scripts/run.mjs --sample-batch           # 3 家项目的批量样例（干净 / 有硬伤 / 未交材料）
node scripts/run.mjs --input <项目目录>     # 批量：每个子目录 = 一家项目
node scripts/run.mjs --input <材料.json>        # 单项目：JSON 或纯文本
```

项目目录怎么放（每个子目录里放这家项目的一套材料，每项用 `=== 检查项 ===` 分段，Tab 分隔最稳）：

```
项目目录/
  豫州云服务项目（2026-04 收入确认）/收入材料.txt
  中岳内容平台项目（2026-04 收入确认）/收入材料.txt
```

## 结论怎么读

- 每家项目一行：`[结论] 项目名｜问题 N 项（P0/P1/P2）｜每一项:通过 / 有问题(n) / 未执行`；
- 有价值的是**问题明细**：每条都带 `项目 + 检查项 + 来源文件:行号 + 类别 + 具体数字`；
- 「未执行」与「通过」是两件事：**没交材料 / 材料认不出表 = 未执行**，不是"没问题"。

## 常见错法

- **把几个项目的材料放进同一个子目录**：`--input` 指向的目录里，**每个子目录 = 一个项目**。混在一起时结论里就没有项目名，跨项目台账也分不出是谁。
- **合同金额与已确认收入口径混用**：前者是合同总额，后者是本期按履约进度确认的部分；两个数混填会让"合同总额 ≠ 去重后合同金额"这类校验直接报出来。
- **含税金额与不含税金额混填**：同一张表里必须统一口径，混填会被逐行相加校验抓出来。
- **把收款方式合计当成收入**：收款是现金流入，收入是确认口径；两者有差额时要能解释（预收 / 应收 / 退款），解释不了就是硬伤。
- **拿 `--sample` 的输出当自己的结论**：样例数字是虚构的，必须换成你自己的材料再跑。

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- 跨项目汇总台账（全部项目 × 全部 7 项核对合并成一张总表）
- 收入风险排序清单（按 P0/P1/P2 排序，带项目名与原文文件行号）
- 跨项目共性问题归类（同一个问题命中 2 个及以上项目时合并成一条共性项）
- 收入台账导出（Markdown 与 CSV 文本，直接用于月度收入复核说明）

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界（请务必知道）

- **不做**：判断收入该按哪个准则、在哪个时点确认（属于**会计判断**，请按公司会计政策与准则执行）；
- **不做**：代替审计或出具鉴证意见（只做表内/表间的算术与勾稽核对）；
- **不做**：核对银行回单、平台账单、合同签署的真实性，或比对业务系统 / 收款平台的逐行明细；
- **不做**：读取 CRM / 计费系统 / 收款平台的导出文件（需要你先导出成文本，每个项目一个目录）；
- **不做**：判断某项收入是否要交税、按什么税率交（属于税务判断，请咨询税务师）；
