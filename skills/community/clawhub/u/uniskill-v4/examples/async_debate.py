#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 - Async Debate Example

High-performance async multi-model debate
"""

import asyncio
import sys
sys.path.insert(0, '..')

from idea_debater_v4 import HighSpeedDebater


async def run_multiple_debates():
    """Run multiple debates concurrently"""
    
    debater = HighSpeedDebater(timeout=10, max_memory_mb=50)
    
    # Multiple problems to debate
    problems = [
        ("技术选型", ["Python", "JavaScript", "Go", "Rust"]),
        ("部署方案", ["Kubernetes", "Docker Compose", "VM"]),
        ("数据存储", ["PostgreSQL", "MongoDB", "Redis"]),
    ]
    
    # Run all debates concurrently
    tasks = [
        debater.debate_async(problem, solutions)
        for problem, solutions in problems
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Print results
    print("=" * 50)
    print("UniSkill V4 - Async Multi-Debate Demo")
    print("=" * 50)
    
    for (problem, _), result in zip(problems, results):
        print(f"\n📊 {problem}")
        print(f"  推荐: {result.recommended}")
        print(f"  评分: {result.score:.2f}")
        print(f"  置信度: {result.confidence*100:.1f}%")


async def benchmark_debate():
    """Benchmark async performance"""
    import time
    
    debater = HighSpeedDebater()
    
    solutions = ["方案A", "方案B", "方案C"]
    
    # Sequential
    start = time.time()
    for _ in range(3):
        debater.debate("测试问题", solutions)
    seq_time = time.time() - start
    
    # Concurrent
    start = time.time()
    await asyncio.gather(*[
        debater.debate_async(f"问题{i}", solutions)
        for i in range(3)
    ])
    async_time = time.time() - start
    
    print("\n" + "=" * 50)
    print("⚡ Performance Benchmark")
    print("=" * 50)
    print(f"顺序执行: {seq_time:.2f}s")
    print(f"并发执行: {async_time:.2f}s")
    print(f"加速比: {seq_time/async_time:.2f}x")


async def main():
    await run_multiple_debates()
    await benchmark_debate()
    
    print("\n✅ Async Demo Complete!")


if __name__ == "__main__":
    asyncio.run(main())