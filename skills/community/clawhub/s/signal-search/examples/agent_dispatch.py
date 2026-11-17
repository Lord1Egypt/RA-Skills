"""examples/agent_dispatch.py - 调用方如何注入真·子 agent 派发（agent_fn 契约示范）。

Signal-Search 库本身不 spawn agent（更轻边界）。要真正并行派多个子 agent 调研各维度，
由调用方实现 agent_fn(prompt, dim, fetch_fn) 并传给 research()。本文件给一个最小可运行
模板：用伪 agent 演示契约（替换 _fake_agent 为你真实的 agent/LLM 调用即可）。
"""

from typing import Any, Dict, List


def _fake_agent(prompt: str, dim: Dict[str, Any], fetch_fn=None) -> List[Dict[str, Any]]:
    """示例子 agent：真实环境应在此调用你的 LLM/agent 框架，返回证据列表。

    prompt 是 research 锁模板生成的派发 prompt（含维度名/深度/主题/时间范围）；
    dim 是当前维度 dict；fetch_fn 可选，供子 agent 取网页。
    """
    # 真实实现示例（伪代码）：
    #   resp = your_llm.chat(prompt, tools=[fetch_web])
    #   return [{"url": u, "text": t, "source_type": "web"} for u, t in resp.citations]
    return [
        {
            "url": "https://example.com/" + str(dim.get("name", "dim")),
            "text": f"[fake agent] {prompt[:60]}",
            "source_type": "web",
        }
    ]


def run_example(query: str, cfg: Dict[str, Any] = None) -> Dict[str, Any]:
    import research

    return research.research(
        query,
        cfg=cfg,
        tier="L3",
        agent_fn=_fake_agent,
        vault_dir=None,  # 设 "./research_vault" 可落盘
    )


if __name__ == "__main__":
    import json

    print(json.dumps(run_example("对比 TCP 与 UDP 的拥塞控制"), ensure_ascii=False, indent=2))
