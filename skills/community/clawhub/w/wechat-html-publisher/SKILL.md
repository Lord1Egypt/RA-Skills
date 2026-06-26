---
name: wechat-html-publisher
description: "直接上传HTML富文本到微信公众号草稿箱。支持完整的HTML格式,无需Markdown转换。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
      },
  }
---

# wechat-html-publisher

**直接上传HTML富文本到微信公众号草稿箱**

与 wechat-publisher 不同,本skill直接上传HTML格式,无需Markdown转换。适合已经有完整HTML排版的文章。

## 功能

- ✅ 直接上传HTML富文本
- ✅ 自动上传HTML中的图片到微信图床
- ✅ 支持本地和网络图片
- ✅ 一键推送到草稿箱
- ✅ 无需Markdown转换

## 快速开始

### 1. 配置API凭证

确保环境变量已设置:
```bash
export WECHAT_APP_ID= YOU_WECHAT_APP_ID
export WECHAT_APP_SECRET= YOU_WECHAT_APP_SECRET
```

**重要:** 确保你的IP已添加到微信公众号后台的白名单!

### 2. 准备HTML文件

HTML文件需要包含完整的样式(内联样式):

```html
<section>
  <h1 style="color: #333; font-size: 24px;">文章标题</h1>
  <p style="line-height: 1.8;">文章内容...</p>
  <img src="./images/photo.jpg" style="width: 100%;">
</section>
```

**注意:**
- 必须使用内联样式(style属性)
- 不支持`<style>`标签或外部CSS
- 图片会自动上传到微信图床

### 3. 发布文章

**使用脚本:**
```bash
python scripts/publish_html.py \
  --file article.html \
  --title "文章标题" \
  --cover ./cover.jpg
```

**参数说明:**
- `--file`: HTML文件路径(必填)
- `--title`: 文章标题(必填)
- `--cover`: 封面图路径(必填)
- `--author`: 作者名称(可选)
- `--digest`: 文章摘要(可选)
- `--source-url`: 原文链接(可选)

## 使用示例

### 示例1: 基本用法
```bash
python scripts/publish_html.py \
  --file my-article.html \
  --title "2026年税务新政解读" \
  --cover ./cover.jpg
```

### 示例2: 完整参数
```bash
python scripts/publish_html.py \
  --file my-article.html \
  --title "2026年税务新政解读" \
  --cover ./cover.jpg \
  --author "慧评税" \
  --digest "详细解读2026年最新税务政策" \
  --source-url "https://example.com/article"
```

### 示例3: 网络封面图
```bash
python scripts/publish_html.py \
  --file my-article.html \
  --title "文章标题" \
  --cover "https://example.com/cover.jpg"
```

## HTML格式要求

### 1. 必须使用内联样式
```html
<!-- ✅ 正确 -->
<p style="color: #333; font-size: 16px;">内容</p>

<!-- ❌ 错误 -->
<style>
  p { color: #333; }
</style>
<p>内容</p>
```

### 2. 图片支持
- ✅ 本地路径: `<img src="./images/photo.jpg">`
- ✅ 绝对路径: `<img src="/Users/user/photo.jpg">`
- ✅ 网络图片: `<img src="https://example.com/photo.jpg">`

所有图片会自动上传到微信图床并替换URL!

### 3. 推荐的HTML结构
```html
<section>
  <section style="text-align: center;">
    <h1 style="font-size: 24px; color: #333;">标题</h1>
  </section>
  
  <section style="margin: 20px 0;">
    <p style="line-height: 1.8; color: #666;">正文内容...</p>
  </section>
  
  <section>
    <img src="./image.jpg" style="width: 100%; display: block;">
  </section>
</section>
```

## 工作流程

1. **读取HTML** - 读取HTML文件内容
2. **上传封面** - 上传封面图到微信图床
3. **处理图片** - 解析HTML中的图片,上传并替换URL
4. **调用API** - 调用微信draft/add接口
5. **返回结果** - 返回草稿media_id

## 与wechat-publisher的区别

| 特性 | wechat-publisher | wechat-html-publisher |
|------|------------------|----------------------|
| 输入格式 | Markdown | HTML |
| 样式转换 | 自动应用主题 | 使用原有样式 |
| 适用场景 | 写作发布 | 已有HTML排版 |
| 依赖 | wenyan-cli | 仅Python |

## 故障排查

### 1. IP不在白名单
**错误:** `ip not in whitelist`

**解决:**
1. 获取公网IP: `curl ifconfig.me`
2. 添加到微信公众号后台白名单

### 2. 图片上传失败
**错误:** `invalid image`

**解决:**
- 检查图片格式(支持jpg, png, gif)
- 检查图片大小(不超过2MB)
- 确保图片路径正确

### 3. HTML格式错误
**错误:** `invalid content`

**解决:**
- 确保使用内联样式
- 移除`<style>`标签
- 检查HTML是否闭合

## 参考资料

- 微信公众号API文档: https://developers.weixin.qq.com/doc/offiaccount/
- 草稿箱接口: https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
- 素材管理接口: https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html

## 更新日志

### 2026-03-09 - v1.0.0
- ✅ 初始版本
- ✅ 支持HTML直接上传
- ✅ 自动图片上传
- ✅ 命令行工具

## License

MIT License
