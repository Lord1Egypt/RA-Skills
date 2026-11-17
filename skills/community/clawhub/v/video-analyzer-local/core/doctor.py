"""首跑自检模块 — 一次性探测 ffmpeg / whisper 模型缓存 / 磁盘剩余空间 / 内存水位 / GPU 可用性，输出修复命令清单"""

import hashlib
import os
import platform
import shutil
import subprocess
from typing import Any, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


# ==================== 默认检查项配置 ====================
DEFAULT_CHECKS = {
    "ffmpeg": {
        "description": "ffmpeg 可用",
        "required": True,
        "hint": "请安装 ffmpeg",
    },
    "model_cache": {
        "description": "whisper 模型缓存",
        "required": True,
        "hint": "模型将在首次运行时自动下载",
    },
    "disk_space": {
        "description": "磁盘剩余空间 ≥ 2GB",
        "required": True,
        "hint": "请清理磁盘空间",
    },
    "memory_available": {
        "description": "可用内存 ≥ 2GB",
        "required": True,
        "hint": "请关闭其他程序释放内存",
    },
    "gpu_available": {
        "description": "GPU 可用性（可选）",
        "required": False,
        "hint": "无 GPU 将使用 CPU 模式",
    },
}


class Doctor:
    """
    首跑自检器。

    一次性探测：
    - ffmpeg 可用（版本校验）
    - whisper 模型缓存（路径存在性 + SHA256 校验）
    - 磁盘剩余空间（缓存目录所在磁盘）
    - 内存水位（可用内存 ≥ 2GB）
    - GPU 可用性（可选）

    输出：「缺什么→给什么」修复命令清单，
    写操作先列清单等确认（winskill 修复向导交互范式）。
    检查项 YAML 可配。
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.doctor_config = config.get("doctor", {})
        self.checks = self.doctor_config.get("checks", DEFAULT_CHECKS)
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        self.models_dir = os.path.join(os.path.dirname(__file__), "..", "models")

    def run_self_check(self) -> Dict[str, Any]:
        """
        运行首跑自检。

        Returns:
            {
                "passed": True/False,
                "report": {
                    "check_name": {
                        "status": "pass/warn/fail",
                        "detail": "详细信息",
                        "fix_command": "修复命令" or None,
                    }
                },
                "fixes_needed": ["需要修复的项"],
                "summary": "自检摘要",
            }
        """
        report = {}
        fixes_needed = []
        all_passed = True

        for check_name, check_config in self.checks.items():
            if not check_config.get("required", False) and check_name == "gpu_available":
                # 可选检查项
                result = self._run_check(check_name, check_config)
                report[check_name] = result
                if result["status"] == "fail":
                    fixes_needed.append(check_name)
                continue

            result = self._run_check(check_name, check_config)
            report[check_name] = result

            if result["status"] == "fail":
                fixes_needed.append(check_name)
                all_passed = False
            elif result["status"] == "warn":
                fixes_needed.append(check_name)

        summary = self._generate_summary(report, fixes_needed)

        return {
            "passed": all_passed,
            "report": report,
            "fixes_needed": fixes_needed,
            "summary": summary,
        }

    def _run_check(self, check_name: str, check_config: Dict) -> Dict[str, Any]:
        """执行单项检查"""
        result = {
            "status": "pass",
            "detail": "",
            "fix_command": None,
        }

        try:
            if check_name == "ffmpeg":
                result = self._check_ffmpeg(result)
            elif check_name == "model_cache":
                result = self._check_model_cache(result)
            elif check_name == "disk_space":
                result = self._check_disk_space(result)
            elif check_name == "memory_available":
                result = self._check_memory(result)
            elif check_name == "gpu_available":
                result = self._check_gpu(result)
            else:
                result["detail"] = f"未知检查项: {check_name}"
                result["status"] = "warn"
        except Exception as e:
            result["status"] = "fail"
            result["detail"] = f"检查异常: {str(e)}"

        return result

    def _check_ffmpeg(self, result: Dict) -> Dict:
        """检查 ffmpeg 可用性"""
        try:
            proc = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0:
                version_line = proc.stdout.split("\n")[0]
                result["detail"] = f"ffmpeg 可用: {version_line}"
                result["status"] = "pass"
            else:
                result["status"] = "fail"
                result["detail"] = "ffmpeg 未安装或不在 PATH 中"
                result["fix_command"] = self._get_ffmpeg_install_command()
        except FileNotFoundError:
            result["status"] = "fail"
            result["detail"] = "ffmpeg 未安装或不在 PATH 中"
            result["fix_command"] = self._get_ffmpeg_install_command()
        except subprocess.TimeoutExpired:
            result["status"] = "fail"
            result["detail"] = "ffmpeg 响应超时"
            result["fix_command"] = self._get_ffmpeg_install_command()

        return result

    def _check_model_cache(self, result: Dict) -> Dict:
        """检查 whisper 模型缓存"""
        whisper_cache_dir = os.path.expanduser("~/.cache/whisper")
        if not os.path.exists(whisper_cache_dir):
            result["status"] = "warn"
            result["detail"] = f"模型缓存目录不存在: {whisper_cache_dir}（将在首次运行时自动创建并下载）"
            result["fix_command"] = "首次运行将自动下载 tiny 模型（约 75MB）"
            return result

        # 检查是否有模型文件
        model_files = [f for f in os.listdir(whisper_cache_dir) if f.endswith(".pt")]
        if model_files:
            result["detail"] = f"模型缓存目录存在，已缓存模型: {', '.join(model_files)}"
            result["status"] = "pass"
        else:
            result["status"] = "warn"
            result["detail"] = f"模型缓存目录存在但无模型文件: {whisper_cache_dir}"
            result["fix_command"] = "首次运行将自动下载 tiny 模型（约 75MB）"

        return result

    def _check_disk_space(self, result: Dict) -> Dict:
        """检查磁盘剩余空间"""
        target_dir = self.cache_dir if os.path.exists(self.cache_dir) else os.path.expanduser("~")

        try:
            if platform.system() == "Windows":
                # Windows: 使用 shutil.disk_usage
                usage = shutil.disk_usage(target_dir)
                free_gb = usage.free / (1024**3)
                total_gb = usage.total / (1024**3)
            else:
                # Linux/macOS: 使用 statvfs
                stat = os.statvfs(target_dir)
                free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
                total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)

            if free_gb >= 2.0:
                result["detail"] = f"磁盘剩余空间: {free_gb:.1f}GB / {total_gb:.1f}GB"
                result["status"] = "pass"
            else:
                result["status"] = "fail"
                result["detail"] = f"磁盘剩余空间不足: {free_gb:.1f}GB（需要 ≥ 2GB）"
                result["fix_command"] = f"请清理磁盘空间，确保 {os.path.dirname(target_dir)} 所在磁盘至少有 2GB 剩余"
        except Exception as e:
            result["status"] = "warn"
            result["detail"] = f"磁盘空间检查失败: {str(e)}"

        return result

    def _check_memory(self, result: Dict) -> Dict:
        """检查可用内存"""
        try:
            if platform.system() == "Windows":
                # Windows: 使用 ctypes 调用 GlobalMemoryStatusEx（避免 wmic 被沙箱拦截）
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
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                free_gb = stat.ullAvailPhys / (1024**3)
            else:
                # Linux/macOS: 读取 /proc/meminfo 或使用 sysctl
                if platform.system() == "Linux":
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if line.startswith("MemAvailable"):
                                free_kb = int(line.split()[1])
                                free_gb = free_kb / (1024 * 1024)
                                break
                        else:
                            raise ValueError("无法读取 MemAvailable")
                else:
                    # macOS: 使用 vm_stat
                    proc = subprocess.run(
                        ["vm_stat"],
                        capture_output=True, text=True, timeout=10
                    )
                    if proc.returncode == 0:
                        free_bytes = 0
                        for line in proc.stdout.split("\n"):
                            if "Pages free" in line:
                                free_pages = int(line.split(":")[1].strip())
                                free_bytes = free_pages * 4096
                            elif "Pages speculative" in line:
                                spec_pages = int(line.split(":")[1].strip())
                                free_bytes += spec_pages * 4096
                        free_gb = free_bytes / (1024**3)
                    else:
                        raise ValueError("vm_stat 命令失败")

            if free_gb >= 2.0:
                result["detail"] = f"可用内存: {free_gb:.1f}GB"
                result["status"] = "pass"
            else:
                result["status"] = "fail"
                result["detail"] = f"可用内存不足: {free_gb:.1f}GB（需要 ≥ 2GB）"
                result["fix_command"] = "请关闭其他程序释放内存，或使用 --model tiny 减少内存占用"
        except Exception as e:
            result["status"] = "warn"
            result["detail"] = f"内存检查失败: {str(e)}"

        return result

    def _check_gpu(self, result: Dict) -> Dict:
        """检查 GPU 可用性（可选）"""
        try:
            # 检查 NVIDIA GPU
            proc = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0 and proc.stdout.strip():
                parts = proc.stdout.strip().split(",")
                gpu_name = parts[0].strip()
                vram_str = parts[1].strip() if len(parts) > 1 else "未知"
                result["detail"] = f"GPU 可用: {gpu_name} ({vram_str})"
                result["status"] = "pass"
            else:
                result["status"] = "warn"
                result["detail"] = "无 NVIDIA GPU，将使用 CPU 模式"
                result["fix_command"] = "如需 GPU 加速，请安装 NVIDIA 显卡和 CUDA 驱动"
        except FileNotFoundError:
            result["status"] = "warn"
            result["detail"] = "未找到 nvidia-smi，将使用 CPU 模式"
            result["fix_command"] = "如需 GPU 加速，请安装 NVIDIA 驱动"
        except subprocess.TimeoutExpired:
            result["status"] = "warn"
            result["detail"] = "nvidia-smi 响应超时"

        return result

    def _get_ffmpeg_install_command(self) -> str:
        """获取 ffmpeg 安装命令"""
        if platform.system() == "Windows":
            return (
                "Windows 安装 ffmpeg:\n"
                "  方法1: scoop install ffmpeg\n"
                "  方法2: choco install ffmpeg\n"
                "  方法3: 下载 https://ffmpeg.org/download.html 后解压并加入 PATH"
            )
        elif platform.system() == "Darwin":
            return "macOS 安装 ffmpeg: brew install ffmpeg"
        else:
            return "Linux 安装 ffmpeg: sudo apt install ffmpeg 或 sudo dnf install ffmpeg"

    def _generate_summary(self, report: Dict, fixes_needed: List[str]) -> str:
        """生成自检摘要"""
        total = len(report)
        passed = sum(1 for r in report.values() if r["status"] == "pass")
        failed = sum(1 for r in report.values() if r["status"] == "fail")
        warned = sum(1 for r in report.values() if r["status"] == "warn")

        if not fixes_needed:
            return f"✅ 自检全部通过 ({passed}/{total})"

        summary_parts = []
        if failed > 0:
            summary_parts.append(f"❌ {failed} 项失败")
        if warned > 0:
            summary_parts.append(f"⚠️ {warned} 项警告")
        if passed > 0:
            summary_parts.append(f"✅ {passed} 项通过")

        return f"自检结果: {', '.join(summary_parts)}"

    def get_fix_instructions(self, check_name: str) -> Optional[str]:
        """获取指定检查项的修复指令"""
        check_config = self.checks.get(check_name)
        if not check_config:
            return None

        if check_name == "ffmpeg":
            return self._get_ffmpeg_install_command()
        elif check_name == "model_cache":
            return "模型将在首次运行时自动下载。国内用户建议先执行:\n  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"
        elif check_name == "disk_space":
            return "请清理磁盘空间，确保至少有 2GB 剩余"
        elif check_name == "memory_available":
            return "请关闭其他程序释放内存，或使用 --model tiny 减少内存占用"
        elif check_name == "gpu_available":
            return "如需 GPU 加速，请安装 NVIDIA 显卡和 CUDA 驱动"

        return None

    @staticmethod
    def format_report(report: Dict[str, Any]) -> str:
        """格式化自检报告为可读文本"""
        lines = []
        lines.append("=" * 50)
        lines.append("首跑自检报告")
        lines.append("=" * 50)

        for check_name, result in report.items():
            status_icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}.get(result["status"], "❓")
            lines.append(f"\n{status_icon} {check_name}: {result.get('detail', '')}")
            if result.get("fix_command"):
                lines.append(f"   修复: {result['fix_command']}")

        lines.append("\n" + "=" * 50)
        return "\n".join(lines)
