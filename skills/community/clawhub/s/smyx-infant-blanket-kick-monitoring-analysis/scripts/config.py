#!/usr/bin/env python3
# 婴儿蹬被监测分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.smyx_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    ApiEnumCommonAiMixin

SceneCodeEnum = ConstantEnumBase.SceneCodeEnum


class ApiEnum(ApiEnumCommonAiMixin, ApiEnumParent):
    pass


class ConstantEnum(ConstantEnumParent):
    @classmethod
    def init(cls, config=None):
        super().init(config)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.INFANT_BLANKET_KICK_MONITORING_ANALYSIS.value
