# 零偏差内容工程手册 · Exact Content Engineering

> reading-notes-master **v2.14** · 配套 `scripts/semantic_stream.py`、`templates/quad-exact/`
> 全部数字来自 2026-11-09/10 四刊合璧 40 页 1:1 全复刻的连续五轮实跑，非示例数据。

## §0 定位与基线结论

**结论先行**：v2.13 的 `apply_redactions` 路径在纯矢量、无透明组、少量槽位时成立；一旦进入
「多刊混合底版 +  photography/透明层 + 数百个槽位 + 中文内容」，它会产生非局部内容流副作用。
v2.14 默认改走 **覆盖式替换**，并补齐 v2.13 缺失的内容层门禁。最终实测：

| 指标 | 首版 | v2.14 最终 |
|---|---|---|
| 文字槽成功数 | 8 | **530** |
| 图片槽 | 81 | **106** |
| PDF 有中文页（文本层实测） | 26/40 | **39/40** |
| 可见色块槽位 | 15.1% | **0.5%**（>8/255） |
| 对比度 <4.5 槽位 | 13.7% | **1.1%** |
| 内容覆盖全书 | 3.2% | **0→97%** |
| 回退为纯版式页 | 3 | **0** |
| 零偏差 | `PASS / 0.0` | `PASS / 0.0`（全程未破） |

**本手册覆盖 A 渲染几何 + B 内容工程两层**；视觉/验收/治理见 `visual-detail-qa.md`
与 `skill-evolution-governance.md`。

---

## §1 覆盖式替换（默认路径）

### 决策表

| 判据 | `apply_redactions`（v2.13） | 覆盖式替换（v2.14 默认） |
|---|---|---|
| 底版类型 | 纯矢量、无透明组 | 多刊混合、含摄影/透明层 |
| 槽位规模 | 个位数～数十 | 数百（实测 548 文字槽 + 106 图片槽） |
| 机制 | 删原文字对象 → 重写 | 同 bbox 不透明矩形覆盖 → 原坐标回写 |
| 副作用 | 内容流 / clip 非局部变化 | 改动严格落在 mask 内 |
| 前置 | `collision_report` 必跑 | `collision_report` 仍必跑 + mask 登记 |

### 最小可运行骨架

```python
# 1) 采样底色（底版渲染 1x），取中位色精确值
pix = pg.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
arr = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3)
reg = arr[y0:y1, x0:x1]
if reg.std() > 72:        # 摄影/复杂底纹 → 硬保护，跳过
    continue
med = tuple(float(v) for v in np.median(reg.reshape(-1, 3), axis=0) / 255.0)

# 2) 精确色覆盖（禁止量化）
pg.draw_rect(r, color=None, fill=med, overlay=True)
masks[pno].append(r)

# 3) 原坐标中文回写
col = text_color(med)     # 见 §2
tb = fitz.Rect(r.x0, r.y0, r.x1 + 0.4, r.y1 + 2.0)
for sz in (size, size * .85, size * .72, 6.0):
    spare = pg.insert_textbox(tb, chunk, fontsize=sz, fontname=fontname,
                              color=col, align=0, overlay=True)
    if spare >= 0:
        masks[pno].append(tb)     # 文本框也必须登记
        break
```

> **不要用 `round(v*8)/8` 分组同色覆盖**。分组能减少 shape 数量，但 1/8 量化最大偏差 0.0625，
> 实测 15.1% 槽位出现肉眼可见色块（P90 0.0498）。改用精确值后实测偏差中位 **1/255**、
> P90 **2/255**、>8/255 仅 **0.5%**（548 槽）。

---

## §2 精确覆盖色与 WCAG 文字色

| 项 | 错误做法 | v2.14 做法 | 实测 |
|---|---|---|---|
| 覆盖色 | 量化到 1/8 | 采样中位色精确 float 三元组 | 色块 15.1% → 0.5% |
| 文字色 | `sum(med)/3 > 0.55` 二值切换 | WCAG 相对亮度择优 + 纯黑兜底 | 低对比 13.7% → 1.1%，中位 16.79 |

```python
def _lum(c):
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]

def contrast(a, b):
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + .05) / (l2 + .05)

def text_color(bg, min_contrast=4.5):
    best = max(((0.13, 0.11, 0.12), (1., 1., 1.)), key=lambda c: contrast(bg, c))
    if contrast(bg, best) < min_contrast:
        best = max(((0., 0., 0.), (1., 1., 1.)), key=lambda c: contrast(bg, c))
    return best
```

