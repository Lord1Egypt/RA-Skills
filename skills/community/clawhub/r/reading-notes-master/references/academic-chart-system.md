# 科研级图表体系（v2.8 核心手册）— Academic Chart System

> **双源实证**：① 本机 `academic-figures v5.9.0`（docsor1212，MIT-0）引擎源码、38 模板、9 色板、9 期刊 JSON、
> `--verify` 像素级重叠检测；②《38种科研图表收集整理报告（样例增强版）.pptx》93 页
> （38 图型 × 「要点页 + 600dpi 样例页」+ 11 大类总览 + 选型决策树 + 投稿规范）。
> 本手册把「科研数据图」的选型纪律、设计令牌与验收门禁，转译成读书笔记可用的**版式图表生成能力**。
> 原则：**科研图负责数据诚实，笔记版式负责叙事节奏；两者共用同一套令牌与门禁，不混用器型语义。**

## §0 定位与边界

| 维度 | 既有能力（v2.7 及以前） | v2.8 新增 |
|---|---|---|
| 器型来源 | 31 份笔记语料实测 + 100 思维模型 | + 38 种科研图型的数据关系语义 |
| 选型依据 | 文字信号（「时间/编号/数字/框架」） | + 数据关系（比较/分布/配对/趋势/矩阵/集合/推断/生存/预测/一致性/流程） |
| 配色 | 20 组主题色映射 + 品牌 DESIGN.md | + 9 套色盲安全色板（hex 全表）+ 语义色跨图一致规则 |
| 尺寸 | 16:9 / NG 660×960px / HBR 612×756pt | + 9 套期刊栏宽/字号/DPI 作为栅格基准 |
| 验收 | 溢出/裁切/空页/结构越界 | + 真实墨迹重叠、最小字号、白底、灰度可分辨、确定性、旁车可复现 |
| 出图 | HTML/SVG 手绘 + 图形资产管线 | + 桥接本机引擎批量生成矢量真图（600dpi / --verify） |

**不做什么**：不把读书笔记改造成统计论文；不为无数据的内容硬造科研图；
不在笔记里放风险表、P 值、CI 等专业标注，除非原书本身就在讲这些（此时必须数据诚实、标注来源）。

## §1 38 图型 × 11 大类 → 笔记器型映射全表

读法：**触发信号**（书里出现什么 → 选它）、**笔记改写**（在笔记里变成什么页）、
**数据契约**（出真图时 JSON 必填字段）、**统计红线**（不可越界的语义）。
「器型」列沿用 `chart-catalog.md` 的 10 类组件名；标 `NEW` 者为 v2.8 新增器型。

### 一、比较与构成（4）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 01 | 柱状图 `bar` | 几组数字并列、A 比 B 高 | 编号卡片 / **大数字卡 NEW** | `labels`,`series`,可选 `errors` | 只画概括统计；误差棒须写明 SD/SE/95%CI |
| 02 | 水平条形 `hbar` | 长书名、长概念、Top N 排名 | **排名条 NEW**（替代编号卡片） | 同 `bar` | 条目 >20–30 只取 Top N 或拆面板；按值降序 |
| 03 | 分组柱状 `grouped_bar` | 「组别 × 系列」两因子 | 双栏对比 / 矩阵 | `labels`,`series`(二维) | 系列 >4 拆面板或改热图 |
| 04 | 堆叠柱状 `stacked_bar` | 构成比、占比随类目变 | **100% 堆叠带 NEW**（阶段带变体） | `labels`,`series`,`percentage` | 段数过多不可读；比较构成优先 100% 形式 |

### 二、数据分布（4）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 05 | 箱线图 `box` | 「多数/少数/离群/区间」 | **分布摘要卡 NEW** | `labels`,`series` 原始数组 | n<10 箱线意义有限，改散点 |
| 06 | 小提琴 `violin` | 「两极分化/双峰」 | 分布摘要卡 | 同 `box` | 小样本密度失真，须叠散点 |
| 07 | 雨云图 `raincloud` | 「个体与整体同时看」 | **云+点三位一体 NEW** | 同 `violin` + `jitter`,`cloud_scale` | 20–200 例最佳；组多则纵向拥挤 |
| 08 | 山脊图 `ridgeline` | 「逐年演变/分布漂移」 | **阶段带 × 密度 NEW**（时间线升级） | `labels`,`datasets`,`overlap`,`sort` | 表达形态位移，不表达精确均值 |

