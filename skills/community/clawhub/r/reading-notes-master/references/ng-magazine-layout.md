# NG 杂志竖版版式手册（v2.6 新增）

> 从 148 页摄影集《Big Cats & African Wildlife》60 页出版级竖版读书笔记实战中逆向沉淀。
> 全部参数经真实交付验证（PDF 60 页 / PPTX 60 页 / 11.1MB，0 破图 0 裁切 0 挤压）。
> 配套资产：`templates/ng-magazine/mag.css`（完整设计系统）、`build-template.py`（流水线）、`generator-template.py`（生成器骨架）。

## 1. 何时用竖版（vs 默认 16:9）

| 信号 | 选 16:9 幻灯片 | 选 NG 竖版杂志 |
|---|---|---|
| 原书类型 | 方法论/商业/数据 | 摄影集/自然/历史/人物/艺术 |
| 图片资产 | 少，靠器型撑 | 充足，图即内容 |
| 阅读场景 | 投屏演示 | 打印/翻阅/画廊式浏览 |
| 心理预期 | "汇报" | "杂志特辑" |

竖版核心心智：**页面=杂志页**。有"文章页"（标题+导语+双栏正文+图注）、有"信息页"（statgrid/时间轴）、有"摄影页"（满版出血）。三种页面节奏交替，就是杂志感。

## 2. 版式参数（全部实测锚定）

```
画布      660 × 960 px  =  495 × 720 pt  =  6.875 × 10 in（16:9 的竖转，A4 近似比例）
截图      viewport 660×960 + device_scale_factor=2 → 1320×1920 @2x
左右边距  56px（正文安全区）
眉区      .hd 高 34px（absolute top:0），内容区 .bd top:46px
脚区      .ft 高 34px 黑条，.bd bottom:44px
双栏      column-count:2, gap:29px, 13px/1.72 衬线, 首字下沉 57px
```

**关键骨架**（магic 三段，勿动）：
```css
.page{width:660px;height:960px;position:relative;overflow:hidden;background:var(--paper)}
.bd{position:absolute;top:46px;bottom:44px;left:0;right:0;padding:14px 56px 10px;
    display:flex;flex-direction:column;min-height:0}
.fullbleed .cap{position:absolute;left:0;right:0;bottom:0;padding:0 56px 40px}
```
`.bd` 是 flex 列容器 → 器型区加 `flex:1;min-height:0` 即可自动吃满余量；溢出由 build 校验兜底。

## 3. 设计令牌（改 `:root` 换肤）

| 层 | 变量 | 默认值（NG 黄盒经典） |
|---|---|---|
| 主墨 | `--ink` | `#231F20`（黑条/标题/边线） |
| 主题黄 | `--yellow` | `#FFD201`（黄星/kicker 方块/下划/章扉号） |
| 辅助色 | `--gold` `--bronze` `--wine` `--red` | `#BB9903 #A77341 #922123 #D22229` |
| 纸色三阶 | `--paper --paper2 --paper3` | `#F4EDE3 #F0EBE5 #F9F4EE`（.page/.alt/.paper3） |
| 图表色 | `--sand --sage --olive --amber --blue` | 沙金/鼠尾草绿/橄榄/琥珀/蓝 |
| 线与暗字 | `--line --line-soft --dim` | `rgba(35,31,32,.20/.11/.58)` |
| 字体三栈 | `--serif --sans --din` | 宋体族(标题/正文)/苹方族(标签/UI)/DIN 族(数字/页码) |

**字体纪律**：标题与正文一律衬线（杂志 DNA）；`.lab/.kicker/byline` 一律 sans 大写+宽字距（.16~.30em）；一切数字（stat/页码/年份/价格）一律 `--din`。换肤只换色板五件套 + serif，其余不用动。

## 4. 十二类页面模板（HTML 骨架速查）

**① 封面 `.cover`**：满版图 + 黄框 `.frame` + 白字刊名 masthead + 红章 over + 55px 大标题 + coverline 三关键词。

**② 黑底目录 `.tocpage`**：`.toc-item` = DIN 大号章号(黄) + 章题 + 页码右对齐竖线分隔。

**③ 章扉 `.chapter`**：满版图 + 左深右浅横向 veil + `part-no`(64px DIN 黄号+3px 黄线+lab) + 52px 衬线白标题 + poet 引诗 + meta。

