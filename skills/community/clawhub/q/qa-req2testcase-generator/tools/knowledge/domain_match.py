#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.utils import _read_json, _write_json, _ensure_dir

# knowledge/domain_match.py — 域名→业务域匹配
import os, json, re

def _detect_domain(text, default="trade"):
    text_lower = text.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return domain
    return default


# ============================================================
# V4.0.0: 云端评审工具推送相关辅助函数
# ============================================================

# 域名→文件名映射（显式字典 + fallback）
DOMAIN_FILENAME_MAP = {
    "客户域": "客户", "交易域": "交易", "资管域": "资管", "自营域": "自营",
    "投顾域": "投顾", "投研域": "投研", "投行业务域": "投行", "机构业务域": "机构",
    "清算托管域": "清算托管", "风控合规域": "风控合规", "行情资讯域": "行情资讯", "互联网终端域": "互联网终端"
}

def _domain_to_filename(domain):
    """域名→文件名（与_sync_review_experience/P6注入共用）"""
    if domain in DOMAIN_FILENAME_MAP:
        return DOMAIN_FILENAME_MAP[domain]
    return domain.replace("域", "").replace("业务", "")


def _load_project_domain_mapping(skill_dir):
    """读取项目名称→业务域映射配置。
    V4.0.0: 支持根据项目名自动关联业务域知识库。
    """
    mapping_path = os.path.join(skill_dir, "config", "project_domain_mapping.json")
    if os.path.exists(mapping_path):
        try:
            return _read_json(mapping_path)
        except Exception:
            pass
    return {"mappings": [], "domain_knowledge_map": {}}


def _match_project_to_domains(requirement_text, skill_dir):
    """V4.0.0: 根据需求文本中的项目名自动匹配业务域。
    
    匹配逻辑：
    1. 扫描需求文本中的关键词（项目名），命中则返回对应的业务域列表
    2. V4.0.1: 同义词模糊匹配，扫描需求文本中的同义词关键词
    3. 匹配优先级：项目关键词命中 > 同义词命中（合并去重）
    
    Returns:
        dict: {"domains": [...], "knowledge_files": [...], "matched_projects": [...], "matched_synonyms": [...]}
    """
    mapping = _load_project_domain_mapping(skill_dir)
    mappings = mapping.get("mappings", [])
    domain_knowledge_map = mapping.get("domain_knowledge_map", {})
    synonyms = mapping.get("synonyms", {})
    
    if not requirement_text or (not mappings and not synonyms):
        return {"domains": [], "knowledge_files": [], "matched_projects": [], "matched_synonyms": []}
    
    requirement_lower = requirement_text.lower()
    
    # 第一层：项目关键词精确匹配
    matched_domains = set()
    matched_projects = []
    
    for item in mappings:
        keywords = item.get("project_keywords", [])
        for kw in keywords:
            if kw.lower() in requirement_lower:
                for domain in item.get("domains", []):
                    matched_domains.add(domain)
                matched_projects.append(kw)
                break  # 一个mapping只需匹配一次
    
    # 第二层：同义词模糊匹配（子串匹配，仅作为辅助信号）
    # 注意：同义词是高频2字词（如"客户""交易"），会广泛命中
    # 设计意图：同义词匹配到的域只用于知识注入，不影响 project_name 判定
    synonym_matched_domains = set()
    matched_synonyms = []
    for keyword, domain in synonyms.items():
        if keyword.lower() in requirement_lower:
            synonym_matched_domains.add(domain)
            matched_synonyms.append(keyword)
    
    # 合并去重：项目关键词匹配 + 同义词匹配
    all_domains = matched_domains | synonym_matched_domains
    
    # 映射到知识库文件
    knowledge_files = []
    for domain in sorted(all_domains):
        kf = domain_knowledge_map.get(domain)
        if kf:
            knowledge_files.append({"domain": domain, "file": kf})
    
    return {
        "domains": sorted(all_domains),
        "knowledge_files": knowledge_files,
        "matched_projects": matched_projects,
        "matched_synonyms": matched_synonyms
    }

