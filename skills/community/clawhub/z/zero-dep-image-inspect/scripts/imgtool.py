# -*- coding: utf-8 -*-
"""零依赖图片工具：PNG 解码 / 双线性缩放 / 裁切 / 写 PNG / 并排对照图。

用于把「本地生成的封面」和「用户截图里的封面」放到同一尺度上比对。
"""
import struct
import zlib


# ------------------------------------------------------------------ 解码
def decode_png(path):
    b = open(path, "rb").read()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", "不是 PNG: %s" % path
    i = 8
    w = h = ct = None
    idat = []
    plte = None
    while i < len(b) - 8:
        ln = struct.unpack(">I", b[i:i + 4])[0]
        typ = b[i + 4:i + 8]
        data = b[i + 8:i + 8 + ln]
        if typ == b"IHDR":
            w, h, bitd, ct, _, _, il = struct.unpack(">IIBBBBB", data)
            assert bitd == 8 and il == 0, "只支持 8bit 非隔行"
        elif typ == b"PLTE":
            plte = data
        elif typ == b"IDAT":
            idat.append(data)
        elif typ == b"IEND":
            break
        i += 12 + ln
    raw = zlib.decompress(b"".join(idat))
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    stride = w * ch
    out = bytearray(h * stride)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 0xFF
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                c = prev[x - ch] if x >= ch else 0
                bb = prev[x]
                p = a + bb - c
                pa, pb, pc = abs(p - a), abs(p - bb), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (bb if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        out[y * stride:(y + 1) * stride] = line
        prev = line
    if ct == 3 and plte:
        rgb = bytearray(w * h * 3)
        for k in range(w * h):
            idx = out[k] * 3
            rgb[k * 3:k * 3 + 3] = plte[idx:idx + 3]
        return w, h, 3, bytes(rgb)
    return w, h, ch, bytes(out)


def to_rgb(w, h, ch, px):
    if ch == 3:
        return px
    out = bytearray(w * h * 3)
    if ch == 4:
        for k in range(w * h):
            o = k * 4
            out[k * 3:k * 3 + 3] = px[o:o + 3]
    elif ch == 1:
        for k in range(w * h):
            v = px[k]
            out[k * 3] = out[k * 3 + 1] = out[k * 3 + 2] = v
    elif ch == 2:
        for k in range(w * h):
            out[k * 3] = out[k * 3 + 1] = out[k * 3 + 2] = px[k * 2]
    return bytes(out)


# ------------------------------------------------------------------ 缩放
def resize(w, h, px, nw, nh):
    """双线性缩放（px 为 RGB 紧凑排列）。"""
    out = bytearray(nw * nh * 3)
    xr = (w - 1) / max(1, nw - 1) if nw > 1 else 0
    yr = (h - 1) / max(1, nh - 1) if nh > 1 else 0
    for y in range(nh):
        sy = y * yr
        y0 = int(sy)
        y1 = min(y0 + 1, h - 1)
        fy = sy - y0
        row0 = y0 * w * 3
        row1 = y1 * w * 3
        orow = y * nw * 3
        for x in range(nw):
            sx = x * xr
            x0 = int(sx)
            x1 = min(x0 + 1, w - 1)
            fx = sx - x0
            o0 = row0 + x0 * 3
            o1 = row0 + x1 * 3
            o2 = row1 + x0 * 3
            o3 = row1 + x1 * 3
            d = orow + x * 3
            for c in range(3):
                a = px[o0 + c] + (px[o1 + c] - px[o0 + c]) * fx
                bb = px[o2 + c] + (px[o3 + c] - px[o2 + c]) * fx
                out[d + c] = int(a + (bb - a) * fy + 0.5)
    return bytes(out)


def crop(w, h, px, x, y, cw, chh):
    """裁切。注意：返回**裸 bytes**（与 resize 一致），不是 (w,h,px)。

    想直接拿去喂 vstack()/write_png() 就用下面的 crop_rgb()，
    否则 `cw, ch, p = crop(...)` 会抛 ValueError（本函数只吐一个值）。
    """
    out = bytearray(cw * chh * 3)
    for j in range(chh):
        sy = min(y + j, h - 1)
        src = (sy * w + x) * 3
        dst = j * cw * 3
        out[dst:dst + cw * 3] = px[src:src + cw * 3]
    return bytes(out)


def crop_rgb(w, h, px, x, y, cw, chh):
    """crop() 的对称三元组版 -> (cw, chh, px)，可直接给 vstack/write_png。"""
    return cw, chh, crop(w, h, px, x, y, cw, chh)


# ------------------------------------------------------------------ 编码
def _chunk(typ, data):
    return (struct.pack(">I", len(data)) + typ + data
            + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))


def write_png(path, w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += px[y * w * 3:(y + 1) * w * 3]
    png = (b"\x89PNG\r\n\x1a\n"
           + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
           + _chunk(b"IEND", b""))
    open(path, "wb").write(png)
    return path


# ------------------------------------------------------------------ 常用
def load_rgb(path):
    w, h, ch, px = decode_png(path)
    return w, h, to_rgb(w, h, ch, px)


def fit_width(path, target_w):
    w, h, px = load_rgb(path)
    nh = max(1, int(round(h * target_w / w)))
    return target_w, nh, resize(w, h, px, target_w, nh), (w, h)


def bbox_nonwhite(path, thresh=235):
    """找出非白区域的外接框（用于从截图里裁出封面）。"""
    w, h, px = load_rgb(path)
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        base = y * w * 3
        for x in range(w):
            o = base + x * 3
            if px[o] < thresh or px[o + 1] < thresh or px[o + 2] < thresh:
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y
    return x0, y0, x1 + 1, y1 + 1


def vstack(items, pad=14, bg=(255, 255, 255)):
    """竖向拼接 [(w,h,px), ...]，宽度取最大值，白色留边。"""
    tw = max(i[0] for i in items)
    th = sum(i[1] for i in items) + pad * (len(items) + 1)
    out = bytearray()
    for _ in range(th * tw):
        out += bytes(bg)
    y = pad
    for (w, h, px) in items:
        x = (tw - w) // 2
        for j in range(h):
            src = j * w * 3
            dst = ((y + j) * tw + x) * 3
            out[dst:dst + w * 3] = px[src:src + w * 3]
        y += h + pad
    return tw, th, bytes(out)
