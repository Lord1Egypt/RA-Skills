# Google 季度经营报告

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> collect 只出事实；Agent 只写 `narrative`；`render` 注入 `google-quarterly-report.html`（大族分页版式 + ECharts）。
> **禁止** Read HTML 模板。行业数据不做。展会 / 蜜月期服务页不自动出。新探索（视频 / PMax / 发现 / 展示）全无量则整章隐藏。
>
> **下期规划**：写 `narrative.plan` 前必读 `report-templates/google-quarterly-plan.md`（九章 + Q01–Q30）。规划只消费 collect，不编造预算/CPA/询盘，不写自动调价/暂停。
>
> **触发（命中即 P10，勿改 P4/P9）**：月度报告、月总结与规划、季度报告、Q3 汇总、Q4 规划、季度汇报、投放季报、客户版、大族模板、下月规划；或「效率 + 区域询盘 + 国家明细 + 规划」。用户说月度则 `--start/--end` 用该月（默认上一完整自然月）。

## 询盘入场（硬规则）

CLI **不读** xlsx / csv / 截图。

**开场必问（未带表则停）**：本轮消息里**没有**询盘表（xlsx / csv / 截图 / 粘贴表 / 已落盘 `inquiries.json`）时，**先问再拉数**。问完必须等用户回复；在用户发来表格、或明确说「没有 / 跳过 / 先不出询盘」之前，**禁止** `google-quarterly collect`、写 `narrative`、`render`。已附表格或用户已回答过则不必再问。

问法（可原样用）：

> 季度报告里的区域询盘、询盘成本和规划主目标会用到询盘明细。您这边有本期询盘表吗（Excel / CSV / 截图 / 粘贴表均可）？有的话请发过来；没有回复「没有」即可，我按广告数据继续出报告。

收到表格后：

1. **Agent** 抽行、归一后落盘 `./snap-p10/inquiries.json`，再 `--inquiries` 传给 collect。
2. collect → 只写 `narrative` → `render` 出 HTML。

**禁止**把原始 `.xlsx` / `.csv` 传给 `--inquiries`（会 `JSON.parse` 失败）。用户说没有：可 `--inquiry-conversion <转化动作名>`（须用户点名）；再没有则询盘位留空并脚注。**禁止编造询盘行。**

落盘 JSON：根为数组或 `{ "items": [...] }`。**用之前先看一眼表头**，有日期/国家/产品这类列即可（列名接近即可，如 `时间`=`询盘日期`）。**禁止编造**。

| 用途 | 常见键 | 归一 |
| ---- | -------- | ---- |
| 询盘日期 | `询盘日期` / `date` / `时间` / `time` | `YYYY-MM-DD`；Excel 序列号由 Agent 转好 |
| 目标国家/地区 | `目标国家/地区` / `国家(中文)` / `国家` / `country` / `countryZh` | 英文/缩写先译中文，与 geographic `countryNameZh` 对齐 |
| 产品/品类 | `产品/品类` / `产品` / `product` | 自由文本 |
| 询盘来源关键词 | `询盘来源关键词` / `客户来源` / `来源` / `source` | 可选 |
| 询盘质量分级 | `询盘质量分级` / `quality` / `qualityGrade` | 有则用 |
| 月份 | `月份` / `month` / `ym` | 可由询盘日期推导 |

样例：

```json
[
  { "询盘日期": "2026-04-12", "目标国家/地区": "印度", "产品/品类": "协作机器人", "询盘来源关键词": "WhatsApp" }
]
```

e2e 对照：`src/commands/google-quarterly/test-fixtures/inquiries-q2-2026.xlsx`（给人看的样表）+ 同目录 `.json`（collect 真入口）。

## CLI

```bash
siluzan-tso google-quarterly collect \
  -a <mediaCustomerId> --start 2023-07-01 --end 2023-09-30 \
  --json-out ./snap-p10 \
  --account-name "客户名" \
  --inquiries ./inquiries.json          # 可选；必须是上节 JSON，禁止传 xlsx
  # --inquiry-conversion "表单提交"     # 无询盘载体时用转化动作名称兜底

# Agent 撰写 ./snap-p10/google-quarterly.json（只含 narrative，勿改 kpis）

siluzan-tso google-quarterly render \
  --data ./snap-p10/google-quarterly.json \
  --collect ./snap-p10/google-quarterly-collect.json \
  --out ./snap-p10/google-quarterly-report.html
```

`render` 打印 HTML 路径后**立刻交付该文件并结束**。封面和章节称呼由日期决定，不用改 HTML：完整自然季 →「Q3 季度…」；从 1 号起、起止在同一个月（含未过完的本月，如 10-01～10-22）→「10月 月度…」；跨月但不是完整自然季 →「本期」。**禁止**打开、grep 或改写 HTML，**禁止**为改「季度 / 月度」再跑一遍 render。用户没要 PDF 不要转换；要了也只转一次，不要读 PDF 正文、不要截图、不要用视觉模型验收。

省略 `--start/--end` 时 collect 用上一完整自然季（上海日历）。

