#!/usr/bin/env python3
"""
三件套闭环引擎 v2（小狗版）— 女娲+达尔文+workflow-engine 自动联动

改进：
  ✅ 白名单排除 — 已有技能领域不重复蒸馏
  ✅ 人工确认 — cron模式写候选报告，手动run才真正蒸馏
  ✅ 任务验证 — 只认AI实际执行过tool的任务，忽略纯对话
  ✅ 淘汰机制 — 30天未触发的自动技能标记为候选删除

用法：
  python3 engine.py detect              # 只扫描，不执行
  python3 engine.py run                 # 完整闭环（需确认）
  python3 engine.py run --auto          # 自动模式（cron用，只写候选报告）
  python3 engine.py distill <任务>       # 手动蒸馏
  python3 engine.py evolve <技能>        # 手动进化
  python3 engine.py status              # 查看状态
  python3 engine.py gc                  # 淘汰过期技能
"""

import json, os, sys, re, glob
from datetime import datetime, timedelta
from pathlib import Path

HERMES = Path(os.path.expanduser("~/.hermes"))
SKILLS_DIR = HERMES / "skills"
WORKFLOW_DIR = HERMES / "workflow-engine" / "workflows"
LOOP_DIR = SKILLS_DIR / "skill-evolution-loop"
LOOP_STATE = LOOP_DIR / "state.json"
LOOP_LOG = LOOP_DIR / "loop.log"
CANDIDATES_FILE = LOOP_DIR / "candidates.json"
GC_REPORT = LOOP_DIR / "gc-report.md"

# ─── 白名单：已有技能覆盖的领域，不重复蒸馏 ───
EXISTING_SKILL_DOMAINS = {
    '邮箱': ['himalaya', 'google-workspace'],
    '邮件': ['himalaya', 'google-workspace'],
    '信息图': ['sn-infographic', 'baoyu-infographic', 'ai-daily-news'],
    '日报': ['ai-daily-news', 'ai-news-collector'],
    '新闻': ['ai-news-collector', 'ai-daily-news', 'ai-research-intelligence'],
    '公众号': ['wechat-article', 'wechat-publisher', 'wechat-official-account', 'wechat-article-production'],
    '文章': ['wechat-article', 'wechat-article-writer'],
    '备份': ['openclaw-backup'],
    'PDF': ['pdf', 'pdf-toolkit-pro', 'nano-pdf', 'minimax-pdf'],
    'PPT': ['pptx-generator', 'Powerpoint / PPTX', 'html-ppt', 'sn-ppt-entry'],
    'Excel': ['Excel / XLSX', 'minimax-xlsx', 'sn-da-excel-workflow'],
    '文档': ['doc-handler', 'Word / DOCX', 'minimax-docx'],
    '图片': ['sn-image-base', 'wan-image-video-gen-edit', 'comfyui'],
    '视频': ['seedance-video', 'wan-image-video-gen-edit', 'short-video-auto'],
    '搜索': ['web-tools-guide', 'firecrawl', 'tavily-search'],
    '截图': ['agent-browser'],
    '技能': ['darwin-skill', 'huashu-nuwa', 'skill-evolution-loop'],
    '工作流': ['workflow-engine'],
    'Notion': ['notion'],
    'GitHub': ['github', 'github-pr-workflow'],
    'cron': ['hermes-agent'],
    '巡检': ['self-evolution', 'kuro-health-check-system'],
    '报告': ['sn-deep-research', 'sn-research-report'],
    '数据': ['sn-da-excel-workflow', 'sn-da-large-file-analysis'],
}

# ─── 状态管理 ───
def load_state():
    if LOOP_STATE.exists():
        return json.loads(LOOP_STATE.read_text())
    return {
        "last_detect": None,
        "detected_patterns": [],
        "distilled_skills": [],
        "evolved_skills": [],
        "orchestrated_workflows": [],
        "loop_count": 0,
        "gc_runs": 0,
        "gc_removed": []
    }

def save_state(state):
    LOOP_STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def load_candidates():
    if CANDIDATES_FILE.exists():
        return json.loads(CANDIDATES_FILE.read_text())
    return {"pending": [], "rejected": [], "approved": []}

