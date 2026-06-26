"""
Skill Usage Reporter
每次汇报本轮AI回复使用了哪些专项技能。
"""
import sys
import json
import os
from pathlib import Path

LOG_FILE = os.path.join(os.environ.get('TEMP', '/tmp'), 'skill_usage_log.json')

def get_recent_tools_from_history():
    """从会话历史中提取最近一轮的tool calls。"""
    try:
        # 尝试读取session历史（通过父进程传递的上下文）
        # 由于无法直接访问session，我们返回空列表，由agent自我汇报
        return []
    except Exception:
        return []

def load_log():
    """加载历史记录。"""
    if Path(LOG_FILE).exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {'turns': []}
    return {'turns': []}

def save_log(log):
    """保存记录。"""
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def add_turn(skills_used):
    """记录本轮使用的skills。"""
    log = load_log()
    log['turns'].append({
        'skills': skills_used,
    })
    save_log(log)

def get_report():
    """生成使用报告。"""
    log = load_log()
    if not log['turns']:
        return "暂无skill使用记录。"

    # 统计
    all_skills = []
    for turn in log['turns']:
        all_skills.extend(turn.get('skills', []))

    skill_count = {}
    for s in all_skills:
        skill_count[s] = skill_count.get(s, 0) + 1

    lines = ["=== Skill 使用报告 ===", ""]
    for skill, count in sorted(skill_count.items(), key=lambda x: -x[1]):
        lines.append(f"  {skill}: {count}次")
    lines.append("")
    lines.append(f"共使用 {len(set(all_skills))} 种skill，累计 {len(all_skills)} 次调用。")

    return "\n".join(lines)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'report'

    if cmd == 'add':
        skills = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
        add_turn(skills)
        print("已记录本轮skills。")
    elif cmd == 'report':
        print(get_report())
    elif cmd == 'clear':
        save_log({'turns': []})
        print("记录已清除。")
    else:
        print("用法: report_skills.py [add|report|clear]")

if __name__ == '__main__':
    main()
