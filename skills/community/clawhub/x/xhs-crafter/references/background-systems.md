# Background Systems

> xhs-crafter 背景系统规范——grain纹理、paper-wash水洗、WebGL流体
> 画布基准：1080 × 1440（3:4）

---

## 三层背景架构

Editorial Magazine 页面使用三层背景叠加，从底到顶：

```
┌─────────────────────────────────────┐
│  Layer 3: grain（纹理）              │  z-index: 2, pointer-events: none
│  ┌─────────────────────────────────┐│
│  │  Layer 2: content（内容）        ││  z-index: 1
│  │  ┌─────────────────────────────┐││
│  │  │  Layer 1: paper-wash（水洗） │││  z-index: 0
│  │  │  ┌─────────────────────────┐│││
│  │  │  │  Layer 0: paper（底色）  ││││  background: var(--paper)
│  │  │  └─────────────────────────┘│││
│  │  └─────────────────────────────┘││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**禁止使用纯平背景**——Editorial 的核心美学是"纸墨感"，flat beige 会显得死板。

---

## Layer 0: Paper（底色）

由 `--paper` CSS 变量控制，每个主题预设自带。

```css
.poster {
  background: var(--paper);
}
```

**硬规则**：
- `--paper` 永远不是 `#FFFFFF`——纯白刺眼，印刷行业从不使用
- `--paper` 永远不是 `#000000`——纯黑暴力，Midnight Ink 用 `#0e0d0c`

---

## Layer 1: Paper-Wash（水洗层）

径向渐变叠加，模拟纸张的不均匀吸墨效果。

### Light 主题（默认）

```css
.paper-wash {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(ellipse at 20% 80%, var(--wash-color) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, var(--wash-color) 0%, transparent 50%),
    linear-gradient(var(--wash-angle), transparent 0%, var(--wash-color) 100%);
}
```

默认变量：
```css
:root {
  --wash-color: rgba(10, 31, 61, .02);
  --wash-angle: 160deg;
}
```

### Midnight Ink 主题（覆盖）

```css
[data-theme="midnight-ink"] .paper-wash {
  background:
    radial-gradient(80% 50% at 28% 16%, rgba(212, 160, 74, .12), transparent 64%),
    radial-gradient(70% 60% at 80% 86%, rgba(60, 40, 20, .20), transparent 72%),
    linear-gradient(180deg, rgba(236, 226, 207, .02), rgba(0, 0, 0, .32));
}
```

**硬规则**：
- Light 主题的 wash-color 透明度 ≤.03——若隐若现，不是渐变背景
- Midnight Ink 的暖光斑必须偏左上角（28% 16%），模拟台灯照射

---

## Layer 2: Grain（纹理层）

模拟纸张纤维/印刷网点的细微纹理。

### Light 主题（默认）

```css
.grain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
  opacity: var(--grain-opacity);
  mix-blend-mode: var(--grain-blend);
  background-image:
    radial-gradient(circle at 17% 32%, rgba(0,0,0,.15) 0%, transparent 50%),
    radial-gradient(circle at 72% 18%, rgba(0,0,0,.10) 0%, transparent 40%),
    radial-gradient(circle at 45% 78%, rgba(0,0,0,.12) 0%, transparent 45%),
    radial-gradient(circle at 88% 55%, rgba(0,0,0,.08) 0%, transparent 35%);
}
```

默认变量：
```css
:root {
  --grain-opacity: .04;
  --grain-blend: multiply;
}
```

### Midnight Ink 主题（覆盖）

```css
[data-theme="midnight-ink"] .grain {
  opacity: .26;
  mix-blend-mode: screen;
  background-image:
    radial-gradient(rgba(255, 244, 214, .10) 1px, transparent 1px);
}
```

**硬规则**：
- Light 主题 grain-opacity ≤.06——纹理是暗示，不是噪点
- Midnight Ink grain-opacity .26 + screen 混合——暗色页需要更明显的纹理才不会死板
- grain 不得降低文字可读性——如果正文变模糊，降低 opacity

---

## 氛围强度分级

