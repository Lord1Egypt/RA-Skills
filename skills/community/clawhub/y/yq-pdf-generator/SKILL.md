---
name: yq-pdf-generator
description: 将任意HTML内容（网页链接、演示文稿、HTML文件）转换为PDF文件。当用户说"生成PDF"、"导出PDF"、"转PDF"、"下载PDF"、"html转PDF"、"导出PDF文件"时触发此技能。
version: 1.0.0
---

# PDF Generator — 已验证方案

> ⚠️ 注意：本技能的PDF导出是**"部署HTML + 用户本地浏览器Ctrl+P导出"**。
> 这与"上传图片到CDN"是完全不同的操作，不要混淆。
>
> 本方案经验证（2026-03-24 UE特效师成长计划、2026-03-30 ComfyUI学习路线）效果良好，已固化为此技能的**唯一标准方案**。

---

## 触发条件
- 用户说"生成PDF"、"导出PDF"、"转PDF"、"下载PDF"、"导出PDF文件"
- 用户提供了HTML文件需要转PDF
- 用户提供了URL需要转PDF

---

## ✅ 标准工作流程（默认唯一方案，2026-03-30确立）

### Step 1：准备HTML文件
在 /workspace/dist/index.html 写入完整HTML内容（包含内联CSS和@media print打印样式）

```bash
# 已有HTML文件时复制到部署目录
cp /workspace/源文件.html /workspace/dist/index.html
```

**@media print 样式必须在HTML中包含（否则导出会变白底）：**
```css
@media print {
  html, body { background: #0d0d1a !important; color: #e8eaf0 !important; }
  .module { background: rgba(255,255,255,0.03) !important; }
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
```

### Step 2：部署
```
deploy --dist_dir /workspace/dist --project_name "项目名称"
```

### Step 3：返回结果给用户

**标准话术（直接复制发给用户）：**
```
📎 已为您生成可下载/导出的页面！

👉 [部署URL]

导出PDF步骤：
1. 点击上方链接打开页面
2. 按 Ctrl+P（Mac：Cmd+P）
3. 打印机选择"另存为PDF"
4. 布局选"横向"（适合文档风格）
5. 务必勾选"背景图形"（否则背景色会变白）
6. 点击保存

该链接长期有效，可随时收藏使用。
```

---

## ⚠️ 禁止事项

- ❌ 不要用 `upload_to_cdn` 来"生成PDF"——CDN只上传文件，不生成PDF
- ❌ 不要说"上传图片"——图片上传和PDF导出是两件事
- ❌ 不要在服务器端用Playwright生成PDF——服务器无GUI浏览器，效果差且不稳定
- ❌ 不要在无深色背景的HTML里导出——打印效果会很差

---

## 适用场景判断

| 场景 | 方案 | 说明 |
|------|------|------|
| HTML文档/资料转PDF | 部署+Ctrl+P ✅ | 最佳效果，用户本地渲染，支持深色背景 |
| 演示文稿/学习路线 | 部署+Ctrl+P ✅ | 支持分页和背景，样式完整保留 |
| 图片集打包为PDF | **不要用本技能** | 图片PDF用其他工具，本技能专用于HTML内容 |

---

## 深色主题HTML打印模板（可直接复用）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>文档标题</title>
<style>
body {
  font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  background: #0d0d1a;
  color: #e8eaf0;
  font-size: 13px;
}
@media print {
  html, body {
    background: #0d0d1a !important;
    color: #e8eaf0 !important;
    width: 100%;
    margin: 0 !important;
    padding: 0 !important;
  }
  .module {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
</style>
</head>
<body>
<!-- 内容 -->
</body>
</html>
```

---

## 效果验证记录

| 日期 | 内容 | 效果 |
|------|------|------|
| 2026-03-24 | UE特效师成长计划 | ✅ 深色背景完整保留，用户体验良好 |
| 2026-03-30 | ComfyUI学习路线 | ✅ 链接长期有效，用户自行Ctrl+P导出 |

---

## 关键文件路径

- 临时部署目录：`/workspace/dist/index.html`（每次使用前直接覆盖）
- HTML源文件备份：保留在用户指定路径或 /workspace/dist/

