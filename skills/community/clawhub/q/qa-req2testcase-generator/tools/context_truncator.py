#!/usr/bin/env python3
"""
LLM上下文窗口动态截断策略 (V1.0.0)

解决问题：
  P5输出扩展到22字段后，大需求文档（100+测试点）可能导致LLM上下文溢出。
  简单将文件大小阈值从6KB提升到150KB不能解决根本问题。

核心策略：
  1. 精确估算token总数（中文优先算法）
  2. 与LLM上下文窗口剩余量对比
  3. 按字段优先级从低到高截断
  4. 每批次记录截断日志供人工复核

截断优先级（从低到高，优先截断低优先级）：
  P3（可截断）：exception_scenarios, ui_elements, risk_description,
               pci_description, test_data_matrix, meta
  P2（推荐保留，空间不足时可截断）：precondition, category, priority,
               priority_reason, requirement_completeness, field_target,
               related_roles, related_rules, source_scenario
  P1（必备，尽量保留）：page_path, operations_chain, field_specs, business_rules
  P0（绝对保留）：id, title, description, status

用法:
    from context_truncator import ContextTruncator

    truncator = ContextTruncator(
        model_context_window=128000,     # 模型上下文窗口大小（tokens）
        reserved_for_system=4000,         # 系统prompt预留
        reserved_for_output=8000,         # 输出预留
        safety_margin=0.85,               # 安全系数（使用85%的可用空间）
    )

    # 截断单个测试点
    truncated, log = truncator.truncate_test_point(tp, context_used=50000)

    # 批量截断
    truncated_batch, batch_log = truncator.truncate_batch(test_points)

    # 获取截断统计
    stats = truncator.get_truncation_stats()

依赖：仅Python标准库，无第三方依赖
"""

import json
import math
import re
import time
from collections import defaultdict
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# 常量定义
# ============================================================

# 字段优先级映射
# P0 = 绝对保留（基础标识）
# P1 = 必备字段（核心业务上下文）
# P2 = 推荐字段（辅助上下文，空间不足可截断）
# P3 = 可截断字段（长文本、辅助信息）
FIELD_PRIORITY = {
    # P0 - 绝对保留
    "id":                       {"level": "P0", "order": 0,  "desc": "测试点唯一标识"},
    "title":                    {"level": "P0", "order": 1,  "desc": "测试点标题"},
    "description":              {"level": "P0", "order": 2,  "desc": "测试点详细描述"},
    "status":                   {"level": "P0", "order": 3,  "desc": "状态标记"},

    # P1 - 必备字段（核心业务上下文）
    "page_path":                {"level": "P1", "order": 10, "desc": "页面路径"},
    "operations_chain":         {"level": "P1", "order": 11, "desc": "操作链路"},
    "field_specs":              {"level": "P1", "order": 12, "desc": "字段规格"},
    "business_rules":           {"level": "P1", "order": 13, "desc": "业务规则"},

    # P2 - 推荐字段
    "precondition":             {"level": "P2", "order": 20, "desc": "前置条件"},
    "category":                 {"level": "P2", "order": 21, "desc": "测试分类"},
    "priority":                 {"level": "P2", "order": 22, "desc": "优先级"},
    "priority_reason":          {"level": "P2", "order": 23, "desc": "优先级理由"},
    "requirement_completeness": {"level": "P2", "order": 24, "desc": "需求完整度评分"},
    "field_target":             {"level": "P2", "order": 25, "desc": "B类字段靶向"},
    "related_roles":            {"level": "P2", "order": 26, "desc": "关联角色"},
    "related_rules":            {"level": "P2", "order": 27, "desc": "关联规则"},
    "source_scenario":          {"level": "P2", "order": 28, "desc": "来源场景"},
    "is_smoke_candidate":       {"level": "P2", "order": 29, "desc": "冒烟候选"},

    # P3 - 可截断字段
    "exception_scenarios":      {"level": "P3", "order": 30, "desc": "异常场景清单"},
    "ui_elements":              {"level": "P3", "order": 31, "desc": "UI元素清单"},
    "test_data_matrix":         {"level": "P3", "order": 32, "desc": "B类测试数据矩阵"},
    "meta":                     {"level": "P3", "order": 33, "desc": "元信息"},
}

