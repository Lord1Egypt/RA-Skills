# 财务命令详解

> 所属 skill：`siluzan-tso`。
> 充值/钱包类操作需通过网页完成，CLI 负责提供链接并引导跳转。

---

## invoice-info — 发票抬头管理

发票抬头是开票申请时使用的公司/企业信息模板，支持三种类型：

- **PI**：形式发票（境外美金账户，英文信息）
- **VATI**：增值税普通发票
- **VATSI**：增值税专用发票

### 查询列表

```bash
siluzan-tso invoice-info list
siluzan-tso invoice-info list --invoice-type PI        # 按类型筛选
siluzan-tso invoice-info list -k "公司名关键字"         # 按公司名搜索
siluzan-tso invoice-info list --json-out ./snap                   # 原始 JSON（含 id 字段）
```

查询结果若 `data` 为空数组或无可核对字段，表示当前账号下**尚无已保存抬头**：向用户展示**原始 JSON** 并如实说明即可，勿推测「测试桩」等未经 CLI 报错佐证的原因。

### 新增发票抬头

**PI（形式发票，境外英文）：**

```bash
siluzan-tso invoice-info create \
  --invoice-type PI \
  --company-name "Shenzhen XX Technology Co., Ltd." \
  --registered-address "Shenzhen, Guangdong, China" \
  --contact "Zhang San" \
  --phone 13800138000 \
  --email zhang@example.com
```

**VATI / VATSI（增值税普票/专票）：**

```bash
siluzan-tso invoice-info create \
  --invoice-type VATI \
  --company-name "深圳XX科技有限公司" \
  --tax-id "914403XXXXXXXXXX" \
  --title "深圳XX科技有限公司" \
  --landline "0755-12345678" \
  --contact "张三" \
  --phone 13800138000 \
  --email zhang@example.com
```

### 更新发票抬头

```bash
# 先查 id
siluzan-tso invoice-info list --json-out ./snap

# 更新（字段与 create 一致，第一个参数为 id）
siluzan-tso invoice-info update <id> \
  --invoice-type VATI \
  --company-name "深圳XX科技有限公司（更新）" \
  --tax-id "914403XXXXXXXXXX" \
  --title "深圳XX科技有限公司" \
  --landline "0755-12345678" \
  --contact "张三" \
  --phone 13800138000
```

### 删除发票抬头

```bash
siluzan-tso invoice-info delete <id>
```

### 字段说明

| 选项                   | 说明                                     | PI     | VATI/VATSI |
| ---------------------- | ---------------------------------------- | ------ | ---------- |
| `--company-name`       | 公司名称（PI 用英文，VATI/VATSI 用中文） | ✅     | ✅         |
| `--registered-address` | 英文注册地址                             | ✅必填 | —          |
| `--tax-id`             | 税号                                     | —      | ✅必填     |
| `--title`              | 发票抬头                                 | —      | ✅必填     |
| `--landline`           | 座机号码                                 | —      | ✅必填     |
| `--contact`            | 联系人姓名                               | ✅     | ✅         |
| `--phone`              | 联系人手机号                             | ✅     | ✅         |
| `--email`              | 推送邮箱                                 | —      | —          |

---

## recharge — 充值业务

### 如何获取 Web 基地址

```bash
siluzan-tso config show
# 输出中 webUrl 行即为网页基地址，例如：
#   webUrl : https://www.siluzan.com        （生产环境）
#   webUrl : https://www-ci.siluzan.com     （测试环境）
```

> 规律：将 `apiBaseUrl` 中的 `tso-api` 替换为 `www` 即得 `webUrl`。

### 功能总览

| 功能                                                       | 引导用户打开的网页路径                                                     | CLI 支持                                |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------- | ----------- |
| 传统充值/现金充值（单笔，仅 Google/TikTok/Meta/Microsoft） | `/v3/foreign_trade/tso/recharge/pay?mediaType=<mediaType>`                 | ❌ 引导网页                             |
| 现金充值（批量，仅 Google/TikTok）                         | `/v3/foreign_trade/tso/recharge/pay_batch?mediaType=<Google                | TikTok>`                                | ❌ 引导网页 |
| 月结充值（仅 Google/TikTok/Meta/Microsoft）                | `/v3/foreign_trade/tso/recharge/accountBillingQuota?mediaType=<mediaType>` | ❌ 引导网页                             |
| 丝路赞钱包（充值/提现/明细）                               | `/v3/foreign_trade/tso/recharge/siluzanWallet`                             | ❌ 引导网页                             |
| 媒体转账记录                                               | `/v3/foreign_trade/tso/recharge/accountTransfer`                           | ✅ `transfer` 命令                      |
| 开票记录                                                   | `/v3/foreign_trade/tso/recharge/invoiceList`                               | ✅ `invoice list`                       |
| 开票申请列表                                               | `/v3/foreign_trade/tso/recharge/invoicingApplicationList`                  | ✅ `invoice billable` / `invoice apply` |

