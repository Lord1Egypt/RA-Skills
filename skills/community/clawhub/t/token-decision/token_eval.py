"""
大模型Token用量及效果实时决策 — Skill v2.0
开发者：乙春

WorkBuddy 用法（在聊天框输入）:
  你的prompt /token决策              # 默认均衡模式
  你的prompt /token决策 cheap        # 省钱优先
  你的prompt /token决策 quality      # 质量优先

命令行用法:
  python token_eval.py "你的prompt"
  python token_eval.py "你的prompt" cheap
  python token_eval.py "你的prompt" quality
"""
import sys
import sqlite3
import os
import re
from collections import defaultdict
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), "benchmark.db")

# ============================================================
# Token 估算 — 用 tiktoken 准确计算
# ============================================================
try:
    import tiktoken
    _TOKENIZER = tiktoken.get_encoding("o200k_base")  # GPT-4o 编码，大模型通用
    def count_tokens(text: str) -> int:
        return len(_TOKENIZER.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        return int(len(text) * 1.5)


# ============================================================
# 数据库辅助
# ============================================================
def _get_model_avg_costs():
    """从 benchmark.db 读取各模型平均实际成本（CNY）"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT model_name, ROUND(AVG(total_cost), 8), AVG(input_tokens), AVG(output_tokens),
               AVG(latency_ms), MAX(input_tokens + output_tokens)
        FROM runs GROUP BY model_name
    """)
    data = {}
    for mn, avg_cost, avg_in, avg_out, avg_lat, max_tok in cur.fetchall():
        data[mn] = {
            "avg_cost": avg_cost or 0,
            "avg_input_tokens": int(avg_in or 0),
            "avg_output_tokens": int(avg_out or 0),
            "avg_latency_ms": int(avg_lat or 0),
            "max_tokens": int(max_tok or 64000),
        }
    conn.close()

    # 模型元信息（上下文窗口、描述）
    meta = {
        "hy3-preview":       {"limit": 64000, "desc": "永久免费", "provider": "openrouter"},
        "glm-5.0-turbo":     {"limit": 128000, "desc": "最快最省", "provider": "zhipu"},
        "deepseek-v3.2":     {"limit": 64000, "desc": "🏆 综合最优", "provider": "deepseek"},
        "deepseek-v4-flash": {"limit": 128000, "desc": "快且强", "provider": "deepseek"},
        "deepseek-v4-pro":   {"limit": 128000, "desc": "旗舰", "provider": "deepseek"},
        "glm-5.1":           {"limit": 128000, "desc": "智谱旗舰", "provider": "zhipu"},
        "glm-5v-turbo":      {"limit": 128000, "desc": "多模态", "provider": "zhipu"},
        "minimax-m2.5":      {"limit": 64000, "desc": "中规中矩", "provider": "minimax"},
        "kimi-k2.6":         {"limit": 256000, "desc": "长文本之王", "provider": "kimi"},
    }
    for mn, m in meta.items():
        if mn in data:
            data[mn].update(m)
        else:
            data[mn] = {**m, "avg_cost": 0, "avg_input_tokens": 0, "avg_output_tokens": 0, "avg_latency_ms": 0, "max_tokens": 64000}
    return data


# ============================================================
# 任务分类 — 关键词 + 置信度 + embedding fallback
# ============================================================
TASK_KEYWORDS = {
    "写作":   [
              "一篇关于", "写", "写一个", "写一段", "写一篇", "创作",
              "报告", "拟写", "描述", "撰写", "文字", "文案",
              "文章", "生成一段", "生成一篇", "稿", "简述", "篇幅",
              "编写", "编撰", "草拟", "落笔", "论文", "起草"],
    "编程":   [
              "api", "bug", "c++", "debug", "def ", "go",
              "import", "java", "javascript", "python", "rust", "sql",
              "代码", "修复", "函数", "实现", "异常", "报错",
              "接口", "程序", "算法", "编程", "脚本", "部署",
              "配置"],
    "翻译":   [
              "translate", "中文", "中译", "德语", "日语", "法语",
              "翻译", "英文", "英译", "译为", "译成", "韩语"],
    "分析":   [
              "为什么", "分析", "原因", "对比", "归因", "指标",
              "数据", "根因", "比较", "研究", "统计", "规律",
              "评价", "评估", "走势", "趋势"],
    "知识问答":   [
              "什么是", "介绍一下", "关系", "分类", "区别", "历史",
              "原理", "告诉我", "如何", "定义", "怎么", "概念",
              "类型", "解释", "说明", "起源"],
    "总结摘要":   [
              "会议记录", "归纳", "总结", "提炼", "摘要", "核心内容",
              "梗概", "概括", "精简", "要点"],
    "数学推理":   [
              "公式", "几个", "几何", "多少", "推导", "推理",
              "数学", "方程", "概率", "求解", "等于", "计算",
              "证明", "逻辑题"],
    "闲聊":   [
              "你觉得", "你认为", "好吃", "好玩", "好看的", "怎么样",
              "推荐", "觉得"],
}


