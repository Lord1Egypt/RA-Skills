#!/usr/bin/env python3
"""
简历-JD 5维度匹配度评分引擎
用法: python score_resume.py --resume-file <path> --jd-file <path> --output <json_path>
      python score_resume.py --resume-text "<text>" --jd-text "<text>" --output <json_path>
输出: JSON (scores, keyword_matches, dimension_breakdown, recommendations, cross_job_comparison)
"""

import json
import re
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from difflib import SequenceMatcher

# ─── 关键词分类词库 ──────────────────────────────────────────

# AI/ML 硬技能关键词（带权重）
AI_ML_KEYWORDS = {
    # 编程语言 (权重: high)
    "python": {"weight": "high", "category": "programming"},
    "c++": {"weight": "high", "category": "programming"},
    "c/c++": {"weight": "high", "category": "programming"},
    "java": {"weight": "medium", "category": "programming"},
    "golang": {"weight": "medium", "category": "programming"},
    "rust": {"weight": "medium", "category": "programming"},
    "sql": {"weight": "medium", "category": "programming"},
    "shell": {"weight": "low", "category": "programming"},
    # 深度学习框架 (权重: high/critical)
    "pytorch": {"weight": "critical", "category": "framework"},
    "tensorflow": {"weight": "critical", "category": "framework"},
    "keras": {"weight": "medium", "category": "framework"},
    "jax": {"weight": "medium", "category": "framework"},
    "paddlepaddle": {"weight": "medium", "category": "framework"},
    "mindspore": {"weight": "medium", "category": "framework"},
    # 模型架构 (权重: critical)
    "transformer": {"weight": "critical", "category": "model_arch"},
    "attention mechanism": {"weight": "high", "category": "model_arch"},
    "bert": {"weight": "high", "category": "model_arch"},
    "gpt": {"weight": "high", "category": "model_arch"},
    "llama": {"weight": "high", "category": "model_arch"},
    "diffusion": {"weight": "high", "category": "model_arch"},
    "cnn": {"weight": "medium", "category": "model_arch"},
    "rnn": {"weight": "medium", "category": "model_arch"},
    "lstm": {"weight": "medium", "category": "model_arch"},
    "gan": {"weight": "medium", "category": "model_arch"},
    "vae": {"weight": "medium", "category": "model_arch"},
    "moe": {"weight": "medium", "category": "model_arch"},
    "mamba": {"weight": "medium", "category": "model_arch"},
    # 训练相关 (权重: critical/high)
    "预训练": {"weight": "critical", "category": "training", "alias": ["pretraining", "pre-training"]},
    "pretraining": {"weight": "critical", "category": "training"},
    "pre-training": {"weight": "critical", "category": "training"},
    "微调": {"weight": "high", "category": "training", "alias": ["fine-tuning", "finetune"]},
    "fine-tuning": {"weight": "high", "category": "training"},
    "finetune": {"weight": "high", "category": "training"},
    "lora": {"weight": "high", "category": "training"},
    "qlora": {"weight": "high", "category": "training"},
    "sft": {"weight": "high", "category": "training"},
    "rlhf": {"weight": "high", "category": "training"},
    "dpo": {"weight": "medium", "category": "training"},
    "分布式训练": {"weight": "high", "category": "training"},
    "distributed training": {"weight": "high", "category": "training"},
    "scaling law": {"weight": "critical", "category": "training"},
    "data parallelism": {"weight": "medium", "category": "training"},
    "model parallelism": {"weight": "medium", "category": "training"},
    "混合精度训练": {"weight": "medium", "category": "training"},
    "mixed precision": {"weight": "medium", "category": "training"},
    "模型训练": {"weight": "high", "category": "training", "alias": ["model training"]},
    # 推理优化 (权重: medium)
    "模型压缩": {"weight": "medium", "category": "inference"},
    "量化": {"weight": "medium", "category": "inference"},
    "quantization": {"weight": "medium", "category": "inference"},
    "剪枝": {"weight": "low", "category": "inference"},
    "pruning": {"weight": "low", "category": "inference"},
    "蒸馏": {"weight": "medium", "category": "inference"},
    "distillation": {"weight": "medium", "category": "inference"},
    "推理优化": {"weight": "medium", "category": "inference"},
    "vllm": {"weight": "medium", "category": "inference"},
    "tensorrt": {"weight": "medium", "category": "inference"},
    "onnx": {"weight": "medium", "category": "inference"},
    # 环境/工具 (权重: medium/high)
    "linux": {"weight": "high", "category": "environment"},
    "docker": {"weight": "medium", "category": "environment"},
    "k8s": {"weight": "medium", "category": "environment"},
    "kubernetes": {"weight": "medium", "category": "environment"},
    "git": {"weight": "low", "category": "environment"},
    "cuda": {"weight": "medium", "category": "environment"},
    "nvidia": {"weight": "low", "category": "environment"},
    "wandb": {"weight": "low", "category": "environment"},
    "mlflow": {"weight": "low", "category": "environment"},
    "deepspeed": {"weight": "high", "category": "environment"},
    "megatron": {"weight": "high", "category": "environment"},
    # 大模型应用 (权重: medium)
    "大模型": {"weight": "high", "category": "llm_app", "alias": ["llm", "large language model"]},
    "llm": {"weight": "high", "category": "llm_app"},
    "rag": {"weight": "high", "category": "llm_app"},
    "agent": {"weight": "high", "category": "llm_app"},
    "langchain": {"weight": "medium", "category": "llm_app"},
    "llamaindex": {"weight": "medium", "category": "llm_app"},
    "prompt engineering": {"weight": "medium", "category": "llm_app"},
    "prompt": {"weight": "low", "category": "llm_app"},
    "mcp": {"weight": "medium", "category": "llm_app"},
    "function calling": {"weight": "medium", "category": "llm_app"},
    "tool use": {"weight": "medium", "category": "llm_app"},
    "workflow": {"weight": "low", "category": "llm_app"},
    # 机器学习基础 (权重: medium)
    "机器学习": {"weight": "medium", "category": "ml_basics", "alias": ["machine learning"]},
    "machine learning": {"weight": "medium", "category": "ml_basics"},
    "深度学习": {"weight": "high", "category": "ml_basics", "alias": ["deep learning"]},
    "deep learning": {"weight": "high", "category": "ml_basics"},
    "nlp": {"weight": "high", "category": "ml_basics"},
    "自然语言处理": {"weight": "high", "category": "ml_basics", "alias": ["nlp"]},
    "cv": {"weight": "high", "category": "ml_basics"},
    "计算机视觉": {"weight": "high", "category": "ml_basics", "alias": ["cv"]},
    "语音识别": {"weight": "medium", "category": "ml_basics"},
    "asr": {"weight": "medium", "category": "ml_basics"},
    "推荐系统": {"weight": "medium", "category": "ml_basics"},
    "recommendation": {"weight": "medium", "category": "ml_basics"},
    "时间序列": {"weight": "medium", "category": "ml_basics"},
    "time series": {"weight": "medium", "category": "ml_basics"},
    "异常检测": {"weight": "low", "category": "ml_basics"},
    "anomaly detection": {"weight": "low", "category": "ml_basics"},
    "知识图谱": {"weight": "medium", "category": "ml_basics"},
    "knowledge graph": {"weight": "medium", "category": "ml_basics"},
    "数据分析": {"weight": "medium", "category": "ml_basics"},
    "data analysis": {"weight": "medium", "category": "ml_basics"},
    # 学术相关
    "顶会": {"weight": "high", "category": "academic"},
    "top conference": {"weight": "high", "category": "academic"},
    "论文": {"weight": "high", "category": "academic"},
    "paper": {"weight": "high", "category": "academic"},
    "发表": {"weight": "high", "category": "academic"},
    "publication": {"weight": "high", "category": "academic"},
    "专利": {"weight": "high", "category": "academic"},
    "patent": {"weight": "high", "category": "academic"},
    "neurips": {"weight": "high", "category": "academic"},
    "icml": {"weight": "high", "category": "academic"},
    "iclr": {"weight": "high", "category": "academic"},
    "cvpr": {"weight": "high", "category": "academic"},
    "iccv": {"weight": "high", "category": "academic"},
    "eccv": {"weight": "high", "category": "academic"},
    "acl": {"weight": "high", "category": "academic"},
    "emnlp": {"weight": "high", "category": "academic"},
    "naacl": {"weight": "high", "category": "academic"},
    "aaai": {"weight": "high", "category": "academic"},
    "ijcai": {"weight": "high", "category": "academic"},
    "kdd": {"weight": "high", "category": "academic"},
    "sigir": {"weight": "high", "category": "academic"},
    "www": {"weight": "medium", "category": "academic"},
    "arxiv": {"weight": "low", "category": "academic"},
}

