#!/usr/bin/env python3
# 人员离岗实时监测技能配置文件
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
    DEFAULT__ABSENCE_THRESHOLD = 300  # 默认离岗阈值 300秒(5分钟)

    @classmethod
    def init(cls, config=None):
        super().init(config)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.PERSONNEL_LEAVE_POST_MONITORING.value
