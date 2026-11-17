# 期刊 DNA 卡：按刊、按子产品线抽取契约

> 引入版本 **v2.13.0** · 配套 `references/exact-replication-contract.md`（完全复刻契约）
> 用途：在启动「完全复刻 / 风格近似复刻」前，先判定**刊物 + 子产品线**，取对档案卡，避免契约套错刊。

## 0. 数据源与口径（全部实测，禁止编造）

| 文件 | 口径 | 提供什么 |
|---|---|---|
| `analysis/cross_magazine_probe.json` | **六刊采样口径** | 页数 / 画布 / 字体族 / 字号 top5 / 主色 / `med_chars` / `med_cover` |
| `analysis/time_original_dna.json` | **TIME 常规周刊全量口径**（74 页逐页汇总） | `n_pages` / `page_sizes` / 字体矩阵 / 色板 / 边距 / `median_*` / 379 项嵌入字体 |
| `analysis/time_archetypes.json` | 74 页人工标注 | 逐页原型与 8 类分布 |

> **口径警告（不可混用）**：`cross_magazine_probe.json` 的 `med_chars / med_cover` 是采样口径
> （TIME 常规周刊 `2706 / 0.38`），`time_original_dna.json:summary` 的 `median_chars / median_cover`
> 是全量口径（`3043.0 / 0.347`）。两者都对，但**不能拼进同一句结论**；引用时务必标注来源。

---

## 1. 六刊实测对照表

全部数值逐项回读自 `analysis/cross_magazine_probe.json`。`med_cover > 1` 是合法值（图像块面积可超出页面，出血/叠加）。

| 刊物 | 页数 | 画布 pt | 主字体族（top6） | 字号 top5 (pt) | 主色 top5 | `med_chars` | `med_cover` | 密度画像 |
|---|---:|---|---|---|---|---:|---:|---|
| **TIME 常规周刊** `Time_2026-09-28.pdf` | 74 | `567.03 × 756.0` | HaffnerTIME-Regular / ITCFranklinGothicStd-Boo / -Med / -Dem / -Hvy / HaffnerTIME-Bold | `10.0 / 8.8 / 8.0 / 9.9 / 8.5` | `#231F20 / #000000 / #ED1C24 / #FFFFFF / #001322` | 2706 | 0.38 | 文字主导、多栏正文 |
| **TIME Special Edition** `…- Spider Man 2026.pdf` | 100 | `576.0 × 783.0` | ITCFranklinGothicStd-Boo / -Hvy / -Dem / HaffnerTIME-Regular / ITCFranklinGothicStd-DmC / DuplicateIonic-Regular | `8.0 / 8.8 / 163.0 / 70.0 / 74.0` | `#111011 / #E6161F / #FFFFFF / #000000 / #262324` | 682 | 1.00 | 巨字标题、满版图像 |
| **Vogue Singapore** Sep 2026 | 182 | `623.62 × 807.87` | SaolText-Regular / -RegularItalic / PPNeueMachina-Regular / SaolText-Book / SaolDisplay-RegularItali / SaolDisplay-Regular | `9.0 / 7.5 / 11.0 / 6.0 / 12.5` | `#231F20 / #94A741 / #FFFFFF / #000002 / #151616` | 35 | 1.00 | 图像满版、极少文字 |
| **New Scientist** 2026-09-19 | 52 | `575.43 × 756.85` | TheAntiquaB-W5Plain / -W8ExtraBold / EnzoPro-Bold / EnzoPro-Medium / TheAntiquaB-W5PlainItali / -W9Black | `8.2 / 8.0 / 6.0 / 7.0 / 13.0` | `#231F20 / #F36F21 / #5BB34A / #58595B / #D2232A` | 4158 | 0.15 | 文字密集、低图像 |
| **National Geographic** 2026-10 | 140 | `495.97 × 720.0` | NatGeoBumstead-Heavy / GeographEdit-Medium / GrosvenorBook-Regular / -Medium / NatGeoCaption-Heavy / GrosvenorBook-Semibold | `9.0 / 8.0 / 6.0 / 7.8 / 7.5` | `#000000 / #FFFFFF / #006DA6 / #CAD9C7 / #FFD201` | 425 | 1.02 | 图像满版（cover 可 >1） |
| **Bloomberg Businessweek** Sept 2026 | 96 | `568.0 × 757.0` | BWText-Roman / BWHaasText-75Bold / BWHaasHead-95Black / BWHaasText-65Medium / BWText-Italic / BWHaasText-66MediumItali | `8.9 / 8.8 / 6.6 / 9.0 / 10.0` | `#231F20 / #FFFFFF / #8F8381 / #F4838D / #16191A` | 92 | 0.67 | 图文混合 |

