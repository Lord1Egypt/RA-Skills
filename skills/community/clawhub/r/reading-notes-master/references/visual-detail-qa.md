# 视觉细节与验收治理手册 · Visual Detail QA

> reading-notes-master **v2.14** · 配套 `scripts/detail_audit.py`、`templates/quad-exact/`
> 覆盖 MECE 的 **C 资产构图** 与 **D 验收治理** 两层；渲染/内容工程见 `exact-content-engineering.md`。

## §1 三层验收体系（不要只用一层）

**结论先行**：零偏差验收只证明「槽位外像素没动」，证明不了「槽位里的内容好不好、
4K 图够不够、文字读不读得清」。v2.14 要求三层同时过：

| 层 | 工具 | 判据 | 回答的问题 |
|---|---|---|---|
| L1 设计层零偏差 | `exact_replication.verify(matrix=2.0, pad_px=3)` | `verdict=PASS` / `worst_outside=0.0` / 未动页 100% 相同 | 版式有没有被改坏？ |
| L2 内容与视觉细节 | `scripts/detail_audit.py` | 八门 D1–D8 | 内容/可读性/4K 够不够？ |
| L3 交付结构 | fitz + python-pptx 脚本 | 页数 / 画布 / 零越界 / 中文落位 | 文件能不能正常打开使用？ |

实测（四刊合璧 40 页）：L1 `PASS / 0.0 / edited=40`；L2 八门全 PASS；
L3 PDF 40 页画布逐页一致、PPTX 40 页 40 图零越界。

> **报告同步硬纪律**：每轮优化都要重跑 L1 + L2，并同步
> `零偏差验收.json` / `全复刻构建报告.json` / `细节体检.json` 三份报告。
> 只替换 PDF/PPTX 而沿用旧报告 = 交付不合格。

---

## §2 4K 资产池与内嵌图提取

### 资产规格（实测）

| 类型 | 数量 | 尺寸 | 来源 | 门禁 |
|---|---|---|---|---|
| 全画幅摄影 | 18 | `2645×3840` | 四刊满版页 `fitz.Matrix(m,m)` 高倍渲染 + LANCZOS | G5 长边 ≥3840、短边 ≥2645 |
| 科研真图 | 14 | `4739×3235` | `figure-bridge.py --resolution 4k --verify` | G1 零重叠 + G5 |
| 底版暗调 backdrop | 24 | `1500×2250` | 四刊各 6 张竖版大图，暗调 30% | 右脑优势资产 |
| 刊头摄影窗 | 12 | `1200×450` | 四刊横幅裁切 | 统一深色刊头 |

### 原刊内嵌图提取（v6 实战）

```python
for pno in range(len(doc)):
    for img in doc[pno].get_images(full=True):
        xref = img[0]
        d = doc.extract_image(xref)
        w, h = d["width"], d["height"]
        if w >= 1000 and h >= 700:      # ≥1MP 去重
            ...
```

全刊统计：953 张 <500px / 60 张 500–999 / 92 张 1000–1499 / 14 张 1500–1999 /
4 张 2000–2499；扫描 ≥1000×700 去重后得 **90 张大图**。
**注意 xref 归属页**：`photo_p028_x3495.jpg` 实属 P29，命名必须按实际页号核对，
否则 `FileNotFoundError`。

### 图片槽选取

```python
img_rects = pick_images(area_thr=0.02, min_side=40)     # >2% 页面积 且 边长>40pt
if not img_rects:
    img_rects = pick_images(0.005, 35)[:2]              # 纯文字/小装饰页自动放宽
plan[pno] = dict(images=img_rects[:6], ...)             # 上限 6
```

实测：图片槽 81 → **106**，零 4K 面积页 8 → 7（其余 6 页为原刊真无图的纯文字页
或透明层降级页，按契约不凭空加图）。

---

## §3 右脑优势量化（不要凭感觉改构图）

### 先量参照刊，再盘自己的页

四本参照刊各抽样 14 页，程序化统计：

| 指标 | NG 2026-10 | History | Italia | Traveller |
|---|---|---|---|---|
| 满幅图页占比（图像覆盖 >75%） | 71% | 64% | 57% | 36% |
| 图像覆盖率中位 | 77–100% | — | — | — |
| 暗像素中位 | 35–77% | — | — | — |
| 文字中位 | 509–2869 字符/页 | — | — | — |

**结论**：杂志感 = 深色摄影出血 + 文字叠压图上，不是白底分区卡片。

### 逐页盘点定位真短板

40 页交付中 **24 页页廊（占 60% 篇幅）图片面积仅 28%**，白底小缩略 + 灰描边。
此前 v5–v7 都在「加新页」，没动存量页廊 → 本轮主攻存量构图。

