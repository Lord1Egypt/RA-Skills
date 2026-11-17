"""硬件探测模块 — 自动检测用户电脑硬件并计算最佳任务分配 + 运行时监控"""

import os
import platform
import subprocess
import threading
import time
from typing import Any, Dict, Optional

from .logger import get_logger

logger = get_logger(__name__)


class ResourceMonitor:
    """实时系统资源监控器 — 运行时动态调整参数"""
    
    def __init__(self, max_memory_gb: float, check_interval: float = 5.0):
        self.max_memory_gb = max_memory_gb
        self.check_interval = check_interval
        self._monitoring = False
        self._thread = None
        self._peak_memory_gb = 0
        self._current_memory_usage = 0
        self._current_cpu_percent = 0
        self._pause_requested = False  # 资源紧张时请求暂停
        self._callbacks = []
    
    def start(self):
        """启动后台监控线程"""
        if self._monitoring:
            return
        self._monitoring = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.debug("资源监控线程已启动")
    
    def stop(self):
        """停止监控"""
        self._monitoring = False
        if self._thread:
            self._thread.join(timeout=10)
        logger.debug("资源监控线程已停止")
    
    def register_callback(self, callback):
        """注册资源告警回调(callback(is_critical: bool))"""
        self._callbacks.append(callback)
    
    def _monitor_loop(self):
        """后台监控循环"""
        while self._monitoring:
            try:
                self._sample_resources()
                
                # 检查是否超出限制
                memory_ratio = self._current_memory_usage / self.max_memory_gb if self.max_memory_gb > 0 else 0
                
                if memory_ratio > 0.9:
                    # 严重：内存接近上限
                    self._pause_requested = True
                    logger.warning(f"⚠️ 内存使用接近上限 ({self._current_memory_gb:.1f}GB/{self.max_memory_gb:.1f}GB)，建议暂停新任务")
                    for cb in self._callbacks:
                        cb(True)
                elif memory_ratio > 0.75:
                    # 警告
                    logger.debug(f"内存使用较高: {self._current_memory_gb:.1f}GB/{self.max_memory_gb:.1f}GB")
                    for cb in self._callbacks:
                        cb(False)
                else:
                    self._pause_requested = False
                    
            except Exception:
                pass
            time.sleep(self.check_interval)
    
    def _sample_resources(self):
        """采样当前系统资源"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            self._current_memory_usage = mem.used / (1024**3)
            self._current_cpu_percent = psutil.cpu_percent(interval=0.5)
            self._peak_memory_gb = max(self._peak_memory_gb, self._current_memory_gb)
        except ImportError:
            # 无 psutil 时使用各平台原生命令
            if platform.system() == "Windows":
                self._sample_windows()
            elif platform.system() == "Linux":
                self._sample_linux()
    
    def _sample_windows(self):
        """Windows 原生采样"""
        try:
            result = subprocess.run(
                ["wmic", "os", "get", "FreePhysicalMemory,TotalVisibleMemorySize"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        total_kb = int(parts[1])
                        free_kb = int(parts[0])
                        total_gb = total_kb / (1024 * 1024)
                        free_gb = free_kb / (1024 * 1024)
                        self._current_memory_usage = total_gb - free_gb
                        self._peak_memory_gb = max(self._peak_memory_gb, self._current_memory_usage)
        except Exception:
            pass
    
    def _sample_linux(self):
        """Linux 原生采样"""
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read()
            mem_total = 0
            mem_available = 0
            for line in meminfo.split("\n"):
                if line.startswith("MemTotal"):
                    mem_total = int(line.split()[1])
                elif line.startswith("MemAvailable"):
                    mem_available = int(line.split()[1])
            if mem_total > 0:
                total_gb = mem_total / (1024 * 1024)
                available_gb = mem_available / (1024 * 1024)
                self._current_memory_usage = total_gb - available_gb
                self._peak_memory_gb = max(self._peak_memory_gb, self._current_memory_usage)
        except Exception:
            pass
    
    @property
    def current_memory_gb(self):
        return self._current_memory_usage
    
    @property
    def current_cpu_percent(self):
        return self._current_cpu_percent
    
    @property
    def peak_memory_gb(self):
        return self._peak_memory_gb
    
    @property
    def pause_requested(self):
        return self._pause_requested
    
    def get_status(self) -> Dict:
        """获取当前状态快照"""
        return {
            "current_memory_gb": round(self._current_memory_gb, 2),
            "peak_memory_gb": round(self._peak_memory_gb, 2),
            "cpu_percent": self._current_cpu_percent,
            "max_memory_gb": self.max_memory_gb,
            "pause_requested": self._pause_requested,
        }


class HardwareProbe:
    """自动检测硬件资源，计算最佳并行参数"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._info = None
    
    def detect(self) -> Dict[str, Any]:
        """
        探测硬件信息。
        
        Returns:
            硬件信息字典
        """
        if self._info is not None:
            return self._info
        
        info = {
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "node": platform.node(),
            },
            "cpu": self._detect_cpu(),
            "memory": self._detect_memory(),
            "gpu": self._detect_gpu(),
        }
        
        # 计算推荐配置
        info["recommended"] = self._calculate_recommended(info)
        
        self._info = info
        logger.info(f"硬件探测: {info['cpu']['cores']}核 CPU, "
                    f"{info['memory']['total_gb']:.1f}GB 内存")
        
        if info["gpu"]["available"]:
            logger.info(f"GPU: {info['gpu']['name']}")
        
        return info
    
    def _detect_cpu(self) -> Dict[str, Any]:
        """检测 CPU 信息"""
        info = {
            "cores": os.cpu_count() or 4,
            "physical_cores": os.cpu_count() or 4,
            "model": "unknown",
        }
        
        try:
            if platform.system() == "Windows":
                # Windows: 使用 wmic
                result = subprocess.run(
                    ["wmic", "cpu", "get", "NumberOfCores,NumberOfLogicalProcessors,Name"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split("\n")
                    if len(lines) >= 2:
                        parts = lines[1].split()
                        if len(parts) >= 3:
                            info["physical_cores"] = int(parts[0])
                            info["cores"] = int(parts[1])
                            info["model"] = " ".join(parts[2:])
            
            elif platform.system() == "Linux":
                # Linux: 读取 /proc/cpuinfo
                with open("/proc/cpuinfo", "r") as f:
                    content = f.read()
                
                # 获取物理核心数
                physical = set()
                for line in content.split("\n"):
                    if line.startswith("physical id"):
                        physical.add(line.split(":")[1].strip())
                
                info["physical_cores"] = len(physical) if physical else info["cores"]
                
                # 获取型号
                for line in content.split("\n"):
                    if line.startswith("model name"):
                        info["model"] = line.split(":")[1].strip()
                        break
            
            elif platform.system() == "Darwin":
                # macOS: 使用 sysctl
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    info["model"] = result.stdout.strip()
                
                result = subprocess.run(
                    ["sysctl", "-n", "hw.physicalcpu"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    info["physical_cores"] = int(result.stdout.strip())
        
        except Exception as e:
            logger.debug(f"CPU 检测失败: {e}")
        
        return info
    
    def _detect_memory(self) -> Dict[str, Any]:
        """检测内存信息"""
        info = {
            "total_gb": 8.0,
            "available_gb": 4.0,
        }
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "os", "get", "FreePhysicalMemory,TotalVisibleMemorySize"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split("\n")
                    if len(lines) >= 2:
                        parts = lines[1].split()
                        if len(parts) >= 2:
                            total_kb = int(parts[1])
                            free_kb = int(parts[0])
                            info["total_gb"] = total_kb / (1024 * 1024)
                            info["available_gb"] = free_kb / (1024 * 1024)
            
            elif platform.system() == "Linux":
                with open("/proc/meminfo", "r") as f:
                    meminfo = f.read()
                
                for line in meminfo.split("\n"):
                    if line.startswith("MemTotal"):
                        info["total_gb"] = int(line.split()[1]) / (1024 * 1024)
                    elif line.startswith("MemAvailable"):
                        info["available_gb"] = int(line.split()[1]) / (1024 * 1024)
            
            elif platform.system() == "Darwin":
                result = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    info["total_gb"] = int(result.stdout.strip()) / (1024 ** 3)
                
                result = subprocess.run(
                    ["vm_stat"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    # 简单估算可用内存
                    for line in result.stdout.split("\n"):
                        if "Pages free" in line:
                            free_pages = int(line.split(":")[1].strip())
                            info["available_gb"] = (free_pages * 4096) / (1024 ** 3)
                            break
        
        except Exception as e:
            logger.debug(f"内存检测失败: {e}")
        
        return info
    
    def _detect_gpu(self) -> Dict[str, Any]:
        """检测 GPU 信息"""
        info = {
            "available": False,
            "name": "unknown",
            "vram_gb": 0,
            "cuda_available": False,
        }
        
        # 检测 NVIDIA GPU
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split(",")
                if len(parts) >= 2:
                    info["available"] = True
                    info["name"] = parts[0].strip()
                    # 解析显存
                    vram_str = parts[1].strip()
                    if "MiB" in vram_str:
                        info["vram_gb"] = int(vram_str.replace("MiB", "").strip()) / 1024
                    elif "GiB" in vram_str:
                        info["vram_gb"] = float(vram_str.replace("GiB", "").strip())
                    info["cuda_available"] = True
                    return info
        except FileNotFoundError:
            logger.debug("nvidia-smi 未找到")
        except Exception as e:
            logger.debug(f"NVIDIA GPU 检测失败: {e}")
        
        # 检测 Apple Silicon (macOS)
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(
                    ["system_profiler", "SPDisplaysDataType"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    for line in result.stdout.split("\n"):
                        if "Chipset Model" in line and ("Apple" in line or "M1" in line or "M2" in line or "M3" in line):
                            info["available"] = True
                            info["name"] = line.split(":")[1].strip()
                            info["vram_gb"] = info["total_gb"] * 0.5  # Apple Silicon 共享内存
                            return result
            except Exception as e:
                logger.debug(f"Apple GPU 检测失败: {e}")
        
        # 检测 AMD GPU (Linux)
        if platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ["lspci"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    for line in result.stdout.lower().split("\n"):
                        if "vga" in line or "display" in line:
                            if "amd" in line or "ati" in line:
                                info["available"] = True
                                info["name"] = line.split(":")[-1].strip()
                                break
            except Exception:
                pass
        
        return info
    
    def _calculate_recommended(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据硬件推荐最佳配置。
        
        策略（v4.1 新增 tiny 模型优先体验）：
        - tiny 模型优先体验：首次使用/低配电脑默认 tiny (75MB)
        - 子进程数 = min(物理核心数 - 1, 内存GB / 2)
        - 视觉分析：GPU 可用则全量，否则限制采样率
        """
        cpu_cores = info["cpu"]["physical_cores"]
        memory_gb = info["memory"]["total_gb"]
        gpu_available = info["gpu"]["available"]
        gpu_vram = info["gpu"]["vram_gb"]
        
        # 获取 whisper 配置（从 config 而不是 info）
        whisper_config = self.config.get("whisper", {})
        tiny_first = whisper_config.get("tiny_first", True)
        low_memory_threshold = whisper_config.get("low_memory_threshold", 4)
        
        # === 计算最佳子进程数 ===
        # 策略：保留 1 核给系统，每 2GB 内存支持 1 子进程
        by_cpu = max(1, cpu_cores - 1)
        by_memory = max(1, int(memory_gb / 2))
        recommended_workers = min(by_cpu, by_memory, 8)  # 最多 8 子进程
        
        # === 推荐 whisper 模型 (v4.1 tiny 优先) ===
        # 低配电脑或启用 tiny_first 时默认 tiny
        if memory_gb < low_memory_threshold or tiny_first:
            recommended_model = "tiny"
        elif memory_gb >= 16 and (gpu_available and gpu_vram >= 4):
            recommended_model = "large-v3"
        elif memory_gb >= 8:
            recommended_model = "medium"
        elif memory_gb >= 4:
            recommended_model = "small"
        else:
            recommended_model = "tiny"
        
        # === 推荐视觉分析策略 ===
        if gpu_available and gpu_vram >= 2:
            visual_quality = "high"  # 全量分析
            visual_sampling = 2  # 每 2 秒
        elif gpu_available:
            visual_quality = "medium"
            visual_sampling = 3
        elif memory_gb >= 8:
            visual_quality = "medium"
            visual_sampling = 5
        else:
            visual_quality = "low"
            visual_sampling = 10  # 低配电脑降低视觉分析频率
        
        # === 内存限制 ===
        # 防止处理大视频时 OOM
        max_memory_usage = min(memory_gb * 0.7, 12)  # 最多使用 70% 内存，上限 12GB
        frame_cache_limit = int(max_memory_usage * 100)  # 帧缓存数量限制
        
        # === 是否启用 GPU 加速 ===
        use_gpu = gpu_available and gpu_vram >= 2
        
        return {
            "workers": recommended_workers,
            "whisper_model": recommended_model,
            "visual_quality": visual_quality,
            "visual_sampling_interval": visual_sampling,
            "max_memory_gb": round(max_memory_usage, 1),
            "frame_cache_limit": frame_cache_limit,
            "use_gpu": use_gpu,
            "device": "cuda" if (gpu_available and gpu_vram >= 2) else "cpu",
            "nice_level": 10 if memory_gb < 8 else 5,  # 低配电脑降低优先级
        }
    
    def apply_to_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        将推荐配置应用到现有配置。
        用户自定义配置优先级最高，空缺处才使用推荐值。
        """
        info = self.detect()
        rec = info["recommended"]
        
        # 只在用户没有显式设置时才使用推荐值
        processing = config.setdefault("processing", {})
        
        # 子进程数：只在默认值或未设置时覆盖
        if processing.get("num_workers") == 4:  # 默认 4
            processing["num_workers"] = rec["workers"]
        
        # whisper 设备
        whisper = config.setdefault("whisper", {})
        if not whisper.get("device") or whisper["device"] == "cpu":
            if rec["use_gpu"]:
                whisper["device"] = "cuda"
        
        # 视觉分析采样间隔
        visual = config.setdefault("visual_analysis", {})
        if not visual.get("sampling_interval"):
            visual["sampling_interval"] = rec["visual_sampling_interval"]
        
        # 缓存帧限制
        if not processing.get("max_frame_cache"):
            processing["max_frame_cache"] = rec["frame_cache_limit"]
        
        # 优先级设置
        if not processing.get("nice_level"):
            processing["nice_level"] = rec["nice_level"]
        
        # 内存限制
        if not processing.get("max_memory_gb"):
            processing["max_memory_gb"] = rec["max_memory_gb"]
        
        logger.info(f"自适应配置: {rec['workers']} 子进程, "
                    f"whisper={rec['whisper_model']}, "
                    f"视觉质量={rec['visual_quality']}, "
                    f"设备={'cuda' if rec['use_gpu'] else 'cpu'}")
        
        return config
    
    def estimate_processing_time(self, video_duration: float, media_info: Dict = None) -> Dict[str, Any]:
        """
        预估处理时间（基于硬件配置）。
        
        Args:
            video_duration: 视频时长（秒）
            media_info: 视频元数据
            
        Returns:
            预估结果
        """
        info = self.detect()
        rec = info["recommended"]
        
        # 基础处理倍数（相对于视频时长）
        # whisper 模型速度（tiny=4x, base=3x, small=2x, medium=1x, large=0.5x）
        model_speed = {
            "tiny": 4,
            "base": 3,
            "small": 2,
            "medium": 1,
            "large-v3": 0.5,
        }.get(rec["whisper_model"], 1)
        
        # 视觉分析开销
        visual_overhead = {
            "high": 0.5,
            "medium": 0.3,
            "low": 0.1,
        }.get(rec["visual_quality"], 0.3)
        
        # 总预估时间 = 视频时长 * (1/模型加速) * (1 + 视觉开销) / 并行因子
        parallel_factor = max(rec["workers"], 1) * 1.5  # CPU/GPU 并行
        
        estimated_seconds = video_duration / (model_speed * parallel_factor) * (1 + visual_overhead)
        
        return {
            "estimated_seconds": round(estimated_seconds, 1),
            "estimated_formatted": self._format_duration(estimated_seconds),
            "model_speed": model_speed,
            "parallel_workers": rec["workers"],
            "visual_overhead": visual_overhead,
        }
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """格式化时长"""
        if seconds < 60:
            return f"{seconds:.0f}秒"
        elif seconds < 3600:
            m = int(seconds // 60)
            s = int(seconds % 60)
            return f"{m}分{s}秒"
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}小时{m}分"
