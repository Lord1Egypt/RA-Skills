---
name: signature-splice
description: 把若干张手写/电子签名图片，经预处理（去背景、去截图边框、紧裁、透明化）后，按指定顺序均匀插入 PDF 的目标区域（报名表/承诺书/审批单/合同等），并在插入后渲染自查。当用户提到"报名表签字、把签名拼进 PDF、给 PDF 加签名、电子签名插入、签字版 PDF、签名均匀排布、按名单顺序签名、签名放到签名栏"时使用。仅做"签名图片"的合成与排版；PDF 数字证书签名（加密签名域/签章证书）不适用。
version: 1.0.0
---

# signature-splice — 电子签名批量拼入 PDF

把 N 张**签名图片**按**给定顺序**、**均匀**排进 PDF 的某个区域，并渲染出来自查。
流程是**对齐的（固定 4 步抽象工作流）**，但**一切具体参数（PDF、签名图、顺序、目标区域、布局）都由参数传入**，
脚本内**零硬编码**：不写死人名、文件名、路径、坐标、阈值。

> ⚠️ 适用前提：插入的是**图片形式的签名**（手写/电子签）。若需要 PDF **数字证书签名**（签名域、时间戳、证书校验），
> 那是另一类工具，本 skill 不覆盖。

---

## 抽象工作流（4 步，固定不变）

```
① 采集与规范命名   → 把签名图整理成有序列表（setup 由调用方完成，见下）
② 预处理           → preprocess_signatures.py   产出"透明底·紧裁·纯黑墨"的 PNG
③ 定位 + 插入      → locate_anchor.py 求区域 → insert_signatures.py 按序均匀排布
④ 自查             → render_pdf.py 看图 + verify_merge.py 校验（页数/正文/嵌入图）
```

关键点：**每一张签名图都要先"归一化"成同一种干净形态**（透明底、紧裁到墨迹、纯黑），
再去排版；这样不同来源（白底 JPG、透明 PNG、"墨迹只在 alpha 通道"的 PNG、带截图边框的图）才能放进同一行而不突兀。

---

## 快速开始

```powershell
$SK = "$env:USERPROFILE\.config\opencode\skills\signature-splice\scripts"
$FORM = "报名表.pdf"
$RAW  = "raw_signatures"          # 里面放 任意名字 的签名图
$TMP  = "$env:OPENCODE_SCRATCH_DIR\2026-09-27_sign"

# ② 预处理（可选先 --input 单张 + inspect_signatures.py 诊断）
python "$SK\preprocess_signatures.py" --input $RAW --outdir "$TMP\clean"

# ③ 定位（确认区域对不对）+ 插入（按名单顺序）
python "$SK\locate_anchor.py" --pdf $FORM --anchor "（签名）" --no-frames
python "$SK\insert_signatures.py" --pdf $FORM --input "$TMP\clean" `
       --anchor "（签名）" --order "甲,乙,丙,丁" --out "$TMP\signed.pdf"