**边界（v2.14 自检新发现）**：中灰 `(0.5,0.5,0.5)` 下深墨 `(0.13,0.11,0.12)` 对比度仅 **4.22**、
白字仅 **3.98**，两者都不到 4.5 —— 这正是实战残留 1.1% 低对比槽位的根因。
**纯黑兜底**可把该值提到 **5.28**。`semantic_stream.py --self-test` 已固化此断言。
（当前 40 页交付仍用两色择优版本，故报告如实写 1.1%；下一版接入兜底后可压到 0。）

---

## §3 CJK `insert_textbox` 静默失败（最高频坑）

**现象**：构建日志显示「文字 530 槽成功」，PDF 文本层却只有 26/40 页能提取中文。

**根因**：CJK 字体的行高约 **1.2×字号**；`insert_textbox` 空间不足时**返回负值且不插入任何文字**，
不抛异常。原代码不看返回值就 `stats["text"] += 1`。实测 `size=10 / height=10pt → -1.4`，
`size=8 → 0.88`。

**修复**：
1. 检查 `spare >= 0` 才算成功；失败时按 `(size, .85size, .72size, 6pt)` 逐级降字号重试。
2. `cap = max(2, int(rect.width / (size * 1.28)))` —— 中文全角字符留 28% 行末余量。
3. **另跑 PDF 文本层审计**（`get_text()` + CJK 正则），绝不以构建 stats 代替落位验证。

**第二个独立根因**：满版摄影页的原刊图注压在照片上，被「不与图片槽相交」规则全部过滤
（13 页文字槽为 0）。修复是补 `over_img` 槽：允许与图片相交，但**只用原刊既有文字 bbox**
（不新增栏位），并把方差阈值放宽到 110、运行时再按底色复核。

---

## §4 mask 契约与高方差保护

| 必须登记的 mask | 原因 |
|---|---|
| 覆盖矩形 `r` | 主改动区 |
| 实际文本框 `Rect(x0,y0,x1+0.4,y1+2.0)` | 抗锯齿边缘、CJK 下伸部会超出 `r` |

`verify(src, out, masks, matrix=2.0, pad_px=3)` 的 pad 仅 1.5pt，文本框下沿 +2.0pt 会越界，
**只登记覆盖矩形会被误判为槽位外漂移**。

**硬保护阈值**：`reg.std() > 72`（正文）/ `> 110`（`over_img` 压图图注）→ 跳过，
保留原刊文字，避免盖坏满版摄影。实测跳过 18 槽 / 548 槽。

---

## §5 漂移页分级局部降级

**诊断先于处理**。逐像素定位漂移 bbox（渲染 2x，`diff & ~mask`），实测：

| 页 | 漂移像素 | 位置 | 距最近槽位 |
|---|---|---|---|
| P28 | 45 | 局部零散 | 33.6pt |
| P32 | 1927 | 全页零散 | 远离全部槽位 |
| P40 | 248 | 右边缘 x=651.5 | 边缘 1px 线 |

三者均**远离槽位**且量级极小 → 判定为 PyMuPDF 重写含透明层页面时 `insert_image` 的
亚像素合成抖动，不是内容越界。分级实验确认：降为「仅 4K 图」仍漂移（0.0372），
降为「仅中文」即 `PASS / 0.0` → 罪魁是图片插入。

**降级链**（替代整页回退）：

```python
DEGRADE = {"full": "images", "images": "text", "text": "none", "none": "none"}
for rnd in range(1, 6):
    masks, stats = replace_pages(plan, modes, photos, figs)
    rep = verify(BASE, OUT, masks, matrix=2.0, pad_px=3, out_json=...)
    bad = [p["page"] for p in rep["pages"] if not p["zero_drift"]]
    if not bad and rep["summary"]["verdict"] == "PASS": break
    modes.update({p: DEGRADE[modes[p]] for p in bad})
```

结果：3 页从「纯版式无内容」→「仅中文替换」，**40/40 页有改动、零回退页**。
每轮保存 `零偏差验收_roundN.json` 供追溯。

> **禁止靠扩大 mask 掩盖漂移**。mask 只能登记真实改动区；扩大 mask 等于放弃零偏差契约。

---

## §6 多画布比例与 PPTX 留白

四刊实测 5 种画布：`495×720 / 496×720 / 595×780 / 652×850 / 670×850 pt`。
PPTX 只能有全局尺寸（6.875×10in），contain 会产生 **9.9–12.8% 上下留白**。

```python
a = np.asarray(im)
t, l = min(4, a.shape[0]), min(4, a.shape[1])
edge = np.concatenate([a[:t].reshape(-1, 3), a[-t:].reshape(-1, 3),
                       a[:, :l].reshape(-1, 3), a[:, -l:].reshape(-1, 3)], axis=0)
pad = tuple(int(v) for v in np.median(edge, axis=0))
cv = Image.new("RGB", (1500, 2182), pad)      # 旧版 "white" 造成硬白边
```

