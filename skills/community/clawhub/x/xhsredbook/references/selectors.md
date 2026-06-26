# 小红书创作者中心选择器参考

> 最后更新: 2026-03-06

## 页面结构

- URL: `https://creator.xiaohongshu.com/publish/publish`
- 默认 tab: 上传视频
- 需要切换到: 上传图文

## 关键选择器

### Tab 切换
- 下拉箭头: `.dropdownBtn`
- 发布笔记按钮: `span.btn-text:has-text("发布笔记")`
- 上传图文 tab: `get_by_text("上传图文")` (多个元素，需通过 bounding_box 找可见的)
- creator-tab: `.creator-tab:has-text("上传图文")`

### 文件上传
- 视频 input: `input[type="file"][accept=".mp4,.mov,.flv,..."]`
- 图片 input: `input[type="file"][accept=".jpg,.jpeg,.png,.webp"]`
- 注意: 切换到图文 tab 后才会出现图片 input

### 内容编辑
- 正文编辑器: `[contenteditable="true"]`
- 标题输入: `input[placeholder*="标题"]`

### 发布
- 发布按钮: `button:has-text("发布")`
- 智能标题: `button:has-text("智能标题")` (可能不存在)

## 注意事项

1. "上传图文"元素有多个，部分被 CSS 隐藏 (`position: absolute; left: -9999px`)
2. 图片上传后需要等待编辑器出现（轮询 + 滚动）
3. 多张图片需要逐张上传，每张间隔等待
4. persistent context 可能记住上次的 tab 选择
