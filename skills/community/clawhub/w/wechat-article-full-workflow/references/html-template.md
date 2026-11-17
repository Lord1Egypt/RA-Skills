# 微信公众号文章 HTML 模板与排版规范

## 完整骨架模板

以下是可直接使用的 HTML 骨架。所有样式必须内联。

```html
<section style="max-width: 680px; margin: 0 auto; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; font-size: 16px; line-height: 1.8; color: #333;">

  <!-- 标题 -->
  <h1 style="font-size: 22px; font-weight: 700; text-align: center; margin-bottom: 24px; color: #1a1a1a;">标题（≤8中文字）</h1>

  <!-- 正文段落 -->
  <p style="margin-bottom: 16px; text-indent: 0;">段落内容...</p>

  <!-- 小标题 -->
  <h2 style="font-size: 18px; font-weight: 600; margin: 28px 0 14px; padding-left: 10px; border-left: 3px solid #4a90d9; color: #1a1a1a;">小标题</h2>

  <!-- 配图占位符（必须带width/height） -->
  <section style="margin: 20px 0; text-align: center;">
    <img width="600" height="338" data-src="IMAGE_PLACEHOLDER_01" alt="配图描述" style="max-width: 100%; height: auto; border-radius: 4px;" />
  </section>

  <!-- 列表（用table模拟，不用ul/ol） -->
  <section style="margin: 16px 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr>
        <td style="width: 24px; vertical-align: top; padding: 6px 8px 6px 0; font-weight: 700; color: #4a90d9;">1.</td>
        <td style="padding: 6px 0; line-height: 1.8;">列表项内容...</td>
      </tr>
    </table>
  </section>

  <!-- 引用/高亮框 -->
  <section style="margin: 20px 0; padding: 16px; background: #f5f7fa; border-radius: 6px; border-left: 3px solid #4a90d9;">
    <p style="margin: 0; font-size: 15px; color: #555;">引用或高亮内容...</p>
  </section>

  <!-- 分隔线 -->
  <section style="margin: 30px 0; border-top: 1px solid #eee;"></section>

  <!-- 结尾引导关注 -->
  <section style="text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid #eee;">
    <p style="font-size: 14px; color: #999; margin-bottom: 12px;">关注公众号，获取更多AI实操经验</p>
    <img width="200" height="200" data-src="QR_CODE_PLACEHOLDER" alt="公众号二维码" style="width: 200px; height: 200px; border-radius: 4px;" />
    <p style="font-size: 13px; color: #bbb; margin-top: 8px;">长按识别二维码关注</p>
  </section>

</section>
```

## 排版避坑速查表

| 类别 | ❌ 不可用 | ✅ 替代方案 |
|------|----------|-----------|
| CSS | `class="xxx"` | 全部写内联 `style="..."` |
| CSS | `<style>` 标签 | 禁止，微信会剥离 |
| 布局 | `display:flex` | `<table>` 布局 |
| 布局 | `display:grid` | `<table>` 布局 |
| 计算 | `calc()` | 写死像素值 |
| 图片 | base64 内嵌 | 上传微信素材库，用CDN URL |
| 图片 | `<img>` 无width/height | 必须加 `width="600" height="338"` |
| 图片 | `http://` URL | 用 `https://` |
| 骨架 | `<!DOCTYPE>` | 禁止，只需 `<section>` 片段 |
| 骨架 | `<html>`, `<head>`, `<body>` | 禁止 |

## 图片占位符规范

文章配图使用以下命名（7张标准配图）：

| 占位符 | 章节 |
|--------|------|
| `IMAGE_PLACEHOLDER_01` | 开场/概念引入 |
| `IMAGE_PLACEHOLDER_02` | 产品介绍/功能展示 |
| `IMAGE_PLACEHOLDER_03` | 零门槛/易上手 |
| `IMAGE_PLACEHOLDER_04` | 核心能力展示 |
| `IMAGE_PLACEHOLDER_05` | 生态联动 |
| `IMAGE_PLACEHOLDER_06` | 多功能/全场景 |
| `IMAGE_PLACEHOLDER_07` | 安全/进化/信任 |

结尾二维码：
| 占位符 | 用途 |
|--------|------|
| `QR_CODE_PLACEHOLDER` | 公众号二维码（200x200） |

## 二维码图片路径

`请替换为你本地的二维码图片路径`

所有文章末尾统一使用此图片，推送时自动上传替换。
