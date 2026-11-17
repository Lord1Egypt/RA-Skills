# 期刊 4K 复刻闭环（v2.11）——Journal 4K Replication

> 核心思想：**同一把尺子量两次**。v2.10 语料采集用 `magcorpus/analyze_mags.py` 度量
> （字体族/矢量色/边距/栏数/图密度），本手册配套 `scripts/journal_4k_check.py` 用
> **完全相同的度量方法**验收你的渲染产物——偏差超门禁就迭代，直到四门全过。
> 「高精度模仿」不是凭感觉，是实测数字闭环。

---

## 一、四门验收门禁（J1–J4）

| 门 | 判定 | 量法 | 容差 |
|---|---|---|---|
| **J1 字体 DNA** | 产物 PDF 字体族命中档案卡官方字体前缀 **或** 声明的替代字体前缀；衬线正文 + 无衬线标题两栈齐备 | PyMuPDF 提取 span font，`^[A-Z]{6}\+` 清洗后前缀匹配 | 至少 serif 栈 1 命中 + sans 栈 1 命中 |
| **J2 色板签名** | 档案卡签名色 ≥1 个出现在产物矢量填充 top8（或降级：像素主色/文字色） | RGB 欧氏距离 | 距离 ≤36（每通道均 ~12） |
| **J3 栅格边距** | 文本左边距比例、栏数、图密度分型与档案卡一致 | 与语料同参数（30pt bin 聚类） | 边距比例差 ≤12pp；栏数差 ≤1；密度分型不换型 |
| **J4 4K 像素** | 位图长边 ≥3840 且短边 ≥2160；矢量 PDF 等效（分辨率无关）；内嵌位图有效 DPI ≥ 目标 DPI | PNG IHDR 实测 / PDF 图像 xref 反推 | 0 豁免（与 v2.9 G5 同尺） |

验收命令：

```bash
python3 scripts/journal_4k_check.py <rendered.pdf> --profile NG --json report.json
# exit 0 = 四门全过 / 1 = WARN / 2 = FAIL
python3 scripts/journal_4k_check.py --list          # 14 个 profile 一览
```

**验收对象规则**：J1–J3 依赖文本层，**验收目标一律用矢量 PDF**（渲染产物本身或同源
PDF）；PNG 交付时对 PNG 量 J4、对同源矢量 PDF 量 J1–J3，两次调用合并出报告。
纯 PNG 直接跑四门会得到 J1–J3 假 FAIL（无文本层可提取），不是产物问题。

## 二、4K 渲染规格——DPI 反推公式

**公式**：`dpi = ceil(3840 / 页面长边英寸)`；短边像素 = 短边英寸 × dpi（须 ≥2160，14 卡全部达标）。

| profile | 开本 pt | 长边 in | 4K DPI | 短边像素实测 |
|---|---|---|---|---|
| NG 主刊 | 496×720 | 10.00 | **384** | 2645 ✅ |
| HBR（v2.7 锚点） | 612×756 | 10.50 | **366** | 3110 ✅ |
| Bloomberg Businessweek | 568×757 | 10.51 | **366** | 2887 ✅ |
| Science | 594×756 | 10.50 | **366** | 3039 ✅ |
| New Scientist | 575×757 | 10.51 | **366** | 2947 ✅ |
| Scientific American | 585×774 | 10.75 | **357** | 2919 ✅ |
| Science News | 558×774 | 10.75 | **357** | 2780 ✅ |
| Vogue Singapore | 624×808 | 11.22 | **342** | 2985 ✅ |
| Cosmo UK | 567×737 | 10.24 | **375** | 2977 ✅ |
| Time 特辑 | 576×783 | 10.88 | **353** | 2851 ✅ |
| The Spectator | 596×784 | 10.89 | **353** | 2946 ✅ |
| The Observer | 820×1018 | 14.14 | **272** | 2230 ✅ |
| How It Works | 652×842 | 11.69 | **329** | 2994 ✅ |
| 青年文摘 | 612×792 | 11.00 | **349** | 2986 ✅ |

**两条渲染路径**（产物都要过 J4）：

