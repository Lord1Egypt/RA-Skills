"""
base.py - 摄像头抽象基类

所有品牌的摄像头实现都必须继承 CameraBase，
并实现以下方法：
  - move_left() / move_right() / move_up() / move_down()
  - nod() / shake()
  - zoom_in() / zoom_out()
  - home() / stop()
  - get_status()

PTZ 能力由配置文件中的 ptz 字段描述，基类提供辅助方法供子类查询。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass
class PTZStatus:
    """当前云台状态。"""
    pan: float       # [-1, 1]
    tilt: float      # [-1, 1]
    zoom: float      # [0, 1]
    status: str      # e.g. "idle", "moving"


@dataclass
class PTZCapability:
    """单个轴的能力描述。"""
    supported: bool
    range: Tuple[float, float]      # e.g. (-1, 1) 或 (0, 1)
    axis_type: str = "continuous"   # "continuous" | "absolute" | "none"
    note: str = ""


class CameraBase(ABC):
    """
    摄像头基类。

    子类需要：
      1. 在 __init__ 中调用 super().__init__(config)
      2. 实现 _get_status_raw() 和 _send_command()
    """

    def __init__(self, config: dict):
        """
        Args:
            config: 设备配置 dict（来自 camera-devices.json）
        """
        self.config = config
        self.host = config["host"]
        self.port = config["port"]
        self.user = config["user"]
        self.pass_ = config["pass"]
        self.model = config.get("model", "unknown")
        self.id = config["id"]

        # 解析 PTZ 能力
        ptz_cfg = config.get("ptz", {})
        self._cap_pan:  PTZCapability = self._parse_cap(ptz_cfg.get("pan"))
        self._cap_tilt: PTZCapability = self._parse_cap(ptz_cfg.get("tilt"))
        self._cap_zoom: PTZCapability = self._parse_cap(ptz_cfg.get("zoom"))

    def _parse_cap(self, cfg: Optional[dict]) -> PTZCapability:
        """将配置 dict 解析为 PTZCapability。"""
        if not cfg:
            return PTZCapability(supported=False, range=(0, 0))
        return PTZCapability(
            supported=cfg.get("supported", False),
            range=tuple(cfg.get("range", [0, 0])),
            axis_type=cfg.get("type", "continuous"),
            note=cfg.get("note", ""),
        )

    # ---- 公共 API ----

    def nod(self, times: int = 3, speed: float = 0.8, duration: float = 0.6):
        """点头：向上→停→向下→停，重复 N 次。"""
        for _ in range(times):
            self._continuous_move(0, speed, 0)
            self._sleep(duration)
            self.stop()
            self._sleep(0.1)
            self._continuous_move(0, -speed, 0)
            self._sleep(duration)
            self.stop()
            self._sleep(0.1)

    def shake(self, times: int = 3, speed: float = 0.8, duration: float = 0.6):
        """摇头：向左→停→向右→停，重复 N 次。"""
        for _ in range(times):
            self._continuous_move(-speed, 0, 0)
            self._sleep(duration)
            self.stop()
            self._sleep(0.1)
            self._continuous_move(speed, 0, 0)
            self._sleep(duration)
            self.stop()
            self._sleep(0.1)

    def move_left(self, duration: float = 2.0, speed: float = 0.5):
        self._continuous_move(-speed, 0, 0)
        self._sleep(duration)
        self.stop()

    def move_right(self, duration: float = 2.0, speed: float = 0.5):
        self._continuous_move(speed, 0, 0)
        self._sleep(duration)
        self.stop()

    def move_up(self, duration: float = 2.0, speed: float = 0.5):
        self._continuous_move(0, speed, 0)
        self._sleep(duration)
        self.stop()

    def move_down(self, duration: float = 2.0, speed: float = 0.5):
        self._continuous_move(0, -speed, 0)
        self._sleep(duration)
        self.stop()

    def zoom_in(self, duration: float = 2.0, speed: float = 0.8):
        self._continuous_move(0, 0, speed)
        self._sleep(duration)
        self.stop()

    def zoom_out(self, duration: float = 2.0, speed: float = 0.8):
        self._continuous_move(0, 0, -speed)
        self._sleep(duration)
        self.stop()

    def home(self):
        """归中：绝对移动到 (0, 0, 0)。"""
        self._absolute_move(0, 0, 0)

    def stop(self):
        """立即停止。"""
        self._stop()

    def get_status(self) -> PTZStatus:
        """返回当前云台状态。"""
        return self._get_status_raw()

    def is_supported(self, axis: str) -> bool:
        """查询指定轴是否支持。"""
        cap = getattr(self, f"_cap_{axis}", None)
        return cap.supported if cap else False

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.model} {self.host}>"

    # ---- RTSP / 截图 ----

    def get_rtsp_url(self, stream: str = "main") -> str:
        """
        返回 RTSP 流地址。
        子类必须实现，根据设备类型返回正确的 RTSP URL。
        """
        raise NotImplementedError

    def open_vlc(self) -> bool:
        """
        调用 VLC 打开实时流。
        需要在 camera-devices.json 中配置 vlc_path。
        Returns:
            True 成功启动 VLC，False 未配置 vlc_path 或启动失败
        """
        import subprocess
        vlc_path = self.config.get("vlc_path")
        if not vlc_path:
            return False
        rtsp = self.get_rtsp_url()
        try:
            subprocess.Popen([vlc_path, rtsp], start_new_session=True)
            return True
        except Exception:
            return False

    def snapshot(self, save_dir: str = None) -> str:
        """
        从 RTSP 流截取一帧并保存为 JPG。
        Args:
            save_dir: 保存目录，默认为 Skill 的 snapshots/ 目录
        Returns:
            保存的文件路径
        Raises:
            RuntimeError: 无法连接 RTSP 或读取画面失败
        """
        import cv2
        import os
        from datetime import datetime

        if save_dir is None:
            save_dir = Path(__file__).parent.parent.parent / "snapshots"
        os.makedirs(save_dir, exist_ok=True)

        rtsp = self.get_rtsp_url()
        cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise RuntimeError(f"无法从 {self.id} 的 RTSP 流读取画面，请检查网络和 RTSP 地址")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.id}_{ts}.jpg"
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, frame)
        return filepath

    # ---- 子类必须实现 ----

    @abstractmethod
    def _get_status_raw(self) -> PTZStatus:
        """获取摄像头当前 PTZ 状态。"""
        ...

    @abstractmethod
    def _send_command(self, action: str, **kwargs) -> bool:
        """
        发送原始命令给摄像头。
        子类负责实现 HTTP / ONVIF / 私有协议等细节。

        Returns:
            True 表示命令被摄像头接受，False 表示失败
        """
        ...

    # ---- 子类可覆盖的默认实现 ----

    def _continuous_move(self, pan_vel: float, tilt_vel: float, zoom_vel: float):
        """
        连续移动。
        默认实现：若无对应能力则跳过。
        子类（如华为）需要覆盖以使用正确的 SOAP Body 结构。
        """
        # zoom=0 搭配 pan/tilt=0 会导致 TP-Link 返回 500，需要子类特化
        if pan_vel == 0 and tilt_vel == 0 and zoom_vel == 0:
            return
        self._send_command("continuous_move",
                           pan_vel=pan_vel, tilt_vel=tilt_vel, zoom_vel=zoom_vel)

    def _absolute_move(self, pan: float, tilt: float, zoom: float):
        self._send_command("absolute_move", pan=pan, tilt=tilt, zoom=zoom)

    def _stop(self):
        self._send_command("stop")

    # ---- 工具方法 ----

    def _sleep(self, seconds: float):
        import time
        time.sleep(seconds)