**v8 改造**：左 5.0in 满幅出血摄影（巨型 86pt 页码叠压图上 + 刊源/res 标注 + 黄条）
+ 右 8.333in INK 深色索引版 6 幅 1.5x 大图；`header()` 统一改杂志式深色刊头
（1.42in INK + 反白标题 + 黄竖标 + 右侧 3.783in 摄影窗）；尾页改满幅摄影对页。

| 结果 | 改前 | 改后 |
|---|---|---|
| 页廊平均图片覆盖率 | 28% | **67%**（进入参照刊 57–71% 区间） |
| P16 暗像素 | — | **74%**（参照 35–77%） |
| 页廊缩略图尺寸 | 1x 小图 | 1.5x 大图、无描边、反白页码 |

> **量化先于改造**：先有数字基线，再谈「右脑优势」，否则只是主观加图。

---

## §4 多刊合璧选页配额

### 选页算法

```python
def cls(r):
    if r["cov"] >= 0.82: return "photo"     # cov = Σ image_bbox_area / page_area
    if r["body"] >= 22:  return "text"
    return "mix"
quota = {"photo": 4, "mix": 4, "text": 2}   # 每刊 10 页
```

四刊各 10 页合并为 40 页底版，实测选页：

| 刊 | 选中原刊页号 |
|---|---|
| NG 2026-10 | 7, 8, 10, 51, 65, 100, 102, 103, 110, 129 |
| NG History 2026-08 | 1, 2, 25, 39, 52, 56, 82, 93, 94, 96 |
| NG Italia 2026-06 | 50, 53, 84, 89, 109, 113, 114, 118, 137, 140 |
| NG Traveller LA 2026 | 1, 2, 3, 6, 22, 31, 33, 42, 78, 112 |

### `page_manifest.json`（必留）

每页一条：`journal / src_page / quad_page / cov / body / imgs / canvas`。
用途：① 追溯每页来自哪本刊哪一页；② 解释画布尺寸差异；③ 漂移页定位来源。

**候选不足的自动放宽**：Traveller 严格条件 `w≥700, h≥900, 0.55≤w/h≤0.86`
只找到 11 张，按步长取 6 会 `IndexError`；候选 <16 张时放宽到
`minw=500, minh=650, 0.45≤ratio≤1.05`。四刊最终各取 6 张。

---

## §5 细节体检八门（`scripts/detail_audit.py`）

| 门 | 指标 | 达标线 | 实测 |
|---|---|---|---|
| D1 | 槽位外零偏差 | `PASS / 0.0` | `PASS / 0.0 / edited=40` |
| D2 | 中文真实落位（PDF 文本层） | ≥90% 页 | 39/40 页、5368 字、中位 109 |
| D3 | 语义字符占比 | ≥70% | 77.7% |
| D4 | 覆盖色偏差 | 中位 ≤4/255 且 >8/255 ≤5% | 1/255、P90 2/255、0.5% |
| D5 | WCAG 对比度 | <4.5 占比 ≤5% | 中位 16.79、1.1% |
| D6 | 中文溢出槽位 | ≤1% | 0/441 = 0% |
| D7 | 4K 图面积 | 中位 ≥50% | 63.4%、满幅页 22、零 4K 页 7 |
| D8 | 全书内容覆盖 | 窗口数 ≥80% 页数 | 40 窗口、正文 200476 字、0→97% |

```bash
python3 scripts/detail_audit.py base.pdf out.pdf \
  --slots plan.json --verify-report 零偏差验收.json \
  --semantic-char-pct 77.7 --body-chars 200476 --windows 40 \
  --json 细节体检.json
```

`--slots` 省略时从底版 span 自动推导候选槽位（体检基线用，非精确契约 mask）。
`--verify-report` 省略时 D1 记 WARN 并要求另跑 `verify()`；脚本不重算零偏差，避免两把尺子。
退出码 `0 = PASS/WARN`、`1 = FAIL`、`2 = 依赖/参数错误`。

**指标口径治理**：尾差补足后「槽位以标点收尾比例」必然下降（57.8%→13.8%），
语义连续性一律以 `semantic_char_pct` 为准；口径说明必须写进 JSON `note`，否则会被误读为退步。

---

## §6 构建报告契约（必含字段）

```jsonc
{
  "slots":   {"text": 0, "chart": 0, "protected": 0, "demoted": 0},
  "stream":  {"book_chars": 0, "consumed": 0, "coverage_pct": 0},
  "images":  {"blocks": 0, "filled": 0, "quote_cards": 0, "charts": 0},
  "tiers":   {"T1": 0, "T2": 0, "T3": 0},
  "output":  {"size_mb": 0},
  // v2.14 新增
  "stats":            {"text": 0, "images": 0, "semantic_char_pct": 0},
  "page_modes":       {"1": "full"},
  "degraded_pages":   {},
  "reverted_pages":   [],
  "content_audit":    {},     // 与 细节体检.json 完全一致
  "optimization":     [],     // 每轮改动逐条登记
  "verify":           {},     // 与 零偏差验收.json summary 一致
  "page_manifest":    []
}
```