### 三、配对与变化对比（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 09 | 配对图 `paired` | 读前 vs 读后、同一对象前后 | **认知改变页 NEW**（双栏对比升级） | `before`,`after` 等长 | 严格配对；n≥6 才标检验 |
| 10 | 斜率图 `slope` | 排名升降、两时点变化 | **升降线 NEW** | `items:{名:[左,右]}` 每项恰 2 值 | >2 时点改 `line`；变化最大者高亮 |
| 11 | 哑铃图 `dumbbell` | 两方法差距、差距排序 | **差距条 NEW** | `from`,`to` 等长 + `labels` | 严格两点；标注值必须从排序后同一条目现算 |

### 四、趋势与相关（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 12 | 折线图 `line` | 走势、随时间变化 | 时间线（数据化）/ 数据图表 | `labels`,`series`,`errors` | 系列 >5 拆面板或突出关键系列；末端直接标注优先于图例 |
| 13 | 散点图 `scatter` | 「A 越高 B 越高」 | 象限/矩阵（点坐标=案例） | `x`,`y` 等长 + `groups` | 相关≠因果；离群点须在图注说明 |
| 14 | 双轴图 `dual_axis` | 两个不同量纲同时讲 | 慎用于笔记；优先拆成两页 | `left`,`right` + 可选误差 | 必须标左右轴变量与单位；**不可比较两轴斜率**，`right_floor` 须声明 |

### 五、矩阵与多变量（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 15 | 热图 `heatmap` | 概念 × 章节相关矩阵、对照表 | **一页纸表格（色阶版）NEW** | `matrix`,`row_labels`,`col_labels`,`cbar_label` | 含正负数据用发散色板（RdBu_r，中心对齐 0） |
| 16 | 聚类热图 `cluster_heatmap` | 主题自动归类 | 一页纸表格（重排版） | 同 `heatmap` | 先 Z-score 标准化；>1500 行降采样、硬上限 3000 |
| 17 | PCA `pca` | 多维指标降到「两类」 | 象限/矩阵（分群示意） | `matrix`(行=样本),`groups`,`feature_names` | ≤200 特征列；**须报 PC1/PC2 方差解释率**；椭圆是示意不是 CI |

### 六、集合与组学（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 18 | 维恩图 `venn` | 两书/三书概念重叠 | **概念交集图 NEW** | `sets{}` 元素列表 | 仅 2–4 集；≥5 改 `upset` |
| 19 | UpSet `upset` | 多标签、多书高频交集 | **交集点阵 NEW** | `sets{}`,`top_n`,`sort`,`min_size` | 2–30 集；截断交集必须说明 |
| 20 | 火山图 `volcano` | 「显著 / 不显著」二分高亮 | **重点高亮散点 NEW** | `log2fc`,`pvalue` 等长 + `fc_cut`,`p_cut` | p=0 须截断为 1e-300；FDR 须数据侧换算 |

### 七、统计推断与 Meta（4）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 21 | 森林图 `forest` | 「多项证据强度不一」 | **证据强弱尺 NEW**（含汇总菱形） | `labels`,`estimates`,`ci_low`,`ci_high` + `overall`,`weights` | 无效线按尺度自动（OR/RR/HR=1，MD/SMD=0）；气泡=权重 |
| 22 | 亚组森林 `subgroup` | 「对不同人群效果不同」 | 分组证据尺 | `subgroups[]{name,p_interaction,levels[]}` | 只可视化已拟合模型；P 值不得手编 |
| 23 | 漏斗图 `funnel` | 「小样本结论更极端」 | **偏倚漏斗 NEW** | `studies[]{name,effect,se}` | ≥3 研究才可 Egger；不对称≠必然偏倚 |
| 24 | Galbraith `galbraith` | 找离群研究 / 异质性 | 离群诊断页 | 同 `funnel` | ±1.96 齐性带；OR/HR/RR 才画效应量弧 |

### 八、生存分析（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 25 | KM 曲线 `km` | 「留存/流失随时间」 | **留存阶梯线 NEW**（用户/习惯留存可借用） | `groups:{组:[[t,e]]}` 或 `time`+`survival`+`censored` | 中位未达到须如实标注；曲线交叉时 log-rank 失效 |
| 26 | CIF `cif` | 存在竞争结局 | 多原因分流曲线 | `time`,`event`(0/1/≥2),`cause_labels` | 单队列；**有竞争事件时 1−KM 系统性高估**（实测 +45.5pp） |
| 27 | RMST `rmst` | 「平均多活 X 个月」这类结论 | 面积差对比页 | `groups` 两臂 `[时间,事件]`,`--rmst-tau` | 报告 τ 取值及理由；PH 不成立时的标准替代 |

