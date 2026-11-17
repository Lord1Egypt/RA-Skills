#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wechat_dat_decrypt.py — 微信 4.x `.dat` 图片缓存批量解密（通用版）

适用：Windows 微信 4.x（实测 4.1.x）落盘的 V2 头 `.dat` 图片缓存。
源目录只读，所有产物只写到 `--out`。

用法：
    python wechat_dat_decrypt.py --account "<账号目录>" --out "<输出目录>"
    python wechat_dat_decrypt.py --account "<账号目录>" --out "<输出目录>" --code <已知code>

参数：
    --account   账号根目录（含 msg/ config/ db_storage/ 的那一层），只读，必填
    --out       解密产物输出目录，必填（绝不写回 --account）
    --code      已知 code（8~10 位数字）。给了就跳过暴力推导，二次使用秒出
    --wxid      wxid 候选，可重复传；不传则自动从账号目录名等推断
    --timeout   暴力推导超时秒数（默认 900）
    --procs     并发进程数（默认 CPU-1）
    --no-pil    跳过 PIL 图片校验

产物（全部落在 --out）：
    <out>/<账号内相对路径>.<还原扩展名>   解密后的图片
    <out>/decrypt_report.json            统计报告（不含 code / wxid / 绝对路径）
    <out>/secret_hit.json                命中的 code+wxid（本机复用，不要随包外发）
    <out>/decrypt_progress.json          暴力推导进度

流程：探测 .dat → 反推 xor → 枚举 wxid 候选 → 暴力 code（下界 0）
      → 批量解密 → PIL 校验 → decrypt_report.json

依赖：pycryptodome（必需）；Pillow（可选，缺了只跳过图片校验）
"""
import argparse
import collections
import glob
import hashlib
import json
import math
import multiprocessing as mp
import os
import struct
import sys
import time
from pathlib import Path

try:
    from Crypto.Cipher import AES
except ImportError:  # pragma: no cover
    sys.stderr.write("[!] 缺少 pycryptodome，请先安装：pip install pycryptodome\n")
    raise

V2 = b"\x07\x08V2\x08\x07"
HEADER = 0x0F
MAGICS = (b"\xff\xd8\xff", b"\x89PNG", b"GIF8", b"RIFF", b"wxgf", b"II*\x00", b"BM")
FORMAT_BY_MAGIC = {
    b"\xff\xd8\xff": "jpg",
    b"\x89PNG": "png",
    b"GIF8": "gif",
    b"RIFF": "webp",
    b"wxgf": "wxgf",
    b"II*\x00": "tif",
    b"BM": "bmp",
}
FOOTER_BY_MAGIC = {
    "jpg": b"\xff\xd9",
    "png": b"IEND",
    "gif": b"\x00;",
}
CODE_LO = 0                 # 下界必须是 0（code 是 8 位量级，从 1e9 起跑会空手）
CODE_HI = 10 ** 10          # 覆盖 1~10 位 code
PROBE_CLASSES = 16384       # 每个任务覆盖的等价类数（步长 256）
EXCLUDE_DIRS = ("cache", "bubble")  # 这些目录下的 .dat 不适合当探针


# ---------------------------------------------------------------- 基础工具

def align_block(n: int) -> int:
    """与已验证实现逐位一致的 16 字节对齐（实测密文段长度恒多出一个整块）。"""
    return n - ~(~n % 16)


def derive_key(code, wxid: str) -> bytes:
    return hashlib.md5((str(int(code)) + wxid).encode("utf-8")).hexdigest()[:16].encode("ascii")


def probe_globs(account: Path):
    """探针候选路径：优先 msg/attach/<会话>/<月份>/Img/*.dat（只有这些才是真图片）。"""
    patterns = [
        "msg/attach/*/*/Img/*.dat",
        "msg/attach/*/*/*/Img/*.dat",
        "msg/attach/*/Img/*.dat",
        "msg/attach/**/*.dat",
        "**/*.dat",
    ]
    seen = set()
    for pat in patterns:
        hits = []
        try:
            for p in sorted(account.glob(pat)):
                if not p.is_file():
                    continue
                key = str(p)
                if key in seen:
                    continue
                seen.add(key)
                low = [s.lower() for s in p.parts]
                if any(x in EXCLUDE_DIRS for x in low):
                    continue
                hits.append(p)
        except (OSError, ValueError):
            continue
        if len(hits) >= 3:
            # 只要 Img 目录下的（.lesson：cache/Bubble 下的 .dat 不是图片）
            img_only = [h for h in hits if "img" in [s.lower() for s in h.parent.parts]]
            return img_only if len(img_only) >= 3 else hits
    return []


