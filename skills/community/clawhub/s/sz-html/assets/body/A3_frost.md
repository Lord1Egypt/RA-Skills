# A3 磨砂玻璃 · FROSTED GLASS

> 编号 `A3` · 族：**玻璃光影** · 调性：深色/暗底 · 组件类前缀 `.frost`

## 设计流派

磨砂玻璃（Frosted Glass）：毛玻璃 backdrop-blur、多彩渐变光斑、半透明卡片、轻盈通透

**关键词**：毛玻璃 · blur · 渐变光斑 · 半透明 · 通透

**一句话氛围**：通透的毛玻璃，光影在呼吸

## 配色 Token（可直接抄用）

| 变量 | 值 | 说明 |
| --- | --- | --- |
| 背景 `--bg` | `radial-gradient(circle at 18% 22%, rgba(138,109,242,.55), transparent 45%),
      radial-gradient(circle at 82% 28%, rgba(74,141,245,.45), transparent 50%),
      radial-gradient(circle at 62% 82%, rgba(255,125,179,.32), transparent 52%),
      radial-gradient(circle at 28% 76%, rgba(42,157,143,.30), transparent 48%),
      linear-gradient(135deg, #1b1633, #0d1226 58%, #060812)；渐变：radial-gradient(circle at 18% 22%, rgba(138,109,242,.55)` | 页面底色 |
| 文字 `--ink` | `#fff` | 主文字色 |
| 强调 `--ac` | `#8A6DF2` | 主强调/按钮/重点 |

**色板（4 色）**：`#fff` `#1b1633` `#0d1226` `#060812`

## 字体与排版

- 字体族：`var(--font)`
- 字号范围：10–48px（标题 48px 级）
- 字重：500 / 600 / 700

## 形状与特效

- 圆角：`3, 12, 24, 32, 999px`
- 阴影：`0 24px 70px rgba(0,0,0,.40)`
- 渐变：`radial-gradient(circle at 18% 22%, rgba(138,109,242,.55)`
- 特效：`blur(24px) saturate(140%)` `.04em` `.06em` `.03em`
- 动画关键帧：`frGlassBreath` `frSpot` `frRise`

## 组件样式特征

- 卡片：半透明背景 `rgba(255,255,255,.18)` + `backdrop-filter:blur(20px)`；圆角 24–32px；光影：径向渐变光斑；按钮：玻璃质感描边。

## 版式建议

- **适用演示场景**：科技新品 · App 发布 · SaaS 产品 · 开发者大会
- **明暗调性**：深色暗底（适合屏幕/沉浸）

---

> 本资产由「风格化待办工作台」49 风格系统提炼，供 sz-html 生成 HTML 演示文稿时注入。
