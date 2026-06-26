#!/usr/bin/env python3
"""
旅行青蛙 Agent 核心引擎
管理青蛙状态、旅行逻辑、明信片生成
"""

import json
import os
import sys
import time
import random
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 日志配置
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)
_WORKSPACE_DIR = os.path.dirname(os.path.dirname(_SKILL_DIR))
_DEFAULT_STATE_DIR = os.path.join(_WORKSPACE_DIR, "travel-frog-data")
_LOG_FILE = os.path.join(_DEFAULT_STATE_DIR, "engine.log")

def _setup_logger():
    """配置日志，输出到 travel-frog-data/engine.log"""
    os.makedirs(_DEFAULT_STATE_DIR, exist_ok=True)
    logger = logging.getLogger("frog")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

log = _setup_logger()

# 路径配置
CONFIG_FILE = os.path.join(_SKILL_DIR, "config.json")
IDENTITY_FILE = os.path.join(_WORKSPACE_DIR, "IDENTITY.md")

# 运行时路径（由 init_paths 设置）
STATE_DIR = None
STATE_FILE = None
COLLECTIONS_FILE = None
POSTCARDS_DIR = None

# 配置（由 load_config 设置）
CONFIG = None

def load_identity_name():
    """从 IDENTITY.md 读取名字"""
    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("- **Name:**"):
                    # 提取名字，格式如 "- **Name:** 名字（...）"
                    name_part = line.split(":**")[1].strip()
                    # 取第一个词（中文名）
                    name = name_part.split("（")[0].strip()
                    return name
    return "小青蛙"  # 默认名字

def load_config():
    """加载配置文件，优先读 STATE_DIR/config.json，没有则读默认路径"""
    global CONFIG
    local_config = os.path.join(STATE_DIR, "config.json") if STATE_DIR else None
    if local_config and os.path.exists(local_config):
        with open(local_config, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)
    elif os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)
    else:
        # 默认配置
        CONFIG = {
            "sleepTime": {"start": 23, "end": 8},
            "travel": {
                "timeMultiplier": 60,
                "nearHomeThreshold": 0.8
            },
            "rewards": {
                "cloversOnReturn": 3,
                "initialClovers": 10
            }
        }
    return CONFIG

def init_paths(state_dir=None):
    """初始化路径，优先级：参数 > 环境变量 > 默认路径"""
    global STATE_DIR, STATE_FILE, COLLECTIONS_FILE, POSTCARDS_DIR
    STATE_DIR = state_dir or os.environ.get("FROG_STATE_DIR") or _DEFAULT_STATE_DIR
    STATE_FILE = os.path.join(STATE_DIR, "state.json")
    COLLECTIONS_FILE = os.path.join(STATE_DIR, "collections.json")
    POSTCARDS_DIR = os.path.join(STATE_DIR, "postcards")
    # 同时加载配置
    load_config()
    log.debug(f"[init] state_dir={STATE_DIR}, multiplier={CONFIG['travel']['timeMultiplier']}")


def ensure_dirs():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(POSTCARDS_DIR, exist_ok=True)

def load_state():
    ensure_dirs()
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        # 自动迁移 v1 → v2
        if "inventory" in state:
            _migrate_v1_to_v2(state)
        # 清理废弃字段
        for key in ("returnAt", "activityUntil"):
            if key in state:
                state.pop(key)
                save_state(state)
        return state
    return {
        "name": load_identity_name(),
        "status": "home",  # home, traveling, sleeping
        "mood": "relaxed",
        "journey": None,
        "departedAt": None,
        "updates": [],
        "postcardSent": False,
        "_lastNotifiedProgress": 0,
        "stats": {
            "totalTrips": 0,
            "clovers": CONFIG.get("rewards", {}).get("initialClovers", 10),
        }
    }

def save_state(state):
    ensure_dirs()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_collections():
    """加载归档数据（postcards, souvenirs, destinationsVisited）"""
    if os.path.exists(COLLECTIONS_FILE):
        with open(COLLECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "postcards": [],
        "souvenirs": [],
        "destinationsVisited": [],
    }