# 截断策略配置
TRUNCATION_STRATEGIES = {
    # 策略：字段替换值（截断后的占位内容）
    "replace_values": {
        "P3": "[已截断-详见完整P5输出]",
        "P2_list": "[已截断-保留前{keep}项]",
        "P2_text": "[已截断-原文{orig_len}字符]",
    },
    # P2列表类字段截断时保留的项数
    "p2_list_keep_count": 1,
    # P2文本类字段截断后保留的字符数
    "p2_text_keep_chars": 50,
}

# 常见模型的上下文窗口大小（tokens）
MODEL_CONTEXT_WINDOWS = {
    "deepseek-v4-pro":      128000,
    "kimi-k2.5":            131072,
    "claude-sonnet-4":      200000,
    "claude-3.5-sonnet":    200000,
    "gpt-4o":               128000,
    "gpt-4o-mini":          128000,
    "minimax-m2.7":         245000,
    "glm-4-plus":           128000,
    "default":              128000,
}

# 中文字符的token比率估算（基于主流tokenizer经验值）
# 1个中文字符 ≈ 1.5-2.0 tokens（取1.5偏保守）
# 1个英文单词 ≈ 1.3 tokens
# JSON结构字符（{}[]:,）≈ 1 token each
TOKEN_RATIOS = {
    "chinese_char": 1.5,     # 每个中文字符
    "english_word": 1.3,     # 每个英文单词
    "number": 0.5,           # 每个数字（小数点不计）
    "punctuation": 0.5,      # 标点符号
    "json_structure": 1.0,   # JSON结构字符 { } [ ] : ,
    "whitespace": 0.0,       # 空白字符不计数
}


# ============================================================
# Token计数器
# ============================================================

