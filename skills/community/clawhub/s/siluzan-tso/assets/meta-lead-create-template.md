# `meta-ad create` JSON 配置说明

`siluzan-tso meta-ad validate` / `meta-ad create` **仅**接受 `--config-file`。流程见 `workflows.md` **W13**。

模板：同目录 [`meta-lead-create-template.json`](meta-lead-create-template.json)。

---

## Agent 常见坑

| 场景 | 正确做法 |
| --- | --- |
| 创建 | `validate` → `meta-ad plan-render` 出运营 4 Sheet xlsx + md → 用户确认 → `create --commit` |
| 仅出方案 | `account`=`[PENDING_ACCOUNT]`，`pageId`=`[PENDING_PAGE]`；JSON + 审查稿即可，**禁止**因缺账户阻塞 |
| 金额 | JSON 填**主币种元**（`10` = $10 / ¥10）；CLI 按账户 `currency` 转最小单位。禁止把 `"1000"` 当 $1000 |
| CBO / ABO | `budgetMode=CBO`：预算只放 `campaign`；`ABO`：只放 `adset`。不能两边都有或都没有 |
| 主页 | 先 `meta-ad pages -a <id> --json-out`；空数组不要硬填历史 `pageId` |
| 表单 | 新建填 `form.name` + `privacyPolicyUrl` + `questions`；复用填 `form.reuseId` |
| 图片 | `imageHash` / `imagePath`（相对 JSON 目录）/ `imageUrl` 三选一；创意用 hash |
| 投放 | create **不会**自动 ACTIVE；三个对象分别 `campaign-status` / `adset-status` / `ad-status` |
| 失败续跑 | `--json-out` 含已建成 ID；用原语从失败步接着建，**不要**回滚、**不要**再 `campaign-create` |
| 细定向 | 审查稿写 `plan.targeting`；要打网关写 `adset.flexibleSpec`，并设 `advantageAudience=0`（有 flexibleSpec 时默认就是 0） |
| 支付方式 | 建广告报「请更新支付方式」→ 停，补付款后只跑 `ad-create` |
| bid cap | 遇到 `BID_AMOUNT_REQUIRED` 会停下。要当时改成 bid cap，事先填 `adset.bidAmountOnRequired`（主币种元）。不会把日/总预算写成出价 |
| 拉线索 | `clue -m Meta`（W11），不是本命令 |

---

## 字段

| 键 | 必填 | 说明 |
| --- | --- | --- |
| `account` | 是 | `list-accounts -m MetaAd` 的 `mediaCustomerId`（数字或 `act_`） |
| `pageId` | 是 | `meta-ad pages` 的主页 ID |
| `budgetMode` | 是 | `CBO` 或 `ABO` |
| `form.reuseId` | 复用时 | 已有 Instant Form ID |
| `form.name` / `privacyPolicyUrl` / `questions` | 新建时 | 至少含一个预定义字段（`EMAIL` / `FULL_NAME` / `PHONE` 等）；`CUSTOM` 必须带 `label` |
| `campaign.name` | 是 | 系列名。CBO 再加 `dailyBudget` 或 `lifetimeBudget` |
| `adset.name` / `countries` | 是 | ISO 两位国家。ABO 再加组预算 |
| `adset.flexibleSpec` | 否 | Graph `flexible_spec`，原样提交 |
| `adset.advantageAudience` | 否 | 仅**创建**：`0` / `1`；默认有非空 `flexibleSpec` 为 `0`，否则 `1`。`adset-edit` 不套这个默认 |
| `adset.bidAmountOnRequired` | 否 | 仅当建组返回 `BID_AMOUNT_REQUIRED` 时使用的出价上限（主币种元）。不填则停下，不会把预算写成 bid cap |
| `adset.optimizationGoal` | 否 | 仅 `LEAD_GENERATION`（默认）/ `QUALITY_LEAD` |
| `creative.message` / `link` | 是 | `link` 常用隐私政策 URL |
| `ad.name` | 是 | 广告名 |
| `plan` | 审查稿建议有 | 品牌/产品/定向/各组 CPL/套系；create **不提交**。结构见 `references/meta-ads/meta-lead-launch-plan-template.md` |

`activate` 即使写 `true` 也不会自动投放。

预定义 `questions.type`：`EMAIL`、`FULL_NAME`、`FIRST_NAME`、`LAST_NAME`、`PHONE`、`CITY`、`STATE`、`COUNTRY`、`POST_CODE`、`ZIP`、`COMPANY_NAME`、`JOB_TITLE`、`WORK_EMAIL`、`WORK_PHONE_NUMBER`、`DATE_OF_BIRTH`、`GENDER`、`MARITAL_STATUS`。
