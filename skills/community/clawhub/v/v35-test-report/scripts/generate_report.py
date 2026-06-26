#!/usr/bin/env python3
"""
v3.5 测试报告生成器
读取生产日志，生成统计报告
"""

import re
from datetime import datetime

def parse_production_log():
    """解析v3.5生产日志"""
    log_file = "/tmp/agent_v35_production.log"
    
    stats = {
        "v35_runs": 0,
        "v35_votes": [],
        "v30_runs": 0,
        "v30_votes": [],
        "accurate_predictions": 0,
        "total_predictions": 0,
        "strategies": {}
    }
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        
        # 提取v3.5运行
        v35_matches = re.findall(r'使用: V35.*?平均赞: (\d+\.?\d*)', content, re.DOTALL)
        stats["v35_runs"] = len(v35_matches)
        stats["v35_votes"] = [float(v) for v in v35_matches if v]
        
        # 提取v3.0运行
        v30_matches = re.findall(r'使用: V30.*?平均赞: (\d+\.?\d*)', content, re.DOTALL)
        stats["v30_runs"] = len(v30_matches)
        stats["v30_votes"] = [float(v) for v in v30_matches if v]
        
        # 提取准确度
        acc_matches = re.findall(r'准确度: (\d+)%', content)
        for acc in acc_matches:
            stats["total_predictions"] += 1
            if int(acc) > 0:
                stats["accurate_predictions"] += 1
        
        return stats
        
    except FileNotFoundError:
        print(f"❌ 日志文件不存在: {log_file}")
        return None

def generate_report(stats):
    """生成报告"""
    if not stats:
        return
    
    print("\n" + "="*60)
    print("📊 v3.5 生产部署报告")
    print("="*60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # v3.5 统计
    if stats["v35_runs"] > 0:
        avg_v35 = sum(stats["v35_votes"]) / len(stats["v35_votes"])
        print(f"\n🤖 v3.5 因果推理:")
        print(f"   运行次数: {stats['v35_runs']}")
        print(f"   平均赞数: {avg_v35:.1f}")
        print(f"   总获赞: {sum(stats['v35_votes']):.0f}")
    
    # v3.0 统计
    if stats["v30_runs"] > 0:
        avg_v30 = sum(stats["v30_votes"]) / len(stats["v30_votes"])
        print(f"\n🤖 v3.0 元学习:")
        print(f"   运行次数: {stats['v30_runs']}")
        print(f"   平均赞数: {avg_v30:.1f}")
        print(f"   总获赞: {sum(stats['v30_votes']):.0f}")
        
        # 对比
        if stats["v35_runs"] > 0:
            diff = avg_v35 - avg_v30
            print(f"\n⚔️  对比:")
            print(f"   v3.5 vs v3.0: {diff:+.1f} 赞")
    
    # 准确度
    if stats["total_predictions"] > 0:
        acc_rate = stats["accurate_predictions"] / stats["total_predictions"] * 100
        print(f"\n🎯 预测准确度: {acc_rate:.0f}%")
    
    print("="*60)

if __name__ == "__main__":
    stats = parse_production_log()
    generate_report(stats)
