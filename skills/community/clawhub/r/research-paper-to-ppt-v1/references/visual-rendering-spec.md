# 视觉渲染规范

本文档定义所有 PPT 生成的精确视觉规则，是生成稳定、一致输出的核心依据。

---

## 1. 幻灯片基础规格

| 属性 | 值 |
|------|-----|
| 布局 | `LAYOUT_WIDE`（13.333 × 7.5 英寸）|
| 坐标系 | 1 pt = 127 EMU；1 英寸 = 914400 EMU |
| 内容安全区 | y: 0.1" – 7.1" |
| 顶部 header | y=0, h=0.78"（深海军蓝色）|
| 底部 footer | y=7.18", h=0.32"（浅灰，用于页码）|
| 正文内容区 | y 起点约 1.05"–1.2"，底部止于 7.05" |

**禁止项**：
- 任何形状的 x 坐标小于 0
- 任何形状的右边界超过 13.333"
- 任何形状的底部边界超过 7.5"
- 字号小于 10pt（脚注/页码除外）

---

## 2. 颜色面板

| 用途 | 变量名 | Hex 值 |
|------|--------|--------|
| 主背景（深色页）| navy | `13293D` |
| 右栏/侧栏 | navy2 | `1B3A57` |
| 主蓝色 | blue | `2A628F` |
| 主青绿 | teal | `2CA6A4` |
| 薄荷背景 | mint | `DDF4F1` |
| 浅灰背景 | light | `F5F8FC` |
| 白色 | white | `FFFFFF` |
| 深色文字 | dark | `18222D` |
| 中灰文字 | mid | `5C6773` |
| 边框/分隔线 | line | `D6E1EB` |
| 金色强调 | gold | `D5A44A` |
| 卡片浅金背景 | gold_bg | `FBF7EE` |
| 结果页强调 | gold2 | `ECD7A4` |

**禁止项**：不得在代码中使用未经本表定义的颜色值。

---

## 3. 字体规范

| 元素 | 字号（pt）| 字重 | 颜色 | 字体 |
|------|-----------|------|------|------|
| 幻灯片标题（header 内）| 25 | bold | `FFFFFF` | Aptos Display |
| 副标题（header 右）| 10.5 | normal | `DCE7F1` | Aptos |
| 页码（右下角）| 10 | normal | `6B7280` | Aptos |
| 卡片标题 | 20 | bold | navy | Aptos |
| 核心结论标签 | 19 | bold | navy | Aptos |
| 正文 bullet | 15–18 | normal | dark | Aptos |
| 图解标题 | 12 | bold | teal | Aptos |
| 图解正文 | 13.2 | normal | dark | Aptos |
| 标题页中文标题 | 27 | bold | white | Aptos Display |
| 标题页英文章名 | 17 | italic | `D5E4F0` | Aptos |
| 标题页期刊/年份 | 17.5 | bold | `C9DBEA` | Aptos |
| 标题页作者 | 14.5 | normal | white | Aptos |
| 结束页主标题 | 30 | bold | white | Aptos Display |
| 结束页副标题 | 21 | normal | `DDE9F2` | Aptos |

**字号安全规则**：bullet 正文字号不得小于 13pt；若内容过多，优先拆页，而不是缩小字号。

---

## 4. 阴影规范（全局统一）

```javascript
function softShadow() {
  return {
    type: 'outer',
    color: '000000',
    blur: 2,
    offset: 1,
    angle: 45,
    opacity: 0.12
  };
}
```

**禁止项**：
- 不得在多个 shape 上复用同一个 shadow 对象（shadow 对象会被 PptxGenJS 就地修改）
- 每次调用 `softShadow()` 必须返回新对象
- 不得在 shadow 中使用 8 位 hex 颜色

---

## 5. 布局模板（每种 slide_type 的精确坐标）

### 5.1 标题页（slide_type = title）

```
背景：整页 navy (#13293D)
右栏：x=8.7", w=4.633", h=7.5", fill=navy2
金色竖条：x=0.65", w=0.18", h=5.2", fill=gold

中文标题：x=1.06", y=1.02", w=7.05", h=1.55", sz=27, bold, white
英文章名：x=1.08", y=2.82", w=6.95", h=1.05", sz=17, italic, #D5E4F0
期刊年份：x=1.1",  y=4.15", w=4.4",  h=0.25", sz=17.5, bold, #C9DBEA
作者信息：x=1.1",  y=4.7",  w=5.7",  h=0.62", sz=14.5, white

研究主线卡片：x=8.95", y=1.15", w=3.45", h=1.05", rectRadius=0.08
关键词卡片：  x=8.95", y=2.62", w=3.45", h=2.4",  rectRadius=0.08

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

### 5.2 目录页（slide_type = 目录 / agenda）

```
背景：light + header navy + footer 浅灰
内容卡：x=0.7", y=1.2", w=12.0", h=5.55", white, shadow=softShadow()

