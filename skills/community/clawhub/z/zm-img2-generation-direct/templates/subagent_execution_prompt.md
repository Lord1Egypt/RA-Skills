# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-img2-generation-direct` Skill。

请使用 happy/gpt-image-2 执行正式生图或参考图生图，并保留完整证据。

## 最小必填

- 提示词
- 输出目录
- 输出数量
- 输出比例/尺寸
- 参考图路径（如 img2img）
- 禁止项
- 用途：PPT / 漫画 / 封面 / 配图

## 硬门禁

- 正式视觉必须证明调用 happy/gpt-image-2。
- 不得用 CSS/HTML/PIL/旧图拼装冒充生图。
- 不得在旧图上打补丁冒充新图。
- 二维码、Logo、真实界面不得由模型伪造。

## 输出

- 输入 prompt 路径
- 输出图片路径
- result JSON 路径
- 日志路径
- 自检结论 PASS / NEEDS_REVISION / BLOCKED