实测留白与页面边缘色差 0（NG 黄页 / 深底页 / 白底页各自跟随），体积 21.16 → 19.82 MB。

---

## §7 内容流四步管线

| 步 | 动作 | 关键参数 | 实测 |
|---|---|---|---|
| 1 | 剥离前置 matter + 书末附录 | `find("前言")`=269 → `rfind("Table of Contents")`=200745 | 正文 200476 字 |
| 2 | 中文标点短语化 | ≤10 字，中文间空白删除、英文词间保留单空格 | 26331 条 |
| 3 | 全书 N 等分 | `page_queues(40)`，每页取 1/40 连续片段 | 各页首段 0%→97% |
| 4 | 栏宽尾差补足 | 下一短语前缀补 cap，剩余 `appendleft` 回队首 | 4276→**5368 字**、语义字符 **77.7%** |

```python
from semantic_stream import (strip_front_matter, build_fragments,
                             page_queues, take_frags, text_color)
body, s, e = strip_front_matter(raw)
queues = page_queues(build_fragments(body), 40)
chunk = take_frags(queues[pno - 1], cap, stats)
```

**补足规则**：不切在成对符号 `（《「‘“` 或英文单词中间；剩余片段留队首保证下一个槽位接着读。
这是「栏宽填满」与「语义完整」的兼顾点，只做前者是断章，只做后者掉 34% 文字量。

---

## §8 文本层审计（stats ≠ 落位）

每轮构建后必须跑：

```python
cjk = re.compile(r"[\u4e00-\u9fff]")
per = [len(cjk.findall(pg.get_text())) for pg in fitz.open(OUT_PDF)]
```

输出 `pages_with_cn / cjk_chars / median_cjk_per_page / pages_without_cn`，写进
`细节体检.json`。实测这一条独立发现了 CJK 静默失败（§3）与满版页槽位过滤（§3）两个根因。

**已知边界**：Italia P53 圣家堂满版信息图共 67 处文字**全为竖排标注**（bbox 宽仅 7pt、
横向 span 0 处），横排中文无法落入原 bbox。按设计层不可变契约硬保护，该页无中文，
并在报告 `note` 中如实登记，不强行改版式。

---

## §9 踩坑库（12 条 · 问题 / 根因 / 修复）

| # | 问题 | 根因 | 修复 |
|---|---|---|---|
| 1 | 槽位外像素变化 | `apply_redactions` 非局部内容流副作用 | 覆盖式替换 + 原坐标回写 |
| 2 | 文字框像彩色贴片 | 覆盖色 1/8 量化 | 采样中位色精确 float |
| 3 | 中灰底文字发灰 | 二值阈值 + 深墨上限 4.22 | WCAG 择优 + 纯黑兜底 5.28 |
| 4 | stats 成功但 PDF 无中文 | `insert_textbox` 负值静默不写 | 查返回值 + 逐级降字号 |
| 5 | 满版摄影页零中文 | 「不与图片相交」全过滤 | `over_img` 图注槽 + 方差 110 |
| 6 | 中文断章 | 按字数硬切 | 语义短语 + 尾差补足 |
| 7 | 内容只有版权/献词 | 从文件第 1 字顺序消费 | 剥离前置 matter |
| 8 | 只覆盖全书 3.2% | 单游标顺序消费 | 全书 N 等分队列 |
| 9 | 补足后文字量掉 34% | 只取完整短语凑不满栏宽 | 下一短语前缀补足 + 回队首 |
| 10 | 3 页漂移 | 透明层 `insert_image` 合成抖动 | 分级局部降级，非整页回退 |
| 11 | mask 漏判漂移 | 文本框超出覆盖矩形 2pt | mask 同时登记两者 |
| 12 | PPTX 上下硬白边 | contain 到统一画布用白底 | 四边中位色留白 |

---

## §10 与 v2.13 契约的关系

v2.13 定义「哪些不可变、哪些可换」，本手册定义「怎么换而不破契约」。
两者共用 `build_page_models()` 与 `verify()`，不另起引擎。
`collision_report` 预检、T1/T2/T3 字体档位、基线用原页面 ascender 等 v2.13 铁律**全部继续有效**。
差异只在：注入机制（redact → overlay）、内容层（新增四步管线）、验收层（新增八门）。

**命令速查**

```bash
python3 scripts/semantic_stream.py --self-test
python3 scripts/semantic_stream.py --file book.txt --pages 40 --json stream.json
python3 scripts/detail_audit.py base.pdf out.pdf --slots plan.json \
    --verify-report 零偏差验收.json --semantic-char-pct 77.7 \
    --body-chars 200476 --windows 40 --json 细节体检.json
```
