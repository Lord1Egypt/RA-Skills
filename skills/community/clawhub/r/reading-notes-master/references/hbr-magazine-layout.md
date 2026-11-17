# HBR 商业杂志横版版式手册（v2.7 新增）

> 从 88 页《哈佛商业评论 2025 年度精选》实战中逆向沉淀（原稿 12 期 2,291 页 → 88 页 = 单期均页 46%）。
> 全部参数经真实交付验证：PDF 88 页 / 11.7MB 三重验收通过（0 溢出 / 0 空页 / MediaBox 恒定），
> PPTX 88 页 16:9 结构 0 越界 + LibreOffice 实渲染 0 溢出重叠。
> 配套资产：`templates/hbr-magazine/mag.css`（设计系统）、`generator-template.py`（12 页型构建器）、
> `build-template.py`（六步流水线）、`scrim/`（4 遮罩 PNG + 生成脚本）。

## 1. 何时用横版商业杂志（三路版式决策）

Step 0.5 的版式判断从"竖版 or 16:9"升级为三选一：

| 信号 | 16:9 幻灯片 | NG 竖版杂志 | **HBR 横版杂志** |
|---|---|---|---|
| 原书类型 | 方法论/商业/数据 | 摄影集/自然/历史/人物 | **商业期刊/杂志文集/多主题合集** |
| 图片资产 | 少，靠器型撑 | 充足，图即内容 | **中等：封面/特写/图表/照片穿插** |
| 内容结构 | 单一主线 | 单一叙事弧 | **多主题分章，每主题独立成篇** |
| 阅读场景 | 投屏演示 | 打印翻阅/画廊 | **打印翻阅 + 屏幕精读** |
| 心理预期 | "汇报" | "杂志特辑" | **"原刊复刻/年度精选"** |

横版核心心智：**页面=杂志页**。三类页面节奏交替——全出血页（封面/章隔/照片/金句）、
信息页（大图表/统计/总览）、文章页（编辑开篇/文本）。每章 11 页一个完整节奏循环，就是杂志感。

## 2. 版式参数（全部实测锚定）

```
画布      612 × 756 pt  =  8.5 × 10.5 in（美式杂志开本，NG 竖版的横转）
页面      .page { width:612pt; height:756pt; position:relative; overflow:hidden; margin:16pt auto }
          屏幕预览时居中带投影；@media print 去 margin/投影出精确纸张
打印      @page { size: 8.5in 10.5in; margin: 0 }   ← margin:0 是全出血的前提
出血      .page.fullbleed { padding: 0 }，背景图 absolute 铺满
安全边距 内容页 padding: 44pt 60pt 40pt；folio 顶 34pt / pageno 底 24pt
字体      --sans: GTAmerica→Helvetica Neue→PingFang SC→Arial（展示/正文）
          --serif: Tiempos→Georgia→Songti SC（导语/图表说明）
          Chrome 打印不嵌字体（系统引用），PDF 体积无字体成本
```

**关键骨架**（勿动）：
```css
.page { width: 612pt; height: 756pt; background: var(--paper);
        position: relative; overflow: hidden; margin: 16pt auto; }
.page.fullbleed { padding: 0; }
.mag-ed { display: flex; }                    /* 非对称编辑页 */
.mag-ed .me-photo { width: 310pt; flex: none; } /* 照片栏固定宽，文字栏 flex:1 吃余量 */
.mag-ed .me-body { flex: 1; min-width: 0; }     /* min-width:0 防 flex 子项溢出 */
.mt-text { column-count: 2; column-gap: 24pt; } /* 文本页双栏 */
```

## 3. 设计令牌（改 `:root` 换肤）

| 层 | 变量 | HBR 默认值 | 说明 |
|---|---|---|---|
| 刊名红 | `--red` | `#E41824` | 刊头/kicker/统计数字/分隔线（中文版实测众数） |
| 暗砖红 | `--brick` | `#842418` | 英文版大标题变体 |
| 橙金 | `--artgold` | `#F09C18` | 特写压图标题/金句来源 |
| 珊瑚红 | `--coral` | `#F37060` | 数据高亮 |
| 墨色 | `--ink` | `#231F20` | 标题/边线/黑底 |
| 暖灰 | `--gray` `--gray-lt` | `#6E6A67` `#A7A9AC` | 辅助文字 |
| 细线 | `--rule` | `#D8D5D0` | 发丝线/双栏分隔 |
| 米色 | `--cream` | `#F4F1EA` | 图表舞台底 |
| 纸色 | `--paper` | `#FFFFFF` | 页面底 |

