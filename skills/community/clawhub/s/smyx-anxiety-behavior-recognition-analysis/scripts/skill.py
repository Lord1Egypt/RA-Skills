#!/usr/bin/env python3
import json

from .config import ApiEnum, ConstantEnum

from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase

from skills.smyx_analysis.scripts.skill import Skill as SkillParent
from skills.smyx_common.scripts.util import JsonUtil


class Skill(SkillParent):
    def __init__(self):
        super().__init__()

    def get_output_analysis_content_head(self, result=None):
        return f"📊 焦虑症相关行为（搓手/咬指甲/来回踱步）识别结构化结果"

    def get_output_analysis_content_foot(self, result):
        pass


skill = Skill()