# ④ 自查
python "$SK\render_pdf.py"   --pdf "$TMP\signed.pdf" --outdir "$TMP\png" --dpi 220 --crop "38,145,575,250"
python "$SK\verify_merge.py" --original $FORM --signed "$TMP\signed.pdf"
```

**顺序来源**：`--order "甲,乙,丙,丁"`（逗号分隔）或 `--order-file names.txt`（每行一个）。
按**子串**匹配文件名，把 `--input` 重排成名单顺序；匹配不全直接报错退出。
不传 `--order` 时就按 `--input` 给定/目录排序的顺序插入。

**区域来源**（三选一）：
- `--anchor "（签名）"`：自动找锚点文本所在行，取其**外层框**内、锚点**行下方**的空白区（推荐，见 §定位）。
- `--box x0,y0,x1,y1`：手动指定外层框（仍取锚点行下方）。
- `--rect x0,y0,x1,y1`：手动指定最终区域，完全绕过自动定位。

**坐标单位**：全部是 PDF point（1 pt = 1/72 inch），原点在页面左上。

---

## 脚本

> 所有脚本：`argparse` 参数化、stdout 只输出 JSON、进度写 stderr、失败非 0 退出。
> 输入支持**多文件** `--input a b c` 或**目录** `--input dir --glob "*.png"`；输出一律 `--out` / `--outdir` 指定。

### scripts/preprocess_signatures.py
用途：把任意来源的签名图归一化为**透明底、紧裁、纯黑墨**的 RGBA PNG。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--input PATH...` | 签名图文件 和/或 目录（目录配 `--glob`） | ✅ |
| `--glob PAT` | 目录下匹配模式（默认 `*`，再按图片扩展名过滤） | 否 |
| `--outdir DIR` | 输出目录（自动创建） | ✅ |
| `--ink-threshold F` | 墨迹阈值（默认 35） | 否 |
| `--adaptive-delta F` | 自适应：阈值 ≥ 背景墨迹 + 该值（默认 25，0 关闭） | 否 |
| `--frame-threshold F` / `--frame-span F` / `--margin-frac F` | 去截图边框：边带内覆盖率 > span 的行/列判为边框线（默认 20 / 0.85 / 0.06） | 否 |
| `--min-blob N` | 去除小于 N 像素的杂点（默认 14，0 关闭） | 否 |
| `--pad-frac F` | 裁剪后留白比例（默认 0.03） | 否 |
| `--polarity {auto,light,dark}` | 墨迹极性（默认 auto：按合成到白底后的边框亮度判） | 否 |
| `--keep-color` | 保留原始墨色（默认强制纯黑） | 否 |

示例：`python scripts/preprocess_signatures.py --input raw/ --outdir clean/`
输出：`{"status":"ok","count":N,"items":[{src,dst,polarity,frame_trimmed,out_size,aspect,...}],"errors":[]}`

### scripts/locate_anchor.py
用途：由锚点文本**数据驱动**地求出插入区域（可当库用：`from locate_anchor import find_region`）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--pdf FILE` | 输入 PDF | ✅ |
| `--anchor TEXT` | 签名栏提示文字（子串匹配，如 `（签名）`） | ✅（或 `--box`/`--rect`） |
| `--page N` / `--nth N` | 页号（默认 1）/ 第几个匹配（默认 0） | 否 |
| `--inset F` / `--gap F` | 距框边距 / 锚点行下方间距（默认 2.5 / 3.0） | 否 |
| `--box x0,y0,x1,y1` | 手动外层框 | 否 |
| `--rect x0,y0,x1,y1` | 手动最终区域 | 否 |
| `--no-frames` | 输出里不列全部框 | 否 |

示例：`python scripts/locate_anchor.py --pdf form.pdf --anchor "（签名）" --no-frames`
输出：`{"status":"ok","anchor":{"bbox":...},"enclosing_frame":[...],"region":[x0,y0,x1,y1], ...}`

### scripts/insert_signatures.py
用途：按顺序把签名图**均匀**排进区域并写入新 PDF。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--pdf FILE` / `--out FILE` | 输入 / 输出 PDF | ✅ |
| `--input PATH...` | 签名图（**按插入顺序**给；目录配 `--glob`） | ✅ |
| `--order "a,b,c"` / `--order-file F` | 按名单重排（子串匹配文件名） | 否 |
| `--anchor` / `--box` / `--rect` / `--inset` / `--gap` / `--nth` / `--page` | 同 locate_anchor（区域来源） | 区域必选一 |
| `--rows N` / `--cols N` | 网格（默认 1 × auto=⌈N/rows⌉） | 否 |
| `--cell-fill F` | 每格内签名占比（默认 0.94，留缝） | 否 |
| `--labels` / `--label-size` / `--label-gap` / `--label-color` / `--label-font` | 每张签名下加说明文字（默认关闭） | 否 |
| `--debug` | 画出格子边框 + 序号（自查用） | 否 |

示例：`python scripts/insert_signatures.py --pdf form.pdf --input clean/ --anchor "（签名）" --order "甲,乙,丙,丁" --out signed.pdf`
输出：`{"status":"ok","region":[...],"grid":[r,c],"slots":[{order,file,cell,target,drawn_pt}...]}`

