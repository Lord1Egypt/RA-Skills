# 微信公众号文章发布工具

把精心排版的 HTML 文章直接推送到公众号草稿箱，**完整保留所有内联 CSS 样式**。

## 为什么需要这个工具

公众号编辑器的复制粘贴会过滤掉大量 CSS 样式（渐变、圆角、阴影等），导致排版全部丢失。

而通过**微信公众号 API 直接创建草稿**，HTML 内联样式可以完整保留——这正是 135编辑器、秀米等专业排版工具的"保存同步"功能背后的原理。

## 快速开始

### 第一步：配置公众号信息

```bash
cd wechat-publisher
cp config.example.json config.json
```

编辑 `config.json`，填入你的公众号信息：

```json
{
  "appId": "你的AppID",
  "appSecret": "你的AppSecret",
  "title": "文章标题",
  "author": "作者名",
  "thumbImagePath": "../cover.png"
}
```

**获取 AppID 和 AppSecret：**
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 左侧菜单 → **设置与开发** → **基本配置**
3. 在「开发者ID」区域找到 AppID 和 AppSecret
4. **重要：** 把你电脑的公网 IP 加到「IP白名单」里
   - 不知道公网 IP？打开 https://www.whatismyip.com 查看

### 第二步：准备封面图

封面图二选一：
- **方式 A**：设置 `thumbImagePath` 指向本地图片，脚本自动上传
- **方式 B**：在公众号后台手动上传图片，拿到 media_id 填入 `thumbMediaId`

### 第三步：预览效果

```bash
node preview.js
```

浏览器打开 http://localhost:3456 查看文章在公众号环境中的模拟效果。

### 第四步：推送到草稿箱

```bash
node publish.js
```

推送成功后，去公众号后台 → 草稿箱 查看，确认效果后点击「发布」。

## 发布其他文章

```bash
# 指定其他 HTML 文件
node publish.js /path/to/other-article.html
```

每次发布前记得更新 `config.json` 中的 `title`、`author`、`digest` 等字段。

## 文章 HTML 编写规范

为了确保在公众号中效果最好，HTML 需要遵循以下规范：

### 推荐使用的 CSS 属性
- `color`、`background-color`（纯色）
- `font-size`、`font-weight`、`line-height`、`letter-spacing`
- `margin`、`padding`
- `border`、`border-radius`、`border-left` 等
- `text-align`
- `box-shadow`
- `display: inline-block`
- `width`、`height`（固定尺寸）
- `vertical-align`

### 避免使用的 CSS 属性
- `position: fixed/absolute`（会被过滤）
- `background: linear-gradient()`（渐变不可靠）
- `transform`、`transition`、`animation`
- `font-family`（可能导致其他样式被一起丢弃）
- `@media` 查询
- 外部 CSS（`<style>` 标签）

### 关键技巧
1. **所有样式必须内联**（写在 `style=""` 属性里）
2. **图片 URL 必须使用微信接口上传后的地址**（外部图片会被过滤）
3. **HTML 会自动压缩**——脚本会去除换行和多余空格，防止公众号后台插入干扰标签

## 工作流程

```
写 Markdown  →  生成排版精美的 HTML  →  本地预览  →  API 推送到草稿箱  →  公众号后台确认发布
```

后续每篇新文章只需要改 HTML 内容和 config.json 中的标题信息，一条命令就能推送。
