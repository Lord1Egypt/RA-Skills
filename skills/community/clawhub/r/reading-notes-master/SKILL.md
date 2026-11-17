---
name: reading-notes-master
description: |
  一图解千言的出版级可视化读书笔记生成器（Chart-First 图表驱动 v2.14）。
  31 份语料双透镜实测（排版美学 + 视觉密度）；6 大叙事原型、9 大模块、10+6 类组件、
  12 类文字→图表映射；v2.2 咨询级页面工艺、v2.3 图形资产管线、v2.4 设计智能前置检索、
  v2.5 思维模型库+文生图、v2.6 NG 竖版杂志、v2.7 HBR 横版杂志、
  v2.8 科研级图表体系（38 图型×11 大类/9 色板/9 期刊预设/四门验收/20 红线/figure-bridge 桥接）、
  v2.9 全图型 4K 级输出（位图长边≥3840 且短边≥2160、矢量等效、DPI 自动反推+像素实测门禁）、
  v2.10 期刊设计语料库（31 刊 2026-10 热点英语期刊 PyMuPDF 实测：NG/财经/科研/时尚/特辑
  12 类设计语言档案卡 + 7 条跨刊实证设计定律 + 矢量型 vs 图片型 PDF 判别 + IMA 知识库挂接）、
  v2.11 期刊 4K 复刻闭环（同一把尺量两次：14 profile 档案卡 × journal_4k_check.py 四门验收
  J1 字体 DNA/J2 色板签名/J3 栅格边距/J4 4K 像素，数字闭环取代凭感觉模仿）、
  v2.12 IMA 知识库全量吸收（海外期刊杂志 KB 七维设计知识库：思维/模型/图表/版式/照片采集/
  财经拆解/封面设计 + 任意格式电子书→期刊复刻通用管线 epub/docx/pdf/html/md/txt 自动或自定义复刻）、
  v2.13 完全复刻模式 exact-replication（原刊每页为不可变矢量底版 → 逐页建模 → 1:1 零偏差复制
  → 文字/图片/图表三类内容槽位替换 → 槽位外逐像素 100% 相同验收；TIME_WEEKLY 与
  TIME_SPECIAL_EDITION 双档案卡拆分，可推广到任意期刊）、
  v2.14 实战反哺·零偏差内容工程与细节门禁（弃用 apply_redactions 改覆盖式替换 + 采样中位色精确覆盖
  + WCAG 对比度择优 + CJK 行高静默失败防护 + 漂移页分级局部降级；内容流剥离版权/附录并按全书
  N 等分取完整语义短语；右脑优势构图量化、多刊合璧选页配额、细节体检八门门禁、构建报告契约、
  SKILL 版本治理 SOP；配套 semantic_stream.py / detail_audit.py / templates/quad-exact/）。
  输入一本书的要点/金句/结构，输出图表主导、少文字、出版级排版笔记（HTML/PDF/PPTX/长图）。
  触发词：读书笔记、生成笔记、可视化读书笔记、一图解千言、图表化笔记、读书分享、书摘卡片、
  reading notes、读书笔记PPT、读书报告、精华笔记、营销笔记、情绪开关、咨询级笔记、论证型笔记、
  图形复刻、复刻图表、位图转矢量、图片超分、思维导图导出、图表工具链、设计系统、品牌风格、
  UI规范检索、思维模型、模型图型、马斯洛/金字塔/SWOT、飞轮/复利/二八/冰山/决策树、文生图、
  竖版笔记、杂志风笔记、国家地理风格、NG风、横版杂志、HBR风、期刊复刻、年度精选、
  科研图表、学术图表、SCI 配图、期刊合规、色盲安全、Okabe-Ito、森林图、KM 曲线、雨云图、
  山脊图、哑铃图、复合多面板、PRISMA、误差棒、600dpi、4K 图表、4K 出图、投稿包、数据契约、
  期刊设计语言、杂志风格复刻、Bloomberg风、Science风、Time风、Vogue风、New Scientist风、
  期刊语料、杂志语料、期刊排版实测、图片型PDF、期刊知识库、4K 复刻、期刊级 4K、
  高保真模仿、复刻验收、期刊模仿、四门验收、IMA 知识库、七维设计、任意格式复刻、
  电子书复刻、期刊设计思维、财经拆解、封面设计、完全复刻、1:1 复刻、逐页建模、
  exact replication、exact-replication、版式全复刻、版式 1:1、
  内容槽位替换、零偏差验收、其他杂志也一样、四刊合璧、多刊选页、右脑优势、构图量化、
  覆盖式替换、中位色精确覆盖、对比度择优、语义片段、全书覆盖采样、细节体检、细节门禁、
  分级降级、内容工程、版本治理、技能升级反哺、同一把尺量三次、进一步优化细节。
metadata:
  author: wdj
  version: 2.14.0
  license: MIT-0
---

# 一图解千言 · 出版级读书笔记生成器（reading-notes-master v2.14.0）

将任何一本书的精华内容，转化为**图表主导、少文字、一图解千言**的出版级读书笔记。
双透镜实证：排版美学来自 31 份样本的程序化实测（字体/字号/色板/结构）；
**视觉语法**来自 30 份语料逐页扫描（图像/矢量对象 + 字符密度 → `notes_study/visual_metrics.json`）：
冠军语料图表主导页占比 73%–98%、每页字符中位数 106–204c、反面教材文字墙 1,025c/页。
**核心原则：先图后文。每一页先选器型，再填文字；选不出器型的内容不配单独立页。**

## 快速开始

0. **设计智能前置**（v2.4 新增，Step 0）：判语言受众 → 跑 `design-intelligence/ui-ux-pro-max/scripts/search.py`
   英文关键词检索 → 指定品牌则读对应 DESIGN.md → 产出《设计决策单》（风格/主色/字体/禁项）。
   完整流程与降级路径见 `references/design-intelligence/INDEX.md`。
1. **收集原料**：书名、作者及履历、2–3 个核心问题、章节结构、每章要点与金句、推荐背书（可选）。
2. **选原型**：查 `references/content-framework.md` §3（六大叙事原型决策树）。
3. **图表化转译**（v2 核心步）：逐条扫每章要点，按 `references/visual-grammar.md` §2 映射表
   把文字转成器型清单（见"时间"画轴线、见"编号"拆卡片、见"数字"放大数、见"框架"连节点…）；
   **同时跑思维模型库信号匹配**（v2.5）：命中模型信号的，直接调用其标准图型构图
   （`references/mental-models-library/INDEX.md` 全量信号速查 / `models-catalog.md` 100 模型全表）。
3.5 **科研图表增强 · 4K**（v2.9）：器型清单里出现可量化数据关系时，查
   `references/academic-chart-system.md` §2 双层决策树补「科研图型」列；有真数据 →
   `scripts/figure-bridge.py` 出真图（**默认 4K**：位图 ≥3840×2160、矢量等效；`--verify` 过 G1），
   无真数据 → 按 §4 用 `templates/academic-charts.css` 画 HTML/SVG 器型并在图注标「示意」；
   **所有图型图表一律 4K 级**，任何低于 4K 的位图不得发版。
4. **取色排页**：《设计决策单》优先，其次查 `references/design-system.md` §3.2 改模板 `:root` 三变量换肤；
   按九大模块序列复制模板 section，内容页按 **图解页:hero图文页 ≈ 6:4** 配比铺器型，每 2–3 页切 `.alt`；
   氛围资产（封面/hero/金句背景/篇章）按 v2.5 文生图规范生成，**每本 ≤5 张**。
   **摄影集/自然/历史/人物类** → 改走竖版：读 `references/ng-magazine-layout.md`，
   画页面地图 → 用 `templates/ng-magazine/generator-template.py` 分片生成 →
   `build-template.py` 出三格式。
   **商业期刊/杂志文集/多主题合集** → 改走横版杂志：读 `references/hbr-magazine-layout.md`，
   画页面地图（每章 11 页节奏）→ 用 `templates/hbr-magazine/generator-template.py` 分片生成 →
   `build-template.py`（Chrome headless）出 PDF/PPTX。
5. **导出**：按 `templates/output-pipelines.md` 出 PDF/PPTX/长图。

## 工作流（v2.9：设计智能前置→选型→定调→转译→科研增强(4K)→排页→导出，0.5 步判版式）

### Step 0.5 判版式（v2.7 升级）——16:9 幻灯片 or NG 竖版杂志 or HBR 横版杂志

三路版式决策树（Step 0/1/2/3 完全共用，只有排页与导出分叉）：

| 判断信号 | 去向 |
|---|---|
| 摄影集/自然/历史/人物/艺术类、图片资产充足、打印翻阅 | **NG 竖版杂志**（跳转"国家地理杂志竖版版式"章节） |
| 商业期刊/杂志文集/多主题合集、封面与图表资产交错、要"原刊复刻/年度精选"感 | **HBR 横版杂志**（跳转"哈佛商业评论横版版式"章节，612×756pt 美式开本） |
| 单主线方法论/数据类、投屏演示 | **默认 16:9 工作流** |

信号表与锚点参数见 `references/hbr-magazine-layout.md` §1（横版）与
`references/ng-magazine-layout.md` §1（竖版）。

> **v2.10 增强**：三路只定画布走向；**页面语言**（字体 DNA/色板/栏数/图片密度）从
> `references/magazine-design-corpus-2026-10.md` §六 按内容类型取——同一竖版画布可分别
> 用 NG 语言（摄影）或 Science 语言（学术），同一横版画布可用 BBW 语言（商业高密度）
> 或 Barron's 语言（财经克制）。拿到期刊 PDF 参考时先过语料库 §一 判型（矢量型/图片型）。

> **v2.11 增强（期刊 4K 复刻闭环）**：选定 profile 后，页面语言参数直接用
> `scripts/journal_4k_check.py --list` 内嵌的 14 张档案卡（与语料库同源实测值）；
> 生成完成后**必跑四门验收**：`journal_4k_check.py <rendered.pdf> --profile <名> --json report.json`
> （J1 字体 DNA / J2 色板签名 / J3 栅格边距 / J4 4K 像素，exit 0 才交付）。
> 方法论、DPI 反推公式、六步工作流与 8 条陷阱库见
> `references/journal-4k-replication.md`。「高保真模仿」不凭感觉，实测数字闭环。

### Step 0 设计智能前置（v2.4 新增）——先检索，后决策

**任何笔记动笔前必跑**，把"凭内置映射表猜风格"升级为"证据驱动定调"：

1. **判语言/受众**：书籍内容或目标读者为中文 → 先读 `references/design-intelligence/ui-ux-pro-max-cn/SKILL.md`
   （中文字体栈/色彩文化/微信小程序规范/国内技术栈/五大行业规则/中文交付清单）。
2. **跑引擎检索**（英文关键词；中文需求先译再检，如"教育平台首页"→ `education platform landing page`）：
   ```bash
   python3 references/design-intelligence/ui-ux-pro-max/scripts/search.py "<english query>" --domain style
   # 定调三件套：--domain style（风格）/ color（配色）/ typography（字体）
   # 按需追加：--domain landing|product|chart|ux；--stack html-tailwind|nextjs|react|vue…
   # 一键聚合：--design-system -p "项目名"（五域汇总推荐；勿加 --persist，那会往 cwd 写文件）
   ```
3. **品牌风格**：用户指定品牌（"做得像 Vercel/Notion"）→ 读 `references/design-intelligence/awesome-design-md/references/<brand>.md`，
   取令牌并入模板 `:root`；未指定 → 按该技能"项目类型→推荐品牌"表主动推荐 3–5 个让用户选。
4. **产出《设计决策单》**并带入后续步骤：风格方向 / 主色与辅色（hex）/ 字体搭配 / 器型偏好 / 禁项
   （品牌 Do's&Don'ts + 中文场景禁忌，如电商忌大面积暗色、金融忌红色表亏损）。
5. **超出覆盖**：需求在四层能力之外 → 查 `references/design-intelligence/awesome-design/SKILL.md`
   决策表，向用户推荐外部技能（只推荐，不擅自安装）。
6. **期刊语言路由**（v2.10）：用户想要"杂志感/像某本刊物"或内容天然贴合某类期刊
   （商业/科研/时尚/科普/特辑）→ 查 `references/magazine-design-corpus-2026-10.md` §六
   路由表选语言，把该语言档案卡的字体 DNA/签名色板/栏数/图片密度并入《设计决策单》
   （可与 NG 竖版/HBR 横版/16:9 任一路叠加使用）。

> 引擎不可用（无 python3/脚本报错）→ 降级读 `design-intelligence/ui-ux-pro-max/data/{styles,colors,typography}.csv`；
> 再不济退回内置映射表，不阻塞交付。中文场景永远可读 cn 规则（纯 Markdown 无执行依赖）。

### Step 1 选型
- 数据/年表多 → **D 数据复盘型**；名家背书强 → **E 背书营销型**；步骤工具清晰 → **B 工具方法型**；
- 章节多需自测 → **C 结构化文档型**；故事案例为主 → **A 叙事演绎型**；条目可分组 → **F 主题分组型**。

