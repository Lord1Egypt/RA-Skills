# Step 2: 红人搜索

## 目标

基于产品分析结果，调用 WotoHub 搜索接口搜索匹配红人博主。

本步骤的核心原则：
- **宿主模型优先**：产品语义、营销意图、搜索策略优先来自加载本 skill 的宿主模型产出的结构化结果
- **执行脚本优先**：payload 编译、API 调用、错误回退、结果整理优先由脚本完成
- **脚本 query/category 推断只作弱 fallback**：默认优先消费宿主模型已经给出的结构化 hints；脚本侧 query/category 推断只能在缺少宿主输出时作为弱 fallback，不应成为主路径

字段约定：
- 新接入默认应提供 canonical 字段，如 `hostAnalysis` / `productSummary`
- 历史兼容字段仍可吸收，但不应继续扩散到新示例或新桥接契约
- 如需完整映射，参考 `references/alias-normalization-matrix.md`

---

## 搜索规则

这是当前 skill 最关键的一条规则：

- **用户未提供 token** → 默认调用 `openSearch`
- **用户已提供 token** → 默认切换调用 `clawSearch`

因此：
- 搜索步骤本身**不要求默认先登录**
- 只有在进入发信、收件箱、自动回复等用户态步骤时，才需要鉴权检查

---

## 前置条件

### 无 token 搜索
默认请求头：

```http
Content-Type: application/json
Sourceapp: hub
```

### 有 token 搜索
默认请求头：

```http
Content-Type: application/json
api-key: YOUR_API_KEY
Sourceapp: hub
```

---

## 脚本优先

搜索执行层必须以脚本为主，不要让模型直接充当 API 调用器。

推荐主链路：
1. 宿主模型先产出结构化分析结果 / search strategy
2. `build_search_payload.py` 负责确定性拼装 payload
3. `claw_search.py` 负责调用 API、处理 fallback、整理结果

先构建 payload：

```bash
python3 scripts/build_search_payload.py --query "找美国 TikTok 美妆达人，1万粉以上，有邮箱" --platform tiktok --region us --min-fans 10000 --has-email

> 当前 skill 搜索字段原则：分类走 `blogCateIds`，关键词走 `advancedKeywordList`。
```

再执行搜索：

```bash
# 默认 page-size=50；首次搜索时会提示可调大
# 未提供 token：走 openSearch
python3 scripts/claw_search.py --platform tiktok --page-size 50 --has-email

# 已提供 token：走 clawSearch
python3 scripts/claw_search.py --token YOUR_API_KEY --platform tiktok --page-size 50 --has-email

# 过滤已联系博主（需 token）
python3 scripts/claw_search.py --token YOUR_API_KEY --payload-file /tmp/woto_payload.json --exclude-contacted
```

---

## API

> ⚠️ **所有 API URL 已统一在 `scripts/config.py` 管理，请勿硬编码。**
> 默认直连正式环境；如需特殊调试，只允许通过 `WOTOHUB_BASE_URL` 显式覆盖。

### openSearch（无需登录）
```text
POST {BASE_URL}/search/openSearch
```

### clawSearch（有 token 时优先）
```text
POST {BASE_URL}/search/clawSearch
```

---

## 参数映射

### 常见自然语言 → API 参数

| 用户描述 | API 参数 | 说明 |
|---|---|---|
| 找 TikTok / YouTube / Instagram 博主 | `platform` | 平台映射 |
| 10万粉以上 | `minFansNum: 100000` | 最小粉丝量 |
| 1-10万粉 | `minFansNum: 10000, maxFansNum: 100000` | 粉丝区间 |
| 美国的 | `regionList` | 地区参数；脚本会把国家 code 聚合成所属业务区域锚点 id |
| 平均观看量2000以上 | `viewVolumeCombination` | 观看量筛选 |
| 互动率2%以上 | `minInteractiveRate: 2` | 互动率筛选 |
| 英语博主 | `blogLangs: ["en"]` | 语言筛选 |
| 最近30天有发布 | `searchRecent: "RECENT_30D"` | 发布时间筛选 |
| 按粉丝量排序 | `searchSort: "FANS_NUM", sortOrder: "desc"` | 排序 |
| 有邮箱的 | `hasEmail: true` | 建议开启 |

### `blogLangs` 映射补充

- 语言映射源：`references/language-source.json`
- 常用别名：
  - `中文 / 简体中文 / 中文简体 / 简中` → `zh-cn`
  - `繁体中文 / 中文繁体 / 繁中` → `zh-tw`
  - `Japanese / jp` → `ja`
  - `Korean / kr` → `ko`
  - `Tagalog / Filipino / 菲律宾语` → `tl`
- 构建 payload 时会动态读取映射表，不再只依赖少量硬编码语言

### 历史内容分析

`claw_search.py` 在达人评分时会额外分析历史内容信号：
- 历史带货产品名
- 视频标题 / 描述
- 内容标签
- recentVideos / productList / recentProducts 等字段

输出到：`historyAnalysis`

典型字段：
- `score`：历史内容加分
- `matchedTerms`：命中的搜索关键词
- `contentSamples`：历史标题/描述样本
- `signals`：命中的历史信号说明

这层分析会直接影响：
- 搜索推荐排序
- 后续邀约邮件的 hook / proof 选择

### 详细参考

需要详细映射时，按需读取：

- 地区映射：`references/region-mapping.md`
- 地区源数据：`references/region-source.json`
- 语言映射：`references/language-mapping.md`
- 语言源数据：`references/language-source.json`
- 分类映射：`references/category-mapping.md`
- 分类树：`references/category-tree.md`
- 分类扁平表：`references/category-flat-map.md`
- 完整分类源数据：`references/category-source.json`
- 搜索参数：`references/search-params.md`

---

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `platform` | string | 是 | `tiktok` / `youtube` / `instagram` |
| `blogCateIds` | array | 否 | 分类 ID 数组 |
| `regionList` | array | 否 | 地区列表；格式为 `[{"id": 区域首条记录id, "country": ["国家小写code"]}]` |
| `minFansNum` | number | 否 | 最小粉丝数 |
| `maxFansNum` | number | 否 | 最大粉丝数 |
| `minInteractiveRate` | number | 否 | 最小互动率 |
| `blogLangs` | array | 否 | 语言 |
| `searchSort` | string | 否 | 排序字段 |
| `sortOrder` | string | 否 | `asc` / `desc` |
| `pageNum` | number | 否 | 默认 1 |
| `pageSize` | number | 否 | `build_search_payload.py` / `run_campaign.py` 默认 50；`claw_search.py` CLI 默认 20；campaign cycle 默认 10 |
| `hasEmail` | boolean | 否 | 建议默认 `true` |

---

## 输出建议

```text
共找到 X 位匹配红人

1. 昵称：xxx
   平台：TikTok
   地区：美国
   粉丝：xx万
   平均观看：xxxx
   互动率：x.x%
   匹配分：xx（高匹配）
   历史内容：命中 skincare / cleanser，近期有相关产品或视频描述
   主页链接：https://www.tiktok.com/@xxx          ← link
   WotoHub分析：https://www.wotohub.com/kocNewDetail?id=UCxxx  ← wotohubLink
   博主ID：UCxxx                                      ← besId
```

> 注意：当前默认值按入口区分：`claw_search.py` CLI 默认 `page-size=20`，`build_search_payload.py` / `run_campaign.py` 主路径默认 `page-size=50`，campaign cycle 默认 `page-size=10` 用于稳定定时运行。需要更高召回时，建议显式调到 50 或 100。
