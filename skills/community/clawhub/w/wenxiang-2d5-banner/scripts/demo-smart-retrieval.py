#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Smart Retrieval with Cost Savings
展示智能触发如何节省成本
"""

import sys
import os
sys.path.insert(0, 'hooks')

from smart_retrieval_trigger import SmartRetrievalTrigger

print("=" * 70)
print("Smart Retrieval Demo - Cost Savings")
print("=" * 70)

# Create trigger
trigger = SmartRetrievalTrigger(debug=True)

# Simulate a day's conversations
daily_conversations = [
    # Morning greetings (should skip)
    "早",
    "你好",
    "在吗",
    
    # Questions (should trigger)
    "TTS 应该怎么用？",
    "阿里云 Embedding 配置好了吗？",
    "我记得你说过瀑布的事情",
    
    # Small talk (should skip)
    "吃了吗",
    "在干嘛",
    "哈哈",
    
    # Long messages (should trigger)
    "今天天气不错，适合出去走走看看风景",
    "帮我查一下之前的对话记录，关于向量数据库的部分",
    
    # More questions (should trigger)
    "之前提到的供应商直连系统进度怎么样？",
    "什么是语义搜索？",
    
    # Confirmations (should skip)
    "好的",
    "收到",
    "谢谢",
    
    # More questions (should trigger)
    "为什么之前会失败？",
    "那个天台瀑布在哪里？",
]

print(f"\n[模拟一天对话] 共 {len(daily_conversations)} 条\n")

for i, message in enumerate(daily_conversations, 1):
    should_retrieve, reason = trigger.should_retrieve(message)
    status = "🔍 检索" if should_retrieve else "⏭️ 跳过"
    print(f"{i:2d}. {status} | '{message}'")
    if trigger.config["debug"]:
        print(f"      原因：{reason}")

# Statistics
stats = trigger.get_stats()

print(f"\n{'='*70}")
print(f"[统计]")
print(f"  总消息数：{stats['total']}")
print(f"  触发检索：{stats['triggered']} 条 ({stats['trigger_rate']})")
print(f"  跳过检索：{stats['skipped']} 条 ({stats['skip_rate']})")
print(f"  预计节省：{stats['estimated_savings']}")

# Cost calculation
print(f"\n[成本计算]")

api_cost_per_call = 0.0005  # 元/次
daily_calls_original = len(daily_conversations)
daily_calls_optimized = stats['triggered']

daily_cost_original = daily_calls_original * api_cost_per_call
daily_cost_optimized = daily_calls_optimized * api_cost_per_call

monthly_cost_original = daily_cost_original * 30
monthly_cost_optimized = daily_cost_optimized * 30

savings = monthly_cost_original - monthly_cost_optimized
savings_percent = savings / monthly_cost_original * 100

print(f"  单次 API 成本：{api_cost_per_call} 元")
print(f"")
print(f"  每日调用（原方案）：{daily_calls_original} 次")
print(f"  每日调用（优化后）：{daily_calls_optimized} 次")
print(f"  减少调用：{daily_calls_original - daily_calls_optimized} 次")
print(f"")
print(f"  每月成本（原方案）：{monthly_cost_original:.2f} 元")
print(f"  每月成本（优化后）：{monthly_cost_optimized:.2f} 元")
print(f"  每月节省：{savings:.2f} 元 ({savings_percent:.0f}%)")

print(f"\n{'='*70}")
print(f"✅ 智能触发优化成功！")
print(f"   节省 {stats['estimated_savings']} 的 API 调用")
print(f"   每月节省 {savings:.2f} 元")
print(f"{'='*70}")
