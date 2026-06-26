#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
Skill Trigger V2 - Core Module

统一阈值 + 优先级仲裁的技能触发系统。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "2.0.0"

# 统一阈值配置
UNIFIED_THRESHOLD = 0.5  # 50% 覆盖率

# 等级优先级权重 (用于仲裁)
LEVEL_PRIORITY_WEIGHT = {
    "L0": 1.2,
    "L1": 1.1,
    "L2": 1.0,
    "L3": 0.9,
}

# 路径配置
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent.parent.parent  # ~/.openclaw/workspace
SKILL_INDEX_PATH = WORKSPACE_DIR / ".lib" / "skill_index.json"
CONFIG_PATH = WORKSPACE_DIR / ".lib" / "skill_trigger_config.json"
DISPATCH_STATE_PATH = WORKSPACE_DIR / ".lib" / "skill_trigger_dispatch_state.json"


@dataclass
class FitResult:
    """技能触发判定结果"""
    matched: bool
    skill_id: Optional[str] = None
    confidence: float = 0.0
    reason: str = ""
    level: Optional[str] = None


@dataclass
class DispatchPlan:
    """技能自动执行调度计划"""
    should_dispatch: bool
    dispatch_id: Optional[str] = None
    skill_id: Optional[str] = None
    blocked_reason: str = ""
    dedup_hit: bool = False
    debounce_hit: bool = False
    circuit_open: bool = False
    source: str = "fit_gate"


def check_dependencies() -> Dict[str, Any]:
    """
    检查依赖技能状态
    
    Returns:
        {
            "skill-quick-index": {"installed": bool, "version": str, "compatible": bool},
            "semantic-router": {"installed": bool, "version": str, "compatible": bool}
        }
    """
    deps = {}
    
    # 检查 skill-quick-index
    try:
        if SKILL_INDEX_PATH.exists():
            with open(SKILL_INDEX_PATH, "r", encoding="utf-8") as f:
                index = json.load(f)
            version = index.get("version", "0.0.0")
            deps["skill-quick-index"] = {
                "installed": True,
                "version": version,
                "compatible": _compare_versions(version, "1.0.0") >= 0
            }
        else:
            deps["skill-quick-index"] = {"installed": False, "version": None, "compatible": False}
    except Exception as e:
        deps["skill-quick-index"] = {"installed": False, "version": None, "compatible": False, "error": str(e)}
    
    # 检查 semantic-router (通过 pools.json 存在性判断)
    try:
        pools_path = WORKSPACE_DIR / ".lib" / "pools.json"
        if pools_path.exists():
            with open(pools_path, "r", encoding="utf-8") as f:
                pools = json.load(f)
            version = pools.get("version", "0.0.0")
            deps["semantic-router"] = {
                "installed": True,
                "version": version,
                "compatible": _compare_versions(version, "2.0.0") >= 0
            }
        else:
            deps["semantic-router"] = {"installed": False, "version": None, "compatible": False}
    except Exception as e:
        deps["semantic-router"] = {"installed": False, "version": None, "compatible": False, "error": str(e)}
    
    return deps