# 权重数值映射
WEIGHT_MAP = {
    "critical": 5,
    "high": 4,
    "medium": 2.5,
    "low": 1,
}

# ─── 角色类型判断 ──────────────────────────────────────────

def analyze_role(resume_text: str, jd_text: str) -> dict:
    """分析目标岗位角色和候选人角色"""
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    # 目标岗位角色检测
    target_role = "unknown"
    if any(w in jd_lower for w in ["算法研究员", "research scientist", "算法工程师", "research engineer",
                                      "algorithm researcher", "预训练", "pre-training", "pretraining"]):
        target_role = "algorithm_researcher"
    elif any(w in jd_lower for w in ["算法工程师", "algorithm engineer", "ml engineer", "machine learning engineer"]):
        target_role = "algorithm_engineer"
    elif any(w in jd_lower for w in ["产品经理", "product manager"]):
        target_role = "product_manager"
    elif any(w in jd_lower for w in ["数据科学家", "data scientist"]):
        target_role = "data_scientist"
    elif any(w in jd_lower for w in ["开发工程师", "software engineer", "后端", "backend"]):
        target_role = "software_engineer"

    # 候选人角色检测
    candidate_role = "unknown"
    if any(w in resume_lower for w in ["产品经理", "product manager"]):
        candidate_role = "product_manager"
    elif any(w in resume_lower for w in ["算法研究员", "research scientist"]):
        candidate_role = "algorithm_researcher"
    elif any(w in resume_lower for w in ["算法工程师", "algorithm engineer"]):
        candidate_role = "algorithm_engineer"
    elif any(w in resume_lower for w in ["开发工程师", "软件工程师", "software engineer"]):
        candidate_role = "software_engineer"
    elif any(w in resume_lower for w in ["项目经理", "project manager"]):
        candidate_role = "project_manager"

    role_mismatch = (target_role != candidate_role) and target_role != "unknown" and candidate_role != "unknown"

    return {
        "target_role": target_role,
        "candidate_role": candidate_role,
        "role_mismatch": role_mismatch,
    }


