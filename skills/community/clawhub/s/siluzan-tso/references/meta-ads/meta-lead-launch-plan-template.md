# Meta Instant Form 投放计划模板

> 用途：用户审查用的线索广告计划；字段须与已落盘的 `meta-lead-create` JSON 一致。流程见 `workflows.md` **W13**。
> 触发：出 Meta / Facebook 线索广告方案、要表格、创建前确认。
> 字段契约：`assets/meta-lead-create-template.json` + `meta-lead-create-template.md`
> 可执行边界：仅 Instant Form（`OUTCOME_LEADS`）。无 Advantage+ / 视频 / 系列列表。一次 `meta-ad create` 只落地 **1 系列 × 1 组 × 1 创意 × 1 广告**。

---

## 交付顺序（固定）

1. 落盘与模板同构的 **`meta-lead-create` JSON**（唯一可执行数据源；对话里勿贴整份 JSON 当主交付）。
2. **创建阶段**跑 `meta-ad validate`；**仅出方案**可跳过网关，但仍建议本地 validate（`account` / `pageId` 可用占位）。
3. **审查稿（必做）**：`siluzan-tso meta-ad plan-render --config-file ./meta-lead.json --out ./meta-lead-plan.xlsx`
   - **必交**运营固定 4 Sheet `.xlsx`（版式锁死，对照运营《Facebook 广告推广方案》表）。
   - **同时**写出同名 `.md`（对话里扫一眼用，**不能**代替 xlsx）。
   - **禁止** Agent 手写脚本 / `excel-style-kit` / 第三方 xlsx Skill 另出 Facebook 方案表。
   - **禁止**跳过 JSON 直接手填表；缺字段渲染为 `[待补]`，不编造。
4. 用户确认后改需求只改 JSON → 再跑 `plan-render` →（创建阶段）再 validate → `meta-ad create --commit`。

### 仅出方案 vs 创建

| 阶段 | 触发 | 账户 | Agent 必须做 | 禁止 |
| --- | --- | --- | --- | --- |
| **仅出方案** | 「出方案 / 先别创建 / 只要表格」；或未给账户且未说要创建 | 不必须 | JSON（`account`=`[PENDING_ACCOUNT]`，`pageId`=`[PENDING_PAGE]`）+ `plan-render` 出 xlsx+md | 因缺账户阻塞交付；未确认就 `create`；Agent 自写 xlsx |
| **创建** | 用户已确认方案并要落地，且已有 `mediaCustomerId` | 必须 | `pages` 写回真 `pageId` → validate → **再 `plan-render` 确认** → `create` | 跳过审查稿；跳过 validate |

占位约定：`account` = `"[PENDING_ACCOUNT]"`；`pageId` = `"[PENDING_PAGE]"`。选定账户后 `meta-ad pages` 写回真 ID，再 validate/create。

---

## Markdown ↔ JSON 映射

| 计划正文 | JSON |
| --- | --- |
| 账户 / 主页 | `account`、`pageId` |
| 品牌 / 客户 / 官网 / 一句话 | `plan.brand`、`plan.customerName`、`plan.siteUrl`、`plan.businessOneLiner` |
| 主结果 / 落地页型 | `plan.mainResult`、`plan.landingType`（须写 Instant Form + 具体页，勿只写「官网」） |
| 素材规格 | `plan.creativeSpec`（建议 `4:5（1080×1350）或 1:1；图字 <20%`） |
| 公开背书 | `plan.endorsements[]`（`verified!=true` 标「投放前删除」） |
| 预算模式 / 日预算 | `budgetMode`、`campaign.dailyBudget` 或 `adset.dailyBudget`（**元**） |
| 国家 / 年龄 | `adset.countries`、`ageMin`、`ageMax` |
| 表单字段 | `form.questions[]`（`reuseId` 时写复用 ID，勿编造字段） |
| 将创建的那条文案 | `creative.message` / `headline` / `link` / 图片三选一 |
| 视觉套系 A/B/C | `plan.tracks[]`（`shots[].headlines` / `primaryText` / `cta` / `description`） |
| 3×2×2 矩阵 | `plan.matrix.visual` / `bodyTone` / `headline` |
| 计划中的多组 | `plan.adSets[]`（`label`/`region`/`targeting`/`creatives`/`cpl`；create 只建 `adset`） |
| 产品 / 卖点 / 工厂 / 认证 | `plan.products` / `adFocus` / `sellingPoints` / `factory` / `certifications` |
| 行业/职位定向（审查稿） | `plan.targeting.industries[]` / `jobs[]` / `extraInterests` |
| 合规 / emoji | `plan.complianceNotes`、`plan.emojiPerPost` |

`plan` **不**发给网关。多组、多套系要落地时：用户确认后先 `create` 第一条，再用 `adset-create` / `creative-create` / `ad-create` 按矩阵补。

---

## 模板正文（Markdown 投影）

脚本按以下格式写。`{{…}}` 只从 JSON 读取，不得手写与 JSON 矛盾的数。