### 九、临床预测模型（5）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 28 | ROC `roc` | 「判断准不准」 | 判别力对比页 | `fpr`,`tpr`,`auc`,`ci` 或 `curves[]` | 须报 95%CI、独立验证集；类别不平衡补 PR 曲线 |
| 29 | 校准曲线 `calibration` | 「说的概率 vs 实际发生」 | **承诺-兑现对照 NEW** | `bins[]` 或 `predicted`/`observed`∈[0,1] | 引擎不自动分箱；大样本 H-L p 几乎必然显著 |
| 30 | DCA `dca` | 「这套方法值不值得用」 | **净收益决策页 NEW** | `thresholds` 严格升序∈(0,1),`models[]` 1–6 | 阈值须来自真实决策点；端点 t/(1−t) 无定义 |
| 31 | 列线图 `nomogram` | 多因素换算成总分 | 评分尺（工具方法型笔记） | `variables[]` 1–12 + `outcome_scales` 1–3 | **只可视化已拟合模型**，引擎不拟合不算分 |
| 32 | RCS `rcs` | J/U 形非线性关系 | 曲线函数族（思维模型 CV） | `points[]{value,est,ci_lo,ci_hi}` ≥5 单调 | 只可视化已拟合样条；CI 带与参照线相交=无差异区 |

### 十、方法一致性与临床疗效（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 33 | Bland-Altman `bland_altman` | 两种测量/两位评分者是否一致 | **一致性诊断页 NEW** | `methods` 恰 2 组等长 | 相关系数不能证明一致性；差值随均值增大须对数变换 |
| 34 | 瀑布图 `waterfall` | 逐条目「变好/变差」排序 | **逐例瀑布 NEW**（要点排序升级） | `change[]`,`group`,`pr_cut=-30`,`pd_cut=20` | 每例一柱；样本大时改分布图；须说明评估时点 |
| 35 | 游泳图 `swimmer` | 逐对象时长 + 里程碑 | **时间线（逐行版）NEW** | `end[]`(>0),`milestones`,`ongoing` | 端点标记必留 pad（xlim 自留 4%，时长 ×1.07） |

### 十一、组图与流程（3）

| # | 图型 / slug | 触发信号 | 笔记改写 · 器型 | 数据契约 | 统计红线 |
|---|---|---|---|---|---|
| 36 | 复合多面板 `composite` | 一页讲完一个多层结论 | **A/B/C 组图主版式 NEW**（咨询级五区骨架升级） | `layout:[行,列]`,`panels[]{type,data,title,pos,span}` | 面板禁嵌 composite/diagram/upset；跨数量级禁 `share_y` |
| 37 | 流程架构 `diagram` | 研究设计、技术路线、因果链 | 框架模型图 / 流程链 | `blocks`,`arrows`,`groups`,`annotations`,`background:"light"` | 示意图不承载数据；白底上禁用纯白流程块 |
| 38 | PRISMA `prisma` | 文献筛选、层层收敛 | **筛选漏斗 NEW**（漏斗变体） | `records_identified`,`studies_included`,`exclusion_reasons`,`lang` | **数字自洽闸门**：加总不平 `exit 1` 拒绝出图 |

## §2 双层选型决策树（v2.8 合并路由）

**第一层：文字信号 → 笔记器型**（沿用 `visual-grammar.md` §2 + 思维模型库）。
**第二层：数据关系 → 科研图型**（吸收 PPTX P3 决策树）：

```
拿到一页内容，先问「有没有可量化的数据关系？」
├─ 组间比较 ─────────→ bar / box / violin / raincloud
├─ 构成比 ───────────→ stacked_bar（100%）；类目排名 → hbar
├─ 前后配对 / 两时点 ─→ paired / slope / dumbbell
├─ 相关与趋势 ───────→ scatter / line；双量纲 → dual_axis（慎用）
├─ 分布形态与位移 ───→ violin / ridgeline
├─ 矩阵数值 ─────────→ heatmap / cluster_heatmap；降维分群 → pca
├─ 集合交集 ─────────→ venn(2–4) / upset(≥5)；差异高亮 → volcano
├─ 生存结局 ─────────→ km；竞争风险 → cif；曲线交叉 → rmst
├─ 预测模型评价 ─────→ roc + calibration + dca + nomogram 四件套
├─ 非线性剂量反应 ───→ rcs；亚组效应 → subgroup
├─ Meta / 证据强弱 ──→ forest + funnel；异质性 → galbraith
├─ 方法一致性 ───────→ bland_altman；逐例疗效 → waterfall / swimmer
└─ 组图与流程 ───────→ composite / diagram / prisma
```

