"""
幸福开瓶器 - 用户画像数据管理器
全本地 JSON 存储，负责画像的读取、写入、置信度更新。

数据目录：~/.marvis/xingfu-kaipingqi/
跨平台兼容 Windows/macOS/Linux，与 Skill 安装目录解耦，Skill 更新不会覆盖用户数据。
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 用户数据根目录（跨平台，与 Skill 包安装位置无关）
DATA_DIR = Path.home() / ".marvis" / "xingfu-kaipingqi"
PROFILE_FILE = str(DATA_DIR / "user_profile.json")
TARGETS_FILE = str(DATA_DIR / "target_profiles.json")
ANNIVERSARIES_FILE = str(DATA_DIR / "anniversaries.json")
MOOD_LOG_FILE = str(DATA_DIR / "mood_log.json")
SUGGESTION_LOG_FILE = str(DATA_DIR / "suggestion_log.json")

os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath, default=None):
    """安全加载 JSON，不存在则返回默认值。"""
    if default is None:
        default = {}
    if not os.path.exists(filepath):
        return default
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 用户画像维度默认值 ──

DEFAULT_PROFILE = {
    "constellation": None,        # 星座
    "zodiac": None,               # 生肖
    "self_evaluation": [],         # 自我评价关键词
    "weight_goal": None,           # 减脂/增肌/塑形/无
    "carb_control": None,          # 严控/宽松/不控
    "calorie_tracking": None,      # 经常/偶尔/从不
    "consumption_tier": None,      # 仅内部匹配，不对外输出
    "taste_prefs": [],             # 口味偏好
    "frequent_areas": [],          # 常去区域
    "commute_mode": None,          # 工作日早高峰/加班晚归/假期前夕/旅行中
    "relationship_stage": None,    # 追求中/热恋期/蜜月期/稳定期
    "relationship_stage_since": None,  # ISO日期
    "family_relations": {},        # {member_id: {harmony, type, tags}}
    "mood_keywords": [],           # 近期情绪关键词
    "work_pressure": None,         # 低/中/高
    "work_achievements": [],       # 近期成就事件
    "financial_mentioned": False,  # 用户是否主动提起过财务话题
    "financial_savings": None,     # 有计划存/随缘/月光
    "financial_risk": None,        # 保守/稳健/进取
    "financial_anxiety": [],       # 财务焦虑点
    "custom_dimensions": {},       # 自定义维度 {name: {value, confidence}}
}

DEFAULT_TARGET_PROFILE = {
    "name": "",
    "relation_type": None,      # 追求对象/恋爱对象/父母/小朋友/其他
    "stage": None,              # 刚认识/暧昧期/即将表白 或 热恋期/蜜月期/稳定期 等
    "personality": [],
    "interests": [],
    "recent_mood": None,
    "recent_topics": [],
    "triggers": [],             # 矛盾触发点（仅恋爱对象）
    "health_notes": [],         # 健康状况（父母）
    "communication_style": None,  # 说教型/朋友型/沉默型（父母）
    "age_group": None,          # 幼儿/小学/初中+（小朋友）
    "harmony_level": None,      # 亲密/一般/紧张（家庭关系）
    "birthday": None,           # ISO日期
    "custom_tags": [],
}

DEFAULT_ANNIVERSARY = {
    "date": None,               # ISO日期
    "type": None,               # 恋爱纪念日/生日/节假日
    "target_id": None,          # 关联的目标对象ID，节假日可为None
    "label": "",                # 用户可读标签
    "reminder_days": 7,         # 提前多少天提醒
}


# ── 公开 API ──

def get_profile() -> dict:
    """获取当前用户画像。"""
    profile = _load_json(PROFILE_FILE, DEFAULT_PROFILE)
    return profile


def update_profile(dimension: str, value, confidence: str = "low") -> dict:
    """更新单个画像维度，自动管理置信度。

    Args:
        dimension: 维度名称
        value: 新值。列表类型会追加合并去重；其他类型直接覆盖。
        confidence: low/medium/high，默认 low
    """
    profile = get_profile()

    if dimension not in profile:
        # 自定义维度
        profile.setdefault("custom_dimensions", {})[dimension] = {
            "value": value,
            "confidence": confidence,
            "updated_at": datetime.now().isoformat()
        }
    else:
        existing = profile[dimension]
        if isinstance(existing, list):
            if isinstance(value, list):
                for v in value:
                    if v not in existing:
                        existing.append(v)
            else:
                if value not in existing:
                    existing.append(value)
        else:
            profile[dimension] = value

    profile["_last_updated"] = datetime.now().isoformat()
    _save_json(PROFILE_FILE, profile)
    return profile


def update_confidence(dimension: str, delta: int = 1) -> dict:
    """调整维度置信度（出现次数越多，置信度越高）。
    置信度升级路径：1次=low, 3次+=medium, 5次+=high

    置信度存储在 meta 字段中，格式：_confidence:{dimension}: int
    """
    profile = get_profile()
    meta_key = f"_confidence:{dimension}"
    current = profile.get(meta_key, 0)
    profile[meta_key] = current + delta
    profile["_last_updated"] = datetime.now().isoformat()
    _save_json(PROFILE_FILE, profile)
    return profile


def get_confidence(dimension: str) -> str:
    profile = get_profile()
    count = profile.get(f"_confidence:{dimension}", 0)
    if count >= 5:
        return "high"
    elif count >= 3:
        return "medium"
    return "low"


def get_high_confidence_dimensions() -> list:
    """返回所有高置信度维度名称，用于高星级推荐匹配。"""
    profile = get_profile()
    high = []
    for key in profile:
        if key.startswith("_confidence:") and profile[key] >= 5:
            dim_name = key.replace("_confidence:", "")
            if profile.get(dim_name):
                high.append(dim_name)
    return high


# ── 目标对象画像 ──

def get_all_targets() -> dict:
    return _load_json(TARGETS_FILE, {})


def get_target(target_id: str) -> dict:
    targets = get_all_targets()
    return targets.get(target_id)


def create_target(target_id: str, name: str, relation_type: str, stage: str = None) -> dict:
    targets = get_all_targets()
    profile = dict(DEFAULT_TARGET_PROFILE)
    profile["name"] = name
    profile["relation_type"] = relation_type
    profile["stage"] = stage
    profile["created_at"] = datetime.now().isoformat()
    targets[target_id] = profile
    _save_json(TARGETS_FILE, targets)
    return profile


def update_target(target_id: str, updates: dict) -> dict:
    targets = get_all_targets()
    if target_id not in targets:
        targets[target_id] = dict(DEFAULT_TARGET_PROFILE)
    for k, v in updates.items():
        if isinstance(targets[target_id].get(k), list) and isinstance(v, list):
            for item in v:
                if item not in targets[target_id][k]:
                    targets[target_id][k].append(item)
        elif isinstance(targets[target_id].get(k), list) and not isinstance(v, list):
            if v not in targets[target_id][k]:
                targets[target_id][k].append(v)
        else:
            targets[target_id][k] = v
    targets[target_id]["updated_at"] = datetime.now().isoformat()
    _save_json(TARGETS_FILE, targets)
    return targets[target_id]


# ── 纪念日/节假日 ──

def get_all_anniversaries() -> list:
    return _load_json(ANNIVERSARIES_FILE, [])


def add_anniversary(date: str, label: str, ann_type: str, target_id: str = None, reminder_days: int = 7):
    anniversaries = get_all_anniversaries()
    ann = dict(DEFAULT_ANNIVERSARY)
    ann["date"] = date
    ann["label"] = label
    ann["type"] = ann_type
    ann["target_id"] = target_id
    ann["reminder_days"] = reminder_days
    anniversaries.append(ann)
    _save_json(ANNIVERSARIES_FILE, anniversaries)


def get_upcoming_anniversaries(days_ahead: int = 14) -> list:
    """返回未来 N 天内的纪念日/节假日。"""
    anniversaries = get_all_anniversaries()
    today = datetime.now().date()
    cutoff = today + timedelta(days=days_ahead)
    upcoming = []
    for ann in anniversaries:
        if not ann.get("date"):
            continue
        try:
            ann_date = datetime.fromisoformat(ann["date"]).date()
            # 只看月-日匹配（周年性质）
            ann_date_this_year = ann_date.replace(year=today.year)
            if ann_date_this_year < today:
                ann_date_this_year = ann_date.replace(year=today.year + 1)
            if today <= ann_date_this_year <= cutoff:
                upcoming.append(ann)
        except (ValueError, TypeError):
            continue
    return upcoming


# ── 情绪日志 ──

def log_mood(keyword: str, sentiment: str = "neutral"):
    """记录一条情绪关键词。sentiment: positive/negative/neutral"""
    moods = _load_json(MOOD_LOG_FILE, [])
    moods.append({
        "keyword": keyword,
        "sentiment": sentiment,
        "timestamp": datetime.now().isoformat()
    })
    _save_json(MOOD_LOG_FILE, moods)


def get_recent_moods(days: int = 30) -> dict:
    """获取最近 N 天情绪统计。返回 {positive: N, negative: N, neutral: N, trend: ...}"""
    moods = _load_json(MOOD_LOG_FILE, [])
    cutoff = datetime.now() - timedelta(days=days)
    recent = [m for m in moods if datetime.fromisoformat(m["timestamp"]) >= cutoff]
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for m in recent:
        counts[m.get("sentiment", "neutral")] = counts.get(m.get("sentiment", "neutral"), 0) + 1
    total = sum(counts.values())
    if total == 0:
        trend = "无数据"
    else:
        positivity_ratio = counts["positive"] / total
        if positivity_ratio > 0.6:
            trend = "上升"
        elif positivity_ratio < 0.3:
            trend = "下降"
        else:
            trend = "平稳"
    counts["trend"] = trend
    counts["total"] = total
    return counts


# ── 建议日志 ──

def log_suggestion(content: str, stars: int, dimension: str = None, accepted: bool = None):
    log = _load_json(SUGGESTION_LOG_FILE, [])
    log.append({
        "content": content,
        "stars": stars,
        "dimension": dimension,
        "accepted": accepted,
        "timestamp": datetime.now().isoformat()
    })
    _save_json(SUGGESTION_LOG_FILE, log)


def get_suggestion_stats(days: int = 30) -> dict:
    log = _load_json(SUGGESTION_LOG_FILE, [])
    cutoff = datetime.now() - timedelta(days=days)
    recent = [s for s in log if datetime.fromisoformat(s["timestamp"]) >= cutoff]
    total = len(recent)
    if total == 0:
        return {"total": 0, "accepted": 0, "acceptance_rate": 0, "by_dimension": {}}
    accepted = sum(1 for s in recent if s.get("accepted"))
    by_dim = {}
    for s in recent:
        dim = s.get("dimension")
        if dim:
            by_dim[dim] = by_dim.get(dim, 0) + 1
    return {
        "total": total,
        "accepted": accepted,
        "acceptance_rate": round(accepted / total * 100, 1),
        "by_dimension": by_dim,
    }


# ── 建议反馈闭环 ──

def process_suggestion_feedback(dimension: str, accepted: bool):
    """建议被采纳/忽略后回写画像。
    
    采纳：对应维度置信度 +1
    忽略：不做变更
    连续 3 次同维度被跳过：降低该维度星星权重偏移 -0.1
    """
    if accepted:
        update_confidence(dimension, 1)
        return {"action": "confidence_boost", "dimension": dimension}
    
    # 检查连续忽略次数
    log = _load_json(SUGGESTION_LOG_FILE, [])
    recent_same_dim = [
        s for s in reversed(log)
        if s.get("dimension") == dimension
    ][:3]
    
    if len(recent_same_dim) == 3 and all(s.get("accepted") is False for s in recent_same_dim):
        profile = get_profile()
        weight_key = f"_weight_suppress:{dimension}"
        profile[weight_key] = profile.get(weight_key, 0) + 0.1
        _save_json(PROFILE_FILE, profile)
        return {"action": "weight_suppressed", "dimension": dimension, "suppression": profile[weight_key]}
    
    return {"action": "no_change"}


# ── 维度权重（人生阶段倾斜）─

# 关系阶段 → 六维度权重偏移表
STAGE_WEIGHT_MATRIX = {
    "追求期":     {"simple": 0.8, "fresh": 1.0, "romantic": 1.5, "meaningful": 1.0, "comforting": 0.9, "surprising": 1.3},
    "热恋期":     {"simple": 0.7, "fresh": 1.1, "romantic": 1.4, "meaningful": 0.9, "comforting": 1.0, "surprising": 1.2},
    "蜜月期":     {"simple": 0.6, "fresh": 1.3, "romantic": 1.6, "meaningful": 1.0, "comforting": 1.1, "surprising": 1.4},
    "稳定期":     {"simple": 1.0, "fresh": 1.2, "romantic": 0.8, "meaningful": 1.1, "comforting": 1.0, "surprising": 0.9},
    "空巢期":     {"simple": 1.2, "fresh": 1.0, "romantic": 0.7, "meaningful": 1.3, "comforting": 1.2, "surprising": 0.8},
    "单身-无目标": {"simple": 1.0, "fresh": 1.0, "romantic": 0.3, "meaningful": 1.0, "comforting": 1.0, "surprising": 1.0},
}

_WEIGHT_DEFAULTS = {"simple": 1.0, "fresh": 1.0, "romantic": 1.0, "meaningful": 1.0, "comforting": 1.0, "surprising": 1.0}


def get_dimension_weights(target_id: str = None) -> dict:
    """返回六维度的最终权重（基准 × 阶段偏移 × 抑制惩罚）。

    优先级：目标对象阶段 > 用户自身关系阶段 > 单身默认。
    """
    weights = dict(_WEIGHT_DEFAULTS)

    # 1. 获取阶段权重
    if target_id:
        target = get_target(target_id)
        stage = target.get("relationship_stage") if target else None
    else:
        profile = get_profile()
        stage = profile.get("relationship_stage")

    stage_offsets = STAGE_WEIGHT_MATRIX.get(stage, _WEIGHT_DEFAULTS)

    # 2. 叠加抑制惩罚
    profile = get_profile()
    for dim in weights:
        suppress = profile.get(f"_weight_suppress:{dim}", 0)
        weights[dim] = round(max(stage_offsets.get(dim, 1.0) - suppress, 0.1), 2)

    return weights


def compute_weighted_stars(base_stars: float, dimension: str, target_id: str = None) -> float:
    """根据维度权重重新计算星级。"""
    weights = get_dimension_weights(target_id)
    w = weights.get(dimension, 1.0)
    return round(base_stars * w, 2)


# ── 干预框架 ──

INTERVENTION_FILE = str(Path(__file__).parent / "intervention_framework.json")


def get_intervention_level(mood_keywords: list) -> dict:
    """根据情绪关键词判定绿/黄/红区，返回干预策略。
    
    返回格式：{"zone": "green|yellow|red", "rules": {...}}
    """
    framework = _load_json(INTERVENTION_FILE)
    if not framework:
        return {"zone": "green", "rules": {}}

    keywords_lower = [kw.lower() for kw in mood_keywords]
    
    # 按优先级检测（单向匹配：触发器必须包含在关键词中，防止"抑郁"被"重度抑郁"反向命中红区）
    for zone in ["red_zone", "yellow_zone"]:
        triggers = [t.lower() for t in framework[zone]["trigger_keywords"]]
        for kw in keywords_lower:
            if any(t in kw for t in triggers):
                zone_name = zone.replace("_zone", "")
                return {
                    "zone": zone_name,
                    "action": framework[zone]["action"],
                    "framework": framework[zone].get("framework"),
                    "template": framework[zone].get("output_template"),
                    "llm_forbidden": framework[zone].get("llm_forbidden", False),
                    "pool": framework[zone].get("pool"),
                    "max_llm_role": framework[zone].get("max_llm_role", "free"),
                }
    
    return {
        "zone": "green",
        "action": framework["green_zone"]["action"],
        "pool": framework["green_zone"]["pool"],
        "max_llm_role": framework["green_zone"]["max_llm_role"],
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "init":
            if not os.path.exists(PROFILE_FILE):
                _save_json(PROFILE_FILE, DEFAULT_PROFILE)
                print("Profile initialized.")
            else:
                print("Profile already exists.")
        elif cmd == "summary":
            profile = get_profile()
            stats = get_suggestion_stats(30)
            moods = get_recent_moods(30)
            anns = get_upcoming_anniversaries(14)
            data = {
                "profile_dims": sum(1 for k, v in profile.items() if v and not k.startswith("_")),
                "high_confidence_dims": len(get_high_confidence_dimensions()),
                "suggestions_30d": stats,
                "moods_30d": moods,
                "upcoming_anniversaries": len(anns),
            }
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif cmd == "get":
            print(json.dumps(get_profile(), ensure_ascii=False, indent=2))
        else:
            print("Usage: profile_manager.py [init|summary|get]")
    else:
        print("Usage: profile_manager.py [init|summary|get]")