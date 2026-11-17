# Demand Gen 投放数据分析汇总报告 — HTML

> **终稿语言**：章节标题跟 `meta.lang`（`zh` 或 `en`）。叙事正文用同一种语言。
> **适用场景**：用户要 **Demand Gen / 需求开发 / 需求生成** 的投放数据分析、汇总报告、客户与运营共用版。工作流 **P4-DG**。
> **默认终稿**：HTML。用户要 Excel / xlsx 时改读 `demand-gen-analysis-report-excel.md`，**不要**调用 `demand-gen-render`。
> **禁止**：手写 HTML；把本模板样例里的演示数字（如 $42,680、286 条有效线索、ROAS 2.84）写进 JSON；把本报告当成 Google 全账户周期报告（那是 P4）或当成创建广告（那是 W3）。

客户与运营共用一份报告，不拆两版。HTML 固定 8 节：结论、口径、核心指标、漏斗、各维度、线索质量、行动建议、测试计划。趋势异常只在 Excel 第 5 张表。

---

## 执行步骤

1. Read `references/core/agent-conventions.md`、本文。
2. `siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-dg`。无记录则停止。币种用 `items[].ma.currencyCode`。
3. 确认本期起止。用户给了对比期就用用户的；没给则取紧挨着的等长上一期，并在可信度说明里写明。
4. 拉数（见下节）。对每个 `google-analysis` section Read 同目录 `*.outline.txt` 后再写脚本。业务 JSON 只在脚本里读。
5. 脚本把能对上的数字写入 `demand-gen-analysis-report.json`（结构见下）。对不上的格子写 `未提供`，不要推算。
6. 渲染：

```bash
siluzan-tso google-analysis demand-gen-render \
  --data ./demand-gen-analysis-report.json \
  --out ./demand-gen-analysis-report.html \
  --lang zh
```

7. 按 `agent-conventions.md` §七 自检。`meta.accountId` 必须是用户给的 `mediaCustomerId`。

---

## 拉数

```bash
mkdir -p ./snap-dg
siluzan-tso list-accounts -m Google -k <id> --json-out ./snap-dg

siluzan-tso google-analysis -a <id> --start <S> --end <E> --json-out ./snap-dg \
  --sections overview,campaigns,daily-metrics,devices,geographic,audience

siluzan-tso ad demand-gen list -a <id> --json-out ./snap-dg
```

`campaigns` 只保留 `channelTypeV2` 为 `DEMAND_GEN` 的行。Search / PMax / Display 不要并进本报告。

每个 Demand Gen 系列再拉版位（日期参数是 `--start-date` / `--end-date`，不是 `google-analysis` 的 `--start`）：

```bash
siluzan-tso ad demand-gen report -a <id> --campaign-id <campaignId> \
  --start-date <S> --end-date <E> --json-out ./snap-dg
```

`spend` 是账户币种浮点，不要拿去当预算。暂停系列全 0 仍是成功，在该行注明。

对比期再拉一遍 `campaigns` 与 `ad demand-gen report`。不要用本期数字充对比期。

### 哪些数不能从广告接口来

有效线索、有效率、商机、商机率、成交、成交收入、业务 ROAS、表单提交、CRM 批次成熟度，都要用户另行提供。用户没给就写 `未提供`，结论里说明因此不能判断该不该加预算。

`devices` / `geographic` / `audience` 是**账户合计**，含非 Demand Gen。不能拆到 Demand Gen 时，该维度整表写一行 `未提供：当前接口是账户合计，不是 Demand Gen 专属`。版位只用 `ad demand-gen report`。

字段名以当次 outline 和版位落盘的键为准。禁止猜 `keywordText`、`geoName` 这类名字。

---

## JSON 结构

根上只有 `meta` 和 `narrative`。金额、比率写成展示字符串（`$120.00`、`1.92%`）。比率若来自 0~1 小数，先乘 100 再写入字符串。

