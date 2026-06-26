# 各媒体开户

> 网页链接：`https://www.siluzan.com/v3/foreign_trade/tso/accountOpeningHistory?tso=%2Fv3umijs%2Ftso%2FaccountOpeningHistory`  
> 多命令串联见 `references/core/workflows.md` § 流程一。

## 首次响应硬规范（必读）

用户提出开户（或本轮对话**首次**进入开户话题）时，Agent **必须先输出完整必填清单**，再收集资料或执行 CLI。**禁止**在未列清单的情况下直接 `open-account …` 或只问一两个字段。

| 用户说法                                | 首次回复必须包含                                                          |
| --------------------------------------- | ------------------------------------------------------------------------- |
| 未指明媒体 / 「开个户」/ 「各平台开户」 | 下文 **§ 全平台必填总览** 六张表（或等价完整列表）                        |
| 已指明单一媒体（如「Google 开户」）     | 该媒体 **§ 必填字段** 表 + 辅助查询命令（若有）+ 资料类说明（执照路径等） |
| 多媒体同时开                            | 每个目标媒体各一张必填表，**禁止**混用字段                                |

清单须写清：**业务含义**、**CLI 选项名**、**格式/枚举**、**是否需本地文件路径**。用户补齐后再确认并提交；写入前仍须用户确认（见 `references/core/agent-conventions.md`）。

只有Google开户时需要询问用户账户币种（USD|CNY）,其他广告平台禁止询问用户币种因为都仅支持USD一种

不确定字段时：先 `siluzan-tso open-account <subcommand> -h`，再以本文件与 CLI 为准，勿猜。

---

## Agent 注意

- 始终用非交互 `open-account <media> ...`。
- **Meta/Facebook 开户**无表单提交命令，使用 `open-account meta` 获取官方 OE 链接交给用户在浏览器完成。
- 各媒体所需资料和参数**完全不同**，不要混用。
- 提交后轮询：`account-history -m <Media>`；通过后 `list-accounts -m <Media>`。
- 充值激活**必须在网页**完成（见 `references/accounts/finance.md`）。

---

## 全平台必填总览

> 与 `siluzan-tso open-account <media> -h` 的 `requiredOption` 对齐；可选字段见各媒体 §。

### Google（`open-account google`，无需图片）

| 业务项   | CLI 选项           | 说明                                        |
| -------- | ------------------ | ------------------------------------------- |
| 公司名称 | `--company`        | 用于匹配/创建广告主组                       |
| 推广链接 | `--promotion-link` | 可只写域名，CLI 补 `https://`               |
| 推广类型 | `--promotion-type` | `b2b` \| `b2c` \| `app`                     |
| 账户名称 | `--account-name`   | 建议 ≤22 字                                 |
| 币种     | `--currency`       | `USD` \| `CNY`                              |
| 时区     | `--timezone`       | IANA；列表：`open-account google-timezones` |
| 邀请邮箱 | `--invite-email`   | 账户邀请发往此邮箱                          |

### TikTok（`open-account tiktok`，需营业执照图片）

| 业务项       | CLI 选项                      | 说明                                                     |
| ------------ | ----------------------------- | -------------------------------------------------------- |
| 公司名称     | `--company`                   | 无 OCR，须用户手填                                       |
| 账户名称     | `--account-name`              |                                                          |
| 时区         | `--timezone`                  | 列表：`open-account tiktok-timezones`                    |
| 行业 ID      | `--industry-id`               | **叶子节点**数字；列表：`open-account tiktok-industries` |
| 注册地       | `--registered-area`           | 国家代码如 `CN`；列表：`open-account tiktok-areas`       |
| 推广链接     | `--promotion-link`            |                                                          |
| 执照编号     | `--license-no`                | 统一社会信用代码                                         |
| 执照图片     | `--license-file`              | 本地 JPG/PNG 路径                                        |
| 法人姓名     | `--representative-name`       | CLI 必填                                                 |
| 法人身份证   | `--representative-id`         | CLI 必填                                                 |
| 法人银联账号 | `--unionpay-account`          | CLI 必填                                                 |
| 法人手机     | `--representative-phone`      | CLI 必填                                                 |
| 币种         | 只支持USD， 无需 `--currency` |

### Yandex（`open-account yandex`，无需图片）

| 业务项       | CLI 选项    | 说明                     |
| ------------ | ----------- | ------------------------ |
| 公司名称     | `--company` |                          |
| 联系邮箱     | `--email`   |                          |
| 税号 TIN/INN | `--tin`     | 类型固定 `FOREIGN_LEGAL` |