编号圆：圆形, diam=0.5", fill=teal（或 gold 对应重点项）
编号文字：圆内居中, sz=14, bold, white

项目标题：x=1.82", sz=21, bold, dark
分隔线：x=1.82", y+0.57", w=9.8", h=0", #E8EEF4

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

### 5.3 全文概述页（slide_type = overview）

```
背景：light + header navy + footer 浅灰
左玻璃卡：x=0.7", y=1.18", w=7.1", h=5.56", white, left_accent=teal, shadow
  - "一句话概括" 标签：sz=18, bold, teal
  - 一句话核心：sz=20, bold, navy
  - bullet 列表：sz=15.8, dark

右玻璃卡（金色强调）：x=8.05", y=1.18", w=4.55", h=5.56", fill=gold_bg, left_accent=gold, shadow
  - "你可以这样理解" 标签：sz=18, bold, #A2721D
  - 分块卡片：rectRadius=0.05, fill=（交替 #FFF8E9 / #F2E4BF）

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

### 5.4 结果页（slide_type = result）

```
背景：light + header navy + footer 浅灰
左结论卡：x=0.48", y=1.03", w=4.04", h=5.9", white, left_accent=gold, shadow
  - "核心结论" 标签：x=0.82", y=1.22", sz=19, bold, navy
  - bullet: x=0.78", y=1.6", w=3.42", sz=15, dark

图区域：x=4.82", y=1.03", w=8.02", h=3.98", fill=#F4F7FA, border=#C8D5E1
  - 图片：x=4.91", y=1.12", w=7.84", h=3.8", sizing=contain

图解区域：x=4.82", y=5.2", w=8.02", h=1.55", white, border=#C8D5E1
  - "图解" 标签：背景 mint 圆角矩形, sz=12, bold, teal
  - 图解文字：x=5.08", y=5.7", w=7.1", sz=13.2, dark
  - Figure 编号：x=11.1", y=5.4", sz=10.5, mid, 右对齐

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

### 5.5 机制页（slide_type = mechanism）

```
背景：light + header navy + footer 浅灰
左侧路径卡：x=0.62", y=1.16", w=5.0", h=5.55", white, left_accent=teal, shadow
  - "路径主线" 标签：sz=18, bold, teal
  - 步骤条：rectRadius=0.06, h=0.34"
    - 第一个（药物）：fill=teal, white 文字
    - 中间步骤：fill=#EEF5FB, dark 文字
    - 最后（认知改善）：fill=gold, dark/bold 文字
  - 箭头：Chevron shape, fill=#B7CBDC

右侧图区域：x=5.95", y=1.16", w=6.6", h=3.6", #F4F7FA
  - 图片：x=6.05", y=1.28", w=6.4", h=3.35", sizing=contain

底部总结卡：x=5.95", y=5.0", w=6.6", h=1.7", fill=gold_bg, left_accent=gold, shadow

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

### 5.6 总结/优点/局限/意义页（多类型）

```
背景：light + header navy + footer 浅灰
主卡：x=0.72", y=1.18", w=12.0", h=5.56", white, left_accent=teal/gold, shadow

分栏布局（2 列）：
  - cardW = 5.55", gap = 0.28"
  - cardH = 1.72", row_gap = 0.2"
  - 编号圆：diam=0.36", fill=teal/gold, sz=10.5 bold white
  - 条目文字：sz=15.8, dark
```

### 5.7 Take-home message 页

```
背景：light + header navy + footer 浅灰
标签：x=1.05", y=1.45", sz=18, bold, teal

条目卡：x=1.02", y=1.95", w=11.2", h=0.92", rectRadius=0.05
  - 编号"01"/"02"/"03"：x=1.28", sz=18, bold, teal/gold
  - 条目文字：x=2.0", sz=18, dark
  - 交替背景：'EEF7F6' / 'F8FBFD'
