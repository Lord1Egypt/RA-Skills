#!/usr/bin/env python3
# 宠物检测技能配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.smyx_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    SceneCodeEnum, ApiEnumCommonAiMixin


class ApiEnum(ApiEnumCommonAiMixin, ApiEnumParent):
    pass


class ConstantEnum(ConstantEnumParent):
    DEFAULT__MEDIA_TYPE = "video"
    DEFAULT__CONFIDENCE_THRESHOLD = 0.5

    @classmethod
    def init(cls, config=None):
        super().init(config)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.PET_DETECTION_ANALYSIS.value