**④ 满版摄影页 `.fullbleed`**：图 absolute inset0 cover + 上下双段 veil + `.cap`（黄标签 ct + 26px 白题 + 12.5px 说明 + csrc）+ 底部 folio 半透明黑条。

**⑤ 文章页**：`kicker(黄方块) → art-title 33px(内嵌 .yl 黄底划词/.rd 红词) → deck 导语 → col2 双栏(dropcap 首字下沉 + crosshead 小节 + sidebar-note 黑底侧栏) → pullquote 粗顶线引文`。文字量大的章节用这页型，全书 ≤3 页。

**⑥ 解剖标注页 `.anat`**：左 fig 白底图盒(1.18fr) + 右 pts 五点列（`.pt` = 黑方块 DIN 序号 + h5 + p）。配 FIG.06 式 figcap。天然科普感，适合"机制/结构/流程分解"。

**⑦ 大数字页 `.statgrid`**：c2/c3/c4 网格，`.stat` 白卡 4px 顶线(.y/.r/.w/.g 分色)，`.num` 44px DIN。数字一律进 stat，禁止埋段落。

**⑧ 图鉴/条目页 `.entrygrid`**：c2/c3，顶 2px 黑线，`.entry` = 24px DIN 金色序号 + h4 大写眉 + h3 衬线题 + p。Field-guide 变体 `.fg-row`（五列：名/域/重量/等级/状态色条）适合物种/产品谱系。

**⑨ 时间轴 `.tl`**：3px 黑轴 + 黄点黑边 dot + 19px DIN 年份 + 10px 事件。`grid-template-columns:repeat(n,1fr)` 均分。适合兴衰史/崩塌史。

**⑩ 价格条 `.pricerow`**：128px 名 + 弹性条(.bar 默认沙/.v 红/.y 黄/.k 黑) + 110px DIN 值。极小值给 `min-width:4px` 并在注里声明"仅示最小可见宽度"。

**⑪ 思维导图 `.mindmap`**：mm-root 黑条全宽(题+黄小字) + 2 列 mm-branch 白卡(顶线五色 .v2~.v5 分支) + leaf 方点列表。收尾页用。

**⑫ 金句页 `.qpage`**：黑底 150px 黄引号 + 30px 衬线金句(关键词 .yl 黄) + qsrc。低像素方差属设计使然，质检时豁免。

另备：**半版图带 `.band-photo`(46%)+.band-body**、**对比双栏 `.duel`**、**图表盒 `.chartbox`(白卡+cb-title+chart+src)**、**阅读地图**（复用 entrygrid，原书页码→笔记页码映射表）、**封底 `.fullbleed`**（居中 cap + Thank You）。

## 5. 页面地图法（先画地图，后写页面）

**页数控制**：成品页数 = 原书页数的 **1/3 ~ 1/2**（148 页 → 60 页 = 40.5%）。低于 1/3 丢内容，高于 1/2 变摘抄。

**地图样例**（60 页，每 PART 8~14 页）：
```
P01–05  前置：封面/出版语/黑底目录/作者/为什么读
P06–13  PART I   章扉 + 6~7 内容页
P14–23  PART II
P24–32  PART III
P33–41  PART IV
P42–55  PART V（最大章可拆两个生成器）
P56–60  收尾：满版尾声/思维导图/金句页/阅读地图/封底
```

规则：每个 PART 以章扉开头；内容页按"信息页:文章页 ≈ 8:2"配比；每 PART 至少 1 满版摄影页；器型不相邻重复；`<!-- P42 母系社会 -->` 式注释标每页主题，收尾"阅读地图"页靠注释回填页码。

## 6. 生成器拆分模式（防 Write 截断，硬纪律）

60 页 ≈ 500KB HTML，**必须**用 Python 生成器分片生产：

```
gen_mag_a1.py → P01–P13   _mag_a.html   （每片 9~13 页）
gen_mag_a2.py → P14–P23   _mag_a2.html
gen_mag_b1.py → P24–P32   _mag_b1.html
gen_mag_b2.py → P33–P41   _mag_b2.html
gen_mag_c1.py → P42–P50   _mag_c1.html
gen_mag_c2.py → P51–P60   _mag_c2.html
```

