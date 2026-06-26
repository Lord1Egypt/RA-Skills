> 默认输出目录优先为当前工作目录下的 meme_outputs；如果当前目录不可写，则自动回退到系统临时目录。

# 输入法接入说明（中文）

## 推荐接入链路
1. 输入法拿到语音识别文本
2. 如果已有润色文本，同时传入 `polished_text`
3. 调用 `generate_meme.py`
4. 获取生成图片路径
5. 将图片作为候选内容插入输入法或聊天面板

## 输入字段建议
- `original_text`: 原始语音识别文本
- `polished_text`: 润色后文本，可选
- `mode`: `direct-text` 或 `template`
- `style`: 可选，手动覆盖自动风格

## 默认优先级
- 优先使用 `polished_text`
- 没有时退回 `original_text`
- 若两者都存在但意义冲突，默认使用更自然、更完整的一版

## UI 建议
- 默认展示单张图
- 如使用 template 模式，可在 UI 侧自行叠字
- 生成失败时，回退为只给一句推荐文案
