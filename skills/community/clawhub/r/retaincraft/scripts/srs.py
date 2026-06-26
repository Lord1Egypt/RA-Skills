#!/usr/bin/env python3
# =============================================================================
# RetainCraft v1.4.0 — 间隔重复学习系统
#
# 文件用途：主程序，包含 FSRS-5/SM-2 算法、24 个 CLI 命令、数据持久化
# 测试覆盖：170 个测试（test_srs.py）
# 外部依赖：零（仅 Python 标准库）
#
# === 文件结构概览 ===
# [1] 文件头 + imports + 常量          (L1-150)
# [2] 输入验证 sanitize                (L56-108)
# [3] 原子写入 _atomic_*               (L154-204)
# [4] 学习数据读写                     (L207-401)
# [5] 会话检查 + 倦怠检测              (L404-558)
# [6] 用户画像 profile                 (L561-705)
# [7] 等级计算 calc_level              (L717-798)
# [8] 配置/概念/进度管理               (L801-960)
# [9] FSRS-5 算法核心                  (L967-1286)
# [10] SM-2 + calc_next_review         (L1046-1136)
# [11] 显示辅助函数                    (L1289-1365)
# [12] 核心命令: init/add/rate/review  (L1370-1576)
# [13] 数据分析命令: due/today/streak/analyze/optimize-params (L1579-1969)
# [14] 状态/配置命令                   (L1972-2111)
# [15] 提醒系统 (openclaw cron)        (L2114-2504)
# [16] 记录/画像命令                   (L2507-2684)
# [17] main() 入口 + dispatch          (L2687-2769)
# =============================================================================

"""
SM-2 Spaced Repetition System for RetainCraft skill.

Usage:
    python3 srs.py init <topic>              # Create a new topic
    python3 srs.py add <topic> <concept>     # Add a concept to a topic
    python3 srs.py review <topic>            # Start a review session
    python3 srs.py rate <topic> <concept> <rating>  # Rate a concept (non-interactive)
    python3 srs.py due                       # Show all due reviews
    python3 srs.py status                    # Show overall status
    python3 srs.py status <topic>            # Show topic status
    python3 srs.py record-test <topic> <total> <correct>  # Record a test result
    python3 srs.py test-history [topic]      # Show test history
    python3 srs.py record-simulation <topic> <scenario> <score> [--rounds N]  # Record a simulation result
    python3 srs.py simulation-history [topic]  # Show simulation history
    python3 srs.py profile                   # Show user profile
    python3 srs.py profile --update          # Update profile for all topics
    python3 srs.py profile --compare <job>   # Compare profile with job requirements
    python3 srs.py check-session [topic]      # Check for unrecorded tests
    python3 srs.py check-burnout <topic>      # Analyze burnout risk
    python3 srs.py config                     # Show config
    python3 srs.py config set <key> <value>  # Set config value
    python3 srs.py setup-reminder             # Setup learning reminder + weekly report cron
    python3 srs.py reminder                   # Generate today's learning plan
    python3 srs.py weekly-report              # Generate weekly report data
    python3 srs.py check-reminder             # Check reminder status
    python3 srs.py switch-channel             # Switch reminder notification channel
    python3 srs.py today                     # Today's learning plan with overdue analysis
    python3 srs.py streak                    # Show consecutive learning days
    python3 srs.py analyze                   # Learning trends and weak concepts

    # v1.3.0 new
    python3 srs.py config set algorithm fsrs # Switch to FSRS-5 algorithm
    python3 srs.py optimize-params          # Personalize FSRS-5 weights from review history

Storage: ~/learn/
"""

from __future__ import annotations

import copy
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# 防止路径遍历攻击：sanitize_topic/concept 用正则白名单过滤用户输入
# 正则 ^[a-zA-Z0-9_\-\u4e00-\u9fff]+$ 只允许字母/数字/下划线/连字符/中文

class SanitizeError(ValueError):
    """Raised when a topic or concept name contains invalid characters."""
    pass


# Pattern: letters, digits, hyphens, underscores, and CJK characters only
_SAFE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\u4e00-\u9fff]+$')


def sanitize_topic(topic: str) -> str:
    """
    Validate and sanitize a topic name to prevent path traversal attacks.

    Args:
        topic: Raw topic name from user input

    Returns:
        The validated topic name (unchanged if valid)

    Raises:
        SanitizeError: If the topic name contains invalid characters
    """
    if not topic or not _SAFE_NAME_PATTERN.match(topic):
        raise SanitizeError(
            f"Invalid topic name: '{topic}'. "
            "Only letters, digits, hyphens, underscores, and CJK characters are allowed."
        )
    return topic


def sanitize_concept(concept_name: str) -> str:
    """
    Validate and sanitize a concept name to prevent path traversal attacks.

    Args:
        concept_name: Raw concept name from user input

    Returns:
        The validated concept name (unchanged if valid)

    Raises:
        SanitizeError: If the concept name is empty, too long, or contains invalid characters
    """
    if not concept_name or not _SAFE_NAME_PATTERN.match(concept_name):
        raise SanitizeError(
            f"Invalid concept name: '{concept_name}'. "
            "Only letters, digits, hyphens, underscores, and CJK characters are allowed."
        )
    if len(concept_name) > 200:
        raise SanitizeError(
            f"Concept name too long ({len(concept_name)} chars). Maximum length is 200 characters."
        )
    return concept_name


LEARN_DIR = Path.home() / "learn"
TOPICS_DIR = LEARN_DIR / "topics"
CONFIG_FILE = LEARN_DIR / "config.json"
TEST_HISTORY_FILE = LEARN_DIR / "test_history.json"
SIMULATION_HISTORY_FILE = LEARN_DIR / "simulation_history.json"
PROFILE_FILE = LEARN_DIR / "profile.json"
LEARNING_LOG_FILE = LEARN_DIR / "learning_log.json"

# For cron detection (used by setup-reminder)
SCRIPTS_DIR = Path(__file__).parent

# SM-2 algorithm constant: second review interval (original SM-2 specification)
SM2_SECOND_INTERVAL = 6

DEFAULT_CONFIG = {
    "learning_depth": "standard",  # Reserved for AI protocol, not read by srs.py
    "learner_type": "practical",   # Reserved for AI protocol, not read by srs.py
    "daily_review_limit": 20,
    "session_duration": 60,        # Reserved for AI protocol, not read by srs.py
    "burnout_threshold": 3,
    "mastery_threshold": 0.8,
    "algorithm": "fsrs",  # v1.3.0: FSRS-5 as default (was SM-2)
    "fsrs_weights": None,  # None = use default 19 weights; list = personalized
    "level_thresholds": {
        "L2": 0.2,
        "L3": 0.4,
        "L4": 0.7,
        "L5": 0.9
    }
}

DEFAULT_CONCEPT = {
    "added": None,
    "interval_days": 1,
    "next_review": None,
    "ease_factor": 2.5,
    "reviews": 0,
    "correct_count": 0,
    "total_count": 0,
    "mastery": "unseen",
}


# 使用 tempfile + os.replace 防止写入过程中断导致数据损坏
# 所有文件写入都经过这两个函数，确保数据一致性

def _atomic_json_save(filepath: Path, data: dict) -> None:
    """
    Atomically write JSON data to a file using temp file + os.replace.

    This prevents data corruption if the process is interrupted during write.

    Args:
        filepath: Target file path
        data: Data to serialize as JSON
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=filepath.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _atomic_text_save(filepath: Path, content: str) -> None:
    """
    Atomically write text content to a file using temp file + os.replace.

    This prevents data corruption if the process is interrupted during write.

    Args:
        filepath: Target file path
        content: Text content to write

    Raises:
        OSError: If the file cannot be written
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=filepath.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(tmp_path, filepath)
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# learning_log.json — 所有学习活动记录（rate/test/simulation/review）
# test_history.json — 模块测试成绩（按 topic 分组）
# simulation_history.json — 模拟场景成绩（按 topic 分组）
# 数据存储位置：~/learn/

def load_learning_log() -> list[dict[str, Any]]:
    """
    Load learning log from file.

    Returns:
        List of learning log entries
    """
    if LEARNING_LOG_FILE.exists():
        try:
            with open(LEARNING_LOG_FILE, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def append_learning_log(action: str, topic: str, details: dict[str, Any]) -> None:
    """
    Append an entry to the learning log.

    Design intent: Keeps learning_log.json bounded to prevent unbounded growth.
    Retains the most recent 5000 entries. Older entries are pruned on append.

    Args:
        action: Action type (e.g., "rate", "record-test")
        topic: Topic name
        details: Additional details about the action
    """
    log = load_learning_log()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "topic": topic,
        **details
    }
    log.append(entry)

    # Prune to most recent 5000 entries to prevent unbounded growth
    MAX_LOG_ENTRIES = 5000
    if len(log) > MAX_LOG_ENTRIES:
        log = log[-MAX_LOG_ENTRIES:]

    LEARNING_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _atomic_json_save(LEARNING_LOG_FILE, log)


def get_last_learning_time() -> datetime | None:
    """
    Get the timestamp of the last learning activity.

    Returns:
        datetime of last activity, or None if no activity found
    """
    log = load_learning_log()
    if not log:
        return None
    try:
        last_entry = log[-1]
        return datetime.fromisoformat(last_entry["timestamp"])
    except (ValueError, KeyError):
        return None


