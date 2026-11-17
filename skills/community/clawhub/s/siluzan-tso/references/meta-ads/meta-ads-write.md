# Meta 线索广告 · 写入与编辑

> 流程见 `workflows.md` **W13**。金额/ID 口径见 [meta-ads.md](meta-ads.md)。
> **何时 Read**：创建/编辑/启停；写操作须用户确认与 `--commit`。

## 写操作硬纪律

- **必须** `--commit "…"`；漏了会直接失败。
- `--json-out <path>`：路径必填；禁止裸 `--json`。
- 创建默认 **PAUSED**。`meta-ad create` **不会**根据 `activate` 自动投放。
- 中途失败**不回滚**；读 `--json-out` 里已建成 ID，用原语续跑。**禁止**再 `campaign-create` / 重头 `create`。
- 建组（`create` / `adset-create`）提交 `targeting.targeting_automation.advantage_audience`（默认 `1`；有非空 `flexibleSpec` 时默认 `0`）。细定向：JSON `adset.flexibleSpec` + `advantageAudience=0`；原语 `--advantage-audience 0`。
- `adset-edit` **不**套用上面的创建默认值。未传 `--advantage-audience` 时保留当前的 `0` 或 `1`。当前组读不到该值时停下（`needs_decision` / `ADVANTAGE_AUDIENCE_UNSET`），须显式传 `--advantage-audience 0` 或 `1` 后再提交；不要省略后交给网关，网关会写成 `1`。`--countries` 默认是整表 **替换**；要在原国家上追加，用 `--countries-mode append`。当前定向里有本命令不能写回的字段时会停下，确认后才加 `--targeting-replace`。

## 主路径（对标 Google `pmax-validate` / `pmax-create`）

| 步骤 | 命令 |
| --- | --- |
| 模板 | 复制 `assets/meta-lead-create-template.json`，字段见 `meta-lead-create-template.md` |
| 主页 | `siluzan-tso meta-ad pages -a <accountId> --json-out ./snap-fb` |
| 校验 | `siluzan-tso meta-ad validate --config-file ./meta-lead.json [--json-out ./snap]` |
| 审查稿 | `siluzan-tso meta-ad plan-render --config-file ./meta-lead.json --out ./meta-lead-plan.xlsx`（运营固定 4 Sheet + 同名 md）→ 用户确认。`--commit` 不是方案确认。**禁止** Agent 手写 Facebook 方案 xlsx |
| 创建 | `siluzan-tso meta-ad create --config-file ./meta-lead.json --json-out ./snap --commit "创建 Instant Form 线索广告"` |
| 复核 | 用返回的 ID：`meta-ad campaign/adset/ad --id … --json-out` |
| 投放 | 三个对象分别 `*-status --status ACTIVE --commit "投放"` |

## 原语命令

失败续跑或改存量时用。金额参数一律**主币种元**。

```bash
siluzan-tso meta-ad form-create -a <id> --page-id <pageId> --config-file ./form.json --commit "新建表单"
siluzan-tso meta-ad image-upload -a <id> --image-url https://… --name lead.jpg --commit "传图"
siluzan-tso meta-ad campaign-create -a <id> --name Lead-CBO --daily-budget 10 --commit "CBO 系列"
siluzan-tso meta-ad adset-create -a <id> --campaign-id <cid> --page-id <pageId> --name Lead-US --countries US --commit "建组"
siluzan-tso meta-ad creative-create -a <id> --page-id <pageId> --name C --message "…" --link https://…/privacy --image-hash <hash> --form-id <fid> --commit "建创意"
siluzan-tso meta-ad ad-create -a <id> --adset-id <sid> --creative-id <crid> --name Lead-Ad --commit "建广告"
```

编辑（只传要改的字段）：

```bash
siluzan-tso meta-ad campaign-edit -a <id> --id <cid> --daily-budget 20 --commit "上调日预算"
siluzan-tso meta-ad adset-edit -a <id> --id <sid> --countries US,CA --countries-mode append --age-min 25 --commit "追加国家并改年龄下限"
siluzan-tso meta-ad ad-edit -a <id> --id <adId> --creative-id <newCrid> --commit "换创意"
```

`adset-edit --countries` 默认是**整表替换**国家，不是在旧国家上追加。追加用 `--countries-mode append`（例如保留 US 再加 CA）。只改年龄、性别时会先读当前组，保留可写回的国家 / 年龄 / 性别 / `flexible_spec` / `advantage_audience`。当前值是 `0` 或 `1` 时原样写回，**不会**改成 `1`。读不到当前值时本次不提交，须加上 `--advantage-audience`。不能写回的定向字段会停下；确认丢掉后再加 `--targeting-replace`。换主页请新建组。不能靠加一侧预算把 CBO 切成 ABO。写完后 CLI 回读，`verification=verified` 才表示已核验；`unknown` 要再查 `meta-ad adset`，不要当成没改成。

## 启停

```bash
siluzan-tso meta-ad campaign-status -a <id> --id <cid> --status ACTIVE --commit "开系列"
siluzan-tso meta-ad adset-status -a <id> --id <sid> --status ACTIVE --commit "开组"
siluzan-tso meta-ad ad-status -a <id> --id <adId> --status ACTIVE --commit "开广告"
```

`status` 原样交给网关：`ACTIVE` / `PAUSED` / `DELETED` / `ARCHIVED`。暂停时三个都停。删除用 `DELETED`，顺序 **广告 → 组 → 系列**；表单 / 图 / 创意 **无删除口**（复用的表单不要删）。

## 常见网关错误

| code | 处理 |
| --- | --- |
| `VALIDATION` | 按 `message` 改请求 |
| `CBO_ABO_CONFLICT` | 预算只放系列或只放组 |
| `BID_AMOUNT_REQUIRED` | 停下，输出 `needs_decision`（保留已建成 `campaignId`）。日/总预算**不是** bid cap。只有事先写了 `adset.bidAmountOnRequired` 或 `--bid-amount-on-required` 才会按该金额改成 `LOWEST_COST_WITH_BID_CAP` 再试一次 |
| `advantage_audience` / `targeting_automation` | **创建**会提交该字段（默认见上）。`adset-edit` 不套创建默认值；读不到当前值时输出 `ADVANTAGE_AUDIENCE_UNSET`，加上 `--advantage-audience` 后再提交。仍失败时用已有 `campaignId` 跑 `adset-create`，不要新建系列 |
| 请更新支付方式 / 添加有效支付方式 | **停**。读 `--json-out` 已建成 ID；让用户补付款方式后只跑 `ad-create`，不要重头 `create` |
| HTTP 403（账户/主页） | 当前 Token 无该户 Facebook Ads 权限，换登录或重新授权 |
| `PAGE_LIST_EMPTY` / `PAGE_NOT_LINKED` / `PAGE_NO_ADVERTISE` | 补主页广告投放权限并重新授权 |
| `LEAD_TOS_REQUIRED` | 用户在 Ads Manager 勾选条款，接口不代勾 |
| `RATE_LIMITED` / `GRAPH_RETRY` | Graph 明确返回的限流或 code 2。可有限退避后**再读或再查**已有 ID。传输超时、响应丢失、部分成功先对账 `--json-out` 进度，**禁止**盲重发创建 |