可选：`--keyword-seeds "a,b"` 走 Keyword Planner（标注数据源，禁止写成行业指数）。**不做**频道订阅总数、订阅来源饼、视频类型（要 YouTube Analytics / 人工分类）。YouTube 广告能拿到的曝光 / TrueView / 完播 / CPV / 频道 ID /（若已关联）广告带来订阅，collect 写入 `exploreAds.types[video]` + `videosSummary`；PMax / 发现 / 展示并行写入 `exploreAds`。render 用 tab 切换，不编造 ABCD / 素材组 / 受众切分。

Agent JSON Schema：`assets/google-quarterly-report.schema.json`。

## Spike（网关）

| 能力 | 官方 | Sammamish | CLI |
| ---- | ---- | --------- | --- |
| 消耗最高国一级行政区 | `geographic_view` + `geo_target_state` / `province` / `region` | `GET …/reports/geo/subdivisions`（可带 `countryCriterionId`） | collect 自动选本期花费最高国家；未发布或该国无分段则国家级回退 |
| YouTube 广告层 | `video` 资源：title / channel_id / TrueView / 四分位完播 / CPV | 已有 `GetVideoReport` | 新探索「视频」tab；无四类试验线则隐藏整章 |
| 广告带来订阅 | Ads 转化动作名含 subscribe/订阅 | 已有 `conversion-actions` | 有则展示；**不是**频道粉数 |

## 事实字段（collect，禁止改）

| 字段 | 来源 |
| ---- | ---- |
| `kpis` / `monthly` | 系列加总；月度来自各月 `campaigns`，不是 daily-metrics |
| `inquiries` | Agent 转好的 JSON（`--inquiries`）优先；否则 `--inquiry-conversion`；再否则空，页脚注明口径 |
| `regions` / `countries` | 询盘按国家归并（印度/印尼单独成桶）+ 花费来自 geographic |
| `usStates` / `meta.drillCountry` | 下钻对象=本期花费最高国家；Sammamish `GET …/reports/geo/subdivisions`（`geo_target_state` / `province` / `region`）；无分段则回退该国国家行，**不写死美国** |
| `exploreAds` / `videosSummary` | 四类并行：视频（Ads 视频报表，无则 VIDEO 系列）/ PMax / 发现 / 展示。`specialAds` 仍保留兼容（只取一类）。不做订阅总数 / 来源饼 / 视频类型。四类全无量则 HTML 隐藏整章 |
| `planDefaults` | 三档：`spendFloor`=本期、`spendLow`=+30%、`spendHigh`=+50%；建议档月度 `monthSuggested` 默认 30/35/35。**不是**已批预算。**不**自动给 CPA/询盘目标 |

频道订阅总数、订阅来源、视频类型本报告不拉。

## Agent 只写 `narrative`

写 `plan` 前 Read `google-quarterly-plan.md`。`plan.analysis` 必填（3～5 条结论）；`goals` / `budget` / `structure` / `keywords` / `audience` / `creative` / `roadmap` / `risks` 写规划时都要有。每条带口径标签。

```json
{
  "narrative": {
    "executiveSummary": ["本期花费…", "询盘…"],
    "sections": {
      "efficiency": { "analysis": ["…"] },
      "adType": { "analysis": ["…"] },
      "region": { "analysis": ["…"] },
      "summary": { "analysis": ["…"] }
    },
    "plan": {
      "analysis": ["已确认：…", "基于历史数据：建议档取 planDefaults.spendLow"],
      "goals": { "analysis": ["主目标：有效询盘…"] },
      "budget": { "analysis": ["核心市场优先；测试设上限"] },
      "structure": { "analysis": ["Search 守基本盘；P0：…"] },
      "keywords": { "analysis": ["产品词精确/词组；否词：求职/教程"] },
      "audience": { "analysis": ["待业务确认：客户名单未导入"] },
      "creative": { "analysis": ["主题：工业场景；缺口：PMax 视频"] },
      "roadmap": { "analysis": ["第一个月基础验证；第二个月核心建设；第三个月已验证方向扩"] },
      "risks": { "analysis": ["销售回传缺失"] }
    }
  }
}
```

缺 `executiveSummary` / `sections.*.analysis` / `plan.analysis`（或 `plan.goals` / `plan.text`）时 render 失败。九章缺章不拒渲染，但规划不合格。

HTML 章节（render 自动分页，勿手写 HTML）：封面 → 浏览逻辑 → 核心结论 → ①效率 ②类型 ③区域 ④国家 ⑤下钻 ⑥账户 → 新探索 tabs → 总结 → 规划核心（五卡 + 月度阶梯）→ 预算配比 → 国家加/守/砍 → 搜索打法 → 非搜索清单 → 受众 → 周节奏 → 谢谢。

规划页数字只来自 collect：`planDefaults` 三档与月拆、`countries` 诊断出加/守/砍、`spendByChannel` 出本期类型占比。`narrative.plan` 九章填目标分层、执行要点、路线图；**禁止**为填满版式编造询盘/CPA/行业数。九章缺章标「待业务确认」，不塞通用运营话术。周节奏表是通用巡检，不是本户规划。`narrative.agenda` 可覆盖浏览逻辑四步说明。
