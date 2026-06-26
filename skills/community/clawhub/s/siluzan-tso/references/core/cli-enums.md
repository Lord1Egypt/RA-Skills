# CLI 枚举速查

> **Agent**：不确定 `--sections`、`-m`、`--operator` 等合法值时，**Read 本文件**（按章节）或执行：
> `siluzan-tso reference enums`（Markdown） / `siluzan-tso reference enums --json`（机器可读）。
> 各功能 reference 只保留业务说明；枚举与 CLI 校验**以此文件为准**（与源码同源）。

### 媒体类型 `-m` / `--media`（多数命令）

| 命令                                                                      | 选项        | 合法值                                                 |
| ------------------------------------------------------------------------- | ----------- | ------------------------------------------------------ |
| list-accounts, stats, balance, account-history, open-account, transfer, … | -m, --media | Google \| TikTok \| Yandex \| MetaAd \| BingV2 \| Kwai |

> 区分大小写；Meta 广告账户用 MetaAd，不是 Facebook。

### 媒体类型（仅 forewarning）

| 命令                                 | 选项        | 合法值           |
| ------------------------------------ | ----------- | ---------------- |
| forewarning list, create, records, … | -m, --media | Google \| TikTok |

### `google-analysis --sections` 维度（25）

| 命令                                       | 选项       | 合法值                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| google-analysis, google-analysis-batch run | --sections | overview \| keywords \| search-terms \| campaigns \| campaign-hour \| ads \| extensions \| devices \| geographic \| geo-matched \| campaign-geo \| campaign-geo-matched \| campaign-device \| audience \| asset-images \| videos \| materials \| resource-counts \| conversion-actions \| daily-metrics \| gold-account \| ads-index \| final-urls \| dimension-summary \| campaign-types |

> 逗号分隔；省略=全部。`final-urls`、`campaign-types` 不传日期。

### `google-analysis --level`（extensions 维度）

| 命令                                  | 选项    | 合法值                          |
| ------------------------------------- | ------- | ------------------------------- |
| google-analysis --sections extensions | --level | Account \| Campaign \| Ad Group |

### `google-analysis --audience-type`（audience 维度）

| 命令                                | 选项            | 合法值                       |
| ----------------------------------- | --------------- | ---------------------------- |
| google-analysis --sections audience | --audience-type | SystemDefined \| UserDefined |

### `facebook-analysis --sections` 维度（7）

| 命令              | 选项       | 合法值                                                                         |
| ----------------- | ---------- | ------------------------------------------------------------------------------ |
| facebook-analysis | --sections | overview \| ad-sets \| platform \| country \| audience \| creative \| material |

> 默认周期报告：overview,ad-sets,platform,country,audience,creative。

### `facebook-analysis --sections` Google 别名

| 命令              | 选项               | 合法值 |
| ----------------- | ------------------ | ------ |
| facebook-analysis | --sections（别名） | —      |

> 解析后映射到左侧 canonical 名。

**别名**：`campaigns` → `ad-sets`；`ad-groups` → `ad-sets`；`geographic` → `country`；`geo` → `country`；`devices` → `platform`；`network` → `platform`；`networks` → `platform`；`ads` → `creative`；`materials` → `material`；`asset-images` → `material`；`videos` → `material`

### `ad extension * --level`

| 命令                                       | 选项          | 合法值                                                                             |
| ------------------------------------------ | ------------- | ---------------------------------------------------------------------------------- |
| ad extension sitelink, callout, snippet, … | --level       | Account \| Campaign \| AdGroup                                                     |
| ad extension list                          | --type        | SITELINK \| CALL \| CALLOUT \| STRUCTURED_SNIPPET \| LEAD_FORM \| BUSINESS_MESSAGE |
| ad extension lead-form / update            | --config-file | JSON（见 `assets/pmax-lead-form-template.json`）                                   |
| ad extension whatsapp / update             | --config-file | JSON（见 `assets/pmax-whatsapp-template.json`）                                    |

### 搜索系列 `BiddingStrategyTypeV2`

| 命令                                                 | 选项                           | 合法值                                                                                                       |
| ---------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| ad campaign-create, campaign-validate（config JSON） | campaign.BiddingStrategyTypeV2 | TARGET_SPEND \| MANUAL_CPC \| TARGET_CPA \| TARGET_ROAS \| MAXIMIZE_CONVERSIONS \| MAXIMIZE_CONVERSION_VALUE |

### 系列 `ChannelTypeV2`

| 命令                                  | 选项                   | 合法值                                                  |
| ------------------------------------- | ---------------------- | ------------------------------------------------------- |
| ad campaign-create, campaign-validate | campaign.ChannelTypeV2 | SEARCH \| DISPLAY \| VIDEO \| SHOPPING \| MULTI_CHANNEL |

### 系列 `StatusV2`

| 命令                                  | 选项              | 合法值            |
| ------------------------------------- | ----------------- | ----------------- |
| ad campaign-create, campaign-validate | campaign.StatusV2 | Enabled \| Paused |

### 预算投放 `BudgetBudgetDeliveryMethodV2`

| 命令                                  | 选项                                  | 合法值                                            |
| ------------------------------------- | ------------------------------------- | ------------------------------------------------- |
| ad campaign-create, campaign-validate | campaign.BudgetBudgetDeliveryMethodV2 | STANDARD \| ACCELERATED \| UNSPECIFIED \| UNKNOWN |

### PMax `BiddingStrategyTypeV2`

| 命令                          | 选项                           | 合法值                                                                         |
| ----------------------------- | ------------------------------ | ------------------------------------------------------------------------------ |
| ad pmax-create, pmax-validate | campaign.BiddingStrategyTypeV2 | MAXIMIZE_CONVERSIONS \| MAXIMIZE_CONVERSION_VALUE \| TARGET_CPA \| TARGET_ROAS |

### 预警比较运算符

| 命令               | 选项       | 合法值                                                     |
| ------------------ | ---------- | ---------------------------------------------------------- |
| forewarning create | --operator | GREATER_EQUALS \| GREATER \| LESS_EQUALS \| LESS \| EQUALS |

### 开户历史状态筛选

| 命令            | 选项                          | 合法值                                    |
| --------------- | ----------------------------- | ----------------------------------------- |
| account-history | --status（mediaAccountState） | Created \| Approved \| Denied \| Inactive |

> Google 默认含 Inactive；其他媒体默认 Created,Approved,Denied。

### 线索表单媒体

| 命令 | 选项        | 合法值         |
| ---- | ----------- | -------------- |
| clue | -m, --media | TikTok \| Meta |

### 网站诊断模块 status

| 命令                                  | 选项             | 合法值                                                               |
| ------------------------------------- | ---------------- | -------------------------------------------------------------------- |
| website-diagnosis collect（响应字段） | modules[].status | Excellent \| Good \| Normal \| Poor \| Full \| NeedImprove \| Absent |

> 撰写报告时转中文展示；细则见 assets/website-diagnosis-rules.md。

### Kwai 开户 `--licence-id-type`（`open-account kwai`）

| 命令              | 选项              | 合法值                                       |
| ----------------- | ----------------- | -------------------------------------------- |
| open-account kwai | --licence-id-type | `1` 统一社会信用代码 \| `2` DUNS \| `3` CNPJ |

> 与网页 `KwaiOpenAnAccount.vue` 的 `licenseCodeTypeOptions` **value** 一致（数字字符串）。**勿用** `ENTERPRISE` / `INDIVIDUAL`（旧文档误写；传入 `ENTERPRISE` 时 CLI 会警告并映射为 `1`）。
