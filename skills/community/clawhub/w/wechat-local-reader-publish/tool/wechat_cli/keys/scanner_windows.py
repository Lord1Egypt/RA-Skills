"""Windows 密钥提取 — 支持微信 4.1+ 的只读 runtime Config.Cipher 扫描 + 老版本明文内存扫描

背景：
  微信 4.0.x 一代仍在进程内存里明文缓存 raw key，可用传统内存扫描（find_all_keys
  风格）提取；但微信 4.1+ 起不再明文缓存密钥，老扫描法失效。本模块主路径改为
  **只读**运行时 `com.Tencent.WCDB.Config.Cipher` 扫描 + HMAC 校验，再回退到老版本
  明文 raw key 内存扫描。

版权与归属：
  微信 4.1+ 的 Config.Cipher 只读扫描算法借鉴自开源项目
  TANGandXUE/wcdb-key-tool (https://github.com/TANGandXUE/wcdb-key-tool, MIT License)。
  此处将其适配进本 skill 的公共扫描框架（common.verify_enc_key / collect_db_files /
  cross_verify_keys / save_results），仅做接口整合，未改动其核心技术逻辑；发布时保留
  上述原作者署名与许可证说明。
"""

import ctypes
import ctypes.wintypes as wt
import functools
import os
import re
import struct
import subprocess
import time

from .common import (
    collect_db_files,
    scan_memory_for_keys,
    cross_verify_keys,
    save_results,
    verify_enc_key,
)

print = functools.partial(print, flush=True)

kernel32 = ctypes.windll.kernel32
MEM_COMMIT = 0x1000
READABLE = {0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80}

# ============================================================
# 微信 4.1+ Config.Cipher 只读扫描所需常量（来源见文件头归属说明）
# ============================================================
WINDOWS_CONFIG_CIPHER_NAME = b"com.Tencent.WCDB.Config.Cipher"
WINDOWS_CONFIG_XOR_MASK = bytes.fromhex(
    "d2c7442458020000004889442450488b"
    "450048844c2448488944254048584c24"
)
WINDOWS_MAX_USER_ADDRESS = 0x0000_8000_0000_0000
WINDOWS_CONFIG_BLOB_MAX = 1024
WINDOWS_CONFIG_LITERAL_RE = re.compile(rb"[xX]'([0-9a-fA-F]{64,192})'")


class MBI(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_uint64), ("AllocationBase", ctypes.c_uint64),
        ("AllocationProtect", wt.DWORD), ("_pad1", wt.DWORD),
        ("RegionSize", ctypes.c_uint64), ("State", wt.DWORD),
        ("Protect", wt.DWORD), ("Type", wt.DWORD), ("_pad2", wt.DWORD),
    ]


def _get_pids():
    """返回所有 Weixin.exe 进程的 (pid, mem_kb) 列表，按内存降序"""
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Weixin.exe", "/FO", "CSV", "/NH"],
                       capture_output=True, text=True)
    pids = []
    for line in r.stdout.strip().split('\n'):
        if not line.strip():
            continue
        p = line.strip('"').split('","')
        if len(p) >= 5:
            pid = int(p[1])
            mem = int(p[4].replace(',', '').replace(' K', '').strip() or '0')
            pids.append((pid, mem))
    if not pids:
        raise RuntimeError("Weixin.exe 未运行")
    pids.sort(key=lambda x: x[1], reverse=True)
    for pid, mem in pids:
        print(f"[+] Weixin.exe PID={pid} ({mem // 1024}MB)")
    return pids


def _read_mem(h, addr, sz):
    buf = ctypes.create_string_buffer(sz)
    n = ctypes.c_size_t(0)
    if kernel32.ReadProcessMemory(h, ctypes.c_uint64(addr), buf, sz, ctypes.byref(n)):
        return buf.raw[:n.value]
    return None