# ─── 关键词提取 ──────────────────────────────────────────

def extract_keywords(text: str) -> dict:
    """从文本中提取关键词及其出现频次"""
    text_lower = text.lower()
    found = {}

    for kw, meta in AI_ML_KEYWORDS.items():
        kw_lower = kw.lower()
        # 精确匹配
        if kw_lower in text_lower:
            # 统计出现次数
            count = len(re.findall(re.escape(kw), text, re.IGNORECASE))
            found[kw] = {
                "count": count,
                "weight": meta["weight"],
                "category": meta["category"],
                "match_type": "exact",
            }
            continue
        # 别名匹配
        aliases = meta.get("alias", [])
        matched = False
        for alias in aliases:
            if alias.lower() in text_lower:
                count = len(re.findall(re.escape(alias), text, re.IGNORECASE))
                found[kw] = {
                    "count": count,
                    "weight": meta["weight"],
                    "category": meta["category"],
                    "match_type": "alias",
                    "matched_alias": alias,
                }
                matched = True
                break
        if matched:
            continue
        # 模糊匹配（关键词长度>4且相似度>0.85）
        if len(kw) > 4:
            words = text_lower.split()
            for w in words:
                if len(w) > 3 and SequenceMatcher(None, kw_lower, w).ratio() > 0.85:
                    found[kw] = {
                        "count": 1,
                        "weight": meta["weight"],
                        "category": meta["category"],
                        "match_type": "fuzzy",
                        "matched_text": w,
                    }
                    break

    return found


def extract_jd_keywords(jd_text: str) -> list:
    """从JD中提取关键词（词汇在JD中出现即作为要求关键词）"""
    found = extract_keywords(jd_text)
    keywords = []
    for kw, meta in found.items():
        keywords.append({
            "keyword": kw,
            "weight": meta["weight"],
            "category": meta["category"],
            "weight_value": WEIGHT_MAP.get(meta["weight"], 1),
        })
    # 按权重排序
    keywords.sort(key=lambda x: x["weight_value"], reverse=True)
    return keywords


# ─── 学历提取 ──────────────────────────────────────────

def extract_education(text: str) -> dict:
    """提取学历信息"""
    text_lower = text.lower()
    result = {"has_phd": False, "has_master": False, "has_bachelor": False,
              "cs_related": False, "schools": []}

    if any(w in text_lower for w in ["博士", "phd", "ph.d", "博士研究生"]):
        result["has_phd"] = True
    if any(w in text_lower for w in ["硕士", "master", "硕士研究生", "研究生"]):
        result["has_master"] = True
    if any(w in text_lower for w in ["本科", "bachelor", "学士", "大学"]):
        result["has_bachelor"] = True

    cs_keywords = ["计算机", "人工智能", "软件工程", "数据科学", "统计", "数学",
                   "computer science", "ai", "artificial intelligence", "data science",
                   "statistics", "mathematics", "machine learning"]
    if any(w in text_lower for w in cs_keywords):
        result["cs_related"] = True

    # 提取学校名（简单模式）
    school_pattern = re.findall(r'([\u4e00-\u9fa5]+大学|[\u4e00-\u9fa5]+学院)', text)
    result["schools"] = list(set(school_pattern))

    return result