```json
{
  "meta": {
    "lang": "zh",
    "accountId": "6326027735",
    "accountName": "账户名",
    "currency": "USD",
    "timezone": "America/Los_Angeles",
    "startDate": "2026-10-01",
    "endDate": "2026-10-29",
    "compareStartDate": "2026-09-02",
    "compareEndDate": "2026-09-30",
    "periodDays": 29,
    "compareDays": 29,
    "objective": "用户给的业务目标，没有则省略",
    "primaryConversion": "用户给的主转化，没有则省略",
    "credibilityNote": "写清哪些层已对账、哪些是未提供",
    "generatedAt": "2026-11-02",
    "confidence": "广告数据已对账"
  },
  "narrative": {
    "headline": "一句话结论",
    "summaryParagraph": "展开一句",
    "summaryPoints": [{ "tag": "有效", "title": "标题", "detail": "依据", "owner": "见第 3 节" }],
    "headlineKpis": [{ "label": "花费", "value": "$120.00", "delta": "▲10%", "tone": "down" }],
    "customerRead": "给客户的一句解释",
    "scopeRows": [{ "item": "投放范围", "value": "Google Ads Demand Gen" }],
    "conversionLevels": [{ "level": "平台转化", "definition": "Google Ads 点击归因", "source": "Google Ads", "use": "判断前端效率" }],
    "kpiGroups": [{ "title": "前端层", "items": [{ "label": "花费", "value": "$120.00", "delta": "▲10%", "tone": "down" }] }],
    "funnel": {
      "bottleneck": "最大流失环节；不知道就写未提供",
      "stages": [{ "name": "展示", "value": "1,200", "width": 100, "tone": "blue" }],
      "rates": [{ "stage": "点击 → 访问", "rate": "未提供", "factor": "无访问字段" }],
      "adsAdvice": "广告侧修改",
      "salesAdvice": "销售侧修改；没有 CRM 就写未提供"
    },
    "dimensions": [{
      "title": "5.1 Campaign",
      "width": "full",
      "columns": ["投放组合", "花费", "平台转化", "修改建议"],
      "rows": [{ "cells": ["系列名", "$120.00", "3", "先看质量"], "tone": "neutral" }],
      "note": "只含 DEMAND_GEN"
    }],
    "quality": {
      "badge": "CRM 未提供",
      "columns": ["线索批次", "表单", "有效", "商机", "成交", "成交收入", "成熟度"],
      "rows": [{ "cells": ["未提供", "未提供", "未提供", "未提供", "未提供", "未提供", "未提供"], "tone": "neutral" }],
      "businessConclusion": "没有 CRM，不能计算业务 ROAS",
      "splitFactors": "广告只对平台转化负责"
    },
    "actionBadge": "先补数据，再谈扩量",
    "actions": [{
      "priority": "P0",
      "title": "补齐业务层",
      "evidence": "有效线索列为未提供",
      "action": "向用户要批次、有效线索、商机、成交",
      "verify": "三列不再是未提供",
      "owner": "运营",
      "deadline": "拿到资料后",
      "risk": "没有业务层时不要加预算"
    }],
    "tests": [{
      "name": "创意开头",
      "hypothesis": "痛点开头优于功能清单",
      "groups": "功能清单 / 痛点+演示",
      "metric": "有效线索成本",
      "sample": "每组 ≥50 有效线索",
      "period": "14–21 天",
      "stop": "样本不足则不判胜负"
    }],
    "trend": {
      "note": "只给 Excel 第 5 张表，HTML 不展示",
      "columns": ["日期", "花费", "平台转化", "平台CPA", "有效线索", "备注"],
      "rows": [{ "cells": ["2026-10-01", "12.00", "1", "12.00", "未提供", ""], "tone": "neutral" }],
      "anomalies": [{ "phenomenon": "某日花费抬升", "evidence": "来自 daily-metrics", "cause": "只写数据里看得到的原因", "action": "次日复核" }]
    }
  }
}
```

`tone`：指标用 `up` / `down` / `neutral`（变好 / 变差 / 只是变化）。表格行用 `good` / `warn` / `bad` / `neutral`。漏斗条用 `blue` / `green` / `purple` / `orange`，`width` 是 0–100 的条宽，不是转化率。

`dimensions` 建议顺序：Campaign、素材、受众、地域、设备、版位、落地页来源。没有数据的维度保留标题，行内写 `未提供` 和原因。`width: "full"` 独占一行，`"half"` 与下一张并排。

渲染会拒绝：缺 `accountId`、币种、日期、`headline`、核心指标、漏斗阶段、维度、行动、测试。

---

## 口径

- 花费、展示、点击、平台转化只加总 Demand Gen 系列。
- 平台 CPA = Demand Gen 花费 / Demand Gen 平台转化。转化是 0 时写 `未提供`，不要写 0 成本。
- 有效成本、有效率、商机率只有用户给了分子分母才算。分母是 0 写 `未提供`。
- 业务 ROAS = 用户给的已归因收入 / Demand Gen 花费。没给收入就不算。
- 地域有效线索少于 30 只观察，不写扩量或关停。
- 系列 ID、广告组 ID 在 Excel 里是文本。HTML 展示名优先用名称，没有名称再展示 ID。