def _enum_regions(h):
    regs = []
    addr = 0
    mbi = MBI()
    while addr < 0x7FFFFFFFFFFF:
        if kernel32.VirtualQueryEx(h, ctypes.c_uint64(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
            break
        if mbi.State == MEM_COMMIT and mbi.Protect in READABLE and 0 < mbi.RegionSize < 500 * 1024 * 1024:
            regs.append((mbi.BaseAddress, mbi.RegionSize))
        nxt = mbi.BaseAddress + mbi.RegionSize
        if nxt <= addr:
            break
        addr = nxt
    return regs


# ============================================================
# 微信 4.1+ Config.Cipher 扫描辅助函数（算法归属见文件头）
# ============================================================

def _xor_repeat(data, mask):
    return bytes(value ^ mask[index % len(mask)] for index, value in enumerate(data))


def _u64_from(data, offset):
    if offset < 0 or offset + 8 > len(data):
        return 0
    return struct.unpack_from("<Q", data, offset)[0]


def _probable_32_byte_key(data):
    return len(data) == 32 and len(set(data)) >= 15 and data not in {b"\x00" * 32, b"\xff" * 32}


def _find_bytes_in_regions(regions, read_region, needle):
    addresses = set()
    overlap = max(0, len(needle) - 1)
    for data_base, haystack in _iter_windows_region_chunks(regions, read_region, overlap=overlap):
        pos = haystack.find(needle)
        while pos >= 0:
            addresses.add(data_base + pos)
            pos = haystack.find(needle, pos + 1)
    return addresses


def _iter_windows_region_chunks(regions, read_region, *, chunk_size=2 * 1024 * 1024, overlap=0):
    """Yield readable chunks from Windows process regions with optional overlap."""
    for base, size in regions:
        offset = 0
        tail = b""
        tail_base = base
        while offset < size:
            current_size = min(chunk_size, size - offset)
            chunk = read_region(base + offset, current_size) or b""
            data_base = tail_base if tail else base + offset
            data = tail + chunk
            if data:
                yield data_base, data
                if overlap:
                    tail = data[-overlap:]
                    tail_base = data_base + max(0, len(data) - len(tail))
                else:
                    tail = b""
                    tail_base = base + offset + current_size
            else:
                tail = b""
                tail_base = base + offset + current_size
            offset += current_size


def _windows_v411_config_key_candidates(blob):
    """Extract redaction-safe key/salt candidates from a Config.Cipher blob."""
    if not blob or len(blob) > WINDOWS_CONFIG_BLOB_MAX:
        return []
    decoded = _xor_repeat(blob, WINDOWS_CONFIG_XOR_MASK)
    out = []
    seen = set()
    for match in WINDOWS_CONFIG_LITERAL_RE.finditer(decoded):
        run = match.group(1).decode("ascii").lower()
        starts = [0]
        if len(run) > 96:
            starts.extend(range(0, len(run) - 63, 32))
            starts.append(len(run) - 64)
        for start in dict.fromkeys(starts):
            if start < 0 or start + 64 > len(run):
                continue
            enc_key_hex = run[start:start + 64]
            try:
                enc_key = bytes.fromhex(enc_key_hex)
            except ValueError:
                continue
            if not _probable_32_byte_key(enc_key):
                continue
            embedded_salt = None
            if start + 96 <= len(run):
                embedded_salt = run[start + 64:start + 96]
            item = (enc_key_hex, embedded_salt)
            if item not in seen:
                seen.add(item)
                out.append(item)
    return out


def _verify_windows_direct_key_candidate(enc_key_hex, embedded_salt, db_files, salt_to_dbs,
                                         key_map, remaining_salts):
    if not remaining_salts:
        return 0
    try:
        enc_key = bytes.fromhex(enc_key_hex)
    except ValueError:
        return 0
    if not _probable_32_byte_key(enc_key):
        return 0
    matched = 0
    target_salts = [embedded_salt] if embedded_salt in remaining_salts else list(remaining_salts)
    for salt_hex in target_salts:
        if salt_hex not in remaining_salts:
            continue
        for _rel, _path, _sz, s, page1 in db_files:
            if s == salt_hex and verify_enc_key(enc_key, page1):
                key_map[salt_hex] = enc_key_hex
                remaining_salts.discard(salt_hex)
                matched += 1
                break
    return matched


def _scan_windows_v411_config_cipher(pid, regions, read_region, read_mem, db_files,
                                     salt_to_dbs, key_map, remaining_salts, print_fn):
    """Read-only Windows WeChat 4.1+ Config.Cipher key scan."""
    stats = {
        "needle_occurrences": 0, "string_object_refs": 0, "node_candidates": 0,
        "config_ptr_candidates": 0, "blob99_count": 0, "candidate_count": 0,
        "verified_candidates": 0, "matched_salts": 0,
    }
    needle_addresses = _find_bytes_in_regions(regions, read_region, WINDOWS_CONFIG_CIPHER_NAME)
    stats["needle_occurrences"] = len(needle_addresses)
    if not needle_addresses:
        return stats

    pair_patterns = [
        struct.pack("<Q", addr) + struct.pack("<Q", len(WINDOWS_CONFIG_CIPHER_NAME))
        for addr in needle_addresses
    ]
    seen_config_ptrs = set()
    seen_candidates = set()

    for base, data in _iter_windows_region_chunks(regions, read_region, overlap=0x80):
        if not remaining_salts:
            break
        for pattern in pair_patterns:
            pos = data.find(pattern)
            while pos >= 0:
                stats["string_object_refs"] += 1
                qaddr = base + pos
                node_base = qaddr - 0x10
                node = read_mem(node_base, 0x50)
                if not node or len(node) < 0x40:
                    pos = data.find(pattern, pos + 1)
                    continue
                if _u64_from(node, 0x10) not in needle_addresses or _u64_from(node, 0x18) != len(WINDOWS_CONFIG_CIPHER_NAME):
                    pos = data.find(pattern, pos + 1)
                    continue
                config_ptr = _u64_from(node, 0x28)
                if not (0x10000 <= config_ptr < WINDOWS_MAX_USER_ADDRESS):
                    pos = data.find(pattern, pos + 1)
                    continue
                stats["node_candidates"] += 1
                seen_config_ptrs.add(config_ptr)

                obj = read_mem(config_ptr + 0x88, 0x28)
                if not obj or len(obj) < 0x18:
                    pos = data.find(pattern, pos + 1)
                    continue
                data_ptr = _u64_from(obj, 0x8)
                data_len = _u64_from(obj, 0x10)
                if not (0 < data_len <= WINDOWS_CONFIG_BLOB_MAX and 0x10000 <= data_ptr < WINDOWS_MAX_USER_ADDRESS):
                    pos = data.find(pattern, pos + 1)
                    continue
                blob = read_mem(data_ptr, int(data_len))
                if not blob or len(blob) != data_len:
                    pos = data.find(pattern, pos + 1)
                    continue
                if data_len == 99:
                    stats["blob99_count"] += 1
                for enc_key_hex, embedded_salt in _windows_v411_config_key_candidates(blob):
                    candidate = (enc_key_hex, embedded_salt)
                    if candidate in seen_candidates:
                        continue
                    seen_candidates.add(candidate)
                    stats["candidate_count"] += 1
                    matched = _verify_windows_direct_key_candidate(
                        enc_key_hex, embedded_salt, db_files, salt_to_dbs,
                        key_map, remaining_salts,
                    )
                    if matched:
                        stats["verified_candidates"] += 1
                        stats["matched_salts"] += matched
                pos = data.find(pattern, pos + 1)

    stats["config_ptr_candidates"] = len(seen_config_ptrs)
    if stats["matched_salts"]:
        print_fn(
            "[+] Windows 4.1 runtime Config.Cipher scan matched "
            f"{stats['matched_salts']}/{len(salt_to_dbs)} salts "
            f"(pid={pid}, candidates={stats['candidate_count']})"
        )
    else:
        print_fn(
            "[INFO] Windows 4.1 runtime Config.Cipher scan found no verified key "
            f"(pid={pid}, nodes={stats['node_candidates']}, candidates={stats['candidate_count']})"
        )
    return stats


# ============================================================
# 主入口：先 4.1+ 只读扫描，再回退老版本明文内存扫描
# ============================================================

def extract_keys(db_dir, output_path, pid=None):
    """提取 Windows 微信数据库密钥。

    优先尝试微信 4.1+ 的只读 runtime Config.Cipher 扫描（主路径），
    再回退到老版本明文 raw key 内存扫描（兼容 4.0.x 及更早）。

    Args:
        db_dir: 微信数据库目录（db_storage）
        output_path: all_keys.json 输出路径
        pid: 可选，指定 PID（默认自动检测所有 Weixin.exe）

    Returns:
        dict: salt_hex -> enc_key_hex 映射

    Raises:
        RuntimeError: 提取失败
    """
    print("=" * 60)
    print("  提取所有微信数据库密钥")
    print("=" * 60)

    db_files, salt_to_dbs = collect_db_files(db_dir)
    if not db_files:
        raise RuntimeError(f"在 {db_dir} 未找到可解密的 .db 文件")

    print(f"\n找到 {len(db_files)} 个数据库, {len(salt_to_dbs)} 个不同的 salt")

    pids = _get_pids() if pid is None else [(pid, 0)]

    key_map = {}
    remaining_salts = set(salt_to_dbs.keys())
    t0 = time.time()

    # ---- 第 1 级：微信 4.1+ 只读 runtime Config.Cipher 扫描（主路径）----
    print("\n[*] 阶段 1/2：微信 4.1+ Config.Cipher 只读扫描")
    for pid_val, _mem_kb in pids:
        h = kernel32.OpenProcess(0x0010 | 0x0400, False, pid_val)
        if not h:
            print(f"[WARN] 无法打开进程 PID={pid_val}，跳过（尝试以管理员身份运行）")
            continue
        try:
            regions = _enum_regions(h)
            print(f"[*] 扫描 PID={pid_val} ({len(regions)} 个可读区域)")
            _scan_windows_v411_config_cipher(
                pid_val, regions,
                lambda base, size, _h=h: _read_mem(_h, base, size),
                lambda addr, size, _h=h: _read_mem(_h, addr, size),
                db_files, salt_to_dbs, key_map, remaining_salts, print,
            )
        finally:
            kernel32.CloseHandle(h)
        if not remaining_salts:
            print("[+] Config.Cipher 扫描已覆盖全部数据库，跳过后续进程")
            break

    # ---- 第 2 级：老版本明文 raw key 内存扫描（回退）----
    if remaining_salts:
        print(
            f"\n[*] 阶段 2/2：老版本明文 raw key 内存扫描"
            f"（剩余 {len(remaining_salts)} 个 salt 未命中，回退兼容 4.0.x 及更早）"
        )
        hex_re = re.compile(b"x'([0-9a-fA-F]{64,192})'")
        for pid_val, _mem_kb in pids:
            h = kernel32.OpenProcess(0x0010 | 0x0400, False, pid_val)
            if not h:
                print(f"[WARN] 无法打开进程 PID={pid_val}，跳过")
                continue
            try:
                regions = _enum_regions(h)
                total_bytes = sum(s for _, s in regions)
                total_mb = total_bytes / 1024 / 1024
                print(f"\n[*] 扫描 PID={pid_val} ({total_mb:.0f}MB, {len(regions)} 区域)")
                scanned_bytes = 0
                for reg_idx, (base, size) in enumerate(regions):
                    data = _read_mem(h, base, size)
                    scanned_bytes += size
                    if not data:
                        continue
                    scan_memory_for_keys(
                        data, hex_re, db_files, salt_to_dbs,
                        key_map, remaining_salts, base, pid_val, print,
                    )
                    if (reg_idx + 1) % 200 == 0:
                        elapsed = time.time() - t0
                        progress = scanned_bytes / total_bytes * 100 if total_bytes else 100
                        print(
                            f"  [{progress:.1f}%] {len(key_map)}/{len(salt_to_dbs)} salts matched, "
                            f"{elapsed:.1f}s"
                        )
            finally:
                kernel32.CloseHandle(h)
            if not remaining_salts:
                print(f"\n[+] 所有密钥已找到，跳过剩余进程")
                break

    elapsed = time.time() - t0
    print(f"\n扫描完成: {elapsed:.1f}s, {len(pids)} 个进程")

    cross_verify_keys(db_files, salt_to_dbs, key_map, print)
    return save_results(db_files, salt_to_dbs, key_map, output_path, print)
