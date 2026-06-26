# HTML 图表风格规范

技术文章中的 HTML 图表必须遵循统一风格。不要用 ASCII art 代替——HTML 图在博客平台上渲染效果远好于代码块里的 ASCII。

## 基础容器

每个图表包裹在一个统一容器里：

```html
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;margin:20px 0;background:#fafafa;border:1px solid #e5e7eb;border-radius:12px;padding:24px">
<div style="text-align:center;font-weight:700;font-size:15px;color:#111;margin-bottom:20px">图表标题</div>
<!-- 内容 -->
</div>
```

关键属性：
- `background:#fafafa` 浅灰底，不用白底（白底和页面融合，看不出边界）
- `border:1px solid #e5e7eb` 细边框
- `border-radius:12px` 圆角
- `padding:24px` 内边距
- `font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif` 系统字体栈
- `font-size:13px` 基础字号
- 标题 `font-size:15px;font-weight:700;color:#111` 居中

## 层级区块

分层架构图、路由表等用层级区块：

```html
<div style="border-radius:8px;padding:14px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:6px">LAYER 1 · 层名称</div>
<div style="font-size:12px;color:#666;margin-bottom:6px">描述文字</div>
<!-- 药丸标签 -->
</div>
```

关键属性：
- 层级标签：`font-size:11px;font-weight:700;letter-spacing:1px` 大写风格
- 层间连接：`<div style="text-align:center;color:#bbb;font-size:11px">↓ 连接说明</div>`

## 药丸标签

工具名、关键词用药丸标签：

```html
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:4px 10px;font-size:12px">标签文字</span>
```

- `border-radius:6px` 圆角
- `padding:4px 10px` 或 `padding:3px 8px`（紧凑版）
- `font-size:12px` 或 `font-size:11px`（紧凑版）

## 颜色系统

6 种语义颜色，每种有 浅底 + 边框 + 文字 三色：

| 语义 | 浅底 background | 边框 border | 文字 color | 适用场景 |
|------|-----------------|-------------|-----------|---------|
| 绿色 | `#f0fdf4` / `#dcfce7` | `#86efac` | `#16a34a` | 成功、推荐、通过 |
| 蓝色 | `#eff6ff` / `#dbeafe` | `#93c5fd` | `#3b82f6` | 信息、中性、常规 |
| 黄色 | `#fefce8` / `#fef3c7` | `#fde68a` | `#a16207` | 警告、注意、中间态 |
| 红色 | `#fef2f2` / `#fee2e2` | `#fca5a5` | `#dc2626` | 错误、失败、危险 |
| 紫色 | `#faf5ff` / `#ede9fe` | `#c4b5fd` | `#7c3aed` | 基础层、运行时 |
| 灰色 | `#fafafa` / `#f3f4f6` | `#e5e7eb` | `#111` / `#666` | 容器、说明文字 |

## 左右对比图

好做法 vs 差做法的对比用 flex 布局：

```html
<div style="display:flex;gap:12px;flex-wrap:wrap">
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#fef2f2;border:1px solid #fca5a5">
<div style="font-size:11px;color:#dc2626;font-weight:700;letter-spacing:1px;margin-bottom:10px">差做法标题</div>
<!-- 内容 -->
</div>
<div style="flex:1;min-width:250px;border-radius:8px;padding:14px;background:#f0fdf4;border:1px solid #86efac">
<div style="font-size:11px;color:#16a34a;font-weight:700;letter-spacing:1px;margin-bottom:10px">好做法标题</div>
<!-- 内容 -->
</div>
</div>
```

## 条形对比图

数值对比用条形：

```html
<div style="display:flex;align-items:center;gap:10px">
<div style="width:80px;text-align:right;font-size:12px;font-weight:600;color:#dc2626">标签 A</div>
<div style="flex:1;background:#fef2f2;border:1px solid #fca5a5;border-radius:6px;padding:8px 12px">
<div style="background:#fca5a5;border-radius:4px;height:8px;width:100%"></div>
<div style="font-size:11px;color:#991b1b;margin-top:4px"><b>数值</b> 说明</div>
</div>
</div>
```

- 用纯色条 `height:8px`，不用渐变（`linear-gradient` 在部分平台渲染异常）
- 用 `width` 百分比表达相对比例

## 流程图

流程节点用药丸标签 + 箭头连接：

```html
<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center">
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:6px 12px;font-size:12px"><b>步骤 1</b></span>
<span style="color:#bbb">→</span>
<span style="background:#dbeafe;border:1px solid #93c5fd;border-radius:6px;padding:6px 12px;font-size:12px"><b>步骤 2</b></span>
<span style="color:#bbb">→</span>
<span style="background:#dcfce7;border:2px solid #86efac;border-radius:6px;padding:6px 12px;font-size:12px;font-weight:600;color:#16a34a"><b>关键步骤</b></span>
</div>
```

- 箭头用 `→` 字符，颜色 `#bbb`
- 垂直箭头用 `↓`，放在 `text-align:center` 的 div 里
- 关键节点用 `border:2px solid` + 加粗颜色突出

## 禁止事项

- 不用 emoji（去掉 ❌ ✅ 🔑 🌐 等，用文字或颜色区分）
- 不用 `linear-gradient`（部分平台渲染异常）
- 不用 `position:absolute`（响应式布局容易错位）
- 不用 `box-shadow`（部分博客平台不渲染）
- 不用 `max-width` 固定像素（用容器自适应）
- 不在图里放大段文字（图是视觉速读，详细说明放正文）
