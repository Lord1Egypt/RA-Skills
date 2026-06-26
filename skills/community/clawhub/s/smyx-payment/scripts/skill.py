#!/usr/bin/env python3
import datetime
import os
import sys

from .config import ApiEnum, ConstantEnum

from .api_service import ApiService

from skills.smyx_common.scripts.util import CommonUtil, JsonUtil
from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase
from skills.smyx_common.scripts.base import BaseSkill
from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase


class Skill(BaseSkill, ApiService):
    def __init__(self):
        super().__init__()


skill = Skill()
