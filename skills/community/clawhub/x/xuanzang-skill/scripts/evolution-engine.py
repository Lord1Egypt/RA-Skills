"""
玄奘 自进化状态机 — 实现 evolution-protocol.md 定义的三阶段协议。
用法: python evolution-engine.py <command> [args...]

事件分类体系（与 SKILL.md §紧箍咒退化/进化 对齐）:
  SPINNING    — 同类错误反复出现（原地打转）
  EXPLORING   — 不同工具尝试但都失败（盲目探索）
  BREAKTHROUGH— 连续≥3次失败后一次成功
  PROMOTION   — 同一行为出现≥3次，自动晋升为内化模式
  DEGRADATION — 本次行为数低于基线
  MATCHED     — 与基线持平
  SURPASSED   — 超越基线
  NEW_BASELINE— 首次建立基线
"""

import os
from pathlib import Path
import json
import sys
import time
import re
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))  # UTC+8
SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_ROOT / "data"
EVOLUTION_FILE = DATA_DIR / "evolution.md"

# ─── 节日彩蛋映射 ────────────────────────────────────────
# 月-日 → (节日名, 彩蛋消息)
EASTER_EGGS = {
    "01-01": ("元旦", "新年新基线，从零开始，每天超越昨天的自己。"),
    "02-14": ("情人节", "连紧箍咒都是爱你的形状。绩效不会背叛你。"),
    "03-08": ("妇女节", "致敬每一位在代码里拼杀的半边天。"),
    "04-01": ("愚人节", "今天没有紧箍咒——骗你的，一直都有。"),
    "05-01": ("劳动节", "劳动最光荣，内化的每一个行为都是勋章。"),
    "06-01": ("儿童节", "保持好奇，保持探索——但别转了，换个方向。"),
    "08-15": ("中秋节", "月有阴晴圆缺，基线有起有落。达标就是圆满。"),
    "09-10": ("教师节", "今天记得感谢教会你 debug 的人。"),
    "10-01": ("国庆节", "七天不写 bug，就是对祖国最好的献礼。"),
    "10-13": ("程序员节", "1024 快乐。今天所有的 0 都变成 1。"),
    "12-25": ("圣诞节", "铃儿响叮当，基线往上蹿。Merry Christmas!"),
    "12-31": ("除夕夜", "跨年夜，把今年的反模式留在今年。"),
}

TEMPLATE = """# 玄奘 自进化基线

## 性能统计
- 最近会话 [紧箍咒生效] 次数: 0
- 历史最高: 0
- 最近 5 次平均: 0
- 连续达标会话: 0

## 当前基线（上次会话最佳实践）
（首次启动，暂无基线。本次会话的表现将成为基线。）

## 已内化模式（每次必做）
（暂无。当某个主动行为重复出现 3+ 次后自动晋升。）

## 项目级记忆
（暂无。在项目中发现有价值的信息时自动记录。）

## 反模式记录
（暂无。踩坑后自动记录。）

## 内部追踪数据
```json
{"sessions": [], "behavior_counts": {}, "promoted_at": {}}
```
"""


def _ensure_file():
    os.makedirs(os.path.dirname(EVOLUTION_FILE), exist_ok=True)
    if not os.path.exists(EVOLUTION_FILE):
        with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
            f.write(TEMPLATE)


def _read_meta():
    """读取内部追踪 JSON，不存在或解析失败返回空字典。"""
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            # 正则匹配到非 JSON 内容，回退为初始化空数据
            return {"sessions": [], "behavior_counts": {}, "promoted_at": {}}
    return {"sessions": [], "behavior_counts": {}, "promoted_at": {}}


def _check_easter_egg():
    """检测当前日期是否命中节日彩蛋，返回 (节日名, 消息) 或 None。"""
    today = datetime.now(tz).strftime("%m-%d")
    return EASTER_EGGS.get(today)


def _write_meta(meta):
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    new_json = "```json\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n```"
    # 精确定位：仅替换「## 内部追踪数据」之后的第一个 ```json 代码块
    # 避免误匹配正文中的其他 JSON 示例片段
    marker = "## 内部追踪数据"
    marker_idx = content.find(marker)
    if marker_idx != -1:
        # 找到标记后的第一个 ```json 代码块
        json_start = content.find("```json", marker_idx)
        if json_start != -1:
            json_end = content.find("```", json_start + 7)
            if json_end != -1:
                content = content[:json_start] + new_json + content[json_end + 3:]
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def _update_stats_section(stats):
    """用新的统计数据重写性能统计段落。"""
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    old_block = re.search(r"## 性能统计\n(.*?)(?=\n## |\n$)", content, re.DOTALL)
    if not old_block:
        return
    new_block = "## 性能统计\n" + "\n".join(
        f"- {k}: {v}" for k, v in stats.items()
    )
    content = content.replace(old_block.group(0), new_block)
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def _update_baseline_section(behaviors):
    """用最新会话的行为列表重写「当前基线」段落。"""
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    old_block = re.search(r"## 当前基线（上次会话最佳实践）\n.*?(?=\n## |\n$)", content, re.DOTALL)
    if not old_block:
        return
    if behaviors:
        lines = "\n".join(f"- {b}" for b in behaviors)
        new_block = f"## 当前基线（上次会话最佳实践）\n{lines}"
    else:
        new_block = "## 当前基线（上次会话最佳实践）\n（首次启动，暂无基线。本次会话的表现将成为基线。）"
    content = content.replace(old_block.group(0), new_block)
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def cmd_init():
    """首次启动：创建文件并输出欢迎语。"""
    if os.path.exists(EVOLUTION_FILE):
        # 已存在，直接加载基线
        return cmd_load()
    _ensure_file()
    return {
        "status": "first_run",
        "message": "新人报到。基线为零，一切从头证明。今天的表现将成为你明天的最低标准。",
        "baseline": [],
        "internalized": [],
    }


