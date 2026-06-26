#!/usr/bin/env python3
# 安全驾驶行为分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.face_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    SceneCodeEnum, ApiEnumCommonAiMixin


class ApiEnum(ApiEnumCommonAiMixin, ApiEnumParent):
    pass


class ConstantEnum(ConstantEnumParent):
    DEFAULT__ANALYSIS_TYPE = "comprehensive"

    @classmethod
    def init(cls, config=None):
        super().init(config)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.DRIVE_ANALYSIS.value
