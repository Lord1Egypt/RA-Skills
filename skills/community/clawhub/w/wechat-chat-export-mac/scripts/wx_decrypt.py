#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量解密微信图片 .dat → jpg/png/webp/gif/hevc(→jpg)。
用法:
  python3 wx_decrypt.py --code 1234567890 --wxid wxid_xxx \
      --src <会话hash>/<YYYY-MM>/Img --dst ./out [--no-transcode]
输出:
  out/full/   原图（非 _t.dat）
  out/thumb/  缩略图（_t.dat）
"""
import hashlib, struct, argparse, os, glob, json, subprocess, collections
from Crypto.Cipher import AES
from Crypto.Util import Padding

MAGIC = {b'\xFF\xD8\xFF': 'jpg', b'\x89PNG': 'png', b'GIF8': 'gif', b'RIFF': 'webp',
         b'wxgf': 'hevc', b'II\x2A\x00': 'tif', b'BM': 'bmp'}
V2, HEADER = b'\x07\x08V2\x08\x07', 0x0F
def align(n): return n - ~(~n % 16)

def decrypt(data, key, xor):
    if len(data) < HEADER or data[:6] != V2:
        return None, None, "非V2头"
    aes_size, xor_size = struct.unpack_from('<LL', data, 6)
    a = align(aes_size)
    if a <= 0 or HEADER + a > len(data):
        return None, None, "尺寸异常"
    aes_c = data[HEADER:HEADER + a]
    off = HEADER + a
    raw_end = len(data) - xor_size if xor_size > 0 else len(data)
    if raw_end < off:
        return None, None, "布局异常"
    raw, xord = data[off:raw_end], data[raw_end:]
    dec = AES.new(key, AES.MODE_ECB).decrypt(aes_c)
    try: dec = Padding.unpad(dec, 16)
    except ValueError: pass
    out = dec + raw + bytes(b ^ xor for b in xord)
    for m, f in MAGIC.items():
        if out[:len(m)] == m:
            return out, f, None
    return None, None, "magic未知:" + out[:8].hex()

def transcode(wxgf_path, jpg_path):
    """wxgf = 微信裸 HEVC，必须 -f hevc"""
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "hevc",
                        "-i", wxgf_path, "-frames:v", "1", jpg_path],
                       capture_output=True, text=True, timeout=60)
    return r.returncode == 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True)
    ap.add_argument("--wxid", required=True)
    ap.add_argument("--src", required=True, help="含 *.dat 的目录")
    ap.add_argument("--dst", required=True)
    ap.add_argument("--no-transcode", action="store_true", help="不把 wxgf 转 jpg")
    a = ap.parse_args()

    key = hashlib.md5((a.code + a.wxid).encode()).hexdigest()[:16].encode()
    xor = int(a.code) & 0xFF
    files = sorted(glob.glob(os.path.join(a.src, "**", "*.dat"), recursive=True))
    if not files:
        raise SystemExit(f"目录里没有 .dat: {a.src}")

    os.makedirs(os.path.join(a.dst, "full"), exist_ok=True)
    os.makedirs(os.path.join(a.dst, "thumb"), exist_ok=True)
    ok = fail = 0
    errs, byfmt = collections.Counter(), collections.Counter()

    for p in files:
        base = os.path.basename(p)
        stem = base[:-4] if base.endswith(".dat") else base
        if stem.endswith("_t"):
            stem, sub = stem[:-2], "thumb"
        else:
            sub = "full"
        try:
            data = open(p, "rb").read()
        except OSError:
            fail += 1; errs["读取失败"] += 1; continue
        out, fmt, err = decrypt(data, key, xor)
        if out is None:
            fail += 1; errs[err] += 1; continue
        if fmt == "hevc" and not a.no_transcode:
            raw = os.path.join(a.dst, sub, stem + ".wxgf")
            dstp = os.path.join(a.dst, sub, stem + ".jpg")
            open(raw, "wb").write(out)
            if transcode(raw, dstp):
                os.remove(raw); ok += 1; byfmt["hevc→jpg"] += 1
            else:
                os.remove(raw); fail += 1; errs["ffmpeg转码失败"] += 1
            continue
        open(os.path.join(a.dst, sub, stem + "." + fmt), "wb").write(out)
        ok += 1; byfmt[fmt] += 1

    print(json.dumps({"key": key.decode(), "xor": hex(xor), "total": len(files),
                      "ok": ok, "fail": fail, "formats": dict(byfmt),
                      "errors": dict(errs)}, ensure_ascii=False, indent=2))
    if fail:
        raise SystemExit(3)

if __name__ == "__main__":
    main()