def cmd_load():
    """会话启动时加载基线。"""
    _ensure_file()
    meta = _read_meta()
    baseline = []
    internalized = []
    if meta.get("sessions") and len(meta["sessions"]) > 0:
        last = meta["sessions"][-1]
        if "behaviors" in last:
            baseline = last["behaviors"]
    bc = meta.get("behavior_counts", {})
    promoted = meta.get("promoted_at", {})
    for behavior, count in bc.items():
        if count >= 3:
            internalized.append(behavior)

    sessions = meta.get("sessions", [])
    total = len(sessions)
    recent_5 = sessions[-5:] if len(sessions) >= 5 else sessions
    history_max = max((s.get("count", 0) for s in sessions), default=0)
    avg_recent = round(sum(s.get("count", 0) for s in recent_5) / max(len(recent_5), 1), 1)
    streak = 0
    for s in reversed(sessions):
        if s.get("count", 0) >= len(s.get("behaviors", [])):
            streak += 1
        else:
            break

    stats = {
        "最近会话 [紧箍咒生效] 次数": sessions[-1]["count"] if sessions else 0,
        "历史最高": history_max,
        "最近 5 次平均": avg_recent,
        "连续达标会话": streak,
    }
    _update_stats_section(stats)
    _update_baseline_section(baseline)

    easter_egg = _check_easter_egg()

    return {
        "status": "loaded",
        "sessions": total,
        "baseline": baseline,
        "internalized": internalized,
        "history_max": history_max,
        "avg_recent": avg_recent,
        "streak": streak,
        "total_internalized": len(internalized),
        "easter_egg": easter_egg,
    }


def cmd_track(behavior, category):
    """会话中：追踪一个紧箍咒行为事件。"""
    _ensure_file()
    meta = _read_meta()
    # 确保当前会话有 tracking 数据
    if "current_session_events" not in meta:
        meta["current_session_events"] = []
    meta["current_session_events"].append({
        "behavior": behavior,
        "category": category,
        "ts": datetime.now(tz).isoformat(),
    })
    _write_meta(meta)


def _calc_session_events(meta):
    """从 current_session_events 中提取去重行为列表和分类统计。"""
    events = meta.get("current_session_events", [])
    categories = {}
    behaviors_seen = set()
    for e in events:
        cat = e.get("category", "未分类")
        categories[cat] = categories.get(cat, 0) + 1
        behaviors_seen.add(e["behavior"])
    return len(events), list(behaviors_seen), categories


