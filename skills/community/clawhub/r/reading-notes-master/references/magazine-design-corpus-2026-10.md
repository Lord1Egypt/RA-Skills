# 期刊设计语料库 2026-10 — 31 刊实测档案（v2.10）

> 数据来源：31 份 2026 年热点英语期刊 PDF（用户 10 月书单）程序化实测。工具 PyMuPDF 1.27.2，
> 每刊抽样 ~12 页（封面/首部/中部/尾部），提取字体族、字号分布、矢量填充色、文字色、
> 图片密度与覆盖率、文本边距、栏数近似。全部原始指标见 IMA 知识库「海外期刊杂志」归档
> （`mags_metrics.json` + `summary.md`，kb_id `ima_kb_rDzPwmRH`）。
> 适用场景：杂志版式任务（NG/HBR 三路之外的第四路语料）——先用 §六 路由表选语言，
> 再按 §二~五 档案卡取字体/色板/栅格令牌。

---

## 一、先判型：矢量型 vs 图片型 PDF（实测判据）

31 刊中 **7 份是图片型 PDF**（整页位图，无可用文字层），**24 份是矢量型**（可提取全部参数）。
拿到任何期刊 PDF，先跑一遍判据再决定解析策略：

| 判据 | 矢量型（可提取） | 图片型（仅视觉参考） |
|---|---|---|
| 字体数 | ≥5 或有真实字体名 | ≤2 且只有 Helvetica |
| 图/页 | 多图或合理分布 | 恒 1.00 且覆盖率恒 100% |
| 文字色 | 多样（≥3 色） | 恒 #808080 或空 |
| 文本左边距 | 80–360pt 有意义 | 恒 30.0pt（整页图框） |

**图片型 7 刊**：Guardian Journal、NYT Magazine、NYT Book Review、Rolling Stone（4 份整页位图，
Helvetica 占位）；Dessin et Peinture、Psychologies、Home Design（3 份高分辨率扫描，0 字体）。
**对策**：这 7 份只做视觉审美参考（构图/色彩氛围靠看图），排版参数从同类别矢量刊借。
**青年文摘**：227 个 Type3 中文字体（字体名不可读但文字层在），双色印刷极简风，可提取
字号/栅格但色板无信息量（正文纯黑 #000000）。

---

## 二、NG 系四刊字体/色板实证（修订 v2.6 手册的官方 DNA）

v2.6 的 NG 竖版手册是逆向工程，本次拿到官方字体族名与扩展色板实证：

| 刊 | 开本(pt) | 官方字体 DNA | 实测扩展色板（矢量填充 top） |
|---|---|---|---|
| NG 主刊 2026-10 | 496×720 | GrosvenorBook(正文衬线) + Geograph/GeographEdit(标题) | 黄 #FFD201 · 橙 #E77741 · 天蓝 #B9E5FA · 红 #ED1B2E · 黑白 |
| NG History 2026-08 | 595×780 | GrosvenorBook + Geograph + MinionPro | 金铜 #C9A43F · 黄 #FFD201（历史系专属金铜） |
| NG Italia 2026-06 | 495×720 | GrosvenorBook + GeographBrand | 鼠尾草绿 #A3C5B3 · 浅水蓝 #E6F4F7 · 近黑 #171717（旅行自然色） |
| NG Traveller LatAm | 652×850 | TiemposText + GeographEdit + LatamSans | 苹果绿 #94C123 · 深紫 #342382 · 红 #D52239 · 青绿 #00A787（高饱和多巴胺） |

**实证修订**：① v2.6 用 `--din`/serif/sans 三栈模拟——现在可指名替代字体：Grosvenor→
`Source Serif 4 / Tiempos`，Geograph→`GT Walsheim / Regional`。② NG 不是只有黄盒四色：
主刊辅助橙 #E77741 与天蓝 #B9E5FA 可做图注/标签，History 系配金铜 #C9A43F，Traveller 系
放开用高饱和四色。③ 图片密度之王是 NG 主刊（**145 图/页**——大量小图拼贴页），
Traveller 覆盖率 81%（满版摄影流），Italia 90%。

## 三、财经系：Bloomberg/MoneyWeek/Barron's