**合并规则（硬纪律）**：
1. 一页只选 **1 个主器型**；科研图型作为该器型的「数据化实现」，不是叠加第二张图。
2. 数据关系与文字信号冲突时，**以数据关系为准**（有真数据就别用抽象示意），但叙事标题仍用判断句。
3. 无真实数据 → 退回 HTML/SVG 器型，**禁止用示例数据伪装成书的证据**；如需示意，图注必须写「示意」。
4. 命中 `consulting-craft.md` 论证信号 → 主器型升级为 `composite` A/B/C，按五区骨架排布。
5. 每页仍受文字预算约束（图解页 ≤120 字）、每章 ≥2 种器型、全书 ≥6 种；38 图型计入器型多样性池。

## §3 出版级设计令牌（可直接抄进 CSS）

### §3.1 9 套色板（唯一权威：引擎 `gen_figure.py:THEMES`）

| 主题 | 尺寸 / 字号 / 网格 alpha | hex 序列（c1→c10） |
|---|---|---|
| `glm`（默认，色盲安全，白底 4.5:1） | 10×6in / 11pt / 0.15 | `#5B8DBE #D79D55 #6BA776 #9B7BB8 #C9694E #5BA0A0 #B47A8E #7A7A7A #C4A44A #7AAF42` |
| `okabe-ito`（投稿金标准） | 8×5.5 / 7pt / 0.2 | `#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000 #999999 #44AA99` |
| `cool`（色盲安全，190–260° 色相） | 9×5.5 / 8pt / 0.15 | `#1B4965 #2E6F9E #4FA3C5 #3D8080 #62A0A8 #5B7BA0 #7B9AB5 #9DB5CC` |
| `classic` | 10×6 / 11pt / 0.3 | `#4C72B0 #DD8452 #55A868 #C44E52 #8172B3 #937860 #DA8BC3 #8C8C8C #CCB974 #64B5CD` |
| `nature`（NPG） | 8×5.5 / 7pt / 0.2 | `#E64B35 #4DBBD5 #00A087 #3C5488 #F39B7F #8491B4 #91D1C2 #DC0000 #7E6148 #B09C85` |
| `lancet` | 9×6 / 7pt / 0.25 | `#00468B #ED0000 #42B540 #0099B4 #525252 #7F6F00 #ED7D31 #8B6914 #4C0099 #99CC00` |
| `nejm` | 9×6 / 8pt / 0.25 | `#BC3C29 #0072B5 #E18727 #20854E #7876B1 #6F99AD #FFDC91 #EE4C97` |
| `science`（AAAS） | 8×5.5 / 7pt / 0.2 | `#3B4992 #EE0000 #008B45 #631879 #008280 #BB0021 #5F559B #A20056 #808180 #1B1919` |
| `conservative` | 9×5.5 / 8pt / 0.3 | `#2E86C1 #A0A0A0 #E74C3C #27AE60 #F39C12 #8E44AD #1ABC9C #E67E22 #34495E #16A085` |

别名：`okabe`/`colorblind`→`okabe-ito`；`default`→`glm`；`npg`→`nature`；`aaas`→`science`。
`glm-brand` 为第 10 套品牌变体（无网格 `#2E5E8F #FFB627 …`），非投稿用途。

**配色策略**（写进《设计决策单》）：
无序分类→离散色；有序→同色系深浅；连续→单色阶；发散→中心对齐 0（RdBu_r）。
对照组=中性灰/浅蓝、处理组=主色、升/危险=暖、降/保护=冷。
**编码色数 ≤ 实际组数、单图 ≤7 色**；灰度转印不可分时加斜纹/换明度阶/换标记形状（三重冗余编码）。

### §3.2 9 套期刊预设（引擎 `scripts/journal/*.json`）

| 期刊 | 单栏 | 双栏 | 正文字号 | 最小字号 | 字体族 | DPI |
|---|---|---|---|---|---|---|
| `nature` | 89mm | 183mm | 7pt | **5pt** | Helvetica | 600 |
| `lancet` | 85mm | 183mm | 8pt | 6pt | Arial | 600 |
| `science` | 55mm | 120mm | 7pt | **5pt** | Helvetica | 600 |
| `cell` | 85mm | 176mm | 8pt | 6pt | Arial | 300 |
| `nejm` | 89mm | 190mm | 8pt | 6pt | Helvetica | 300 |
| `jama` | 89mm | 183mm | 8pt | 6pt | Arial | 600 |
| `ieee` | 89mm | 181mm | 8pt | 6pt | Times New Roman | 600 |
| `cma` | 80mm | 170mm | 8pt | 6pt | Arial + CJK | 600 |
| `cn-core` | 80mm | 170mm | 9pt | 6pt | Arial + CJK | 300 |

