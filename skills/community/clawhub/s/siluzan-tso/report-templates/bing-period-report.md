# Bing（Microsoft Advertising / BingV2）— 账户分析报告（模板纲要）

> 统计区间：`{startDate}` ~ `{endDate}`（**不可包含今天或昨天**，见下文）  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

数据块：总览、设备、地域、受众（年龄/性别）、系列、广告组、广告、关键词、搜索字词。

---

## 日期规则（必读）

- Bing 接口**无法**拉取过新的数据；时间范围内**任意一天**若为**今天**或**昨天**，请求会失败。
- **CLI**：`--start` / `--end` 须**同传或同省略**；省略时默认**截至前天**的近 7 天（与 `report bing-*` 实现一致）。
- 自选区间时请确保结束日 ≤ **前天**。

---

## 1. 执行摘要（总览）

- **CLI**：`siluzan-tso report bing-overview -a <mediaCustomerId> [--start … --end …] --json-out <dir>`

## 2. 设备与地域

- 设备：`report bing-device` → `DeviceSectionData`
- 地域：`report bing-geographic` → `GeographicSectionData`（响应中常见 `countries` 等字段，**以实际 JSON 为准**）

## 3. 受众

- 年龄：`report bing-age-audience` → `AgeAudienceData`
- 性别：`report bing-gender-audience` → `GenderAudienceData`
- 合并输出：`report bing-audience-merged`（**固定输出合并 JSON**，含年龄+性别）

## 4. 广告结构

- 系列：`report bing-campaigns` → `CampaignReport`
- 广告组：`report bing-ad-groups` → `AdGroupReport`
- 广告：`report bing-ads` → `AdReport`

## 5. 关键词与搜索字词

- 关键词：`report bing-keywords` → `KeywordReport`，Query 含 `limit`（默认 **100**）、`orderByCost=true`
- 搜索字词：`report bing-search-terms` → `SearchQueryReport`，参数同上

## 6. 附录

- 鉴权：与 TSO 其他接口相同（`config show` 中 `tsoApiBaseUrl` / Token）。
- 与 steward「优化报告」区别：见 `meta-period-report.md` 末节；此处为**实时分析 JSON**。

---

### CLI 速查表

| 数据块   | 子命令                        |
| -------- | ----------------------------- |
| 总览     | `report bing-overview`        |
| 设备     | `report bing-device`          |
| 地域     | `report bing-geographic`      |
| 年龄受众 | `report bing-age-audience`    |
| 性别受众 | `report bing-gender-audience` |
| 受众合并 | `report bing-audience-merged` |
| 系列     | `report bing-campaigns`       |
| 广告组   | `report bing-ad-groups`       |
| 广告     | `report bing-ads`             |
| 关键词   | `report bing-keywords`        |
| 搜索字词 | `report bing-search-terms`    |