| 刊 | 开本 | 字体 DNA | 色板 | 栅格与图片 |
|---|---|---|---|---|
| Bloomberg Businessweek | 568×757 | BWText + BWHaasText + HelveticaNowDisplay（自有字体家族） | 焦糖棕 #AD6B42(146次!) · 粉 #F4838D · 红 #E11A22 · 芥黄 #DCCD45 | **5 栏 · 23.3 图/页（全语料密度第一）**· 覆盖 68% |
| MoneyWeek | 595×842 | SabonLTStd(衬线正文) + UniversLTPro(瑞士无衬线) | 红 #E31F27 强调 + 黑白 | 1 栏长文 · 瑞士经典搭 |
| Barron's | 756×765 近方报 | FarnhamText + B4Retina + TitlingGothicFB（46 字体，全语料最多） | 钢蓝 #375177 · 蜜桃 #FDDECF · 冰蓝 #D6E5E4 · 藏青 #1B3370（柔和财经色系） | 2 栏 · 图覆盖仅 23%（文字密集型报纸） |

**取用**：商业读书笔记要杂志感 → BBW 语言（多栏多图大色块）；要克制权威 → Barron's
柔和四色 + 宽边距（L292pt）。

## 四、科研系：Science×2/Sci Am/Sci News/New Scientist

| 刊 | 字体 DNA | 色板 | 栅格特征 |
|---|---|---|---|
| Science（AAAS） | MillerDaily(正文衬线) + BentonSansCond(窄无衬线标题) + Akkurat | 学术蓝 #204197/#2C50A3 · 灰 #58595B | **3 栏报纸式** · 宽边距 264–289pt · 图覆盖 40–50% |
| Scientific American | MartinaPlantijn(衬线) + GT America + Apres | 黄点 #FFCA38 · 近黑蓝 #001722 | 2 栏 · 白底大留白 |
| Science News | Wulkan(圆润衬线) + HelveticaNeue + Wix Madefor | 浅蓝块 #9FBDE3(141次) · 深蓝 #005B91 · 红 #EF3F3B | 3 栏 · 图覆盖 83%（科普摄影流） |
| New Scientist | TheAntiquaB(正文) + EnzoPro + MundoSans | **品红 #CC1D4C(200次大色块!)** · 绿 #25AE48 · 橙 #F36F21 · 天蓝 #0079C1 | 5 栏 · 多巴胺科普 |

**取用**：科研笔记要严肃 → Science 语言（Miller/Benton + 学术蓝 + 3 栏）；要年轻流量感
→ New Scientist（品红大色块是它的视觉签名）；平衡 → SciAm（白底留白 + 一点黄）。
v2.8 科研图表系统（38 图型）配 Science/SciAm 色板即得期刊级学术版面。

## 五、生活方式/时尚/设计/科普特辑/中文

| 刊 | 字体 DNA | 色板 | 特征 |
|---|---|---|---|
| Cosmo UK | BasisGrotesque + Chronicle 三栈 | 荧光粉 #FF447E · 绿 #309156 | L92pt 大胆出血 · 6.1 图/页 · 青年女刊张力 |
| Vogue Singapore | Saol Display/Saol Text + FancyCutPro(装饰) + PP Neue Machina(几何) | 橄榄绿点 #94A741 · 近黑 | L84pt 极窄边距 · 满版大图 · 时装精三字体混搭 |
| Healthy Food Guide | AvenirNext + TradeGothic + Archer | 青 #68B3BB · 橙 #D76F2C（食物色） | 3 栏食谱网格 |
| Living Without Inflammation | EloquiaText + Chronicle 系特辑 | 番茄红 #F0493E · 深蓝 #0B4D91 | 健康特辑：衬线正文+双强调色 |
| How It Works (Claude 特辑) | Saira/SairaCondensed + Khand + Kanit（伸展无衬线家族） | 品红 #CD489C · 橙 #F3612A · 紫 #A088C3 · 浅灰蓝 #A7B2B7 | **特辑多巴胺**· 3 栏 · 图解密集 3.8 图/页 · 116p 单题深挖 |
| The Art of Design | KontrapunktBob + Montserrat + SourceSans | 青 #148C9F | 北欧克制设计刊 |
| 100 Crochet Tiles | Gotham 全家桶(Light 主体) + JustLovely 斜体 | 中性灰阶 #EEE/#EA/#EF(大面积) + 黄 #FFC700 · 冰蓝 #BCE5E7 | 工艺图鉴：浅灰底 + 亮点缀 · 2 栏 |
| Time 正刊 | HaffnerTIME + ITC FranklinGothic + AktivGroteskEx | 红 #CF2226 · 近黑 #221F1D | 新闻周刊权威红框 |
| Time Spider-Man 特辑 | ITC FranklinGothic + HaffnerTIME | 红 #E6161F(842次) · 黑 #111011 | **display 24%**（特辑巨型标题党）· 满版剧照 |
| The Observer | SoleSerifText + PreloPro + CaslonIonic | 洋红 #9B005C · 珊瑚 #EA8187 · 深绿 #38512F | 820×1018 大报 · 3 栏 · 12.3 图/页 |
| The Spectator | Times + FuturaPT + GoudyOldSty 复古混搭 | 深海军蓝 #001346(200次) · 红 #C9252B · 绿 #00A650 | 评论刊：复古衬线 + 大蓝块 |
| 青年文摘 | Type3 中文 227 个（不可读名） | 纯黑正文 | 中文双色传统排版 · 图仅 0.25/页 |

