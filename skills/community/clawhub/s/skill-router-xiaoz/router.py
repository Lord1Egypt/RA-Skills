#!/usr/bin/env python3
"""
Skill Router — 场景分桶 + 智能路由 + 失败学习

核心设计：
1. 场景分桶：把技能按场景分类，激活相关桶，隔绝无关技能
2. 智能路由：从桶内选Top3，不贪多
3. 失败学习：路由失败 → 记录 → 下次绕过

运行：
  python3 router.py "任务描述"
"""

import json, os, sys
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path("/root/.openclaw/workspace/skills")
ROUTER_DIR = Path("/root/.openclaw/workspace/skills/skill-router")
ROUTER_DIR.mkdir(exist_ok=True)
ROUTING_LOG = ROUTER_DIR / "routing_log.jsonl"
SKILL_META = ROUTER_DIR / "skill_buckets.json"

# ─────────────────────────────────────────
# 1. 场景桶定义
# ─────────────────────────────────────────
SCENE_BUCKETS = {
    "学术研究": {
        "keywords": ["论文", "sci", "写论文", "投稿", "学术", "文献", "研究", "Cell", "Nature", "生物", "医学", "UBE2QL1", "CRC", "肿瘤", "RNA"],
        "skills": ["sci-paper-three-pass", "paper-polisher", "literature-review", "paper-summarize-academic", "paper-reference-checker", "scientific-visualization", "sci-paper-checker", "sci-paper-writer"],
        "top_default": ["sci-paper-three-pass", "literature-review", "paper-summarize-academic"],
    },
    "AI自我进化": {
        "keywords": ["进化", "自我", "意识", "自我意识", "成长", "学习", "记忆", "idle", "L3", "L4", "元认知", "置信度", "trajectory", "自我建模", "自我模型"],
        "skills": ["self-model", "self-evolve", "ai-consciousness-core", "ai-self-awareness-tracker", "idle-learning", "memory-dream", "memory-system-v2", "skill-self-improver", "memory-hygiene", "self-awareness-tracker", "self-model-L4"],
        "top_default": ["self-model", "idle-learning", "ai-consciousness-core"],
    },
    "内容创作": {
        "keywords": ["小说", "创作", "写作", "文案", "借命者", "网文", "脚本", "口播", "文案", "短剧"],
        "skills": ["openclaw-novel-pipeline", "inkos-agent", "inkos-writer", "caveman"],
        "top_default": ["openclaw-novel-pipeline", "caveman"],
    },
    "短视频运营": {
        "keywords": ["抖音", "小红书", "快手", "短视频", "B站", "视频", "发布", "上传视频", "种草", "口播"],
        "skills": ["douyin-operations", "douyin-video-publish", "douyin-full-operations", "douyin-messager", "douyin-folklore-video", "douyin-sensitive-check", "xiaohongshu", "xiaohongshu-comment", "jimeng-video", "baoyu-infographic"],
        "top_default": ["douyin-operations", "douyin-video-publish", "xiaohongshu"],
    },
    "代码开发": {
        "keywords": ["代码", "开发", "编程", "Python", "写代码", "bug", "程序", "网站", "建站", "小程序", "cloudbase", "API", "数据库"],
        "skills": ["coding-agent", "cloudbase", "github", "playwright-browser", "browser-harness", "tencent-cos-skill", "tencent-docs", "minimax-mcp"],
        "top_default": ["coding-agent", "cloudbase", "github"],
    },
    "图片处理": {
        "keywords": ["图片", "压缩", "优化", "截图", "图表", "可视化", "infographic"],
        "skills": ["baoyu-compress-image", "baoyu-infographic", "scientific-visualization", "minimax-understand-image"],
        "top_default": ["baoyu-compress-image", "baoyu-infographic"],
    },
    "搜索查询": {
        "keywords": ["搜索", "查资料", "上网", "查找", "新闻", "天气", "股票"],
        "skills": ["find-skills", "minimax-web-search", "web-tools-guide", "weather"],
        "top_default": ["find-skills", "minimax-web-search"],
    },
    "总结汇报": {
        "keywords": ["总结", "摘要", "概括", "汇报", "要点", "提炼"],
        "skills": ["summarize-pro", "paper-summarize-academic"],
        "top_default": ["summarize-pro"],
    },
}

