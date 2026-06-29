# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-pptx-create-edit-tool` Skill。

请创建、检查或编辑 PPTX 文件，并保证文件可打开、版式稳定、备注/页码/Logo 等元素正确。

## 最小必填

- 输入 PPTX 或新建要求
- 输出 PPTX 路径
- 页面数量
- 模板/版式要求
- Logo/页脚/页码规则
- 是否需要备注
- 验证方式

## 硬门禁

- 命令成功不等于 PPT 成功，必须打开/解析/渲染核验。
- 正式 Deck 需配合 ZM PPT/Deck 正式生产流程。
- 不得伪造真实 Logo、二维码、数据截图。

## 输出状态

最终必须输出：`PASS / NEEDS_REVISION / BLOCKED`，并说明理由。