**换肤纪律**：只改刊名 DNA 四色（`--red/--artgold/--ink/--cream`）+ 两个字体栈；
其余（页面骨架/页型组件/遮罩曲线）不用动。换成别的刊物（如《财新》《经济学人》）
只需替换四色 + 刊名文案。

## 4. 十二类页面模板（HTML 骨架速查）

**① 封面 `.mag-cover`**：满版图 + mc-scrim 渐变 + 刊名 masthead（左中文右英文三行）+ 年份徽章
（描边胶囊）+ 44pt 大标题 + 红色分隔线 + 导语 + 底部 6 连封面条 `.mc-strip/.mc-cell` + 页脚。

**② 章隔页 `.mag-div`**：满版图 + md-scrim + 左上 CHAPTER 标签 + **150pt 巨号章节数字** +
右侧竖排英文 `writing-mode: vertical-rl` + 底部 34pt 章题 + 英文小字 + 衬线导语。

**③ 编辑开篇 `.mag-ed`**：非对称双栏——照片栏 310pt（me-photo，底部深色说明条 me-pcap）+
文字栏（kicker + 23pt 标题 + 衬线 deck + 红色统计数字条 me-stat + 8.2pt 双栏正文 me-text）。
`me-flip` 翻面（照片在右），每章第二篇用，避免连续两页同构。

**④ 整页大图表 `.mag-chart`**：kicker + 26pt 标题 + 衬线副题 + **图表舞台**
（`.mch-stage` 位图版 `background-size: contain` / `.mch-svgstage` SVG 版）+
底部解读框（黑底白字"解读"标签）+ 资料来源。原刊真实图表直接提取复用。

**⑤ 巨型统计 `.mag-stat`**：照片栏 208pt + **100pt 统计数字**（红色单位后缀）+
描述 + 红线 + 标题 + 正文。数字必须进这页型，禁止埋段落。

**⑥ 大字文本 `.mag-text`**：kicker + 22pt 标题 + 衬线导语（左侧红色竖线 mt-lead）+
**双栏正文**（column-count:2，8.2pt/1.86，可内嵌 pullquote/keybox/statrow）。

**⑦ 照片特写 `.mag-photo`**：满版图 + mp-scrim + 底部金色 kicker + 衬线说明（≤2 行）。

**⑧ 金句页 `.mag-quote`**：满版图 + mq-scrim（0.66 平铺压暗）+ 居中 72pt 红色引号 +
24pt 金句 + 金色来源 + 衬线注脚。

**⑨ 目录 `.mag-toc`**：分组细线表——组名（红色 10.5pt）+ 行（方点 + 标题 + 出处右对齐 +
页码）。45 条以上必须分两页双栏平衡。

**⑩ 期号总览 `.mag-imap`**：4×3 卡片网格——封面图 62pt + 期号（HOT 红标）+ 主题 + 描述 + 标签。
**12 张是上限**（再多行高超页）。

另备 SVG 三组件（`generator-template.py` 内置）：`svg_bigbar` 大横幅条形图（高亮行刊名红）、
`svg_bigstat_ring` 巨型圆环、`svg_steps_big` 大版步骤带（暗色/浅色双模）。

## 5. 章节节奏与页面地图法（先画地图，后写页面）

**页数控制**：成品页数 = 原书 **1/3 ~ 1/2**。文集按"单期均页"口径：
12 期 2,291 页 → 单期均 191 页 → 1/3=64 页、1/2=96 页。88 页 = 46% 落在窗口内。

**每章 11 页固定节奏**（实测零溢出，照抄）：
```
P+01  章隔页        全出血 + 150pt 巨号
P+02  编辑开篇      非对称图文（照片在左）
P+03  整页大图表    原刊图表 / SVG 重绘
P+04  巨型统计      100pt 数字
P+05  文本页①      双栏 + 导语
P+06  文本页②      双栏
P+07  文本页③      双栏
P+08  照片特写      满版 + 小注
P+09  金句页        满版 + 居中金句
P+10  编辑开篇②     me-flip 翻面（照片在右）
P+11  文本页④      双栏收尾
```

