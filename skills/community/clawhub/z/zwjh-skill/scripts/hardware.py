# -*- coding: utf-8 -*-
"""
硬件自适应调度 —— 让技能「不拖累用户电脑」。

核心思路：
  - 只用标准库探测 CPU 核心数、物理内存、操作系统。
  - 据此把机器分成 low / mid / high 三档，自动给出：
      * 最大并发数（concurrency）
      * 单批处理条数（batch_size）
      * 是否启用内存缓存（enable_embed_cache）
      * 索引重建是否走后台（background_index）
  - 对外提供 recommend_subtasks(n_items)：根据任务量与档位，建议拆成几个子任务。

无任何外部依赖；探测失败则回退到保守（low）档位，绝不把电脑跑满。
"""

from __future__ import annotations

import os
import platform
import sys


def detect_cpu_count() -> int:
    try:
        n = os.cpu_count()
        return int(n) if n else 1
    except Exception:
        return 1


def detect_ram_gb() -> float:
    """跨平台获取物理内存（GB），失败返回 0（调用方回退保守档）。"""
    try:
        if sys.platform.startswith("win"):
            return _ram_windows()
        if sys.platform.startswith("linux"):
            return _ram_linux()
        if sys.platform == "darwin":
            return _ram_macos()
    except Exception:
        pass
    return 0.0


def _ram_windows() -> float:
    # 使用 kernel32.GlobalMemoryStatusEx（标准库 ctypes，无外部依赖）
    import ctypes

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))  # type: ignore[attr-defined]
    if not ok:
        return 0.0
    return stat.ullTotalPhys / (1024.0 ** 3)


def _ram_linux() -> float:
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return kb / (1024.0 ** 2)
    except Exception:
        pass
    return 0.0


def _ram_macos() -> float:
    # sysctl 通过 ctypes libc 读取，避免启动子进程
    try:
        import ctypes

        libc = ctypes.CDLL("/usr/lib/libc.dylib")
        size = ctypes.c_size_t(8)
        value = ctypes.c_uint64(0)
        ret = libc.sysctlbyname(
            b"hw.memsize", ctypes.byref(value), ctypes.byref(size), None, 0
        )
        if ret == 0:
            return value.value / (1024.0 ** 3)
    except Exception:
        pass
    return 0.0


def detect_os() -> str:
    return f"{platform.system()} {platform.release()}".strip()


def compute_tier(cores: int, ram_gb: float) -> str:
    # 任一指标缺失（ram_gb==0）时，按核心数保守估计内存
    eff_ram = ram_gb if ram_gb > 0 else cores * 1.5
    if cores <= 2 or eff_ram < 4:
        return "low"
    if cores <= 4 or eff_ram < 8:
        return "mid"
    return "high"


# 各档位的执行预算
_TIERS = {
    "low": {
        "concurrency": 1,
        "batch_size": 20,
        "enable_embed_cache": False,
        "background_index": False,
        "note": "低配机：单线程、小批量，避免卡顿",
    },
    "mid": {
        "concurrency": 2,
        "batch_size": 60,
        "enable_embed_cache": True,
        "background_index": False,
        "note": "中配机：轻并发，常规批处理",
    },
    "high": {
        "concurrency": min(detect_cpu_count(), 8),
        "batch_size": 200,
        "enable_embed_cache": True,
        "background_index": True,
        "note": "高配机：多并发 + 后台索引",
    },
}


def get_plan() -> dict:
    """返回当前机器的执行计划（含探测信息）。"""
    cores = detect_cpu_count()
    ram = detect_ram_gb()
    tier = compute_tier(cores, ram)
    plan = dict(_TIERS[tier])
    plan.update(
        {
            "tier": tier,
            "cpu_cores": cores,
            "ram_gb": round(ram, 1),
            "os": detect_os(),
        }
    )
    return plan


def recommend_subtasks(n_items: int, plan: dict | None = None) -> int:
    """
    根据任务量与硬件档位，建议把任务拆成几个子任务。

    规则：单子任务条数不超过 batch_size；并发子任务数不超过 concurrency；
    至少 1 个、最多 concurrency 个。
    """
    if plan is None:
        plan = get_plan()
    if n_items <= 0:
        return 1
    by_batch = max(1, -(-n_items // plan["batch_size"]))  # 向上取整
    by_concurrency = max(1, min(plan["concurrency"], by_batch))
    return by_concurrency


def describe() -> str:
    p = get_plan()
    return (
        f"硬件档位={p['tier']} | CPU={p['cpu_cores']}核 | 内存≈{p['ram_gb']}GB | "
        f"系统={p['os']}\n  建议并发={p['concurrency']} | 单批={p['batch_size']} | "
        f"向量缓存={'开' if p['enable_embed_cache'] else '关'} | {p['note']}"
    )


if __name__ == "__main__":
    print(describe())
    print("示例：1000 条知识点建议子任务数 =", recommend_subtasks(1000))
