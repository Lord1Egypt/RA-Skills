# Shoelace Design Token 速查表

编写 CSS 样式时，颜色、间距、字号、圆角等属性**必须**优先使用以下 Shoelace Design Token（CSS 自定义属性），**禁止**直接写死 hex 色值或 px 数值。这确保组件在主题切换、品牌定制时能自动适配。

> **注意**：下方表格仅列出最常用的 Token。Shoelace 提供的完整 Token 远多于此。当下方表格中没有合适的 Token 时，**必须**查阅 Shoelace 官方文档获取完整列表：
> - 颜色 Token: https://shoelace.style/tokens/color
> - 间距 Token: https://shoelace.style/tokens/spacing
> - 字号 Token: https://shoelace.style/tokens/typography
> - 圆角 Token: https://shoelace.style/tokens/border-radius
> - 其他 Token（阴影、过渡、层级等）: https://shoelace.style/tokens/elevation

## 颜色 Token

| 用途 | Token | 参考值 |
|------|-------|--------|
| 主文字色 | `var(--sl-color-neutral-700)` | ~#333 |
| 次要文字色 | `var(--sl-color-neutral-600)` | ~#666 |
| 辅助/禁用色 | `var(--sl-color-neutral-500)` | ~#999 |
| 边框色 | `var(--sl-color-neutral-300)` | ~#ccc |
| 分割线色 | `var(--sl-color-neutral-200)` | ~#e8e8e8 |
| 浅背景色 | `var(--sl-color-neutral-100)` | ~#f5f5f5 |
| 卡片背景 | `var(--sl-color-neutral-50)` | ~#fafafa |
| 白色背景 | `var(--sl-color-neutral-0)` | ~#fff |
| 品牌/链接色 | `var(--sl-color-primary-600)` | ~#1890ff |
| 成功色 | `var(--sl-color-success-600)` | ~#52c41a |
| 危险色 | `var(--sl-color-danger-600)` | ~#ff4d4f |
| 警告色 | `var(--sl-color-warning-600)` | ~#faad14 |

各语义色均有 50~950 色阶，浅色背景用 50/100，边框用 200/300，文字/图标用 600。

## 间距 Token（用于 padding / margin / gap）

| Token | 值 |
|-------|-----|
| `var(--sl-spacing-2x-small)` | 4px |
| `var(--sl-spacing-x-small)` | 8px |
| `var(--sl-spacing-small)` | 12px |
| `var(--sl-spacing-medium)` | 16px |
| `var(--sl-spacing-large)` | 20px |

## 字号 Token（用于 font-size）

| Token | 值 |
|-------|-----|
| `var(--sl-font-size-x-small)` | 12px |
| `var(--sl-font-size-small)` | 14px |
| `var(--sl-font-size-medium)` | 16px |

## 圆角 Token（用于 border-radius）

| Token | 值 |
|-------|-----|
| `var(--sl-border-radius-medium)` | 4px |
| `var(--sl-border-radius-large)` | 8px |

## 正确 vs 错误示例

```css
/* ✗ 错误 - 硬编码 */
.panel {
  color: #333;
  padding: 16px;
  font-size: 14px;
  border-radius: 4px;
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
}

/* ✓ 正确 - 使用 Design Token */
.panel {
  color: var(--sl-color-neutral-700);
  padding: var(--sl-spacing-medium);
  font-size: var(--sl-font-size-small);
  border-radius: var(--sl-border-radius-medium);
  background: var(--sl-color-neutral-100);
  border: 1px solid var(--sl-color-neutral-300);
}
```

## 允许硬编码的例外情况
- 布局固定尺寸：`width`、`height`、`max-width`、`min-height` 等
- 行高：`line-height` 的具体值
- 边框宽度：`border: 1px solid ...` 中的 `1px`
- 无对应 token 的数值（如 `24px`、`13px`）
- 主题定制场景中覆盖组件 CSS 变量的特定设计稿色值