def collect_probe_blocks(account: Path, need: int = 6):
    """返回 (探针文件列表, 各自 16 字节密文块)。"""
    files, blocks, seen = [], [], set()
    for p in probe_globs(account):
        try:
            size = p.stat().st_size
            if size <= 3000:
                continue
            with open(p, "rb") as f:
                head = f.read(HEADER + 16)
        except OSError:
            continue
        if head[:6] != V2:
            continue
        aes_size, xor_size = struct.unpack_from("<LL", head, 6)
        if aes_size < 32 or HEADER + aes_size + 16 > size:
            continue
        blk = head[HEADER:HEADER + 16]
        if blk in seen:
            continue
        seen.add(blk)
        files.append(p)
        blocks.append(blk)
        if len(blocks) >= need:
            break
    return files, blocks


def read_tail_sample(path: Path, max_tail: int = 16):
    """读文件尾部（xor 混淆区），返回 (尾字节, xor_size)。"""
    try:
        size = path.stat().st_size
        with open(path, "rb") as f:
            head = f.read(HEADER + 16)
            if head[:6] != V2:
                return None, 0
            _aes_size, xor_size = struct.unpack_from("<LL", head, 6)
            if xor_size < 2:
                return None, xor_size
            take = min(xor_size, max_tail)
            f.seek(size - take)
            return f.read(take), xor_size
    except OSError:
        return None, 0


def infer_xor(paths):
    """尾字节反推 xor：明文尾部有固定结束标记（jpg/png/gif），逐字节异或后应还原。"""
    votes = collections.Counter()
    tried = 0
    for p in paths:
        tail, xor_size = read_tail_sample(p)
        if not tail or len(tail) < 3:
            continue
        tried += 1
        for x in range(256):
            dec = bytes(b ^ x for b in tail)
            if dec.endswith(b"\xff\xd9") or dec[-8:-4] == b"IEND" or dec.endswith(b"\x00;"):
                votes[x] += 1
    if not votes:
        return None, 0, tried
    best, score = votes.most_common(1)[0]
    return best, score, tried


def refine_xor(key: bytes, paths):
    """拿到 key 后再复核一次 xor：整文件解密 + 结束标记校验，256 个候选里挑得分最高的。"""
    scores = collections.Counter()
    usable = 0
    for p in paths[:40]:
        try:
            size = p.stat().st_size
            if size > (8 << 20):
                continue
            data = p.read_bytes()
        except OSError:
            continue
        out, fmt, _err = decrypt_blob(data, key, 0)
        if out is None or fmt not in FOOTER_BY_MAGIC:
            continue
        usable += 1
        _aes_size, xor_size = struct.unpack_from("<LL", data, 6)
        if xor_size < 2 or xor_size > len(out):
            continue
        want = FOOTER_BY_MAGIC[fmt]
        tail = data[len(data) - min(xor_size, 16):]
        for x in range(256):
            dec = bytes(b ^ x for b in tail)
            if fmt == "jpg" and dec.endswith(b"\xff\xd9"):
                scores[x] += 1
            elif fmt == "png" and dec[-8:-4] == b"IEND":
                scores[x] += 1
            elif fmt == "gif" and dec.endswith(b"\x00;"):
                scores[x] += 1
    if not scores:
        return None
    return scores.most_common(1)[0][0]


