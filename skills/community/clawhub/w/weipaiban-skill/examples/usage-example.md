# 使用示例

用户："请帮我用微排版创建一个清明节的微信图文"

执行流程：

1. 提取分类标签和关键词：标签 `节日`，关键词"清明"。创建任务目录 `/tmp/weipaiban-task-tmp-{时间戳}/`，写入 `meta.json`
2. 搜索模板：分别执行仅关键词搜索（`search=清明`）和仅标签搜索（`tags=节日`），每路各取前 5，按模板 ID 去重合并
3. 展示最多 10 个候选模板，用户选择一个。更新 `meta.json` 的 templateId
4. 从模板创建新作品，重命名任务目录为 `/tmp/weipaiban-task-{作品ID}/`
5. 获取简化元素（文本、矩形色块、图片、轮播），写入 `elements.json`
6. 自动分析模板画像（排版类型、色系、密度），写入 `template-profile.json`
7. 根据清明节主题生成清新绿色系配色方案，替换 rect 和 text 的颜色。用户确认后写入 `color-changes.json`
8. 为每个文本生成清明节主题的新内容。用户确认后写入 `text-changes.json`
9. 分析每张图片的用途和内容（通过名称、尺寸、视觉识别），分类为场景背景/人物/装饰等，跳过 logo 和二维码。用户确认后写入 `image-classifications.json`
10. 为每张图片构造分类专属的生成 prompt，写入 `image-prompts.json`，初始化 `image-progress.json`
11. 逐张调用即梦 API 生成图片，每张完成后即时反馈进度
12. 对需要透明背景的图片逐张执行 rembg 白底转透明
13. 逐张上传到微排版 CDN，展示汇总结果，失败可重试
14. 从 `color-changes.json`、`text-changes.json`、`image-progress.json` 汇总所有变更，批量更新作品
15. 返回编辑链接给用户