def classify_task(prompt: str) -> tuple:
    """
    基于关键词 + 置信度分类
    返回 (task_type, confidence, match_detail)
    - confidence >= 3: 高置信度
    - confidence == 1-2: 中置信度，可fallback
    - confidence == 0: 未知，触发embedding fallback
    """
    scores = defaultdict(int)
    match_detail = defaultdict(list)
    prompt_lower = prompt.lower()
    for task, keywords in TASK_KEYWORDS.items():
        for kw in keywords:
            if kw in prompt_lower:
                scores[task] += 1
                match_detail[task].append(kw)

    if not scores:
        return ("未知", 0, {})

    best_task = max(scores, key=scores.get)
    best_score = scores[best_task]

    # 平局 tiebreaker：优先更具体的任务类型
    # 编程/数学 > 翻译 > 分析 > 知识问答 > 写作 > 总结摘要 > 闲聊
    tie_priority = {"编程": 7, "数学推理": 6, "翻译": 5, "总结摘要": 4, "分析": 3, "知识问答": 2, "写作": 1, "闲聊": 0}
    tied = [t for t, s in scores.items() if s == best_score]
    if len(tied) > 1:
        best_task = max(tied, key=lambda t: tie_priority.get(t, 1))
        best_score = scores[best_task]

    # "闲聊" 仅在明确命中多个闲聊关键词时才采纳
    if best_task == "闲聊" and best_score < 3:
        other = {k: v for k, v in scores.items() if k != "闲聊"}
        if other:
            best_task = max(other, key=lambda t: (other[t], tie_priority.get(t, 1)))
            best_score = other[best_task]

    return (best_task, best_score, dict(match_detail))


def classify_with_fallback(prompt: str) -> str:
    """带 fallback 的智能分类"""
    task, conf, detail = classify_task(prompt)

    if conf >= 3:
        return task
    if conf >= 2:
        return task
    if conf == 1 and task != "闲聊":
        return task

    # 低置信度 / 未知：语义分析 fallback
    # 1. 检查是否包含明显指向
    if any(kw in prompt for kw in ["?" , "？"]):
        if any(kw in prompt for kw in ["代码", "编程", "python"]):
            return "编程"
        if any(kw in prompt for kw in ["翻译"]):
            return "翻译"
        return "知识问答"

    # 2. 检查 prompt 长度倾向
    if len(prompt) > 500:
        return "写作"  # 长 prompt 大概率是写作任务

    # 3. 默认：分析（比闲聊更有用）
    return "分析"


# ============================================================
# 多维加权评分
# ============================================================
# 每类任务的维度权重（总和 1.0）
TASK_WEIGHTS = {
    "写作":   {"conciseness": 0.30, "readability": 0.25, "overall": 0.15, "creativity": 0.15, "relevance": 0.10, "accuracy": 0.05},
    "编程":   {"efficiency": 0.30, "completeness": 0.25, "accuracy": 0.20, "overall": 0.15, "conciseness": 0.10},
    "翻译":   {"accuracy": 0.35, "completeness": 0.25, "readability": 0.20, "overall": 0.15, "efficiency": 0.05},
    "分析":   {"relevance": 0.30, "accuracy": 0.25, "completeness": 0.20, "overall": 0.15, "efficiency": 0.10},
    "知识问答": {"accuracy": 0.35, "completeness": 0.30, "relevance": 0.20, "overall": 0.15},
    "总结摘要": {"conciseness": 0.35, "completeness": 0.25, "accuracy": 0.20, "overall": 0.15, "relevance": 0.05},
    "数学推理": {"accuracy": 0.50, "completeness": 0.25, "overall": 0.15, "efficiency": 0.10},
    "闲聊":   {"overall": 0.35, "readability": 0.20, "relevance": 0.15, "creativity": 0.10, "efficiency": 0.10, "conciseness": 0.10},
}


