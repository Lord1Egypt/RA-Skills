# Screenshot Treatment Specification

> 截图装裱规范：如何将 UI 截图和照片内容优雅地嵌入 3:4 卡片。

---

## 何时使用 .frame-shot vs .frame-img

| 类别 | 使用 | 典型场景 |
|------|------|---------|
| **.frame-shot** | 应用/Web UI、代码/终端、仪表盘、IDE 截图 | 网页截图、App 界面、代码编辑器、数据面板 |
| **.frame-img** | 摄影内容（人物、风景、产品） | 人物照、风景照、产品摄影、食物摄影 |

---

## 主体预处理（Subject Prep）

- 裁切到前景窗口/卡片后再装裱
- **禁止** 透视/倾斜/旋转，除非用户明确要求
- 保持截图原始比例，不拉伸

---

## 解剖结构（Anatomy）

```
.frame-shot.r-{ratio}.corners-{sq|sm|md}.shadow-{none|soft|ed}.bg-{paper|grid|dot|grey-1|ink}.inset-{none|sub|bal}
  └─ <img src="…" style="object-fit:contain">
```

### 参数说明

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `r-{ratio}` | `r-3-4`, `r-16-9`, `r-4-3`, `r-1-1` | 截图原始比例 |
| `corners-{}` | `corners-sq` (0px), `corners-sm` (4px), `corners-md` (8px) | 圆角大小 |
| `shadow-{}` | `shadow-none`, `shadow-soft`, `shadow-ed` | 阴影风格 |
| `bg-{}` | `bg-paper`, `bg-grid`, `bg-dot`, `bg-grey-1`, `bg-ink` | 背景材质 |
| `inset-{}` | `inset-none` (0px), `inset-sub` (12px), `inset-bal` (24px) | 内边距 |

---

## 设备外壳（Device Wrappers）

### .device-browser — macOS 浏览器外壳

模拟 macOS 浏览器窗口，包含地址栏和交通灯按钮。

```html
<div class="device-browser">
  <div class="browser-chrome">
    <div class="traffic-lights">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <div class="address-bar">https://example.com</div>
  </div>
  <div class="browser-content">
    <img src="…" style="object-fit:contain">
  </div>
</div>
```

### .device-phone — iOS 手机外壳

模拟 iOS 手机边框，包含刘海和 Home 指示条。

```html
<div class="device-phone">
  <div class="phone-bezel">
    <div class="notch"></div>
    <div class="phone-screen">
      <img src="…" style="object-fit:contain">
    </div>
    <div class="home-indicator"></div>
  </div>
</div>
```

---

## 风格锁定默认值（Style-Locked Defaults）

| 参数 | Swiss 国际风格 | Editorial 杂志风格 |
|------|---------------|-------------------|
| **Corners** | `corners-sq` | `corners-sm` |
| **Shadow** | `shadow-none` | `shadow-soft` |
| **Default bg** | `bg-grey-1` | `bg-paper` |
| **Default inset** | `inset-sub` | `inset-sub` |

---

## 背景材质（Background Materials）

| 类名 | 效果 | 适用场景 |
|------|------|---------|
| `bg-paper` | 暖色纸张纹理 | Editorial 风格、温暖质感 |
| `bg-grid` | 方格纸网格线 | Swiss 风格、技术/数据内容 |
| `bg-dot` | 点阵图案 | Swiss 风格、宣言/声明页 |
| `bg-grey-1` | 中性浅灰 | Swiss 风格默认、通用 |
| `bg-ink` | 深色背景 | 浅色截图反衬、深色模式 |

---

## 截图清晰度规则（Screenshot Clarity Rules）

1. **截图清晰度优先时**：放大截图区域，减少周围文字
2. **禁止拉伸截图**：始终保持原始比例
3. **UI 截图使用 `object-fit:contain`**：确保完整显示，不裁切
4. **安全边距**：截图内容周围保留足够 padding，避免紧贴边框
5. **高 DPI 适配**：截图源分辨率应 ≥ 2x 目标显示尺寸
6. **文字可读性**：截图内文字必须可辨认，必要时放大截图比例
7. **避免过度装饰**：截图本身是主角，装裱不应喧宾夺主

---

## 完整示例

### Swiss 风格 UI 截图

```html
<div class="frame-shot r-16-9 corners-sq shadow-none bg-grey-1 inset-sub">
  <img src="dashboard.png" style="object-fit:contain">
</div>
```

### Editorial 风格 App 截图 + 手机外壳

```html
<div class="device-phone">
  <div class="phone-bezel">
    <div class="notch"></div>
    <div class="phone-screen">
      <div class="frame-shot r-3-4 corners-sm shadow-soft bg-paper inset-sub">
        <img src="app-screen.png" style="object-fit:contain">
      </div>
    </div>
    <div class="home-indicator"></div>
  </div>
</div>
```

### 深色背景浅色截图

```html
<div class="frame-shot r-16-9 corners-sq shadow-none bg-ink inset-bal">
  <img src="light-theme-ui.png" style="object-fit:contain">
</div>
```