### 充值页链接（按媒体 × 类型）

链接模式：`https://www.siluzan.com/v3/foreign_trade/tso/recharge/<page>?mediaType=<mediaType>`；丝路赞钱包：`https://www.siluzan.com/v3/foreign_trade/tso/recharge/siluzanWallet`（无媒体参数）。

| 充值类型                  | `<page>`              | 支持媒体（`mediaType` 参数）                |
| ------------------------- | --------------------- | ------------------------------------------- |
| 传统充值/现金充值（单笔） | `pay`                 | `Google`、`TikTok`、`MetaAd`、`MicrosoftAd` |
| 现金充值（批量）          | `pay_batch`           | 仅 `Google`、`TikTok`                       |
| 月结充值                  | `accountBillingQuota` | `Google`、`TikTok`、`MetaAd`、`MicrosoftAd` |

> **Yandex、Kwai** 当前没有任何充值页面：不要拼接链接，说明网页暂不提供对应入口，建议联系丝路赞客服或业务负责人。不支持的「媒体 × 类型」组合（如 Meta 批量充值）同样不要引导。

### 引导用户的标准话术

当用户需要充值/查看钱包时，先取 `webUrl`，再按上表拼出**完整链接**。用户已指定媒体时，只给对应媒体的单笔充值链接（按需补批量/月结）；未指定媒体时，先询问媒体，或列出全部支持媒体的单笔充值链接 + 丝路赞钱包链接，并附 Yandex/Kwai 的说明。

---

## transfer list — 媒体转账记录

```bash
siluzan-tso transfer list [选项]
```

| 选项                     | 说明                                             |
| ------------------------ | ------------------------------------------------ |
| `-m, --media <type>`     | 媒体类型：`Google \| TikTok \| MetaAd \| BingV2` |
| `-n, --number <no>`      | 转账单号                                         |
| `-s, --status <status>`  | 到账状态                                         |
| `--start / --end <date>` | 日期范围（YYYY-MM-DD）                           |
| `--json-out`             | 输出原始 JSON                                    |

**示例：**

```bash
# 查询 Google 全部转账记录
siluzan-tso transfer list -m Google

# 查询 TikTok 本月转账记录
siluzan-tso transfer list -m TikTok --start 2026-03-01 --end 2026-03-31

# 按转账单号查询
siluzan-tso transfer list -m Google -n "TXN20260301001"

# JSON 输出
siluzan-tso transfer list -m Google --json-out ./snap
```

---

## transfer create — 提交账户间转账申请

> 在同媒体下，将资金从一个广告账户转入另一个广告账户。

```bash
siluzan-tso transfer create -m <媒体> --out <转出ID> --in <转入ID> --amount <金额>
```

| 选项                     | 说明                                               | 必填 |
| ------------------------ | -------------------------------------------------- | ---- |
| `-m, --media <type>`     | 媒体类型：`Google \| TikTok \| MetaAd \| BingV2`   | ✅   |
| `--out <id>`             | 转出账户 `mediaCustomerId`（来自 `list-accounts`） | ✅   |
| `--in <id>`              | 转入账户 `mediaCustomerId`                         | ✅   |
| `--amount <amount>`      | 转账金额（与账户货币单位一致）                     | ✅   |
| `--customer-name <name>` | 客户名称备注（可选）                               |      |
| `--json-out`             | 输出原始 JSON                                      |      |

**示例：**

```bash
# 先查出账户 ID
siluzan-tso list-accounts -m Google

# 从账户 A 转 100 USD 到账户 B
siluzan-tso transfer create -m Google --out 1234567890 --in 9876543210 --amount 100
```

---

## invoice — 开票管理

### invoice list — 开票申请记录

