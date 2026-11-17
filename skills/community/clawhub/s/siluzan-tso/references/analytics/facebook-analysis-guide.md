# Facebook Ads 账户分析 — 字段与撰写指南

> 拉数命令见 `account-analytics.md` § Meta / Facebook Ads。周期报告纲要见 `report-templates/meta-period-report.md`；诊断见 `report-templates/meta-account-diagnosis-report.md`。

---

## 周期报告标准流程（默认 HTML）

用户要 **Facebook / Meta 分析报告**且**未指定交付格式**时，按以下四步执行：

| 步骤           | 说明                                                                                                                                   |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 拉数**    | `facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb --sections overview,daily,country,campaigns,audience`（省略 `--sections` 会拉全部 10 维） |
| **2. 分析**    | Agent 用脚本读 `report-manifest-<id>.json` 与各 `<section>-<id>.json`，完成聚合与洞察（禁止 Read 业务 JSON、禁止对话里手填数）         |
| **3. 写 JSON** | 产出 `meta-period-report.json`（`fourQuestions` 4 问 + `recommendations` ≥3 卡 + `sections.*.insight`；数值由 render 从快照覆盖） |
| **4. 渲染**    | `facebook-analysis render --data ./meta-period-report.json --snapshot-dir ./snap-fb --out ./meta-period-report.html`                   |

**禁止**：跳过步骤 3/4 直接交付 Markdown；禁止 Agent 手写 HTML。

### Excel 分支（仅用户指定时）

用户明确要求 **Excel / xlsx / 表格** 时：步骤 1～3 相同；步骤 4 改为 `facebook-analysis render --format xlsx`（版式见 `meta-period-report-excel.md`）。同时要两种格式：`--format html,xlsx`。

---

## 与 Google 周期报告的能力对照

| Google 默认/常见维度                                                              | Facebook 对应                   | CLI        | 说明                                                                                           |
| --------------------------------------------------------------------------------- | ------------------------------- | ---------- | ---------------------------------------------------------------------------------------------- |
| 执行摘要 `overview`                                                               | ✅ 本期/上期环比                | `overview` | 上一周期由后端自动算，勿再拉第二次                                                             |
| 每日趋势 `daily-metrics`                                                          | ✅ 按日                         | `daily`    | `DailySectionData`；别名 `daily-metrics`；不补空日                                             |
| 月度汇总 `dimension-summary`                                                      | ⚠️ 用 `overview` 单周期汇总代替 | `overview` | 仅 currentPeriod 即全区间汇总                                                                  |
| 系列 `campaigns`                                                                  | ✅ 独立系列维                   | `campaigns` | `CampaignSectionData`（`campaignId` / `campaignName` / `objective`）；广告组另拉 `ad-sets`   |
| 设备 `devices`                                                                    | ✅ 设备 + ⚠️ 平台×版位          | `device` / `platform` | 真设备维用 `device`；`devices` 仍是 platform 旧别名；版位看 `platform`                         |
| 地域 `geographic`                                                                 | ✅ 国家                         | `country`  | 可选 `--limit N`                                                                               |
| 关键词 `keywords`                                                                 | ❌ 无                           | —          | 非搜索广告；章节写「不适用」                                                                   |
| 受众 `audience`                                                                   | ⚠️ 年龄×性别                    | `audience` | 无兴趣/自定义受众列表                                                                          |
| 广告创意 `ads`                                                                    | ✅ 创意+文案+缩略图             | `creative` | 一行 = ad + creative                                                                           |
| 图片/视频素材 `materials`                                                         | ⚠️ DC 素材                      | `material` | 标准账户为空，用 `creative`                                                                    |
| 搜索词 / 附加信息 / 落地页 / 黄金账户 / 质量分 / 转化动作列表 / 系列类型 / 按小时 | ❌ 无                           | —          | 诊断模板中标注「Facebook 无此数据」                                                            |

