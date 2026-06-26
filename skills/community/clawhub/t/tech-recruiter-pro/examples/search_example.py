#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索候选人示例
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from recruiter import TechRecruiterPro


def main():
    """主函数"""
    print("=" * 60)
    print("TechRecruiter Pro - 搜索候选人示例")
    print("=" * 60)
    
    recruiter = TechRecruiterPro()
    
    # 示例 1: 搜索 RLHF 方向研究员
    print("\n🔍 示例 1: 搜索 RLHF 方向研究员")
    print("-" * 60)
    
    candidates = recruiter.search_candidates(
        keywords=["RLHF", "PPO", "LLM", "Alignment"],
        target_companies=["DeepMind", "OpenAI", "Meta", "Moonshot"],
        min_citations=100,
        min_h_index=10
    )
    
    print(f"\n✅ 找到 {len(candidates)} 位候选人")
    
    # 示例 2: 搜索大模型方向
    print("\n\n🔍 示例 2: 搜索大模型方向工程师")
    print("-" * 60)
    
    candidates2 = recruiter.search_candidates(
        keywords=["Large Language Model", "Transformer", "Pretraining"],
        target_companies=["Google", "Microsoft", "Anthropic"],
        min_citations=200
    )
    
    print(f"\n✅ 找到 {len(candidates2)} 位候选人")
    
    # 示例 3: 搜索计算机视觉方向
    print("\n\n🔍 示例 3: 搜索计算机视觉方向研究员")
    print("-" * 60)
    
    candidates3 = recruiter.search_candidates(
        keywords=["Computer Vision", "Image Generation", "Diffusion"],
        target_companies=["OpenAI", "Stability AI", "Runway"],
        min_citations=150
    )
    
    print(f"\n✅ 找到 {len(candidates3)} 位候选人")
    
    # 导出报告
    print("\n\n📊 导出招聘报告")
    print("-" * 60)
    
    recruiter.export_report("example_recruiting_report.md")
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()
