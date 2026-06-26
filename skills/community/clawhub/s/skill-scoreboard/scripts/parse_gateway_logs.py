#!/usr/bin/env python3
"""
技能使用自动追踪器 v2
从 Gateway 日志中提取技能使用信息并记录到积分榜
"""

import json
import re
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict
import subprocess

# 技能关键词映射
SKILL_KEYWORDS = {
    'clawhub': ['clawhub', 'skill install', 'skill search', 'claw hub'],
    'skill-scoreboard': ['scoreboard', '积分榜', '技能榜'],
    'dream-selfimproving': ['dream', '梦境', '蒸馏', 'self-improving'],
    'weather': ['weather', '天气', '温度', 'forecast'],
    'github': ['github', 'git repo', 'github.com'],
    'feishu-doc': ['feishu doc', '飞书文档'],
    'feishu-wiki': ['feishu wiki', '飞书 wiki'],
    'feishu-drive': ['feishu drive', '飞书云盘'],
    'xia-zhua-zhua': ['xia-zhua', '抓取', '网页转', '内容抓取'],
    'xia-zhuan-audio': ['xia-zhuan-audio', '音频转', '视频转', '格式转换'],
    'xia-anquan': ['xia-anquan', '虾安全', '安全监控'],
    'weather': ['天气', 'weather', '温度'],
    'token-manager': ['token-manager', '令牌管理', '密钥管理'],
    'healthcheck': ['healthcheck', '健康检查', '系统检查'],
    'capability-evolver': ['capability', 'evolver', '进化', 'analyzer'],
    'image_generate': ['image_generate', '生成图片', '生成图像', '画图', '封面图'],
    'video_generate': ['video_generate', '生成视频'],
    'music_generate': ['music_generate', '生成音乐'],
    'web_search': ['web_search', '搜索', 'search', 'tavily'],
    'web_fetch': ['web_fetch', '抓取网页', '获取网页'],
    'exec': ['exec', 'execute', '命令执行', 'shell'],
}

# 日志文件路径
LOG_DIR = Path("/tmp/openclaw")

def get_gateway_logs(days: int = 1) -> list:
    """获取 Gateway 日志内容"""
    logs = []
    today = date.today()
    
    for i in range(days):
        log_date = today - timedelta(days=i)
        log_file = LOG_DIR / f"openclaw-{log_date.isoformat()}.log"
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs.append(f.read())
    
    return logs

def detect_skill_from_text(text: str) -> list:
    """从文本中检测技能使用"""
    text_lower = text.lower()
    found = []
    
    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                if skill not in found:
                    found.append(skill)
                break
    
    return found

def parse_gateway_logs(logs: list) -> dict:
    """解析 Gateway 日志，提取技能使用"""
    skill_usage = defaultdict(lambda: {
        'count': 0,
        'total_chars': 0,
        'examples': []
    })
    
    for log_content in logs:
        lines = log_content.split('\n')
        
        for line in lines:
            if '"type":"error"' in line or '"type":"warn"' in line:
                continue
            
            try:
                entry = json.loads(line)
                msg = entry.get('0', '') or entry.get('message', '')
                
                if isinstance(msg, str):
                    skills = detect_skill_from_text(msg)
                    for skill in skills:
                        skill_usage[skill]['count'] += 1
                        skill_usage[skill]['total_chars'] += len(msg)
                        if len(skill_usage[skill]['examples']) < 3:
                            example = msg[:100].replace('\n', ' ')
                            skill_usage[skill]['examples'].append(example)
            except:
                continue
    
    return dict(skill_usage)

def estimate_duration(count: int, total_chars: int) -> float:
    """估算总使用时长（秒）"""
    if count == 0:
        return 0.0
    
    base_time = (total_chars / 1000) * 1.0
    return max(base_time, count * 0.5)

def record_to_scoreboard(skill: str, duration: float, count: int):
    """记录到积分榜"""
    score_tracker = Path.home() / 'SharedSkills' / 'skill-scoreboard' / 'scripts' / 'score_tracker.py'
    
    if not score_tracker.exists():
        print(f"  ⚠️ score_tracker.py 未找到")
        return
    
    cmd = [
        'python3', str(score_tracker), 'record',
        '--skill', skill,
        '--duration', str(round(duration, 2)),
        '--success', 'true'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ {skill}: 记录 {count} 次, ~{duration:.1f}s")
    else:
        print(f"  ❌ {skill}: 记录失败")

def main():
    print("🔍 分析 Gateway 日志中的技能使用...")
    print("=" * 60)
    
    logs = get_gateway_logs(days=3)
    
    if not logs:
        print("❌ 未找到 Gateway 日志")
        return
    
    print(f"📂 已加载 {len(logs)} 个日志文件")
    
    skill_usage = parse_gateway_logs(logs)
    
    if not skill_usage:
        print("⚠️ 未检测到技能使用")
        return
    
    print(f"\n📊 检测到 {len(skill_usage)} 个技能/工具的使用\n")
    
    sorted_skills = sorted(skill_usage.items(), key=lambda x: -x[1]['count'])
    
    print("技能使用详情:")
    print("-" * 60)
    
    for skill, data in sorted_skills:
        count = data['count']
        total_chars = data['total_chars']
        duration = estimate_duration(count, total_chars)
        
        print(f"\n🔧 {skill}")
        print(f"   调用: {count} 次")
        print(f"   字符: {total_chars:,}")
        print(f"   估算时长: ~{duration:.1f}s")
        
        record_to_scoreboard(skill, duration, count)
    
    print("\n" + "=" * 60)
    print("✅ 技能使用分析完成")

if __name__ == '__main__':
    main()