### Step 2 定调
- **《设计决策单》（Step 0 产出）优先于内置映射表**：两者冲突时以检索结果为准，并在交付说明中注明依据。
- 未跑 Step 0 时主题色查映射表（投资红 `#C20001` / 金融史青绿 `#208A88` / 战略蓝 `#537CC3` / 科技暗色 / 治愈薄荷绿 / 心理暖土系…）。
- **营销/情绪类内容**（出现痛点/痒点/爽点/燃点/爆点、情绪开关、三感三力等信号）→ 直接取
  `references/emotion-marketing.md` §1 五色情绪光谱（酒红/暖橙/金/猩红/电紫 + 暖纸 + 深紫墨），
  案例与四法矩阵同文件 §2–§4。
- 字体四字重 ≤700；字号阶梯（16:9）：封面 64–120 / 篇章 42–56 / 页标 34–40 / 正文 20–24 / 注释 14–18。
- v2 质感：负字距渐进、展示行高 1.08–1.15、耳语边框 + 三级柔影 + 圆角 8/12/16。详见 `references/design-tokens.md`。

### Step 3 图表化转译（Chart-First 核心）
- 对每章要点逐条跑 `visual-grammar.md` §2 映射表，产出**全书器型清单**（页号→器型→素材），
  动笔写 HTML 前完成；器型优先级按实测信号强度：时间线/阶段带 ≫ 编号卡 ≫ 大数字/公式卡 ≈ 框架图
  ≫ 流程链 ≫ 图标网格 ≈ 双栏对比 ≫ 漏斗 ≈ 环形 ≫ 金字塔 ≫ 象限。
- 铁律：数字必须可视化（大数字卡/图表标注）；同一章器型不相邻重复；全书 ≥6 种器型、每章 ≥2 种。
- 选不出器型的内容（纯故事/情绪）→ hero 整页图 + ≤80 字 + 图注药丸，或降级并入相邻页。
- **论证型内容页**（商业书/方法论书/数据复盘类，出现"因为/导致/证明/取决于"等论证信号）→
  升级到 `references/consulting-craft.md` 工艺：标题改判断句（§2）、按叙事弧线排页（§1）、
  图型过数据契约（§5）、机制图带证据状态（§8）。
- **图表类型交叉验证**（v2.4）：器型清单中的"数据关系"类（趋势/对比/占比/分布/漏斗），
  可用 `design-intelligence/ui-ux-pro-max/scripts/search.py "<data relationship>" --domain chart`
  校验图表选型与配色/可访问性建议，与 `chart-catalog.md` 冲突时取更具体的可访问性指引。
- **中文场景加固**（v2.4）：受众为中文读者时，器型与措辞过 `design-intelligence/ui-ux-pro-max-cn/SKILL.md`
  行业规则（如教育类忌花哨动画、金融类数字用等宽字体），落地到组件文案与图表标注。
- **思维模型库路由**（v2.5，Chart-First 的第二信号源）：逐章扫描内容，命中
  `references/mental-models-library/INDEX.md` §2 的全量信号速查表（或 `models-catalog.md`
  100 模型全表的"内容信号词"列）→ 调用该模型的**标准图型构图**（10 大图型族模板），
  产出《模型-图型清单》（章号→模型→族）并入全书器型清单；一章可命中多个，取最强 1–2 个，
  可叠加（如 #01 机会成本 + #58 二八定律 = 取舍矩阵 + 帕累托聚焦）。
  模型图必须过"图型-内容契约"（模型定义要素齐全、节点标注 ≤12 字、遮题可读、与文字预算兼容）。

### Step 3.5 科研级图表增强（v2.8 新增）——数据关系 → 真图 / 器型

沿用 Step 3 的《器型清单》，新增两列：**科研图型 slug** 与 **数据契约**。判据与硬纪律见
`references/academic-chart-system.md` §2，此处只记动作顺序：

1. **判有无真数据**：书里给出可复现的数值/表格/样本 → 走真图；只有观点与比喻 → 走 HTML/SVG 器型，
   **禁止拿示例数据伪装成原书证据**，示意必须在图注写「示意」。
2. **跑第二层决策树**：比较/构成→bar·stacked_bar；分布→box·violin·raincloud·ridgeline；
   两时点→paired·slope·dumbbell；趋势相关→line·scatter；矩阵→heatmap·pca；
   集合→venn·upset；证据强弱→forest·funnel；留存→km；重点高亮→volcano；
   逐例排序→waterfall·swimmer；一页多层结论→composite；流程→diagram·prisma。
3. **一页只留 1 个主器型**：科研图型是该器型的「数据化实现」，不是叠第二张图；
   数据关系与文字信号冲突时以数据关系为准，叙事标题仍用判断句。
4. **出图**：
   ```bash
   python3 scripts/figure-bridge.py --check
   python3 scripts/figure-bridge.py --type <slug> --data <ch.json> --out assets/fig/<name> \
     --theme okabe-ito --journal nature --column double --formats pdf,png \
     --resolution 4k --verify --alt --caption
   ```
   批量用 `--pipeline assets/figures.json`（桥接器逐条过校验闸门 + G1 + G5，出 `.bridge-report.json`，
   每项带 `resolution` 实测字段）。`--resolution 4k` 为默认值，可省略；显式豁免才用 `auto`。
5. **过五门**：G1 真实墨迹重叠（`--verify`，exit 2 必须修）→ G2 最小字号 → G3 白底/灰度可分辨
   → G4 确定性与旁车 → **G5 4K 分辨率**（`[4K OK] W×H = X MP ≥ 3840x2160`）；任一不过不发版。
6. **落地版式**：`templates/academic-charts.css` 提供 9 色板 / 9 期刊令牌与 `.af-*` 组件；
   图例用预留顶部带、端点留 ≥4% pad、靠边标注内翻（§4 构造性避让三铁律）。

> 依赖坑：WorkBuddy 内置 python 缺 matplotlib/scipy，桥接器自动探测系统 python；
> 别往内置环境 pip install。CSV 会静默丢失误差棒与复杂 schema，一律 JSON。

### Step 4 排页与预算裁剪
- 页面序列：`封面 → 书档速览 stat卡 → 作者 → [背书] → [为什么读] → 目录 → (篇章 → 内容页×n)×PART → 金句×2–3 → 思维导图 → 封底`。
- 文字预算硬上限：图解页 ≤120 字、卡片页 ≤150 字，单页 >300 字=文字墙违规必须返工；
  超页时先砍文字页、不砍器型页。
- 器型实现查 `references/chart-catalog.md`（10 类组件 HTML/SVG）；每页 ≥1 个视觉锚点，0 锚点页禁发。
- **品牌风格对齐**（v2.4）：若 Step 0 选了品牌 DESIGN.md，其 Do's&Don'ts 与组件规范视为硬约束
  （如 Vercel 黑白精准、Stripe 紫渐变+轻字重），与本文件其他规则冲突时品牌规范优先。
- **中文交付清单**（v2.4，中文受众必过）：中文字体栈 fallback 完整 / 中文行高 ≥1.6 /
  按钮与 CTA 为中文 / 数字字体与中文协调 / 375–1440px 覆盖主流中文设备 / 中文屏幕阅读器兼容。
- **氛围资产规划**（v2.5）：封面主视觉 / hero 意象图 / 金句背景 / 篇章过渡氛围图——
  四类共 ≤5 张，按下节文生图规范生成；其余全部器型化，不滥用生成图。
- **论证页按咨询级五区骨架排布**（`consulting-craft.md` §4）：结论型标题→主展品→支持证据+限定→
  含义或行动→来源；每页恰 1 个收束、标题全页最大字级；同排模块填充率差 ≤15pp（§9）；
  16:9 容量先算后填（§10），超容量砍内容不缩字号。

### Step 5 导出交付
- `templates/reading-notes-template.html` 为骨架（12 类页面示例与 SVG 组件）。
- 导出命令与命名规范见 `templates/output-pipelines.md`。

## 风格定制（v2 出版级令牌）

模板 `:root` 分两层，换肤只动第一层：主题层 `--c-primary / --c-primary-soft / --c-accent`
（**先查《设计决策单》，再查映射表**）；质感层（勿动）暖墨/耳语边框/三级柔影/圆角阶梯/暖纸 `#F7F5F2`/衬线。
内容页每 2–3 页加一次 `.alt`；金句页自动衬线 500。护栏详见 `references/design-tokens.md`。
v2.4 起主题层令牌可来自三处：Step 0 检索结果 > 品牌 DESIGN.md > 内置映射表。

## 图形资产管线（v2.3 新增）——任何图型/图片/图表，复刻或生成双通道

笔记所需图形资产，两条路径全覆盖（工具版本/安装/踩坑详见 `references/graphics-toolchain.md`）：

- **路径 A · 原样复刻**（复刻既有 PDF/PPTX 笔记的图形）：
  PyMuPDF 分层提取 → sn-image-base VLM 看图 → `scripts/superres.sh` 4× 超分（Real-ESRGAN）→
  `scripts/bitmap2vector.sh` 位图→矢量描摹（vtracer 彩色 / potrace 黑白）→ 组件重画。
  位图照片先超分再描摹，质量翻倍。
- **路径 B · 从文字生成**：
  流程/时序/甘特 → `scripts/mermaid-export.sh`（mmdc 三格式，已绕开 -w/-H 与 Chromium 下载坑）；
  全书结构一图流 → markmap（md→交互 HTML）；坐标轴级精确图表 → `scripts/clip-chart.sh`（.clp 文本→SVG）；
  MCP 宿主可直连 cognigraph-mcp-server（4 工具，配置见 graphics-toolchain.md §5）。

**对接工作流**：Step 3 器型清单中"流程/关系"类优先 B4 出 SVG 内嵌；Step 4 需要位图素材先 A6 超分；
Step 5 导出前统一 16:9 校验。中国市场约定：涨红跌绿、货币 ¥。

## 思维模型库（v2.5 新增）——信号→模型→图型，构图建模层

全量收录《万物皆模型》**100 个思维模型**（每模型：一句话定义 + 内容信号词 + 构图要点），
按 **10 大图型族**组织（层级金字塔 PY / 矩阵象限 MX / 循环反馈 CY / 曲线函数 CV / 流程链条 FL /
对比对立 CP / 网络系统 NW / 机制杠杆 MC / 决策分叉 DK / 树形分解 TR）。

- **总入口**：`references/mental-models-library/INDEX.md`——四步用法、全量信号速查表（101 条）、
  文生图 prompt 模板、与工作流对接表。
- **全量档案**：`references/mental-models-library/models-catalog.md`——100 模型逐条
  （定义/信号词/族/构图要点）+ 10 族构图模板总表 + 图型-内容契约。
- **用法**：Step 3 转译时扫描信号词 → 命中即调用对应模型的标准图型构图
  （同族模型共用构图法，换模不换构图）；模型图须过"图型-内容契约"。
- **典型命中**：见"选择/取舍"→#01 机会成本（CP）；"利滚利/指数"→#57 复利（CV）；
  "结论先行/汇报"→#62 金字塔（TR）；"80/20"→#58 二八（CV）；"心流/沉浸"→#33（CV 通道）；
  "启动难/飞轮"→#75（CY）；"护城河/壁垒"→#100（NW）。

## 文生图规范（v2.5 新增）——氛围资产五要素公式

**边界铁律**：器型/结构化图示（矩阵、循环、曲线、树形）一律 HTML/SVG/脚本绘制，**不作文生图**
（文字标注精度不可丢）；文生图只做四类氛围资产——封面主视觉、hero 意象图、金句页背景、篇章过渡页。

**Prompt 五要素公式**（详见 mental-models-library/INDEX.md §3）：
```
[主体意象：取模型库该模型的视觉意象] + [图型几何：按图型族的构图指令]
+ [风格令牌：flat vector / 暖纸 #F7F5F2 /  ink #1A1A1A / 三级柔影 / 耳语边框 / editorial print]
+ [主题色：Step 0《设计决策单》主色 hex，少量使用] + [负面约束：no text/letters/watermark/logo/3D/clutter]
```

- **各族模板**：10 个图型族各有一条 prompt 主干（PY 层叠金字塔 / MX 软方块网格 / CY 墨线环 /
  CV 单线曲线+主色点 / FL 节点链 / CP 镜像对峙 / NW 稀疏网点 / MC 杠杆放大镜 / DK 分叉路径 / TR 根枝树）。
- **数量纪律**：每本笔记文生图 ≤5 张（封面 1 + hero ≤2 + 金句背景 ≤2）；尺寸
  封面 1600×900 / hero 1200×800 / 背景 1600×900（压字前高斯模糊 8px）。
- **降级**：无可用图像生成工具 → 退化为"几何氛围图"（SVG 大色块 + 主题色渐变 + 器型剪影），不阻塞交付；
  产物统一存 `assets/generated/` 并在交付说明标注工具与 prompt 摘要。

## 国家地理杂志竖版版式（v2.6 新增）——NG Portrait Magazine Layout

