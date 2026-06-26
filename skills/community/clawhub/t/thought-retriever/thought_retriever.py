# Thought-Retriever 五步循环引擎
# 
# 五步：
#   1. 检索相关 Thought（从 ontology 查）
#   2. 生成回答（已由主模型完成，这里只记录）
#   3. 提炼候选思想 + 计算置信度
#   4. 查重剔除（置信度过滤 + 相似度去重）
#   5. 更新记忆（写入 ontology Thought 实体）
#
# 阈值参数（可调）：
GAMMA = 0.6   # 置信度阈值，低于此值丢弃
THETA = 0.80   # 相似度阈值，高于此值视为重复

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────
WORKSPACE = Path("C:/Users/89627/.openclaw/workspace").resolve()
MEMORY_DIR = WORKSPACE / "memory"
GRAPH_PATH = MEMORY_DIR / "ontology" / "graph.jsonl"
SCHEMA_PATH = MEMORY_DIR / "ontology" / "schema.yaml"
THOUGHTS_DIR = MEMORY_DIR / "thoughts"

# ── 引入 ontology 核心 ─────────────────────────────────
sys.path.insert(0, str(WORKSPACE / "skills" / "ontology" / "scripts"))
from ontology import load_graph, append_op, create_entity, update_entity, list_entities

# ── LLM 调用（用 SiliconFlow）──────────────────────────
import requests

SF_API = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
SF_KEY = "sk-b841f4b7c91d40ddb12502462708f361"

def make_sf_session():
    """创建不走代理的 requests session"""
    session = requests.Session()
    session.trust_env = False  # 禁用环境变量中的代理
    return session

def llm_extract_thoughts(user_query: str, generated_answer: str, context: str = "") -> list[dict]:
    """
    调用 LLM 从回答中提炼候选思想（步骤3）
    返回: [{"content": str, "confidence": float}, ...]
    """
    prompt = f"""你是一个知识提炼专家。从以下对话中提取出有长期价值的"思想"（knowledge crystals）。

要求：
- 每个思想是一个独立的洞察点，简洁明了（1-2句话）
- 思想应该是有意义的、可复用的知识，不是普通的事实陈述
- 为每个思想给出一个置信度分数（0.0-1.0），参考：
  - 0.9-1.0：明确验证过的结论，多个证据支持
  - 0.7-0.8：合理的推断，有一定依据
  - 0.5-0.6：初步观察，可能需要更多验证
  - < 0.5：低置信度，丢弃

用户问题：{user_query}
回答内容：{generated_answer}

请以 JSON 数组格式输出，例如：
[
  {{"content": "当用户询问X时，应该使用Y方法", "confidence": 0.85}},
  {{"content": "Z情况下需要特别注意", "confidence": 0.7}}
]

只输出 JSON，不要有其他文字。"""

    try:
        session = make_sf_session()
        resp = session.post(
            SF_API,
            headers={"Authorization": f"Bearer {SF_KEY}", "Content-Type": "application/json"},
            json={
                "model": "glm-5.1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=30
        )
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        # 尝试解析 JSON
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        thoughts = json.loads(content)
        return thoughts
    except Exception as e:
        print(f"[Thought-Retriever] LLM 提炼失败: {e}")
        return []


def llm_similarity(text1: str, text2: str) -> float:
    """
    用 LLM 判断两段文本的语义相似度（步骤4查重）
    返回: 0.0-1.0 的相似度分数
    """
    prompt = f"""判断以下两段文本的语义相似度（0.0-1.0）：
文本1：{text1[:200]}
文本2：{text2[:200]}
只输出一个数字，例如 0.85"""

    try:
        resp = make_sf_session().post(
            SF_API,
            headers={"Authorization": f"Bearer {SF_KEY}", "Content-Type": "application/json"},
            json={
                "model": "glm-5.1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0
            },
            timeout=20
        )
        result = resp.json()["choices"][0]["message"]["content"].strip()
        # 提取数字
        import re
        match = re.search(r"0?\.\d+", result)
        if match:
            return float(match.group())
        return 0.0
    except Exception as e:
        print(f"[Thought-Retriever] 相似度判断失败: {e}")
        return 0.0


def retrieve_relevant_thoughts(user_query: str, limit: int = 5) -> list[dict]:
    """
    步骤1：从 ontology 中检索与当前话题最相关的 Thought 实体
    当前实现：简单的关键词匹配 + 相似度排序
    """
    entities, _ = load_graph(str(GRAPH_PATH))
    thoughts = [e for e in entities.values() if e["type"] == "Thought"]
    
    if not thoughts:
        return []
    
    # 用 LLM 给每个 Thought 打相关性分数
    scored = []
    for thought in thoughts:
        sim = llm_similarity(user_query, thought["properties"].get("content", ""))
        scored.append((sim, thought))
    
    # 排序取 top-K
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored[:limit]]


