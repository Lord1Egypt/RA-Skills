---
name: zm-quality-production-workflow
description: ZM 高质量产出流程。适用于课程、PPT/HTML Deck、漫画/手册、公众号文章、行业方案等正式产出，按“标准化输入→样章/样页→专业生产→双 Agent 审核→返工循环→main 终审→交付包归档”的多 Agent 流程稳定落地。
---

# ZM 高质量产出流程｜zm-quality-production-workflow

## 1. 定位

这是 OpenClaw / 筑梦学院的“ZM 高质量产出流程”总控 Skill，用于把一次正式产出做成可复用、可审核、可交付的稳定流程。

它适用于：

- 课程章节作战包；
- PPT / HTML Deck；
- 漫画 / 小白手册 / 图文手册；
- 公众号文章 / 长文 / 观点文；
- 行业 AI 方案 / 售前材料；
- 其他需要多角色协同、质量审核和交付包归档的正式产出。

## 2. Skill 与 SubAgent 的边界

本 Skill 负责定义：

1. 标准化输入；
2. 标准化输出；
3. 必要依赖；
4. 先后流程；
5. 样章 / 样页 / 样稿门禁；
6. 双 Agent 审核机制；
7. 返工循环；
8. 放行标准；
9. 交付包和审计记录。

本 Skill **不负责自己创建 SubAgent**。真正调度仍由 main / course-director / media-director 等外层执行者完成。

硬边界：main 不得因流程麻烦而绕过专业 SubAgent；正式视觉/生图交 media-director，正式正文交 writer-pro，正式代码交 code-engineer，main 负责调度、验收和终审。

正确用法：

```text
main 总控
  ↓ 调用本 Skill 制定流程和门禁
专业 SubAgent 执行
  ↓
双 Agent / 双视角审核
  ↓
返工或放行
  ↓
main 终审与交付
```

## 3. 最高优先级原则

1. **先锁目标，再做内容**：目标用户、业务目的、交付场景不清，不进入生产。
2. **先做标准化输入，再启动专业执行**：缺主角图、Logo、二维码、真实案例、数据来源等必要依赖时，先列缺口，不得伪造。
3. **先样章 / 样页 / 样稿，再全量扩展**：漫画先 P1；PPT 先 1-3 页样张；文章先大纲和开头；课程先章节结构和一页样例。
4. **先专业生产，再独立审核**：不得由同一执行者自写自审自放行。
5. **正式产出必须双审**：至少一个内容/逻辑审，一个用户目标/体验审。
6. **用户反馈是样本，不是修复上限**：必须扩展到全稿/全包同类问题排查。
7. **没有审核记录，不得宣称完成**。
8. **没有交付包结构，不得宣称完整交付**。
9. **main 是最终负责人**：不能把 SubAgent 回传原样当结果。
10. **缺关键素材时标记 BLOCKED**：不得用 AI 伪造真实 Logo、二维码、人物、案例、数据、截图。

## 4. 标准生产流程

通用流程见：`workflows/full-quality-production-workflow.md`。

简版：

```text
01 需求卡
02 标准化输入检查
03 依赖缺口清单
04 内容结构 / 页面合同 / 脚本大纲
05 样章 / 样页 / 样稿
06 用户或 main 确认样式与方向
07 全量生产
08 执行者自检
09 双 Agent 审核
10 汇总返工清单
11 返工循环
12 main 终审
13 交付包归档
14 发送/发布前核验
```

## 5. 标准化输入

正式任务启动前必须填写 `templates/standard_input_card.md`。

至少包括：

- 任务名称；
- 产出类型；
- 目标用户；
- 使用场景；
- 核心目标；
- 页数 / 字数 / 产物范围；
- 风格要求；
- 禁止项；
- 必需素材；
- 真实案例；
- 数据来源；
- Logo / 二维码 / 人物参考 / 主角图；
- 交付格式；
- 审核门槛。

## 6. 标准化输出

正式交付至少包含：

```text
00_README/
01_text/
02_versions/
03_outputs/
04_design_specs/
05_assets/
06_reviews/
07_publish/
08_sources/
09_meta/
```

不同产物可以扩展，但不得缺少核心产物、审核记录和版本记录。

## 7. 双 Agent 审核机制

双审流程见：`workflows/dual-agent-review-workflow.md`。

默认两个审核角色：

### Reviewer A：内容逻辑 / 专业质量审核

负责看：

- 目标是否成立；
- 结构是否顺；
- 论点是否有支撑；
- 数据 / 案例是否可靠；
- 是否跑题；
- 是否夸大；
- 是否符合课程体系 / 业务目标。

### Reviewer B：用户体验 / 场景可用性审核

负责看：

- 学员 / 读者 / 客户能否看懂；
- 野哥能否讲顺；
- 是否有互动和行动；
- 是否有常见问题和答案；
- 是否能转化成交付 / 发布 / 上课；
- 是否符合目标人群心理。

### main 终审

负责：

- 汇总两个审核；
- 判断冲突；
- 制定返工清单；
- 放行 / 返工 / BLOCKED；
- 写 `06_reviews/final_acceptance.md`。

## 8. 返工循环

默认最多 2 轮返工。

每轮必须产生：

- 返工问题清单；
- 返工 owner；
- 返工范围；
- 不改范围；
- 新版本路径；
- 复审结论。

两轮后仍未达标，必须标记 `BLOCKED` 或请求野哥补材料，不得无限循环。

