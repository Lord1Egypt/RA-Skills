# Report Design Brief Template

Generate this brief only for a new build or meaning-changing continuation after the route-appropriate source gate and the design-ready gate in `intake-workflow.md` both pass. A bound Word/PDF/PPT/HTML material route requires a confirmed Material Understanding Summary; an idea-only route does not. A read-only review and a meaning-preserving local continuation do not generate or reconfirm this brief. If a minimum hard-boundary gap remains, use the blocked-intake output instead of this template. Ordinary missing details may be completed after confirmation and disclosed in the delivery verification list.

Keep it readable by the customer. Include only fields that affect this project. Do not emit a separate JSON configuration and do not pre-design every page.

```markdown
# 报告设计简报

## 项目定义
- 任务意图：新建 / 含义变化续作（只读复审与无含义变化的局部续作不生成设计简报）
- 输入入口：只有想法 / Word / PDF / 已有 PPT / HTML
- 使用模式：阅读 / 现场演讲
- 内容长度：精简 / 标准 / 详细
- 预计页数：根据当前材料动态估算
- 交付形式：单 HTML，或 HTML + assets / ZIP

## 主要工作场景
- 主工作场景：九场景目录中的精确客户名称
- 稳定 profile_id：对应 Workflow Profile 的稳定 id
- definition version：所加载定义文件中的当前版本
- 语义选择依据：用户明确目标与合格材料语义如何支持该主要场景
- bounded capability overlays：无；或逐项写明借用能力、来源 Profile、原因和影响范围

## 场景特有决策（仅当所选 definition_ref 声明设计简报增量时保留）
- 只写入当前主 Profile 的场景特有字段；逐项沿用该定义的客户可读字段名称与当前决策状态
- 不展示未选 Profile 的字段，不新建第二份简报，也不增加 Profile 独立确认

## 续作基线（含义变化续作时保留）
- 当前成品：精确路径或上传标识、检查覆盖与当前可预览状态
- 继承状态：仍有直接依据的目标、受众、结构、视觉、来源解释与确认产物
- 本次变更：请求修改的范围及不改变的边界
- 来源恢复/确认：修改真实数据、来源、证据关系或核心结论所需的原始来源或明确确认
- 当前就绪状态：仅记录已实际通过的当前检查；未完成时写“已找到 / 可以预览 / 尚未核验”，不写“已就绪 / 可正式交付”

## 报告目标
- 受众：...
- 希望受众理解或相信：...
- 期望行动：...

## 行动闭环（仅在目标要求外部行动时保留）
- 真实执行路径：完整 URL / Agent 调用语法 / 命令 / 下载或预约入口 / 联系方式
- 渠道来源与验证状态：用户明确提供 / 来源材料或项目上下文 + 验证方式与结果 / 用户授权 TaoHtml 选择 + 独立验证结果
- 最终页面展示方式：可见链接、完整命令、联系方式，或已解码核对且同时展示文本入口的二维码

## 必须保留的核心观点
1. ...

## 章节结构

### 第一章：...
- 本章任务：...
- 核心观点：...
- 支撑证据：...
- 预期结论：...

## 视觉方向
- 视觉来源：企业模板档案复用 / 用户明确参考 / TaoHtml 内置主题
- 企业模板档案（复用或临时 override 时保留）：profile id、企业显示名、active version、theme fingerprint、解析依据、binding 路径与当前验证状态
- 本次档案状态（复用或临时 override 时保留）：沿用 active version / `temporary_override`；临时 override 不修改企业默认档案
- 用户参考（如适用）：本地文件或可定位描述
- 参考图模式（如适用）：`reconstruct` 参考风格重构 / `corporate_fidelity` 企业模板保真
- 保真边界（企业模板保真时保留）：只承诺截图中可见效果；不承诺恢复原始 PPT 母版、矢量 Logo、字体源文件或截图外资产
- 来源页面与角色（企业模板保真时保留）：每页 id、自动识别的 cover / toc / section / content / data 角色、源图哈希与尺寸、canvas_bbox、observed 状态
- 锁定企业元素（企业模板保真时保留）：shared asset 与各 shell 固定 placement 的 id、类型、来源页、归一化 bbox、确认状态
- 可编辑安全区（企业模板保真时保留）：每个 shell 的区域 id、归一化 bbox、唯一允许内容角色；固定层不参与排版或动效
- 参考事实边界（如适用）：`observed` 直接观察 / `extension` 可确认延展 / `unknown` 截图无法判断；按 source / shell / asset / page role 分别记录
- 延展页面与限制（企业模板保真时保留）：所有未观察角色的 proposed extension 状态；更清晰截图等真实阻塞项；不承诺独立 Logo 上传
- VI 规范图（静态参考时保留）：统一 PNG / HTML 路径 + 已确认状态
- 所选内置主题（如适用）：稳定 theme id + 完整主题名称 + 一句具体画面描述
- 内置主题决定（如适用）：客户选择 / 明确委托 TaoHtml；当前选择或委托的会话引用
- 选择理由：...
- 必要偏离说明：无 / 偏离项、原因及仍保留的主题语法
- 动效密度：`minimal` 少量 / `moderate` 适中 / `rich` 丰富
- 动效决定：客户选择 / 明确委托 TaoHtml；当前选择或委托的会话引用
- 动效推荐依据：TaoHtml 的推荐及与报告任务、使用模式的关系；推荐不等于已选择
- 阅读与演讲行为：...

## 来源与证据记录
- 来源：路径、上传标识或精确外部定位
- source_binding：current_upload_or_user_explicit / task_instruction_explicit / candidate_confirmed / agent_retrieved_external
- source_role：original_customer_material / external_public_evidence / secondary_handoff_summary / current_artifact / visual_reference / agent_generated_material / described_unavailable_material
- availability_status：workspace_readable / external_retrieved_inspected / platform_visible_not_retrieved / handoff_record_only / confirmed_missing / not_yet_verified
- evidence_verification：verified / unverified / conflicting / not_applicable
- 检查覆盖、观察依据与限制：...
- 来源理由：...
- 支撑观点：...
- 最终页面是否展示及展示位置：...

## 交付约束
- 离线、画布、浏览器、素材和附件要求

## 待确认项
- TaoHtml 的自动推断及依据：...
- 预计创作性补全范围：可能补充的场景、数字、观点、示例或表达；具体生成内容将在交付时逐条列入《待核实内容清单》
- 数据修正及原因：...
- 其他会影响成品的判断：...

请确认或修正这份当前完整设计简报；明确确认只绑定此版本的完整设计简报、其中记录的当前内置主题/不适用状态与动效决定，以及当前会话记录，并允许进入独立的 current-file Production Authorization 检查。任一设计决定变更后都必须更新并重新确认完整简报。设计简报确认不是正式 HTML 制作授权；只有该检查允许 `formal-html` 后，才能开始正式制作。
```