def _compare_versions(v1: str, v2: str) -> int:
    """比较版本号，返回 -1/0/1"""
    def parse(v):
        try:
            return tuple(int(x) for x in v.split(".")[:3])
        except:
            return (0, 0, 0)
    
    t1, t2 = parse(v1), parse(v2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    return 0


def _normalize(text: str) -> str:
    """文本归一化"""
    return text.lower().strip()


def _tokenize_trigger_phrase(phrase: str) -> List[str]:
    """将触发短语拆成可组合命中的词元"""
    p = _normalize(phrase)
    if not p:
        return []
    
    parts = [x for x in re.split(r"[\s,，、/|:：;；]+", p) if x]
    if len(parts) >= 2:
        return parts
    
    mixed = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", p)
    if len(mixed) >= 2:
        return [x for x in mixed if x]
    
    if re.fullmatch(r"[\u4e00-\u9fff]+", p):
        n = len(p)
        if n == 4:
            return [p[:2], p[2:]]
        if n == 6:
            return [p[:3], p[3:]]
    
    return []


def _calculate_coverage(user_input: str, groups: List[List[str]]) -> float:
    """计算分组覆盖率：命中组数 / 总组数"""
    if not groups:
        return 0.0
    text = _normalize(user_input)
    passed = 0
    for g in groups:
        if not isinstance(g, list) or not g:
            continue
        if any(_normalize(tok) in text for tok in g if tok):
            passed += 1
    return passed / len(groups) if groups else 0.0


def _extract_signature_words(skill_detail: Dict[str, Any]) -> List[str]:
    """提取技能的独占词"""
    sig = skill_detail.get("signature_words", [])
    if sig:
        return [str(s).lower() for s in sig]
    
    groups = skill_detail.get("trigger_groups_all", [])
    if groups and len(groups) > 0:
        return [str(groups[0][0]).lower()] if groups[0] else []
    return []


def _negative_filter(user_input: str, negative_keywords: List[str]) -> bool:
    """负向关键词过滤，返回 True 表示被过滤"""
    if not negative_keywords:
        return False
    
    text = _normalize(user_input)
    for nkw in negative_keywords:
        if not nkw:
            continue
        nkw_norm = _normalize(nkw)
        if nkw_norm in text:
            return True
    return False


def _load_skill_index() -> Dict[str, Any]:
    """加载 skill_index.json"""
    if not SKILL_INDEX_PATH.exists():
        return {}
    try:
        return json.loads(SKILL_INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def fit_gate(user_input: str, custom_threshold: Optional[float] = None) -> FitResult:
    """
    技能触发判定器 - 统一阈值 + 优先级仲裁
    
    Args:
        user_input: 用户输入文本
        custom_threshold: 自定义阈值（覆盖默认50%）
    
    Returns:
        FitResult: 匹配结果
    """
    threshold = custom_threshold or UNIFIED_THRESHOLD
    
    # 检查依赖
    deps = check_dependencies()
    if not all(d.get("installed", False) for d in deps.values()):
        missing = [k for k, v in deps.items() if not v.get("installed")]
        return FitResult(
            matched=False,
            reason=f"依赖缺失: {', '.join(missing)}"
        )
    
    # 加载技能索引
    skill_index = _load_skill_index()
    skills = skill_index.get("skill_details", {})
    
    if not skills:
        return FitResult(matched=False, reason="技能索引为空")
    
    # 计算所有技能的覆盖率，进入候选池
    candidates = []
    
    for skill_id, detail in skills.items():
        level = str(detail.get("level", "L3")).upper()
        if level not in ("L0", "L1", "L2", "L3"):
            level = "L3"
        
        # 获取触发词组
        trigger_groups_all = detail.get("trigger_groups_all", []) or []
        
        # 兼容旧格式：从 triggers 推导
        if not trigger_groups_all:
            triggers = detail.get("triggers", []) or []
            inferred = []
            for t in triggers:
                toks = _tokenize_trigger_phrase(str(t))
                if len(toks) >= 2:
                    inferred.append(toks)
            trigger_groups_all = inferred
        
        if not trigger_groups_all:
            continue
        
        # 负向过滤
        negative = detail.get("negative_keywords", []) or detail.get("negative_patterns", [])
        if _negative_filter(user_input, negative):
            continue
        
        # 计算覆盖率
        coverage = _calculate_coverage(user_input, trigger_groups_all)
        
        # 统一阈值过滤
        if coverage < threshold:
            continue
        
        # 检查独占词
        signatures = _extract_signature_words(detail)
        sig_hit = any(sig in _normalize(user_input) for sig in signatures)
        
        candidates.append({
            "skill_id": skill_id,
            "level": level,
            "name": detail.get("name"),
            "coverage": coverage,
            "signature_hit": sig_hit,
            "signatures": signatures,
            "priority_weight": LEVEL_PRIORITY_WEIGHT.get(level, 1.0),
            "quick_ref": detail.get("quick_ref"),
        })
    
    if not candidates:
        return FitResult(matched=False, reason=f"无技能达到{threshold:.0%}覆盖率")
    
    # 优先级仲裁
    
    # P0: 独占词直接胜出（若唯一）
    sig_candidates = [c for c in candidates if c["signature_hit"]]
    if len(sig_candidates) == 1:
        winner = sig_candidates[0]
        return FitResult(
            matched=True,
            skill_id=winner["skill_id"],
            confidence=winner["coverage"] * winner["priority_weight"],
            reason=f"独占词匹配 ({', '.join(winner['signatures'][:2])})",
            level=winner["level"]
        )
    elif len(sig_candidates) > 1:
        candidates = sig_candidates  # 多个独占词，继续仲裁
    
    # P1-P3: 加权分数
    for c in candidates:
        c["weighted_score"] = c["coverage"] * c["priority_weight"]
        if c["signature_hit"]:
            c["weighted_score"] += 0.3  # 独占词加成
    
    candidates.sort(key=lambda x: x["weighted_score"], reverse=True)
    best = candidates[0]
    
    # P2: 置信度差距
    confidence_gap = 0.0
    if len(candidates) >= 2:
        confidence_gap = best["weighted_score"] - candidates[1]["weighted_score"]
    
    if confidence_gap >= 0.2 or len(candidates) == 1:
        reason = f"{best['level']}优先级仲裁胜出 (gap={confidence_gap:.2f})"
    else:
        reason = f"{best['level']}平局决胜 (权重{best['priority_weight']})"
    
    return FitResult(
        matched=True,
        skill_id=best["skill_id"],
        confidence=best["weighted_score"],
        reason=reason,
        level=best["level"]
    )


def generate_declaration(result: FitResult) -> str:
    """生成技能触发声明（供代理回复使用）"""
    if not result.matched or not result.skill_id:
        return ""
    
    dispatch_id = hashlib.sha1(
        f"{result.skill_id}:{result.reason}:{time.time()}".encode()
    ).hexdigest()[:12]
    # dispatch_id logged for tracing only, not injected into LLM context
    # (avoids dynamic field breaking LLM prefix cache on every turn)
    
    return (
        f"【Skill Trigger】本轮命中技能：{result.skill_id} 🔷 Powered by halfmoon82 🔷\n"
        f"请优先按该技能流程执行当前任务；若技能不可用或无关，直接忽略并正常回复即可。"
    )


class SkillTrigger:
    """
    技能触发器类接口
    
    Example:
        trigger = SkillTrigger()
        result = trigger.match("帮我安装安全技能")
        if result.matched:
            print(trigger.get_declaration(result))
    """
    
    def __init__(self, threshold: Optional[float] = None):
        self.threshold = threshold or UNIFIED_THRESHOLD
        self._deps = check_dependencies()
    
    def match(self, user_input: str) -> FitResult:
        """匹配用户输入到技能"""
        return fit_gate(user_input, self.threshold)
    
    def get_declaration(self, result: FitResult) -> str:
        """获取声明文本"""
        return generate_declaration(result)
    
    def check_deps(self) -> Dict[str, Any]:
        """检查依赖状态"""
        self._deps = check_dependencies()
        return self._deps
    
    def is_ready(self) -> bool:
        """检查是否就绪（所有依赖满足）"""
        return all(d.get("compatible", False) for d in self._deps.values())


# 向后兼容：保留原函数名
match_skill = fit_gate
