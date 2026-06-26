---
name: rednote-knowledge-layout
description: >
  将话题或文章转化为小红书知识型图文（3:4 竖版图片组）。专为企业主、创业者、知识型 IP 设计。
  首图以大字标题 + 数字/反问/反常识/信息差策略吸引停留；内容图文字密度高，传递实质干货。
  设计风格：纸张浅色背景 + 深咖前景色系，高级感强，区别于生活博主审美。

  凡用户提到以下任何情形，必须立即调用本技能：
  - 帮我做小红书图文 / 帮我做知识卡片 / 帮我做内容图
  - 把这篇文章/话题/干货做成小红书
  - 做几张小红书图片 / 做一组图文
  - 企业主/创业者内容 / 知识型小红书 / 干货图文
  - 帮我出图 / 帮我排版成小红书格式
  不适用于：生活方式/美食/旅游类博主内容（请用 rednote-image-layout skill）。
---

# RedNote Knowledge Layout Skill

将话题或文章转化为适合企业主/创业者 IP 的小红书知识型图文组。
输出：多张 3:4（1080×1440px）PNG 图片，直接发送给用户。

---

## 核心定位与语气

- **目标读者**：企业主、创业者、管理者
- **内容语气**：克制、直接、有观点。像一个已经踩过坑的前辈在说真话 —— 不煽情，不鸡汤，数据说话，观点明确
- **禁止**：励志金句堆砌、模糊表达、"相信自己"类空话
- **禁止**：大段总结原文、缩写内容。要保留原文细节和完整信息
- **允许**：反常识判断、数据对比、"大多数人错在哪"句式、行业黑话解构

---

## 工作流程（严格按顺序执行）

**重要：直接输出 PNG 图片，不输出 HTML 文件。**

1. 读取用户提供的话题或文章
2. **提炼首图钩子**：从内容中找出最反常识/最有信息差/最有数字感的核心观点，作为封面标题
3. **规划幻灯片结构**：封面 1 张 + 内容图 3–5 张 + 结尾 CTA 1 张（共 5–7 张）
4. **逐张规划内容密度**：每张先做文字预算，确保内容充实不溢出
5. 生成 HTML 并导出为 PNG 图片（1080x1440px，3:4 竖版）
6. 保存 PNG 图片到本地输出目录
7. 直接用 message 工具发送图片给用户（每张图片作为附件发送）

---

## 调色板 —— 统一单色系（WARM PAPER）

**所有幻灯片使用同一套配色，无深色背景幻灯片。**

```css
:root {
  /* 背景：全部统一用暖纸白 */
  --bg:      #FAF7F2;   /* 唯一背景色，所有幻灯片一致 */
  --ink:     #2A1508;   /* 页面底色（body 背景） */

  /* 文字 */
  --brown:   #482E28;   /* 主前景色：深咖，标题/正文 */
  --mocha:   #6B3D30;   /* 次级文字：中咖，副文字/说明 */
  --muted:   rgba(72,46,40,0.45);  /* 弱化文字：眉注、页码 */

  /* 装饰色（克制使用，不超过每张幻灯片 10–15% 面积） */
  --orange:  #EE8136;   /* 主装饰色：关键词高亮、分割线、序号、CTA 按钮 */
  --orange-lt: rgba(238,129,54,0.12);  /* 淡橙：卡片背景、callout 底色 */
  --orange-bd: rgba(238,129,54,0.30);  /* 橙边框 */
}
```

**背景规则**：每张幻灯片背景统一为 `#FAF7F2`，不交替、不使用深色背景。
视觉节奏通过**装饰线、序号圆圈、callout 色块、标题粗细**来区分层次，而非背景色变化。

**点阵纹理（每张幻灯片必须有）**：
```css
.tex-dots {
  position: absolute; inset: 0; pointer-events: none; z-index: 1;
  background-image: radial-gradient(circle, rgba(72,46,40,0.055) 1.2px, transparent 1.2px);
  background-size: 30px 30px;
}
```

---

## 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700
  &family=Noto+Sans+SC:wght@300;400;500
  &family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600
  &display=swap" rel="stylesheet">