# ─── 论文/专利检测 ──────────────────────────────────────────

def extract_publications(text: str) -> dict:
    """检测论文和专利"""
    result = {
        "has_paper": False,
        "has_patent": False,
        "has_top_conference": False,
        "paper_count": 0,
    }

    # 论文检测
    paper_indicators = ["论文", "发表", "paper", "publication", "published", "arxiv", "doi"]
    if any(w in text.lower() for w in paper_indicators):
        result["has_paper"] = True

    # 顶会检测
    top_venues = ["neurips", "icml", "iclr", "cvpr", "iccv", "eccv", "acl", "emnlp",
                  "naacl", "aaai", "ijcai", "kdd", "sigir"]
    text_lower = text.lower()
    for venue in top_venues:
        if venue in text_lower:
            result["has_top_conference"] = True
            result["paper_count"] += 1

    # 专利检测
    if any(w in text for w in ["专利", "patent"]):
        result["has_patent"] = True

    return result


# ─── 核心评分函数 ──────────────────────────────────────────

def score_resume(resume_text: str, jd_text: str) -> dict:
    """
    5维度评分主函数
    返回完整的评分字典
    """
    # Step 1: 角色分析
    role_info = analyze_role(resume_text, jd_text)

    # Step 2: 关键词提取
    jd_kws = extract_jd_keywords(jd_text)
    resume_kws = extract_keywords(resume_text)

    # Step 3: 关键词交叉匹配
    kw_matches = []
    matched_critical = 0
    total_critical = 0
    matched_high = 0
    total_high = 0
    matched_medium = 0
    total_medium = 0
    matched_low = 0
    total_low = 0

    for jd_kw in jd_kws:
        kw_name = jd_kw["keyword"]
        weight = jd_kw["weight"]
        category = jd_kw["category"]

        # 统计权重计数
        if weight == "critical":
            total_critical += 1
        elif weight == "high":
            total_high += 1
        elif weight == "medium":
            total_medium += 1
        elif weight == "low":
            total_low += 1

        # 匹配检测
        match_status = "miss"
        evidence = ""
        if kw_name in resume_kws:
            match_status = "full"
            evidence = f"简历中明确出现'{kw_name}'（{resume_kws[kw_name]['count']}次）"
            if weight == "critical":
                matched_critical += 1
            elif weight == "high":
                matched_high += 1
            elif weight == "medium":
                matched_medium += 1
            elif weight == "low":
                matched_low += 1
        else:
            # 尝试部分匹配
            kw_lower = kw_name.lower()
            resume_lower = resume_text.lower()
            # 检查语义相关（关键词在同一类别下的其他命中）
            for rkw, rmeta in resume_kws.items():
                if rmeta["category"] == category:
                    match_status = "partial"
                    evidence = f"简历有同类关键词'{rkw}'（类别: {category}），但未精确匹配'{kw_name}'"
                    break

        kw_matches.append({
            "keyword": kw_name,
            "weight": weight,
            "category": category,
            "match_status": match_status,
            "evidence": evidence,
        })

    # 额外命中（简历有但JD没有的关键词）
    jd_kw_names = {k["keyword"] for k in jd_kws}
    extra_hits = []
    for rkw, rmeta in resume_kws.items():
        if rkw not in jd_kw_names:
            extra_hits.append({
                "keyword": rkw,
                "category": rmeta["category"],
                "weight": rmeta["weight"],
            })

    # Step 4: 提取学历和学术信息
    education = extract_education(resume_text)
    publications = extract_publications(resume_text)

    # ── 维度1: 硬技能匹配 (30分) ──
    hard_categories = {"programming", "framework", "model_arch", "training", "inference", "environment", "ml_basics"}
    jd_hard_kws = [k for k in jd_kws if k["category"] in hard_categories]
    jd_hard_names = {k["keyword"] for k in jd_hard_kws}

    hard_matched = sum(1 for k in jd_hard_kws if k["keyword"] in resume_kws)
    hard_total = max(len(jd_hard_kws), 1)
    hard_score_raw = (hard_matched / hard_total) * 30

    # 加分：critical权重命中
    critical_in_hard = [k for k in jd_hard_kws if k["weight"] == "critical"]
    critical_matched_in_hard = sum(1 for k in critical_in_hard if k["keyword"] in resume_kws)
    critical_bonus = (critical_matched_in_hard / max(len(critical_in_hard), 1)) * 5

    hard_skills_score = min(round(hard_score_raw + critical_bonus), 30)

    hard_gains = []
    hard_losses = []
    for k in jd_hard_kws:
        if k["keyword"] in resume_kws:
            hard_gains.append(f"命中 {k['keyword']}（{k['weight']}权重）")
        elif k["weight"] in ("critical", "high"):
            hard_losses.append(f"缺失 {k['keyword']}（{k['weight']}权重）")

    if len(hard_losses) > 6:
        hard_losses = hard_losses[:6] + [f"...及其他 {len(hard_losses)-6} 项"]

    # ── 维度2: 经历相关性 (25分) ──
    role_score = 10 if not role_info["role_mismatch"] else 3  # 角色匹配10分
    if role_info["role_mismatch"]:
        role_penalty = 7  # PM→Researcher 重大错位
    else:
        role_penalty = 0

    # 行业匹配
    industry_keywords = ["人工智能", "ai", "机器学习", "深度学习", "nlp", "大模型",
                         "智能", "算法", "数据挖掘", "machine learning", "deep learning"]
    industry_match = sum(1 for w in industry_keywords if w.lower() in resume_text.lower())
    industry_score = min(industry_match * 1.5, 8)

    # 项目相关性
    project_keywords = ["agent", "mcp", "rag", "模型", "训练", "数据", "问答",
                        "知识图谱", "智能体", "工作流", "推荐", "预测"]
    project_match = sum(1 for w in project_keywords if w.lower() in resume_text.lower())
    project_score = min(project_match * 1.2, 7)

    experience_score = min(round(role_score - role_penalty + industry_score + project_score), 25)
    experience_score = max(experience_score, 3)

    exp_gains = []
    exp_losses = []
    if industry_match > 0:
        exp_gains.append(f"命中 {industry_match} 个行业关键词")
    if project_match > 0:
        exp_gains.append(f"命中 {project_match} 个项目关键词")
    if not role_info["role_mismatch"]:
        exp_gains.append("角色匹配（候选人经历与目标岗位角色一致）")
    else:
        exp_losses.append(f"角色不匹配：{role_info['candidate_role']} ≠ {role_info['target_role']} (-7分)")
    if industry_match < 3:
        exp_losses.append("行业关键词覆盖不足")

    # ── 维度3: 学术产出 (20分) ──
    academic_score = 0
    acad_gains = []
    acad_losses = []

    if publications["has_top_conference"]:
        academic_score += 12
        acad_gains.append(f"有顶会论文发表")
    elif publications["has_paper"]:
        academic_score += 6
        acad_gains.append("有论文发表记录")
    else:
        acad_losses.append("无论文发表记录 (-8分)")

    if publications["has_patent"]:
        academic_score += 4
        acad_gains.append("有专利")
    else:
        acad_losses.append("无专利 (-5分)")

    if education["has_phd"]:
        academic_score += 4
        acad_gains.append("博士学位")
    elif education["has_master"]:
        academic_score += 3
        if education["cs_related"]:
            academic_score += 1
            acad_gains.append("硕士学历（CS/AI相关专业）")
        else:
            acad_gains.append("硕士学历（非CS/AI专业）")
    elif education["has_bachelor"]:
        academic_score += 1
        acad_gains.append("本科学历")

    academic_score = min(academic_score, 20)

    # ── 维度4: ATS关键词覆盖率 (15分) ──
    total_jd_kw = len(jd_kws)
    total_matched = sum(1 for k in kw_matches if k["match_status"] in ("full", "partial"))
    ats_coverage = total_matched / max(total_jd_kw, 1)
    ats_score = round(ats_coverage * 15)

    ats_gains = [f"JD关键词总命中率 {ats_coverage:.0%}"]
    ats_losses = []
    missing_critical = [k["keyword"] for k in kw_matches
                        if k["match_status"] == "miss" and k["weight"] == "critical"]
    if missing_critical:
        ats_losses.append(f"缺失核心关键词: {', '.join(missing_critical[:5])}")

    # ── 维度5: 加分项 (10分) ──
    bonus_score = 0
    bonus_gains = []
    bonus_losses = []

    # 经验年限
    years_exp = 0
    exp_match = re.search(r'(\d+)\s*年.*?(?:工作|经验)', resume_text)
    if exp_match:
        years_exp = int(exp_match.group(1))
    if years_exp >= 10:
        bonus_score += 3
        bonus_gains.append(f"{years_exp}年工作经验 (+3)")
    elif years_exp >= 5:
        bonus_score += 2
        bonus_gains.append(f"{years_exp}年工作经验 (+2)")
    elif years_exp >= 3:
        bonus_score += 1
        bonus_gains.append(f"{years_exp}年工作经验 (+1)")

    # 学历加分
    if education["has_phd"]:
        bonus_score += 2
        bonus_gains.append("博士学位 (+2)")
    elif education["has_master"] and education["cs_related"]:
        bonus_score += 2
        bonus_gains.append("CS相关硕士 (+2)")
    elif education["has_master"]:
        bonus_score += 1
        bonus_gains.append("硕士学历 (+1)")

    # 前沿技术
    frontier_kws = ["agent", "mcp", "rag", "langchain", "llamaindex", "deepspeed"]
    frontier_match = sum(1 for w in frontier_kws if w in resume_text.lower())
    if frontier_match >= 2:
        bonus_score += 2
        bonus_gains.append(f"前沿技术经验 (Agent/MCP/RAG等, +2)")
    elif frontier_match >= 1:
        bonus_score += 1
        bonus_gains.append(f"前沿技术经验 (+1)")

    # 跨行业经验
    industry_count = 0
    industries = ["电力", "电网", "能源", "医疗", "心理", "体育", "运动", "金融", "教育", "零售",
                  "power", "energy", "medical", "sports", "finance", "education", "retail"]
    for ind in industries:
        if ind.lower() in resume_text.lower():
            industry_count += 1
    if industry_count >= 3:
        bonus_score += 2
        bonus_gains.append(f"跨行业经验 ({industry_count}+行业, +2)")
    elif industry_count >= 1:
        bonus_score += 1
        bonus_gains.append(f"跨行业经验 (+1)")

    # 证书
    cert_keywords = ["证书", "认证", "计算机二级", "cet", "英语", "统计", "pmp"]
    cert_count = sum(1 for w in cert_keywords if w.lower() in resume_text.lower())
    if cert_count >= 3:
        bonus_score += 1
        bonus_gains.append("多项资格证书 (+1)")

    bonus_score = min(bonus_score, 10)

    # ── 总分计算 ──
    total_score = hard_skills_score + experience_score + academic_score + ats_score + bonus_score

    # 评级
    if total_score >= 85:
        grade = "A"
        grade_text = "高度匹配"
    elif total_score >= 70:
        grade = "B"
        grade_text = "较好匹配"
    elif total_score >= 50:
        grade = "C"
        grade_text = "部分匹配"
    else:
        grade = "D"
        grade_text = "严重不匹配"

    # ── 一句话定位 ──
    if role_info["role_mismatch"]:
        oneliner = f"「{role_info['candidate_role']} → {role_info['target_role']}：结构性错位」"
    elif total_score >= 70:
        oneliner = "「经历与JD核心要求高度吻合，可直接投递」"
    elif total_score >= 50:
        oneliner = "「部分匹配但存在明显短板，需针对性优化」"
    else:
        oneliner = "「核心要求存在结构性差距，建议调整岗位方向或大幅补课」"

    # ── TOP 3 建议 ──
    recommendations = generate_recommendations(
        kw_matches, hard_losses, acad_losses,
        publications, education, role_info,
        extra_hits
    )

    return {
        "meta": {
            "scoring_version": "1.0",
            "scoring_system": "5-dimension × 100",
            "target_role": role_info["target_role"],
            "candidate_role": role_info["candidate_role"],
            "role_mismatch": role_info["role_mismatch"],
        },
        "total_score": total_score,
        "grade": grade,
        "grade_text": grade_text,
        "oneliner": oneliner,
        "dimensions": {
            "hard_skills": {"score": hard_skills_score, "max": 30, "rate": round(hard_skills_score/30, 2),
                           "gains": hard_gains, "losses": hard_losses},
            "experience": {"score": experience_score, "max": 25, "rate": round(experience_score/25, 2),
                          "gains": exp_gains, "losses": exp_losses},
            "academic": {"score": academic_score, "max": 20, "rate": round(academic_score/20, 2),
                        "gains": acad_gains, "losses": acad_losses},
            "ats": {"score": ats_score, "max": 15, "rate": round(ats_score/15, 2),
                    "gains": ats_gains, "losses": ats_losses},
            "bonus": {"score": bonus_score, "max": 10, "rate": round(bonus_score/10, 2),
                     "gains": bonus_gains, "losses": bonus_losses},
        },
        "keyword_matches": kw_matches,
        "extra_hits": extra_hits,
        "education": education,
        "publications": publications,
        "recommendations": recommendations,
        "keyword_stats": {
            "total_jd_keywords": total_jd_kw,
            "full_match": sum(1 for k in kw_matches if k["match_status"] == "full"),
            "partial_match": sum(1 for k in kw_matches if k["match_status"] == "partial"),
            "miss": sum(1 for k in kw_matches if k["match_status"] == "miss"),
        },
    }