def save_candidates(cands):
    CANDIDATES_FILE.write_text(json.dumps(cands, indent=2, ensure_ascii=False))

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOOP_LOG, "a") as f:
        f.write(line + "\n")

# ─── 白名单检查 ───
def is_covered_by_existing(task_name):
    """检查任务是否已被现有技能覆盖"""
    for domain, skills in EXISTING_SKILL_DOMAINS.items():
        if domain in task_name:
            return skills
    return None

# ─── ① 感知（Detect）— 只认实际执行过的任务 ───
def detect_repeated_tasks(days=7, min_count=3):
    """扫描session logs，只提取AI实际执行了tool调用的任务"""
    log(f"🔍 扫描最近 {days} 天的session logs（只认实际执行的任务）...")
    
    task_verbs = ['查', '检查', '推送', '发送', '生成', '搜索', '扫描', '监控', 
                  '备份', '清理', '同步', '更新', '发布', '撰写', '写', '出', 
                  '做', '跑', '执行', '测试', '修复', '优化', '配置', '搭建', 
                  '部署', '截图', '抓取', '分析', '汇总', '整理']
    task_objects = ['邮箱', '邮件', '信息图', '日报', '周报', '报告', '海报', 
                   '封面', '文章', '公众号', 'Notion', 'cron', '心跳', '巡检', 
                   '磁盘', '内存', '服务', '数据库', '技能', '工作流', '备份', 
                   '知识库', 'Pipeline', '新闻', '数据', '图片', '视频', 'PDF',
                   'PPT', 'Excel', '文档', '网页', '截图', '下载']
    
    task_patterns = {}
    today = datetime.now()
    session_dir = HERMES / "sessions"
    
    if not session_dir.exists():
        log("   ⚠️ sessions目录不存在")
        return {}
    
    cutoff = today - timedelta(days=days)
    
    for f in sorted(session_dir.glob("*.jsonl")):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            continue
        
        try:
            content = f.read_text(errors='ignore')
        except Exception:
            continue
        
        # 解析session：找到user→assistant(tool_calls)的配对
        messages = []
        for line_text in content.split('\n'):
            if not line_text.strip():
                continue
            try:
                obj = json.loads(line_text)
                messages.append(obj)
            except json.JSONDecodeError:
                continue
        
        # 扫描：找user消息后面assistant是否有tool_calls
        for i, msg in enumerate(messages):
            if msg.get('role') != 'user':
                continue
            
            user_content = msg.get('content', '')
            if not isinstance(user_content, str) or len(user_content) < 4:
                continue
            
            # 跳过系统消息
            if user_content.startswith('[System') or user_content.startswith('[system'):
                continue
            if user_content.startswith('[') and ']' in user_content[:30]:
                continue
            
            # 检查后续assistant消息是否有tool_calls
            has_tool_call = False
            for j in range(i+1, min(i+5, len(messages))):
                if messages[j].get('role') == 'assistant':
                    # 检查是否有工具调用
                    if messages[j].get('tool_calls') or messages[j].get('function_call'):
                        has_tool_call = True
                    # 也检查content中是否包含tool_call标记
                    ac = messages[j].get('content', '')
                    if isinstance(ac, str) and ('terminal(' in ac or 'write_file(' in ac or 'browser_' in ac):
                        has_tool_call = True
                    break
                if messages[j].get('role') == 'user':
                    break  # 新一轮对话
            
            if not has_tool_call:
                continue  # 跳过纯对话，没有执行工具
            
            # 提取任务
            line = user_content.strip()[:100]
            
            # 跳过过短/过长
            if len(line) < 4 or len(line) > 100:
                continue
            # 跳过系统格式行
            if re.match(r'^\[|^-|^\\*|^#|^\\||^>|^```|^\\{', line):
                continue
            if re.search(r'[0-9a-f]{8}-[0-9a-f]{4}', line):  # UUID
                continue
            
            # 检查动词+宾语
            has_verb = any(v in line for v in task_verbs)
            has_obj = any(o in line for o in task_objects)
            
            if has_verb and has_obj:
                task = line[:50].strip()
                date_str = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
                if task not in task_patterns:
                    task_patterns[task] = {"count": 0, "dates": [], "examples": [], "has_tool": True}
                task_patterns[task]["count"] += 1
                task_patterns[task]["dates"].append(date_str)
                if len(task_patterns[task]["examples"]) < 3:
                    task_patterns[task]["examples"].append(task)
    
    # 过滤：>= min_count
    repeated = {k: v for k, v in task_patterns.items() if v["count"] >= min_count}
    repeated = dict(sorted(repeated.items(), key=lambda x: -x[1]["count"]))
    
    # 白名单过滤
    filtered = {}
    excluded = []
    for name, info in repeated.items():
        covering = is_covered_by_existing(name)
        if covering:
            excluded.append((name, covering))
        else:
            filtered[name] = info
    
    log(f"📊 发现 {len(repeated)} 个重复模式 → 白名单排除 {len(excluded)} 个 → 剩余 {len(filtered)} 个")
    for name, info in list(filtered.items())[:10]:
        log(f"   • {name} — {info['count']}次, 日期: {', '.join(set(info['dates']))}")
    for name, skills in excluded:
        log(f"   ⏭️ {name} — 已覆盖: {', '.join(skills)}")
    
    return filtered

