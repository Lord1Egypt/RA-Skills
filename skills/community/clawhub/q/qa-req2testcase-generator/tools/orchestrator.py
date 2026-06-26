#!/usr/bin/env python3
"""
V3.3.1 Orchestrator - 测试用例生成流程控制器
代码控制流程,Agent只负责生成内容。

用法:
  由SKILL.md指导Agent调用:
  exec: python3 {SKILL_DIR}/tools/orchestrator.py --action <action> [--args ...]

支持的action:
  init          - 初始化任务(创建task_id, DATA_DIR)
  onboarding    - 执行Onboarding检查(环境/Python/路径)
  step0         - 接收需求,写入task_meta
  step0_8_prep  - PX图片抽取+选图(返回待Agent理解的图片列表)
  step0_8_save  - 保存Agent的图片理解结果+调用image_enhance
  step_run      - 执行P0-P7任一步骤(准备prompt输入,校验Agent输出,写文件+guard)
  step7_export  - 调用export_excel.py导出
  status        - 查看当前任务状态
  resume        - 断点续跑(检测已完成步骤,返回下一步)
"""

import argparse
import json
import hashlib
import os
import sys
import time
import shlex
import subprocess
import glob
from pathlib import Path


# ============================================================
# 常量
# ============================================================

SKILL_VERSION = "4.12.6"
STEPS = ["onboarding", "step0", "step0_8", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "step7"]
GATE_STEPS = ["onboarding", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]

# # V4.7.3: 子Agent环境检测函数
def _is_sub_agent_session():
    """检测当前是否在子Agent会话中执行。

    P6用例生成任务量大(每批50条用例+大量上下文读取),
    在子Agent的30分钟超时限制下无法完成,必须拒绝。

    检测策略(多层fallback):
      1. 环境变量 OPENCLAW_IS_SUBAGENT=1 → 直接判定
      2. 进程树检测: 祖父进程也是openclaw/node → 判定为子Agent嵌套
      3. 无法判定时放行(fail-open,避免误杀)
    """
    import subprocess as _sp

    # 策略1: 环境变量显式标记(OpenClaw运行时可设置)
    if os.environ.get('OPENCLAW_IS_SUBAGENT') == '1':
        return True

    # 策略2: 进程树检测(两层openclaw嵌套=子Agent→exec→脚本)
    try:
        ppid = os.getppid()
        # 获取父进程信息
        r = _sp.run(['ps', '-o', 'ppid=,comm=', '-p', str(ppid)],
                    capture_output=True, text=True, timeout=3)
        if r.returncode != 0 or not r.stdout.strip():
            return False
        parts = r.stdout.strip().split()
        if len(parts) < 2:
            return False
        gppid, pname = parts[0], parts[1]
        # 父进程是openclaw/node → 进一步检查祖父进程
        if ('openclaw' in pname.lower() or 'node' in pname.lower()):
            r2 = _sp.run(['ps', '-o', 'comm=', '-p', gppid],
                        capture_output=True, text=True, timeout=3)
            gpname = r2.stdout.strip().lower()
            if 'openclaw' in gpname or 'node' in gpname:
                # 两层openclaw嵌套 → 子Agent环境
                return True
    except Exception:
        pass

    return False

# HMAC固定密钥(V4.0.1: 避免文件内容变化导致密钥断裂)
import sys, os, json, hashlib, hmac, time, subprocess, glob, re, argparse

# V4.0.1: 模块化拆分 - 共享常量/工具/状态/安全到core/knowledge
# V4.1.8: 确保skill_v4根目录在sys.path,以便import knowledge模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import constants as _c, utils as _u, state as _s, security as _sec
from knowledge import domain_match as _dm, cloud_sync as _cs
from gate_checker import run_gate_checks as _run_gate_checks, evaluate_gate as _evaluate_gate, format_gate_report as _format_gate_report

# V4.8.0: 弱模型适配 - 模型检测 + 引导卡生成(按需导入,避免循环)
_model_detect = None
_p6_guide = None

def _get_model_detect():
    global _model_detect
    if _model_detect is None:
        from tools import model_detect as _md
        _model_detect = _md
    return _model_detect

def _get_p6_guide():
    global _p6_guide
    if _p6_guide is None:
        from tools import p6_guide as _pg
        _p6_guide = _pg
    return _p6_guide

HMAC_SECRET = "xy-req2testcase-v4-hmac-2026"

# P6分批大小(V4.0.1: 提取为全局常量,便于灰度调整)
P6_BATCH_SIZE = 8

# V4.8.5: 从 data_dir 读取 model_tier(用于 Gate 分级等场景)
def _get_model_tier_for_dir(data_dir: str) -> str:
    """读取 model_tier。优先级:state > OPENCLAW_MODEL > 默认LOW"""
    state_path = os.path.join(data_dir, "orchestrator_state.json")
    if os.path.exists(state_path):
        try:
            st = _read_json(state_path)
            tier = st.get("model_tier", "")
            if tier:
                return tier
        except Exception:
            pass
    # 兜底:环境变量
    env_model = os.environ.get('OPENCLAW_MODEL', '') or os.environ.get('OPENCLAW_DEFAULT_MODEL', '')
    if env_model:
        return _get_model_detect().classify(env_model)
    return "LOW"  # 保守策略


# ============================================================
# V4.6.14: P6动态分批策略
# ============================================================

import math


def calculate_complexity_score(test_point: dict) -> str:
    """
    V4.6.14: 测试点复杂度打分

    返回: "simple" / "medium" / "complex"

    维度:
      - 描述长度: <50=simple, 50-150=medium, >150=complex
      - 操作动作关键词数量
      - 多实体关键词(多/多个/批量/并发/跨/不同)
    """
    desc = test_point.get("description", "") or ""
    length = len(desc)

    # 动作关键词
    action_keywords = ["验证", "检查", "确认", "输入", "点击", "选择",
                       "提交", "审批", "查询", "删除", "修改", "登录",
                       "登出", "上传", "下载", "导出", "导入"]
    action_count = sum(1 for kw in action_keywords if kw in desc)

    # 多实体关键词
    multi_keywords = ["多", "多个", "批量", "并发", "跨", "不同",
                      "所有", "全部", "各种", "各类"]
    multi_count = sum(1 for kw in multi_keywords if kw in desc)

    # 综合打分
    if length > 150 or action_count >= 5 or multi_count >= 2:
        return "complex"
    elif length > 50 or action_count >= 3:
        return "medium"
    else:
        return "simple"


def calculate_dynamic_batches(test_points: list, max_batches: int = 5) -> dict:
    """
    V4.6.14: 根据复杂度动态计算批次

    策略:
      - simple每批25个,medium每批15个,complex每批8个
      - 最多5批,超出则提升每批处理量

    Returns:
        dict: {
            "total_batches": int,
            "batches": [{"start": int, "end": int, "complexity": str}],
        }
    """
    if not test_points:
        return {"total_batches": 0, "batches": []}

    # 计算每个测试点的复杂度
    complexities = [calculate_complexity_score(tp) for tp in test_points]

    # 计算各复杂度测试点数量
    simple_count = complexities.count("simple")
    medium_count = complexities.count("medium")
    complex_count = complexities.count("complex")

    # 计算理论批次
    simple_batches = math.ceil(simple_count / 25) if simple_count > 0 else 0
    medium_batches = math.ceil(medium_count / 15) if medium_count > 0 else 0
    complex_batches = math.ceil(complex_count / 8) if complex_count > 0 else 0
    total_theoretical = simple_batches + medium_batches + complex_batches

    # 如果不超过max_batches,直接使用动态分批
    if total_theoretical <= max_batches:
        batches = []
        idx = 0
        for complexity, batch_size in [("simple", 25), ("medium", 15), ("complex", 8)]:
            count_for_type = complexities.count(complexity)
            if count_for_type == 0:
                continue
            remaining = count_for_type
            while remaining > 0:
                batch_count = min(batch_size, remaining)
                start = idx
                end = idx + batch_count
                batches.append({
                    "start": start,
                    "end": end,
                    "complexity": complexity,
                    "count": batch_count,
                })
                idx = end
                remaining -= batch_count

        return {
            "total_batches": len(batches),
            "batches": batches,
            "strategy": "dynamic",
        }

    # 超过max_batches,使用均匀分批
    per_batch = math.ceil(len(test_points) / max_batches)
    batches = []
    for i in range(max_batches):
        start = i * per_batch
        end = min((i + 1) * per_batch, len(test_points))
        if start >= len(test_points):
            break
        batches.append({
            "start": start,
            "end": end,
            "complexity": "mixed",
            "count": end - start,
        })

    return {
        "total_batches": len(batches),
        "batches": batches,
        "strategy": "uniform",
    }


# ============================================================
# V4.6.14: 骨架锁定智能决策
# ============================================================

import re as _re


def extract_operation_semantics(steps_text: str) -> set:
    """
    V4.6.14: 提取步骤操作语义:动作+对象

    从步骤文本中提取「点击XX」「输入XX」「选择XX」等语义单元。
    用于语义相似度计算。

    Returns: set of semantic units
    """
    if not steps_text:
        return set()

    # 动作词列表
    actions = ["点击", "输入", "选择", "提交", "审批", "查询",
               "删除", "修改", "登录", "登出", "打开", "关闭",
               "上传", "下载", "导出", "导入", "刷新", "勾选"]

    semantics = set()
    # 先按行拆分,避免跨行匹配产生碎片
    lines = steps_text.split('\n')
    for line in lines:
        for action in actions:
            # 匹配「点击XX」「输入XXX」等模式,动作词+最多15个字符
            pattern = f"({action}[^\n。!?,、;]{{0,15}})"
            match = _re.search(pattern, line)
            if match:
                m = match.group(1).strip()
                if m and len(m) >= len(action) + 2:
                    semantics.add(m)

    return semantics


def semantic_similarity(steps_a: str, steps_b: str) -> float:
    """
    V4.6.14: 语义相似度计算(Jaccard)

    比较两个步骤文本的语义相似度。

    Returns: 0.0 ~ 1.0 (1.0表示完全相似)
    """
    sem_a = extract_operation_semantics(steps_a)
    sem_b = extract_operation_semantics(steps_b)

    if not sem_a and not sem_b:
        return 1.0  # 两个都无语义,视为相似
    if not sem_a or not sem_b:
        return 0.0

    intersection = len(sem_a & sem_b)
    union = len(sem_a | sem_b)
    return intersection / union if union > 0 else 0.0


def skeleton_override_decision(
    agent_steps: str,
    skeleton_steps: str,
    priority: str
) -> str:
    """
    V4.6.14: 骨架覆盖决策

    决定在保存用例时是否用骨架内容覆盖Agent输出。

    决策逻辑:
      - P0用例:必须使用骨架的priority/is_smoke
      - 语义相似度>70%:骨架内容更可靠,用骨架覆盖steps
      - 语义相似度≤70%:Agent有差异化创作,保留Agent输出
      - 骨架步骤为空/无意义:保留Agent输出

    Returns: "use_skeleton" | "keep_agent"
    """
    # P0用例必须用骨架的元数据
    if priority == "P0":
        return "use_skeleton"

    # 骨架步骤为空,保留Agent
    if not skeleton_steps or len(skeleton_steps.strip()) < 10:
        return "keep_agent"

    # 计算语义相似度
    sim = semantic_similarity(agent_steps, skeleton_steps)

    if sim > 0.7:
        return "use_skeleton"
    else:
        return "keep_agent"


# P0必需顶层字段
# === 各步骤必需字段(以云端实际JSON为真源,2026-04-29统一) ===
P0_REQUIRED_FIELDS = ["quality_score", "blocks", "objective"]
P1_REQUIRED_FIELDS = ["feature_tree"]  # 云端实际输出用feature_tree
P3_REQUIRED_FIELDS = ["risk_points"]  # 云端实际输出用risk_points
P4_REQUIRED_FIELDS = ["pci_list"]  # 云端实际输出用pci_list
P5_REQUIRED_FIELDS = ["test_points", "merge_log"]
P6_REQUIRED_FIELDS = ["testcases"]
P7_REQUIRED_FIELDS = ["gate_result"]  # 云端实际输出gate_result,不是quality_check

# 域识别关键词
# ============================================================
# 自动发现 SKILL_DIR(V3.0.0-patch3)
# ============================================================

DEFAULT_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve_skill_dir(cli_value=""):
    """自动发现skill_dir,带目录完整性校验"""
    candidate = cli_value or DEFAULT_SKILL_DIR
    required_files = [
        os.path.join(candidate, "tools", "export_excel.py"),
        os.path.join(candidate, "tools", "truncation_guard.py"),
        os.path.join(candidate, "prompts", "P0_requirement_structuring.md"),
    ]
    missing = [p for p in required_files if not os.path.exists(p)]
    if missing:
        # 尝试DEFAULT_SKILL_DIR作为兜底
        if cli_value and cli_value != DEFAULT_SKILL_DIR:
            return resolve_skill_dir("")  # 递归用默认值重试
        raise ValueError(f"skill_dir无效({candidate}),缺失: {[os.path.basename(p) for p in missing[:3]]}")
    return candidate


# ============================================================
# 自动发现最近任务(V3.0.0-patch3)
# ============================================================

def find_latest_task():
    """查找最近的未完成任务,返回(task_id, data_dir)或(None, None)"""
    base = os.path.expanduser("~/.openclaw/workspace/data")
    if not os.path.exists(base):
        return None, None
    tasks = sorted(glob.glob(os.path.join(base, "task_*")), reverse=True)
    for task_dir in tasks[:3]:  # 只看最近3个,减少串task风险
        state_path = os.path.join(task_dir, "orchestrator_state.json")
        if os.path.exists(state_path):
            try:
                state = _read_json(state_path)
                tid = state.get("task_id", "")
                # 未完成的任务(没有step7)
                if "step7" not in state.get("completed_steps", []):
                    return tid, task_dir
            except Exception:
                pass
    return None, None


# ============================================================
# P6模式推荐映射表 (V3.4.0)
# ============================================================
import re

DOMAIN_KEYWORDS = {
    "trade": ["交易", "委托", "撤单", "成交", "清算", "结算", "资金冻结", "T+1", "smt", "smart station", "银证转账"],
    "asset_mgmt": ["资管", "净值", "申赎", "申购", "赎回", "衍生品", "期货", "期权", "保证金", "基金理财"],
    "risk_ctrl": ["风控", "预警", "限额", "合规检查", "风险控制", "适当性"],
    "crm": ["客户", "跟进", "开户", "KYC", "客户经理", "客户关系", "crm"],
    "investment_advice": ["投顾", "债券投顾", "投顾分润", "分润", "投资顾问", "财富梦工厂"],
    "etrading": ["网上营业厅", "APP", "适当性", "产品推荐", "在线交易", "移动端", "H5", "优理宝"],
    "ops_mgmt": ["运营", "活动", "营销", "后台管理", "数据报表", "统计", "导出"],
    "compliance": ["合规", "证书", "从业", "监管", "报送", "资质", "执照"],
    "institutional": ["机构", "主经纪商", "pb", "机构户", "智达"],
    "it_infra": ["部署", "监控", "服务器", "权限配置", "变更", "IT", "基础设施", "投行", "承销", "IPO"],
}


# ============================================================
# 工具函数
# ============================================================

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _file_exists(path):
    return os.path.exists(path) and os.path.getsize(path) > 10

def _sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def _detect_domain(text, default="trade"):
    """检测业务域,返回API标准域名"""
    if not text:
        return INTERNAL_TO_API_DOMAIN.get(default, "客户域")
    text_lower = text.lower().strip()
    # 优先精确匹配
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() == text_lower:
                api_domain = INTERNAL_TO_API_DOMAIN.get(domain)
                if api_domain:
                    return api_domain
    # 其次包含匹配
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                api_domain = INTERNAL_TO_API_DOMAIN.get(domain)
                if api_domain:
                    return api_domain
    return INTERNAL_TO_API_DOMAIN.get(default, "客户域")


# ============================================================
# V4.0.0: 云端评审工具推送相关辅助函数
# ============================================================

# 域名→文件名映射(显式字典 + fallback)
# 内部域名到API业务域名的映射(用于评审推送)
INTERNAL_TO_API_DOMAIN = {
    "trade": "交易域",
    "asset_mgmt": "资管域",
    "risk_ctrl": "风控合规域",
    "crm": "客户域",
    "investment_advice": "投顾域",
    "etrading": "互联网终端域",
    "ops_mgmt": "运营管理域",
    "compliance": "合规域",
    "institutional": "机构业务域",
    "it_infra": "投行业务域",
    # 默认
    None: "客户域",
}

DOMAIN_FILENAME_MAP = {
    "客户域": "客户", "交易域": "交易", "资管域": "资管", "自营域": "自营",
    "投顾域": "投顾", "投研域": "投研", "投行业务域": "投行", "机构业务域": "机构",
    "清算托管域": "清算托管", "风控合规域": "风控合规", "行情资讯域": "行情资讯", "互联网终端域": "互联网终端"
}

def _domain_to_filename(domain):
    """域名→文件名(与_sync_review_experience/P6注入共用)"""
    if domain in DOMAIN_FILENAME_MAP:
        return DOMAIN_FILENAME_MAP[domain]
    return domain.replace("域", "").replace("业务", "")

def _load_cloud_config(skill_dir, runtime_api_key=None):
    """读取 skill_v4/config/cloud.json 配置文件。
    如不存在返回默认配置(enabled=false),不抛异常。

    V4.1.2: api_key优先从runtime_api_key参数读取(Onboarding时输入,保存在task目录.cache文件),
    其次从cloud.json读取。避免api_key存储在配置文件中。
    """
    config_path = os.path.join(skill_dir, "config", "cloud.json")
    config = None
    if os.path.exists(config_path):
        try:
            config = _read_json(config_path)
        except Exception:
            pass

    if config is None:
        config = {
            "review_tool": {
                "enabled": False,
                "api_url": "",
                "frontend_url": "",
                "api_key": "",
                "auto_push": False,
            },
            "experience_sync": {
                "enabled": False,
            }
        }

    # V4.1.2: runtime_api_key优先(由调用方从task目录的.image_api_key文件读取后传入)
    if runtime_api_key and runtime_api_key.strip():
        config["review_tool"]["api_key"] = runtime_api_key.strip()

    return config


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

    匹配逻辑:
    1. 扫描需求文本中的关键词(项目名),命中则返回对应的业务域列表
    2. V4.0.1: 同义词模糊匹配,扫描需求文本中的同义词关键词
    3. 匹配优先级:项目关键词命中 > 同义词命中(合并去重)

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

    # 第一层:项目关键词精确匹配
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

    # 第二层:同义词模糊匹配(子串匹配,仅作为辅助信号)
    # 注意:同义词是高频2字词(如"客户""交易"),会广泛命中
    # 设计意图:同义词匹配到的域只用于知识注入,不影响 project_name 判定
    synonym_matched_domains = set()
    matched_synonyms = []
    for keyword, domain in synonyms.items():
        if keyword.lower() in requirement_lower:
            synonym_matched_domains.add(domain)
            matched_synonyms.append(keyword)

    # 合并去重:项目关键词匹配 + 同义词匹配
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


def _should_push_to_review_tool(config):
    """V4.12.6: 默认开启推送,仅api_key非空即推送
    条件: api_key非空即可(优先runtime key → cloud.json → 环境变量)
    无api_key时提示用户配置,不静默跳过
    """
    rt = config.get("review_tool", {})
    if not rt.get("api_key", "").strip():
        return False
    return True


def _push_to_review_tool(data_dir, task_id, config):
    """推送用例到云端评审工具。

    流程:
    1. 读取 p6_output.json
    2. HTTP POST 到 /api/projects/import
    3. 完整的HTTP响应校验(raise_for_status + project_id存在性)
    4. 异常分类处理(Timeout/HTTPError/其他)
    5. 失败时记录到重试队列 queue/pending_reviews.jsonl
    6. 返回 review_url 或 None

    Args:
        data_dir: 任务数据目录
        task_id: 任务ID
        config: cloud.json 配置字典

    Returns:
        review_url (str) 或 None(推送失败时)
    """
    import requests

    # V4.1.8: 幂等检查--若上次推送成功记录存在,则跳过(避免HMAC断裂重跑时重复推送)
    push_marker = os.path.join(data_dir, ".review_push_done")
    if os.path.exists(push_marker):
        print(f"[_push_to_review_tool] 跳过:{task_id} 已推送过", file=sys.stderr)
        return None

    # 读取 p6_output.json
    p6_path = os.path.join(data_dir, "p6_output.json")
    if not os.path.exists(p6_path):
        _enqueue_failed_push(data_dir, task_id, config, "p6_output.json不存在")
        return None

    try:
        p6_data = _read_json(p6_path)
    except Exception as e:
        _enqueue_failed_push(data_dir, task_id, config, f"p6_output.json读取失败: {e}")
        return None

    rt_cfg = config.get("review_tool", {})
    api_url = rt_cfg.get("api_url", "http://localhost:4174")
    api_key = rt_cfg.get("api_key", "")
    frontend_url = rt_cfg.get("frontend_url", api_url.replace(":4174", ""))

    # 读取 task_meta 获取 domain 信息
    meta_path = os.path.join(data_dir, "task_meta.json")
    domain = "未分类"
    requirement_id = ""
    project_name = ""
    if os.path.exists(meta_path):
        try:
            meta = _read_json(meta_path)
            domain = _detect_domain(meta.get("domain", ""))
            requirement_id = meta.get("task_id", "")
            project_name = meta.get("project_name", "")
        except Exception:
            pass

    # 构造请求
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    # V4.1.8: 字段映射转换(p6_output格式 → API期望格式)
    # 兼容两种格式:嵌套结构 {fields:{...}} 或扁平结构 {...}
    raw_cases = p6_data.get("testcases", [])
    testcases_for_api = []
    for c in raw_cases:
        nested = c.get("fields")
        fields = nested if isinstance(nested, dict) and nested else c
        # 字段名转换
        # V4.1.8: 补充 isSmoke 字段(之前漏推,导致评审工具冒烟用例=0)
        raw_smoke = fields.get("is_smoke", False)
        is_smoke_bool = _is_smoke(raw_smoke)  # 统一判断逻辑
        tc = {
            "case_id": fields.get("case_id", ""),
            "title": fields.get("title", ""),
            "priority": fields.get("priority", ""),
            "isSmoke": is_smoke_bool,  # V4.1.8: 修复冒烟用例推送
            "module": fields.get("test_suite", "") or fields.get("module", ""),
            "menu_path": fields.get("menu_path", ""),
            "precondition": fields.get("preconditions", "") or fields.get("precondition", ""),
            "steps": fields.get("steps", ""),
            "expected_results": fields.get("expected_results", ""),
        }
        # steps/expected_results转为数组
        if isinstance(tc["steps"], str):
            tc["steps"] = [s.strip() for s in tc["steps"].split("\n") if s.strip()]
        if isinstance(tc["expected_results"], str):
            tc["expected_results"] = [e.strip() for e in tc["expected_results"].split("\n") if e.strip()]
        testcases_for_api.append(tc)

    payload = {
        "task_id": task_id,
        "testcases": testcases_for_api,
        "metadata": {
            "domain": domain,
            "requirement_id": requirement_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "project_name": project_name,
        }
    }

    print(f"DEBUG: POST {api_url}/api/projects/import", flush=True)
    if payload.get('testcases'):
        tc0 = payload['testcases'][0]
    try:
        response = requests.post(
            f"{api_url}/api/projects/import",
            json=payload,
            headers=headers,
            timeout=10
        )
        # 完整的HTTP响应校验
        response.raise_for_status()
        result = response.json()

        # project_id 存在性校验(兼容 result.data.project_id 格式)
        raw_data = result.get("data")
        data = raw_data if isinstance(raw_data, dict) else result  # 防御:data为null/非dict时fallback
        project_id = data.get("project_id") or result.get("project_id")
        if not project_id:
            raise ValueError(f"服务端响应缺少project_id: {result}")
        review_url = data.get("review_url") or result.get("review_url") or f"{frontend_url}/?project={project_id}"
        # V4.1.8: 推送成功后写入marker,防止重跑时重复推送
        try:
            with open(push_marker, "w") as f:
                f.write(f"{project_id}\n{review_url}")
        except Exception:
            pass
        return review_url

    except requests.exceptions.Timeout:
        # 超时异常:记录重试队列
        error_msg = "推送超时(10秒),请检查网络或服务端状态"
        _enqueue_failed_push(data_dir, task_id, config, error_msg)
        return None
    except requests.exceptions.HTTPError as e:
        # HTTP错误异常:记录重试队列
        status_code = e.response.status_code if e.response else "unknown"
        error_msg = f"推送失败: HTTP {status_code}"
        _enqueue_failed_push(data_dir, task_id, config, error_msg)
        return None
    except Exception as e:
        # 其他异常:记录重试队列
        error_msg = f"推送异常: {str(e)[:200]}"
        _enqueue_failed_push(data_dir, task_id, config, error_msg)
        return None


def _enqueue_failed_push(data_dir, task_id, config, error_msg, push_type="p6_testcases"):
    """推送失败时记录到重试队列 queue/pending_reviews.jsonl"""
    # 队列目录放在 data_dir 同级的 queue 目录下
    base_dir = os.path.dirname(data_dir) if data_dir else os.path.expanduser("~/.openclaw/workspace/data")
    queue_dir = os.path.join(base_dir, "queue")
    _ensure_dir(queue_dir)
    queue_path = os.path.join(queue_dir, "pending_reviews.jsonl")

    entry = {
        "task_id": task_id,
        "data_dir": data_dir,
        "push_type": push_type,
        "timestamp": time.time(),
        "error": error_msg,
        "retry_count": 0,
    }
    try:
        with open(queue_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 队列写入失败不阻塞主流程


def _push_p0p1_to_review_tool(data_dir, task_id, config):
    """推送P0/P1摘要数据到云端评审工具。

    V4.0.0: 段落3完成后推送P0/P1报告摘要,与P6用例推送独立。
    推送是"尽力而为",失败不影响主流程。

    Args:
        data_dir: 任务数据目录
        task_id: 任务ID
        config: cloud.json 配置字典

    Returns:
        dict: {"success": bool, "review_url": str或None, "message": str}
    """
    import requests

    rt_cfg = config.get("review_tool", {})
    api_url = rt_cfg.get("api_url", "http://localhost:4174")
    api_key = rt_cfg.get("api_key", "")
    frontend_url = rt_cfg.get("frontend_url", api_url.replace(":4174", ""))

    # 读取 p0_output.json
    p0_path = os.path.join(data_dir, "p0_output.json")
    p0_data = {}
    if os.path.exists(p0_path):
        try:
            p0_data = _read_json(p0_path)
        except Exception:
            pass

    # 读取 p1_output.json
    p1_path = os.path.join(data_dir, "p1_output.json")
    p1_data = {}
    if os.path.exists(p1_path):
        try:
            p1_data = _read_json(p1_path)
        except Exception:
            pass

    if not p0_data and not p1_data:
        error_msg = "p0_output.json和p1_output.json均不存在或读取失败"
        _enqueue_failed_push(data_dir, task_id, config, error_msg, push_type="p0p1_report")
        return {"success": False, "review_url": None, "message": error_msg}

    # 读取 task_meta 获取 domain 等信息
    meta_path = os.path.join(data_dir, "task_meta.json")
    domain = "未分类"
    project_name = ""
    if os.path.exists(meta_path):
        try:
            meta = _read_json(meta_path)
            domain = _detect_domain(meta.get("domain", ""))
            project_name = meta.get("project_name", "")
        except Exception:
            pass

    # 统计P1模块数和功能点数
    p1_module_count = 0
    p1_feature_count = 0
    if p1_data:
        ft = p1_data.get("feature_tree", {})
        modules = ft.get("modules", []) if isinstance(ft, dict) else []
        if not modules:
            modules = p1_data.get("modules", [])
        p1_module_count = len(modules)
        for mod in modules:
            p1_feature_count += len(mod.get("children", []))

    # 获取P0 score
    p0_score = p0_data.get("score", None)
    if p0_score is None:
        p0_score = p0_data.get("blocks", {}).get("score", None)

    # 构造推送payload
    payload = {
        "task_id": task_id,
        "metadata": {
            "domain": domain,
            "requirement_id": task_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "push_type": "p0p1_report",
            "project_name": project_name,
        },
        "testcases": [],
        "p0p1_summary": {
            "p0_score": p0_score,
            "p1_module_count": p1_module_count,
            "p1_feature_count": p1_feature_count,
            "p1_modules": [mod.get("name", "") for mod in (modules or [])[:10]],
            "report_file": "p0p1_report.md",
            "clarification_questions": p0_data.get("blocks", {}).get("clarification_questions", []),
            "unknowns": p0_data.get("blocks", {}).get("unknowns", []),
        }
    }

    # 构造请求头
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    try:
        response = requests.post(
            f"{api_url}/api/projects/import",
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        # 兼容 result.data.project_id 格式(与 _push_to_review_tool 一致)
        raw_data = result.get("data")
        data = raw_data if isinstance(raw_data, dict) else result  # 防御:data为null/非dict时fallback
        project_id = data.get("project_id") or result.get("project_id")
        if not project_id:
            raise ValueError(f"服务端响应缺少project_id: {result}")
        review_url = data.get("review_url") or result.get("review_url") or f"{frontend_url}/?project={project_id}"
        return {"success": True, "review_url": review_url, "message": "P0/P1摘要已推送到评审工具"}

    except requests.exceptions.Timeout:
        error_msg = "推送超时(10秒),请检查网络或服务端状态"
        _enqueue_failed_push(data_dir, task_id, config, error_msg, push_type="p0p1_report")
        return {"success": False, "review_url": None, "message": error_msg}
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else "unknown"
        error_msg = f"P0/P1推送失败: HTTP {status_code}"
        _enqueue_failed_push(data_dir, task_id, config, error_msg, push_type="p0p1_report")
        return {"success": False, "review_url": None, "message": error_msg}
    except Exception as e:
        error_msg = f"P0/P1推送异常: {str(e)[:200]}"
        _enqueue_failed_push(data_dir, task_id, config, error_msg, push_type="p0p1_report")
        return {"success": False, "review_url": None, "message": error_msg}


def _check_api_features(data_dir):
    """V3.3.2: 判断是否需要接口测试规则(检查P0 operations和P1 feature names)"""
    API_KEYWORDS = {"接口", "API", "api", "推送", "webhook", "回调", "对接", "同步", "通知", "HTTP", "http"}
    # 检查P0 operations
    p0_path = os.path.join(data_dir, "p0_output.json")
    if os.path.exists(p0_path):
        try:
            p0_data = _read_json(p0_path)
            ops = p0_data.get("blocks", {}).get("operations", [])
            for op in ops:
                name = op.get("name", "") + op.get("trigger", "")
                if any(kw in name for kw in API_KEYWORDS):
                    return True
        except Exception:
            pass
    # 检查P1 feature names
    p1_path = os.path.join(data_dir, "p1_output.json")
    if os.path.exists(p1_path):
        try:
            p1_data = _read_json(p1_path)
            ft = p1_data.get("feature_tree", {})
            ft_modules = ft.get("modules", []) if isinstance(ft, dict) else []
            if not ft_modules:
                ft_modules = p1_data.get("modules", [])
            for mod in ft_modules:
                for feat in mod.get("children", []):
                    if any(kw in feat.get("name", "") for kw in API_KEYWORDS):
                        return True
        except Exception:
            pass
    return False


def _get_case_field(case, field, default=""):
    """从P6用例中读取字段值,兼容两种结构:
    1. 扁平结构:case.get(field)
    2. 嵌套结构:case.get("fields", {}).get(field)

    V3.2.4新增:修复P6数据结构为嵌套fields时,
    quality_check/p6_merge/step7_export/export_excel全部读不到字段的致命Bug。
    """
    val = case.get(field)
    if val is not None and val != "":
        return val
    fields = case.get("fields")
    if isinstance(fields, dict):
        val = fields.get(field)
        if val is not None:
            return val
    return default


def _set_case_field(case, field, value):
    """V4.12.6: 设置用例字段值,兼容扁平结构和嵌套fields结构
    对应 _get_case_field 的写入端
    """
    if "fields" in case and isinstance(case.get("fields"), dict):
        case["fields"][field] = value
    else:
        case[field] = value


def _is_smoke(value):
    """V3.2.8: 统一is_smoke判断逻辑,兼容所有格式。
    返回True/False,消除多处重复的判断代码。
    支持: True, "true", "是", "Y", "yes", 1
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        return value.lower() in ("true", "是", "y", "yes", "1")
    return False


def _write_text(path, content):
    """写入文本文件,UTF-8编码"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ============================================================
# HMAC签名机制 (V3.2.6: 防止Agent伪造gate pass)
# ============================================================

import hmac as _hmac_mod

# V3.5.2: 全局变量记录当前执行的action,只在main()的dispatch时设置
# Agent即使import了orchestrator,也无法伪造此值(因为不经过main dispatch)
_CURRENT_ACTION = ""

# V3.5.2: gate合法来源映射表
_VALID_GATE_SOURCES = {
    "onboarding": ["onboarding"],
    "step0": ["step0"],
    "step0_8": ["step0_8_save"],
    "P0": ["step_run", "quality_check"],
    "P1": ["step_run", "quality_check", "p1_code_merge"],
    "P2": ["p2_code_generate", "quality_check"],
    "P3": ["step_run", "quality_check"],
    "P4": ["step_run", "quality_check"],
    "P5": ["p5_code_merge", "quality_check"],
    "P6": ["p6_merge", "quality_check"],
    "P7": ["p7_code_check", "quality_check"],
}

# 内嵌密钥:V4.0.1改为固定secret派生,避免文件内容变化导致密钥断裂
def _get_hmac_key():
    """V4.0.1: 使用固定HMAC_SECRET常量派生密钥。
    不再依赖文件内容哈希,拆分/修改文件后旧任务仍可resume。
    """
    return HMAC_SECRET.encode("utf-8")


def _get_legacy_hmac_key():
    """V4.0.1兼容: 旧版基于文件哈希的密钥,用于验签兼容。"""
    orch_path = os.path.abspath(__file__)
    with open(orch_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return f"orch-gate-{file_hash[:32]}".encode("utf-8")


def _sign_gate(gate_data, task_id):
    """V3.2.6: 对gate pass数据生成HMAC签名。
    签名覆盖gate_data的所有字段(排除hmac字段本身)+ task_id。
    """
    # 拷贝并移除hmac字段,避免循环依赖
    data_copy = {k: v for k, v in gate_data.items() if k != "hmac"}
    data_copy["_task_id"] = task_id  # 确保task_id参与签名
    payload = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
    key = _get_hmac_key()
    sig = _hmac_mod.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return sig


def _write_signed_gate(gate_path, gate_data, task_id):
    """V3.5.2: 写入带HMAC签名+来源标记的gate pass文件。"""
    # V3.5.2: 记录创建gate的action来源
    gate_data["source_action"] = _CURRENT_ACTION
    gate_data["hmac"] = _sign_gate(gate_data, task_id)
    _write_json(gate_path, gate_data)


def _verify_gate_hmac(gate_data, task_id):
    """V4.0.1: 验证gate pass的HMAC签名 + 来源合法性。
    返回 (True, "OK") 或 (False, "原因")
    校验顺序:先HMAC验签(新密钥→旧密钥兼容)→ 再校验source_action合法性
    """
    stored_hmac = gate_data.get("hmac")
    if not stored_hmac:
        return False, "gate pass缺少HMAC签名(可能Agent伪造)"
    # 先用新密钥验签
    expected = _sign_gate(gate_data, task_id)
    hmac_ok = _hmac_mod.compare_digest(stored_hmac, expected)
    # V4.0.1: 新密钥失败时,尝试旧密钥(文件哈希)兼容验签
    if not hmac_ok:
        legacy_key = _get_legacy_hmac_key()
        data_copy = {k: v for k, v in gate_data.items() if k != "hmac"}
        data_copy["_task_id"] = task_id
        payload = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
        legacy_sig = _hmac_mod.new(legacy_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        hmac_ok = _hmac_mod.compare_digest(stored_hmac, legacy_sig)
    if not hmac_ok:
        return False, "HMAC签名不匹配(gate pass被篡改或Agent伪造)"
    # V3.5.2: HMAC通过后再校验source_action合法性
    # 空source_action表示旧版本创建的gate,兼容跳过
    step = gate_data.get("step", "")
    source_action = gate_data.get("source_action", "")
    if step in _VALID_GATE_SOURCES and source_action and source_action not in _VALID_GATE_SOURCES[step]:
        return False, f"{step}的gate来源非法: '{source_action}'(合法来源: {_VALID_GATE_SOURCES[step]},可能Agent绕过orchestrator伪造)"
    return True, "OK"


# ============================================================
# 状态管理
# ============================================================

class TaskState:
    """任务状态管理器"""

    def __init__(self, data_dir=None, task_id=None):
        self.task_id = task_id
        self.data_dir = data_dir
        self.state_path = os.path.join(data_dir, "orchestrator_state.json") if data_dir else None
        self.state = self._load()

    def _load(self):
        if self.state_path and os.path.exists(self.state_path):
            try:
                return _read_json(self.state_path)
            except Exception:
                pass
        return {
            "task_id": self.task_id,
            "data_dir": self.data_dir,
            "skill_dir": "",
            "current_step": None,
            "completed_steps": [],
            "current_phase": 1,
            "requirement_file": "",
            "skill_version": SKILL_VERSION,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "updated_at": None,
        }

    def save(self):
        if self.state_path:
            self.state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            _write_json(self.state_path, self.state)

    def mark_complete(self, step):
        if step not in self.state["completed_steps"]:
            self.state["completed_steps"].append(step)
        self.state["current_step"] = step
        self.save()

    def is_complete(self, step):
        return step in self.state["completed_steps"]

    def get_next_step(self):
        for step in STEPS:
            if step not in self.state["completed_steps"]:
                return step
        return None


# ============================================================
# Gate Pass 管理
# ============================================================

def check_gate(data_dir, step, task_id):
    """V3.2.6: 检查指定步骤的gate pass是否存在、task_id一致、且HMAC签名有效"""
    gp_path = os.path.join(data_dir, "gates", f"{step}.pass.json")
    if not os.path.exists(gp_path):
        return False, f"{step}.pass.json不存在"
    try:
        gp = _read_json(gp_path)
        if gp.get("task_id") != task_id:
            return False, f"task_id不匹配: {gp.get('task_id')} != {task_id}"
        # V3.2.6: HMAC验签
        hmac_ok, hmac_msg = _verify_gate_hmac(gp, task_id)
        if not hmac_ok:
            return False, f"{step}: {hmac_msg}"
        return True, "OK"
    except Exception:
        return False, f"{step}.pass.json读取失败"

def run_truncation_guard(skill_dir, data_dir, task_id, step, revision=1):
    """调用truncation_guard.py进行四级校验+auto-mv"""
    tmp_path = os.path.join(data_dir, f"{step.lower()}_output.tmp.json")
    guard_script = os.path.join(skill_dir, "tools", "truncation_guard.py")

    if not os.path.exists(guard_script):
        return False, "truncation_guard.py不存在"
    if not os.path.exists(tmp_path):
        return False, f"{tmp_path}不存在"

    cmd = [
        "python3", guard_script,
        "--file", tmp_path,
        "--step", step,
        "--data-dir", data_dir,
        "--task-id", task_id,
        "--revision", str(revision),
        "--auto-mv"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode == 0:
        return True, result.stdout.strip()
    else:
        return False, f"exit={result.returncode}: {result.stderr.strip() or result.stdout.strip()}"


# ============================================================
# Action: init
# ============================================================

def action_init(args):
    """初始化任务:创建task_id和DATA_DIR"""
    task_id = f"task_{time.strftime('%Y%m%d_%H%M%S')}"
    base_dir = os.path.expanduser("~/.openclaw/workspace/data")
    data_dir = os.path.join(base_dir, task_id)

    _ensure_dir(data_dir)
    _ensure_dir(os.path.join(data_dir, "gates"))

    state = TaskState(data_dir=data_dir, task_id=task_id)
    state.state["skill_dir"] = resolve_skill_dir("")
    state.state["data_dir"] = data_dir
    state.save()

    print(json.dumps({
        "status": "ok",
        "task_id": task_id,
        "data_dir": data_dir,
    }))


# ============================================================
# Action: onboarding
# ============================================================

def action_onboarding(args):
    """执行Onboarding环境检查(非交互部分)"""
    skill_dir = args.skill_dir
    data_dir = args.data_dir
    task_id = args.task_id

    checks = []

    # 检查1: 文件完整性
    required_files = [
        "prompts/P0_requirement_structuring.md",
        "prompts/P1_feature_tree_generation.md",
        "prompts/P2_test_point_draft.md",
        "prompts/P6_testcase_generation.md",
        "prompts/archive/P7_quality_gate.md",  # V3.3.1: P7已改为代码校验,prompt归档
        "tools/export_excel.py",
        "tools/truncation_guard.py",
        "tools/image_extract.py",
    ]
    missing = [f for f in required_files if not os.path.exists(os.path.join(skill_dir, f))]
    checks.append({
        "name": "file_integrity",
        "passed": len(missing) == 0,
        "missing": missing,
    })

    # 检查1.5: SKILL_DIR确认
    checks.append({
        "name": "skill_dir",
        "passed": os.path.exists(os.path.join(skill_dir, "tools", "export_excel.py")),
        "skill_dir": skill_dir,
    })

    # 检查2: Python + openpyxl
    try:
        result = subprocess.run(
            ["python3", "-c", "import openpyxl; print('ok')"],
            capture_output=True, text=True, timeout=10
        )
        openpyxl_ok = result.returncode == 0
    except Exception:
        openpyxl_ok = False
    checks.append({"name": "python_openpyxl", "passed": openpyxl_ok})

    # 检查0.5: 缓存检测
    cache_dir = os.path.expanduser("~/.openclaw/workspace/data")
    existing = sorted(glob.glob(os.path.join(cache_dir, "task_*")), reverse=True)[:3]
    checks.append({
        "name": "cache_detection",
        "existing_tasks": [os.path.basename(p) for p in existing],
    })

    all_passed = all(c.get("passed", True) for c in checks)

    # V4.8.1: 自动检测模型名和档位,写入 state(后续 P6 自动适配,无需 Agent 传 --model-name)
    model_name = (
        getattr(args, 'model_name', '') or
        os.environ.get('OPENCLAW_MODEL', '') or
        os.environ.get('OPENCLAW_DEFAULT_MODEL', '') or
        ''
    )
    model_tier = "LOW"  # V4.8.4: 保守策略,与prep_prompt/p6_batch_info一致
    if model_name:
        md = _get_model_detect()
        model_tier = md.classify(model_name)
    else:
        # 未检测到模型名 → 保守策略:走 LOW(引导卡模式),但标记为 unknown
        model_tier = "LOW"
        model_name = "unknown"

    checks.append({
        "name": "model_detection",
        "model_name": model_name,
        "model_tier": model_tier,
        "high_whitelist": list(_get_model_detect().HIGH_TIER_WHITELIST),
    })

    # 写入onboarding.pass.json (V3.2.6: HMAC签名)
    if all_passed:
        gate_path = os.path.join(data_dir, "gates", "onboarding.pass.json")
        gate_data = {
            "step": "onboarding",
            "task_id": task_id,
            "status": "PASS",
            "source": "onboarding",
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "checks": checks,
        }
        _write_signed_gate(gate_path, gate_data, task_id)

        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.state["skill_dir"] = args.skill_dir
        state.state["data_dir"] = data_dir
        state.state["model_tier"] = model_tier
        state.state["model_name"] = model_name
        if model_tier == "LOW":
            state.state["p6_mode"] = "guided"
        else:
            state.state["p6_mode"] = "full"
        state.save()
        state.mark_complete("onboarding")

    print(json.dumps({
        "status": "ok" if all_passed else "blocked",
        "checks": checks,
        "onboarding_pass": all_passed,
        "interaction_required": True,
        "interaction_steps": 3,
        "next_action": "❗ 环境检查通过。接下来必须向用户逐步展示3个交互步骤,每步必须等待用户回复后才能展示下一步。禁止跳过任何步骤。每步必须原样输出以下内容:",
        "step_1_display": "📋 PRD审查可在生成用例前检查需求文档质量。\n请选择:\n• 回复「开启」→ 启动PRD审查\n• 回复「跳过」→ 直接生成用例",
        "step_2_display": "📚 L5知识库可注入历史测试经验,提升用例质量。\n请选择:\n• 上传知识库文件 → 解析入库\n• 回复「跳过」→ 不使用历史经验库(其他知识库仍正常使用)",
        "step_3_display": "🔐 API密码同时控制两个功能:图片理解 + 行业知识库。\n请选择:\n• 回复API密码 → 同时启用图片理解和行业知识库\n• 回复「跳过」→ 纯文本模式(无行业知识库,质量降20-30%)\n\n用户输入密码后执行 orchestrator --action check_image_api --api-key 密码\n验证成功→记住密码+拉取行业知识库+后续step0_8_prep传入。验证失败→提示重试或跳过。\n\nV4.0.0新增:密码正确后自动从云端拉取行业知识库到本地,无需额外操作。",
    }))


# ============================================================
# Action: step0
# ============================================================

def _auto_discover_requirement(data_dir):
    """方案A: 当Agent未传requirement_file时,自动扫描常见路径找需求文档。
    扫描顺序:
    1. data_dir 同级目录(任务目录旁边)
    2. ~/Downloads
    3. ~/Desktop
    4. ~/.openclaw/workspace/sharetasks(共享工作区)
    5. 当前工作目录 (cwd)
    返回找到的第一个 .docx/.md/.txt 文件路径,找不到返回 ""
    """
    import glob as _glob
    # data_dir 为空时不扫描,避免 os.path.dirname("") 返回 "." 误命中当前目录
    parent_dir = os.path.dirname(data_dir) if data_dir else ""
    candidate_dirs = [
        parent_dir,
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/.openclaw/workspace/sharetasks"),
        os.getcwd(),
    ]
    # 优先 .docx,其次 .md,最后 .txt
    for ext in (".docx", ".md", ".txt"):
        for d in candidate_dirs:
            # 跳过空路径和非目录
            if not d or not os.path.isdir(d):
                continue
            # 只扫一层,不递归,避免误命中
            matches = sorted(_glob.glob(os.path.join(d, f"*{ext}")), key=os.path.getmtime, reverse=True)
            if matches:
                return matches[0]  # 最新修改的文件
    return ""


def action_step0(args):
    """Step 0: 接收需求,写入task_meta"""
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir
    requirement_text = args.requirement_text or ""
    requirement_file = args.requirement_file or ""

    # 方案A: Agent未传 requirement_file 且无 requirement_text 时,自动发现需求文档
    auto_discovered = False
    if not requirement_file and not requirement_text:
        discovered = _auto_discover_requirement(data_dir)
        if discovered:
            requirement_file = discovered
            auto_discovered = True

    # 门禁检查
    ok, msg = check_gate(data_dir, "onboarding", task_id)
    if not ok:
        print(json.dumps({"status": "gate_blocked", "step": "onboarding", "reason": msg}))
        sys.exit(1)

    # 如果是文件,提取文本
    if requirement_file and not requirement_text:
        if requirement_file.endswith(".docx"):
            try:
                result = subprocess.run(
                    ["python3", "-c", "import zipfile,re,sys; z=zipfile.ZipFile(sys.argv[1]); xml=z.read('word/document.xml').decode('utf-8'); text=re.sub(r'<[^>]+>',' ',xml); text=re.sub(r'\s+',' ',text).strip(); print(text[:50000])", requirement_file],
                    capture_output=True, text=True, timeout=30
                )
                requirement_text = result.stdout.strip()
            except Exception as e:
                requirement_text = f"[docx解析失败: {e}]"
        else:
            try:
                with open(requirement_file, "r", encoding="utf-8") as f:
                    requirement_text = f.read()[:50000]
            except Exception:
                requirement_text = "[文件读取失败]"

    domain = _detect_domain(requirement_text)

    # 读取preferences(脱敏:不写入api_key等敏感字段到task_meta)
    prefs_path = os.path.join(skill_dir, "user_knowledge", "preferences.json")
    prefs = {}
    prefs_safe = {}  # 脱敏版本,只保留非敏感字段
    if os.path.exists(prefs_path):
        try:
            prefs = _read_json(prefs_path)
            # 脱敏:image_api只保留url/model/timeout(api_key运行时输入,不存此处)
            if "image_api" in prefs:
                ia = prefs["image_api"]
                prefs_safe["image_api"] = {
                    "url": ia.get("url", ""),
                    "model": ia.get("model", "ci"),
                    "timeout": ia.get("timeout", 120),
                }
        except Exception:
            pass

    # 从需求文件名提取项目名(去掉路径、扩展名、云端上传的随机后缀)
    project_name = ""
    if requirement_file:
        basename = os.path.splitext(os.path.basename(requirement_file))[0]
        # 去掉云端上传时附加的随机后缀(如 ---7bc1d4d1-869c-452a-a6aa-2215b6ded1a2)
        import re as _re
        basename = _re.sub(r'---[0-9a-f\-]{20,}$', '', basename).strip()
        project_name = basename

    # V4.0.1: 业务域匹配(项目关键词 + 同义词模糊匹配)
    domain_match_result = _match_project_to_domains(requirement_text, skill_dir)
    matched_project_name = domain_match_result["matched_projects"][0] if domain_match_result["matched_projects"] else ""

    # domain字段优先用域匹配结果(中文全名),降级用_detect_domain(英文key)
    resolved_domain = domain_match_result["domains"][0] if domain_match_result["domains"] else domain

    # 写入task_meta
    meta = {
        "task_id": task_id,
        "domain": resolved_domain,
        "domains": domain_match_result["domains"],
        "matched_projects": domain_match_result["matched_projects"],
        "matched_synonyms": domain_match_result["matched_synonyms"],
        "project_name": matched_project_name,
        "project": project_name,
        "requirement_text": requirement_text,
        "requirement_file": requirement_file,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "preferences": prefs_safe,  # 脱敏版本
        "skill_version": SKILL_VERSION,
        "requirement_hash": _sha256(requirement_text),
    }
    # V3.5.2: 保留已有的task_meta字段(如set_prd_review写入的prd_quality_review)
    existing_meta_path = os.path.join(data_dir, "task_meta.json")
    if os.path.exists(existing_meta_path):
        existing_meta = _read_json(existing_meta_path)
        # 保留已有字段,新字段覆盖旧字段
        existing_meta.update(meta)
        meta = existing_meta
    _write_json(os.path.join(data_dir, "task_meta.json"), meta)

    state = TaskState(data_dir=data_dir, task_id=task_id)
    state.state["requirement_file"] = requirement_file
    state.state["current_phase"] = 2
    state.mark_complete("step0")

    result = {
        "status": "ok",
        "task_id": task_id,
        "domain": domain,
        "requirement_length": len(requirement_text),
        "requirement_file": requirement_file,
    }
    if auto_discovered:
        result["auto_discovered"] = True
        result["warning"] = f"requirement_file未传入,已自动发现并使用: {requirement_file}"
    elif not requirement_file and not requirement_text:
        result["status"] = "error"
        result["reason"] = "未传入requirement_file或requirement_text,且自动扫描未找到任何需求文档(.docx/.md/.txt)。请明确传入 --requirement-file 参数。"
    print(json.dumps(result))
    if result["status"] == "error":
        sys.exit(1)


# ============================================================
# ============================================================
# 图片理解API配置读取
# ============================================================

def _load_image_api_config(skill_dir, api_key=None):
    """读取图片理解API配置

    - url/model/timeout从preferences.json读取(写死,用户无需输入)
    - api_key从运行时参数传入(Onboarding交互时用户输入,不落盘)
    - enabled由api_key是否非空决定(有密码=启用,无密码=降级)
    """
    prefs_path = os.path.join(skill_dir, "user_knowledge", "preferences.json")
    prefs = {}
    if os.path.exists(prefs_path):
        try:
            prefs = _read_json(prefs_path)
        except Exception:
            pass

    ia = prefs.get("image_api", {})

    config = {
        "enabled": bool(api_key and api_key.strip()),  # 有密码才启用
        "url": ia.get("url", ""),
        "model": ia.get("model", "ci"),  # ci=数据万象, qwen=通义千问VL
        "timeout": ia.get("timeout", 120),
        "api_key": (api_key or "").strip(),
    }

    # 配置完整性校验
    if config["enabled"]:
        if not config["url"].startswith("https://") and not config["url"].startswith("http://"):
            config["enabled"] = False
            config["_invalid_reason"] = "API地址未配置或格式不正确(检查preferences.json中image_api.url)"

    return config


def _sync_knowledge_from_cloud(skill_dir, api_key, cloud_config):
    """V4.0.0: 从云端拉取知识库到本地

    流程:
    1. 读取本地版本号(.knowledge_version.json)
    2. 调用云端 GET /api/knowledge/version 获取最新版本
    3. 版本一致则跳过,不一致则下载
    4. 调用 GET /api/knowledge/pack 下载文件
    5. 写入本地 knowledge/ 目录
    6. 更新版本号
    """
    import urllib.request
    import urllib.error

    # 确定API base URL(兼容嵌套结构)
    api_base = (
        cloud_config.get("knowledge_api_url") or
        cloud_config.get("review_tool", {}).get("api_url") or
        cloud_config.get("experience_sync", {}).get("api_url") or
        ""
    )
    if not api_base:
        return "未配置云端地址"

    api_base = api_base.rstrip("/")

    # 1. 读取本地版本
    version_path = os.path.join(skill_dir, ".knowledge_version.json")
    local_version = None
    if os.path.exists(version_path):
        try:
            local_version = _read_json(version_path)
        except Exception:
            pass

    local_checksum = (local_version or {}).get("checksum", "")

    # 2. 检查云端版本
    try:
        ver_req = urllib.request.Request(
            f"{api_base}/api/knowledge/version",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(ver_req, timeout=10) as resp:
            cloud_version = json.loads(resp.read().decode("utf-8"))

        if cloud_version.get("status") != "ok":
            return f"云端返回错误"

        cloud_data = cloud_version["data"]
        if cloud_data.get("checksum") == local_checksum:
            return f"已是最新(v{cloud_data['version']})"

    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return "密码无权访问知识库"
        return f"云端版本检查失败(HTTP {e.code})"
    except Exception as e:
        return f"云端不可用({str(e)[:50]})"

    # 3. 下载知识库包
    try:
        pack_url = f"{api_base}/api/knowledge/pack"
        pack_req = urllib.request.Request(
            pack_url,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(pack_req, timeout=30) as resp:
            pack = json.loads(resp.read().decode("utf-8"))

        if pack.get("status") != "ok":
            return f"下载失败"

        pack_data = pack["data"]
        files = pack_data.get("files", {})
        if not files:
            return "无文件"

        # 4. 写入本地
        saved_count = 0
        for rel_path, content in files.items():
            abs_path = os.path.join(skill_dir, "knowledge", rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            saved_count += 1

        # 5. 更新版本号
        new_version = {
            "last_sync": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "version": pack_data.get("version", ""),
            "checksum": pack_data.get("checksum", ""),
            "files_count": len(files),
        }
        with open(version_path, "w", encoding="utf-8") as f:
            json.dump(new_version, f, ensure_ascii=False, indent=2)

        return f"已同步{saved_count}个文件(v{pack_data.get('version', '?')})"

    except urllib.error.HTTPError as e:
        return f"下载失败(HTTP {e.code})"
    except Exception as e:
        return f"同步失败({str(e)[:50]})"


def _sync_review_experience(skill_dir, api_key, cloud_config, domain=None):
    """V4.0.1: 从云端评审工具拉取评审经验规则到本地 knowledge/reviewed_cases/

    Args:
        skill_dir: skill目录
        api_key: API密钥
        cloud_config: cloud.json配置
        domain: 指定域(None=全量同步所有12个域)

    Returns:
        str: 同步结果摘要
    """
    import urllib.request
    import urllib.error
    import urllib.parse

    api_base = cloud_config.get("review_tool", {}).get("api_url", "")
    if not api_base:
        return "未配置评审工具地址"
    api_base = api_base.rstrip("/")

    # 12个一级域
    ALL_DOMAINS = ["客户域", "交易域", "资管域", "自营域", "投顾域", "投研域",
                   "投行业务域", "机构业务域", "清算托管域", "风控合规域", "行情资讯域", "互联网终端域"]
    domains = [domain] if domain else ALL_DOMAINS

    rules_dir = os.path.join(skill_dir, "knowledge", "reviewed_cases")
    _ensure_dir(rules_dir)

    synced = 0
    skipped = 0
    failed = 0

    for d in domains:
        try:
            # 调用 GET /api/experience/rules?domain=X
            url = f"{api_base}/api/experience/rules?domain={urllib.parse.quote(d)}"
            req = urllib.request.Request(url, headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            if result.get("status") != "ok":
                failed += 1
                continue

            data = result.get("data", {})
            # 检查是否有规则
            rules = data.get("rules")
            if not rules:
                skipped += 1
                continue
            total = (len(rules.get("tag_rules", [])) + len(rules.get("operation_rules", [])) +
                     len(rules.get("domain_rules", [])) + len(rules.get("positive_rules", [])))
            if total == 0:
                skipped += 1
                continue

            # 写入本地
            domain_file = _domain_to_filename(d)
            out_path = os.path.join(rules_dir, f"{domain_file}_rules.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(rules, f, ensure_ascii=False, indent=2)
            synced += 1

        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return "密码无权访问评审经验"
            failed += 1
        except Exception:
            failed += 1

    return f"同步{synced}个域, 跳过{skipped}个(无数据), 失败{failed}个"


def _check_image_api_health(config):
    """预检:调用API的auth-check接口验证密码+服务可用性

    V3.0.3-patch1: 改用/api/auth-check替代/api/health
    原因: /api/health不鉴权,无法验证密码正确性(F2/F17修复)
    """
    try:
        import requests
        # 从analyze URL推导auth-check URL
        if "/api/" in config["url"]:
            base_url = config["url"].rsplit("/api/", 1)[0]
        else:
            base_url = config["url"].rsplit("/", 1)[0]
        auth_check_url = base_url + "/api/auth-check"

        resp = requests.get(
            auth_check_url,
            headers={"X-API-Key": config["api_key"]},
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("status") == "ok", data
        elif resp.status_code in (401, 403):
            return False, {"error": "auth_failed", "message": "密码错误"}
        elif resp.status_code == 503:
            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            return False, {"error": "service_not_configured", "message": data.get("reason", data.get("message", "服务未配置密码验证"))}
        return False, {"error": f"HTTP {resp.status_code}"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "connection_failed", "message": "无法连接到API服务"}
    except requests.exceptions.Timeout:
        return False, {"error": "timeout", "message": "API服务响应超时"}
    except Exception as e:
        return False, {"error": str(e)[:100]}


def _call_image_api(image_path, config):
    """调用图片理解API分析单张图片"""
    try:
        import requests
        with open(image_path, "rb") as f:
            resp = requests.post(
                config["url"],
                headers={"X-API-Key": config["api_key"]},
                files={"file": f},
                data={"model": config["model"]},
                timeout=config["timeout"],
            )
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code in (401, 403):
            return {"status": "auth_failed", "error": f"鉴权失败: HTTP {resp.status_code}"}
        elif resp.status_code == 429:
            return {"status": "rate_limited", "error": "请求频率超限"}
        else:
            return {"status": "error", "error": f"HTTP {resp.status_code}"}
    except requests.exceptions.Timeout:
        return {"status": "timeout", "error": "请求超时"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}


# ============================================================
# Action: step0_8_prep (PX图片抽取+选图+API理解/caption_only降级)
# ============================================================

def action_step0_8_prep(args):
    """PX图片抽取+价值优先选图+自动调用API理解(或降级为caption_only)

    V3.0.3改动:
    - API模式:orchestrator直接调用图片理解API,不依赖Agent
    - 降级模式:caption_only(用前后文生成描述),不回退Agent看图
    - 结果写入px_api_results.json,由step0_8_save统一收口
    """
    data_dir = args.data_dir
    skill_dir = args.skill_dir
    requirement_file = args.requirement_file or ""

    # 方案A延伸:如果未传requirement_file,先尝试从 task_meta.json 读取
    if not requirement_file:
        meta_path = os.path.join(data_dir, "task_meta.json")
        if os.path.exists(meta_path):
            try:
                meta = _read_json(meta_path)
                requirement_file = meta.get("requirement_file", "")
            except Exception:
                pass

    if not requirement_file or not requirement_file.endswith(".docx"):
        print(json.dumps({"status": "skipped", "reason": "非docx格式,跳过PX"}))
        return

    # 调用image_extract.py
    extract_script = os.path.join(skill_dir, "tools", "image_extract.py")
    px_images_dir = os.path.join(data_dir, "px_images")
    px_extract_path = os.path.join(data_dir, "px_extract.json")

    _ensure_dir(px_images_dir)

    result = subprocess.run(
        ["python3", extract_script, requirement_file,
         "--output-dir", px_images_dir,
         "--json-output", px_extract_path],
        capture_output=True, text=True, timeout=60
    )

    if result.returncode != 0 or not os.path.exists(px_extract_path):
        print(json.dumps({"status": "skipped", "reason": f"图片抽取失败: {result.stderr[:200]}"}))
        return

    extract_data = _read_json(px_extract_path)
    images = extract_data.get("images", [])

    if not images:
        print(json.dumps({"status": "skipped", "reason": "docx中无图片"}))
        return

    # 价值优先选图
    value_keywords = ["流程", "状态", "原型", "页面", "规则", "接口", "表格", "如下图", "见图"]
    scored = []
    for img in images:
        caption = (img.get("caption", "") or "").lower()
        before = (img.get("before_text", "") or "").lower()
        after = (img.get("after_text", "") or "").lower()
        context = caption + " " + before + " " + after

        score = 0
        for kw in value_keywords:
            if kw in context:
                score += 1

        # 跳过装饰性图片
        w = img.get("width", 100)
        h = img.get("height", 100)
        if (w < 50 and h < 50) or "logo" in context or "icon" in context:
            score = -1

        scored.append((score, img))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [img for score, img in scored if score >= 0][:50]

    # ============================================================
    # V3.0.3: 图片理解(API模式 or caption_only降级)
    # ============================================================
    # V3.2.0: api_key优先从命令行参数读取,其次从task目录缓存读取(解决Agent跨段落丢密码问题)
    api_key = getattr(args, 'api_key', None) or ''
    if not api_key.strip():
        cache_path = os.path.join(data_dir, ".image_api_key")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    api_key = f.read().strip()
            except Exception:
                pass
    api_config = _load_image_api_config(skill_dir, api_key=api_key or None)
    use_api = api_config["enabled"]

    # 预检:API health check
    service_ok = False
    if use_api:
        service_ok, health_data = _check_image_api_health(api_config)
        if not service_ok:
            use_api = False  # 降级

    results = []
    api_success = 0
    api_fallback = 0

    # V3.2.0: 并行调用API(解决19张图串行~570s的问题)
    # 策略:线程池并发=3,主线程汇总结果,401/403立即标记
    def _process_single_image(img):
        """处理单张图片(线程安全:只读输入,返回结果,不修改共享状态)"""
        image_id = img.get("image_id", "")
        file_path = img.get("file_path", "")
        caption = img.get("caption", "") or ""
        before_text = (img.get("before_text", "") or "")[:200]
        after_text = (img.get("after_text", "") or "")[:200]

        caption_desc = caption
        if before_text or after_text:
            context_parts = []
            if before_text:
                context_parts.append(f"图片前文: {before_text}")
            if caption:
                context_parts.append(f"图片标题: {caption}")
            if after_text:
                context_parts.append(f"图片后文: {after_text}")
            caption_desc = " | ".join(context_parts)

        if not file_path or not os.path.exists(file_path):
            return {"image_id": image_id, "understanding_mode": "caption_only",
                    "failure_type": "file_not_found", "description": caption_desc,
                    "ocr_text": "", "labels": [],
                    "before_text": before_text, "after_text": after_text, "_ok": False}

        api_result = _call_image_api(file_path, api_config)

        if api_result.get("status") in ("ok", "partial"):
            mode = "api" if api_result.get("status") == "ok" else "api_partial"
            return {"image_id": image_id, "understanding_mode": mode,
                    "api_provider": api_result.get("model", api_config["model"]),
                    "description": api_result.get("description", caption_desc),
                    "ocr_text": api_result.get("ocr_text", ""),
                    "labels": api_result.get("labels", []),
                    "confidence": api_result.get("confidence", 0),
                    "before_text": before_text, "after_text": after_text, "_ok": True}
        elif api_result.get("status") in ("auth_failed", "rate_limited"):
            return {"image_id": image_id, "understanding_mode": "api_fallback_caption",
                    "failure_type": api_result.get("status"), "description": caption_desc,
                    "ocr_text": "", "labels": [],
                    "before_text": before_text, "after_text": after_text, "_ok": False, "_fatal": True}
        else:
            return {"image_id": image_id, "understanding_mode": "api_fallback_caption",
                    "failure_type": api_result.get("status", "unknown"), "description": caption_desc,
                    "ocr_text": "", "labels": [],
                    "before_text": before_text, "after_text": after_text, "_ok": False}

    if use_api:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        fatal_detected = False
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_map = {executor.submit(_process_single_image, img): img.get("image_id", "") for img in selected}
            try:
                for future in as_completed(future_map, timeout=600):
                    try:
                        r = future.result(timeout=120)
                        ok = r.pop("_ok", False)
                        is_fatal = r.pop("_fatal", False)
                        results.append(r)
                        if ok:
                            api_success += 1
                        else:
                            api_fallback += 1
                        # 401/403立即取消剩余任务
                        if is_fatal:
                            fatal_detected = True
                            for f in future_map:
                                f.cancel()
                            break
                    except Exception as e:
                        results.append({"image_id": future_map.get(future, "?"),
                                        "understanding_mode": "api_fallback_caption",
                                        "failure_type": "exception", "description": str(e)[:200],
                                        "ocr_text": "", "labels": [],
                                        "before_text": "", "after_text": ""})
                        api_fallback += 1
            except TimeoutError:
                # 总超时600s,未完成的图片降级为caption_only
                for f, img_id in future_map.items():
                    if not f.done():
                        results.append({"image_id": img_id,
                                        "understanding_mode": "api_fallback_caption",
                                        "failure_type": "total_timeout",
                                        "description": "总超时600s未完成",
                                        "ocr_text": "", "labels": [],
                                        "before_text": "", "after_text": ""})
                        api_fallback += 1
    else:
        for img in selected:
            image_id = img.get("image_id", "")
            caption = img.get("caption", "") or ""
            before_text = (img.get("before_text", "") or "")[:200]
            after_text = (img.get("after_text", "") or "")[:200]
            caption_desc = caption
            if before_text or after_text:
                parts = []
                if before_text: parts.append(f"图片前文: {before_text}")
                if caption: parts.append(f"图片标题: {caption}")
                if after_text: parts.append(f"图片后文: {after_text}")
                caption_desc = " | ".join(parts)
            results.append({"image_id": image_id, "understanding_mode": "caption_only",
                            "description": caption_desc, "ocr_text": "", "labels": [],
                            "before_text": before_text, "after_text": after_text})

    # 将结果写入临时文件,由step0_8_save统一收口
    _write_json(os.path.join(data_dir, "px_api_results.json"), {
        "results": results,
        "summary": {
            "mode": "api" if api_config["enabled"] and service_ok else "caption_only",
            "service_status": "ok" if api_success > 0 and api_fallback == 0 else
                              ("partial_success" if api_success > 0 else "degraded"),
            "api_success_count": api_success,
            "api_fallback_count": api_fallback,
            "total_selected": len(selected),
            "total_images": len(images),
            "api_provider": api_config["model"] if api_config["enabled"] else "none",
        }
    })

    # 输出状态
    mode = "api" if api_config["enabled"] and service_ok else "caption_only"
    if not api_config["enabled"]:
        mode_msg = "caption_only(未输入图片API密码,如需启用请在Onboarding时输入密码)"
    elif not service_ok:
        mode_msg = f"caption_only(API健康检查失败: {health_data.get('error', 'unknown')})"
    elif api_fallback > 0:
        mode_msg = f"api_with_fallback(成功{api_success}张,降级{api_fallback}张)"
    else:
        mode_msg = f"api(全部{api_success}张通过{api_config['model']}理解)"

    print(json.dumps({
        "status": "ok",
        "mode": mode,
        "mode_message": mode_msg,
        "total_images": len(images),
        "selected_count": len(selected),
        "api_success_count": api_success,
        "api_fallback_count": api_fallback,
    }))


# ============================================================
# Action: step0_8_save (保存图片理解结果)
# ============================================================

def action_step0_8_save(args):
    """保存图片理解结果,调用image_enhance(统一收口)

    V3.0.3改动:
    - 优先读取px_api_results.json(API/caption_only模式产出)
    - 如无API结果文件,回退读取args.results_json(兼容旧模式)
    - 统一生成px_understand.json + 调用image_enhance + mark_complete
    """
    data_dir = args.data_dir
    skill_dir = args.skill_dir
    task_id = args.task_id

    # 优先读取API结果文件
    api_results_path = os.path.join(data_dir, "px_api_results.json")
    if os.path.exists(api_results_path):
        api_data = _read_json(api_results_path)
        results = api_data.get("results", [])
        api_summary = api_data.get("summary", {})
    elif args.results_json:
        # 兼容旧模式:从命令行参数读取
        try:
            results = json.loads(args.results_json)
            api_summary = {}
        except Exception:
            print(json.dumps({"status": "error", "reason": "图片理解结果JSON解析失败"}))
            return
    else:
        print(json.dumps({"status": "error", "reason": "无图片理解结果(px_api_results.json不存在且未传入results_json)"}))
        return

    # 读取抽取数据获取总数
    px_extract_path = os.path.join(data_dir, "px_extract.json")
    total = 0
    if os.path.exists(px_extract_path):
        total = len(_read_json(px_extract_path).get("images", []))

    # 构造px_understand.json
    api_count = sum(1 for r in results if r.get("understanding_mode") == "api")
    caption_count = sum(1 for r in results if r.get("understanding_mode") in ("caption_only", "api_fallback_caption"))
    vision_count = sum(1 for r in results if r.get("understanding_mode") == "vision")  # 兼容旧模式

    # 构造skipped_images列表(未被选中的图片)
    skipped_images = []
    if os.path.exists(px_extract_path):
        all_images = _read_json(px_extract_path).get("images", [])
        selected_ids = set(r.get("image_id", "") for r in results)
        for img in all_images:
            if img.get("image_id", "") not in selected_ids:
                skipped_images.append({
                    "image_id": img.get("image_id", ""),
                    "file_path": img.get("file_path", ""),
                    "selected": False,
                    "selection_reason": "超出50张上限或未命中高价值关键词",
                    "understanding_mode": "skipped"
                })

    understand = {
        "task_id": task_id,
        "total_images": total,
        "selected_images": len(results),
        "results": results,
        "skipped_images": skipped_images,
        "summary": {
            "api_count": api_count,
            "caption_count": caption_count,
            "vision_count": vision_count,
            "skipped_count": total - len(results),
            "mode": api_summary.get("mode", "unknown"),
            "service_status": api_summary.get("service_status", "unknown"),
            "api_provider": api_summary.get("api_provider", "none"),
        }
    }
    _write_json(os.path.join(data_dir, "px_understand.json"), understand)

    # 调用image_enhance
    enhance_script = os.path.join(skill_dir, "tools", "image_enhance.py")
    enhance_output = os.path.join(data_dir, "px_enhance.json")

    result = subprocess.run(
        ["python3", enhance_script,
         os.path.join(data_dir, "px_understand.json"),
         "--output", enhance_output],
        capture_output=True, text=True, timeout=30
    )

    state = TaskState(data_dir=data_dir, task_id=task_id)
    state.mark_complete("step0_8")

    print(json.dumps({
        "status": "ok",
        "mode": api_summary.get("mode", "unknown"),
        "api_count": api_count,
        "caption_count": caption_count,
        "vision_count": vision_count,
        "total": total,
        "enhance_ok": result.returncode == 0,
    }))


# ============================================================
# Action: step_run (执行P0-P7任一步骤)
# ============================================================

def action_step_run(args):
    """
    执行P0-P4/P7步骤:
    1. 检查前置gate pass
    2. 准备prompt输入(读取上游产物+知识注入)
    3. 接收Agent的JSON输出
    4. 写入tmp → truncation_guard → gate pass

    V3.2.5: P5和P6禁止通过step_run执行,必须走专用流程
    """
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir
    step = args.step  # P0/P1/P2/P3/P4/P7
    agent_output = args.agent_output  # Agent返回的JSON字符串

    # V3.3.3: P2/P5/P6/P7禁止通过step_run执行,必须走代码路径
    if step == "P2":
        print(json.dumps({
            "status": "rejected",
            "reason": "❌ P2禁止用step_run执行!P2是代码自动生成,必须用: python3 orchestrator.py --action p2_code_generate",
            "correct_action": "p2_code_generate",
        }))
        sys.exit(1)
    if step == "P5":
        print(json.dumps({
            "status": "rejected",
            "reason": "❌ P5禁止用step_run执行!P5是代码自动合并,必须用: python3 orchestrator.py --action p5_code_merge",
            "correct_action": "p5_code_merge",
        }))
        sys.exit(1)
    if step == "P6":
        print(json.dumps({
            "status": "rejected",
            "reason": "❌ P6禁止用step_run执行!P6必须用逐条流程: p6_tp_list → 循环(p6_generate_one → p6_generate_one --save) → p6_merge (V4.11.0)",
            "correct_flow": "p6_tp_list -> p6_generate_one --tp-index N -> p6_generate_one --tp-index N --save (V4.11.0)",
        }))
        sys.exit(1)
    # V3.3.1: P7禁止通过step_run执行,必须走代码校验
    if step == "P7":
        print(json.dumps({
            "status": "rejected",
            "reason": "❌ P7禁止用step_run执行!P7是代码自动校验,必须用: python3 orchestrator.py --action p7_code_check",
            "correct_action": "p7_code_check",
        }))
        sys.exit(1)

    # 前置gate pass检查
    prerequisites = {
        "P0": ["onboarding"],
        "P1": ["P0"],
        "P2": ["P1"],
        "P3": ["P1"],
        "P4": ["P1"],
        "P5": ["P2", "P3", "P4"],
        "P6": ["P5"],
        "P7": ["P6"],
    }

    for prereq in prerequisites.get(step, []):
        ok, msg = check_gate(data_dir, prereq, task_id)
        if not ok:
            print(json.dumps({"status": "gate_blocked", "step": prereq, "reason": msg}))
            sys.exit(1)

    # 解析Agent输出
    try:
        output_data = json.loads(agent_output)
    except json.JSONDecodeError:
        # JSON解析兜底:尝试正则提取
        import re
        match = re.search(r'\{[\s\S]*\}', agent_output)
        if match:
            try:
                output_data = json.loads(match.group())
            except Exception:
                print(json.dumps({"status": "error", "reason": "Agent输出JSON解析失败(含正则兜底)"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "reason": "Agent输出不含有效JSON"}))
            sys.exit(1)

    # V3.5.2: output文件写入保护 - 检测是否被Agent提前写入
    final_output_path = os.path.join(data_dir, f"{step.lower()}_output.json")
    if os.path.exists(final_output_path):
        state_check = TaskState(data_dir=data_dir, task_id=task_id)
        if state_check.is_completed(step):
            print(json.dumps({"status": "error", "reason": f"{step}已完成,禁止重复执行。如需重跑请先重置状态。"}))
            sys.exit(1)
        else:
            # 文件存在但state未标记完成 → 可能Agent伪造的,删除
            try:
                os.unlink(final_output_path)
            except Exception:
                pass

    # V4.8.5: P1输出截断检测 - 检测JSON是否被模型截断
    if step == "P1":
        agent_output_stripped = agent_output.strip()
        if not (agent_output_stripped.endswith('}') or agent_output_stripped.endswith(']')):
            print(json.dumps({
                "status": "truncation_detected",
                "reason": "P1输出JSON不完整(末尾非闭合括号),模型输出可能被截断。请重跑P1。",
                "hint": "若反复截断,请检查模型上下文窗口是否不足,LOW模式已自动精简P1 prompt"
            }))
            sys.exit(1)

    # 写入tmp文件
    tmp_path = os.path.join(data_dir, f"{step.lower()}_output.tmp.json")
    _write_json(tmp_path, output_data)

    # V3.5.4: PRD审查字段强制校验 - 当prd_quality_review=True时,P0必须输出blocks_markdown和issues
    if step == "P0":
        meta_path = os.path.join(data_dir, "task_meta.json")
        if os.path.exists(meta_path):
            _meta = _read_json(meta_path)
            if _meta.get("prd_quality_review", False):
                # PRD审查模式下,blocks_markdown和issues为必须字段
                missing_prd_fields = []
                if "blocks_markdown" not in output_data:
                    missing_prd_fields.append("blocks_markdown")
                if "issues" not in output_data:
                    missing_prd_fields.append("issues")
                if missing_prd_fields:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                    print(json.dumps({
                        "status": "prd_review_validation_failed",
                        "step": "P0",
                        "reason": f"PRD审查模式下必须输出字段: {missing_prd_fields}。请检查prompt是否正确注入,Agent是否遵循输出要求。",
                        "missing_fields": missing_prd_fields,
                        "hint": "PRD审查开启后,P0必须输出 blocks_markdown (结构化Markdown) 和 issues (问题清单数组)。请重新生成P0输出。"
                    }))
                    sys.exit(1)

                # V3.5.6: PRD审查内容质量校验
                blocks_md = output_data.get("blocks_markdown", "")
                issues_list = output_data.get("issues", [])
                quality_issues = []

                # 检查1: blocks_markdown类型防御(建议3)
                if not isinstance(blocks_md, str):
                    quality_issues.append(f"blocks_markdown必须是字符串类型,当前为{type(blocks_md).__name__}")
                else:
                    # 检查2: blocks_markdown最小长度
                    if len(blocks_md.strip()) < 200:
                        quality_issues.append("blocks_markdown内容过于简单(<200字符),请展开业务规则、约束条件等5个维度")

                    # 检查3: 关键维度检查(至少包含2个维度)
                    dimension_keywords = ["输入", "输出", "业务规则", "角色权限", "状态流转", "约束条件"]
                    found_dimensions = sum(1 for kw in dimension_keywords if kw in blocks_md)
                    if found_dimensions < 2:
                        quality_issues.append(f"blocks_markdown缺少关键维度(仅发现{found_dimensions}个,应至少包含2个:输入/输出、业务规则、约束条件等)")

                # 检查4: issues格式校验(建议1+建议2:全量校验+类型防御)
                if not isinstance(issues_list, list):
                    quality_issues.append("issues必须是数组类型")
                elif len(issues_list) > 0:
                    required_issue_fields = ["severity", "location", "type", "problem", "suggestion"]
                    for i, issue in enumerate(issues_list):
                        if not isinstance(issue, dict):
                            quality_issues.append(f"issues[{i}]必须是对象类型,当前为{type(issue).__name__}")
                            continue
                        missing_issue_fields = [f for f in required_issue_fields if f not in issue]
                        if missing_issue_fields:
                            quality_issues.append(f"issues[{i}]对象缺少字段: {missing_issue_fields}")

                if quality_issues:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                    print(json.dumps({
                        "status": "prd_review_quality_failed",
                        "step": "P0",
                        "reason": "PRD审查内容质量不达标",
                        "quality_issues": quality_issues,
                        "hint": "blocks_markdown内容应≥200字符,需至少覆盖2个关键维度(如输入/输出、业务规则等)。issues数组中每个对象必须包含severity/location/type/problem/suggestion字段。"
                    }))
                    sys.exit(1)

    # === V3.0.3新增:写入tmp后、guard前,先做必需字段校验(代码硬控) ===
    required_fields_map = {
        "P0": P0_REQUIRED_FIELDS,
        "P1": P1_REQUIRED_FIELDS,
        "P3": P3_REQUIRED_FIELDS,
        "P4": P4_REQUIRED_FIELDS,
        "P5": P5_REQUIRED_FIELDS,
        "P6": P6_REQUIRED_FIELDS,
        "P7": P7_REQUIRED_FIELDS,
    }
    if step in required_fields_map:
        missing_fields = []
        for field in required_fields_map[step]:
            # 支持嵌套路径和多候选
            val = _get_nested(output_data, field)
            if val is None:
                missing_fields.append(field)
        if missing_fields:
            # 删除tmp文件,拒绝写入
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            print(json.dumps({
                "status": "validation_failed",
                "step": step,
                "reason": f"必需字段缺失: {missing_fields}。请确保输出JSON包含这些顶层字段。",
                "missing_fields": missing_fields,
                "hint": f"{step}输出必须包含: {required_fields_map[step]}",
            }))
            sys.exit(1)

    # V4.8.8: P1 场景数量质量校验(Gate级硬控,防止Agent为规避截断而压缩scenario)
    if step == "P1":
        p1_quality_issues = []
        feature_tree = output_data.get("feature_tree", {})
        modules = feature_tree.get("children", feature_tree.get("modules", []))

        # 收集所有feature节点
        all_features = []
        def _collect_features(node_list, parent_module=""):
            for node in node_list:
                if isinstance(node, dict):
                    ntype = node.get("type", "")
                    if ntype == "feature" or (ntype == "" and "children" in node and node.get("children")):
                        all_features.append({"node": node, "module": parent_module})
                    # 递归子节点(但feature的children是scenarios,不再递归)
                    if ntype in ("module", "") and "children" in node:
                        _collect_features(node.get("children", []), node.get("name", parent_module))
        _collect_features(modules)

        # 校验1: 每个feature的scenario数量≥2
        low_scenario_features = []
        total_scenarios = 0
        for fi in all_features:
            node = fi["node"]
            children = node.get("children", [])
            scenario_count = len([c for c in children if isinstance(c, dict) and c.get("type") == "scenario"])
            total_scenarios += scenario_count
            if scenario_count < 2:
                mod = fi.get("module", "")
                name = node.get("name", node.get("id", "?"))
                low_scenario_features.append(f"{mod}/{name}:仅{scenario_count}个场景")

        if low_scenario_features:
            p1_quality_issues.append(f"{len(low_scenario_features)}个功能点场景不足(应≥2): {', '.join(low_scenario_features[:5])}")

        # 校验2: 总叶节点数 ≥ P0 operations × 2
        p0_path = os.path.join(data_dir, "p0_output.json")
        if os.path.exists(p0_path):
            try:
                p0_data = _read_json(p0_path)
                blocks = p0_data.get("blocks", {})
                operations = blocks.get("operations", []) if isinstance(blocks, dict) else []
                op_count = len(operations) if isinstance(operations, list) else 0
                min_expected = op_count * 2
                if total_scenarios < min_expected:
                    p1_quality_issues.append(f"场景总数{total_scenarios}<最低要求{min_expected}(P0 operations {op_count}×2)")
            except Exception:
                pass

        if p1_quality_issues:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            print(json.dumps({
                "status": "p1_quality_rejected",
                "step": "P1",
                "reason": "P1场景覆盖不达标",
                "quality_issues": p1_quality_issues,
                "hint": "每个功能点(feature)必须有≥2个scenario(1正向+1异常)。不要为规避JSON截断而压缩scenario数量--如JSON过长,精简每个scenario的description文本而非砍scenario。场景总数应≥P0 operations数量×2。"
            }))
            sys.exit(1)

    # 调用truncation_guard
    ok, msg = run_truncation_guard(skill_dir, data_dir, task_id, step)

    if ok:
        # V3.5.7: P0且开启PRD审查时,自动生成报告文件(不依赖Agent是否调用quality_check)
        if step == "P0":
            meta_path = os.path.join(data_dir, "task_meta.json")
            if os.path.exists(meta_path):
                _meta = _read_json(meta_path)
                if _meta.get("prd_quality_review", False):
                    try:
                        # 读取P0输出
                        p0_output_path = os.path.join(data_dir, "p0_output.json")
                        if os.path.exists(p0_output_path):
                            p0_data = _read_json(p0_output_path)
                            blocks_md = p0_data.get("blocks_markdown", "")
                            prd_issues_list = p0_data.get("issues", [])
                            quality_score = p0_data.get("quality_score", 0)

                            # 生成报告文件
                            report_path = os.path.join(data_dir, "prd_review_report.md")
                            score_label = "PASS" if quality_score >= 0.7 else ("CONDITIONAL_PASS" if quality_score >= 0.5 else "FAIL")
                            report_lines = [
                                "# PRD审查报告\n",
                                f"**质量评分**: {quality_score} ({score_label})\n",
                                f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
                                "\n---\n",
                                "## 📋 需求结构化结果\n",
                                (blocks_md if blocks_md else "*未输出结构化内容*"),
                                "\n\n---\n",
                                "## ⚠️ 问题清单\n",
                            ]
                            if prd_issues_list:
                                report_lines.append("| 严重度 | 位置 | 类型 | 问题 | 建议 |\n")
                                report_lines.append("|--------|------|------|------|------|\n")
                                for issue in prd_issues_list:
                                    if isinstance(issue, dict):
                                        severity = issue.get("severity", "")
                                        location = issue.get("location", "")
                                        issue_type = issue.get("type", "")
                                        problem = issue.get("problem", issue.get("issue", ""))
                                        suggestion = issue.get("suggestion", issue.get("recommendation", ""))
                                        report_lines.append(f"| {severity} | {location} | {issue_type} | {problem} | {suggestion} |\n")
                                    else:
                                        report_lines.append(f"| - | - | - | {issue} | - |\n")
                            else:
                                report_lines.append("*未发现问题*\n")
                            _write_text(report_path, "".join(report_lines))
                    except Exception:
                        pass  # 生成报告失败不影响主流程

        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete(step)
        print(json.dumps({"status": "ok", "step": step, "guard_result": msg}))
    else:
        print(json.dumps({"status": "guard_failed", "step": step, "reason": msg}))
        sys.exit(1)


# ============================================================
# V4.8.9: P1 分批生成 - skeleton → 逐feature填充 → 合并
# ============================================================

def action_p1_skeleton_save(args):
    """V4.8.9: 保存P1骨架(module+feature结构,不含scenario)"""
    data_dir = args.data_dir
    task_id = args.task_id
    agent_output = args.agent_output

    try:
        sk = json.loads(agent_output)
    except Exception:
        import re
        m = re.search(r'\{[\s\S]*\}', agent_output)
        if m:
            try:
                sk = json.loads(m.group())
            except Exception:
                print(json.dumps({"status": "error", "reason": "P1骨架JSON解析失败"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "reason": "P1骨架输出不含JSON"}))
            sys.exit(1)

    # 校验 feature_tree 存在
    ft = sk.get("feature_tree", {})
    if not ft:
        print(json.dumps({"status": "error", "reason": "缺少feature_tree字段"}))
        sys.exit(1)

    # 提取所有 feature(空children = 场景占位)
    features = []
    modules = ft.get("children", ft.get("modules", []))
    def _walk(nodes, mod_name=""):
        for node in nodes:
            if isinstance(node, dict):
                ntype = node.get("type", "")
                if ntype == "module":
                    _walk(node.get("children", []), node.get("name", mod_name))
                elif ntype == "feature":
                    fid = node.get("id", "")
                    fname = node.get("name", "")
                    child_count = len(node.get("children", []))
                    features.append({"feature_id": fid, "feature_name": fname, "module": mod_name, "current_scenarios": child_count})
    _walk(modules)

    if not features:
        print(json.dumps({"status": "error", "reason": "骨架中未找到feature节点"}))
        sys.exit(1)

    # 保存骨架
    sk_path = os.path.join(data_dir, "p1_skeleton.json")
    _write_json(sk_path, sk)

    # 创建 features 目录
    features_dir = os.path.join(data_dir, "p1_features")
    _ensure_dir(features_dir)

    print(json.dumps({
        "status": "ok",
        "skeleton_saved": "p1_skeleton.json",
        "total_features": len(features),
        "features": features,
        "hint": f"共{len(features)}个功能点,请逐feature生成scenarios。对每个feature: 1) prep_prompt --step P1 --feature-id ID 2) 生成scenario JSON 3) p1_save_feature --feature-id ID",
    }))


def action_p1_save_feature(args):
    """V4.8.9: 保存单个feature的scenario数据到 p1_features/"""
    data_dir = args.data_dir
    feature_id = getattr(args, 'feature_id', '')
    agent_output = args.agent_output

    if not feature_id:
        feature_id = getattr(args, 'feature_id_str', '')
    if not feature_id:
        print(json.dumps({"status": "error", "reason": "缺少 --feature-id 参数"}))
        sys.exit(1)

    try:
        fd = json.loads(agent_output)
    except Exception:
        import re
        m = re.search(r'\{[\s\S]*\}', agent_output)
        if m:
            try:
                fd = json.loads(m.group())
            except Exception:
                print(json.dumps({"status": "error", "reason": f"feature {feature_id} JSON解析失败"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "reason": f"feature {feature_id} 输出不含JSON"}))
            sys.exit(1)

    scenarios = fd.get("scenarios", [])
    if len(scenarios) < 2:
        print(json.dumps({
            "status": "quality_rejected",
            "feature_id": feature_id,
            "reason": f"scenario数量不足: {len(scenarios)}<2(需1正向+1异常)",
            "hint": "每个功能点至少需要2个scenario。请重新生成。"
        }))
        sys.exit(1)

    # 检查 scenario_type 多样性
    types = set(s.get("scenario_type", "") for s in scenarios)
    if "positive" not in types:
        print(json.dumps({
            "status": "quality_rejected",
            "feature_id": feature_id,
            "reason": "缺少positive类型scenario",
        }))
        sys.exit(1)

    # 保存到 p1_features/ 目录
    features_dir = os.path.join(data_dir, "p1_features")
    _ensure_dir(features_dir)
    safe_id = feature_id.replace("/", "_").replace("\\", "_")
    ft_path = os.path.join(features_dir, f"feature_{safe_id}.json")
    _write_json(ft_path, {"feature_id": feature_id, "scenarios": scenarios})

    print(json.dumps({
        "status": "ok",
        "feature_id": feature_id,
        "scenarios_saved": len(scenarios),
        "types": list(types),
    }))


def action_p1_code_merge(args):
    """V4.8.9: 合并P1骨架+所有feature scenarios → 完整 p1_output.json → Gate pass"""
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # 读取骨架
    sk_path = os.path.join(data_dir, "p1_skeleton.json")
    if not os.path.exists(sk_path):
        print(json.dumps({"status": "error", "reason": "p1_skeleton.json不存在,请先执行 p1_skeleton_save"}))
        sys.exit(1)

    sk = _read_json(sk_path)
    ft = sk.get("feature_tree", {})

    # 读取所有 feature 数据
    features_dir = os.path.join(data_dir, "p1_features")
    feature_map = {}
    if os.path.exists(features_dir):
        for fname in os.listdir(features_dir):
            if fname.startswith("feature_") and fname.endswith(".json"):
                fpath = os.path.join(features_dir, fname)
                fd = _read_json(fpath)
                fid = fd.get("feature_id", "")
                if fid:
                    feature_map[fid] = fd.get("scenarios", [])

    # 遍历骨架,填充 scenarios
    total_scenarios = 0
    missing_features = []
    modules = ft.get("children", ft.get("modules", []))

    def _fill(node):
        nonlocal total_scenarios, missing_features
        if isinstance(node, dict):
            ntype = node.get("type", "")
            if ntype == "module":
                for child in node.get("children", []):
                    _fill(child)
            elif ntype == "feature":
                fid = node.get("id", "")
                if fid in feature_map:
                    node["children"] = feature_map[fid]
                    total_scenarios += len(feature_map[fid])
                else:
                    missing_features.append(fid)

    for mod in modules:
        _fill(mod)

    if missing_features:
        print(json.dumps({
            "status": "error",
            "reason": f"{len(missing_features)}个feature缺少scenario数据: {', '.join(missing_features[:10])}",
            "hint": "请对每个feature执行: prep_prompt --step P1 --feature-id ID → 生成scenario → p1_save_feature --feature-id ID"
        }))
        sys.exit(1)

    # V4.8.8 校验: 场景数量
    p1_quality_issues = []
    low_scenario_features = []
    def _validate(node):
        if isinstance(node, dict):
            ntype = node.get("type", "")
            if ntype == "feature":
                sc = node.get("children", [])
                sc_count = len([c for c in sc if isinstance(c, dict) and c.get("type") == "scenario"])
                if sc_count < 2:
                    low_scenario_features.append(f"{node.get('id','?')}:仅{sc_count}个")
            if "children" in node:
                for c in node.get("children", []):
                    _validate(c)
    for mod in modules:
        _validate(mod)

    if low_scenario_features:
        p1_quality_issues.append(f"{len(low_scenario_features)}个功能点场景<2: {', '.join(low_scenario_features[:5])}")

    # 校验: 总数 ≥ P0 operations × 2
    p0_path = os.path.join(data_dir, "p0_output.json")
    if os.path.exists(p0_path):
        try:
            p0_data = _read_json(p0_path)
            blocks = p0_data.get("blocks", {})
            operations = blocks.get("operations", []) if isinstance(blocks, dict) else []
            op_count = len(operations) if isinstance(operations, list) else 0
            if total_scenarios < op_count * 2:
                p1_quality_issues.append(f"场景总数{total_scenarios}<{op_count*2}(P0 ops {op_count}×2)")
        except Exception:
            pass

    if p1_quality_issues:
        print(json.dumps({
            "status": "p1_merge_quality_rejected",
            "issues": p1_quality_issues,
            "hint": "请对场景不足的feature重新生成scenario,确保每个≥2个且总数达标"
        }))
        sys.exit(1)

    # 组装完整 P1 output - 兼容 P2 读取(P2 优先查 feature_tree.modules)
    # V4.8.9: 骨架用 children,转换为 modules 供 P2 读取
    if "children" in ft and "modules" not in ft:
        ft["modules"] = ft.pop("children")
    # V4.8.12: 从 task_meta 自动填充 requirement_id,避免 P2→P6 全链路 REQ-UNKNOWN
    req_id = task_id or ""
    tm_path = os.path.join(data_dir, "task_meta.json")
    if os.path.exists(tm_path):
        try:
            tm = _read_json(tm_path)
            req_id = tm.get("project", tm.get("task_id", task_id))
        except Exception:
            pass
    p1_output = {
        "feature_tree": ft,
        "requirement_id": req_id,
        "coverage_check": sk.get("coverage_check", {}),
        "statistics": {
            "total_modules": len(modules),
            "total_features": len(feature_map),
            "total_scenarios": total_scenarios,
        }
    }

    # 写入 tmp → truncation_guard → gate pass
    tmp_path = os.path.join(data_dir, "p1_output.tmp.json")
    _write_json(tmp_path, p1_output)

    ok, msg = run_truncation_guard(skill_dir, data_dir, task_id, "P1")
    if ok:
        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete("P1")
        print(json.dumps({
            "status": "ok",
            "step": "P1",
            "statistics": p1_output["statistics"],
            "merged_from": f"{len(feature_map)} features",
        }))
    else:
        print(json.dumps({"status": "guard_failed", "step": "P1", "reason": msg}))
        sys.exit(1)


# ============================================================
# Action: step7_export
# ============================================================

def action_step7_export(args):
    """Step 7: 调用export_excel.py导出

    V3.0.3: 内置quality_check硬门禁,Agent无法绕过
    """
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # 检查全链路gate pass完整性(防止Agent"表演"流程)
    required_gates = ["onboarding", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]
    missing_gates = []
    for step in required_gates:
        ok, msg = check_gate(data_dir, step, task_id)
        if not ok:
            missing_gates.append(step)

    if missing_gates:
        print(json.dumps({
            "status": "gate_blocked",
            "reason": f"以下步骤的gate pass缺失: {missing_gates}。Agent必须真正执行这些步骤(通过orchestrator),不能跳过。",
            "missing_gates": missing_gates,
        }))
        sys.exit(1)

    # V3.5.2: 全链路gate来源审计(检测 Agent 绕过 orchestrator 伪造gate的行为)
    audit_warnings = []
    for step in required_gates:
        gate_path = os.path.join(data_dir, "gates", f"{step}.pass.json")
        if os.path.exists(gate_path):
            gp = _read_json(gate_path)
            source = gp.get("source_action", "")
            # 兑容旧版本的gate(没有source_action字段)
            if source == "":
                continue
            valid = _VALID_GATE_SOURCES.get(step, [])
            if valid and source not in valid:
                audit_warnings.append(f"{step}: gate来源异常(source_action='{source}',合法来源={valid})")

    if audit_warnings:
        print(json.dumps({
            "status": "audit_blocked",
            "reason": "检测到部分步骤的gate pass来源异常,可能Agent绕过orchestrator伪造。禁止导出。",
            "details": audit_warnings,
        }))
        sys.exit(1)

    # === V3.3.0: P6用例数量底线校验(精简版,详细校验已移至P7 code_check) ===
    p6_path = os.path.join(data_dir, "p6_output.json")
    if os.path.exists(p6_path):
        p6_data = _read_json(p6_path)
        cases = p6_data.get("testcases", [])
        total = len(cases)
        if total < 15:
            print(json.dumps({
                "status": "quality_blocked",
                "reason": f"P6用例数量{total}<底线15,禁止导出",
            }))
            sys.exit(1)

        # V4.10.1: 输出完整性校验 - 防御Agent篡改
        batches_dir = os.path.join(data_dir, "p6_batches")
        batch_total = 0
        if os.path.isdir(batches_dir):
            for fn in sorted(os.listdir(batches_dir)):
                if fn.startswith("batch_") and fn.endswith(".json") and "_agent" not in fn and "_skeleton" not in fn and "_context" not in fn:
                    try:
                        bd = _read_json(os.path.join(batches_dir, fn))
                        batch_total += len(bd.get("testcases", []))
                    except Exception:
                        pass
        if batch_total > 0 and total > batch_total:
            print(json.dumps({
                "status": "integrity_blocked",
                "reason": f"p6_output.json有{total}条用例,但p6_batches/各批次合计仅{batch_total}条。数据来源可疑(可能被手动篡改),拒绝导出。请通过p6_merge重新生成。",
            }))
            sys.exit(1)

    # V4.10.1: P5完整性校验
    p5_path = os.path.join(data_dir, "p5_output.json")
    if os.path.exists(p5_path):
        p5_data = _read_json(p5_path)
        merge_log = p5_data.get("merge_log", {})
        required_merge_keys = ["from_p2", "from_p3", "from_p4"]
        missing_keys = [k for k in required_merge_keys if k not in merge_log]
        if missing_keys:
            print(json.dumps({
                "status": "integrity_blocked",
                "reason": f"p5_output.json缺少merge_log必要字段: {missing_keys}。数据来源可疑(可能被手动篡改),请通过p5_code_merge重新生成。",
            }))
            sys.exit(1)



    # === V3.3.0: P7门禁校验(必须由p7_code_check生成) ===
    p7_path = os.path.join(data_dir, "p7_output.json")
    if os.path.exists(p7_path):
        p7_data = _read_json(p7_path)
        # V3.3.1: 验证source字段确认是代码生成的
        if p7_data.get("source") != "p7_code_check":
            print(json.dumps({
                "status": "quality_blocked",
                "reason": "P7输出不是由p7_code_check生成的,禁止导出。请执行: python3 orchestrator.py --action p7_code_check",
            }))
            sys.exit(1)
        gate_result = p7_data.get("gate_result", {})
        if isinstance(gate_result, str):
            gate_passed = gate_result.upper() in ("PASS", "PASSED")
        elif isinstance(gate_result, dict):
            gate_passed = gate_result.get("status", "").upper() in ("PASS", "PASSED")
        else:
            gate_passed = False
        if not gate_passed:
            print(json.dumps({
                "status": "quality_blocked",
                "reason": f"P7质量门禁未通过: {gate_result}",
                "gate_result": gate_result,
            }))
            sys.exit(1)

    # === V3.2.6新增:P5结构特征校验(辅助防线,确认P5由代码合并生成) ===
    p5_path = os.path.join(data_dir, "p5_output.json")
    if os.path.exists(p5_path):
        p5_data = _read_json(p5_path)
        merge_log = p5_data.get("merge_log", {})
        required_merge_keys = ["from_p2", "from_p3", "from_p4"]
        missing_merge_keys = [k for k in required_merge_keys if k not in merge_log]
        if missing_merge_keys:
            print(json.dumps({
                "status": "structure_blocked",
                "reason": f"P5 merge_log缺少必要字段: {missing_merge_keys}。P5必须由p5_code_merge生成,不允许Agent自己写。",
                "missing_keys": missing_merge_keys,
            }))
            sys.exit(1)

    # === V3.2.6新增:P6批次结构校验(辅助防线,确认P6由分批流程生成) ===
    p6_batches_dir = os.path.join(data_dir, "p6_batches")
    if not os.path.isdir(p6_batches_dir):
        print(json.dumps({
            "status": "structure_blocked",
            "reason": "p6_batches目录不存在。P6必须用分批流程(p6_batch_info→p6_save_batch→p6_merge)生成,不允许Agent直接写p6_output.json。",
        }))
        sys.exit(1)
    p6_batch_files = glob.glob(os.path.join(p6_batches_dir, "batch_*.json"))
    if len(p6_batch_files) == 0:
        print(json.dumps({
            "status": "structure_blocked",
            "reason": "p6_batches目录下无batch文件。P6必须用分批流程生成。",
        }))
        sys.exit(1)

    # 读取task_meta获取文件名
    meta = _read_json(os.path.join(data_dir, "task_meta.json"))
    domain = meta.get("domain", "unknown")

    export_script = os.path.join(skill_dir, "tools", "export_excel.py")
    p6_path = os.path.join(data_dir, "p6_output.json")
    output_path = os.path.join(data_dir, f"测试用例_{task_id}.xlsx")

    result = subprocess.run(
        ["python3", export_script, "--input", p6_path, "--output", output_path],
        capture_output=True, text=True, timeout=60
    )

    if result.returncode == 0 and os.path.exists(output_path):
        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete("step7")
        # V3.2.9: 重置重试计数
        state.state.pop("p6_retry_count", None)
        state.save()

        # V4.0.0: 推送到云端评审工具
        push_result = None
        # V4.1.2: 优先从data_dir/.image_api_key读取runtime api_key(Onboarding时输入)
        runtime_key = None
        cache_path = os.path.join(args.data_dir, ".image_api_key")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    runtime_key = f.read().strip()
            except Exception:
                pass
        config = _load_cloud_config(args.skill_dir, runtime_api_key=runtime_key)
        if _should_push_to_review_tool(config):
            try:
                review_url = _push_to_review_tool(args.data_dir, args.task_id, config)
                if review_url:
                    push_result = {
                        "pushed": True,
                        "review_url": review_url,
                        "message": "✅ 用例已推送到在线评审工具"
                    }
                else:
                    push_result = {
                        "pushed": False,
                        "review_url": None,
                        "message": "⚠️ 推送失败,已加入重试队列"
                    }
            except Exception as e:
                push_result = {
                    "pushed": False,
                    "review_url": None,
                    "message": f"⚠️ 推送异常: {str(e)}"
                }
                print(json.dumps({
                    "message": f"⚠️ 推送异常: {str(e)}"
                }), file=sys.stderr)
        else:
            # V4.12.6: api_key缺失时明确提示
            push_result = {
                "pushed": False,
                "review_url": None,
                "message": "⚠️ 未配置api_key,跳过推送。配置方式: Onboarding时输入密码 或 在cloud.json中设置review_tool.api_key"
            }

        output_data = {
            "status": "ok",
            "excel_path": output_path,
            "file_size": os.path.getsize(output_path),
            "media_instruction": f"MEDIA:{output_path}",
            "__must_emit__": f"MEDIA:{output_path}",
            "reminder": "🔴 必须在回复中独占一行输出: MEDIA:{output_path} (将此行原样输出,不可省略)",
        }
        if push_result:
            output_data["cloud_review"] = push_result
        print(json.dumps(output_data))
    else:
        # V3.2.9: 失败时检查重试计数,返回结构化重试指引
        state = TaskState(data_dir=data_dir, task_id=task_id)
        retry_count = state.state.get("p6_retry_count", 0)
        error_msg = result.stderr[:300] if result.stderr else "unknown"

        if retry_count < 4:
            # 可重试:返回明确的自动回流指令
            state.state["p6_retry_count"] = retry_count + 1
            state.save()
            print(json.dumps({
                "status": "auto_retry",
                "retry_count": retry_count + 1,
                "max_retries": 2,
                "reason": f"Excel导出失败: {error_msg}",
                "action": "Agent必须立即执行 restart_from P6 然后重新走段落7的分批流程,禁止向用户抛选择题",
            }))
            sys.exit(1)
        else:
            # 超过最大重试次数,报告用户
            print(json.dumps({
                "status": "error",
                "reason": f"Excel导出失败(已重试{retry_count}次): {error_msg}",
                "retry_exhausted": True,
            }))
            sys.exit(1)


# ============================================================
# Action: retry_push (V4.0.0: 重试推送失败的评审任务)
# ============================================================

def action_retry_push(args):
    """重试推送失败的任务。

    读取 queue/pending_reviews.jsonl,逐个重试推送,
    成功的从队列移除,失败的保留,返回重试统计。
    """
    skill_dir = args.skill_dir
    data_dir = args.data_dir

    # 队列文件位置:data_dir同级的queue目录
    base_dir = os.path.dirname(data_dir) if data_dir else os.path.expanduser("~/.openclaw/workspace/data")
    queue_path = os.path.join(base_dir, "queue", "pending_reviews.jsonl")

    if not os.path.exists(queue_path):
        print(json.dumps({"status": "ok", "message": "无待重试任务", "total": 0, "success": 0, "failed": 0}))
        return

    # 读取队列
    tasks = []
    try:
        with open(queue_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        tasks.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(json.dumps({"status": "error", "reason": f"队列文件读取失败: {e}"}))
        sys.exit(1)

    if not tasks:
        print(json.dumps({"status": "ok", "message": "队列为空,无待重试任务", "total": 0, "success": 0, "failed": 0}))
        return

    # 加载配置(使用当前data_dir的api_key)
    runtime_key = None
    cache_path = os.path.join(data_dir, ".image_api_key")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                runtime_key = f.read().strip()
        except Exception:
            pass
    config = _load_cloud_config(skill_dir, runtime_api_key=runtime_key)

    success_count = 0
    failed_tasks = []
    success_urls = []

    for task in tasks:
        task_data_dir = task.get("data_dir", "")
        task_task_id = task.get("task_id", "")
        retry_count = task.get("retry_count", 0)

        if not task_data_dir or not task_task_id:
            failed_tasks.append(task)
            continue

        # 尝试重新推送
        review_url = _push_to_review_tool(task_data_dir, task_task_id, config)
        if review_url:
            success_count += 1
            success_urls.append({"task_id": task_task_id, "review_url": review_url})
        else:
            # 推送失败,保留在队列中(更新retry_count)
            task["retry_count"] = retry_count + 1
            task["last_retry"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            failed_tasks.append(task)

    # 重写队列文件(只保留失败的)
    try:
        with open(queue_path, "w", encoding="utf-8") as f:
            for task in failed_tasks:
                f.write(json.dumps(task, ensure_ascii=False) + "\n")
    except Exception:
        pass

    print(json.dumps({
        "status": "ok",
        "total": len(tasks),
        "success": success_count,
        "failed": len(failed_tasks),
        "success_urls": success_urls,
        "message": f"重试完成: {success_count}成功, {len(failed_tasks)}失败"
    }))


# ============================================================
# Action: status
# ============================================================

def action_status(args):
    """查看当前任务状态"""
    data_dir = args.data_dir
    task_id = args.task_id

    state = TaskState(data_dir=data_dir, task_id=task_id)
    next_step = state.get_next_step()

    # 检查所有gate pass
    gates = {}
    gates_dir = os.path.join(data_dir, "gates")
    if os.path.exists(gates_dir):
        for f in os.listdir(gates_dir):
            if f.endswith(".pass.json"):
                step_name = f.replace(".pass.json", "")
                gates[step_name] = True

    print(json.dumps({
        "task_id": task_id,
        "completed_steps": state.state["completed_steps"],
        "next_step": next_step,
        "gates": gates,
    }))


# ============================================================
# Action: resume
# ============================================================

def action_resume(args):
    """断点续跑:检测已完成步骤,返回下一步"""
    data_dir = args.data_dir
    task_id = args.task_id

    state = TaskState(data_dir=data_dir, task_id=task_id)

    # 扫描gate pass补充completed_steps
    gates_dir = os.path.join(data_dir, "gates")
    if os.path.exists(gates_dir):
        for f in sorted(os.listdir(gates_dir)):
            if f.endswith(".pass.json"):
                step_name = f.replace(".pass.json", "")
                try:
                    gp = _read_json(os.path.join(gates_dir, f))
                    if gp.get("task_id") == task_id:
                        if step_name not in state.state["completed_steps"]:
                            state.state["completed_steps"].append(step_name)
                except Exception:
                    pass
        state.save()

    next_step = state.get_next_step()

    print(json.dumps({
        "status": "ok",
        "task_id": task_id,
        "completed_steps": state.state["completed_steps"],
        "next_step": next_step,
    }))


# ============================================================
# Action: prep_prompt (为每个P步骤准备完整prompt)
# ============================================================

# Prompt文件映射
PROMPT_FILES = {
    "P0": "prompts/P0_requirement_structuring.md",
    "P1": "prompts/P1_feature_tree_generation.md",
    "P2": "prompts/P2_test_point_draft.md",
    "P3": "prompts/P3_risk_identification.md",
    "P4": "prompts/P4_pci_identification.md",
    "P5": "prompts/P5_test_point_merge.md",
    "P6": "prompts/P6_testcase_generation.md",
    "P7": "prompts/archive/P7_quality_gate.md",  # V3.3.1: deprecated, P7走p7_code_check
}

# 每步需要的上游产物
UPSTREAM_FILES = {
    "P0": ["task_meta.json"],
    "P1": ["p0_output.json"],
    "P2": ["p1_output.json"],
    "P3": ["p1_output.json"],
    "P4": ["p1_output.json"],
    "P5": ["p2_output.json", "p3_output.json", "p4_output.json"],
    "P6": [],  # V3.3.2: 移除完整p5注入,改为批次信息中注入P1 scenario语义
    "P7": ["p6_output.json"],
}

# 知识注入映射
KNOWLEDGE_INJECT = {
    "P0": ["knowledge/industry/{domain}.md", "knowledge/methodology/design_methods.md"],
    "P1": ["knowledge/methodology/design_methods.md"],
    "P2": ["knowledge/methodology/boundary_rules.md", "knowledge/methodology/api_test_standard.md"],
    "P3": ["knowledge/industry/{domain}.md"],
    "P4": ["knowledge/industry/{domain}.md"],
    "P5": [],
    "P6": ["knowledge/company_standards/testcase_design_spec.md"],  # V3.3.2: 移除defect_schema(与P6用例生成无关)
    "P7": [],
}

def _read_file_safe(path, max_chars=8000):
    """安全读取文件,不存在返回空字符串"""
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:max_chars]
    except Exception:
        return ""

def action_prep_prompt(args):
    """为指定的P步骤准备完整prompt,输出给Agent执行"""
    skill_dir = args.skill_dir
    data_dir = args.data_dir
    task_id = args.task_id
    step = args.step  # Bugfix V4.6.8: step未定义会导致NameError
    batch_index = int(getattr(args, 'batch_index', 0))  # P6分批用,确保int类型

    # V3.3.3: 代码路径步骤禁止生成Prompt(P6保留,分批流程需要)
    PREP_PROMPT_BLOCKED = {"P2": "p2_code_generate", "P5": "p5_code_merge", "P7": "p7_code_check"}
    if step in PREP_PROMPT_BLOCKED:
        print(json.dumps({
            "status": "rejected",
            "reason": f"❌ {step}禁止生成Prompt!{step}由代码自动执行,必须用: python3 orchestrator.py --action {PREP_PROMPT_BLOCKED[step]}",
            "correct_action": PREP_PROMPT_BLOCKED[step],
        }))
        sys.exit(1)

    if step not in PROMPT_FILES:
        print(json.dumps({"status": "error", "reason": f"不支持的步骤: {step}"}))
        sys.exit(1)

    # 前置gate pass检查
    prerequisites = {
        "P0": ["onboarding"], "P1": ["P0"], "P2": ["P1"],
        "P3": ["P1"], "P4": ["P1"], "P5": ["P2", "P3", "P4"],
        "P6": ["P5"], "P7": ["P6"],
    }
    for prereq in prerequisites.get(step, []):
        ok, msg = check_gate(data_dir, prereq, task_id)
        if not ok:
            print(json.dumps({"status": "gate_blocked", "step": prereq, "reason": msg}))
            sys.exit(1)

    # 1. 读取prompt模板
    prompt_path = os.path.join(skill_dir, PROMPT_FILES[step])
    prompt_template = _read_file_safe(prompt_path, 15000)
    if not prompt_template:
        print(json.dumps({"status": "error", "reason": f"Prompt文件不存在: {PROMPT_FILES[step]}"}))
        sys.exit(1)

    # V4.8.9: P1分批模式 - skeleton / feature场景
    if step == "P1":
        mode = getattr(args, 'mode', '')
        feature_id = getattr(args, 'feature_id', '')
        if mode == "skeleton":
            sk_path = os.path.join(skill_dir, "prompts", "P1_skeleton.md")
            prompt_template = _read_file_safe(sk_path, 8000) or prompt_template
        elif feature_id:
            # 加载 feature 场景专用 prompt
            sc_path = os.path.join(skill_dir, "prompts", "P1_feature_scenario.md")
            prompt_template = _read_file_safe(sc_path, 8000) or prompt_template
            # 读取骨架获取feature上下文
            sk_path = os.path.join(data_dir, "p1_skeleton.json")
            feature_context = {"feature_id": feature_id, "feature_name": "", "description": ""}
            related_rules = []
            if os.path.exists(sk_path):
                sk = _read_json(sk_path)
                ft = sk.get("feature_tree", {})
                modules = ft.get("children", ft.get("modules", []))
                def _find_feature(nodes):
                    for n in nodes:
                        if n.get("id") == feature_id:
                            feature_context["feature_name"] = n.get("name", "")
                            feature_context["description"] = n.get("description", "")
                            return
                        if "children" in n:
                            _find_feature(n["children"])
                _find_feature(modules)
                # 注入关联的P0业务规则
                p0_path_f = os.path.join(data_dir, "p0_output.json")
                if os.path.exists(p0_path_f):
                    p0 = _read_json(p0_path_f)
                    blocks = p0.get("blocks", {})
                    business_rules = blocks.get("business_rules", []) if isinstance(blocks, dict) else []
                    related_rules = [r for r in business_rules if feature_id.lower() in str(r).lower()]
                    relations_text = p0.get("relations", [])
                    if relations_text:
                        related_rules += [r for r in relations_text if feature_id.lower() in str(r).lower()]
            prompt_template = prompt_template.replace("{{feature_context}}", json.dumps(feature_context, ensure_ascii=False, indent=2))
            prompt_template = prompt_template.replace("{{related_rules}}", json.dumps(related_rules[:10], ensure_ascii=False, indent=2) if related_rules else "[]")

    # V3.3.2: P6接口测试规则按需注入
    if step == "P6":
        # V4.8.10: 入口拦截 - P6禁止在子Agent中执行,prep_prompt是P6第一个入口
        if _is_sub_agent_session():
            print(json.dumps({
                "status": "rejected",
                "reason": "⛔ P6禁止在子Agent中执行!prep_prompt是P6入口,子Agent不能生成用例。",
                "hint": "请回到主会话执行。子Agent没有完整的context文件数据,无法生成高质量用例(会产出占位符)。"
            }))
            sys.exit(1)
        has_api = _check_api_features(data_dir)
        if has_api:
            api_rules_path = os.path.join(skill_dir, "prompts", "P6_api_rules.md")
            api_rules = _read_file_safe(api_rules_path, 5000)
            if api_rules:
                prompt_template += f"\n\n---\n{api_rules}"

        # V4.0.1: 文件上传安全用例条件注入
        # 仅当需求涉及文件上传/导入时才保留该section,否则替换为跳过提示
        _upload_keywords = ["上传", "导入", "批量", "文件", "Excel", "CSV", "附件", "docx", "xlsx", "上传文件", "批量导入"]
        _meta_path_p6 = os.path.join(data_dir, "task_meta.json")
        _req_text_p6 = ""
        if os.path.exists(_meta_path_p6):
            try:
                _meta_p6 = _read_json(_meta_path_p6)
                _req_text_p6 = _meta_p6.get("requirement_text", "")
            except Exception:
                pass
        _has_file_upload = any(kw in _req_text_p6 for kw in _upload_keywords)
        if not _has_file_upload:
            # 替换文件上传安全用例section为跳过提示
            _upload_section_marker = "### 文件上传场景安全用例(强制)"
            if _upload_section_marker in prompt_template:
                # 找到section开始位置,截取到下一个###或---分隔符
                _start_idx = prompt_template.index(_upload_section_marker)
                _rest = prompt_template[_start_idx + len(_upload_section_marker):]
                # 找下一个section分隔符
                _end_offset = len(_rest)
                for _sep in ["\n### ", "\n---", "\n## "]:
                    _sep_pos = _rest.find(_sep)
                    if _sep_pos != -1 and _sep_pos < _end_offset:
                        _end_offset = _sep_pos
                _end_idx = _start_idx + len(_upload_section_marker) + _end_offset
                _skip_notice = "### 文件上传场景安全用例(强制)\n【安全用例跳过】当前需求不涉及文件上传/导入功能,跳过安全用例生成\n"
                prompt_template = prompt_template[:_start_idx] + _skip_notice + prompt_template[_end_idx:]

        # V4.8.1: LOW模型适配 - 引导卡 + 微型 prompt
        # 优先级:state(自动检测) > --model-name(显式指定) > OPENCLAW_MODEL(环境变量) > 兜底LOW
        model_name = ''
        model_tier = 'LOW'  # 兜底保守策略
        state_path = os.path.join(data_dir, 'orchestrator_state.json')
        if os.path.exists(state_path):
            try:
                st = _read_json(state_path)
                model_tier = st.get('model_tier', 'LOW')
                model_name = st.get('model_name', '')
            except Exception:
                pass
        # 如果 state 中没有,尝试从参数/环境变量获取
        if not model_name:
            model_name = getattr(args, 'model_name', '') or os.environ.get('OPENCLAW_MODEL', '')
            if model_name:
                md = _get_model_detect()
                model_tier = md.classify(model_name)

        # 如果是 LOW 模型 → 走引导卡模式
        if model_tier == "LOW":
            pg = _get_p6_guide()
            # 读取当前批次的测试点
            batch_points = []
            p5_path = os.path.join(data_dir, "p5_output.json")
            if os.path.exists(p5_path):
                try:
                    p5_data = _read_json(p5_path)
                    all_tps = p5_data.get("test_points", [])
                    # LOW模式用小批次(每批3-5个测试点)
                    md = _get_model_detect()
                    bs = md.get_batch_size("LOW", len(all_tps))
                    start = batch_index * bs
                    end = min(start + bs, len(all_tps))
                    batch_points = all_tps[start:end]
                    # V4.9.1: P7修复模式 - 指定TP子集过滤
                    tp_ids = getattr(args, 'tp_ids', '')
                    if tp_ids and step == "P6":
                        wanted = set(tp_ids.split(','))
                        batch_points = [bp for bp in batch_points if bp.get('id','') in wanted]
                        if not batch_points:  # 兜底:跨batch查找
                            batch_points = [bp for bp in all_tps if bp.get('id','') in wanted]
                except Exception:
                    pass
            # 读取 P0/P1 数据
            p0_data = {}
            p1_data = {}
            p0_path = os.path.join(data_dir, "p0_output.json")
            p1_path = os.path.join(data_dir, "p1_output.json")
            if os.path.exists(p0_path):
                try:
                    p0_data = _read_json(p0_path)
                except Exception:
                    pass
            if os.path.exists(p1_path):
                try:
                    p1_data = _read_json(p1_path)
                except Exception:
                    pass

            # V4.10.0: LOW模型窄聚焦模式 - 精简prompt,Agent只产出3个核心字段
            simple_prompt_path = os.path.join(skill_dir, "prompts", "P6_low_simple.md")
            simple_template = _read_file_safe(simple_prompt_path, 2000)
            if simple_template and "{{business_context}}" in simple_template and batch_points:
                # 1. 构建业务上下文(从P0/P1提取)
                biz_lines = []
                if p0_data:
                    blocks = p0_data.get("blocks", {})
                    obj = blocks.get("objective", "") if isinstance(blocks, dict) else ""
                    if obj:
                        biz_lines.append(f"需求目标:{str(obj)[:200]}")
                    rules = blocks.get("business_rules", []) if isinstance(blocks, dict) else []
                    for r in (rules or [])[:3]:
                        if isinstance(r, dict) and r.get("description"):
                            biz_lines.append(f"业务规则:{r['description'][:150]}")
                if p1_data:
                    ft = p1_data.get("feature_tree", {})
                    fms = ft.get("modules", []) if isinstance(ft, dict) else p1_data.get("modules", [])
                    for mod in fms:
                        for feat in mod.get("children", []):
                            if feat.get("type") == "feature":
                                biz_lines.append(f"功能模块:{mod.get('name','')} → {feat.get('name','')}"[:100])
                                break
                business_context = "\n".join(biz_lines[:8]) or "根据需求文档生成测试用例"

                # 2. 格式化测试点列表(精简,只保留核心信息)
                tp_lines = []
                for bp in batch_points[:10]:
                    desc = (bp.get("description", "") or "")[:120]
                    pri = bp.get("priority", "P1")
                    tp_lines.append(f"- [{pri}] {desc}")
                test_points_text = "\n".join(tp_lines)

                # 3. 构建示例(从第一个TP的P1 scenario提取)
                example_text = "验证分润比例录入后保存成功:\n步骤: 1. 进入分润管理页面 2. 对员工设置分润比例 3. 点击保存按钮\n期望: 1. 页面刷新显示更新后数据 2. 系统提示保存成功"
                first_bp = batch_points[0] if batch_points else {}
                src_id = first_bp.get("source_scenario", "")
                if p1_data and src_id:
                    ft = p1_data.get("feature_tree", {})
                    fms = ft.get("modules", []) if isinstance(ft, dict) else p1_data.get("modules", [])
                    for mod in fms:
                        for feat in mod.get("children", []):
                            for scen in feat.get("children", []):
                                if scen.get("id") == src_id and scen.get("type") == "scenario":
                                    sn = scen.get("name", "验证功能")
                                    ops = scen.get("operations_chain") or scen.get("operations_steps", [])
                                    if ops and isinstance(ops, list) and len(ops) >= 2:
                                        op_lines = [f"{i+1}. {o.get('action','操作')}「{o.get('target','目标')}」{',输入' + o.get('value','') if o.get('value') else ''}" for i, o in enumerate(ops[:4])]
                                        exp_lines = [f"{i+1}. {o.get('expected','预期结果')}" for i, o in enumerate(ops[:4])]
                                        example_text = f"{sn}:\n步骤:\n" + "\n".join(op_lines) + "\n期望:\n" + "\n".join(exp_lines)
                                    break

                # 4. 组装精简prompt
                simple_prompt = simple_template
                simple_prompt = simple_prompt.replace("{{business_context}}", business_context)
                simple_prompt = simple_prompt.replace("{{test_points}}", test_points_text)
                simple_prompt = simple_prompt.replace("{{examples}}", example_text)
                simple_prompt = simple_prompt.replace("{{expected_case_count}}", str(max(bp.get("expected_case_count", 2) for bp in batch_points)))

                # 5. 生成骨架(仅case_id映射,Agent不写其余16列)
                _build_skeleton_for_batch(data_dir, batch_points, batch_index)

                # 5b. 提取case_id清单注入prompt
                sk_path = os.path.join(data_dir, "p6_batches", f"batch_{batch_index:03d}_skeleton.json")
                case_ids = []
                if os.path.exists(sk_path):
                    sk_data = _read_json(sk_path)
                    for sk in sk_data:
                        cid = sk.get("case_id", "")
                        desc = sk.get("p5_description", "")[:60]
                        case_ids.append(f"{cid}  ← {desc}" if desc else cid)
                case_id_list = "\n".join(case_ids) if case_ids else "(无骨架数据,请使用格式 REQ-xxx-TP-NNN-TC-001)"
                simple_prompt = simple_prompt.replace("{{case_id_list}}", case_id_list)

                tier_info = json.dumps({"status": "ok", "mode": "simple", "tier": model_tier, "batch_index": batch_index, "model_name": model_name, "tp_count": len(batch_points), "prompt_size": len(simple_prompt)})
                print(tier_info, file=sys.stderr)
                print(simple_prompt)
                return

            # 降级到旧的引导卡模式(P6_low_simple.md不存在时)
            # 生成引导卡
            guides = pg.generate_guide_cards(batch_points, p0_data, p1_data, skill_dir)
            guide_json = json.dumps(guides, ensure_ascii=False, indent=2)
            # 加载微型 prompt 模板
            guided_prompt_path = os.path.join(skill_dir, "prompts", "P6_guided.md")
            guided_template = _read_file_safe(guided_prompt_path, 5000)
            if guided_template:
                # 替换引导卡占位符
                guided_template = guided_template.replace("{{guides}}", guide_json)
                # 替换禁止词样本
                if guides:
                    g0 = guides[0]
                    step_sample = "、".join(g0.get("step_must_avoid", [])[:5])
                    exp_sample = "、".join(g0.get("expected_must_avoid", [])[:5])
                    guided_template = guided_template.replace("{{step_must_avoid_sample}}", step_sample)
                    guided_template = guided_template.replace("{{expected_must_avoid_sample}}", exp_sample)
                # 输出微型 prompt,跳过后续的通用 prompt 组装
                tier_info = json.dumps({"status": "ok", "mode": "guided", "tier": model_tier, "batch_index": batch_index, "guide_count": len(guides), "model_name": model_name})
                print(tier_info, file=sys.stderr)
                print(guided_template)
                return
            else:
                # 微型 prompt 不存在,降级到精简模式(继续现有流程)
                print(json.dumps({"status": "warning", "reason": "P6_guided.md不存在,降级到标准prompt", "model_tier": model_tier}), file=sys.stderr)

    # 2. 读取上游产物
    upstream_data = {}
    for fname in UPSTREAM_FILES.get(step, []):
        fpath = os.path.join(data_dir, fname)
        content = _read_file_safe(fpath, 20000)
        if content:
            upstream_data[fname] = content

    # 3. 知识注入
    # 读取domain
    meta_path = os.path.join(data_dir, "task_meta.json")
    domain = "trade"
    requirement_text = ""
    if os.path.exists(meta_path):
        try:
            meta = _read_json(meta_path)
            domain = meta.get("domain", "trade")
            requirement_text = meta.get("requirement_text", "")
        except Exception:
            pass

    knowledge_texts = []
    for kpath_template in KNOWLEDGE_INJECT.get(step, []):
        kpath = os.path.join(skill_dir, kpath_template.replace("{domain}", domain))
        kt = _read_file_safe(kpath, 3000)
        if kt:
            knowledge_texts.append(kt)

    # V4.0.0: 项目名→业务域自动匹配,4层渐进注入
    project_match = _match_project_to_domains(requirement_text, skill_dir)
    project_knowledge_texts = []
    if project_match["matched_projects"] or project_match["matched_synonyms"]:
        # 根据当前步骤选择注入层级
        # P0 → L1(领域入门引导,~2-3K/域)
        # P1 → L2(领域蓝图,~4-6K/域)
        # P2/P3/P4/P5 → L3(领域规则集,~6-9K/域)
        # P6/P7 → L4(全文/动态检索)
        step_level_map = {"P0": "L1", "P1": "L2", "P2": "L3", "P3": "L3", "P4": "L3", "P5": "L3", "P6": "L4", "P7": "L4"}
        inject_level = step_level_map.get(step, "L1")

        # 同义词匹配的域只注入L1(防止高频词导致prompt膨胀)
        synonym_only_domains = set()
        if project_match["matched_synonyms"] and not project_match["matched_projects"]:
            # 纯同义词匹配:所有域都限制L1
            synonym_only_domains = set(project_match["domains"])
        elif project_match["matched_synonyms"] and project_match["matched_projects"]:
            # 有项目匹配:同义词匹配到的额外域(不在项目匹配结果中的)限制L1
            # 简化处理:通过比较域列表长度判断是否有额外域
            project_domain_count = len(set())  # 占位,下方通过实际匹配判断
            # 由于无法在此处区分哪些域来自项目vs同义词,统一按正常层级注入
            # 但限制总注入量不超过15KB(安全阈值)
            pass

        summaries_dir = os.path.join(skill_dir, "knowledge", "industry", "summaries")

        for kf in project_match["knowledge_files"]:
            base_name = kf["file"].replace(".md", "")
            domain = kf["domain"]
            # 同义词独有的域限制L1,项目匹配的域用正常层级
            actual_level = "L1" if domain in synonym_only_domains else inject_level
            kt = None

            if actual_level == "L4":
                # L4: 全文注入(P6/P7)
                kf_full_path = os.path.join(skill_dir, "knowledge", "industry", kf["file"])
                kt = _read_file_safe(kf_full_path, 25000)
            elif actual_level in ("L1", "L2", "L3"):
                # L1/L2/L3: 优先读预编译JSON,不存在则降级读全文截取
                level_file = os.path.join(summaries_dir, f"{base_name}_{actual_level}.json")
                if os.path.exists(level_file):
                    kt = _read_file_safe(level_file, 10000)
                    if kt:
                        # JSON文件直接作为结构化知识注入
                        kt = f"## {domain}知识库({actual_level})\n{kt}"

                if not kt:
                    # 降级:读取全文,按层级截取不同大小
                    fallback_sizes = {"L1": 2000, "L2": 4000, "L3": 6000}
                    fallback_size = fallback_sizes.get(actual_level, 2000)
                    kf_full_path = os.path.join(skill_dir, "knowledge", "industry", kf["file"])
                    kt_raw = _read_file_safe(kf_full_path, fallback_size)
                    if kt_raw:
                        kt = f"## {domain}知识库({actual_level}降级)\n{kt_raw}"

            if kt:
                project_knowledge_texts.append(kt)

        if project_knowledge_texts:
            # 注入匹配信息
            match_parts = []
            if project_match['matched_projects']:
                match_parts.append(f"项目: {', '.join(project_match['matched_projects'])}")
            if project_match['matched_synonyms']:
                match_parts.append(f"同义词: {', '.join(project_match['matched_synonyms'])}")
            match_info = f"\n识别到 {', '.join(match_parts)} → 关联业务域: {', '.join(project_match['domains'])} → 注入层级: {inject_level}\n"
            knowledge_texts.insert(0, match_info)
            knowledge_texts.extend(project_knowledge_texts)

    # 4. PX增强注入(如有)
    px_inject = ""
    px_enhance_path = os.path.join(data_dir, "px_enhance.json")
    if os.path.exists(px_enhance_path):
        try:
            px_data = _read_json(px_enhance_path)
            step_subsets = px_data.get("step_subsets", {})
            step_key = step  # P0/P1/...
            if step_key in step_subsets:
                px_inject = json.dumps(step_subsets[step_key], ensure_ascii=False)
                # Qwen VL的description可能很长,截取注入不超过3000字符
                if len(px_inject) > 3000:
                    px_inject = px_inject[:3000] + "\n...(内容过长已截断)"
        except Exception:
            pass

    # 5. P6分批处理
    p6_batch_info = ""
    if step == "P6" and batch_index >= 0:
        # 读取P5测试点,按批次切分
        p5_path = os.path.join(data_dir, "p5_output.json")
        if os.path.exists(p5_path):
            try:
                p5 = _read_json(p5_path)
                test_points = p5.get("test_points", [])
                # V4.6.17: 启用动态分批
                batch_info = calculate_dynamic_batches(test_points, max_batches=5)
                total_batches = batch_info["total_batches"]
                strategy = batch_info.get("strategy", "dynamic")
                # 按batch_index定位当前批次(V4.8.12: 0-based)
                if batch_index < len(batch_info["batches"]):
                    b = batch_info["batches"][batch_index]
                    batch_points = test_points[b["start"]:b["end"]]
                else:
                    batch_points = []
                # V4.9.1: P7修复模式 - 指定TP子集过滤
                tp_ids = getattr(args, 'tp_ids', '')
                if tp_ids and step == "P6" and batch_points:
                    wanted = set(tp_ids.split(','))
                    batch_points = [bp for bp in batch_points if bp.get('id','') in wanted]
                    if not batch_points:
                        batch_points = [tp for tp in test_points if tp.get('id','') in wanted]
                start = batch_info["batches"][batch_index]["start"] if batch_index < len(batch_info["batches"]) else 0
                # V3.2.8: 注入complexity预算信息
                batch_budget = sum(bp.get("expected_case_count", 2) for bp in batch_points)
                budget_detail = []
                for bp in batch_points:
                    bp_id = bp.get("id", "?")
                    bp_complexity = bp.get("complexity", "L2")
                    bp_expected = bp.get("expected_case_count", 2)
                    budget_detail.append(f"  - {bp_id}: {bp_complexity}(应展开{bp_expected}条)")
                budget_text = f"\n\n## ❗ 本批次用例预算(必须遵守)\n本批次应生成至少 **{batch_budget}条** 用例。每个测试点的展开数量如下:\n" + "\n".join(budget_detail) + f"\n\n复杂度说明:L1(简单)≥{1}条, L2(常规)≥{2}条, L3(复杂)≥{3}条。复杂测试点可以展开更多。"
                # V3.2.8: 精简字段版batch_points(避免全量 JSON被[:5000]截断削弱预算绑定)
                slim_points = []
                for bp in batch_points:
                    slim_points.append({
                        "id": bp.get("id", ""),
                        "description": bp.get("description", ""),
                        "category": bp.get("category", ""),
                        "priority": bp.get("priority", ""),
                        "risk_flag": bp.get("risk_flag", False),
                        "pci_flag": bp.get("pci_flag", False),
                        "complexity": bp.get("complexity", "L2"),
                        "expected_case_count": bp.get("expected_case_count", 2),
                    })
                # V3.2.9: 骨架预分配(priority/is_smoke由代码预设,Agent只填内容)
                # 冷烟分配策略:每个测试点的第1条用例为正向验证,仅当测试点priority为P0且category为main_flow/branch/integration时标记冷烟
                def _extract_keywords(desc):
                    """V4.1.2: 从description提取核心操作关键词,消除通用截断"""
                    if not desc:
                        return ""
                    # 去掉验证类型前缀
                    for prefix in ["验证正向-", "验证异常-", "验证边界-", "验证-", "边界值-"]:
                        desc = desc.replace(prefix, "")
                    # 取第一段(按标点分割),最多40字符
                    core = desc.split("。")[0].split(",")[0].split(";")[0][:40]
                    return core.strip() or (desc[:25] if desc else "")

                def _generate_pairs(bp, bp_category, case_idx, keywords, bp_desc):
                    """V4.6.17 DEPRECATED: 不再调用,Agent基于P5原文自由创作步骤。保留以供参考。"""
                    """DEPRECATED"""
                    return []  # V4.6.17: 已废弃,不再调用

                SMOKE_CATEGORIES = {"main_flow", "branch", "integration", "正向验证", "分支验证", "集成验证"}
                case_skeletons = []
                batch_smoke_count = 0
                batch_total_count = 0
                for bp in batch_points:
                    bp_id = bp.get("id", "")
                    bp_priority = bp.get("priority", "P1")
                    bp_category = (bp.get("category", "") or "").lower()
                    bp_expected = bp.get("expected_case_count", 2)
                    for case_idx in range(1, bp_expected + 1):
                        batch_total_count += 1
                        # 第1条=正向验证,后续=异常/边界
                        if case_idx == 1:
                            case_priority = bp_priority
                            # 冷烟标记:P0+主流程类别才标冷烟,且控制总比例≨20%
                            is_smoke = (bp_priority == "P0" and bp_category in SMOKE_CATEGORIES)
                        else:
                            # 后续用例降一级优先级
                            case_priority = "P2" if bp_priority in ("P0", "P1") else "P3"
                            is_smoke = False
                        if is_smoke:
                            batch_smoke_count += 1
                                # V4.6.17: 骨架只分配元数据,不给步骤草稿
                        # Agent基于P5测试点原始description/precondition自行创作步骤
                        bp_desc = bp.get("description", "")
                        bp_precond = bp.get("precondition", "")
                        bp_rules = bp.get("related_rules", [])

                        case_skeletons.append({
                            "case_id": f"{bp_id}-TC-{case_idx:03d}",
                            "source_test_point": bp_id,
                            "priority": case_priority,
                            "is_smoke": is_smoke,
                            # P5原始数据注入,Agent基于这些自由创作
                            "p5_description": bp_desc,
                            "p5_precondition": bp_precond,
                            "p5_related_rules": bp_rules,
                        })
                # 冷烟比例安全检查:如果批次内无冷烟且有P0测试点,强制第一个P0的第1条为冷烟
                if batch_smoke_count == 0:
                    for sk in case_skeletons:
                        if sk["priority"] == "P0":
                            sk["is_smoke"] = True
                            batch_smoke_count = 1
                            break

                # V4.8.14: P0比例自动降级--防止小批次P0浓度过高被Gate拒绝
                # 根因:P2给每个feature第1个main_flow升P0,导致P0占整体的40-60%。
                # LOW模型每批5个测试点,部分批次聚类3-5个P0测试点→P0比例可达36-55%→被Gate拒绝。
                # 解决:骨架生成阶段预降级,确保每批P0≤阈值,Agent基于降级后骨架生成。
                p0_limit = 0.35  # LOW模型阈值(已确认当前在LOW分支内)
                smoke_limit = 0.30
                total_skeleton = len(case_skeletons)
                if total_skeleton > 0:
                    p0_skeletons = [sk for sk in case_skeletons if sk["priority"] == "P0"]
                    p0_count = len(p0_skeletons)
                    p0_ratio = p0_count / total_skeleton

                    if p0_ratio > p0_limit:
                        # 计算需要降级的P0用例数(ceil确保降级后≤阈值)
                        max_p0 = int(total_skeleton * p0_limit)
                        downgrade_count = p0_count - max_p0

                        # V4.8.14: Feature级别P0保护--从source_test_point提取feature归属,
                        # 降级时确保每个feature至少保留1条P0,防止某feature完全失去P0覆盖。
                        def _extract_feature_key(sk):
                            """从source_test_point提取feature key,如 REQ-XXX-M01-F01-TP-001 → M01-F01"""
                            src = sk.get("source_test_point", "")
                            parts = src.split("-")
                            m_idx = next((i for i, p in enumerate(parts) if p.startswith("M") and len(p) >= 3 and p[1:].isdigit()), None)
                            f_idx = next((i for i, p in enumerate(parts) if p.startswith("F") and len(p) >= 3 and p[1:].isdigit()), None)
                            if m_idx is not None and f_idx is not None:
                                return f"{parts[m_idx]}-{parts[f_idx]}"
                            return src.rsplit("-TC-", 1)[0] if "-TC-" in src else src  # 降级用case_id兜底

                        # 统计每feature的P0数(降级前)
                        feature_p0_count = {}
                        for sk in case_skeletons:
                            if sk["priority"] == "P0":
                                fk = _extract_feature_key(sk)
                                feature_p0_count[fk] = feature_p0_count.get(fk, 0) + 1
                        # 追踪降级后每feature剩余P0数
                        feature_p0_remaining = dict(feature_p0_count)

                        # 降级优先级:非冷烟P0先降→冷烟P0后降(尽量保留冷烟)
                        non_smoke_p0 = [sk for sk in p0_skeletons if not sk.get("is_smoke")]
                        smoke_p0 = [sk for sk in p0_skeletons if sk.get("is_smoke")]
                        downgraded = 0
                        auto_downgrade_log = []
                        for sk in non_smoke_p0:
                            if downgraded >= downgrade_count:
                                break
                            # Feature保护:如果该feature只剩1条P0,跳过不降级
                            fk = _extract_feature_key(sk)
                            if feature_p0_remaining.get(fk, 0) <= 1:
                                continue
                            old_pri = sk["priority"]
                            was_smoke = sk.get("is_smoke", False)
                            sk["priority"] = "P1"
                            sk["is_smoke"] = False
                            auto_downgrade_log.append(f"{sk['case_id']}:{old_pri}→P1")
                            downgraded += 1
                            feature_p0_remaining[fk] = feature_p0_remaining.get(fk, 1) - 1
                            if old_pri == "P0" and was_smoke:
                                batch_smoke_count = max(0, batch_smoke_count - 1)
                        # 如果非冷烟P0不够,降冷烟P0(同样带feature保护)
                        for sk in smoke_p0:
                            if downgraded >= downgrade_count:
                                break
                            fk = _extract_feature_key(sk)
                            if feature_p0_remaining.get(fk, 0) <= 1:
                                continue
                            old_pri = sk["priority"]
                            sk["priority"] = "P1"
                            sk["is_smoke"] = False
                            auto_downgrade_log.append(f"{sk['case_id']}:{old_pri}→P1(含冷烟)")
                            downgraded += 1
                            feature_p0_remaining[fk] = feature_p0_remaining.get(fk, 1) - 1
                            batch_smoke_count = max(0, batch_smoke_count - 1)

                        new_p0 = sum(1 for sk in case_skeletons if sk["priority"] == "P0")
                        new_ratio = new_p0 / total_skeleton if total_skeleton > 0 else 0
                        print(json.dumps({
                            "status": "info",
                            "action": "auto_downgrade_p0",
                            "batch_index": batch_index,
                            "original_p0_ratio": f"{p0_ratio:.0%}",
                            "downgraded": downgraded,
                            "new_p0_ratio": f"{new_ratio:.0%}",
                            "details": auto_downgrade_log,
                            "hint": f"P0比例{p0_ratio:.0%}>{p0_limit:.0%},骨架阶段自动降级{downgraded}条→新P0比例{new_ratio:.0%}"
                        }), file=sys.stderr)

                        # 降级后如果无冷烟但仍有P0,补一个冷烟标记
                        if batch_smoke_count == 0:
                            for sk in case_skeletons:
                                if sk["priority"] == "P0":
                                    sk["is_smoke"] = True
                                    batch_smoke_count = 1
                                    break

                # V4.8.14: 冒烟比例自动降级--防止smoke过多被Gate拒绝
                if total_skeleton > 0:
                    smoke_skeletons = [sk for sk in case_skeletons if sk.get("is_smoke")]
                    smoke_count = len(smoke_skeletons)
                    smoke_ratio = smoke_count / total_skeleton
                    if smoke_ratio > smoke_limit:
                        max_smoke = int(total_skeleton * smoke_limit)
                        # 降优先级低的冒烟(P0冒烟最后降)
                        smoke_p0 = [sk for sk in smoke_skeletons if sk["priority"] == "P0"]
                        smoke_p1 = [sk for sk in smoke_skeletons if sk["priority"] != "P0"]
                        downgrade_smoke = smoke_count - max_smoke
                        downgraded_smoke = 0
                        for sk in smoke_p1:
                            if downgraded_smoke >= downgrade_smoke:
                                break
                            sk["is_smoke"] = False
                            downgraded_smoke += 1
                        for sk in smoke_p0:
                            if downgraded_smoke >= downgrade_smoke:
                                break
                            sk["is_smoke"] = False
                            downgraded_smoke += 1
                        if downgraded_smoke > 0:
                            print(json.dumps({
                                "status": "info",
                                "action": "auto_downgrade_smoke",
                                "batch_index": batch_index,
                                "original_smoke_ratio": f"{smoke_ratio:.0%}",
                                "downgraded": downgraded_smoke,
                                "hint": f"冒烟比例{smoke_ratio:.0%}>{smoke_limit:.0%},自动降级{downgraded_smoke}条"
                            }), file=sys.stderr)

                # V4.6.17: 骨架只提供元数据,Agent基于P5原始描述自由创作
                skeleton_text = f"""

## ❗ 用例元数据(代码预分配,禁止修改priority/is_smoke/case_id)

每条用例必须输出以下字段,基于对应的P5测试点信息自行编写具体步骤。
- case_id/source_test_point/priority/is_smoke: 代码预设,你必须原样使用
- p5_description/p5_precondition/p5_related_rules: P5原始数据,你基于这些创作步骤

🔴 **你的任务:**
1. 读取每条用例的 p5_description/p5_precondition/p5_related_rules
2. 基于P5原文自由编写具体可执行的步骤(每条≥15字,包含「按钮名」「字段名」「路径」)
3. 基于P5原文编写可观测的期望结果(禁止:正常/成功/正确/符合预期)
4. 最终输出19列扁平JSON(参考Prompt中的正反例示范)
5. 每个测试点基于P5原文的差异自动产生不同步骤,严禁复制
```json
{json.dumps(case_skeletons, ensure_ascii=False)}
```
"""

                # 将骨架写入文件供 save_batch 读取
                skeleton_path = os.path.join(data_dir, "p6_batches", f"batch_{batch_index:03d}_skeleton.json")
                _write_json(skeleton_path, case_skeletons)

                # V3.3.2: 全局上下文摘要 + P1 scenario语义注入 + 输出预估
                # 全局摘要
                p1_path_for_p6 = os.path.join(data_dir, "p1_output.json")
                module_names_for_summary = []
                p1_for_p6 = {}
                if os.path.exists(p1_path_for_p6):
                    try:
                        p1_for_p6 = _read_json(p1_path_for_p6)
                        ft = p1_for_p6.get("feature_tree", {})
                        ft_modules = ft.get("modules", []) if isinstance(ft, dict) else []
                        if not ft_modules:
                            ft_modules = p1_for_p6.get("modules", [])
                        module_names_for_summary = [m.get("name", "") for m in ft_modules]
                    except Exception:
                        pass
                module_names_str = '、'.join(module_names_for_summary)
                global_summary = f"\n---\n## 全局上下文(仅供参考,不要为非本批次的内容生成用例)\n本需求共{len(module_names_for_summary)}个模块:{module_names_str}。\n总测试点{len(test_points)}条,分{total_batches}批处理。本批次为第{batch_index}批。"

                # P1 scenario语义注入:提取当前批次对应的scenario详情
                batch_scenario_ids = set(bp.get("source_scenario", "") for bp in batch_points)
                scenario_details = []
                if p1_for_p6:
                    ft = p1_for_p6.get("feature_tree", {})
                    ft_modules = ft.get("modules", []) if isinstance(ft, dict) else []
                    if not ft_modules:
                        ft_modules = p1_for_p6.get("modules", [])
                    for mod in ft_modules:
                        for feat in mod.get("children", []):
                            for scen in feat.get("children", []):
                                if scen.get("id") in batch_scenario_ids:
                                    scenario_details.append({
                                        "id": scen["id"],
                                        "name": scen.get("name", ""),
                                        "module": mod.get("name", ""),
                                        "feature": feat.get("name", ""),
                                        "precondition": scen.get("precondition", ""),
                                        "related_rules": scen.get("related_rules", []),
                                        "scenario_type": scen.get("scenario_type", ""),
                                        # V4.9.1: 兼容 operations_chain 和 operations_steps(旧字段名)
                                        "operations_chain": scen.get("operations_chain") or scen.get("operations_steps", []),
                                        "page_path": scen.get("page_path", ""),
                                        "test_point_hint": scen.get("test_point_hint", ""),
                                    })
                scenario_inject = ""
                if scenario_details:
                    scenario_text = json.dumps(scenario_details, ensure_ascii=False, indent=2)
                    # 大小限制:防止极端情况下注入过大
                    MAX_SCENARIO_INJECT = 3000
                    if len(scenario_text) > MAX_SCENARIO_INJECT:
                        scenario_details_slim = [{"id": s["id"], "name": s["name"], "module": s["module"], "page_path": s.get("page_path", ""), "operations_chain": s.get("operations_chain", []), "test_point_hint": s.get("test_point_hint", "")} for s in scenario_details]
                        scenario_text = json.dumps(scenario_details_slim, ensure_ascii=False, indent=2)
                    scenario_inject = f"\n---\n## 业务场景详情(用于理解测试点的业务语义)\n```json\n{scenario_text}\n```"

                # R1-R4修复:P0 field_specs/ui_elements/business_objects/test_point_candidates注入P6
                p0_enhance_inject = ""
                p0_path_for_p6 = os.path.join(data_dir, "p0_output.json")
                if os.path.exists(p0_path_for_p6):
                    try:
                        p0_for_p6 = _read_json(p0_path_for_p6)
                        p0_blocks = p0_for_p6.get("blocks", {})
                        p0_inject_data = {}
                        # R1: field_specs
                        field_specs = p0_blocks.get("field_specs", [])
                        if field_specs:
                            p0_inject_data["field_specs"] = field_specs
                        # R2: ui_elements
                        ui_elements = p0_blocks.get("ui_elements", [])
                        if ui_elements:
                            p0_inject_data["ui_elements"] = ui_elements
                        # R3: business_objects
                        business_objects = p0_blocks.get("business_objects", [])
                        if business_objects:
                            p0_inject_data["business_objects"] = business_objects
                        # R4: test_point_candidates
                        test_point_candidates = p0_blocks.get("test_point_candidates", [])
                        if test_point_candidates:
                            p0_inject_data["test_point_candidates"] = test_point_candidates
                        if p0_inject_data:
                            p0_enhance_text = json.dumps(p0_inject_data, ensure_ascii=False, indent=2)
                            # 截断保护:P0增强注入不超过2000字符
                            MAX_P0_ENHANCE_INJECT = 2000
                            if len(p0_enhance_text) > MAX_P0_ENHANCE_INJECT:
                                # 精简:每个字段只保留前3条
                                for key in p0_inject_data:
                                    if isinstance(p0_inject_data[key], list) and len(p0_inject_data[key]) > 3:
                                        p0_inject_data[key] = p0_inject_data[key][:3]
                                p0_enhance_text = json.dumps(p0_inject_data, ensure_ascii=False, indent=2)
                            p0_enhance_inject = f"\n---\n## P0原始分析数据(字段规格/UI元素/业务对象/测试候选点)\n```json\n{p0_enhance_text}\n```"
                    except Exception:
                        pass

                # V4.7.2: 输出引导 - 明确"期望至少"而非"硬性门槛"
                output_estimate = f"\n---\n## ❗ 输出要求\n本批次期望至少 **{batch_total_count}条** 用例(非硬性门槛,根据测试点复杂度可适当增加)。\n预计输出JSON约{batch_total_count * 800}-{batch_total_count * 1200}字符。\n请确保输出完整的JSON对象,包含testcases数组,不要截断。"

                # V4.7.1: 精简 prompt - 移除 P0/P1 场景注入(已写入 batch_N_context.json)
                # 只保留核心字段:slim_points + budget + skeleton + output_estimate
                p6_batch_info = f"\n---\n## 当前批次\n第{batch_index}/{total_batches}批(batch-index={batch_index},对应skeleton p6_batches/batch_{batch_index:03d}_skeleton.json),处理测试点{start+1}-{min(end, len(test_points))}:\n{json.dumps(slim_points, ensure_ascii=False)}{budget_text}{skeleton_text}{global_summary}{output_estimate}\n\n🔴 **请先读取文件** `{data_dir}/p6_batches/batch_{batch_index:03d}_context.json` **获取本批次测试点的完整上下文**(含操作骨架 step_expected_pairs、字段清单 field_checklist、UI 元素 ui_elements、风险标记等),基于完整上下文生成用例。\n\n⚠️ 起始batch-index=0(非1),skeleton文件名为 p6_batches/batch_000_skeleton.json,与prep_prompt --batch-index 参数完全一致。"
            except Exception:
                pass

    # 6. 组装完整prompt
    full_prompt_parts = [prompt_template]

    # V4.0.1: P6评审经验注入(项目关键词或同义词匹配时均触发)
    review_experience = ""
    if step == "P6" and (project_match.get("matched_projects") or project_match.get("matched_synonyms")):
        for kf in project_match.get("knowledge_files", []):
            domain = kf['domain']
            # 域名→文件名映射(与_sync_review_experience保持一致)
            domain_file = _domain_to_filename(domain)
            rules_path = os.path.join(skill_dir, "knowledge", "reviewed_cases", f"{domain_file}_rules.json")
            if os.path.exists(rules_path):
                try:
                    rules_data = _read_json(rules_path)
                    # 用蒸馏引擎生成注入文本
                    layers = []
                    for layer_name, label in [("tag_rules", "质量规则"), ("operation_rules", "操作规范"), ("domain_rules", "域特定规则"), ("positive_rules", "优秀模式")]:
                        rules = rules_data.get(layer_name, [])
                        if not rules:
                            continue
                        layer_lines = [f"【{label}】"]
                        for r in rules[:5]:  # 每层最多5条
                            freq = r.get("frequency", 1)
                            if freq >= 5:
                                prefix = "[强规则] "
                            elif freq >= 2:
                                prefix = "[规则] "
                            else:
                                prefix = "[参考] "
                            weight = r.get("weight", 1.0)
                            if weight < 1.0:
                                prefix += "[置信度:中] "
                            layer_lines.append(f"- {prefix}{r['rule']}")
                        layers.append("\n".join(layer_lines))
                    if layers:
                        # 统计经验规则总数
                        total_rules = sum(len(r) for r in [rules_data.get("tag_rules", []), rules_data.get("operation_rules", []), rules_data.get("domain_rules", []), rules_data.get("positive_rules", [])])
                        total_reviewed = rules_data.get("total_reviewed_cases", "?")
                        review_experience = (
                            f"\n---\n## 🔴 历史评审经验({kf['domain']},基于{total_reviewed}条用例评审,{total_rules}条规则)\n"
                            f"🔴 以下规则来自历史评审,生成用例时必须遵守,优先级高于通用规则。违反会被再次驳回。\n"
                            + "\n".join(layers) + "\n"
                        )
                        break  # 取第一个有经验的域即可,避免prompt膨胀
                except Exception:
                    pass

    if knowledge_texts:
        full_prompt_parts.append("\n---\n## 注入知识\n" + "\n\n".join(knowledge_texts))

    if review_experience:
        full_prompt_parts.append(review_experience)
    elif step == "P6":
        # 降级:无域经验时注入通用种子规则
        seed_path = os.path.join(skill_dir, "knowledge", "reviewed_cases", "通用_rules.json")
        if os.path.exists(seed_path):
            try:
                seed_data = _read_json(seed_path)
                seed_rules = []
                for layer_name, label in [("tag_rules", "质量规则"), ("operation_rules", "操作规范"), ("positive_rules", "优秀模式")]:
                    for r in seed_data.get(layer_name, [])[:3]:
                        seed_rules.append(f"- [种子规则] {r['rule']}")
                if seed_rules:
                    review_experience = (
                        f"\n---\n## 🔴 通用评审经验(种子规则,适用于所有项目)\n"
                        f"🔴 以下规则来自历史评审最佳实践,生成用例时必须遵守。\n"
                        + "\n".join(seed_rules) + "\n"
                    )
                    full_prompt_parts.append(review_experience)
            except Exception:
                pass

    if px_inject:
        full_prompt_parts.append(f"\n---\n## 图片理解增强\n{px_inject}")

    # V4.8.5: P1 LOW模型 - 精简P0数据,只注入核心5区块(避免MiniMax 53KB爆炸)
    if step == "P1" and upstream_data:
        # 检测模型档位
        p1_model_tier = "HIGH"
        state_path_p1 = os.path.join(data_dir, "orchestrator_state.json")
        if os.path.exists(state_path_p1):
            try:
                st_p1 = _read_json(state_path_p1)
                p1_model_tier = st_p1.get("model_tier", "HIGH")
            except Exception:
                pass
        if not p1_model_tier or p1_model_tier == "HIGH":
            # 兜底:从环境变量检测
            env_model = os.environ.get('OPENCLAW_MODEL', '') or os.environ.get('OPENCLAW_DEFAULT_MODEL', '')
            if env_model:
                p1_model_tier = _get_model_detect().classify(env_model)

        if p1_model_tier == "LOW" and "p0_output.json" in upstream_data:
            p0_raw = upstream_data["p0_output.json"]
            try:
                p0_obj = json.loads(p0_raw) if isinstance(p0_raw, str) else p0_raw
                # 只保留P1需要的5个核心区块
                blocks = p0_obj.get("blocks", {})
                slim_p0 = {
                    "objective": p0_obj.get("objective", "")[:500],
                    "blocks": {
                        "business_rules": blocks.get("business_rules", [])[:10],
                        "constraints": blocks.get("constraints", [])[:10],
                        "state_flow": blocks.get("state_flow", [])[:5],
                    },
                    "unknowns": p0_obj.get("unknowns", [])[:10],
                    "test_point_candidates": p0_obj.get("test_point_candidates", [])[:15],
                    "field_specs": p0_obj.get("field_specs", [])[:15],
                }
                trimmed = json.dumps(slim_p0, ensure_ascii=False, indent=2)
                upstream_data["p0_output.json"] = trimmed
                print(json.dumps({"status": "info", "p1_prompt_trimmed": f"P0 {len(p0_raw)}→{len(trimmed)}字符(LOW模型精简)"}), file=sys.stderr)
            except Exception:
                pass  # 解析失败时保持原样

    if upstream_data:
        full_prompt_parts.append("\n---\n## 输入数据")
        for fname, content in upstream_data.items():
            full_prompt_parts.append(f"\n### {fname}\n{content}")

    # R9修复:P3/P4显式注入P0 dependencies和known_risks
    if step in ("P3", "P4"):
        p0_path_for_r9 = os.path.join(data_dir, "p0_output.json")
        if os.path.exists(p0_path_for_r9):
            try:
                p0_data_r9 = _read_json(p0_path_for_r9)
                p0_blocks_r9 = p0_data_r9.get("blocks", {})
                r9_inject_parts = []
                deps = p0_blocks_r9.get("dependencies", [])
                if deps:
                    r9_inject_parts.append(f"### P0识别的外部依赖(风险/PCI识别必须参考)\n{json.dumps(deps, ensure_ascii=False, indent=2)}")
                risks = p0_blocks_r9.get("known_risks", [])
                if risks:
                    r9_inject_parts.append(f"### P0识别的已知风险(风险/PCI识别必须参考)\n{json.dumps(risks, ensure_ascii=False, indent=2)}")
                if r9_inject_parts:
                    full_prompt_parts.append("\n---\n## P0依赖与风险数据(必须明确引用)\n" + "\n".join(r9_inject_parts))
            except Exception:
                pass

    # P0需要需求文本
    if step == "P0" and requirement_text:
        full_prompt_parts.append(f"\n---\n## 需求文本\n{requirement_text[:15000]}")

    if p6_batch_info:
        full_prompt_parts.append(p6_batch_info)

    # P0内联必需字段提醒
    if step == "P0":
        full_prompt_parts.append("\n---\n## ❗ 输出必须包含以下顶层字段\n- quality_score: number (0~1.0)\n- blocks: object\n- objective: string")

        # V3.5.1: PRD审查增强 - 条件注入blocks_markdown/issues输出要求
        meta_path = os.path.join(data_dir, "task_meta.json")
        if os.path.exists(meta_path):
            _meta = _read_json(meta_path)
            if _meta.get("prd_quality_review", False):
                enhance_prompt_path = os.path.join(skill_dir, "prompts", "P0_prd_review_enhance.md")
                if os.path.exists(enhance_prompt_path):
                    enhance_text = _read_file_safe(enhance_prompt_path, max_chars=8000)
                    if enhance_text:
                        full_prompt_parts.append(f"\n---\n{enhance_text}")
                        full_prompt_parts.append("\n---\n## ❗ PRD审查模式额外必须输出\n- blocks_markdown: string (结构化Markdown,≤5000字符)\n- issues: array (问题清单,无问题时为空数组[])")


    # P1内联必需字段提醒
    if step == "P1":
        full_prompt_parts.append("\n---\n## ❗ 输出必须包含以下顶层字段\n- feature_tree: array (模块列表,每个元素为module_node对象)\n- coverage_check: object (覆盖率检查)")  # Bugfix V4.6.9: 与p1_output.schema.json一致(feature_tree是array而非object)

    # P2内联必需字段提醒(确保Agent生成的测试点带priority和status)
    if step == "P2":
        full_prompt_parts.append("""\n---\n## ❗ 每个test_point必须包含以下字段
- id: 字符串,测试点唯一标识
- source_scenario: 字符串,来源场景
- description: 字符串,测试点描述
- category: 字符串,测试类型
- priority: 必须是 "P0"/"P1"/"P2"/"P3" 之一
- status: 必须是 "active"/"blocked" 之一(默认active)
- priority_hint: 字符串,优先级建议

## ❗ 优先级分布要求(必须遵守,否则后续质量门禁会拒绝)
- P0优先级不得超过20%,推荐控制在10%-15%。P0仅用于核心主链路可用性+核心权限/交易入口级阻断场景
- P1应占主体(40%-60%),用于重要分支/异常场景
- P2/P3用于边界/兼容/性能等补充场景
- 删除/隐藏类、普通异常类、一般展示类原则上不标P0
- 不允许所有测试点为同一优先级""")

    # P7内联必需字段提醒
    if step == "P7":
        full_prompt_parts.append("""\n---\n## ❗ 输出必须包含以下顶层字段
- gate_result: object (必须包含status字段)
  - gate_result.status: 必须是 "PASS" 或 "FAIL"(全大写)
  - gate_result.summary: 字符串,检查结论
  - gate_result.checks: 数组,各项检查结果

⚠️ 注意:顶层字段名是 gate_result,不是 quality_check""")

    # P6质量规则+字段格式注入
    if step == "P6":
        full_prompt_parts.append("""\n---\n## ❗ 用例质量硬性规则(必须遵守,quality_check会校验)
1. **每个测试点至少展开为2条用例**(1条正向+1条反向/异常/边界),复杂测试点应展开更多
2. **冒烟用例比例**: 必须在5%~20%之间。冒烟用例=P0优先级+核心功能正向验证(排除删除/隐藏/异常用例)
3. **P0优先级占比**: 不得超过20%。大部分用例应为P1/P2
4. **优先级分布**: 不允许所有用例为同一优先级
5. **每需求冒烟**: 每个需求至少1条冒烟用例
6. **用例数下限**: 合并后至少15条用例,且不少于P5测试点数×1.5

违反以上任何规则的用例集将被quality_check拒绝,需要重新生成。

## ❗ 字段格式要求(必须严格遵守)
- **is_smoke**: 必须是布尔值 true 或 false(不是字符串,不是"是/否",不是"?")
- **priority**: 必须是 "P0"/"P1"/"P2"/"P3" 之一
- **title**: 必须非空
- **preconditions**: 必须非空
- **steps**: 必须是数组,每项包含 step 和 expected
- **testcases**: 顶层字段名必须是 testcases(小写)

## ❗ 严禁占位符内容(违反将被直接拒绝)
- 每条用例的steps必须是**具体的、可执行的操作步骤**,不允许使用"执行相关操作""观察结果"等泛化描述
- 每条用例的expected_results必须是**具体的、可验证的预期结果**,不允许使用"页面展示正常""数据与预期一致"等泛化描述
- **核心规则:steps行数 = expected_results行数,一一对应**
- 请基于skeleton中每条用例的p5_description/p5_precondition信息,**自由编写具体步骤和期望结果**
- 违反以上规则的批次将被p6_save_batch直接拒绝

## ❗ 步骤编写最佳实践
每个步骤必须包含:明确动作 + 操作对象 + 具体数据
每个期望结果必须包含:可观察的系统响应 + 具体验证点

✅ 正向验证示例(main_flow,3步=3期望):
steps: "1. 使用机构管理员账号admin01登录CRM系统\n2. 点击左侧菜单「兴光闪耀竞赛活动」,点击「月榜」Tab\n3. 点击「有效机构户」Tab查看数据列表"
expected_results: "1. 登录成功,页面显示用户名admin01\n2. 月榜Tab选中,显示当月数据\n3. 列表展示机构名称、有效户数、排名,数据与导入一致"

✅ 异常验证示例(exception,3步=3期望):
steps: "1. 使用机构管理员账号登录CRM系统\n2. 进入月榜页面,在搜索框输入超长字符串(256字符)\n3. 点击搜索按钮"
expected_results: "1. 登录成功\n2. 输入框接受输入或截断至最大长度\n3. 系统提示「搜索内容过长」或返回空结果,不报错"

✅ 权限验证示例(permission,3步=3期望):
steps: "1. 使用普通员工账号user01登录CRM系统\n2. 在地址栏直接输入月榜管理页面URL\n3. 观察页面响应"
expected_results: "1. 登录成功\n2. 页面返回403或跳转到无权限提示页\n3. 显示「您没有权限访问此页面」提示"

❌ 错误示例(会被拒绝):
steps: "1. 登录\n2. 进入页面\n3. 操作\n4. 验证\n5. 完成"
expected_results: "1. 页面展示正常\n2. 数据正确"
问题:5个步骤但只有2个期望结果,且内容泛化无具体验证点

## ❗ 你只需要生成以下核心字段(其余由代码自动补全)
必须生成:title, preconditions, steps, expected_results, remarks, test_case_type, test_category
代码自动补全:project, case_type, creator, assignee, status, screenshot, test_suite, menu_path, case_id, requirement, priority, is_smoke""")
    full_prompt = "\n".join(full_prompt_parts)

    # 输出
    result = {
        "status": "ok",
        "step": step,
        "prompt_length": len(full_prompt),
        "upstream_files": list(upstream_data.keys()),
        "knowledge_injected": len(knowledge_texts),
        "px_injected": bool(px_inject),
    }

    # 将prompt写入文件(太长不适合通过stdout传递)
    prompt_output_path = os.path.join(data_dir, f"{step.lower()}_prompt.txt")
    with open(prompt_output_path, "w", encoding="utf-8") as f:
        f.write(full_prompt)
    result["prompt_file"] = prompt_output_path

    print(json.dumps(result))


# ============================================================
# Action: set_prd_review (V3.5.1: 设置PRD审查开关)
# ============================================================

def action_set_prd_review(args):
    """设置PRD质量审查开关(用户在Onboarding第1步选择"开启"时调用)"""
    data_dir = args.data_dir
    task_id = args.task_id
    enabled = (getattr(args, 'enabled', 'true') or 'true').lower().strip()
    enabled_bool = enabled in ('true', '1', '开启', 'on', 'yes')

    # 写入task_meta.json
    meta_path = os.path.join(data_dir, "task_meta.json")
    if os.path.exists(meta_path):
        meta = _read_json(meta_path)
    else:
        meta = {"task_id": task_id}
    meta["prd_quality_review"] = enabled_bool
    _write_json(meta_path, meta)

    print(json.dumps({
        "status": "ok",
        "prd_quality_review": enabled_bool,
        "message": "PRD质量审查已开启" if enabled_bool else "PRD质量审查已关闭",
    }))


# ============================================================
# Action: p6_batch_info (P6分批信息)
# ============================================================

# ============================================================
# Action: p2_code_generate (V3.3.2: P2测试点代码自动生成)
# ============================================================

def action_p2_code_generate(args):
    """代码层从P1 feature_tree自动生成P2测试点(零Agent依赖)

    职责边界:只管结构(数量、category、priority、source_scenario)
    语义细化由P6承担(P6 prompt注入P1 scenario详情)
    """
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # 前置gate检查:P1必须完成
    ok, msg = check_gate(data_dir, "P1", task_id)
    if not ok:
        print(json.dumps({"status": "gate_blocked", "step": "P1", "reason": msg}))
        sys.exit(1)

    # 读取P1 feature_tree
    p1_path = os.path.join(data_dir, "p1_output.json")
    if not os.path.exists(p1_path):
        print(json.dumps({"status": "error", "reason": "p1_output.json不存在"}))
        sys.exit(1)
    p1_data = _read_json(p1_path)

    # P1数据结构:feature_tree.modules 包含嵌套children结构
    feature_tree = p1_data.get("feature_tree", {})
    if isinstance(feature_tree, list):
        modules = feature_tree  # Bugfix V4.6.9: feature_tree是list时直接作为modules列表
    elif isinstance(feature_tree, dict):
        modules = feature_tree.get("modules", [])
    else:
        modules = []
    # 兼容:如果feature_tree为空,尝试顶层modules
    if not modules:
        modules = p1_data.get("modules", [])

    if not modules:
        print(json.dumps({"status": "error", "reason": "P1数据中未找到modules"}))
        sys.exit(1)

    # 读取P0 operations(补充语义判断)
    p0_path = os.path.join(data_dir, "p0_output.json")
    p0_operations = []
    # R1-R4修复:读取P0 field_specs/ui_elements/business_objects/test_point_candidates
    p0_field_specs = []
    p0_ui_elements = []
    p0_business_objects = []
    p0_test_point_candidates = []
    if os.path.exists(p0_path):
        try:
            p0_data = _read_json(p0_path)
            p0_operations = p0_data.get("blocks", {}).get("operations", [])
            p0_field_specs = p0_data.get("blocks", {}).get("field_specs", [])
            p0_ui_elements = p0_data.get("blocks", {}).get("ui_elements", [])
            p0_business_objects = p0_data.get("blocks", {}).get("business_objects", [])
            p0_test_point_candidates = p0_data.get("blocks", {}).get("test_point_candidates", [])
        except Exception:
            pass

    # 关键词集合
    DATA_KEYWORDS = {"导入", "导出", "上传", "下载", "查询", "统计", "推送", "同步"}

    # 获取requirement_id
    requirement_id = p1_data.get("requirement_id", "REQ-UNKNOWN")

    # 遍历所有scenario生成测试点
    test_points = []
    seq = 1

    for module in modules:
        for feature in module.get("children", []):
            if feature.get("type") != "feature":
                continue
            feature_scenarios = [s for s in feature.get("children", []) if s.get("type") == "scenario"]
            feature_exception_added = False  # 每个feature只生成1条异常测试点

            for scenario in feature_scenarios:
                scenario_id = scenario.get("id", "")
                scenario_name = scenario.get("name", "")
                scenario_type = scenario.get("scenario_type", "positive")
                precondition = scenario.get("precondition", "")
                related_rules = scenario.get("related_rules", [])
                related_roles = scenario.get("related_roles", [])

                # 规则1:正向验证(所有scenario必有)
                test_points.append({
                    "id": f"{requirement_id}-TP-{seq:03d}",
                    "source_scenario": scenario_id,
                    "category": "main_flow",
                    "description": f"验证{scenario_name}正常流程",
                    "precondition": precondition,
                    "related_rules": related_rules,
                    "related_roles": related_roles,
                    "priority": "P1",
                    "priority_hint": "P1",
                    "status": "active",
                })
                seq += 1

                # 规则2:异常验证(每个feature只生成1条,避免膨胀)
                if not feature_exception_added:
                    test_points.append({
                        "id": f"{requirement_id}-TP-{seq:03d}",
                        "source_scenario": scenario_id,
                        "category": "exception",
                        "description": f"验证{feature.get('name', scenario_name)}异常场景处理",
                        "precondition": precondition,
                        "related_rules": related_rules,
                        "related_roles": related_roles,
                        "priority": "P2",
                        "priority_hint": "P2",
                        "status": "active",
                    })
                    seq += 1
                    feature_exception_added = True

                # 规则3:边界验证(数据相关场景,且该scenario名称含数据关键词)
                if any(kw in scenario_name for kw in DATA_KEYWORDS):
                    test_points.append({
                        "id": f"{requirement_id}-TP-{seq:03d}",
                        "source_scenario": scenario_id,
                        "category": "boundary",
                        "description": f"验证{scenario_name}边界条件和数据完整性",
                        "precondition": precondition,
                        "related_rules": related_rules,
                        "related_roles": related_roles,
                        "priority": "P3",
                        "priority_hint": "P3",
                        "status": "active",
                    })
                    seq += 1

                # 规则4:权限验证(多角色场景,且scenario_type含permission信号)
                if related_roles and len(related_roles) > 1 and scenario_type in ("permission", "role", "auth"):
                    test_points.append({
                        "id": f"{requirement_id}-TP-{seq:03d}",
                        "source_scenario": scenario_id,
                        "category": "permission",
                        "description": f"验证{scenario_name}不同角色权限控制",
                        "precondition": precondition,
                        "related_rules": related_rules,
                        "related_roles": related_roles,
                        "priority": "P1",
                        "priority_hint": "P1",
                        "status": "active",
                    })
                    seq += 1

    # P0提升逻辑:每feature第1个main_flow升为P0(原来每module只升1个,导致P0太少冒烟不足)
    seen_features_for_p0 = set()
    for tp in test_points:
        if tp["category"] == "main_flow":
            # 从source_scenario提取feature key(如REQ-2026-XG-014-M01-F01-S01中的M01-F01)
            src = tp.get("source_scenario", "")
            feature_key = None
            parts = src.split("-")
            m_idx = next((i for i, p in enumerate(parts) if p.startswith("M") and p[1:].isdigit()), None)
            f_idx = next((i for i, p in enumerate(parts) if p.startswith("F") and p[1:].isdigit()), None)
            if m_idx is not None and f_idx is not None:
                feature_key = f"{parts[m_idx]}-{parts[f_idx]}"
            elif m_idx is not None:
                feature_key = parts[m_idx]  # 备用:无F编号时降级为module级
            if feature_key and feature_key not in seen_features_for_p0:
                tp["priority"] = "P0"
                tp["priority_hint"] = "P0"
                seen_features_for_p0.add(feature_key)

    # complexity和expected_case_count标签(与P5 merge逻辑一致)
    SIMPLE_CATEGORIES = {"compatibility", "display", "ui_check"}
    COMPLEX_CATEGORIES = {"permission", "exception", "integration", "data_consistency"}
    for tp in test_points:
        cat = tp.get("category", "").lower()
        has_risk = tp.get("risk_flag", False)
        priority = tp.get("priority", "P1")
        score = 0
        if cat in COMPLEX_CATEGORIES:
            score += 2
        if has_risk:
            score += 1
        if priority in ("P0", "P1"):
            score += 1
        if score >= 3:
            tp["complexity"] = "L3"
            tp["expected_case_count"] = 3
        elif score >= 1:
            tp["complexity"] = "L2"
            tp["expected_case_count"] = 2
        else:
            tp["complexity"] = "L1"
            tp["expected_case_count"] = 1
        # P0测试点强制上限expected_case_count=2:
        # P0第1条是冒烟用例,展开过多会稀释冒烟比例导致不达标8%门槛
        if tp.get("priority") == "P0" and tp.get("expected_case_count", 2) > 2:
            tp["expected_case_count"] = 2
        # 初始化risk/pci标记(P5 merge会覆盖)
        tp.setdefault("risk_flag", False)
        tp.setdefault("pci_flag", False)

    # 覆盖率校验
    modules_covered = set()
    features_covered = set()
    for tp in test_points:
        src = tp.get("source_scenario", "")
        for part in src.split("-"):
            if part.startswith("M") and part[1:].isdigit():
                modules_covered.add(part)
            if part.startswith("F") and part[1:].isdigit():
                # 提取到feature级别
                idx = src.index(part)
                features_covered.add(src[:idx + len(part)])

    total_modules = len(modules)
    coverage_ok = len(modules_covered) >= total_modules

    # 构建输出
    # R1-R4修复:将P0关键数据附加到P2输出供下游使用
    p0_context = {}
    if p0_field_specs:
        p0_context["field_specs"] = p0_field_specs
    if p0_ui_elements:
        p0_context["ui_elements"] = p0_ui_elements
    if p0_business_objects:
        p0_context["business_objects"] = p0_business_objects
    if p0_test_point_candidates:
        p0_context["test_point_candidates"] = p0_test_point_candidates

    output = {
        "schema_version": "1.0.0",
        "prompt_version": "1.0.0",
        "requirement_id": requirement_id,
        "test_points": test_points,
        "p0_context": p0_context,
        "coverage_summary": {
            "total_test_points": len(test_points),
            "modules_covered": len(modules_covered),
            "total_modules": total_modules,
            "features_covered": len(features_covered),
            "coverage_ok": coverage_ok,
            "generation_method": "code",
        }
    }

    # 写入tmp文件
    tmp_path = os.path.join(data_dir, "p2_output.tmp.json")
    _write_json(tmp_path, output)

    # 调用truncation_guard
    guard_ok, guard_msg = run_truncation_guard(skill_dir, data_dir, task_id, "P2", revision=1)
    if not guard_ok:
        print(json.dumps({"status": "guard_failed", "reason": guard_msg}))
        sys.exit(1)

    # 统计
    from collections import Counter
    pri_dist = dict(Counter(tp["priority"] for tp in test_points))
    cat_dist = dict(Counter(tp["category"] for tp in test_points))

    # V4.8.11: P2完成后自动生成需求结构报告,Agent无需手动调用export_p0p1
    p0p1_path = os.path.join(data_dir, "p0p1_report.md")
    try:
        import subprocess as _sp
        ep = os.path.join(skill_dir, "tools", "export_p0p1.py")
        _sp.run([sys.executable, ep, "--data-dir", data_dir, "--output", p0p1_path],
                capture_output=True, timeout=15)
        if os.path.exists(p0p1_path):
            report_generated = True
    except Exception:
        report_generated = os.path.exists(p0p1_path)

    output_msg = {
        "status": "ok",
        "step": "P2",
        "test_points_count": len(test_points),
        "priority_distribution": pri_dist,
        "category_distribution": cat_dist,
        "coverage": output["coverage_summary"],
        "guard_result": f"GUARD_PASS:P2:{len(test_points)}",
    }
    if report_generated:
        output_msg["__must_emit__"] = f"📄 需求理解与功能点拆解报告已生成\nMEDIA:{data_dir}/p0p1_report.md\n⏸️ 段落3完成。请回复「继续」进入段落4(P3+P4风险识别)。禁止自动跨段。"

    print(json.dumps(output_msg))


# ============================================================
# Action: p3_p4_parallel (V4.1.0: P3+P4并行执行+失败处理)
# ============================================================

def action_p3_p4_parallel(args):
    """V4.1.0: P3+P4并行执行,带完整失败处理逻辑。

    使用ThreadPoolExecutor同时执行P3和P4的prep_prompt+step_run流程。
    失败处理:
    1. 任一步骤失败 → 立即标记另一个为"跳过" → 不进入P5合并
    2. 失败日志聚合:记录哪个步骤失败、失败原因、耗时
    3. 资源释放:无论成功失败,清理临时文件(.tmp.json)

    前置条件:P1 gate pass必须存在(P3和P4都依赖P1)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import traceback

    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # 前置gate检查:P3和P4都依赖P1
    ok, msg = check_gate(data_dir, "P1", task_id)
    if not ok:
        print(json.dumps({"status": "gate_blocked", "step": "P1", "reason": msg}))
        sys.exit(1)

    # 临时文件列表(用于finally清理)
    temp_files = []

    def _run_step(step):
        """执行单个步骤的完整流程:prep_prompt → Agent输出文件读取 → step_run。

        此函数在线程中执行,返回结构化结果。
        注意:此处不直接调用action_step_run(因为它会sys.exit),
        而是通过subprocess调用orchestrator自身。

        Returns:
            dict: {"step": str, "status": "ok"|"failed", "reason": str, "duration": float}
        """
        start_time = time.time()
        orch_path = os.path.abspath(__file__)

        try:
            # Step 1: 执行prep_prompt
            prep_cmd = [
                "python3", orch_path,
                "--action", "prep_prompt",
                "--step", step,
                "--data-dir", data_dir,
                "--task-id", task_id,
                "--skill-dir", skill_dir,
            ]
            prep_result = subprocess.run(
                prep_cmd, capture_output=True, text=True, timeout=60
            )
            if prep_result.returncode != 0:
                error_msg = prep_result.stderr.strip() or prep_result.stdout.strip()
                return {
                    "step": step,
                    "status": "failed",
                    "phase": "prep_prompt",
                    "reason": f"prep_prompt失败: {error_msg[:500]}",
                    "duration": time.time() - start_time,
                }

            # Step 2: 检查Agent输出文件是否存在
            # Agent需要在prep_prompt之后生成 {step.lower()}_agent_output.json
            agent_output_path = os.path.join(data_dir, f"{step.lower()}_agent_output.json")
            if not os.path.exists(agent_output_path):
                return {
                    "step": step,
                    "status": "failed",
                    "phase": "agent_output",
                    "reason": f"Agent输出文件不存在: {step.lower()}_agent_output.json。Agent需先根据prep_prompt生成输出。",
                    "duration": time.time() - start_time,
                }

            # Step 3: 执行step_run(校验+写入gate pass)
            run_cmd = [
                "python3", orch_path,
                "--action", "step_run",
                "--step", step,
                "--data-dir", data_dir,
                "--task-id", task_id,
                "--skill-dir", skill_dir,
            ]
            run_result = subprocess.run(
                run_cmd, capture_output=True, text=True, timeout=60
            )
            if run_result.returncode != 0:
                error_msg = run_result.stderr.strip() or run_result.stdout.strip()
                # 记录临时文件路径(供finally清理)
                tmp_path = os.path.join(data_dir, f"{step.lower()}_output.tmp.json")
                temp_files.append(tmp_path)
                return {
                    "step": step,
                    "status": "failed",
                    "phase": "step_run",
                    "reason": f"step_run失败: {error_msg[:500]}",
                    "duration": time.time() - start_time,
                }

            return {
                "step": step,
                "status": "ok",
                "phase": "complete",
                "reason": "",
                "duration": time.time() - start_time,
            }

        except subprocess.TimeoutExpired:
            return {
                "step": step,
                "status": "failed",
                "phase": "timeout",
                "reason": f"{step}执行超时(60秒限制)",
                "duration": time.time() - start_time,
            }
        except Exception as e:
            return {
                "step": step,
                "status": "failed",
                "phase": "exception",
                "reason": f"{step}执行异常: {str(e)[:300]}",
                "duration": time.time() - start_time,
            }

    # ============================================================
    # 并行执行P3和P4
    # ============================================================
    results = {}
    failed_step = None
    skipped_step = None

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_step = {
                executor.submit(_run_step, "P3"): "P3",
                executor.submit(_run_step, "P4"): "P4",
            }

            for future in as_completed(future_to_step, timeout=180):
                step_name = future_to_step[future]
                try:
                    result = future.result(timeout=120)
                    results[step_name] = result

                    # 任一步骤失败 → 标记另一个为"跳过"
                    if result["status"] == "failed":
                        failed_step = step_name
                        other_step = "P4" if step_name == "P3" else "P3"
                        # 尝试取消另一个(如果还没完成)
                        for f, s in future_to_step.items():
                            if s == other_step and not f.done():
                                f.cancel()
                                skipped_step = other_step
                        break

                except Exception as e:
                    results[step_name] = {
                        "step": step_name,
                        "status": "failed",
                        "phase": "future_exception",
                        "reason": f"线程执行异常: {str(e)[:300]}",
                        "duration": 0,
                    }
                    failed_step = step_name
                    other_step = "P4" if step_name == "P3" else "P3"
                    for f, s in future_to_step.items():
                        if s == other_step and not f.done():
                            f.cancel()
                            skipped_step = other_step
                    break

    except TimeoutError:
        # 总超时180秒
        for step_name in ["P3", "P4"]:
            if step_name not in results:
                results[step_name] = {
                    "step": step_name,
                    "status": "failed",
                    "phase": "total_timeout",
                    "reason": "并行执行总超时(180秒)",
                    "duration": 180,
                }
        failed_step = "P3+P4"

    finally:
        # ============================================================
        # 资源释放:清理临时文件
        # ============================================================
        for step_name in ["P3", "P4"]:
            tmp_path = os.path.join(data_dir, f"{step_name.lower()}_output.tmp.json")
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
        # 清理额外记录的临时文件
        for tmp_path in temp_files:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    # ============================================================
    # 结果聚合与输出
    # ============================================================

    # 如果有跳过的步骤,补充记录
    if skipped_step and skipped_step not in results:
        results[skipped_step] = {
            "step": skipped_step,
            "status": "skipped",
            "phase": "skipped",
            "reason": f"因{failed_step}失败而跳过",
            "duration": 0,
        }

    # 判断整体结果
    p3_ok = results.get("P3", {}).get("status") == "ok"
    p4_ok = results.get("P4", {}).get("status") == "ok"
    all_ok = p3_ok and p4_ok

    # 构造失败日志
    failure_log = []
    for step_name in ["P3", "P4"]:
        r = results.get(step_name, {})
        if r.get("status") in ("failed", "skipped"):
            failure_log.append({
                "step": step_name,
                "status": r.get("status"),
                "phase": r.get("phase", ""),
                "reason": r.get("reason", ""),
                "duration_sec": round(r.get("duration", 0), 2),
            })

    output = {
        "status": "ok" if all_ok else "failed",
        "p3_result": results.get("P3", {}).get("status", "unknown"),
        "p4_result": results.get("P4", {}).get("status", "unknown"),
        "p3_duration_sec": round(results.get("P3", {}).get("duration", 0), 2),
        "p4_duration_sec": round(results.get("P4", {}).get("duration", 0), 2),
        "can_proceed_to_p5": all_ok,
    }

    if not all_ok:
        output["failure_log"] = failure_log
        output["message"] = (
            f"❌ 并行执行失败。"
            f"{'P3' if not p3_ok else 'P4'}{'失败' if results.get('P3' if not p3_ok else 'P4', {}).get('status') == 'failed' else '被跳过'},"
            f"不进入P5合并步骤。请检查失败原因后重试。"
        )
        output["hint"] = "使用 --action restart_from --step P3 重置后重试"
    else:
        output["message"] = (
            f"✅ P3+P4并行执行成功。"
            f"P3耗时{output['p3_duration_sec']}秒,P4耗时{output['p4_duration_sec']}秒。"
            f"可执行P5合并。"
        )
        output["next_action"] = "p5_code_merge"

    print(json.dumps(output, ensure_ascii=False))

    if not all_ok:
        sys.exit(1)


# ============================================================
# Action: p5_code_merge (V3.2.0: P5合并下沉代码层)
# ============================================================

# ============================================================
# V4.7.0: P5 骨架增强 - 为每个测试点生成 step_expected_pairs、
# ui_elements、field_checklist,供给 P6 Agent 具体参考
# ============================================================

def _build_step_expected_pairs(point: dict) -> list:
    """
    从 operations_chain 提取步骤-期望骨架。
    兜底策略(p1_operations_chain为空时): 从 description 提取。
    """
    ops_chain = point.get("operations_chain", [])
    if not isinstance(ops_chain, list):
        ops_chain = []

    pairs = []
    if ops_chain:
        for op in ops_chain:
            if isinstance(op, dict):
                action = op.get("action", op.get("operation", ""))
                target = op.get("target", op.get("target_element", ""))
                value = op.get("value", op.get("data_value", ""))
                expected = op.get("expected", op.get("expected_result", ""))
                if action and target:
                    step = f"{action}「{target}」"
                    if value:
                        step += f",输入{value}"
                    pairs.append({"step": step, "expected": expected or f"{target}操作完成"})
        if pairs:
            return pairs

    # 兜底策略: 从 description 提取骨架关键词
    desc = point.get("description", "") or ""
    category = point.get("category", "") or ""
    import re as _re

    # 尝试从描述中提取操作关键词
    nav = _re.search(r'(?:进入|打开|跳转|导航)(.{2,20}?)(?:[,,。]|页面|模块|功能)', desc)
    if nav:
        pairs.append({"step": f"进入{nav.group(1).strip()}页面", "expected": "页面正常加载"})

    action_pat = _re.search(r'(点击|选择|输入|填写|录入|查询|搜索|勾选|上传|下载|导出)(.{2,20}?)(?:[,,。]|按钮|后|并|查看)', desc)
    if action_pat:
        pairs.append({"step": f"{action_pat.group(1)}「{action_pat.group(2).strip()}」", "expected": "操作执行完成"})

    # 分类兜底模板(仅当上述提取结果为0时使用)
    # V4.10.2: 差异化注入--从 title/id 提取TP特有信息,避免同category骨架完全相同
    if not pairs:
        tp_title = point.get("title", "") or ""
        tp_id = point.get("id", "") or ""
        tp_desc = point.get("description", "") or ""

        # 提取差异化关键词(title > description关键词 > id后缀)
        diff_hint = ""
        if tp_title:
            diff_hint = tp_title.strip()[:30]
        if not diff_hint and tp_desc:
            # 从description提取前几个有意义的中文词
            keywords = _re.findall(r'[\u4e00-\u9fa5]{2,6}', tp_desc)
            if keywords:
                diff_hint = keywords[0] if len(keywords) == 1 else keywords[0] + keywords[-1]
        if not diff_hint and tp_id:
            parts = tp_id.split("-")
            diff_hint = parts[-1] if len(parts) >= 2 else tp_id[-10:]

        fallback_map = {
            "main_flow": [{"step": "进入{diff}功能页面,执行核心操作流程", "expected": "{diff}核心功能按预期完成"}],
            "branch": [{"step": "进入{diff}功能页面,选择分支路径", "expected": "{diff}分支功能按预期完成"}],
            "exception": [{"step": "针对{diff}构造异常输入条件", "expected": "系统针对{diff}给出明确错误提示"}],
            "boundary": [{"step": "针对{diff}输入边界值测试数据", "expected": "系统按{diff}边界规则处理"}],
            "risk_verification": [{"step": "触发{diff}风险验证场景", "expected": "验证{diff}风险处理逻辑是否符合预期"}],
            "permission": [{"step": "以受限角色登录并访问{diff}", "expected": "系统按权限规则限制{diff}访问"}],
        }
        base = fallback_map.get(category,
            [{"step": "针对{diff}执行相关测试操作", "expected": "{diff}验证结果符合预期"}])
        # 注入差异化关键词(浅拷贝避免修改模板原值)
        pairs = []
        for p in base:
            injected = {}
            for k, v in p.items():
                injected[k] = v.replace("{diff}", diff_hint) if diff_hint else v
            pairs.append(injected)

    return pairs


def _build_ui_elements(point: dict) -> dict:
    """从 field_specs + operations_chain + page_path 汇总 UI 元素清单
    V4.9.0: 增加page_path提取兜底--当field_specs和operations_chain都为空时,
    从page_path和scenario name中提取UI关键词。"""
    elements = {"buttons": [], "inputs": [], "selectors": [], "labels": []}

    field_specs = point.get("field_specs", [])
    if isinstance(field_specs, list):
        for fs in field_specs:
            if isinstance(fs, dict):
                name = fs.get("name", fs.get("field_name", ""))
                ftype = (fs.get("type", fs.get("field_type", "text")) or "").lower()
                if name:
                    if ftype in ("select", "dropdown", "下拉", "选择"):
                        elements["selectors"].append(name)
                    else:
                        elements["inputs"].append(name)
            elif isinstance(fs, str) and fs.strip():
                elements["inputs"].append(fs.strip())

    ops_chain = point.get("operations_chain", [])
    if isinstance(ops_chain, list):
        for op in ops_chain:
            if isinstance(op, dict):
                target = op.get("target", op.get("target_element", ""))
                action = (op.get("action", op.get("operation", "")) or "").lower()
                if target:
                    if action in ("点击", "click", "提交", "submit"):
                        elements["buttons"].append(target)
                    elif action in ("选择", "select", "下拉"):
                        elements["selectors"].append(target)
                    elif action in ("输入", "填写", "录入", "input"):
                        elements["inputs"].append(target)
                    else:
                        elements["labels"].append(target)

    # V4.9.0: 兜底--从page_path和scenario name提取UI关键词
    # P1场景通常不输出field_specs和operations_chain,但page_path包含了页面导航路径
    if not ops_chain and not field_specs:
        # 从page_path提取(如"分润管理→员工配置"→提取"分润管理"/"员工配置")
        pp = point.get("page_path", "")
        if pp:
            path_parts = [p.strip() for p in pp.replace("→", ">").replace("/", ">").split(">") if p.strip()]
            for part in path_parts:
                if len(part) >= 2:
                    elements["labels"].append(part)

        # 从scenario name提取关键词
        sn = point.get("_scenario_name", point.get("name", ""))
        if sn:
            elements["labels"].append(sn[:20])  # 截断,避免过长

        # 从precondition提取操作关键词
        precond = point.get("_precondition", point.get("precondition", ""))
        if precond:
            # 提取包含动词的短语
            for kw in ["登录", "进入", "打开", "选择", "配置"]:
                idx = precond.find(kw)
                if idx >= 0:
                    chunk = precond[idx:idx+15].split(",")[0].split(",")[0]
                    elements["labels"].append(chunk.strip())
                    break

    for key in elements:
        elements[key] = list(dict.fromkeys(elements[key]))
    return elements


# ============================================================
# V4.10.0: LOW模型窄聚焦模式 - 骨架生成辅助函数
# ============================================================

def _build_skeleton_for_batch(data_dir, batch_points, batch_index):
    """为LOW简单模式生成最小骨架(仅case_id映射,供p6_save_batch补全字段)

    Agent只产出title/steps/expected_results,其余字段由skeleton锁定后代码补全。
    """
    case_skeletons = []
    SMOKE_CATEGORIES = {"main_flow", "branch", "integration"}

    for bp in batch_points:
        bp_id = bp.get("id", "")
        bp_priority = bp.get("priority", "P1")
        bp_category = (bp.get("category", "") or "").lower()
        bp_expected = bp.get("expected_case_count", 2)
        bp_desc = bp.get("description", "")
        bp_precond = bp.get("precondition", "")

        for case_idx in range(1, bp_expected + 1):
            if case_idx == 1:
                case_priority = bp_priority
                is_smoke = (bp_priority == "P0" and bp_category in SMOKE_CATEGORIES)
            else:
                case_priority = "P2" if bp_priority in ("P0", "P1") else "P3"
                is_smoke = False

            case_skeletons.append({
                "case_id": f"{bp_id}-TC-{case_idx:03d}",
                "source_test_point": bp_id,
                "priority": case_priority,
                "is_smoke": is_smoke,
                "p5_description": bp_desc,
                "p5_precondition": bp_precond,
                "preconditions": bp_precond,  # V4.10.0: 骨架补全
                "test_case_type": "正例" if bp_category in ("main_flow", "branch", "integration", "正向验证") else "反例",
                "test_category": "功能测试",
            })

    # 冷烟兜底
    if not any(sk.get("is_smoke") for sk in case_skeletons):
        for sk in case_skeletons:
            if sk["priority"] == "P0":
                sk["is_smoke"] = True
                break

    # V4.10.0: P0比例自动降级(复用旧内联骨架逻辑)
    p0_limit = 0.35  # LOW模型阈值
    total = len(case_skeletons)
    if total > 0:
        p0_count = sum(1 for sk in case_skeletons if sk["priority"] == "P0")
        p0_ratio = p0_count / total
        if p0_ratio > p0_limit:
            max_p0 = int(total * p0_limit)
            downgrade_count = p0_count - max_p0
            # 非冷烟P0先降 → 冷烟P0后降
            non_smoke = [sk for sk in case_skeletons if sk["priority"] == "P0" and not sk.get("is_smoke")]
            smoke = [sk for sk in case_skeletons if sk["priority"] == "P0" and sk.get("is_smoke")]
            downgraded = 0
            for sk in non_smoke:
                if downgraded >= downgrade_count:
                    break
                sk["priority"] = "P1"
                sk["is_smoke"] = False
                downgraded += 1
            for sk in smoke:
                if downgraded >= downgrade_count:
                    break
                sk["priority"] = "P1"
                sk["is_smoke"] = False
                downgraded += 1

    batches_dir = os.path.join(data_dir, "p6_batches")
    _ensure_dir(batches_dir)
    skeleton_path = os.path.join(batches_dir, f"batch_{batch_index:03d}_skeleton.json")
    _write_json(skeleton_path, case_skeletons)


def _build_field_checklist(point: dict, p0_field_specs: list = None) -> list:
    """收集该测试点涉及的所有字段名(含P0全局字段)"""
    fields = []

    field_specs = point.get("field_specs", [])
    if isinstance(field_specs, list):
        for fs in field_specs:
            if isinstance(fs, dict):
                name = fs.get("name", fs.get("field_name", ""))
                if name:
                    fields.append(name)
            elif isinstance(fs, str) and fs.strip():
                fields.append(fs.strip())

    if isinstance(p0_field_specs, list):
        for fs in p0_field_specs:
            if isinstance(fs, dict):
                name = fs.get("name", fs.get("field_name", ""))
                if name and name not in fields:
                    fields.append(name)
            elif isinstance(fs, str) and fs.strip() and fs.strip() not in fields:
                fields.append(fs.strip())

    return fields


def action_p5_code_merge(args):
    """代码层合并P2+P3+P4→P5(不再依赖Agent/prompt合并)

    读取P2测试点 + P3风险点 + P4 PCI项,代码合并后写入P5
    V4.7.0: 新增骨架增强(step_expected_pairs/ui_elements/field_checklist)
    """
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # 前置gate检查
    for prereq in ["P2", "P3", "P4"]:
        ok, msg = check_gate(data_dir, prereq, task_id)
        if not ok:
            print(json.dumps({"status": "gate_blocked", "step": prereq, "reason": msg}))
            sys.exit(1)

    # 读取P2测试点
    p2_path = os.path.join(data_dir, "p2_output.json")
    p2_data = _read_json(p2_path) if os.path.exists(p2_path) else {}
    p2_points = p2_data.get("test_points", [])

    # 读取P3风险点(兼容risk_points和risks)
    p3_path = os.path.join(data_dir, "p3_output.json")
    p3_data = _read_json(p3_path) if os.path.exists(p3_path) else {}
    p3_risks = p3_data.get("risk_points", p3_data.get("risks", []))

    # 读取P4 PCI项(兼容pci_list和pci_items)
    p4_path = os.path.join(data_dir, "p4_output.json")
    p4_data = _read_json(p4_path) if os.path.exists(p4_path) else {}
    p4_pcis = p4_data.get("pci_list", p4_data.get("pci_items", []))

    # V4.7.0: 读取P0/P1用于骨架增强的字段清单
    p0_path = os.path.join(data_dir, "p0_output.json")
    p0_data = _read_json(p0_path) if os.path.exists(p0_path) else {}
    p0_field_specs = []
    # P0 field_specs 位于 blocks 内(与 p2_code_generate 保持一致)
    p0_blocks = p0_data.get("blocks", {})
    if isinstance(p0_blocks, dict) and isinstance(p0_blocks.get("field_specs"), list):
        p0_field_specs = p0_blocks["field_specs"]

    p1_path = os.path.join(data_dir, "p1_output.json")
    p1_data = _read_json(p1_path) if os.path.exists(p1_path) else {}
    p1_field_specs = []
    if isinstance(p1_data.get("field_specs"), list):
        p1_field_specs = p1_data["field_specs"]
    global_field_specs = p0_field_specs + p1_field_specs

    # 合并逻辑:P2测试点为基础,P3风险补充风险标记,P4 PCI补充待确认标记
    merged_points = []
    from_p3_count = 0
    from_p4_count = 0

    # 复制P2测试点
    for tp in p2_points:
        point = dict(tp)  # 浅拷贝
        point["source"] = "P2"
        point.setdefault("risk_flag", False)
        point.setdefault("pci_flag", False)
        merged_points.append(point)

    # 边界安全前缀匹配(防止M01-F01误匹配M01-F010)
    def _boundary_prefix_match(full_str, prefix):
        """prefix后必须紧跟'-'或完全相等"""
        if not prefix or not full_str:
            return False
        if full_str == prefix:
            return True
        return full_str.startswith(prefix + "-")

    # P3风险点补充:多策略匹配(精确→边界前缀→新增)
    # P3实际字段:source_node(feature级别如M01-F01),无source_scenario
    # 改进:feature级风险应映射到该feature下所有scenario(不再break)
    for risk in p3_risks:
        risk_ref = risk.get("source_scenario") or risk.get("source_node") or risk.get("source", "")
        matched = False
        if risk_ref:
            # 策略1:精确匹配(scenario级别)
            for point in merged_points:
                point_source = point.get("source_scenario", "")
                if point_source and risk_ref == point_source:
                    point["risk_flag"] = True
                    point["risk_description"] = risk.get("description", "")
                    point["risk_severity"] = risk.get("severity", risk.get("impact", "medium"))
                    matched = True
                    from_p3_count += 1
                    break  # 精确匹配只命中1个
            # 策略2:边界前缀匹配(feature级→所有子scenario,不break)
            if not matched:
                for point in merged_points:
                    point_source = point.get("source_scenario", "")
                    if point_source and _boundary_prefix_match(point_source, risk_ref):
                        point["risk_flag"] = True
                        point["risk_description"] = risk.get("description", "")
                        point["risk_severity"] = risk.get("severity", risk.get("impact", "medium"))
                        matched = True
                # 前缀匹配命中后统一计数
                if matched:
                    from_p3_count += 1
        # R8修复:展开P3风险点的extended_test_points为独立测试点
        ext_tps = risk.get("extended_test_points", [])
        if ext_tps and isinstance(ext_tps, list):
            for idx_etp, etp in enumerate(ext_tps):
                if isinstance(etp, dict) and etp.get("description"):
                    merged_points.append({
                        "id": f"{risk.get('id', 'RISK')}-ETP-{idx_etp+1}",
                        "source": "P3",
                        "source_scenario": risk_ref,
                        "description": f"[扩展测试点] {etp.get('description', '')}",
                        "category": etp.get("category", "risk_verification"),
                        "risk_flag": True,
                        "risk_severity": risk.get("severity", risk.get("impact", "medium")),
                        "pci_flag": False,
                        "priority_hint": etp.get("priority_hint", "P1"),
                    })
                    from_p3_count += 1
        if not matched:
            merged_points.append({
                "id": risk.get("id", f"RISK-{len(merged_points)+1}"),
                "source": "P3",
                "source_scenario": risk_ref,
                "description": f"[风险验证] {risk.get('description', '')}",
                "category": "risk_verification",
                "risk_flag": True,
                "risk_severity": risk.get("severity", risk.get("impact", "medium")),
                "pci_flag": False,
                "priority_hint": "P1",
            })
            from_p3_count += 1

    # P4 PCI补充:多策略全量匹配(blocked_scenarios全量→source边界前缀→新增)
    # P4实际字段:source="P1"(无用),blocked_scenarios=[scenario IDs](有用)
    # 改进:blocked_scenarios全量匹配,不再break
    for pci in p4_pcis:
        blocked = pci.get("blocked_scenarios", [])
        # 兼容字符串转单元素数组
        if isinstance(blocked, str) and blocked:
            blocked = [blocked]
        elif not isinstance(blocked, list):
            blocked = []
        pci_source = pci.get("source_scenario") or pci.get("source", "")
        matched = False
        # 策略1:用blocked_scenarios全量匹配P2测试点(不break)
        if blocked:
            for point in merged_points:
                point_source = point.get("source_scenario", "")
                if point_source and point_source in blocked:
                    point["pci_flag"] = True
                    point["pci_description"] = pci.get("description", "")
                    # R10修复:透传P4 resolution_condition
                    if pci.get("resolution_condition"):
                        point["resolution_condition"] = pci["resolution_condition"]
                    matched = True
            if matched:
                from_p4_count += 1
        # 策略2:用source_scenario或source边界前缀匹配(全量)
        if not matched and pci_source and pci_source not in ("P0", "P1", "P2", "P3", "P4"):
            for point in merged_points:
                point_source = point.get("source_scenario", "")
                if point_source and (pci_source == point_source or _boundary_prefix_match(point_source, pci_source)):
                    point["pci_flag"] = True
                    point["pci_description"] = pci.get("description", "")
                    # R10修复:透传P4 resolution_condition
                    if pci.get("resolution_condition"):
                        point["resolution_condition"] = pci["resolution_condition"]
                    matched = True
            if matched:
                from_p4_count += 1
        if not matched:
            merged_points.append({
                "id": pci.get("id", f"PCI-{len(merged_points)+1}"),
                "source": "P4",
                "source_scenario": blocked[0] if isinstance(blocked, list) and blocked else pci_source,
                "description": f"[待确认] {pci.get('description', '')}",
                "category": "pci_verification",
                "risk_flag": False,
                "pci_flag": True,
                "priority_hint": "P1",
                # R10修复:透传resolution_condition
                "resolution_condition": pci.get("resolution_condition", ""),
            })
            from_p4_count += 1

    # 去重(基于description相似度,简化为完全相同)
    seen_descs = set()
    deduped = []
    removed = 0
    for point in merged_points:
        desc = point.get("description", "")
        if desc and desc in seen_descs:
            removed += 1
            continue
        if desc:
            seen_descs.add(desc)
        deduped.append(point)

    # V4.7.0: P5骨架增强 - 为每条测试点生成 step_expected_pairs/ui_elements/field_checklist
    # 解决P6 Agent "无参考乱生成"的根因问题
    # V4.9.0: 从P1 scenario数据补充operations_chain/page_path到测试点
    # P2测试点只有source_scenario引用,ui_elements需要从P1 scenario提取
    p1_scenario_map = {}  # scenario_id → scenario data
    if p1_data:
        ft = p1_data.get("feature_tree", {})
        ft_modules = ft.get("modules", []) if isinstance(ft, dict) else []
        if not ft_modules:
            ft_modules = p1_data.get("modules", [])
        for mod in ft_modules:
            for feat in mod.get("children", []):
                for scen in feat.get("children", []):
                    if scen.get("type") == "scenario":
                        # V4.9.1: 兼容 operations_chain 和 operations_steps(旧字段名)
                        ops = scen.get("operations_chain") or scen.get("operations_steps", [])
                        p1_scenario_map[scen.get("id", "")] = {
                            "operations_chain": ops,
                            "page_path": scen.get("page_path", ""),
                            "precondition": scen.get("precondition", ""),
                            "scenario_type": scen.get("scenario_type", ""),
                            "related_rules": scen.get("related_rules", []),
                            "name": scen.get("name", ""),
                            "description": scen.get("description", ""),  # V4.12.0: 场景完整描述
                        }

    # 注入P1 scenario数据到测试点
    for point in deduped:
        src = point.get("source_scenario", "")
        if src and src in p1_scenario_map:
            sc = p1_scenario_map[src]
            if not point.get("operations_chain"):
                point["operations_chain"] = sc.get("operations_chain", [])
            if not point.get("page_path"):
                point["page_path"] = sc.get("page_path", "")
            if not point.get("related_rules"):
                point["related_rules"] = sc.get("related_rules", [])
            if not point.get("precondition"):
                point["precondition"] = sc.get("precondition", "")
            pp = sc.get("page_path", "")
            if pp and not point.get("field_specs"):
                path_parts = [p.strip() for p in pp.replace("→", ">").replace("/", ">").split(">") if p.strip()]
                point["_page_path_parts"] = path_parts
            point["_scenario_name"] = sc.get("name", "")
            point["_scenario_description"] = sc.get("description", "")  # V4.12.0

    enrichment_count = 0
    for point in deduped:
        if not point.get("step_expected_pairs"):
            point["step_expected_pairs"] = _build_step_expected_pairs(point)
            enrichment_count += 1
        if not point.get("ui_elements") or (
            isinstance(point.get("ui_elements"), dict) and all(len(v) == 0 for v in point["ui_elements"].values())
        ):
            point["ui_elements"] = _build_ui_elements(point)
        if not point.get("field_checklist"):
            point["field_checklist"] = _build_field_checklist(point, global_field_specs)

    # 统一补齐 priority 和 status(truncation_guard L3 必检字段)
    for point in deduped:
        if "priority" not in point:
            point["priority"] = point.get("priority_hint", "P1")
        if "status" not in point:
            point["status"] = "active"

    # V3.2.8: 给每个测试点打complexity和expected_case_count标签
    # V4.7.0: risk_verification 使用规则表驱动(基于 risk_severity),覆盖率更精确
    # 规则:根据测试点类型、风险标记、PCI标记、描述长度综合判断
    # L1(简单)≥1条, L2(常规)≥2条, L3(复杂)≥3条
    SIMPLE_CATEGORIES = {"compatibility", "display", "ui_check", "兼容回归", "展示校验"}
    COMPLEX_CATEGORIES = {"permission", "exception", "integration", "data_consistency",
                          "权限验证", "异常处理", "集成异常", "数据一致性"}

    # V4.7.0: risk_verification 规则表(基于 P3 risk_severity)
    RISK_CASE_COUNT_MAP = {"low": 1, "medium": 2, "high": 3, "critical": 3}

    for point in deduped:
        cat = (point.get("category", "") or "").lower()
        desc = point.get("description", "") or ""
        has_risk = point.get("risk_flag", False)
        has_pci = point.get("pci_flag", False)
        source = point.get("source", "P2")

        # V4.7.0: risk_verification 使用规则表驱动(不再依赖通用评分)
        if cat == "risk_verification":
            severity = (point.get("risk_severity", "") or "").lower()
            expected = RISK_CASE_COUNT_MAP.get(severity, 1)
            point["complexity"] = "L2"
            point["expected_case_count"] = expected
            continue

        # 通用复杂度评分
        score = 0
        if cat in COMPLEX_CATEGORIES:
            score += 2
        elif cat in SIMPLE_CATEGORIES:
            score += 0
        else:
            score += 1  # 默认常规
        if has_risk:
            score += 1
        if has_pci:
            score += 1
        if source in ("P3", "P4"):
            score += 1  # 风险/PCI派生的测试点本身就复杂
        if len(desc) > 100:
            score += 1  # 描述越长通常越复杂

        # 分级
        if score <= 0:
            point["complexity"] = "L1"
            point["expected_case_count"] = 1
        elif score <= 2:
            point["complexity"] = "L2"
            point["expected_case_count"] = 2
        else:
            point["complexity"] = "L3"
            point["expected_case_count"] = 3
        # P0测试点强制上限expected_case_count=2,避免冒烟比例被稀释
        if point.get("priority") == "P0" and point.get("expected_case_count", 2) > 2:
            point["expected_case_count"] = 2

    # 统计复杂度分布
    complexity_dist = {}
    total_expected = 0
    for point in deduped:
        c = point.get("complexity", "L2")
        complexity_dist[c] = complexity_dist.get(c, 0) + 1
        total_expected += point.get("expected_case_count", 2)

    # 构造P5输出
    p5_output = {
        "schema_version": "1.0.0",
        "prompt_version": "1.0.0",
        "requirement_id": p2_data.get("requirement_id", ""),
        "test_points": deduped,
        "merge_log": {
            "from_p2": len(p2_points),
            "from_p3": from_p3_count,
            "from_p4": from_p4_count,
            "merged": len(merged_points),
            "removed_duplicates": removed,
            "final_count": len(deduped),
            "v470_enriched": enrichment_count,
        },
        "coverage_summary": {
            "total_test_points": len(deduped),
            "risk_flagged": sum(1 for p in deduped if p.get("risk_flag")),
            "pci_flagged": sum(1 for p in deduped if p.get("pci_flag")),
            "complexity_distribution": complexity_dist,
            "total_expected_cases": total_expected,
        },
    }

    # V4.12.0: description自动扩展 - 当description<30字时从step_expected_pairs/operations_chain合成
    # 解决P5测试点description过于简单导致P6 Agent无据可依的问题
    for point in deduped:
        desc = str(point.get("description", "")).strip()
        if len(desc) >= 30:
            continue
        page_path = point.get("page_path", "")
        pairs = point.get("step_expected_pairs", []) or []
        ops_chain = point.get("operations_chain", []) or []
        category = point.get("category", "")

        # 从step_expected_pairs提取操作序列
        action_parts = []
        if ops_chain:
            for op in ops_chain[:5]:
                if isinstance(op, dict):
                    a = op.get("action", op.get("operation", ""))
                    t = op.get("target", op.get("target_element", ""))
                    if a and t:
                        action_parts.append(f"{a}「{t}」")
                    elif a:
                        action_parts.append(a)
        if not action_parts and pairs:
            for sp in pairs[:4]:
                if isinstance(sp, dict):
                    s = sp.get("step", "")
                    if s:
                        action_parts.append(s)

        # 构建扩展description
        expanded_parts = []
        if page_path and desc:
            expanded_parts.append(f"在{page_path}页面")
        if action_parts:
            expanded_parts.append("→".join(action_parts[:4]))
        if not expanded_parts and desc:
            expanded_parts.append(desc)
        if expanded_parts:
            # 避免重复"验证"前缀(description通常已含"验证"开头)
            verify_target = desc
            if desc.startswith("验证"):
                verify_target = desc[2:]
            expanded_parts.append(f"验证{verify_target}")
            new_desc = ",".join(expanded_parts)
            # 确保≥30字,不足则追加category描述
            if len(new_desc) < 30:
                cat_map = {
                    "main_flow": "核心正向流程",
                    "branch": "分支场景",
                    "exception": "异常处理",
                    "boundary": "边界条件",
                    "permission": "权限控制",
                }
                new_desc += f"({cat_map.get(category, category)})"
            point["description"] = new_desc[:200]  # 截断保护
            point["_desc_auto_expanded"] = True  # 标记来源

    # 写入tmp→truncation_guard→gate pass
    tmp_path = os.path.join(data_dir, "p5_output.tmp.json")
    _write_json(tmp_path, p5_output)

    ok, msg = run_truncation_guard(skill_dir, data_dir, task_id, "P5")
    if ok:
        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete("P5")
        print(json.dumps({
            "status": "ok",
            "step": "P5",
            "total_test_points": len(deduped),
            "from_p2": len(p2_points),
            "from_p3": from_p3_count,
            "from_p4": from_p4_count,
            "removed_duplicates": removed,
        }))
    else:
        print(json.dumps({"status": "guard_failed", "step": "P5", "reason": msg}))
        sys.exit(1)


# ============================================================
# V4.11.0: P6逐条生成(替代批量分批)
# ============================================================

def _extract_project_name(data_dir):
    """V4.12.6: 从task_meta提取干净的项目名称
    优先级: task_meta.project_name → task_meta.requirement_title → 空
    """
    meta_path = os.path.join(data_dir, "task_meta.json")
    if not os.path.exists(meta_path):
        return ""
    try:
        meta = _read_json(meta_path)
        name = meta.get("project_name", "") or meta.get("requirement_title", "")
        # 清理: 去除项目名中的路径前缀和多余标点
        if name:
            name = str(name).strip().split("\n")[0][:50]  # 取第一行,限50字
        return name
    except Exception:
        return ""


def _extract_biz_context(data_dir):
    """V4.11.0: 从P0输出提取业务上下文(精简版,~800字上限)"""
    p0_path = os.path.join(data_dir, "p0_output.json")
    if not os.path.exists(p0_path):
        return ""
    try:
        p0 = _read_json(p0_path)
        parts = []
        pages = p0.get("blocks", {}).get("pages", p0.get("pages", []))
        ops = p0.get("blocks", {}).get("operations", p0.get("operations", []))
        rules = p0.get("blocks", {}).get("business_rules", p0.get("business_rules", []))
        if pages:
            parts.append("页面: " + "; ".join(str(p)[:200] for p in pages[:5]))
        if ops:
            parts.append("操作: " + "; ".join(str(o)[:200] for o in ops[:5]))
        if rules:
            parts.append("业务规则: " + "; ".join(str(r)[:200] for r in rules[:5]))
        return "\n".join(parts)[:800]
    except Exception:
        return ""


def _classify_source_type(tp):
    """V4.12.4: 从source+category推导source_type"""
    source = tp.get("source", "")
    category = tp.get("category", "")
    if source == "risk" or category == "risk_verification":
        return "risk_extension"
    if category in ("boundary",):
        return "boundary_value"
    if category in ("exception", "permission", "security"):
        return "exception"
    if category in ("integration", "compatibility"):
        return "integration"
    return "functional"


def _check_tp_risk_link(tp, p3_risks):
    """V4.12.4: 检查TP是否关联P3风险点
    匹配策略: TP title/description包含P3风险点的关键词
    """
    if not p3_risks:
        return False, ""
    tp_text = f"{tp.get('title','')} {tp.get('description','')}".lower()
    for risk in p3_risks:
        risk_id = str(risk.get("id", ""))
        risk_desc = str(risk.get("description", ""))
        # 风险ID匹配(如 RISK-001 → TP中可能引用)
        if risk_id and risk_id.lower() in tp_text:
            return True, str(risk.get("severity", risk.get("risk_severity", "")))
        # 风险关键词匹配(取风险描述中的关键短语)
        for word in risk_desc.split()[:5]:
            if len(word) >= 3 and word.lower() in tp_text:
                return True, str(risk.get("severity", risk.get("risk_severity", "")))
    return False, ""


def _category_hint(category):
    """V4.12.4: 将category映射为中文引导提示"""
    hints = {
        "main_flow": "主流程功能验证(核心路径,冒烟覆盖)",
        "branch": "分支流程验证(备选路径)",
        "exception": "异常场景验证(输入异常/状态异常/权限异常)",
        "boundary": "边界值验证(数值/长度/时间边界)",
        "permission": "权限控制验证(不同角色/数据权限)",
        "risk_verification": "风险触发场景验证(系统应对因果链)",
        "field_validation": "字段级校验",
        "integration": "集成联动验证",
        "security": "安全合规验证",
        "state_migration": "状态流转验证",
        "compatibility": "兼容性验证",
    }
    return hints.get(category, "功能验证")


def _write_tp_contexts(data_dir, test_points, model_tier, p3_risks=None, p4_pci_list=None):
    """V4.12.0: 为每个TP写入完整上下文(供p6_generate_one读取)

    V4.12变更:补全page_path/precondition/step_expected_pairs/ui_elements/
    field_checklist/operations_chain字段,解决P6 Agent无据可依的根因问题。
    所有新增字段带兜底空值,兼容旧P5数据。
    """
    out_dir = os.path.join(data_dir, "p6_tp_output")
    _ensure_dir(out_dir)
    biz_ctx = _extract_biz_context(data_dir)
    for i, tp in enumerate(test_points):
        # V4.12.0: 相邻TP差异化提示(前2后2,供LLM生成差异化用例)
        adj_tps = []
        for offset in (-2, -1, 1, 2):
            ni = i + offset
            if 0 <= ni < len(test_points):
                nt = test_points[ni]
                adj_tps.append({
                    "relation": "上一个" if offset < 0 else "下一个",
                    "title": nt.get("title", ""),
                    "category": nt.get("category", ""),
                })

        risk_flag, risk_severity = _check_tp_risk_link(tp, p3_risks or [])

        ctx = {
            "tp_index": i,
            "tp_id": tp.get("id", ""),
            "title": tp.get("title", ""),
            "description": tp.get("description", ""),
            "category": tp.get("category", ""),
            "priority": tp.get("priority", ""),
            "expected_case_count": tp.get("expected_case_count", 2),
            "business_context": biz_ctx,
            "model_tier": model_tier,
            # V4.12.0: 补全P6 prompt消费的结构化字段(所有字段兜底空值)
            "page_path": tp.get("page_path", ""),
            "precondition": tp.get("precondition", "") or tp.get("_precondition", ""),
            "step_expected_pairs": tp.get("step_expected_pairs", []) or [],
            "ui_elements": tp.get("ui_elements", {}) or {},
            "field_checklist": tp.get("field_checklist", []) or [],
            "operations_chain": tp.get("operations_chain", []) or [],
            "related_rules": tp.get("related_rules", []) or [],
            "scenario_description": tp.get("_scenario_description", ""),  # P1场景完整描述
            # V4.12.0: 相邻TP供差异化参考
            "adjacent_tps": adj_tps,
            "total_tps": len(test_points),  # V4.12.5: 总TP数(用于分批回顾+频率检测豁免)
            # V4.12.4: P6质量引导增强字段
            "source": tp.get("source", "requirement"),
            "source_type": _classify_source_type(tp),
            "risk_flag": risk_flag,
            "risk_severity": risk_severity,
            "need_smoke": (tp.get("priority", "").upper() in ("P0", "HIGHEST")
                          and tp.get("category", "") in ("main_flow", "正向", "功能")),
            "pci_flag": bool(p4_pci_list and any(
                tp.get("id", "") in str(pci) for pci in p4_pci_list)),
            "category_hint": _category_hint(tp.get("category", "")),
        }
        _write_json(os.path.join(out_dir, f"tp_{i:03d}_context.json"), ctx)


def _build_single_tp_prompt(ctx, model_tier):
    """V4.12.1: 构建单TP完整prompt(~1100B)
    
    核心改进:
    - 补全ui_elements/field_checklist/operations_chain等结构化数据
    - LLM输出5核心字段(title/menu_path/preconditions/steps/expected_results)
    - 增加强制具体性要求(引用UI元素、步骤≥15字、禁止通用模板)
    - 修复LOW格式示例中的模糊词("操作成功"→具体描述)
    - 增加提交前自检清单
    """
    title = ctx.get("title", "")
    desc = ctx.get("description", "")
    ec = ctx.get("expected_case_count", 2)
    biz = ctx.get("business_context", "")
    page_path = ctx.get("page_path", "")
    precondition = ctx.get("precondition", "")
    step_pairs = ctx.get("step_expected_pairs", []) or []
    ui_elems = ctx.get("ui_elements", {}) or {}
    fields = ctx.get("field_checklist", []) or []
    ops_chain = ctx.get("operations_chain", []) or []
    related_rules = ctx.get("related_rules", []) or []
    scenario_desc = ctx.get("scenario_description", "")
    # V4.12.4: P6质量引导字段
    source = ctx.get("source", "requirement")
    source_type = ctx.get("source_type", "functional")
    risk_flag = ctx.get("risk_flag", False)
    risk_severity = ctx.get("risk_severity", "")
    need_smoke = ctx.get("need_smoke", False)
    pci_flag = ctx.get("pci_flag", False)
    category_hint = ctx.get("category_hint", "功能验证")

    lines = [
        "你是测试用例编写专家,基于以下上下文为测试点生成具体可执行的测试用例。",
        "",
        "## 测试点",
        f"**{title}**",
        desc,
        "",
    ]

    # 页面路径
    if page_path:
        lines.extend(["## 页面路径", page_path, ""])

    # 操作链路(优先operations_chain,其次step_expected_pairs)
    if ops_chain:
        lines.append("## 操作链路")
        for op in ops_chain[:8]:
            if isinstance(op, dict):
                action = op.get("action", op.get("operation", ""))
                target = op.get("target", op.get("target_element", ""))
                if action and target:
                    lines.append(f"- {action}「{target}」")
                elif action:
                    lines.append(f"- {action}")
        lines.append("")
    elif step_pairs:
        lines.append("## 操作骨架")
        for sp in step_pairs[:5]:
            if isinstance(sp, dict):
                s = sp.get("step", "")
                e = sp.get("expected", "")
                if s:
                    lines.append(f"- {s}  →  期望:{e}" if e else f"- {s}")
        lines.append("")

    # UI元素清单
    if ui_elems:
        parts = []
        for cat in ("buttons", "inputs", "selectors", "labels"):
            items = ui_elems.get(cat, [])
            if items:
                label = {"buttons": "按钮", "inputs": "输入框", "selectors": "下拉", "labels": "标签"}.get(cat, cat)
                parts.append(f"{label}:{'、'.join(str(x)[:20] for x in items[:5])}")
        if parts:
            lines.extend(["## 可用UI元素", "; ".join(parts), ""])

    # 涉及字段
    if fields:
        lines.extend(["## 涉及字段", "、".join(str(f)[:30] for f in fields[:8]), ""])

    # 前置条件
    if precondition:
        lines.extend(["## 前置条件", precondition, ""])

    # 业务上下文
    if biz:
        lines.extend(["## 业务上下文", biz, ""])

    # 场景描述(P1级丰富上下文)
    if scenario_desc:
        lines.extend(["## 场景描述(来自需求分析)", scenario_desc[:300], ""])

    # 业务规则
    if related_rules:
        lines.append("## 业务规则(期望结果必须基于这些规则断言)")
        for r in related_rules[:5]:
            if isinstance(r, str):
                lines.append(f"- {r[:120]}")
            elif isinstance(r, dict):
                rid = r.get("id", r.get("rule_id", ""))
                rdesc = r.get("description", r.get("rule", ""))
                if rid or rdesc:
                    lines.append(f"- {rid}: {rdesc}"[:120])
        lines.append("")

    # 相邻TP差异化提示
    adj_tps = ctx.get("adjacent_tps", []) or []
    if adj_tps:
        lines.append("## 相邻测试点(确保你的用例步骤与以下TP有差异化)")
        for at in adj_tps:
            lines.append(f"- {at['relation']}:{at['title']}({at['category']})")
        lines.append("⚠️ 你的用例步骤必须与上述相邻TP有明显差异,禁止复用相同步骤。")
        lines.append("")

    # === V4.12.4: 差异化引导模块 ===

    # 模块1：风险扩展引导
    if risk_flag:
        lines.extend([
            "🔴 **风险扩展测试点**" + (f" (风险等级: {risk_severity})" if risk_severity else ""),
            "",
            "此测试点存在关联风险，你必须生成覆盖以下维度的风险场景用例：",
            "- **风险触发路径**：描述从正常状态→异常状态的变化过程（谁、做什么、在什么条件下触发）",
            "- **系统应对链**：期望结果必须包含「检测→告警→阻断→恢复」的因果链",
            "- **不同触发条件**：每个用例覆盖不同的风险触发入口（数据异常/操作异常/并发冲突）",
            "",
            "❌ 禁止生成纯功能正向验证用例（这不是功能测试点）",
            "✅ 必须生成风险触发 → 系统应对的因果链用例",
            "",
        ])

    # 模块2：PCI合规引导
    if pci_flag:
        lines.extend([
            "🔒 **PCI合规审计测试点**",
            "",
            "要求：",
            "- 每个用例必须绑定至少一个 PCI 合规项（标注PCI编号）",
            "- 覆盖：数据脱敏、权限边界、审计日志 三类合规场景",
            "- 期望结果必须包含合规判定（如'敏感字段已脱敏显示'）",
            "",
        ])

    # 模块3：冒烟用例引导
    if need_smoke:
        lines.extend([
            "🔥 **冒烟用例要求** (此测试点是核心主流程P0)",
            "",
            "第1条用例必须是冒烟用例：",
            "- 覆盖核心正向功能的最短完整路径（3-5步）",
            "- 预置条件为标准正常业务状态",
            "- 步骤包含最小必要操作，直达目标页面/功能",
            "- 期望结果可观测（页面跳转/数据变化/状态变更）",
            '- 必须在JSON中设置 `\"is_smoke\": true`',
            "",
            f"后续 {ec} 条可覆盖异常/边界/权限等其他场景。",
            "",
        ])

    # 模块4：用例类型分布建议
    lines.extend([
        f"📊 **用例类型指引** ({category_hint})",
        "",
    ])
    if need_smoke:
        lines.append("- 第1条：冒烟用例(主流程核心正向)")
    if ec >= 2:
        smoke_offset = 1 if need_smoke else 0
        lines.append(f"- 第{smoke_offset+1}条：主流程正向验证")
        n_exc = max(1, ec // 3)
        if n_exc > 0:
            lines.append(f"- 第{smoke_offset+2}条起：异常场景 ({n_exc}条)")
        n_bnd = max(0, ec - 1 - (1 if need_smoke else 0) - n_exc)
        if n_bnd > 0:
            lines.append(f"- 余下：边界场景 ({n_bnd}条)")
    lines.extend([
        f"- ⚠️ 禁止{ec}条用例全部为同一类型！",
        "",
    ])

    # 生成要求
    lines.extend([
        "## 生成要求",
        "1. 每条步骤 ≥15字,格式:「动作词」+「UI元素名」(如点击「查询」按钮、在「员工姓名」输入框输入'张三')",
        "2. steps 第1步必须包含页面入口描述(引用上述页面路径)" if page_path else "2. steps 第1步必须包含具体页面路径",
        "3. 步骤中必须引用至少1个上述UI元素或字段(用「」包裹)" if (ui_elems or fields) else "3. 步骤中必须引用具体UI元素或字段(用「」包裹)",
        "4. 禁止使用:执行相关操作/进入对应页面/验证结果/执行操作流程",
        "5. 期望结果必须可观测:页面跳转/弹出提示/列表刷新/状态变为/显示具体值",
        "6. 每条用例的步骤必须与其他用例有差异,不得复用相同步骤",
        "7. 必须输出 menu_path(用例菜单,引用上述页面路径)",
        "8. 必须输出 preconditions(前置条件,基于上述前置条件+场景描述)",
        "",
    ])

    # 格式示例
    if model_tier == "LOW":
        lines.extend([
            "## 格式示例",
            "```json",
            '[{"title":"验证XX-正常场景","menu_path":"营销管理→协同分润→债券投顾","preconditions":"已登录CRM系统",'
            '"steps":"1. 点击「查询」按钮\\n2. 在「员工姓名」输入框输入\u2018张三\u2019",'
            '"expected_results":"1. 列表刷新显示查询结果\\n2. 列表数据中员工姓名字段与输入值一致"}]',
            "```",
            "",
        ])

    lines.extend([
        f"🔴 必须生成 **{ec}** 条用例（不是1条！必须达到{ec}条！），直接输出JSON数组(每条必须包含title/menu_path/preconditions/steps/expected_results):",
        "```json",
        "[",
        '  {"title":"...","menu_path":"...","preconditions":"...","steps":"1. ...\\n2. ...","expected_results":"1. ...\\n2. ..."},',
        "... （共计{ec}条用例，不得少于{ec}条）".replace("{ec}", str(ec)),
        "]",
        "```",
    ])

    return "\n".join(lines)


def _quick_gate_single_tp(cases):
    """V4.11.0: 单TP快速Gate(G1+G1.5+G5-intra),不跨TP"""
    issues = []
    fuzzy_words = ["正常", "成功", "正确", "符合预期", "功能正常", "数据正确处理", "操作成功完成"]
    for c in cases:
        cid = c.get("case_id", "?")
        if not str(c.get("title", "")).strip():
            issues.append({"case_id": cid, "rule": "G1", "violation": "title为空"})
        if not str(c.get("steps", "")).strip():
            issues.append({"case_id": cid, "rule": "G1", "violation": "steps为空"})
        exp = str(c.get("expected_results", "")).strip()
        if not exp:
            issues.append({"case_id": cid, "rule": "G1.5", "violation": "expected_results为空"})
            continue
        for w in fuzzy_words:
            if w in exp:
                issues.append({"case_id": cid, "rule": "G1.5",
                    "violation": f"期望含模糊词'{w}'"})
                break
    # G5-intra: 同TP内步骤完全相同 → WARNING(不retry)
    if len(cases) >= 2:
        steps_set = set(str(c.get("steps", "")).strip() for c in cases)
        if len(steps_set) == 1:
            issues.append({
                "rule": "G5-intra",
                "violation": f"同TP内{len(cases)}条用例步骤完全相同",
                "type": "warning",
            })
    # 仅返回需retry的(排除warning)
    return [i for i in issues if i.get("type") != "warning"]


def _check_placeholder_patterns(cases, tp_index, ctx=None):
    """V4.12.2: 占位符检测 — 拦截Agent模板注入
    
    策略①: 关键词模式匹配（拦截模板短语，4个中风险词加二次判定）
    策略②: steps空洞检测（拦截无具体对象的通用步骤）
    策略③: 同TP内case相似度WARNING（标记但不拦截）
    策略④: context消费检查（Agent是否引用了TP上下文的具体元素）
    """
    issues = []
    
    # 策略①: 关键词模式匹配
    # 高风险短语（绝对是占位符，直接拦截）
    HIGH_RISK_PATTERNS = [
        "进入功能页面执行测试点", "进入功能页面执行",
        "验证操作结果", "页面或数据发生相应变化",
        "执行相关操作", "进入对应页面",
        "执行操作流程", "验证功能正常",
    ]
    # 中风险短语（含具体UI引用时可能合法，需二次判定）
    MEDIUM_RISK_PATTERNS = ["验证结果", "查看执行结果"]
    # UI元素标记
    HAS_UI_ELEMENT = re.compile(r'[「『《].+?[」』》]')
    
    for c in cases:
        cid = c.get("case_id", "?")
        title = str(c.get("title", ""))
        steps_text = str(c.get("steps", ""))
        exp_text = str(c.get("expected_results", ""))
        combined = f"{title} {steps_text} {exp_text}"
        
        # 高风险直接拦截
        for pat in HIGH_RISK_PATTERNS:
            if pat in combined:
                issues.append({
                    "case_id": cid,
                    "rule": "PLACEHOLDER_DETECT",
                    "violation": f"检测到占位符短语'{pat}'——Agent未基于P6 prompt生成用例",
                    "type": "block",
                })
                break
        if any(i["case_id"] == cid for i in issues):
            continue
        
        # 中风险二次判定：同句含「」UI引用 → 合法，否则拦截
        for pat in MEDIUM_RISK_PATTERNS:
            if pat in combined:
                # 找到含该短语的句子
                for line in combined.split("\n"):
                    if pat in line:
                        if HAS_UI_ELEMENT.search(line):
                            break  # 含具体UI引用 → 放过
                else:
                    # 所有含该短语的行都没有UI引用 → 拦截
                    issues.append({
                        "case_id": cid,
                        "rule": "PLACEHOLDER_DETECT",
                        "violation": f"检测到占位符短语'{pat}'且无具体UI引用——Agent未基于P6 prompt生成用例",
                        "type": "block",
                    })
                    break

    # 策略②: steps空洞检测
    HOLLOW_PATTERNS = [
        r'^\s*\d*[.、)]?\s*(执行|进行|操作|验证|检查|查看|确认)\s*(相关|对应|指定)?\s*(操作|内容|功能|动作|流程|数据|结果)?\s*$',
    ]
    for c in cases:
        cid = c.get("case_id", "?")
        steps_text = str(c.get("steps", "")).strip()
        if not steps_text:
            continue
        if any(i["case_id"] == cid for i in issues):
            continue
        steps_lines = [s.strip() for s in steps_text.split("\n") if s.strip()]
        hollow_count = 0
        for sl in steps_lines:
            cleaned = re.sub(r'^\s*\d+[.、)]?\s*', '', sl)
            # 步骤含具体UI元素引用(「」包裹) → 视为非空洞
            if HAS_UI_ELEMENT.search(cleaned):
                continue
            # 检测1: 步骤过短（<10字去除编号后）
            if len(cleaned) < 10:
                hollow_count += 1
                continue
            # 检测2: 步骤匹配空洞模式
            for pattern in HOLLOW_PATTERNS:
                if re.match(pattern, sl, re.IGNORECASE):
                    hollow_count += 1
                    break
        # 超过60%步骤空洞 → 拦截
        if steps_lines and hollow_count / len(steps_lines) > 0.6:
            issues.append({
                "case_id": cid,
                "rule": "HOLLOW_STEPS",
                "violation": f"{hollow_count}/{len(steps_lines)}条步骤空洞（缺乏具体操作对象）",
                "type": "block",
            })

    # 策略③: 同TP内case步骤高度相似 → WARNING标记（不拦截）
    if len(cases) >= 2:
        steps_list = [str(c.get("steps", "")).strip() for c in cases]
        # 简单检测：步骤完全相同的比例
        from collections import Counter
        steps_counter = Counter(steps_list)
        most_common_count = steps_counter.most_common(1)[0][1] if steps_counter else 0
        if most_common_count >= 2:
            issues.append({
                "rule": "SIMILAR_STEPS_WARNING",
                "violation": f"同TP内{most_common_count}/{len(cases)}条用例步骤完全相同",
                "type": "warning",
            })

    # 策略④: context消费检查 — Agent是否引用了TP上下文的具体元素
    # 当任何case被拦截时，额外检查该case是否引用了任何context元素
    # 如果引用了至少1个具体元素 → 可能是误杀，降级为WARNING
    if ctx and issues:
        ctx_elems = set()
        ue = ctx.get("ui_elements", {}) or {}
        for cat_elems in ue.values():
            for e in (cat_elems if isinstance(cat_elems, list) else []):
                ctx_elems.add(str(e))
        for f in (ctx.get("field_checklist", []) or []):
            ctx_elems.add(str(f))
        # 从operations_chain提取目标元素
        for op in (ctx.get("operations_chain", []) or []):
            if isinstance(op, dict):
                t = op.get("target", op.get("target_element", ""))
                if t:
                    ctx_elems.add(str(t))
        
        if ctx_elems:
            for iss in issues:
                if iss.get("type") == "block":
                    cid = iss.get("case_id", "")
                    # 找对应case的内容
                    for c in cases:
                        if c.get("case_id", "") == cid:
                            case_text = str(c.get("steps", "")) + " " + str(c.get("title", ""))
                            referenced = [e for e in ctx_elems if e in case_text]
                            if referenced:
                                iss["type"] = "warning"
                                iss["rule"] = iss.get("rule", "") + "_OVERRIDE"
                                iss["violation"] += f"（但引用了上下文元素{referenced[:3]}，降级为WARNING）"
                            break

    # 返回需拦截的（排除warning）
    return [i for i in issues if i.get("type") != "warning"]


def _build_fix_hints_single_tp(issues):
    """V4.11.0: 单TP修复提示"""
    hints = []
    for iss in issues:
        v = str(iss.get("violation", ""))
        if "title为空" in v:
            hints.append({"action": "fill_title", "hint": "补全title"})
        elif "steps为空" in v:
            hints.append({"action": "fill_steps", "hint": "补全steps"})
        elif "模糊词" in v:
            hints.append({"action": "fix_vague", "hint": "改为可观测描述(显示XX/提示XX/跳转XX)"})
    return hints


def _save_single_tp(data_dir, tp_index, agent_output):
    """V4.12.1: 保存单TP生成的用例(19列全量补全)
    V4.12.5: 频率检测(反脚本) + 质量预览(条件阻断)
    """
    import re as _tp_re

    # === V4.12.5: 频率检测 — 软拦截三段式 ===
    freq_path = os.path.join(data_dir, "p6_tp_output", ".save_freq.json")
    freq_data = {}
    if os.path.exists(freq_path):
        try:
            freq_data = _read_json(freq_path)
        except Exception:
            pass
    now = time.time()
    tp_key = f"tp_{tp_index:03d}"
    repeat_count = 0  # V4.12.5: 初始化为0，避免小任务豁免时未定义

    # 豁免：TP总数≤5的小任务
    ctx_small_path = os.path.join(data_dir, "p6_tp_output", f"tp_{tp_index:03d}_context.json")
    if os.path.exists(ctx_small_path):
        try:
            ctx_small = _read_json(ctx_small_path)
            total_tps = ctx_small.get("total_tps", 0)
        except Exception:
            total_tps = 0
    else:
        total_tps = 0

    if total_tps > 5:
        # 检查1：同一TP重复save间隔 < 8秒
        last_save = freq_data.get(tp_key, {}).get("last_save", 0)
        repeat_count = freq_data.get(tp_key, {}).get("repeat_count", 0)
        if last_save and (now - last_save) < 8:
            repeat_count += 1
        else:
            repeat_count = 0

        # 检查2：最近3次save平均间隔 < 5秒
        recent = [(k, v.get("last_save", 0)) for k, v in freq_data.items()
                  if v.get("last_save", 0) > now - 120]
        recent.sort(key=lambda x: x[1])
        fast_saves = 0
        if len(recent) >= 3:
            intervals = [recent[-(i+1)][1] - recent[-(i+2)][1]
                        for i in range(min(2, len(recent)-1))]
            avg_interval = sum(intervals) / len(intervals) if intervals else 999
            if avg_interval < 5:
                fast_saves = len(recent)

        if repeat_count >= 2 or fast_saves >= 5:
            # 第3次快速save → 拒绝
            print(json.dumps({
                "status": "rejected",
                "reason": "⛔ 疑似脚本批量生成：连续快速save。请阅读prompt后逐条手写用例，不是写脚本循环调用。",
                "tp_index": tp_index,
                "repeat_count": repeat_count,
                "fast_saves": fast_saves,
                "fix": "每个TP应花30秒以上阅读p6_generate_one输出的prompt，手写生成用例JSON",
            }))
            sys.exit(1)
        elif repeat_count >= 1 or fast_saves >= 3:
            # 第2次快速save → 警告
            print(json.dumps({
                "status": "warning",
                "reason": "⚠️ 连续快速save。请花更多时间阅读prompt后再生成用例。",
                "tp_index": tp_index,
                "hint": "如果确实需要修正已保存的用例，请使用 --merge 模式（增量更新）而非重新save",
            }), file=sys.stderr)

    # 记录本次save
    freq_data[tp_key] = {"last_save": now, "repeat_count": repeat_count}
    # 只保留最近30条记录
    if len(freq_data) > 30:
        oldest_keys = sorted(freq_data.keys(),
                            key=lambda k: freq_data[k].get("last_save", 0))[:len(freq_data)-30]
        for ok in oldest_keys:
            del freq_data[ok]
    _write_json(freq_path, freq_data)
    # === 频率检测结束 ===

    try:
        data = json.loads(agent_output)
    except Exception:
        m = _tp_re.search(r'\[[\s\S]*\]', agent_output)
        if m:
            try:
                data = json.loads(m.group())
            except Exception:
                print(json.dumps({"status": "error", "reason": "JSON解析失败"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "reason": "不含JSON"}))
            sys.exit(1)
    if isinstance(data, list):
        data = {"testcases": data}
    cases = data.get("testcases", data.get("cases", []))
    if not cases:
        print(json.dumps({"status": "quality_rejected", "reason": "用例为空"}))
        sys.exit(1)
    # 读取context获取TP元信息
    ctx_path = os.path.join(data_dir, "p6_tp_output", f"tp_{tp_index:03d}_context.json")
    ctx = _read_json(ctx_path)
    tp_id = ctx.get("tp_id", "")
    pri = ctx.get("priority", "P1")
    cat = ctx.get("category", "")
    biz_ctx = ctx.get("business_context", "")
    page_path = ctx.get("page_path", "")
    # V4.12.6: 从task_meta提取项目名(不截断biz_ctx)
    project_name = _extract_project_name(data_dir) or ""
    if not project_name:
        # 兜底: 从biz_ctx中提取纯文本项目名(跳过"页面:"等前缀)
        first_line = biz_ctx.split("\n")[0] if biz_ctx else ""
        if first_line and not first_line.startswith("页面:") and not first_line.startswith("操作:"):
            project_name = first_line[:30]
    # V4.12.1: 自动补全字段 - 补全全部19列必填字段,与batch模式一致
    # LLM输出5核心字段(title/menu_path/preconditions/steps/expected_results),其余代码补全
    for i, c in enumerate(cases):
        # V4.12.6: 如果agent提供的case_id含非ASCII字符(乱码)→自动生成
        agent_cid = c.get("case_id", "")
        auto_cid = f"{tp_id}-TC-{i + 1:03d}"
        if agent_cid and not all(ord(ch) < 128 for ch in str(agent_cid)):
            c["case_id"] = auto_cid
        else:
            c["case_id"] = agent_cid or auto_cid
        c["source_test_point"] = tp_id
        c["priority"] = c.get("priority", "") or pri
        c["is_smoke"] = c.get("is_smoke", "") or (
            (pri == "P0" and cat in ("main_flow", "branch", "integration"))
        )
        c["test_category"] = c.get("test_category", c.get("category", "")) or cat
        # V4.12.0: 补全batch模式已有但单TP模式缺失的19列格式字段
        c["project"] = c.get("project", "") or project_name
        c["case_type"] = c.get("case_type", "") or "测试用例"
        c["requirement"] = c.get("requirement", "") or ""
        c["menu_path"] = c.get("menu_path", "") or page_path
        c["creator"] = c.get("creator", "") or "AI生成"
        c["assignee"] = c.get("assignee", "") or ""
        c["test_case_type"] = c.get("test_case_type", "") or ""
        c["status"] = c.get("status", "") or ""
        c["screenshot"] = c.get("screenshot", "") or ""
        c["test_suite"] = c.get("test_suite", "") or ""
        for f in ["preconditions", "remarks"]:
            if f not in c:
                c[f] = ""
    # 格式归一化
    for c in cases:
        for f in ["steps", "expected_results", "preconditions"]:
            if isinstance(c.get(f), list):
                c[f] = "\n".join(str(s) for s in c[f] if s)
    # Gate快速检查
    issues = _quick_gate_single_tp(cases)
    if issues:
        # V4.11.0: retry计数追踪
        retry_state_path = os.path.join(data_dir, "orchestrator_state.json")
        retry_key = f"p6_tp_{tp_index}_retry"
        retry_count = 0
        if os.path.exists(retry_state_path):
            try:
                sd = _read_json(retry_state_path)
                retry_count = sd.get(retry_key, 0) + 1
                sd[retry_key] = retry_count
                _write_json(retry_state_path, sd)
            except Exception:
                pass
        print(json.dumps({
            "status": "quality_rejected",
            "tp_index": tp_index,
            "retry_count": retry_count,
            "issues": issues,
            "fix_hints": _build_fix_hints_single_tp(issues),
            "retry_hint": f"按fix_hints修复后重新 p6_generate_one --tp-index {tp_index} --save "
                          f"--agent-output '...'"
        }))
        sys.exit(1)

    # V4.12.2: 占位符检测 — 拦截Agent模板注入（如"进入功能页面执行测试点"）
    placeholder_issues = _check_placeholder_patterns(cases, tp_index, ctx)
    if placeholder_issues:
        print(json.dumps({
            "status": "quality_rejected",
            "tp_index": tp_index,
            "reason": "占位符检测失败 — Agent未基于P6 prompt生成用例，使用了模板占位符",
            "placeholder_issues": placeholder_issues,
            "fix_hints": [{
                "action": "regenerate_from_prompt",
                "hint": "重新执行 p6_generate_one --tp-index N，阅读prompt中的11章节信息（页面路径/UI元素/业务规则/场景描述等），"
                        "基于这些具体信息生成用例。禁止使用'进入功能页面执行测试点'、'验证操作结果'等通用模板短语。"
            }],
            "retry_hint": f"重读prompt基于真实业务信息生成，然后 p6_generate_one --tp-index {tp_index} --save --agent-output '...'"
        }))
        sys.exit(1)

    # === V4.12.5: 质量预览 — 步骤过短条件阻断 ===
    short_steps = 0
    no_smoke_warn = False
    need_smoke_from_ctx = ctx.get("need_smoke", False)
    for c in cases:
        steps_text = _get_case_field(c, "steps", "")
        if isinstance(steps_text, str):
            step_count = len([s for s in steps_text.split("\n") if s.strip()])
        else:
            step_count = 0
        if step_count <= 2:
            short_steps += 1
    has_smoke = any(_is_smoke(_get_case_field(c, "is_smoke", "")) for c in cases)

    qp_warnings = []
    if short_steps > 0:
        qp_warnings.append(f"{short_steps}/{len(cases)}条用例步骤≤2步")
    if need_smoke_from_ctx and not has_smoke:
        no_smoke_warn = True
        qp_warnings.append("缺少冒烟用例(is_smoke未标记)")

    # 条件阻断：≥50%用例步骤过短 → reject
    if len(cases) > 0 and short_steps >= len(cases) / 2:
        print(json.dumps({
            "status": "quality_rejected",
            "tp_index": tp_index,
            "reason": f"质量预览不通过: {short_steps}/{len(cases)}条用例步骤≤2步",
            "quality_warnings": qp_warnings,
            "fix_hints": [{
                "action": "expand_steps",
                "hint": "每条用例至少3步详细操作。格式: '动作动词「UI元素」具体内容'（如: 点击「查询」按钮、在「员工姓名」输入框输入'张三'）"
            }],
            "retry_hint": f"重新 p6_generate_one --tp-index {tp_index} --save --agent-output '...'",
        }))
        sys.exit(1)
    # <50%但>0 → stderr警告
    if qp_warnings:
        print(json.dumps({
            "status": "quality_hint",
            "tp_index": tp_index,
            "warnings": qp_warnings,
        }), file=sys.stderr)
    # === 质量预览结束 ===

    # 保存
    out_dir = os.path.join(data_dir, "p6_tp_output")
    _ensure_dir(out_dir)
    tp_path = os.path.join(out_dir, f"tp_{tp_index:03d}.json")
    # 累计：如果已有保存，合并case（支持多次save同一TP）
    existing_cases = []
    if os.path.exists(tp_path):
        try:
            existing = _read_json(tp_path)
            existing_cases = existing.get("testcases", [])
        except Exception:
            pass
    all_cases = existing_cases + cases
    _write_json(tp_path, {"tp_index": tp_index, "tp_id": tp_id, "testcases": all_cases})
    
    # V4.12.3: 数量校验 — 比对expected_case_count
    ec = ctx.get("expected_case_count", 2)
    result = {
        "status": "ok",
        "tp_index": tp_index,
        "cases_this_save": len(cases),
        "cases_total_saved": len(all_cases),
        "expected_case_count": ec,
        "file": tp_path,
    }
    if len(all_cases) < ec:
        shortfall = ec - len(all_cases)
        result["status"] = "saved_shortfall"
        result["shortfall"] = shortfall
        result["hint"] = (
            f"⚠️ 当前TP已保存{len(all_cases)}条（{ec - shortfall}/{ec}），还需要{shortfall}条。"
            f"继续调用 p6_generate_one --tp-index {tp_index} --save 补充剩余用例。"
        )
    print(json.dumps(result))


def action_p6_tp_list(args):
    """V4.11.0: 返回P6逐条生成的TP列表(替代p6_batch_info)"""
    data_dir = args.data_dir
    task_id = args.task_id
    ok, msg = check_gate(data_dir, "P5", task_id)
    if not ok:
        print(json.dumps({"status": "gate_blocked", "reason": msg}))
        sys.exit(1)
    if _is_sub_agent_session():
        print(json.dumps({"status": "rejected", "reason": "P6禁止子Agent执行"}))
        sys.exit(1)
    p5_path = os.path.join(data_dir, "p5_output.json")
    p5 = _read_json(p5_path)
    tps = p5.get("test_points", [])
    tp_list = []
    for i, tp in enumerate(tps):
        tp_list.append({
            "index": i,
            "id": tp.get("id", ""),
            "title": tp.get("title", ""),
            "category": tp.get("category", ""),
            "priority": tp.get("priority", ""),
            "expected_case_count": tp.get("expected_case_count", 2),
            "description": tp.get("description", "")[:120],
        })
    # V4.11.0: TP质量门禁 - 检查每个TP是否独立完整
    tp_quality_warnings = 0
    for tp in tps:
        issues = []
        if not str(tp.get('title','')).strip():
            issues.append('title为空')
        if len(str(tp.get('description',''))) < 20:
            issues.append(f"description过短({len(str(tp.get('description','')))})字")
        if tp.get('category','') not in ('main_flow','branch','exception','boundary','permission',
                'risk_verification','field_validation','integration','security','state_migration','compatibility'):
            issues.append(f"category异常:{tp.get('category','')}")
        if tp.get('priority','') not in ('P0','P1','P2','P3','P4'):
            issues.append(f"priority异常:{tp.get('priority','')}")
        if issues:
            tp_quality_warnings += 1
            print(json.dumps({"status":"warning","action":"tp_quality","tp_index":i,
                "tp_id":tp.get('id',''),"issues":issues}), file=sys.stderr)
    if tp_quality_warnings:
        state = _read_json(os.path.join(data_dir, "orchestrator_state.json"))
        state["tp_quality_warnings"] = tp_quality_warnings
        _write_json(os.path.join(data_dir, "orchestrator_state.json"), state)

    mt = _get_model_tier_for_dir(data_dir)
    p3_path = os.path.join(data_dir, "p3_output.json")
    p3_risks = _read_json(p3_path).get("risk_points", []) if os.path.exists(p3_path) else []
    p4_path = os.path.join(data_dir, "p4_output.json")
    p4_pci = _read_json(p4_path).get("pci_list", []) if os.path.exists(p4_path) else []
    _write_tp_contexts(data_dir, tps, mt, p3_risks, p4_pci)
    minutes_per_tp = 0.5 if mt == "LOW" else 0.2
    print(json.dumps({
        "status": "ok",
        "tp_list": tp_list,
        "total": len(tp_list),
        "model_tier": mt,
        "estimated_minutes": round(len(tp_list) * minutes_per_tp, 1),
        "mode": "sequential",
        "next_action": f"对 tp_index=0..{len(tp_list) - 1} 逐条调用 p6_generate_one"
    }))


def action_p6_generate_one(args):
    """V4.11.0: 单TP端到端生成(替代prep_prompt P6 + save_batch)"""
    data_dir = args.data_dir
    tp_index = int(args.tp_index)
    agent_output = getattr(args, 'agent_output', '') or ''
    # 保存模式
    if agent_output:
        return _save_single_tp(data_dir, tp_index, agent_output)
    # 生成模式:输出prompt
    ctx_path = os.path.join(data_dir, "p6_tp_output", f"tp_{tp_index:03d}_context.json")
    if not os.path.exists(ctx_path):
        p5 = _read_json(os.path.join(data_dir, "p5_output.json"))
        p3_path = os.path.join(data_dir, "p3_output.json")
        p3_risks = _read_json(p3_path).get("risk_points", []) if os.path.exists(p3_path) else []
        p4_path = os.path.join(data_dir, "p4_output.json")
        p4_pci = _read_json(p4_path).get("pci_list", []) if os.path.exists(p4_path) else []
        _write_tp_contexts(data_dir, p5.get("test_points", []),
                          _get_model_tier_for_dir(data_dir), p3_risks, p4_pci)
    ctx = _read_json(ctx_path)
    prompt = _build_single_tp_prompt(ctx, ctx.get("model_tier", "LOW"))
    print(prompt)


# V4.11.0: action_p6_batch_info 已废弃,替代为 action_p6_tp_list
def action_p6_batch_info(args):
    """返回P6分批信息:总批次数、每批测试点数
    V4.7.1: 写入 batch_{N:03d}_context.json 供 Agent 按需读取(P6 prompt 分片)
    """
    data_dir = args.data_dir
    task_id = args.task_id

    # V4.7.3: 子Agent环境检测(P6必须在主会话执行,子Agent有30分钟超时)
    if _is_sub_agent_session():
        print(json.dumps({
            "status": "rejected",
            "reason": "⛔ P6禁止在子Agent(spawn)中执行!P6需要主会话的完整上下文和充足时间。请在主会话中直接运行P6流程。",
            "hint": "返回到主会话,执行: python3 $ORCH --action p6_batch_info"
        }))
        sys.exit(1)

    # V3.2.6: P5前置gate校验
    ok, msg = check_gate(data_dir, "P5", task_id)
    if not ok:
        print(json.dumps({
            "status": "gate_blocked",
            "reason": f"P6批次信息需要P5 gate pass: {msg}。必须先执行p5_code_merge完成P5。",
        }))
        sys.exit(1)

    p5_path = os.path.join(data_dir, "p5_output.json")
    if not os.path.exists(p5_path):
        print(json.dumps({"status": "error", "reason": "p5_output.json不存在"}))
        sys.exit(1)

    p5 = _read_json(p5_path)
    test_points = p5.get("test_points", [])
    total = len(test_points)
    # V4.8.4: 读取模型档位(修复:默认LOW与prep_prompt一致,state不存在时兜底检测OPENCLAW_MODEL)
    model_tier = "LOW"  # 保守策略:与prep_prompt保持一致
    recommended_batch_size = _get_model_detect().get_batch_size("LOW", total)
    state_path = os.path.join(data_dir, "orchestrator_state.json")
    model_source = "fallback_LOW"
    if os.path.exists(state_path):
        try:
            st = _read_json(state_path)
            model_tier = st.get("model_tier", "LOW")
            model_source = "state"
        except Exception:
            pass
    else:
        # State不存在:尝试从环境变量兜底检测
        env_model = os.environ.get('OPENCLAW_MODEL', '') or os.environ.get('OPENCLAW_DEFAULT_MODEL', '')
        if env_model:
            model_tier = _get_model_detect().classify(env_model)
            model_source = "env_fallback"

    if model_tier == "LOW":
        recommended_batch_size = _get_model_detect().get_batch_size("LOW", total)
    else:
        recommended_batch_size = _get_model_detect().get_batch_size("HIGH", total)

    # V4.6.17: 启用动态分批
    batch_info = calculate_dynamic_batches(test_points, max_batches=5)
    total_batches = batch_info["total_batches"]
    strategy = batch_info.get("strategy", "dynamic")

    # V4.7.1: 为每批写入 batch context 文件(Agent 按需读取,prompt 精简后从 66KB → ~20KB)
    batches_dir = os.path.join(data_dir, "p6_batches")
    _ensure_dir(batches_dir)
    context_files = []
    for b in batch_info["batches"]:
        start, end = b["start"], b["end"]
        batch_idx = len(context_files)  # V4.8.12: 0-based,与prep_prompt --batch-index一致
        chunk_tps = test_points[start:end]
        # 精简测试点数据(保留 Agent 生成用例必需字段)
        slim_tps = []
        for tp in chunk_tps:
            ops = tp.get("operations_chain", [])
            is_ops_chain = isinstance(ops, list) and len(ops) > 0
            stp = {
                "id": tp.get("id", ""),
                "title": tp.get("title", ""),
                "description": tp.get("description", ""),
                "category": tp.get("category", ""),
                "priority": tp.get("priority", ""),
                "expected_case_count": tp.get("expected_case_count", 2),
                "page_path": tp.get("page_path", ""),
                "step_expected_pairs": tp.get("step_expected_pairs", []),
                "step_expected_pairs_source": "operations_chain" if is_ops_chain else "fallback_template",
                "field_checklist": tp.get("field_checklist", []),
                "ui_elements": tp.get("ui_elements", {}),
                "risk_flag": tp.get("risk_flag", False),
                "risk_severity": tp.get("risk_severity", ""),
                "precondition": tp.get("precondition", ""),
            }
            slim_tps.append(stp)
        context = {"batch_index": batch_idx, "test_points": slim_tps, "total_in_batch": len(slim_tps)}
        ctx_path = os.path.join(batches_dir, f"batch_{batch_idx:03d}_context.json")
        _write_json(ctx_path, context)
        context_files.append(f"p6_batches/batch_{batch_idx:03d}_context.json")

    # V4.7.2: 计算预计用例分布表(按优先级和类别)
    expected_total = sum(tp.get("expected_case_count", 2) for tp in test_points)
    by_priority = {}
    by_category = {}
    for tp in test_points:
        p = tp.get("priority", "P1")
        c = tp.get("category", "unknown")
        ec = tp.get("expected_case_count", 2)
        by_priority[p] = by_priority.get(p, 0) + ec
        by_category[c] = by_category.get(c, 0) + ec

    # V4.8.7: 明确计算LOW模型执行批次数,避免Agent混淆complexity批次和执行批次
    import math
    total_execution_batches = math.ceil(total / recommended_batch_size) if recommended_batch_size > 0 else math.ceil(total / 5)
    # V4.8.8: 估算执行时间(LOW模型每批约1.5分钟,HIGH约0.5分钟)
    minutes_per_batch = 1.5 if model_tier == "LOW" else 0.5
    estimated_minutes = round(total_execution_batches * minutes_per_batch, 1)

    print(json.dumps({
        "status": "ok",
        "total_test_points": total,
        "total_execution_batches": total_execution_batches,
        "recommended_batch_size": recommended_batch_size,
        "estimated_minutes": estimated_minutes,
        "model_tier": model_tier,
        "model_source": model_source,
        "complexity_groups": total_batches,
        "strategy": strategy,
        "batches": batch_info["batches"],
        "context_files": context_files,
        "execution_hint": f"🔴🔴 必须循环执行 {total_execution_batches} 批(batch-index从0到{total_execution_batches-1})!预计耗时{estimated_minutes}分钟。complexity_groups({total_batches})仅用于展示复杂度分布,不是执行批次数。以 total_execution_batches 为准,全部跑完后再 p6_merge。",
        "model_aware_hint": f"🔴 当前模型档位={model_tier}(来源:{model_source}),prep_prompt 每次只生成 {recommended_batch_size} 个测试点!不要期待 25 个!p6_batch_info 的批次划分仅基于复杂度(不受模型影响),实际循环 prep_prompt 时请按 recommended_batch_size 计算批次数。",
        "expected_distribution": {
            "total_expected_cases": expected_total,
            "by_priority": by_priority,
            "by_category": by_category,
            "hint": f"预计共{expected_total}条用例(非硬性门槛,按复杂度可增减)。优先保证每个测试点至少展开到 expected_case_count 条。"
        },
        "auto_downgrade_estimation": {
            "p0_tp_count": sum(1 for tp in test_points if tp.get("priority") == "P0"),
            "p1_tp_count": sum(1 for tp in test_points if tp.get("priority") == "P1"),
            "p0_skeleton_ratio": round(sum(1 for tp in test_points if tp.get("priority") == "P0") / expected_total, 3) if expected_total > 0 else 0,
            "threshold_p0": 0.35,
            "threshold_smoke": 0.30,
            "hint": "🔴 P0测试点占比过高(P2给每feature第1个main_flow升P0导致)。骨架生成阶段会自动降级超标批次(P0>35%或smoke>30%),Agent无需手动调整优先级。预期降级后P0比例≤35%。"
        },
    }))


# ============================================================
# V4.8.10: 占位符质量检测 - 标记不拒绝
# ============================================================

def _check_placeholder_quality(cases: list) -> dict:
    """检测用例中的占位符/空洞内容,标记到remarks,不拒绝保存。"""
    import re

    # 标题占位符模式
    TITLE_PLACEHOLDER_PATTERNS = [
        (r'^测试用例[-_\s]*(TP-\d+|\d+)[-_\s]*\d*$', '占位符标题'),
        (r'^用例\d*$', '占位符标题'),
        (r'^[Tt]est\s*[Cc]ase[-_\s]*\d+$', '占位符标题'),
    ]

    # 步骤空洞模式
    STEP_HOLLOW_PATTERNS = [
        r'^\d*[.、)]?\s*(执行|进行|完成|操作|验证|检查|查看|确认)\s*(相关|对应|相应|指定|该|所有|各项)?\s*(操作|内容|步骤|功能|动作|流程|数据|结果|信息|页面)?\s*$',
    ]

    # 期望空洞模式
    EXPECTED_HOLLOW_PATTERNS = [
        r'^\d*[.、)]?\s*(操作|执行|验证|数据|结果|页面|功能|跳转|显示|保存|提交|登录|导出|导入|查询|搜索|删除|新增|修改|编辑)?\s*(成功|完成|正常|正确|无误|通过|ok|OK)?\s*$',
    ]

    warnings = {
        "total_checked": len(cases),
        "title_placeholder": [],
        "step_short": [],
        "step_hollow": [],
        "expected_hollow": [],
        "total_tagged": 0,
    }

    tagged_ids = set()
    for ci, c in enumerate(cases):
        if not isinstance(c, dict):
            continue
        cid = c.get("case_id", f"idx_{ci}")
        tags = []

        # 标题检测
        title = str(c.get("title", "")).strip()
        for pattern, label in TITLE_PLACEHOLDER_PATTERNS:
            if re.match(pattern, title, re.IGNORECASE):
                tags.append(f'[{label}]')
                warnings["title_placeholder"].append(f"{cid}: {title[:40]}")
                break

        # 步骤检测
        steps_text = str(c.get("steps", "")).strip()
        if steps_text:
            steps_lines = [s.strip() for s in steps_text.split('\n') if s.strip()]
            for sl in steps_lines:
                # 去除编号后检测
                cleaned = re.sub(r'^\d+[.、)]?\s*', '', sl)
                if len(cleaned) < 15:
                    if "step_short" not in [t for t in tags if "步骤" in t]:
                        tags.append('[步骤过短<15字]')
                        warnings["step_short"].append(f"{cid}: {cleaned[:40]}")
                for pattern in STEP_HOLLOW_PATTERNS:
                    if re.match(pattern, sl, re.IGNORECASE):
                        if "步骤空洞" not in [t for t in tags if "步骤空洞" in t]:
                            tags.append('[步骤空洞]')
                            warnings["step_hollow"].append(f"{cid}: {cleaned[:40]}")
                        break

        # 期望检测
        exp_text = str(c.get("expected_results", "")).strip()
        if exp_text:
            exp_lines = [e.strip() for e in exp_text.split('\n') if e.strip()]
            for el in exp_lines:
                cleaned = re.sub(r'^\d+[.、)]?\s*', '', el)
                for pattern in EXPECTED_HOLLOW_PATTERNS:
                    if re.match(pattern, cleaned, re.IGNORECASE):
                        if "期望空洞" not in [t for t in tags if "期望空洞" in t]:
                            tags.append('[期望空洞]')
                            warnings["expected_hollow"].append(f"{cid}: {cleaned[:40]}")
                        break

        # 标记到 remarks
        if tags:
            tagged_ids.add(cid)
            existing = str(c.get("remarks", "")).strip()
            tag_str = ' '.join(tags)
            if tag_str not in existing:
                c["remarks"] = f"{existing} {tag_str}".strip() if existing else tag_str

    warnings["total_tagged"] = len(tagged_ids)
    return warnings if tagged_ids else {}


# ============================================================
# V4.8.3: LOW模型后处理工具函数
# ============================================================

def _check_terminology_consistency(cases: list) -> list:
    """V4.8.3: 术语一致性检测(纯代码,零token)。

    提取所有用例步骤中的 [动作动词+「UI元素」] 对,
    对编辑距离<3的对做聚类,标记不一致的用例。

    Returns:
        [{"canonical": 规范用语, "variants": [变体列表], "suggestion": 统一建议, "affected_case_indices": [受影响的用例索引]}]
    """
    import difflib

    # 1. 提取所有 [动作动词+UI元素] 对
    action_pairs = []  # [(case_index, step_index, verb, element)]
    for ci, c in enumerate(cases):
        steps_str = _get_case_field(c, "steps", "")
        if not isinstance(steps_str, str):
            continue
        if not steps_str:
            continue
        # 匹配: 动作动词「UI元素」
        pairs = re.findall(
            r'(点击|输入|选择|删除|勾选|上传|下载|拖拽|切换|打开|关闭|填写|修改|清空|提交|保存|确认|取消)'
            r'[「「]?([^」」]{1,15})[」」]?',
            steps_str
        )
        for si, (verb, element) in enumerate(pairs):
            element = element.strip()
            if element:
                action_pairs.append((ci, si, verb, element))

    if len(action_pairs) < 3:
        return []

    # 2. 按 verb 分组,在每个组内做聚类
    from collections import defaultdict
    by_verb = defaultdict(list)
    for ci, si, verb, element in action_pairs:
        by_verb[verb].append((ci, si, element))

    issues = []
    for verb, group in by_verb.items():
        if len(group) < 3:
            continue

        # 提取唯一的 element 名称
        unique_elements = list(set(e for _, _, e in group))
        if len(unique_elements) < 2:
            continue

        # 对 element 做编辑距离聚类
        clusters = {}
        processed = set()
        for i, e1 in enumerate(unique_elements):
            if e1 in processed:
                continue
            cluster = [e1]
            for e2 in unique_elements[i+1:]:
                if e2 in processed:
                    continue
                # 编辑距离 < 3 且至少3字 → 视为变体
                ratio = difflib.SequenceMatcher(None, e1, e2).ratio()
                if ratio > 0.6 and max(len(e1), len(e2)) >= 2:
                    cluster.append(e2)
                    processed.add(e2)
            if len(cluster) >= 2:
                clusters[e1] = cluster
                processed.add(e1)

        for canonical, variants in clusters.items():
            if len(variants) <= 1:
                continue
            # 取最长的为规范用语
            best = max(variants, key=len)
            # 找出受影响的用例
            affected = []
            for ci, si, e in group:
                if e in variants and e != best:
                    if ci not in affected:
                        affected.append(ci)
            if affected:
                other_variants = [v for v in variants if v != best]
                issues.append({
                    "verb": verb,
                    "canonical": f"{verb}「{best}」",
                    "variants": [f"{verb}「{v}」" for v in other_variants],
                    "suggestion": f"统一为 {verb}「{best}」",
                    "affected_case_indices": affected[:10],
                })

    return issues[:10]  # 最多10个问题


def _dedup_preconditions(cases: list) -> dict:
    """V4.8.3: 前置条件去重(纯代码,零token)。

    按模块分组,提取 ≥50% 用例共享的 precondition → 写入公共前置。

    Returns:
        {"extracted_count": 提取条数, "reduced_count": 减少的重复次数, "details": [...]}
    """
    if len(cases) < 3:
        return {"extracted_count": 0, "reduced_count": 0}

    # 1. 按模块分组(从 case_id 提取模块前缀,或从 test_suite/menu_path)
    from collections import Counter
    modules = {}
    for ci, c in enumerate(cases):
        cid = _get_case_field(c, "case_id", "")
        # 从 case_id 提取模块前缀: TC-XG-RZ-xxx → XG-RZ
        mod = "default"
        match = re.match(r'TC-([A-Z]+(?:-[A-Z]+)?)', cid)
        if match:
            mod = match.group(1)
        else:
            # fallback: test_suite 或 menu_path
            ts = _get_case_field(c, "test_suite", "") or _get_case_field(c, "menu_path", "")
            if ts:
                mod = ts.split("→")[0].strip()[:20]
        if mod not in modules:
            modules[mod] = []
        modules[mod].append(ci)

    # 2. 对每个模块提取公共 precondition
    total_extracted = 0
    total_reduced = 0
    details = []

    for mod_name, indices in modules.items():
        if len(indices) < 3:
            continue

        # 收集该模块所有用例的 precondition
        preconds = []
        for ci in indices:
            pc = _get_case_field(cases[ci], "preconditions", "")
            if not isinstance(pc, str):
                continue
            if pc:
                preconds.append(pc)

        if len(preconds) < 3:
            continue

        # 解析每行 precondition,统计每行出现次数
        line_counter = Counter()
        for pc in preconds:
            for line in pc.split("\n"):
                line = line.strip()
                if not line:
                    continue
                # 去序号 "1. " 或 "1、"
                line = re.sub(r'^\d+[.、]\\s*', '', line)
                if len(line) >= 5:
                    line_counter[line] += 1

        # 提取 ≥50% 用例共享的行
        threshold = max(2, len(preconds) // 2)
        common_lines = [line for line, count in line_counter.items() if count >= threshold]

        if not common_lines:
            continue

        # 3. 从个体用例中删除公共行,添加到模块公共 precondition
        common_text = "\n".join(f"{i}. {line}" for i, line in enumerate(common_lines, 1))
        reduced = 0
        for ci in indices:
            pc = _get_case_field(cases[ci], "preconditions", "")
            if not pc:
                continue
            lines = pc.split("\n")
            new_lines = []
            for line in lines:
                stripped = re.sub(r'^\d+[.、]\\s*', '', line.strip())
                if stripped not in common_lines:
                    new_lines.append(line)
                else:
                    reduced += 1
            if len(new_lines) < len(lines):
                # 在前面加模块公共前置引用
                mod_ref = f"0. [模块公共前置] {mod_name}: {', '.join(common_lines[:3])}"
                new_pc = mod_ref + "\n" + "\n".join(new_lines)
                # 更新用例
                if "fields" in cases[ci] and isinstance(cases[ci].get("fields"), dict):
                    cases[ci]["fields"]["preconditions"] = new_pc
                else:
                    cases[ci]["preconditions"] = new_pc

        total_extracted += len(common_lines)
        total_reduced += reduced
        details.append({
            "module": mod_name,
            "extracted_lines": common_lines,
            "reduced_count": reduced,
        })

    return {
        "extracted_count": total_extracted,
        "reduced_count": total_reduced,
        "details": details[:10],
    }


def action_p6_checkpoint(args):
    """V4.12.5: P6分批回顾检查点 — 检查已完成TP的质量"""
    data_dir = args.data_dir
    tp_dir = os.path.join(data_dir, "p6_tp_output")

    # 收集已完成TP
    tp_files = sorted(glob.glob(os.path.join(tp_dir, "tp_[0-9]*.json")))
    tp_files = [f for f in tp_files if "_context" not in os.path.basename(f)]

    if not tp_files:
        print(json.dumps({"status": "info", "completed": 0, "hint": "尚未完成任何TP"}))
        return

    # 统计每个已完成TP的用例
    summary = []
    total_cases = 0
    total_short = 0
    total_no_smoke = 0
    issues = []

    for tf in tp_files:
        try:
            tp_data = _read_json(tf)
            cases = tp_data.get("testcases", [])
            tp_index = tp_data.get("tp_index", 0)
            tp_id = tp_data.get("tp_id", "?")

            short_count = 0
            has_smoke = False
            for c in cases:
                steps_text = _get_case_field(c, "steps", "")
                if isinstance(steps_text, str):
                    step_count = len([s for s in steps_text.split("\n") if s.strip()])
                else:
                    step_count = 0
                if step_count <= 2:
                    short_count += 1
                if _is_smoke(_get_case_field(c, "is_smoke", "")):
                    has_smoke = True

            ctx_path = os.path.join(tp_dir, f"tp_{tp_index:03d}_context.json")
            need_smoke = False
            if os.path.exists(ctx_path):
                try:
                    ctx = _read_json(ctx_path)
                    need_smoke = ctx.get("need_smoke", False)
                except Exception:
                    pass

            total_cases += len(cases)
            total_short += short_count
            tp_issues = []
            if short_count >= 1:
                tp_issues.append(f"{short_count}条过短")
            if need_smoke and not has_smoke:
                total_no_smoke += 1
                tp_issues.append("缺冒烟")

            summary.append({
                "tp_index": tp_index,
                "tp_id": tp_id,
                "cases": len(cases),
                "short_steps": short_count,
                "issues": tp_issues,
                "ok": len(tp_issues) == 0,
            })
            if tp_issues:
                issues.append(f"{tp_id}: {', '.join(tp_issues)}")
        except Exception as e:
            summary.append({"tp_index": -1, "error": str(e)})

    problem_count = sum(1 for s in summary if not s.get("ok", False))
    total_tp = len(summary)
    need_fix = problem_count > total_tp / 2

    result = {
        "status": "needs_fix" if need_fix else "ok",
        "completed_tps": total_tp,
        "total_cases": total_cases,
        "problem_tps": problem_count,
        "short_step_cases": total_short,
        "missing_smoke_tps": total_no_smoke,
        "issues": issues[:8],
        "summary": summary,
    }

    if need_fix:
        result["hint"] = (
            f"⚠️ {problem_count}/{total_tp}个TP存在问题，请修复后再继续。"
        )
    else:
        result["hint"] = f"✅ {total_tp}个TP质量检查通过，可以继续生成下一批"

    print(json.dumps(result))
    if need_fix:
        sys.exit(1)


def action_p6_merge(args):
    """合并P6所有批次结果,写入p6_output.tmp.json,调用truncation_guard"""
    data_dir = args.data_dir
    task_id = args.task_id
    skill_dir = args.skill_dir

    # V4.7.3: 子Agent环境检测(P6必须在主会话执行,子Agent有30分钟超时)
    if _is_sub_agent_session():
        print(json.dumps({
            "status": "rejected",
            "reason": "⛔ P6禁止在子Agent(spawn)中执行!P6需要主会话的完整上下文和充足时间。请在主会话中直接运行P6流程。",
            "hint": "返回到主会话,执行: python3 $ORCH --action p6_merge"
        }))
        sys.exit(1)

    # V3.2.6: P5前置gate校验(防止Agent伪造batch后借刀签名)
    ok, msg = check_gate(data_dir, "P5", task_id)
    if not ok:
        print(json.dumps({
            "status": "gate_blocked",
            "reason": f"P6合并需要P5 gate pass: {msg}。必须先执行p5_code_merge完成P5。",
        }))
        sys.exit(1)

    # V4.11.0: 优先读逐条TP格式(p6_tp_output/tp_*.json),兼容旧批量格式
    all_cases = []
    tp_dir = os.path.join(data_dir, "p6_tp_output")
    tp_files = sorted(glob.glob(os.path.join(tp_dir, "tp_[0-9]*.json")))
    tp_files = [tf for tf in tp_files if "_context" not in os.path.basename(tf)]

    if tp_files:
        for tf in tp_files:
            tp_data = _read_json(tf)
            if isinstance(tp_data, list):
                tp_data = {"testcases": tp_data}
            all_cases.extend(tp_data.get("testcases", []))
        print(json.dumps({"status":"info","mode":"sequential",
            "tp_files":len(tp_files),"cases":len(all_cases)}), file=sys.stderr)
    else:
        batches_dir = os.path.join(data_dir, "p6_batches")
        if not os.path.exists(batches_dir):
            print(json.dumps({"status":"error","reason":"p6_batches目录不存在"}))
            sys.exit(1)
        batch_files = sorted(glob.glob(os.path.join(batches_dir, "batch_[0-9]*.json")))
        batch_files = [bf for bf in batch_files if "_output" not in os.path.basename(bf) and "_agent_output" not in os.path.basename(bf)]

    # V4.7.2: 合并前校验各批次状态(仅旧批量格式)
    batch_status = []
    empty_batches = []
    if not tp_files:
        for bf in batch_files:
            try:
                bd = _read_json(bf)
                bcases = bd.get("testcases", bd.get("cases", []))
                batch_status.append({
                    "file": os.path.basename(bf),
                    "cases": len(bcases),
                    "empty": len(bcases) == 0,
                })
                if len(bcases) == 0:
                    empty_batches.append(os.path.basename(bf))
                all_cases.extend(bcases)
            except Exception as e:
                print(json.dumps({"status": "warning", "reason": f"批次文件读取失败: {bf}: {e}"}), file=sys.stderr)
                empty_batches.append(os.path.basename(bf))

    if empty_batches:
        print(json.dumps({
            "status": "info",
            "empty_batches": empty_batches,
            "hint": f"{len(empty_batches)}个批次为空或读取失败,请检查Agent输出后重新执行该批次的p6_save_batch",
        }), file=sys.stderr)

    if not all_cases:
        print(json.dumps({"status": "error", "reason": "所有批次合并后用例数为0", "batch_status": batch_status if not tp_files else [], "hint": "请检查各批次是否存在非空用例数据。如有空批次,用p6_save_batch重新保存对应批次。"}))
        sys.exit(1)

    # V4.7.0: p6_merge 自动去重(保留首次出现,丢弃后续同名 case_id)
    seen_ids = set()
    deduped_cases = []
    dup_count = 0
    for c in all_cases:
        cid = _get_case_field(c, "case_id", "")
        if cid and cid in seen_ids:
            dup_count += 1
            continue
        if cid:
            seen_ids.add(cid)
        deduped_cases.append(c)
    if dup_count > 0:
        print(json.dumps({"status": "info", "dedup_removed": dup_count, "before": len(all_cases), "after": len(deduped_cases)}), file=sys.stderr)
    all_cases = deduped_cases

    if not all_cases:
        print(json.dumps({"status": "error", "reason": "去重后所有用例被移除", "dedup_removed": dup_count, "hint": "所有case_id均为重复,请检查是否同一批次被多次保存或Agent重复生成了相同用例"}))
        sys.exit(1)

    # V4.7.3: 防御性补全 source_test_point - 从各批次skeleton回填缺失字段
    # 场景:Agent用Python脚本绕过p6_save_batch生成用例时,source_test_point未被填充
    missing_stp = 0
    for c in all_cases:
        if not _get_case_field(c, "source_test_point", ""):
            cid = _get_case_field(c, "case_id", "")
            # 尝试从case_id反推(格式: TC-XXX-YYY-ZZZ 或 TP-XXX-TC-YYY)
            if cid and "-TC-" in cid:
                c["source_test_point"] = cid.rsplit("-TC-", 1)[0]
                missing_stp += 1
    if missing_stp > 0:
        print(json.dumps({"status": "info", "source_test_point_backfill": missing_stp, "hint": f"{missing_stp}条用例缺少source_test_point,已从case_id反推补全"}), file=sys.stderr)

    # 统计(V3.2.4: 使用_get_case_field兼容fields嵌套结构)
    p0_count = sum(1 for c in all_cases if _get_case_field(c, "priority", "").upper() in ("P0", "HIGHEST"))
    smoke_count = sum(1 for c in all_cases if _is_smoke(_get_case_field(c, "is_smoke", "")))

    # 按优先级统计
    by_priority = {}
    for c in all_cases:
        p = _get_case_field(c, "priority", "unknown").upper()
        by_priority[p] = by_priority.get(p, 0) + 1

    merged = {
        "testcases": all_cases,
        "statistics": {
            "total": len(all_cases),
            "by_priority": by_priority,
            "smoke_count": smoke_count,
            "p0_count": p0_count,
            "batch_count": len(batch_files) if not tp_files else len(tp_files),
        }
    }

    # V3.2.9: 全局硬校验(代码层硬控,不依赖Agent)
    merge_issues = []
    p5_path = os.path.join(data_dir, "p5_output.json")
    if os.path.exists(p5_path):
        try:
            p5_data = _read_json(p5_path)
            p5_points = p5_data.get("test_points", [])
            p5_ids = set(tp.get("id", "") for tp in p5_points if tp.get("id"))
            total_expected = p5_data.get("coverage_summary", {}).get("total_expected_cases", 0)

            # 校验1:总用例数≥总预算
            if total_expected > 0 and len(all_cases) < total_expected:
                merge_issues.append(f"用例总数{len(all_cases)}<预算{total_expected}")

            # 校验2:逐测试点展开数达标
            tp_actual = {}
            covered_ids = set()
            for c in all_cases:
                src = _get_case_field(c, "source_test_point", "")
                if not src:
                    cid = _get_case_field(c, "case_id", "")
                    if cid and "-TC-" in cid:
                        src = cid.rsplit("-TC-", 1)[0]
                if src:
                    tp_actual[src] = tp_actual.get(src, 0) + 1
                    covered_ids.add(src)

            shortfall_points = []
            shortfall_hints = []  # V4.12.3: 可执行的补缺命令
            for tp in p5_points:
                tp_id = tp.get("id", "")
                expected = tp.get("expected_case_count", 2)
                actual = tp_actual.get(tp_id, 0)
                if actual < expected:
                    shortfall_points.append(f"{tp_id}:应{expected}实{actual}")
                    # 从tp_id提取tp_index（TP-NNN → NNN-1）
                    try:
                        tp_num = int(tp_id.split("-")[-1]) if "-" in tp_id else 0
                        tp_idx = tp_num - 1
                        shortfall_hints.append(
                            f"python3 $ORCH --action p6_generate_one --tp-index {tp_idx} --save --agent-output '...'"
                            f"  # {tp_id}还需{expected - actual}条"
                        )
                    except Exception:
                        pass
            if shortfall_points:
                merge_issues.append(f"{len(shortfall_points)}个测试点展开不足: {', '.join(shortfall_points[:5])}")

            # 校验3:未覆盖的测试点
            uncovered = p5_ids - covered_ids
            if uncovered:
                merge_issues.append(f"{len(uncovered)}个测试点未覆盖: {', '.join(sorted(uncovered)[:5])}")

            # 写入覆盖统计
            merged["statistics"]["p5_coverage"] = {
                "total_p5": len(p5_ids),
                "covered": len(covered_ids),
                "uncovered": sorted(uncovered) if uncovered else [],
                "shortfall_points": shortfall_points[:10] if shortfall_points else [],
                "shortfall_hints": shortfall_hints[:10] if shortfall_hints else [],  # V4.12.3
            }
        except Exception:
            pass

    # V3.3.1: 全局底线校验(精确比例校验已移至P7 code_check)
    # 校验4:全局smoke>0(底线,避免全局smoke=0的极端情况)
    if len(all_cases) > 0:
        if smoke_count == 0:
            merge_issues.append("全局冒烟用例为0,必须有核心主链路的冒烟用例")

    # 校验5:全局P0>0(底线)
    if len(all_cases) > 0:
        if p0_count == 0:
            merge_issues.append("全局P0用例为0,必须有核心主链路的P0用例")
    # V4.8.7: LOW模型p6_merge失败 → 不阻断,接受当前用例(模型能力有限,重启无法达标)
    # V4.8.9: stdout+stderr双通道输出,确保Agent能看到
    mt = _get_model_tier_for_dir(data_dir)
    if merge_issues:
        if mt == "LOW":
            accepted_msg = {
                "status": "quality_accepted_low",
                "total_cases": len(all_cases),
                "issues": merge_issues,
                "message": f"⚠️ LOW模型用例数未达期望,已接受当前{len(all_cases)}条用例(所有单批质量门均已通过)。进入P7+Excel导出,不阻塞流程。",
                "hint": "LOW模型能力有限,不restart P6,直接进入段落6的P7+Excel导出",
                "next_action": "继续执行 p7_code_check + step7_export"
            }
            print(json.dumps(accepted_msg), file=sys.stderr)
            # V4.8.9: 同时输出到 stdout,确保 Agent 不会因看不到 stderr 而误判失败
            print(json.dumps(accepted_msg))
            _invalidate_batch_cache()  # V4.9.1: batch已修改,清除索引缓存
        else:
            print(json.dumps({
                "status": "quality_rejected",
                "issues": merge_issues,
                "retry_hint": "全局质量校验未通过,请重新执行P6分批流程",
            }))
            sys.exit(1)

    # 写入tmp
    tmp_path = os.path.join(data_dir, "p6_output.tmp.json")

    # V4.8.3: LOW模型后处理 - 术语一致性 + 前置条件去重(仅LOW触发)
    post_process_report = {}
    model_tier = "HIGH"
    state_path = os.path.join(data_dir, "orchestrator_state.json")
    if os.path.exists(state_path):
        try:
            st = _read_json(state_path)
            model_tier = st.get("model_tier", "HIGH")
        except Exception:
            pass

    if model_tier == "LOW" and all_cases:
        # 术语一致性检测
        term_issues = _check_terminology_consistency(all_cases)
        if term_issues:
            for issue in term_issues:
                # 标记到受影响用例的remarks
                for ci in issue.get("affected_case_indices", []):
                    if ci < len(all_cases):
                        c = all_cases[ci]
                        existing = _get_case_field(c, "remarks", "")
                        tag = f"[术语不一致: {issue.get('suggestion', '')}]"
                        if tag not in str(existing):
                            # 处理 nested fields 结构
                            if "fields" in c and isinstance(c.get("fields"), dict):
                                c["fields"]["remarks"] = (str(existing) + " " + tag).strip() if existing else tag
                            else:
                                c["remarks"] = (str(existing) + " " + tag).strip() if existing else tag
            post_process_report["terminology"] = {
                "clusters_found": len(term_issues),
                "details": [{"canonical": i.get("canonical", ""), "variants": i.get("variants", []), "suggestion": i.get("suggestion", "")} for i in term_issues]
            }

        # 前置条件去重
        dedup_info = _dedup_preconditions(all_cases)
        if dedup_info.get("extracted_count", 0) > 0:
            post_process_report["precondition_dedup"] = dedup_info

        # V4.8.4: 烟雾比例自动纠正(<10% → 自动标记P0用例为烟雾)
        if len(all_cases) > 0:
            smoke_count_current = sum(1 for c in all_cases if _is_smoke(_get_case_field(c, "is_smoke", "")))
            smoke_ratio = smoke_count_current / len(all_cases)
            min_smoke = max(1, int(len(all_cases) * 0.10))  # 至少10%或1条
            if smoke_count_current < min_smoke:
                # 按优先级排序:P0 > P1 > P2,选top-priority用例标记为烟雾
                priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
                sorted_cases = sorted(
                    enumerate(all_cases),
                    key=lambda x: priority_order.get(_get_case_field(x[1], "priority", "P2").upper(), 99)
                )
                auto_marked = 0
                for ci, c in sorted_cases:
                    if _is_smoke(_get_case_field(c, "is_smoke", "")):
                        continue
                    cat = _get_case_field(c, "test_category", "") or _get_case_field(c, "category", "")
                    # 只标记main_flow/正向验证类用例为烟雾
                    if cat and cat not in ("main_flow", "正向", "功能", ""):
                        continue
                    # 标记为烟雾
                    if "fields" in c and isinstance(c.get("fields"), dict):
                        c["fields"]["is_smoke"] = True
                    else:
                        c["is_smoke"] = True
                    auto_marked += 1
                    if smoke_count_current + auto_marked >= min_smoke:
                        break
                if auto_marked > 0:
                    post_process_report["smoke_auto_fix"] = {
                        "before_count": smoke_count_current,
                        "before_ratio": f"{smoke_ratio:.1%}",
                        "auto_marked": auto_marked,
                        "after_count": smoke_count_current + auto_marked,
                        "after_ratio": f"{(smoke_count_current + auto_marked) / len(all_cases):.1%}",
                    }

        # 写入后处理报告供Agent查阅
        if post_process_report:
            report_path = os.path.join(data_dir, "p6_post_process.json")
            _write_json(report_path, {
                "model_tier": model_tier,
                "version": "4.8.3",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                **post_process_report
            })
            print(json.dumps({"status": "info", "post_process": "LOW模型后处理完成", "report": report_path}), file=sys.stderr)

    # === V4.12.6: 比率自动调平 ===
    if all_cases:
        total = len(all_cases)
        p0_cases = [c for c in all_cases if _get_case_field(c, "priority", "").upper() == "P0"]
        smoke_cases = [c for c in all_cases if _is_smoke(_get_case_field(c, "is_smoke", ""))]
        p0_ratio = len(p0_cases) / total
        smoke_ratio = len(smoke_cases) / total
        adjustments = []

        # 冒烟超20% → 降级多余的P0冒烟为非冒烟P1
        if smoke_ratio > 0.20:
            target_smoke = int(total * 0.18)  # 降到18%留缓冲
            excess = len(smoke_cases) - target_smoke
            # 优先降非主流程的冒烟用例
            downgraded = 0
            for c in smoke_cases:
                if downgraded >= excess:
                    break
                cat = _get_case_field(c, "test_category", _get_case_field(c, "category", ""))
                if cat not in ("main_flow", "正向"):
                    _set_case_field(c, "priority", "P1")
                    _set_case_field(c, "is_smoke", False)
                    downgraded += 1
                    adjustments.append(f"冒烟→P1非冒烟: {_get_case_field(c, 'case_id', '?')}")
            # 如果还不够，降主流程的冒烟
            for c in smoke_cases:
                if downgraded >= excess:
                    break
                _set_case_field(c, "is_smoke", False)
                downgraded += 1
                adjustments.append(f"取消冒烟: {_get_case_field(c, 'case_id', '?')}")

        # 重新计算P0（冒烟降级可能影响P0数量）
        p0_cases_now = [c for c in all_cases if _get_case_field(c, "priority", "").upper() == "P0"]
        p0_ratio_now = len(p0_cases_now) / total

        # P0超20% → 降级多余非冒烟P0为P1
        if p0_ratio_now > 0.20:
            target_p0 = int(total * 0.18)
            excess_p0 = len(p0_cases_now) - target_p0
            downgraded_p0 = 0
            for c in all_cases:
                if downgraded_p0 >= excess_p0:
                    break
                if _get_case_field(c, "priority", "").upper() == "P0" and not _is_smoke(_get_case_field(c, "is_smoke", "")):
                    _set_case_field(c, "priority", "P1")
                    downgraded_p0 += 1
                    adjustments.append(f"P0→P1: {_get_case_field(c, 'case_id', '?')}")

        if adjustments:
            # 更新统计
            merged["testcases"] = all_cases
            merged["statistics"]["smoke_count"] = sum(1 for c in all_cases if _is_smoke(_get_case_field(c, "is_smoke", "")))
            merged["statistics"]["p0_count"] = sum(1 for c in all_cases if _get_case_field(c, "priority", "").upper() == "P0")
            by_p_new = {}
            for c in all_cases:
                p = _get_case_field(c, "priority", "unknown").upper()
                by_p_new[p] = by_p_new.get(p, 0) + 1
            merged["statistics"]["by_priority"] = by_p_new
            print(json.dumps({
                "status": "info",
                "action": "ratio_auto_balance",
                "adjustments": adjustments[:10],
                "total_adjusted": len(adjustments),
                "after_smoke_ratio": f"{merged['statistics']['smoke_count'] / total:.1%}",
                "after_p0_ratio": f"{merged['statistics']['p0_count'] / total:.1%}",
            }), file=sys.stderr)
    # === 比率调平结束 ===

    _write_json(tmp_path, merged)

    # truncation_guard
    ok, msg = run_truncation_guard(skill_dir, data_dir, task_id, "P6")

    if ok:
        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete("P6")
        print(json.dumps({
            "status": "ok",
            "total_cases": len(all_cases),
            "smoke_count": smoke_count,
            "batches_merged": len(batch_files) if not tp_files else len(tp_files),
            "guard_result": msg,
            "quality_check": "V3.3.1_global_hard_pass",
        }))
    else:
        print(json.dumps({"status": "guard_failed", "reason": msg}))
        sys.exit(1)


# ============================================================
# Action: p6_save_batch (保存P6单批结果)
# ============================================================

def action_p6_save_batch(args):
    """保存P6单批结果到p6_batches/batch_N.json"""
    data_dir = args.data_dir
    task_id = args.task_id
    batch_index = int(args.batch_index) if args.batch_index else 0  # V4.8.12: 默认0-based
    agent_output = args.agent_output

    # V4.7.3: 子Agent环境检测(P6必须在主会话执行,子Agent有30分钟超时)
    if _is_sub_agent_session():
        print(json.dumps({
            "status": "rejected",
            "reason": "⛔ P6禁止在子Agent(spawn)中执行!P6需要主会话的完整上下文和充足时间。请在主会话中直接运行P6流程。",
            "hint": "返回到主会话,执行: python3 $ORCH --action p6_save_batch --batch-index N"
        }))
        sys.exit(1)

    # V3.2.6: P5前置gate校验(防止Agent在无合法P5时伪造batch)
    ok, msg = check_gate(data_dir, "P5", task_id)
    if not ok:
        print(json.dumps({
            "status": "gate_blocked",
            "reason": f"P6保存批次需要P5 gate pass: {msg}。必须先执行p5_code_merge完成P5。",
        }))
        sys.exit(1)

    expected_file = os.path.join(data_dir, f"p6_batch_{batch_index:03d}_agent_output.json")
    try:
        batch_data = json.loads(agent_output)
    except Exception:
        import re
        match = re.search(r'\{[\s\S]*\}', agent_output)
        if match:
            try:
                batch_data = json.loads(match.group())
            except Exception:
                print(json.dumps({"status": "error", "reason": f"P6批次JSON解析失败。请检查 {expected_file} 内容是否为合法JSON,或使用 --agent-output 参数直接传递JSON字符串", "expected_file": expected_file, "fix_hint": f"将生成的JSON保存到 {expected_file}(注意_agent_output后缀不能少)"}))
                sys.exit(1)
        else:
            print(json.dumps({"status": "error", "reason": f"P6批次输出不含JSON。预期文件: {expected_file}。请确认: 1)文件名含_agent_output后缀 2)文件内容为完整JSON 3)或使用--agent-output参数直接传递JSON", "expected_file": expected_file, "fix_hint": f"将生成的JSON保存到 {expected_file}(注意_agent_output后缀不能少)"}))
            sys.exit(1)

    # V4.8.9: 裸数组自动包装 - Agent 可能输出 [] 而非 {"testcases": [...]}
    if isinstance(batch_data, list):
        print(json.dumps({"status": "info", "reason": f"检测到裸数组格式[{len(batch_data)}条],已自动包装为{{\"testcases\":[...]}},请下次使用正确格式"}), file=sys.stderr)
        batch_data = {"testcases": batch_data}

    batches_dir = os.path.join(data_dir, "p6_batches")
    _ensure_dir(batches_dir)

    batch_path = os.path.join(batches_dir, f"batch_{batch_index:03d}.json")

    # V4.7.2: --merge 增量更新模式 - 只更新指定case_id,保留其余用例
    if getattr(args, 'merge', False):
        if not os.path.exists(batch_path):
            print(json.dumps({"status": "error", "reason": f"merge模式要求batch_{batch_index:03d}.json已存在,但文件不存在"}))
            sys.exit(1)
        existing = _read_json(batch_path)
        existing_cases = existing.get("testcases", existing.get("cases", []))
        new_cases = batch_data.get("testcases", batch_data.get("cases", []))
        # 按 case_id 索引合并
        new_ids = {_get_case_field(c, "case_id", "") for c in new_cases if _get_case_field(c, "case_id", "")}
        merged_cases = [c for c in existing_cases if _get_case_field(c, "case_id", "") not in new_ids]
        merged_cases.extend(new_cases)
        updated = len(new_ids)
        print(json.dumps({"status": "info", "action": "merge", "batch_index": batch_index, "updated": updated, "total": len(merged_cases)}), file=sys.stderr)
        batch_data["testcases"] = merged_cases
        _write_json(batch_path, batch_data)
        # 增量更新后仍需走 Gate quick check
        cases = merged_cases
    else:
        _write_json(batch_path, batch_data)
        cases = batch_data.get("testcases", batch_data.get("cases", []))

    # V3.2.9: 骨架锁定--读取预分配的skeleton,用代码原值覆盖Agent返回的priority/is_smoke
    # V4.8.6: skeleton统一放在 p6_batches/ 目录
    skeleton_path = os.path.join(data_dir, "p6_batches", f"batch_{batch_index:03d}_skeleton.json")
    skeleton_map = {}  # case_id -> {priority, is_smoke, source_test_point}
    skeleton_missing = False
    if os.path.exists(skeleton_path):
        try:
            skeletons = _read_json(skeleton_path)
            for sk in skeletons:
                skeleton_map[sk.get("case_id", "")] = sk
        except Exception:
            pass
    else:
        skeleton_missing = True
        print(json.dumps({"status": "warning", "reason": f"骨架文件缺失: {skeleton_path},跳过骨架锁定,质量检查降级为宽松模式"}), file=sys.stderr)

    # V4.6.12 Bugfix: 强制扁平化--将嵌套 fields 结构展开为顶层字段
    # V4.7.2: 关键字段(steps/expected_results)优先取较长版本,防止截断数据丢失
    for c in cases:
        if isinstance(c, dict) and "fields" in c and isinstance(c["fields"], dict):
            for k, v in c["fields"].items():
                if k not in c or c[k] is None:
                    c[k] = v
                elif k in ("steps", "expected_results", "description", "preconditions"):
                    # 取较长的版本(Agent 可能在顶层输出截断版,fields 内是完整版)
                    if len(str(v)) > len(str(c.get(k, ""))):
                        c[k] = v
            del c["fields"]

    # 对每条用例强制覆盖priority/is_smoke/source_test_point(扁平化之后)
    if skeleton_map:
        for c in cases:
            cid = _get_case_field(c, "case_id", "")
            if cid in skeleton_map:
                sk = skeleton_map[cid]
                # 扁平化后直接覆盖顶层字段
                c["priority"] = sk["priority"]
                c["is_smoke"] = sk["is_smoke"]
                c["source_test_point"] = sk["source_test_point"]
                c["case_id"] = sk["case_id"]
        # 重新写入覆盖后的batch文件
        batch_data["testcases"] = cases
        _write_json(batch_path, batch_data)

    # V4.6.17: 格式归一化--自动修复list→string、空值等常见格式问题
    for c in cases:
        if not isinstance(c, dict):
            continue
        # steps:list → "\n"连接的字符串
        steps_val = c.get("steps")
        if isinstance(steps_val, list):
            c["steps"] = "\n".join(str(s) for s in steps_val if s)
        # expected_results:list → "\n"连接的字符串
        exp_val = c.get("expected_results")
        if isinstance(exp_val, list):
            c["expected_results"] = "\n".join(str(e) for e in exp_val if e)
        # preconditions:list → "\n"连接的字符串
        pre_val = c.get("preconditions")
        if isinstance(pre_val, list):
            c["preconditions"] = "\n".join(str(p) for p in pre_val if p)
    # 归一化后重新写回batch文件
    batch_data["testcases"] = cases
    _write_json(batch_path, batch_data)

    # V4.8.11: 步骤-期望数量自动校准 - 差1行自动补齐,减少Agent重试
    auto_fixed = 0
    for c in cases:
        st = str(c.get("steps", ""))
        ex = str(c.get("expected_results", ""))
        sl = [l for l in st.split('\n') if l.strip() and l.strip()[0:1].isdigit()]
        el = [l for l in ex.split('\n') if l.strip() and l.strip()[0:1].isdigit()]
        diff = len(sl) - len(el)
        if diff == 1:
            c["expected_results"] = ex.rstrip('\n') + f"\n{len(el)+1}. (自动补齐)待补充期望结果"
            auto_fixed += 1
        elif diff == -1:
            c["steps"] = st.rstrip('\n') + f"\n{len(sl)+1}. (自动补齐)待补充步骤"
            auto_fixed += 1
    if auto_fixed:
        batch_data["testcases"] = cases
        _write_json(batch_path, batch_data)
        print(json.dumps({"status": "info", "auto_fixed_step_exp": auto_fixed, "hint": f"{auto_fixed}条用例步骤/期望自动补齐(差1行)"}), file=sys.stderr)

    # V3.2.9: 硬校验(不达标直接拒绝保存)
    hard_issues = []

    # V4.10.1: case_id兜底 - 窄聚焦模式下Agent可能不输出case_id或只部分输出
    # 当skeleton存在且case_id校验可能失败时,先尝试修复
    if skeleton_map and (not skeleton_missing):
        skeletons_for_match = _read_json(skeleton_path) if os.path.exists(skeleton_path) else []
        empty_cids = [i for i, c in enumerate(cases) if not _get_case_field(c, "case_id", "")]

        if empty_cids:
            # 部分或全部case_id为空 → 按骨架顺序兜底填充
            if len(cases) != len(skeletons_for_match):
                hard_issues.append(f"❌ Agent输出{len(cases)}条,骨架期望{len(skeletons_for_match)}条。数量不匹配,无法自动补全case_id。请重新生成。")
                # 直接跳到硬校验输出,跳过骨架匹配
            else:
                # 数量匹配 → 按顺序一一对应填充case_id/priority/is_smoke
                for i, c in enumerate(cases):
                    if i < len(skeletons_for_match):
                        sk = skeletons_for_match[i]
                        _set_case_field(c, "case_id", sk.get("case_id", ""))
                        _set_case_field(c, "priority", sk.get("priority", "P1"))
                        _set_case_field(c, "is_smoke", sk.get("is_smoke", False))
                        _set_case_field(c, "source_test_point", sk.get("source_test_point", ""))
                # 重新写入batch文件
                batch_data["testcases"] = cases
                _write_json(batch_path, batch_data)
                print(json.dumps({"status": "info", "action": "auto_fix_case_ids", "batch_index": batch_index, "filled": len(empty_cids), "hint": "case_id按骨架顺序自动补全"}), file=sys.stderr)

    # 校验0:case_id全集一致性(防止Agent伪造/缺少/重复case_id)
    if skeleton_map:
        skeleton_ids = set(skeleton_map.keys())
        returned_ids = set()
        duplicate_ids = []
        for c in cases:
            cid = _get_case_field(c, "case_id", "")
            if cid in returned_ids:
                duplicate_ids.append(cid)
            returned_ids.add(cid)
        missing_ids = skeleton_ids - returned_ids
        extra_ids = returned_ids - skeleton_ids
        if missing_ids:
            hard_issues.append(f"缺少{len(missing_ids)}个骨架用例: {', '.join(sorted(missing_ids)[:3])}")
        if extra_ids:
            hard_issues.append(f"多出{len(extra_ids)}个非法用例: {', '.join(sorted(extra_ids)[:3])}")
        if duplicate_ids:
            hard_issues.append(f"重复{len(duplicate_ids)}个case_id: {', '.join(duplicate_ids[:3])}")

    # 校验1:用例数量≥batch_budget(逐测试点校验)
    p5_path = os.path.join(data_dir, "p5_output.json")
    if os.path.exists(p5_path) and os.path.exists(skeleton_path):
        try:
            p5_data = _read_json(p5_path)
            p5_map = {tp.get("id", ""): tp for tp in p5_data.get("test_points", [])}
            skeletons = _read_json(skeleton_path)
            # 统计每个测试点的实际用例数
            tp_actual = {}
            for c in cases:
                src = _get_case_field(c, "source_test_point", "")
                if not src:
                    cid = _get_case_field(c, "case_id", "")
                    if cid and "-TC-" in cid:
                        src = cid.rsplit("-TC-", 1)[0]
                if src:
                    tp_actual[src] = tp_actual.get(src, 0) + 1
            # 逐点校验
            tp_expected = {}
            for sk in skeletons:
                src = sk.get("source_test_point", "")
                tp_expected[src] = tp_expected.get(src, 0) + 1
            shortfall = []
            for tp_id, expected in tp_expected.items():
                actual = tp_actual.get(tp_id, 0)
                if actual < expected:
                    shortfall.append(f"{tp_id}:应{expected}条实际{actual}条")
            if shortfall:
                hard_issues.append(f"测试点展开不足: {', '.join(shortfall[:5])}")
        except Exception:
            pass

    # V4.8.7: LOW模型批次小(3-5条/批),放宽比例阈值避免每批都超标
    mt = _get_model_tier_for_dir(data_dir)
    smoke_limit = 0.30 if mt == "LOW" else 0.25
    p0_limit = 0.35 if mt == "LOW" else 0.25

    # 校验2:冷烟比例(LOW模型放宽到30%,单批少量用例极易突破25%)
    if len(cases) > 0:
        smoke_count = sum(1 for c in cases if _is_smoke(_get_case_field(c, "is_smoke", "")))
        smoke_ratio = smoke_count / len(cases)
        if smoke_ratio > smoke_limit:
            hard_issues.append(f"冷烟比例{smoke_ratio:.0%}>{smoke_limit:.0%}")

    # 校验3:P0比例(LOW模型放宽到35%)
    if len(cases) > 0:
        p0_count = sum(1 for c in cases if _get_case_field(c, "priority", "").upper() in ("P0", "HIGHEST"))
        p0_ratio = p0_count / len(cases)
        if p0_ratio > p0_limit:
            hard_issues.append(f"P0比例{p0_ratio:.0%}>{p0_limit:.0%}")

    # 校验4:步骤去重检测(唯一步骤<50%拒绝)
    # V4.7.3: 排除共同前缀(登录/导航步骤) + risk_verification类豁免
    if len(cases) >= 4:
        def _strip_common_prefix(steps_text: str) -> str:
            """去除所有用例共享的登录/导航前缀步骤,只保留差异化业务步骤。

            登录步骤(如「使用有权限账号登录CRM系统,进入首页→XX页面」)
            在所有用例中相同,会污染唯一性计算。"""
            if not steps_text:
                return steps_text
            lines = steps_text.strip().split('\n')
            # 识别并移除包含登录/导航关键词的前缀行
            login_keywords = ['登录', '进入首页', '进入系统', '打开', '输入密码', '输入账号']
            result_lines = []
            for line in lines:
                stripped = line.strip()
                # 去除编号前缀后检查
                import re as _re2
                content = _re2.sub(r'^\d+[\.\、\))]\s*', '', stripped)
                is_common_prefix = any(kw in content for kw in login_keywords)
                if not is_common_prefix:
                    result_lines.append(stripped)
            return '\n'.join(result_lines) if result_lines else steps_text

        # 检查是否全部为risk_verification/exception类用例
        all_risk_or_exc = True
        for c in cases:
            cat = _get_case_field(c, "test_category", "") or _get_case_field(c, "category", "")
            if cat not in ("risk_verification", "exception"):
                all_risk_or_exc = False
                break

        # V4.9.4: LOW模型步骤唯一性降为WARNING(MiniMax无法稳定产出差异化步骤)
        model_tier_save = _get_model_tier_for_dir(data_dir)
        if model_tier_save == "LOW" and not all_risk_or_exc:
            min_unique = 0.2  # LOW模型只要求20%唯一性,不通过仅标记不拒绝
            threshold_label = "20%(LOW模型放宽)"
        elif all_risk_or_exc:
            # risk_verification/exception类用例: 放宽到30%(风险点天然场景单一)
            min_unique = 0.3
            threshold_label = "30%(risk_verification豁免)"
        else:
            min_unique = 0.5
            threshold_label = "50%"

        steps_set = set()
        for c in cases:
            s = _get_case_field(c, "steps", "")
            if s:
                # 去除共同前缀后再比较
                stripped = _strip_common_prefix(s.strip())
                if stripped:
                    steps_set.add(stripped)
        unique_ratio = len(steps_set) / len(cases)
        if unique_ratio < min_unique:
            if model_tier_save == "LOW":
                # LOW模型: 标记stderr警告但不阻断保存
                print(json.dumps({"status": "warning", "action": "step_uniqueness_low", "ratio": f"{unique_ratio:.0%}", "batch_index": batch_index, "hint": "LOW模型步骤差异化能力有限,已标记警告但继续保存"}), file=sys.stderr)
            else:
                hard_issues.append(f"步骤唯一性{len(steps_set)}/{len(cases)}=({unique_ratio:.0%}<{threshold_label})。每条用例必须基于p5_description生成差异化步骤,严禁复制。提示:读取skeleton中每条用例的p5_description,从描述中提取不同的操作流程。")

    # 校验5:关键字段非空
    empty_title = sum(1 for c in cases if not _get_case_field(c, "title", ""))
    empty_steps = sum(1 for c in cases if not _get_case_field(c, "steps", ""))
    empty_expected = sum(1 for c in cases if not _get_case_field(c, "expected_results", ""))
    if empty_title > 0:
        hard_issues.append(f"{empty_title}条用例title为空")
    if empty_steps > 0:
        hard_issues.append(f"{empty_steps}条用例steps为空")
    if empty_expected > 0:
        hard_issues.append(f"{empty_expected}条用例expected_results为空")

    # V3.3.5: 步骤-结果数量一一对应校验 + 跨测试点唯一性检查
    if len(cases) > 3:
        # 校验A:步骤数=期望结果数(阈值15%)
        step_exp_mismatch = 0
        for c in cases:
            steps_text = str(_get_case_field(c, "steps", ""))
            exp_text = str(_get_case_field(c, "expected_results", ""))
            step_lines = [l for l in steps_text.split('\n') if l.strip() and l.strip()[0:1].isdigit()]
            exp_lines = [l for l in exp_text.split('\n') if l.strip() and l.strip()[0:1].isdigit()]
            if abs(len(step_lines) - len(exp_lines)) >= 1:
                step_exp_mismatch += 1
        if step_exp_mismatch > len(cases) * 0.15:
            hard_issues.append(
                f"{step_exp_mismatch}/{len(cases)}条用例步骤数≠期望结果数。"
                f"规则:每个步骤必须有对应的期望结果。基于P5测试点description中列出的操作流程,逐一编写步骤和期望。"
            )

        # V4.11.0: 校验B已移除 - 逐条生成模式下无跨TP场景
        # 原校验B逻辑:跨测试点步骤唯一性检查
        # 替代:G5-intra 在 _quick_gate_single_tp 中处理(同TP内弱化检测)

    # V4.6.17: 骨架已不含step_expected_pairs,R14检查移除。Agent基于P5原文自由创作步骤。

    if hard_issues:
        # V4.10.1: 生成 fix_hints 指引 Agent 自动修复
        fix_hints = []
        batch_path_fix = os.path.join(batches_dir, f"batch_{batch_index:03d}.json")
        for iss in hard_issues:
            if "P0比例" in iss:
                fix_hints.append({"action": "reduce_p0", "batch": batch_index, "issue": iss,
                    "hint": "读取batch文件,将非冷烟P0用例的priority改为P1,用 p6_save_batch --batch-index " + str(batch_index) + " --merge 保存"})
            elif "步骤唯一性" in iss and "差异化" in iss:
                fix_hints.append({"action": "differentiate_steps", "batch": batch_index, "issue": iss,
                    "hint": "读取skeleton的p5_description,为每个TP写不同的操作步骤。改后用 --merge 保存"})
            elif "模糊" in iss or "表述" in iss:
                fix_hints.append({"action": "fix_vague_expected", "batch": batch_index, "issue": iss,
                    "hint": "改期望结果禁止词(正常/成功/正确/符合预期)→可观测描述。改后用 --merge 保存"})
            elif "步骤完全相同" in iss:
                fix_hints.append({"action": "differentiate_all_steps", "batch": batch_index, "issue": iss,
                    "hint": "全部步骤相同,必须为每个TP重写差异化步骤。改后用 --merge 保存"})
            elif "title为空" in iss or "steps为空" in iss or "expected_results为空" in iss:
                fix_hints.append({"action": "fill_empty_fields", "batch": batch_index, "issue": iss,
                    "hint": "补全空字段。改后用 --merge 保存"})

        # V4.8.0: LOW模型重试熔断 - 同批累计≥3次拒绝 → 草稿兜底,不阻塞流程
        retry_state_path = os.path.join(data_dir, "orchestrator_state.json")
        retry_key = f"p6_batch_{batch_index}_retry"
        retry_count = 0
        tier = "HIGH"
        state_data = {}
        if os.path.exists(retry_state_path):
            try:
                state_data = _read_json(retry_state_path)
                retry_count = state_data.get(retry_key, 0)
                tier = state_data.get("model_tier", "HIGH")
            except Exception:
                state_data = {}
        # 如果是 LOW 模型且已达熔断上限 → 草稿兜底
        LOW_MAX_RETRIES = 3
        if tier == "LOW" and retry_count >= LOW_MAX_RETRIES:
            # 生成兜底草稿
            pg = _get_p6_guide()
            draft_cases = []
            p5_path = os.path.join(data_dir, "p5_output.json")
            if os.path.exists(p5_path) and os.path.exists(skeleton_path):
                try:
                    p5_data = _read_json(p5_path)
                    skeletons = _read_json(skeleton_path)
                    tp_map = {tp.get("id", ""): tp for tp in p5_data.get("test_points", [])}
                    for sk in skeletons:
                        tp_id = sk.get("source_test_point", "")
                        tp = tp_map.get(tp_id, {"description": "", "category": "main_flow"})
                        draft = pg.generate_draft_case(tp, sk, p5_data)
                        draft_cases.append(draft)
                except Exception:
                    pass
            if draft_cases:
                batch_data["testcases"] = draft_cases
                batch_data["quality"] = "low_quality_draft"
                _write_json(batch_path, batch_data)
                print(json.dumps({"status": "draft_saved", "batch_index": batch_index, "draft_count": len(draft_cases), "hint": "该批次连续被拒,已保存草稿兜底,需人工审查"}), file=sys.stderr)
                # 重置该批次计数,继续流程
                state_data[retry_key] = 0
                _write_json(retry_state_path, state_data)
                return
        # 未达上限:计数+1,正常拒绝
        retry_count += 1
        state_data[retry_key] = retry_count
        state_data["model_tier"] = tier
        _write_json(retry_state_path, state_data)
        print(json.dumps({"status": "info", "retry_key": retry_key, "retry_count": retry_count, "max_retries": LOW_MAX_RETRIES if tier == "LOW" else 999}), file=sys.stderr)
        # 删除已写入的不合格文件
        if os.path.exists(batch_path):
            os.remove(batch_path)
        # V4.6.17: 增量修复--提取失败用例ID,提示只重写问题用例
        failed_ids = []
        for iss in hard_issues:
            import re as _re
            ids = _re.findall(r'[A-Za-z0-9]+-[A-Za-z0-9]+-?\d*?TP-\d+-TC-\d+', str(iss))
            failed_ids.extend(ids)
        failed_ids = list(set(failed_ids))[:20]
        print(json.dumps({
            "status": "quality_rejected",
            "batch_index": batch_index,
            "issues": hard_issues,
            "fix_hints": fix_hints,
            "failed_case_ids": failed_ids,
            "retry_hint": f"🔴 按 fix_hints 逐项修复后重新 p6_save_batch --batch-index {batch_index} --merge。自动重试最多3次。" if fix_hints else (
                f"仅需重写以下{len(failed_ids)}条问题用例: {failed_ids}" if failed_ids else "请重新生成本批次用例"),
        }))
        sys.exit(1)

    # V4.8.10: 占位符质量检测 - 标记不拒绝,供Agent重跑时重点关注
    placeholder_warnings = _check_placeholder_quality(cases)
    if placeholder_warnings:
        total_tagged = placeholder_warnings.get("total_tagged", 0)
        print(json.dumps({
            "status": "info",
            "placeholder_warnings": placeholder_warnings,
            "hint": f"{total_tagged}条用例含占位符/空洞内容,已标记到remarks字段。非致命,批次已保存。重跑时请关注这些用例。"
        }), file=sys.stderr)

    # V4.3.0: Gate G1+G2+G5 快速质量检查(每批次保存时执行)
    gate_quick_results = []
    gate_quick_eval = {"status": "PASS", "block_failed": 0}
    if os.path.exists(p5_path):
        try:
            p5_data = _read_json(p5_path)
            p5_tps = p5_data.get("test_points", [])
            gate_quick_results = _run_gate_checks(cases, p5_tps, check_ids=["G1", "G2", "G5"])
            # V4.8.5: LOW模型Gate分级 - G1/G1.5从BLOCK降为WARNING
            # V4.9.4: LOW模型G5也降为WARNING(MiniMax无法稳定产出差异化步骤)
            if _get_model_tier_for_dir(data_dir) == "LOW":
                for r in gate_quick_results:
                    if r.get("check_id") in ("G1", "G1.5", "G5"):
                        r["level"] = "WARNING"
            gate_quick_eval = _evaluate_gate(gate_quick_results)
        except Exception as _gate_err:
            gate_quick_eval = {"status": "PASS", "block_failed": 0, "warning": f"Gate检查执行异常(跳过): {_gate_err}"}

    # G1+G2+G5 BLOCK失败时拒绝批次
    if gate_quick_eval.get("status") == "FAIL":
        if os.path.exists(batch_path):
            os.remove(batch_path)
        gate_issue_summary = "; ".join(
            f"{r['check_id']}:{r['detail']}" for r in gate_quick_results if r.get("status") == "FAILED"
        )
        print(json.dumps({
            "status": "gate_rejected",
            "batch_index": batch_index,
            "gate_checks": gate_quick_results,
            "gate_summary": gate_issue_summary,
            "retry_hint": f"Gate G1+G2+G5快速检查不通过: {gate_issue_summary}",
        }))
        sys.exit(1)

    print(json.dumps({
        "status": "ok",
        "batch_index": batch_index,
        "cases_in_batch": len(cases),
        "batch_file": batch_path,
        "skeleton_locked": bool(skeleton_map),
        "gate_quick_check": gate_quick_eval.get("status", "SKIP"),
        "gate_quick_issues": gate_quick_eval.get("block_failed", 0) + gate_quick_eval.get("warnings", 0),
    }))
    _invalidate_batch_cache()  # V4.9.1: batch已修改,清除索引缓存


# ============================================================
# Action: quality_check (质量校验强化)
# ============================================================

# 每步最小产出数量
# 每步最小产出数量(以云端实际JSON字段名为真源,支持多候选路径用|分隔)
MIN_OUTPUT_COUNTS = {
    "P0": {"blocks.operations|blocks.pages|blocks.business_rules": 1},  # P0实际输出用blocks.operations/pages/business_rules
    "P1": {"feature_tree": 2},  # Bugfix V4.6.9: feature_tree是array,_get_nested已特殊处理返回len()
    "P2": {"test_points": 8},  # V3.2.8: 静态底线8,quality_check中动态计算为max(8, P1叶节点数×2)
    "P3": {"risk_points": 1},  # 至少1个风险点
    "P4": {"pci_list": 1},  # 至少1个PCI
    "P5": {"test_points": 10},
    "P6": {"testcases": 15},  # V3.2.7: 静态底线15,quality_check中动态计算为P5测试点数×1.5
}

# P6用例质量规则(V3.0.3统一真源,prep_prompt和quality_check共用)
P6_QUALITY_RULES = {
    "smoke_ratio_min": 0.05,  # 冒烟用例至少5%(原8%过严,12功能点需求数学上难稳定达到)
    "smoke_ratio_max": 0.20,  # 冒烟用例不超过20%
    "p0_ratio_max": 0.20,  # P0优先级不超过20%(V3.2.3收紧→V3.2.4沿用,与P2 prep_prompt注入一致)
    "all_same_priority": False,  # 不允许所有用例同一优先级
    "per_requirement_smoke": True,  # 每个需求至少1条冒烟用例
}

def _get_nested(data, key_path):
    """获取嵌套字段值,支持多候选路径(用|分隔)

    示例:
      _get_nested(data, "blocks.modules")  # 单路径
      _get_nested(data, "blocks.operations|blocks.pages")  # 多候选,返回第一个非空的

    Bugfix V4.6.9: 当key_path=="feature_tree"且data为list时,返回len(data)(feature_tree是array)
    """
    # Bugfix V4.6.9: 特殊处理feature_tree为array的情况
    if key_path == "feature_tree" and isinstance(data, list):
        return len(data)

    candidates = key_path.split("|")
    for candidate in candidates:
        keys = candidate.strip().split(".")
        current = data
        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
            else:
                current = None
                break
        if current is not None:
            return current
    return None

# ============================================================
# Action: p7_code_check (V3.3.1: P7代码硬校验,替代Agent审计)
# ============================================================

# P7子检查函数
def _p7_check_c1(cases):
    """C1 要素完整性 [BLOCK]: 必填7项非空"""
    required = ['case_id', 'title', 'preconditions', 'steps', 'expected_results', 'priority', 'is_smoke']
    issues = []
    for c in cases:
        for rf in required:
            val = _get_case_field(c, rf, "")
            if val is None or (isinstance(val, str) and not val.strip()):
                issues.append({"case_id": _get_case_field(c, "case_id", "?"), "field": rf, "issue": f"{rf}为空"})
    return {
        "check_id": "C1", "name": "要素完整性", "level": "BLOCK",
        "status": "FAILED" if issues else "PASSED",
        "detail": f"{len(cases)}/{len(cases)}条用例7项必填字段完整" if not issues else f"{len(issues)}个字段缺失",
        "issues": issues[:20],
    }

def _p7_check_c2(cases):
    """C2 步骤-结果数量对应 [分级]: ±1=INFO, ±2=WARNING, >=3=BLOCK (V4.6.14增强根因分析+verify闭环)"""
    import re as _re
    block_issues, warn_issues, info_issues = [], [], []
    for c in cases:
        steps = _get_case_field(c, "steps", "")
        expected = _get_case_field(c, "expected_results", "")
        s_lines = [l for l in steps.split('\n') if l.strip() and _re.match(r'^\d+\.', l.strip())]
        e_lines = [l for l in expected.split('\n') if l.strip() and _re.match(r'^\d+\.', l.strip())]
        diff = abs(len(s_lines) - len(e_lines))
        cid = _get_case_field(c, "case_id", "?")
        priority = _get_case_field(c, "priority", "P2")

        # V4.6.14: 增强根因分析
        cause = ""
        fix_hint = ""
        verify = ""

        if len(s_lines) > len(e_lines):
            # 步骤多于期望
            avg_step_len = sum(len(l) for l in s_lines) / max(len(s_lines), 1)
            if avg_step_len < 15:
                cause = "步骤过短(平均{:.0f}字),可能将每个操作不当拆分成多个步骤".format(avg_step_len)
                fix_hint = "将连续的子步骤合并为一个步骤组,每个组对应一个期望结果"
            else:
                cause = "步骤数({})多于期望数({}),可能在应写期望时偷懒".format(len(s_lines), len(e_lines))
                fix_hint = "为每个有效操作步骤补充对应期望结果"
            verify = "修复后验证:步骤数与期望数偏差应≤2,且期望覆盖率≥60%"
        elif len(e_lines) > len(s_lines):
            cause = "期望结果数({})多于步骤数({}),可能将多个期望合并为一条".format(len(e_lines), len(s_lines))
            fix_hint = "将模糊的期望结果拆分为多个具体期望,每条期望对应一个验证点"
            verify = "修复后验证:每条期望都应有对应步骤"

        issue_entry = {
            "case_id": cid,
            "steps": len(s_lines),
            "expected": len(e_lines),
            "diff": diff,
            "cause": cause,
            "fix_hint": fix_hint,
            "verify": verify,
        }

        if diff >= 3:
            block_issues.append(issue_entry)
        elif diff == 2:
            warn_issues.append(issue_entry)
        elif diff == 1:
            info_issues.append(issue_entry)

    if block_issues:
        status = "FAILED"
    elif warn_issues:
        status = "WARNING"
    else:
        status = "PASSED"
    return {
        "check_id": "C2", "name": "步骤-结果数量对应", "level": "BLOCK",
        "status": status,
        "detail": f"差≥3:{len(block_issues)}条, 差2:{len(warn_issues)}条, 差1:{len(info_issues)}条(INFO)",
        "issues": block_issues[:10] + warn_issues[:10],
        "info_count": len(info_issues),
    }

def _p7_check_c3(cases):
    """C3 P0占比 [WARNING/BLOCK]: ≤20%通过, 20-40%警告, >40%阻塞"""
    total = len(cases)
    p0 = sum(1 for c in cases if _get_case_field(c, "priority", "").upper() in ("P0", "HIGHEST"))
    ratio = p0 / max(total, 1)
    if ratio > 0.40:
        status = "FAILED"
    elif ratio > 0.20:
        status = "WARNING"
    else:
        status = "PASSED"
    return {
        "check_id": "C3", "name": "P0占比", "level": "WARNING",
        "status": status,
        "detail": f"P0={p0}/{total}({ratio:.1%})",
        "issues": [],
    }

def _p7_check_c4(cases):
    """C4 冒烟占比 [WARNING]: 按总数分档校验"""
    total = len(cases)
    smoke = sum(1 for c in cases if _is_smoke(_get_case_field(c, "is_smoke", "")))
    ratio = smoke / max(total, 1)
    if total <= 15:
        lo, hi = 0.20, 0.35
    elif total <= 30:
        lo, hi = 0.15, 0.25
    else:
        lo, hi = 0.10, 0.20
    if ratio < lo or ratio > hi:
        status = "WARNING"
    else:
        status = "PASSED"
    return {
        "check_id": "C4", "name": "冒烟占比", "level": "WARNING",
        "status": status,
        "detail": f"冒烟={smoke}/{total}({ratio:.1%}), 期望{lo:.0%}-{hi:.0%}",
        "issues": [],
    }

def _p7_check_c5(cases):
    """C5 步骤描述质量 [WARNING]: 上下文感知正则"""
    import re as _re
    VAGUE_NOUNS = {'数据', '结果', '页面', '功能', '状态', '信息', '内容', '格式'}
    issues = []
    for c in cases:
        steps = _get_case_field(c, "steps", "")
        lines = [l.strip() for l in steps.split('\n') if _re.match(r'^\d+\.', l.strip())]
        for line in lines:
            m = _re.match(r'^\d+\.\s*(验证|检查|确认)\s*(.*)$', line)
            if m:
                verb, rest = m.group(1), m.group(2).strip()
                # 放行:有判断词
                if _re.search(r'是否|能否|有无|包含|显示为|等于|大于|小于|超出|不足', rest):
                    continue
                # 放行:去掉模糊名词后仍有内容
                cleaned = rest
                for vn in VAGUE_NOUNS:
                    cleaned = cleaned.replace(vn, '')
                cleaned = _re.sub(r'[正确正常无误成功]', '', cleaned).strip()
                if len(cleaned) >= 2:
                    continue
                issues.append({"case_id": _get_case_field(c, "case_id", "?"), "line": line[:80], "verb": verb})
    ratio = len(issues) / max(len(cases), 1)
    return {
        "check_id": "C5", "name": "步骤描述质量", "level": "WARNING",
        "status": "WARNING" if ratio > 0.30 else "PASSED",
        "detail": f"{len(issues)}/{len(cases)}条含模糊动词({ratio:.1%})",
        "issues": issues[:15],
    }

def _p7_check_c6(cases):
    """C6 期望结果质量 [WARNING]: 负向模式正则"""
    import re as _re
    VAGUE_PATTERNS = [
        r'(?:操作|执行|处理|加载|保存|删除|修改|提交)(?:成功|正确|正常)\s*$',
        r'(?:显示|展示|呈现)(?:正确|正常|无误)\s*$',
        r'符合预期\s*$',
        r'(?:数据|结果|内容|信息)(?:正确|正常|无误)\s*$',
        r'(?:功能|模块|接口)(?:正常|可用)\s*$',
        r'(?:验证|校验)(?:通过|成功)\s*$',
    ]
    issues = []
    for c in cases:
        expected = _get_case_field(c, "expected_results", "")
        lines = [l.strip() for l in expected.split('\n') if _re.match(r'^\d+\.', l.strip())]
        for line in lines:
            for pattern in VAGUE_PATTERNS:
                if _re.search(pattern, line):
                    issues.append({"case_id": _get_case_field(c, "case_id", "?"), "line": line[:80]})
                    break
    ratio = len(issues) / max(len(cases), 1)
    return {
        "check_id": "C6", "name": "期望结果质量", "level": "WARNING",
        "status": "WARNING" if ratio > 0.30 else "PASSED",
        "detail": f"{len(issues)}/{len(cases)}条含模糊描述({ratio:.1%})",
        "issues": issues[:15],
    }

def _p7_check_c61(cases):
    """C6.1 前置条件三要素 [BLOCK]: 账号/权限 + 数据构造 + 环境配置(V3.3.5: 2/3匹配即通过)"""
    import re as _re
    KW_ACCOUNT = _re.compile(r'账号|权限|登录|用户|角色|管理员|员工')
    KW_DATA = _re.compile(r'数据|预置|构造|预设|测试数据|造数|记录|条|导入|创建')
    KW_ENV = _re.compile(r'环境|系统|配置|服务|运行|部署|开通|正常|时间|状态')
    issues = []
    for c in cases:
        precond = _get_case_field(c, "preconditions", "")
        elements_found = 0
        if KW_ACCOUNT.search(precond):
            elements_found += 1
        if KW_DATA.search(precond):
            elements_found += 1
        if KW_ENV.search(precond):
            elements_found += 1
        # V3.3.5: 2/3匹配即通过(放宽)
        if elements_found < 2:
            issues.append({"case_id": _get_case_field(c, "case_id", "?"), "found": elements_found})
    return {
        "check_id": "C6.1", "name": "前置条件三要素", "level": "BLOCK",
        "status": "FAILED" if issues else "PASSED",
        "detail": f"{len(issues)}/{len(cases)}条前置条件不完整" if issues else f"{len(cases)}条前置条件均含三要素",
        "issues": issues[:20],
    }

def _p7_check_c7(cases, p5_test_points):
    """C7 测试点覆盖率 [BLOCK]: P5 active测试点必须100%覆盖"""
    p5_active = set()
    for tp in p5_test_points:
        if tp.get('status', 'active') == 'active':
            p5_active.add(tp.get('id', ''))
    p6_covered = set()
    for c in cases:
        src = _get_case_field(c, "source_test_point", "")
        if not src:
            src = c.get("source_test_point", "")
        if src:
            p6_covered.add(src)
    uncovered = sorted(p5_active - p6_covered)
    rate = len(p6_covered & p5_active) / max(len(p5_active), 1)
    return {
        "check_id": "C7", "name": "测试点覆盖率", "level": "BLOCK",
        "status": "FAILED" if uncovered else "PASSED",
        "detail": f"覆盖{len(p6_covered & p5_active)}/{len(p5_active)}({rate:.0%})",
        "issues": [{"test_point": tp, "issue": "未覆盖"} for tp in uncovered[:20]],
        "coverage_rate": rate,
    }

def _p7_check_c71(cases, p5_test_points):
    """C7.1 语义覆盖 [WARNING]: 业务实体匹配"""
    import re as _re
    # 从P5描述中提取业务实体
    ENTITY_PATTERNS = [
        r'月亮晒|周亮晒|金种子|商机沙盘|海交综服',
        r'个人标杆|分公司综合实力|有效机构[户客]',
        r'重点机构|债融|托管|福建区域',
        r'增量排名|目标完成率',
    ]
    combined_re = _re.compile('|'.join(ENTITY_PATTERNS))
    tp_entities = {}
    for tp in p5_test_points:
        tp_id = tp.get('id', '')
        desc = tp.get('description', '')
        entities = set(combined_re.findall(desc))
        # 补充引号内术语
        quoted = _re.findall(r'[「""\u201c]([^「""\u201d]+)[」""\u201d]', desc)
        entities.update(q for q in quoted if len(q) >= 2)
        tp_entities[tp_id] = entities

    issues = []
    for c in cases:
        src_tp = _get_case_field(c, "source_test_point", "") or c.get("source_test_point", "")
        if src_tp not in tp_entities or not tp_entities[src_tp]:
            continue
        entities = tp_entities[src_tp]
        text = _get_case_field(c, "title", "") + ' ' + _get_case_field(c, "steps", "")
        hit = sum(1 for e in entities if e in text)
        ratio = hit / max(len(entities), 1)
        if ratio < 0.3:
            issues.append({
                "case_id": _get_case_field(c, "case_id", "?"),
                "source_tp": src_tp,
                "hit_ratio": f"{hit}/{len(entities)}",
            })
    return {
        "check_id": "C7.1", "name": "语义覆盖(业务实体)", "level": "WARNING",
        "status": "WARNING" if issues else "PASSED",
        "detail": f"{len(issues)}/{len(cases)}条语义覆盖不足" if issues else "全部用例语义覆盖充分",
        "issues": issues[:15],
    }

def _p7_check_c8(cases):
    """C8 冒烟合规性 [WARNING]: 冒烟用例priority应为P0/P1"""
    issues = []
    for c in cases:
        if _is_smoke(_get_case_field(c, "is_smoke", "")):
            p = _get_case_field(c, "priority", "")
            if p not in ("P0", "P1"):
                issues.append({
                    "case_id": _get_case_field(c, "case_id", "?"),
                    "priority": p,
                    "suggestion": f"建议将priority从{p}升级为P1",
                })
    return {
        "check_id": "C8", "name": "冒烟合规性", "level": "WARNING",
        "status": "WARNING" if issues else "PASSED",
        "detail": f"{len(issues)}条冒烟用例priority不合规" if issues else "冒烟用例priority均为P0/P1",
        "issues": issues,
    }

def _p7_check_c9(cases):
    """C9 伞形用例检测 [WARNING] - V4.6.11改进

    真正的伞形用例:同一功能点的多个对称模块(月榜/周榜/日榜等)被合并为1条用例。
    误伤场景:"与OA一致"等外部系统引用不属于伞形用例。

    检测逻辑:对称模块词 + 合并意图词 同时出现才判定为伞形。
    """
    import re as _re

    # 对称模块词列表(多选一出现即可)
    SYMMETRIC_MODULE_RE = _re.compile(
        r'月榜|周榜|日榜|季榜|'
        r'PC端|移动端|H5端|APP端|'
        r'总公司|分公司|'
        r'东区|西区|南区|北区|'
        r'版本\d|版本A|版本B|'
        r'Android|iOS|Windows|Mac|'
        r'浏览器端|小程序端'
    )

    # 合并意图词(多选一出现即可)
    MERGE_INTENT_RE = _re.compile(
        r'相应调整|同步调整|一致|同理|同上|类似|'
        r'与.*同|与.*一致|参照.*处理|参考.*调整'
    )

    issues = []
    for c in cases:
        title = _get_case_field(c, "title", "")
        steps = _get_case_field(c, "steps", "")
        text = title + ' ' + steps

        has_module = bool(SYMMETRIC_MODULE_RE.search(text))
        has_merge_intent = bool(MERGE_INTENT_RE.search(text))

        # 必须同时满足:对称模块词 + 合并意图词
        if has_module and has_merge_intent:
            issues.append({
                "case_id": _get_case_field(c, "case_id", "?"),
                "module_match": SYMMETRIC_MODULE_RE.findall(text),
                "merge_match": MERGE_INTENT_RE.findall(text),
            })

    return {
        "check_id": "C9", "name": "伞形用例检测", "level": "WARNING",
        "status": "WARNING" if issues else "PASSED",
        "detail": f"{len(issues)}条伞形用例" if issues else "无伞形用例",
        "issues": issues[:10],
    }

def _p7_statistics(cases):
    """INFO级统计指标"""
    from collections import Counter as _Counter
    priorities = _Counter(_get_case_field(c, "priority", "unknown") for c in cases)
    step_texts = set()
    step_lens = []
    precond_lens = []
    title_counter = _Counter()
    for c in cases:
        s = _get_case_field(c, "steps", "")
        step_texts.add(s.strip())
        step_lens.append(len(s))
        precond_lens.append(len(_get_case_field(c, "preconditions", "")))
        title_counter[_get_case_field(c, "title", "")] += 1
    dup_titles = {t: cnt for t, cnt in title_counter.items() if cnt > 1}
    return {
        "total_cases": len(cases),
        "priority_distribution": dict(priorities),
        "smoke_count": sum(1 for c in cases if _is_smoke(_get_case_field(c, "is_smoke", ""))),
        "step_uniqueness": len(step_texts) / max(len(cases), 1),
        "avg_step_length": sum(step_lens) / max(len(step_lens), 1),
        "avg_precondition_length": sum(precond_lens) / max(len(precond_lens), 1),
        "duplicate_titles": len(dup_titles),
        "duplicate_title_samples": list(dup_titles.keys())[:5],
    }

def _generate_p7_html_report(checks, statistics, output_path):
    """生成P7质量报告HTML"""
    status_icon = {"PASSED": "✅", "FAILED": "❌", "WARNING": "⚠️"}
    status_color = {"PASSED": "#27ae60", "FAILED": "#e74c3c", "WARNING": "#f39c12"}
    checks_html = ""
    for ck in checks:
        color = status_color.get(ck["status"], "#999")
        icon = status_icon.get(ck["status"], "")
        issues_html = ""
        if ck.get("issues"):
            issues_html = "<ul>" + "".join(f"<li>{json.dumps(i, ensure_ascii=False)[:200]}</li>" for i in ck["issues"][:10]) + "</ul>"
        checks_html += f"""<tr>
            <td>{ck['check_id']}</td><td>{ck['name']}</td><td>{ck['level']}</td>
            <td style="color:{color};font-weight:bold;">{icon} {ck['status']}</td>
            <td>{ck['detail']}</td></tr>"""
        if issues_html:
            checks_html += f"<tr><td colspan='5' style='background:#fafafa;padding-left:40px;'>{issues_html}</td></tr>"

    pri = statistics.get("priority_distribution", {})
    total = statistics.get("total_cases", 0)
    smoke = statistics.get("smoke_count", 0)

    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>P7 Quality Report</title>
<style>
body{{font-family:-apple-system,sans-serif;background:#f5f7fa;padding:20px;color:#333;line-height:1.6;}}
.container{{max-width:960px;margin:0 auto;}}
h1{{font-size:22px;color:#1a1a2e;}}
.card{{background:#fff;border-radius:10px;padding:20px;margin:16px 0;box-shadow:0 2px 6px rgba(0,0,0,0.05);}}
table{{width:100%;border-collapse:collapse;font-size:13px;}}
th{{background:#f8f9fb;padding:8px 10px;text-align:left;border-bottom:2px solid #e8ecf1;}}
td{{padding:8px 10px;border-bottom:1px solid #f0f0f0;}}
.metric{{display:inline-block;text-align:center;padding:10px 16px;margin:4px;background:#f8f9fb;border-radius:6px;}}
.metric .v{{font-size:24px;font-weight:700;color:#1a1a2e;}}
.metric .l{{font-size:11px;color:#888;}}
ul{{margin:4px 0;padding-left:20px;font-size:12px;color:#666;}}
</style></head><body><div class="container">
<h1>🐈‍⬛ P7 Quality Report</h1>
<p style="color:#666;font-size:13px;">Generated by p7_code_check V3.3.1</p>
<div class="card">
<div class="metric"><div class="v">{total}</div><div class="l">总用例</div></div>
<div class="metric"><div class="v">{smoke}</div><div class="l">冒烟用例</div></div>
<div class="metric"><div class="v">{statistics.get('step_uniqueness',0):.0%}</div><div class="l">步骤唯一率</div></div>
<div class="metric"><div class="v">{pri.get('P0',0)}/{pri.get('P1',0)}/{pri.get('P2',0)}/{pri.get('P3',0)}</div><div class="l">P0/P1/P2/P3</div></div>
</div>
<div class="card"><h2>校验结果</h2>
<table><tr><th>ID</th><th>校验项</th><th>级别</th><th>状态</th><th>详情</th></tr>
{checks_html}</table></div>
</div></body></html>"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


# ============================================================
# V4.9.1: P7自动修复 - fix_hints生成 + batch索引查找
# ============================================================

def _find_batch_for_case(data_dir, case_id):
    """V4.9.1: 查找case_id所属batch索引(带缓存,一次构建,多次查询)"""
    cache_attr = '_batch_index_cache'
    cache = getattr(_find_batch_for_case, cache_attr, None)
    if cache and cache.get('_dir') == data_dir:
        return cache.get(case_id, -1)

    batches_dir = os.path.join(data_dir, "p6_batches")
    batch_map = {}
    if os.path.isdir(batches_dir):
        for fn in sorted(os.listdir(batches_dir)):
            if not (fn.startswith("batch_") and fn.endswith(".json")):
                continue
            if "_agent" in fn or "_skeleton" in fn or "_context" in fn:
                continue
            try:
                bd = _read_json(os.path.join(batches_dir, fn))
                bi = int(fn.replace("batch_", "").replace(".json", ""))
                for c in bd.get("testcases", []):
                    batch_map[_get_case_field(c, "case_id", "")] = bi
            except Exception:
                pass
    batch_map['_dir'] = data_dir
    setattr(_find_batch_for_case, cache_attr, batch_map)
    return batch_map.get(case_id, -1)


def _invalidate_batch_cache():
    """V4.9.1: 清除batch索引缓存(p6_merge/p6_save_batch修改后调用)"""
    setattr(_find_batch_for_case, '_batch_index_cache', None)


def _build_p7_fix_hints(checks, data_dir):
    """V4.9.1: 基于P7检查结果生成结构化修复指引

    为4类常见P7 BLOCK生成可执行的修复指令:
    1. generate_missing - 覆盖率不足,补充缺失TP的用例
    2. fix_step_expected - 步骤期望不匹配(C2)
    3. fix_vague_expected - 模糊表述(G2/C5/C6)
    4. fix_forbidden - 禁止模式(G4/C3/C4)
    """
    fix_hints = []
    c7 = next((ck for ck in checks if ck["check_id"] == "C7"), None)
    coverage_rate = c7.get("coverage_rate", 0) if c7 else 1.0

    # 1. C7 覆盖率不足 → generate_missing
    if c7 and c7["status"] == "FAILED":
        uncovered = [iss.get("test_point", "") for iss in c7.get("issues", [])]
        if uncovered:
            fix_hints.append({
                "action": "generate_missing",
                "tp_ids": uncovered[:50],  # 单次最多50个
                "count": len(uncovered),
                "command": "python3 $ORCH --action p6_generate_one --tp-index {N}",
                "save_cmd": "python3 $ORCH --action p6_generate_one --tp-index {N} --save --agent-output '...'",
                "note": "V4.11.0 逐条生成,每个TP独立调用",
                "estimated_minutes": round(len(uncovered) * 0.3, 1)
            })

    # 2. C2 步骤期望不匹配 → fix_step_expected
    c2 = next((ck for ck in checks if ck["check_id"] == "C2"), None)
    if c2 and c2["status"] == "FAILED":
        c2_cases = []
        for iss in c2.get("issues", [])[:30]:
            cid = iss.get("case_id", "")
            bi = _find_batch_for_case(data_dir, cid)
            c2_cases.append({"case_id": cid, "batch_index": bi,
                "field": iss.get("field", "steps"), "issue": iss.get("issue", "步骤期望不匹配")})
        if c2_cases:
            fix_hints.append({"action": "fix_step_expected", "cases": c2_cases,
                "count": len(c2_cases), "hint": "修改batch文件使步骤数和期望数一致,用 --merge模式保存"})

    # 3. G2/C5/C6 模糊表述 → fix_vague_expected
    for ck_id in ("G2", "C5", "C6"):
        ck = next((c for c in checks if c["check_id"] == ck_id and c["status"] == "FAILED"), None)
        if ck:
            vague = []
            for iss in ck.get("issues", [])[:30]:
                cid = iss.get("case_id", "")
                bi = _find_batch_for_case(data_dir, cid)
                vague.append({"case_id": cid, "batch_index": bi,
                    "field": "expected_results", "issue": iss.get("issue", "含模糊表述")})
            if vague:
                fix_hints.append({"action": "fix_vague_expected", "cases": vague,
                    "count": len(vague), "hint": "改期望为具体可观测结果,禁止:正常/成功/正确/符合预期/功能正常"})
            break  # 同类问题只生成一次指引

    # 4. G4/C3/C4 禁止模式 → fix_forbidden
    for ck_id in ("G4", "C3", "C4"):
        ck = next((c for c in checks if c["check_id"] == ck_id and c["status"] == "FAILED"), None)
        if ck:
            forbid = []
            for iss in ck.get("issues", [])[:30]:
                cid = iss.get("case_id", "")
                bi = _find_batch_for_case(data_dir, cid)
                forbid.append({"case_id": cid, "batch_index": bi,
                    "field": iss.get("field", ""), "issue": iss.get("issue", "含禁止词")})
            if forbid:
                fix_hints.append({"action": "fix_forbidden", "cases": forbid,
                    "count": len(forbid), "hint": "替换禁止词为具体可观测描述"})
            break

    # 判定修复策略
    if coverage_rate >= 0.1:
        strategy = "local_repair"  # 覆盖率≥10%都走局部修复(LOW模型restart也无用)
        estimated_minutes = round(sum(h.get("estimated_minutes", 1) for h in fix_hints), 1)
    else:
        strategy = "restart_p6"  # 覆盖率<10%说明P6基本没跑,必须重跑
        estimated_minutes = 0

    # V4.12.3: fix_hints为空时自动生成通用fallback（LOW模型兼容）
    if not fix_hints:
        fix_hints.append({
            "action": "regenerate_from_prompt",
            "hint": "重新逐条执行 p6_generate_one --tp-index N → 阅读prompt生成JSON → --save",
            "fallback_note": "fix_hints由代码规则生成（V4.12.3不再依赖模型），请基于P7检查结果手动修复或regenerate",
            "retry_command": "python3 $ORCH --action p6_generate_one --tp-index {N} --save --agent-output '...'",
        })

    return fix_hints, strategy, estimated_minutes


# ============================================================
# Action: p7_code_check (V3.3.1: P7代码硬校验)
# ============================================================

def action_p7_code_check(args):
    """V3.3.1: P7代码硬校验,替代Agent审计。

    纯代码执行C1-C9+C7.1全部校验,零Agent依赖,秒级完成。
    读取p5_output.json和p6_output.json,输出p7_output.json + P7.pass.json + p7_report.html
    """
    data_dir = args.data_dir
    task_id = args.task_id

    # 前置gate校验
    ok, msg = check_gate(data_dir, "P6", task_id)
    if not ok:
        print(json.dumps({"status": "gate_blocked", "step": "P6", "reason": msg}))
        sys.exit(1)

    # 读取P5和P6产出
    p5_path = os.path.join(data_dir, "p5_output.json")
    p6_path = os.path.join(data_dir, "p6_output.json")
    if not os.path.exists(p5_path):
        print(json.dumps({"status": "error", "reason": "p5_output.json不存在"}))
        sys.exit(1)
    if not os.path.exists(p6_path):
        print(json.dumps({"status": "error", "reason": "p6_output.json不存在"}))
        sys.exit(1)

    p5_data = _read_json(p5_path)
    p6_data = _read_json(p6_path)
    if isinstance(p6_data, list):
        p6_data = {"testcases": p6_data}
    cases = p6_data.get("testcases", [])
    p5_tps = p5_data.get("test_points", [])

    if not cases:
        print(json.dumps({"status": "error", "reason": "p6_output.json中testcases为空"}))
        sys.exit(1)

    # 执行全部校验
    checks = [
        _p7_check_c1(cases),
        _p7_check_c2(cases),
        _p7_check_c3(cases),
        _p7_check_c4(cases),
        _p7_check_c5(cases),
        _p7_check_c6(cases),
        _p7_check_c61(cases),
        _p7_check_c7(cases, p5_tps),
        _p7_check_c71(cases, p5_tps),
        _p7_check_c8(cases),
        _p7_check_c9(cases),
    ]
    statistics = _p7_statistics(cases)

    # V4.3.0: 执行 Gate G1-G7 全量质量检查
    gate_results = []
    gate_evaluation = {"status": "PASS", "block_failed": 0, "warnings": 0}
    try:
        gate_results = _run_gate_checks(cases, p5_tps)
        # V4.8.5: LOW模型Gate分级 - G1/G1.5从BLOCK降为WARNING
        # V4.9.4: LOW模型G5也降为WARNING
        if _get_model_tier_for_dir(data_dir) == "LOW":
            for r in gate_results:
                if r.get("check_id") in ("G1", "G1.5", "G5"):
                    r["level"] = "WARNING"
        gate_evaluation = _evaluate_gate(gate_results)
    except Exception as _gate_err:
        gate_evaluation = {"status": "PASS", "block_failed": 0, "warnings": 0,
                           "summary": f"Gate G1-G7检查执行异常(跳过): {_gate_err}"}

    # 将Gate检查结果追加到checks列表
    for gr in gate_results:
        checks.append({
            "check_id": gr.get("check_id", "?"),
            "name": gr.get("name", ""),
            "level": gr.get("level", "WARNING"),
            "status": gr.get("status", "PASSED"),
            "detail": gr.get("detail", ""),
            "issues": gr.get("issues", []),
        })

    # 判定门禁(含Gate G1-G7结果)
    block_failed = any(ck["status"] == "FAILED" and ck["level"] == "BLOCK" for ck in checks)
    # Gate G1-G7 BLOCK失败也阻断
    gate_block_failed = gate_evaluation.get("status") == "FAIL" and gate_evaluation.get("block_failed", 0) > 0
    has_warning = any(ck["status"] in ("WARNING", "FAILED") and ck["level"] == "WARNING" for ck in checks)

    if block_failed or gate_block_failed:
        gate_status = "FAIL"
        action_required = "RETRY_P6"
        failed_cases = []
        for ck in checks:
            if ck["status"] == "FAILED":
                for iss in ck.get("issues", []):
                    fc = {"check_id": ck["check_id"], "case_id": iss.get("case_id", ""), "field": iss.get("field", "")}
                    fc.update(iss)
                    failed_cases.append(fc)
    elif has_warning:
        gate_status = "PASS"
        action_required = "MANUAL_REVIEW"
        failed_cases = []
    else:
        gate_status = "PASS"
        action_required = "NONE"
        failed_cases = []

    block_passed = sum(1 for ck in checks if ck["level"] == "BLOCK" and ck["status"] == "PASSED")
    block_total = sum(1 for ck in checks if ck["level"] == "BLOCK")
    warn_triggered = sum(1 for ck in checks if ck["level"] == "WARNING" and ck["status"] in ("WARNING", "FAILED"))
    warn_total = sum(1 for ck in checks if ck["level"] == "WARNING")

    summary = f"{len(checks)}项检查: BLOCK {block_passed}/{block_total}通过, WARNING {warn_triggered}/{warn_total}项触发"

    # 构造输出
    p7_output = {
        "schema_version": "2.0.0",
        "source": "p7_code_check",
        "gate_result": {
            "status": gate_status,
            "summary": summary,
            "checks": checks,
        },
        "gate_g1_g7": {
            "results": gate_results,
            "evaluation": gate_evaluation,
            "report": _format_gate_report(gate_results, gate_evaluation) if gate_results else "",
        },
        "statistics": statistics,
        "p7_check_summary": {
            "status": gate_status,
            "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "block_passed": block_passed,
            "block_total": block_total,
            "warnings": warn_triggered,
            "source": "p7_code_check",
        },
        "action_required": action_required,
        "failed_cases": failed_cases[:50],
    }

    # V4.9.1: P7失败时生成修复指引(只在FAIL时生成,避免无意义计算)
    if gate_status == "FAIL":
        fix_hints, fix_strategy, fix_minutes = _build_p7_fix_hints(checks, data_dir)
        p7_output["fix_hints"] = fix_hints
        p7_output["fix_strategy"] = fix_strategy
        p7_output["fix_estimated_minutes"] = fix_minutes
        p7_output["_fix_note"] = ("🔴 Agent按fix_hints逐项自动修复(禁止抛选择题):"
            "generate_missing→p6_generate_one→p6_merge | "
            "fix_*→读tp文件→修改→覆盖保存→p6_merge | "
            "全部修复后重新p7_code_check"
            "\n🔴 tp文件映射关系(V4.12.2): "
            "tp_NNN.json对应TP-(N+1), 例: tp_006.json→测试点TP-007 | "
            "修复后必须先 p6_merge 再 p7_code_check, "
            "直接修tp文件后不merge会导致P7检查的是旧合并结果")

    # 写入p7_output.json (V4.11.0)
    p7_out_path = os.path.join(data_dir, "p7_output.json")
    _write_json(p7_out_path, p7_output)

    # 生成HTML报告
    html_path = os.path.join(data_dir, "p7_report.html")
    _generate_p7_html_report(checks, statistics, html_path)

    # 写gate pass(仅PASS时)
    if gate_status == "PASS":
        state = TaskState(data_dir=data_dir, task_id=task_id)
        state.mark_complete("P7")
        gate_dir = os.path.join(data_dir, "gates")
        _ensure_dir(gate_dir)
        gate_path = os.path.join(gate_dir, "P7.pass.json")
        gate_data = {
            "step": "P7",
            "status": "PASS",
            "task_id": task_id,
            "source": "p7_code_check",
            "summary": summary,
            "validated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        }
        _write_signed_gate(gate_path, gate_data, task_id)

    print(json.dumps({
        "status": "ok" if gate_status == "PASS" else ("needs_review" if gate_status == "PARTIAL" else "quality_failed"),
        "gate_result": gate_status,
        "summary": summary,
        "action_required": action_required,
        "block_checks": f"{block_passed}/{block_total}",
        "warnings": warn_triggered,
        "p7_output": p7_out_path,
        "html_report": html_path,
    }))
    if gate_status not in ("PASS", "PARTIAL"):
        sys.exit(1)


def action_p7_batch_fix(args):
    """V4.12.6: 批量修复P7检测到的同类问题"""
    data_dir = args.data_dir
    check = getattr(args, 'check', '') or args.step or ''
    p6_path = os.path.join(data_dir, "p6_output.json")
    if not os.path.exists(p6_path):
        print(json.dumps({"status": "error", "reason": "p6_output.json不存在,请先执行p6_merge"}))
        sys.exit(1)
    p6_data = _read_json(p6_path)
    if isinstance(p6_data, list):
        p6_data = {"testcases": p6_data}
    cases = p6_data.get("testcases", [])
    if not cases:
        print(json.dumps({"status": "error", "reason": "无用例可修复"}))
        sys.exit(1)
    fixed = 0
    details = []
    if check == "C2":
        for c in cases:
            steps_text = _get_case_field(c, "steps", "")
            exp_text = _get_case_field(c, "expected_results", "")
            if not steps_text or not isinstance(steps_text, str):
                continue
            step_lines = [s.strip() for s in steps_text.split("\n") if s.strip()]
            exp_lines = [s.strip() for s in exp_text.split("\n") if s.strip()] if exp_text else []
            if len(step_lines) > len(exp_lines) + 1:
                missing = len(step_lines) - len(exp_lines)
                new_exps = []
                for si in range(len(exp_lines), len(step_lines)):
                    step = step_lines[si]
                    last_verb = "操作"
                    for v in ["点击", "输入", "选择", "确认", "提交", "保存", "切换", "打开"]:
                        if v in step:
                            last_verb = v
                            break
                    new_exps.append(f"{len(exp_lines)+len(new_exps)+1}. {last_verb}操作完成后,系统响应正常")
                exp_lines.extend(new_exps)
                _set_case_field(c, "expected_results", "\n".join(exp_lines))
                fixed += 1
                details.append(f"{_get_case_field(c, 'case_id', '?')}: +{missing}期望")
    elif check == "C6_1":
        for c in cases:
            pre_text = _get_case_field(c, "preconditions", "")
            if not pre_text or not isinstance(pre_text, str):
                continue
            hints = []
            if "登录" not in pre_text and "login" not in pre_text.lower():
                hints.append("[用户状态]建议补充: 已登录XX系统")
            if "环境" not in pre_text and "系统" not in pre_text and "运行" not in pre_text:
                hints.append("[环境]建议补充: XX系统正常运行")
            if hints:
                cid = _get_case_field(c, "case_id", "?")
                existing = _get_case_field(c, "remarks", "")
                hint_text = "; ".join(hints)
                new_r = f"{existing} [P7_C6_1:{hint_text}]".strip() if existing else f"[P7_C6_1:{hint_text}]"
                _set_case_field(c, "remarks", new_r)
                fixed += 1
                details.append(f"{cid}: 前置缺{'用户状态' if '用户状态' in hint_text else ''}{'环境' if '环境' in hint_text else ''}")
    else:
        print(json.dumps({"status": "error", "reason": f"不支持: {check}, 可选:C2,C6_1"}))
        sys.exit(1)
    _write_json(p6_path, {"testcases": cases})
    print(json.dumps({"status": "ok", "check": check, "fixed_count": fixed,
        "details": details[:10],
        "next_action": "执行 p6_merge 重新合并, 然后 p7_code_check 重新验证"}))


def action_quality_check(args):
    """对指定步骤的产出进行质量校验"""
    data_dir = args.data_dir
    step = args.step

    output_path = os.path.join(data_dir, f"{step.lower()}_output.json")
    if not os.path.exists(output_path):
        print(json.dumps({"status": "error", "reason": f"{step}产出文件不存在"}))
        sys.exit(1)

    data = _read_json(output_path)
    issues = []
    warnings = []

    # 1. 最小产出数量校验
    if step in MIN_OUTPUT_COUNTS:
        for field_path, min_count in MIN_OUTPUT_COUNTS[step].items():
            value = _get_nested(data, field_path)
            if value is None:
                issues.append(f"字段{field_path}不存在")
            elif isinstance(value, list) and len(value) < min_count:
                issues.append(f"{field_path}数量{len(value)}<最小要求{min_count}")
            elif isinstance(value, (int, float)) and value < min_count:
                issues.append(f"{field_path}值{value}<最小要求{min_count}")

    # 2. P0质量评分校验
    if step == "P0":
        score = data.get("quality_score", 0)
        if score < 0.5:
            issues.append(f"质量评分{score}<0.5,需求结构化质量太低")
        elif score < 0.7:
            warnings.append(f"质量评分{score}<0.7,建议补充需求")

    # 2.3 P1 scenario数量校验:每feature不得超过6个scenario
    if step == "P1":
        ft = data.get("feature_tree", {})
        modules = ft.get("modules", []) if isinstance(ft, dict) else []
        if not modules:
            modules = data.get("modules", [])
        overflow_features = []
        for m in (modules if isinstance(modules, list) else []):
            for f in m.get("children", []):
                if f.get("type") != "feature":
                    continue
                scenarios = [s for s in f.get("children", []) if s.get("type") == "scenario"]
                if len(scenarios) > 6:
                    overflow_features.append(
                        f"{f.get('id','')} {f.get('name','')} ({len(scenarios)}个scenario,超过6个限制)"
                    )
        if overflow_features:
            issues.append(
                "以下feature的scenario数量超过6个,必须合并相似场景再重新生成: "
                + "; ".join(overflow_features)
            )
        # R11修复:P1 coverage_check缺失项告警
        # 检查每个feature的scenario是否有coverage_check
        for m in (modules if isinstance(modules, list) else []):
            for f in m.get("children", []):
                if f.get("type") != "feature":
                    continue
                for s in f.get("children", []):
                    if s.get("type") == "scenario":
                        cc = s.get("coverage_check", {})
                        if cc and isinstance(cc, dict):
                            missing_ops = cc.get("operations_covered", {}).get("missing", [])
                            missing_st = cc.get("state_transitions_covered", {}).get("missing", [])
                            missing_rules = cc.get("rules_covered", {}).get("missing", [])
                            total_missing = len(missing_ops) + len(missing_st) + len(missing_rules)
                            if total_missing > 0:
                                warnings.append(
                                    f"场景 {s.get('id', '')} coverage_check有{total_missing}个未覆盖项"
                                    f"(操作:{len(missing_ops)}, 状态:{len(missing_st)}, 规则:{len(missing_rules)})"
                                )

    # 2.5 V3.2.8: P2测试点数量动态校验 = max(8, P1叶节点数×2)
    if step == "P2":
        test_points = data.get("test_points", [])
        p2_count = len(test_points) if isinstance(test_points, list) else 0
        p1_path = os.path.join(data_dir, "p1_output.json")
        p2_dynamic_min = 8
        if os.path.exists(p1_path):
            try:
                p1_data = _read_json(p1_path)
                # 计算P1叶节点数(场景数)
                ft = p1_data.get("feature_tree", {})
                modules = ft.get("modules", p1_data.get("modules", [])) if isinstance(ft, dict) else p1_data.get("modules", [])  # Bugfix V4.6.8: feature_tree可能是list
                leaf_count = 0
                for m in (modules if isinstance(modules, list) else []):
                    features = m.get("features", [])
                    for f in (features if isinstance(features, list) else []):
                        scenarios = f.get("scenarios", [])
                        leaf_count += len(scenarios) if isinstance(scenarios, list) else 1
                    if not features:
                        leaf_count += 1  # 模块本身算一个叶节点
                p2_dynamic_min = max(8, leaf_count * 2)
            except Exception:
                pass
        if p2_count < p2_dynamic_min:
            issues.append(f"测试点数量{p2_count}<最低要求{p2_dynamic_min}(P1叶节点×2),每个场景应至少生成2个测试点")

    # 3. P6用例质量校验(V3.2.4: 使用_get_case_field兼容fields嵌套结构)
    if step == "P6":
        cases = data.get("testcases", [])
        total = len(cases)

        # V3.2.8: 动态计算P6最低用例数
        # 优先用P5的total_expected_cases(基于complexity标签精确计算)
        # 其次用P5测试点数×1.5(V3.2.7兼容)
        # 底线15
        p5_min = 15
        p5_path = os.path.join(data_dir, "p5_output.json")
        if os.path.exists(p5_path):
            try:
                p5_data = _read_json(p5_path)
                p5_count = len(p5_data.get("test_points", []))
                # V3.2.8: 优先用complexity标签的精确预算
                total_expected = p5_data.get("coverage_summary", {}).get("total_expected_cases", 0)
                if total_expected > 0:
                    p5_min = max(15, total_expected)
                else:
                    p5_min = max(15, int(p5_count * 1.5))
            except Exception:
                pass
        if total < p5_min:
            issues.append(f"用例数量{total}<最低要求{p5_min}(P5测试点×1.5),每个测试点应至少展开为2条用例")

        if total > 0:
            smoke = sum(1 for c in cases if _is_smoke(_get_case_field(c, "is_smoke", "")))
            p0 = sum(1 for c in cases if _get_case_field(c, "priority", "").upper() in ("P0", "HIGHEST"))

            smoke_ratio = smoke / total
            p0_ratio = p0 / total

            # 冒烟比例超限→拒绝(与prep_prompt注入规则一致)
            if smoke_ratio < P6_QUALITY_RULES["smoke_ratio_min"]:
                issues.append(f"冒烟用例比例{smoke_ratio:.1%}<{P6_QUALITY_RULES['smoke_ratio_min']:.0%},不达标")
            if smoke_ratio > P6_QUALITY_RULES["smoke_ratio_max"]:
                issues.append(f"冒烟用例比例{smoke_ratio:.1%}>{P6_QUALITY_RULES['smoke_ratio_max']:.0%},过高")
            if p0_ratio > P6_QUALITY_RULES["p0_ratio_max"]:
                issues.append(f"P0优先级占比{p0_ratio:.1%}>{P6_QUALITY_RULES['p0_ratio_max']:.0%},优先级分布异常")

            # 检查是否所有用例同一优先级
            priorities = set(_get_case_field(c, "priority", "") for c in cases)
            if len(priorities) == 1 and total > 5:
                issues.append(f"所有{total}条用例都是{priorities.pop()}优先级,分布异常")

            # 每需求至少1条冒烟用例(与prep_prompt注入规则一致)
            if P6_QUALITY_RULES.get("per_requirement_smoke"):
                req_smoke = {}
                for c in cases:
                    req = _get_case_field(c, "requirement", _get_case_field(c, "module", "unknown"))
                    if req not in req_smoke:
                        req_smoke[req] = False
                    if _is_smoke(_get_case_field(c, "is_smoke", "")):
                        req_smoke[req] = True
                no_smoke_reqs = [r for r, has in req_smoke.items() if not has]
                if no_smoke_reqs and len(req_smoke) > 1:
                    warnings.append(f"{len(no_smoke_reqs)}个需求无冒烟用例: {', '.join(no_smoke_reqs[:3])}")

    passed = len(issues) == 0
    # P7失败时提供回流指引
    retry_hint = None
    if not passed and step == "P7":
        retry_hint = "P7质量自检失败,建议重新执行P6用例展开(从 prep_prompt P6 重新开始)"
    if not passed and step == "P6":
        retry_hint = "P6质量校验失败,建议重新执行P6全部批次"

    # V3.2.4新增:quality_check通过后自动创建gate文件,不再需要Agent手动创建
    # V3.2.6: 使用HMAC签名
    if passed and step in GATE_STEPS:
        task_id = args.task_id
        gate_dir = os.path.join(data_dir, "gates")
        _ensure_dir(gate_dir)
        gate_path = os.path.join(gate_dir, f"{step}.pass.json")
        if not os.path.exists(gate_path):
            gate_data = {
                "task_id": task_id,
                "step": step,
                "status": "PASS",
                "source": "quality_check",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            }
            _write_signed_gate(gate_path, gate_data, task_id)

    # V3.5.1: PRD审查增强 - P0时附带blocks_markdown和prd_issues
    prd_review_extra = {}
    if step == "P0":
        meta_path = os.path.join(data_dir, "task_meta.json")
        if os.path.exists(meta_path):
            _meta = _read_json(meta_path)
            if _meta.get("prd_quality_review", False):
                blocks_md = data.get("blocks_markdown", "")
                prd_issues_list = data.get("issues", [])
                # 截断保护
                if isinstance(blocks_md, str) and len(blocks_md) > 5000:
                    blocks_md = blocks_md[:5000] + "\n\n... (内容过长已截断)"
                # 格式兜底
                if not isinstance(prd_issues_list, list):
                    prd_issues_list = []
                prd_review_extra = {
                    "prd_review_enabled": True,
                    "blocks_markdown": blocks_md if blocks_md else "",
                    "prd_issues": prd_issues_list,
                }
                # V3.5.5: 将PRD审查结果写入文件,供用户下载
                try:
                    report_path = os.path.join(data_dir, "prd_review_report.md")
                    quality_score = data.get("quality_score", 0)
                    score_label = "PASS" if quality_score >= 0.7 else ("CONDITIONAL_PASS" if quality_score >= 0.5 else "FAIL")
                    report_lines = [
                        "# PRD审查报告\n",
                        f"**质量评分**: {quality_score} ({score_label})\n",
                        f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
                        "\n---\n",
                        "## 📋 需求结构化结果\n",
                        (blocks_md if blocks_md else "*未输出结构化内容*"),
                        "\n\n---\n",
                        "## ⚠️ 问题清单\n",
                    ]
                    if prd_issues_list:
                        report_lines.append("| 严重度 | 位置 | 类型 | 问题 | 建议 |\n")
                        report_lines.append("|--------|------|------|------|------|\n")
                        for issue in prd_issues_list:
                            if isinstance(issue, dict):
                                severity = issue.get("severity", "")
                                location = issue.get("location", "")
                                issue_type = issue.get("type", "")
                                problem = issue.get("problem", issue.get("issue", ""))
                                suggestion = issue.get("suggestion", issue.get("recommendation", ""))
                                report_lines.append(f"| {severity} | {location} | {issue_type} | {problem} | {suggestion} |\n")
                            else:
                                report_lines.append(f"| - | - | - | {issue} | - |\n")
                    else:
                        report_lines.append("*未发现问题*\n")
                    _write_text(report_path, "".join(report_lines))
                    prd_review_extra["prd_review_report_path"] = report_path
                except Exception as _e:
                    pass  # 写文件失败不影响主流程

    result = {
        "status": "ok" if passed else "quality_failed",
        "step": step,
        "passed": passed,
        "issues": issues,
        "warnings": warnings,
        "retry_hint": retry_hint,
        "gate_created": passed and step in GATE_STEPS,
    }
    result.update(prd_review_extra)
    print(json.dumps(result, ensure_ascii=False))
    if not passed:
        sys.exit(1)


# ============================================================
# Action: export_p0p1 (导出P0/P1为Markdown文件)
# ============================================================

def action_export_p0p1(args):
    """导出P0需求理解和P1功能点拆解为Markdown文件

    用于段落3完成后发送给产品经理审阅。
    """
    data_dir = args.data_dir
    skill_dir = args.skill_dir
    task_id = args.task_id

    # 检查P0和P1的gate pass
    p0_ok, p0_msg = check_gate(data_dir, "P0", task_id)
    p1_ok, p1_msg = check_gate(data_dir, "P1", task_id)

    if not p0_ok and not p1_ok:
        print(json.dumps({
            "status": "error",
            "reason": "P0和P1均未完成,无法导出"
        }))
        sys.exit(1)

    # 调用export_p0p1.py脚本
    export_script = os.path.join(skill_dir, "tools", "export_p0p1.py")
    if not os.path.exists(export_script):
        print(json.dumps({
            "status": "error",
            "reason": f"导出脚本不存在: {export_script}"
        }))
        sys.exit(1)

    output_file = os.path.join(data_dir, "p0p1_report.md")

    try:
        import subprocess
        result = subprocess.run(
            ["python3", export_script, "--data-dir", data_dir, "--output", output_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(json.dumps({
                "status": "error",
                "reason": f"导出失败: {result.stderr}"
            }))
            sys.exit(1)

        # 检查文件是否生成
        if not os.path.exists(output_file):
            print(json.dumps({
                "status": "error",
                "reason": "导出脚本执行成功但文件未生成"
            }))
            sys.exit(1)

        # 获取文件大小
        file_size = os.path.getsize(output_file)

        # V4.1.9: 读取MD文件内容,用于返回给用户
        md_path = os.path.join(data_dir, "p0p1_report.md")
        md_content = ""
        if os.path.exists(md_path):
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
            except Exception:
                pass

        # V4.1.9: 检查文件大小合理性(避免部分写入/截断问题)
        if file_size < 500:
            print(json.dumps({
                "status": "error",
                "reason": f"导出的HTML文件异常小({file_size}字节),内容可能不完整。"
            }))
            sys.exit(1)

        # 同时检查MD文件
        if os.path.exists(md_path):
            md_size = os.path.getsize(md_path)
            if md_size < 1000:
                print(json.dumps({
                    "status": "error",
                    "reason": f"导出的MD文件异常小({md_size}字节),内容可能不完整"
                }))
                sys.exit(1)

        # Bugfix V4.6.9: P0/P1评审推送(原为死代码,从未被调用)
        # V4.0.0设计:export_p0p1成功后自动推送到云端评审工具
        cloud_review = None
        runtime_key = None
        cache_path = os.path.join(args.data_dir, ".image_api_key")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    runtime_key = f.read().strip()
            except Exception:
                pass
        config = _load_cloud_config(args.skill_dir, runtime_api_key=runtime_key)
        if _should_push_to_review_tool(config):
            try:
                review_url = _push_p0p1_to_review_tool(args.data_dir, args.task_id, config)
                if review_url:
                    cloud_review = {
                        "pushed": True,
                        "review_url": review_url,
                        "message": "✅ 需求理解已推送到在线评审工具"
                    }
                else:
                    cloud_review = {
                        "pushed": False,
                        "message": "⚠️ 推送失败,已加入重试队列"
                    }
            except Exception as e:
                cloud_review = {
                    "pushed": False,
                    "message": f"⚠️ 推送异常: {str(e)[:50]}"
                }

        result_json = {
            "status": "success",
            "output_file": output_file,
            "html_file": output_file,
            "md_file": md_path,
            "file_size": file_size,
            "media_instruction": f"MEDIA:{md_path}" if md_path and os.path.exists(md_path) else None,
            "reminder": "Agent必须在对话中独占一行输出上面的MEDIA指令发送附件,否则用户收不到文件",
            "message": "需求理解与功能点拆解报告已生成(MD文件见media_instruction,必须发送附件)",
            "cloud_review": cloud_review  # Bugfix V4.6.9: 新增cloud_review字段
        }

        print(json.dumps(result_json, ensure_ascii=False))

    except subprocess.TimeoutExpired:
        print(json.dumps({
            "status": "error",
            "reason": "导出超时(30秒)"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "reason": f"导出异常: {str(e)}"
        }))
        sys.exit(1)


# ============================================================
# 主入口
# ============================================================


# ============================================================
# Action: check_image_api (验证图片理解API密码)
# ============================================================

def action_check_image_api(args):
    """验证用户输入的API密码是否正确"""
    skill_dir = args.skill_dir
    api_key = getattr(args, 'api_key', '') or ''

    if not api_key.strip():
        print(json.dumps({"status": "skipped", "reason": "未输入密码,将使用纯文本模式"}))
        return

    config = _load_image_api_config(skill_dir, api_key=api_key)

    if not config["enabled"]:
        reason = config.get("_invalid_reason", "API地址未配置")
        print(json.dumps({"status": "error", "reason": reason}))
        return

    # V3.0.3-patch1: 调用auth-check验证密码(不再用health,因为health不鉴权)
    ok, data = _check_image_api_health(config)

    if ok:
        # V3.2.0: 验证成功后缓存密码到task目录(解决Agent跨段落丢密码问题)
        # 密码只在当前task生命周期内有效,不会泄露到其他任务
        data_dir = getattr(args, 'data_dir', '') or ''
        if data_dir and os.path.isdir(data_dir):
            cache_path = os.path.join(data_dir, ".image_api_key")
            try:
                with open(cache_path, "w") as f:
                    f.write(api_key)
                os.chmod(cache_path, 0o600)  # 只有owner可读写
            except Exception:
                pass  # 缓存失败不阻塞流程
        # V4.0.0: 密码验证成功后,尝试从云端拉取知识库
        knowledge_sync_result = "未配置"
        cloud_config = _load_cloud_config(skill_dir, runtime_api_key=api_key)
        # V4.1.8: Onboarding验证成功后,将api_key持久化到cloud.json
        if api_key and api_key.strip():
            try:
                config_path = os.path.join(skill_dir, "config", "cloud.json")
                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                    if "review_tool" not in cfg:
                        cfg["review_tool"] = {}
                    cfg["review_tool"]["api_key"] = api_key.strip()
                    with open(config_path, "w", encoding="utf-8") as f:
                        json.dump(cfg, f, indent=2, ensure_ascii=False)
            except Exception:
                pass  # 写入失败不阻塞流程
        if (cloud_config.get("knowledge_api_url") or
            cloud_config.get("review_tool", {}).get("api_url") or
            cloud_config.get("experience_sync", {}).get("api_url")):
            knowledge_sync_result = _sync_knowledge_from_cloud(skill_dir, api_key, cloud_config)

        # V4.0.1: 同步评审经验
        review_exp_result = _sync_review_experience(skill_dir, api_key, cloud_config)

        print(json.dumps({
            "status": "ok",
            "message": "密码验证成功,图片理解API已启用",
            "provider": config["model"],
            "ci_configured": data.get("ci_configured", True),
            "qwen_configured": data.get("qwen_configured", False),
            "key_cached": bool(data_dir),
            "knowledge_sync": knowledge_sync_result,
            "review_experience_sync": review_exp_result,
        }))
    else:
        error = data.get("error", "unknown")
        message = data.get("message", "")
        # 精确区分密码错误/服务未配置/服务不可用
        if error == "auth_failed":
            print(json.dumps({"status": "auth_failed", "reason": "密码错误,请重新输入或回复「跳过」使用纯文本模式"}))
        elif error == "service_not_configured":
            print(json.dumps({"status": "service_error", "reason": f"API服务未配置密码验证: {message}"}))
        elif error == "connection_failed":
            print(json.dumps({"status": "service_error", "reason": f"无法连接API服务,请检查API地址: {message}"}))
        elif error == "timeout":
            print(json.dumps({"status": "service_error", "reason": "API服务响应超时,请稍后重试"}))
        else:
            print(json.dumps({"status": "service_error", "reason": f"API服务暂不可用: {message or error}"}))


# ============================================================
# Action: restart_from (从指定步骤重新开始)
# ============================================================

def _check_gate_exists(data_dir, step):
    """检查指定步骤的gate pass是否存在"""
    gates_dir = os.path.join(data_dir, "gates")
    gp = os.path.join(gates_dir, f"{step}.pass.json")
    return os.path.exists(gp)

def action_restart_from(args):
    """从指定步骤重新开始:清除该步及后续的gate pass和output"""
    data_dir = args.data_dir
    task_id = args.task_id
    step = args.step.upper()
    force = getattr(args, 'force', False)

    if step not in GATE_STEPS:
        print(json.dumps({"status": "error", "reason": f"无效步骤: {step},可选: {GATE_STEPS}"}))
        sys.exit(1)

    # 非force模式:检查gate是否存在,避免误清
    if not force:
        if not _check_gate_exists(data_dir, step):
            print(json.dumps({
                "status": "error",
                "reason": f"P{step} gate pass不存在,无需restart。请确认流程是否已到达该步骤。",
                "hint": "如需强制重置,使用 --force 参数"
            }))
            sys.exit(1)

    # 找到该步骤及后续所有步骤
    step_idx = GATE_STEPS.index(step)
    steps_to_clear = GATE_STEPS[step_idx:]

    gates_dir = os.path.join(data_dir, "gates")
    cleared = []
    for s in steps_to_clear:
        # 清除gate pass
        gp = os.path.join(gates_dir, f"{s}.pass.json")
        if os.path.exists(gp):
            os.remove(gp)
            cleared.append(f"{s}.pass.json")
        # 清除output
        for suffix in ["_output.json", "_output.tmp.json", "_output.prev.json"]:
            op = os.path.join(data_dir, f"{s.lower()}{suffix}")
            if os.path.exists(op):
                os.remove(op)
                cleared.append(f"{s.lower()}{suffix}")

    # 更新state
    state = TaskState(data_dir=data_dir, task_id=task_id)
    state.state["completed_steps"] = [s for s in state.state["completed_steps"] if s not in [st.lower() for st in steps_to_clear] and s not in steps_to_clear]
    state.save()

    # V4.8.9: P1重启时清除分批文件
    if step == "P1":
        sk_path = os.path.join(data_dir, "p1_skeleton.json")
        if os.path.exists(sk_path):
            os.remove(sk_path)
            cleared.append("p1_skeleton.json")
        features_dir = os.path.join(data_dir, "p1_features")
        if os.path.exists(features_dir):
            import shutil
            shutil.rmtree(features_dir, ignore_errors=True)
            cleared.append("p1_features/ (目录已清除)")
        agent_files = [f for f in os.listdir(data_dir) if f.startswith("p1_feature_") or f.startswith("p1_skeleton_")]
        for af in agent_files:
            af_path = os.path.join(data_dir, af)
            if os.path.isfile(af_path):
                os.remove(af_path)
                cleared.append(af)

    # V4.10.1: P6重启时清除agent_output残留
    if step == "P6":
        agent_files = [f for f in os.listdir(data_dir) if f.startswith("p6_batch_") and "_agent_output" in f]
        for af in agent_files:
            af_path = os.path.join(data_dir, af)
            if os.path.isfile(af_path):
                os.remove(af_path)
                cleared.append(af)

    print(json.dumps({
        "status": "ok",
        "restart_from": step,
        "cleared_files": cleared,
        "next_step": step,
    }))


# Action: verify_gates (验证所有gate pass状态)
# ============================================================

def action_verify_gates(args):
    """检查所有已存在的gate pass状态,用于restart前的人工确认"""
    data_dir = args.data_dir
    gates_dir = os.path.join(data_dir, "gates")
    results = {}
    missing = []
    for step in GATE_STEPS:
        gp = os.path.join(gates_dir, f"{step}.pass.json")
        if os.path.exists(gp):
            try:
                with open(gp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results[step] = {"exists": True, "step": data.get("step"), "passed_at": data.get("passed_at")}
            except:
                results[step] = {"exists": True, "error": "JSON解析失败"}
        else:
            results[step] = {"exists": False}
            missing.append(step)

    print(json.dumps({
        "status": "ok",
        "total_steps": len(GATE_STEPS),
        "existing": len(GATE_STEPS) - len(missing),
        "missing": missing,
        "gates": results,
    }))

def main():
    parser = argparse.ArgumentParser(description="V3.0 Orchestrator")
    parser.add_argument("--action", required=True, choices=[
        "init", "onboarding", "step0", "step0_8_prep", "step0_8_save",
        "step_run", "step7_export", "status", "resume",
        "prep_prompt", "p2_code_generate", "p3_p4_parallel", "p5_code_merge",
        "p6_tp_list", "p6_generate_one", "p6_batch_info", "p6_save_batch", "p6_merge", "p6_checkpoint",
        "p1_skeleton_save", "p1_save_feature", "p1_code_merge",
        "set_prd_review",
        "quality_check", "p7_code_check", "p7_batch_fix",
        "restart_from", "verify_gates", "check_image_api", "export_p0p1", "retry_push"
    ])
    parser.add_argument("--skill-dir", default="")
    parser.add_argument("--data-dir", default="")
    parser.add_argument("--task-id", default="")
    parser.add_argument("--requirement-text", default="")
    parser.add_argument("--requirement-file", default="")
    parser.add_argument("--step", default="")
    parser.add_argument("--force", action="store_true", default=False, help="restart_from时跳过gate状态检查,强制清除")
    parser.add_argument("--agent-output", default="")  # 兼容保留,优先从文件读
    parser.add_argument("--results-json", default="")  # 兼容保留,优先从文件读
    parser.add_argument("--batch-index", default="0")
    parser.add_argument("--tp-index", type=int, default=0, help="V4.11.0: P6逐条生成TP索引")
    parser.add_argument("--tp-ids", default="", help="V4.9.1: P7修复模式,指定要处理的测试点ID列表(逗号分隔)")
    parser.add_argument("--merge", action="store_true", default=False, help="V4.7.2: 增量更新模式,仅更新指定case_id的用例,保留其余")
    parser.add_argument("--api-key", default="", help="图片理解API密钥(Onboarding时用户输入,不落盘)")
    parser.add_argument("--model-name", default="", help="V4.8.0: 当前使用的模型名称(用于LOW模型自适应)")
    parser.add_argument("--feature-id", default="", help="V4.8.9: P1分批生成 - 功能点ID")
    parser.add_argument("--mode", default="", help="V4.8.9: P1骨架生成模式(skeleton)")
    parser.add_argument("--enabled", default="true", help="V3.5.1: PRD审查开关(true/false)")

    args = parser.parse_args()

    # === V3.0.0-patch3: 参数自动化 ===
    # 1. skill_dir自动发现
    try:
        args.skill_dir = resolve_skill_dir(args.skill_dir)
    except ValueError as e:
        print(json.dumps({"status": "error", "reason": str(e)}))
        sys.exit(1)

    # 2. data_dir/task_id自动回填(非init action时)
    if args.action != "init":
        if not args.data_dir or not args.task_id:
            auto_tid, auto_dir = find_latest_task()
            if auto_tid and auto_dir:
                if not args.task_id:
                    args.task_id = auto_tid
                if not args.data_dir:
                    args.data_dir = auto_dir
            else:
                if args.action not in ("status",):
                    print(json.dumps({"status": "error", "reason": "未找到活跃任务,请先执行 --action init"}))
                    sys.exit(1)

    # 3. agent-output从文件读取(优先级:文件 > 命令行参数)
    if args.action in ("step_run", "p6_save_batch", "p1_skeleton_save", "p1_save_feature") and not args.agent_output:
        step = args.step or "unknown"
        if args.action == "p6_save_batch":
            batch_idx = int(args.batch_index) if args.batch_index else 0  # V4.8.12: 0-based
            agent_file = os.path.join(args.data_dir, f"p6_batch_{batch_idx:03d}_agent_output.json")
        elif args.action == "p1_skeleton_save":
            agent_file = os.path.join(args.data_dir, "p1_skeleton_agent_output.json")
        elif args.action == "p1_save_feature":
            fid = getattr(args, 'feature_id', '')
            safe_fid = fid.replace("/", "_").replace("\\", "_")
            agent_file = os.path.join(args.data_dir, f"p1_feature_{safe_fid}_agent_output.json")
        else:
            agent_file = os.path.join(args.data_dir, f"{step.lower()}_agent_output.json")
        if os.path.exists(agent_file):
            args.agent_output = _read_file_safe(agent_file, 100000)

    # 4. results-json从文件读取
    if args.action == "step0_8_save" and not args.results_json:
        results_file = os.path.join(args.data_dir, "px_agent_results.json")
        if os.path.exists(results_file):
            args.results_json = _read_file_safe(results_file, 100000)

    actions = {
        "init": action_init,
        "onboarding": action_onboarding,
        "step0": action_step0,
        "step0_8_prep": action_step0_8_prep,
        "step0_8_save": action_step0_8_save,
        "step_run": action_step_run,
        "step7_export": action_step7_export,
        "status": action_status,
        "resume": action_resume,
        "prep_prompt": action_prep_prompt,
        "p2_code_generate": action_p2_code_generate,
        "p3_p4_parallel": action_p3_p4_parallel,
        "p5_code_merge": action_p5_code_merge,
        "p6_tp_list": action_p6_tp_list,
        "p6_generate_one": action_p6_generate_one,
        "p6_batch_info": action_p6_batch_info,
        "p6_save_batch": action_p6_save_batch,
        "p6_merge": action_p6_merge,
        "p6_checkpoint": action_p6_checkpoint,
        "p1_skeleton_save": action_p1_skeleton_save,
        "p1_save_feature": action_p1_save_feature,
        "p1_code_merge": action_p1_code_merge,
        "set_prd_review": action_set_prd_review,
        "quality_check": action_quality_check,
        "p7_code_check": action_p7_code_check,
        "p7_batch_fix": action_p7_batch_fix,
        "restart_from": action_restart_from,
        "verify_gates": action_verify_gates,
        "check_image_api": action_check_image_api,
        "export_p0p1": action_export_p0p1,
        "retry_push": action_retry_push,
    }

    try:
        # V3.5.2: 设置全局变量,记录当前执行的action
        global _CURRENT_ACTION
        _CURRENT_ACTION = args.action
        actions[args.action](args)
    except SystemExit:
        raise
    except Exception as e:
        print(json.dumps({"status": "error", "reason": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