** `--journal` 锁宽**：与 `--width` 同给时 width 被忽略（`--height` 仍有效）；
`nature/lancet/science/nejm` 未显式给 `--theme` 时自动联动同款配色。
笔记用法：双栏 183mm 可直接作为 NG 竖版「图表盒」宽、HBR 横版「整页大图表」栅格基准。

### §3.3 字体 / 线宽 / 坐标轴规范

- 字号层级：轴标签/标题=`font_size`；刻度=`fs−1`；热图列标签=`fs−2`；注释/显著性 ≥6pt。
- 框线：**隐藏上、右 spine**；y 轴虚线网格 alpha 0.15–0.3；`nature-clean` 皮肤另设
  `axes.linewidth=1.0`、无框图例、`grid.alpha=0`、粗体左对齐标题、线端直接标注。
- 误差棒：bootstrap CI `elinewidth=1.4/capsize=4`；bar `linewidth=1/capsize=3`；森林图 CI `linewidth=1.5`。
- 线型：折线 `linewidth=2/markersize=6`；趋势线灰虚线 `1.2`；参照线 `--` `1/alpha 0.6`。
- 斜纹：`['//','\\\\','||','--','++','xx','..','oo','**']`（无 None，所有柱都有纹），黑边 `0.6pt`。
- **白底硬约束** `facecolor='white'`；`axes.unicode_minus=False`；CJK 优先级
  Noto CJK → PingFang → STHeiti → YaHei/SimHei/SimSun → WQY → `fc-list` 兜底。
- 中国市场约定不变：涨红跌绿、货币 ¥（与「升/危险=暖」一致）。

## §4 HTML/SVG 版式落地规范（v2.8 新增组件）

资产：`templates/academic-charts.css`（:root 令牌 + 组件类，可直接 `<link>` 或内联）。

1. **令牌层**：9 色板用 `[data-af-theme="okabe-ito"]` 属性选择器切换；
   `--af-fig-w`（期刊栏宽 mm→px）、`--af-fs`（pt→px）、`--af-grid-alpha`、`--af-ink`。
2. **语义色 class**：`.af-control`（中性灰）、`.af-treatment`（主色）、`.af-up` / `.af-down`、
   `.af-ref`（参照线灰虚线）。**跨卡片、跨面板、跨页强制复用同一 class**，禁止逐图挑色。
3. **多面板 A/B/C**：CSS Grid + `::before` 生成粗体角标；`span` → `grid-row/column: span N`；
   同 y 轴标签面板才共享 y 轴，跨数量级自动断开。
4. **图例「预留顶部带」**：`af-legend-band` 为无框、绝对定位在图表区上方的独立 flex 行，
   **绝不 `position:absolute` 浮在数据区**；折线优先末端直接标注（`af-end-label`）替代图例。
5. **构造性避让三铁律**（机制级，优于事后目检）：
   - 预留带：图例/事实框/Δ 标注在 grid 里先占一行，不留「碰运气」的空白；
   - 端点 pad：SVG `viewBox` 四周自留 ≥4% 跨度，防圆点/CI 帽被裁半；
   - 靠边翻向：最右/最上 10% 区域的逐点标注自动 `text-anchor:end` / `dominant-baseline` 内翻。
6. **打印层**：`@media print` 强制白底、剥离装饰阴影、矢量优先；不输出深色/渐变背景图。

## §5 质量门禁（v2.9 验收五门 + 引擎门禁）

| 门 | 检查 | 阈值 / 判定 | 落点 |
|---|---|---|---|
| G1 真实墨迹重叠 | 不信任 bbox 相交；按 200dpi 渲染取墨迹连通分量，候选对在局部 600dpi 重渲染求最小欧氏距离 | 距离 >0.05pt 判分离；有真实重叠 → 拒收 | 引擎 `--verify`（PDF only，`exit 2`）；HTML 版式用 DOM 实测渲染像素复核，不只 `getBoundingClientRect()` |
| G2 最小字号 | 扫每个文本 span | 默认 ≥7pt（印刷安全线）；nature/science ≥5pt、其余 ≥6pt；笔记正文 ≥14pt 不变 | `audit_pdf.py --min-size N --fail-below` |
| G3 白底与可分辨 | 背景色、灰度转印、红绿共现、色数 | 白底零容忍深色；≤7 色；红绿不共现编码关键信息；灰度不可分加斜纹/明度阶 | `academic-charts.css` 打印层 + 人工闸门 |
| G4 确定性与可复现 | 同输入→字节相同；元数据剥离；旁车文件 | PDF `CreationDate:None`、固定 bootstrap 种子 `20260925`、期刊预设下**禁用 `bbox_inches='tight'`**（会把 85mm 裁成 82.4mm） | `--audit`（计数+sha256）、`--repro`（命令+数据副本+成图）、`--alt`/`--caption` |
| **G5 4K 分辨率**（v2.9 新增） | 按 PNG IHDR 实测位图像素；**不信任「600dpi」标签** | 位图 `max(W,H) ≥ 3840` **且** `min(W,H) ≥ 2160`（≥8.29MP）；矢量 PDF/SVG/EPS 等效；不达标 `exit 2` | `figure-bridge.py --resolution 4k`（默认）；`[4K OK/FAIL]`；`.bridge-audit.json.resolution`；`.bridge-report.json.items[].resolution` |