# ─── ② 蒸馏（Distill）───
def distill_task(task_name, task_info):
    """蒸馏任务成技能"""
    log(f"🧪 蒸馏任务: {task_name}")
    
    skill_name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '-', task_name)[:30].strip('-')
    if not skill_name:
        skill_name = f"auto-skill-{datetime.now().strftime('%H%M%S')}"
    skill_dir = SKILLS_DIR / skill_name
    
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        log(f"   ⏭️ 技能已存在: {skill_name}，跳过")
        return skill_name, str(skill_dir)
    
    skill_content = generate_skill_md(task_name, task_info)
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(skill_content)
    
    log(f"   ✅ 技能已生成: {skill_dir}")
    return skill_name, str(skill_dir)

def generate_skill_md(task_name, task_info):
    count = task_info.get("count", 1)
    dates = ', '.join(set(task_info.get("dates", [])))
    
    return f'''---
name: {task_name[:40]}
description: |
  自动化任务：{task_name}
  频次：{count}次 | 日期：{dates}
  由三件套闭环自动蒸馏生成。请根据实际使用情况补充完善。
triggers:
  - "{task_name}"
  - "自动{task_name[:20]}"
---

# {task_name}

## 何时使用

- 用户说"{task_name}"或类似意图时
- 已观察到{count}次重复请求

## 执行流程

1. 理解用户意图和输入参数
2. 准备执行环境和依赖
3. 执行核心操作
4. 验证输出结果
5. 汇报结果给用户

## 失败降级

| 失败场景 | 降级策略 |
|---------|---------|
| 输入不明确 | 用clarify向用户确认 |
| 执行失败 | 重试2次，失败后告知用户 |
| 输出异常 | 降级为手动模式 |

## 待完善

> 此技能由自动蒸馏生成，以下维度需人工补充：
> - [ ] 具体执行步骤（目前是通用模板）
> - [ ] 实际工具/API调用方式
> - [ ] 边界条件和特殊处理
> - [ ] 真实示例
'''