def generate_recommendations(kw_matches, hard_losses, acad_losses,
                              publications, education, role_info, extra_hits):
    """生成TOP 3修改建议"""
    recs = []

    # 建议1: 如果缺失critical/high权重硬技能 → 补课
    missing_critical = [k for k in kw_matches
                        if k["match_status"] == "miss" and k["weight"] in ("critical", "high")]
    if missing_critical:
        missing_names = [k["keyword"] for k in missing_critical[:4]]
        recs.append({
            "priority": 1,
            "roi": "最高优先级",
            "action_type": "需补做",
            "title": f"补充核心硬技能: {', '.join(missing_names)}",
            "detail": f"当前简历缺失这些JD明确要求的核心技术栈。建议通过在线课程/认证/开源项目补齐，并将项目经历写入简历。",
            "estimated_improvement": "+12~15分",
        })

    # 建议2: 改写已有内容
    if extra_hits:
        recs.append({
            "priority": 2,
            "roi": "高优先级",
            "action_type": "改写已有",
            "title": "将现有经验用JD术语重新包装",
            "detail": f"简历有{', '.join([h['keyword'] for h in extra_hits[:3]])}等经验但未用JD关键词表述。建议将这些内容与目标岗位核心要求建立连接。",
            "estimated_improvement": "+6~9分",
        })
    elif role_info["role_mismatch"]:
        recs.append({
            "priority": 2,
            "roi": "高优先级",
            "action_type": "改写已有",
            "title": "用目标岗位术语重构经历描述",
            "detail": f"当前角色为{role_info['candidate_role']}，需用{role_info['target_role']}的语言重写项目经历。",
            "estimated_improvement": "+5~8分",
        })

    # 建议3: 学术产出
    if not publications["has_paper"] or not publications["has_patent"]:
        recs.append({
            "priority": 3,
            "roi": "中优先级",
            "action_type": "需补做",
            "title": "产出至少1项学术成果",
            "detail": "发表技术博客/arXiv短文、参与开源项目、申请专利。对算法研究岗，学术产出是硬性门槛。",
            "estimated_improvement": "+4~6分",
        })

    # 确保有3条
    while len(recs) < 3:
        recs.append({
            "priority": len(recs) + 1,
            "roi": "低优先级",
            "action_type": "建议优化",
            "title": "优化简历排版和关键词密度",
            "detail": "增加JD关键词在简历中的出现频次，特别是权重较高的关键词需要自然融入各段经历。",
            "estimated_improvement": "+1~3分",
        })

    return recs[:3]


