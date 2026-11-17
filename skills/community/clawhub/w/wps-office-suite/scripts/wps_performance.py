"""
性能管理 v3.0 - 自动检测用户硬件，动态调整 Worker 配置
"""
import os
import sys
import platform
from pathlib import Path

WORKER_CONFIG = {}


def get_cpu_count():
    """获取 CPU 核心数，失败时返回保守值 2"""
    try:
        return max(2, os.cpu_count() or 2)
    except Exception:
        return 2


def get_memory_gb():
    """获取物理内存大小（GB），失败时返回保守值 4"""
    try:
        if sys.platform == "win32":
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
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys / (1024 ** 3)
        else:
            # Linux/macOS
            import subprocess
            if sys.platform == "darwin":
                result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
                return int(result.stdout.strip()) / (1024 ** 3)
            else:
                result = subprocess.run(["free", "-b"], capture_output=True, text=True)
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    parts = lines[1].split()
                    return int(parts[1]) / (1024 ** 3)
    except Exception:
        pass
    return 4.0  # 保守默认值


def get_disk_free_gb(path="C:\\"):
    """获取磁盘剩余空间（GB）"""
    try:
        import shutil
        usage = shutil.disk_usage(path)
        return usage.free / (1024 ** 3)
    except Exception:
        return 10.0  # 保守默认


def get_hardware_info():
    """
    综合检测用户硬件，返回硬件配置摘要。
    """
    cpu = get_cpu_count()
    mem = get_memory_gb()
    disk = get_disk_free_gb()
    
    # 确定硬件等级
    if cpu >= 8 and mem >= 16:
        level = "high"
    elif cpu >= 4 and mem >= 8:
        level = "medium"
    else:
        level = "low"
    
    return {
        "cpu_cores": cpu,
        "memory_gb": round(mem, 1),
        "disk_free_gb": round(disk, 1),
        "level": level,
        "platform": platform.system(),
    }


def get_worker_config():
    """
    根据硬件配置，返回 Worker 最佳参数。
    
    返回:
        {
            "max_workers": int,       # 最大并行 Worker 数
            "timeout": int,           # 单次操作超时（秒）
            "retry_count": int,       # 自动重试次数
            "chunk_size": int,        # 分批处理大小（行数）
            "memory_limit_mb": int,   # 内存使用限制
        }
    """
    global WORKER_CONFIG
    if WORKER_CONFIG:
        return WORKER_CONFIG
    
    hw = get_hardware_info()
    
    if hw["level"] == "high":
        # 高性能：多并行、短超时、小批量
        config = {
            "max_workers": min(hw["cpu_cores"], 8),
            "timeout": 30,
            "retry_count": 2,
            "chunk_size": 500,
            "memory_limit_mb": 512,
        }
    elif hw["level"] == "medium":
        # 中等：并行数减半、中等超时
        config = {
            "max_workers": min(max(2, hw["cpu_cores"] // 2), 4),
            "timeout": 60,
            "retry_count": 3,
            "chunk_size": 200,
            "memory_limit_mb": 256,
        }
    else:
        # 低性能：单进程、长超时、小批量
        config = {
            "max_workers": 1,
            "timeout": 120,
            "retry_count": 3,
            "chunk_size": 50,
            "memory_limit_mb": 128,
        }
    
    config["hardware"] = hw
    WORKER_CONFIG = config
    return config


def estimate_file_complexity(filepath, file_size_mb=None):
    """
    估算文件复杂度，用于动态调整超时和重试。
    
    返回: {"level": "small"|"medium"|"large"|"huge", "timeout_multiplier": float}
    """
    if file_size_mb is None:
        try:
            file_size_mb = Path(filepath).stat().st_size / (1024 * 1024)
        except Exception:
            file_size_mb = 0
    
    if file_size_mb < 1:
        return {"level": "small", "timeout_multiplier": 1.0}
    elif file_size_mb < 10:
        return {"level": "medium", "timeout_multiplier": 1.5}
    elif file_size_mb < 50:
        return {"level": "large", "timeout_multiplier": 2.5}
    else:
        return {"level": "huge", "timeout_multiplier": 5.0}


def adjust_timeout_for_file(base_timeout, filepath):
    """根据文件大小动态调整超时"""
    est = estimate_file_complexity(filepath)
    return int(base_timeout * est["timeout_multiplier"])


def should_use_parallel(file_count):
    """根据硬件和任务数量决定是否使用并行"""
    cfg = get_worker_config()
    if cfg["max_workers"] <= 1:
        return False
    if file_count <= 1:
        return False
    return True


def get_optimal_worker_count(file_count):
    """获取当前硬件下的最佳 Worker 数量"""
    cfg = get_worker_config()
    return min(file_count, cfg["max_workers"])