**可直接读出的契约差异**：画布 6 种全不同（`495.97×720` 到 `623.62×807.87`）；
`med_chars` 从 `35`（Vogue）到 `4158`（New Scientist）跨两个数量级；
`med_cover` 从 `0.15` 到 `1.02`；字号从 `6.0pt` 到 `163.0pt`。
因此**不存在一份「通用期刊模板」**——契约必须按「刊 × 子产品线」分别抽取。

---

## 2. 常规周刊与特辑不能共用档案卡（破坏性认知修正，v2.13）

同一品牌 `TIME` 的两条产品线，实测差异如下（左列采样口径 / 右列同源）：

| 指标 | 常规周刊 `Time_2026-09-28.pdf` | Special Edition `Spider-Man 2026` | 差异 |
|---|---|---|---|
| 画布 pt | `567.03 × 756.0` | `576.0 × 783.0` | 不同 |
| 页数 | 74 | 100 | 不同 |
| 主字号 | `10.0 / 8.8`（正文） | `163.0 / 70.0 / 74.0`（巨字） | 正文 vs 展示 |
| `med_chars` | 2706 | 682 | 约 4 倍 |
| `med_cover` | 0.38 | 1.00 | 文字主导 vs 满版 |
| 主红 | `#ED1C24` | `#E6161F` | 红不同 |
| 密度画像 | `text-led`（文字主导） | `fullbleed`（满版特辑） | 分型不同 |

**根因错误（已确认）**：`scripts/journal_4k_check.py` 旧 `TIME_SPECIAL` 档案卡
（`page_pt=(576,783)`、`dpi=353`、`cols=3`、`density="fullbleed"`、`cov_ref=1.0`、
`margin_l=28.3`、`margin_r=11.4`、`sig_degraded=True`）**实际描述的是 Special Edition**，
却被当作常规周刊使用，是契约套错刊的根源。

**v2.13 整改**（三条互不覆盖的独立卡，旧键保留向后兼容）：

| 键 | 语义 | 用于 |
|---|---|---|
| `TIME_WEEKLY` | Time 美国版常规周刊（文字主导） | **常规周刊任务一律用这条** |
| `TIME_SPECIAL` | 旧键，`name` 标「Time 特辑（满版降级卡）」 | 向后兼容；**不适用于常规周刊** |
| `TIME_SPECIAL_EDITION` | `TIME_SPECIAL` 的语义别名（同参数） | 新代码按语义取名，指满版特辑 |

> 一句话规则：**开工前先比对画布 pt 与 `med_cover`——`567.03×756 / 0.38` 走 TIME_WEEKLY，
> `576×783 / 1.00` 走 TIME_SPECIAL_EDITION，两者绝不混用。**

---

## 3. 按刊 / 子产品线的 DNA 卡

### 3.1 TIME 常规周刊（全量口径，`time_original_dna.json`）

| 项 | 实测值 |
|---|---|
| `source` | `Time_2026-09-28.pdf` |
| `n_pages` / `page_sizes` | `74` / 唯一 `[[567.03, 756.0]]` |
| `median_chars` / `median_images` / `median_cover` | `3043.0` / `2.0` / `0.347` |
| `global_margin_l` / `global_margin_r` | `41.86` / `38.72` |
| 字体族数 / 嵌入字体项 | `52` 族 / `379` 项（`type=Type1`、`ext=pfa`、页级子集） |
| 正文主字体（body 8–10.9 计数） | `HaffnerTIME-Regular 3159` / `ITCFranklinGothicStd-Boo 2149` / `ITCFranklinGothicStd-Med 1458` |
| 展示字体 | `HaffnerTIMEDisplay-*` 家族（`-Black` 在 `display≥24` 段 8 次、`title 14-23` 段 47 次） |
| 文字色 top5 | `#231F20(5974)` / `#000000(2039)` / `#252525(380)` / `#FFFFFF(171)` / `#ED1C24(149)` |
| 填充色 top3 | `#211F1D(19104)` / `#FFFFFF(985)` / `#131A1F(632)` |