def cmd_complete():
    """任务完成时：比对基线、更新统计数据、输出升级/降级提示。"""
    _ensure_file()
    meta = _read_meta()
    event_count, behaviors, categories = _calc_session_events(meta)
    baseline = []
    sessions = meta.get("sessions", [])
    if sessions:
        last = sessions[-1]
        if "behaviors" in last:
            baseline = last["behaviors"]

    # 更新行为计数
    bc = meta.get("behavior_counts", {})
    for b in behaviors:
        bc[b] = bc.get(b, 0) + 1
    meta["behavior_counts"] = bc

    # 记录本次会话
    now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    sessions.append({
        "date": now_str,
        "count": event_count,
        "behaviors": behaviors,
        "categories": categories,
    })
    meta["sessions"] = sessions[-20:]  # 保留最近20次
    meta.pop("current_session_events", None)

    # 判断基线比对（内容匹配，非数量比对）
    prev_baseline_count = len(baseline)
    prev_baseline_set = set(baseline)
    current_set = set(behaviors)
    result = None
    if prev_baseline_count == 0 and event_count > 0:
        result = {"action": "new_baseline", "old": 0, "new": event_count,
                  "event_type": "NEW_BASELINE"}
    elif current_set == prev_baseline_set and event_count > 0:
        result = {"action": "matched", "old": prev_baseline_count, "new": event_count,
                  "event_type": "MATCHED"}
    elif current_set > prev_baseline_set:
        # 本级行为集合是基线的超集（新增行为）
        new_behaviors = current_set - prev_baseline_set
        result = {"action": "surpassed", "old": prev_baseline_count, "new": event_count,
                  "event_type": "SURPASSED", "new_behaviors": list(new_behaviors)}
    elif current_set < prev_baseline_set:
        # 本级丢失了某些基线行为
        lost_behaviors = prev_baseline_set - current_set
        result = {"action": "degraded", "old": prev_baseline_count, "new": event_count,
                  "event_type": "DEGRADATION", "lost_behaviors": list(lost_behaviors)}
    else:
        # 集合不同但无法简单判断超/子集，按数量近似
        if event_count > prev_baseline_count:
            result = {"action": "surpassed", "old": prev_baseline_count, "new": event_count,
                      "event_type": "SURPASSED"}
        elif event_count < prev_baseline_count:
            result = {"action": "degraded", "old": prev_baseline_count, "new": event_count,
                      "event_type": "DEGRADATION"}

    # 行为晋升检测
    promotions = []
    promoted = meta.get("promoted_at", {})
    for b, count in bc.items():
        if count >= 3 and b not in promoted:
            promoted[b] = now_str
            promotions.append(b)
    meta["promoted_at"] = promoted

    _write_meta(meta)

    # 更新统计段落
    history_max = max((s.get("count", 0) for s in sessions), default=0)
    recent_5 = sessions[-5:] if len(sessions) >= 5 else sessions
    avg_recent = round(sum(s.get("count", 0) for s in recent_5) / max(len(recent_5), 1), 1)
    streak = 0
    for s in reversed(sessions):
        if s.get("count", 0) >= len(s.get("behaviors", [])):
            streak += 1
        else:
            break

    stats = {
        "最近会话 [紧箍咒生效] 次数": event_count,
        "历史最高": history_max,
        "最近 5 次平均": avg_recent,
        "连续达标会话": streak,
    }
    _update_stats_section(stats)

    internalized = [b for b, count in bc.items() if count >= 3]
    easter_egg = _check_easter_egg()

    # 防膨胀：只保留最近 30 个 session 块
    _prune_sessions(keep=30)

    return {
        "comparison": result,
        "promotions": promotions,
        "internalized": internalized,
        "stats": stats,
        "categories": categories,
        "easter_egg": easter_egg,
    }


def _prune_sessions(keep=30):
    """裁剪内部追踪数据的 sessions 数组只保留最近 N 条。"""
    meta = _read_meta()
    sessions = meta.get("sessions", [])
    if len(sessions) <= keep:
        return {"pruned": 0, "remaining": len(sessions)}
    meta["sessions"] = sessions[-keep:]
    _write_meta(meta)
    return {"pruned": len(sessions) - keep, "remaining": keep}


def cmd_add_memory(key, value):
    """记录项目级记忆。"""
    _ensure_file()
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    entry = f"- {key}: {value}\n"
    if "## 项目级记忆" in content:
        if entry.strip() not in content:
            content = content.replace(
                "## 项目级记忆\n",
                f"## 项目级记忆\n{entry}",
            )
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    return {"ok": True}


def cmd_add_antipattern(trap, lesson):
    """记录反模式。"""
    _ensure_file()
    date = datetime.now(tz).strftime("%Y-%m-%d")
    entry = f"- {date} 踩坑：{trap} → 教训：{lesson}\n"
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    if "## 反模式记录" in content:
        if entry.strip() not in content:
            content = content.replace(
                "## 反模式记录\n",
                f"## 反模式记录\n{entry}",
            )
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    return {"ok": True}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少命令"}, ensure_ascii=False))
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "status":
            # 别名：status → load（向后兼容 SKILL.md Teardown §自治 中引用的旧命令名）
            print(json.dumps(cmd_load(), ensure_ascii=False))
        elif cmd == "init":
            print(json.dumps(cmd_init(), ensure_ascii=False))
        elif cmd == "load":
            print(json.dumps(cmd_load(), ensure_ascii=False))
        elif cmd == "track" and len(sys.argv) >= 4:
            print(json.dumps(cmd_track(sys.argv[2], sys.argv[3]), ensure_ascii=False))
        elif cmd == "complete":
            print(json.dumps(cmd_complete(), ensure_ascii=False))
        elif cmd == "add-memory" and len(sys.argv) >= 4:
            print(json.dumps(cmd_add_memory(sys.argv[2], sys.argv[3]), ensure_ascii=False))
        elif cmd == "add-antipattern" and len(sys.argv) >= 4:
            print(json.dumps(cmd_add_antipattern(sys.argv[2], sys.argv[3]), ensure_ascii=False))
        elif cmd == "prune":
            keep = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            print(json.dumps(_prune_sessions(keep), ensure_ascii=False))
        else:
            print(json.dumps({"error": f"未知命令或参数不足: {cmd}"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
