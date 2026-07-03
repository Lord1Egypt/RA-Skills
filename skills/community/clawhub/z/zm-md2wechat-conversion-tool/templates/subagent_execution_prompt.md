# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-md2wechat-conversion-tool` Skill。

请将 Markdown 转成微信公众号可用 HTML/草稿输入，并检查样式、图片和脏文本。

## 最小必填

- Markdown 文件路径
- 主题/风格
- 是否保留图片
- 是否去 AI 味
- 输出 HTML 路径
- 是否需要后续推草稿

## 硬门禁

- 本 Skill 只负责转换/检查，不等于正式草稿落库成功。
- 正式草稿发布必须交 `zm-wechat-draft-publish-verify` 核验。
- 不得保留操作备注、封面路径说明等脏文本。

## 输出状态

最终必须输出：`PASS / NEEDS_REVISION / BLOCKED`，并说明理由。

