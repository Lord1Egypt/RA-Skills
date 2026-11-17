"""术语表引擎 v4.7.0 — 人名/产品名/专业词强制校正（纯本地，无外部 API）

机制：
- 前置替换：翻译前用占位符隔离受保护术语，避免被机翻改写
- 后置校对：翻译后还原占位符并按术语表校正，统计命中率
- 未命中术语：输出「待确认清单」JSON + 校对报告

术语表 JSON 格式（源词 -> 目标词，支持按语言分表）：
    {"牛魔科技": "Niumo Technology", "大模型": "Large Model"}
或：
    {"en": {"牛魔科技": "Niumo Technology"}, "ja": {"牛魔科技": "ニウモ科技"}}

遵循死规则9：纯本地字符串替换，无外部 API 依赖。
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from ..logger import get_logger

logger = get_logger(__name__)

# 占位符前缀（不易与自然语言冲突）
PLACEHOLDER_PREFIX = "\uE000GL"  # 私用区字符 + GL


class GlossaryEngine:
    """术语表前置替换 + 后置校对引擎"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.glossary_cfg = config.get("glossary", {}) or config.get("editing", {}).get("translator", {})
        self.enabled = self.glossary_cfg.get("enabled", True)
        self.glossary_path = self.glossary_cfg.get("glossary_path") or self.glossary_cfg.get("path")
        self.pending_dir = self.glossary_cfg.get("pending_dir", ".cache/glossary")
        self.placeholder_template = PLACEHOLDER_PREFIX + "{idx}\uE001"

    # ---------- 加载 ----------

    def load(self, glossary_path: Optional[str] = None, target_lang: Optional[str] = None) -> Dict[str, str]:
        """加载术语表：支持扁平表与按语言分表"""
        path = glossary_path or self.glossary_path
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.warning(f"术语表加载失败: {path} - {e}")
            return {}

        # 按语言分表
        if isinstance(data.get(target_lang), dict):
            data = data.get(target_lang, {})
        elif isinstance(data.get("terms"), dict):
            data = data.get("terms", {})

        # 归一化 value 为字符串
        return {str(k): str(v) for k, v in data.items() if not isinstance(v, dict)}

    # ---------- 前置替换 ----------

    def protect(self, texts: List[str], glossary: Dict[str, str]) -> Tuple[List[str], Dict[str, str]]:
        """
        前置替换：把文本中命中的源术语替换为占位符。
        返回 (保护后文本列表, 占位符->目标词 映射)。
        """
        if not glossary:
            return list(texts), {}

        # 长词优先，避免短词先匹配造成嵌套错乱
        terms = sorted(glossary.keys(), key=lambda x: -len(x))
        mapping: Dict[str, str] = {}
        protected: List[str] = []

        for text in texts:
            out = text
            for term in terms:
                target = glossary[term]
                # 只保护尚未被占位符覆盖的原文术语
                if term not in out:
                    continue
                ph = self.placeholder_template.format(idx=len(mapping))
                # 用回调避免 re 特殊字符问题：直接字符串替换
                out = out.replace(term, ph)
                mapping[ph] = target
            protected.append(out)

        return protected, mapping

    # ---------- 后置校对 ----------

    def restore(self, texts: List[str], mapping: Dict[str, str]) -> Tuple[List[str], List[str]]:
        """
        后置校对：还原占位符为目标术语。
        返回 (还原后文本列表, 未还原占位符列表 -> 视为未命中待确认)。
        """
        restored: List[str] = []
        unresolved: List[str] = []
        for text in texts:
            out = text
            for ph, target in mapping.items():
                if ph in out:
                    out = out.replace(ph, target)
                else:
                    unresolved.append(target)
            restored.append(out)
        return restored, unresolved

    def proofread(
        self,
        original_texts: List[str],
        translated_texts: List[str],
        glossary: Dict[str, str],
        target_lang: str,
    ) -> Dict[str, Any]:
        """
        校对报告：统计术语命中率 + 未命中待确认清单。
        命中 = 源术语在原文出现，且目标词在对应译文中出现（或占位符成功还原）。
        """
        report: Dict[str, Any] = {
            "target_lang": target_lang,
            "glossary_size": len(glossary),
            "total_terms": 0,
            "hit_terms": 0,
            "hit_rate": 1.0,
            "hits": [],
            "pending": [],
            "pending_list_path": None,
        }
        if not glossary:
            return report

        pair_count = min(len(original_texts), len(translated_texts))
        seen_terms = set()

        for i in range(pair_count):
            src = original_texts[i] or ""
            dst = translated_texts[i] or ""
            for term, target in glossary.items():
                if term in src and term not in seen_terms:
                    seen_terms.add(term)
                    report["total_terms"] += 1
                    if target and target in dst:
                        report["hit_terms"] += 1
                        report["hits"].append({"term": term, "target": target, "segment": i})
                    else:
                        report["pending"].append({
                            "term": term,
                            "expected": target,
                            "found_in": i,
                            "reason": "译文中未找到目标术语，需人工确认",
                        })

        if report["total_terms"] > 0:
            report["hit_rate"] = round(report["hit_terms"] / report["total_terms"], 4)

        if report["pending"]:
            report["pending_list_path"] = self.write_pending_list(report["pending"], target_lang)

        logger.info(
            f"术语校对: 命中 {report['hit_terms']}/{report['total_terms']} "
            f"({report['hit_rate']:.0%}), 待确认 {len(report['pending'])}"
        )
        return report

    # ---------- 待确认清单 ----------

    def write_pending_list(self, pending: List[Dict[str, Any]], target_lang: str) -> Optional[str]:
        """把未命中术语写入 JSON 待确认清单"""
        os.makedirs(self.pending_dir, exist_ok=True)
        path = os.path.join(self.pending_dir, f"glossary_pending_{target_lang}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "target_lang": target_lang,
                    "generated_by": "glossary_engine v4.7.0",
                    "pending": pending,
                }, f, ensure_ascii=False, indent=2)
            return path
        except Exception as e:
            logger.warning(f"待确认清单写入失败: {e}")
            return None