为摄影集/自然/历史/人物/艺术类书籍准备的**杂志级竖版**管线。全部参数从 148 页摄影集
60 页实战交付逆向沉淀（0 破图/0 裁切/0 挤压，PDF+PPTX 各 11.1MB）。
**详细手册：`references/ng-magazine-layout.md`；资产：`templates/ng-magazine/`（mag.css 设计系统 + build-template.py 流水线 + generator-template.py 生成器骨架）。**

- **版式锚点**：660×960px 画布（=495×720pt=6.875×10in）、56px 边距、34px 黑条页眉
  （刊名+PART+页码）与页脚（黑条+黄星+页码）、`.bd` 内容区 flex 列（top:46/bottom:44）。
- **设计系统**：NG 黄盒色板（墨 `#231F20` + 主题黄 `#FFD201` + 金/铜/酒红/红 + 暖纸三阶）；
  三字体栈——标题正文衬线（宋体族）、标签大写 sans 宽字距、一切数字 DIN；
  换肤只改 `:root` 色板五件套 + serif。
- **12 类页面模板**：封面/黑底目录/章扉/满版摄影/文章页（双栏+首字下沉+侧栏+粗顶线引文）/
  解剖标注/大数字 statgrid/图鉴 entrygrid/时间轴/价格条/思维导图/黑底金句页，
  另备半版图带/对比双栏/图表盒/阅读地图/封底——HTML 骨架速查见手册 §4。
- **页面地图法**：先画地图后写页面；成品页数=原书 **1/3~1/2**（148→60=40.5%）；
  每 PART 以章扉开头、内容页按 信息页:文章页≈8:2、每 PART ≥1 满版页、器型不相邻重复；
  每页 `<!-- P42 主题 -->` 注释，收尾"阅读地图"页靠注释回填页码。
- **生成器分片生产（硬纪律）**：60 页 ≈500KB HTML 必须拆 3~6 个 Python 生成器
  （每片 9~13 页、**≤20KB** 防 Write 截断），三函数头（HD/FT/FOLIO）+ `P=[]` +
  `P.append(...)` + 尾部合并写出；系统 python3 跑生成器，build 才用 playwright 环境。
- **六步 build 流水线**（`build-template.py` 全内置）：合并（regex+页数 assert）→
  Playwright 三重校验（破图 naturalWidth / 裁切 DOM 行走 / 挤压 scrollHeight）→
  @2x 逐页截图 → PDF（`width='6.875in'`，**pt 单位会报错**）→ PPTX（JPEG q87 重建，
  体积 −75%）→ 交付打包；追加 PIL 方差空白页检测（金句黑页豁免）。
- **6 条踩坑库**：pt 单位 / SVG defs 小写 tagName 误报（toUpperCase 黑名单）/
  沙箱 mkdir EEXIST / 图片相对路径 grep 预校验 / PPTX PNG→JPEG / flex 容器漏
  `min-height:0` 被脚区吃掉——完整对照表见手册 §8。
- **文字预算**：文章页双栏 ≤400 字（首字下沉+侧栏+引文占版面），信息页 ≤150 字不变。
- **文生图竖版化**：封面/满版/章扉出 1320×1920 竖构图，prompt 加
  `portrait orientation, vertical composition, magazine full-bleed photography`。

## 哈佛商业评论横版版式（v2.7 新增）——HBR Landscape Magazine Layout

为商业期刊/杂志文集/多主题合集准备的**杂志级横版**管线。全部参数从 88 页
《哈佛商业评论 2025 年度精选》实战交付逆向沉淀（原稿 12 期 2,291 页 → 88 页 = 单期均页 46%，
0 溢出/0 空页/MediaBox 恒定，PDF 11.7MB + PPTX 88 页 16:9 双验收通过）。
**详细手册：`references/hbr-magazine-layout.md`；资产：`templates/hbr-magazine/`
（mag.css 设计系统 + generator-template.py 12 页型构建器 + build-template.py 流水线 + scrim/ 遮罩 PNG）。**

- **版式锚点**：612×756pt 画布（=8.5×10.5in 美式杂志开本）、内容页 padding 44/60/40pt、
  `@page { size: 8.5in 10.5in; margin: 0 }`（margin:0 是全出血前提）、folio 顶 34pt / pageno 底 24pt。
- **设计系统**：刊名 DNA 四色——刊名红 `#E41824` + 橙金 `#F09C18` + 墨色 `#231F20` + 米色 `#F4F1EA`；
  双字体栈——sans（GTAmerica→PingFang SC，展示/正文）+ serif（Tiempos→Georgia，导语/说明）。
  换肤只改四色 + 字体栈。
- **12 类页面模板**：全出血封面（刊名+年份徽章+44pt 大标题+6 连封面条）/ 150pt 巨号章隔页
  （竖排英文）/ 非对称编辑开篇（照片 310pt + 文字栏，me-flip 翻面）/ 整页大图表（原刊图表
  contain 全宽 + 解读框）/ 100pt 巨型统计 / 双栏大字文本 / 全出血照片特写 / 全出血金句页 /
  分组细线目录 / 4×3 期号总览网格；另备 3 个 SVG 大图表组件（大条形/圆环/步骤带）。
- **每章 11 页固定节奏**（实测零溢出，照抄）：章隔→编辑→大图表→统计→文本×3→照片→金句→
  编辑(翻面)→文本。全书 = 前置 7 + N 章×11 + 后置附录；成品页数 = 原书 1/3~1/2（文集按单期均页口径）。
- **Chrome headless 打印管线**（非 Playwright）：`--headless=new --user-data-dir=<临时>` +
  `--print-to-pdf`，**CSS 必须内联进 full.html**；遮罩渐变必须预渲染 PNG——
  CSS linear-gradient 叠照片会把照片光栅化进平铺 Pattern（体积 ×2.4）。
- **验收双轨**：PDF pymupdf 三重（MediaBox 恒定/文本零溢出/零空页）+ PPTX 结构越界与
  LibreOffice 实渲染（边缘溢出/重叠）；瘦身靠 XObject 内容哈希去重（18.3→11.7MB），不做页内有损重压缩。
- **8 条踩坑库**：Pattern 光栅化 / 背景缺 no-repeat / full.html CSS 快照与 Chrome file:// 缓存 /
  PPTX kicker 固定宽越界 / 总览网格 3×4 超页高 / q72 重压缩收益仅 5% / 资产路径指错目录——
  完整对照表见手册 §8。
- **文生图横版化**：封面/章隔/照片/金句出横构图 1600×1000，prompt 加
  `landscape orientation, magazine full-bleed photography, editorial`；图表一律原刊提取或 SVG 重绘。

## 科研级图表体系（v2.8 新增）——Academic Chart System

**来源双实证**：本机 `academic-figures v5.9.0`（docsor1212，MIT-0；38 规范图型、9 色板、
9 期刊 JSON、YAML 流水线、`--verify` 像素级重叠检测、`audit_pdf.py` 字号门禁、退出码 0–6）
＋《38种科研图表收集整理报告（样例增强版）.pptx》93 页（38 图型 × 11 大类 × 每型
「用途/场景/要点/提示」四段式 + 34 张引擎模板样例 + 4 张真实数据样例 + 选型决策树 + 投稿规范）。
**完整手册：`references/academic-chart-system.md`**（§1 全表 / §2 决策树 / §3 令牌 / §4 组件 /
§5 门禁 / §6 红线 / §7 桥接 / §8 工作流对接）。

### 38 图型 × 11 大类（slug 速查，逐条映射见手册 §1）

| 大类 | 图型 | 笔记里最常用 |
|---|---|---|
| 一 比较与构成 4 | `bar` `hbar` `grouped_bar` `stacked_bar` | **排名条**（长书名/概念）、100% 堆叠带 |
| 二 数据分布 4 | `box` `violin` `raincloud` `ridgeline` | **云+点三位一体**、阶段带×密度（分布漂移） |
| 三 配对与变化 3 | `paired` `slope` `dumbbell` | **认知改变页**（读前 vs 读后）、差距条 |
| 四 趋势与相关 3 | `line` `scatter` `dual_axis` | 时间线数据化、象限点坐标；双轴图慎用 |
| 五 矩阵多变量 3 | `heatmap` `cluster_heatmap` `pca` | **一页纸表格（色阶版）** |
| 六 集合与组学 3 | `venn` `upset` `volcano` | **概念交集图**、重点高亮散点 |
| 七 推断与 Meta 4 | `forest` `subgroup` `funnel` `galbraith` | **证据强弱尺**（含汇总菱形） |
| 八 生存分析 3 | `km` `cif` `rmst` | 留存阶梯线（习惯/用户留存借用） |
| 九 预测模型 5 | `roc` `calibration` `dca` `nomogram` `rcs` | **承诺-兑现对照**、净收益决策页 |
| 十 一致性与疗效 3 | `bland_altman` `waterfall` `swimmer` | 逐例瀑布、时间线（逐行版） |
| 十一 组图与流程 3 | `composite` `diagram` `prisma` | **A/B/C 组图主版式**、筛选漏斗 |

### 设计令牌（手册 §3 有全表）

- **9 套色板**：默认 `glm`（色盲安全、白底 4.5:1）；投稿/无障碍 `okabe-ito`；
  期刊联动 `nature`/`lancet`/`nejm`/`science`；另有 `cool` `classic` `conservative`。
  别名 `okabe`/`colorblind`→okabe-ito、`npg`→nature、`aaas`→science。
- **9 套期刊预设**：`nature` 89/183mm·7pt·min5pt·600dpi｜`lancet` 85/183·8·6·600｜
  `science` 55/120·7·**5**·600｜`cell` 85/176·8·6·300｜`nejm` 89/190·8·6·300｜
  `jama` 89/183·8·6·600｜`ieee` 89/181·8·6·600｜`cma` 80/170·8·6·600｜`cn-core` 80/170·9·6·300。
  `--journal` **锁宽**（`--width` 被忽略）；双栏 183mm 可作 NG「图表盒」/ HBR「整页大图表」栅格基准。
- **硬规范**：白底零容忍深色；隐藏上/右框线；网格 alpha 0.15–0.3；单图 ≤7 色；
  编码色数 ≤ 实际组数；红绿不共现编码关键信息；对照组恒中性色、处理组恒主色（跨页一致）；
  字号层级 轴标签 > 刻度=fs−1 > 注释 ≥6pt；误差棒 `1.5pt`/CI、参照线灰虚线；
  中国市场约定不变（涨红跌绿、¥）。

### 验收五门（手册 §5；v2.9 新增 G5 4K 门禁）

| 门 | 判定 | 工具 |
|---|---|---|
| G1 真实墨迹重叠 | 不信任 bbox 相交；200dpi 取墨迹连通分量 → 局部 600dpi 求最小距离 >0.05pt 判分离 | `--verify`（PDF only，`exit 2` 拒收） |
| G2 最小字号 | 默认 ≥7pt，nature/science ≥5pt，其余 ≥6pt；笔记正文 ≥14pt 不变 | `audit_pdf.py --min-size N --fail-below` |
| G3 白底与可分辨 | 白底、≤7 色、灰度转印仍可分（否则加斜纹/明度阶/形状三重冗余） | `academic-charts.css` 打印层 |
| G4 确定性与可复现 | 同输入→字节相同；剥离 CreationDate；期刊预设下禁用 `bbox_inches='tight'` | `--audit` / `--repro` / `--alt` / `--caption` / `.bridge-audit.json` |
| **G5 4K 分辨率**（v2.9） | 位图**长边 ≥3840 且短边 ≥2160**（≥8.29MP）；矢量 PDF/SVG/EPS 等效；按 PNG IHDR 实测，不达标 `exit 2` | `figure-bridge.py --resolution 4k`（默认）；`[4K OK]` / `[4K FAIL]` / `.bridge-audit.json.resolution` |

### 4K 级输出（v2.9 新增）——所有图型图表同一把尺

- **硬标准**：位图 `max(W,H) ≥ 3840` **且** `min(W,H) ≥ 2160`；默认 600dpi 的主题（glm/okabe-ito 等）
  实测约 4739×3227 ≈ 15.3MP，本就超 4K；**期刊锁宽才是真正的风险点**（science 单栏 55mm 仅 2.17in，
  600dpi 只有 ~1300px 宽）。
- **自动反推 DPI**：`dpi = max(600, ceil(3840/图宽in), ceil(2160/图高in), 显式dpi)`，上限 2000；
  `science --column single` 实测自动提到 **1774dpi → 3841×2640 = 10.14MP 达标**。
- **双轨**：矢量（PDF/SVG/EPS）分辨率无关，视为等效 4K；位图 PNG/TIFF 必须实测达标。
  仅出 TIFF 时自动补一张 PNG 作像素校验代理。
- **一次自愈**：引擎内存护栏可能把 dpi 砍半 → 实测不达标时自动 `dpi×1.6` 重渲染一次；
  仍不达标打印 `[4K FAIL]` 并 `exit 2`，建议改 `--column double` / 去掉 `--journal` / `--resolution auto` 显式豁免。
