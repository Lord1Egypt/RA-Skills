---
name: zm-ppt-deck-production-workflow
description: ZM PPT/Deck 正式生产流程。用于把课程课件、行业专场、招商/培训/沙龙 Deck 的需求、大纲、页面合同、素材分级、样页确认、视觉生产、PPT/HTML 组装、渲染审核、返工和交付包归档串成稳定流水线。
---

# zm-ppt-deck-production-workflow

## 定位

这是 ZM PPT/Deck 正式生产流程 Skill，不是单一生成器。

它负责：

1. 锁定内容大纲；
2. 制定制作规范；
3. 生成逐页页面合同；
4. 区分 Image 生图、真实素材、混合融合；
5. 给导演台 / zm-image2-ppt-generator 下发生图需求；
6. 给 zm-pptx-create-edit-tool 下发 PPT 组装需求；
7. 给 zm-pptx-inspect-review-tool 下发渲染审核需求；
8. 管理版本、返工、压缩、上传、交付包。

## 协作 Skill

- `zm-image2-ppt-generator`：页面主视觉 / 背景 / 高质量视觉生成。
- `zm-pptx-create-edit-tool`：PPTX 组装、页序、Logo、页脚、页码、Part 标签、文件处理。
- `zm-pptx-inspect-review-tool`：PPT 读取、渲染、视觉审核、文本审核、返工定位。

## 最高优先级规则

1. 内容大纲是唯一依据；未锁定大纲，不进入视觉生产。
2. 一页只传递一个核心认知；页面不是讲稿，不堆文字。
3. 生图负责高级感、氛围和概念表达；真实素材负责可信度、案例证明和实际演示。
4. 页面主体应是完整单页视觉图；禁止用多层图像叠加拼主体页。
5. Logo、Part 标签、页脚、页码后期统一添加；主视觉图内禁止生成这些元素。
6. 真实 Logo、真实产品界面、讲师本人、二维码、真实案例和业务数据不得由模型伪造。
7. 同构页必须联动设计与返工，例如 P3/P4、P6/P7。
8. 每版必须渲染审核；没有最终审核记录，不得宣称完成。
9. 压缩版必须标明用途；低清压缩版不得冒充正式展示版。
10. 外部上传必须记录节点、文件名、file_token/链接、验证结果。

## 默认生产流程

1. 需求卡；
2. 内容大纲；
3. 制作规范；
4. 逐页制作说明 / 页面合同；
5. 素材清单与分级；
6. 页面主视觉生成；
7. PPTX 组装与后期元素；
8. 渲染审核与返工；
9. 交付包与知识库归档。

详细流程见 `workflows/full-ppt-production-workflow.md`。

## 交互式制作要求

所有正式 PPT 制作必须遵守 `workflows/interactive-production-workflow.md`。

关键门禁：

- 内容大纲未经用户确认，不进入视觉生产；
- 首批样张未经确认，不全量生成；
- 真实素材缺失，不得伪造，只能占位；
- 用户反馈必须扩展到全稿同类问题排查；
- 知识库上传/外部发送必须记录目标节点与 token。

## 页面充实度门禁

所有页面在内容大纲和页面合同阶段必须通过 `checklists/page-density-checklist.md`。

禁止只用“高级感、少字、留白”替代内容承载。开场页也必须至少包含标题、副标题、核心判断和支撑点。视觉高级但内容空，判定为 NEEDS_ENRICHMENT，不能进入最终组装。

## 默认审核口径：高密度内容建议

用户确认：PPT 审核和建议阶段，默认给高密度内容方案。审核不只看视觉高级感，还要主动判断页面是否饱满，并给出结构化扩容建议。

高密度不是堆字，而是让页面具备：核心判断、支撑点、小框架、证据位、讲师口述分工。

## 美感审核与 Logo 安全位硬门禁

所有 PPT 页面最终审核必须调用：

- `standards/aesthetic-review-standard-v1.md`
- `standards/logo-safe-area-standard-v1.md`

文字正确、结构完整但视觉平庸，不得放行。Logo 必须后期添加，但页面设计阶段必须预留左上角安全位；Logo 最大宽度不超过页面宽度 7%，不得压住标题、图片、内容框或边框。

## IMG-2 Only 正式视觉门禁

正式 PPT 主体视觉必须遵守 `standards/img2-only-visual-production-standard-v1.md`。

没有 `happy/gpt-image-2` / `skills/zm-img2-generation-direct` 证据的页面主体视觉，一律 REJECTED_NOT_IMG2。禁止用 PIL、SVG、矢量图、HTML/CSS、程序绘图、贴片补丁冒充生图。

## 主流程优先门禁

用户确认：高密度不能影响主流程。所有 PPT 页面必须遵守 `standards/main-flow-priority-and-density-control-v1.md`。

如果页面信息太多、表达点过散、支撑信息抢主流程，即使视觉高级、内容正确，也判定为 NEEDS_FLOW_REDUCTION，必须做内容减法后再进入视觉生产或最终放行。
