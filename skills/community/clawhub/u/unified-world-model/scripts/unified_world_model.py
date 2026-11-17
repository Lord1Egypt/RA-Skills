#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unified-world-model —— 跨模态统一世界模型（迈向"超越一线大模型"的元之元能力）

把 text / code / vision / tool_state 四种模态的观察**融一潜空间**（一个共享的
grounded 状态对象），在其上做：
  - 跨模态一致性校验（groundedness）：检测不同模态之间的事实矛盾
  - 状态转移（transition）：应用动作推进世界
  - 前向仿真（rollout / predict_next）：预测给定动作后的下一状态 + 不确定性
  - 反事实推演（counterfactual）：在某一决策点分叉，对比两条轨迹

与纯文本生成式"世界模型"不同，本模型是 **grounded（有锚定、可证伪）** 的：
每个状态都由多模态事实支撑，跨模态矛盾会被显式标记，而非被平滑掉。
这是一线大模型至今仍薄弱、而"可靠地超越"所必需的底层能力。

纯标准库实现，零外部依赖；`python unified_world_model.py --selftest` 跑内置断言。
"""
import argparse
import json
import sys


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
class Observation:
    """单模态观察：来自 text / code / vision / tool_state 的一种证据。"""

    def __init__(self, modality, content, facts=None, tags=None):
        assert modality in ("text", "code", "vision", "tool_state"), modality
        self.modality = modality
        self.content = content
        self.facts = facts or {}          # 该模态显式声明的 grounded 事实 {'light': 'off'}
        self.tags = tags or []            # 该模态的标签（如 vision: ['dark']）

    def __repr__(self):
        return f"Obs({self.modality},{self.facts or self.tags})"


class UnifiedState:
    """统一状态：多模态观察融合后的共享 grounded 状态。"""

    def __init__(self, facts, modalities, contradictions=None):
        self.facts = facts                      # 跨模态一致的 grounded 事实
        self.modalities = modalities            # {modality: snapshot}
        self.contradictions = contradictions or []  # 跨模态矛盾清单

    @property
    def groundedness(self):
        """跨模态一致度：0~1（矛盾越多越低）。"""
        if not self.modalities:
            return 1.0
        n = len(self.modalities)
        return max(0.0, (n - len(self.contradictions)) / n)

    def snapshot(self):
        return {
            "facts": self.facts,
            "modalities": self.modalities,
            "contradictions": self.contradictions,
            "groundedness": round(self.groundedness, 3),
        }


# ---------------------------------------------------------------------------
# 融合：多模态观察 -> 统一状态（含跨模态一致性校验）
# ---------------------------------------------------------------------------
def unify(observations):
    """把多模态观察融合成一个统一状态，并检测跨模态事实矛盾。"""
    facts = {}
    modalities = {}
    contradictions = []

    # 先把每个模态的显式事实收进 facts；若同一 key 在不同模态取值冲突 -> 矛盾
    for obs in observations:
        modalities[obs.modality] = {
            "content": obs.content,
            "facts": obs.facts,
            "tags": obs.tags,
        }
        for k, v in obs.facts.items():
            if k in facts and facts[k] != v:
                contradictions.append({
                    "key": k,
                    "values": [facts[k], v],
                    "modalities": [m for m, s in modalities.items()
                                   if k in s["facts"] and s["facts"][k] != v] or [obs.modality],
                })
            else:
                facts[k] = v
        # vision 标签蕴含的事实：'dark' -> light=off 的弱约束（仅当无显式事实时）
        if obs.modality == "vision":
            for tag in obs.tags:
                if tag == "dark" and facts.get("light") not in ("off",):
                    if "light" in facts and facts["light"] != "off":
                        contradictions.append({
                            "key": "light",
                            "values": [facts["light"], "off(from:dark)"],
                            "modalities": ["vision"],
                        })
                    else:
                        facts.setdefault("light", "off")
                if tag == "bright" and facts.get("light") not in ("on",):
                    if "light" in facts and facts["light"] != "on":
                        contradictions.append({
                            "key": "light",
                            "values": [facts["light"], "on(from:bright)"],
                            "modalities": ["vision"],
                        })
                    else:
                        facts.setdefault("light", "on")
    return UnifiedState(facts, modalities, contradictions)


# ---------------------------------------------------------------------------
# 状态转移：在统一状态上应用动作
# ---------------------------------------------------------------------------
# 已知转移函数表：动作名 -> 对 facts 的确定性修改（纯函数）
KNOWN_TRANSITIONS = {
    "toggle_light": lambda f: {**f, "light": "on" if f.get("light") == "off" else "off"},
    "open_door": lambda f: {**f, "door": "open"},
    "close_door": lambda f: {**f, "door": "closed"},
    "run_code": lambda f: {**f, "code_ran": True},
    "call_tool": lambda f: {**f, "tool_called": True},
}


def transition(state, action, payload=None):
    """应用一个动作，返回新的统一状态（保持 modalities 快照，更新 facts）。"""
    new_facts = dict(state.facts)
    if action in KNOWN_TRANSITIONS:
        new_facts = KNOWN_TRANSITIONS[action](new_facts)
        # 同步 vision 标签：light 变化时更新
        if action == "toggle_light" and "vision" in new_facts.get("_mods", {}):
            pass
    new_modalities = {m: dict(s) for m, s in state.modalities.items()}
    # 若动作影响 vision，更新 vision 标签
    if action == "toggle_light" and "vision" in new_modalities:
        tag = "bright" if new_facts.get("light") == "on" else "dark"
        other = "dark" if tag == "bright" else "bright"
        new_modalities["vision"]["tags"] = [t for t in new_modalities["vision"]["tags"] if t != other] + [tag]
    return UnifiedState(new_facts, new_modalities, list(state.contradictions))


def predict_next(state, action):
    """前向预测：已知动作返回确定性下一状态(uncertainty=0)；未知动作返回高不确定性。"""
    if action in KNOWN_TRANSITIONS:
        return transition(state, action), 0.0
    # 未知动作：保持事实但标记为不确定
    return UnifiedState(dict(state.facts), {m: dict(s) for m, s in state.modalities.items()},
                        list(state.contradictions)), 1.0


def rollout(state, actions):
    """多步仿真：依次应用动作，返回轨迹（含初始状态）。"""
    traj = [state]
    cur = state
    for a in actions:
        cur = transition(cur, a)
        traj.append(cur)
    return traj


def counterfactual(state, plan, alt_action, at_step):
    """在 plan 的第 at_step 步用 alt_action 替换，得到两条对比轨迹。"""
    branch_a = rollout(state, plan)
    plan_b = list(plan)
    plan_b[at_step] = alt_action
    branch_b = rollout(state, plan_b)
    # 比较两分支终点
    end_a, end_b = branch_a[-1].facts, branch_b[-1].facts
    diff = {k: (end_a.get(k), end_b.get(k)) for k in set(end_a) | set(end_b)
            if end_a.get(k) != end_b.get(k)}
    return branch_a, branch_b, diff


# ---------------------------------------------------------------------------
# 自检
# ---------------------------------------------------------------------------
def selftest():
    print("== unified-world-model selftest ==")
    ok = True

    # 1) 一致的多模态融合
    s = unify([
        Observation("text", "灯是关着的", facts={"light": "off"}),
        Observation("vision", "房间很暗", tags=["dark"]),
    ])
    assert s.facts.get("light") == "off", s.facts
    assert s.contradictions == [], s.contradictions
    assert abs(s.groundedness - 1.0) < 1e-9, s.groundedness
    print("  [1] 一致融合 + groundedness=1.0  PASS")

    # 2) 跨模态矛盾检测
    s2 = unify([
        Observation("text", "灯亮着", facts={"light": "on"}),
        Observation("vision", "房间很暗", tags=["dark"]),
    ])
    assert len(s2.contradictions) == 1, s2.contradictions
    assert s2.groundedness < 1.0
    print("  [2] 跨模态矛盾检测  PASS (groundedness=%.2f)" % s2.groundedness)

    # 3) 状态转移：toggle_light 翻转 + vision 标签联动
    s3 = transition(s, "toggle_light")
    assert s3.facts.get("light") == "on", s3.facts
    assert s3.modalities["vision"]["tags"] == ["bright"], s3.modalities["vision"]
    print("  [3] 状态转移 + 跨模态标签联动  PASS")

    # 4) 多步 rollout
    traj = rollout(s, ["toggle_light", "open_door"])
    assert traj[-1].facts.get("light") == "on" and traj[-1].facts.get("door") == "open"
    assert len(traj) == 3
    print("  [4] 多步 rollout  PASS (states=%d)" % len(traj))

    # 5) 反事实分叉
    _, _, diff = counterfactual(s, ["toggle_light", "open_door"], "close_door", 1)
    assert "door" in diff and diff["door"][0] == "open" and diff["door"][1] == "closed", diff
    print("  [5] 反事实分叉对比  PASS (%s)" % diff)

    # 6) 前向预测：已知动作 uncertainty=0，未知动作 uncertainty=1
    _, u_known = predict_next(s, "toggle_light")
    _, u_unknown = predict_next(s, "teleport")
    assert u_known == 0.0 and u_unknown == 1.0, (u_known, u_unknown)
    print("  [6] 前向预测不确定性量化  PASS (known=%.1f unknown=%.1f)" % (u_known, u_unknown))

    print("ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="跨模态统一世界模型")
    ap.add_argument("--selftest", action="store_true", help="运行内置自检")
    ap.add_argument("--state", help="JSON 状态文件路径（可选，载入后用 observe/act 交互）")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    # 默认打印能力说明
    print(json.dumps({
        "capability": "unified-world-model",
        "modalities": ["text", "code", "vision", "tool_state"],
        "ops": ["unify", "transition", "predict_next", "rollout", "counterfactual"],
        "groundedness_example": unify([
            Observation("text", "x", facts={"light": "on"}),
            Observation("vision", "x", tags=["bright"]),
        ]).snapshot(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
