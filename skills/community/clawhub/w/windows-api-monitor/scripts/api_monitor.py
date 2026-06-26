#!/usr/bin/env python3
"""
Windows专用API使用监控脚本
用于监控OpenClaw在Windows环境下的API使用情况
"""

import os
import sys
import json
import argparse
import datetime
import pathlib
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# 添加工具模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# OpenClaw工作区路径
OPENCLAW_HOME = os.path.expanduser("~/.openclaw")
WORKSPACE_DIR = os.path.join(OPENCLAW_HOME, "workspace")
LOG_DIR = os.path.join(OPENCLAW_HOME, "logs")
CACHE_DIR = os.path.join(OPENCLAW_HOME, "cache", "model_usage")

# 模型成本参考（元/百万令牌）
MODEL_COSTS = {
    "deepseek-ai": 0.001,  # DeepSeek-V3.2
    "glm-5": 0.0015,       # GLM-5
    "gpt-4": 0.03,
    "gpt-3.5-turbo": 0.001,
    "claude-3": 0.015,
    "default": 0.002,
}

class APIMonitor:
    """API使用监控器"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.stats = defaultdict(lambda: {
            "calls": 0,
            "tokens": 0,
            "cost": 0.0,
            "sessions": set(),
        })
        
    def find_log_files(self, days: int = 7) -> List[str]:
        """查找最近的日志文件"""
        log_files = []
        log_dir = pathlib.Path(LOG_DIR)
        
        if not log_dir.exists():
            if self.debug:
                print(f"日志目录不存在: {LOG_DIR}")
            return log_files
            
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
        
        for log_file in log_dir.glob("*.log"):
            try:
                mtime = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime >= cutoff_time:
                    log_files.append(str(log_file))
            except Exception as e:
                if self.debug:
                    print(f"读取文件时间失败 {log_file}: {e}")
                    
        return sorted(log_files, reverse=True)  # 最新的在前面
    
    def parse_log_file(self, log_path: str) -> List[Dict]:
        """解析日志文件中的API调用记录"""
        calls = []
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 尝试解析JSON日志行
                    if line.startswith('{') and line.endswith('}'):
                        try:
                            entry = json.loads(line)
                            if self.is_api_call_entry(entry):
                                calls.append(entry)
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            if self.debug:
                print(f"解析日志文件失败 {log_path}: {e}")
                
        return calls
    
    def is_api_call_entry(self, entry: Dict) -> bool:
        """检查是否为API调用记录"""
        # 检查是否有模型相关字段
        model_fields = ['model', 'provider', 'agent', 'usage']
        return any(field in entry for field in model_fields)
    
    def extract_model_info(self, entry: Dict) -> Tuple[str, int]:
        """从日志条目中提取模型信息和令牌数"""
        model = "unknown"
        tokens = 0
        
        # 尝试从不同字段提取模型信息
        for field in ['model', 'provider', 'agent']:
            if field in entry:
                model = str(entry[field])
                break
        
        # 尝试提取令牌数
        if 'usage' in entry and isinstance(entry['usage'], dict):
            usage = entry['usage']
            if 'total_tokens' in usage:
                tokens = usage['total_tokens']
            elif 'prompt_tokens' in usage and 'completion_tokens' in usage:
                tokens = usage['prompt_tokens'] + usage['completion_tokens']
        
        return model, tokens
    
    def calculate_cost(self, model: str, tokens: int) -> float:
        """计算API调用成本"""
        cost_per_million = MODEL_COSTS.get(model, MODEL_COSTS["default"])
        return (tokens / 1_000_000) * cost_per_million
    
    def collect_stats(self, days: int = 1) -> Dict:
        """收集指定天数的统计信息"""
        log_files = self.find_log_files(days)
        session_count = 0
        
        if self.debug:
            print(f"找到 {len(log_files)} 个日志文件")
        
        for log_file in log_files:
            calls = self.parse_log_file(log_file)
            
            for call in calls:
                model, tokens = self.extract_model_info(call)
                cost = self.calculate_cost(model, tokens)
                session_id = call.get('session', 'unknown')
                
                self.stats[model]["calls"] += 1
                self.stats[model]["tokens"] += tokens
                self.stats[model]["cost"] += cost
                self.stats[model]["sessions"].add(session_id)
                
                session_count += 1
        
        # 转换sessions集合为数量
        result = {}
        for model, data in self.stats.items():
            result[model] = {
                "calls": data["calls"],
                "tokens": data["tokens"],
                "cost": round(data["cost"], 4),
                "sessions": len(data["sessions"]),
            }
            
        return result, session_count
    
    def format_report(self, stats: Dict, total_calls: int, days: int, 
                     mode: str = "text") -> str:
        """格式化报告"""
        if mode == "json":
            return json.dumps({
                "date": datetime.datetime.now().isoformat(),
                "period_days": days,
                "total_calls": total_calls,
                "models": stats,
            }, indent=2, ensure_ascii=False)
        
        # 文本格式报告
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        report = []
        report.append(f"=== API使用监控报告 ({today}) ===")
        report.append("")
        
        # 总体统计
        total_tokens = sum(data["tokens"] for data in stats.values())
        total_cost = sum(data["cost"] for data in stats.values())
        total_sessions = sum(data["sessions"] for data in stats.values())
        
        report.append("📊 总体统计:")
        report.append(f"- 统计周期: 最近{days}天")
        report.append(f"- 总调用次数: {total_calls}")
        report.append(f"- 总令牌数: {total_tokens:,}")
        report.append(f"- 估计成本: ~¥{total_cost:.4f}")
        report.append(f"- 涉及会话数: {total_sessions}")
        report.append("")
        
        # 按模型统计
        if stats:
            report.append("📈 按模型统计:")
            sorted_models = sorted(stats.items(), key=lambda x: x[1]["calls"], reverse=True)
            
            for i, (model, data) in enumerate(sorted_models, 1):
                percentage = (data["calls"] / total_calls * 100) if total_calls > 0 else 0
                report.append(f"{i}. {model}: {data['calls']}次 (¥{data['cost']:.4f}) - {percentage:.1f}%")
                report.append(f"   令牌: {data['tokens']:,} | 会话: {data['sessions']}")
        else:
            report.append("📈 按模型统计: 无数据")
        
        report.append("")
        
        # 效率建议
        report.append("💡 效率建议:")
        if total_calls == 0:
            report.append("- 未检测到API调用，系统运行正常")
        elif total_cost > 1.0:
            report.append("- 成本较高，建议检查高频调用模型")
        elif any(data["calls"] > 50 for data in stats.values()):
            report.append("- 检测到高频调用，建议优化工作流")
        else:
            report.append("- API使用效率良好")
        
        report.append("")
        report.append("⚠️ 告警信息: 无异常")
        report.append("")
        report.append(f"报告生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Windows专用API使用监控工具")
    parser.add_argument("--mode", choices=["current", "today", "week", "month", "all"],
                       default="today", help="监控模式")
    parser.add_argument("--model", type=str, help="指定模型名称")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="输出格式")
    parser.add_argument("--output", type=str, help="输出到文件")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--sort", choices=["calls", "tokens", "cost"],
                       default="calls", help="排序方式")
    parser.add_argument("--alerts", action="store_true", help="启用告警")
    parser.add_argument("--threshold", type=int, default=100,
                       help="告警阈值（调用次数）")
    
    args = parser.parse_args()
    
    # 根据模式确定天数
    days_map = {
        "current": 1,
        "today": 1,
        "week": 7,
        "month": 30,
        "all": 365,
    }
    days = days_map.get(args.mode, 1)
    
    # 创建监控器
    monitor = APIMonitor(debug=args.debug)
    
    # 收集统计信息
    try:
        stats, total_calls = monitor.collect_stats(days)
        
        # 如果有指定模型，筛选统计
        if args.model:
            filtered_stats = {}
            for model, data in stats.items():
                if args.model.lower() in model.lower():
                    filtered_stats[model] = data
            stats = filtered_stats
        
        # 排序
        if args.sort == "calls":
            sorted_items = sorted(stats.items(), key=lambda x: x[1]["calls"], reverse=True)
        elif args.sort == "tokens":
            sorted_items = sorted(stats.items(), key=lambda x: x[1]["tokens"], reverse=True)
        else:  # cost
            sorted_items = sorted(stats.items(), key=lambda x: x[1]["cost"], reverse=True)
        
        stats = dict(sorted_items)
        
        # 生成报告
        report = monitor.format_report(stats, total_calls, days, args.format)
        
        # 输出报告
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        else:
            print(report)
            
        # 告警检查
        if args.alerts and total_calls > args.threshold:
            print(f"\n⚠️ 警告: 检测到高频API调用 ({total_calls}次)")
            print(f"  超过阈值: {args.threshold}次")
            
    except Exception as e:
        print(f"监控失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()