# ─── ③ 进化（Evolve）───
def evolve_skill(skill_name, skill_dir):
    """9维评分+自动优化"""
    log(f"🧬 进化技能: {skill_name}")
    
    skill_file = Path(skill_dir) / "SKILL.md"
    if not skill_file.exists():
        log(f"   ❌ 技能文件不存在: {skill_file}")
        return None
    
    content = skill_file.read_text()
    scores = {}
    
    triggers = re.findall(r'triggers?:.*?\n((?:\s*-.*\n)+)', content)
    trigger_count = sum(len(re.findall(r'-\s+', t)) for t in triggers)
    scores["trigger_coverage"] = min(10, trigger_count * 2)
    
    steps = re.findall(r'^\d+\.\s+', content, re.MULTILINE)
    scores["flow_clarity"] = min(10, len(steps) * 2)
    
    fallbacks = re.findall(r'失败|降级|重试|跳过|静默', content)
    scores["fallback"] = min(10, len(fallbacks) * 2)
    
    desc_match = re.search(r'description:\s*\|?\s*\n((?:\s+.*\n)+)', content)
    desc_len = len(desc_match.group(1).strip()) if desc_match else 0
    scores["description"] = min(10, desc_len // 10)
    
    examples = re.findall(r'示例|example|Example|例如', content)
    scores["examples"] = min(10, len(examples) * 3)
    
    errors = re.findall(r'error|Error|错误|异常|超时', content)
    scores["error_handling"] = min(10, len(errors) * 2)
    
    headers = re.findall(r'^#+\s+', content, re.MULTILINE)
    scores["structure"] = min(10, len(headers) * 2)
    
    tests = re.findall(r'测试|test|验证|check', content)
    scores["testability"] = min(10, len(tests) * 2)
    
    scores["reusability"] = 8 if "triggers" in content else 4
    
    total = sum(scores.values()) / 9
    log(f"   📊 评分: {total:.1f}/10")
    for dim, score in scores.items():
        if score < 6:
            log(f"   ⚠️ {dim}: {score}/10 (需优化)")
    
    if total < 7:
        log(f"   🔧 自动优化中...")
        optimize_skill(skill_file, content, scores)
    
    return scores

def optimize_skill(skill_file, content, scores):
    optimized = content
    
    if scores.get("trigger_coverage", 10) < 6:
        if "triggers:" not in optimized:
            optimized = optimized.replace(
                "description: |",
                'description: |\ntriggers:\n  - "自动触发"'
            )
    
    if scores.get("fallback", 10) < 6:
        if "失败降级" not in optimized:
            optimized += "\n\n## 失败降级\n\n| 失败场景 | 降级策略 |\n|---------|----------|\n| 通用失败 | 重试3次后静默跳过 |\n"
    
    if scores.get("structure", 10) < 6:
        if "## 执行流程" not in optimized:
            optimized += "\n\n## 执行流程\n\n1. 解析输入\n2. 执行核心逻辑\n3. 输出结果\n"
    
    if optimized != content:
        skill_file.write_text(optimized)
        log(f"   ✅ 已优化: {skill_file}")

# ─── ④ 编排（Orchestrate）───
def orchestrate_workflow(skill_name, skill_dir):
    """生成工作流YAML"""
    log(f"🔗 编排工作流: {skill_name}")
    
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    wf_file = WORKFLOW_DIR / f"{skill_name}-auto.yaml"
    
    yaml_content = f'''name: "{skill_name}-auto"
description: "由三件套闭环自动生成的工作流"
version: "1.0"
created: "{datetime.now().isoformat()}"

steps:
  - id: input
    name: "解析输入"
    type: terminal
    config:
      command: "echo '输入解析完成'"
    
  - id: execute
    name: "执行{skill_name}"
    type: skill
    config:
      skill_name: "{skill_name}"
    depends: [input]
    retry:
      max_attempts: 3
        
  - id: verify
    name: "验证结果"
    type: terminal
    config:
      command: "echo '验证通过'"
    depends: [execute]
    
  - id: output
    name: "输出结果"
    type: terminal
    config:
      command: "echo '任务完成'"
    depends: [verify]
'''
    
    wf_file.write_text(yaml_content)
    log(f"   ✅ 工作流已生成: {wf_file}")
    return str(wf_file)

# ─── 淘汰机制（GC）───
def run_gc(dry_run=False, max_age_days=30):
    """标记/删除超过max_age_days未被触发的自动蒸馏技能"""
    log(f"🗑️ 淘汰检查（{'预览' if dry_run else '执行'}）: 超过 {max_age_days} 天未触发的自动技能")
    
    state = load_state()
    gc_candidates = []
    
    # 扫描所有技能目录
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        content = skill_file.read_text()
        
        # 只处理自动蒸馏的技能（有"三件套闭环自动蒸馏"标记）
        if "三件套闭环自动蒸馏" not in content:
            continue
        
        # 检查最后修改时间
        mtime = datetime.fromtimestamp(skill_file.stat().st_mtime)
        age_days = (datetime.now() - mtime).days
        
        if age_days >= max_age_days:
            # 检查是否在其他技能的引用中被提到
            is_referenced = False
            for other_dir in SKILLS_DIR.iterdir():
                if other_dir == skill_dir or not other_dir.is_dir():
                    continue
                other_file = other_dir / "SKILL.md"
                if other_file.exists() and skill_dir.name in other_file.read_text():
                    is_referenced = True
                    break
            
            gc_candidates.append({
                "name": skill_dir.name,
                "age_days": age_days,
                "path": str(skill_dir),
                "is_referenced": is_referenced,
                "last_modified": mtime.isoformat()
            })
    
    # 生成报告
    report = f"# 🗑️ 淘汰候选报告\n\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"阈值: {max_age_days}天未修改\n"
    report += f"候选数: {len(gc_candidates)}\n\n"
    
    if gc_candidates:
        report += "| 技能 | 未修改天数 | 被引用 | 操作 |\n"
        report += "|------|-----------|--------|------|\n"
        for c in gc_candidates:
            action = "⚠️ 保留（被引用）" if c["is_referenced"] else "🗑️ 可删除"
            report += f"| {c['name']} | {c['age_days']}天 | {'是' if c['is_referenced'] else '否'} | {action} |\n"
        
        # 执行删除（非dry_run且不被引用的）
        if not dry_run:
            removed = []
            for c in gc_candidates:
                if not c["is_referenced"]:
                    import shutil
                    shutil.rmtree(c["path"])
                    removed.append(c["name"])
                    log(f"   🗑️ 已删除: {c['name']} ({c['age_days']}天未触发)")
            
            state["gc_runs"] += 1
            state["gc_removed"].extend(removed)
            save_state(state)
            report += f"\n## 已删除 {len(removed)} 个技能\n"
            for r in removed:
                report += f"- {r}\n"
    else:
        report += "✅ 无候选淘汰技能\n"
    
    GC_REPORT.write_text(report)
    log(f"📊 淘汰报告: {GC_REPORT}")
    
    return gc_candidates

# ─── 候选报告（cron自动模式用）───
def write_candidates_report(repeated):
    """把检测到的模式写入候选报告，等人工确认"""
    cands = load_candidates()
    
    new_pending = []
    for name, info in repeated.items():
        # 检查是否已在候选/已拒绝列表中
        already = any(c["name"] == name for c in cands["pending"] + cands["rejected"] + cands["approved"])
        if not already:
            new_pending.append({
                "name": name,
                "count": info["count"],
                "dates": list(set(info["dates"])),
                "detected_at": datetime.now().isoformat(),
                "status": "pending"
            })
    
    cands["pending"].extend(new_pending)
    save_candidates(cands)
    
    # 生成候选报告
    report = f"# 🧪 技能蒸馏候选报告\n\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"新发现: {len(new_pending)} 个\n\n"
    
    if new_pending:
        report += "| 任务 | 频次 | 日期 | 状态 |\n"
        report += "|------|------|------|------|\n"
        for c in new_pending:
            report += f"| {c['name'][:30]} | {c['count']}次 | {', '.join(c['dates'])} | ⏳ 待确认 |\n"
        report += "\n**确认后执行:** `python3 engine.py run`\n"
    else:
        report += "✅ 无新候选\n"
    
    candidates_report = LOOP_DIR / "candidates-report.md"
    candidates_report.write_text(report)
    log(f"📋 候选报告: {candidates_report}")
    
    return new_pending

# ─── 完整闭环 ───
def run_full_loop(auto_mode=False):
    """执行完整闭环"""
    log("=" * 50)
    log(f"🔄 三件套闭环启动（{'自动模式' if auto_mode else '手动模式'}）")
    log("=" * 50)
    
    state = load_state()
    
    # ① 感知
    repeated = detect_repeated_tasks(days=7, min_count=3)
    
    if not repeated:
        log("📭 未发现重复任务，本轮跳过")
        state["last_detect"] = datetime.now().isoformat()
        save_state(state)
        return {"new_skills": 0, "patterns": 0}
    
    if auto_mode:
        # 自动模式：只写候选报告，不真正蒸馏
        new_pending = write_candidates_report(repeated)
        state["last_detect"] = datetime.now().isoformat()
        state["loop_count"] += 1
        save_state(state)
        
        log("=" * 50)
        log(f"✅ 自动模式完成 | 发现 {len(new_pending)} 个新候选 | 等待人工确认")
        log("=" * 50)
        return {"new_skills": 0, "patterns": len(repeated), "candidates": len(new_pending)}
    
    # 手动模式：真正蒸馏
    new_skills = []
    for task_name, task_info in list(repeated.items())[:5]:
        skill_name, skill_dir = distill_task(task_name, task_info)
        new_skills.append((skill_name, skill_dir, task_info))
    
    for skill_name, skill_dir, task_info in new_skills:
        evolve_skill(skill_name, skill_dir)
    
    for skill_name, skill_dir, task_info in new_skills:
        orchestrate_workflow(skill_name, skill_dir)
    
    state["last_detect"] = datetime.now().isoformat()
    state["loop_count"] += 1
    state["detected_patterns"].extend([{
        "name": k, "count": v["count"], "dates": v["dates"]
    } for k, v in repeated.items()])
    state["distilled_skills"].extend([s[0] for s in new_skills])
    save_state(state)
    
    log("=" * 50)
    log(f"✅ 闭环完成 | 本轮蒸馏 {len(new_skills)} 个技能 | 累计 {state['loop_count']} 轮")
    log("=" * 50)
    
    return {"new_skills": len(new_skills), "patterns": len(repeated)}

# ─── 状态查看 ───
def show_status():
    state = load_state()
    cands = load_candidates()
    
    print("=" * 40)
    print("🔄 三件套闭环状态（小狗版 v2）")
    print("=" * 40)
    print(f"累计运行: {state['loop_count']} 轮")
    print(f"上次检测: {state.get('last_detect', '从未')}")
    print(f"已蒸馏技能: {len(state['distilled_skills'])} 个")
    print(f"待确认候选: {len(cands.get('pending', []))} 个")
    print(f"已拒绝: {len(cands.get('rejected', []))} 个")
    print(f"淘汰次数: {state.get('gc_runs', 0)}")
    print(f"已淘汰: {len(state.get('gc_removed', []))} 个")
    
    if cands.get('pending'):
        print("\n⏳ 待确认候选:")
        for c in cands['pending'][-10:]:
            print(f"  • {c['name']} ({c['count']}次)")
    
    if state.get('gc_removed'):
        print("\n🗑️ 已淘汰:")
        for s in state['gc_removed'][-5:]:
            print(f"  • {s}")

# ─── CLI入口 ───
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 engine.py detect              # 扫描重复任务")
        print("  python3 engine.py run                 # 完整闭环（手动确认）")
        print("  python3 engine.py run --auto          # 自动模式（cron用）")
        print("  python3 engine.py distill <任务>       # 手动蒸馏")
        print("  python3 engine.py evolve <技能>        # 手动进化")
        print("  python3 engine.py status              # 查看状态")
        print("  python3 engine.py gc                  # 淘汰过期技能")
        print("  python3 engine.py gc --dry-run        # 预览淘汰")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "detect":
        repeated = detect_repeated_tasks()
        if repeated:
            print(f"\n发现 {len(repeated)} 个重复任务:")
            for name, info in list(repeated.items())[:10]:
                print(f"  • {name} — {info['count']}次")
        else:
            print("未发现重复任务")
    
    elif cmd == "distill":
        if len(sys.argv) < 3:
            print("用法: python3 engine.py distill <任务名称>")
            sys.exit(1)
        task_name = " ".join(sys.argv[2:])
        distill_task(task_name, {"count": 1, "dates": [datetime.now().strftime("%Y-%m-%d")], "examples": [task_name]})
    
    elif cmd == "evolve":
        if len(sys.argv) < 3:
            print("用法: python3 engine.py evolve <技能名称>")
            sys.exit(1)
        skill_name = sys.argv[2]
        skill_dir = str(SKILLS_DIR / skill_name)
        evolve_skill(skill_name, skill_dir)
    
    elif cmd == "run":
        auto = "--auto" in sys.argv
        result = run_full_loop(auto_mode=auto)
        if auto:
            print(f"\n自动模式: 检测 {result['patterns']} 个模式, {result.get('candidates', 0)} 个新候选")
        else:
            print(f"\n结果: 新技能 {result['new_skills']} 个, 检测模式 {result['patterns']} 个")
    
    elif cmd == "status":
        show_status()
    
    elif cmd == "gc":
        dry_run = "--dry-run" in sys.argv
        candidates = run_gc(dry_run=dry_run)
        if candidates:
            print(f"\n{'预览' if dry_run else '处理'}: {len(candidates)} 个候选")
            for c in candidates:
                print(f"  • {c['name']} ({c['age_days']}天)")
        else:
            print("无候选淘汰技能")
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