def load_test_history() -> dict[str, list[dict[str, Any]]]:
    """
    Load test history from file.
    
    Returns:
        Dictionary mapping topics to test history lists
    """
    if TEST_HISTORY_FILE.exists():
        try:
            with open(TEST_HISTORY_FILE, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_test_history(history: dict[str, list[dict[str, Any]]]) -> None:
    """
    Save test history to file using atomic write.
    
    Args:
        history: Dictionary mapping topics to test history lists
    """
    ensure_dirs()
    _atomic_json_save(TEST_HISTORY_FILE, history)


def record_test(topic: str, total: int, correct: int) -> dict[str, Any]:
    """
    Record a test result for a topic.
    
    Args:
        topic: Topic name
        total: Total number of questions
        correct: Number of correct answers
    
    Returns:
        Recorded test result dictionary
    
    Raises:
        ValueError: If input parameters are invalid
    """
    # Validate input
    topic = sanitize_topic(topic)
    if total <= 0:
        raise ValueError(f"Total questions must be positive, got: {total}")
    if correct < 0:
        raise ValueError(f"Correct answers cannot be negative, got: {correct}")
    if correct > total:
        raise ValueError(f"Correct answers ({correct}) cannot exceed total ({total})")
    
    history = load_test_history()
    if topic not in history:
        history[topic] = []
    
    test_result = {
        "timestamp": datetime.now().isoformat(),
        "accuracy": correct / total,
        "total": total,
        "correct": correct
    }
    history[topic].append(test_result)
    save_test_history(history)
    # Log the test action
    append_learning_log("record-test", topic, {
        "total": total,
        "correct": correct,
        "accuracy": correct / total
    })
    return test_result


def load_simulation_history() -> dict[str, list[dict[str, Any]]]:
    """
    Load simulation history from file.
    
    Returns:
        Dictionary mapping topics to simulation history lists
    """
    if SIMULATION_HISTORY_FILE.exists():
        try:
            with open(SIMULATION_HISTORY_FILE, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_simulation_history(history: dict[str, list[dict[str, Any]]]) -> None:
    """
    Save simulation history to file using atomic write.
    
    Args:
        history: Dictionary mapping topics to simulation history lists
    """
    ensure_dirs()
    _atomic_json_save(SIMULATION_HISTORY_FILE, history)


def record_simulation(topic: str, scenario: str, score: int, rounds: int = 3) -> dict[str, Any]:
    """
    Record a simulation result for a topic.
    
    Args:
        topic: Topic name
        scenario: Scenario name
        score: Simulation score (0-100)
        rounds: Number of rounds (default: 3)
    
    Returns:
        Recorded simulation result dictionary
    
    Raises:
        ValueError: If input parameters are invalid
    """
    # Validate input
    topic = sanitize_topic(topic)
    if score < 0 or score > 100:
        raise ValueError(f"Simulation score must be between 0-100, got: {score}")
    if rounds < 1:
        raise ValueError(f"Simulation rounds must be positive, got: {rounds}")
    
    history = load_simulation_history()
    if topic not in history:
        history[topic] = []
    
    simulation_result = {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario,
        "score": score,
        "rounds": rounds
    }
    history[topic].append(simulation_result)
    save_simulation_history(history)
    # Log the simulation action
    append_learning_log("record-simulation", topic, {
        "scenario": scenario,
        "score": score,
        "rounds": rounds
    })
    return simulation_result


# check_session: 检测未记录的模块测试（防止 AI 遗忘导致等级不更新）
# check_burnout: 分析学习倦怠风险（基于准确率趋势 + 连续低分 + 学习频率）

def check_session(topic: str | None = None, stale_minutes: int = 120) -> dict[str, Any]:
    """
    Check if there are unrecorded module tests in the current session.

    Compares the timestamp of the last record-test call against the current
    time. If the gap exceeds *stale_minutes*, the session is flagged so
    the AI can remind the user (or the user can invoke this manually).

    Args:
        topic: Topic name to check (None = all topics)
        stale_minutes: Minutes of silence after which a record is considered stale (default 120)

    Returns:
        Dictionary with check result details
    """
    history = load_test_history()
    topics_to_check = [topic] if topic else list(history.keys())

    if not topics_to_check:
        return {
            "status": "no_history",
            "message": "No test history found. Start learning first!",
        }

    now = datetime.now()
    findings: list[dict[str, Any]] = []

    for t in topics_to_check:
        tests = history.get(t, [])
        if not tests:
            continue
        latest = tests[-1]
        ts = datetime.fromisoformat(latest["timestamp"])
        gap_minutes = (now - ts).total_seconds() / 60

        finding: dict[str, Any] = {
            "topic": t,
            "last_record": latest["timestamp"],
            "gap_minutes": round(gap_minutes, 1),
            "last_accuracy": latest["accuracy"],
            "stale": gap_minutes > stale_minutes,
        }
        findings.append(finding)

    if not findings:
        return {
            "status": "no_history",
            "message": "No test history found.",
        }

    stale_topics = [f for f in findings if f["stale"]]
    status = "stale" if stale_topics else "fresh"

    return {
        "status": status,
        "stale_minutes_threshold": stale_minutes,
        "findings": findings,
        "stale_count": len(stale_topics),
    }


def _calc_accuracy_trend(recent: list[dict[str, Any]]) -> str:
    """Calculate accuracy trend by comparing first-half vs second-half averages."""
    mid = len(recent) // 2
    if mid == 0:
        return "stable"
    first_half_avg = sum(t["accuracy"] for t in recent[:mid]) / mid
    second_half_avg = sum(t["accuracy"] for t in recent[mid:]) / (len(recent) - mid)
    diff = second_half_avg - first_half_avg
    if diff < -0.1:
        return "declining"
    elif diff > 0.1:
        return "improving"
    return "stable"


def _count_consecutive_low(recent: list[dict[str, Any]], threshold: float = 0.5) -> int:
    """Count consecutive tests below threshold from the end."""
    count = 0
    for t in reversed(recent):
        if t["accuracy"] < threshold:
            count += 1
        else:
            break
    return count


def _assess_burnout_risk(consecutive_low: int, trend: str, avg_accuracy: float) -> str:
    """Determine burnout risk level from metrics."""
    if consecutive_low >= 3 or (trend == "declining" and avg_accuracy < 0.4):
        return "high"
    elif consecutive_low >= 2 or (trend == "declining" and avg_accuracy < 0.6):
        return "medium"
    return "low"


def _get_burnout_suggestions(risk: str) -> list[str]:
    """Generate suggestions based on burnout risk level."""
    if risk == "high":
        return [
            "休息至少 30 分钟后再继续学习。",
            "复习已掌握的概念以重建信心。",
            "考虑暂时切换到其他主题。",
        ]
    elif risk == "medium":
        return [
            "缩短下次学习时长。",
            "专注复习薄弱点，不要学新内容。",
            "如果感到疲劳，休息 10-15 分钟。",
        ]
    return []


def check_burnout(topic: str, window: int = 5) -> dict[str, Any]:
    """
    Analyze burnout risk for a topic based on recent test trends.

    Design intent: Delegates trend/risk/suggestion calculation to helpers
    so each concern is isolated and testable.

    Args:
        topic: Topic name to analyze
        window: Number of recent tests to consider (default 5)

    Returns:
        Dictionary with burnout analysis
    """
    topic = sanitize_topic(topic)
    history = load_test_history().get(topic, [])

    if len(history) == 0:
        return {
            "status": "no_data",
            "topic": topic,
            "message": "No test history found for this topic.",
        }

    recent = history[-window:]
    trend = _calc_accuracy_trend(recent)
    consecutive_low = _count_consecutive_low(recent)
    avg_accuracy = sum(t["accuracy"] for t in recent) / len(recent)
    risk = _assess_burnout_risk(consecutive_low, trend, avg_accuracy)
    suggestions = _get_burnout_suggestions(risk)

    return {
        "status": "ok",
        "topic": topic,
        "window": window,
        "recent_tests": len(recent),
        "avg_accuracy": round(avg_accuracy, 3),
        "trend": trend,
        "consecutive_below_50": consecutive_low,
        "risk": risk,
        "suggestions": suggestions,
    }


# profile.json — 用户学习画像（各 topic 的等级、掌握度、测试成绩）
# 支持：查看画像、更新画像、与职位要求对比

def load_profile() -> dict[str, Any]:
    """
    Load user profile from file.
    
    Returns:
        User profile dictionary
    """
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "goal": "",
        "started": today(),
        "total_hours": 0,
        "topics": {},
        "strengths": [],
        "weaknesses": [],
        "last_updated": datetime.now().isoformat()
    }


def save_profile(profile: dict[str, Any]) -> None:
    """
    Save user profile to file using atomic write.
    
    Args:
        profile: User profile dictionary to save
    """
    ensure_dirs()
    profile["last_updated"] = datetime.now().isoformat()
    _atomic_json_save(PROFILE_FILE, profile)


def update_profile(topic: str) -> dict[str, Any]:
    """
    Update user profile with topic data.
    
    Args:
        topic: Topic name to update
    
    Returns:
        Updated user profile dictionary
    """
    topic = sanitize_topic(topic)
    profile = load_profile()
    concepts = load_concepts(topic)
    test_history = load_test_history().get(topic, [])

    # Calculate topic stats
    mastered, total, _ = calc_mastery_overview(concepts)
    level_code, _, _ = calc_level_by_accuracy(topic, concepts_fallback=concepts)

    # Calculate test average
    test_avg = 0
    if test_history:
        test_avg = sum(t["accuracy"] for t in test_history) / len(test_history) * 100

    # Calculate total hours (estimate from test count)
    # Rough estimate: each test takes ~15 minutes
    hours = len(test_history) * 0.25

    # Update topic data
    profile["topics"][topic] = {
        "level": level_code,
        "status": "completed" if level_code in ("L4", "L5") else "in_progress",
        "hours": hours,
        "concepts_mastered": mastered,
        "concepts_total": total,
        "test_avg": test_avg
    }

    # Update total hours
    profile["total_hours"] = sum(t["hours"] for t in profile["topics"].values())

    # Update strengths and weaknesses
    strengths = []
    weaknesses = []
    for name, c in concepts.items():
        if c["mastery"] == "mastered":
            strengths.append(name)
        elif c["mastery"] == "learning":
            weaknesses.append(name)
    profile["strengths"] = strengths[:10]  # Top 10
    profile["weaknesses"] = weaknesses[:10]  # Top 10

    save_profile(profile)
    return profile


def compare_profile_with_job(job_title: str) -> dict[str, Any]:
    """
    Compare user profile with job requirements.
    
    Args:
        job_title: Job title to compare with
    
    Returns:
        Dictionary with comparison results
    """
    profile = load_profile()
    
    # Get current level from topics
    topics = profile.get("topics", {})
    if not topics:
        return {
            "job_title": job_title,
            "current_level": "L1",
            "mastered_skills": [],
            "weaknesses": [],
            "total_hours": 0,
            "suggestion": "Run Step 2a industry research to search for job requirements."
        }
    
    # Find the highest level topic (use numeric comparison)
    highest_level = "L1"
    highest_level_num = 1
    total_hours = 0
    
    for _, data in topics.items():
        level = data.get("level", "L1")
        # Extract numeric level for comparison
        try:
            level_num = int(level[1:])
        except (ValueError, IndexError):
            level_num = 1
        if level_num > highest_level_num:
            highest_level = level
            highest_level_num = level_num
        total_hours += data.get("hours", 0)
    
    # Get strengths and weaknesses from profile
    strengths = profile.get("strengths", [])
    weaknesses = profile.get("weaknesses", [])
    
    return {
        "job_title": job_title,
        "current_level": highest_level,
        "mastered_skills": strengths[:10],
        "weaknesses": weaknesses[:10],
        "total_hours": total_hours,
        "suggestion": f"Run Step 2a industry research to search for '{job_title} 岗位要求' and get gap analysis."
    }


_LEVEL_MAP = {
    "L1": ("L1", "入门 (Novice)", "[L1]"),
    "L2": ("L2", "初学 (Beginner)", "[L2]"),
    "L3": ("L3", "进阶 (Intermediate)", "[L3]"),
    "L4": ("L4", "熟练 (Proficient)", "[L4]"),
    "L5": ("L5", "精通 (Mastery)", "[L5]"),
}


def _calc_upgrade_level(history: list[dict[str, Any]], level_thresholds: dict[str, float]) -> int:
    """
    Calculate level by walking through test pairs for tiered upgrades.

    Design intent: Isolate upgrade logic so it's independently testable.
    No-skip rule: can only upgrade one level per adjacent test pair.
    """
    level = 1
    first_avg = sum(h["accuracy"] for h in history[:2]) / 2
    if first_avg >= level_thresholds["L2"]:
        level = 2

    thresholds = {3: level_thresholds["L3"], 4: level_thresholds["L4"], 5: level_thresholds["L5"]}
    next_level = 3
    for i in range(len(history) - 1):
        if next_level > 5:
            break
        pair = history[i:i + 2]
        threshold = thresholds[next_level]
        if all(h["accuracy"] >= threshold for h in pair) and level >= next_level - 1:
            level = next_level
            next_level += 1
    return level


def _check_demotion(level: int, history: list[dict[str, Any]], level_thresholds: dict[str, float]) -> int:
    """
    Check if level should be demoted based on recent performance.

    Design intent: Gradual degradation — only demote one level per check.
    SM-2 principle: incorrect answers reset interval but don't skip stages.
    """
    if level >= 3 and len(history) >= 3:
        maintain_thresholds = {
            2: level_thresholds["L2"], 3: level_thresholds["L3"],
            4: level_thresholds["L4"], 5: level_thresholds["L5"],
        }
        threshold = maintain_thresholds[level]
        last3 = history[-3:]
        if all(h["accuracy"] < threshold for h in last3):
            return level - 1
    return level


# L1-L5 等级系统：基于模块测试准确率，非 SM-2 掌握度
# 升级规则：前2次测试平均 >= 阈值
# 降级规则：最近3次测试低于阈值（渐进降级，每次只降一级）
# 权威标准：等级 ≠ 掌握度，等级基于测试成绩，掌握度基于复习正确率

def calc_level_by_accuracy(topic: str, concepts_fallback: dict[str, Any] | None = None) -> tuple[str, str, str]:
    """
    Calculate level based on test accuracy (not SM-2 mastery).

    Design intent: Delegates upgrade/demotion to helpers for clarity.
    Fallback to mastery overview when no test history exists.

    算法说明：
    1. 初始等级为L1
    2. 前2次测试平均答对率 >= 20% → 升级到L2
    3. 遍历所有相邻测试对，检查是否满足下一级阈值（不跳级）
    4. 降级检查：最近3次都低于阈值则降一级
    """
    history = load_test_history().get(topic, [])
    config = load_config()
    level_thresholds = config["level_thresholds"]

    if len(history) == 0:
        if concepts_fallback:
            _, _, pct = calc_mastery_overview(concepts_fallback)
            if pct >= 0.9:
                return _LEVEL_MAP["L4"]
            elif pct >= 0.5:
                return _LEVEL_MAP["L3"]
            elif pct >= 0.2:
                return _LEVEL_MAP["L2"]
        return _LEVEL_MAP["L1"]

    if len(history) == 1:
        avg = history[0]["accuracy"]
        if avg >= level_thresholds["L2"]:
            return _LEVEL_MAP["L2"]
        return _LEVEL_MAP["L1"]

    level = _calc_upgrade_level(history, level_thresholds)
    level = _check_demotion(level, history, level_thresholds)

    return _LEVEL_MAP.get(f"L{level}", _LEVEL_MAP["L1"])


def calc_mastery_overview(concepts: dict[str, Any]) -> tuple[int, int, float]:
    """
    Calculate mastery overview for display purposes only.
    NOT used for level calculation.
    
    Args:
        concepts: Dictionary of concepts
    
    Returns:
        Tuple of (mastered_count, total_count, percentage)
    """
    if not concepts:
        return 0, 0, 0
    total = len(concepts)
    mastered = sum(1 for c in concepts.values() if c["mastery"] == "mastered")
    pct = mastered / total if total > 0 else 0
    return mastered, total, pct


# config.json — 用户配置（算法选择、学习深度、每日限额等）
# concepts.json — 每个 topic 的概念列表（间隔、难度、稳定性等）
# progress.md — 每个 topic 的学习进度 Markdown
# ensure_dirs() 在每个 cmd_* 开头调用，防止 FileNotFoundError

def ensure_dirs() -> None:
    """Ensure required directories exist."""
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)