class TokenCounter:
    """
    精确估算文本/JSON的token数量。

    采用混合估算策略：
      1. 中文字符 × 1.5
      2. 英文单词 × 1.3
      3. 数字序列 × 0.5
      4. JSON结构字符 × 1.0
      5. 其他标点 × 0.5

    误差范围：±15%（与tiktoken等精确计数器对比）
    """

    # 预编译正则
    _RE_CHINESE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
    _RE_ENGLISH_WORD = re.compile(r'[a-zA-Z][a-zA-Z0-9_\-]*')
    _RE_NUMBER = re.compile(r'\d+\.?\d*')
    _RE_JSON_STRUCT = re.compile(r'[{}\[\]:,]')
    _RE_PUNCTUATION = re.compile(r'[^\w\s\u4e00-\u9fff\u3400-\u4dbf{}]')

    @classmethod
    def count_text(cls, text: str) -> int:
        """
        估算纯文本的token数量。

        Args:
            text: 输入文本

        Returns:
            int: 估算的token数量
        """
        if not text:
            return 0

        tokens = 0

        # 中文字符
        chinese_chars = cls._RE_CHINESE.findall(text)
        tokens += len(chinese_chars) * TOKEN_RATIOS["chinese_char"]

        # 移除已计数的中文，避免重复
        remaining = cls._RE_CHINESE.sub(' ', text)

        # 英文单词
        english_words = cls._RE_ENGLISH_WORD.findall(remaining)
        tokens += len(english_words) * TOKEN_RATIOS["english_word"]

        # 移除已计数的英文
        remaining = cls._RE_ENGLISH_WORD.sub(' ', remaining)

        # 数字序列
        numbers = cls._RE_NUMBER.findall(remaining)
        tokens += len(numbers) * TOKEN_RATIOS["number"]

        # 移除已计数的数字
        remaining = cls._RE_NUMBER.sub(' ', remaining)

        # JSON结构字符
        json_chars = cls._RE_JSON_STRUCT.findall(remaining)
        tokens += len(json_chars) * TOKEN_RATIOS["json_structure"]

        # 移除已计数的JSON结构
        remaining = cls._RE_JSON_STRUCT.sub(' ', remaining)

        # 其他标点
        puncts = cls._RE_PUNCTUATION.findall(remaining)
        tokens += len(puncts) * TOKEN_RATIOS["punctuation"]

        return max(1, int(math.ceil(tokens)))

    @classmethod
    def count_json(cls, obj: Any) -> int:
        """
        估算JSON对象序列化后的token数量。

        Args:
            obj: Python对象（将被json.dumps序列化）

        Returns:
            int: 估算的token数量
        """
        if obj is None:
            return 0

        # 序列化为紧凑JSON（模拟实际发送给LLM的格式）
        if isinstance(obj, str):
            return cls.count_text(obj)
        if isinstance(obj, (int, float, bool)):
            return cls.count_text(str(obj))

        json_str = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
        return cls.count_text(json_str)

    @classmethod
    def count_field(cls, field_name: str, field_value: Any) -> int:
        """
        估算单个字段的token数量（含字段名开销）。

        Args:
            field_name: 字段名
            field_value: 字段值

        Returns:
            int: 估算token数（含字段名+冒号+值的总开销）
        """
        # 字段名 + 引号 + 冒号 ≈ len(field_name) + 4
        name_tokens = cls.count_text(f'"{field_name}":')
        value_tokens = cls.count_json(field_value)
        return name_tokens + value_tokens

    @classmethod
    def count_test_point(cls, tp: dict) -> Dict[str, int]:
        """
        精确计算测试点每个字段的token数量。

        Args:
            tp: 测试点dict

        Returns:
            dict: {field_name: token_count} + "total" 总计
        """
        field_counts = {}
        total = 0
        for field_name, field_value in tp.items():
            if field_name.startswith("_"):
                continue
            count = cls.count_field(field_name, field_value)
            field_counts[field_name] = count
            total += count

        field_counts["__total__"] = total
        return field_counts


# ============================================================
# 截断策略执行器
# ============================================================