```

```
封面大标题：    Noto Serif SC 700    118–128px   letter-spacing: 8–12px   line-height: 1.20–1.28
章节标题：      Noto Serif SC 700    72–86px     letter-spacing: 4–7px
数字/数据：     Cormorant Garamond 600  90–110px  （强调时可更大）
正文：          Noto Serif SC 300    30–33px     line-height: 1.85–2.00
要点标题：      Noto Serif SC 600    36–40px     letter-spacing: 2px
要点正文：      Noto Serif SC 300    28–30px     line-height: 1.80
眉注/英文：     Cormorant Garamond italic  28–30px  letter-spacing: 7–9px
底栏：          Cormorant Garamond   22–24px     letter-spacing: 2–4px
标签药丸：      Noto Sans SC 400     24–26px     letter-spacing: 3px
```

**禁止使用**：任何手写体、马善政、ZCOOL XiaoWei、装饰字体。

---

## 封面幻灯片（首图策略）

封面是决定用户是否停留的关键。必须包含以下钩子之一：

**钩子类型（从内容中选最强的一种）：**
- **数字型**：`92% 的老板不知道…` / `做到这 3 点，利润翻倍`
- **反问型**：`你的团队真的在执行吗？` / `为什么降价反而亏更多？`
- **反常识型**：`越努力越穷，问题出在这` / `不做品牌反而更赚钱`
- **信息差型**：`行业内部都在用这个方法` / `2024 最新政策，90% 老板没看到`

**封面布局：**
```
[点阵纹理（.tex-dots）]
[幽灵字 —— 单个大汉字，~480px，opacity 3%，右上角，置于内容层之下，颜色 --brown]
[左侧竖向装饰线 —— --orange色，渐变至透明，opacity 35%]
[四角定位框 —— 仅封面有，颜色 --orange，opacity 40%]
[内容区：padding 120px 96px 96px，flex column]
  - 眉注      (Cormorant italic, 28px, letter-spacing 9px, --orange)
  - 主标题    (Noto Serif SC 700, 118–128px, --brown；关键词/数字用 .accent → color: --orange)
  - 分割线    (68px 宽, 2px, --orange)
  - 副标题    (Noto Serif SC 300, 31px, line-height 2.00, --mocha, 2–3 行)
  - 标签行    (2–3 个药丸标签，margin-top auto，padding-bottom 100px)
[底栏]
```

**封面标题字数控制**：主标题控制在 8–16 字，宁短勿长。
**不在封面堆砌内容**，封面只做一件事：让人想看下一张。

---

## 内容幻灯片（要点型）

适合列举观点、步骤、对比、解析。文字密度高，每张传递 3–5 个实质信息点。

```
[点阵纹理（.tex-dots）]
[内容区：padding 100px 88px 88px]
  - 眉注      (Cormorant italic, 28px, --orange)
  - 章节标题  (76–86px, Noto Serif SC 700, --brown)
  - 分割线    (52px, 2px, --orange)
  - 要点列表  (每条：序号圆圈 + 要点标题 36px + 要点正文 28–30px，3–5 条)
  - 引用框    (可选：左侧 4px --orange 竖线，背景 --orange-lt，padding 24px 36px)
[底栏]
```

**序号圆圈样式：**
```css
.num-circle {
  width: 52px; height: 52px; min-width: 52px; border-radius: 50%;
  background: rgba(238,129,54,0.10); border: 1px solid rgba(238,129,54,0.28);
  font-family: 'Cormorant Garamond', serif; font-size: 26px; color: #EE8136;
  display: flex; align-items: center; justify-content: center;
}
```

---

## 数据/对比幻灯片

当内容包含数据对比、前后对比、行业均值 vs 目标值时使用此布局。

```
[点阵纹理（.tex-dots）]
[内容区：padding 96px 80px 80px]
  - 章节标题  (76px, Noto Serif SC 700, --brown)
  - 大数字展示区：
      数字本体  (Cormorant Garamond 600, 100–120px, --orange)
      单位/说明 (Noto Sans SC 400, 28px, --mocha)
  - 对比行    (两列并排：左侧"普通做法" vs 右侧"正确做法"，右侧用 --orange-lt 底色 + --orange-bd 边框)
  - 结论句    (引用框，Noto Serif SC 300, 32px, line-height 1.90)