> 页级 Type1/PFA 子集（前缀 `XVHNVY+` / `KTQNVY+` / `VHBQTC+` 等，`pages` 多为 1）
> 是完全复刻「字体资源边界」的物理依据，见 `exact-replication-contract.md` §6。

### 3.2 TIME 常规周刊原型分布（`time_archetypes.json`）

74 页全部归类，`distribution` 合计 = 74：

| 原型 | 页数 | 原型 | 页数 |
|---|---:|---|---:|
| `FEATURE 特稿正文` | 45 | `SECTION OPENER 栏目开场` | 7 |
| `DEPARTMENT 栏目页` | 8 | `FULL-BLEED AD/IMAGE 全版图/广告` | 7 |
| `SHORT/IMAGE 短页` | 4 | `COVER 封面` | 1 |
| `CONTENTS 目录/版权` | 1 | `AD 广告` | 1 |

`archetypes[74]` 逐页绑定（如 P1=COVER、P2=CONTENTS、P8=SECTION OPENER、P26/P36/P40/P43/P61/P67/P74=FULL-BLEED）。
**完全复刻的页序/页数/原型绑定据此冻结**，是 §4 验收 C7 的依据。

### 3.3 其余四刊要点（采样口径，`cross_magazine_probe.json`）

- **TIME Special Edition**：100 页、`576×783`、163pt 巨字、`med_cover=1.00`、红 `#E6161F` → 满版特辑卡。
- **Vogue Singapore**：182 页、`623.62×807.87`、Saol 三栈、`med_chars=35`、`med_cover=1.00` → 极窄边距满版，文字极少。
- **New Scientist**：52 页、`575.43×756.85`、TheAntiquaB/EnzoPro、`med_chars=4158`、`med_cover=0.15` → 文字最密、图像最低。
- **National Geographic**：140 页、`495.97×720`、GrosvenorBook/Geograph、`med_cover=1.02` → 图像满版且允许 cover >1。
- **Bloomberg Businessweek**：96 页、`568×757`、BWText/BWHaas、`med_chars=92`、`med_cover=0.67` → 图文混合。

---

## 4. 档案卡参数对照（`scripts/journal_4k_check.py::PROFILES`，v2.13）

| 键 | name | `page_pt` | `dpi` | 字体 serif / sans | 签名色 | 降级 | 边距 L/R | `cols` | `density` | `cov_ref` |
|---|---|---|---|---|---|---|---|---|---|---|
| `TIME_WEEKLY` | Time 美国版常规周刊 | `(567.03, 756.0)` | 300 | `HaffnerTIME`,`HaffnerTIMEDisplay` / `ITCFranklinGothicStd`,`FranklinGothic` | `#231F20 #000000 #ED1C24 #FFFFFF` | `sig_degraded=False` | 25.3 / 45.3 | 2 | `text-led` | 0.471 |
| `TIME_SPECIAL`（旧键保留） | Time 特辑（满版降级卡） | `(576, 783)` | 353 | `HaffnerTIME`,`Haffner`,`Playfair`,`Georgia` / `ITCFranklinGothic`,`FranklinGothic`,`Franklin Gothic`,`Archivo` | 空 | `sig_degraded=True` | 28.3 / 11.4 | 3 | `fullbleed` | 1.0 |
| `TIME_SPECIAL_EDITION`（语义别名） | Time Special Edition（满版特辑） | `(576, 783)` | 353 | 同上 | 空 | `sig_degraded=True` | 28.3 / 11.4 | 3 | `fullbleed` | 1.0 |

**数值来源与口径（两套度量不可混用）**：
- `TIME_WEEKLY` 的 **J3 卡片参数** `margin_l=25.3 / margin_r=45.3 / cols_est=2 / cov_avg=0.471 / dpi=300`
  出自 `journal_4k_check.measure_pdf()` 对原刊实跑：12 个采样页各自 `median(x0)` 再跨页取 median，
  覆盖率为 12 页 `cov_pp` 均值。**切勿**用「正文 x0 ÷ 页宽 ≈ 5.3%」充当 `margin_l`，
  那是视觉左边距，不是四门口径。