- **PNG 截图路径**（4K 位图）：HTML 画布按原尺寸定义，Chrome headless 加
  `--force-device-scale-factor=<dpi/72>`（NG=5.33x / HBR=5.08x / 16:9 用 @3x），
  输出像素 = CSS px × scale。速查：NG 竖版 660×960 @4x → 2640×3840 ✅；
  HBR 横版 816×1008 @4x → 3264×4032 ✅；16:9 1280×720 @3x → 3840×2160 ✅。
- **PDF 矢量路径**（等效 4K）：v2.6 `width='6.875in'` / v2.7 `@page 8.5in 10.5in`
  照旧——矢量分辨率无关；但**内嵌位图素材**必须各自达标（源图 <4K 先走 v2.3
  `superres.sh` 4× 超分再入版），J4 会逐图反推有效 DPI。

## 三、14 个复刻档案（profile）——实测值固化

度量值全部来自 31 列语料实测（`magcorpus/mags_metrics.json`），容差按 §一。
字体授权不可得时用「替代字体」列，J1 按替代名单验收。

| profile | 字体 DNA（官方 → 替代） | 签名色（实测 fill top） | 栅格锚点（L/R 边距比例 · 栏 · 图型） |
|---|---|---|---|
| `NG` | GrosvenorBook+GeographEdit → Source Serif 4 / GT Walsheim | #FFD201 #E77741 #B9E5FA #ED1B2E | 51.6%/27.0% · 3 栏 · 拼贴流 145 图/页 |
| `BBW` | BWText+BWHaas+HelveticaNow → Tiempos / Inter | #AD6B42 #F4838D #E11A22 #DCCD45 | 38.3%/37.7% · 5 栏 · 拼贴流 23 图/页 |
| `BARRONS` | FarnhamText+B4Retina+TitlingGothicFB → Georgia / Roboto Condensed | #375177 #FDDECF #D6E5E4 | 38.7%/44.5% · 2 栏 · 克制流 cov23% |
| `SCIENCE` | MillerDaily+BentonSansCond+Akkurat → Source Serif 4 / Barlow Condensed | #253D92 #C72426 #58595B | 44.4%/44.3% · 3 栏 · 克制流 cov40% |
| `SCIAM` | MartinaPlantijn+GTAmerica → Lora / Inter | #FFCA38 #001722 #8C0C42 | 35.2%/41.6% · 2 栏 · 平衡 cov56% |
| `SCI_NEWS` | Wulkan+HelveticaNeue+WixMadefor → PT Serif / Inter | #9FBDE3 #005B91 #13254B | 30.7%/45.4% · 3 栏 · 摄影流 cov83% |
| `NEW_SCIENTIST` | TheAntiquaB+EnzoPro+MundoSans → Lora / Archivo | #CC1D4C #25AE48 #0079C1 #F36F21 | 36.1%/36.3% · 5 栏 · 平衡 cov46% |
| `VOGUE` | SaolText+FancyCutPro+PPNeueMachina → Playfair Display / Space Grotesk | 满版无矢量色块 → **降级**文字色/像素主色 | 13.5%/69.9% · 1 栏 · 满版流 cov100% |
| `COSMO` | BasisGrotesquePro+ChronicleTextG1 → Archivo / Lora | #FF447E #309156 | 16.3%/64.9% · 2 栏 · 满版流 cov98% |
| `TIME_SPECIAL` | ITCFranklinGothic+HaffnerTIME → Archivo / Playfair | 满版剧照无矢量 → **降级** | 28.3%/11.4% · display 巨字 24% · 满版流 |
| `SPECTATOR` | TimesNewRoman+FuturaPT+GoudyOldSty → Times / Jost | #001346 #C9252B #00A650 | 36.0%/36.1% · 1 栏 · 评论 cov45% |
| `OBSERVER` | SoleSerifText+PreloPro+CaslonIonic → Source Serif 4 / Work Sans | #38512F #FCE7E3 #9B005C | 43.1%/44.0% · 3 栏 · 大报 cov38% |
| `HIW` | Saira+SairaCondensed+Khand → Barlow / Khand | #CD489C #F3612A #A088C3 | 31.5%/48.1% · 3 栏 · 图解 cov60% |
| `QNWZ` | Type3 中文 227 个（不可读）→ **J1 降级**字号桶/栅格 | 双色纯黑 → **J2 降级** | 44.4%/52.5% · 2 栏 · 克制流 cov15% |

