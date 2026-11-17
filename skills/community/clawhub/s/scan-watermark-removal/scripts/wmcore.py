# -*- coding: utf-8 -*-
"""扫描件水印清除核心算法。

原理
----
水印是"均匀色 + 均匀透明度"的叠加层：
    观测值 = alpha * 水印色 + (1 - alpha) * 纸面(白)
所以水印像素在色度空间里落在一条**从白点出发的射线**上。真实内容（红笔迹、
黑字、蓝色表格线、灰色插图）的色度方向与水印不同或亮度不在纸面区间，
因此可以用"色相锥 + 亮度带 + 纸面邻域 + 墨迹邻近保护"把水印像素单独挑出来
漂白，笔迹毫发无损。

实测色度指纹（本项目素材）：
    粉色水印   r-g ≈ 12~62, b-g ≈ 0        (讲义扫描件，红微信水印)
    紫色水印   b-g ≈ 5~20, r-g ≈ 0        (PDF 提取页，蓝紫"唯一购买微信"水印)
    蓝色表格线 r-g ≈ -20, b-g ≈ 18~50     (青色，靠 r-g 负值区分)
    灰色插图   r-g ≈ 1,  b-g ≈ 18, 亮度 < 180 (靠亮度下限排除)

接口
----
    process_image()   处理单张图
    batch_process()   批处理 + 进度/日志回调 + 报告
    residue_count()   复核：纸上残留水印像素数
"""
import os
import re

import numpy as np
from PIL import Image

# ---- 内容保护阈值 -------------------------------------------------------
INK_DARK = 150       # 最小通道低于此值视为深色墨迹
INK_RED_G = 55       # r-g 超过此值且 r>INK_RED_R 视为饱和红笔迹
INK_RED_R = 110
PAPER_LIGHT = 225    # 亮度高于此值视为"纸面/浅色"（水印自身也算纸面）
PAPER_MIN = 232      # 近乎纯白（复核用）
RESIDUE_LIMIT = 50

# ---- 颜色窗口（实测标定） ----------------------------------------------
PINK = dict(lo=6, hi=62, perp=10, mx_min=168, mn_min=148)
PURPLE = dict(lo=4, hi=32, perp=10, mx_min=180, mn_min=165)
FAINT = dict(lo=3, hi=24, mx_min=238, mn_min=230)

IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff")