# ─── 跨岗位匹配度估算 ──────────────────────────────────────────

def cross_job_comparison(resume_text: str, current_score: int, target_role: str) -> list:
    """生成跨岗位匹配度对比表"""
    comparisons = []

    # 基础匹配分（从简历中提取的通用指标）
    years_exp = 0
    exp_match = re.search(r'(\d+)\s*年.*?(?:工作|经验)', resume_text)
    if exp_match:
        years_exp = int(exp_match.group(1))
    edu_info = extract_education(resume_text)
    pub_info = extract_publications(resume_text)

    has_agent = "agent" in resume_text.lower()
    has_rag = "rag" in resume_text.lower()
    has_mcp = "mcp" in resume_text.lower()
    has_python = "python" in resume_text.lower()
    has_ml = "机器学习" in resume_text.lower() or "machine learning" in resume_text.lower()
    has_product = "产品" in resume_text.lower()
    has_pm = "产品经理" in resume_text.lower()
    has_project_mgmt = "项目经理" in resume_text.lower() or "项目管理" in resume_text.lower()
    has_data = "数据分析" in resume_text.lower() or "数据挖掘" in resume_text.lower()

    # AI产品经理
    ai_pm_score = 50
    if has_product and has_ml:
        ai_pm_score += 15
    if has_agent and has_rag:
        ai_pm_score += 10
    if has_pm:
        ai_pm_score += 7
    if years_exp >= 5:
        ai_pm_score += 5
    ai_pm_score = min(ai_pm_score, 95)

    comparisons.append({
        "job": "AI 产品经理（大模型方向）",
        "score": ai_pm_score,
        "grade": "A" if ai_pm_score >= 85 else "B" if ai_pm_score >= 70 else "C",
        "match_points": ["AI产品经验", "大模型/Agent/RAG全栈理解"],
        "is_best_match": True,
    })

    # AI应用开发工程师
    ai_dev_score = 40
    if has_python:
        ai_dev_score += 10
    if has_agent or has_mcp:
        ai_dev_score += 10
    if has_rag:
        ai_dev_score += 5
    if has_ml:
        ai_dev_score += 5
    if years_exp >= 3:
        ai_dev_score += 5
    ai_dev_score = min(ai_dev_score, 90)
    comparisons.append({
        "job": "AI 应用开发工程师",
        "score": ai_dev_score,
        "grade": "B" if ai_dev_score >= 70 else "C",
        "match_points": ["MCP/Agent/Skills开发", "Python", "大模型生态"],
    })

    # AI解决方案架构师
    arch_score = 35
    if has_product:
        arch_score += 10
    if years_exp >= 8:
        arch_score += 10
    if has_ml:
        arch_score += 5
    if has_project_mgmt:
        arch_score += 5
    arch_score = min(arch_score, 85)
    comparisons.append({
        "job": "AI 解决方案架构师",
        "score": arch_score,
        "grade": "B-" if arch_score >= 60 else "C",
        "match_points": ["多行业AI落地", "产品规划", "项目管理"],
    })

    # 大模型数据工程师
    data_score = 30
    if has_data:
        data_score += 10
    if edu_info["has_master"] and edu_info["cs_related"]:
        data_score += 8
    elif edu_info["has_master"]:
        data_score += 5
    if has_python:
        data_score += 5
    data_score = min(data_score, 80)
    comparisons.append({
        "job": "大模型数据工程师",
        "score": data_score,
        "grade": "C",
        "match_points": ["数据清洗经验", "统计/数据背景"],
    })

    # 数据分析师
    analyst_score = 25
    if has_data:
        analyst_score += 12
    if edu_info["has_master"] and "统计" in resume_text:
        analyst_score += 8
    if has_python:
        analyst_score += 5
    analyst_score = min(analyst_score, 75)
    comparisons.append({
        "job": "数据分析师（AI方向）",
        "score": analyst_score,
        "grade": "C",
        "match_points": ["统计背景", "数据分析"],
    })

    # 当前目标岗位
    comparisons.append({
        "job": f"{target_role} ← 当前",
        "score": current_score,
        "grade": "D" if current_score < 50 else "C",
        "match_points": ["Python" if has_python else "", "大模型概念理解" if has_ml else ""],
        "is_current": True,
    })

    # 按分数排序
    comparisons.sort(key=lambda x: x["score"], reverse=True)
    return comparisons