```bash
siluzan-tso invoice list [选项]
```

> **与投放报表类任务不同**：用户只说「本月开票记录」而未写起止日时，可用**当月 1 日 ~ 昨天**（`Asia/Shanghai` 日历）直接执行 `invoice list --start … --end … --json-out ./snap`，**不必**先做 SKILL「投放数据」类的时间范围 A/B/C 反问；若用户随后纠正区间再重查即可。

| 选项                     | 说明                   |
| ------------------------ | ---------------------- |
| `-k, --keyword <text>`   | 发票号/关键字          |
| `--start / --end <date>` | 日期范围（YYYY-MM-DD） |
| `--json-out`             | 输出原始 JSON          |

**示例：**

```bash
# 查询全部开票记录
siluzan-tso invoice list

# 查询本月开票记录
siluzan-tso invoice list --start 2026-03-01 --end 2026-03-31

# 按发票号搜索
siluzan-tso invoice list -k "INV2026001"

# JSON 输出
siluzan-tso invoice list --json-out ./snap
```

---

### invoice billable — 可开票订单列表

查询符合开票条件的订单，用于提交开票申请前确认 `billId`。

```bash
siluzan-tso invoice billable [选项]
```

| 选项                     | 说明                   |
| ------------------------ | ---------------------- |
| `-m, --media <type>`     | 媒体类型筛选           |
| `-c, --currency <code>`  | 币种，如 `USD \| CNY`  |
| `--wallet`               | 查询钱包充值可开票记录 |
| `--start / --end <date>` | 日期范围               |
| `--json-out`             | 输出原始 JSON          |

**示例：**

```bash
# 查询所有 Google USD 可开票订单
siluzan-tso invoice billable -m Google -c USD

# 查询钱包充值可开票订单
siluzan-tso invoice billable --wallet

# JSON 输出，获取 billId 供后续 apply 使用
siluzan-tso invoice billable -m Google --json-out ./snap
```

---

### invoice apply — 提交开票申请

开票业务规则：

- **人民币（CNY）订单**：只能开 **增值税** 发票（`VATI` / `VATSI`），不能选形式发票 `PI`。
- **美金等外币订单**（常见为 USD，且不含 CNY）：只能开 **形式发票 `PI`**（系统自动出具），不能选增值税票。
- **形式发票（PI）** 与 **增值税票** 填写的抬头字段不同：PI 为英文公司名 + 英文地址；增值税票为中文公司名、税号、发票抬头、座机等。

CLI 默认会分页查询 `invoice billable` 同源接口，按 `entityId` 解析订单币种并校验与 `--invoice-type` 是否匹配；若列表中找不到 id 或需跳过校验，可使用 `--skip-currency-check`（须自行保证与上表一致）。

**PI（形式发票，境外英文）：**

```bash
siluzan-tso invoice apply \
  --bill-ids "entityId1,entityId2" \
  --bill-type AmountAccount \
  --invoice-type PI \
  --media Google \
  --company-name-en "Shenzhen XX Technology Co., Ltd." \
  --registered-address-en "Shenzhen, Guangdong, China" \
  --recipient-name "张三" \
  --recipient-phone 13800138000 \
  --recipient-email zhang@example.com
```

**VATI / VATSI（增值税普票/专票）：**

```bash
siluzan-tso invoice apply \
  --bill-ids "entityId1,entityId2" \
  --bill-type AmountAccount \
  --invoice-type VATI \
  --media Google \
  --company-name "深圳XX科技有限公司" \
  --tax-id "914403XXXXXXXXXX" \
  --title "深圳XX科技有限公司" \
  --company-phone "0755-12345678" \
  --recipient-name "张三" \
  --recipient-phone 13800138000 \
  --recipient-email zhang@example.com
```

