"""
树莓派摄像头硬件管理模块
支持 CSI (Picamera2) 和 USB (FFmpeg 直接录制) 双模式
"""
from __future__ import annotations

import logging
import signal
import subprocess
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

# 尝试导入 Picamera2
try:
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder
    from picamera2.outputs import FileOutput
    PICAMERA_AVAILABLE: bool = True
except ImportError:
    PICAMERA_AVAILABLE = False
    logger.debug("Picamera2 未安装")
    Picamera2 = None
    H264Encoder = None
    FileOutput = None


class BaseCamera(ABC):
    """摄像头抽象基类"""

    @abstractmethod
    def init(self, width: int, height: int, fps: int) -> bool:
        pass

    @abstractmethod
    def start_recording(self, filepath: str) -> None:
        pass

    @abstractmethod
    def stop_recording(self) -> None:
        pass

    @abstractmethod
    def release(self) -> None:
        pass

    @abstractmethod
    def capture_image(self, filepath: str) -> None:
        """拍照并保存到指定路径"""
        pass


class CSICamera(BaseCamera):
    """CSI 摄像头（Picamera2 硬件编码）"""
    
    def __init__(self) -> None:
        self._picam2: Picamera2 | None = None
        self._encoder: H264Encoder | None = None
        
    def init(self, width: int = 1920, height: int = 1080, fps: int = 30) -> bool:
        if not PICAMERA_AVAILABLE:
            return False
            
        try:
            self._picam2 = Picamera2()
            config = self._picam2.create_video_configuration(
                main={"size": (width, height), "format": "RGB888"},
                controls={"FrameRate": fps}
            )
            self._picam2.configure(config)
            self._encoder = H264Encoder(bitrate=10000000)
            logger.info(f"CSI 初始化成功: {width}x{height}@{fps}fps")
            return True
        except Exception as e:
            logger.error(f"CSI 初始化失败: {e}")
            return False
    
    def start_recording(self, filepath: str) -> None:
        if not self._picam2:
            raise RuntimeError("CSI 未初始化")
        output = FileOutput(filepath)
        self._picam2.start_recording(self._encoder, output)
    
    def stop_recording(self) -> None:
        if self._picam2:
            self._picam2.stop_recording()
    
    def release(self) -> None:
        if self._picam2:
            self._picam2.close()
            self._picam2 = None
            logger.info("CSI 已释放")

    def capture_image(self, filepath: str) -> None:
        """使用 Picamera2 拍照"""
        if not self._picam2:
            raise RuntimeError("CSI 未初始化")
        self._picam2.capture_file(filepath)
        logger.info(f"CSI 拍照完成: {filepath}")