### BingV2（`open-account bing`，需营业执照图片）

| 业务项     | CLI 选项             | 说明                                                                     |
| ---------- | -------------------- | ------------------------------------------------------------------------ |
| 直接/代理  | `--pattern`          | `Direct` \| `Agency`                                                     |
| 广告主全称 | `--advertiser-name`  | 用于匹配/创建广告主组                                                    |
| 公司简称   | `--name-short`       |                                                                          |
| 开户名称   | `--name-remark-list` | 账户显示名                                                               |
| 省份       | `--province`         |                                                                          |
| 城市       | `--city`             |                                                                          |
| 详细地址   | `--address`          |                                                                          |
| 邮编       | `--postcode`         |                                                                          |
| 行业       | `--trade-id`         | 先 `bing-industries`；传输出 **id**（与网页下拉 value 一致），勿猜中文名 |
| 推广链接   | `--promotion-link`   |                                                                          |
| 执照图片   | `--license-file`     | JPG/PNG/PDF 本地路径                                                     |

### Kwai（`open-account kwai`，需营业执照图片）

| 业务项        | CLI 选项             | 说明                                                                                       |
| ------------- | -------------------- | ------------------------------------------------------------------------------------------ |
| 营业执照号    | `--licence-id`       |                                                                                            |
| 注册国家      | `--licence-country`  | 如 `CN`                                                                                    |
| 注册地址      | `--licence-location` | 省市区详细地址                                                                             |
| 营业范围      | `--business-scope`   |                                                                                            |
| 产品/品牌名   | `--product`          |                                                                                            |
| 账户类型      | `--ad-type`          | `1` 效果 / `2` 品牌                                                                        |
| 产品网址      | `--product-url`      |                                                                                            |
| 执照/证件类型 | `--licence-id-type`  | `1` 统一社会信用代码 / `2` DUNS / `3` CNPJ（与网页下拉 value 一致；**勿用** `ENTERPRISE`） |
| 账户名称      | `--account-name`     |                                                                                            |
| 公司主体名    | `--company-name`     |                                                                                            |
| 一级行业 ID   | `--industry-id1`     |                                                                                            |
| 二级行业 ID   | `--industry-id2`     |                                                                                            |
| 有效期类型    | `--expire-type`      | `1` 有限期（须 `--expire-at`）/ `2` 长期                                                   |
| 投放地区      | `--target-country`   | ISO 如 `US`                                                                                |
| 执照图片      | `--license-file`     | 本地路径                                                                                   |

### MetaAd（`open-account meta`）

| 业务项     | 说明                                         |
| ---------- | -------------------------------------------- |
| 用户侧资料 | 在 Meta 官方 OE 网页填写；CLI **无**表单字段 |

---

## Google

**必填**：见上表 § Google；字段语义见 `references/accounts/open-account-google-ui.md`。

**Google 字段说明**：`references/accounts/open-account-google-ui.md`

**常用时区**（完整：`siluzan-tso open-account google-timezones`）：

| Code                  | 含义     |
| --------------------- | -------- |
| `Asia/Shanghai`       | CNY 默认 |
| `Asia/Hong_Kong`      | USD 默认 |
| `America/New_York`    | 美东     |
| `America/Los_Angeles` | 美西     |
| `Europe/London`       | 伦敦     |

```bash
siluzan-tso open-account google \
  --company "Brand A Inc." \
  --promotion-link "https://www.brand-a.com" \
  --promotion-type b2c \
  --account-name "品牌A美国推广账户" \
  --currency USD \
  --timezone "America/New_York" \
  --invite-email "marketing@brand-a.com"

siluzan-tso account-history -m Google
siluzan-tso list-accounts -m Google
```

---

## TikTok

**必填**：见上表 § TikTok。CLI 不做执照 OCR；法人银联四项在 CLI 中为必填。

**辅助查询**（行业/注册地/时区不确定时先跑）：

```bash
siluzan-tso open-account tiktok-areas --keyword China
siluzan-tso open-account tiktok-industries --keyword "电商"
siluzan-tso open-account tiktok-timezones --keyword Shanghai
```

```bash
siluzan-tso open-account tiktok \
  --company "Brand A Inc." \
  --account-name "品牌A TikTok账户" \
  --timezone "Asia/Shanghai" \
  --industry-id <叶子节点 ID> \
  --registered-area CN \
  --promotion-link "https://www.brand-a.com" \
  --license-no "91440300XXXXXXXXXX" \
  --license-file "/path/to/license.jpg" \
  --representative-name "张三" \
  --representative-id "440300XXXXXXXXXXXXXXXXX" \
  --unionpay-account "6222XXXXXXXXXXXX" \
  --representative-phone "13800138000"

siluzan-tso account-history -m TikTok
```