### §5.1 G5 4K 门禁细则（v2.9）

**为什么需要单独一门**：默认 600dpi 在自由画幅上已是 4739×3227≈15.3MP（超 4K），
但期刊预设会**锁宽**：`science` 单栏 55mm = 2.17in × 600dpi ≈ 1300px 宽，远不足 4K；
`nature` 单栏 89mm = 3.50in × 600dpi ≈ 2100px 也不足。只看 DPI 数字会漏判，必须实测像素。

| 项 | 规则 |
|---|---|
| 判据 | `long_edge ≥ 3840 AND short_edge ≥ 2160`（可用 `--min-long-edge` / `--min-short-edge` 覆盖） |
| 矢量 | PDF/SVG/EPS 分辨率无关，判为 `[4K OK] vector`；需要位图交付物时必须显式出 png/tiff |
| 自动反推 | `dpi = max(600, ceil(3840/图宽in), ceil(2160/图高in), 显式dpi)`，上限 `--max-dpi 2000` |
| 图幅估算 | 期刊模式读 `scripts/journal/*.json` 的 `widths_mm[column]`；自由模式取主题 `figsize`（保守取 8×5.5in） |
| 实测 | 纯标准库读 PNG IHDR（无需 Pillow）；仅出 TIFF 时自动补一张 PNG 作校验代理 |
| 一次自愈 | 引擎内存护栏可能把 dpi 砍半 → 不达标时自动 `dpi×1.6` 重渲染一次；仍失败 `exit 2` |
| 失败处置 | 改 `--column double` / 去掉 `--journal` 用自由尺寸 / `--resolution auto` 显式豁免并在交付说明注明 |
| HTML/SVG 版式 | 截图导出长边按 3840px（`--af-export-w`）；NG 竖版 2160×3840、HBR 横版 3840×4560 等比；导出后按 IHDR 复核 |

**实测基线（本机 2026-11-04）**：

| 场景 | DPI | PNG 像素 | 判定 |
|---|---|---|---|
| 默认自由画幅 `okabe-ito` | 600 | 4739×3231 = 15.31MP | 4K OK |
| `science --column single` | **1774**（自动反推） | 3841×2640 = 10.14MP | 4K OK |
| 纯 `pdf,svg` | — | 矢量 | 4K OK (vector) |
| JSON 流水线 2 图 | 600 | 4739×3227 / 4740×3226 ≈ 15.29MP | 2/2 4K OK |

**引擎退出码**：`0` 成功｜`1` 参数/致命校验（不落盘）｜`2` verify 重叠或批量有失败项｜
`3` 数据/格式｜`4` 环境/依赖｜`5` 看门狗超时（30–1800s 自适应）｜`6` 内存护栏。
`AF_DEBUG=1` 出完整堆栈。**投稿/交付 PDF 忘加 `--verify` 是最高频退稿点**；该 flag 在 PNG/TIFF 上静默跳过。

**导出规格**：矢量 PDF/SVG/EPS 优先；位图 PNG/TIFF 600dpi（严格期刊线条图可 1000dpi）；
`--multi-format tiff,png,pdf` 一次渲染同源文件名；`--pub-ready` = `--verify` + 色盲安全主题 + pdf,png + 复跑包。

## §6 反模式红线（20 条，写入验收清单）