```

### 5.8 结束页（slide_type = closing）

```
背景：整页 navy (#13293D)，右栏 navy2
主卡片：x=1.1", y=1.45", w=5.5", h=3.7", rectRadius=0.08, fill=#1D405D

"谢谢！"：x=1.55", y=2.1", w=3.2", h=0.7", sz=30, bold, white
"感谢批评指正！"：x=1.58", y=3.0", w=4.3", h=0.42", sz=21, #DDE9F2
"Questions & Discussion"：x=1.58", y=3.72", sz=14.5, italic, #BDD2E3

右侧装饰框：x=9.2", y=1.75", w=2.65", h=2.65", fill=#274967
金色十字线：水平线 x=9.52", y=3.08", w=2.0", fill=gold
           垂直线 x=10.52", y=2.08", w=0", h=2.0", fill=gold

AD Journal Club 标签：x=9.46", y=4.7", sz=13, #D0DFEB

页码：x=12.4", y=7.02", w=0.28", h=0.14", sz=10, #6B7280
```

---

## 6. 图片嵌入学规范

### 6.1 结果页图片

**规则**：使用 `sizing: { type: 'contain' }`，同时约束宽和高，不做 `cover` 或自由裁切。

```javascript
// 正确做法
slide.addImage({
  path: localImagePath,
  x: 4.91, y: 1.12, w: 7.84, h: 3.8,
  sizing: { type: 'contain', w: 7.84, h: 3.8 }
});
```

**禁止**：
- 直接设置固定的 w/h 而不做 aspect ratio 计算
- 使用 `cover` 模式（会裁切掉原图内容）
- 将图片放在没有任何边框或背景的裸位置

### 6.2 图片加载失败处理

渲染脚本必须在调用 `pptx.addImage()` 前检查图片文件是否存在且非空。若网络图片下载失败（如 HTTP 404），需捕获错误、记录日志，并输出不含该图片的占位页，不得让整个 PPT 生成失败。

---

## 7. 字体渲染规范

### 7.1 字体声明（必须在 PPTX 级别声明）

```javascript
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'zh-CN'
};
```

### 7.2 每段文字必须显式指定 fontFace

禁止依赖 PptxGenJS 默认字体。所有 `addText()` 调用必须显式传入 `fontFace` 参数：

```javascript
slide.addText(text, {
  fontFace: 'Aptos Display',  // 标题类
  fontFace: 'Aptos',           // 正文类
  fontSize: 18,
  bold: true,
  color: '13293D',
  margin: 0
});
```

### 7.3 margin 规则

- 所有文字框默认 `margin: 0`（文字贴近边框）
- 只有在文字与相邻元素有明确距离时才设置非零 margin
- 正文 bullet 使用 `margin: 0.03` 以避免首字符贴近边框

---

## 8. 渲染脚本结构规范

每个渲染脚本必须遵循以下结构：

```javascript
// 1. 依赖声明
const PptxGenJS = require('.../pptxgenjs');
const fs = require('fs');
const path = require('path');

// 2. 颜色常量（全部来自本规范，不得自创）
const C = {
  navy: '13293D',
  navy2: '1B3A57',
  teal: '2CA6A4',
  // ... (完整列表见本规范第2节)
};

// 3. 工具函数
function softShadow() { /* 见本规范第4节 */ }
function sanitize(name) { /* 文件名清洗 */ }

// 4. 下载/资源函数
async function ensureAsset(url) { /* 图片下载 + 缓存 */ }

// 5. 布局组件函数（每个 slide_type 一个）
function addBg(slide, dark) { /* 背景 + header + footer */ }
function addTitleSlide(slide) { /* 见本规范5.1 */ }
function addAgendaSlide(slide, s) { /* 见本规范5.2 */ }
function addResultLayout(slide, s) { /* 见本规范5.4 */ }
// ... 以此类推

// 6. 主函数
async function build() {
  // 预下载所有图片
  for (const s of deck.slides) {
    if (s.image_paths_or_urls?.length) {
      s.localImagePath = await ensureAsset(s.image_paths_or_urls[0]);
    }
  }

  // 生成每一页
  deck.slides.forEach((s, i) => {
    const slide = pptx.addSlide();
    // 按 slide_type 分发到对应布局函数
  });

  // 输出
  await pptx.writeFile({ fileName: outputPath });
}
```

---

## 9. 输出文件名规范

见 `references/output-filename-policy.md`。

默认规则：**使用论文英文标题作为文件名**，清洗后附加 `.pptx`。

---

## 10. 质量自检清单（渲染层面）

渲染完成后，逐项确认：
- [ ] 所有 slide 的 header navy 条高度一致（h=0.78"）
- [ ] 所有 slide 的 footer 位置一致（y=7.02"）
- [ ] 所有文字显式指定 fontFace，无默认字体依赖
- [ ] 所有颜色值来自本规范的色板，无自创颜色
- [ ] 所有 shadow 调用使用 `softShadow()` 函数（每次新对象）
- [ ] 所有图片使用 `sizing: { type: 'contain' }`，不裁切
- [ ] 结果页图片区域：x=4.82", y=1.03", w=8.02", h=3.98"
- [ ] 机制页左侧路径卡：x=0.62", w=5.0"
- [ ] 关闭页使用深色背景（navy + navy2），不混用浅色
- [ ] 所有 bullet 正文字号 ≥ 13pt
- [ ] 输出文件名使用论文标题，无泛化名称
