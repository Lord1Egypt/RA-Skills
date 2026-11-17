# -*- coding: utf-8 -*-
"""PDF 去水印：导出为图 → 逐页去水印 → 合并回 PDF。

为什么必须走"位图化"这条路
--------------------------
这类素材（夏梦迪讲义/笔记）里的水印不是 PDF 的文字或图形对象，而是**已经被压进
扫描位图里**的像素——PDF 页面既没有文字层（get_text() 返回空），水印也不可能用
"删除对象"的方式干掉。所以唯一可行的路径是：

    PDF ──渲染──> 位图 ──像素级去水印──> 位图 ──重新打包──> PDF

两处细节：
* 渲染统一走 get_pixmap()。**不要**贪快去取内嵌原图——同一份 PDF 里有的页是"整页
  一张大图"，有的页是"多张小图拼贴"（比如第 71 页：版面 + 黄色飞机插图），
  取"最大的一张"会拿到插图而不是页面本身。
* 写回时把每页按原始物理尺寸（A4 = 595.276 × 841.89 pt）铺成整页图，页面比例
  与原件完全一致。

页眉 logo（"夏梦迪物理"五个字）
--------------------------------
它不是半透明水印，而是**印刷体的彩色 logo**，走另一套逻辑。主色 (255,192,0) 的
色相楔在页眉带里是唯一的（蓝框 79,129,189 的 b 太高、灰色插图不进楔、正文里没有
纯黄），所以按"最靠上的一团橙黄 + 尺寸校验"来定位。

限定在页眉带内非常重要：正文插图里也有黄色物体（第 71 页的黄色飞机就在 y≈1200），
全图按颜色清会误伤。
"""
import io
import os

import numpy as np

try:
    import pymupdf
except ImportError:  # 兼容旧名
    try:
        import fitz as pymupdf
    except ImportError:
        # pymupdf 只是 PDF 输入才需要。logo 清除是纯 numpy，没有它也能用。
        pymupdf = None

from PIL import Image

import wmcore

# ---- 页眉 logo 颜色参数 -------------------------------------------------
# 主色 (255,192,0)：r 拉满、b 压到 0、g 居中。判定用色相楔而非"接近某具体 RGB"，
# 才能同时吃下抗锯齿过渡色。
LOGO_CORE = dict(r_min=240, g_min=150, g_max=235, b_max=60, rb_min=150, gb_min=90)

# 形状校验一律用**相对页面的比例**，不写死像素——同一份素材在 150dpi 下文字块
# 只有 116×22px，按绝对像素判断会被当成噪声漏掉。
# 实测（300dpi A4 2481×3508）：高 40~45 → h/H≈0.0114~0.0128；
# 宽 210~233 → w/W≈0.085~0.094；字面填充率 n/(w·h)≈0.21~0.25。
LOGO_H_FRAC = (0.005, 0.030)   # 团高度 / 页高
LOGO_W_FRAC = (0.040, 0.220)   # 团宽度 / 页宽
LOGO_FILL = (0.10, 0.45)       # 核心像素 / bbox 面积，排除实心色块与插图
LOGO_MIN_PIXELS = 100          # 绝对下限，滤掉小图上的噪点
LOGO_MAX_PIXELS = 8000         # 绝对上限（不分辨率缩放），黄飞机有 24k

# 页眉带（相对页高）。logo 实测落在 y/H ∈ [0.066, 0.109]，取 [0.02, 0.15] 留余量。
HEADER_BAND_TOP = 0.02
HEADER_BAND_BOT = 0.15


def _page_array(page, dpi=300):
    """取页面位图。统一走渲染——见模块 docstring。"""
    pix = page.get_pixmap(dpi=dpi)
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    arr = arr.reshape(pix.height, pix.width, pix.n)[:, :, :3]
    return np.ascontiguousarray(arr), "渲染"