**`--sections` 别名**：`daily-metrics`→`daily`，`campaign`→`campaigns`，`geographic`→`country`，`devices`→`platform`（旧），`ads`→`creative`，`materials`→`material`。`campaigns` 现为独立 Section，不再映射到 `ad-sets`。

---

## 公共指标（JSON camelCase）

### 基础

| 字段                | 撰写展示                                          |
| ------------------- | ------------------------------------------------- |
| `impressions`       | 展示（整数）                                      |
| `clicks`            | 点击                                              |
| `spend`             | 花费（账户币种，**非** micros）                   |
| `ctr`               | 点击率：**小数**，展示时 ×100 加 `%`（0.05 → 5%） |
| `averageCpc`        | 平均 CPC                                          |
| `conversions`       | 业务转化次数（lead/purchase/messaging 等汇总）    |
| `costPerConversion` | CPA                                               |
| `conversionRate`    | CVR（小数，×100 为 %）                            |

### Facebook 扩展

| 字段                 | 撰写展示                |
| -------------------- | ----------------------- |
| `reach`              | 覆盖人数                |
| `frequency`          | 频次；>3 可提示创意疲劳 |
| `resultType`         | 结果类型（如 `lead`）   |
| `attributionSetting` | 归因（如 `7d_click`）   |
| `results`            | 对齐 Meta「结果」列     |
| `costPerResult`      | 单次成效费用            |

### 口径（必读）

- **对客户/对齐后台**：优先 `results`、`costPerResult`。
- **对内诊断**：可同时列 `conversions`、`costPerConversion`。
- **禁止**：将 `creative` / `ad-sets` 各行 `results` 简单加总后与 `overview.currentPeriod.results` 对比（见 API 附录 B）。
- **`material` 行**：无 `results` / `costPerResult`，只看 spend、转化、CTR、reach。

---

## PlatformSectionData 字段（平台 / 版位）

后端按 Meta `publisher_platform,platform_position` breakdown 拆分（2026-06 起）。`networks[]` 每行：

| 字段                | 含义                                    | 示例                                                            |
| ------------------- | --------------------------------------- | --------------------------------------------------------------- |
| `publisherPlatform` | 投放平台（Meta `publisher_platform`）   | `facebook`、`instagram`、`audience_network`                     |
| `platformPosition`  | 版位（Meta `platform_position`）        | `feed`、`facebook_reels`、`instagram_stories`、`instream_video` |
| `network`           | 兼容旧前端，**等于 `platformPosition`** | 勿单独当作「平台」列使用                                        |

**撰写表格建议列**：投放平台 | 版位 | 展示 | 花费 | 结果 | 单次成效费用。

**汇总规则**：

- 按**平台**占比：对 `publisherPlatform` 聚合 `spend` / `results`。
- 按**版位**占比：对 `platformPosition` 聚合（跨平台合并同名版位时须注明）。
- 精细诊断：保留 `publisherPlatform` + `platformPosition` 组合行（如 `instagram` + `feed` vs `facebook` + `feed`）。

---

## 各 Section 文件与章节要点