- **单片 ≤20KB**（实测 9~10 页 ≈ 18KB 安全）。写之前估体量，超了对半再拆。
- 每片 = 三函数头（`HD/FT/FOLIO`，见 `generator-template.py`）+ `P=[]` + N 个 `P.append(...)` + 尾部 `write_text('\n'.join(P))` + `print('xx ok', len(P))`。
- HD/FT 在 `<section class="page">` **外**（absolute 定位）；金句页/满版页不用 HD/FT，用 FOLIO 或 `.folio` 条。
- 用**运行环境的系统 python3** 跑生成器（纯标准库）；build 才用带 playwright 的环境。

## 7. build 流水线（六步，`build-template.py` 全内置）

```
① 合并   regex <section class="page.*?</section> 拼接 6 片段 → assert 页数
② 校验   Playwright evaluate 三查：破图(naturalWidth=0) / 裁切(getBoundingClientRect 走 DOM 树,
         跳过 SVG DEFS|STYLE|… 用 toUpperCase) / 挤压(.bd 等容器 scrollHeight>clientHeight+3)
③ 截图   逐 .page element.screenshot → v2_png/p%02d.png (1320×1920)
④ PDF    pg.pdf(width='6.875in', height='10in', print_background=True,
         prefer_css_page_size=False, margin 全 0)   ← 单位必须 in，pt 会报解析错
⑤ PPTX   6.875×10in 母版 + JPEG q87 重建贴图（PNG 44MB→JPEG 11MB，-75%）
⑥ 打包   交付目录：pdf/pptx/notes.html(改 assets 相对路径)/mag.css/assets/
```

追加 **PIL 方差空白页检测**（灰度 std<18 标记人工复核；黑底金句页豁免）。

## 8. 踩坑库（每条都是实测血泪）

| # | 症状 | 根因 | 修复 |
|---|---|---|---|
| 1 | `Failed to parse parameter value: 495pt` | Playwright `pdf()` 只认 in/cm/mm/px，**不认 pt** | `width='6.875in', height='10in'`（495pt=6.875in 换算） |
| 2 | SVG 图表被误报 16 条"裁切"（负偏移） | `<defs>/<style>` 等不可渲染元素 getBoundingClientRect 异常；且 SVG 元素 `tagName` 是**小写**，大写黑名单匹配不上 | SKIP 黑名单 + `c.tagName.toUpperCase()` |
| 3 | 沙箱内 `PermissionError: [EEXIST] mkdir` | WorkBuddy sitecustomize shim 拦截 `mkdir(exist_ok=True)` 对已存在目录误报 | `if not d.exists(): d.mkdir(parents=True)` |
| 4 | P37 broken-img | 图片相对路径写错目录（`../assets/illustrations/` 实际在 `../assets/mag/`） | 生成器里 grep 校验全部 `src=` 路径存在再跑 build |
| 5 | PPTX 44MB 发不动 | PNG 贴图无压缩 | PIL 转 JPEG quality=87 optimize 重建，体积 −75% |
| 6 | 内容被脚区吃掉 | 器型区没给 `flex:1;min-height:0`，flex 列被绝对定位脚区遮蔽 | 所有弹性容器带 `min-height:0`；靠②校验兜底 |

## 9. 与 16:9 工作流的对接

- **Step 0/1/2/3 不变**：设计智能前置、原型选择、思维模型路由照旧；竖版只接管 **Step 4 排页 + Step 5 导出**。
- 器型对照：statgrid↔大数字卡、entrygrid↔编号卡、tl↔时间线、anat↔机制图、duel↔对比、mindmap↔思维导图、pricerow↔条形对比。**竖版不用的器型**：象限/漏斗/环形（杂志语境里违和）。
- 文字预算加严：文章页双栏 ≤400 字（首字下沉+侧栏占版面），信息页 ≤150 字不变。
- 文生图资产竖版化：封面/满版/章扉出 **竖构图 1320×1920**（prompt 加 `portrait orientation, vertical composition, magazine full-bleed photography`）。
- 交付物命名与多格式导出沿用 `templates/output-pipelines.md`，PDF/PPTX 页面尺寸改为 6.875×10in。

## 10. 快速启动清单

1. `cp templates/ng-magazine/mag.css <项目>/output/`
2. 画页面地图（§5），定 60±页分配，每页标器型
3. 每片段复制 `generator-template.py` 头尾，中段填 `P.append`
4. 系统跑生成器 → 每片核对页数
5. `cp build-template.py → build_mag.py` 改 6 参数 → playwright 环境跑
6. issues 全清零 → 交付包 present