## 六、按任务路由（读书笔记 → 期刊语言映射）

| 你的笔记场景 | 借用语言 | 关键令牌 |
|---|---|---|
| 自然/历史/摄影书 | NG 系（v2.6 手册） | Grosvenor/Geograph + 黄盒 + §二 扩展色 |
| 商业书/公司案例 | Bloomberg Businessweek | 5 栏 · 焦糖棕大色块 · 高图密度 |
| 财报解读/价值投资 | Barron's | 柔和四色（钢蓝/蜜桃/冰蓝）· 宽边距 · 文字主导 |
| 学术论文笔记 | Science 或 SciAm | Miller+学术蓝 3 栏 / 白底留白+黄点 |
| 科普书/前沿科技 | New Scientist 或 How It Works | 品红大色块 / 伸展无衬线+紫品红 |
| 生活方式/健康书 | Healthy Food / Living Without | 食物双色 / 番茄红+深蓝 |
| 时尚/摄影集 | Vogue / Cosmo | Saol 三栈极窄边距 / 荧光粉出血 |
| 人物特辑/单题深挖 | Time 特辑 | display 24% 巨型标题 + 满版图 |
| 评论/杂文集 | The Spectator / Observer | 复古衬线+海军蓝 / 大报 3 栏 |
| 中文读物 | 青年文摘 | 双色极简 · 纯黑正文 |

## 七、跨刊实证设计定律（24 刊矢量语料归纳）

1. **正文主导律**：body+caption 占字符 90–100% 是所有刊的常态；display 巨字仅出现在
   封面/章扉/特辑（唯一例外 Spider-Man 特辑 display 24%）。→ 杂志版式不要炫技大字，
   每期 2–4 个 display 页即可。
2. **强调色预算律**：每刊强调色 1–2 个且用量克制（文字色第 2 名普遍 <4%）：NG 黄 401/15k、
   Time 红 CF2226 仅 14 次矢量、SciAm 黄 11 次。→ 单页强调色 ≤1，整期 ≤2。
3. **大色块签名律**：品牌记忆点来自「单一高饱和色的大面积重复」：New Scientist 品红 200 次、
   Spectator 海军蓝 200 次、BBW 焦糖棕 146 次、Science News 浅蓝 141 次、Observer 近黑 264 次。
   → 想要品牌感，选定一个签名色反复出现在色块/边条/底纹。
4. **字体家族三栈律**：24 刊全部是「衬线正文 + 无衬线标题 + （可选）display 装饰」三栈，
   极少超过 3 族（BBW/NG 拥有自有字体家族但内部仍三角色）。→ 自制版式沿用三栈，
   拒绝四族混搭。
5. **栅格分野律**：财经/科普 3–5 栏高密度流（BBW 5 栏、NS 5 栏、Science 3 栏）；
   时尚/评论 1 栏长文流（Vogue/Spectator/MoneyWeek）。→ 栏数由内容类型决定，不由美学决定。
6. **边距个性律**：图片主导刊边距窄（Vogue 84pt、Cosmo 92pt、Time 143pt），文字主导刊
   边距宽（Barron's 292pt、Science 264–289pt、Observer 354pt）。→ 先定图文比再定边距。
7. **图片密度分型律**：拼贴流（BBW 23 图/页、NG 主刊 145 图/页）vs 满版流（Vogue/Cosmo
   覆盖 ~100%）vs 克制流（Barron's 覆盖 23%）。三型对应信息图鉴 / 画册 / 评论三种内容。

## 八、IMA 知识库挂接（生产闭环）

- 知识库「海外期刊杂志」（31 份 PDF 全量归档，kb_id `ima_kb_rDzPwmRH`）。
- 需要**回看某刊原文页面**时：用 IMA OpenAPI `search_knowledge`（query=刊名）→
  `get_media_info` 取原文 URL。
- 升级语料同仓归档：`magcorpus/mags_metrics.json`（31 刊原始指标）、`magcorpus/summary.md`
  （汇总表）、本文件（设计语言档案）。
- 新增期刊时复跑 `magcorpus/analyze_mags.py` 即可增量建档，判型先行（§一）。
