---
name: weigui-weekly-report
description: 生成、筛选或解读上市公司违规案例周报，只使用聚源违规案例库及其关联表，并按 LatestInfoPublDate（公告日期/发布时间）选取连续 7 个自然日。用户要求“违规案例周报”“最近一周违规处罚案例”“本周处罚对象、违规事项、处罚情况或法规依据汇总”，或要求输出可交付 Word、JSON、Markdown 时使用。
---

# 违规案例周报

使用 `weigui_weekly_report` 获取周报。不得改用公告库、iFind、网络搜索或其他案例数据源。

## 工作流

1. 确定 `report_end_date`。
   - 用户说“最近 7 天”且未指定日期：省略该参数，使用北京时间当天。
   - 用户要完整自然周：传入该周周日。
   - 时间范围固定为结束日及向前 6 日，共 7 个自然日。
2. 首次调用固定传：

```json
{
  "quality": "all",
  "detail_level": "full",
  "format": "both",
  "page": 1,
  "limit": 100
}
```

3. 应用用户明确给出的 `bankuai`、`trigger_institution`、`violation_type` 条件；不得自行增加筛选。
4. 检查 `last_page`。大于 1 时继续逐页调用，后续页使用 `format=json`，合并时按 `publish_time DESC, case_id DESC` 排序，并按 `case_id` 防御性去重。
5. 检查 `coverage.source_degraded`、`invalid_publish_time`、缺失统计和每案 `quality`。
6. 用户要机器数据时返回 JSON；用户要 Word 时按“生成 Word”执行；其他周报请求优先返回 Markdown。

## 生成 Word

1. 先取得并合并完整 JSON，保留 `coverage`、`quality` 和 `missing_fields` 供内部校验，不把这些字段写入 Word。
2. 运行技能自带的确定性渲染器：

```bash
python3 scripts/build-weekly-word.py DATA_JSON OUTPUT_DOCX
```

3. 若当前 Python 缺少 `python-docx`，使用工作区提供的文档运行时；不得为此改写模板或降级为纯文本。
4. 渲染后必须检查：
   - 首页仅有日期、统计口径及三项数量指标；
   - 案例索引无质量列，且公司简称可跳转到对应案例；
   - 公司作为处罚对象时身份为“上市公司”；
   - 无处罚期限的案例不显示处罚期限列；
   - 每案结尾无质量状态；
   - 页脚为“董小屿违规案例库”；
   - 无文字截断、表格溢出、重叠或意外空白页。
5. 将最终 `.docx` 作为交付物返回。模板的颜色、字体、页眉页脚、表格几何、内部书签和分页规则均由 `scripts/build-weekly-word.py` 固化，不要临时重写。

## 强制口径

- 仅使用 `LC_ViolatiEventNew`、`LC_ViolatiParty`、`SecuMain`、`CT_SystemConst` 以及由这些记录生成的结构化缓存。
- 将 `LatestInfoPublDate` 表述为“公告日期/发布时间”，不要解释为公告库的公告日期。
- 一条 `LC_ViolatiEventNew.id` 计为一起案例；处罚对象明细不得重复增加案例数。
- 公司简称、名称和板块以 `SecuMain` 为准。
- 触发机构以 `PenalOrgs/PenalOrg` 解码结果为准。
- 法规依据只还原 `ViolationClauses/ViolationClause/EventContent` 中已有内容，不补写、不判断现行有效性。
- `null`、空数组和 `missing_fields` 表示原字段未取得，不得推断成“没有”或自行补齐。
- `partial` 和 `review_required` 案例不得静默删除；在报告中明确标注。

## 输出要求

每个案例至少保留以下键：

```text
company
trigger_institution / trigger_institutions
violation_matters
penalty_situation
case_penalties
legal_basis
quality
```

`case_penalties[]` 必须展示：

```text
object_name
object_identity
violation_types
penalty_types
penalty_term（仅案例明确载明处罚期限时展示）
```

- “违规事项”保留违规事实、违规认定和责任认定；以“根据/依据《……》……规定，决定/作出如下处分”等引出具体处罚决定的内容起，归入“处罚情况”，不得重复摘入“违规事项”。
- 处罚对象名称与本案例 `company.short_name` 或 `company.full_name` 一致时，对象身份固定显示“上市公司”。除此之外，对象身份只从最终展示的 `violation_matters.text` 中按处罚对象姓名查找；未出现职务/身份时显示“——”，不得用 `PartyType`、主体基本信息、处罚段或关联公司字段补写。
- 若某案例全部 `penalty_term=null`，该案例的“案例处罚情况”表隐藏“处罚期限”列；不得用发布时间、处罚日期或仅有日期起止值、但处罚原文没有期限语义的 `BeginDate/EndDate` 推算处罚期限。
- `detail_level=full` 时不得对违规事项或处罚情况作字符数截断；段落必须在语义边界完整结束，不得残留“经”“……的”等吞字/断句。
- 对外交付的 Word 周报使用“董小屿违规案例库”作为展示名称。页脚显示“董小屿违规案例库”；首页统计口径固定显示“统计口径：董小屿违规案例库 https://www.dxy-aiagent.com/website/weigui”。
- Word 首页仅展示违规案例数、涉及公司数和处罚对象数，不展示“完整/部分”等质量指标，也不展示数据源限制或动态入库提示。
- Word 仅输出“周报概览”和“案例明细”，不输出“数据质量与口径说明”第三部分；`coverage` 和 `quality` 仍保留在机器数据及内部校验中。
- Word 的“案例索引”不展示“质量”列；公司简称必须设置为内部超链接，点击后跳转到该案例在“案例明细”中的案例标题，股票代码保留为公司简称下一行的普通文本。
- Word 每个案例下方不展示质量状态、完整度、缺失字段或复核提示；`quality` 只保留在机器数据和内部校验中。

详细字段来源、质量状态和展示规则见 [references/schema.md](references/schema.md)。仅在需要解释字段、排查缺失或重组多页结果时读取。Word 渲染器要求的 JSON 结构也以该文件和工具返回结构为准。

## 失败处理

- 工具技术失败：说明“聚源违规案例库本次查询失败”，建议重试；不得回答“最近 7 天无案例”。
- `source_degraded=true`：可以交付主表结果；该状态仅用于内部校验和机器数据，不在对外交付的 Word 周报中展示结构化缓存、降级生成、质量状态、完整度或缺失/复核等技术提示。
- 工具不可用：优先提示启用项目中的 `weigui` MCP；不要切换到其他数据源替代。
- 在本项目开发环境中，若 HTTP MCP 未启动但 `mcp-weigui/dist/index.js` 已构建，可用工作区依赖提供的 Node 通过 stdio 启动该文件并调用 `weigui_weekly_report` 做只读查询。不得因此绕过数据源限制。
