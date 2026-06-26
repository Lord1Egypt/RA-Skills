"""LLM 改写：基于原简历 + JD，重写经历描述"""
from __future__ import annotations
from typing import Optional
import json
import os

from .parser import Resume, Experience


SYSTEM_PROMPT = """你是资深 HR 招聘专家 + 简历优化师。

任务：根据目标 JD，将候选人的简历经历重写，使其：
1. 使用 JD 原词表达（提高 ATS 命中）
2. 采用 STAR 结构（Situation / Task / Action / Result）
3. 量化成果（百分比 / 倍数 / 金额 / 人数）
4. **绝对不得**编造候选人没做过的事；只能对已有事实重新表达

输出 JSON：
{
  "summary": "3-5 句专业简介",
  "experiences": [
    {"company": "...", "title": "...", "period": "...", "bullets": ["..."]}
  ],
  "skills_reordered": ["..."],
  "highlight_tips": ["..."]
}
"""


def _get_llm_client():
    provider = os.getenv("RR_LLM_PROVIDER", "alibaba")
    key = os.getenv("RR_LLM_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        return None, None
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("请先 pip install openai")

    base_urls = {
        "alibaba": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "deepseek": "https://api.deepseek.com/v1",
        "zhipu": "https://open.bigmodel.cn/api/paas/v4",
        "openai": None,
    }
    models = {
        "alibaba": "qwen-plus",
        "deepseek": "deepseek-chat",
        "zhipu": "glm-4-plus",
        "openai": "gpt-4o-mini",
    }
    client = OpenAI(api_key=key, base_url=base_urls.get(provider))
    return client, models.get(provider, "qwen-plus")


def rewrite_resume(resume: Resume, jd, score) -> Resume:
    client, model = _get_llm_client()
    if client is None:
        # 无 Key → 返回原样 + 拼个基础 summary
        rewritten = Resume(**resume.__dict__)
        rewritten.summary = f"【未配置 LLM Key，展示原简历】{jd.title} 岗位候选人。匹配度 {score.total}/100。"
        return rewritten

    user_msg = {
        "resume_raw": resume.raw_text[:4000],
        "resume_skills": resume.skills,
        "resume_experiences": [e.__dict__ for e in resume.experiences],
        "jd_title": jd.title,
        "jd_company": jd.company,
        "jd_description": jd.description[:2000],
        "jd_keywords": jd.keywords,
        "missing_keywords": score.missing_keywords,
    }

    try:
        print("[rewriter] LLM 改写中...")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(user_msg, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
            timeout=60,
        )
        print("[rewriter] LLM 改写完成")
        data = json.loads(resp.choices[0].message.content)
    except Exception as ex:
        print(f"[rewriter] LLM 调用失败: {ex}，降级为原简历")
        return resume

    new_resume = Resume(
        raw_text=resume.raw_text,
        name=resume.name,
        contact=resume.contact,
        summary=data.get("summary", ""),
        skills=data.get("skills_reordered", resume.skills),
        education=resume.education,
    )
    for e in data.get("experiences", []):
        new_resume.experiences.append(Experience(
            company=e.get("company", ""),
            title=e.get("title", ""),
            period=e.get("period", ""),
            bullets=e.get("bullets", []),
        ))
    return new_resume