| section    | 落盘文件             | 根字段                                 | 报告章节要点                                                                                                                                                                                                                |
| ---------- | -------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `overview` | `overview-<id>.json` | `currentPeriod`, `previousPeriod`      | 环比表：消耗、展示、点击、CTR、CPC、转化、CPA、结果、单次成效、reach、frequency；注明 `resultType` / `attributionSetting`                                                                                                   |
| `daily`    | `daily-<id>.json`    | `days[]`                               | 按日行，`date` 升序，不补空日                                                                                                                                                                                               |
| `campaigns`| `campaigns-<id>.json`| `campaigns[]`                          | 系列级 spend / results / CPL；含 `campaignId` `campaignName` `objective`                                                                                                                                                    |
| `ad-sets`  | `ad-sets-<id>.json`  | `adGroups[]`                           | Top 组 by spend；`spendPercentage`；按 `campaignName` 归并；高消耗低结果组                                                                                                                                                  |
| `platform` | `platform-<id>.json` | `networks[]`                           | **两列维度**：`publisherPlatform`（投放平台）+ `platformPosition`（版位）；`network` 与 `platformPosition` 同值（兼容旧版）。同版位名可能跨平台出现（如 facebook/instagram 均有 `feed`），**禁止**仅用 `network` 当平台汇总 |
| `country`  | `country-<id>.json`  | `countries[]`                          | Top 国家；`countryOrRegion` 为展示名                                                                                                                                                                                        |
| `device`   | `device-<id>.json`   | `devices[]`                            | `devicePlatform`：desktop / mobile / unknown                                                                                                                                                                                |
| `audience` | `audience-<id>.json` | `audiences[]`                          | 年龄×性别矩阵；高/低效人群段                                                                                                                                                                                                |
| `creative` | `creative-<id>.json` | `creatives[]`                          | 按 `creativeType` 汇总；Top 创意表（adName、title、spend、results、costPerResult）                                                                                                                                          |
| `material` | `material-<id>.json` | `materials[]`, `dataSource`, `message` | 仅 `dataSource===meta_asset_breakdown` 且有条目时写章节；否则一句说明                                                                                                                                                       |

---

## 周期报告默认拉数（步骤 1）

```bash
mkdir -p ./snap-fb
siluzan-tso facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb \
  --sections overview,daily,country,campaigns,audience
```

叙事结构与 Agent JSON：**`meta-period-report.md`** + **`assets/meta-period-report.schema.json`**。  
仅 Excel 交付时再读 **`report-templates/meta-period-report-excel.md`**，并用 `render --format xlsx`。

可选追加：`--sections ad-sets,platform,device,creative,material`。

国家 Top 10：整次命令加 `--limit 10`（仅 `country` 请求带 limit）。

---

## HTML 终稿渲染（步骤 4 · 默认交付）

完成步骤 2（分析）与步骤 3（`meta-period-report.json`）后执行，**禁止手写 HTML**。  
`render` 为独立子命令，**不需要** `-a` / `--json-out`（与批拉命令分离）：

```bash
siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --out ./meta-period-report.html
```

- `--snapshot-dir`：与拉数 `--json-out` 同目录；CLI 自动合并 KPI、日/国家/系列/受众表格与图表。
- 模板：`report-templates/meta-period-report.html`（浅色运营版式 + ECharts）。
- JSON 字段说明：见 `report-templates/meta-period-report.md`。
- 用户要表格：同一命令加 `--format xlsx`。

---

## 优化建议撰写清单（不额外拉数）

**必读** `assets/meta-period-report-rules.md`。每条建议须**引用当次数字** + **可执行动作**。

| JSON 字段 | 要求 |
| --------- | ---- |
| `fourQuestions` | 固定 4 问（钱花得值不值 / 谁真的想买 / 广告还新鲜吗 / 用户为什么不留资） |
| `recommendations` | ≥3 张卡，`title` + `tag` + `items[]` |
| `sections.*.insight` | daily / country / campaigns / audience 各有 `analysis[]` + `advice[]` |

数据驱动抓手：国家 CPL、按日零转化、系列是否共用学习池、年龄×性别线索质量。无关键词维 — 一句「接口未提供」，不编造。

---

## 辅助命令（非报告 Section）

| 意图         | CLI                                                                     |
| ------------ | ----------------------------------------------------------------------- |
| 账户列表     | `list-accounts -m MetaAd -k <id> --json-out <dir>`                      |
| 余额（若需） | `balance` / `stats`（口径与报告 spend 可能不同，须标注来源）            |
| 当天/小时巡检 | `facebook-analysis account-status` / `campaign-entities` / `adset-entities` / `ad-entities` / `insights`（见 `hosted-automation-facebook.md`） |
| 遗留仅总览   | `report meta-overview`（`MetaAd` 路径，不推荐替代 `facebook-analysis`） |