- **HTML/SVG 版式同样 4K**：`templates/academic-charts.css` 新增 `--af-export-w:3840px` /
  `--af-export-h:2160px` / `--af-export-scale` 令牌；截图导出按 @2x/@4x 取 3840 长边，
  NG 竖版按 2160×3840、HBR 横版按 3840×4560 等比；**禁止把 1280×720 的幻灯片截图冒充 4K 图表**。
- **流水线**：JSON 流水线逐条过 G5 并把 `resolution` 实测写进 `.bridge-report.json`；
  YAML 流水线委托引擎时无法逐条过 G1/G5，桥接器会明确告警。

**构造性避让三铁律**（§4，优于事后目检）：图例/事实框用预留带而非浮动覆盖；
SVG viewBox 四周自留 ≥4% 端点 pad 防圆点/CI 帽裁半；最右/最上 10% 区域标注自动内翻。

**20 条反模式红线**（§6 全表）：白底 3D/渐变、红绿共现、>7 色、语义色跨图不一致、
误差棒不标 SD/SE/CI、星号无可溯源检验、手编 P 值、让引擎「自动拟合」nomogram/rcs/subgroup、
PH 不成立仍用 log-rank、有竞争事件仍报 1−KM、先排序后标注不同源索引、浮动图例碰运气、
显式 xlim 裁掉端点、靠边标注朝外、跨数量级共享 y 轴、误以为 `--width` 生效、
`--verify` 只加在 PNG 上、composite 嵌 diagram、PRISMA 数字不自洽、CJK 上下标字形缺失、输入未变反复重试。

### 资产与触发

- `templates/academic-charts.css`：9 色板 `[data-af-theme]` + 9 期刊 `[data-af-journal]` 令牌、
  `.af-legend-band` / `.af-end-label` / `.af-panels` / `.af-panel::before` 角标 / 打印白底层。
- `scripts/figure-bridge.py`：纯标准库；`--check` 探测引擎与系统 python；`--list types|themes|journals`；
  单图/JSON 流水线；渲染前校验闸门（必填/等长/数值有限/PRISMA 自洽，失败 exit 3 不落盘）；
  自动 CJK；**默认 4K**（`--resolution 4k` / `--min-long-edge` / `--max-dpi` / 自动 DPI 反推 /
  PNG IHDR 实测 / 一次自愈）；批量出 `.bridge-report.json`（含逐图 `resolution`）。
- 触发时机：Step 0《设计决策单》加色板与栏宽两栏 → Step 3 补科研图型列 → Step 3.5 出图过四门
  → Step 4 composite A/B/C 排页 → Step 5 矢量优先 + 旁车随交付。

## 期刊设计语料库（v2.10 新增）——Magazine Design Corpus 2026-10

**来源**：31 份 2026-10 热点英语期刊（NG 系 4/财经 3/科研 5/生活方式 3/时尚 2/新闻特辑 3/
报纸评论 4/设计工艺 4/科普特辑 1/中文 1）PyMuPDF 程序化实测——每刊抽样 ~12 页，提取
字体族/字号分布/矢量色板/图片密度/边距/栏数。语料同步归档 IMA 知识库「海外期刊杂志」。
**完整档案：`references/magazine-design-corpus-2026-10.md`**（§一 判型 / §二~五 12 类语言
档案卡 / §六 任务路由表 / §七 7 条实证定律 / §八 IMA 挂接）。

### 先判型，再取参（31 刊实测出的第一道工序）

| 型 | 实测判据 | 语料中的 7 刊 | 对策 |
|---|---|---|---|
| 矢量型 | 字体名真实且 ≥5 族、文本左边距 80–360pt 有意义 | 24 刊全部可提取 | 字体/色板/栅格全量入令牌 |
| 图片型 | ≤2 字体且只有 Helvetica、恒 1 图/页覆盖 100%、左边距恒 30pt | Guardian/NYT Magazine/NYT Book Review/Rolling Stone（位图）；Dessin/Psychologies/Home Design（扫描） | 只做视觉参考；排版参数从同类矢量刊借 |

### 12 类语言速览（详表与 hex 全量见语料库 §二~五）

- **NG 系**（修订 v2.6）：官方字体实证 GrosvenorBook+Geograph（替代：Source Serif 4 / GT Walsheim）；
  主刊辅助橙 #E77741/天蓝 #B9E5FA，History 金铜 #C9A43F，Traveller 高饱和四色；主刊 145 图/页拼贴流。
- **财经**：BBW 5 栏 23 图/页+焦糖棕 #AD6B42 大色块（杂志感之王）；Barron's 46 字体+柔和四色
  （钢蓝/蜜桃/冰蓝，克制权威）；MoneyWeek Sabon+Univers 瑞士经典。
- **科研**：Science MillerDaily+学术蓝 3 栏宽边距（严肃）；New Scientist 品红 #CC1D4C 大色块
  （流量感）；SciAm 白底留白+黄点 #FFCA38（平衡）；Science News 浅蓝块 141 次。
- **时尚**：Vogue Saol 三栈+极窄边距 84pt 满版大图；Cosmo 荧光粉 #FF447E+L92 出血。
- **特辑**：How It Works 伸展无衬线 Saira/Khand+品红橙紫多巴胺；Time 特辑 display 24% 巨型标题
  （唯一例外，印证"正文主导律"）。
- **评论**：Spectator 复古衬线+海军蓝 #001346 大色块 200 次；Observer 820×1018 大报 3 栏。

### 7 条实证设计定律（§七 全文）

① 正文主导律：body 占 90–100% 是常态，display 巨字仅封面/章扉/特辑，每期 2–4 页封顶；
② 强调色预算律：单页 ≤1 个、整期 ≤2 个强调色（实测第 2 强调色用量普遍 <4%）；
③ 大色块签名律：品牌感=单一高饱和色的反复大面积出现（NS 品红 200 次/BBW 焦糖棕 146 次）；
④ 三栈律：衬线正文+无衬线标题+（可选）display，拒绝四族混搭；
⑤ 栅格分野律：财经科普 3–5 栏高密度，时尚评论 1 栏长文——栏数由内容定；
⑥ 边距个性律：图主导窄边距（84–143pt），文主导宽边距（264–354pt）；
⑦ 图片密度三型：拼贴流（23–145 图/页）/满版流（覆盖 ~100%）/克制流（覆盖 ~25%）。

**用法**：Step 0 产《设计决策单》时按 §六 路由取语言；新增期刊复跑
`magcorpus/analyze_mags.py`（判型先行）增量建档；需回看原文走 IMA `search_knowledge`。

## 期刊 4K 复刻闭环（v2.11 新增）——Journal 4K Replication

> 核心思想：**同一把尺子量两次**。语料采集（analyze_mags.py）与产物验收
> （journal_4k_check.py）用完全相同的度量方法——四门验收数字闭环，取代凭感觉模仿。

**四门验收**（`python3 scripts/journal_4k_check.py <rendered.pdf> --profile NG --json report.json`，exit 0 才交付）：

| 门 | 判定 | 容差 |
|---|---|---|
| **J1 字体 DNA** | serif+sans 两栈各自命中档案卡官方字体或替代字体前缀 | 每栈 ≥1 命中 |
| **J2 色板签名** | 签名色 ≥1 出现在矢量填充 top8（满版刊降级文字色/像素主色） | RGB 距离 ≤36 |
| **J3 栅格边距** | 边距比例 / 栏数 / 图密度分型与档案卡一致 | 边距差 ≤12pp、栏数差 ≤1、分型不换型 |
| **J4 4K 像素** | 位图长边 ≥3840 且短边 ≥2160；PDF 按内嵌位图逐图反推有效 DPI | 主图（显示宽 ≥25% 页宽）DPI ≥ 目标×0.9 |

**要点**：①验收对象用矢量 PDF（J1–J3 需文本层；PNG 交付另对 PNG 量 J4）；
②4K DPI 反推公式 `dpi = ceil(3840 / 页面长边英寸)`（NG 384 / HBR 366 / 16:9 @3x），
内嵌位图源 <4K 先走 v2.3 `superres.sh` 4× 超分；③降级卡（VOGUE/TIME_SPECIAL/QNWZ）
J1/J2 转 WARN 不 FAIL，J3/J4 仍硬门；④14 张档案卡内嵌于脚本（`--list` 一览），
与语料库同源实测、同参数度量（30pt bin / `^[A-Z]{6}\+` / 覆盖率上限 1.6）。
完整方法论见 `references/journal-4k-replication.md`（六步工作流 + 8 条陷阱库）。

## 期刊设计七维知识库（v2.12 新增）——Seven Dimensions + IMA 接入 + 任意格式管线

> **全量吸收闭环**：IMA「海外期刊杂志」知识库（kb `ima_kb_rDzPwmRH`：31 刊 PDF + 2 份实测汇总）
> 经七维蒸馏 → 任意格式电子书/材料 → 自动或自定义生成高清晰高密度高质量期刊复刻版。

**① IMA 云端知识库接入**（需要查原刊/检索设计知识时）：
- MCP 工具链：`mcp__ima-mcp__search_knowledge`（query 检索，中文关键词即可命中 31 刊设计要素）→
  `get_knowledge_list`（kb `ima_kb_rDzPwmRH`；limit ≤50；子文件夹 `10月热点英语期刊` 31 PDFs）→
  `get_media_info`（取原文）。
- 本地镜像：`magcorpus/`（analyze_mags.py + mags_metrics.json + summary.md）——离线优先用本地，云端用于语义检索与原文回看。
- 新语料归档：五步上传链（preflight-check.cjs → check_repeated_names → create_media → cos-upload.cjs → add_knowledge），详见 ima-skills。