| 选项                      | 说明                                                                                | 必填           |
| ------------------------- | ----------------------------------------------------------------------------------- | -------------- |
| `--bill-ids`              | 可开票订单 `entityId`，逗号分隔（来自 `invoice billable --json-out ./snap`）        | ✅             |
| `--bill-type`             | 账单来源类型：`AmountAccount`（充值开票）\| `WalletRecharge`（钱包开票）            | ✅             |
| `--invoice-type`          | 发票格式：`PI`（形式发票，境外英文）\| `VATI`（增值税普票）\| `VATSI`（增值税专票） | ✅             |
| `--recipient-name`        | 收件人姓名                                                                          | ✅             |
| `--recipient-phone`       | 收件人手机号                                                                        | ✅             |
| `--recipient-email`       | 推送邮箱                                                                            | —              |
| `--company-name-en`       | 公司英文名称（PI 必填）                                                             | PI✅           |
| `--registered-address-en` | 英文单位地址（PI 必填）                                                             | PI✅           |
| `--company-name`          | 公司中文名称（VATI/VATSI 必填）                                                     | VATI✅         |
| `--tax-id`                | 税号（VATI/VATSI 必填）                                                             | VATI✅         |
| `--title`                 | 发票抬头（VATI/VATSI 必填）                                                         | VATI✅         |
| `--company-phone`         | 公司座机（VATI/VATSI 必填，对应接口 `InvoiceInfomation.Phone`）                     | VATI✅         |
| `--media`                 | 媒体类型（与 `invoice billable` 一致；核对币种时会传给列表接口）                    | 建议与订单一致 |
| `--skip-currency-check`   | 跳过币种与发票类型校验                                                              | —              |

**完整示例流程：**

```bash
# 第一步：查询可开票订单，记录 entityId
siluzan-tso invoice billable -m Google --json-out ./snap
# 从输出中找到目标订单的 entityId

# 第二步：提交开票申请（形式发票 PI 示例）
siluzan-tso invoice apply \
  --bill-ids "75dba917-5130-4c19-aca6-e2c7a420b02a" \
  --bill-type AmountAccount \
  --invoice-type PI \
  --media Google \
  --company-name-en "Shenzhen XX Technology Co., Ltd." \
  --registered-address-en "Shenzhen, Guangdong, China" \
  --recipient-name "张三" \
  --recipient-phone 13800138000 \
  --recipient-email zhang@example.com
```

---

### AI 助手：订单开票对话智能点

当用户表达「给订单开发票」「申请开票」「充值要开票」等意图时，助手应**分步引导**，顺序如下。

#### 1. 先让用户选择订单

- 执行 `siluzan-tso invoice billable`（按需加 `-m`、`-c`、`--wallet`、日期范围等），把结果整理成**可读的订单列表**（建议标注：金额、币种、时间、媒体、`entityId`）。
- **必须**请用户明确要开哪一笔或哪几笔（可多选），得到确认的 `bill-ids`（`entityId` 逗号分隔）和 `bill-type`（`AmountAccount` / `WalletRecharge`）之后，再进入抬头环节。
- 不要替用户猜测订单；未确认订单前不要直接 `invoice apply`。

#### 2. 再让用户选择发票抬头

- 根据已选订单的**币种**确定允许的发票类型（与上文规则一致：人民币 → `VATI`/`VATSI`；外币 → `PI`）。
- 执行 `siluzan-tso invoice-info list --invoice-type <PI|VATI|VATSI>`（需要结构化数据时用 `--json-out <路径>`），向用户展示**已保存的发票抬头列表**。
- 请用户**从列表中选一条**（按 id 或公司名/抬头说明），或明确说要用**新的自定义抬头**。

#### 3. 自定义抬头：先匹配列表，没有再创建

- 用户给出自定义抬头（公司名、税号、抬头文案、地址、联系人等）时：
  1. 先用 `invoice-info list`（可加 `-k` 关键字、`--invoice-type`）在**已有抬头**中检索：公司名、`title`、税号等与用户输入是否**实质相同**（允许轻微空格/标点差异）。
  2. **若已存在等价记录**：不要重复 `invoice-info create`；直接沿用该条字段填 `invoice apply`（传完整 `InvoiceInfomation`，不是只传抬头 id）。
  3. **若不存在**：先 `siluzan-tso invoice-info create ...` 创建成功，再 `siluzan-tso invoice apply ...`。避免未落库就假定「已保存」。

#### 4. 最后调用开票接口

- 组装 `invoice apply`：`--bill-ids`、`--bill-type`、`--invoice-type`、收件人信息，以及 PI 与 VATI/VATSI 各自必填的抬头字段（见上表）。
- 默认保留 CLI 的币种与发票类型校验；仅在用户理解风险时使用 `--skip-currency-check`。

**避免**：跳过订单选择；不展示 `invoice billable` 就让用户手写 id；对自定义抬头不做查重、反复 `create` 造成多条重复抬头。