# ─── CLI 入口 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="简历-JD 5维度匹配度评分引擎")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--resume-file", help="简历文本文件路径")
    input_group.add_argument("--resume-text", help="简历文本内容")

    jd_group = parser.add_mutually_exclusive_group(required=True)
    jd_group.add_argument("--jd-file", help="JD文本文件路径")
    jd_group.add_argument("--jd-text", help="JD文本内容")

    parser.add_argument("--output", required=True, help="输出JSON文件路径")
    parser.add_argument("--pretty", action="store_true", help="格式化JSON输出")

    args = parser.parse_args()

    # 读取输入
    if args.resume_file:
        with open(args.resume_file, "r", encoding="utf-8") as f:
            resume_text = f.read()
    else:
        resume_text = args.resume_text

    if args.jd_file:
        with open(args.jd_file, "r", encoding="utf-8") as f:
            jd_text = f.read()
    else:
        jd_text = args.jd_text

    # 执行评分
    result = score_resume(resume_text, jd_text)

    # 添加跨岗位对比
    result["cross_job_comparison"] = cross_job_comparison(
        resume_text, result["total_score"], result["meta"]["target_role"]
    )

    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        if args.pretty:
            json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            json.dump(result, f, ensure_ascii=False)

    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(f"[OK] Score: {result['total_score']}/100 (Grade: {result['grade']})")
    print(f"  Hard Skills: {result['dimensions']['hard_skills']['score']}/30")
    print(f"  Experience: {result['dimensions']['experience']['score']}/25")
    print(f"  Academic: {result['dimensions']['academic']['score']}/20")
    print(f"  ATS: {result['dimensions']['ats']['score']}/15")
    print(f"  Bonus: {result['dimensions']['bonus']['score']}/10")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
