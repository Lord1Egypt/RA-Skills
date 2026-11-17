#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-prompt（元引）—— 零依赖意图澄清与生态入口引擎
========================================================

跨智能体的「意图澄清 + 生态入口」能力：用户输入一句模糊的话 / 一个词时，
本引擎帮他把意图识别出来，给出 2-4 个候选方向；选定后深挖（目标 / 范围 /
输出 / 约束），再串联到对应元阁技能，输出能直接运行的提示词。

它不是 prompt 美化器：不做文本润色、不堆形容词、不套模板；只做
「把模糊的话补全成可执行任务」这一件事（生态的门，不是 standalone 工具）。

特性
----
- 十个意图域：dev / analysis / planning / memory / security / logs / learning / writing / quality / general
- 关键词加权意图分类（中文 + 英文，纯本地离线，不联网）
- 直接识别技能名（yotta-* / 元X）并锁定到对应意图域
- 候选方向 2-4 个，各带一句中文说明；不足 2 个时补「通用引导」
- map：方向 / 技能名 → 元阁技能 + 安装命令 + 可直接运行的提示词模板
- scenarios：内置常见场景案例（模糊输入 → 候选 → 深挖 → 串联）
- 输出 text / JSON；退出码 0 / 1 / 4（沿用元阁 CLI 惯例）

用法
----
  python3 scripts/yotta_prompt.py clarify "帮我写一封邮件"
  python3 scripts/yotta_prompt.py clarify "记一下这个" --json
  python3 scripts/yotta_prompt.py clarify "怎么学 python" --top 3
  python3 scripts/yotta_prompt.py map 写作
  python3 scripts/yotta_prompt.py map yotta-humanize --json
  python3 scripts/yotta_prompt.py scenarios
  python3 scripts/yotta_prompt.py --version

退出码：
  clarify / map / scenarios：0 = 成功；1 = 未识别（已给引导）；4 = 用法或读取错误。