不同页面角色使用不同氛围强度：

| 页面角色 | 氛围强度 | grain-opacity | paper-wash | 说明 |
|---------|---------|---------------|------------|------|
| 封面 | Strong | .06 | 全部3层 | 封面需要氛围感 |
| 引言/引语 | Strong | .06 | 全部3层 | 引用页需要仪式感 |
| 封底 | Strong | .06 | 全部3层 | 收尾需要余韵 |
| 数据/清单 | Subtle | .02 | 仅1层 | 数据页需要清晰 |
| 正文/essay | Medium | .04 | 2层 | 阅读页需要舒适 |

**CSS 实现**：

```css
/* Strong 氛围（封面/引言/封底） */
.poster.atmosphere-strong .grain { opacity: .06; }
.poster.atmosphere-strong .paper-wash { opacity: 1; }

/* Subtle 氛围（数据/清单） */
.poster.atmosphere-subtle .grain { opacity: .02; }
.poster.atmosphere-subtle .paper-wash { opacity: .3; }
```

---

## 满铺图页背景

封面和封底使用满铺背景图时，背景系统简化：

```
┌─────────────────────────────────────┐
│  Layer 4: hero-content（文字内容）   │  z-index: 3
│  ┌─────────────────────────────────┐│
│  │  Layer 3: hero-overlay（遮罩）   ││  z-index: 1
│  │  ┌─────────────────────────────┐││
│  │  │  Layer 2: grain（纹理）      │││  z-index: 2
│  │  │  ┌─────────────────────────┐│││
│  │  │  │  Layer 1: hero-bleed    ││││  z-index: 0
│  │  │  │  （满铺背景图）           ││││
│  │  │  └─────────────────────────┘│││
│  │  └─────────────────────────────┘││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**关键规则**：
1. hero-overlay 使用渐变遮罩，不是纯色半透明块
2. 遮罩方向：从上到下加深，确保底部文字可读
3. 遮罩颜色取自主题的 ink 色——Indigo Porcelain 用深蓝遮罩，Kraft Paper 用深棕遮罩
4. grain 仍然叠加在 overlay 之上，保持纸墨感一致性

### Light 主题遮罩

```css
.hero-overlay {
  background: linear-gradient(180deg,
    rgba(10, 31, 61, .55) 0%,
    rgba(10, 31, 61, .25) 40%,
    rgba(10, 31, 61, .45) 100%
  );
}
```

### Midnight Ink 遮罩

```css
[data-theme="midnight-ink"] .hero-overlay {
  background: linear-gradient(180deg,
    rgba(14, 13, 12, .50) 0%,
    rgba(14, 13, 12, .20) 35%,
    rgba(14, 13, 12, .60) 100%
  );
}
```

---

## Swiss International 背景

Swiss 体系不使用 grain 和 paper-wash，背景极简：

```css
/* Swiss 使用纯 paper 底色 + 可选网格点阵 */
.poster.swiss {
  background: var(--paper);
}

/* 可选：极细网格点阵（仅用于数据页） */
.poster.swiss.grid-dots {
  background-image:
    radial-gradient(circle, var(--grey-2) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

**硬规则**：
- Swiss 不使用 grain 纹理
- Swiss 不使用 paper-wash 水洗
- Swiss 网格点阵仅用于数据页，且 opacity ≤.3
- Swiss 封面不使用网格点阵

---

## 反模式

| 反模式 | 问题 | 修复 |
|-------|------|------|
| 纯平 beige 背景 | 像网页不像杂志 | 添加 grain + paper-wash |
| grain-opacity >.10 | 文字模糊不可读 | 降至 .04-.06 |
| 全页渐变背景 | 像PPT不像杂志 | 用 paper-wash（透明度≤.03）代替 |
| 遮罩用纯色半透明 | 死板无层次 | 改用渐变遮罩 |
| Swiss 用 grain | 破坏极简感 | Swiss 不用 grain |
| 暗色页不加 grain 覆盖 | 暗色背景死板 | Midnight Ink 必须加 screen 混合 grain |