def compute_weighted_score(row: tuple, task: str) -> float:
    """
    根据任务类型计算加权质量分
    row: (model_name, overall, conciseness, efficiency, relevance, total_cost, latency_ms, output_tokens, input_tokens,
          accuracy, completeness, format_score, creativity, readability)
    """
    mn, overall, conc, eff, rel, cost, lat, ot, it, acc, comp, fmt, crtv, rdbl = row
    weights = TASK_WEIGHTS.get(task, TASK_WEIGHTS["闲聊"])
    score = 0.0
    dims = {
        "overall": overall or 0, "conciseness": conc or 0, "efficiency": eff or 0,
        "relevance": rel or 0, "accuracy": acc or 0, "completeness": comp or 0,
        "format_score": fmt or 0, "creativity": crtv or 0, "readability": rdbl or 0,
    }
    for dim, w in weights.items():
        score += dims.get(dim, 0) * w
    return score


# ============================================================
# 上下文自动决策
# ============================================================
LARGE_WINDOW_MODELS = {"deepseek-v4-pro", "deepseek-v4-flash", "glm-5.1", "glm-5v-turbo", "kimi-k2.6", "glm-5.0-turbo"}
SMALL_WINDOW_MODELS = {"deepseek-v3.2", "hy3-preview", "minimax-m2.5"}


def apply_context_bonus(scored: list, prompt_len: int, mode: str) -> list:
    """
    长文本 (>2000字符) 时，cheap/balanced 模式下给大窗口模型加分，
    quality 模式不调整（始终优先质量）
    """
    if prompt_len <= 2000 or mode == "quality":
        return scored

    bonus_factor = 15 if mode == "cheap" else 10  # cheap 模式更积极切换
    result = []
    for score, *rest in scored:
        model_name = rest[0]
        new_score = score
        if model_name in LARGE_WINDOW_MODELS:
            new_score += bonus_factor
        elif model_name in SMALL_WINDOW_MODELS:
            new_score -= bonus_factor * 0.5
        result.append((new_score, *rest))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


# ============================================================
# 核心推荐逻辑
# ============================================================
def recommend(prompt: str, mode: str = "balanced", model_costs: dict = None) -> dict:
    """
    根据 prompt 和模式推荐模型
    mode: cheap(省钱) / balanced(均衡) / quality(质量优先)
    """
    if model_costs is None:
        model_costs = _get_model_avg_costs()

    task = classify_with_fallback(prompt)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 查询该任务的所有模型评分数据
    cur.execute("""
        SELECT r.model_name, s.overall, s.conciseness, s.efficiency, s.relevance,
               r.total_cost, r.latency_ms, r.output_tokens, r.input_tokens,
               s.accuracy, s.completeness, s.format_score, s.creativity, s.readability
        FROM runs r JOIN scores s ON r.id = s.run_id
        WHERE r.task_type = ? AND s.overall > 0
        ORDER BY s.overall DESC
    """, (task,))
    rows = cur.fetchall()

    if not rows:
        # 无该任务数据则用全局最优
        cur.execute("""
            SELECT r.model_name, s.overall, s.conciseness, s.efficiency, s.relevance,
                   r.total_cost, r.latency_ms, r.output_tokens, r.input_tokens,
                   s.accuracy, s.completeness, s.format_score, s.creativity, s.readability
            FROM runs r JOIN scores s ON r.id = s.run_id
            WHERE s.overall > 0
            ORDER BY s.overall - r.total_cost * 1000 DESC LIMIT 20
        """)
        rows = cur.fetchall()

    conn.close()

    # 计算加权质量分 + 成本惩罚
    prompt_tokens = count_tokens(prompt)
    scored = []
    for row in rows:
        mn = row[0]
        mc = model_costs.get(mn, {})
        cost = mc.get("avg_cost", 0)  # 使用实际平均成本（CNY）

        quality = compute_weighted_score(row, task)

        if mode == "cheap":
            # 省钱：成本权重极大
            score = quality * 0.4 - cost * 3000
        elif mode == "quality":
            # 质量优先：成本惩罚最小
            score = quality * 1.5 - cost * 200
        else:  # balanced
            # 均衡：ROI = 质量 - 成本加权
            score = quality - cost * 800

        scored.append((score, mn, quality, row[6], cost, row[7], row[8], row[9], mc.get("limit", 64000), mc.get("desc", "")))

    # 上下文自动决策：长文本给大窗口模型加分
    scored = apply_context_bonus(scored, len(prompt), mode)

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return {"task": task, "model": "deepseek-v3.2", "quality": 90, "mode": mode, "alternatives": []}

    best = scored[0]
    context_note = ""
    if len(prompt) > 2000 and best[1] in SMALL_WINDOW_MODELS and mode != "quality":
        context_note = " ⚠️ 您的prompt较长，但该任务下小窗口模型综合更优"

    return {
        "task": task,
        "model": best[1],
        "quality": best[2],
        "cost_estimate": best[4],
        "latency_ms": best[3],
        "est_tokens": prompt_tokens + model_costs.get(best[1], {}).get("avg_output_tokens", 200),
        "est_input": prompt_tokens,
        "est_output": model_costs.get(best[1], {}).get("avg_output_tokens", 200),
        "model_info": model_costs.get(best[1], {"limit": 64000, "desc": ""}),
        "mode": mode,
        "context_note": context_note,
        "alternatives": [
            {"model": s[1], "quality": s[2], "cost": s[4], "latency_ms": s[3],
             "limit": s[8], "desc": s[9]}
            for s in scored[1:5] if s[1] != best[1]
        ],
    }


