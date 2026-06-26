"""
xiang_query.py — 类象知识库查询引擎（完全开源版）

将 28 个类象 JSON 知识库（data/xiang/ 下 6 类别）展开为
人/物/时/空/状态五维语义映射，支持多语境上下文匹配。

MIT License — 完全开源，欢迎审查和贡献
"""

import json
import os
from typing import Dict, List, Optional, Any


class XiangQuery:
    """类象知识库查询引擎"""

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化查询引擎

        Args:
            data_dir: 类象 JSON 数据根目录
                      默认自动定位到 workspace/data/xiang
        """
        if data_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            workspace = os.path.dirname(os.path.dirname(script_dir))
            data_dir = os.path.join(workspace, "data", "xiang")
        self.data_dir = data_dir
        self._cache: Dict[str, dict] = {}
        self._index: Dict[str, str] = {}
        self._load_all()

    # ──── 数据加载 ─────────────────────────────

    def _load_all(self):
        """递归加载 data_dir 下所有 JSON 文件到缓存"""
        if not os.path.isdir(self.data_dir):
            return
        for root, _, files in os.walk(self.data_dir):
            for fn in files:
                if fn.endswith(".json"):
                    path = os.path.join(root, fn)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        symbol = data.get("symbol", "")
                        category = data.get("category", "")
                        self._cache[symbol] = data
                        self._index[symbol] = category
                    except Exception:
                        pass

    def available_symbols(self) -> List[str]:
        """列出所有已加载的符号"""
        return sorted(self._index.keys())

    def available_categories(self) -> List[str]:
        """列出所有已加载的分类"""
        cats = set(v for v in self._index.values())
        return sorted(cats)

    # ──── 精确查询 ─────────────────────────────

    def query(self, symbol: str, context: Optional[str] = None,
              dimension: Optional[str] = None) -> Optional[Dict]:
        """
        查询一个符号的类象数据

        Args:
            symbol:    符号名称，如 "乾"、"官鬼"、"青龙"
            context:   语境上下文，如 "career"、"health"
                       None = 返回所有语境
            dimension: 维度过滤，如 "person"、"state"
                       None = 返回所有维度

        Returns:
            {"symbol":..., "category":..., "context":..., "result":...}
            或 None（符号不存在）
        """
        data = self._cache.get(symbol)
        if data is None:
            return None

        contexts = data.get("contexts", {})

        if context and context in contexts:
            ctx_data = contexts[context]
            result = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": context,
                "result": result,
            }
        elif context:
            # 语境不存在 → fallback 到 general
            ctx_data = contexts.get("general", {})
            result = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": "general",
                "fallback": True,
                "result": result,
            }
        else:
            # 返回所有语境
            all_ctx = {}
            for ctx_name, ctx_data in contexts.items():
                all_ctx[ctx_name] = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": None,
                "result": all_ctx,
            }

    def _filter_dimension(self, ctx_data: dict, dimension: Optional[str]) -> dict:
        """按维度过滤语境数据"""
        if dimension:
            return {dimension: ctx_data.get(dimension, [])}
        return dict(ctx_data)

    # ──── 人类可读展开 ─────────────────────────

    _DIM_NAMES = {
        "person": "人物", "object": "物品", "time": "时间",
        "space": "空间", "state": "状态",
    }

    def expand_full(self, symbol: str, context: Optional[str] = None) -> str:
        """
        将一个符号展开为完整人类可读文本

        Args:
            symbol:  符号名称
            context: 语境

        Returns:
            多行文本字符串
        """
        result = self.query(symbol, context=context)
        if result is None:
            return f"【{symbol}】未找到对应的类象数据。"

        lines = []
        props = result.get("core_properties", [])
        wuxing = result.get("wu_xing", "")
        lines.append(f"【{symbol}】")
        lines.append(f"五行：{wuxing}　核心属性：{'、'.join(props)}")
        lines.append("")

        if context and result.get("context"):
            ctx_name = result["context"]
            data = result.get("result", {})
            lines.append(f"语境：{ctx_name}")
            lines.append(self._format_dimensions(data))
        else:
            all_ctx = result.get("result", {})
            for ctx_name in ["general", "career", "health", "relationship", "finance"]:
                if ctx_name in all_ctx:
                    lines.append(f"语境：{ctx_name}")
                    lines.append(self._format_dimensions(all_ctx[ctx_name]))
                    lines.append("")

        return "\n".join(lines).strip()

    def _format_dimensions(self, data: dict) -> str:
        """格式化维度数据为多行文本"""
        lines = []
        for dim, items in data.items():
            if items and dim != "core_properties":
                name = self._DIM_NAMES.get(dim, dim)
                lines.append(f"  {name}：{'、'.join(items)}")
        return "\n".join(lines)

    # ──── 批量查询 ─────────────────────────────

    def multi_query(self, symbols: List[str],
                    context: Optional[str] = None) -> List[Dict]:
        """批量查询多个符号"""
        results = []
        for sym in symbols:
            r = self.query(sym, context=context)
            if r:
                results.append(r)
        return results

    def expand_for_context(self, symbols: List[str], context: str) -> str:
        """针对同一语境批量展开多个符号"""
        parts = []
        for sym in symbols:
            text = self.expand_full(sym, context=context)
            parts.append(text)
        return "\n\n".join(parts)

    def get_wuxing_combo(self, symbols: List[str]) -> Dict[str, str]:
        """获取多个符号的五行"""
        result = {}
        for sym in symbols:
            data = self._cache.get(sym, {})
            result[sym] = data.get("wu_xing", "未知")
        return result
