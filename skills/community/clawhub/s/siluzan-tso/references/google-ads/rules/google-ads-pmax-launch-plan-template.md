# PMax 广告投放计划模板

> 用途：用户审查用的 Performance Max 计划结构；字段须与已落盘的 `pmax-create` JSON 一致。
> 触发：出 PMax 方案 / `pmax-create` 前确认。
> 字段契约：`assets/pmax-create-template.json` + `assets/pmax-create-template.md`
> 命令：`ad pmax-validate` / `ad pmax-create`（见 `references/google-ads/pmax-api.md`）

---

## 交付顺序（固定）

1. 落盘与模板同构的 **`pmax-create` JSON**（唯一可执行数据源；勿把整份 JSON 当主交付贴进对话）。
2. **创建阶段**跑 `ad pmax-validate --config-file … --json-out …`；**仅出方案**可跳过。
3. **审查稿（必做）**：Agent **写代码**（Node/Python）读取该 JSON，按下方章节写出完整文件并交给用户审查。
   - 默认 **Markdown**（如 `./pmax-plan.md`）。
   - 用户要求 Excel / 表格 / 其他格式时，同一脚本改输出格式；文案与金额只从 JSON 投影。
   - 须列出：**全部**短标题 / 长标题 / 描述、callouts、structuredSnippets、sitelinks、leadForm、businessMessage、imagePaths——**禁止**只交概览表或「15 条标题已通过」类勾选摘要。
4. 用户确认 → 补齐图片等待办 →（必要时重跑 validate）→ `ad pmax-create`。

多份配置（多系列）时：每个 JSON 各投影一份审查稿（或脚本合并为一份，但每组文案仍须全量列出）。

---

## Markdown ↔ JSON 映射

| 计划正文      | `pmax-create` JSON（camelCase）                                 |
| ------------- | --------------------------------------------------------------- |
| 账户          | `account`                                                       |
| 系列名称      | `name`                                                          |
| 日预算（元）  | `budget`                                                        |
| 预算/资产组名 | `budgetName`、`assetGroupName`                                  |
| 落地页        | `finalUrls[]`                                                   |
| 商家名        | `businessName`                                                  |
| 短标题 ×15    | `headlines[]`                                                   |
| 长标题 ×5     | `longHeadlines[]`                                               |
| 描述 ×5       | `descriptions[]`                                                |
| 地域 / 语言   | `targetedLocations[].id`、`targetedLanguages[].id`              |
| 出价          | `biddingStrategyTypeV2`、`targetCpa_BidingAmount`、`targetRoas` |
| 图片          | `imagePaths.marketing` / `square` / `logo`（或对应 assetId）    |
| 视频          | `videoPath` 或 `youtubeUrlOrId`                                 |
| 宣传信息      | `campaignExtensions.callouts[]`                                 |
| 结构化摘要    | `campaignExtensions.structuredSnippets[]`                       |
| 站内链接      | `campaignExtensions.sitelinks[]`                                |
| 潜在客户表单  | `campaignExtensions.leadForm`（须单独成节）                     |
| WhatsApp      | `campaignExtensions.businessMessage`                            |

---

## 模板正文（须与 JSON 一致）

脚本投影时按下列章节输出；`{{…}}` 仅表示从 JSON 填入。

```markdown
# Google PMax 广告投放计划

> 账户 ID：{{account}}
> 制定日期：{{日期}}
> 计划状态：**待确认**

## 一、方案总览

| 项目            | 内容                                        |
| --------------- | ------------------------------------------- |
| 系列名称        | {{name}}                                    |
| 日预算（元）    | {{budget}}                                  |
| 出价策略        | {{biddingStrategyTypeV2}}                   |
| 目标 CPA / ROAS | {{targetCpa_BidingAmount}} / {{targetRoas}} |
| 地域 ID         | {{targetedLocations}}                       |
| 语言 ID         | {{targetedLanguages}}                       |
| 落地页          | {{finalUrls}}                               |
| 商家名          | {{businessName}}                            |

## 二、资产组文案（全量）

| 资产类型          | 文案                 | 字符数 |
| ----------------- | -------------------- | ------ |
| Business Name     | {{businessName}}     | …      |
| Headline 1…15     | {{headlines[i]}}     | …      |
| Long Headline 1…5 | {{longHeadlines[i]}} | …      |
| Description 1…5   | {{descriptions[i]}}  | …      |

## 三、附加资产（全量）

- callouts：逐条列出
- structuredSnippets：header + values 全量
- sitelinks：text + destinationUrl 全量

## 四、潜在客户表单

| 项目         | 内容                                             |
| ------------ | ------------------------------------------------ |
| 标题 / 描述  | {{leadForm.headline}} / {{leadForm.description}} |
| 收集字段     | {{leadForm.fields}}                              |
| 隐私政策 URL | {{leadForm.privacyPolicyUrl}}                    |
| 落地页       | {{leadForm.finalUrl}}                            |

（JSON 无 leadForm 且为 Lead Gen/B2B 时：须说明省略原因，或补回后再审查。）

## 五、WhatsApp / 图片与视频

列出 businessMessage 与 imagePaths / videoPath / youtubeUrlOrId；缺图写在「待确认」。

## 六、待确认

- 占位账户、缺图、privacyPolicyUrl 待核实等
```

JSON 中没有的内容（受众信号建议、效果预估、落地页优化建议）可作**附录**，并标注「非 JSON 字段」；不得写入后当作已进创建配置。

---

## 禁止

- 只输出概览表（账户/预算/「文案已齐」勾选）而不列全文案
- 手抄与 JSON 不一致的审查稿；改文案只改 JSON 后重跑投影脚本
- 未获用户确认审查稿就执行 `pmax-create`