[底栏]
```

---

## 结尾 CTA 幻灯片

每组图文最后一张，引导关注/保存/评论。背景同样是 `#FAF7F2`，用装饰元素拉开层次。

```
[点阵纹理（.tex-dots）]
[内容区：padding 104px 96px 96px]
  - 眉注      (Cormorant italic, 28px, --orange)
  - 分割线    (48px, 2px, --orange)
  - 结语标题  (76px, Noto Serif SC 700, --brown)
  - 总结正文  (30px, Noto Serif SC 300, line-height 1.90, --mocha, 3–4 句)
  - 行动号召  (药丸按钮：background #EE8136, color #FAF7F2, 32px, border-radius 48px, padding 18px 52px)
  - 品牌签名  (BaoAI，Cormorant Garamond 600, 36px, --orange, 右对齐，margin-top auto)
[底栏]
```

---

## 标签药丸

所有幻灯片背景相同，只需一套标签样式：

```css
/* 统一标签 —— 在 #FAF7F2 背景上 */
.tag-a { background: rgba(238,129,54,0.10); color: #C45E10; border: 1px solid rgba(238,129,54,0.30); }
.tag-b { background: rgba(72,46,40,0.07);  color: #482E28; border: 1px solid rgba(72,46,40,0.20); }
.tag-c { background: rgba(72,46,40,0.04);  color: #6B3D30; border: 1px solid rgba(72,46,40,0.14); }
/* 通用基础样式 */
.tag { display: inline-flex; align-items: center; padding: 10px 22px; border-radius: 40px;
       font-family: 'Noto Sans SC', sans-serif; font-size: 24px; letter-spacing: 3px; }
```

---

## 底栏

所有幻灯片底栏颜色一致（浅色背景上统一用深咖透明色）：

```css
.btm {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 84px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 80px; z-index: 30;
}
.btm-num, .btm-brand { font-family: 'Cormorant Garamond', serif; letter-spacing: 3px; }
.btm-num   { font-size: 23px; color: rgba(72,46,40,0.28); }
.btm-brand { font-size: 22px; font-weight: 600; color: rgba(72,46,40,0.28); }
```

---

## 幻灯片外壳与缩放 JS

```html
<div class="slide s1">
  <div class="slide-inner">
    <!-- 内容 -->
  </div>
</div>
```

```css
.slide       { width: 100%; max-width: 540px; position: relative; overflow: hidden; border-radius: 3px; }
.slide-inner { width: 1080px; height: 1440px; position: relative; transform-origin: top left; }
```

```javascript
function scaleSlides() {
  document.querySelectorAll('.slide').forEach(slide => {
    const inner = slide.querySelector('.slide-inner');
    if (!inner) return;
    const s = slide.clientWidth / 1080;
    inner.style.transform = `scale(${s})`;
    slide.style.height = (1440 * s) + 'px';
  });
}
scaleSlides();
window.addEventListener('resize', scaleSlides);
```

---

## SVG 图标系统（无需外部图片）

不依赖外部图片 URL（沙盒网络封锁）。所有装饰图形用内联 SVG 绘制。

**常用图标（stroke-width 2–2.5，颜色 #C8956A）：**
- 勾选 `✓`：`<path d="M5 12l5 5L19 7"/>`
- 箭头右：`<polyline points="9 18 15 12 9 6"/>`
- 灯泡（洞见）：自定义 path
- 警告三角：`<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>`
- 圆圈数字：SVG `<circle>` + `<text>` 组合

**禁止使用 emoji 作为图标**，一律用 SVG stroke 路径或 Unicode 纯文本符号（①②③ 等）。

---

## 内容密度规则

每张幻灯片必须**填满整页**，不能留白下半页。