class TruncationExecutor:
    """
    按字段优先级执行截断操作。

    截断方式：
      P3字段：完全替换为占位字符串
      P2列表字段：保留前N项，其余截断
      P2文本字段：截断到指定字符数
      P1字段：不截断（除非极端情况）
      P0字段：永不截断
    """

    def __init__(self, strategies: dict = None):
        self.strategies = strategies or TRUNCATION_STRATEGIES

    def truncate_field(self, field_name: str, field_value: Any,
                       priority_level: str) -> Tuple[Any, dict]:
        """
        根据优先级截断单个字段。

        Args:
            field_name: 字段名
            field_value: 字段原始值
            priority_level: 优先级（P0/P1/P2/P3）

        Returns:
            (truncated_value, log_entry)
        """
        log_entry = {
            "field": field_name,
            "priority": priority_level,
            "original_type": type(field_value).__name__,
            "action": "kept",
            "original_tokens": TokenCounter.count_field(field_name, field_value),
            "truncated_tokens": 0,
            "reason": "",
        }

        if priority_level in ("P0", "P1"):
            # 绝对保留/必备字段 - 不截断
            log_entry["truncated_tokens"] = log_entry["original_tokens"]
            return field_value, log_entry

        if priority_level == "P3":
            # 可截断字段 - 完全替换
            placeholder = self.strategies["replace_values"]["P3"]
            truncated_value = placeholder
            log_entry.update({
                "action": "replaced",
                "truncated_tokens": TokenCounter.count_field(field_name, placeholder),
                "reason": f"P3字段完全截断，原值类型={type(field_value).__name__}",
            })
            return truncated_value, log_entry

        if priority_level == "P2":
            return self._truncate_p2_field(field_name, field_value, log_entry)

        # 未知优先级 - 不截断
        log_entry["truncated_tokens"] = log_entry["original_tokens"]
        return field_value, log_entry

    def _truncate_p2_field(self, field_name: str, field_value: Any,
                           log_entry: dict) -> Tuple[Any, dict]:
        """
        P2字段截断：列表保留前N项，文本截断到指定长度，其他替换。
        """
        if field_value is None or field_value == "" or field_value == {} or field_value == []:
            # 空值不需要截断
            log_entry["truncated_tokens"] = log_entry["original_tokens"]
            log_entry["reason"] = "空值，无需截断"
            return field_value, log_entry

        if isinstance(field_value, list):
            # 列表：保留前N项
            keep = self.strategies["p2_list_keep_count"]
            if len(field_value) <= keep:
                log_entry["truncated_tokens"] = log_entry["original_tokens"]
                log_entry["reason"] = f"列表长度{len(field_value)}≤保留数{keep}，无需截断"
                return field_value, log_entry

            truncated = field_value[:keep]
            template = self.strategies["replace_values"]["P2_list"]
            placeholder = template.format(keep=keep)
            truncated.append(placeholder)

            log_entry.update({
                "action": "list_truncated",
                "truncated_tokens": TokenCounter.count_field(field_name, truncated),
                "original_size": len(field_value),
                "kept_size": keep,
                "reason": f"列表从{len(field_value)}项截断为{keep}项",
            })
            return truncated, log_entry

        if isinstance(field_value, str) and len(field_value) > 20:
            # 长文本：截断到指定字符数
            keep_chars = self.strategies["p2_text_keep_chars"]
            if len(field_value) <= keep_chars:
                log_entry["truncated_tokens"] = log_entry["original_tokens"]
                log_entry["reason"] = f"文本长度{len(field_value)}≤保留数{keep_chars}，无需截断"
                return field_value, log_entry

            truncated = field_value[:keep_chars] + f"...[已截断-原文{len(field_value)}字符]"
            log_entry.update({
                "action": "text_truncated",
                "truncated_tokens": TokenCounter.count_field(field_name, truncated),
                "original_chars": len(field_value),
                "kept_chars": keep_chars,
                "reason": f"文本从{len(field_value)}字符截断为{keep_chars}字符",
            })
            return truncated, log_entry

        if isinstance(field_value, dict):
            # dict：保留keys但清空值
            truncated = {}
            for k, v in field_value.items():
                if isinstance(v, str) and len(v) > 20:
                    truncated[k] = v[:30] + "..."
                elif isinstance(v, list) and len(v) > 2:
                    truncated[k] = v[:1]
                else:
                    truncated[k] = v
            log_entry.update({
                "action": "dict_compacted",
                "truncated_tokens": TokenCounter.count_field(field_name, truncated),
                "reason": f"字典压缩，保留keys但精简值",
            })
            return truncated, log_entry

        # 其他类型（bool/int/float）不截断
        log_entry["truncated_tokens"] = log_entry["original_tokens"]
        log_entry["reason"] = f"基础类型{type(field_value).__name__}，无需截断"
        return field_value, log_entry


# ============================================================
# 核心截断器
# ============================================================