- 上表 §1 的 `median_cover=0.347`（常简写 ~0.35）、`median_chars=3043`、
  `global_margin_l/r=41.86/38.72`、`page_pt=(567.03,756.0)` 是 **原刊 DNA 全量逐页口径**，
  出自 `analysis/time_original_dna.json` 与 `analysis/cross_magazine_probe.json`，
  只用于「判线」——判断同品牌是否属于不同子产品线，不用于填写档案卡 J3 参数。
- 特辑两卡沿用旧 `TIME_SPECIAL` 实测参数（`page_pt=(576,783)`、`dpi=353`、`cols=3`、
  `fullbleed`、边距 28.3/11.4），与 `cross_magazine_probe.json` 的 Special Edition 行一致。

> 兼容说明：v2.13 之前 `PROFILES` 为 14 张卡；现为 16 张（新增上述 2 张语义卡，旧 `TIME_SPECIAL`
> 键与取值**完全不动**，仅补注释「不适用于常规周刊」）。`DENSITY_TOL` 同步新增 `text-led`
> 分型，保证 `--profile TIME_WEEKLY` 走 J3 判定时不报 `KeyError`。原有 14 卡行为不变。

---

## 5. 新刊接入：DNA 卡抽取步骤

对齐 `exact-replication-contract.md` §2 的六阶段管线；每步产出可复算、可冻结的契约文件。

```text
1. 探查（S1）：对目标 PDF 量测——画布唯一值、页数、字体矩阵（族名/字号）、
   文字色/填充色 top、字号 top5、med_chars、med_cover、global_margin_l/r、嵌入字体项数与类型。
   → 写成 <MAG>_original_dna.json；多刊对照写 cross_magazine_probe.json。
2. 判线：与已有契约库比对；同品牌出现两套以上画布/med_cover 画像 → 判为子产品线，
   另立契约（TIME 常规周刊 vs Special Edition 即此例）。先比对画布 pt 与 med_cover。
3. 建模（S2/S3）：build_page_models 逐页抽 span/image/drawing + ladder/hist；
   classify_archetype 归类，得到 <MAG>_archetypes.json 与逐页模型。
4. 固化：写 contracts/<CONTRACT_ID>.json，锁定固定设计层全部字段
   （画布/页序/原型/字体参数/色板/栅格/边距/页眉页脚/图片位置/图表图形）
   + 字体资源边界声明 + 零偏差验收协议；同时把档案卡参数写进 journal_4k_check.py::PROFILES
   （新增键，不覆盖旧键；新 density 分型同步补 DENSITY_TOL）。
5. 冻结：契约文件加版本号与哈希；任何变更需新版本号，禁止原地覆盖。
6. 复用：同刊次期只需重跑 S1 校验契约是否仍成立；成立则直接沿用 S4 底版流程
   （replicate_1to1）与已冻结的槽位表。
```

**门禁**：步骤 2 判错线 = 契约套错刊（§2 根因错误）；步骤 4 漏登字体边界 = 交付违规；
步骤 3 逐页模型元素总数必须可复算。抽取完成后再进入 S5 槽位定义 + `collision_report` 碰撞预检。

---

## 6. 数字出处速查

| 数字 | 出处 |
|---|---|
| 六刊页数 / 画布 / 字体 / 字号 / 主色 / `med_chars` / `med_cover` | `analysis/cross_magazine_probe.json`（§1 全表） |
| 74 页、`567.03×756.0`、`median_chars 3043` / `median_images 2` / `median_cover 0.347`、`global_margin_l 41.86` / `global_margin_r 38.72` | `analysis/time_original_dna.json:summary` |
| 379 嵌入字体 / 52 字体族 / 文字色与填充色计数 | `analysis/time_original_dna.json:embedded_fonts / font_matrix / text_colors / fill_colors` |
| 原型 `45/8/7/7/4/1/1/1`、逐页 `archetypes[74]` | `analysis/time_archetypes.json:distribution / archetypes` |
| 旧卡 `page_pt=(576,783)` / `dpi=353` / `cols=3` / `margin 28.3/11.4` / `sig_degraded=True` / `cov_ref=1.0` | `scripts/journal_4k_check.py` 旧 `TIME_SPECIAL` |
| `TIME_WEEKLY`/`TIME_SPECIAL_EDITION` 档案卡参数 | `scripts/journal_4k_check.py::PROFILES`（v2.13） |

> 本卡全部数值均已逐项回读核对，未外推、未编造；采样口径与全量口径已分列标注，引用时不得混用。
