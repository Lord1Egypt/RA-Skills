"""
tplink.py - TP-Link 摄像头 ONVIF PTZ 实现

型号：TL-IPC44AW-COLOR
  - ONVIF 端口：2020
  - 认证：WS-UsernameToken Digest
  - 关键：Zoom=0 时必须省略 Zoom 元素，否则返回 500
  - 凭证从 camera-devices.json 动态读取，无硬编码
"""

import logging
import time

from .onvif_ptz_control import TPClient
from .base_brand import BrandBase

logger = logging.getLogger(__name__)


class TPLinkCamera(BrandBase):

    def __init__(self, config: dict):
        super().__init__(config)
        # 从设备配置动态创建客户端（无硬编码凭证）
        self._client = TPClient(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.pass_,
            ptz_token=self.config.get("ptz_token", "PTZTOKEN"),
        )

    def _stop(self):
        return self._client.stop()

    def _do_continuous_move(self, pan_vel: float, tilt_vel: float, zoom_vel: float) -> bool:
        return self._client.move_cont(pan_vel, tilt_vel, zoom_vel)

    def _do_absolute_move(self, pan: float, tilt: float, zoom: float) -> bool:
        return self._client.move_abs(pan, tilt, zoom)

    def _do_stop(self) -> bool:
        return self._client.stop()

    def nod(self, times: int = 3, tilt_target: float = 0.5, duration: float = 0.5):
        """点头：向下 → 停 → 向上 → 停 → 归中，重复 N 次。"""
        for _ in range(times):
            self._client.move_abs(0, tilt_target, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)
            self._client.move_abs(0, -tilt_target, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)
            self._client.move_abs(0, 0, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)

    def shake(self, times: int = 3, pan_target: float = 0.5, duration: float = 0.5):
        """摇头：向左 → 停 → 向右 → 停 → 归中，重复 N 次。"""
        for _ in range(times):
            self._client.move_abs(-pan_target, 0, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)
            self._client.move_abs(pan_target, 0, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)
            self._client.move_abs(0, 0, 0)
            time.sleep(duration)
            self._client.stop()
            time.sleep(0.15)

    def _get_status_raw(self):
        from protocol.base import PTZStatus
        pos, zoom_val, status = self._client.get_status()
        return PTZStatus(pan=pos[0], tilt=pos[1], zoom=zoom_val or 0.0, status=status)

    def zoom_in(self, duration: float = 2.0, speed: float = 1.0):
        if not self._cap_zoom.supported:
            return
        steps = max(1, int(duration / 0.2))
        for _ in range(steps):
            self._client.move_abs(0, 0, min(1.0, speed))
            time.sleep(0.2)

    def zoom_out(self, duration: float = 2.0, speed: float = 0.0):
        if not self._cap_zoom.supported:
            return
        steps = max(1, int(duration / 0.2))
        for _ in range(steps):
            self._client.move_abs(0, 0, speed)
            time.sleep(0.2)

    # ---- RTSP / 调阅 ----

    def get_rtsp_url(self, stream: str = "main") -> str:
        """返回 TP-Link RTSP URL。密码中特殊字符自动 URL 编码。"""
        import urllib.parse
        user_enc = urllib.parse.quote(self.user, safe="")
        pass_enc = urllib.parse.quote(self.pass_, safe="")
        rtsp_port = self.config.get("rtsp_port", 554)
        rtsp_path = self.config.get("rtsp_path", "stream1")
        return (
            f"rtsp://{user_enc}:{pass_enc}"
            f"@{self.host}:{rtsp_port}/{rtsp_path}"
        )

    def open_vlc(self) -> bool:
        """调用 VLC 打开实时流（需配置 vlc_path）。"""
        import subprocess
        vlc = self.config.get("vlc_path")
        if not vlc:
            return False
        rtsp = self.get_rtsp_url()
        try:
            subprocess.Popen([vlc, rtsp], start_new_session=True)
            return True
        except Exception:
            return False
