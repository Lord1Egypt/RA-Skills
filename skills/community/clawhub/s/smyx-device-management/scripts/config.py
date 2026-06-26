#!/usr/bin/env python3
# 中医面诊分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase, ConstantEnum as ConstantEnumBase


class ApiEnum(ApiEnumBase):
    PAGE_URL = "/web/camera/page"

    GET_URL = "/web/camera/query-one"

    ADD_URL = "/web/camera/register"

    EDIT_URL = "/web/camera/modify-camera-partial-info"

    DELETE_URL = "/web/camera/delete"

    GET_SHARED_USER_TOKEN = '/api/tange/get-shared-user-token'

    GET_CAMERA_CONNECT_INFO = "/api/tange/get-camera-connect-info"

    CONTROL_MOVE_PTZ_URL = "/web/camera/move-ptz"

    CONTROL_RESET_PTZ_URL = "/web/camera/reset-ptz"

    CONTROL_AUDIO_URL = "/web/camera/reset-ptz"

    class CameraTypeEnum(Enum):
        DA_HUA = "DA_HUA"
        TAN_GE = "TAN_GE"


class ConstantEnum(ConstantEnumBase):
    DEFAULT__APP_ID_TANGE = "AD_32vKWD5JmHWfmgajGG0aeUwVcV4"

    @classmethod
    def init(cls, config=None):
        super().init(config)