class USBCamera(BaseCamera):
    """USB 摄像头（FFmpeg 录制）"""
    
    def __init__(self, device: str = "/dev/video0") -> None:
        self._device: str = device
        self._process: subprocess.Popen | None = None
        self._fps: int = 30
        self._size: tuple[int, int] = (1280, 720)
        self._ffmpeg_cmd: list[str] | None = None
        
    def init(self, width: int = 1280, height: int = 720, fps: int = 30) -> bool:
        """检查设备并探测支持的格式"""
        if not Path(self._device).exists():
            logger.error(f"USB 设备不存在: {self._device}")
            return False
        
        # 检查 FFmpeg 可用性
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                timeout=5
            )
            if result.returncode != 0:
                return False
        except Exception:
            return False
        
        self._size = (width, height)
        self._fps = fps
        
        logger.info(f"USB 就绪: {self._device} {width}x{height}@{fps}fps")
        return True
    
    def _build_ffmpeg_cmd(self, filepath: str) -> list[str]:
        """
        构建 FFmpeg 命令
        优先尝试硬件编码流（如 C920），失败则使用 MJPEG + 快速编码
        """
        width, height = self._size
        
        # 方案 A: 尝试直接复制 H264 流（零 CPU，仅部分摄像头支持如 C920）
        cmd_h264 = [
            "ffmpeg",
            "-y",
            "-f", "v4l2",
            "-input_format", "h264",
            "-video_size", f"{width}x{height}",
            "-framerate", str(self._fps),
            "-i", self._device,
            "-c", "copy",
            filepath
        ]
        
        return cmd_h264
    
    def start_recording(self, filepath: str) -> None:
        """启动 FFmpeg 录制"""
        cmd = self._build_ffmpeg_cmd(filepath)
        
        try:
            # 启动 FFmpeg，捕获 stderr 以便调试
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,  # 捕获错误
                preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL)
            )
            
            # 立即检查是否启动失败（如格式不支持）
            time.sleep(0.5)  # 给 FFmpeg 一点时间初始化
            if self._process.poll() is not None:
                # 进程已退出，读取错误
                _, stderr = self._process.communicate()
                error_msg = stderr.decode() if stderr else "未知错误"
                logger.warning(f"FFmpeg H264 模式失败: {error_msg}")
                
                # 回退到 MJPEG + 软件编码（兼容性更好）
                logger.info("尝试回退到 MJPEG 模式...")
                self._start_mjpeg_recording(filepath)
                return
            
            logger.info(f"FFmpeg 开始录制 USB (H264 copy): {filepath}")
            
        except Exception as e:
            raise RuntimeError(f"FFmpeg 启动失败: {e}")
    
    def _start_mjpeg_recording(self, filepath: str) -> None:
        """
        回退方案：使用 MJPEG 输入 + 快速软件编码
        兼容性最好，但 CPU 占用较高
        """
        width, height = self._size

        # 使用更保守的参数，确保兼容性
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "v4l2",
            "-input_format", "mjpeg",
            "-video_size", f"{width}x{height}",
            "-framerate", str(self._fps),
            "-i", self._device,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",
            "-f", "h264",  # 明确指定输出格式为 H264 裸流
            filepath
        ]

        logger.debug(f"FFmpeg MJPEG 命令: {' '.join(cmd)}")

        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL)
        )

        # 等待更长时间检查是否启动成功
        time.sleep(1.0)
        if self._process.poll() is not None:
            _, stderr = self._process.communicate()
            error_msg = stderr.decode() if stderr else "未知错误"
            logger.error(f"MJPEG 模式失败详情: {error_msg}")
            raise RuntimeError(f"MJPEG 模式也失败: {error_msg}")

        logger.info(f"FFmpeg 开始录制 USB (MJPEG encode): {filepath}")
    
    def stop_recording(self) -> None:
        """停止录制"""
        if not self._process:
            return

        if self._process.poll() is None:
            # 先发送 SIGINT (Ctrl+C) 让 FFmpeg 优雅地关闭文件
            try:
                self._process.send_signal(signal.SIGINT)
                stdout, stderr = self._process.communicate(timeout=5)
                if self._process.returncode != 0:
                    err = stderr.decode()[-500:] if stderr else "未知错误"
                    # -22 表示参数错误，但文件可能已正确写入
                    if "signal" in err.lower() or self._process.returncode == -signal.SIGINT:
                        logger.debug(f"FFmpeg 被中断，返回码: {self._process.returncode}")
                    else:
                        logger.warning(f"FFmpeg 退出异常: {err}")
            except subprocess.TimeoutExpired:
                logger.warning("FFmpeg 未响应 SIGINT，尝试 SIGTERM")
                self._process.terminate()
                try:
                    self._process.communicate(timeout=3)
                except subprocess.TimeoutExpired:
                    logger.warning("FFmpeg 未响应，强制杀死")
                    self._process.kill()
                    self._process.wait()

        self._process = None
    
    def release(self) -> None:
        self.stop_recording()
        logger.info("USB 摄像头已释放")

    def capture_image(self, filepath: str) -> None:
        """使用 FFmpeg 拍照"""
        width, height = self._size
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "v4l2",
            "-input_format", "mjpeg",
            "-video_size", f"{width}x{height}",
            "-i", self._device,
            "-frames:v", "1",
            "-q:v", "2",
            filepath
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            error_msg = result.stderr.decode()[-300:] if result.stderr else "未知错误"
            raise RuntimeError(f"FFmpeg 拍照失败: {error_msg}")

        logger.info(f"USB 拍照完成: {filepath}")