降级卡（VOGUE/TIME_SPECIAL/QNWZ）验收时 J1/J2 转 WARN 不 FAIL，J3/J4 仍硬门。

## 四、六步复刻工作流

1. **选语言**：v2.10 语料库 §六 路由表按内容类型定 profile（可叠加任一画布走向）。
2. **建画布**：按 §二 反推 DPI；HTML 画布 CSS px 用档案卡开本 pt × (96/72)，
   截图 scale = dpi/72；PDF 路径直接用 in 单位 @page。
3. **生成**：复用 v2.6 NG 竖版 / v2.7 HBR 横版 / 16:9 三条既有管线（生成器分片、
   11 页节奏、页面地图法全部照旧），只把「页面语言令牌」换成档案卡值——
   字体栈、签名色、栏数、边距比例、图密度按 §三。
4. **渲染 4K**：PNG 路径按 §二 scale 出图；PDF 路径 v2.6/v2.7 build 流水线照旧
   （遮罩 PNG 预渲染、XObject 哈希去重等坑全部沿用）。
5. **四门验收**：`journal_4k_check.py` 跑 J1–J4（对象规则见 §一：矢量 PDF 量
   J1–J3，PNG 交付另对 PNG 量 J4）；`--json` 报告随交付归档。
6. **迭代**：FAIL 项对照 §六 陷阱库修；PASS 后输出交付说明（profile 名 + 四门结果 +
   替代字体声明 + sRGB 屏显口径）。

## 六、陷阱库（实测沉淀）

1. **scale factor 与 window-size 混用截半**：加 `--force-device-scale-factor` 时
   window-size 须保持 CSS px 原值（输出像素自动放大）；再手动改 window-size 会二次放大裁切。
2. **官方字体缺失破坏 J1**：商业字体（GrosvenorBook/Saol/BWHaas）无授权——CSS 必须显式
   `@font-face` 指向替代字体，且把映射写进交付说明；J1 按替代名单匹配，裸 fallback 算 FAIL。
3. **位图源不足 4K，上采样不救**：满版摄影页源图 <3840 时先 `superres.sh` 4×（v2.3 管线）
   再入版；直接放大截图是假 4K，J4 逐图 DPI 反推会揪出来。
4. **PDF 瘦身禁用有损重压缩**：JPEG 重压会破坏位图 DPI 达标——瘦身只用 XObject 内容哈希
   去重（v2.7 已内置），页内重压缩一律不做。
5. **Type3 中文/图片型 PDF 无法建 profile**：字体名不可读（青年文摘 227 个 Type3）或整页
   位图（语料 7 刊）时，profile 标降级；新刊建档先跑语料库 §一 判型，禁止硬提取。
6. **@page 与 scale 双轨别混**：PDF（print-to-pdf + @page）与 4K PNG（screenshot + scale）
   是两条独立产物链，各过各的 J4；别指望 print-to-pdf 出 4K 位图。
7. **度量可比性靠同参数**：栏数聚类 30pt bin、字体清洗 `^[A-Z]{6}\+`、覆盖率上限 1.6——
   产物验收与语料采集必须同参数（脚本已内置）；自改度量会让 J3 失去基准。
8. **色彩空间口径**：Chrome 渲染 sRGB，与印刷 CMYK 存在色差；交付说明注明
   「sRGB 屏显复刻」，印刷需求另行校色（J2 阈值按 sRGB 标定）。

## 五、与既有能力的关系（分层不重叠）

- v2.6/v2.7 三条管线 = **画布载体**（版式骨架、build 流水线、验收三重）；
- v2.8/v2.9 = **图表内容**（38 图型 + G1–G5 门禁，图表照旧走 figure-bridge）；
- v2.10 = **页面语言**（14 档案卡的字体/色板/栅格从哪来）；
- **v2.11 = 闭环验收**（语言是否复刻到位，用同一把尺量产物说了算）。
