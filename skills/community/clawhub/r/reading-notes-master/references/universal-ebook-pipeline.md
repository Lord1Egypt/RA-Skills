# 任意格式电子书 → 期刊复刻通用管线（v2.12）——Universal eBook Pipeline

> **目标**：任何格式的电子书/电子材料（epub/docx/pdf/html/md/txt），经本管线统一解析后，按自动或自定义模式生成"高清晰、高密度、高质量"的海外期刊杂志复刻版（接 v2.11 六步复刻工作流与 J1–J4 四门验收）。
> 设计知识源：`journal-design-seven-dimensions.md`（七维知识库）+ `magazine-design-corpus-2026-10.md`（31 刊档案卡）。

## 一、输入格式矩阵

| 格式 | 首选解析器 | 备选 | 提取物 | 陷阱 |
|---|---|---|---|---|
| **epub** | pandoc `epub→markdown`（保留章节结构） | ebooklib (py) | 章节/图/表/脚注 | 图在 zip 内需解包重链 |
| **docx** | pandoc `docx→markdown` | python-docx | 标题层级/图/表 | 复杂表格用 python-docx 直读 |
| **pdf**（原生文本） | PyMuPDF `get_text("dict")` | pdfplumber | 文本/字体/图位（可同时作为风格源！） | 扫描件走 OCR 分支 |
| **pdf**（扫描件） | OCR（tesseract / PaddleOCR） | — | 纯文本（丢失版式，仅内容复刻） | J1–J3 无法量原刊，需用户提供风格参照 |
| **html** | 直接 DOM 解析（readability 抽正文） | pandoc | 正文/图/表 | 广告噪声先洗 |
| **md / txt** | 原生 | — | 已是结构化 | txt 需探测标题规律（全角序号/缩进） |
| **mobi / azw3** | `ebook-convert → epub` 先转 | calibre CLI | 同 epub | 需装 calibre |
| **微信文章/网页链接** | ima `import_urls` 或 WebFetch | — | 正文 md | 图床外链需落地 |

**双源情形（最常见）**：用户给"内容 pdf + 风格参照刊 pdf"——内容走解析分支，风格走 `analyze_mags.py` 实测分支（内容与风格分离是本管线的设计核心）。

## 二、模式路由

### 自动模式（Auto）
内容类型探测 → 自动选型（调用七维快速路由）：

```
探测信号（正文关键词密度 + 结构统计）：
  财经信号（营收/毛利率/EPS/估值/行情词 >阈值）→ 财经拆解范式（Barron's/BBW/MoneyWeek）
  科研信号（实验/样本/显著性/参考文献 >阈值）→ D 型 Science/SciAm 骨架
  视觉素材占比 >50%（图数/页 >3）→ B 型 NG 骨架
  单主角叙事（人物传记/产品发布）→ E 型 Vogue/Time 特辑
  默认 → D 型 Time 平衡叙事
```

输出自动选型报告（命中信号 + 选用 profile + 七维参数）交用户确认，可一句话改型。

### 自定义模式（Custom）
用户点名风格：`"按 NG 风格复刻"` / `"模仿 HBR 版式"` / `"要 BBW 那种图阵感"` → 直接加载对应档案卡（`magazine-design-corpus-2026-10.md` §二~五 + profile 卡 `journal_4k_check.py --list`），跳过探测。

混合模式：正文用刊 A、封面用刊 B（如"NG 的图 + TIME 的封面字"）——分别取两卡参数，封面单独过 J1/J2。

## 三、五步管线

### Step 1 解析归一
按格式矩阵解析 → 统一中间表示（IR）：
```
IR = { title, chapters: [{level, heading, blocks: [para|quote|list|table|image|figure_caption|data_series]}],
       assets: {images: [...], tables: [...]}, meta: {word_count, image_ratio, table_ratio} }
```
- 图片全部落地本地目录并重命名（`img_ch{n}_{i}.png`）；
- 低分辨率图（<1200px 长边）标记 → 交 Step 4 superres。

### Step 2 风格定型
- 自动模式跑探测；自定义模式载档案卡；混合模式双卡。
- 产出**版式令牌单**：字体双栈（display/body）、字号双轨、色板（骨架+签名色）、边距/栏数、密度分型、DPI 目标（公式：`dpi = ceil(3840 / 页长边英寸)`，或查 14 卡速查表）。

### Step 3 结构映射（内容 → 栏目）
| 电子书元素 | 期刊化映射 |
|---|---|
| 书名/章节标题 | 封面主题大字 / 栏目题（display 轨） |
| 章节引言/金句 | pull quote（签名色底或大字引号） |
| 数据/表格 | 图阵小图（BBW 范式）或全页表（Barron's 范式） |
| 人物介绍 | 人物卡（头像 + 边栏简介） |
| 长段落 | 按 ~350 词/栏切栏，段首下沉或小标隔断 |
| 参考文献/脚注 | 页脚小字或文末 "Sources" 块（衬线 7–8pt） |
| 全书结构 | 封面 → 目录 Contents → 专题 Section → 卷尾 |

### Step 4 渲染（两条路径，同 v2.11）
- **路径 P（PDF 矢量）**：HTML/CSS 或 WeasyPrint/ReportLab 排版 → 矢量 PDF（J1–J3 量此产物）。
- **路径 G（PNG 位图）**：PDF 高倍渲染或直接 4K 画布（J4 量 PNG）。
- 低清图先 `superres.sh` 放大再嵌入；字体缺失用档案卡替代栈 + `@font-face`。

### Step 5 验收交付（同 v2.11 四门）
```
python3 scripts/journal_4k_check.py <产物> --profile <name> [--min-long 3840]
```
- 矢量 PDF 量 J1–J3；PNG 量 J4；两次调用合并报告；exit 0 才交付。
- 验收 FAIL → 按 `journal-4k-replication.md` §八 陷阱库修复后复跑。

## 四、批量模式

多文件/整本书库批处理：
```bash
for f in ~/books/*.epub; do
  # Step1-3 为纯本地解析与令牌生成，可脚本化
  python3 scripts/ebook2ir.py "$f" --out /tmp/ir/
done
# Step4-5 渲染与验收按 profile 分组跑（同 profile 合批渲染省字体加载）
```
批量交付清单：每本一行（书名 / profile / 四门结果 / 产物路径）。

## 五、错误处理

| 症状 | 处置 |
|---|---|
| epub 图全丢 | 图在 zip `EPUB/images/`，解包后按 IR 引用重链 |
| pdf 扫描件无文本层 | 走 OCR 分支；向用户声明"内容复刻、风格需另给参照" |
| 探测信号冲突（财经+科研双高） | 按"目标读者"问一句定范式；不问则取密度更高者并在报告标注 |
| 中文书目 | 骨架用中文刊实测（青年文摘卡：Type3 字体需替换为思源宋/黑双栈，L272-R321 边距 2 栏）；涨跌色遵守红涨绿跌 |
| 单章超长（>2 万字） | 拆多个 Section，每 Section 独立起页，共用目录 |
| 字体版权 | 复刻用替代字体栈（档案卡已给），不内嵌原刊商用字体文件 |

## 相关文档
- `journal-design-seven-dimensions.md`：七维设计知识库（选型依据）
- `magazine-design-corpus-2026-10.md`：31 刊档案卡（参数源）
- `journal-4k-replication.md`：四门验收与渲染路径（质量门）
- IMA 云端 KB `ima_kb_rDzPwmRH`：31 刊原刊 PDF + 实测汇总（风格参照与语义检索源）