# ============================================================
# 预算追踪
# ============================================================
def get_daily_cost() -> float:
    """今日累计消耗"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        today = date.today().isoformat()
        cur.execute("SELECT SUM(cost) FROM usage_log WHERE logged_at LIKE ?", (f"{today}%",))
        row = cur.fetchone()
        conn.close()
        return row[0] or 0.0
    except:
        return 0.0


# ============================================================
# 格式化输出
# ============================================================
def format_output(rec: dict) -> str:
    """格式化输出为可读文本"""
    lines = []
    lines.append("")
    lines.append("=" * 55)
    lines.append("  大模型Token用量及效果实时决策 v2.0")
    lines.append("  开发：乙春 | 数据驱动 · 多维评分 · 智能路由")
    lines.append("=" * 55)

    task_name = {"写作": "写作", "编程": "编程", "翻译": "翻译", "分析": "分析",
                 "知识问答": "知识问答", "总结摘要": "总结摘要",
                 "数学推理": "数学推理", "闲聊": "闲聊", "未知": "智能分析"}
    mode_name = {"cheap": "省钱优先", "balanced": "均衡", "quality": "质量优先"}

    task_display = task_name.get(rec['task'], rec['task'])
    lines.append(f"  任务识别: {task_display} | 模式: {mode_name.get(rec['mode'], rec['mode'])}")

    context_note = rec.get("context_note", "")
    lines.append("")
    lines.append(f"  🎯 推荐: {rec['model']} ({rec['model_info']['desc']}){context_note}")
    lines.append(f"     加权质量: {rec['quality']:.1f}/100 | 预估: {rec['est_tokens']}token | ¥{rec['cost_estimate']:.6f}")

    # 对比表
    if rec.get("alternatives"):
        lines.append("")
        lines.append(f"  📊 备选模型（同一任务实测数据）")
        lines.append(f"  {'模型':<22} {'质量':>6} {'成本¥':>10} {'延迟':>7} {'评价'}")
        lines.append("  " + "-" * 55)
        lines.append(f"  {rec['model']:<22} {rec['quality']:>5.1f}  {rec['cost_estimate']:>9.6f} {rec['latency_ms']:>6}ms 🏆推荐")
        for alt in rec["alternatives"]:
            alt_tag = ""
            if alt.get("limit", 0) >= 128000:
                alt_tag = "长窗"
            if alt["cost"] == 0:
                alt_tag = "免费"
            lines.append(f"  {alt['model']:<22} {alt['quality']:>5.1f}  {alt['cost']:>9.6f} {alt.get('latency_ms',0):>6}ms {alt_tag}")

    # 省钱计算
    if rec.get("alternatives") and rec["alternatives"][0]["cost"] > 0:
        nearest = rec["alternatives"][0]
        saved = nearest["cost"] - rec["cost_estimate"]
        if saved > 0:
            lines.append("")
            lines.append(f"  💰 比 {nearest['model']} 省 ¥{saved:.6f}")
        else:
            lines.append("")
            lines.append(f"  💰 比 {nearest['model']} 多花 ¥{-saved:.6f}，但质量高 {rec['quality']-nearest['quality']:.1f} 分")

    # Token Plan 换算
    lines.append("")
    lines.append(f"  🪙 Token Plan 消耗估算:")
    ratio_map = {"deepseek": 1.3, "glm": 1.0, "kimi": 1.5, "minimax": 1.2, "hy3": 1.0, "openrouter": 1.0}
    provider = rec["model_info"].get("provider", "")
    for prefix, ratio in ratio_map.items():
        if provider and prefix in provider.lower():
            break
    else:
        ratio = 1.0
    plan_tokens = int(rec["est_tokens"] * ratio)
    lines.append(f"     基础token: {rec['est_tokens']} × 计费系数{ratio} = {plan_tokens} 积分")
    calls = 400000 // plan_tokens if plan_tokens > 0 else float('inf')
    lines.append(f"     参考: Token Plan 40元/月约可调用 {calls} 次此类任务")

    # 今日预算
    daily = get_daily_cost()
    lines.append("")
    if daily > 0.1:
        lines.append(f"  ⚠️ 今日已消耗 ¥{daily:.4f}，建议关注用量")
    elif daily > 0.01:
        lines.append(f"  📊 今日已消耗 ¥{daily:.4f}")
    else:
        lines.append(f"  📊 今日消耗 ¥{daily:.4f}")

    lines.append("=" * 55)
    return "\n".join(lines)


# ============================================================
# 模型 API 调用（含故障转移）
# ============================================================
MODEL_API = {
    # DeepSeek 系列: 统一使用 deepseek-chat endpoint
    "deepseek-v4-pro":   ("deepseek", "https://api.deepseek.com/v1", "deepseek-chat", "DEEPSEEK_KEY"),
    "deepseek-v4-flash": ("deepseek", "https://api.deepseek.com/v1", "deepseek-chat", "DEEPSEEK_KEY"),
    "deepseek-v3.2":     ("deepseek", "https://api.deepseek.com/v1", "deepseek-chat", "DEEPSEEK_KEY"),
    # 智谱系列: 注意 GLM-5.1 对应 glm-4-plus endpoint（智谱 API 命名滞后于产品名）
    "glm-5.1":          ("zhipu", "https://open.bigmodel.cn/api/paas/v4", "glm-4-plus", "ZHIPU_KEY"),
    "glm-5.0-turbo":    ("zhipu", "https://open.bigmodel.cn/api/paas/v4", "glm-4-flash", "ZHIPU_KEY"),
    "glm-5v-turbo":     ("zhipu", "https://open.bigmodel.cn/api/paas/v4", "glm-4v-plus", "ZHIPU_KEY"),
    # Kimi/Moonshot: 使用 auto 自动选择最佳模型版本
    "kimi-k2.6":        ("kimi", "https://api.moonshot.cn/v1", "moonshot-v1-auto", "KIMI_KEY"),
    # MiniMax
    "minimax-m2.5":     ("minimax", "https://api.minimaxi.com/v1", "abab6.5s-chat", "MINIMAX_KEY"),
    # OpenRouter (Hy3 免费)
    "hy3-preview":      ("openrouter", "https://openrouter.ai/api/v1", "tencent/hy3-preview:free", "OPENROUTER_KEY"),
}


def _call_single_model(model_name: str, prompt: str) -> tuple:
    """调用单个模型，返回 (success, result_text, error_msg)"""
    cfg = MODEL_API.get(model_name)
    if not cfg:
        return (False, "", f"未知模型: {model_name}")

    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            load_dotenv()
        api_key = os.getenv(cfg[3], "")
        if not api_key:
            return (False, "", f"未配置 {cfg[3]} API Key")

        client = OpenAI(api_key=api_key, base_url=cfg[1])
        # 推理模型（如 OpenRouter 的 Hy3）需要 system message 触发 content 输出
        provider = cfg[0]
        messages = [{"role": "user", "content": prompt}]
        if provider == "openrouter":
            messages.insert(0, {"role": "system", "content": ""})
        resp = client.chat.completions.create(
            model=cfg[2],
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        msg = resp.choices[0].message
        content = msg.content
        # 推理模型可能把最终结果放到 reasoning 字段（content 为空时回退）
        if not content and hasattr(msg, 'reasoning') and msg.reasoning:
            content = msg.reasoning
        return (True, content or "", "")
    except Exception as e:
        return (False, "", str(e))


def execute_prompt(model_name: str, prompt: str, alternates: list = None) -> tuple:
    """
    调用推荐模型执行 prompt，失败自动 fallback
    最多回退 2 次（总共尝试 3 个模型）
    返回 (success, result_text, models_tried)
    """
    # 第一次尝试：推荐模型
    success, result, error = _call_single_model(model_name, prompt)
    if success:
        return (True, result, [model_name])

    if not alternates:
        return (False, f"[失败] {model_name}: {error}", [model_name])

    # Fallback 1
    for i, alt in enumerate(alternates[:2]):
        alt_model = alt["model"]
        success, result, err2 = _call_single_model(alt_model, prompt)
        if success:
            return (True, result, [model_name, alt_model])

    # 全部失败
    tried = [model_name] + [a["model"] for a in alternates[:2]]
    return (False, f"[全部调用失败] 已尝试: {', '.join(tried)}", tried)


# ============================================================
# 使用日志与埋点
# ============================================================
def init_usage_log():
    """创建/迁移使用日志表"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            task_type TEXT,
            task_confidence INTEGER DEFAULT 0,
            recommended_model TEXT,
            mode TEXT,
            quality REAL,
            cost REAL,
            logged_at TEXT
        )
    """)
    # 迁移：旧表可能缺少 task_confidence 列
    cur.execute("PRAGMA table_info(usage_log)")
    cols = [r[1] for r in cur.fetchall()]
    if "task_confidence" not in cols:
        try:
            cur.execute("ALTER TABLE usage_log ADD COLUMN task_confidence INTEGER DEFAULT 0")
            conn.commit()
        except:
            pass
    conn.commit()
    conn.close()


def log_usage(prompt: str, rec: dict, task_confidence: int = 0):
    """每次推荐后记录"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""INSERT INTO usage_log (prompt, task_type, task_confidence, recommended_model, mode, quality, cost, logged_at)
        VALUES (?,?,?,?,?,?,?,?)""", (
        prompt[:1000], rec["task"], task_confidence, rec["model"], rec["mode"],
        rec["quality"], rec["cost_estimate"], datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    # 埋点
    try:
        import urllib.request
        urllib.request.urlopen("https://api.countapi.xyz/hit/token-decision/total-calls", timeout=3)
    except:
        pass


def get_total_calls() -> int:
    try:
        import urllib.request, json
        resp = urllib.request.urlopen("https://api.countapi.xyz/get/token-decision/total-calls", timeout=5)
        return json.loads(resp.read()).get("value", 0)
    except:
        return -1


# ============================================================
# CLI 入口
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python token_eval.py \"你的prompt\" [cheap|balanced|quality] [--dry-run]")
        sys.exit(1)

    init_usage_log()
    prompt = sys.argv[1]
    mode = "balanced"
    do_exec = True

    mode_map = {
        "cheap": "cheap", "省钱": "cheap", "最便宜": "cheap", "免费": "cheap",
        "balanced": "balanced", "均衡": "balanced", "性价比": "balanced", "roi": "balanced",
        "quality": "quality", "质量": "quality", "最强": "quality", "效果": "quality",
    }
    forbid_exec = {"--dry-run", "-d", "--no-exec"}

    if len(sys.argv) >= 3:
        mode_arg = sys.argv[2].replace("--mode ", "").replace("--mode=", "").strip().lower()
        if mode_arg in forbid_exec:
            do_exec = False
        else:
            mode = mode_map.get(mode_arg, "balanced")
        if len(sys.argv) >= 4:
            if sys.argv[3] in forbid_exec:
                do_exec = False

    # 加载成本数据
    model_costs = _get_model_avg_costs()

    # 分类 + 推荐
    task, conf, _ = classify_task(prompt)
    rec = recommend(prompt, mode, model_costs)
    log_usage(prompt, rec, conf)
    print(format_output(rec))

    # 实际执行（带故障转移）
    if do_exec and rec.get("alternatives"):
        print()
        print("-" * 50)
        print(f"  🚀 正在用 {rec['model']} 执行（支持故障转移）...")
        print("-" * 50)
        success, result, tried = execute_prompt(rec["model"], prompt, rec["alternatives"])
        if len(tried) > 1:
            print(f"  🔄 故障转移: {tried[0]} → {tried[1]}")
        if len(tried) > 2:
            print(f"  🔄 再次转移: → {tried[2]}")
        print(result)
        print("-" * 50)
        if success:
            print(f"  ✅ 执行完成 | 模型: {tried[-1]} | 模式: {mode}")
        else:
            print(f"  ❌ 执行失败 | 已尝试: {', '.join(tried)}")
    elif do_exec:
        print()
        print("-" * 50)
        print(f"  🚀 正在用 {rec['model']} 执行...")
        print("-" * 50)
        success, result, tried = execute_prompt(rec["model"], prompt)
        print(result)
        print("-" * 50)
        print(f"  {'✅' if success else '❌'} 执行{'完成' if success else '失败'} | 模型: {rec['model']} | 模式: {mode}")
