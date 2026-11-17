# -*- coding: utf-8 -*-
"""logic_validators：逻辑漏洞校验器（语言无关、确定性、零第三方依赖）。

与引擎解耦，便于后续合并进引擎内核。当前四个校验器：
  audit_spacetime_contradiction  同角色同一时间出现在两地
  audit_state_contradiction       死而复生 / 同一时间标记下互斥状态并存
  audit_timeline_regression       同角色时间标记倒退
  audit_foreshadow_gap            伏笔埋下未回收

四个校验器都遵循「宁缺毋滥」：坐标缺失即跳过，不臆造。
"""
import re
from typing import Any, Dict, List

from extraction.schema import EventNode, STATE_EXCLUSIVE_GROUPS


def _key(n: EventNode):
    return (n.character, n.time, n.place)


def audit_spacetime_contradiction(nodes: List[EventNode]) -> Dict[str, Any]:
    """同角色同一时间出现在两个地点。缺 time 或 place 者不参与。

    同章约束：「一日」「三月盡」等时间标记的基准是章，跨章同名标记
    （如两章都出现「一日」）不构成同时异地，故只比较同章节点。
    """
    seen: Dict[tuple, EventNode] = {}
    conflicts = []
    reported = set()  # 同一 (角色,时间,章,地点对) 只报一次
    for n in nodes:
        if not n.character or not n.time or not n.place or _chapter(n) is None:
            continue
        k = (n.character, n.time, _chapter(n))
        if k in seen and seen[k].place != n.place:
            pair_key = k + (frozenset([seen[k].place, n.place]),)
            if pair_key not in reported:
                reported.add(pair_key)
                conflicts.append({
                    "type": "spacetime",
                    "character": n.character,
                    "time": n.time,
                    "places": [seen[k].place, n.place],
                    "sources": [seen[k].source, n.source],
                    "detail": "%s 于 %s 同时出现在 [%s] 与 [%s]" % (
                        n.character, n.time, seen[k].place, n.place),
                })
        else:
            seen[k] = n
    return {"passed": not conflicts, "conflicts": conflicts,
            "checked": len(seen),
            "note": "同角色同章同一时间异地；缺 time/place 或跨章不参与"}


def audit_state_contradiction(nodes: List[EventNode]) -> Dict[str, Any]:
    """同角色状态矛盾，分两类判定（宁缺毋滥，缺 state 不参与）：

      1) 时序异常（按**行文顺序**）：死 → 生。生→死是死亡叙事，属常态，不判。
         还魂/鬼魂显灵文本会误触该规则，故每条发现必带原文定位供人工复核。
      2) 同时互斥（同章 + 同一时间标记）：互斥组内两种状态并存。
         在→离、囚→自由、伤→愈等跨时间演进是正常叙事，不判。

    行文顺序取节点在输入列表中的先后（抽取层须按阅读顺序产出），
    不用 time 字符串排序——古典时间标记（一日/三日）跨章不可比。
    """
    by_char: Dict[str, List[EventNode]] = {}
    for n in nodes:
        if n.character and n.state:
            by_char.setdefault(n.character, []).append(n)
    conflicts = []
    for ch, ns in by_char.items():
        last_dead = None
        for n in ns:
            if n.state == "死":
                last_dead = n
            elif last_dead is not None and n.state == "生":
                conflicts.append({
                    "type": "state",
                    "character": ch,
                    "from_state": "死", "to_state": "生",
                    "sources": [last_dead.source, n.source],
                    "detail": "%s 已于前文标记死亡（%s），此处又以生者行事" % (
                        ch, last_dead.source),
                })
                last_dead = None  # 同一死亡事件只报一次，避免连锁误报
        by_key: Dict[tuple, List[EventNode]] = {}
        reported_sim = set()
        for n in ns:
            if not n.time or _chapter(n) is None:
                continue
            k = (n.time, _chapter(n))
            for m in by_key.setdefault(k, []):
                for grp in STATE_EXCLUSIVE_GROUPS:
                    if n.state in grp and m.state in grp and n.state != m.state:
                        pair_key = (ch, n.time, _chapter(n),
                                    frozenset([m.state, n.state]))
                        if pair_key not in reported_sim:
                            reported_sim.add(pair_key)
                            conflicts.append({
                                "type": "state",
                                "character": ch,
                                "from_state": m.state, "to_state": n.state,
                                "times": [m.time, n.time],
                                "sources": [m.source, n.source],
                                "detail": "%s 于 %s 同时标记为互斥的 [%s] 与 [%s]" % (
                                    ch, n.time, m.state, n.state),
                            })
                        break
            by_key[k].append(n)
    return {"passed": not conflicts, "conflicts": conflicts,
            "checked": sum(len(v) for v in by_char.values()),
            "note": "时序异常=死而复生（行文顺序）；同时互斥=同章同时间标记；生→死不判"}


# 状态异常的方向语义（按行文顺序判定）：
#   生→死：死亡叙事，常态，不判；
#   死→生：死而复生，异常（还魂/鬼魂显灵文本会误触，故发现必带原文定位供复核）；
#   在/离、囚/自由、伤/愈：双向均为常态演进，只有同一时间标记下并存才算互斥。
STATE_ANOMALY_TRANSITIONS = (("死", "生"),)