def decrypt_blob(data: bytes, key: bytes, xor: int):
    """单文件解密。返回 (明文, 扩展名, 错误原因)。"""
    if len(data) < HEADER or data[:6] != V2:
        return None, None, "非V2头"
    aes_size, xor_size = struct.unpack_from("<LL", data, 6)
    if aes_size < 16:
        return None, None, "尺寸异常"
    # 密文段长度：首选与已验证实现完全一致的整块对齐；该布局不成立时再退而求其次
    raw_size = len(data) - xor_size - HEADER - align_block(aes_size)
    chosen = None
    if align_block(aes_size) > 0 and align_block(aes_size) % 16 == 0 \
            and HEADER + align_block(aes_size) <= len(data) and raw_size >= 0:
        a = align_block(aes_size)
        chosen = a
    else:
        for a in (((aes_size + 15) // 16) * 16, aes_size, aes_size + 16):
            if a <= 0 or a % 16 or HEADER + a > len(data):
                continue
            if len(data) - xor_size - HEADER - a < 0:
                continue
            chosen = a
            break
    if chosen is None:
        return None, None, "布局异常"
    a = chosen
    off = HEADER + a
    raw_end = len(data) - xor_size if xor_size > 0 else len(data)
    if raw_end < off:
        return None, None, "布局异常"
    try:
        dec = AES.new(key, AES.MODE_ECB).decrypt(data[HEADER:HEADER + a])[:aes_size]
    except Exception as exc:  # noqa: BLE001
        return None, None, "AES错误:" + str(exc)[:40]
    out = dec + data[off:raw_end] + bytes(b ^ xor for b in data[raw_end:])
    for m, fmt in FORMAT_BY_MAGIC.items():
        if out[:len(m)] == m:
            return out, fmt, None
    return None, None, "magic未知:" + out[:8].hex()


# ------------------------------------------------------------ key 解析部分

def discover_wxids(account: Path, extra=()):
    """wxid 候选：显式 --wxid 优先，其次从账号目录名与少量配置文件名里推断。"""
    out = []

    def push(v):
        v = (v or "").strip()
        if v and v not in out and len(out) < 16:
            out.append(v)

    for v in (extra or []):
        push(v)

    base = account.name
    push(base)
    if "_" in base:
        push(base.split("_")[0])
    import re
    m = re.match(r"^(.*)_[0-9a-fA-F]{4,16}$", base)
    if m:
        push(m.group(1))
    for m in re.finditer(r"wxid_[A-Za-z0-9_]{4,32}", base):
        push(m.group(0))

    # 目录/文件名里的 wxid_* 与 32 位十六进制 token（浅层，限量）
    import re as _re
    scanned, names = 0, []
    try:
        for dp, dns, fns in os.walk(account):
            depth = Path(dp).relative_to(account).parts
            if len(depth) > 3:
                dns[:] = []
                continue
            names.extend(dns)
            names.extend(fns)
            scanned += 1
            if scanned > 4000:
                break
    except OSError:
        pass
    for nm in names:
        for mm in _re.finditer(r"wxid_[A-Za-z0-9_]{4,32}", nm):
            push(mm.group(0))

    # 少量小体积配置文件里扫 wxid_*
    try:
        cfg_files = []
        for sub in ("", "config", "resource"):
            d = account / sub
            if d.is_dir():
                cfg_files.extend([p for p in d.iterdir() if p.is_file()])
        used = 0
        for p in cfg_files:
            if used >= 60:
                break
            try:
                if p.stat().st_size > (1 << 20):
                    continue
                used += 1
                txt = p.read_bytes()[: (1 << 20)].decode("utf-8", "ignore")
            except OSError:
                continue
            for mm in _re.finditer(r"wxid_[A-Za-z0-9_]{4,32}", txt):
                push(mm.group(0))
    except OSError:
        pass
    return out


def verify_key(code, wxid: str, blocks) -> bool:
    if not blocks:
        return False
    key = derive_key(code, wxid)
    try:
        aes = AES.new(key, AES.MODE_ECB)
    except Exception:  # noqa: BLE001
        return False
    for b in blocks:
        out = aes.decrypt(b)
        if not any(out.startswith(m) for m in MAGICS):
            return False
    return True


def verify_full(code, wxid: str, paths, max_files=24):
    """命中后整文件复核：解密 + magic + 结束标记。返回 (是否通过, 摘要)"""
    key = derive_key(code, wxid)
    xor = int(code) & 0xFF
    good = bad = 0
    for p in paths:
        try:
            if p.stat().st_size > (4 << 20):
                continue
            data = p.read_bytes()
        except OSError:
            continue
        out, fmt, _err = decrypt_blob(data, key, xor)
        ok = out is not None
        if ok and fmt == "jpg" and not out.endswith(b"\xff\xd9"):
            ok = False
        if ok and fmt == "png" and out[-8:-4] != b"IEND":
            ok = False
        if ok:
            good += 1
        else:
            bad += 1
        if good + bad >= max_files:
            break
    return good >= 3 and good >= bad * 2, "good=%d bad=%d" % (good, bad)


_BLOCKS = None


def _init_worker(blocks):
    global _BLOCKS
    _BLOCKS = blocks


def _worker(task):
    start, stop, wxid = task
    md5 = hashlib.md5
    blocks = _BLOCKS
    b0 = blocks[0]
    for c in range(start, stop, 256):
        k = md5((str(c) + wxid).encode("utf-8")).hexdigest()[:16].encode("ascii")
        aes = AES.new(k, AES.MODE_ECB)
        if not any(aes.decrypt(b0).startswith(m) for m in MAGICS):
            continue
        if all(any(aes.decrypt(b).startswith(m) for m in MAGICS) for b in blocks[1:]):
            return c, wxid
    return None


def brute_code(blocks, wxids, out_dir: Path, timeout: int, procs: int, first: int):
    """暴力推导 code（下界 0）。返回 (code|None, wxid|None, 状态, 耗时)。"""
    first = max(CODE_LO, first & 0xFF)   # code 的低 8 位 == xor，等价类步长 256
    span = PROBE_CLASSES * 256
    n_chunk = max(1, int(math.ceil((CODE_HI - first) / float(span))))
    tasks = []
    for i in range(n_chunk):
        start = first + i * span
        stop = min(start + span, CODE_HI)
        for w in wxids:
            tasks.append((start, stop, w))
    procs = max(1, procs)
    t0 = time.time()
    done = 0
    hit = None
    status = "miss"
    prog_path = out_dir / "decrypt_progress.json"
    with mp.Pool(procs, initializer=_init_worker, initargs=(blocks,)) as pool:
        for r in pool.imap_unordered(_worker, tasks):
            done += 1
            if r:
                code, wxid = r
                ok, detail = verify_full(code, wxid, _VERIFY_PATHS)
                if ok:
                    hit = (code, wxid)
                    status = "hit"
                    pool.terminate()
                    break
            if done % 25 == 0:
                el = time.time() - t0
                _write_json(prog_path, {"status": "running", "tasks_done": done,
                                         "tasks_total": len(tasks),
                                         "elapsed_sec": round(el, 1)})
            if time.time() - t0 > timeout:
                status = "timeout"
                pool.terminate()
                break
    _write_json(prog_path, {"status": status, "tasks_done": done,
                            "tasks_total": len(tasks),
                            "elapsed_sec": round(time.time() - t0, 1)})
    code, wxid = (hit if hit else (None, None))
    return code, wxid, status, round(time.time() - t0, 1)


_VERIFY_PATHS = []


def _write_json(path: Path, obj):
    try:
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


# ------------------------------------------------------------ 批量解密部分

def batch_decrypt(account: Path, out_dir: Path, key: bytes, xor: int):
    files = sorted(p for p in account.glob("**/*.dat") if p.is_file())
    ok = fail = non_v2 = 0
    errors = collections.Counter()
    formats = collections.Counter()
    outputs = []
    t0 = time.time()
    for i, p in enumerate(files):
        rel = p.relative_to(account)
        try:
            data = p.read_bytes()
        except OSError:
            fail += 1
            errors["读取失败"] += 1
            continue
        if len(data) < HEADER or data[:6] != V2:
            non_v2 += 1
            errors["非V2头"] += 1
            continue
        out, fmt, err = decrypt_blob(data, key, xor)
        if out is None:
            fail += 1
            errors[err or "未知"] += 1
            continue
        target = out_dir / (str(rel)[:-4] + "." + fmt)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            stem = str(target.with_suffix(""))
            k = 1
            while Path(f"{stem}-v{k}.{fmt}").exists():
                k += 1
            target = Path(f"{stem}-v{k}.{fmt}")
        try:
            target.write_bytes(out)
        except OSError:
            fail += 1
            errors["写入失败"] += 1
            continue
        ok += 1
        formats[fmt] += 1
        outputs.append(target)
        if (i + 1) % 500 == 0:
            print("[.] progress %d/%d ok=%d fail=%d %.0fs"
                  % (i + 1, len(files), ok, fail, time.time() - t0), flush=True)
    return files, outputs, ok, fail, non_v2, errors, formats, round(time.time() - t0, 1)


def pil_check(outputs):
    try:
        from PIL import Image
    except ImportError:
        return {"available": False, "ok": 0, "fail": 0, "skipped_wxgf": 0, "fail_samples": []}
    ok = fail = skip = 0
    samples = []
    for p in outputs:
        if p.suffix.lower() == ".wxgf":
            skip += 1
            continue
        try:
            with Image.open(p) as im:
                im.verify()
            ok += 1
        except Exception as exc:  # noqa: BLE001
            fail += 1
            if len(samples) < 10:
                samples.append(p.name + ":" + str(exc)[:60])
    return {"available": True, "ok": ok, "fail": fail,
            "skipped_wxgf": skip, "fail_samples": samples}


# ---------------------------------------------------------------- 主流程

def main(argv=None):
    ap = argparse.ArgumentParser(description="微信 4.x .dat 图片缓存批量解密")
    ap.add_argument("--account", required=True, help="账号根目录（只读）")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--code", default=None, help="已知 code（8~10 位），给了就跳过暴力")
    ap.add_argument("--wxid", action="append", default=[], help="wxid 候选，可重复")
    ap.add_argument("--timeout", type=int, default=900, help="暴力推导超时秒数")
    ap.add_argument("--procs", type=int, default=0, help="并发进程数（0=CPU-1）")
    ap.add_argument("--no-pil", action="store_true", help="跳过 PIL 校验")
    args = ap.parse_args(argv)

    account = Path(args.account).expanduser()
    out_dir = Path(args.out).expanduser()
    if not account.is_dir():
        sys.stderr.write("[!] 账号目录不存在: %s\n" % account)
        return 1
    try:
        out_dir.resolve().relative_to(account.resolve())
        sys.stderr.write("[!] --out 不能位于 --account 内部（源目录只读）\n")
        return 1
    except (ValueError, OSError):
        pass
    out_dir.mkdir(parents=True, exist_ok=True)

    t_start = time.time()
    files, blocks = collect_probe_blocks(account)
    if len(blocks) < 3:
        sys.stderr.write("[!] 探针不足（找到 %d 个有效 .dat），无法校验密钥\n" % len(files))
        _write_json(out_dir / "decrypt_report.json",
                    {"schema": "wechat-dat-decrypt/1", "status": "no_probe",
                     "probe_files": len(files)})
        return 2
    print("[*] 探针文件 %d 个" % len(files), flush=True)

    xor, xor_score, tail_tried = infer_xor(files)
    if xor is None:
        # 放宽探针范围再试一次（cache 等目录也纳入），尾标记仍拿不到就只能报边界
        broad = sorted(p for p in account.glob("**/*.dat") if p.is_file())[:400]
        xor, xor_score, tail_tried = infer_xor(broad)
    if xor is None:
        sys.stderr.write("[!] 尾字节反推 xor 失败：本账号 .dat 里没有 jpg/png/gif 结束标记可反推。\n"
                         "    请显式 --code 或 --wxid 后重试。\n")
        _write_json(out_dir / "decrypt_report.json",
                    {"schema": "wechat-dat-decrypt/1", "status": "no_xor",
                     "probe_files": len(files)})
        return 2
    print("[*] 反推 xor=0x%02x（尾标记命中 %d/%d）" % (xor, xor_score, tail_tried), flush=True)

    wxids = discover_wxids(account, args.wxid)
    print("[*] wxid 候选 %d 个" % len(wxids), flush=True)

    code = None
    hit_wxid = None
    brute_info = None
    if args.code:
        code = int(args.code)
        for w in wxids:
            if verify_key(code, w, blocks):
                hit_wxid = w
                break
        if hit_wxid is None:
            sys.stderr.write("[!] --code 给了，但所有 wxid 候选都过不了探针校验；"
                             "请补 --wxid\n")
            _write_json(out_dir / "decrypt_report.json",
                        {"schema": "wechat-dat-decrypt/1", "status": "wxid_mismatch",
                         "wxid_candidates": len(wxids), "xor": xor})
            return 4
        print("[*] 使用给定 code + 自动命中的 wxid（跳过暴力）", flush=True)
        key_source = "provided"
    else:
        global _VERIFY_PATHS
        _VERIFY_PATHS = files
        ncpu = args.procs or max(1, (os.cpu_count() or 4) - 1)
        print("[*] 开始暴力推导 code（空间 0~1e10，低 8 位按 xor 对齐），并发 %d" % ncpu,
              flush=True)
        code, hit_wxid, status, el = brute_code(blocks, wxids, out_dir, args.timeout,
                                                ncpu, xor)
        brute_info = {"status": status, "elapsed_sec": el}
        if code is None:
            sys.stderr.write("[!] 暴力未命中（状态 %s）。可补 --wxid 或 --code 重试\n" % status)
            _write_json(out_dir / "decrypt_report.json",
                        {"schema": "wechat-dat-decrypt/1", "status": status,
                         "wxid_candidates": len(wxids), "xor": xor,
                         "elapsed_sec": round(time.time() - t_start, 1)})
            return 2
        key_source = "brute"
        print("[*] 暴力命中，耗时 %.1fs" % el, flush=True)

    if xor is None:
        xor = code & 0xFF
    refined = refine_xor(derive_key(code, hit_wxid), files)
    if refined is not None and refined != xor:
        print("[*] xor 复核修正：0x%02x -> 0x%02x" % (xor, refined), flush=True)
        xor = refined

    key = derive_key(code, hit_wxid)
    # 命中结果只写 --out（本机复用），绝不写进技能包目录
    _write_json(out_dir / "secret_hit.json",
                {"code": int(code), "wxid": hit_wxid, "xor": int(code) & 0xFF,
                 "hit_at": time.strftime("%Y-%m-%d %H:%M:%S")})
    print("[*] 密钥已写入 --out/secret_hit.json（复用时用 --code 直接跳过暴力）", flush=True)

    dat_files, outputs, ok, fail, non_v2, errors, formats, el = batch_decrypt(
        account, out_dir, key, xor)
    pil = {"available": False, "ok": 0, "fail": 0, "skipped_wxgf": 0, "fail_samples": []}
    if not args.no_pil:
        pil = pil_check(outputs)

    report = {
        "schema": "wechat-dat-decrypt/1",
        "status": "ok" if fail == 0 else "partial",
        "key_source": key_source,
        "wxid_candidates": len(wxids),
        "xor": xor,
        "probe_files": len(files),
        "brute": brute_info,
        "dat_total": len(dat_files),
        "decrypted_ok": ok,
        "decrypted_fail": fail,
        "skipped_non_v2": non_v2,
        "errors": dict(errors),
        "formats": dict(formats),
        "pil": pil,
        "decrypt_elapsed_sec": el,
        "total_elapsed_sec": round(time.time() - t_start, 1),
        "source_readonly": True,
    }
    _write_json(out_dir / "decrypt_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 0 if fail == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
