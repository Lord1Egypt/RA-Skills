"""
huawei.py - 华为摄像头 ONVIF PTZ 实现

型号：D2150-10-I-P（枪机，固定镜头）
  - ONVIF 端口：80
  - SOAP 命名空间：SOAP 1.1（旧版，与 TP-Link 不同）
  - 认证：鉴权关闭，无密码
  - 注意：此型号为枪机（固定镜头），PTZ 命令返回 200 但镜头物理上不动
  - Profile Token: Profile_1

扩展：其他华为 ONVIF 摄像头通常也是 SOAP 1.1 + 无认证模式，
      只需修改 camera-devices.json 中的 host/port/aliases。
⚠️  不含硬编码凭证，不依赖用户 workspace 下的外部文件。
"""

import logging
import time

from .base_brand import BrandBase
from . import huawei_ptz as _huawei_ptz

logger = logging.getLogger(__name__)


class HuaweiCamera(BrandBase):

    def __init__(self, config: dict):
        super().__init__(config)
        self._profile = self.config.get("profile_token", "Profile_1")

    # ---- 底层 PTZ ----

    def _do_continuous_move(self, pan_vel: float, tilt_vel: float, zoom_vel: float) -> bool:
        if pan_vel == 0 and tilt_vel == 0 and zoom_vel == 0:
            return True
        code, _ = _huawei_ptz.continuous_move(
            self.host, self.port, self._profile, pan_vel, tilt_vel, zoom_vel
        )
        return code == 200

    def _do_absolute_move(self, pan: float, tilt: float, zoom: float) -> bool:
        code, _ = _huawei_ptz.absolute_move(
            self.host, self.port, self._profile, pan, tilt, zoom
        )
        return code == 200

    def _do_stop(self) -> bool:
        code, _ = _huawei_ptz.stop(self.host, self.port, self._profile)
        return code == 200

    def _stop(self):
        """华为专用 stop（避免 BrandBase._stop 使用不存在的 self.onvif）。"""
        return self._do_stop()

    # ---- nod / shake：ContinuousMove ----

    def nod(self, times: int = 3, tilt_speed: float = 0.5, duration: float = 0.6):
        """点头：向上 → 停 → 向下 → 停，重复 N 次（华为只支持 ContinuousMove）。"""
        for _ in range(times):
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, 0, tilt_speed, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, 0, -tilt_speed, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, 0, 0, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)

    def shake(self, times: int = 3, pan_speed: float = 0.5, duration: float = 0.6):
        """摇头：向左 → 停 → 向右 → 停，重复 N 次（华为只支持 ContinuousMove）。"""
        for _ in range(times):
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, -pan_speed, 0, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, pan_speed, 0, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)
            _huawei_ptz.continuous_move(self.host, self.port, self._profile, 0, 0, 0)
            time.sleep(duration)
            _huawei_ptz.stop(self.host, self.port, self._profile)
            time.sleep(0.15)

    # ---- 状态查询 ----

    def _get_status_raw(self):
        from protocol.base import PTZStatus
        code, pan, tilt, zoom, status = _huawei_ptz.get_status(
            self.host, self.port, self._profile
        )
        return PTZStatus(pan=pan, tilt=tilt, zoom=zoom, status=status if code == 200 else "error")

    # ---- RTSP 流地址（供参考）----

    def get_rtsp_url(self, stream: str = "main") -> str:
        """返回华为 RTSP URL。"""
        import urllib.parse
        user_enc = urllib.parse.quote(self.user, safe="")
        pass_enc = urllib.parse.quote(self.pass_, safe="")
        rtsp_port = self.config.get("rtsp_port", 554)
        base_path = self.config.get("rtsp_path", "LiveMedia/ch1/Media1")
        if stream == "sub":
            base_path = base_path.replace("Media1", "Media2")
        return f"rtsp://{user_enc}:{pass_enc}@{self.host}:{rtsp_port}/{base_path}"

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