### 核心原则
1. **不要总结，要保留原文**：直接引用/转述原文核心内容，而不是缩写总结
2. **内容要足够多**：每张内容图必须有 5-8 个要点，每个要点包含标题+详细说明
3. **文字密集度**：正文 28-30px，行间距 1.75-1.85，每张幻灯片文字量约 400-600 字

### 填充策略（按优先级）
1. **增加要点数量**：从 3-5 个增加到 5-8 个
2. **每个要点加详细说明**：不只是标题，每个点要有 2-3 行的解释
3. **添加案例/数据/具体例子**：补充具体数字、案例、场景描述
4. **可适当添加**：对比说明、注意事项、适用场景、常见误区
5. **引用原文金句**：保留原文的精彩表述

### 字号与间距
- 眉注：28px，letter-spacing: 9px
- 章节标题：72-86px
- 要点标题：34-36px
- 要点正文：28-30px，line-height: 1.75-1.85
- padding：上 80-96px，下 80-88px（不再留大量底部空间）

**每张内容图要求**：章节标题 + 5-8 个要点（含小标题 + 详细正文）+ 底部可加标签


```python
from playwright.sync_api import sync_playwright
import os, zipfile, shutil

TOPIC     = "topic-name"   # 替换为实际话题关键词
HTML_PATH = f"/mnt/user-data/outputs/rednote-{TOPIC}.html"
PNG_DIR   = f"/home/claude/slides_{TOPIC}"
ZIP_PATH  = f"/mnt/user-data/outputs/rednote_{TOPIC}.zip"

LABELS = {
    "slide_01.png": "01_封面.png",
    "slide_02.png": "02_内容.png",
    # 自动按 slide 数量导出
}

shutil.rmtree(PNG_DIR, ignore_errors=True)
os.makedirs(PNG_DIR)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 900}, device_scale_factor=2)
    page.goto(f"file://{HTML_PATH}")
    page.wait_for_timeout(4000)   # 等待 Google Fonts 加载

    for i, slide in enumerate(page.query_selector_all(".slide")):
        slide.screenshot(path=f"{PNG_DIR}/slide_{i+1:02d}.png")

    browser.close()

# 直接发送图片，不需要打包 ZIP
    # 用 message 工具逐一发送每张图片
        if f.endswith(".png"):
            zf.write(f"{PNG_DIR}/{f}", LABELS.get(f, f))

print(f"ZIP ready: {ZIP_PATH}")
```

完成后：用 message 工具发送所有 PNG 图片给用户

**关键参数（不可改动）：**
- `device_scale_factor=2` → 物理分辨率 1080×1440
- `wait_for_timeout(4000)` 最低 4 秒（深色背景 + 多字体）
- 截图 `.slide` 元素，不是 `.slide-inner`

---

## 质检清单

**HTML：**
- [ ] 所有幻灯片背景统一为 `#FAF7F2`，无深色背景幻灯片
- [ ] 前景色统一为 `#482E28`，次级文字 `#6B3D30`
- [ ] 装饰色 `#EE8136` 克制使用（分割线、序号、.accent 高亮、CTA 按钮），不超过每张 15% 面积
- [ ] 封面：Noto Serif SC 700，无手写字体，`.accent` 用在关键词/数字上（颜色 #EE8136）
- [ ] 每张幻灯片有点阵纹理（统一用 `.tex-dots`）
- [ ] 四角定位框仅出现在封面
- [ ] 封面标题包含钩子（数字/反问/反常识/信息差之一）
- [ ] 每张内容图内容充实，3–5 个实质信息点
- [ ] 底栏左：页码格式 `01 / N`；右：`BaoAI` 水印；颜色 `rgba(72,46,40,0.28)`
- [ ] 无任何 emoji（SVG 图标或 Unicode 符号替代）
- [ ] 无外部图片 URL（如需图形，用内联 SVG）
- [ ] 无内容溢出

**PNG 导出：**
- [ ] Playwright `device_scale_factor=2`
- [ ] 每张 PNG 物理尺寸 1080×1440px
- [ ] ZIP 含描述性中文文件名
- [ ] 用 message 工具发送 PNG 图片给用户
