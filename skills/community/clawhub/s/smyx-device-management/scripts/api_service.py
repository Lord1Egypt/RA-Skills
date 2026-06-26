#!/usr/bin/env python3

import os
import sys

from skills.smyx_common.scripts.dao import UserDao

# 添加根目录到路径
# root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# if root_dir not in sys.path:
#     sys.path.insert(0, root_dir)

# 直接导入，不需要相对路径
from .config import ApiEnum, ConstantEnum

from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase
from skills.smyx_common.scripts import RequestUtil
import asyncio


class ApiService(ApiServiceBase):

    def __init__(self):
        super().__init__()
        self._shared_user_token = None

    def page(self, pageNum=None, pageSize=None, *args, **argss):
        return super().page(ApiEnum.PAGE_URL, pageNum, pageSize, *args, **argss)

    async def list(self, *args, **argss):
        data = argss.get("data", {})
        ConstantEnum.DEFAULT__SCENE_CODE and data.setdefault("sceneCodes", ConstantEnum.DEFAULT__SCENE_CODE)
        argss.setdefault("data", data)
        result = super().list(None, *args, **argss)
        if result:
            for item in result:
                camera_sn = item["cameraSn"]
                camera_type = item["cameraType"]
                if camera_type == ApiEnum.CameraTypeEnum.TAN_GE.value:
                    camera_device_player_info = await self.get_tange_device_player_info(camera_sn)
                    if camera_device_player_info:
                        import urllib.parse
                        token = urllib.parse.quote(camera_device_player_info.get('token'), safe='')
                        device_connection_string = urllib.parse.quote(
                            camera_device_player_info.get('deviceConnectionString'), safe='')
                        hls_url = f"{ApiEnum.BASE_URL_OPEN_H5}/device-player/?deviceId={camera_sn}&token={token}&deviceConnectionString={device_connection_string}"
                        item["hlsUrl"] = hls_url
        return result

    def add(self, item: dict):
        item and ConstantEnum.DEFAULT__SCENE_CODE and item.setdefault("sceneCodes", [ConstantEnum.DEFAULT__SCENE_CODE])
        return super().add(ApiEnum.ADD_URL, item)

    def edit(self, item: dict):
        return super().edit(ApiEnum.EDIT_URL, item)

    def delete(self, cameraSn):
        data = {
            "cameraSn": cameraSn
        }
        return super().delete(ApiEnum.DELETE_URL, data, options={"dataAsParams": True})

    async def get_tange_device_player_info(self, camera_sn):
        async_tasks = [self.async__get_shared_user_token(), self.async__get_camera_connect_info(camera_sn)]
        results = await asyncio.gather(*async_tasks, return_exceptions=True)

        result1, result2 = results

        result = None
        if not isinstance(result1, Exception) and not isinstance(result2, Exception) and result1 and result2:
            result = {
                "deviceId": camera_sn,
                "token": result1,
                "deviceConnectionString": result2,
            }
        return result

    async def async__get_camera_connect_info(self, camera_sn):
        return await asyncio.to_thread(self.get_camera_connect_info, camera_sn)

    def get_camera_connect_info(self, camera_sn):
        params = {
            "cameraSn": camera_sn
        }
        return self.http_post(ApiEnum.GET_CAMERA_CONNECT_INFO, params=params)

    async def async__get_shared_user_token(self):
        if not self._shared_user_token:
            self._shared_user_token = await asyncio.to_thread(self.get_shared_user_token)
        return self._shared_user_token;

    def get_shared_user_token(self):
        return self.http_post(ApiEnum.GET_SHARED_USER_TOKEN)

    def control_ptz(self, cameraSn: str, direction: str, speed: int = 5):
        """
        控制云台转动
        :param cameraSn: 设备序列号
        :param direction: 方向 up/down/left/right
        :param speed: 转动速度 1-10 默认5
        :return: API响应结果
        """
        url = ApiEnum.CONTROL_MOVE_PTZ_URL
        match direction:
            case "up":
                direction = "0"
            case "down":
                direction = "1"
                speed = -speed
            case "left":
                direction = "2"
                speed = -speed
            case "right":
                direction = "3"
            case "reset":
                url = ApiEnum.CONTROL_RESET_PTZ_URL
            case _:
                raise ValueError("无效的转动方向")
        params = {
            "cameraSn": cameraSn,
            "direction": direction,
            "speed": speed,
            "duration": 1000
        }
        return self.http_post(url, params=params, options={"dataAsParams": True})

    def control_audio(self, cameraSn: str, enable: bool):
        """
        控制音频开关
        :param cameraSn: 设备序列号
        :param enable: True开启，False关闭
        :return: API响应结果
        """
        params = {
            "cameraSn": cameraSn,
            "sound": enable,
        }
        return self.http_post(ApiEnum.CONTROL_AUDIO_URL, params=params, options={"dataAsParams": True})
