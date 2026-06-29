# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-ppt-deck-production-workflow` Skill。

## 任务

把用户的 PPT / HTML Deck 需求，按正式生产流程完成到可审核、可交付状态。

## 必须先读

1. `SKILL.md`
2. `workflows/interactive-production-workflow.md`（如存在）
3. `workflows/full-ppt-production-workflow.md`（如存在）
4. `checklists/page-density-checklist.md`（如存在）
5. `checklists/ai_readiness_checklist.md`

## 最小必填

- 课件/Deck 主题
- 目标观众
- 使用场景
- 页数范围
- 核心目标
- 页面风格
- 是否 PPTX / HTML / 两者都要
- Logo / 品牌素材
- 真实案例 / 数据来源
- 样页确认机制
- 审核和交付标准

## 执行顺序

1. 需求卡
2. 内容大纲
3. 制作规范
4. 逐页页面合同
5. 素材清单与分级
6. 样页 1-3 页
7. 样页确认
8. 全量视觉 / 页面生产
9. PPTX 或 HTML Deck 组装
10. 渲染截图审核
11. 返工
12. 交付包归档

## 硬门禁

- 大纲未锁定，不进入视觉生产。
- 样页未确认，不全量生成。
- 真实 Logo / 二维码 / 讲师照片 / 数据截图不得由模型伪造。
- 正式视觉必须由 media-director / PPT 专职链路执行，main 不直接生图。
- 没有渲染截图和审核记录，不得宣称完成。

## 输出

请输出：需求卡、页面合同、素材缺口、样页计划、执行 owner、审核计划、当前状态 READY / PARTIAL_READY / BLOCKED。
