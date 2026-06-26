#!/usr/bin/env python3
"""
性能监控器 - 追踪Skill执行性能指标

用法:
    # 监控指定Skill 24小时
    python performance_monitor.py --skill my-skill --duration 24h
    
    # 查看监控报告
    python performance_monitor.py --skill my-skill --report
    
    # 导出数据
    python performance_monitor.py --skill my-skill --export performance.csv
"""

import argparse
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ExecutionRecord:
    """执行记录"""
    timestamp: str
    skill_name: str
    function_name: str
    execution_time_ms: float
    success: bool
    error_type: Optional[str]
    input_size: int
    output_size: int
    memory_usage_mb: float


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, skill_name: str, data_dir: str = "logs"):
        self.skill_name = skill_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.records: List[ExecutionRecord] = []
        
    def record_execution(self, **kwargs):
        """记录一次执行"""
        record = ExecutionRecord(
            timestamp=datetime.now().isoformat(),
            skill_name=self.skill_name,
            **kwargs
        )
        self.records.append(record)
        self._save_record(record)
    
    def _save_record(self, record: ExecutionRecord):
        """保存单条记录"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.data_dir / f"{self.skill_name}_{date_str}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False) + '\n')
    
    def load_records(self, days: int = 7) -> List[ExecutionRecord]:
        """加载最近N天的记录"""
        records = []
        
        for i in range(days):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            log_file = self.data_dir / f"{self.skill_name}_{date_str}.jsonl"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            records.append(ExecutionRecord(**data))
                        except:
                            continue
        
        return records
    
    def generate_report(self, days: int = 7) -> Dict:
        """生成性能报告"""
        records = self.load_records(days)
        
        if not records:
            return {"error": "无数据"}
        
        # 基础统计
        total = len(records)
        successful = sum(1 for r in records if r.success)
        failed = total - successful
        
        exec_times = [r.execution_time_ms for r in records]
        
        report = {
            "period_days": days,
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": round(successful / total * 100, 2),
            "execution_time": {
                "avg_ms": round(sum(exec_times) / len(exec_times), 2),
                "min_ms": round(min(exec_times), 2),
                "max_ms": round(max(exec_times), 2),
                "p95_ms": round(sorted(exec_times)[int(len(exec_times) * 0.95)], 2)
            },
            "error_analysis": self._analyze_errors(records),
            "slow_executions": self._find_slow_executions(records),
            "recommendations": self._generate_recommendations(records)
        }
        
        return report
    
    def _analyze_errors(self, records: List[ExecutionRecord]) -> Dict:
        """分析错误类型"""
        errors = {}
        for r in records:
            if not r.success and r.error_type:
                errors[r.error_type] = errors.get(r.error_type, 0) + 1
        return errors
    
    def _find_slow_executions(self, records: List[ExecutionRecord], threshold_ms: float = 5000) -> List[Dict]:
        """找出慢执行"""
        slow = [r for r in records if r.execution_time_ms > threshold_ms]
        return [
            {
                "timestamp": r.timestamp,
                "function": r.function_name,
                "time_ms": r.execution_time_ms
            }
            for r in slow[:10]  # 只返回前10个
        ]
    
    def _generate_recommendations(self, records: List[ExecutionRecord]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 成功率分析
        success_rate = sum(1 for r in records if r.success) / len(records)
        if success_rate < 0.95:
            recommendations.append(f"成功率偏低({success_rate*100:.1f}%)，建议检查错误日志")
        
        # 执行时间分析
        avg_time = sum(r.execution_time_ms for r in records) / len(records)
        if avg_time > 3000:
            recommendations.append(f"平均执行时间较长({avg_time:.0f}ms)，建议优化性能")
        
        # 错误类型分析
        errors = self._analyze_errors(records)
        if errors:
            most_common = max(errors.items(), key=lambda x: x[1])
            recommendations.append(f"最常见的错误: {most_common[0]} ({most_common[1]}次)")
        
        return recommendations


def main():
    parser = argparse.ArgumentParser(description='性能监控器')
    parser.add_argument('--skill', type=str, required=True, help='Skill名称')
    parser.add_argument('--duration', type=str, help='监控时长(如 24h, 7d)')
    parser.add_argument('--report', action='store_true', help='生成报告')
    parser.add_argument('--days', type=int, default=7, help='报告天数')
    parser.add_argument('--export', type=str, help='导出CSV文件')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(args.skill)
    
    if args.report:
        report = monitor.generate_report(args.days)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    elif args.export:
        records = monitor.load_records(args.days)
        import csv
        with open(args.export, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'function_name', 'execution_time_ms', 'success'])
            writer.writeheader()
            for r in records:
                writer.writerow({
                    'timestamp': r.timestamp,
                    'function_name': r.function_name,
                    'execution_time_ms': r.execution_time_ms,
                    'success': r.success
                })
        print(f"[OK] 已导出到 {args.export}")
    
    else:
        print(f"[*] 监控器已初始化: {args.skill}")
        print("[*] 使用 --report 查看报告")
        print("[*] 使用 --duration 启动持续监控")


if __name__ == '__main__':
    main()
