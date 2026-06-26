#!/usr/bin/env python3
"""
技能使用积分榜核心脚本
功能：
1. 记录技能调用积分 (+1 * 调用时间秒/权重)
2. 记录调用结果和错误日志
3. 计算技能复杂度权重
4. 生成积分榜单
5. 每日23:00自动记录
"""

import json
import os
import sys
import glob
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional
import argparse

SKILL_DB_PATH = Path.home() / ".skill_scoreboard"
LOG_DIR = SKILL_DB_PATH / "logs"
DAILY_DIR = SKILL_DB_PATH / "daily"

# 确保目录存在
SKILL_DB_PATH.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
DAILY_DIR.mkdir(exist_ok=True)

DB_FILE = SKILL_DB_PATH / "scores.json"
LOG_FILE = LOG_DIR / "calls.log"
ERROR_LOG_FILE = LOG_DIR / "errors.log"

def load_scores() -> Dict:
    """加载积分数据"""
    if DB_FILE.exists():
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_scores(scores: Dict):
    """保存积分数据"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

def calculate_complexity(skill_path: Path) -> float:
    """
    计算技能复杂度权重（归一化到1.0附近，差距控制在5%内）
    
    算法：
    1. 统计技能的文件数和代码行数作为原始复杂度指标
    2. 对所有技能计算出的原始指标做 min-max 归一化
    3. 将归一化结果缩放到 [0.95, 1.05] 区间，即最大差距5%
    """
    if not skill_path.exists():
        return 1.0
    
    total_lines = 0
    file_count = 0
    
    # 统计所有代码文件的行数
    for ext in ['*.md', '*.js', '*.py', '*.sh', '*.json']:
        for file in skill_path.rglob(ext):
            if '.git' not in str(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                    file_count += 1
                except:
                    pass
    
    # 原始复杂度指标（用于归一化）
    raw_score = total_lines * 0.1 + file_count * 1.0
    
    return raw_score  # 返回原始分数，后续归一化处理

def get_all_skills() -> Dict[str, Dict]:
    """获取所有技能及其复杂度（归一化权重）"""
    import math
    shared_skills = Path.home() / "SharedSkills"
    skills = {}
    
    if not shared_skills.exists():
        return skills
    
    # 第一遍：收集所有技能的原始复杂度分数（用对数缩放处理极端值）
    raw_scores = {}
    for skill_dir in shared_skills.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            raw = calculate_complexity(skill_dir)
            # 对数缩放：log(1 + x)，避免大值过度影响
            raw_scores[skill_dir.name] = math.log1p(raw)
    
    # 第二遍：min-max 归一化到 [0.95, 1.05]，差距最多 5%
    if raw_scores:
        min_score = min(raw_scores.values())
        max_score = max(raw_scores.values())
        score_range = max_score - min_score if max_score != min_score else 1
        
        for skill_name, raw in raw_scores.items():
            # 归一化到 [0, 1]
            normalized = (raw - min_score) / score_range
            # 缩放到 [0.95, 0.9975]，确保最大差距 ≤5%
            weight = 0.95 + normalized * 0.0475
            
            skills[skill_name] = {
                'path': str(shared_skills / skill_name),
                'weight': round(weight, 4),
                'raw_score': raw,
                'calls': 0,
                'total_time': 0.0,
                'score': 0.0,
                'last_call': None,
                'success_count': 0,
                'error_count': 0
            }
    
    return skills

def record_call(skill_name: str, duration_seconds: float, success: bool = True, error_msg: str = None):
    """
    记录一次技能调用
    积分 = 1 * (调用时间秒 / 权重)
    """
    scores = load_scores()
    skills = get_all_skills()
    
    # 初始化技能记录
    if skill_name not in scores:
        scores[skill_name] = {
            'calls': 0,
            'total_time': 0.0,
            'score': 0.0,
            'last_call': None,
            'success_count': 0,
            'error_count': 0,
            'call_log': []
        }
    
    # 获取权重
    weight = skills.get(skill_name, {}).get('weight', 1.0)
    
    # 计算积分
    points = duration_seconds / weight
    scores[skill_name]['calls'] += 1
    scores[skill_name]['total_time'] += duration_seconds
    scores[skill_name]['score'] += points
    scores[skill_name]['last_call'] = datetime.now().isoformat()
    
    if success:
        scores[skill_name]['success_count'] += 1
    else:
        scores[skill_name]['error_count'] += 1
        # 记录错误日志
        log_error(skill_name, error_msg)
    
    # 记录调用日志
    call_entry = {
        'time': datetime.now().isoformat(),
        'duration': duration_seconds,
        'weight': weight,
        'points': points,
        'success': success
    }
    scores[skill_name]['call_log'].append(call_entry)
    
    # 只保留最近100条调用记录
    if len(scores[skill_name]['call_log']) > 100:
        scores[skill_name]['call_log'] = scores[skill_name]['call_log'][-100:]
    
    save_scores(scores)
    
    # 同时记录到调用日志文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {skill_name} | {duration_seconds:.2f}s | weight={weight} | +{points:.4f} | {'✓' if success else '✗'}\n")
    
    return points

def log_error(skill_name: str, error_msg: str):
    """记录错误日志"""
    with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {skill_name} | {error_msg}\n")

def get_leaderboard(limit: int = 10) -> List[Dict]:
    """获取积分榜单"""
    scores = load_scores()
    
    # 转换为列表并排序
    leaderboard = []
    for skill_name, data in scores.items():
        leaderboard.append({
            'skill': skill_name,
            'calls': data['calls'],
            'total_time': round(data['total_time'], 2),
            'score': round(data['score'], 4),
            'success_rate': round(data['success_count'] / data['calls'] * 100, 1) if data['calls'] > 0 else 0,
            'last_call': data['last_call']
        })
    
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard[:limit]

def get_today_leaderboard() -> List[Dict]:
    """获取今日积分榜单"""
    scores = load_scores()
    today = date.today().isoformat()
    
    leaderboard = []
    for skill_name, data in scores.items():
        # 筛选今日的调用
        today_calls = [c for c in data['call_log'] if c['time'].startswith(today)]
        
        if today_calls:
            today_score = sum(c['points'] for c in today_calls)
            today_calls_count = len(today_calls)
            today_time = sum(c['duration'] for c in today_calls)
            success_count = sum(1 for c in today_calls if c['success'])
            
            leaderboard.append({
                'skill': skill_name,
                'calls': today_calls_count,
                'total_time': round(today_time, 2),
                'score': round(today_score, 4),
                'success_rate': round(success_count / today_calls_count * 100, 1) if today_calls_count > 0 else 0
            })
    
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard

def get_week_leaderboard() -> List[Dict]:
    """获取本周积分榜单"""
    scores = load_scores()
    today = date.today()
    week_ago = today.replace(day=max(1, today.day - 7))
    week_ago_str = week_ago.isoformat()
    
    leaderboard = []
    for skill_name, data in scores.items():
        week_calls = [c for c in data['call_log'] if week_ago_str <= c['time'][:10] <= today.isoformat()]
        
        if week_calls:
            week_score = sum(c['points'] for c in week_calls)
            week_calls_count = len(week_calls)
            week_time = sum(c['duration'] for c in week_calls)
            success_count = sum(1 for c in week_calls if c['success'])
            
            leaderboard.append({
                'skill': skill_name,
                'calls': week_calls_count,
                'total_time': round(week_time, 2),
                'score': round(week_score, 4),
                'success_rate': round(success_count / week_calls_count * 100, 1) if week_calls_count > 0 else 0
            })
    
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard

def get_month_leaderboard() -> List[Dict]:
    """获取本月积分榜单"""
    scores = load_scores()
    today = date.today()
    month_ago = today.replace(day=1)
    month_ago_str = month_ago.isoformat()
    
    leaderboard = []
    for skill_name, data in scores.items():
        month_calls = [c for c in data['call_log'] if month_ago_str <= c['time'][:10] <= today.isoformat()]
        
        if month_calls:
            month_score = sum(c['points'] for c in month_calls)
            month_calls_count = len(month_calls)
            month_time = sum(c['duration'] for c in month_calls)
            success_count = sum(1 for c in month_calls if c['success'])
            
            leaderboard.append({
                'skill': skill_name,
                'calls': month_calls_count,
                'total_time': round(month_time, 2),
                'score': round(month_score, 4),
                'success_rate': round(success_count / month_calls_count * 100, 1) if month_calls_count > 0 else 0
            })
    
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard

def get_year_leaderboard() -> List[Dict]:
    """获取本年积分榜单"""
    scores = load_scores()
    today = date.today()
    year_ago = today.replace(month=1, day=1)
    year_ago_str = year_ago.isoformat()
    
    leaderboard = []
    for skill_name, data in scores.items():
        year_calls = [c for c in data['call_log'] if year_ago_str <= c['time'][:10] <= today.isoformat()]
        
        if year_calls:
            year_score = sum(c['points'] for c in year_calls)
            year_calls_count = len(year_calls)
            year_time = sum(c['duration'] for c in year_calls)
            success_count = sum(1 for c in year_calls if c['success'])
            
            leaderboard.append({
                'skill': skill_name,
                'calls': year_calls_count,
                'total_time': round(year_time, 2),
                'score': round(year_score, 4),
                'success_rate': round(success_count / year_calls_count * 100, 1) if year_calls_count > 0 else 0
            })
    
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard

def daily_snapshot():
    """每日23:00快照"""
    today = date.today().isoformat()
    snapshot_file = DAILY_DIR / f"{today}.json"
    
    scores = load_scores()
    leaderboard = get_leaderboard()
    today_stats = get_today_leaderboard()
    
    snapshot = {
        'date': today,
        'generated_at': datetime.now().isoformat(),
        'overall_leaderboard': leaderboard,
        'today_stats': today_stats,
        'total_skills': len(scores)
    }
    
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    
    return snapshot

def generate_workflow_insights(skill_name: str, scores: Dict) -> Dict:
    """分析技能调用记录，生成工作流洞察"""
    if skill_name not in scores:
        return None
    
    data = scores[skill_name]
    call_log = data.get('call_log', [])
    
    if not call_log:
        return None
    
    # 筛选今日调用
    today = date.today().isoformat()
    today_calls = [c for c in call_log if c['time'].startswith(today)]
    
    if not today_calls:
        return None
    
    # 分析各项指标
    durations = [c['duration'] for c in today_calls]
    success_calls = [c for c in today_calls if c['success']]
    error_calls = [c for c in today_calls if not c['success']]
    
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    success_rate = len(success_calls) / len(today_calls) * 100
    
    # 计算效率评分 (越快越好)
    # 效率分 = 基础分 * (最慢耗时 / 实际耗时)
    efficiency_score = avg_duration / min_duration if min_duration > 0 else 1.0
    
    # 生成工作流建议
    insights = []
    
    if success_rate >= 80:
        insights.append(f"✓ 成功率 {success_rate:.0f}% 表现优秀，可总结成功模式")
    elif success_rate < 50:
        insights.append(f"⚠ 成功率 {success_rate:.0f}% 偏低，需分析错误原因")
    
    if efficiency_score >= 1.5:
        insights.append(f"⚡ 存在效率提升空间：最慢({max_duration:.1f}s) vs 平均({avg_duration:.1f}s)")
        insights.append(f"   → 可尝试用平均耗时作为基准优化流程")
    
    if len(today_calls) >= 3:
        insights.append(f"📈 高频使用({len(today_calls)}次)，适合固化标准化流程")
    
    # 生成最佳实践建议
    best_practices = []
    if success_calls:
        best_avg = sum(c['duration'] for c in success_calls) / len(success_calls)
        best_practices.append(f"成功案例平均耗时: {best_avg:.2f}s")
    
    if error_calls:
        error_durations = [c['duration'] for c in error_calls]
        best_practices.append(f"失败案例平均耗时: {sum(error_durations)/len(error_durations):.2f}s (可能超时或异常)")
    
    return {
        'skill_name': skill_name,
        'date': today,
        'total_calls': len(today_calls),
        'success_rate': round(success_rate, 1),
        'avg_duration': round(avg_duration, 2),
        'min_duration': round(min_duration, 2),
        'max_duration': round(max_duration, 2),
        'efficiency_score': round(efficiency_score, 2),
        'total_score': round(data['score'], 4),
        'insights': insights,
        'best_practices': best_practices
    }

def daily_workflow_review() -> Dict:
    """每日工作流复盘：找出积分第一的技能并生成优化建议"""
    today_stats = get_today_leaderboard()
    
    if not today_stats:
        return {'status': 'no_calls', 'message': '今日暂无调用记录'}
    
    # 找出积分第一的技能
    top_skill = today_stats[0]
    skill_name = top_skill['skill']
    
    scores = load_scores()
    insights = generate_workflow_insights(skill_name, scores)
    
    # 保存复盘报告
    today = date.today().isoformat()
    review_file = DAILY_DIR / f"{today}_workflow_review.json"
    
    review = {
        'date': today,
        'generated_at': datetime.now().isoformat(),
        'top_skill': top_skill,
        'insights': insights
    }
    
    with open(review_file, 'w', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=2)
    
    return review

def print_workflow_review(review: Dict):
    """打印工作流复盘报告"""
    if review.get('status') == 'no_calls':
        print("今日暂无调用记录，跳过复盘")
        return
    
    top = review['top_skill']
    insights = review.get('insights')
    
    print(f"\n{'='*60}")
    print(f"  📋 每日工作流复盘报告 ({review['date']})")
    print(f"{'='*60}")
    print(f"  🏆 今日积分冠军: {top['skill']}")
    print(f"     调用次数: {top['calls']}次")
    print(f"     总耗时: {top['total_time']}s")
    print(f"     获得积分: {top['score']:.4f}")
    
    if insights:
        print(f"\n  📊 效率分析:")
        print(f"     平均耗时: {insights['avg_duration']}s")
        print(f"     最快耗时: {insights['min_duration']}s")
        print(f"     最慢耗时: {insights['max_duration']}s")
        print(f"     成功率: {insights['success_rate']}%")
        print(f"     效率评分: {insights['efficiency_score']}x")
        
        print(f"\n  💡 优化建议:")
        for insight in insights['insights']:
            print(f"     {insight}")
        
        if insights.get('best_practices'):
            print(f"\n  ✅ 最佳实践:")
            for bp in insights['best_practices']:
                print(f"     • {bp}")
    
    print(f"{'='*60}\n")

def print_leaderboard(leaderboard: List[Dict], title: str = "📊 技能积分榜"):
    """格式化打印榜单"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"{'排名':<6}{'技能':<20}{'调用次数':<10}{'总时长':<10}{'积分':<12}{'成功率':<10}")
    print(f"{'-'*60}")
    
    for i, item in enumerate(leaderboard, 1):
        print(f"{i:<6}{item['skill']:<20}{item['calls']:<10}{item['total_time']:<10}{item['score']:<12.4f}{item.get('success_rate', 0):.1f}%")
    
    print(f"{'='*60}\n")

