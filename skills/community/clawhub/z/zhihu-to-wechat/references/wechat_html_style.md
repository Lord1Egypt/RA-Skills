# 微信公众号 HTML 排版规范（IT科技风格）

## 核心约束

微信公众号编辑器对 HTML 有严格限制：

| 特性 | 支持情况 |
|------|----------|
| 内联 `style` 属性 | ✅ 完全支持 |
| `<style>` 标签 | ❌ **不支持**（会被过滤） |
| 外部 CSS 文件 | ❌ 不支持 |
| 外部字体（Google Fonts等）| ❌ 不支持 |
| 外链图片 | ❌ **必须上传到微信CDN** |
| SVG | ⚠️ 部分支持，建议转 PNG |
| `<script>` | ❌ 不支持 |
| `<iframe>` | ❌ 不支持 |
| CSS 变量 `var()` | ❌ 不支持 |
| `calc()` | ⚠️ 部分支持 |
| Flexbox / Grid | ⚠️ 部分支持，需测试 |

---

## IT科技风配色方案

```
主色（科技蓝）:   #1a6ff4
辅色（科技紫）:   #6c3be8
代码背景:         #1e1e2e  (Catppuccin Mocha 风格)
代码文字:         #cdd6f4
引用背景:         #f0f4ff
正文文字:         #333333
次要文字:         #666666
边框:             #e8edf5
```

渐变公式（标题装饰）：
```css
background: linear-gradient(135deg, #1a6ff4, #6c3be8);
```

---

## 推荐内联样式片段

### 文章容器
```html
<section style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; font-size: 16px; line-height: 1.75; color: #333; max-width: 677px; margin: 0 auto; padding: 0 16px; word-break: break-word;">
```

### 一级标题（文章标题）
```html
<h1 style="font-size: 22px; font-weight: bold; color: #1a6ff4; text-align: center; padding: 16px 0 8px; margin: 0 0 24px; border-bottom: 2px solid #1a6ff4; letter-spacing: 1px;">
```

### 二级标题（章节标题）
```html
<h2 style="font-size: 18px; font-weight: bold; color: #1a6ff4; margin: 28px 0 12px; padding: 0 0 0 12px; border-left: 4px solid #1a6ff4; background: linear-gradient(90deg, #f0f4ff, transparent);">
```

### 正文段落
```html
<p style="font-size: 16px; line-height: 1.8; color: #333; margin: 0 0 16px; text-align: justify;">
```

### 代码块（深色主题）
```html
<pre style="font-family: Menlo, Monaco, Consolas, monospace; font-size: 13px; background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0; line-height: 1.6; white-space: pre;">
```

### 行内代码
```html
<code style="font-family: Menlo, Monaco, Consolas, monospace; font-size: 14px; background: #f0f4ff; color: #6c3be8; padding: 2px 6px; border-radius: 3px;">
```

### 引用块
```html
<blockquote style="background: #f0f4ff; border-left: 4px solid #1a6ff4; margin: 16px 0; padding: 12px 16px; border-radius: 0 8px 8px 0; color: #666; font-style: italic;">
```

### 重要提示框（信息框）
```html
<div style="background: linear-gradient(135deg, #f0f4ff, #f5f0ff); border: 1px solid #e8edf5; border-radius: 12px; padding: 16px; margin: 16px 0;">
  <strong style="color: #1a6ff4;">💡 提示：</strong>内容
</div>
```

### 图片
```html
<img src="微信CDN地址" alt="描述" style="width: 100%; border-radius: 8px; margin: 16px 0; display: block;" />
<p style="text-align: center; font-size: 13px; color: #999; margin: -8px 0 16px;">▲ 图片说明</p>
```

### CTA 按钮区域（结尾互动引导）
```html
<div style="background: linear-gradient(135deg, #1a6ff4, #6c3be8); color: white; text-align: center; padding: 16px; border-radius: 12px; margin: 24px 0; font-size: 15px; font-weight: bold;">
  👋 觉得有用？点个「在看」支持一下<br/>
  💬 欢迎在留言区分享你的看法
</div>
```

### 标签
```html
<span style="display: inline-block; background: linear-gradient(135deg, #1a6ff4, #6c3be8); color: white; font-size: 12px; padding: 2px 10px; border-radius: 12px; margin: 0 4px 8px 0;">#标签名</span>
```

---

## 图片尺寸规范

| 用途 | 推荐尺寸 | 备注 |
|------|----------|------|
| 封面图（头图）| 900×500px 或 16:9 | 在文章列表显示 |
| 正文配图 | 宽 900px，高度不限 | 自适应宽度 |
| 小图标/表情 | 40×40px | inline 使用 |

---

## 字体回退链

微信公众号不支持自定义字体，使用系统字体栈：

```css
font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, 
             'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
```

- iOS/macOS：PingFang SC（苹方）
- Android：Noto Sans CJK
- Windows：微软雅黑

---

## 排版最佳实践

1. **每段不超过 150 字**，移动端阅读友好
2. **多用小标题分割**，方便快速扫读
3. **数字用阿拉伯数字**：「5 个原因」比「五个原因」更抓眼球
4. **适当使用 emoji**：增加活跃感，但不要堆砌（每 H2 最多 1 个）
5. **重点词加粗**：每段最多 1-2 处，不要满屏加粗
6. **避免纯文字大段落**：超过 3 段就加一张图或引用块打断节奏