def _box_sum(mask, size):
    """size×size 中心窗口内 True 计数（边缘裁剪）与窗口面积。"""
    m = mask.astype(np.int64)
    c = np.cumsum(np.cumsum(m, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    H, W = m.shape
    r = size // 2
    ys, xs = np.arange(H), np.arange(W)
    y0 = np.clip(ys - r, 0, H); y1 = np.clip(ys + r + 1, 0, H)
    x0 = np.clip(xs - r, 0, W); x1 = np.clip(xs + r + 1, 0, W)
    area = (y1 - y0)[:, None] * (x1 - x0)[None, :]
    s = (c[y1[:, None], x1[None, :]] - c[y0[:, None], x1[None, :]]
         - c[y1[:, None], x0[None, :]] + c[y0[:, None], x0[None, :]])
    return s, area


def ink_mask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return ((np.minimum(np.minimum(r, g), b) < INK_DARK)
            | ((r - g > INK_RED_G) & (r > INK_RED_R)))


def _base_mask(a, near):
    """公共前提：不在墨迹旁 + 处于纸面邻域 + 亮度在纸面区间。"""
    r, g, b = a[:, :, 0].astype(np.int32), a[:, :, 1].astype(np.int32), a[:, :, 2].astype(np.int32)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    near_ink = _box_sum(ink_mask(a), near)[0] > 0
    paperish = mx >= PAPER_LIGHT
    s, area = _box_sum(paperish, 9)
    paper_frac = s / np.maximum(area, 1)
    return (~near_ink) & (paper_frac >= 0.5), mx, mn, (r - g), (b - g)


def watermark_mask(a, near=5, pink=True, purple=True):
    """水印像素掩膜。"""
    ok, mx, mn, cg_r, cg_b = _base_mask(a, near)
    wm = np.zeros(a.shape[:2], bool)
    if pink:
        wm |= (ok & (mx >= PINK["mx_min"]) & (mx <= 255) & (mn >= PINK["mn_min"])
               & (cg_r >= PINK["lo"]) & (cg_r <= PINK["hi"])
               & (np.abs(cg_b) <= PINK["perp"]))
    if purple:
        wm |= (ok & (mx >= PURPLE["mx_min"]) & (mx <= 255) & (mn >= PURPLE["mn_min"])
               & (cg_b >= PURPLE["lo"]) & (cg_b <= PURPLE["hi"])
               & (np.abs(cg_r) <= PURPLE["perp"]))
    # 超淡残留：亮度逼近纸面、色度很弱
    wm |= (ok & (mx >= FAINT["mx_min"]) & (mx <= 255) & (mn >= FAINT["mn_min"])
           & (((cg_r >= FAINT["lo"]) & (cg_r <= FAINT["hi"]) & (np.abs(cg_b) <= 10))
              | ((cg_b >= FAINT["lo"]) & (cg_b <= 14) & (np.abs(cg_r) <= 10))))
    return wm


def process_array(before, near=5, pink=True, purple=True):
    """返回 (处理后数组, 清除像素数)。"""
    wm = watermark_mask(before, near, pink, purple)
    out = before.copy()
    out[wm] = 255
    return out, int(wm.sum())


def _content_counts(a):
    """(红, 深, 蓝) 三类内容像素数。判据故意偏宽，用来做覆盖率参考。"""
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    red = int(((r > 150) & (r - g > 60) & (r - b > 60)).sum())
    dark = int((np.minimum(np.minimum(r, g), b) < 150).sum())
    blue = int(((b - r > 15) & (b - g > 15) & (r - g < -10)).sum())
    return red, dark, blue


def strong_content(a):
    """"确定是内容"的像素——比 _content_counts 严得多。

    用处是回答"到底有没有伤到内容"，而不是"内容像素数变没变"。
    宽判据下的 min<150 会把抗锯齿边缘全算进来，JPEG 一压缩边缘值挪几个单位
    就会"掉出"统计，看起来像内容损失。这里只认真正深/真正艳的像素：

        深色  min < 120
        饱和红 r-g > 90 且 r-b > 90 且 r > 150
        饱和蓝 b-r > 60 且 b-g > 40 且 min < 150

    蓝和深都加了"够暗"约束（min < 120 / 150）：淡蓝 (184,218,255) 这类
    中间调在 JPEG 4:2:0 色度子采样下会被挪动十几到几十个单位，但它本身
    接近纸面亮度，不是需要保护的内容。
    """
    a = a.astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mn = np.minimum(np.minimum(r, g), b)
    return (((mn < 120)
             | ((r - g > 90) & (r - b > 90) & (r > 150))
             | ((b - r > 60) & (b - g > 40) & (mn < 150))))


def erased_content(before, after, exclude=None, whiten_min=210):
    """强内容像素被涂成近白的个数——真正的内容损失。

    exclude 用来排除主动清除的区域（页眉 logo），否则"正确清掉 logo"会被
    误判成"擦掉了内容"。
    """
    strong = strong_content(before)
    if exclude is not None:
        strong &= ~exclude
    if not strong.any():
        return 0
    a = after.astype(int)
    mn = np.minimum(np.minimum(a[:, :, 0], a[:, :, 1]), a[:, :, 2])
    return int((strong & (mn > whiten_min)).sum())


def residue_profile(a, near=5, faint_min=235):
    """纸上残留的水印像素概况，返回 (总数, 其中"够暗能看见"的个数)。

    为什么要分两个数：PNG 输出没有压缩噪声，残留计数直接可用；PDF 输出是
    JPEG，白纸上会出现 1~15 个色度单位的振铃，落进超淡水印窗口后能把计数
    抬到几千，但它们 min 通道都在 240 以上——肉眼绝对看不出。用"暗于
    faint_min 的残留数"判断有没有真水印，比拿总数卡阈值可靠得多。
    """
    wm = watermark_mask(a, near)
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    paper = np.minimum(np.minimum(r, g), b) >= PAPER_MIN
    s, area = _box_sum(paper, 9)
    m = wm & (s >= 0.9 * area)
    if not m.any():
        return 0, 0
    mn = np.minimum(np.minimum(r, g), b)[m]
    return int(m.sum()), int((mn < faint_min).sum())


def residue_count(a, near=5):
    """纸上残留的水印像素数（复核指标）。"""
    return residue_profile(a, near)[0]


def out_name(stem, suffix="_去水印"):
    """name_275.png -> name_去水印_275.png；name.png -> name_去水印.png"""
    m = re.match(r"^(.*)_(\d+)$", stem)
    if m:
        return f"{m.group(1)}{suffix}_{m.group(2)}.png"
    return f"{stem}{suffix}.png"


def list_images(folder, skip_done=True, suffix="_去水印"):
    out = []
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith(IMG_EXTS):
            continue
        if skip_done and suffix and suffix in os.path.splitext(f)[0]:
            continue
        out.append(os.path.join(folder, f))
    return out


def process_image(src, dst, near=5, pink=True, purple=True, extra=None):
    """处理单张图片，返回统计字典。

    extra 是可选的二次清理回调 extra(arr) -> arr，在水印清除之后执行
    （比如清除页眉 logo）。留空则只做水印。

    内容保留率的对比会**排除 extra 主动改动的像素**：页眉 logo 是实心彩色字，
    既满足"红"判据（r-g>60）也满足"深"判据（min<150），不排除的话正确清除
    反而会让保留率凭空掉一截（纯 logo 页甚至会报 0%）。
    """
    before = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    after, cleared = process_array(before, near, pink, purple)
    wm_done = after
    changed = None
    if extra is not None:
        after = extra(after)
        changed = np.any(after.astype(np.int16) != wm_done.astype(np.int16), axis=2)
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    Image.fromarray(after.astype(np.uint8)).save(dst)

    ob = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    nb = np.asarray(Image.open(dst).convert("RGB")).astype(np.int16)
    if changed is not None and changed.any():
        # 排除区膨胀 2px，把抗锯齿晕圈一起排除
        for _ in range(2):
            changed = (changed | np.roll(changed, 1, 0) | np.roll(changed, -1, 0)
                       | np.roll(changed, 1, 1) | np.roll(changed, -1, 1))
        ob = ob.copy()
        nb = nb.copy()
        ob[changed] = 255
        nb[changed] = 255
    (orr, odb, obl), (nrr, ndb, nbl) = _content_counts(ob), _content_counts(nb)
    erased = erased_content(before, nb, exclude=changed)
    return dict(
        cleared=cleared,
        logo=int(changed.sum()) if changed is not None else 0,
        residue=residue_count(nb, near),
        visible_residue=residue_profile(nb, near)[1],
        erased=erased,
        red_keep=100.0 * nrr / orr if orr else 100.0,
        dark_keep=100.0 * ndb / odb if odb else 100.0,
        blue_keep=100.0 * nbl / obl if obl else 100.0,
    )


def batch_process(input_path, output_dir, near=5, suffix="_去水印", skip_done=True,
                  pink=True, purple=True, extra=None, progress=None, log=None, report=None,
                  should_stop=None):
    """批处理。progress(done, total, name) / log(str) 为回调；
    should_stop() 返回 True 时中断（已处理的文件保留）。"""
    if os.path.isfile(input_path):
        files = [input_path]
        base = os.path.dirname(os.path.abspath(input_path))
    else:
        files = list_images(input_path, skip_done, suffix)
        base = os.path.abspath(input_path)
    os.makedirs(output_dir, exist_ok=True)

    total = len(files)
    rows = []
    stopped = False
    for i, f in enumerate(files, 1):
        if should_stop is not None and should_stop():
            stopped = True
            break
        name = os.path.basename(f)
        try:
            dst = os.path.join(output_dir, out_name(os.path.splitext(name)[0], suffix))
            st = process_image(f, dst, near, pink, purple, extra)
            rows.append((name, st["cleared"], st["logo"], st["residue"],
                         st["red_keep"], st["dark_keep"], st["blue_keep"],
                         st["visible_residue"], st["erased"]))
            if log:
                log(f"{name}  清除={st['cleared']}  logo={st['logo']}  "
                    f"红={st['red_keep']:.1f}%  深={st['dark_keep']:.1f}%  "
                    f"蓝={st['blue_keep']:.1f}%  残留={st['residue']}"
                    f"(可见 {st['visible_residue']})  误伤={st['erased']}")
        except Exception as exc:
            rows.append((name, 0, 0, -1, 0.0, 0.0, 0.0, -1, -1))
            if log:
                log(f"{name}  处理失败：{exc}")
        if progress:
            progress(i, total, name)

    if report:
        try:
            with open(report, "w", encoding="utf-8") as fh:
                fh.write("扫描件水印清除报告\n")
                fh.write(f"输入：{base}\n输出：{output_dir}\n"
                         f"墨迹保护窗：{near}  粉色水印：{'开' if pink else '关'}  "
                         f"紫色水印：{'开' if purple else '关'}\n")
                if stopped:
                    fh.write("（本次被手动停止，以下为已完成部分）\n")
                fh.write("\n")
                fh.write(f"{'文件':<44}{'清除px':>9}{'logo px':>9}{'残留px':>8}"
                         f"{'可见残留':>9}{'误伤px':>8}"
                         f"{'红保留':>8}{'深保留':>8}{'蓝保留':>8}\n")
                for row in rows:
                    fh.write(f"{row[0]:<44}{row[1]:>9}{row[2]:>9}{row[3]:>8}"
                             f"{row[7]:>9}{row[8]:>8}"
                             f"{row[4]:>7.1f}%{row[5]:>7.1f}%{row[6]:>7.1f}%\n")
                fh.write("\n说明：误伤px = 原本是强内容（深 min<120 / 饱和红 / 饱和蓝）"
                         "却被涂白的像素数，正常必须为 0。\n")
        except OSError:
            pass
    return rows