```markdown
# {{plan.brand}} — Facebook 图文广告草案

- 客户/站点：{{plan.customerName}} + {{plan.siteUrl}} + {{plan.businessOneLiner}}
- 主结果：{{plan.mainResult}}
- 落地建议：{{plan.landingType}}（Instant Form；写清页型，不要只说「官网」）
- 素材规格：{{plan.creativeSpec}}
- 可引用公开背书（列表；`verified!=true` 标「投放前删除」）
  {{plan.endorsements}}

> 账户：{{account}}　主页：{{pageId}}　预算：{{budgetMode}} {{日预算}} 元　国家：{{adset.countries}}
> 计划状态：**待确认**　本批可执行：Instant Form 线索广告（非 Advantage+）

## 套系 A｜{{plan.tracks[0].name}}
### A1 画面说明（给设计/拍摄）
- 构图：{{shots[0].composition}}
- 图上仅一行英文：{{shots[0].onImageText}}
- 调性：{{shots[0].tone}}
- 禁忌：{{shots[0].forbid}}

Headline（≤5 词）
- `{{shots[0].headlines[0]}}`
- `{{shots[0].headlines[1]}}`

Primary text
  {{shots[0].primaryText}}

CTA：{{shots[0].cta}}
Description：`{{shots[0].description}}`

（继续 A2 / B1 / C1… **至少 3 个视觉差异套系**）

## 将创建的这一条（JSON.creative，create 只交这个）

| 项 | 内容 |
| --- | --- |
| message | {{creative.message}} |
| headline | {{creative.headline}} |
| link | {{creative.link}} |
| 图片 | {{imageHash / imagePath / imageUrl}} |
| 表单 | {{form.name 或 form.reuseId}}；字段：{{form.questions}} |

## 3×2×2 测试矩阵（上传时组合）
| 维度    | 选项 1 | 选项 2 | 选项 3 |
|---------|--------|--------|--------|
| 视觉    | {{matrix.visual[0]}} | {{matrix.visual[1]}} | {{matrix.visual[2]}} |
| 正文气质 | {{matrix.bodyTone[0]}} | {{matrix.bodyTone[1]}} |  |
| 标题    | {{matrix.headline[0]}} | {{matrix.headline[1]}} |  |

说明：每个「视觉 × 正文 × 标题」是素材组合建议；本批 **无 Advantage+**。
至少 3 图 × 2 文 × 2 标题再开投；create 先落地 JSON.creative，其余用原语补。

## Instant Form 字段

| type | label | key |
| --- | --- | --- |
| {{questions[i]}} |  |  |

## Emoji 与合规备忘
- {{plan.complianceNotes}}
- 每帖 emoji 个数：{{plan.emojiPerPost}}

草案依据为公开页面/客户材料，非广告后台数据。
```

---

## Excel 四表（`plan-render` 锁死，勿改 Sheet 名/表头）

```bash
siluzan-tso meta-ad plan-render --config-file ./meta-lead.json --out ./meta-lead-plan.xlsx
```

对照运营表：`方案总览` / `1-客户画像` / `2-账户结构` / `3-表单询盘C1`。配色：藏青标题 `#1F4E79`、橙分区 `#C55A11`、蓝表头 `#2E75B6`。缺值 `[待补]`。

### Sheet `方案总览`

| 项目 | 内容 |
| --- | --- |
| 客户名称 | `plan.customerName` |
| Facebook 主页 | `plan.pageUrl` 或「待 pages 后补」 |
| 官方网站 | `plan.siteUrl` |
| 主营业务 | `plan.businessOneLiner` |
| 核心产品 | `plan.products` |
| 核心卖点 | `plan.sellingPoints` |
| 目标市场 | `plan.targetMarkets` 或 `adset.countries` |
| 营销目标 | `plan.mainResult` |
| 日预算 | `campaign.dailyBudget` 或 `adset.dailyBudget` |
| 广告结构 | `plan.structureSummary`（须写清本次 create：1×1×1） |
| 投放策略 | `plan.strategy` / `plan.landingType` |

### Sheet `1-客户画像`

分区「一、公司基本信息」：公司名称 / 官网 / 核心产品 / 广告聚焦 / 工厂实力 / 认证资质 / 核心卖点。  
分区「应用行业 / 兴趣」：`plan.targeting.industries[]` 与 `jobs[]` 对照。  
页脚：补充兴趣词 + 「本批组定向只认国家/年龄/性别」。

### Sheet `2-账户结构`

`层级` / Campaign 名 / 投放目标 / 日预算。广告组区域来自 `plan.adSets[]`。

### Sheet `3-表单询盘C1`

4.1 广告组：`label` / `region` / `targeting` / `creatives` / `cpl`。  
4.2 表单：`form.questions[]`（`#` / 字段名 / 必填 / 选项）。  
4.3 文案：`plan.copyBlocks[]`，缺省回退 `creative.message` / `headline` / `tracks`。

---

## Agent 投影纪律

- Facebook 方案 xlsx **只**用 `meta-ad plan-render`；禁止手写脚本或通用样式套件另出表。
- `plan.targeting` 默认只进审查稿；要打进网关写 `adset.flexibleSpec`（此时 `advantageAudience` 默认 0）。
- `create` 失败用 `--json-out` 已建成 ID 续跑；**禁止**再 `campaign-create`。
- 改需求改 JSON 后重跑 `plan-render`，不要只改审查稿。
- `create` 前必须把 xlsx（+ md）交给用户并得到确认；`--commit` 不是方案确认。
- 数字（同心度、年限、客户数）写进 `plan.endorsements` / `complianceNotes`：不可证的标 `verified=false`，不要写死进 `creative.message` 除非用户书面确认。