---

## Yandex

**必填**：见上表 § Yandex（仅三项，与网页 v2 表单一致）。

```bash
siluzan-tso open-account yandex \
  --company "Brand A Inc." \
  --email "contact@brand-a.com" \
  --tin "XXXXXXXXXX"

siluzan-tso account-history -m Yandex
```

---

## BingV2

**必填**：见上表 § BingV2。

> **行业（Agent 硬规范）**：与网页一致，数据源为 `TradeList` + `BingTradeList/Read` 合并后的**二级**选项。必须先执行 `open-account bing-industries`（`--keyword` 可匹配中文行业名、分组名、英文 name 或 id），从输出取 **`id`** 填入 `--trade-id`。**禁止**凭记忆写行业名或编造「一级/二级」拼接字符串。

```bash
siluzan-tso open-account bing-industries --keyword "科技"

siluzan-tso open-account bing \
  --pattern Direct \
  --advertiser-name "深圳XX科技有限公司" \
  --name-short "XX科技" \
  --name-remark-list "XX科技-推广户" \
  --province "广东省" \
  --city "深圳市" \
  --address "南山区科技园XX路XX号" \
  --postcode "518000" \
  --promotion-link "https://www.brand-a.com" \
  --trade-id "<bing-industries 输出的 id>" \
  --license-file "/path/to/license.jpg"

siluzan-tso account-history -m BingV2
```

---

## Kwai

**必填**：见上表 § Kwai。

> **双上传**：CLI 先上传附件得 `imageId`（更新广告主组 MAG），再上传 Kwai 资质得 `blobstoreKey`（写入 `mainCertPhotos`）。二者不可混用。
>
> **落库确认**：`AddKwaiAccount` 返回 HTTP 202（异步受理）。CLI 提交后会轮询 `account-history` 同源接口，**仅在查到对应 `--account-name` 后才报成功**；否则 exit 1 并提示核对 `--licence-id-type` 等字段。

```bash
siluzan-tso open-account kwai \
  --company-name "深圳XX科技有限公司" \
  --licence-id "91440300XXXXXXXXXX" \
  --licence-country CN \
  --licence-location "广东省深圳市南山区XX路XX号" \
  --business-scope "电商零售" \
  --product "品牌A" \
  --ad-type 1 \
  --product-url "https://www.brand-a.com" \
  --licence-id-type 1 \
  --account-name "品牌A Kwai账户" \
  --industry-id1 "1234" \
  --industry-id2 "5678" \
  --expire-type 2 \
  --target-country US \
  --license-file "/path/to/license.jpg"

siluzan-tso account-history -m Kwai
```

---

## MetaAd（Facebook / Meta）

**流程**：与 TSO 网页「申请开户」相同——调用 `GetOpenAccountLink` 得到 **Meta 官方 OE 动态链接**（有时效，不可写死 URL），用户在浏览器完成开户。

**所需**：已配置 `siluzan-tso` 鉴权（`config show` 或 `SILUZAN_API_KEY`）。

```bash
# 获取链接（stdout 打印 URL，Agent 可直接转给用户）
siluzan-tso open-account meta

# 结构化输出（含 openAccountUrl 字段）
siluzan-tso open-account meta --json-out ./snap-meta-open

# 本机尝试自动打开浏览器（可选）
siluzan-tso open-account meta --open-browser
```

提交后查进度：

```bash
siluzan-tso account-history -m MetaAd
siluzan-tso list-accounts -m MetaAd
```

网页入口（需登录）：账户管理 `…/manageAccounts?mediaType=MetaAd`；开户记录 `…/accountOpeningHistory?mediaType=Meta`（CLI 打印链接时会从 `MetaAd` 自动映射为 `Meta`，与网页 Tab 一致）。

---

## 审核结果

| 状态   | 含义         | 下一步                                                                                                                                                  |
| ------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 审核中 | 等待媒体审核 | 继续 `account-history` 轮询                                                                                                                             |
| 已通过 | 账户可用     | `list-accounts` 确认 + 按 `finance.md` 打开对应媒体充值页（传统充值/月结充值仅 Google/TikTok/Meta/Microsoft 有页面；Kwai、Yandex 当前没有对应充值界面） |
| 已拒绝 | 资料问题     | 查看拒绝原因，修正后重新提交                                                                                                                            |

完整参数：`siluzan-tso open-account <subcommand> -h`