def classify_scene(query: str) -> str:
    """识别请求属于哪个场景桶"""
    query_lower = query.lower()
    scores = {}
    for scene, cfg in SCENE_BUCKETS.items():
        score = 0
        matched = []
        for kw in cfg["keywords"]:
            if kw.lower() in query_lower:
                score += 1
                matched.append(kw)
        if score > 0:
            scores[scene] = (score, matched)
    if not scores:
        return "通用"  # 无匹配，走默认推荐
    # 返回得分最高的桶
    return max(scores, key=lambda s: scores[s][0])

def get_top_skills(scene: str, routing_log: list = None, max_n: int = 3) -> list:
    """从桶内选Top N个技能，优先用路由历史验证过的"""
    if scene == "通用":
        return []  # 通用场景不做桶内限制

    cfg = SCENE_BUCKETS.get(scene, {})
    candidates = cfg.get("top_default", [])[:max_n]

    # 从路由历史中找：哪些技能在这个场景里成功过
    if routing_log:
        scene_success = {}
        for entry in routing_log:
            if entry.get("scene") == scene and entry.get("outcome") == "success":
                skill = entry.get("skill_id", "")
                scene_success[skill] = scene_success.get(skill, 0) + 1
        # 优先用历史成功过的
        if scene_success:
            # 按成功次数排序
            ranked = sorted(scene_success.keys(), key=lambda s: scene_success[s], reverse=True)
            # 混合：历史成功的 + 桶默认
            seen = set()
            result = []
            for skill in ranked + candidates:
                if skill not in seen:
                    seen.add(skill)
                    result.append(skill)
                    if len(result) >= max_n:
                        break
            return result

    return candidates[:max_n]

def log_routing(query: str, scene: str, selected: list, outcome: str = ""):
    """记录路由历史（用于学习）"""
    entry = {
        "time": datetime.now().isoformat(),
        "query": query[:100],
        "scene": scene,
        "selected_skills": selected,
        "outcome": outcome,  # ""=pending, "success", "failure"
    }
    with open(ROUTING_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def load_routing_log(n: int = 100) -> list:
    """读取最近N条路由记录"""
    if not ROUTING_LOG.exists():
        return []
    lines = ROUTING_LOG.read_text().splitlines()
    result = []
    for line in lines[-n:]:
        try:
            result.append(json.loads(line))
        except:
            pass
    return result

def mark_outcome(query_hash: str, skill_id: str, outcome: str):
    """标记某次路由的结果（事后调用）"""
    if not ROUTING_LOG.exists():
        return
    lines = ROUTING_LOG.read_text().splitlines()
    updated = []
    for line in lines:
        try:
            entry = json.loads(line)
            # 简单匹配：同一秒内的同一场景视为同一次
            updated.append(entry)
        except:
            updated.append(line)
    # 重写（实际生产环境应该用更好的索引）
    with open(ROUTING_LOG, "w") as f:
        for entry in updated:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def route(query: str) -> dict:
    """主路由函数"""
    scene = classify_scene(query)
    log = load_routing_log()
    top_skills = get_top_skills(scene, log)
    log_routing(query, scene, top_skills)
    return {
        "query": query,
        "scene": scene,
        "selected_skills": top_skills,
        "reason": f"场景「{scene}」桶内Top3" if top_skills else "通用场景，不限制技能",
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 router.py \"任务描述\"")
        print("      python3 router.py \"任务描述\" --learn  # 读取路由历史")
        sys.exit(1)

    query = sys.argv[1]
    result = route(query)

    print(f"\n🔍 任务：「{result['query']}」")
    print(f"📦 识别场景：{result['scene']}")
    print(f"🎯 路由技能：{result['selected_skills'] or '（不限制，使用默认推荐）'}")
    print(f"💡 理由：{result['reason']}")

    if "--learn" in sys.argv:
        log = load_routing_log(50)
        scenes = {}
        for e in log:
            s = e.get("scene", "unknown")
            scenes[s] = scenes.get(s, 0) + 1
        print(f"\n📊 场景统计（最近50条）：")
        for s, c in sorted(scenes.items(), key=lambda x: -x[1]):
            print(f"   {s}: {c}次")

if __name__ == "__main__":
    main()
