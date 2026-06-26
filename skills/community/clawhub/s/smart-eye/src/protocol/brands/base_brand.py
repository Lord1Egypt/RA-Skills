"""
base_brand.py - 品牌实现基类

继承 CameraBase，提供品牌公共逻辑。
各品牌（TP-Link、华为等）继承此类并实现协议细节。
"""

from ..base import CameraBase


class BrandBase(CameraBase):
    """
    品牌实现基类。

    提供：
      - 品牌名称（self.brand_name）
      - profile_token（ONVIF Media Profile Token）
      - 子类实现 _do_continuous_move / _do_absolute_move / _do_stop

    使用示例：
        class MyCamera(BrandBase):
            def _do_continuous_move(self, pan_vel, tilt_vel, zoom_vel):
                # 调用 self.onvif.continuous_move(self.profile_token, ...)
                ...
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.brand_name = config.get("brand", "unknown").lower()
        # 多数 ONVIF 设备的 Media Profile Token 就是 "Profile_1"
        # 部分设备需要先调用 GetProfiles 获取，这里先用固定值
        self.profile_token = config.get("profile_token", "Profile_1")

    def _get_status_raw(self):
        from ...protocol.base import PTZStatus
        try:
            code, body = self.onvif.get_status(self.profile_token)
            if code == 200:
                # 简单解析 <tt:PanTilt x="..." y="..."/> 和 <tt:Zoom x="..."/>
                import re
                pan_m = re.search(r'<tt:PanTilt[^>]+x="([^"]+)"[^>]+y="([^"]+)"', body)
                zoom_m = re.search(r'<tt:Zoom[^>]+x="([^"]+)"', body)
                status_m = re.search(r'<tt:StatusState[^>]+x="([^"]+)"', body)
                if pan_m:
                    pan, tilt = float(pan_m.group(1)), float(pan_m.group(2))
                    zoom = float(zoom_m.group(1)) if zoom_m else 0.0
                    st = status_m.group(1) if status_m else "unknown"
                    return PTZStatus(pan=pan, tilt=tilt, zoom=zoom, status=st)
        except Exception:
            pass
        return PTZStatus(pan=0.0, tilt=0.0, zoom=0.0, status="unknown")

    def _send_command(self, action: str, **kwargs) -> bool:
        """根据 action 分发到对应私有方法。"""
        if action == "continuous_move":
            pan_vel  = kwargs.get("pan_vel", 0.0)
            tilt_vel = kwargs.get("tilt_vel", 0.0)
            zoom_vel = kwargs.get("zoom_vel", 0.0)
            return self._do_continuous_move(pan_vel, tilt_vel, zoom_vel)
        elif action == "absolute_move":
            return self._do_absolute_move(kwargs["pan"], kwargs["tilt"], kwargs["zoom"])
        elif action == "stop":
            return self._do_stop()
        return False

    # ---- 子类必须实现 ----

    def _do_continuous_move(self, pan_vel: float, tilt_vel: float, zoom_vel: float) -> bool:
        """
        连续移动实现。
        使用 self.onvif.continuous_move(self.profile_token, pan_vel, tilt_vel, zoom_vel)
        """
        raise NotImplementedError

    def _do_absolute_move(self, pan: float, tilt: float, zoom: float) -> bool:
        raise NotImplementedError

    def _do_stop(self) -> bool:
        raise NotImplementedError

    # ---- 默认实现：使用 ONVIF ----

    def _stop(self):
        code, _ = self.onvif.stop(self.profile_token)
        return code == 200
