from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class EncyclopediaMixin:
    def get_encyclopedia(self, category: str = None) -> list[dict]:
        """获取百科条目"""
        return self.distiller.get_encyclopedia(category=category)

    def search_encyclopedia(self, query: str) -> list[dict]:
        """搜索百科"""
        return self.distiller.search_encyclopedia(query)

    def export_encyclopedia(self, output_path: str = None) -> str:
        """导出百科为 Markdown"""
        return self.distiller.export_encyclopedia(output_path)