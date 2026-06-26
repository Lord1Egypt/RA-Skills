#!/usr/bin/env python3
# 智能失禁状态提醒分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.smyx_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    SceneCodeEnum, ApiEnumCommonAiMixin


class ApiEnum(ApiEnumCommonAiMixin, ApiEnumParent):
    pass


class ConstantEnum(ConstantEnumParent):
    DEFAULT__USER_TYPE = "other"
    DEFAULT__DETECTION_MODE = "real-time"

    @classmethod
    def init(cls, config=None):
        super().init(config)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.INCONTINENCE_ALERT_ANALYSIS.value