class CameraManager:
    """
    统一摄像头管理器
    自动检测 CSI 或 USB，统一输出 H264 格式
    """
    
    def __init__(
        self, 
        output_dir: str | Path = "/tmp/videos",
        prefer_usb: bool = False,
        usb_device: str = "/dev/video0"
    ) -> None:
        self.output_dir: Path = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self._camera: BaseCamera | None = None
        self._camera_type: str = "none"
        self.current_file: Path | None = None
        self.is_recording: bool = False
        self.start_time: float = 0.0
        self._prefer_usb: bool = prefer_usb
        self._usb_device: str = usb_device
        
    def init_camera(
        self, 
        width: int = 1920, 
        height: int = 1080, 
        fps: int = 30
    ) -> bool:
        """
        初始化摄像头
        策略：优先 CSI（最佳质量），失败则 USB（FFmpeg）
        """
        if self._prefer_usb:
            return self._init_usb(width, height, fps)
        
        # 尝试 CSI
        if PICAMERA_AVAILABLE:
            csi = CSICamera()
            if csi.init(width, height, fps):
                self._camera = csi
                self._camera_type = "csi"
                return True
        
        logger.warning("CSI 不可用，尝试 USB + FFmpeg...")
        return self._init_usb(width, height, fps)
    
    def _init_usb(self, width: int, height: int, fps: int) -> bool:
        """初始化 USB 摄像头（通过 FFmpeg）"""
        # USB 摄像头通常不支持高分辨率，使用保守的默认参数
        # 优先使用 640x480@30fps，这是最通用的配置
        usb_width = min(width, 640)
        usb_height = min(height, 480)
        usb_fps = min(fps, 30)

        # 如果设备是高清摄像头，尝试 1280x720
        if Path(self._usb_device).exists():
            # 先尝试 640x480（兼容性最好）
            usb_cam = USBCamera(self._usb_device)
            if usb_cam.init(640, 480, 30):
                self._camera = usb_cam
                self._camera_type = "usb"
                return True

            # 如果失败，尝试请求的分辨率
            usb_cam = USBCamera(self._usb_device)
            if usb_cam.init(usb_width, usb_height, usb_fps):
                self._camera = usb_cam
                self._camera_type = "usb"
                return True

        return False
    
    def start_recording(self, execution_id: str, task_name: str = "") -> str:
        """开始录制，统一输出 .h264"""
        if not self._camera:
            raise RuntimeError("摄像头未初始化")
        
        if self.is_recording:
            raise RuntimeError("已经在录制中")
        
        # 统一使用 .h264 后缀（FFmpeg 和 Picamera2 都支持）
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_task: str = task_name.replace(" ", "_")[:50] if task_name else "untitled"
        filename: str = f"{timestamp}_{execution_id}_{safe_task}.h264"
        
        self.current_file = self.output_dir / filename
        
        self._camera.start_recording(str(self.current_file))
        self.is_recording = True
        self.start_time = time.time()
        
        logger.info(f"开始录制 ({self._camera_type.upper()}): {self.current_file}")
        return str(self.current_file)
    
    def stop_recording(self) -> Tuple[str | None, int]:
        """停止录制"""
        if not self.is_recording or not self._camera:
            return None, 0
        
        try:
            self._camera.stop_recording()
            self.is_recording = False
            
            duration: float = time.time() - self.start_time
            file_size: int = (
                self.current_file.stat().st_size 
                if self.current_file and self.current_file.exists() 
                else 0
            )
            
            logger.info(
                f"停止录制: {self.current_file}, "
                f"时长: {duration:.1f}s, 大小: {file_size/1024/1024:.2f}MB, "
                f"类型: {self._camera_type}"
            )
            return str(self.current_file), file_size
            
        except Exception as e:
            logger.error(f"停止录制失败: {e}")
            return None, 0
    
    def delete_recording(self) -> bool:
        """删除当前录制的文件"""
        if self.current_file and self.current_file.exists():
            try:
                self.current_file.unlink()
                logger.info(f"已删除视频: {self.current_file}")
                return True
            except Exception as e:
                logger.error(f"删除失败: {e}")
        return False
    
    def release(self) -> None:
        """释放资源"""
        if self._camera:
            self._camera.release()
            self._camera = None
        
        self.is_recording = False
        self.current_file = None
        self._camera_type = "none"
        logger.info("摄像头管理器已释放")
    
    def get_camera_type(self) -> str:
        """获取当前摄像头类型: 'csi', 'usb', 'none'"""
        return self._camera_type

    def capture_image(self, task_name: str = "") -> str:
        """拍照，返回文件路径"""
        if not self._camera:
            raise RuntimeError("摄像头未初始化")

        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_task: str = task_name.replace(" ", "_")[:50] if task_name else "capture"
        filename: str = f"{timestamp}_{safe_task}.jpg"

        image_path = self.output_dir / filename
        self._camera.capture_image(str(image_path))

        logger.info(f"拍照完成 ({self._camera_type.upper()}): {image_path}")
        return str(image_path)