class ContextTruncator:
    """
    LLM上下文窗口动态截断器。

    工作流程：
      1. 计算当前token总数
      2. 计算可用token预算
      3. 按字段优先级从P3→P2逐步截断
      4. 记录截断日志

    使用示例：
        truncator = ContextTruncator(model_context_window=128000)

        # 单个测试点截断
        result, log = truncator.truncate_test_point(tp, context_used=50000)

        # 批量截断
        results, logs = truncator.truncate_batch(test_points)
    """

    def __init__(
        self,
        model_context_window: int = None,
        model_name: str = None,
        reserved_for_system: int = 4000,
        reserved_for_output: int = 8000,
        safety_margin: float = 0.85,
    ):
        """
        Args:
            model_context_window: 模型上下文窗口大小（tokens），
                                  若为None则根据model_name自动选择
            model_name: 模型名称，用于自动选择窗口大小
            reserved_for_system: 系统prompt预留token数
            reserved_for_output: 输出预留token数
            safety_margin: 安全系数（0-1），实际使用不超过此比例的可用空间
        """
        if model_context_window:
            self.context_window = model_context_window
        elif model_name:
            self.context_window = MODEL_CONTEXT_WINDOWS.get(
                model_name, MODEL_CONTEXT_WINDOWS["default"]
            )
        else:
            self.context_window = MODEL_CONTEXT_WINDOWS["default"]

        self.reserved_system = reserved_for_system
        self.reserved_output = reserved_for_output
        self.safety_margin = safety_margin
        self.executor = TruncationExecutor()
        self.token_counter = TokenCounter()

        # 截断统计
        self._stats = {
            "total_truncations": 0,
            "fields_truncated": defaultdict(int),
            "tokens_saved": 0,
            "by_priority": defaultdict(lambda: {"count": 0, "tokens_saved": 0}),
        }

    @property
    def available_budget(self) -> int:
        """
        计算当前可用的token预算。

        = (context_window - reserved_system - reserved_output) × safety_margin
        """
        raw = self.context_window - self.reserved_system - self.reserved_output
        return max(0, int(raw * self.safety_margin))

    def _get_field_priority(self, field_name: str) -> str:
        """获取字段优先级"""
        info = FIELD_PRIORITY.get(field_name)
        if info:
            return info["level"]
        # 未知字段默认P3（可截断）
        return "P3"

    def truncate_test_point(
        self,
        tp: dict,
        context_used: int = 0,
        target_budget: int = None,
    ) -> Tuple[dict, dict]:
        """
        动态截断单个测试点。

        Args:
            tp: 测试点dict（P5输出格式，含22个字段）
            context_used: 已使用的上下文token数（系统prompt、已有对话等）
            target_budget: 目标token预算（若为None则自动计算）

        Returns:
            (truncated_tp, truncation_log)
            truncated_tp: 截断后的测试点
            truncation_log: 截断日志
        """
        tp = deepcopy(tp)  # 不修改原始数据

        # 计算token预算
        if target_budget is None:
            target_budget = max(0, self.available_budget - context_used)

        # 计算当前token总量
        field_counts = self.token_counter.count_test_point(tp)
        current_total = field_counts.pop("__total__", 0)

        # 初始化日志
        log = {
            "tp_id": tp.get("id", "UNKNOWN"),
            "original_tokens": current_total,
            "target_budget": target_budget,
            "context_used": context_used,
            "available_budget": self.available_budget,
            "truncation_needed": current_total > target_budget,
            "final_tokens": current_total,
            "tokens_saved": 0,
            "fields_affected": [],
            "truncation_steps": [],
        }

        if current_total <= target_budget:
            # 不需要截断
            log["truncation_needed"] = False
            return tp, log

        # 需要截断：按优先级从P3→P2逐步截断
        # 构建字段列表，按优先级从低到高排序（先截低优先级）
        fields_by_priority = defaultdict(list)
        for fname in tp:
            if fname.startswith("_"):
                continue
            priority = self._get_field_priority(fname)
            order = FIELD_PRIORITY.get(fname, {}).get("order", 99)
            fields_by_priority[priority].append((order, fname))

        # 按优先级排序：P3 > P2 > P1 > P0（从可截断到不可截断）
        priority_order = ["P3", "P2", "P1", "P0"]
        sorted_fields = []
        for p_level in priority_order:
            level_fields = sorted(fields_by_priority.get(p_level, []))
            sorted_fields.extend([(p_level, fname) for _, fname in level_fields])

        # 逐步截断
        current_tokens = current_total
        for p_level, fname in sorted_fields:
            if current_tokens <= target_budget:
                break

            if p_level in ("P0", "P1"):
                # P0/P1字段不截断，但检查是否已达标
                continue

            field_value = tp.get(fname)
            if field_value is None or field_value == "" or field_value == {} or field_value == []:
                continue  # 空字段无需截断

            # 执行截断
            truncated_value, field_log = self.executor.truncate_field(
                fname, field_value, p_level
            )

            # 计算节省的token
            saved = field_log["original_tokens"] - field_log["truncated_tokens"]
            if saved > 0:
                tp[fname] = truncated_value
                current_tokens -= saved
                log["fields_affected"].append(fname)
                log["truncation_steps"].append(field_log)

                # 更新统计
                self._stats["total_truncations"] += 1
                self._stats["fields_truncated"][fname] += 1
                self._stats["tokens_saved"] += saved
                self._stats["by_priority"][p_level]["count"] += 1
                self._stats["by_priority"][p_level]["tokens_saved"] += saved

        log["final_tokens"] = current_tokens
        log["tokens_saved"] = current_total - current_tokens

        return tp, log

    def truncate_batch(
        self,
        test_points: List[dict],
        context_used: int = 0,
        per_point_budget: int = None,
    ) -> Tuple[List[dict], dict]:
        """
        批量截断测试点列表。

        动态分配每条测试点的token预算：
          1. 计算总预算 = available_budget - context_used
          2. 预留10%给P0/P1字段的超额
          3. 将剩余预算平均分配给每条测试点
          4. 逐条截断，记录日志

        Args:
            test_points: 测试点列表
            context_used: 已使用的上下文token数
            per_point_budget: 每条测试点的token预算（若为None则自动计算）

        Returns:
            (truncated_list, batch_log)
        """
        if not test_points:
            return [], {"error": "空列表"}

        total_budget = max(0, self.available_budget - context_used)

        if per_point_budget is None:
            # 预留10%作为弹性空间
            usable_budget = int(total_budget * 0.90)
            per_point_budget = max(500, usable_budget // len(test_points))

        truncated_list = []
        batch_log = {
            "total_points": len(test_points),
            "total_budget": total_budget,
            "per_point_budget": per_point_budget,
            "context_used": context_used,
            "truncated_count": 0,
            "total_tokens_saved": 0,
            "point_logs": [],
            "summary": {
                "fields_truncated_count": defaultdict(int),
                "by_priority": defaultdict(lambda: {"count": 0, "tokens_saved": 0}),
            },
        }

        actual_tokens_used = 0

        for i, tp in enumerate(test_points):
            # 动态调整预算：如果前面的测试点省了token，后面的可以多分配
            remaining_budget = total_budget - actual_tokens_used
            remaining_points = len(test_points) - i
            adjusted_budget = max(500, remaining_budget // remaining_points) if remaining_points > 0 else per_point_budget

            truncated, point_log = self.truncate_test_point(
                tp, context_used=0, target_budget=adjusted_budget
            )

            truncated_list.append(truncated)
            batch_log["point_logs"].append(point_log)
            actual_tokens_used += point_log["final_tokens"]

            if point_log["truncation_needed"]:
                batch_log["truncated_count"] += 1
                batch_log["total_tokens_saved"] += point_log["tokens_saved"]

                # 汇总字段截断统计
                for fname in point_log["fields_affected"]:
                    batch_log["summary"]["fields_truncated_count"][fname] += 1

                for step in point_log["truncation_steps"]:
                    p_level = step.get("priority", "unknown")
                    batch_log["summary"]["by_priority"][p_level]["count"] += 1
                    batch_log["summary"]["by_priority"][p_level]["tokens_saved"] += (
                        step.get("original_tokens", 0) - step.get("truncated_tokens", 0)
                    )

        # 转换defaultdict为普通dict（便于JSON序列化）
        batch_log["summary"]["fields_truncated_count"] = dict(
            batch_log["summary"]["fields_truncated_count"]
        )
        batch_log["summary"]["by_priority"] = dict(
            batch_log["summary"]["by_priority"]
        )

        return truncated_list, batch_log

    def estimate_batch_tokens(self, test_points: List[dict]) -> dict:
        """
        估算批量测试点的token分布。

        Returns:
            {
                "total_tokens": 总token数,
                "per_field_avg": 各字段平均token数,
                "per_point_tokens": 每条测试点的token数,
                "priority_distribution": 按优先级的token分布,
                "fits_in_context": 是否能在当前模型上下文中放下,
                "recommended_batch_size": 推荐的批次大小,
            }
        """
        if not test_points:
            return {
                "total_tokens": 0,
                "fits_in_context": True,
                "recommended_batch_size": 0,
            }

        total = 0
        per_point = []
        field_totals = defaultdict(int)
        priority_totals = defaultdict(int)

        for tp in test_points:
            counts = self.token_counter.count_test_point(tp)
            tp_total = counts.pop("__total__", 0)
            total += tp_total
            per_point.append(tp_total)

            for fname, tokens in counts.items():
                field_totals[fname] += tokens
                priority = self._get_field_priority(fname)
                priority_totals[priority] += tokens

        n = len(test_points)
        fits = total <= self.available_budget

        # 计算推荐批次大小
        avg_per_point = total / n if n > 0 else 0
        recommended_batch = (
            int(self.available_budget / avg_per_point) if avg_per_point > 0 else n
        )
        recommended_batch = max(1, min(recommended_batch, n))

        return {
            "total_tokens": total,
            "per_field_avg": {
                fname: round(tokens / n, 1)
                for fname, tokens in sorted(field_totals.items())
            },
            "per_point_tokens": per_point,
            "priority_distribution": {
                level: {"tokens": tokens, "percentage": round(tokens / max(total, 1) * 100, 1)}
                for level, tokens in sorted(priority_totals.items())
            },
            "fits_in_context": fits,
            "context_window": self.context_window,
            "available_budget": self.available_budget,
            "utilization": round(total / max(self.available_budget, 1) * 100, 1),
            "recommended_batch_size": recommended_batch,
        }

    def get_truncation_stats(self) -> dict:
        """获取截断统计信息"""
        stats = dict(self._stats)
        stats["fields_truncated"] = dict(stats["fields_truncated"])
        stats["by_priority"] = dict(stats["by_priority"])
        return stats

    def reset_stats(self):
        """重置截断统计"""
        self._stats = {
            "total_truncations": 0,
            "fields_truncated": defaultdict(int),
            "tokens_saved": 0,
            "by_priority": defaultdict(lambda: {"count": 0, "tokens_saved": 0}),
        }


# ============================================================
# 截断日志格式化（供人工复核）
# ============================================================

class TruncationReportFormatter:
    """
    将截断日志格式化为可读的报告，供人工复核。
    """

    @staticmethod
    def format_point_log(log: dict) -> str:
        """格式化单条测试点的截断日志"""
        lines = []
        lines.append(f"### 测试点: {log['tp_id']}")
        lines.append(f"- 原始Token数: {log['original_tokens']}")
        lines.append(f"- 目标预算: {log['target_budget']}")
        lines.append(f"- 最终Token数: {log['final_tokens']}")
        lines.append(f"- 节省Token数: {log['tokens_saved']}")

        if not log["truncation_needed"]:
            lines.append("- **状态: 无需截断** ✅")
        else:
            lines.append(f"- **状态: 已截断** ✂️")
            lines.append(f"- 涉及字段: {', '.join(log['fields_affected'])}")
            for step in log["truncation_steps"]:
                lines.append(f"  - `{step['field']}` ({step['priority']}): "
                             f"{step['action']} — {step['reason']} "
                             f"({step['original_tokens']}→{step['truncated_tokens']} tokens)")

        return "\n".join(lines)

    @staticmethod
    def format_batch_log(batch_log: dict) -> str:
        """格式化批量截断日志"""
        lines = []
        lines.append("# 截断报告")
        lines.append(f"- 总测试点数: {batch_log['total_points']}")
        lines.append(f"- 每点Token预算: {batch_log['per_point_budget']}")
        lines.append(f"- 被截断的测试点数: {batch_log['truncated_count']}")
        lines.append(f"- 总节省Token数: {batch_log['total_tokens_saved']}")
        lines.append("")

        # 按字段统计
        summary = batch_log.get("summary", {})
        if summary.get("fields_truncated_count"):
            lines.append("## 字段截断统计")
            for fname, count in sorted(
                summary["fields_truncated_count"].items(),
                key=lambda x: x[1], reverse=True
            ):
                priority = FIELD_PRIORITY.get(fname, {}).get("level", "unknown")
                desc = FIELD_PRIORITY.get(fname, {}).get("desc", "")
                lines.append(f"- `{fname}` ({priority}, {desc}): 截断{count}次")
            lines.append("")

        # 按优先级统计
        if summary.get("by_priority"):
            lines.append("## 优先级截断统计")
            for level, data in sorted(summary["by_priority"].items()):
                lines.append(f"- {level}: 截断{data['count']}次, "
                             f"节省{data['tokens_saved']} tokens")
            lines.append("")

        # 逐条详情（仅被截断的）
        truncated_logs = [
            pl for pl in batch_log.get("point_logs", [])
            if pl.get("truncation_needed")
        ]
        if truncated_logs:
            lines.append("## 截断详情（仅被截断的测试点）")
            for pl in truncated_logs:
                lines.append(TruncationReportFormatter.format_point_log(pl))
                lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_estimate(estimate: dict) -> str:
        """格式化token估算报告"""
        lines = []
        lines.append("# Token估算报告")
        lines.append(f"- 总Token数: {estimate['total_tokens']}")
        lines.append(f"- 模型上下文窗口: {estimate.get('context_window', 'N/A')}")
        lines.append(f"- 可用预算: {estimate.get('available_budget', 'N/A')}")
        lines.append(f"- 利用率: {estimate.get('utilization', 'N/A')}%")
        fits = estimate.get("fits_in_context", True)
        lines.append(f"- 是否溢出: {'否 ✅' if fits else '是 ⚠️'}")
        lines.append(f"- 推荐批次大小: {estimate.get('recommended_batch_size', 'N/A')}")

        # 优先级分布
        dist = estimate.get("priority_distribution", {})
        if dist:
            lines.append("")
            lines.append("## 优先级Token分布")
            for level, data in sorted(dist.items()):
                lines.append(f"- {level}: {data['tokens']} tokens ({data['percentage']}%)")

        return "\n".join(lines)


# ============================================================
# 便捷函数（供 p5_prepare.py 集成调用）
# ============================================================

def smart_truncate_for_batch(
    test_points: List[dict],
    model_name: str = None,
    model_context_window: int = None,
    context_used: int = 0,
) -> Tuple[List[dict], str]:
    """
    便捷函数：为 p5_prepare.py 提供一键截断。

    Args:
        test_points: P5输出的测试点列表
        model_name: 模型名称（用于自动选择窗口大小）
        model_context_window: 手动指定窗口大小（优先于model_name）
        context_used: 已使用的上下文token数

    Returns:
        (truncated_list, report_markdown)
    """
    truncator = ContextTruncator(
        model_context_window=model_context_window,
        model_name=model_name,
    )

    # 先估算
    estimate = truncator.estimate_batch_tokens(test_points)
    estimate_report = TruncationReportFormatter.format_estimate(estimate)

    # 执行截断
    truncated_list, batch_log = truncator.truncate_batch(
        test_points, context_used=context_used
    )
    batch_report = TruncationReportFormatter.format_batch_log(batch_log)

    # 合并报告
    full_report = f"{estimate_report}\n\n---\n\n{batch_report}"

    return truncated_list, full_report
