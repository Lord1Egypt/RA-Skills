# Mode C: 品牌模板生成（Brand Template）

> **Triggers**: "品牌模板 / 品牌手册 / 参考风格 / 上传品牌素材 / 品牌色 / VI / 按这个品牌风格排 / 用我司的品牌风格".
> **Resource**: `scripts/style_extractor.py`（`--image/--pdf/--doc/--html`）+ `references/theme-index.md` + `references/theme-generator.md`.

用户上传品牌手册或参考风格素材（**图片 / PDF / 文档 / HTML**），提取品牌元素（色板、字体气质、版式偏好），生成**品牌专属的公众号排版模板**。生成后与内置行业模板同权，可在 Mode A 直接选用。

---

## 与既有机制的关系

| 机制 | 区别 |
|------|------|
| **Mode B（风格提取）** | 仅限公众号 URL / 本地 HTML → 主题。Mode C 扩展输入源为**品牌素材**（图片/PDF/文档），且产出带品牌专属元素 |
| **theme-generator.md** | 一句话/参考图 → 主题（AI 看图推断）。Mode C 用**脚本确定性提取**色板 + AI 补充气质描述，两者互补 |
| **行业模板（theme-*.md）** | 按行业预置。品牌模板是**按品牌定制**的常驻模板，优先于行业模板使用 |

**一句话**：用户给品牌素材 → 脚本提色 + AI 判断气质 → 生成 `theme-{brand}.md` → 登记 → Mode A 可选。

---

## 工作流（6 步）

### Step 0: 输入（可多份）

| 输入类型 | 示例 | 提取重点 |
|---------|------|---------|
| 品牌图 / 参考图 | logo.png、KV 主视觉.jpg | 主色板（PIL 量化）、视觉气质 |
| 品牌手册 PDF | brand-manual.pdf、VI 规范.pdf | 首页配色 + 文本色值 + 文字规范描述 |
| 品牌文档 | brand.md、VI.txt、规范.docx | 明确写的 hex 色值 + 品牌字段 |
| 本地 HTML | 官网/落地页.html | 完整色板 + 排版规则（同 Mode B） |

### Step 1: 脚本确定性提取

```bash
# 品牌图提色（pillow）
python3 scripts/style_extractor.py --image logo.png --output {brand}

# 品牌手册 PDF：文本色值 + 首页渲染提色（pymupdf）
python3 scripts/style_extractor.py --pdf brand-manual.pdf --output {brand}

# 品牌文档：精确提取文档中写明的 hex 色值
python3 scripts/style_extractor.py --doc brand.md --output {brand}

# 本地 HTML（同 Mode B）
python3 scripts/style_extractor.py --html page.html --output {brand}
```

脚本自动生成 `references/theme-{brand}.md` 骨架（设计变量表 + 全套组件 + 骨架 + 配方表 + 映射表）。

**提取精度提示**：
- `--doc` 提取文档明文色值 → **精确**（品牌手册通常直接写 hex）
- `--image`/`--pdf` 是像素量化 → **近似**（±1-2 色阶），主色需用户确认
- 排版规则（字号/行高/字重）仅 HTML 输入能提取；图片/PDF 用标准值，靠 Step 2 人工/AI 补充

### Step 2: AI/人工补充品牌气质（看图判断）

脚本无法确定的主观维度，由 AI 结合图片分析能力判断，用户确认：

| 维度 | 判断项 | 示例输出 |
|------|--------|---------|
| 圆角 | 组件圆角大小 | 8px / 全圆角（胶囊） / 直角 |
| 字体气质 | 标题与正文的字族气质 | 衬线复古 / 现代几何无衬线 / 圆体亲和 |
| 版式偏好 | 留白密度、对齐方式 | 大留白居中 / 左对齐密集 / 卡片化 |
| 情绪基调 | 品牌传达的情绪词 | 专业克制 / 温暖治愈 / 年轻活力 |

**同时从素材提取品牌专属字段**（写入模板头部）：
- 品牌名称（中文名 + 英文标识）
- Slogan（如有）
- Logo 图片路径（如有，用于封面/签名区槽位）

### Step 3: 汇总确认（一次问全）

用 AskUserQuestion 一次性确认：
1. 主色板（脚本提取结果 vs 用户指定修正）
2. 品牌气质描述（Step 2 的 4 个维度）
3. 骨架基座：沿用哪套行业模板的结构（默认 Blueprint 蓝图骨架，可换 Editorial/Report 等）
4. 是否需要品牌专属组件（Logo 区 / 品牌色板展示卡 / Slogan 标语卡）

### Step 4: 完善品牌模板文件

在脚本生成的骨架上补充：
1. **头部声明**：品牌名、来源素材、提取日期、品牌色板（含 hex + 用途）
2. **品牌专属组件**（按需，写入组件库）：
   - **品牌色板卡**（展示主色/辅助色的色块，用于品牌相关文章）
   - **Logo 区**（封面顶部/签名区预留 Logo 图位）
   - **Slogan 标语卡**（品牌标语居中金句）
3. **气质变量**：按 Step 2 结论覆盖圆角/字体/阴影变量
4. 全文件补齐 `<span leaf="">` 包裹，遵守平台红线

### Step 5: 预览确认

按 [`theme-generator.md`](./theme-generator.md) Step 2 的提示词生成区块库预览页 `assets/theme-previews/{brand}.html`，让用户在浏览器确认风格后进入 Step 6。

### Step 6: 登记 + 校验 + 上线

1. 在 `references/theme-index.md` 登记一行（标识 `{brand}`，适用场景「品牌专属」）
2. 跑源头检查：
   ```bash
   python3 scripts/component_lint.py .
   ```
   必须 0 严重问题
3. 品牌模板成为常驻可选模板，Mode A Step 1 可直接选用；**品牌账号排版时优先于行业模板**

---

## 品牌模板与行业模板的协同

| 场景 | 用哪个 |
|------|--------|
| 该品牌账号日常发文 | 品牌模板（锁定品牌识别） |
| 无品牌素材的新账号 | 行业模板（按文章行业推荐） |
| 品牌模板未覆盖的特定行业文章 | 品牌模板 + 该行业配方表微调 |

---

## 质量标准

- `--doc` 色值提取准确率 ≥ 95%（明文 hex 直读）
- `--image` 主色提取误差 ≤ 2 个色阶（量化容差，需用户确认）
- 生成模板必须通过 `component_lint.py` 0 严重问题
- 品牌色板卡等专属组件不破坏平台红线（无 div/class/grid/var）

---

## 容错与降级

| 场景 | 处理方式 |
|------|---------|
| 图片提色结果与品牌色不符 | 用户在 Step 3 手动修正主色，脚本重跑或直接改变量表 |
| PDF 无法渲染首页 | 仅用文本色值，提示用户另传品牌图 |
| 素材中无颜色信息 | 退回 theme-generator（一句话描述 + AI 看图推断） |
| 缺依赖（pillow/pymupdf） | 脚本给出精确安装命令，其余功能不受影响 |

---

## 与 Mode A 的衔接

品牌模板与内置模板完全同权：章节编号、关键词下划线、全角标点、配图建议等 Mode A 智能处理全部适用；品牌专属组件（色板卡/Logo 区/Slogan 卡）在配方表中按需选用。