1. 白底零容忍深色/渐变/3D 装饰；流程块禁用 `#FFFFFF`（白底隐形）。
2. 红绿共现编码关键信息（约 8% 男性红绿色盲）；升/降改暖橙/蓝。
3. 单图 >7 色；编码色数 > 实际组数。
4. 语义色跨图不一致：对照组/处理组/同一变量换色。
5. 高饱和荧光色、startup 感渐变；白底对比不足 4.5:1。
6. 误差棒不标 SD/SE/95%CI；bar+误差棒冒充原始分布（应用 box/violin/raincloud）。
7. 显著性星号无可溯源检验；多组两两比较不做 Tukey / Dunn+Hochberg 校正。
8. 手编 P 值 / 星号；`nomogram/rcs/subgroup/calibration` 让引擎「自动拟合」（引擎只可视化）。
9. PH 不成立仍用 log-rank（改 `rmst`）；有竞争事件仍报 1−KM（改 `cif`）。
10. 「先排序后标注」不同源索引 → Δ 错位（哑铃图类级铁律）。
11. 浮动图例/事实框用 `loc="lower right"` 碰运气，而非构造性预留带。
12. 显式 `set_xlim` 关闭自动边距，端点圆点/CI 帽被裁半。
13. 最右/最上 10% 的逐点标注仍朝外，冲出画布。
14. 跨数量级面板共享 y 轴（>5× 范围差；`--doctor` 会提示）。
15. `--journal` 与 `--width` 同给却以为 width 生效。
16. `--verify` 只加在 PNG/TIFF 上（静默跳过）；投稿 PDF 不加。
17. composite 面板嵌套 composite/diagram/upset；对自管图型用 `tight_layout`。
18. PRISMA 数字不自洽还强行出图；venn 画 ≥5 集；slope 画 >2 时点；pca >200 列；cluster_heatmap >3000 行不降采样。
19. CJK 细节：字典键中文未触发字体加载；`⁹/³/²` 字形缺失（改写 `10^9/L`）；负号显示成方块。
20. 输入未变却反复重试同一命令（结果/报错必然相同）；不信任 bbox 报告、逐图特判而不修机制。

## §7 引擎桥接（把 38 图型真图接进笔记）

**本机引擎**（v2.8 安装时确认）：
- 主用：`/Users/wdj/.workbuddy/skills/academic-figures`（ClawHub 发布包，含 `references/pitfalls.md` 21KB 踩坑全集）
- 备用：`/Users/wdj/.openclaw/skills/academic-figures`（GitHub tag v5.9.0 完整源码，含 7 张色板样张）
- 两份 `scripts/*.py` 逐字节一致；SKILL.md 仅差 frontmatter 一行 `version: 5.9.0`。

**依赖坑（实测）**：WorkBuddy 内置 Python 3.13.12 缺 `matplotlib/scipy/openpyxl`；
`/opt/homebrew/bin/python3` 与 `/usr/bin/python3` 五项齐全。
→ **必须用系统 python 调引擎**，见 `scripts/figure-bridge.py` 的自动探测；不要 `pip install` 到内置环境。

**桥接脚本**（纯标准库，无需第三方）：
```bash
# 0) 环境自检（引擎路径 / 可用 python / 依赖）
python3 scripts/figure-bridge.py --check

# 1) 列出 38 图型 / 9 色板 / 9 期刊
python3 scripts/figure-bridge.py --list types
python3 scripts/figure-bridge.py --list themes
python3 scripts/figure-bridge.py --list journals

# 2) 出单图（JSON 数据契约 + 色盲安全主题 + 期刊锁宽 + G1 真实墨迹 + G5 4K）
python3 scripts/figure-bridge.py \
  --type bar --data assets/data/ch01.json --out assets/fig/ch01-bar \
  --theme okabe-ito --journal nature --column double \
  --formats pdf,png --resolution 4k --verify --alt --caption
# --resolution 4k 为默认值，可省略；日志必须出现 [4K OK] W×H = X MP ≥ 3840x2160

# 3) 批量：YAML/JSON 流水线（defaults + figures），失败项出汇总报告并整体判失败
python3 scripts/figure-bridge.py --pipeline assets/figures.yaml --verify
```
数据契约（JSON schema 速查，完整字段见引擎 `references/data-formats.md`）：
`bar{labels,series,errors?,significance?}` · `heatmap{matrix,row_labels,col_labels,cbar_label}` ·
`scatter{x,y,groups?}` · `forest{labels,estimates,ci_low,ci_high,overall,weights}` ·
`km{groups:{组:[[t,e]]}}` · `roc{fpr,tpr,auc,ci}` ·
`composite{layout,panels:[{title,type,pos,data,span?}],panel_labels,share_y}` ·
`diagram{background:"light",blocks,arrows,groups,annotations}` ·
`prisma{records_identified,studies_included,exclusion_reasons,lang}`。

**JSON vs CSV 硬边界**：CSV/TSV 只承载「首列=X 标签、每列=series」的最简数据；
`errors`、`significance`、KM 风险表、`composite`、`dual_axis`、`diagram`、`prisma`、forest 复杂 schema
**一律 JSON**（CSV 会静默丢失误差棒）。`.xlsx` 需 `--sheet`。