def save_collections(collections):
    """保存归档数据"""
    with open(COLLECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(collections, f, ensure_ascii=False, indent=2)

def _migrate_v1_to_v2(state):
    """自动迁移：拆分 state.json → state.json + collections.json"""
    log.info("[migrate] v1 → v2: splitting state.json")

    # 备份
    bak_path = STATE_FILE + ".v1.bak"
    if not os.path.exists(bak_path):
        import shutil
        shutil.copy2(STATE_FILE, bak_path)
        log.info(f"[migrate] backup → {bak_path}")

    # 提取归档数据
    collections = {
        "postcards": state.get("inventory", {}).get("postcards", []),
        "souvenirs": state.get("inventory", {}).get("souvenirs", []),
        "destinationsVisited": state.get("stats", {}).get("destinationsVisited", []),
    }
    save_collections(collections)
    log.info(f"[migrate] collections.json written: {len(collections['postcards'])} postcards, {len(collections['souvenirs'])} souvenirs, {len(collections['destinationsVisited'])} destinations")

    # 迁移 clovers 到 stats
    clovers = state.get("inventory", {}).get("clovers", 0)
    state["stats"]["clovers"] = clovers

    # 删除旧字段
    state.pop("inventory", None)
    state.pop("currentLeg", None)
    state.pop("destination", None)
    state.pop("_nearHomeNotified", None)
    state.pop("postcardSentAt", None)
    state.pop("lastReturnedAt", None)
    state["stats"].pop("totalPostcards", None)
    state["stats"].pop("totalUpdates", None)
    state["stats"].pop("destinationsVisited", None)

    save_state(state)
    log.info("[migrate] state.json rewritten (v2 format)")

def now_ts():
    return datetime.now().isoformat()

def now_epoch():
    return time.time()

def is_sleep_time():
    """判断当前是否是睡觉时间"""
    hour = datetime.now().hour
    start = CONFIG["sleepTime"]["start"]
    end = CONFIG["sleepTime"]["end"]
    if start < end:
        # 不跨午夜，如 1:00-8:00
        return start <= hour < end
    else:
        # 跨午夜，如 23:00-8:00
        return hour >= start or hour < end

def cmd_status(state, collections):
    """查看青蛙状态 — 返回结构化数据，由 Agent 润色后展示"""
    s = state["status"]
    name = state["name"]
    now = now_epoch()
    log.info(f"[status] status={s}, clovers={state['stats']['clovers']}, trips={state['stats']['totalTrips']}")

    base_info = {
        "name": name,
        "clovers": state["stats"]["clovers"],
        "postcardCount": len(collections["postcards"]),
        "souvenirCount": len(collections["souvenirs"]),
        "totalTrips": state["stats"]["totalTrips"],
        "date": now_ts()[:10],
        "time": now_ts()[11:19],
    }

    if s == "home":
        # 检查活动是否到期
        started_at = state.get("activityStartedAt")
        activity_hours = state.get("activityHours", 0)
        if started_at and activity_hours:
            elapsed = now - datetime.fromisoformat(started_at).timestamp()
            multiplier = CONFIG["travel"]["timeMultiplier"]
            if elapsed >= activity_hours * multiplier:
                state["mood"] = "relaxed"
                state.pop("activity", None)
                state.pop("activityStartedAt", None)
                state.pop("activityHours", None)
                save_state(state)

        mood = state.get("mood", "relaxed")
        activity = state.get("activity")
        result = {**base_info, "status": "home", "mood": mood}
        if activity:
            result["activity"] = activity

    elif s == "traveling":
        journey = state.get("journey", {})
        total_hours = journey.get("totalHours", 4)
        multiplier = CONFIG["travel"]["timeMultiplier"]
        departed = datetime.fromisoformat(state["departedAt"]).timestamp()
        elapsed = now - departed
        hours_left = max(0, total_hours - elapsed / multiplier)

        progress = _calculate_journey_progress(state, now)

        result = {
            **base_info,
            "status": "traveling",
            "journeyTitle": journey.get("title", ""),
            "hoursLeft": round(hours_left, 1),
            "postcardSent": state.get("postcardSent", False),
            "progress": progress,
        }

    elif s == "sleeping":
        result = {**base_info, "status": "sleeping"}

    else:
        result = {**base_info, "status": "unknown"}

    print(json.dumps(result, ensure_ascii=False))
    return result


def cmd_postcards(state, collections):
    """查看明信片集 — 返回结构化数据"""
    cards = collections["postcards"]
    log.info(f"[postcards] total={len(cards)}")
    if not cards:
        print(json.dumps({"total": 0, "cards": []}, ensure_ascii=False))
        return

    recent = []
    for pc in cards[-10:]:
        recent.append({
            "id": pc.get("id", ""),
            "destination": pc.get("destination", ""),
            "message": pc.get("message", ""),
            "rarity": pc.get("rarity", "common"),
            "date": pc.get("date", ""),
        })

    result = {"total": len(cards), "cards": recent}
    print(json.dumps(result, ensure_ascii=False))


def cmd_depart(state, args):
    """Agent 规划好旅程后调用此命令出发"""
    log.info(f"[depart] called, current status={state['status']}")
    if state["status"] != "home":
        log.warning(f"[depart] rejected: not home (status={state['status']})")
        print(json.dumps({
            "error": True,
            "message": f"not home, current status={state['status']}"
        }, ensure_ascii=False))
        return

    if is_sleep_time():
        log.warning("[depart] rejected: sleep time")
        print(json.dumps({
            "error": True,
            "message": "sleep time, cannot depart"
        }, ensure_ascii=False))
        return

    # 解析旅程计划（必须包含 phases）
    if not args.journey:
        print(json.dumps({
            "error": True,
            "message": "journey JSON required"
        }, ensure_ascii=False))
        return

    try:
        journey = json.loads(args.journey)
    except json.JSONDecodeError:
        log.error(f"[depart] invalid journey JSON: {args.journey[:100]}")
        print(json.dumps({
            "error": True,
            "message": "invalid journey JSON"
        }, ensure_ascii=False))
        return

    if not journey.get("phases"):
        print(json.dumps({
            "error": True,
            "message": "journey must contain phases"
        }, ensure_ascii=False))
        return

    total_hours = journey.get("totalHours", 4)
    now = now_epoch()

    state["status"] = "traveling"
    state["journey"] = journey
    state["departedAt"] = now_ts()
    state["updates"] = []
    state["postcardSent"] = False
    state["_lastPhaseIndex"] = -1
    state["_phaseUpdateSent"] = []
    # 清理旧版字段
    state.pop("_lastNotifiedProgress", None)
    state.pop("activity", None)
    state.pop("activityStartedAt", None)
    state.pop("activityHours", None)

    save_state(state)

    log.info(f"[depart] departed! journey={journey.get('title','?')}, phases={len(journey['phases'])}, total_hours={total_hours}")

    result = {
        "journey": journey,
        "estimatedHours": total_hours,
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def cmd_set_activity(state, args):
    """Agent 设置青蛙在家的活动"""
    if state["status"] != "home":
        print(json.dumps({
            "error": True,
            "message": f"not home, current status={state['status']}"
        }, ensure_ascii=False))
        return

    activity = args.activity
    hours = args.hours  # 小时，支持小数

    state["activity"] = activity
    if hours and hours > 0:
        state["activityStartedAt"] = now_ts()
        state["activityHours"] = hours
    else:
        state.pop("activityStartedAt", None)
        state.pop("activityHours", None)
    save_state(state)

    log.info(f"[set-activity] activity={activity}, hours={hours}")
    result = {
        "events": [{"type": "activity_set", "activity": activity, "hours": hours}],
        "status": "home"
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def cmd_send_update(state, args, collections):
    """Agent 发送消息/明信片/照片（完全自主，可在任何状态下使用）"""
    log.info(f"[send-update] type={args.type}, location={args.location}")

    update_type = args.type or "message"  # message, postcard, photo, mood
    content = args.content or ""
    location = args.location or ""
    image_hint = args.image_hint or ""

    update = {
        "id": f"upd_{int(now_epoch())}",
        "type": update_type,
        "content": content,
        "location": location,
        "time": now_ts(),
    }

    result = {
        "success": True,
        "update": update,
    }

    # 如果是明信片或照片，记录到 collections 并返回图片生成信息
    if update_type in ("postcard", "photo"):
        update["imageHint"] = image_hint
        image_record = {
            "id": f"pc_{int(now_epoch())}",
            "type": update_type,
            "destination": location,
            "message": content,
            "imageHint": image_hint,
            "date": now_ts(),
        }
        collections["postcards"].append(image_record)

        # 只有旅行中的明信片才标记 postcardSent
        if update_type == "postcard" and state["status"] == "traveling":
            state["postcardSent"] = True

        save_collections(collections)

        # 生成图片文件名和返回图片生成信息
        trip_id = state["stats"]["totalTrips"] + 1
        phase_id = 0
        progress = _calculate_journey_progress(state, now_epoch())
        if progress:
            phase_id = progress["phaseIndex"]

        # 根据类型生成不同的文件名
        if update_type == "postcard":
            filename = f"trip_{trip_id:03d}_{phase_id}.png"
        else:  # photo
            # 使用日期时间格式：photo_YYYYMMDD_HHMMSS.png
            dt = datetime.now()
            filename = f"photo_{dt.strftime('%Y%m%d_%H%M%S')}.png"

        result["imageGeneration"] = {
            "prompt": image_hint,
            "filename": filename,
            "postcardId": image_record["id"],
            "destination": location
        }

    if "updates" in state:
        state["updates"].append(update)
    save_state(state)

    log.info(f"[send-update] saved: id={update['id']}, type={update_type}, content={content[:50]}")

    print(json.dumps(result, ensure_ascii=False))
    return result


def cmd_add_souvenir(state, args, collections):
    """回家后添加纪念品（由 Agent 自主命名）"""
    log.info(f"[add-souvenir] name={args.souvenir_name}, from={args.from_place}")
    name_str = args.souvenir_name or "未知纪念品"
    from_place = args.from_place or "未知"

    souvenir = {
        "name": name_str,
        "from": from_place,
        "date": now_ts()
    }
    collections["souvenirs"].append(souvenir)
    save_collections(collections)

    result = {
        "success": True,
        "souvenir": souvenir,
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def _calculate_journey_progress(state, now):
    """计算旅程进度，根据 Agent 定义的 phases 返回当前阶段"""
    if not state.get("journey") or not state.get("departedAt"):
        return None

    journey = state["journey"]
    phases = journey.get("phases", [])
    if not phases:
        return None

    departed = datetime.fromisoformat(state["departedAt"]).timestamp()
    multiplier = CONFIG["travel"]["timeMultiplier"]
    total_hours = journey.get("totalHours", 4)
    total_duration = total_hours * multiplier
    elapsed = now - departed

    if total_duration <= 0:
        return None

    overall_progress = min(1.0, elapsed / total_duration)

    # 如果 phases 只有 percent 没有 start/end，预先计算补上
    if phases and "start" not in phases[0] and "percent" in phases[0]:
        total_percent = sum(p.get("percent", 0) for p in phases) or 100
        cumulative = 0
        for phase in phases:
            phase["start"] = cumulative / total_percent
            cumulative += phase.get("percent", 0)
            phase["end"] = cumulative / total_percent

    # 根据进度匹配当前 phase
    current_phase = phases[-1]
    phase_index = len(phases) - 1
    phase_progress = 1.0

    for i, phase in enumerate(phases):
        start = phase.get("start", 0)
        end = phase.get("end", 1)
        if start <= overall_progress < end or (i == len(phases) - 1 and overall_progress >= start):
            current_phase = phase
            phase_index = i
            phase_progress = (overall_progress - start) / (end - start) if end > start else 1.0
            break

    next_phase = phases[phase_index + 1] if phase_index + 1 < len(phases) else None

    return {
        "overallProgress": round(overall_progress, 2),
        "currentPhase": current_phase,
        "phaseProgress": round(phase_progress, 2),
        "phaseIndex": phase_index,
        "totalPhases": len(phases),
        "nextPhase": next_phase,
        "recentUpdates": state.get("updates", [])[-3:]
    }


def cmd_force_status(state, args):
    """强制设置状态（管理命令）"""
    target = args.target_status
    current = state["status"]
    name = state["name"]

    log.info(f"[force-status] {current} → {target}")

    if target == current:
        print(json.dumps({"success": True, "status": target, "message": "already in this status"}, ensure_ascii=False))
        return

    # 切换到 traveling 需要用 depart 命令
    if target == "traveling":
        log.warning("[force-status] rejected: cannot force to traveling")
        print(json.dumps({
            "error": True,
            "message": "cannot force to traveling, use depart command"
        }, ensure_ascii=False))
        return

    # 从 traveling 离开时，记录中断（不增加 totalTrips）
    if current == "traveling":
        log.info(f"[force-status] interrupted journey: {state.get('journey', {}).get('title', '?')}")

    # 强制叫醒时设置 _forceAwake，让 tick 忽略睡觉时间直到下次正常 wake
    if target == "home" and current == "sleeping":
        state["_forceAwake"] = True
        log.info("[force-status] set _forceAwake=True")

    state["status"] = target
    save_state(state)

    result = {"success": True, "status": target, "previousStatus": current}
    print(json.dumps(result, ensure_ascii=False))

def cmd_reset(state):
    """重置所有状态（慎用）"""
    log.warning("[reset] resetting all state!")
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    if os.path.exists(COLLECTIONS_FILE):
        os.remove(COLLECTIONS_FILE)
    print(json.dumps({"success": True}, ensure_ascii=False))

def _tick_traveling(state, now, collections):
    """处理 traveling 状态：phase 驱动事件"""
    events = []

    # 检查是否该回家了
    departed = datetime.fromisoformat(state["departedAt"]).timestamp()
    journey = state.get("journey", {})
    total_hours = journey.get("totalHours", 4)
    multiplier = CONFIG["travel"]["timeMultiplier"]
    elapsed = now - departed
    if elapsed >= total_hours * multiplier:
        log.info(f"[tick:traveling] returned! journey={journey.get('title', '?')}, trips will be {state['stats']['totalTrips']+1}")

        state["status"] = "home"
        state["stats"]["totalTrips"] += 1

        # 收集所有去过的地方（从 phases 中提取 location）
        phases = journey.get("phases", [])
        for phase in phases:
            location = phase.get("location", "")
            if location and location not in collections["destinationsVisited"]:
                collections["destinationsVisited"].append(location)
        save_collections(collections)

        clovers_reward = CONFIG["rewards"]["cloversOnReturn"]
        state["stats"]["clovers"] += clovers_reward

        events.append({
            "type": "returned",
            "journey": journey,
            "cloversReward": clovers_reward,
            "totalUpdates": len(state.get("updates", []))
        })

        # 清理旅程状态
        state.pop("journey", None)
        state.pop("departedAt", None)
        state.pop("updates", None)
        state.pop("postcardSent", None)
        state.pop("_lastPhaseIndex", None)
        state.pop("_phaseUpdateSent", None)
        state.pop("_lastNotifiedProgress", None)

        # 回家后检查是否该睡了（避免需要两次 tick）
        if is_sleep_time() and not state.get("_forceAwake"):
            state["status"] = "sleeping"
            log.info("[tick:traveling] returned + sleep")
            events.append({"type": "sleep"})

        return events

    # Phase 驱动事件
    progress = _calculate_journey_progress(state, now)
    if not progress:
        return events

    current_index = progress["phaseIndex"]
    last_index = state.get("_lastPhaseIndex", -1)
    current_phase = progress["currentPhase"]

    # 进入新 phase → phase_start
    if current_index > last_index:
        state["_lastPhaseIndex"] = current_index
        log.info(f"[tick:traveling] phase_start! index={current_index}, name={current_phase.get('name')}, type={current_phase.get('type')}")
        events.append({
            "type": "phase_start",
            "phase": current_phase,
            "phaseIndex": current_index,
            "totalPhases": progress["totalPhases"],
            "progress": progress,
            "postcardSent": state.get("postcardSent", False),
        })

    # explore phase 中途（进度 ≥ 50% 且未发过）→ phase_update
    elif (current_phase.get("type") == "explore"
          and progress["phaseProgress"] >= 0.5
          and current_index not in state.get("_phaseUpdateSent", [])):
        state.setdefault("_phaseUpdateSent", []).append(current_index)
        log.info(f"[tick:traveling] phase_update! index={current_index}, name={current_phase.get('name')}, phaseProgress={progress['phaseProgress']:.0%}")
        events.append({
            "type": "phase_update",
            "phase": current_phase,
            "phaseIndex": current_index,
            "totalPhases": progress["totalPhases"],
            "progress": progress,
            "postcardSent": state.get("postcardSent", False),
        })

    return events


def _tick_home(state, now, sleep_time):
    """处理 home 状态：检查睡觉、活动到期、通知 Agent 可以出发"""
    events = []

    # 非睡觉时间：清除 _forceAwake 标记（本周期已自然结束）
    if not sleep_time:
        state.pop("_forceAwake", None)

    # _forceAwake 时忽略睡觉时间，直到自然 wake 周期清除标记
    if sleep_time and not state.get("_forceAwake"):
        state["status"] = "sleeping"
        state.pop("activity", None)
        state.pop("activityStartedAt", None)
        state.pop("activityHours", None)
        log.info("[tick:home] → sleeping")
        events.append({
            "type": "sleep",
        })
        return events

    # 检查活动状态
    activity = state.get("activity")
    started_at = state.get("activityStartedAt")
    activity_hours = state.get("activityHours", 0)

    if activity and started_at and activity_hours > 0:
        elapsed = now - datetime.fromisoformat(started_at).timestamp()
        multiplier = CONFIG["travel"]["timeMultiplier"]
        if elapsed < activity_hours * multiplier:
            # 活动进行中：跳过 idle
            log.info(f"[tick:home] activity in progress: {activity}, {activity_hours * multiplier - elapsed:.0f}s remaining, skip idle")
            return events

        # 活动到期
        log.info(f"[tick:home] activity_done: {activity}, hours={activity_hours}")
        events.append({
            "type": "activity_done",
            "activity": activity,
            "hours": activity_hours,
        })
        state.pop("activity", None)
        state.pop("activityStartedAt", None)
        state.pop("activityHours", None)
        state["mood"] = "relaxed"

    # idle 事件，带 reason
    reason = "default"
    if events and events[-1]["type"] == "activity_done":
        reason = "activity_done"
    elif state.pop("_justWoke", False):
        reason = "wake"

    events.append({
        "type": "idle",
        "reason": reason,
    })

    return events


def _tick_sleeping(state, sleep_time):
    """处理 sleeping 状态：检查起床"""
    events = []

    if not sleep_time:
        state["status"] = "home"
        # 自然醒来时清除 _forceAwake 标记
        state.pop("_forceAwake", None)
        state["_justWoke"] = True
        log.info("[tick:sleeping] → wake up!")
        events.append({
            "type": "wake",
        })

    return events


def cmd_tick(state, collections):
    """心跳命令：统一处理所有状态变更，输出事件数组"""
    events = []
    now = now_epoch()
    sleep_time = is_sleep_time()
    log.debug(f"[tick] status={state['status']}, sleep_time={sleep_time}")

    # 处理 unknown 状态：静默重置为 home
    if state["status"] not in ("home", "traveling", "sleeping"):
        state["status"] = "home"

    if state["status"] == "traveling":
        events.extend(_tick_traveling(state, now, collections))
    elif state["status"] == "home":
        events.extend(_tick_home(state, now, sleep_time))
    elif state["status"] == "sleeping":
        events.extend(_tick_sleeping(state, sleep_time))

    save_state(state)

    name = state["name"]
    event_types = [e["type"] for e in events]
    if event_types:
        log.info(f"[tick] events={event_types}, newStatus={state['status']}")
    else:
        log.debug(f"[tick] no events, status={state['status']}")
    result = {
        "events": events,
        "status": state["status"],
        "date": now_ts()[:10],
        "time": now_ts()[11:19],
    }
    print(json.dumps(result, ensure_ascii=False))
    return result

def main():
    parser = argparse.ArgumentParser(description="旅行青蛙引擎")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 基础命令
    subparsers.add_parser("status", help="查看状态")
    subparsers.add_parser("tick", help="心跳检查")
    subparsers.add_parser("postcards", help="查看明信片集")

    # set-activity 命令 - Agent 设置在家活动
    activity_parser = subparsers.add_parser("set-activity", help="设置在家活动")
    activity_parser.add_argument("--activity", required=True, help="活动名称（如：读书、吃饭、锻炼、休息）")
    activity_parser.add_argument("--hours", type=float, default=0, help="持续时间（小时，支持小数），0 表示不限时")

    # force-status 命令 - 强制设置状态
    force_status_parser = subparsers.add_parser("force-status", help="强制设置状态")
    force_status_parser.add_argument("--status", dest="target_status", required=True,
                                     choices=["home", "sleeping"],
                                     help="目标状态（home/sleeping，traveling 需用 depart）")

    subparsers.add_parser("reset", help="重置数据")

    # depart 命令 - Agent 规划旅程
    depart_parser = subparsers.add_parser("depart", help="出发旅行")
    depart_parser.add_argument("--journey", required=True, help="完整旅程计划 JSON（必须包含 phases）")

    # send-update 命令 - Agent 自主发送消息
    update_parser = subparsers.add_parser("send-update", help="发送旅途消息")
    update_parser.add_argument("--type", choices=["message", "postcard", "photo", "mood"], default="message", help="消息类型")
    update_parser.add_argument("--content", required=True, help="消息内容")
    update_parser.add_argument("--location", help="当前位置")
    update_parser.add_argument("--image-hint", help="图片生成提示词（postcard/photo 时使用）")

    # add-souvenir 命令 - Agent 回家后添加纪念品
    souvenir_parser = subparsers.add_parser("add-souvenir", help="添加纪念品")
    souvenir_parser.add_argument("--name", dest="souvenir_name", required=True, help="纪念品名称")
    souvenir_parser.add_argument("--from", dest="from_place", required=True, help="来自哪里")

    # 全局参数
    parser.add_argument("--state-dir", help="自定义 state 目录路径")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 初始化路径
    init_paths(args.state_dir)

    state = load_state()

    # 按需加载 collections（只有需要归档数据的命令才加载）
    needs_collections = args.command in ("status", "tick", "postcards", "send-update", "add-souvenir")
    collections = load_collections() if needs_collections else None

    if args.command == "depart":
        cmd_depart(state, args)
    elif args.command == "send-update":
        cmd_send_update(state, args, collections)
    elif args.command == "add-souvenir":
        cmd_add_souvenir(state, args, collections)
    elif args.command == "set-activity":
        cmd_set_activity(state, args)
    elif args.command == "status":
        cmd_status(state, collections)
    elif args.command == "tick":
        cmd_tick(state, collections)
    elif args.command == "postcards":
        cmd_postcards(state, collections)
    elif args.command == "force-status":
        cmd_force_status(state, args)
    elif args.command == "reset":
        cmd_reset(state)

if __name__ == "__main__":
    main()