def _row_groups(mask):
    """把掩膜里的行按连通（间隙 ≤8px）聚成团，返回 [(y0,y1), ...]。"""
    rows = np.nonzero(mask.any(axis=1))[0]
    if rows.size == 0:
        return []
    groups, cur = [], [int(rows[0])]
    for y in rows[1:]:
        if y - cur[-1] <= 8:
            cur.append(int(y))
        else:
            groups.append((cur[0], cur[-1]))
            cur = [int(y)]
    groups.append((cur[0], cur[-1]))
    return groups


def logo_mask(a, band_top=HEADER_BAND_TOP, band_bot=HEADER_BAND_BOT):
    """页眉 logo 文字的像素掩膜（只取橙黄文字，不含蓝框、不含正文插图）。

    规则：页眉带内找"最靠上的一团橙黄核心色"，再用尺寸与像素数校验它确实是
    那五个字；校验不过就当没有 logo（宁可漏掉，不能伤正文）。
    """
    H, W = a.shape[:2]
    y0, y1 = int(H * band_top), int(H * band_bot)
    band = a[y0:y1].astype(np.int16)
    r, g, b = band[:, :, 0], band[:, :, 1], band[:, :, 2]
    core = ((r >= LOGO_CORE["r_min"]) & (g >= LOGO_CORE["g_min"])
            & (g <= LOGO_CORE["g_max"]) & (b <= LOGO_CORE["b_max"])
            & ((r - b) >= LOGO_CORE["rb_min"]) & ((g - b) >= LOGO_CORE["gb_min"]))
    if int(core.sum()) < LOGO_MIN_PIXELS:
        return np.zeros((H, W), bool)

    groups = _row_groups(core)
    full = np.zeros((H, W), bool)
    for gy0, gy1 in groups:
        m = core[gy0:gy1 + 1]
        n = int(m.sum())
        h = gy1 - gy0 + 1
        xs = np.nonzero(m.any(axis=0))[0]
        w = int(xs.max() - xs.min() + 1) if xs.size else 0
        if not (LOGO_MIN_PIXELS <= n <= LOGO_MAX_PIXELS):
            continue
        if not (LOGO_H_FRAC[0] <= h / H <= LOGO_H_FRAC[1]):
            continue
        if not (LOGO_W_FRAC[0] <= w / W <= LOGO_W_FRAC[1]):
            continue
        # 填充率：文字是"稀疏笔画"，实心色块/插图填充率会明显偏离
        if not (LOGO_FILL[0] <= n / max(w * h, 1) <= LOGO_FILL[1]):
            continue
        full[y0 + gy0:y0 + gy1 + 1] |= m
        # 同一页面只取最靠上的合格团（正文插图的黄色物体在更下方）
        break
    return full


def _dilate(mask, times=2):
    d = mask.copy()
    for _ in range(times):
        d = (d | np.roll(d, 1, 0) | np.roll(d, -1, 0)
             | np.roll(d, 1, 1) | np.roll(d, -1, 1))
    return d