`content_audit == 细节体检.json` 与 `verify == 零偏差验收.json.summary` 是**交付前必查等式**。

---

## §7 IMA 知识库归档五步（ima-skill / knowledge-base 模块）

> 归档前先读 `ima-skills/knowledge-base/SKILL.md`（`Skill("ima-skill")` 是注册名，
> `Skill("ima-skills")` 会报找不到）。文件上传**二进制原始内容，不转码**。

| 步 | 动作 | 关键约束 |
|---|---|---|
| 1 | `stat -f "%z" file` 取**精确字节** | `file_size` 必须与实际完全一致，否则签名校验失败 |
| 2 | `create_media(apply_upload_mode=1, content_type, file_name, file_ext, file_size, knowledge_base_id)` | `content_type` 按扩展名精确填，禁止 `application/octet-stream` |
| 3 | `curl --noproxy '*' -X PUT -T file` + 三个 header | `Content-Length`（与步骤 1 一致）/ `Content-Type` / `x-cos-acl: private`；`url_expired_ts` 前有效 |
| 4 | 检查 `HTTP 200` 且 `size_upload == file_size` | 失败即停，不继续 `add_knowledge` |
| 5 | `add_knowledge(media_id, duplicate_name_strategy=REPLACE)` | 同名迭代用 REPLACE，新增用 SAVE |

常用 MIME：`pdf→application/pdf` ·
`pptx→application/vnd.openxmlformats-officedocument.presentationml.presentation` ·
`md/markdown→text/markdown` · `txt→text/plain` · `png→image/png` · `html→text/html`。
**表中没有的扩展名（如 zip）不要猜测上传**；zip 只做本地分发。

**本地代理坑**：`http_proxy=http://127.0.0.1:55731` 会拦截 curl →
必须 `--noproxy '*'`。

---

## §8 交付结构验证清单（L3）

```python
# PDF
assert len(base) == len(out) == 40
assert all(base[i].rect == out[i].rect for i in range(len(base)))   # 画布逐页一致
# PPTX（python-pptx）
W, H = prs.slide_width, prs.slide_height
over = sum(1 for s in prs.slides for sh in s.shapes
           if sh.left < 0 or sh.top < 0
           or sh.left + sh.width > W + Inches(0.02)
           or sh.top + sh.height > H + Inches(0.02))
assert over == 0
```

另查：PDF 每页 `get_text()` 非空页比例、`get_image_info()` 中 4K 长边图数量、
PPTX 每页至少 1 张 `shape_type=13` PICTURE、文件头 `%PDF` / `PK`（PPTX 是 ZIP）。
实测 40 页 / 40 图 / 0 越界 / 59 张 4K 长边内嵌图。

**soffice 命名隔离**：`soffice --outdir delivery` 会按 PPTX 同名输出 PDF，
可能覆盖冻结的 140 页主刊 PDF。必须先导出到 `/tmp` 再复制为 `_演示文稿.pdf`。

---

## §9 已知边界与口径不适用

| 边界 | 处理 | 依据 |
|---|---|---|
| 满版信息图全竖排标注（Italia P53，67 竖 / 0 横） | 硬保护，该页可无中文，报告登记 | 设计层不可变契约 |
| 含透明层页面插大图合成抖动 | 分级局部降级，不扩大 mask | 见 `exact-content-engineering.md` §5 |
| 原刊纯文字页无图槽 | 不凭空加图，只放宽阈值到原刊既有小图 | 同上 |
| 四门验收 J3（英文原刊 3 栏拼贴流 ≥5 图/页、宽边距 51.6%） | 与「全画幅 4K 一图一世界」冲突时**披露为口径不适用**，另建专属门禁 | v2.11 规则 + 技能「用户点名风格优先」 |
| 未改动页 100% 相同 | 若 40 页全部改动，该项检查对象为 0，须在报告如实注明 | 验收语义 |

**不要为过门禁改坏版式**。口径冲突时如实披露 + 建专属验收，是技能既有原则。

---

## §10 命令速查

```bash
# 结构验证
python3 - <<'PY'  # fitz + python-pptx，见 §8
PY
# 细节八门
python3 scripts/detail_audit.py base.pdf out.pdf --slots plan.json --json 细节体检.json
# 归档（精确字节 → create_media → PUT → add_knowledge REPLACE）
stat -f "%z" out.pdf
```