## 9. 各产物专门门禁

### 9.1 课程章节作战包

必须包含：

- 学员课件；
- 讲师口播稿；
- 讲师提示卡；
- 知识补充；
- 案例库；
- 学员问答库；
- 课堂互动设计；
- 作业模板；
- 作业验收标准。

检查表：`checklists/course_chapter_quality_checklist.md`。

### 9.2 PPT / HTML Deck

必须包含：

- 内容大纲；
- 页面合同；
- 样页；
- 视觉规范；
- HTML / PPTX 输出；
- 渲染截图；
- 视觉审核；
- DOM / 结构检查；
- 交付包。

正式视觉不得由 main 直接生成，必须交 media-director / PPT 专职链路。

### 9.3 漫画 / 小白手册

硬流程：

1. 先出完整文字版；
2. main 自审文字逻辑；
3. 明确主角图、角色参考、风格参考、Logo、二维码真实资产、禁止项；
4. 文字定稿后，只先做 P1 样章；
5. P1 用于锁定画风、人物、Logo、排版、气泡风格、文字密度；
6. P1 经野哥 / main 确认后，才扩展 P2-Pn；
7. 每页图审通过后，才进入 HTML；
8. 二维码不得出现在漫画图本体，真实二维码只在 HTML 最后转化页后期嵌入；
9. HTML 必须真实打开 `index.html` 验收；
10. ZIP 必须符合完整交付包结构。

检查表：`checklists/comic_handbook_quality_checklist.md`。

### 9.4 公众号文章 / 长文

必须包含：

- 选题定位；
- 查重；
- 正文；
- 标题备选；
- 去 AI 味；
- reviewer / critic；
- 合规审核；
- 排版；
- 草稿箱 / 发布前核验；
- 交付包。

正文必须由 writer-pro / 写作专职生产，main 不直接裸写正式正文。

### 9.5 行业 AI 方案

必须包含：

- 目标行业；
- 用户画像；
- 痛点；
- AI 介入动作；
- 工作流；
- 交付边界；
- 成本 / 价值说明；
- 案例；
- FAQ；
- 售前材料；
- 验收标准。

## 10. 必要依赖判断

如果缺以下素材，不得进入对应生产阶段：

- 漫画缺主角图 / 角色参考：不得全量生图；
- 漫画缺 P1 样章确认：不得扩 P2-Pn；
- 需要真实二维码但缺二维码资产：不得生成假二维码；
- 需要真实 Logo 但缺 Logo：不得用临时 Logo 冒充；
- 数据页缺来源：必须标记待核准；
- 真实案例缺失：只能写案例占位，不能编造成已发生事实；
- 发布 / 发送 / 删除 / 付款等外部动作：必须确认。

## 11. 使用方式

当任务是正式产出时，main 或专业 agent 应先读取本 Skill，并创建：

1. `standard_input_card.md`；
2. `dependency_gap_list.md`；
3. `production_plan.md`；
4. `review_plan.md`；
5. `final_acceptance.md`。

然后再进入实际生产。

## 12. 相关 Skill / 标准

- `skills/zm-ppt-deck-production-workflow/`
- `skills/happy-img2-direct/`
- `skills/gpt-image2-ppt/`
- `skills/powerpoint-pptx/`
- `skills/pptx-2/`
- `skills/md2wechat/`
- `standards/delivery-package-standard-v1.md`
- `standards/comic-science-handbook-dual-standard-v1.md`
- `standards/formal-ppt-industry-deck-production-standard-v1.md`
## 13. 编排前自检与任务路由

正式启用本 Skill 前，必须先检查：

- `checklists/preflight_orchestration_checklist.md`
- `workflows/task-type-routing.md`
- `templates/production_plan_template.md`

目的：确认任务是否需要 SubAgent、哪些依赖是硬门槛、样章门禁在哪里、返工和 BLOCKED 条件是什么。
## 14. 成功标准

一个其它 AI / SubAgent 读完本 Skill 后，必须能做到：

1. 判断任务是否适用本 Skill；
2. 填写标准化输入卡；
3. 列出依赖缺口；
4. 判断 READY / PARTIAL_READY / BLOCKED；
5. 制定样章 / 样页计划；
6. 知道该调用哪个 SubAgent；
7. 按模板输出生产计划；
8. 按双 Agent 审核流程出报告；
9. 根据 PASS / NEEDS_REVISION / BLOCKED 做下一步；
10. 形成 final_acceptance.md 和交付包。

如果做不到以上 10 点，说明 Skill 还不够可执行，必须继续补模板或流程。

## 15. 给其它 AI 的最短使用路径

1. 读 `SKILL.md`；
2. 复制 `templates/subagent_execution_prompt.md` 作为执行指令；
3. 填 `templates/minimum_required_fields.md` 和 `templates/standard_input_card.md`；
4. 填 `templates/dependency_gap_list.md`；
5. 按 `workflows/task-type-routing.md` 确定 owner；
6. 按 `templates/production_plan_template.md` 建生产计划；
7. 样章确认后再全量；
8. 按 `workflows/dual-agent-review-workflow.md` 双审；
9. 按 `templates/final_acceptance_template.md` 终审。

## 16. 入库 / 上传

本地入库和外部上传流程见：`workflows/skill_publish_workflow.md`。

外部发布必须先确认目标、公开范围和脱敏要求。

