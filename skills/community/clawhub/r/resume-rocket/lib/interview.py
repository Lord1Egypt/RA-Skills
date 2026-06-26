"""面试卡片生成（付费功能）"""
from __future__ import annotations
import json
import os
from .rewriter import _get_llm_client


PROMPT = """基于候选人简历和目标 JD，生成 {n} 张面试话术卡。

每张卡格式：
{{
  "q": "面试官可能问的问题",
  "intent": "面试官的真实意图",
  "answer_outline": "STAR 结构答题要点 3-5 条",
  "example_answer": "150-250 字范例回答",
  "pitfall": "常见翻车点"
}}

问题分布：
- 3 张自我介绍 / 为什么来 / 职业规划
- 4 张 JD 技术栈深挖
- 2 张项目经历追问
- 1 张反问面试官

输出 JSON：{{"cards": [...]}}
"""


def generate_interview_cards(resume, jd, n: int = 10) -> str:
    client, model = _get_llm_client()
    if client is None:
        return "# 面试卡片\n\n_未配置 LLM Key，请配置后重试_"

    user = {
        "resume_summary": resume.summary or resume.raw_text[:1500],
        "resume_experiences": [e.__dict__ for e in resume.experiences[:5]],
        "jd_title": jd.title,
        "jd_description": jd.description[:1500],
        "jd_keywords": jd.keywords,
    }
    try:
        print(f"[interview] 生成 {n} 张面试卡...")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": PROMPT.format(n=n)},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            temperature=0.6,
            timeout=90,
        )
        print("[interview] 面试卡生成完成")
        data = json.loads(resp.choices[0].message.content)
    except Exception as ex:
        return f"# 面试卡片\n\n_生成失败: {ex}_"

    lines = [f"# 面试话术卡 · {jd.title} @ {jd.company}", ""]
    for i, c in enumerate(data.get("cards", []), 1):
        lines.extend([
            f"## 卡片 {i}: {c.get('q', '')}",
            f"**面试官意图**：{c.get('intent', '')}",
            f"",
            f"**答题要点**：",
            c.get("answer_outline", ""),
            f"",
            f"**范例回答**：",
            f"> {c.get('example_answer', '')}",
            f"",
            f"**⚠️ 避坑**：{c.get('pitfall', '')}",
            f"",
            "---",
            "",
        ])
    return "\n".join(lines)