## Adaptation Rules

- For a simple report, merge short sections and keep the brief compact.
- For a complex report, preserve the chapter-level viewpoint, evidence, and conclusion mapping.
- Copy the selected Workflow Profile's exact customer-facing name, stable `profile_id`, definition version, semantic selection basis, and bounded capability overlays into `主要工作场景`. Write `无` when there is no overlay. Do not expose a Profile or IR questionnaire.
- When the selected definition contains `设计简报增量`, copy only those fields into the one adaptive `场景特有决策` section. Omit the whole section for definitions without an increment, and never display fields from an unselected Profile. This is part of the complete current brief, not a second brief or confirmation round.
- Treat Profile selection, confirmation of the complete current Report Design Brief, and Production Authorization as three independent facts. Selecting a Profile neither confirms the brief nor authorizes production, and brief confirmation does not replace current-file Production Authorization. Bind the confirmed brief to the current normalized built-in-theme/not-required object and motion decision through the canonical digest defined in `production-authorization.md`; any value, status, or decision-reference change requires an updated brief and fresh confirmation.
- For a meaning-changing continuation, preserve every still-supported inherited decision, describe only the requested delta in `续作基线`, rebuild only affected fields, then display and confirm the complete current brief. Avoid replaying the original interview. A read-only handoff and a meaning-preserving local continuation never use this template.
- For a meaning-changing continuation whose dominant business outcome changes, update the affected `主要工作场景` fields inside the complete current brief and use the existing single brief-confirmation gate. For a meaning-preserving local continuation, keep the inherited Profile state without generating or reconfirming a brief. Do not add a Profile-specific confirmation round.
- Keep the seven source roles, six availability states, and evidence-verification status independent from `source_binding`. A secondary summary and a current artifact must state what each can and cannot support; neither becomes original evidence through reuse. Retrieved public/third-party evidence uses its external role and availability and must never be relabeled as customer material or Agent-generated content.
- Record only current observed readiness and operation evidence. A found/openable HTML is not formally deliverable; operating instructions must come from the exact artifact tested or be labeled as generic current Runtime-contract behavior.
- If the user supplied a clear visual reference, record `reference_mode`. Do not reduce `corporate_fidelity` to “closely reproduced”: state the screenshot-visible fidelity boundary, locked elements, editable region, and extension/unknown limits explicitly.
- For a reused corporate profile, copy the exact live binding's profile id, display name, version, theme fingerprint, identity-resolution basis, and temporary-override state. Do not require or claim a new VI confirmation. Keep the profile binding, current brief confirmation, and production authorization as three separate facts.
- A temporary override records the active profile that was deliberately not used and the current replacement visual route; it never changes the profile pointer. A permanent template update appears only after the new corporate VI/theme becomes an immutable profile version. Another company never reuses or overwrites the original profile record.
- If the user supplied a clear visual reference, do not add a competing built-in-theme requirement.
- For supported static-reference inputs, include the confirmed unified VI board path and confirmation state. In corporate fidelity, copy the exact source-role, canvas, shared-asset, shell placement, editable-region, extension, and limitation summary from the confirmed contract; do not silently alter it after current-board confirmation. Do not include a dynamic-analysis field or infer sequential behavior from multiple stills.
- Treat VI confirmation and Report Design Brief confirmation as separate gates. A confirmed VI board may enter the separate project-theme handoff, but it does not authorize report production.
- For a built-in visual system, copy its stable theme id, full customer-facing name, one-line description, `user_selected | delegated_to_taohtml` status, exact decision reference, fit reason, and every necessary deviation. A recommendation without either status cannot enter this brief. Write `无` when there is no deviation.
- For every visual route, copy the native `minimal | moderate | rich` motion density, its 少量 / 适中 / 丰富 customer label, `user_selected | delegated_to_taohtml` status, exact decision reference, and recommendation basis. Never turn a Workflow Profile default or static reference into a selected value. Do not repeat a choice already recorded.
- Include `行动闭环` only when the confirmed goal requires the audience to complete an external action. Omit it for explanatory, educational, or internal reports that do not require conversion; do not add a gratuitous CTA.
- Copy the exact verified action path into the brief. Record its provenance and verification status separately from the desired action, and state how the audience will see and use it on the final page.
- Put every outcome-changing design inference and its basis, planned creative-supplement scope, and source-data correction in `待确认项`. This is where `inferred` design-ledger items receive unified confirmation; do not require the customer to pre-approve every production sentence or illustrative value.
- During production, record each actual creative supplement in the delivery verification ledger rather than silently converting it into a source fact. Do not list customer-provided or independently verified facts as creative supplements.
- Never disguise a minimum hard-boundary decision as an inference. Return to the blocked-intake output in `intake-workflow.md` instead.
- Keep source records in the brief whether or not the final pages visibly cite them.
- Copy every used material's source identity, `source_binding`, source role, availability status, evidence-verification status, inspection coverage, limits, and binding reason from the source ledger. Do not include a merely discovered or conventionally named workspace file, and do not relabel an eligible bound source as a creative supplement.
- Do not split content into slide copy, speaker notes, and appendix at this stage; production makes that allocation from the confirmed mode.

## Authorization

The brief must be displayed as a whole before asking for confirmation. If the customer edits one section, revise the whole current brief and request one final confirmation. Profile selection is not this confirmation, and this confirmation is not Production Authorization. Only after the complete current brief is confirmed may the existing current-file authorization gate permit production.