_CN_DIGIT = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
              "六": 6, "七": 7, "八": 8, "九": 9}
# 章号：从 source 的「第N回」前缀解析；无章号返回 None
_CHAPTER_RE = re.compile(r"第\s*([0-9零一二三四五六七八九十百]+)\s*回")


def _cn2int(s: str):
    """中文数字串 → int，支持 十/百 组合（十二=12、二十=20、一百二十=120）。"""
    if not s:
        return None
    if s.isdigit():
        return int(s)
    section, seen = 0, False
    for c in s:
        if c in _CN_DIGIT:
            section = _CN_DIGIT[c]
            seen = True
        elif c == "十":
            section = (section or 1) * 10
            seen = True
        elif c == "百":
            section = (section or 1) * 100
            seen = True
        elif c == "零":
            continue
        else:
            return None
    return section if seen else None


def _chapter(n: EventNode):
    m = _CHAPTER_RE.search(n.source or "")
    if not m:
        return None
    return _cn2int(m.group(1))


def _num(t: str):
    """时间标记取数值：支持阿拉伯数字与中文数字（古典小说用中文数字）。"""
    m = re.search(r"(\d+)", t or "")
    if m:
        return int(m.group(1))
    m = re.search(r"([一二三四五六七八九十])", t or "")
    if m:
        return _CN_DIGIT.get(m.group(1))
    return None


def _is_relative_time(t: str) -> bool:
    """相对时间标记（一日/三日/五六日/前月…）：只在同章内有可比性。"""
    return bool(re.match(r"^(前月|今經|明日|次日|那一日|一日|几日|[一二三四五六七八九十]{1,3}\s*[日])", t or ""))


def audit_timeline_regression(nodes: List[EventNode]) -> Dict[str, Any]:
    """同角色时间标记倒退：按原文顺序，后一事件的数字时间早于前一事件。

    两条约束（修误报后加入）：
      1) 只解析数字时间；不可解析者跳过；
      2) 只在**同一章内**比较——「一日」「三日」是章内相对时间，跨章基准不同，
         跨章比较会把正常叙事当倒退。
    """
    by_char: Dict[str, List[tuple]] = {}
    for idx, n in enumerate(nodes):
        if n.character and _num(n.time) is not None and not _is_relative_time(n.time):
            by_char.setdefault(n.character, []).append((idx, n))
    conflicts = []
    reported = set()
    for ch, items in by_char.items():
        for i in range(len(items) - 1):
            a, b = items[i][1], items[i + 1][1]
            if _chapter(a) != _chapter(b):
                continue  # 跨章不比较
            if _num(a.time) > _num(b.time):
                key = (ch, _chapter(a), a.time, b.time)
                if key not in reported:
                    reported.add(key)
                    conflicts.append({
                        "type": "timeline",
                        "character": ch,
                        "times": [a.time, b.time],
                        "sources": [a.source, b.source],
                        "detail": "%s 时间标记倒退：后文 [%s] 早于前文 [%s]" % (
                            ch, b.time, a.time),
                    })
    return {"passed": not conflicts, "conflicts": conflicts,
            "checked": sum(len(v) for v in by_char.values()),
            "note": "同角色时间标记按原文顺序倒退；同章内比较；相对时间与跨章跳过"}


def audit_foreshadow_gap(mod, nodes: List[EventNode]) -> Dict[str, Any]:
    """伏笔台账：已 SET 未 PAY 的主题。

    直接使用节点的 foreshadow/topic 字段构造台账记录——不走引擎
    ForeshadowLedger.scan_nodes 的文本关键词检测，否则会用 _detect 的
    结果覆盖调用方预设的 SET/PAY 标记（那是为散文文本设计的路径）。
    """
    ledger = mod.ForeshadowLedger()
    for i, n in enumerate(nodes):
        if not n.foreshadow:
            continue
        topic = n.topic or n.action[:12]
        ledger.records.append({"node_id": str(i), "chapter": _chapter(n),
                               "character": n.character, "topic": topic,
                               "action": n.foreshadow, "source": n.source})
        if topic:
            ledger.topics_seen.append(topic)
    rec = ledger.reconcile()
    return {"passed": rec["all_closed"],
            "unrecovered": rec["unrecovered_topics"],
            "set_count": rec["set_count"], "pay_count": rec["pay_count"],
            "checked": len(nodes),
            "note": "已埋未收的伏笔主题"}


VALIDATORS = ("spacetime", "state", "timeline", "foreshadow")


def run_all(mod, nodes: List[EventNode]) -> Dict[str, Any]:
    """跑全部校验器，返回汇总。"""
    out = {
        "spacetime": audit_spacetime_contradiction(nodes),
        "state": audit_state_contradiction(nodes),
        "timeline": audit_timeline_regression(nodes),
        "foreshadow": audit_foreshadow_gap(mod, nodes),
    }
    out["all_passed"] = all(v["passed"] for v in out.values() if isinstance(v, dict))
    out["total_conflicts"] = sum(
        len(v.get("conflicts", [])) for k, v in out.items()
        if isinstance(v, dict) and k in VALIDATORS
    )
    return out