def show_skill_detail(skill_name: str):
    """显示技能详细统计"""
    scores = load_scores()
    
    if skill_name not in scores:
        print(f"技能 '{skill_name}' 未找到")
        return
    
    data = scores[skill_name]
    print(f"\n{'='*60}")
    print(f"  📊 技能详情: {skill_name}")
    print(f"{'='*60}")
    print(f"  调用次数:    {data['calls']}")
    print(f"  总运行时长:  {data['total_time']:.2f}s")
    print(f"  当前积分:    {data['score']:.4f}")
    print(f"  成功次数:    {data['success_count']}")
    print(f"  错误次数:    {data['error_count']}")
    print(f"  最后调用:    {data['last_call']}")
    print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description='技能使用积分榜工具')
    parser.add_argument('action', choices=['record', 'leaderboard', 'today', 'week', 'month', 'year', 'daily', 'detail', 'weight', 'review'],
                       help='操作类型')
    parser.add_argument('--skill', help='技能名称')
    parser.add_argument('--duration', type=float, help='调用时长（秒）')
    parser.add_argument('--success', type=lambda x: x.lower() == 'true', default=True, help='是否成功')
    parser.add_argument('--error', help='错误信息')
    parser.add_argument('--limit', type=int, default=10, help='榜单数量限制')
    
    args = parser.parse_args()
    
    if args.action == 'record':
        if not args.skill or args.duration is None:
            print("错误: record 操作需要 --skill 和 --duration 参数")
            sys.exit(1)
        points = record_call(args.skill, args.duration, args.success, args.error)
        print(f"✓ 已记录: {args.skill} +{points:.4f}分")
    
    elif args.action == 'leaderboard':
        lb = get_leaderboard(args.limit)
        print_leaderboard(lb, "📊 全局技能积分榜（历史）")
    
    elif args.action == 'today':
        lb = get_today_leaderboard()
        if lb:
            print_leaderboard(lb, f"📊 今日积分榜 ({date.today()})")
        else:
            print("今日暂无技能调用记录")
    
    elif args.action == 'week':
        lb = get_week_leaderboard()
        if lb:
            print_leaderboard(lb, "📊 本周积分榜")
        else:
            print("本周暂无技能调用记录")
    
    elif args.action == 'month':
        lb = get_month_leaderboard()
        if lb:
            print_leaderboard(lb, "📊 本月积分榜")
        else:
            print("本月暂无技能调用记录")
    
    elif args.action == 'year':
        lb = get_year_leaderboard()
        if lb:
            print_leaderboard(lb, "📊 本年积分榜")
        else:
            print("本年暂无技能调用记录")
    
    elif args.action == 'daily':
        snapshot = daily_snapshot()
        print(f"✓ 每日快照已保存: {snapshot['date']}")
        print_leaderboard(snapshot['today_stats'], f"📊 今日积分榜 ({snapshot['date']})")
    
    elif args.action == 'detail':
        if not args.skill:
            print("错误: detail 操作需要 --skill 参数")
            sys.exit(1)
        show_skill_detail(args.skill)
    
    elif args.action == 'weight':
        skills = get_all_skills()
        print("\n📊 技能复杂度权重表（归一化，差距 ≤5%）")
        print(f"{'技能':<25}{'原始分':<10}{'归一化权重':<15}{'差距':<10}")
        print("-" * 60)
        
        if skills:
            weights = [s['weight'] for s in skills.values()]
            min_w = min(weights)
            max_w = max(weights)
            max_diff = (max_w - min_w) / min_w * 100
            
            for name, data in sorted(skills.items(), key=lambda x: x[1]['weight'], reverse=True):
                diff_pct = (data['weight'] - min_w) / min_w * 100
                print(f"{name:<25}{data.get('raw_score', 0):<10.2f}{data['weight']:<15.4f}{diff_pct:+.1f}%")
            
            print("-" * 60)
            print(f"权重范围: {min_w:.4f} ~ {max_w:.4f}，最大差距: {max_diff:.2f}%")
    
    elif args.action == 'review':
        review = daily_workflow_review()
        print_workflow_review(review)

if __name__ == '__main__':
    main()
