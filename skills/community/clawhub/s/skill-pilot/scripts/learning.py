# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
历史学习模块

从历史执行记录中学习最优调度策略
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class ExecutionHistory:
    """执行历史学习"""
    
    def __init__(self, history_file: str = None):
        self.history_file = history_file or os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/history/execution_log.jsonl"
        )
        self.stats_file = os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/history/skill_stats.json"
        )
        self.learning_file = os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/history/learned_patterns.json"
        )
    
    def record(self, request, result, context: Dict = None):
        """
        记录一次执行
        
        Args:
            request: 原始请求对象
            result: 执行结果对象
            context: 上下文信息（环境/偏好等）
        """
        record = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'category': getattr(request, 'category', 'unknown'),
            'query': getattr(request, 'query', None),
            'query_hash': self._hash_query(getattr(request, 'query', '')),
            'url': getattr(request, 'url', None),
            'selected_skill': getattr(result, 'used_skill', None),
            'success': getattr(result, 'success', False),
            'response_time': getattr(result, 'response_time', 0),
            'fallback_count': getattr(result, 'fallback_count', 0),
            'tried_skills': getattr(result, 'tried_skills', []),
            'error': getattr(result, 'error', None),
            'context': context or {},
        }
        
        self._append(record)
        self._update_stats(record)
    
    def _hash_query(self, query: str) -> str:
        """对查询内容哈希（保护隐私）"""
        if not query:
            return ''
        return hashlib.sha256(query.encode()).hexdigest()[:16]
    
    def _append(self, record: Dict):
        """追加记录到日志文件"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"记录执行历史失败：{e}")
    
    def _update_stats(self, record: Dict):
        """更新技能统计"""
        stats = self._load_stats()
        
        skill = record['selected_skill']
        if not skill:
            return
        
        if skill not in stats:
            stats[skill] = {
                'total_calls': 0,
                'success_count': 0,
                'failed_count': 0,
                'total_response_time': 0,
                'last_used': None,
                'by_category': {},
                'by_context': {},
            }
        
        s = stats[skill]
        s['total_calls'] += 1
        
        if record['success']:
            s['success_count'] += 1
        else:
            s['failed_count'] += 1
        
        s['total_response_time'] += record['response_time']
        s['last_used'] = record['datetime']
        
        # 按类别统计
        category = record['category']
        if category not in s['by_category']:
            s['by_category'][category] = {'total': 0, 'success': 0}
        s['by_category'][category]['total'] += 1
        if record['success']:
            s['by_category'][category]['success'] += 1
        
        # 保存
        self._save_stats(stats)
    
    def _load_stats(self) -> Dict:
        """加载统计数据"""
        if not os.path.exists(self.stats_file):
            return {}
        
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_stats(self, stats: Dict):
        """保存统计数据"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存统计数据失败：{e}")
    
    def _load_learned_patterns(self) -> Dict:
        """加载学习到的模式"""
        if not os.path.exists(self.learning_file):
            return {}
        
        try:
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_learned_patterns(self, patterns: Dict):
        """保存学习到的模式"""
        try:
            os.makedirs(os.path.dirname(self.learning_file), exist_ok=True)
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存学习模式失败：{e}")
    
    def query(self, category: str = None, days: int = 7, limit: int = 1000) -> List[Dict]:
        """
        查询历史记录
        
        Args:
            category: 类别过滤
            days: 最近 N 天
            limit: 最大返回条数
        
        Returns:
            历史记录列表
        """
        if not os.path.exists(self.history_file):
            return []
        
        records = []
        cutoff_time = time.time() - (days * 24 * 3600)
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if len(records) >= limit:
                        break
                    
                    try:
                        record = json.loads(line.strip())
                        
                        # 时间过滤
                        if record['timestamp'] < cutoff_time:
                            continue
                        
                        # 类别过滤
                        if category and record['category'] != category:
                            continue
                        
                        records.append(record)
                    except:
                        continue
        except Exception as e:
            print(f"查询历史记录失败：{e}")
        
        return records
    
    def analyze_skill_performance(self, skill_name: str = None, days: int = 7) -> Dict:
        """
        分析技能表现
        
        Returns:
            {
                'skill_name': {...},
                'success_rate': 0.92,
                'avg_response_time': 1234,
                'total_calls': 150,
                'by_category': {...},
            }
        """
        stats = self._load_stats()
        
        if skill_name:
            if skill_name not in stats:
                return None
            
            s = stats[skill_name]
            return {
                'skill_name': skill_name,
                'success_rate': s['success_count'] / max(1, s['total_calls']),
                'avg_response_time': s['total_response_time'] / max(1, s['total_calls']),
                'total_calls': s['total_calls'],
                'failed_count': s['failed_count'],
                'last_used': s['last_used'],
                'by_category': s['by_category'],
            }
        
        # 返回所有技能
        results = {}
        for name, s in stats.items():
            results[name] = {
                'success_rate': s['success_count'] / max(1, s['total_calls']),
                'avg_response_time': s['total_response_time'] / max(1, s['total_calls']),
                'total_calls': s['total_calls'],
            }
        
        return results
    
    def analyze_pattern(self, category: str, context: Dict = None) -> Dict:
        """
        分析特定场景下的最优技能
        
        Args:
            category: 类别 (search/fetch/summarize)
            context: 上下文（环境/区域等）
        
        Returns:
            {
                'best_skill': 'multi-search-engine',
                'success_rate': 0.95,
                'avg_response_time': 1200,
                'sample_size': 50,
                'alternatives': [...],
            }
        """
        records = self.query(category=category, days=30, limit=500)
        
        if not records:
            return None
        
        # 按技能分组统计
        skill_stats = {}
        for r in records:
            skill = r['selected_skill']
            if not skill:
                continue
            
            if skill not in skill_stats:
                skill_stats[skill] = {
                    'success': 0,
                    'total': 0,
                    'response_times': [],
                }
            
            skill_stats[skill]['total'] += 1
            if r['success']:
                skill_stats[skill]['success'] += 1
            skill_stats[skill]['response_times'].append(r['response_time'])
        
        # 计算综合得分
        ranked = []
        for skill, stats in skill_stats.items():
            success_rate = stats['success'] / max(1, stats['total'])
            avg_time = sum(stats['response_times']) / max(1, len(stats['response_times']))
            
            # 综合得分：成功率优先，响应时间其次
            score = success_rate * 100 - avg_time / 100
            
            ranked.append({
                'skill': skill,
                'score': score,
                'success_rate': success_rate,
                'avg_response_time': avg_time,
                'sample_size': stats['total'],
            })
        
        # 按得分排序
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        if not ranked:
            return None
        
        best = ranked[0]
        return {
            'best_skill': best['skill'],
            'success_rate': best['success_rate'],
            'avg_response_time': best['avg_response_time'],
            'sample_size': best['sample_size'],
            'alternatives': ranked[1:5],  # 前 5 个备选
            'category': category,
            'analyzed_at': datetime.now().isoformat(),
        }
    
    def learn_patterns(self):
        """
        学习调度模式
        
        分析所有类别的历史记录，提取最优技能选择模式
        """
        patterns = {
            'learned_at': datetime.now().isoformat(),
            'patterns': {},
        }
        
        # 分析每个类别
        for category in ['search', 'fetch', 'summarize', 'analyze']:
            pattern = self.analyze_pattern(category)
            if pattern:
                patterns['patterns'][category] = pattern
        
        # 按环境分组学习
        records = self.query(days=30, limit=1000)
        env_patterns = {}
        
        for r in records:
            context = r.get('context', {})
            env = context.get('environment', {}).get('region', 'unknown')
            
            if env not in env_patterns:
                env_patterns[env] = {'search': [], 'fetch': [], 'summarize': []}
            
            if r['success']:
                env_patterns[env][r['category']].append(r['selected_skill'])
        
        # 统计每个环境下的最优技能
        patterns['by_environment'] = {}
        for env, cats in env_patterns.items():
            patterns['by_environment'][env] = {}
            for cat, skills in cats.items():
                if skills:
                    # 找出最常用的技能
                    from collections import Counter
                    counter = Counter(skills)
                    most_common = counter.most_common(3)
                    patterns['by_environment'][env][cat] = [
                        {'skill': s, 'count': c} for s, c in most_common
                    ]
        
        self._save_learned_patterns(patterns)
        return patterns
    
    def get_recommendation(self, category: str, context: Dict = None) -> Optional[str]:
        """
        获取技能推荐
        
        基于历史学习结果推荐最优技能
        """
        # 1. 先看学习到的模式
        patterns = self._load_learned_patterns()
        
        if context:
            env = context.get('environment', {}).get('region', 'unknown')
            if env in patterns.get('by_environment', {}):
                env_recs = patterns['by_environment'][env].get(category, [])
                if env_recs:
                    return env_recs[0]['skill']
        
        # 2. 再看类别模式
        if category in patterns.get('patterns', {}):
            return patterns['patterns'][category]['best_skill']
        
        # 3. 实时分析
        pattern = self.analyze_pattern(category)
        if pattern:
            return pattern['best_skill']
        
        return None
    
    def get_stats_summary(self) -> Dict:
        """获取统计摘要"""
        stats = self._load_stats()
        patterns = self._load_learned_patterns()
        
        total_calls = sum(s['total_calls'] for s in stats.values())
        total_success = sum(s['success_count'] for s in stats.values())
        
        return {
            'total_skills_tracked': len(stats),
            'total_calls': total_calls,
            'overall_success_rate': total_success / max(1, total_calls),
            'patterns_learned': len(patterns.get('patterns', {})),
            'last_updated': patterns.get('learned_at', 'N/A'),
        }
    
    def clear_history(self, days_before: int = None):
        """
        清理历史记录
        
        Args:
            days_before: 清理 N 天前的记录，None 表示清空全部
        """
        if not os.path.exists(self.history_file):
            return
        
        if days_before is None:
            # 清空全部
            os.remove(self.history_file)
            print("✓ 已清空全部历史记录")
            return
        
        # 保留最近 N 天
        cutoff_time = time.time() - (days_before * 24 * 3600)
        kept_records = []
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if record['timestamp'] >= cutoff_time:
                        kept_records.append(line)
                except:
                    continue
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            f.writelines(kept_records)
        
        print(f"✓ 已清理 {days_before} 天前的历史记录，保留 {len(kept_records)} 条")


if __name__ == '__main__':
    # 命令行测试
    import sys
    
    history = ExecutionHistory()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == 'stats':
            stats = history.get_stats_summary()
            print("执行历史统计:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        
        elif action == 'analyze':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            pattern = history.analyze_pattern(category)
            if pattern:
                print(f"{category} 类别最优技能分析:")
                print(json.dumps(pattern, indent=2, ensure_ascii=False))
            else:
                print("暂无足够数据进行分析")
        
        elif action == 'learn':
            patterns = history.learn_patterns()
            print("学习到的模式:")
            print(json.dumps(patterns, indent=2, ensure_ascii=False))
        
        elif action == 'clear':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else None
            history.clear_history(days)
        
        elif action == 'recommend':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            rec = history.get_recommendation(category)
            print(f"推荐技能：{rec or '暂无推荐'}")
    else:
        # 默认：显示统计摘要
        stats = history.get_stats_summary()
        print("执行历史统计:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