**② 七维设计知识库**（`references/journal-design-seven-dimensions.md`）——选型时按维取规则：
| 维度 | 一句话规则 | 实测锚点 |
|---|---|---|
| 1 设计思维 | 版式哲学五型论：图先于文(A)/一图一世界(B)/密度即权威(C)/图文对半(D)/满版宣言(E) | 图密度 0.25→145 图/页光谱 |
| 2 设计模型 | 四模型：栅格模型（栏数=内容区÷目标栏宽，边距随栏数联动）/密度模型（五分型映射 DENSITY_TOL）/色彩模型（一刊一签名色+中性骨架）/字号模型（display/body 双轨） | 1 栏 436pt 边距 ↔ 5 栏 214pt |
| 3 图表语言 | 三范式：图阵叙事(BBW 23图页)/表格权威(Barron's)/论证配图(Science)；同页图表色系必须同族 | 签名色占比 3–15% |
| 4 版式栅格 | 三律：对称律（边距差<40pt=庄重）/偏移律（>150pt=视觉重心设计）/报纸律（30pt 窄边距=快报） | Cosmo L92/R367 |
| 5 照片采集 | 覆盖率四级采摄策略：>90% 单主角压字 / 60–90% 组照沉浸 / 30–60% 证据配图 / <30% 点缀 | 峰值 160% 出血合法 |
| 6 财经拆解 | 三范式路由：周度叙事→BBW 图阵型 / 个股财报→Barron's 表格型 / 组合通讯→MoneyWeek 型；中文财经用 BBW 骨架+红涨绿跌 | 正文黑占比 >90% |
| 7 封面设计 | 刊名框类型学（色块框/字标型/报头型）+ 压图文字色规则（白压图/黑压底/签名色点睛）+ 特刊 display ×6 | Time特辑 display 24% |

**60 秒定型**：材料类型 → 七维快速路由选型 → 档案卡取参数 → 渲染 → 四门验收。

**③ 任意格式电子书→期刊复刻通用管线**（`references/universal-ebook-pipeline.md`）：
- **格式矩阵**：epub/docx/pdf（原生+扫描 OCR 分支）/html/md/txt/mobi → 统一解析为 IR（章节树+资产清单）。
- **双源分离**（核心设计）：内容源（解析出的正文）与风格源（参照刊 PDF 或档案卡）分离——风格参数永远来自档案卡/实测，不来自内容源。
- **模式路由**：自动模式（内容信号探测→七维选型→报告交用户确认）/ 自定义模式（点名刊名直载档案卡）/ 混合模式（正文刊 A + 封面刊 B）。
- **五步管线**：解析归一 → 风格定型（版式令牌单）→ 结构映射（章节→栏目/金句→pull quote/数据→图阵）→ 渲染（P 矢量/G 位图双路径）→ J1–J4 四门验收交付。
- **批量模式**：多文件合批（同 profile 分组渲染），交付清单逐本记录四门结果。

## 期刊完全复刻模式（v2.13 新增）——Exact Replication

> **触发词**：完全复刻 / 1:1 复刻 / 逐页学习 / 逐页建模 / 内容槽位替换 /
> 零偏差验收 / 除了文字图片图表其他都要一样 / 「复刻其他杂志也一样」。
> 用户给出**真实原刊 PDF** 并要求「除内容可更新外其他全部一样」时，一律走本模式。

**契约**：`固定设计层`（画布 / 页序 / 页数 / 页面原型 / 栅格 / 栏位 / 边距 / 页眉页脚 /
页码 / 装饰矢量 / 图片位置与尺寸 / 图表图形 / 字体族名 / 字号 / 字重 / 字距 / 行距 /
颜色 / 基线）**不可变**；只有 `文字`、`图片`、`图表数据` 三类**内容槽位**可更新。
字形本身属「文字内容载体」随内容更新，但字号/字重/基线等设计参数必须固定。

**与风格近似复刻的本质区别**（不要混用）：

| | 风格近似复刻（v2.10–v2.12） | 完全复刻（v2.13） |
|---|---|---|
| 起点 | 档案卡参数 + CSS/HTML 从零排版 | 原刊每页作为不可变 Form XObject 底版 |
| 可动部分 | 整套设计都由生成器重建 | 只开三类内容槽位，其余像素不动 |
| 验收 | `journal_4k_check.py` 四门容差 J1–J4 | 逐像素零偏差：槽位外 100% 相同、未改动页 100% 相同 |
| 交付判据 | `PASS` 或降级卡 `WARN` | `verdict=PASS`；WARN 不交付 |
| v2.11 三本《穿透》系列 | 属于此类 | **不算**完全复刻 |

**决策表**：用户说「做成 XX 风格 / 高保真模仿 / 4K 复刻」→ 四门验收；
用户说「完全一样 / 只换内容 / 原刊照搬 / 其他杂志也一样」→ 零偏差验收（本模式）。
两者不确定时先问清，不要默认按风格近似处理。

> **不要把原刊 PDF 直接送进四门验收**。J4 是「4K 复刻产物」门，
> 目标 DPI = `max(卡 dpi, ceil(3840 ÷ 页长英寸))`，TIME 算得 366；
> 而真实原刊内嵌位图只有 300 DPI（印刷标准），所以原刊跑 J4 必然 FAIL，
> 这是预期行为而非档案卡错误。对 `Time_2026-09-28.pdf` 实跑为
> `J1 PASS / J2 PASS / J3 PASS (L Δ0.0pp, R Δ0.0pp, 栏 2 vs 2, 覆盖 47%)` / `J4 FAIL`。
> 四门只用于验收**按契约生成的产物**；完全复刻一律用零偏差验收。

**六阶段管线**（`scripts/exact_replication.py`，跨刊通用）：
1. `build_page_models(doc)` 逐页元素级建模（spans / images / drawings / 字号·字体·色阶 / x0 直方图）
2. `classify_archetype()` 原型分类
3. `replicate_1to1(src,out)` 用 `show_pdf_page()` 生成 1:1 矢量底版（阶段 A 零偏差凭证）
4. 槽位定义（text / image / chart / chart-redraw）+ `collision_report(models,slots)` **必跑预检**
5. `ExactEditor(...).apply_pack(slots,pack).save(out)` 注入新内容
6. `verify(src,out,masks,matrix=2.0,pad_px=3,out_json=...)` 零偏差验收

**三条硬约束（实测踩坑，违反即破坏设计层）**：
- `add_redact_annot(fill=None, cross_out=False)` + `apply_redactions(images=0, graphics=0, text=0)`
  才能只删文字；`cross_out` 默认 True 会画叉线。
- **碰撞检测不能省**：首字下沉大 W 的 bbox 常与正文首行相交，redact 会削掉其 ink，
  造成槽位外像素变化。必须预检并改选槽位，不能靠扩大 mask 掩盖。
- **基线用目标页原字体 ascender**（HaffnerTIME≈0.743），不要用替代字体的（≈1.05），
  否则新文字溢出槽位。T2 回退必须按字重映射（`tibo`/`hebo` vs `tiro`/`helv`）。

**字体资源边界**：原刊多为页级 Type1/PFA 子集，只含该页 glyph。
`T1` 目标页自身子集复用（字形 100% 原样）/ `T2` 字重映射 Base14 / `T3` CJK 扩展 `china-s`。
**跨页子集池已否决**——子集化后 `/Encoding` 重排，按 WinAnsi 写字节会取错 glyph。
详见 `references/exact-replication-contract.md`；模板在 `templates/time-exact/`；
按刊按子产品线的实测契约见 `references/journal-dna-cards.md`。

**档案卡修正**：`journal_4k_check.py` 现拆为 `TIME_WEEKLY`（567.03×756、
text-led、J3 实测 `margin_l=25.3 / margin_r=45.3 / cols=2 / cov=0.471 / dpi=300`）与
`TIME_SPECIAL_EDITION`（576×783、fullbleed、降级卡）两条独立卡；
旧 `TIME_SPECIAL` 键保留兼容但**不得用于常规周刊任务**。常规周刊与特辑绝不可共用一张卡。

## 实战反哺 · 零偏差内容工程与细节门禁（v2.14 新增）

> **来源**：2026-11-09/10 连续 5 轮真实交付逆向沉淀 —— NG 2026-10 主刊 140 页完全复刻（74.22MB，
> 四轮 `PASS`）、v6 4K 全画幅、v8 右脑优势全篇构图、《先发影响力》NG 竖版 4K 视觉笔记（40 页）、
> **四刊合璧 1:1 版式全复刻**（40 页 / `verdict=PASS` / `worst_outside=0.0` / 40 页全部有改动）
> 及其细节优化轮。全部数字来自程序化实测，非经验估计。
>
> **定位**：v2.13 定义「完全复刻契约」，v2.14 解决「按契约大规模落地时踩到的工程坑」，并补上
> v2.13 缺失的**内容层门禁**与**视觉细节门禁**。两者是同一条管线的上下游，不另起炉灶。

### 五层 MECE 拆解（互不重叠、完全穷尽）

| 层 | 解决的问题 | 关键实证 | 落点 |
|---|---|---|---|
| **A 渲染几何** | 内容怎么放上去而不破坏设计层 | `apply_redactions` 非局部副作用；覆盖色量化致 15.1% 色块；CJK 静默失败致 14 页无字 | `references/exact-content-engineering.md` §1–5 |
| **B 内容工程** | 放什么内容、是否代表全书 | 旧版只用书稿前 3.2%；版权页/电子书定价/献词误入正文 | 同文件 §6–7 + `scripts/semantic_stream.py` |
| **C 资产构图** | 用什么图、右脑优势够不够 | 页廊图片覆盖率 28%→67%；P16 暗像素 74%；四刊选页配额 | `references/visual-detail-qa.md` §2–4 |
| **D 验收治理** | 怎么证明合格、怎么固化 | 零偏差 `0.0` + 细节八门 + 构建报告契约 + IMA 归档 | 同文件 §1/§5–7 + `scripts/detail_audit.py` |
| **E 版本治理** | 经验如何回哺技能、不靠口头传承 | MECE/金字塔/假设驱动 + 持续进化机制 + 同一把尺量三次 | `references/skill-evolution-governance.md` |

### A. 覆盖式替换（v2.13 契约的工程实现，默认路径）

| | `apply_redactions`（v2.13 原路径） | **覆盖式替换（v2.14 默认）** |
|---|---|---|
| 机制 | 删除原文字对象再写 | 同 bbox 不透明矩形覆盖 + 原坐标回写 |
| 副作用 | 内容流/clip 非局部变化，透明层页面像素抖动 | 改动严格落在 mask 内 |
| 适用 | 纯矢量、无透明组、少量槽位 | 多刊混合、含摄影/透明层、批量替换 |
| 验收 | 需 `collision_report` 预检 | 仍需 `collision_report` + mask 登记 |

**六条铁律**（违反即破坏零偏差或可读性）：

1. **覆盖色 = 该槽位采样中位色精确值**，用 `page.draw_rect(r, color=None, fill=med, overlay=True)`；
   禁止 `round(v*8)/8` 之类量化（实测 15.1% 槽位出现肉眼可见色块，偏差 P90 0.0498）。
   精确色实测偏差中位 **1/255**、P90 **2/255**、>8/255 仅 **0.7%**。
2. **文字色按 WCAG 相对亮度择优**：`argmax(contrast(med, DARK), contrast(med, WHITE))`，
   不要 `亮度>0.55` 二值阈值（实测低对比页 13.7%→**1.1%**，中位 16.79）。
3. **CJK `insert_textbox` 必须检查返回值**。行高约 **1.2×字号**，空间不足时返回负值且
   **静默不写入任何文字**；用 `(size, .85size, .72size, 6pt)` 逐级降字号重试，`spare>=0` 才算成功。
   `stats["text"]` 只统计成功数，并另跑 PDF 文本层审计（曾出现「统计 530 成功、PDF 仅 26/40 页有中文」）。
4. **mask 必须同时登记覆盖矩形与实际文本框**（`Rect(x0,y0,x1+0.4,y1+2.0)`）；
   只登记前者会让抗锯齿边缘被判为槽位外漂移。
5. **高方差区域硬保护**：`reg.std() > 72`（正文）/ `> 110`（压图图注）跳过，避免盖坏满版摄影。
6. **漂移页分级局部降级**，不要整页回退：`full → images → text → none`。
   实测 3 页因 PyMuPDF 重写含透明层页面时 `insert_image` 合成抖动（45 / 1927 / 248 像素且远离槽位），
   降到 `text`（仅中文、原刊图保留）后 `PASS`，从「3 页纯版式」变成 **40/40 页有内容、零回退页**。

### B. 内容工程（v2.13 完全缺失的一层）

**问题**：按单一游标顺序消费书稿，40 页只用了 20 万字中的 6525 字（**3.2%**），
且开头几页填的是版权信息、电子书定价、献词；按字数硬切导致仅 **7.1%** 片段以标点收尾。

**四步管线**（`scripts/semantic_stream.py` 可直接复用）：

1. **剥离前置 matter 与附录**：`find("前言")` → `rfind("Table of Contents")`，得正文 200476 字。
2. **语义短语化**：按中文标点切 ≤10 字完整短语（26331 条）；中文间空白删除、英文词间保留单空格。
3. **全书 N 等分**：40 页各取 1/40 连续片段，实测各页首段落在全书 **0% → 97%**。
4. **栏宽尾差补足**：优先取完整短语，尾差用下一短语前缀补足（避开成对符号/英文单词中间），
   剩余 `appendleft` 回队首保证跨槽位连续。中文量 4276→**5368 字**，
   **语义字符占比 77.7%**，每页中位 109 字。

> **指标口径**：尾差补足后「槽位以标点收尾比例」必然下降（57.8%→13.8%），
> 语义连续性一律以 `semantic_char_pct` 为准；口径说明必须写进报告，否则会被误读为退步。

### C. 右脑优势量化与多刊合璧

- **不要凭感觉改构图**。先量化参照刊：图像覆盖率中位 77–100%、满幅图页 36–71%、暗像素中位 35–77%；
  再逐页盘点自己的交付。实测 40 页中 24 页页廊图片面积仅 **28%**（白底小缩略图）→ 重构为
  左 5.0in 满幅出血摄影 + 右深色索引版，覆盖率升至 **67%**、P16 暗像素 **74%**。
- **多刊合璧选页配额**：每刊 10 页，按 `photo 4 / mix 4 / text 2` 三类版式搭配；
  选页依据 `cov = Σ image_bbox_area / page_area` 与正文 span 数；输出 `page_manifest.json`
  记录 `journal / src_page / quad_page / cov / body / imgs / canvas` 供追溯。
- **4K 资产池**：摄影 18 张 `2645×3840`、科研图 14 张 `4739×3235`；图片槽按面积阈值
  `>2% 页面积 且 边长>40pt` 选取，无大图页自动放宽到 `>0.5% / >35pt` 补 1–2 槽（图片槽 81→**106**）。
- **多画布比例**：四刊实测 5 种画布（495×720 至 670×850），PPTX 统一 6.875×10in 时
  contain 会产生 9.9–12.8% 留白；留白色取该页四边像素中位色（NG 黄 / 深底 / 白各自跟随），
  实测色差 0，且体积 21.16→19.82MB。

### D. 细节体检八门（交付前必跑，独立于零偏差验收）

`scripts/detail_audit.py <base.pdf> <out.pdf> --slots <plan.json> --json detail.json`

| 门 | 指标 | 达标线（实测值） |
|---|---|---|
| D1 | 槽位外零偏差 | `worst_outside_change_ratio = 0.0`、`edited_pages = 40` |
| D2 | 中文真实落位 | PDF 文本层 39/40 页有中文、5368 字（**不能只看构建 stats**） |
| D3 | 语义字符占比 | ≥70%（实测 77.7%） |
| D4 | 覆盖色量化偏差 | =0；实测覆盖色 vs 原底中位 1/255、P90 2/255 |
| D5 | WCAG 对比度 | <4.5 的槽位 ≤5%（实测 1.1%，中位 16.79） |
| D6 | 中文溢出槽位 | 0%（实测 0/518） |
| D7 | 4K 图面积 | 中位 ≥60%（实测 63.4%），大幅内嵌图长边 ≥3840 |
| D8 | 全书内容覆盖 | 40 个采样窗口，正文区间覆盖 0→97% |

**构建报告契约**（`全复刻构建报告.json` 必含字段）：
`slots{text,chart,protected,demoted}` · `stream{book_chars,consumed,coverage_pct}` ·
`images{blocks,filled,quote_cards,charts}` · `tiers{T1,T2,T3}` · `output{size_mb}` ·
`page_modes` · `degraded_pages` · `content_audit` · `optimization[]` · `verify{}`。
**每轮优化都重跑全链并同步三份报告**（验收 / 构建 / 细节体检），禁止只改产物不改报告。

### E. 技能版本治理（麦肯锡 × GCCEO）

- **麦肯锡假设驱动**：先程序化体检量化问题 → 再假设根因 → 单点修复 → 全链复测，禁止盲调。
  结论先行（第一段给判断与关键数字）、MECE 拆解（五层互不重叠）、Issue Tree 定位
  （如「中文覆盖率低」→ 槽位过滤 / CJK 行高 / 内容流起点 三支）。
- **GCCEO 持续进化机制**：Self-Improving Agent 落地为「每个实战项目必须回哺一条铁律 +
  一个可复用脚本 + 一个门禁指标」；季度增量版本（v2.x）、年度大版本（v3.0）；
  四维质量：温度（中文场景贴合）/ 深度（实测数字可复算）/ 硬度（脚本可直接运行）/ 品质（版本与引用一致）。
- **同一把尺量三次**（v2.11「量两次」的扩展）：① 语料采集 `analyze_mags.py` → ② 生成验收
  `journal_4k_check.py` / `verify()` → ③ 细节复检 `detail_audit.py`，三次同源同参数，
  数字可横向比较，不以人工目检替代。
- **反哺清单**：新项目完成后按 `references/skill-evolution-governance.md` §4 走
  「检测 → 根因 → 修复 → 固化 → 归档 → 交付」六步闭环，并追加工作日志。

### 快速上手（完全复刻 + 细节门禁）

```bash
# 1) 内容与视觉基线体检（先量化，别先改）
python3 scripts/detail_audit.py base.pdf draft.pdf --slots plan.json --json detail.json
# 2) 语义片段与全书等分（可 import）
python3 -c "from semantic_stream import build_fragments, page_queues, take_frags; ..."
# 3) 按四刊合璧模板构建（覆盖式替换 + 分级降级 + 零偏差验收 + PPTX）
cp -r templates/quad-exact/ <project>/scripts/
# 4) 交付前：verify(PASS/0.0) + 细节八门 + 三份报告同步 + IMA 归档
```

**已知边界（如实披露，不要硬修）**：满版信息图页若全部文字为竖排标注（实测 Italia P53
共 67 处竖排、横向 0 处），横排中文无法落入原 bbox，按设计层不可变契约硬保护，
该页可无中文；含透明层页面插大图可能触发亚像素合成抖动，走分级降级而非扩大 mask。
J3 栅格/拼贴流口径与「全画幅 4K 一图一世界」天然冲突时按 v2.11 规则披露为口径不适用。

## 质量核对清单（Chart-First 出版级标准）

- [ ] **图表主导页（一个器型占版面 ≥60%）占内容页 ≥60%**（对齐冠军语料下沿 73%×0.8）
- [ ] **每页 ≤150 字正文**（图解页 ≤120）；全文搜索无 >300 字的单页文字墙
- [ ] **数字 100% 可视化**：无数字埋在段落中；关键数字用 stat 大数字卡/图表标注
- [ ] 器型多样性：全书 ≥6 种、每章 ≥2 种、同款器型不相邻重复
- [ ] 每页 ≥1 视觉锚点；≤3 族色彩；金句带引号引用原书并标章节
- [ ] 封面含书名大字+作者+笔记署名+定位语；书档速览页存在（stat 卡）
- [ ] 字号阶梯、负字距渐进、无 #000 纯文本、无 800/900 字重、阴影全出自三级柔影栈
- [ ] 暖纸 `.alt` 每 2–3 内容页一换；页眉页脚齐全；数据图表标出处；金融涨红跌绿
- [ ] **论证页通过咨询级工艺**（v2.2）：标题是判断句且为全页最大字级、每页恰 1 收束、
      图型过数据契约、无反模式红线（伪 3D/双轴伪相关/半径气泡/只报均值/截轴不声明）、来源齐全
- [ ] **设计智能层通过**（v2.4）：Step 0 已跑且《设计决策单》存在；主题色/字体可溯源到检索结果或品牌规范；
      品牌页遵守其 Do's&Don'ts；中文受众通过中文交付清单（字体栈/行高≥1.6/中文 CTA/375–1440px）
- [ ] **思维模型层通过**（v2.5）：已产出《模型-图型清单》；命中模型的内容页全部用标准图型呈现；
      模型图过"图型-内容契约"（定义要素齐全/节点标注 ≤12 字/遮题可读）；器型多样性计入模型图
- [ ] **文生图纪律**（v2.5）：生成图 ≤5 张且仅限四类氛围资产；结构化图示无一用生成图凑数；
      每张生成图可溯源（工具+prompt 摘要）；无工具时已降级几何氛围图
- [ ] **竖版杂志管线通过**（v2.6，仅竖版交付）：页面地图先画后写、页数在原书 1/3~1/2；
      生成器每片 ≤20KB；build 三重校验 0 issue（破图/裁切/挤压）；PDF 6.875×10in 页数吻合；
      PPTX JPEG 重建；满版/章扉/金句页节奏齐备；黑条页眉页脚与 DIN 数字统一
- [ ] **横版杂志管线通过**（v2.7，仅横版交付）：页面地图先画后写、页数在原书 1/3~1/2；
      每章 11 页节奏且两篇编辑开篇翻面；PDF 三重验收 0 issue（MediaBox 612×756/溢出/空页）；
      PPTX 结构 0 越界 + LibreOffice 渲染 0 溢出重叠；遮罩全部为 PNG（CSS 渐变 0 处）；
      CSS 已内联 full.html 且渲染用全新 profile；目录页码 100% 命中；资产无跨章重复
- [ ] **科研图表层通过**（v2.8，仅有数据页）：《器型清单》含「科研图型 + 数据契约」两列；
      一页恰 1 个主器型；无真数据的页面图注标「示意」且未用示例数据冒充原书证据
- [ ] **科研五门通过**（v2.9）：G1 `--verify` 0 真实重叠（exit 2 已修）/ G2 最小字号达标 /
      G3 白底 + ≤7 色 + 灰度可分辨 / G4 旁车 `alt`·`caption`·`.bridge-audit.json`·批量报告齐全 /
      **G5 4K：每一张位图长边 ≥3840 且短边 ≥2160，日志出现 `[4K OK]`，无一 `[4K FAIL]`**
- [ ] **全图型 4K 覆盖**（v2.9）：38 图型、11 大类、单图与流水线、期刊单/双栏、
      矢量与位图、16:9 / NG 竖版 / HBR 横版导出全部按同一把尺；HTML/SVG 截图按 3840 长边出图
- [ ] **令牌与避让通过**（v2.8）：色板 9 选 1 且跨图语义色一致；期刊锁宽未被 `--width` 覆盖；
      图例用预留带、端点留 ≥4% pad、靠边标注内翻；CJK 字体与负号/上下标字形正常
- [ ] **期刊语料层通过**（v2.10，使用期刊语言时）：语言从 §六 路由表选取且有档案卡依据；
      参考期刊 PDF 已过 §一 判型（图片型不提取排版参数）；强调色 ≤2、display 巨字页 ≤4、
      字体三栈、栏数与边距符合 ⑤⑥ 律；版式走向（NG/HBR/16:9）与页面语言叠加关系明确
- [ ] **期刊 4K 复刻四门验收通过**（v2.11，使用期刊语言时）：`journal_4k_check.py`
      对渲染 PDF 跑 J1–J3 全 PASS（J1 字体两栈命中、J2 签名色 ≤36 距离、J3 边距 ≤12pp/栏数 ≤1/
      密度不换型）+ J4 达标（PNG 3840×2160 或 PDF 主图有效 DPI ≥ 目标×0.9）；
      exit 0；`--json` 报告随交付归档；降级卡 WARN 项已写入交付说明
- [ ] **七维选型通过**（v2.12，使用期刊语言时）：版式哲学已按五型论判定（A–E）且与材料类型匹配；
      栏数/边距经栅格模型计算（非凭感觉）；色板符合"一刊一签名色+中性骨架"；字号双轨占比在模型区间；
      自动模式已输出选型报告并经用户确认，自定义/混合模式已正确载卡
- [ ] **任意格式管线通过**（v2.12，非 PDF 直读输入时）：输入格式矩阵解析成功（epub/docx/html/md/txt）；
      双源分离（内容源≠风格源）；低清图已 superres；IR 章节树完整；交付物过四门验收
- [ ] **完全复刻模式通过**（v2.13，仅完全复刻交付）：`build_page_models` 逐页建模 + `classify_archetype`
      原型分类完成；`replicate_1to1` 1:1 底版画布/文本层一致；`collision_report` 槽位碰撞 0 处
      （P08 首字下沉大 W 已避让，未靠扩大 mask 掩盖）；三类槽位 `apply_pack` 注入后
      `verify(matrix=2.0, pad_px=3)` 报告 `verdict=PASS`（槽位外像素 100% 相同、未改动页 100% 相同）；
      字体 T1/T2/T3 档位与 CJK 资源扩展已在交付说明登记，基线用原页面字体 ascender；
      档案卡按子产品线选对（常规周刊 `TIME_WEEKLY` ≠ 特辑 `TIME_SPECIAL_EDITION`）
- [ ] **覆盖式替换通过**（v2.14，完全复刻工程化）：覆盖色为采样中位色精确值（无量化色块）/
      文字色 WCAG 择优 / `insert_textbox` 已检查返回值并逐级降字号 / mask 同时登记覆盖矩形与文本框 /
      高方差区域已硬保护 / 漂移页走 `full→images→text→none` 分级局部降级而非整页回退
- [ ] **内容工程通过**（v2.14）：前置 matter 与附录已剥离；全书 N 等分采样（各页落在 0→97%）/
      语义短语 + 尾差补足 / `semantic_char_pct ≥70%` / 以 PDF 文本层复核中文页数与字数（不只看 stats）
- [ ] **细节体检八门通过**（v2.14）：`detail_audit.py` 输出 D1–D8 全达标并归档 `细节体检.json`；
      构建报告含 `slots/stream/images/tiers/output/page_modes/degraded_pages/content_audit/optimization/verify`；
      三份报告（验收/构建/体检）口径已同步
- [ ] **版本治理通过**（v2.14）：本项目新增铁律、可复用脚本、门禁指标各 ≥1 项已回哺技能；
      SKILL.md frontmatter 版本 / README 徽章 / 参考索引 / 触发词四处一致；工作日志已追加
- [ ] 思维导图收尾 + 封底 Thank You；HTML 逐页无溢出无滚动条

## 参考文件索引

| 文件 | 内容 | 何时读 |
|---|---|---|
| `references/design-intelligence/INDEX.md` | **v2.4 新增：设计智能层总索引——四层能力架构/Step 0 前置检索流程/命令速查/降级路径/来源许可** | **Step 0 第一站，动笔前必读** || `references/design-intelligence/ui-ux-pro-max/` | **v2.4 全量收录：设计智能检索引擎**（SKILL.md 工作流 + scripts/ 4 个纯标准库脚本 + data/ 31 张 CSV：67 风格/161 配色/57 字体/13 技术栈/UX 规范/图表选型/落地页模式 + references/ 上游原文） | Step 0 检索；Step 2 定调；Step 3 图表选型交叉验证 |
| `references/design-intelligence/ui-ux-pro-max-cn/` | **v2.4 全量收录：中文本土化设计规则**（中文字体栈/中国色彩文化/微信小程序规范/国内技术栈/五大中文行业规则/中文交付清单） | 中文受众场景，Step 0/4 必读 |
| `references/design-intelligence/awesome-design-md/` | **v2.4 全量收录：54 个真实品牌 DESIGN.md 完整规范**（references/ 下按品牌名取文件，每份 9 节：主题/色板/字体/组件/布局/阴影/禁忌/响应式/提示词） | 用户指定品牌或需品牌级质感时 |
| `references/design-intelligence/awesome-design/` | **v2.4 全量收录：20+ 设计技能选型导航**（按任务/按框架决策表 + 安全扫描方法） | 需求超出四层覆盖时 |
| `references/mental-models-library/INDEX.md` | **v2.5 新增：思维模型库总入口——四步用法（信号扫描→模型匹配→构图调用→契约检查）/全量信号速查表（101 条）/文生图五要素公式+10 族 prompt 模板/与工作流对接表** | **Step 3 转译时必查（信号→图型路由）** |
| `references/mental-models-library/models-catalog.md` | **v2.5 新增：100 个思维模型全量档案**（每模型：一句话定义/内容信号词/图型族/构图要点）+ 10 大图型族构图模板总表 + 图型-内容契约 + 易混辨析 | Step 3 命中信号后取构图细节 |
| `references/visual-grammar.md` | **一图解千言视觉语法：实证基线+三铁律+12 类文字→图表映射+页面配比公式（v2 新增）** | Step 3 转译前必读 |
| `references/emotion-marketing.md` | **v2.1 新增：情绪营销方法论库（五点情绪开关定义/五色情绪光谱/实证案例库/五点四法观察矩阵/新增 6 器型/认知金句库）** | 营销·销售·产品·增长类内容 Step 1 前必读 |
| `references/consulting-craft.md` | **v2.2 新增：咨询级页面工艺库（四弧线叙事+adds/标题纪律+强词清单/页面角色表/五区骨架+密度三档+收束唯一/关系→图型选型+数据契约/反模式 13 红线/瀑布对账 9 条/图示语义五合同/模块填充 P-D-F-X-V/16:9 容量硬网格/验收四门禁+12 问+返工顺序）** | 商业·方法论·数据复盘类论证页 Step 3/4 必读 |
| `references/design-tokens.md` | v2 出版级质感令牌（暖墨/耳语边框/柔影栈/负字距/护栏） | Step 2 定调 |
| `references/design-system.md` | 版式/字体/字号/主题色映射/图像/页面框架件 | Step 2 定调 |
| `references/content-framework.md` | 九大模块/八模块模板/六原型/金句工程 | Step 1、4 |
| `references/chart-catalog.md` | 10 类组件实现+决策树+图文配比 | Step 4 |
| `references/graphics-toolchain.md` | **v2.3 新增：图形资产管线双路径（A 复刻 7 环节/B 生成 9 环节）+ 7 工具注册表（版本/路径/SHA256）+ 安装命令 + cognigraph MCP 配置 + 10 条踩坑库** | 需要位图描摹/超分/图表即代码/MCP 时 |
| `scripts/bitmap2vector.sh` | 位图→SVG 描摹包装器（vtracer 彩色/potrace 黑白） | 路径 A5 |
| `scripts/superres.sh` | Real-ESRGAN 4× 超分包装器（upscayl-bin） | 路径 A6 |
| `scripts/mermaid-export.sh` | mermaid→SVG/PNG/PDF 包装器（mmdc，复用本机 Chrome） | 路径 B4 |
| `scripts/clip-chart.sh` | .clp 文本→SVG 图表包装器（clip 0.8.0） | 路径 B4+ |
| `references/ng-magazine-layout.md` | **v2.6 新增：NG 杂志竖版版式手册——何时用竖版/版式参数锚点/设计令牌换肤/12 类页面 HTML 骨架/页面地图法(1/3~1/2)/生成器拆分硬纪律/六步 build 流水线/6 条踩坑库/与 16:9 工作流对接** | **摄影集·自然·历史·人物类书籍必读（Step 0.5 判竖版后第一站）** |
| `templates/ng-magazine/mag.css` | **v2.6 新增：NG 杂志设计系统完整 CSS**（色板/三字体栈/页面骨架/黑条页眉页脚/12 类页面组件，462 行实战版） | 竖版项目复制到 output/ 直接用 |
| `templates/ng-magazine/build-template.py` | **v2.6 新增：六步 build 流水线模板**（合并/三重校验 JS/@2x 截图/PDF in 单位/PPTX JPEG q87/打包/方差检测，踩坑全修复） | 竖版 build 阶段 |
| `templates/ng-magazine/generator-template.py` | **v2.6 新增：生成器骨架模板**（HD/FT/FOLIO 三函数 + P.append 模式 + ≤20KB 拆分说明） | 竖版每个片段动笔前 |
| `references/hbr-magazine-layout.md` | **v2.7 新增：HBR 商业杂志横版版式手册——三路版式决策/612×756pt 锚点/刊名四色令牌/12 类页面 HTML 骨架/每章 11 页节奏与页面地图法(1/3~1/2)/生成器拆分/Chrome headless 六步 build/PDF 三重验收+去重瘦身/8 条踩坑库/与既有工作流对接** | **商业期刊·杂志文集·多主题合集必读（Step 0.5 判横版后第一站）** |
| `templates/hbr-magazine/mag.css` | **v2.7 新增：HBR 杂志设计系统完整 CSS**（刊名四色/双字体栈/页面骨架/folio+pageno/12 类页型组件/打印规则，实战 88 页版） | 横版项目复制到 output/ 直接用 |
| `templates/hbr-magazine/generator-template.py` | **v2.7 新增：12 页型构建器骨架**（封面/章隔/编辑/大图表/统计/文本/照片/金句/目录/总览 + 3 个 SVG 大图表组件 + P.append 模式 + ≤20KB 拆分说明） | 横版每个片段动笔前 |
| `templates/hbr-magazine/build-template.py` | **v2.7 新增：六步 build 流水线模板**（合并内联 CSS→Chrome headless 渲染→三重验收→XObject 去重瘦身→PPTX 同源 16:9→打包；8 坑全修复） | 横版 build 阶段 |
| `templates/hbr-magazine/scrim/` | **v2.7 新增：4 个遮罩 PNG（mc/md/mp/mq，各约 280B）+ make_scrims.py 再生脚本**（渐变曲线可调；防 Pattern 光栅化的关键资产） | 横版项目必备；改曲线时重跑脚本 |
| `references/magazine-design-corpus-2026-10.md` | **v2.10 新增：期刊设计语料库——31 刊实测（矢量型/图片型判据 + NG/财经/科研/时尚/特辑/评论 12 类语言档案卡（字体 DNA/签名色板 hex/栏数/图片密度）+ 任务路由表 + 7 条实证设计定律 + IMA 知识库挂接）** | **Step 0 期刊语言路由；用户点名刊物风格或内容贴近期刊类型时** |
| `references/case-patterns.md` | 31 份语料风格档案+复用规则 | 风格参照 |
| `templates/reading-notes-template.html` | 出版级 HTML 骨架 v2.0（12 类页面，质感令牌内置） | Step 4 |
| `templates/output-pipelines.md` | PDF/PPTX/长图导出管线 | Step 5 |
| `references/academic-chart-system.md` | **v2.8 新增：科研级图表体系核心手册**——38 图型×11 大类→笔记器型映射全表/双层选型决策树/9 色板 hex+9 期刊预设全表/HTML-SVG 组件规范/验收四门/20 条反模式/引擎桥接/七步工作流对接 | **任何含数据页的笔记 Step 3–5 必读** |
| `templates/academic-charts.css` | **v2.8 新增：科研图表设计令牌 CSS**（9 色板 `[data-af-theme]` + 9 期刊 `[data-af-journal]` + `.af-legend-band`/`.af-end-label`/`.af-panels` A/B/C 角标/灰度自检/打印白底层） | Step 4 排页、Step 5 打印导出 |
| `scripts/figure-bridge.py` | **v2.8 新增 / v2.9 升级：38 图型桥接器**（`--check`/`--list`/单图/JSON 流水线；自动探测带依赖的系统 python；渲染前数据契约闸门；自动 CJK；`--verify` 五门；**默认 4K**：DPI 反推 + PNG IHDR 实测 + 一次自愈；旁车 audit 与批量报告） | Step 3.5 出真图时 |
| `references/journal-4k-replication.md` | **v2.11 新增：期刊 4K 复刻闭环手册——四门验收 J1–J4 判定/量法/容差 + 4K DPI 反推公式与 14 卡速查表 + 两条渲染路径（PNG scale / PDF 矢量+superres）+ 14 profile 档案表（字体 DNA/签名色/栅格锚点/降级卡）+ 六步复刻工作流 + 8 条陷阱库** | **期刊风格复刻项目 Step 4–5 必读；用户要求「高保真模仿/4K 复刻」时** |
| `scripts/journal_4k_check.py` | **v2.11 新增：四门验收脚本**（14 profile 内嵌档案卡与语料同源同参数度量；J1 字体 DNA/J2 色板签名/J3 栅格边距/J4 4K 像素；`--json` 报告 + `--min-long/--min-short` 阈值覆盖 + `--list` 档案卡一览；exit 0/1/2） | 期刊复刻渲染完成后跑门禁 |
| `references/journal-design-seven-dimensions.md` | **v2.12 新增：期刊设计七维知识库——IMA KB 全量吸收（版式哲学五型论/栅格·密度·色彩·字号四模型/图表三范式/边距三律/照片四级采摄/财经三范式路由/封面 masthead 类型学+压图规则 + 60 秒定型快速路由）** | **期刊语言选型时先读（Step 0/2）；财经/摄影/封面类材料定型必查** |
| `references/universal-ebook-pipeline.md` | **v2.12 新增：任意格式电子书→期刊复刻通用管线——格式矩阵（epub/docx/pdf/扫描OCR/html/md/txt/mobi）+ 双源分离 + 自动/自定义/混合三模式 + 五步管线（解析归一→风格定型→结构映射→渲染→四门验收）+ 批量模式 + 6 条错误处理** | **非 PDF 直读输入时必读；用户要求"任何电子书生成期刊复刻版"时** |

| `scripts/exact_replication.py` | **v2.13 新增：期刊完全复刻通用引擎**——逐页建模 / 原型分类 / `replicate_1to1` 1:1 矢量底版 / `collision_report` 槽位碰撞预检 / `ExactEditor` 三类槽位注入（T1–T3 字体策略、基线固定、字重映射、居中对齐全槽位统一）/ `verify` 槽位外零偏差验收 | **用户要求「完全复刻 / 只换内容 / 其他杂志也一样」时主控脚本** |
| `references/exact-replication-contract.md` | **v2.13 新增：完全复刻契约手册**——固定设计层 vs 三类槽位 / 六阶段管线 / 模型 schema / 槽位识别 / 零偏差验收协议 / 字体三档与跨页子集池否决 / 碰撞检测与基线踩坑 / 已知边界 | 完全复刻项目启动前必读 |
| `references/journal-dna-cards.md` | **v2.13 新增：按刊按子产品线的 DNA 契约卡**——TIME 常规周刊 / TIME Special Edition / Vogue / New Scientist / NG / Bloomberg Businessweek 六刊实测对照 + 新刊接入抽取步骤 + 常规周刊与特辑不得共卡的说明 | 新刊接入或档案卡取值争议时 |
| `templates/time-exact/` | **v2.13 新增：完全复刻模板**——`slots.example.json` / `content_pack.example.json` / `build.example.py` / `README.md` | 新刊开槽位时的起点 |
| `references/exact-content-engineering.md` | **v2.14 新增：零偏差内容工程手册**——覆盖式替换 vs redaction 决策表 / 精确中位色与 WCAG 文字色 / CJK 行高静默失败 / mask 契约 / 分级局部降级 / 多画布留白 / 内容流四步管线 / 文本层审计 / 12 条踩坑库 | **完全复刻项目落地第一步必读** |
| `references/visual-detail-qa.md` | **v2.14 新增：视觉细节与验收治理手册**——右脑优势四刊量化 / 多刊选页配额 / 4K 资产池 / 细节体检八门阈值 / 构建报告契约 / IMA 归档五步 / 结构验证清单 | 交付前跑门禁、构图量化时 |
| `references/skill-evolution-governance.md` | **v2.14 新增：技能版本治理 SOP（麦肯锡 × GCCEO）**——MECE 五层拆解 / 金字塔与假设驱动 / Issue Tree 根因定位 / 四维质量 / 持续进化与版本节奏 / 同一把尺量三次 / 六步反哺闭环 | 技能升级、经验回哺、版本发布时 |
| `scripts/semantic_stream.py` | **v2.14 新增：内容流语义化库 + CLI**——前置 matter 剥离 / 中文标点短语切分 / 全书 N 等分队列 / 栏宽尾差补足 / `--self-test` 自检 | 任何「把长书稿填进固定栏位」的任务 |
| `scripts/detail_audit.py` | **v2.14 新增：细节体检八门脚本**——BASE/OUT 双 PDF 对比，输出中文落位 / 语义 / 对比度 / 覆盖色偏差 / 溢出 / 4K 面积 / 全书采样 JSON，可独立运行 | 每轮优化前量化基线、交付前复检 |
| `templates/quad-exact/` | **v2.14 新增：四刊合璧 1:1 全复刻构建模板**——`build.example.py`（选页配额 / 槽位规划 / 覆盖式替换 / 分级降级 / `verify` / PPTX / 三报告）+ `README.md` | 多刊混合底版、40 页级完全复刻项目 |

## 错误处理

- **书中信息不足**（无推荐人/无作者履历）：跳过对应模块，页面序列自动收缩，不留占位符。
- **某章找不到任何器型信号**：该章压缩为 1 页金句页或 1 页 hero 叙事，禁止硬造图表。- **无法确定主题色**：先跑 Step 0 引擎检索；仍无果则四大家族兜底——商务蓝 `#142534` / 方法论红 `#C20001` / 心理暖土 `#A5300F` / 科技暗色 `#05173E`。
- **导出 PDF 分页错位**：确认每 section 固定 720px 高、无内部溢出；检查 `@page` 尺寸。
- **内容超页**：先砍文字页、不砍器型页；一章最多 2 页；总页数向精华版 30–60 页收敛。
- **四门验收 J1 FAIL**（字体不命中）：商业字体无授权——CSS 显式 `@font-face` 指向档案卡
  替代字体并把映射写进交付说明；裸系统 fallback 算 FAIL，不算降级。
- **四门验收 J4 FAIL**（位图 DPI 不足）：源图 <4K 先跑 v2.3 `superres.sh` 4× 超分再入版，
  禁止直接放大截图蒙混；J4 逐图反推只对主图（显示宽 ≥25% 页宽）设门，小贴片豁免。
- **四门验收对 PNG 报 J1–J3 假 FAIL**：纯位图无文本层属预期——对同源矢量 PDF 量 J1–J3、
  对 PNG 量 J4，两次调用合并出报告（见 journal-4k-replication.md §一 验收对象规则）。
- **图表密度不达标**（<60%）：回 Step 3 重跑映射表——绝大多数"只能写文字"的内容其实是
  未识别的编号/时间/对比/数字信号。
- **设计智能引擎不可用**（v2.4）：无 python3 或脚本报错 → 降级读 `design-intelligence/ui-ux-pro-max/data/{styles,colors,typography}.csv`；
  中文场景无条件读 `ui-ux-pro-max-cn/SKILL.md`；均不可用 → 退回内置映射表并在交付说明中注明"未走检索"。
- **引擎中文检索 0 结果**（v2.4，已知限制）：L3 语料为英文——把需求译成英文关键词重试
  （"金融数据看板"→ `fintech data dashboard`），或直接走 L2 中文规则层。
- **品牌 DESIGN.md 与既有令牌冲突**（v2.4）：品牌 Do's&Don'ts 优先，质感层令牌（暖墨/耳语边框/柔影）保持不动，
  只让主题层向品牌色板靠拢；无法调和时在交付说明中注明取舍。
- **思维模型匹配失败**（v2.5）：全章扫描无信号命中 → 回退 visual-grammar §2 通用映射表，
  禁止为套模型而歪曲内容；一词多模按篇章语境取最贴近者，仍冲突则两个都画对比页。
- **模型图型契约不过**（v2.5）：图缺模型定义要素（如飞轮无"自持段"）→ 补要素或换更简单的族；
  节点标注超 12 字 → 精简为关键词，长解释移页内正文。
- **文生图不可用或违规**（v2.5）：无工具 → 几何氛围图降级（SVG 色块+渐变+器型剪影）；
  生成图带文字/水印 → 重生成或弃用；超 5 张 → 优先删 hero 类、保留封面与金句背景。
- **竖版页面溢出/裁切**（v2.6）：build 校验 issues 非零 → 按"挤压(.bd scrollHeight)>
  裁切(单元素越界)>破图(路径错)"顺序修；信息页超容量先砍内容不缩字号；
  满版页 caption 过长压图 → 缩 .cdesc 到 2 行以内。
- **竖版生成器片段超 20KB**（v2.6）：Write 截断风险 → 对半再拆片段；
  片段页数与页面地图不一致时以地图为准回补/删页，禁止顺手加页。
- **竖版图片路径 404**（v2.6）：生成器里 grep 全部 src= 校验文件存在；
  资产统一放 `assets/mag/`，禁止多目录混放。
- **横版 PDF 体积暴涨/出现 Pattern 对象**（v2.7）：CSS linear-gradient 遮罩叠背景照片，
  Chrome 把照片光栅化进平铺 Pattern（未压缩位图 ×2.4）→ 遮罩一律用 `scrim/` 预渲染 PNG
  （`background-image + 100% 100% + no-repeat`）；背景类全部补 `background-repeat: no-repeat`。
- **横版改 CSS 后渲染结果字节级不变**（v2.7）：full.html 是构建时内联 CSS 的快照
  （改 style.css 不重跑 build_full 等于没改）+ Chrome 默认 profile 磁盘缓存 file:// 子资源
  → 改 CSS 必须重新生成 full.html；渲染命令带 `--user-data-dir=` 全新临时目录。
- **横版 PDF 文本溢出某几页**（v2.7）：杂志文本页内容超高 → 收紧 `.mt-text`
  （8.2pt/1.86 双栏）、编辑页照片栏 310pt、标题 22pt；仍溢出先砍该页文字，不缩字号。
- **横版 PPTX shape 越界**（v2.7）：kicker 固定 9in 文本框在右侧元素上冲出页面
  → 宽度 clamp 到页宽；期号总览 3 列×4 行超页高 → 4 列×3 行（cw 2.90/chh 1.52/行距 0.14in）。
- **横版瘦身收益低**（v2.7）：Pattern 未清之前 garbage 回收无效（被 Pattern 引用看似可达）
  → 先清 Pattern 再做 XObject 内容哈希去重；页内 JPEG 重压缩收益仅 5%，不做。
- **引擎/依赖不可用**（v2.8）：先跑 `figure-bridge.py --check`；WorkBuddy 内置 python 缺
  matplotlib/scipy/openpyxl → 桥接器自动切 `/opt/homebrew/bin/python3` 或 `/usr/bin/python3`，
  **不要往内置环境 pip install**；引擎未安装 → 退回 §4 HTML/SVG 器型，不阻塞交付。
- **数据契约闸门 FAIL exit 3**（v2.8）：缺必填字段/数组等长不一致/NaN·Inf/PRISMA 数字不自洽
  → 改数据再跑，不落半成品；CSV 静默丢误差棒与复杂 schema → 一律改 JSON。
- **`--verify` 报真实重叠 exit 2**（v2.8）：按 §6 第 10–13 条修机制（预留带/端点 pad/
  靠边翻向/同源索引），**禁止逐图特判或改小字号蒙混**；`--verify` 只对 PDF 生效，
  若 `--formats` 无 pdf 会静默跳过 → 出图格式必须含 pdf。
- **误以为期刊锁宽未生效**（v2.8）：`--journal` 与 `--width` 同给时 width 被忽略（`--height` 有效）；
  要自由尺寸就去掉 preset；期刊预设下禁用 `bbox_inches='tight'`（85mm 会被裁成 82.4mm）。
- **中文图乱码/上下标缺字**（v2.8）：桥接器按数据文本自动加 `--cjk`；字典键里的中文也会触发；
  `⁹/³/²` 改写 `10^9/L`；`axes.unicode_minus=False` 防负号变方块；头less 环境需装一款 CJK 字体。
- **无真数据却想放科研图**（v2.8）：禁止用引擎模板示例数据冒充原书证据；
  退回 `academic-charts.css` 的 HTML/SVG 器型并在图注标「示意」，或并入相邻页。
- **位图不到 4K / `[4K FAIL]`**（v2.9）：最常见于期刊**单栏锁宽**（science 55mm=2.17in，
  600dpi 仅 ~1300px）→ 桥接器已自动反推 DPI（该例 1774dpi）并一次自愈；仍失败则改
  `--column double`、去掉 `--journal` 用自由尺寸，或 `--resolution auto` 显式豁免并在交付说明注明。
  引擎内存护栏把 dpi 砍半时同理；**不要用 1280×720 幻灯片截图冒充 4K 图表**。
- **纯矢量输出被误判不达标**（v2.9）：PDF/SVG/EPS 分辨率无关，桥接器返回 `[4K OK] vector`；
  若需要位图交付物，必须显式加 `png`/`tiff` 到 `--formats`，否则只有矢量、无 4K 位图可验收。
- **HTML/SVG 版式导出不足 4K**（v2.9）：截图按 `--af-export-w:3840px` 长边 + @2x/@4x 出图；
  NG 竖版 2160×3840、HBR 横版 3840×4560 等比；导出后按 PNG IHDR 复核，不达标重截。
- **期刊 PDF 提不出字体/色板**（v2.10）：先过语料库 §一 判型——≤2 字体且只有 Helvetica、
  恒 1 图/页覆盖 100%、左边距恒 30pt = 图片型 PDF（整页位图/扫描），**禁止硬提取**；
  只作视觉参考，排版参数改从同类别矢量刊档案卡取（语料中 7 刊即此型）。
- **青年文摘类中文 Type3 字体不可读**（v2.10）：中文字体常以 Type3 嵌入（数百个无名字体），
  字体名不可提取属正常；可提取字号/栅格/页数，色板信息量低（双色印刷纯黑正文），
  设计令牌改走 `ui-ux-pro-max-cn` 中文规则层。
- **期刊语言与既有版式冲突**（v2.10）：语料库只供"页面语言"（字体/色板/密度），画布锚点
  仍以 NG 竖版 v2.6 / HBR 横版 v2.7 手册为准；档案卡的 pt 边距/栏数按画布比例换算，
  不直接照抄开本。
- **七维选型与用户直觉冲突**（v2.12）：用户点名风格永远优先于自动探测——自动模式只做
  "建议 + 报告"，用户一句话即可改型；探测信号冲突（财经+科研双高）按密度更高者定型并标注。
- **电子书解析失败/图丢失**（v2.12）：epub 图在 zip `EPUB/images/` 需解包重链；扫描 pdf 无
  文本层走 OCR 分支并声明"仅内容复刻，风格需另给参照"；mobi/azw3 先 `ebook-convert` 转 epub。
- **IMA 云端不可用**（v2.12）：MCP 工具超时/未连接时全部降级本地镜像 `magcorpus/`
  （mags_metrics.json + summary.md 与云端同源）；不要为云端检索阻塞交付。
- **完全复刻套错档案卡**（v2.13）：同品牌常规周刊与特辑是两条契约——先比对画布 pt 与图像覆盖，
  `567.03×756 / 全量 med_cover≈0.35` 走 `TIME_WEEKLY`、`576×783 / 1.00` 走 `TIME_SPECIAL_EDITION`；
  此处覆盖率是**原刊 DNA 全量中位口径，只用于判线**，不是档案卡值——`TIME_WEEKLY` 的
  J3 参数为 `25.3 / 45.3 / cols 2 / cov 0.471`（12 页采样口径），两者不可混用。
  旧 `TIME_SPECIAL` 仅向后兼容且**不适用于常规周刊**。详见 `references/journal-dna-cards.md` §2。
- **零偏差验收 FAIL / 槽位外像素变化**（v2.13）：先查 `collision_report` 是否在注入前跑过且 0 冲突
  （首字下沉、跨栏大标题与正文相交会削掉固定设计层墨迹，**禁止靠扩大 mask 掩盖**）；再查 redact 三个
  `*_NONE/*_REMOVE` 常量与 `fill=None, cross_out=False`；中文方框走 T3 档；基线误用替代字体
  ascender 会让文字下溢；双方渲染必须同引擎、同 matrix。只有 `verdict=PASS` 才交付，无 WARN 可交付。
- **文字槽出现明显色块 / 文字框像贴片**（v2.14）：覆盖色被量化（如 1/8 分级）→ 改用采样中位色
  精确 float 三元组 `draw_rect(fill=med)`；实证量化偏差 >0.03 的槽位 15.1%，精确化后实测中位 1/255。
- **文字在浅灰/中灰底上读不清**（v2.14）：别用 `亮度>0.55` 二值切换，改 WCAG 相对亮度择优；
  实证低对比槽位 13.7%→1.1%。
- **构建 stats 显示文字替换成功，但 PDF 大面积无中文**（v2.14）：CJK `insert_textbox` 行高约
  1.2×字号，空间不足返回负值且静默不写入；必须检查 `spare>=0` + 逐级降字号，并跑 PDF 文本层审计。
  另一个独立根因是满版摄影页的文字槽被「不与图片相交」规则全过滤 → 补 `over_img` 图注槽
  （只用原刊既有文字 bbox，不新增栏位）。
- **中文断章、开头几页是版权/定价/献词**（v2.14）：内容流从文件第 1 字顺序消费所致 →
  剥离前置 matter 与附录、按全书 N 等分取完整语义短语、栏宽尾差用下一短语前缀补足且剩余留队首。
- **内容只覆盖全书前几个百分点**（v2.14）：单游标顺序消费 → 改 `page_queues(N)` 各页取 1/N 连续片段，
  用「各页首段在正文中的相对位置」量化验证（实测 0%→97%）。
- **零偏差 FAIL 但漂移像素远离所有槽位**（v2.14）：多为 PyMuPDF 重写含透明层页面时
  `insert_image` 的亚像素合成抖动（实测 45 / 1927 / 248 像素、全页零散或右边缘），
  **禁止靠扩大 mask 掩盖** → 走 `full→images→text→none` 分级局部降级，尽量保住该页内容。
- **PPTX 宽画布页出现上下硬白边**（v2.14）：contain 到统一画布时白底所致 →
  留白色取该页四边像素中位色，随 NG 黄 / 深底 / 白底自适应。
- **指标被误读为退步**（v2.14）：尾差补足后 `punctuation_closed_pct` 必然下降，
  语义连续性以 `semantic_char_pct` 为准；口径说明必须写进 `细节体检.json` 与交付说明。
- **三份报告口径不一致**（v2.14）：每轮优化后必须重跑 `verify` + `detail_audit` 并同步
  `全复刻构建报告.json.content_audit`；禁止只替换 PDF/PPTX 而沿用旧报告。