# Cache for config to avoid repeated file reads
_config_cache: dict[str, Any] | None = None
_config_cache_time: float | None = None


def load_config(use_cache: bool = True) -> dict[str, Any]:
    """
    Load configuration from file with optional caching.
    
    Args:
        use_cache: Whether to use cached config (default: True)
    
    Returns:
        Configuration dictionary
    """
    global _config_cache, _config_cache_time
    
    # Check cache validity (5 minutes)
    if use_cache and _config_cache is not None and _config_cache_time is not None:
        if (datetime.now().timestamp() - _config_cache_time) < 300:  # 5 minutes
            return copy.deepcopy(_config_cache)
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding='utf-8') as f:
                config = json.load(f)
            # Merge with defaults for missing keys
            for k, v in DEFAULT_CONFIG.items():
                if k not in config:
                    config[k] = v
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error loading config file: {e}")
            config = DEFAULT_CONFIG.copy()
    else:
        config = DEFAULT_CONFIG.copy()
    
    # Update cache
    _config_cache = copy.deepcopy(config)
    _config_cache_time = datetime.now().timestamp()
    
    return config


def save_config(config: dict[str, Any]) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
    """
    global _config_cache, _config_cache_time
    
    ensure_dirs()
    _atomic_json_save(CONFIG_FILE, config)
    
    # Invalidate cache
    _config_cache = None
    _config_cache_time = None


def load_concepts(topic: str) -> dict[str, Any]:
    """
    Load concepts for a specific topic.
    
    Args:
        topic: Topic name
    
    Returns:
        Dictionary of concepts
    """
    topic_dir = TOPICS_DIR / topic
    concepts_file = topic_dir / "concepts.json"
    if concepts_file.exists():
        try:
            with open(concepts_file, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_concepts(topic: str, concepts: dict[str, Any]) -> None:
    """
    Save concepts for a specific topic using atomic write.
    
    Args:
        topic: Topic name
        concepts: Dictionary of concepts to save
    """
    ensure_dirs()
    topic_dir = TOPICS_DIR / topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    concepts_file = topic_dir / "concepts.json"
    _atomic_json_save(concepts_file, concepts)


def load_progress(topic: str) -> str:
    """
    Load progress content for a specific topic.
    
    Args:
        topic: Topic name
    
    Returns:
        Progress content as string
    """
    topic_dir = TOPICS_DIR / topic
    progress_file = topic_dir / "progress.md"
    if progress_file.exists():
        return progress_file.read_text()
    return ""


def save_progress(topic: str, content: str) -> None:
    """
    Save progress content for a specific topic.
    
    Args:
        topic: Topic name
        content: Progress content to save
    """
    topic_dir = TOPICS_DIR / topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    progress_file = topic_dir / "progress.md"
    _atomic_text_save(progress_file, content)


def today() -> str:
    """
    Get today's date as string.
    
    Returns:
        Today's date in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")


# 基于 IEEE TKDE 2023 论文：Su, Ye, Nie, Cao & Chen
# DOI: 10.1109/TKDE.2023.3251721
# 自实现 ~120 行，保持零外部依赖
# 19 个默认参数（FSRS_V5_WEIGHTS_DEFAULT）
# 幂律遗忘曲线：R(t, S) = (1 + FACTOR × t / S)^DECAY
#
# 核心函数（8个）：
# - fsrs_init_stability: 初始稳定性 S₀(G) = w[G-1]
# - fsrs_init_difficulty: 初始难度 D₀(G) = w₄ - exp(w₅×(G-1)) + 1
# - fsrs_retrievability: 遗忘曲线 R(t, S)
# - fsrs_next_interval: 从稳定性计算间隔 I = S/FACTOR × (R^(1/DECAY) - 1)
# - fsrs_update_difficulty: 难度均值回归 D' = w₇×D₀(4) + (1-w₇)×(D - w₆×(G-3))
# - fsrs_stability_after_recall: 成功回忆后稳定性更新
# - fsrs_stability_after_forgetting: 遗忘后稳定性更新
# - fsrs_short_term_stability: 同天复习的短期稳定性
#
# 精确 R 计算（v1.3.0）：
# _compute_r_at_recall 从 next_review 和 interval_days 反推 elapsed days
# 避免 R=0.9 近似值在同天 review 时的误差

# Map user-facing ratings to FSRS integer ratings
# "wrong" = Again (1), "hard" = Hard (2), "good" = Good (3), "easy" = Easy (4)
RATING_TO_INT = {"wrong": 1, "hard": 2, "good": 3, "easy": 4}


def _compute_r_at_recall(c: dict[str, Any], s: float) -> float:
    """
    Compute exact retrievability R at recall time from elapsed days.

    Design intent: Use the forgetting curve R(t, S) = (1 + FACTOR*t/S)^DECAY
    where t = days since last review. Derived from concept's next_review
    and interval_days. Falls back to 0.9 if data is missing.
    """
    try:
        next_review = c.get("next_review")
        interval_days = c.get("interval_days", 0)
        if not next_review or interval_days <= 0:
            return 0.9  # Fallback for first review or missing data
        # last_review_date = next_review - interval_days
        review_date = datetime.strptime(next_review, "%Y-%m-%d")
        last_review = review_date - timedelta(days=interval_days)
        elapsed = (datetime.now() - last_review).days
        if elapsed <= 0:
            elapsed = 1  # Minimum 1 day
        r = (1 + FSRS_FACTOR * elapsed / s) ** FSRS_DECAY
        return max(FSRS_R_MIN, min(FSRS_R_MAX, r))
    except (ValueError, OSError, OverflowError):
        return 0.9  # Safe fallback


def _calc_next_review_fsrs(c: dict[str, Any], rating: str) -> dict[str, Any]:
    """
    FSRS-5 scheduling: update difficulty, stability, retrievability.

    Design intent: Separated from SM-2 logic for clarity.
    Falls back to SM-2 on any calculation error (defensive).
    """

    rating_int = RATING_TO_INT.get(rating, 3)

    # Initialize FSRS fields on first review
    if "difficulty" not in c:
        c["difficulty"] = fsrs_init_difficulty(rating_int)
        c["stability"] = fsrs_init_stability(rating_int)
        c["retrievability"] = 1.0
    else:
        d = c["difficulty"]
        s = c["stability"]
        # Compute exact R from elapsed time since last review.
        # R(t, S) = (1 + FACTOR * t / S)^DECAY where t = days since last review.
        # We derive t from next_review (scheduled date) and interval_days:
        #   last_review_date = next_review - interval_days
        #   elapsed = today - last_review_date
        r = _compute_r_at_recall(c, s)

        try:
            # Update difficulty
            d = fsrs_update_difficulty(d, rating_int)

            # Update stability based on rating
            if rating_int == 1:  # Again/wrong = lapse
                s = fsrs_stability_after_forgetting(s, d, r)
            else:  # Hard/Good/Easy = successful recall
                s = fsrs_stability_after_recall(s, d, r, rating_int)

            # Defensive: check for NaN/Inf
            if math.isnan(d) or math.isinf(d) or math.isnan(s) or math.isinf(s):
                raise ValueError("NaN/Inf in FSRS calculation")

            c["difficulty"] = d
            c["stability"] = s
        except (ValueError, ZeroDivisionError, OverflowError):
            # Fallback: keep current values, don't crash
            pass

    c["retrievability"] = 1.0  # Just reviewed, R resets to 1

    # Calculate interval from stability
    interval = fsrs_next_interval(c["stability"])
    c["interval_days"] = int(interval)

    return c


