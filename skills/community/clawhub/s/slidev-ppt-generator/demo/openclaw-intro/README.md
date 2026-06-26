# OpenClaw Intro Demo

这个目录保存了一次通过 OpenClaw + `slidev-ppt-generator` 实际生成出来的演示文稿产物。

包含文件：

- `slides.md`
  Slidev 源文件
- `openclaw-intro.pdf`
  导出的 PDF 成品
- `openclaw-intro.pptx`
  导出的 PPTX 成品
- `package.json`
  OpenClaw 自动初始化的最小项目依赖
- `package-lock.json`
  锁文件

说明：

- 本次 demo 由 OpenClaw 真实触发生成，不是手工拼装
- 生成路径来自 OpenClaw 工作区中的 `openclaw-intro/` 项目
- 导出依赖按最佳实践安装在项目目录，而不是全局环境
- 当前仓库内产物对应最新一次正式测试：
  - `slides.md` 约 `18K`
  - `openclaw-intro.pdf` 约 `1.2M`
  - `openclaw-intro.pptx` 约 `1.9M`

本次测试走的是正式用户路径：

1. OpenClaw 发现并选择 `slidev-ppt-generator`
2. skill 初始化本地 Slidev 项目依赖
3. skill 生成 `slides.md`
4. skill 导出 PDF / PPTX 产物

触发时使用的请求形态：

- 中文示例：`帮我用 Slidev 做一个关于 OpenClaw 介绍的 PPT，生成 slides.md，并导出 PDF`
- 英文示例：`Create a Slidev deck about OpenClaw, generate slides.md, and export a PDF`

这份 demo 的提示策略不是把视觉细节写死在一次 prompt 里，而是分成两层：

- `SKILL.md`
  固定工作流、项目内依赖安装、导出要求、溢出检查、信息密度和版式护栏
- 用户请求
  决定主题、语言、页数、导出格式，以及本次表达风格（如 `formal`、`technical`）

如果要复现这份 demo，建议直接让 OpenClaw 触发 skill，而不是手工改 `slides.md`。