def thought_retriever_cycle(
    user_query: str,
    generated_answer: str,
    user_feedback: str = None,
    gamma: float = GAMMA,
    theta: float = THETA
):
    """
    完整的 Thought-Retriever 五步循环。
    在每次对话结束时调用。
    """
    print(f"[Thought-Retriever] 开始五步循环...")
    print(f"  用户问题: {user_query[:80]}...")
    
    # 步骤1：检索相关思想
    relevant = retrieve_relevant_thoughts(user_query, limit=5)
    print(f"  步骤1: 检索到 {len(relevant)} 个相关 Thought")
    
    # 步骤3：提炼候选思想
    candidate_thoughts = llm_extract_thoughts(user_query, generated_answer)
    print(f"  步骤3: 提炼出 {len(candidate_thoughts)} 个候选思想")
    
    # 步骤4：过滤与去重
    new_thoughts_to_add = []
    all_thoughts = list_entities("Thought", str(GRAPH_PATH))
    
    for thought in candidate_thoughts:
        conf = thought.get("confidence", 0.5)
        
        # 4a. 置信度过滤
        if conf < gamma:
            print(f"    丢弃（低置信度 {conf:.2f} < {gamma}）: {thought['content'][:50]}...")
            continue
        
        # 4b. 查重
        highest_sim = 0.0
        most_similar_existing = None
        for existing in all_thoughts:
            sim = llm_similarity(thought["content"], existing["properties"].get("content", ""))
            if sim > highest_sim:
                highest_sim = sim
                most_similar_existing = existing
        
        if highest_sim > theta:
            # 重复：更新已存在的思想，提高置信度
            existing_id = most_similar_existing["id"]
            new_conf = min(1.0, most_similar_existing["properties"].get("confidence", 0.5) + 0.1)
            update_entity(existing_id, {"confidence": new_conf}, str(GRAPH_PATH))
            print(f"    合并（相似度 {highest_sim:.2f} > {theta}）: {thought['content'][:40]}... -> 更新已有")
        else:
            new_thoughts_to_add.append(thought)
    
    print(f"  步骤4: 去重后剩余 {len(new_thoughts_to_add)} 个新思想")
    
    # 步骤5：批量写入
    for thought in new_thoughts_to_add:
        create_entity(
            "Thought",
            {
                "content": thought["content"],
                "confidence": thought["confidence"],
                "last_accessed": datetime.now(timezone.utc).isoformat(),
                "source": "conversation",
                "query": user_query[:100],
            },
            str(GRAPH_PATH)
        )
        print(f"    新增 Thought: {thought['content'][:50]}... (conf={thought['confidence']:.2f})")
    
    print(f"[Thought-Retriever] 循环完成，新增 {len(new_thoughts_to_add)} 个 Thought")
    return {
        "relevant_count": len(relevant),
        "candidates": len(candidate_thoughts),
        "new_thoughts": len(new_thoughts_to_add)
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Thought-Retriever 五步循环引擎")
    parser.add_argument("--query", "-q", required=True, help="用户问题")
    parser.add_argument("--answer", "-a", required=True, help="生成的回答")
    parser.add_argument("--feedback", "-f", help="用户反馈（可选）")
    parser.add_argument("--gamma", "-g", type=float, default=GAMMA, help="置信度阈值")
    parser.add_argument("--theta", "-t", type=float, default=THETA, help="相似度阈值")
    args = parser.parse_args()
    
    result = thought_retriever_cycle(
        args.query, args.answer, args.feedback,
        gamma=args.gamma, theta=args.theta
    )
    print(json.dumps(result, indent=2))