**渲染前校验闸门**（脚本内置）：文件存在 → JSON 合法 → 必填字段齐全 → 数组等长 → 数值有限 →
自洽性（如 prisma 加总）→ 才调引擎；失败 `exit 3`，不落半成品。

## §8 与七步工作流对接

| 步骤 | v2.8 插入动作 |
|---|---|
| Step 0 设计智能前置 | 《设计决策单》新增两栏：**科研色板**（9 选 1，默认 `glm` / 无障碍 `okabe-ito`）与**栏宽基准**（9 期刊预设或自定义 mm） |
| Step 0.5 判版式 | 三路版式不变；NG 竖版「图表盒」/ HBR 横版「整页大图表」直接引用期刊双栏宽 |
| Step 2 定调 | 主题层令牌可来自：Step 0 检索 > 品牌 DESIGN.md > **科研色板** > 内置映射表；冲突时品牌优先，但科研图内部必须保持色板自洽 |
| Step 3 图表化转译 | 先跑第一层文字信号，再跑 §2 第二层数据关系；产出《器型清单》新增「科研图型」列与「数据契约」列 |
| Step 3.5 科研级增强 | 有真数据 → 走 §7 桥接出真图并过 §5 **五门**（含 G5 4K）；无真数据 → 走 §4 HTML/SVG 器型（截图长边 3840px），图注标「示意」 |
| Step 4 排页 | 论证页主器型可升级 `composite` A/B/C；图例用预留带；端点 pad 与靠边翻向由 CSS 保证；文字预算不变 |
| Step 5 导出 | 矢量优先；交付包附 `alt.txt`/`caption.txt`/`audit.json`；批量失败项汇总报告随交付说明 |

## §9 来源与版本

- `academic-figures v5.9.0`（2026-10-23，docsor1212，MIT-0）：38 规范图型（注册表 41 键含 3 别名）、
  9 色板、9 期刊预设、YAML 流水线、`--verify` 三级像素重叠检测、`audit_pdf.py` 字号门禁、退出码 0–6。
- 《38种科研图表收集整理报告（样例增强版）.pptx》：93 页，38 图型 × 11 大类 × 每型「用途/场景/要点/提示」四段式，
  34 张引擎模板样例 + 4 张易方达基金 MCP 真实数据（柱状/水平条/折线/散点），600dpi PNG 约 4800×3300px。
- 交叉校验结论：PPTX 的 38 与引擎注册表 38 一致；SKILL.md 里「37」是 v5.8 滞后口径，不采用。
- **v2.9.1（2026-11-04）**：新增 G5 4K 分辨率门禁——所有图型图表统一 4K 级输出
  （位图长边 ≥3840 且短边 ≥2160、矢量等效、DPI 自动反推、PNG IHDR 实测、一次自愈、
  JSON 流水线逐图记录 `resolution`）；同步把 SKILL.md 的 frontmatter description 压到 ≤1024 字符，
  避免 ClawHub / ZCode 自动发现静默丢弃超长描述。

## §10 v2.9.1 发布与同步

- 本机主副本：`~/.workbuddy/skills/reading-notes-master/`（WorkBuddy 用户级 skill）。
- GitHub：`git@github.com:yjkj999999/reading-notes-master.git`，tag `v2.9.1`（`v2.9.0` 保留为历史 tag）。
- ClawHub：slug `reading-notes-master`，owner `yjkj999999`，version `2.9.1`。
- 三端一致性原则：SKILL.md / references / templates / scripts 同源发布；
  `dist/` 与 `.git/` 不进发布包（`.gitignore` 已排除 `dist/`）。
- **发布踩坑（2026-11-04）**：`clawhub publish --version 2.9.0` 返回
  `OK. Published reading-notes-master@2.9.0 (versionId)`，但服务端
  `GET /api/v1/skills/<slug>/versions/2.9.0` 恒为 404，版本列表与 `latest` tag 仍停在 2.6.0；
  重发同一版本被拒 `Version 2.9.0 already exists. Increment the version number and try again.`
  —— 该版本号已被占用却未挂载公开索引，**版本号不可覆盖，只能递增**。
  处置：本地推进 `2.9.1` 后重发，并立即做 `inspect --versions` + `install --version` 双验证。
  排查要点：本机 `HTTP_PROXY/HTTPS_PROXY=http://127.0.0.1:<port>`，curl 默认走代理会报
  `CONNECT tunnel failed, response 502`；用 `curl --noproxy '*'` 直连 registry 才能拿到真实响应。
  CLI 报 `... (reset in Ns)` 是 `http.js` 把 `ratelimit-reset` 响应头附加到服务端错误后面，
  **不等于限流导致**，要看前半段的基础错误信息。