**地图样例**（88 页，7 章 + 前置 + 后置）：
```
P01–07  前置：封面 / 目录×2 / 12 期总览 / 方法口径 / 金句 / 金句墙
P08–18  PART 01  章隔 + 11 页节奏
P19–29  PART 02  …（每章 11 页，章隔页是章内第 1 页）
P30–84  PART 03–07
P85–88  后置附录：行动清单 / 全年索引 / 设计系统 / 关于本书
```

规则：每章以章隔页开头；每章 2 篇编辑开篇必须一左一右翻面；器型不相邻重复
（两篇编辑页之间至少隔 3 页）；照片资产全书不重复（封面条/总览卡/章隔/编辑/统计/照片/金句
各自分资产，7 章 × 8 张 ≈ 56 张 + 前置 12 张封面）；每页 `<!-- P42 主题 -->` 注释，
收尾索引页靠注释回填页码。

## 6. 生成器拆分模式（防 Write 截断，硬纪律）

88 页 ≈ 106KB HTML，**必须**用 Python 生成器分片生产：
```
gen_mag_a1.py → P01–P13   _mag_a1.html   （每片 9~13 页）
gen_mag_a2.py → P14–P23   _mag_a2.html
gen_mag_b1.py → P24–P32   _mag_b1.html
gen_mag_b2.py → P33–P41   _mag_b2.html
gen_mag_c1.py → P42–P50   _mag_c1.html
gen_mag_c2.py → P51–P60   _mag_c2.html
gen_mag_d1.py → P61–P77   _mag_d1.html
gen_mag_d2.py → P78–P88   _mag_d2.html
```

- **单片 ≤20KB**（实测 9~10 页 ≈ 18KB 安全）。超了对半再拆。
- 每片复制 `generator-template.py`：CONFIG（刊名/资产目录）+ 12 页型函数 +
  `P=[]` + N 个 `P.append(...)` + 尾部 `write_text('\n'.join(P))` + `print('xx ok', len(P))`。
- 用**系统 python3** 跑生成器（纯标准库）；build 才用带 Chrome 的环境。
- 页码：生成器里写**临时页码**，build 前由统一 `renumber()` 按物理页序重写
  （目录页码则由 build 时按标题匹配自动计算，45 条目级校验）。

## 7. build 流水线（六步，`build-template.py` 全内置）

```
① 合并   regex 拼接 8 片段 → full.html（**CSS 必须内联**，见踩坑 #3）+ assert 页数
② 渲染   Chrome headless：--headless=new --user-data-dir=<全新临时目录> --no-sandbox
         --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage
         --no-pdf-header-footer --virtual-time-budget=20000 file://<绝对路径>
③ 验收   pymupdf 三重：MediaBox 612×756 恒定 / 逐页文本 span bbox 零溢出 / 零空页
         （空页=无文本且无 drawings 且无 images；照片页无文本属正常，按图形页豁免）
④ 瘦身   XObject 内容哈希去重（Chrome 每页各嵌一份背景图）+ garbage=4 + clean
         实测 18.3MB → 11.7MB；有损重压缩收益仅 5%，不做
⑤ PPTX   从 full.html 解析页型同源重建 16:9（python-pptx，裁切贴图 + 页型分派）
⑥ 打包   delivery/：pdf + pptx + notes.html + assets/
```

**PPTX 同源要点**（88 页零越界实测）：照片用 `add_picture` + `crop_*` 按目标框宽高比裁切；
kicker 文本框宽度 **clamp 到页宽**；总览网格 **4 列×3 行**；编辑页翻面几何
（照片 6.4in + 文字 5.85in，flip 时文字在左 x=0.55）；图表舞台 10.5×3.6in 居中。
PPTX 还需 LibreOffice 实渲染验收（边缘溢出 + 文本块重叠）。

