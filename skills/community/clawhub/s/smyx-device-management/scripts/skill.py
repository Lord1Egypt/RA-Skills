#!/usr/bin/env python3
import os
import sys

from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase
from skills.smyx_common.scripts.base import BaseSkill
from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase

from .api_service import ApiService


class Skill(BaseSkill, ApiService):

    def __init__(self):
        super().__init__()


skill = Skill()