Windows 下用 python 代替 python3。
"""

import argparse
import json
import sys

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.2.6"
TOOL = "yotta-prompt"
TOOL_CN = "元引"

MAX_CANDIDATES = 4
MIN_CANDIDATES = 2

# ---------------------------------------------------------------------------
# 元阁技能台账（map 输出的权威映射；中文名以《技能登记表》为准）
# ---------------------------------------------------------------------------
SKILLS = {
    "yotta-memory":          {"cn": "元忆", "tagline": "有权限边界的文件式智能体记忆（记一笔 / 别忘 / 跨会话）", "domain": "memory"},
    "yotta-workflow":        {"cn": "元序", "tagline": "跨会话 / 跨项目通用工作流协议（开工读状态 / 收工留锚点）", "domain": "memory"},
    "yotta-code-quality":    {"cn": "元质", "tagline": "结对式代码质量评审（十二类腐化风险 + 健康分）", "domain": "dev"},
    "yotta-guardian":        {"cn": "元盾", "tagline": "危险调用拦截（exec / write / shell 等工具调用护栏）", "domain": "dev"},
    "yotta-humanize":        {"cn": "元真", "tagline": "中文去 AI 味：检测 + 确定性改写（写邮件 / 润色 / 降噪）", "domain": "writing"},
    "yotta-anti-shallow":    {"cn": "元谨", "tagline": "防敷衍规则引擎（认真 / 严谨 / 全链路验证）", "domain": "quality"},
    "yotta-learn":           {"cn": "元习", "tagline": "自我改进学习循环（记一笔，下次可复用）", "domain": "learning"},
    "yotta-logs":            {"cn": "元史", "tagline": "零依赖会话 / 日志检索（定位 / 检索 / 提取 / 统计）", "domain": "logs"},
    "yotta-logwatch":        {"cn": "元察", "tagline": "系统日志监控（文件 / 目录 / Windows 事件日志）", "domain": "logs"},
    "yotta-security-audit":  {"cn": "元安", "tagline": "技能 / 系统安全审计扫描（13 类检测器，只读）", "domain": "security"},
    "yotta-vetter":          {"cn": "元审", "tagline": "技能安装前审查协议（来源 / 代码 / 权限 / 风险）", "domain": "security"},
    "yotta-secret":          {"cn": "元钥", "tagline": "密钥与凭据泄露扫描（云凭据 / 私钥 / URL 内嵌 / 高熵）", "domain": "security"},
    "yotta-chain":           {"cn": "元链", "tagline": "供应链依赖校验（依赖混淆 / lockfile 一致性 / SBOM-lite）", "domain": "security"},
    "yotta-triage":          {"cn": "元鉴", "tagline": "恶意样本静态初筛（hash / 熵 / 字符串 / PE-ELF 头）", "domain": "security"},
    "yotta-intel":           {"cn": "元情", "tagline": "威胁情报 IOC 提取与规范化（IP / 域名 / URL / 哈希 / CVE）", "domain": "security"},
    "yotta-recon":           {"cn": "元析", "tagline": "零依赖网络侦察（端口 / 服务 / 版本指纹，仅授权环境）", "domain": "security"},
}

# 技能别名（slug 与中文名）→ 所属意图域；clarify 命中时锁定该方向
SKILL_ALIAS = {}
for _slug, _info in SKILLS.items():
    SKILL_ALIAS[_slug] = _info["domain"]
    SKILL_ALIAS[_info["cn"]] = _info["domain"]

# ---------------------------------------------------------------------------
# 意图域定义（顺序即候选排序的稳定次序）
# ---------------------------------------------------------------------------
DOMAINS = [
    {
        "id": "dev",
        "label_zh": "开发与代码",
        "label_en": "Development & Code",
        "ask": "你想解决什么具体问题：写新代码、修 bug、重构，还是做代码质量评审？涉及什么语言 / 框架？",
        "skills": ["yotta-code-quality", "yotta-guardian"],
        "keywords": [
            ("写代码", 4), ("写个程序", 4), ("写个脚本", 4), ("代码", 3), ("编程", 3),
            ("程序", 2), ("函数", 2), ("重构", 4), ("优化代码", 4), ("代码优化", 4),
            ("bug", 4), ("报错", 3), ("调试", 4), ("debug", 4), ("单测", 3), ("单元测试", 3),
            ("测试用例", 3), ("接口", 2), ("api", 2), ("前端", 2), ("后端", 2), ("脚本", 2),
            ("code", 3), ("coding", 3), ("program", 2), ("refactor", 4), ("function", 2),
            ("代码质量", 5), ("审查代码", 4), ("审代码", 4), ("代码审查", 4),
        ],
    },
    {
        "id": "analysis",
        "label_zh": "数据与整理",
        "label_en": "Data & Organization",
        "ask": "要处理什么数据 / 材料？希望得到什么（表格 / 统计 / 汇总 / 结论）？数据从哪来、范围多大？",
        "skills": [],
        "keywords": [
            ("表格", 4), ("excel", 4), ("数据", 3), ("统计", 4), ("汇总", 4), ("整理", 3),
            ("分析", 3), ("报表", 4), ("数据可视化", 4), ("图表", 3), ("透视表", 4),
            ("筛选", 3), ("排序", 3), ("对比", 2), ("指标", 3), ("看板", 4),
            ("data", 3), ("analysis", 3), ("spreadsheet", 3),
        ],
    },
    {
        "id": "planning",
        "label_zh": "计划与组织",
        "label_en": "Planning & Organizing",
        "ask": "要计划 / 组织什么？目标是什么、什么时候要完成、有哪些约束 / 依赖？",
        "skills": [],
        "keywords": [
            ("计划", 4), ("规划", 4), ("安排", 4), ("项目", 3), ("进度", 4), ("排期", 4),
            ("流程", 3), ("sop", 4), ("目标", 3), ("拆解", 4), ("里程碑", 4), ("日程", 3),
            ("时间表", 4), ("待办", 3), ("清单", 3), ("方案", 3), ("策划", 4), ("头脑风暴", 5),
            ("创意", 3), ("plan", 3), ("schedule", 3), ("milestone", 3), ("roadmap", 3),
            ("checklist", 3),
        ],
    },
    {
        "id": "memory",
        "label_zh": "记忆与跨会话",
        "label_en": "Memory & Cross-session",
        "ask": "想记下什么信息？希望下次会话还能想起它吗？它属于公共共享、个人偏好还是私密信息？",
        "skills": ["yotta-memory", "yotta-workflow"],
        "keywords": [
            ("记住", 5), ("记一笔", 5), ("记一下", 5), ("别忘了", 5), ("别忘", 5), ("备忘", 4),
            ("记忆", 4), ("回忆", 4), ("上次说到", 5), ("上次", 3), ("上下文", 4), ("交接", 4),
            ("跨会话", 5), ("续上", 4), ("归档", 3), ("remember", 4), ("memory", 4),
            ("recall", 4), ("handoff", 4), ("context", 3), ("忘记", 3), ("想不起来", 4),
        ],
    },
    {
        "id": "security",
        "label_zh": "安全与合规",
        "label_en": "Security & Compliance",
        "ask": "具体是哪类安全需求：代码 / 技能审计、密钥泄露扫描、供应链校验、样本初筛、威胁情报，还是网络侦察？涉及什么对象？",
        "skills": [
            "yotta-security-audit", "yotta-vetter", "yotta-secret", "yotta-chain",
            "yotta-triage", "yotta-intel", "yotta-logwatch", "yotta-recon",
        ],
        "keywords": [
            ("安全", 3), ("审计", 4), ("密钥", 5), ("凭据", 5), ("泄露", 4), ("泄漏", 4),
            ("扫描", 3), ("漏洞", 4), ("恶意", 4), ("病毒", 4), ("木马", 4), ("样本", 4),
            ("供应链", 4), ("依赖", 3), ("威胁情报", 5), ("ioc", 5), ("钓鱼", 4), ("入侵", 4),
            ("加固", 4), ("渗透", 4), ("授权测试", 4), ("红队", 3), ("蓝队", 3), ("合规", 3),
            ("弱口令", 4), ("后门", 4), ("security", 4), ("audit", 4), ("secret", 5),
            ("credential", 5), ("malware", 4), ("virus", 4), ("trojan", 4), ("sample", 3),
            ("supply", 3), ("chain", 2), ("threat", 4), ("intel", 3), ("phishing", 4),
            ("pentest", 4), ("等保", 4), ("密评", 4),
        ],
    },
    {
        "id": "logs",
        "label_zh": "日志与运维",
        "label_en": "Logs & Operations",
        "ask": "要查哪里的日志？想找什么（错误 / 关键字 / 某段时间）？希望输出什么（匹配行 / 统计 / 报告）？",
        "skills": ["yotta-logs", "yotta-logwatch"],
        "keywords": [
            ("日志", 5), ("查日志", 5), ("查看日志", 5), ("日志分析", 5), ("检索日志", 5),
            ("日志检索", 5), ("日志统计", 4), ("报错日志", 5), ("排障", 4), ("故障", 3),
            ("排查", 3), ("运行状态", 3), ("状态", 2), ("log", 4), ("logs", 4),
            ("troubleshoot", 4), ("排查问题", 4),
        ],
    },
    {
        "id": "learning",
        "label_zh": "学习与教学",
        "label_en": "Learning & Teaching",
        "ask": "想学什么主题？当前基础如何？希望怎么学（概念讲解 / 例子 / 练习 / 复习）？",
        "skills": ["yotta-learn"],
        "keywords": [
            ("学习", 4), ("学会", 4), ("入门", 4), ("概念", 4), ("教程", 4), ("教学", 4),
            ("讲给我", 4), ("解释一下", 4), ("解释", 3), ("了解", 2), ("复习", 3),
            ("learn", 4), ("study", 3), ("explain", 4), ("tutorial", 4), ("concept", 4),
            ("teach", 4), ("知识", 2), ("原理", 3), ("怎么理解", 4), ("科普", 3),
        ],
    },
    {
        "id": "writing",
        "label_zh": "写作与语言",
        "label_en": "Writing & Language",
        "ask": "要写 / 改什么内容？给谁看？语气是正式还是亲切？希望多长？",
        "skills": ["yotta-humanize"],
        "keywords": [
            ("写邮件", 5), ("邮件", 4), ("写作", 4), ("润色", 5), ("降噪", 5), ("去ai味", 5),
            ("ai味", 4), ("口语化", 4), ("文案", 4), ("文章", 3), ("报告", 3), ("总结", 3),
            ("改写", 4), ("措辞", 4), ("表达", 3), ("口吻", 3), ("语气", 3), ("文风", 4),
            ("朋友圈", 3), ("小红书", 3), ("公文", 3), ("通知", 2), ("write", 4),
            ("email", 4), ("polish", 4), ("rewrite", 4), ("tone", 3), ("copy", 3),
        ],
    },
    {
        "id": "quality",
        "label_zh": "严谨与质量",
        "label_en": "Rigor & Quality",
        "ask": "要对什么把关：一份代码、一篇文档、一个结论，还是整套交付？最担心哪类问题（敷衍 / 漏检 / 不一致）？",
        "skills": ["yotta-anti-shallow", "yotta-code-quality"],
        "keywords": [
            ("认真", 4), ("严谨", 4), ("别敷衍", 5), ("敷衍", 4), ("仔细", 4), ("检查", 3),
            ("核对", 4), ("自检", 4), ("质量", 3), ("评审", 4), ("代码评审", 5), ("review", 4),
            ("rigorous", 4), ("careful", 3), ("check", 3), ("quality", 3), ("结对评审", 5),
            ("发版前", 4), ("把关", 3), ("校验", 3), ("深度", 2), ("全面", 2),
        ],
    },
    {
        "id": "general",
        "label_zh": "通用与入门",
        "label_en": "General & Getting Started",
        "ask": "没关系，先聊聊你手上想解决的事：它是关于写东西、查东西、记东西，还是别的？",
        "skills": [],
        "keywords": [],
    },
]

DOMAIN_BY_ID = {d["id"]: d for d in DOMAINS}

# 每个意图域一条「可直接运行的提示词模板」（map 输出；<占位> 由用户填写）
PROMPTS = {
    "dev": "请帮我【写 / 修 / 重构】一段代码：功能 <功能描述>，语言 / 框架 <语言>，约束 <限制>。先给出方案再写，写完自查可读性、边界情况与潜在 bug，并按代码质量评审标准（可读性 / 一致性 / 边界 / 冗余）过一遍。（若已安装元质 yotta-code-quality，请按它的十二类风险标准评审）",
    "memory": "请把 <要记住的信息> 记入我的长期记忆：标注类型（公共共享 / 个人偏好 / 私密），说明后续如何回忆，并在本会话收工时归档。（若已安装元忆 yotta-memory，请用它的 CLI 写入并声明身份）",
    "security": "请对 <目标对象> 做一次安全自查：先明确授权范围，再按类型（审计 / 密钥 / 供应链 / 样本 / 情报 / 日志 / 侦察）执行，输出结构化报告；不得做未授权入侵测试。（若已安装对应元阁安全技能，请优先用其引擎）",
    "logs": "请检索 <日志位置>：关键词 <关键字>，时间范围 <范围>，输出 <匹配行 / 统计 / 报告>。（若已安装元史 yotta-logs，请用它的检索 CLI）",
    "learning": "请帮我学习 <主题>：先讲清核心概念与原理，给 2-3 个例子，再出一个练习并给反馈；把新知识点记入长期记忆。（若已安装元习 yotta-learn，请按它的学习循环执行）",
    "writing": "请以中文帮我写 / 润色 <内容>：目的 <目的>，读者 <对象>，语气 <风格>，长度 <限制>。写完后自查 AI 味（少用「首先 / 其次 / 此外」等套话、避免过度正式、别每段都总结）并按需改写。（若已安装元真 yotta-humanize，请先跑它的检测评分再改写）",
    "quality": "请认真、严谨地完成 <任务>：先分析、再执行、后自检，逐条核对是否有敷衍 / 漏检 / 不一致。（若已安装元谨 yotta-anti-shallow，请按它的规则引擎自检；涉及代码另按元质 yotta-code-quality 结对评审）",
    "analysis": "请帮我处理这份数据 / 材料 <来源>：目标 <要得到什么>，输出 <表格 / 统计 / 汇总 / 结论>。先说明处理思路，再给出结构化结果；涉及敏感信息请先脱敏。",
    "planning": "请帮我制定 <计划主题>：目标 <目标>，期限 <时间>，约束 <限制>。拆解成可执行步骤与里程碑，标出依赖与风险，并给一个待办清单。",
    "general": "我现在还不太清楚想要什么，请先问我 2-3 个问题帮我理清目标（要什么结果 / 与什么相关 / 输出形态），再给出可执行方案；如果合适，推荐一个元阁技能。",
}

# ---------------------------------------------------------------------------
# 内置场景案例（完整逐场景示例见 references/scenarios.md）
# ---------------------------------------------------------------------------
SCENARIOS = [
    {"id": "email",        "title": "想写一封邮件",   "input": "帮我写个邮件",          "domain": "writing",  "skill": "yotta-humanize"},
    {"id": "learn-concept", "title": "想学一个概念",  "input": "机器学习是啥",          "domain": "learning", "skill": "yotta-learn"},
    {"id": "remember",     "title": "怕忘事",         "input": "帮我记住这个",          "domain": "memory",   "skill": "yotta-memory"},
    {"id": "troubleshoot", "title": "看日志排障",     "input": "日志里好像报错了",       "domain": "logs",     "skill": "yotta-logs"},
    {"id": "code-bug",     "title": "代码有 bug",     "input": "这段代码为什么报错",     "domain": "dev",      "skill": "yotta-code-quality"},
    {"id": "secret-scan",  "title": "查密钥泄露",     "input": "看看项目里有没有密钥",   "domain": "security", "skill": "yotta-secret"},
    {"id": "de-ai",        "title": "去 AI 味",       "input": "写的东西一股 AI 味",     "domain": "writing",  "skill": "yotta-humanize"},
    {"id": "rigor",        "title": "要严谨",         "input": "认真点别敷衍",           "domain": "quality",  "skill": "yotta-anti-shallow"},
    {"id": "no-idea",      "title": "不知道问什么",   "input": "我不知道怎么问",         "domain": "general",  "skill": None},
    {"id": "weekly-report", "title": "写周报 / 总结",   "input": "帮我把这周的工作写成周报", "domain": "writing",  "skill": None},
    {"id": "data-table",    "title": "做表格整理数据", "input": "帮我整理数据做个表格",     "domain": "analysis", "skill": None},
    {"id": "learn-plan",    "title": "制定学习计划",   "input": "帮我定个学习计划",         "domain": "planning", "skill": None},
    {"id": "speech",        "title": "写演讲稿 / 述职", "input": "帮我写个述职演讲稿",       "domain": "writing",  "skill": None},
    {"id": "translate",     "title": "翻译文档",       "input": "帮我翻译这段英文",         "domain": "writing",  "skill": None},
    {"id": "meeting-notes", "title": "整理会议纪要",   "input": "把会议内容整理成纪要",     "domain": "writing",  "skill": None},
    {"id": "contract",      "title": "审阅合同 / 文书", "input": "帮我审一下这份合同",       "domain": "quality",  "skill": None},
    {"id": "brainstorm",    "title": "头脑风暴 / 策划", "input": "帮我想几个活动创意",       "domain": "planning", "skill": None},
    {"id": "interview",     "title": "准备面试",       "input": "帮我准备后端面试",         "domain": "learning", "skill": None},
]


def normalize(text):
    """小写并合并空白，便于关键词子串匹配。"""
    return " ".join(str(text).lower().split())


def score_domains(text):
    """对输入做关键词加权评分；返回 {domain_id: {score, matched, pinned}}。"""
    t = normalize(text)
    out = {}
    for d in DOMAINS:
        s = 0
        matched = []
        for kw, w in d["keywords"]:
            if kw in t:
                s += w
                matched.append(kw)
        if s > 0:
            out[d["id"]] = {"score": s, "matched": matched, "pinned": []}
    for alias, dom_id in SKILL_ALIAS.items():
        if alias in t:
            rec = out.setdefault(dom_id, {"score": 0, "matched": [], "pinned": []})
            rec["score"] += 100
            rec["pinned"].append(alias)
    return out


def _domain_index(dom_id):
    for i, d in enumerate(DOMAINS):
        if d["id"] == dom_id:
            return i
    return len(DOMAINS)


def _reason(d, info, lang):
    if info.get("pinned"):
        return "输入直接提到了技能「%s」，锁定到该方向" % "、".join(info["pinned"])
    if info.get("matched"):
        return "命中关键词：" + "、".join(info["matched"][:4])
    return d["label_zh"] if lang == "zh" else d["label_en"]


def candidates_for(text, top=4, lang="zh"):
    """返回 2-4 个候选方向；不足 2 个时补「通用与入门」。"""
    scores = score_domains(text)
    ordered = [d for d in DOMAINS if d["id"] in scores]
    ordered.sort(key=lambda d: (-scores[d["id"]]["score"], _domain_index(d["id"])))
    limit = max(MIN_CANDIDATES, min(int(top), MAX_CANDIDATES))
    cands = []
    for d in ordered:
        if len(cands) >= limit:
            break
        info = scores[d["id"]]
        cands.append({
            "id": d["id"],
            "label_zh": d["label_zh"],
            "label_en": d["label_en"],
            "reason": _reason(d, info, lang),
            "matched": info.get("matched", [])[:4],
            "skills": ["%s %s" % (SKILLS[s]["cn"], s) for s in d["skills"]],
        })
    if len(cands) < MIN_CANDIDATES:
        g = DOMAIN_BY_ID["general"]
        cands.append({
            "id": "general",
            "label_zh": g["label_zh"],
            "label_en": g["label_en"],
            "reason": "还没想清楚，先从通用引导开始",
            "matched": [],
            "skills": [],
        })
    return cands


# ---------------------------------------------------------------------------
# map：方向 / 技能名 → 元阁技能 + 安装命令 + 提示词
# ---------------------------------------------------------------------------
def resolve_map(query):
    q = normalize(query)
    for slug, info in SKILLS.items():
        if q in (slug, info["cn"], info["cn"][1:]):
            return {"kind": "skill", "domain": info["domain"], "skills": [slug]}
    for d in DOMAINS:
        if q in (d["id"], d["label_zh"], d["label_en"]) or q in d["label_zh"] or q in d["label_en"]:
            return {"kind": "domain", "domain": d["id"], "skills": list(d["skills"])}
    scores = score_domains(query)
    if scores:
        best = max(scores, key=lambda k: (scores[k]["score"], -_domain_index(k)))
        return {"kind": "domain", "domain": best, "skills": list(DOMAIN_BY_ID[best]["skills"]), "by_keyword": True}
    return None


def map_result(query):
    res = resolve_map(query)
    if res is None:
        return None
    dom = DOMAIN_BY_ID[res["domain"]]
    skills = []
    for slug in res["skills"]:
        info = SKILLS[slug]
        skills.append({
            "slug": slug,
            "cn": info["cn"],
            "tagline": info["tagline"],
            "install": "npx -y @yottameta/%s -g" % slug,
        })
    prompt = PROMPTS[res["domain"]]
    if res["kind"] == "skill" and len(res["skills"]) == 1:
        slug = res["skills"][0]
        prompt = "请用%s %s 处理：<具体任务>。%s" % (SKILLS[slug]["cn"], slug, prompt)
    return {
        "tool": TOOL,
        "version": VERSION,
        "query": query.strip(),
        "kind": res["kind"],
        "domain": {"id": dom["id"], "label_zh": dom["label_zh"], "label_en": dom["label_en"]},
        "skills": skills,
        "prompt": prompt,
    }


# ---------------------------------------------------------------------------
# 渲染（text 模式）
# ---------------------------------------------------------------------------
def render_clarify(text, cands, lang="zh"):
    lines = ["%s %s v%s —— 意图澄清" % (TOOL_CN, TOOL, VERSION)]
    lines.append("输入：「%s」" % text)
    lines.append("")
    lines.append("我猜你想做这几件事（回复数字选择，或直接说出你的选择）：")
    lines.append("")
    for i, c in enumerate(cands, 1):
        label = c["label_en"] if lang == "en" else c["label_zh"]
        lines.append("%d. %s（%s）" % (i, label, c["id"]))
        lines.append("   · %s" % c["reason"])
        if c["skills"]:
            lines.append("   · 可串联：" + "、".join(c["skills"]))
    lines.append("")
    lines.append('输入 `yotta-prompt map <方向>` 可查看可串联的技能与可直接运行的提示词。')
    return "\n".join(lines)


UNRECOGNIZED_DOMAIN_IDS = ("writing", "dev", "analysis")


def _unrecognized_questions(lang="zh"):
    if lang == "en":
        return [
            {"id": "outcome", "question": "What final result do you want?"},
            {"id": "domain", "question": "What topic or field is this about?"},
            {"id": "format", "question": "What output form and length do you want?"},
        ]
    return [
        {"id": "outcome", "question": "你希望得到的最终结果是什么？"},
        {"id": "domain", "question": "这件事的主题或领域是什么？"},
        {"id": "format", "question": "你希望的输出形式和长度是什么？"},
    ]


def _unrecognized_choices(lang="zh"):
    out = []
    for dom_id in UNRECOGNIZED_DOMAIN_IDS:
        d = DOMAIN_BY_ID[dom_id]
        out.append({
            "id": dom_id,
            "label": d["label_en"] if lang == "en" else d["label_zh"],
        })
    return out


def _unrecognized_template(text, lang="zh"):
    if lang == "en":
        return (
            "Please clarify my request before taking action.\n"
            "Original input: \"%s\"\n\n"
            "1. Final result: [fill in]\n"
            "2. Topic / field: [fill in]\n"
            "3. Output form and length: [fill in]\n\n"
            "If the information is still incomplete, offer 2-4 candidate directions, "
            "recommend one, and ask me to choose."
        ) % text
    return (
        "我想请你先帮我澄清需求，不要直接执行。\n"
        "我的原始输入：「%s」\n\n"
        "1. 最终结果：[填写]\n"
        "2. 主题/领域：[填写]\n"
        "3. 输出形式与长度：[填写]\n\n"
        "如果信息仍不足，请给出 2-4 个候选方向并推荐一个，再让我选择。"
    ) % text


def render_unrecognized(text, lang="zh"):
    lines = ["%s %s v%s —— 意图澄清" % (TOOL_CN, TOOL, VERSION)]
    lines.append("输入：「%s」" % text)
    lines.append("")
    lines.append("我暂时没能识别出你的意图。没关系，再给我一点信息，比如：")
    lines.append("请复制下面这段补充信息，直接回复即可：")
    lines.append("")
    lines.append("我想请你先帮我澄清需求，不要直接执行。")
    lines.append("我的原始输入：「%s」" % text)
    lines.append("")
    for i, item in enumerate(_unrecognized_questions(lang), 1):
        label = "Final result" if lang == "en" and item["id"] == "outcome" else (
            "Topic / field" if lang == "en" and item["id"] == "domain" else (
                "Output form and length" if lang == "en" else
                {"outcome": "最终结果", "domain": "主题/领域", "format": "输出形式与长度"}[item["id"]]
            )
        )
        lines.append("%d. %s：[填写]" % (i, label))
    lines.append("")
    lines.append("也可以从这些常见方向里选一个：")
    for label, item in zip(("A", "B", "C"), _unrecognized_choices(lang)):
        lines.append("%s. %s（%s）" % (label, item["label"], item["id"]))
    return "\n".join(lines)


def render_map(res, lang="zh"):
    dom_label = res["domain"]["label_en"] if lang == "en" else res["domain"]["label_zh"]
    lines = ["%s %s v%s —— 方向映射" % (TOOL_CN, TOOL, VERSION)]
    lines.append("查询：「%s」→ 方向：%s（%s）" % (res["query"], dom_label, res["domain"]["id"]))
    lines.append("")
    lines.append("可串联的元阁技能：")
    for i, s in enumerate(res["skills"], 1):
        lines.append("%d. %s %s —— %s" % (i, s["cn"], s["slug"], s["tagline"]))
        lines.append("   安装：%s" % s["install"])
    lines.append("")
    lines.append("")
    lines.append("提示：以上技能为可选加速器——提示词本身不依赖它们已安装；未安装也能直接用，装了效果更好。")
    lines.append("")
    lines.append("可直接运行的提示词：")
    lines.append(res["prompt"])
    return "\n".join(lines)


def render_map_miss(query):
    lines = ["%s %s v%s —— 方向映射" % (TOOL_CN, TOOL, VERSION)]
    lines.append("未找到与「%s」匹配的方向或技能。" % query)
    lines.append("可用方向：开发与代码 / 记忆与跨会话 / 安全与合规 / 日志与运维 / 学习与教学 / 写作与语言 / 严谨与质量。")
    lines.append("可用技能：yotta-memory、yotta-workflow、yotta-code-quality、yotta-guardian、yotta-humanize、")
    lines.append("yotta-anti-shallow、yotta-learn、yotta-logs、yotta-logwatch、yotta-security-audit、yotta-vetter、")
    lines.append("yotta-secret、yotta-chain、yotta-triage、yotta-intel、yotta-recon。")
    return "\n".join(lines)


def render_scenarios(lang="zh"):
    lines = ["%s %s v%s —— 内置场景案例（%d 个）" % (TOOL_CN, TOOL, VERSION, len(SCENARIOS))]
    lines.append("完整逐场景示例见 references/scenarios.md。")
    lines.append("")
    for i, sc in enumerate(SCENARIOS, 1):
        d = DOMAIN_BY_ID[sc["domain"]]
        label = d["label_en"] if lang == "en" else d["label_zh"]
        skill = SKILLS[sc["skill"]]["cn"] + " " + sc["skill"] if sc["skill"] else ("元引自身" if sc["domain"] == "general" else "提示词自包含（无专属技能）")
        lines.append("%d. %s（%s）—— 输入「%s」→ %s → %s" % (i, sc["title"], sc["id"], sc["input"], label, skill))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
class _Parser(argparse.ArgumentParser):
    """让用法错误统一以退出码 4 结束（元阁 CLI 惯例）。"""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(4, "%s: error: %s\n" % (self.prog, message))


def cmd_clarify(args):
    if not args.text or not args.text.strip():
        print("缺少输入：请提供一句话或一个词，例如 clarify \"帮我写一封邮件\"", file=sys.stderr)
        return 4
    text = args.text.strip()
    if not score_domains(text):
        # 没有任何真实命中（不含 general 补齐）：未识别
        if args.json:
            payload = {
                "tool": TOOL, "version": VERSION, "input": text, "recognized": False,
                "guidance": "未识别出意图。请补充：想得到什么结果 / 与什么相关 / 输出形态；也可从常见方向（写作 / 记忆 / 开发 / 日志 / 学习 / 安全 / 质量）里选一个。",
                "questions": _unrecognized_questions(args.lang),
                "choices": _unrecognized_choices(args.lang),
                "template": _unrecognized_template(text, args.lang),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_unrecognized(text, args.lang))
        return 1
    cands = candidates_for(text, args.top, args.lang)
    if not cands:
        if args.json:
            payload = {
                "tool": TOOL, "version": VERSION, "input": text, "recognized": False,
                "guidance": "未识别出意图。请补充：想得到什么结果 / 与什么相关 / 输出形态；也可从常见方向（写作 / 记忆 / 开发 / 日志 / 学习 / 安全 / 质量）里选一个。",
                "questions": _unrecognized_questions(args.lang),
                "choices": _unrecognized_choices(args.lang),
                "template": _unrecognized_template(text, args.lang),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_unrecognized(text, args.lang))
        return 1
    if args.json:
        payload = {
            "tool": TOOL, "version": VERSION, "input": text, "recognized": True,
            "candidates": cands,
            "next": "选择候选后，用 yotta-prompt map <方向> 查看可串联技能与提示词。",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(render_clarify(text, cands, args.lang))
    return 0


def cmd_map(args):
    if not args.query or not args.query.strip():
        print("缺少查询：请提供方向或技能名，例如 map 写作 / map yotta-humanize", file=sys.stderr)
        return 4
    res = map_result(args.query)
    if res is None:
        if args.json:
            print(json.dumps({"tool": TOOL, "version": VERSION, "query": args.query.strip(), "found": False},
                             ensure_ascii=False, indent=2))
        else:
            print(render_map_miss(args.query))
        return 1
    if args.json:
        res["found"] = True
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(render_map(res, args.lang))
    return 0


def cmd_scenarios(args):
    if args.json:
        print(json.dumps(SCENARIOS, ensure_ascii=False, indent=2))
        return 0
    print(render_scenarios())
    return 0


def cmd_version():
    print("%s %s v%s" % (TOOL_CN, TOOL, VERSION))
    return 0


def main(argv=None):
    ap = _Parser(prog="yotta-prompt", description="%s（%s）意图澄清与生态入口 CLI" % (TOOL_CN, TOOL))
    ap.add_argument("--version", action="store_true", help="显示版本")
    sub = ap.add_subparsers(dest="cmd")

    p_c = sub.add_parser("clarify", help="意图澄清：一句话 / 一个词 → 2-4 个候选方向")
    p_c.add_argument("text", nargs="?", help="一句话或一个词")
    p_c.add_argument("--json", action="store_true", help="输出 JSON")
    p_c.add_argument("--top", type=int, default=4, help="候选数量上限（2-4，默认 4）")
    p_c.add_argument("--lang", choices=["zh", "en"], default="zh", help="界面语言")

    p_m = sub.add_parser("map", help="方向 / 技能名 → 元阁技能 + 安装命令 + 提示词")
    p_m.add_argument("query", nargs="?", help="方向（如 写作 / security）或技能名（如 yotta-humanize / 元真）")
    p_m.add_argument("--json", action="store_true", help="输出 JSON")
    p_m.add_argument("--lang", choices=["zh", "en"], default="zh", help="界面语言")

    p_s = sub.add_parser("scenarios", help="列出内置场景案例")
    p_s.add_argument("--json", action="store_true", help="输出 JSON")

    args = ap.parse_args(argv)
    if args.version:
        return cmd_version()
    if not args.cmd:
        ap.print_help()
        return 4
    if args.cmd == "clarify":
        return cmd_clarify(args)
    if args.cmd == "map":
        return cmd_map(args)
    if args.cmd == "scenarios":
        return cmd_scenarios(args)
    ap.print_help()
    return 4


if __name__ == "__main__":
    sys.exit(main())
