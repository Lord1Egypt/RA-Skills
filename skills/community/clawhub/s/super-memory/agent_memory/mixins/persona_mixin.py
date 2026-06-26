from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class PersonaMixin:
    def build_persona(self) -> dict:
        """
        构建数字孪生人格画像。

        返回: 包含认知风格、决策模式、情感模式、知识边界和价值观的统一画像
        """
        return self.digital_twin.build_unified_profile()

    def get_persona(self) -> dict:
        """
        获取最新的数字孪生人格画像。

        返回: 最新的人格画像，或 None（如果尚未构建）
        """
        return self.digital_twin.get_latest_profile()