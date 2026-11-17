"""examples/conflict_llm.py - M51 语义冲突检测「调用方注入 agent 的 LLM」（参考实现 / 适配器）。

设计边界（与库一致「更轻 / 调用方注入」）：
- 库本身【不】调用任何 LLM；research(conflict_check_fn=) 只暴露回调契约，由调用方注入。
- 本文件演示「调用方如何把一个【已有的 LLM】包装成该契约」——即 agent 用哪个 LLM，
  就把哪个 LLM 的调用函数传进来。库/示例零 key、零第二条连接、零硬编码端点。
- 适配器 make_llm_conflict(llm_fn)：llm_fn(prompt: str) -> str 由调用方注入（即 agent 用的
  LLM，例如 CodeBuddy 当前模型、DeepSeek、任意 OpenAI 兼容端点——由调用方自己持有 key）。
  未注入（llm_fn=None）→ 确定性兜底返回 []（库内默认零 LLM 行为），无 key、无网络。
- 与已有 examples/agent_dispatch.py 同一范式：库不 spawn、不持有，全部「调用方注入」。

回调签名严格匹配 research()：conflict_check_fn(query, evidence) -> list[dict]
  返回: [{"claim_a": str, "claim_b": str, "sources": [url...], "detail": str}, ...]；无冲突返回 []。

注入方式（一行）：
    from research import research
    from conflict_llm import make_llm_conflict
    research(query, conflict_check_fn=make_llm_conflict(my_agent_llm))   # my_agent_llm 是你自己的 LLM 调用
"""

import json
import sys
from typing import Any, Callable, Dict, List, Optional


def make_llm_conflict(llm_fn: Optional[Callable[[str], str]] = None):
    """返回一个 conflict_check_fn，内部用【调用方注入】的 llm_fn 做语义冲突检测。

    llm_fn: 调用方注入的 LLM 调用函数，签名 llm_fn(prompt: str) -> str。
            agent 用哪个 LLM，就传哪个；库/示例不持有任何 key 或端点。
            None → 返回的函数直接走确定性兜底（返回 []），不调用 LLM。
    用法：
        research(query, conflict_check_fn=make_llm_conflict(my_agent_llm))
    """

    def conflict_check_fn(query: str, evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if llm_fn is None:
            sys.stderr.write(
                "[conflict_llm] 未注入 llm_fn（agent 的 LLM），走确定性兜底（返回 []）\n"
            )
            return _heuristic_conflicts(query, evidence)
        snippets = []
        for i, e in enumerate(evidence[:12], 1):
            txt = (e.get("text") or e.get("snippet") or "")[:600]
            snippets.append(f"[{i}] (url={e.get('url', '')})\n{txt}")
        sys_prompt = (
            "你是事实核查助手。判断下列证据片段之间，是否存在针对【同一事实】的"
            "相互矛盾陈述（如数字、结论、因果关系、时间、主体相反）。"
            "忽略无关差异与互补视角。只输出 JSON，不要解释。"
        )
        user_prompt = (
            f"主问题: {query}\n\n证据:\n"
            + "\n\n".join(snippets)
            + '\n\n请输出 JSON 对象：{"conflicts": [{"claim_a": str, "claim_b": str, '
            '"sources": [url...], "detail": str}]}。若无矛盾，输出 {"conflicts": []}。'
        )
        try:
            content = llm_fn(f"{sys_prompt}\n\n{user_prompt}")
        except Exception as ex:
            sys.stderr.write(f"[conflict_llm] llm_fn 调用失败，退确定性兜底: {ex}\n")
            return _heuristic_conflicts(query, evidence)
        if not content:
            return _heuristic_conflicts(query, evidence)
        try:
            c = content.strip()
            if c.startswith("```"):
                c = c.strip("`")
                if c.lower().startswith("json"):
                    c = c[4:]
            parsed = json.loads(c)
            conflicts = parsed.get("conflicts") if isinstance(parsed, dict) else parsed
            return conflicts if isinstance(conflicts, list) else []
        except Exception as ex:
            sys.stderr.write(f"[conflict_llm] LLM 响应解析失败，退确定性兜底: {ex}\n")
            return _heuristic_conflicts(query, evidence)

    return conflict_check_fn


def _heuristic_conflicts(query: str, evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """零 LLM 确定性兜底：库内默认行为即返回空；真语义冲突需 LLM。"""
    return []


def _mock_llm(prompt: str) -> str:
    """演示用 mock LLM：命中「特斯拉 创立年份」冲突模式时返回冲突 JSON，否则 []。
    仅用于脱 key 验证接线，不代表真实 LLM 能力。"""
    if "特斯拉" in prompt and "2003" in prompt and "2008" in prompt:
        return (
            '{"conflicts": [{"claim_a": "特斯拉由艾伯哈德和塔彭宁于 2003 年创立",'
            '"claim_b": "特斯拉成立于 2008 年，马斯克是联合创始人",'
            '"sources": ["https://example.com/a", "https://example.com/b"],'
            '"detail": "创立年份矛盾：2003 vs 2008"}]}'
        )
    return '{"conflicts": []}'


def _demo():
    """脱 key 演示：注入 mock LLM 验证接线；再演示未注入时的默认兜底。"""
    conflicting = [
        {
            "url": "https://example.com/a",
            "text": "特斯拉由马丁·艾伯哈德和马克·塔彭宁于 2003 年创立。",
        },
        {"url": "https://example.com/b", "text": "特斯拉成立于 2008 年，埃隆·马斯克是联合创始人。"},
        {"url": "https://example.com/c", "text": "特斯拉总部位于美国得克萨斯州奥斯汀。"},
    ]
    clean = [
        {"url": "https://example.com/d", "text": "特斯拉是一家美国电动汽车制造商。"},
        {"url": "https://example.com/e", "text": "特斯拉总部位于美国得克萨斯州奥斯汀。"},
    ]
    print("=== 注入 mock LLM（脱 key 验证接线）===")
    fn = make_llm_conflict(_mock_llm)
    print(
        "含冲突:", json.dumps(fn("特斯拉成立于哪一年？", conflicting), ensure_ascii=False, indent=2)
    )
    print("无冲突:", json.dumps(fn("特斯拉是做什么的？", clean), ensure_ascii=False, indent=2))
    print("\n=== 未注入 llm_fn（默认兜底，返回 []）===")
    fn0 = make_llm_conflict(None)
    print(json.dumps(fn0("特斯拉成立于哪一年？", conflicting), ensure_ascii=False))


if __name__ == "__main__":
    _demo()