### scripts/render_pdf.py
用途：PDF→PNG，用于插入后**肉眼自查**。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--pdf FILE`（可含通配） | 输入 PDF | ✅ |
| `--outdir DIR` | 输出目录 | ✅ |
| `--dpi N` | 分辨率（默认 150） | 否 |
| `--crop x0,y0,x1,y1` | 只渲染该矩形区域（放大看细节） | 否 |
| `--page N` | 只渲染该页 | 否 |

示例：`python scripts/render_pdf.py --pdf signed.pdf --outdir png/ --dpi 220 --crop 38,145,575,250`

### scripts/verify_merge.py
用途：核对签字版与原稿：页数、**正文文本是否逐页一致**、嵌入了哪些图。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--original FILE` / `--signed FILE` | 原稿 / 签字版 | ✅ |

输出：`{"original":{...},"signed":{...},"images_in_signed":[...],"text_identical":true/false}`

### scripts/contact_sheet.py
用途：把预处理结果拼成一张预览图（看透明底/裁剪/大小是否正常）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--input PATH...`（+`--glob`） | 签名图 | ✅ |
| `--out FILE` | 输出 PNG | ✅ |
| `--scale F` / `--bg COLOR` | 缩放 / 底色（默认 1.0 / white） | 否 |

### scripts/inspect_signatures.py
用途：**诊断**难以处理的图（当预处理结果不对时先跑它）：模式/尺寸、alpha 与亮度范围、墨色色度、
合成背景亮度与极性猜测、检测到的**截图边框线**、墨迹包围盒与长宽比。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--input PATH...`（+`--glob`） | 待诊断图片 | ✅ |
| `--ink-threshold` / `--frame-threshold` / `--frame-span` / `--margin-frac` | 同预处理 | 否 |

---

## 定位原理（为什么能自动找到签名栏）

1. 把页面**矢量线条**按相交/相邻合并成「框」（表格、方框、单元格都会各自合并成一个矩形）。
2. 找到含 `--anchor` 的**文本行**，取其行 bbox。
3. 在所有"包含该行、且高度 ≥ 2 倍行高"的框里，取**面积最小**的那个 → 该签名栏的框。
4. 区域 = 框内、**锚点行下方**（`y = 行底 + gap` 到 `框底 − inset`），横向 `框左+inset` 到 `框右−inset`。

若页面没有可用矢量框（纯扫描图、无边框），自动定位会报 `error` 并提示改用 `--rect`/`--box`。
表格类表单里如果锚点出现在**多行**（如"签名"两处），用 `--nth` 选第几个，或用 `--rect` 精确指定。

---

## 常见坑与对策

| 现象 | 原因 | 对策 |
|------|------|------|
| 预处理后一片空白 / 全黑 | 极性判反（深底浅字，或"墨迹只在 alpha 通道"） | 先跑 `inspect_signatures.py` 看 `polarity_guess`，必要时 `--polarity light/dark` |
| 结果里带灰色/黑色边框线 | 签名图是**截图**，四周有边框 | 默认已去边框；更宽的框调大 `--margin-frac`（如 0.1）或放宽 `--frame-span` |
| 边缘被裁掉笔画 | 裁剪包围盒太紧 | 调大 `--pad-frac`（如 0.06） |
| 带小白点/噪点 | JPG 压缩噪点 | 调大 `--min-blob`（如 30） |
| 保留下来的灰底/阴影成块 | 背景不够白（扫描件） | 调大 `--adaptive-delta`（如 40）或 `--ink-threshold` |
| 签名大小不一 | 各图长宽比/留白不同 | 正常；预处理已统一裁到墨迹并统一高度。仍不齐可 `--cell-fill` 微调 |
| 想保留蓝笔颜色 | 默认强制纯黑 | 加 `--keep-color` |
| 顺序不对 | `--input` 目录排序 ≠ 名单顺序 | 用 `--order` / `--order-file` |

更多细节见 `references/workflow.md`。

---

## 依赖与文件管理

- 依赖：`PyMuPDF(fitz)`、`Pillow`、`numpy`、`scipy`。
- 所有**产物/中间件写调用方指定的项目文件夹**（`--out`/`--outdir`），skill 目录不留产物。
- 本机跨机同步：`~/.config/opencode/skills/signature-splice/`。
