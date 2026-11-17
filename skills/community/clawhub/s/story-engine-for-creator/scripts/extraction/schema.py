# -*- coding: utf-8 -*-
"""EventNode：逻辑漏洞检测的结构化输入契约（抽取层与校验层之间的唯一接口）。

设计原则（宁缺毋滥）：
  - character 与 action 必填；time/place/state 可空；
  - 空坐标的节点不参与对应校验（引擎不臆造坐标）；
  - 每个节点必须带 source（原文定位），保证任何结论可回原文核验。
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class EventNode:
    """一个可参与逻辑校验的最小事件单元。

    字段:
      character  角色名（必填）。同一角色须使用同一书写形式，别名归一由抽取层负责。
      action     动作/事件描述（必填）。用于因果断裂与近距复用判定。
      time       时间标记（可空）。绝对或相对时间均可，但同角色须同一计时体系。
      place      地点标记（可空）。
      state      人物状态（可空）。取值建议: 生/死/伤/愈/在/离/囚/自由 等互斥状态词。
      source     原文定位（建议 "第N回|摘录"）。必填，用于回查。
      foreshadow 伏笔标记（可空）: SET=埋下 / PAY=回收 / 空=非伏笔节点。
      topic      伏笔主题（foreshadow 非空时使用）。
      gold       黄金样本标注（可空）: ""=正常样本 / "spacetime"/"state"/"timeline"
                 =该节点所属的已知漏洞类型，供验收脚本判分。
    """
    character: str
    action: str
    time: str = ""
    place: str = ""
    state: str = ""
    source: str = ""
    foreshadow: str = ""
    topic: str = ""
    gold: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.character:
            raise ValueError("EventNode.character 不可为空（校验层不猜角色）")
        if not self.action:
            raise ValueError("EventNode.action 不可为空（无动作则不构成事件）")
        if not self.source:
            raise ValueError("EventNode.source 不可为空（无原文定位则结论不可核验）")

    def to_causal_node(self, mod, node_id: str = ""):
        """转成引擎的 CausalNode（供 ForeshadowLedger / 五步算子消费）。"""
        return mod.CausalNode(
            premise=self.action, conclusion=self.action,
            character=self.character, time=self.time, place=self.place,
            foreshadow=self.foreshadow, foreshadow_topic=self.topic,
        )


# 人物状态的互斥组：同组内状态不可同时/相继成立于同一角色同一时间线
STATE_EXCLUSIVE_GROUPS = [
    frozenset({"生", "死"}),
    frozenset({"在", "离"}),
    frozenset({"囚", "自由"}),
    frozenset({"伤", "愈"}),
]


def load_nodes(path: str) -> List[EventNode]:
    """从 JSON 载入 EventNode 列表（黄金样本或抽取产物）。"""
    import json
    import os
    if not os.path.exists(path):
        raise FileNotFoundError("节点文件不存在: " + path)
    raw = json.load(open(path, encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("nodes", raw.get("events", []))
    return [EventNode(**r) for r in raw]


def dump_nodes(nodes: List[EventNode], path: str) -> None:
    import json
    import os
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(n) for n in nodes], f, ensure_ascii=False, indent=1)


def schema_doc() -> Dict[str, Any]:
    """契约说明（供 README/报告引用）。"""
    return {
        "interface": "extraction.EventNode",
        "required": ["character", "action", "source"],
        "optional": ["time", "place", "state", "foreshadow", "topic", "gold", "meta"],
        "principle": "空坐标不参与对应校验；每个节点必须可回原文定位",
        "consumers": [
            "audit_spacetime_consistency（需 character+time+place）",
            "audit_state_contradiction（需 character+state+time）",
            "ForeshadowLedger（需 foreshadow+topic）",
        ],
    }