def calc_next_review(concept: dict[str, Any], rating: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Calculate next review using SM-2 or FSRS-5 based on config.

    Design intent: Dispatch to algorithm-specific implementation.
    Default is FSRS-5 (since v1.3.0).
    Falls back to SM-2 when config.algorithm = "sm2".

    Args:
        concept: Concept dictionary with scheduling parameters
        rating: Review rating ("easy", "good", "hard", "wrong")
        config: Optional configuration dictionary (loaded if not provided)

    Returns:
        Updated concept dictionary with new review schedule

    Raises:
        ValueError: If rating is not valid
    """
    if rating not in ("easy", "good", "hard", "wrong"):
        raise ValueError(f"Invalid rating: {rating}. Must be 'easy', 'good', 'hard', or 'wrong'")

    if config is None:
        config = load_config()

    algorithm = config.get("algorithm", "sm2")

    # FSRS path
    if algorithm == "fsrs":
        # Use personalized weights if available, otherwise defaults
        custom_weights = config.get("fsrs_weights")
        if custom_weights and len(custom_weights) >= 19:
            _set_fsrs_weights(custom_weights)
        c = concept.copy()
        c["reviews"] = c.get("reviews", 0) + 1
        c["total_count"] = c.get("total_count", 0) + 1
        if rating != "wrong":
            c["correct_count"] = c.get("correct_count", 0) + 1
        c = _calc_next_review_fsrs(c, rating)
        _update_mastery(c, config)
        next_date = datetime.now() + timedelta(days=c["interval_days"])
        c["next_review"] = next_date.strftime("%Y-%m-%d")
        return c

    # SM-2 path (default, backward compatible)
    c = concept.copy()
    is_second_review = (c["reviews"] == 1)
    c["reviews"] += 1
    c["total_count"] += 1
    mastery_threshold = config.get("mastery_threshold", 0.8)

    if rating == "wrong":
        c["interval_days"] = 1
        c["ease_factor"] = max(1.3, c["ease_factor"] - 0.2)
    elif rating == "hard":
        if is_second_review:
            c["interval_days"] = SM2_SECOND_INTERVAL
        else:
            c["interval_days"] = max(1, int(c["interval_days"] * 1.2))
        c["ease_factor"] = max(1.3, c["ease_factor"] - 0.15)
        c["correct_count"] += 1
    elif rating == "good":
        if is_second_review:
            c["interval_days"] = SM2_SECOND_INTERVAL
        else:
            c["interval_days"] = max(1, int(c["interval_days"] * c["ease_factor"]))
        c["correct_count"] += 1
    elif rating == "easy":
        if is_second_review:
            c["interval_days"] = SM2_SECOND_INTERVAL
        else:
            c["interval_days"] = max(1, int(c["interval_days"] * (c["ease_factor"] + 0.15)))
        c["ease_factor"] = c["ease_factor"] + 0.15
        c["correct_count"] += 1

    _update_mastery(c, config)
    next_date = datetime.now() + timedelta(days=c["interval_days"])
    c["next_review"] = next_date.strftime("%Y-%m-%d")
    return c


def _update_mastery(c: dict[str, Any], config: dict[str, Any]) -> None:
    """Update mastery level based on recent accuracy. Shared by SM-2 and FSRS."""
    mastery_threshold = config.get("mastery_threshold", 0.8)
    if c["total_count"] >= 1 and c["mastery"] == "unseen":
        c["mastery"] = "learning"
    if c["total_count"] >= 3:
        accuracy = c["correct_count"] / c["total_count"]
        if accuracy >= mastery_threshold and c["reviews"] >= 3:
            c["mastery"] = "mastered"
        elif accuracy >= 0.6:
            c["mastery"] = "reviewing"
        else:
            c["mastery"] = "learning"


# --- FSRS-5 Algorithm Implementation ---
# Based on: IEEE TKDE 2023 (DOI: 10.1109/TKDE.2023.3251721)
# Self-implemented to maintain zero external dependencies

# FSRS-5 default weights (19 parameters)
FSRS_V5_WEIGHTS_DEFAULT = [
    0.40255, 1.18385, 3.173, 15.69105,      # w[0-3]: initial stability (Again/Hard/Good/Easy)
    7.1949, 0.5345, 1.4604, 0.0046,          # w[4-7]: difficulty calculation
    1.54575, 0.1192, 1.01925, 1.9395,        # w[8-11]: stability after recall/forgetting
    0.11, 0.29605, 2.2698, 0.2315,           # w[12-15]: stability after forgetting cont.
    2.9898, 0.51655, 0.6621                  # w[16-18]: short-term stability
]

# Active weights (mutable, can be personalized via optimize-params)
FSRS_V5_WEIGHTS = list(FSRS_V5_WEIGHTS_DEFAULT)


def _set_fsrs_weights(weights: list[float]) -> None:
    """Set personalized FSRS weights. Called by calc_next_review when config has fsrs_weights."""
    global FSRS_V5_WEIGHTS
    FSRS_V5_WEIGHTS = list(weights[:19])

# Forgetting curve constants (derived from w[20] = -0.5 in FSRS-5)
FSRS_DECAY = -0.5
FSRS_FACTOR = 19 / 81  # ≈ 0.234568, ensures R(S, S) = 0.9

# Defensive bounds
FSRS_D_MIN = 1.0
FSRS_D_MAX = 10.0
FSRS_S_MIN = 0.1
FSRS_S_MAX = 36500.0
FSRS_R_MIN = 0.0
FSRS_R_MAX = 1.0


def fsrs_init_stability(rating: int) -> float:
    """
    Initial stability S₀(G) = w[G-1].

    Design intent: Direct lookup from weights based on first rating.
    Higher ratings give higher initial stability.
    """
    w = FSRS_V5_WEIGHTS
    return w[rating - 1]


def fsrs_init_difficulty(rating: int) -> float:
    """
    Initial difficulty D₀(G) = w₄ - exp(w₅ × (G-1)) + 1, clamped to [1, 10].

    Design intent: Exponential formula — higher ratings give lower difficulty.
    Clamped to prevent extreme values.
    """

    w = FSRS_V5_WEIGHTS
    d = w[4] - math.exp(w[5] * (rating - 1)) + 1
    return max(FSRS_D_MIN, min(FSRS_D_MAX, d))


def fsrs_retrievability(t: float, s: float) -> float:
    """
    Retrievability R(t, S) = (1 + FACTOR × t / S)^DECAY.

    Design intent: Power-law forgetting curve. When t=S, R≈0.9 by design.
    Defensive: clamps result to [0, 1], handles S≤0.
    """
    if s <= 0:
        return FSRS_R_MIN
    r = (1 + FSRS_FACTOR * t / s) ** FSRS_DECAY
    return max(FSRS_R_MIN, min(FSRS_R_MAX, r))


def fsrs_next_interval(s: float, desired_r: float = 0.9) -> float:
    """
    Calculate interval from stability: I = S/FACTOR × (desired_r^(1/DECAY) - 1).

    Design intent: Inverse of retrievability formula.
    For desired_r=0.9 and S=10, interval ≈ 10 days.
    """

    if s <= 0:
        return 1.0
    interval = s / FSRS_FACTOR * (desired_r ** (1 / FSRS_DECAY) - 1)
    return max(1.0, round(interval))


def fsrs_update_difficulty(d: float, rating: int) -> float:
    """
    Difficulty update: D' = w₇ × D₀(4) + (1 - w₇) × (D - w₆ × (G - 3)).

    Design intent: Mean-reversion toward initial difficulty of Easy rating.
    Successful reviews (G>3) decrease difficulty, failures (G<3) increase it.
    Clamped to [1, 10].
    """
    w = FSRS_V5_WEIGHTS
    d0_easy = fsrs_init_difficulty(4)
    d_new = w[7] * d0_easy + (1 - w[7]) * (d - w[6] * (rating - 3))
    return max(FSRS_D_MIN, min(FSRS_D_MAX, d_new))


def fsrs_stability_after_recall(s: float, d: float, r: float, rating: int) -> float:
    """
    Stability after successful recall (rating >= 2).

    S'ᵣ = S × (1 + exp(w₈) × (11-D) × S^(-w₉) × (exp(w₁₀×(1-R))-1) × hard_penalty × easy_bonus)

    Design intent: Stability increases more when difficulty is lower,
    current stability is lower, and retrievability is lower.
    Hard rating applies penalty, Easy rating applies bonus.
    """

    w = FSRS_V5_WEIGHTS
    hard_penalty = w[15] if rating == 2 else 1.0
    easy_bonus = w[16] if rating == 4 else 1.0
    increment = math.exp(w[8]) * (11 - d) * (s ** (-w[9])) * (math.exp(w[10] * (1 - r)) - 1)
    s_new = s * (1 + increment * hard_penalty * easy_bonus)
    return max(FSRS_S_MIN, min(FSRS_S_MAX, s_new))


def fsrs_stability_after_forgetting(s: float, d: float, r: float) -> float:
    """
    Stability after forgetting (rating = 1, lapse).

    S'f = w₁₁ × D^(-w₁₂) × ((S+1)^(w₁₃) - 1) × exp(w₁₄ × (1-R))

    Design intent: Stability decreases. Higher difficulty and higher previous
    stability lead to larger drops.
    """

    w = FSRS_V5_WEIGHTS
    s_new = w[11] * (d ** (-w[12])) * ((s + 1) ** w[13] - 1) * math.exp(w[14] * (1 - r))
    return max(FSRS_S_MIN, min(FSRS_S_MAX, s_new))


def fsrs_short_term_stability(s: float, rating: int) -> float:
    # NOTE: Not currently used — kept for reference / future same-day review handling
    """
    Short-term stability for same-day reviews.

    S' = S × exp(w₁₇ × (rating - 3 + w₁₈))

    Design intent: Adjusts stability for reviews within the same session.
    Simplified from full FSRS-5 (which also uses S^(-w₁₉)).
    """

    w = FSRS_V5_WEIGHTS
    s_new = s * math.exp(w[17] * (rating - 3 + w[18]))
    return max(FSRS_S_MIN, min(FSRS_S_MAX, s_new))


def get_accuracy_str(concept: dict[str, Any]) -> str:
    """
    Get accuracy string for display.
    
    Args:
        concept: Concept dictionary
    
    Returns:
        Accuracy percentage string or "N/A"
    """
    if concept["total_count"] == 0:
        return "N/A"
    acc = concept["correct_count"] / concept["total_count"]
    return f"{acc:.0%}"


def calc_overdue(next_review: str | None) -> int:
    """
    Calculate overdue days from next_review date string.
    
    Args:
        next_review: Date string in YYYY-MM-DD format, or None
    
    Returns:
        Number of overdue days (0 if not overdue or invalid date)
    """
    if not next_review:
        return 0
    try:
        review_date = datetime.strptime(next_review, "%Y-%m-%d")
        return max(0, (datetime.now() - review_date).days)
    except ValueError:
        return 0


def get_mastery_emoji(mastery: str) -> str:
    """
    Get mastery status emoji for display.
    
    Args:
        mastery: Mastery status string
    
    Returns:
        Mastery status emoji string
    """
    return {"mastered": "[MASTERED]", "reviewing": "[REVIEWING]", "learning": "[LEARNING]", "unseen": "[UNSEEN]"}.get(mastery, "[UNSEEN]")


def calc_level(concepts: dict[str, Any], topic: str | None = None) -> tuple[str, str, str]:
    """
    Calculate skill level.

    If topic is provided, uses test_history for authoritative level.
    Otherwise, falls back to mastery-based overview (for display only).
    
    Args:
        concepts: Dictionary of concepts
        topic: Optional topic name for authoritative level calculation
    
    Returns:
        Tuple of (level_code, level_name, level_emoji)
    """
    if topic:
        return calc_level_by_accuracy(topic, concepts_fallback=concepts)

    # Fallback: mastery-based overview (for display only, not authoritative)
    _, _, pct = calc_mastery_overview(concepts)
    if pct >= 0.9:
        return "L5", "精通 (Mastery)", "[L5]"
    elif pct >= 0.7:
        return "L4", "熟练 (Proficient)", "[L4]"
    elif pct >= 0.4:
        return "L3", "进阶 (Intermediate)", "[L3]"
    elif pct >= 0.2:
        return "L2", "初学 (Beginner)", "[L2]"
    else:
        return "L1", "入门 (Novice)", "[L1]"


# get_accuracy_str: 准确率显示字符串
# calc_overdue: 计算逾期天数 = today - next_review
# get_mastery_emoji: 掌握状态 emoji
# calc_level: 综合等级计算（优先用 test_history，回退用 concepts）

# cmd_init: 创建新 topic（~/learn/topics/{topic}/）
# cmd_add: 添加概念到 topic
# cmd_rate: 非交互式评分（AI 助手调用）
# cmd_review: 交互式复习（用户使用）

def cmd_init(args: list[str]) -> None:
    """
    Initialize a new topic.

    Design intent: Accept raw args list so main() dispatch is uniform.
    Validates topic name to prevent path traversal.
    """
    if len(args) < 1:
        print("Usage: srs.py init <topic>")
        return
    topic = args[0]
    try:
        topic = sanitize_topic(topic)
    except SanitizeError as e:
        print(f"Error: {e}")
        return
    ensure_dirs()
    topic_dir = TOPICS_DIR / topic
    if topic_dir.exists():
        print(f"Topic '{topic}' already exists.")
        return
    topic_dir.mkdir(parents=True)
    save_concepts(topic, {})
    # Create notes.md
    (topic_dir / "notes.md").write_text(f"# {topic}\n\n## Notes\n\n")
    # Create progress.md
    (topic_dir / "progress.md").write_text(f"# {topic} - Progress\n\n## Started: {today()}\n\n")
    print(f"[OK] Topic '{topic}' created at {topic_dir}")


def cmd_add(args: list[str]) -> None:
    """
    Add a concept to a topic.

    Design intent: Accept raw args list so main() dispatch is uniform.
    Both topic and concept are sanitized to prevent path traversal.
    """
    if len(args) < 2:
        print("Usage: srs.py add <topic> <concept>")
        return
    topic = args[0]
    concept_name = args[1]
    try:
        topic = sanitize_topic(topic)
        concept_name = sanitize_concept(concept_name)
    except SanitizeError as e:
        print(f"Error: {e}")
        return
    concepts = load_concepts(topic)
    if concept_name in concepts:
        print(f"Concept '{concept_name}' already exists in '{topic}'.")
        return
    concepts[concept_name] = DEFAULT_CONCEPT.copy()
    concepts[concept_name]["added"] = today()
    concepts[concept_name]["next_review"] = today()  # Due immediately for first review
    save_concepts(topic, concepts)
    print(f"[OK] Added '{concept_name}' to '{topic}'. First review due today.")


def cmd_rate(args: list[str]) -> None:
    """
    Non-interactively rate a concept and update its SM-2 state.

    Design intent: Accept raw args list so main() dispatch is uniform.
    This is the safe way for AI assistants to update concept review status
    without needing to call the interactive cmd_review.
    """
    if len(args) < 3:
        print("Usage: srs.py rate <topic> <concept> <rating>")
        return
    topic = args[0]
    concept_name = args[1]
    rating = args[2]
    try:
        topic = sanitize_topic(topic)
        concept_name = sanitize_concept(concept_name)
    except SanitizeError as e:
        print(f"Error: {e}")
        return
    if rating not in ("easy", "good", "hard", "wrong"):
        print(f"Error: Invalid rating '{rating}'. Must be 'easy', 'good', 'hard', or 'wrong'")
        return
    concepts = load_concepts(topic)
    if not concepts:
        print(f"Error: Topic '{topic}' does not exist or has no concepts")
        return
    if concept_name not in concepts:
        print(f"Error: Concept '{concept_name}' not found in topic '{topic}'")
        return
    c = concepts[concept_name]
    updated = calc_next_review(c, rating)
    concepts[concept_name] = updated
    save_concepts(topic, concepts)
    # Log the rating action
    append_learning_log("rate", topic, {
        "concept": concept_name,
        "rating": rating
    })
    print(f"[OK] Rated '{concept_name}' as '{rating}'. Next review: {updated['next_review']}")


def _find_due_concepts(concepts: dict[str, Any], today_str: str) -> list[tuple[str, dict[str, Any]]]:
    """Find concepts due for review today. Returns sorted list of (name, concept)."""
    due = []
    for name, c in concepts.items():
        if c["next_review"] and c["next_review"] <= today_str:
            due.append((name, c))
    return due


def _print_no_due_message(concepts: dict[str, Any]) -> None:
    """Print message when no reviews are due, including next review date if available."""
    next_dates = []
    for name, c in concepts.items():
        if c["next_review"]:
            next_dates.append((c["next_review"], name))
    if next_dates:
        next_dates.sort()
        print(f"   Next review: {next_dates[0][0]} ({next_dates[0][1]})")


def _run_review_loop(
    due: list[tuple[str, dict[str, Any]]],
    concepts: dict[str, Any],
    burnout_threshold: int,
) -> int:
    """
    Run the interactive review loop. Returns number of concepts reviewed.

    Design intent: Isolate the interactive state machine from data loading.
    """
    consecutive_wrong = 0
    reviewed = 0

    for name, c in due:
        if consecutive_wrong >= burnout_threshold:
            print(f"\n[WARNING] Burnout detected ({consecutive_wrong} consecutive wrong).")
            print("   Consider taking a break or switching to easier material.")
            resp = input("   Continue anyway? (y/n): ").strip().lower()
            if resp != "y":
                break
            consecutive_wrong = 0

        mastery = get_mastery_emoji(c["mastery"])
        accuracy = get_accuracy_str(c)
        print(f"\n{'='*50}")
        print(f"  {mastery} {name}")
        print(f"  Reviews: {c['reviews']} | Accuracy: {accuracy} | Interval: {c['interval_days']}d")
        print(f"{'='*50}")
        print("  (In interactive mode, AI助手 would quiz you on this concept)")

        while True:
            rating = input("  Rate [easy/good/hard/wrong]: ").strip().lower()
            if rating in ("easy", "good", "hard", "wrong", "quit"):
                break
            print("  Invalid. Use: easy, good, hard, wrong, or quit")

        if rating == "quit":
            print("\nSession ended early.")
            break

        concepts[name] = calc_next_review(c, rating)
        reviewed += 1
        consecutive_wrong = consecutive_wrong + 1 if rating == "wrong" else 0

    return reviewed


def cmd_review(args: list[str]) -> None:
    """
    Start a review session for a topic.

    Design intent: Orchestrates data loading, due-finding, and review loop.
    """
    if len(args) < 1:
        print("Usage: srs.py review <topic>")
        return
    topic = args[0]
    try:
        topic = sanitize_topic(topic)
    except SanitizeError as e:
        print(f"Error: {e}")
        return
    concepts = load_concepts(topic)
    if not concepts:
        print(f"No concepts in '{topic}'. Add some first: srs.py add {topic} <concept>")
        return

    config = load_config()
    limit = config.get("daily_review_limit", 20)
    burnout_threshold = config.get("burnout_threshold", 3)

    due = _find_due_concepts(concepts, today())
    if not due:
        print(f"[OK] No reviews due today for '{topic}'.")
        _print_no_due_message(concepts)
        return

    due = due[:limit]
    print(f"\n[REVIEW] Review Session: {topic}")
    print(f"   Due today: {len(due)} concept(s)")
    print(f"   Rate each: easy / good / hard / wrong")
    print(f"   Type 'quit' to stop early\n")

    reviewed = _run_review_loop(due, concepts, burnout_threshold)
    save_concepts(topic, concepts)
    print(f"\n[OK] Reviewed {reviewed} concept(s). Progress saved.")


def cmd_due(args: list[str]) -> None:
    """Show all due reviews for today. Ignores args."""
    ensure_dirs()
    today_str = today()
    all_due = []

    for topic_dir in TOPICS_DIR.iterdir():
        if not topic_dir.is_dir():
            continue
        # Filter out test/debug/temp directories
        if topic_dir.name.startswith(("test-", "debug-", "temp-")):
            continue
        concepts = load_concepts(topic_dir.name)
        for name, c in concepts.items():
            if c["next_review"] and c["next_review"] <= today_str:
                all_due.append((topic_dir.name, name, c))

    if not all_due:
        print("[OK] No reviews due today!")
        return

    # Sort by next_review (oldest first)
    all_due.sort(key=lambda x: x[2]["next_review"])

    config = load_config()
    limit = config.get("daily_review_limit", 20)
    all_due = all_due[:limit]

    print(f"\n[DUE] Due Reviews ({len(all_due)} total):\n")
    current_topic = None
    for topic, name, c in all_due:
        if topic != current_topic:
            print(f"  [DIR] {topic}")
            current_topic = topic
        mastery = get_mastery_emoji(c["mastery"])
        accuracy = get_accuracy_str(c)
        overdue = calc_overdue(c["next_review"])
        overdue_str = f" ({overdue}d overdue)" if overdue > 0 else ""
        print(f"     {mastery} {name} [acc: {accuracy}, int: {c['interval_days']}d]{overdue_str}")


# cmd_due: 显示所有到期复习
# cmd_today: 今日学习计划 + 逾期分析（v1.3.0 新增）
# cmd_streak: 连续学习天数（从今天倒推计算）（v1.3.0 新增）
# cmd_analyze: 学习趋势 + 薄弱概念 + 活动统计（v1.3.0 新增）
# cmd_optimize_params: FSRS 参数个性化（梯度下降，需 1000+ review）（v1.3.0 新增）

def cmd_today(args: list[str]) -> None:
    """
    Show today's learning plan with overdue analysis.

    Design intent: More actionable than cmd_due — includes overdue count,
    topic breakdown, and a learning recommendation.
    """
    ensure_dirs()
    today_str = today()
    all_due = []
    overdue_count = 0

    for topic_dir in TOPICS_DIR.iterdir():
        if not topic_dir.is_dir():
            continue
        if topic_dir.name.startswith(("test-", "debug-", "temp-")):
            continue
        concepts = load_concepts(topic_dir.name)
        for name, c in concepts.items():
            if c["next_review"] and c["next_review"] <= today_str:
                overdue = calc_overdue(c["next_review"])
                if overdue > 0:
                    overdue_count += 1
                all_due.append((topic_dir.name, name, c, overdue))

    if not all_due:
        print("\n[TODAY] No reviews due today. Great job staying on track!")
        return

    # Sort by overdue (most overdue first)
    all_due.sort(key=lambda x: -x[3])

    config = load_config()
    limit = config.get("daily_review_limit", 20)

    # Group by topic
    topics_summary: dict[str, list] = {}
    for topic, name, c, overdue in all_due:
        if topic not in topics_summary:
            topics_summary[topic] = []
        topics_summary[topic].append((name, c, overdue))

    print(f"\n[TODAY] Learning Plan for {today_str}\n")
    print(f"  Total due: {len(all_due)} concept(s)")
    if overdue_count > 0:
        print(f"  Overdue:   {overdue_count} concept(s) — prioritize these first!")
    print()

    for topic, items in topics_summary.items():
        print(f"  [{topic}] ({len(items)} due)")
        for name, c, overdue in items[:5]:  # Show top 5 per topic
            overdue_str = f" ({overdue}d overdue)" if overdue > 0 else ""
            mastery = get_mastery_emoji(c["mastery"])
            print(f"    {mastery} {name}{overdue_str}")
        if len(items) > 5:
            print(f"    ... and {len(items) - 5} more")

    # Recommendation
    print()
    if overdue_count > len(all_due) // 2:
        print("  [TIP] Many concepts are overdue. Focus on reviewing before learning new material.")
    elif overdue_count > 0:
        print("  [TIP] Start with overdue concepts, then review normally.")
    else:
        print("  [TIP] All concepts are on time. Keep up the good work!")


def cmd_streak(args: list[str]) -> None:
    """
    Show consecutive learning days streak.

    Design intent: Uses learning_log.json to count consecutive days
    with at least one learning activity.
    """
    log = load_learning_log()
    if not log:
        print("\n[STREAK] No learning activity recorded yet. Start learning today!")
        return

    # Extract unique dates from log
    dates = sorted(set(entry["timestamp"][:10] for entry in log), reverse=True)

    # Count streak from today backwards
    today_str = today()
    streak = 0
    check_date = datetime.now()

    for _ in range(len(dates)):
        date_str = check_date.strftime("%Y-%m-%d")
        if date_str in dates:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    print(f"\n[STREAK] Learning Streak\n")
    print(f"  Current streak: {streak} day(s)")
    print(f"  Total active days: {len(dates)}")
    if dates:
        print(f"  Last activity: {dates[0]}")
    if streak == 0 and dates:
        print(f"\n  [TIP] Streak counts from today. Study today to keep it going!")

    if streak >= 7:
        print(f"\n  [GREAT] 7+ day streak! Consistency is the key to mastery.")
    elif streak >= 3:
        print(f"\n  [GOOD] Keep going! Try to reach 7 days.")
    elif streak > 0:
        print(f"\n  [START] Good start! Build momentum.")


def cmd_analyze(args: list[str]) -> None:
    """
    Analyze learning trends, weak concepts, and efficiency.

    Design intent: Data-driven analysis using test_history and learning_log.
    Shows actionable insights, not just raw data.
    """
    ensure_dirs()
    history = load_test_history()
    log = load_learning_log()

    if not history:
        print("\n[ANALYZE] No test history available. Complete some tests first.")
        return

    print("\n[ANALYZE] Learning Analysis\n")

    # Topic-level analysis
    print("  Topic Performance:")
    for topic, tests in history.items():
        if not tests:
            continue
        recent = tests[-5:]
        avg = sum(t["accuracy"] for t in recent) / len(recent)
        trend = "↑" if len(tests) >= 2 and tests[-1]["accuracy"] > tests[-2]["accuracy"] else "↓" if len(tests) >= 2 and tests[-1]["accuracy"] < tests[-2]["accuracy"] else "→"
        level_code, level_name, _ = calc_level_by_accuracy(topic)
        print(f"    {topic:20s} | {level_code} | avg: {avg:.0%} {trend} | {len(tests)} tests")

    # Weak concepts (overdue + low mastery)
    print("\n  Weak Concepts (overdue or struggling):")
    weak_count = 0
    today_str = today()
    for topic_dir in TOPICS_DIR.iterdir():
        if not topic_dir.is_dir():
            continue
        concepts = load_concepts(topic_dir.name)
        for name, c in concepts.items():
            overdue = calc_overdue(c.get("next_review"))
            if overdue > 3 or c.get("mastery") == "learning":
                weak_count += 1
                if weak_count <= 5:
                    mastery = get_mastery_emoji(c.get("mastery", "unseen"))
                    print(f"    {mastery} {topic_dir.name}/{name} (overdue: {overdue}d)")
    if weak_count == 0:
        print("    [OK] No weak concepts found!")
    elif weak_count > 5:
        print(f"    ... and {weak_count - 5} more")

    # Activity summary
    if log:
        rate_actions = [e for e in log if e["action"] == "rate"]
        test_actions = [e for e in log if e["action"] == "record-test"]
        print(f"\n  Activity Summary:")
        print(f"    Total ratings: {len(rate_actions)}")
        print(f"    Total tests: {len(test_actions)}")
        if rate_actions:
            print(f"    Last rating: {rate_actions[-1]['timestamp'][:16]}")


def cmd_optimize_params(args: list[str]) -> None:
    """
    Optimize FSRS-5 parameters using local review history.

    Design intent: Uses numerical gradient descent (finite differences) to
    minimize binary cross-entropy loss between predicted R and actual recall.
    Pure Python implementation, zero external dependencies.

    Best practices (from FSRS community):
    - Minimum 1,000 reviews for meaningful optimization
    - Optimize every 2-3 months, not more frequently
    - Check rating distribution — >95% same rating = bad signal
    - New parameters need 2 weeks to evaluate
    - Parameters drastically different from defaults = anomaly warning

    Saves optimized weights to config.json under 'fsrs_weights' key.
    """

    log = load_learning_log()

    # Collect rate actions (review events)
    rate_actions = [e for e in log if e["action"] == "rate"]
    if len(rate_actions) < 1000:
        print(f"\n[OPTIMIZE] Need at least 1,000 reviews for meaningful optimization.")
        print(f"  Current: {len(rate_actions)} reviews")
        print(f"  FSRS community recommends 1,000+ to avoid overfitting.")
        print(f"  Keep learning and come back after more reviews!")
        return

    # Check rating distribution — >95% same rating is a pitfall
    rating_counts: dict[str, int] = {}
    for entry in rate_actions:
        r = entry.get("details", {}).get("rating", "unknown")
        rating_counts[r] = rating_counts.get(r, 0) + 1
    total = len(rate_actions)
    for r, count in rating_counts.items():
        if count / total > 0.95:
            print(f"\n[OPTIMIZE] Warning: {count/total:.0%} of ratings are '{r}'.")
            print(f"  The optimizer needs diverse ratings to learn your patterns.")
            print(f"  Try using 'hard' and 'wrong' more often when appropriate.")
            return

    print(f"\n[OPTIMIZE] Optimizing FSRS-5 parameters...")
    print(f"  Reviews: {len(rate_actions)}")
    print(f"  Rating distribution: {rating_counts}")

    # Group by topic+concept to build review histories
    histories: dict[str, list[dict]] = {}
    for entry in rate_actions:
        topic = entry.get("topic", "")
        concept = entry.get("details", {}).get("concept", "")
        key = f"{topic}/{concept}"
        if key not in histories:
            histories[key] = []
        histories[key].append({
            "timestamp": entry["timestamp"],
            "rating": entry["details"].get("rating", "good"),
        })

    # Sort each history by timestamp
    for key in histories:
        histories[key].sort(key=lambda x: x["timestamp"])

    # Count different-day reviews
    different_day_count = 0
    for key, reviews in histories.items():
        dates = set(r["timestamp"][:10] for r in reviews)
        different_day_count += len(dates)

    if different_day_count < 50:
        print(f"  Different-day reviews: {different_day_count} (need 50+)")
        print(f"  Try reviewing across multiple days for better optimization.")
        return

    print(f"  Different-day reviews: {different_day_count}")
    print(f"  Concepts: {len(histories)}")

    # Simple gradient descent with finite differences
    # Minimize: sum of -[y*log(R) + (1-y)*log(1-R)] where y=1 if recalled, 0 if forgotten
    weights = list(FSRS_V5_WEIGHTS_DEFAULT)
    learning_rate = 0.001
    epochs = 10
    epsilon = 0.01  # For finite differences

    def compute_loss(w):
        """Compute total BCE loss across all review histories."""
        global FSRS_V5_WEIGHTS
        FSRS_V5_WEIGHTS = list(w)
        total_loss = 0.0
        count = 0
        for key, reviews in histories.items():
            s = None
            d = None
            prev_date = None
            for rev in reviews:
                rating_int = RATING_TO_INT.get(rev["rating"], 3)
                rev_date = rev["timestamp"][:10]
                if s is None:
                    # First review — initialize
                    s = fsrs_init_stability(rating_int)
                    d = fsrs_init_difficulty(rating_int)
                    prev_date = rev_date
                    continue
                # Compute elapsed days
                try:
                    dt_prev = datetime.strptime(prev_date, "%Y-%m-%d")
                    dt_curr = datetime.strptime(rev_date, "%Y-%m-%d")
                    elapsed = max(1, (dt_curr - dt_prev).days)
                except ValueError:
                    elapsed = 1
                # Predict R
                r = fsrs_retrievability(elapsed, s)
                r = max(0.001, min(0.999, r))  # Clamp for log stability
                # Actual recall: 1 if not "wrong", 0 if "wrong"
                y = 0.0 if rev["rating"] == "wrong" else 1.0
                # BCE loss
                loss = -(y * math.log(r) + (1 - y) * math.log(1 - r))
                total_loss += loss
                count += 1
                # Update state
                d = fsrs_update_difficulty(d, rating_int)
                if rating_int == 1:
                    s = fsrs_stability_after_forgetting(s, d, r)
                else:
                    s = fsrs_stability_after_recall(s, d, r, rating_int)
                prev_date = rev_date
        return total_loss / max(1, count)

    # Initial loss
    best_loss = compute_loss(weights)
    best_weights = list(weights)
    print(f"  Initial loss: {best_loss:.4f}")

    # Gradient descent with finite differences (only optimize w[0]-w[14], skip bounds)
    for epoch in range(epochs):
        gradients = [0.0] * 15  # Only optimize first 15 parameters
        for i in range(15):
            w_plus = list(weights)
            w_plus[i] += epsilon
            loss_plus = compute_loss(w_plus)

            w_minus = list(weights)
            w_minus[i] -= epsilon
            loss_minus = compute_loss(w_minus)

            gradients[i] = (loss_plus - loss_minus) / (2 * epsilon)

        # Update weights
        for i in range(15):
            weights[i] -= learning_rate * gradients[i]
            # Clamp to reasonable bounds
            weights[i] = max(0.001, min(100.0, weights[i]))

        current_loss = compute_loss(weights)
        if current_loss < best_loss:
            best_loss = current_loss
            best_weights = list(weights)
        print(f"  Epoch {epoch+1}/{epochs}: loss={current_loss:.4f} (best={best_loss:.4f})")

    # Save optimized weights
    config = load_config(use_cache=False)
    config["fsrs_weights"] = best_weights
    save_config(config)

    # Check parameter drift (FSRS community best practice)
    max_drift = 0.0
    for i in range(15):
        if FSRS_V5_WEIGHTS_DEFAULT[i] > 0:
            drift = abs(best_weights[i] - FSRS_V5_WEIGHTS_DEFAULT[i]) / FSRS_V5_WEIGHTS_DEFAULT[i]
            max_drift = max(max_drift, drift)

    print(f"\n[OK] Optimized parameters saved to config.json")
    print(f"  Loss: {best_loss:.4f} (lower is better)")
    print(f"  Optimized {15} of 19 parameters (w[0]-w[14])")
    if max_drift > 2.0:
        print(f"  ⚠️ Warning: parameters drifted {max_drift:.1f}x from defaults.")
        print(f"  This may indicate unusual review patterns. Consider resetting.")
    print(f"  To use: algorithm is already 'fsrs' — parameters applied automatically")
    print(f"  To reset: srs.py config set fsrs_weights null")
    print(f"\n  [TIP] Re-optimize every 2-3 months. Give new parameters 2 weeks to evaluate.")


# cmd_status: 显示学习状态（总体 / 单个 topic）
# cmd_config: 查看/设置配置（algorithm、learning_depth 等）

def _show_topic_status(topic: str, concepts: dict[str, Any]) -> None:
    """Display status for a single topic. Called by cmd_status."""
    level_code, level_name, level_emoji = calc_level(concepts, topic=topic)
    mastered = sum(1 for c in concepts.values() if c["mastery"] == "mastered")
    reviewing = sum(1 for c in concepts.values() if c["mastery"] == "reviewing")
    learning = sum(1 for c in concepts.values() if c["mastery"] == "learning")
    unseen = sum(1 for c in concepts.values() if c["mastery"] == "unseen")
    total = len(concepts)

    print(f"\n[STATUS] {topic} Status:\n")
    print(f"  等级:{level_emoji} {level_code} {level_name}")
    print()
    print(f"  [MASTERED] Mastered:  {mastered}/{total}")
    print(f"  [REVIEWING] Reviewing: {reviewing}/{total}")
    print(f"  [LEARNING] Learning:  {learning}/{total}")
    print(f"  [UNSEEN] Unseen:    {unseen}/{total}")

    print("\n  Concepts:")
    for name, c in concepts.items():
        mastery = get_mastery_emoji(c["mastery"])
        accuracy = get_accuracy_str(c)
        print(f"    {mastery} {name:30s} | acc: {accuracy:4s} | int: {c['interval_days']:3d}d | next: {c['next_review']}")


def _show_overall_status() -> None:
    """Display overall learning status across all topics. Called by cmd_status."""
    print("\n[STATUS] Overall Learning Status:\n")

    total_concepts = 0
    total_mastered = 0
    total_due = 0
    today_str = today()

    for topic_dir in sorted(TOPICS_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue
        concepts = load_concepts(topic_dir.name)
        if not concepts:
            continue

        mastered = sum(1 for c in concepts.values() if c["mastery"] == "mastered")
        due = sum(1 for c in concepts.values() if c["next_review"] and c["next_review"] <= today_str)
        total = len(concepts)

        total_concepts += total
        total_mastered += mastered
        total_due += due

        status = "[OK]" if mastered == total else "[PROGRESS]"
        print(f"  {status} {topic_dir.name:20s} | {mastered}/{total} mastered | {due} due today")

    if total_concepts > 0:
        pct = total_mastered / total_concepts * 100
        print(f"\n  Total: {total_mastered}/{total_concepts} mastered ({pct:.0f}%)")
        print(f"  Due today: {total_due}")


def cmd_status(args: list[str]) -> None:
    """
    Show learning status.

    Design intent: Delegates to _show_topic_status or _show_overall_status
    based on whether a topic argument is provided.
    """
    ensure_dirs()
    topic = args[0] if args else None

    if topic:
        try:
            topic = sanitize_topic(topic)
        except SanitizeError as e:
            print(f"Error: {e}")
            return
        concepts = load_concepts(topic)
        if not concepts:
            print(f"No concepts in '{topic}'.")
            return
        _show_topic_status(topic, concepts)
    else:
        _show_overall_status()


def cmd_config(args: list[str]) -> None:
    """
    Show or set configuration.

    Design intent: Accept raw args list so main() dispatch is uniform.
    Handles 'set' subcommand internally: config set <key> <value>.
    """
    config = load_config()

    # Handle "set" subcommand: args = ["set", "key", "value"]
    if args and args[0] == "set":
        if len(args) < 3:
            print("Usage: srs.py config set <key> <value>")
            return
        key = args[1]
        value = args[2]
    else:
        key = args[0] if args else None
        value = args[1] if len(args) > 1 else None

    if key is None:
        print(f"\n[CONFIG] Config ({CONFIG_FILE}):\n")
        for k, v in config.items():
            print(f"  {k}: {v}")
        return

    if value is None:
        if key in config:
            print(f"  {key}: {config[key]}")
        else:
            print(f"  Key '{key}' not found.")
        return

    # Set value
    if key not in DEFAULT_CONFIG:
        print(f"  Unknown key: {key}")
        print(f"  Valid keys: {', '.join(DEFAULT_CONFIG.keys())}")
        return

    # Type coercion
    default_val = DEFAULT_CONFIG[key]
    converted_value = value
    if isinstance(default_val, int):
        try:
            converted_value = int(value)
        except ValueError:
            print(f"  Error: {key} must be an integer")
            return
    elif isinstance(default_val, float):
        try:
            converted_value = float(value)
        except ValueError:
            print(f"  Error: {key} must be a number")
            return

    config[key] = converted_value
    save_config(config)
    print(f"  [OK] {key} = {converted_value}")


# 所有 subprocess 调用都在这里，调用 openclaw CLI 管理定时任务
# _cron_exists: 检查 cron 任务是否存在
# _get_user_channel: 从 openclaw sessions 检测用户通知渠道
# _delete_cron: 删除 cron 任务
# _recreate_crons_with_channel: 重建 cron 任务（切换渠道时用）
# cmd_setup_reminder: 创建学习提醒 + 周报 cron
# cmd_check_reminder: 检查提醒状态
# cmd_switch_channel: 切换通知渠道
# cmd_reminder: 生成今日学习计划（含遗忘风险分析）
# cmd_weekly_report: 生成周报数据
#
# 注意：这些命令依赖 openclaw CLI，仅在 OpenClaw 环境中可用
# v1.4.0: setup-reminder 添加平台检测，非 OpenClaw 环境自动降级为 REMINDER_REQUIRED

def _is_openclaw_available() -> bool:
    """Check if openclaw CLI is available on this system.

    Design intent: v1.4.0 multi-agent-framework compatibility.
    Instead of silently failing when openclaw is not installed,
    setup-reminder falls back to REMINDER_REQUIRED output.
    """
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _cron_exists(name: str) -> bool:
    """
    Check if a cron job with the given name exists.

    Args:
        name: Cron job name to check

    Returns:
        True if the cron job exists, False otherwise
    """
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return False
        data = json.loads(result.stdout)
        # openclaw cron list --json returns {"jobs": [...], ...}
        jobs = data.get("jobs", []) if isinstance(data, dict) else data
        return any(j.get("name") == name for j in jobs)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return False


def _get_user_delivery(channel_filter: str = "") -> tuple[str, str] | None:
    """Detect the user's delivery target from OpenClaw sessions.

    Parses the session key format: agent:main:{channel}:{kind}:{chat_id}
    to extract both the channel provider and the user's chat ID.

    Args:
        channel_filter: If provided, only match sessions from this channel.
                        E.g., "openclaw-weixin" to find the WeChat session.

    Returns:
        (channel, chat_id) tuple, e.g., ("openclaw-weixin", "o9cq80...@im.wechat"),
        or None if not detected.

    Design intent: v1.4.0+ fix — openclaw sessions --json does NOT return an
    "origin" field. The provider and chat_id are encoded in the session "key".
    Without both values, cron --announce cannot resolve the delivery target
    in isolated sessions when multiple channels are configured.
    """
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        sessions = data.get("sessions", []) if isinstance(data, dict) else data
        for session in sessions:
            if not isinstance(session, dict):
                continue
            # Session key format: agent:main:{channel}:{kind}:{chat_id}
            key = session.get("key", "")
            if not key.startswith("agent:main:"):
                continue
            parts = key.split(":")
            if len(parts) >= 5:
                channel = parts[2]       # e.g., "openclaw-weixin"
                chat_id = ":".join(parts[4:])  # e.g., "o9cq80...@im.wechat" (may contain colons)
                # If filter specified, only return matching channel
                if channel_filter and channel != channel_filter:
                    continue
                return (channel, chat_id)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def _get_user_channel() -> str | None:
    """Detect the user's channel name from OpenClaw sessions. Returns channel name or None.

    Kept for backward compatibility with cmd_check_reminder and cmd_switch_channel.
    """
    delivery = _get_user_delivery()
    return delivery[0] if delivery else None


def _delete_cron(name: str) -> bool:
    """Delete a cron job by name. Returns True if deleted."""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "delete", "--name", name],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _recreate_crons_with_channel(channel: str, chat_id: str = "") -> None:
    """Delete existing crons and recreate them with the given channel and target."""
    config = load_config()
    contract = config.get("learning_contract", {})
    reminder_time = contract.get("time", "09:00")
    hour = reminder_time.split(":")[0]
    to_target = f"{channel}:{chat_id}" if chat_id else ""

    # Delete existing crons
    _delete_cron("retaincraft-reminder")
    _delete_cron("retaincraft-weekly-report")

    # Recreate daily reminder
    cron_args = [
        "openclaw", "cron", "add",
        "--name", "retaincraft-reminder",
        "--cron", f"0 {hour} * * *",
        "--tz", "Asia/Shanghai",
        "--session", "isolated",
        "--channel", channel,
        "--message", f"执行: python3 {SCRIPTS_DIR / 'srs.py'} reminder",
        "--announce"
    ]
    if to_target:
        cron_args.extend(["--to", to_target])
    try:
        subprocess.run(cron_args, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Recreate weekly report
    cron_args = [
        "openclaw", "cron", "add",
        "--name", "retaincraft-weekly-report",
        "--cron", "0 20 * * 0",
        "--tz", "Asia/Shanghai",
        "--session", "isolated",
        "--channel", channel,
        "--message", f"执行: python3 {SCRIPTS_DIR / 'srs.py'} weekly-report",
        "--announce"
    ]
    if to_target:
        cron_args.extend(["--to", to_target])
    try:
        subprocess.run(cron_args, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


def cmd_setup_reminder(args: list[str]) -> None:
    """Setup learning reminder and weekly report cron jobs. Ignores args.

    Design intent: v1.4.0 multi-agent-framework compatibility.
    If openclaw CLI is not available, falls back to REMINDER_REQUIRED output
    so the AI agent can create a platform-native reminder instead.
    """
    # v1.4.0: Platform detection — fallback for non-OpenClaw environments
    if not _is_openclaw_available():
        config = load_config()
        contract = config.get("learning_contract", {})
        reminder_time = contract.get("time", "09:00")
        days = contract.get("days", ["Mon", "Tue", "Wed", "Thu", "Fri"])
        days_str = ", ".join(days)

        print(f"[INFO] OpenClaw CLI not detected. Falling back to platform-agnostic mode.")
        print(f"")
        print(f"REMINDER_REQUIRED")
        print(f"Please create a timed learning reminder for the user:")
        print(f"  Schedule: daily at {reminder_time}")
        print(f"  Days: {days_str}")
        print(f"  Message: Time to study! You have concepts due for review.")
        print(f"")
        print(f"Use whatever reminder mechanism your platform supports.")
        return

    config = load_config()
    contract = config.get("learning_contract", {})
    reminder_time = contract.get("time", "09:00")

    # Validate time format (HH:MM)
    if not re.match(r'^\d{2}:\d{2}$', reminder_time):
        print(f"[WARN] Invalid reminder time format: '{reminder_time}'. Expected HH:MM (e.g., '09:00').")
        print("       Using default: 09:00")
        reminder_time = "09:00"

    hour = reminder_time.split(":")[0]

    # Resolve delivery target with priority:
    #   1. config.active_channel (user-explicit) → find that channel's session
    #   2. Current session channel + chat_id (auto-detect)
    #   3. No --to (legacy fallback)
    active_channel = config.get("active_channel", "")
    if active_channel:
        # User explicitly chose a channel — find that channel's session
        channel_delivery = _get_user_delivery(channel_filter=active_channel)
        if channel_delivery:
            user_channel = channel_delivery[0]
            user_to = f"{channel_delivery[0]}:{channel_delivery[1]}"
        else:
            # Active channel set but no session found for it — fall back to current
            session_delivery = _get_user_delivery()
            user_channel = session_delivery[0] if session_delivery else None
            user_to = f"{session_delivery[0]}:{session_delivery[1]}" if session_delivery else None
    else:
        # No explicit channel — auto-detect from current session
        session_delivery = _get_user_delivery()
        user_channel = session_delivery[0] if session_delivery else None
        user_to = f"{session_delivery[0]}:{session_delivery[1]}" if session_delivery else None

    # Setup daily reminder
    if _cron_exists("retaincraft-reminder"):
        print("[OK] Learning reminder cron already exists.")
    else:
        cron_args = [
            "openclaw", "cron", "add",
            "--name", "retaincraft-reminder",
            "--cron", f"0 {hour} * * *",
            "--tz", "Asia/Shanghai",
            "--session", "isolated",
            "--message", f"执行: python3 {SCRIPTS_DIR / 'srs.py'} reminder",
            "--announce"
        ]
        if user_channel and user_to:
            cron_args.extend(["--channel", user_channel, "--to", user_to])

        try:
            result = subprocess.run(cron_args, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"[OK] Learning reminder cron created (daily at {reminder_time}).")
                if user_channel:
                    print(f"     Channel: {user_channel}")
                    print(f"     Target: {user_to}")
            else:
                print(f"[WARN] Failed to create reminder cron: {result.stderr}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"[WARN] Failed to create reminder cron: {e}")

    # Setup weekly report
    if _cron_exists("retaincraft-weekly-report"):
        print("[OK] Weekly report cron already exists.")
    else:
        cron_args = [
            "openclaw", "cron", "add",
            "--name", "retaincraft-weekly-report",
            "--cron", "0 20 * * 0",
            "--tz", "Asia/Shanghai",
            "--session", "isolated",
            "--message", f"执行: python3 {SCRIPTS_DIR / 'srs.py'} weekly-report",
            "--announce"
        ]
        if user_channel and user_to:
            cron_args.extend(["--channel", user_channel, "--to", user_to])

        try:
            result = subprocess.run(cron_args, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("[OK] Weekly report cron created (Sunday at 20:00).")
            else:
                print(f"[WARN] Failed to create weekly report cron: {result.stderr}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"[WARN] Failed to create weekly report cron: {e}")


def cmd_check_reminder(args: list[str]) -> None:
    """Check the status of learning reminders. Ignores args."""
    print("\n[CHECK-REMINDER] Reminder Status:\n")

    # Check daily reminder
    if _cron_exists("retaincraft-reminder"):
        config = load_config()
        contract = config.get("learning_contract", {})
        reminder_time = contract.get("time", "09:00")
        delivery = _get_user_delivery()
        channel = delivery[0] if delivery else "auto-detect"
        to_target = f"{delivery[0]}:{delivery[1]}" if delivery else "not detected"
        print(f"  ✅ Learning reminder: ENABLED")
        print(f"     Time: {reminder_time}")
        print(f"     Channel: {channel}")
        print(f"     Target: {to_target}")
    else:
        print(f"  ⚠️  Learning reminder: NOT ENABLED")
        print(f"     Run 'srs.py setup-reminder' to enable")

    # Check weekly report
    if _cron_exists("retaincraft-weekly-report"):
        print(f"  ✅ Weekly report: ENABLED")
        print(f"     Schedule: Sunday at 20:00")
    else:
        print(f"  ⚠️  Weekly report: NOT ENABLED")
        print(f"     Run 'srs.py setup-reminder' to enable")


def cmd_switch_channel(args: list[str]) -> None:
    """List available notification channels and switch the active one. Ignores args."""
    current = _get_user_channel()
    print(f"\n[SWITCH-CHANNEL] Current channel: {current or 'not detected'}\n")

    # List available channels from config
    config = load_config()
    channels = config.get("reminder_channels", [])

    if not channels:
        print("  No channels configured. Add channels to config.json:")
        print('  "reminder_channels": [')
        print('    {"type": "telegram", "target": "-1001234567890"},')
        print('    {"type": "qqbot", "target": "group123"}')
        print('  ]')
        return

    print("  Available channels:")
    for i, ch in enumerate(channels, 1):
        marker = " (current)" if ch["type"] == current else ""
        print(f"    {i}. {ch['type']} - {ch['target']}{marker}")

    # Prompt user to select a channel
    print()
    try:
        choice = input("  Enter channel number to switch (or press Enter to cancel): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n  Cancelled.")
        return

    if not choice:
        print("  Cancelled.")
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(channels):
            print(f"  Invalid choice: {choice}. Must be 1-{len(channels)}.")
            return
    except ValueError:
        print(f"  Invalid input: {choice}. Must be a number.")
        return

    selected = channels[idx]
    config["active_channel"] = selected["type"]
    save_config(config)

    # Recreate cron jobs with the new channel
    # Use channel_filter to get the TARGET channel's chat_id, not the current session's
    print(f"\n  Switching to: {selected['type']} - {selected['target']}")
    delivery = _get_user_delivery(channel_filter=selected["type"])
    chat_id = delivery[1] if delivery else ""
    _recreate_crons_with_channel(selected["type"], chat_id)
    print(f"  [OK] Channel switched to {selected['type']}.")


def cmd_reminder(args: list[str]) -> None:
    """Generate today's learning plan with forgetting risk analysis. Ignores args."""
    ensure_dirs()
    config = load_config()
    contract = config.get("learning_contract", {})

    # Calculate forgetting risk
    last_time = get_last_learning_time()
    now = datetime.now()
    days_since = (now - last_time).days if last_time else 999

    # Forgetting risk based on Ebbinghaus (1885), validated by Murre & Dros (2015)
    if days_since >= 7:
        risk = "critical"
        risk_msg = f"你已经 {days_since} 天没学习了。知识基本回到起点，建议从最简单的概念重新开始。"
    elif days_since >= 2:
        risk = "high"
        forgetting_rates = {2: 72, 3: 73, 4: 74, 5: 74, 6: 75}
        forgetting_pct = forgetting_rates.get(days_since, 75)
        risk_msg = f"你已经 {days_since} 天没学习了。遗忘率已达约{forgetting_pct}%，建议今天只复习，不学新内容。"
    elif days_since == 1:
        risk = "low"
        risk_msg = "昨天没学习，今天复习一下。24 小时是遗忘拐点。"
    else:
        risk = "none"
        risk_msg = ""

    # Get due concepts across all topics
    today_str = today()
    topics_due = []
    for topic_dir in sorted(TOPICS_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue
        concepts = load_concepts(topic_dir.name)
        if not concepts:
            continue

        due_concepts = []
        for name, c in concepts.items():
            if c["next_review"] and c["next_review"] <= today_str:
                overdue = calc_overdue(c["next_review"])
                due_concepts.append({
                    "name": name,
                    "status": c["mastery"],
                    "overdue_days": overdue
                })

        if due_concepts:
            # Sort by overdue days (descending)
            due_concepts.sort(key=lambda x: -x["overdue_days"])
            topics_due.append({
                "name": topic_dir.name,
                "concepts": due_concepts,
                "count": len(due_concepts)
            })

    # Build output
    output = {
        "date": today_str,
        "risk": risk,
        "risk_msg": risk_msg,
        "days_since_learning": days_since,
        "topics": topics_due,
        "total_due": sum(t["count"] for t in topics_due)
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_weekly_report(args: list[str]) -> None:
    """Generate weekly learning report data. Ignores args."""
    log = load_learning_log()
    now = datetime.now()

    # Filter logs for the past 7 days
    week_ago = now - timedelta(days=7)
    week_log = [
        entry for entry in log
        if datetime.fromisoformat(entry["timestamp"]) >= week_ago
    ]

    # Calculate statistics
    learning_days = len(set(
        entry["timestamp"][:10] for entry in week_log
    ))

    rate_actions = [e for e in week_log if e["action"] == "rate"]
    test_actions = [e for e in week_log if e["action"] == "record-test"]

    topics_covered = list(set(entry["topic"] for entry in week_log))

    # Calculate average accuracy from tests
    avg_accuracy = 0
    if test_actions:
        accuracies = [e.get("accuracy", 0) for e in test_actions]
        avg_accuracy = sum(accuracies) / len(accuracies)

    # Detect level changes
    level_changes = {}
    for topic in topics_covered:
        level_code, level_name, level_emoji = calc_level_by_accuracy(topic)
        level_changes[topic] = f"{level_code} {level_name}"

    # Check burnout status
    burnout_status = {}
    for topic in topics_covered:
        try:
            burnout = check_burnout(topic)
            burnout_status[topic] = burnout.get("risk", "unknown")
        except Exception:
            burnout_status[topic] = "unknown"

    # Build report
    report = {
        "period": {
            "start": week_ago.strftime("%Y-%m-%d"),
            "end": now.strftime("%Y-%m-%d")
        },
        "learning_days": learning_days,
        "total_actions": len(week_log),
        "rate_actions": len(rate_actions),
        "test_actions": len(test_actions),
        "topics_covered": topics_covered,
        "avg_accuracy": avg_accuracy,
        "level_changes": level_changes,
        "burnout_status": burnout_status
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))


def cmd_sign_contract(args: list[str]) -> None:
    """Save learning contract to config and output reminder requirement.

    Design intent: When user confirms the learning contract via AI conversation,
    AI calls this command to persist the contract. The output tells AI to create
    a timed reminder using whatever mechanism the current platform provides.
    This is the core of v1.4.0 multi-agent-framework compatibility:
    code outputs WHAT to do, AI figures out HOW to do it on its platform.
    """
    if len(args) < 1:
        print("Usage: srs.py sign-contract <json_string>")
        print('Example: srs.py sign-contract \'{"time": "20:00", "days": ["Mon","Tue","Wed","Thu","Fri"], "duration": 60, "target_level": "L4"}\'')
        return

    try:
        contract = json.loads(args[0])
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        return

    # Save to config
    config = load_config(use_cache=False)
    config["learning_contract"] = contract
    save_config(config)

    # Output reminder requirement for AI
    reminder_time = contract.get("time", "09:00")
    days = contract.get("days", ["Mon", "Tue", "Wed", "Thu", "Fri"])
    days_str = ", ".join(days)

    print(f"[OK] Learning contract saved.")
    print(f"")
    print(f"REMINDER_REQUIRED")
    print(f"Please create a timed learning reminder for the user:")
    print(f"  Schedule: daily at {reminder_time}")
    print(f"  Days: {days_str}")
    print(f"  Message: Time to study! You have concepts due for review.")
    print(f"")
    print(f"Use whatever reminder mechanism your platform supports.")


# cmd_record_test: 记录模块测试成绩
# cmd_test_history: 查看测试历史
# cmd_record_simulation: 记录模拟场景成绩
# cmd_simulation_history: 查看模拟历史
# cmd_profile: 查看/更新用户画像
# cmd_check_session: 检查未记录的测试
# cmd_check_burnout: 分析倦怠风险

def cmd_record_test(args: list[str]) -> None:
    """
    Record a test result for a topic.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    Handles integer parsing and error display.
    """
    if len(args) < 3:
        print("Usage: srs.py record-test <topic> <total> <correct>")
        return
    try:
        total = int(args[1])
        correct = int(args[2])
    except ValueError:
        print("Error: total and correct must be integers")
        return
    try:
        result = record_test(args[0], total, correct)
        print(f"[OK] Recorded test for '{args[0]}': {correct}/{total} ({result['accuracy']:.0%})")
        level_code, level_name, level_emoji = calc_level_by_accuracy(args[0])
        print(f"   Level: {level_emoji} {level_code} {level_name}")
    except ValueError as e:
        print(f"[ERROR] Input error: {e}")


def cmd_test_history(args: list[str]) -> None:
    """
    Show test history for a topic or all topics.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    """
    topic = args[0] if args else None
    history = load_test_history()
    if topic:
        tests = history.get(topic, [])
        if not tests:
            print(f"No test history for '{topic}'.")
            return
        print(f"\n[HISTORY] Test History: {topic}\n")
        for i, t in enumerate(tests, 1):
            print(f"  {i}. {t['timestamp'][:16]} | {t['correct']}/{t['total']} ({t['accuracy']:.0%})")
        level_code, level_name, level_emoji = calc_level_by_accuracy(topic)
        print(f"\n  Level: {level_emoji} {level_code} {level_name}")
    else:
        if not history:
            print("No test history.")
            return
        print("\n[HISTORY] Test History:\n")
        for tpc, tests in history.items():
            level_code, level_name, level_emoji = calc_level_by_accuracy(tpc)
            print(f"  [DIR] {tpc}: {len(tests)} tests | {level_emoji} {level_code} {level_name}")


def cmd_record_simulation(args: list[str]) -> None:
    """
    Record a simulation result.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    Handles --rounds optional flag.
    """
    if len(args) < 3:
        print("Usage: srs.py record-simulation <topic> <scenario> <score> [--rounds N]")
        return
    try:
        score = int(args[2])
    except ValueError:
        print("Error: score must be an integer")
        return
    rounds = 3
    if "--rounds" in args:
        rounds_idx = args.index("--rounds")
        if rounds_idx + 1 < len(args):
            try:
                rounds = int(args[rounds_idx + 1])
            except ValueError:
                print("Error: rounds must be an integer")
                return
    record_simulation(args[0], args[1], score, rounds)
    print(f"[OK] Recorded simulation for '{args[0]}': {args[1]} | Score: {score}/100 | Rounds: {rounds}")


def cmd_simulation_history(args: list[str]) -> None:
    """
    Show simulation history for a topic or all topics.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    """
    topic = args[0] if args else None
    history = load_simulation_history()
    if topic:
        simulations = history.get(topic, [])
        if not simulations:
            print(f"No simulation history for '{topic}'.")
            return
        print(f"\n[HISTORY] Simulation History: {topic}\n")
        for i, s in enumerate(simulations, 1):
            print(f"  {i}. {s['timestamp'][:16]} | {s['scenario']} | Score: {s['score']}/100 | Rounds: {s['rounds']}")
    else:
        if not history:
            print("No simulation history.")
            return
        print("\n[HISTORY] Simulation History:\n")
        for tpc, simulations in history.items():
            print(f"  [DIR] {tpc}: {len(simulations)} simulations")


def cmd_profile(args: list[str]) -> None:
    """
    Show or update user profile.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    Handles --update and --compare subcommands.
    """
    if args and args[0] == "--update":
        ensure_dirs()
        topics = [d.name for d in TOPICS_DIR.iterdir() if d.is_dir()]
        if not topics:
            print("No topics found.")
            return
        for topic in topics:
            update_profile(topic)
        print(f"[OK] Profile updated for {len(topics)} topic(s).")
    elif args and args[0] == "--compare":
        if len(args) < 2:
            print("Usage: srs.py profile --compare <job_title>")
            return
        result = compare_profile_with_job(args[1])
        print(f"\n[PROFILE] Profile Comparison: {args[1]}\n")
        print(f"  当前最高等级: {result['current_level']}")
        print(f"  总学习时长: {result['total_hours']:.1f} 小时")
        if result.get('mastered_skills'):
            skills = ', '.join(result['mastered_skills'][:5])
            print(f"  掌握技能: {skills}")
        if result.get('weaknesses'):
            weaknesses = ', '.join(result['weaknesses'][:5])
            print(f"  薄弱环节: {weaknesses}")
        print(f"  [TIP] {result['suggestion']}")
    else:
        profile = load_profile()
        print("\n[PROFILE] User Profile:\n")
        print(f"  Goal: {profile['goal'] or 'Not set'}")
        print(f"  Started: {profile['started']}")
        print(f"  Total Hours: {profile['total_hours']:.1f}")
        print(f"  Last Updated: {profile['last_updated'][:16]}")
        if profile['topics']:
            print("\n  Topics:")
            for topic, data in profile['topics'].items():
                status = "[OK]" if data['status'] == 'completed' else "[PROGRESS]"
                print(f"    {status} {topic}: {data['level']} | {data['concepts_mastered']}/{data['concepts_total']} mastered | {data['test_avg']:.0f}% avg")
        if profile['strengths']:
            print(f"\n  Strengths: {', '.join(profile['strengths'][:5])}")
        if profile['weaknesses']:
            print(f"  Weaknesses: {', '.join(profile['weaknesses'][:5])}")


def cmd_check_session(args: list[str]) -> None:
    """
    Check for unrecorded test sessions.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    """
    topic = args[0] if args else None
    result = check_session(topic)
    if result["status"] == "no_history":
        print(f"[INFO] {result['message']}")
    else:
        threshold = result["stale_minutes_threshold"]
        print(f"\n[CHECK-SESSION] Session Integrity Check (stale > {threshold} min)\n")
        for f in result["findings"]:
            status_icon = "[STALE]" if f["stale"] else "[OK]"
            acc = f["last_accuracy"]
            gap = f["gap_minutes"]
            print(f"  {status_icon} {f['topic']:20s} | last: {f['last_record'][:16]} | acc: {acc:.0%} | {gap:.0f} min ago")
        if result["stale_count"] > 0:
            print(f"\n  [WARNING] {result['stale_count']} topic(s) have stale records.")
            print("  If a module test was conducted without record-test, the level will not update.")
        else:
            print(f"\n  [OK] All records are fresh (within {threshold} minutes).")


def cmd_check_burnout(args: list[str]) -> None:
    """
    Analyze burnout risk for a topic.

    Design intent: Extracted from main() to enable dispatch dict pattern.
    Handles --window optional flag.
    """
    if len(args) < 1:
        print("Usage: srs.py check-burnout <topic> [--window N]")
        return
    topic = args[0]
    window = 5
    if "--window" in args:
        idx = args.index("--window")
        if idx + 1 < len(args):
            try:
                window = int(args[idx + 1])
            except ValueError:
                print("Error: window must be an integer")
                return
    try:
        result = check_burnout(topic, window)
    except SanitizeError as e:
        print(f"Error: {e}")
        return
    if result["status"] == "no_data":
        print(f"[INFO] {result['message']}")
    else:
        risk_map = {"low": "[LOW]", "medium": "[MEDIUM]", "high": "[HIGH]"}
        print(f"\n[CHECK-BURNOUT] Burnout Risk Analysis: {topic}\n")
        print(f"  Risk Level:   {risk_map.get(result['risk'], result['risk'])}")
        print(f"  Trend:        {result['trend']}")
        print(f"  Avg Accuracy: {result['avg_accuracy']:.0%} (last {result['recent_tests']} tests)")
        print(f"  Consecutive below 50%: {result['consecutive_below_50']}")
        if result["suggestions"]:
            print("\n  Suggestions:")
            for s in result["suggestions"]:
                print(f"    - {s}")


# dispatch 字典：24 个命令的 O(1) 查表路由
# v1.3.0 重构：246 行 if-elif → 38 行 dispatch 字典
# 所有 cmd_* 函数统一签名为 (args: list[str])

def main() -> None:
    """Main entry point for the CLI. Dispatch via dict lookup for O(1) routing."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return

    cmd = args[0]
    cmd_args = args[1:]

    dispatch = {
        "init": cmd_init,
        "add": cmd_add,
        "review": cmd_review,
        "rate": cmd_rate,
        "due": cmd_due,
        "today": cmd_today,
        "streak": cmd_streak,
        "analyze": cmd_analyze,
        "optimize-params": cmd_optimize_params,
        "status": cmd_status,
        "record-test": cmd_record_test,
        "test-history": cmd_test_history,
        "record-simulation": cmd_record_simulation,
        "simulation-history": cmd_simulation_history,
        "profile": cmd_profile,
        "check-session": cmd_check_session,
        "check-burnout": cmd_check_burnout,
        "config": cmd_config,
        "setup-reminder": cmd_setup_reminder,
        "reminder": cmd_reminder,
        "weekly-report": cmd_weekly_report,
        "check-reminder": cmd_check_reminder,
        "switch-channel": cmd_switch_channel,
        "sign-contract": cmd_sign_contract,
    }

    func = dispatch.get(cmd)
    if func:
        func(cmd_args)
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'srs.py help' for usage.")


if __name__ == "__main__":
    main()
