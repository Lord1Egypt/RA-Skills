#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 CODE + WXID 是否正确：拿真实 .dat 试解，magic 命中即对。
用法: python3 wx_probe.py --code 1234567890 --wxid wxid_xxx --dat 某个.dat
"""
import hashlib, struct, argparse, os, glob
from Crypto.Cipher import AES
from Crypto.Util import Padding

MAGIC = {b'\xFF\xD8\xFF': 'jpg', b'\x89PNG': 'png', b'GIF8': 'gif', b'RIFF': 'webp',
         b'wxgf': 'hevc', b'II\x2A\x00': 'tif', b'BM': 'bmp'}
V2 = b'\x07\x08V2\x08\x07'
HEADER = 0x0F

def align(n): return n - ~(~n % 16)

def decrypt_full(data, key, xor):
    if len(data) < HEADER or data[:6] != V2:
        return None, "非V2头"
    aes_size, xor_size = struct.unpack_from('<LL', data, 6)
    a = align(aes_size)
    if a <= 0 or HEADER + a > len(data):
        return None, "尺寸异常"
    aes_c = data[HEADER:HEADER + a]
    off = HEADER + a
    raw_end = len(data) - xor_size if xor_size > 0 else len(data)
    if raw_end < off:
        return None, "布局异常"
    raw, xord = data[off:raw_end], data[raw_end:]
    dec = AES.new(key, AES.MODE_ECB).decrypt(aes_c)
    try: dec = Padding.unpad(dec, 16)
    except ValueError: pass
    return dec + raw + bytes(b ^ xor for b in xord), None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True, help="账号码 kvcomm_code（10位数字）")
    ap.add_argument("--wxid", required=True, help="解密用 wxid（目录名去掉最后一段后缀）")
    ap.add_argument("--dat", help="指定一个 .dat 文件")
    ap.add_argument("--src", help="或指定含 .dat 的目录（取第一个）")
    a = ap.parse_args()

    key = hashlib.md5((a.code + a.wxid).encode()).hexdigest()[:16].encode()
    xor = int(a.code) & 0xFF
    print(f"KEY = {key.decode()}   XOR = {xor:#04x}")

    path = a.dat
    if not path and a.src:
        hits = glob.glob(os.path.join(a.src, "**", "*.dat"), recursive=True)
        path = hits[0] if hits else None
    if not path or not os.path.isfile(path):
        raise SystemExit("请用 --dat 指定一个 .dat 文件（或 --src 目录）")

    data = open(path, 'rb').read()
    out, err = decrypt_full(data, key, xor)
    if err:
        print(f"❌ {err}  → 文件损坏或头格式已变（微信升级？）")
        raise SystemExit(1)
    for m, f in MAGIC.items():
        if out[:len(m)] == m:
            print(f"✅ 成功！magic={m[:4]} → 格式={f}，解出 {len(out)} 字节")
            print("   CODE 与 WXID 都正确，可跑 wx_decrypt.py 批量解密")
            return
    print(f"❌ magic未知: {out[:8].hex()}  → CODE 或 WXID 不对")
    print("   换 CODE 或核对 wxid（用 wx_locate.py 查）再试")
    raise SystemExit(2)

if __name__ == "__main__":
    main()