## 8. 踩坑库（每条都是实测血泪）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | PDF 18MB+， Pattern 对象 76 个、图像对象 138 个 | **CSS linear-gradient 遮罩叠在背景照片上**，Chrome 把照片光栅化进平铺 Pattern（未压缩位图，×2.4） | 渐变预渲染成 PNG（`scrim/make_scrims.py`，8×1024 带 alpha，~280B/个），CSS 改 `background-image + 100% 100% + no-repeat` |
| 2 | 同样出现 Pattern（40 个） | 背景类缺 `background-repeat: no-repeat`（`.me-photo/.ms-photo/.mch-stage/.im-img/.mc-cell`）；`contain` 尺寸还会真实平铺出视觉 artifact | 所有背景图类一律补 `no-repeat` |
| 3 | 改 CSS 后重新渲染，PDF 字节级不变 | ① full.html 是**构建时内联 CSS 的快照**，改 style.css 不重跑 build_full 等于没改；② Chrome 默认 profile **磁盘缓存 file:// 子资源** | 改 CSS 必须重跑生成 full.html；渲染加 `--user-data-dir=` 全新临时目录 |
| 4 | PPTX 14 处 shape 越界（右缘外 0.7~2.8in） | kicker() 固定 9in 宽文本框，位于页面右侧时冲出页面 | 宽度 clamp：`max(1in, 页宽 - x - 0.2in)` |
| 5 | PPTX 总览页第 4 行 y=9.73in 远超 7.5in 页高 | issuemap 3 列×4 行，起始 y=2.2in + 3 行高 | 改 **4 列×3 行**（cw 2.90in / chh 1.52in / 行距 0.14in） |
| 6 | PDF 瘦身只省 0.4MB | pymupdf `garbage=4` 清不掉 Chrome 的 Pattern 内图像（被 Pattern 对象引用，"看起来"可达） | 先修 #1/#2 消灭 Pattern，再对页面直连 XObject 做内容哈希去重 |
| 7 | 内嵌 JPEG q76→q72 重压缩只省 5% | 照片内容已在编码器效率曲线附近，且 Chrome 原样直通源 JPEG | 不做页内有损重压缩；要瘦身回到源头——源图预压缩（长边 1700px / q76 / progressive） |
| 8 | 照片页/金句页渲染成"灰色渐变空页" | 资产路径指错目录（`use/` vs `use2/`），背景图加载失败只剩遮罩 | 构建前 grep 全部 `url()` 引用校验文件存在；`ph()/cov()` 单一出处管路径 |

## 9. 与既有工作流的对接

- **Step 0/1/2/3 不变**：设计智能前置、原型选择、思维模型路由照旧；横版只接管
  **Step 4 排页 + Step 5 导出**。书籍→杂志的转译发生在 Step 4：把"章节"升级为"PART"，
  每 PART 套 11 页节奏。
- **版式决策树**（Step 0.5 三选一）：摄影集/自然/历史/人物 → NG 竖版；
  商业期刊/杂志文集/多主题合集 → **HBR 横版**；单主线方法论投屏 → 16:9。
- 器型对照：统计页↔大数字卡、大图表页↔整页 chartbox、期号总览↔卡片网格、
  章隔页↔篇章过渡、金句页↔pullquote 特写。**横版不用的器型**：象限/漏斗（杂志语境违和），
  环形/条形图进 SVG 大图表页。
- 文字预算加严：文本页双栏 ≤400 字、编辑页 ≤150 字、图解页 ≤120 字（本 skill 基线不变）；
  照片/金句页 ≤80 字。**超页先砍文字页，不砍全出血页**。
- 文生图横版化：封面/章隔/照片/金句出 **横构图 1600×1000**（prompt 加
  `landscape orientation, magazine full-bleed photography, editorial`）；
  图表类资产一律从原刊提取或 SVG 重绘，不生成。
- 交付物命名与多格式导出沿用 `templates/output-pipelines.md`，PDF 页面尺寸 8.5×10.5in，
  PPTX 16:9（13.333×7.5in）。

## 10. 快速启动清单

1. `cp -r templates/hbr-magazine/ <项目>/`，`scrim/` 连 PNG 一起拷（或跑 `make_scrims.py` 再生）
2. 资产预压缩进 `assets/mag/`（长边 ≤1700px / JPEG q76 / progressive；封面条与总览卡用小图另存一套）
3. 画页面地图（§5）：前置 + N 章×11 + 后置，每页标页型与资产名
4. 每片段复制 `generator-template.py` 改 CONFIG 与中段 `P.append`，跑生成器核对页数
5. `cp build-template.py → build_mag.py` 改 CONFIG 六参数 → 跑
6. 三重验收 + PPTX LibreOffice 实渲染全清零 → `delivery/` present