def _clean_logo(after, lm):
    """在白纸上清掉 logo 字形，返回清除的像素数。

    三步，从紧到松：
    1. 核心楔形像素直接填白。
    2. 核心外围 4px 内的暖色抗锯齿晕圈填白。
    3. 整个字形簇的 bbox（外扩 6px）内，凡是"暖色且不深"的像素一并填白。

    第 3 步是给低分辨率兜底的：150dpi 下采样后字芯往往够不到楔形阈值
    （b 被抬到 90 左右），只做 1、2 会留下一层淡黄残晕。bbox 内本来就只有
    白纸和蓝框，蓝框是冷色（b > r）不会被碰。

    两条"别吃错东西"的边界：
    * 蓝框及其过渡色：冷色 b > r，被 `b <= r` 排除。
    * 红笔迹：logo 是橙黄（r-g ≈ 63），红笔写出来 r-g ≈ 90 以上。bbox 可能
      压到页眉里的红色批注，所以要求 `r-g <= 80` 才算"logo 的暖色"。
    """
    if not lm.any():
        return after, 0
    after = after.copy()
    n = int(lm.sum())
    after[lm] = 255

    r, g, b = after[:, :, 0], after[:, :, 1], after[:, :, 2]
    warm = ((r >= 200) & ((r - b) >= 8) & (r >= g - 2) & ((r - g) <= 80))

    halo = _dilate(lm, 4) & ~lm
    h = halo & warm
    if h.any():
        n += int(h.sum())
        after[h] = 255

    ys, xs = np.nonzero(lm)
    pad = 6
    y0, y1 = max(0, ys.min() - pad), min(after.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(after.shape[1], xs.max() + pad + 1)
    box = np.zeros(after.shape[:2], bool)
    box[y0:y1, x0:x1] = True
    # 重新取色（halo 已改过像素）。min > 140 保护深色内容，b <= r 排除蓝框，
    # r-g <= 80 排除红笔迹（见 docstring）
    r, g, b = after[:, :, 0], after[:, :, 1], after[:, :, 2]
    warm = ((r >= 200) & ((r - b) >= 8) & (r >= g - 2) & ((r - g) <= 80))
    sweep = (box & warm & (np.minimum(np.minimum(r, g), b) > 140)
             & (b <= r) & (r < 255))
    if sweep.any():
        n += int(sweep.sum())
        after[sweep] = 255
    return after, n


def process_page_array(arr, near=5, pink=True, purple=True, remove_logo=True):
    """处理单页位图，返回 (结果, 统计)。"""
    before = arr.astype(np.int16)
    after, cleared = wmcore.process_array(before, near, pink, purple)
    logo_px = 0
    if remove_logo:
        after, logo_px = _clean_logo(after, logo_mask(after))
    return after, dict(cleared=cleared, logo=logo_px)


def logo_only(arr):
    """只清页眉 logo，不动水印。给图片批处理的二次清理钩子用。"""
    after, _ = _clean_logo(np.asarray(arr).copy(), logo_mask(np.asarray(arr)))
    return after


def process_pdf(src, dst, near=5, pink=True, purple=True, remove_logo=True,
                jpeg_quality=98, progress=None, log=None, report=None,
                should_stop=None, keep_images=False, image_dir=None):
    """PDF 去水印主流程。返回 rows 列表（每页一行）。

    jpeg_quality 默认 98：实测 q88 会把淡蓝抗锯齿边缘压坏（蓝保留 98.7%），且
    JPEG 噪点会落进超淡水印窗口造成假残留（1078px）；q98 时残留仅 21px、
    红/深/蓝全部 ≥100%，再往上 q100 只省 4px 却多 18% 体积。
    """
    if pymupdf is None:
        raise RuntimeError("PDF 输入需要 pymupdf：pip install pymupdf")
    doc = pymupdf.open(src)
    os.makedirs(os.path.dirname(os.path.abspath(dst)) or ".", exist_ok=True)
    out = pymupdf.open()
    rows = []
    total = doc.page_count
    stopped = False

    for i in range(total):
        if should_stop is not None and should_stop():
            stopped = True
            break
        page = doc[i]
        try:
            arr, note = _page_array(page)
            lm = logo_mask(arr) if remove_logo else None
            after, st = process_page_array(arr, near, pink, purple, remove_logo)

            # 内容保留率必须把 logo 区域排除在外：橙黄 logo 字本身会被
            # "红"和"深"两条判据命中（r-g=63>60、min 通道=0<150），
            # 不排除的话清除 logo 就会让红/深保留率凭空掉一截（白页甚至报 0%）。
            # 排除区用**膨胀后**的掩膜——连同文字外围的抗锯齿晕圈一起算进去，
            # 否则 halo 清掉的边缘像素会被记成"内容丢失"。
            cmp_before, cmp_after = arr.astype(np.int16), after.astype(np.int16)
            if lm is not None and lm.any():
                excl = _dilate(lm, 5)
                cmp_before = cmp_before.copy()
                cmp_after = cmp_after.copy()
                cmp_before[excl] = 255
                cmp_after[excl] = 255
            (orr, odb, obl), (nrr, ndb, nbl) = (
                wmcore._content_counts(cmp_before),
                wmcore._content_counts(cmp_after))

            rect = page.rect
            newp = out.new_page(width=rect.width, height=rect.height)
            buf = io.BytesIO()
            Image.fromarray(after.astype(np.uint8)).save(
                buf, format="JPEG", quality=jpeg_quality, optimize=True)
            newp.insert_image(rect, stream=buf.getvalue())

            if keep_images and image_dir:
                os.makedirs(image_dir, exist_ok=True)
                Image.fromarray(after.astype(np.uint8)).save(
                    os.path.join(image_dir, f"p{i + 1:04d}.png"))

            # 残留按"能看见的"算：JPEG 会在白纸上留下 min≥240 的近白振铃，
            # 落进超淡水印窗口能把计数抬到几千，但肉眼不可见。
            res, res_dark = wmcore.residue_profile(after)
            # 真内容损失：原本是强内容、却被涂白的像素数。比"保留率百分比"
            # 可靠——抗锯齿边缘在 JPEG 里挪几个单位就会让百分比掉几个点，
            # 但那些从来不是内容。
            erased = wmcore.erased_content(
                arr.astype(np.int16), after,
                exclude=_dilate(lm, 5) if (lm is not None and lm.any()) else None)
            row = (i + 1, st["cleared"], st["logo"],
                   100.0 * nrr / orr if orr else 100.0,
                   100.0 * ndb / odb if odb else 100.0,
                   100.0 * nbl / obl if obl else 100.0, note, res, res_dark, erased)
            rows.append(row)
            if log:
                log(f"第 {i + 1:>3} 页  水印清除={st['cleared']}  logo={st['logo']}  "
                    f"红={row[3]:.1f}%  深={row[4]:.1f}%  蓝={row[5]:.1f}%  "
                    f"残留={res}(可见 {res_dark})  误伤={erased}")
        except Exception as exc:
            rows.append((i + 1, 0, 0, 0.0, 0.0, 0.0, "失败", -1, -1, -1))
            if log:
                log(f"第 {i + 1} 页  处理失败：{exc}")
        if progress:
            progress(i + 1, total, f"第 {i + 1}/{total} 页")

    try:
        out.save(dst, deflate=True, garbage=3)
    finally:
        out.close()
        doc.close()

    if report:
        try:
            with open(report, "w", encoding="utf-8") as fh:
                fh.write("PDF 去水印报告\n")
                fh.write(f"输入：{src}\n输出：{dst}\n页数：{total}\n"
                         f"墨迹保护窗：{near}  粉色水印：{'开' if pink else '关'}  "
                         f"紫色水印：{'开' if purple else '关'}  "
                         f"页眉logo：{'清除' if remove_logo else '保留'}\n")
                if stopped:
                    fh.write("（本次被手动停止，以下为已完成部分）\n")
                fh.write("\n")
                fh.write(f"{'页':>5}{'水印清除px':>12}{'logo清除px':>12}"
                         f"{'红保留':>9}{'深保留':>9}{'蓝保留':>9}"
                         f"{'残留px':>9}{'可见残留':>9}{'误伤px':>8}{'  来源':>8}\n")
                for r in rows:
                    fh.write(f"{r[0]:>5}{r[1]:>12}{r[2]:>12}"
                             f"{r[3]:>8.1f}%{r[4]:>8.1f}%{r[5]:>8.1f}%"
                             f"{r[7]:>9}{r[8]:>9}{r[9]:>8}{r[6]:>8}\n")
                fh.write("\n说明：残留px 含 JPEG 振铃（近白、肉眼不可见）；"
                         "可见残留 = min 通道 < 235 的残留像素；"
                         "误伤px = 强内容被涂白的像素数。后两者正常均应为 0。\n")
        except OSError:
            pass
    return rows
