# 各媒体开户

> 网页链接：`https://www.siluzan.com/v3/foreign_trade/tso/accountOpeningHistory?tso=%2Fv3umijs%2Ftso%2FaccountOpeningHistory`  
> 多命令串联见 `references/core/workflows.md` § 流程一。

## Contents

- 首次响应硬规范（必读）
- Agent 注意
- 全平台必填总览
- Google
- TikTok
- Yandex
- BingV2
- MetaAd（Facebook / Meta）
- 审核结果

---

## 首次响应硬规范（必读）

用户提出开户（或本轮对话**首次**进入开户话题）时，Agent **必须先输出完整必填清单**，再收集资料或执行 CLI。**禁止**在未列清单的情况下直接 `open-account …` 或只问一两个字段。

| 用户说法                                | 首次回复必须包含                                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 未指明媒体 / 「开个户」/ 「各平台开户」 | 下文 **§ 全平台必填总览** 五媒体的**业务项 + 说明**（或等价完整列表）                                     |
| 已指明单一媒体（如「Google 开户」）     | 该媒体 **业务项 + 说明**（格式/枚举、是否需本地文件）+ 资料类说明（执照路径等）；时区等可用业务语言辅助表 |
| 多媒体同时开                            | 每个目标媒体各一份业务清单，**禁止**混用字段                                                              |

**对用户清单只写**：业务项含义、格式/枚举（如「b2b / b2c / app」）、是否需本地文件路径。  
**禁止**在对用户回复中出现：`--flag`、CLI 选项名、命令行参数列、`siluzan-tso …` 完整命令块、本文件「Agent 参数」列内容。  
CLI 参数仅供 Agent **内部**组命令使用（见下表第三列）。用户补齐后再确认并提交；写入前仍须用户确认（见 `references/core/agent-conventions.md`）。

只有 Google 开户时需要询问用户账户币种（USD|CNY）；其他广告平台禁止询问币种（均仅支持 USD）。

不确定字段时：先 `siluzan-tso open-account <subcommand> -h`，再以本文件与 CLI 为准，勿猜。

---

## Agent 注意

- 始终用非交互 `open-account <media> ...`。
- **对用户永不展示 CLI 参数名 / 命令行选项**（见上节）；示例 bash 块仅供 Agent 执行参考，勿原样贴进对话。
- **Meta/Facebook 开户**无表单提交命令，使用 `open-account meta` 获取官方 OE 链接交给用户在浏览器完成。
- 各媒体所需资料和参数**完全不同**，不要混用。
- 提交后轮询：`account-history -m <Media>`；通过后 `list-accounts -m <Media>`。
- 充值激活**必须在网页**完成（见 `references/accounts/finance.md`）。

---

## 全平台必填总览

> 与 `siluzan-tso open-account <media> -h` 的 `requiredOption` 对齐；可选字段见各媒体 §。  
> 表中 **Agent 参数**列仅供内部映射；**对用户展示时删除该列**，只保留「业务项 + 说明」。

### Google（`open-account google`，无需图片）

| 业务项   | 说明                                                      | Agent 参数（勿展示） |
| -------- | --------------------------------------------------------- | -------------------- |
| 公司名称 | 用于匹配/创建广告主组                                     | `--company`          |
| 推广链接 | 可只写域名，提交时会自动补 `https://`                     | `--promotion-link`   |
| 推广类型 | `b2b`（企业对企业）/ `b2c`（企业对消费者）/ `app`（应用） | `--promotion-type`   |
| 一级行业 | 可选；网页已隐藏；不传则 `customer_info.industry`=`-`     | `--industry1`        |
| 二级行业 | 可选；与一级成对；皆空时统一为 `-`                        | `--industry2`        |
| 账户名称 | 广告账户显示名，建议 ≤22 字                               | `--account-name`     |
| 币种     | `USD`（美元）或 `CNY`（人民币）                           | `--currency`         |
| 时区     | 时区 Code；可省略（USD→香港、CNY→上海）；其它先查列表     | `--timezone`（可选） |
| 邀请邮箱 | 开通后接收账户邀请的邮箱                                  | `--invite-email`     |

### TikTok（`open-account tiktok`，需营业执照图片）

| 业务项       | 说明                                   | Agent 参数（勿展示）     |
| ------------ | -------------------------------------- | ------------------------ |
| 公司名称     | 无 OCR，须用户手填                     | `--company`              |
| 账户名称     | 广告账户显示名                         | `--account-name`         |
| 时区         | IANA；不确定时先查时区列表             | `--timezone`             |
| 行业 ID      | **叶子节点**数字；不确定时先查行业列表 | `--industry-id`          |
| 注册地       | 国家代码如 `CN`；不确定时先查地区列表  | `--registered-area`      |
| 推广链接     | 推广网址                               | `--promotion-link`       |
| 执照编号     | 统一社会信用代码                       | `--license-no`           |
| 执照图片     | 本地 JPG/PNG 路径                      | `--license-file`         |
| 法人姓名     | 必填                                   | `--representative-name`  |
| 法人身份证   | 必填                                   | `--representative-id`    |
| 法人银联账号 | 必填                                   | `--unionpay-account`     |
| 法人手机     | 必填                                   | `--representative-phone` |
| 币种         | 只支持 USD，无需再问用户               | （无 `--currency`）      |

### Yandex（`open-account yandex`，无需图片）

| 业务项       | 说明                     | Agent 参数（勿展示） |
| ------------ | ------------------------ | -------------------- |
| 公司名称     |                          | `--company`          |
| 联系邮箱     |                          | `--email`            |
| 税号 TIN/INN | 类型固定 `FOREIGN_LEGAL` | `--tin`              |

### BingV2（`open-account bing`，需营业执照图片）

| 业务项     | 说明                                                        | Agent 参数（勿展示） |
| ---------- | ----------------------------------------------------------- | -------------------- |
| 直接/代理  | `Direct`（直接）或 `Agency`（代理）                         | `--pattern`          |
| 广告主全称 | 用于匹配/创建广告主组                                       | `--advertiser-name`  |
| 公司简称   |                                                             | `--name-short`       |
| 开户名称   | 账户显示名                                                  | `--name-remark-list` |
| 省份       |                                                             | `--province`         |
| 城市       |                                                             | `--city`             |
| 详细地址   |                                                             | `--address`          |
| 邮编       |                                                             | `--postcode`         |
| 行业       | 先查行业列表，传输出的 **id**（与网页下拉一致），勿猜中文名 | `--trade-id`         |
| 推广链接   |                                                             | `--promotion-link`   |
| 执照图片   | JPG/PNG/PDF 本地路径                                        | `--license-file`     |

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
# 不传行业时与网页一致：customer_info.industry = "-"

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
| 已通过 | 账户可用     | `list-accounts` 确认 + 按 `finance.md` 打开对应媒体充值页（传统充值/月结充值仅 Google/TikTok/Meta/Microsoft 有页面；Yandex 当前没有对应充值界面） |
| 已拒绝 | 资料问题     | 查看拒绝原因，修正后重新提交                                                                                                                            |

完整参数：`siluzan-tso open-account <subcommand> -h`
