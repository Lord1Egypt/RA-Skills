# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-image2-ppt-generator` Skill。

请基于 Markdown 大纲或 slides_plan.json 生成视觉化幻灯片，并输出 HTML viewer / PPTX。

## 最小必填

- 大纲或 slides_plan.json 路径
- 输出目录
- 幻灯片数量
- 视觉风格
- 页面比例
- 是否需要模板克隆
- 是否为正式项目

## 硬门禁

- 本 Skill 是生成器，不替代正式 PPT 总控流程。
- 正式项目必须先有大纲/页面合同/样页确认。
- 生成后必须渲染审核，不能只看命令成功。

## 输出状态

最终必须输出：`PASS / NEEDS_REVISION / BLOCKED`，并说明理由。

