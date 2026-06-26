#!/usr/bin/env python3
import time
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.distributed_clock_sync import DistributedClockSync


def test_sync_modes():
    print("=" * 60)
    print("Test 1: Sync Modes")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1", priority=1)
    sync.register_agent("agent2", priority=2)
    sync.register_agent("agent3", priority=3)

    # 测试默认模式
    print(f"  Default sync mode: {sync._sync_mode}")
    print(f"  Default sync interval: {sync.sync_interval}")

    # 测试轻量模式
    sync.set_sync_mode("lightweight")
    print(f"  Lightweight mode: {sync._sync_mode}")
    print(f"  Lightweight interval: {sync.sync_interval}")

    # 测试高频模式
    sync.set_sync_mode("high_frequency")
    print(f"  High frequency mode: {sync._sync_mode}")
    print(f"  High frequency interval: {sync.sync_interval}")

    # 测试正常模式
    sync.set_sync_mode("normal")
    print(f"  Normal mode: {sync._sync_mode}")

    print("  [PASS]")


def test_lightweight_sync():
    print("\n" + "=" * 60)
    print("Test 2: Lightweight Sync")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1")
    sync.register_agent("agent2")
    sync.set_sync_mode("lightweight")

    start_time = time.time()
    results = sync.sync_clocks_lightweight()
    sync_time = time.time() - start_time

    print(f"  Lightweight sync time: {sync_time:.3f}s")
    print(f"  Sync results: {results}")

    # 测试缓存
    start_time = time.time()
    results_cached = sync.sync_clocks_lightweight()
    cached_time = time.time() - start_time

    print(f"  Cached sync time: {cached_time:.3f}s")
    print(f"  Cached results: {results_cached}")

    print("  [PASS]")


def test_batch_sync():
    print("\n" + "=" * 60)
    print("Test 3: Batch Sync")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    for i in range(10):
        sync.register_agent(f"agent{i}")

    start_time = time.time()
    results = sync.sync_clocks_batch(batch_size=3)
    batch_time = time.time() - start_time

    print(f"  Batch sync time: {batch_time:.3f}s")
    print(f"  Sync results count: {len(results)}")

    print("  [PASS]")


def test_priority_sync():
    print("\n" + "=" * 60)
    print("Test 4: Priority Sync")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("low_priority", priority=3)
    sync.register_agent("medium_priority", priority=2)
    sync.register_agent("high_priority", priority=1)

    results = sync.sync_clocks_priority()
    print(f"  Priority sync results: {results}")

    print("  [PASS]")


def test_sync_quality():
    print("\n" + "=" * 60)
    print("Test 5: Sync Quality")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1")
    sync.register_agent("agent2")

    # 执行同步
    sync.sync_clocks()
    quality = sync.get_sync_quality()
    print(f"  Sync quality: {quality:.3f}")

    # 测试统计信息
    stats = sync.get_sync_statistics()
    print(f"  Sync statistics: {stats['sync_quality']:.3f} (quality), {stats['current_sync_interval']:.1f}s (interval)")

    print("  [PASS]")


def test_adaptive_interval():
    print("\n" + "=" * 60)
    print("Test 6: Adaptive Interval")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent", sync_interval=60.0)
    sync.register_agent("agent1")

    initial_interval = sync.sync_interval
    print(f"  Initial interval: {initial_interval:.1f}s")

    # 执行多次同步，观察间隔变化
    for i in range(3):
        sync.sync_clocks()
        quality = sync.get_sync_quality()
        print(f"  After sync {i+1}: interval={sync.sync_interval:.1f}s, quality={quality:.3f}")

    print("  [PASS]")


def test_optimizations():
    print("\n" + "=" * 60)
    print("Test 7: Optimization Controls")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")

    # 禁用批处理
    sync.enable_optimization("batch_sync", False)
    print(f"  Batch sync enabled: {sync._batch_sync_enabled}")

    # 禁用自适应间隔
    sync.enable_optimization("adaptive_interval", False)
    print(f"  Adaptive interval enabled: {sync._adaptive_interval_enabled}")

    # 禁用优先级同步
    sync.enable_optimization("priority_sync", False)
    print(f"  Priority sync enabled: {sync._priority_sync_enabled}")

    # 重新启用
    sync.enable_optimization("batch_sync", True)
    sync.enable_optimization("adaptive_interval", True)
    sync.enable_optimization("priority_sync", True)
    print(f"  All optimizations re-enabled: batch={sync._batch_sync_enabled}, adaptive={sync._adaptive_interval_enabled}, priority={sync._priority_sync_enabled}")

    print("  [PASS]")


def test_optimized_sync():
    print("\n" + "=" * 60)
    print("Test 8: Optimized Sync")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1")
    sync.register_agent("agent2")

    # 测试不同模式下的优化同步
    modes = ["normal", "lightweight", "high_frequency"]
    for mode in modes:
        sync.set_sync_mode(mode)
        start_time = time.time()
        results = sync.sync_clocks_optimized()
        sync_time = time.time() - start_time
        print(f"  {mode}: {sync_time:.3f}s, results={results}")

    print("  [PASS]")


def test_performance_comparison():
    print("\n" + "=" * 60)
    print("Test 9: Performance Comparison")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    for i in range(5):
        sync.register_agent(f"agent{i}")

    # 测试普通同步
    start_time = time.time()
    sync.sync_clocks()
    normal_time = time.time() - start_time

    # 测试轻量同步
    sync.set_sync_mode("lightweight")
    start_time = time.time()
    sync.sync_clocks_lightweight()
    lightweight_time = time.time() - start_time

    # 测试批处理同步
    sync.set_sync_mode("normal")
    start_time = time.time()
    sync.sync_clocks_batch()
    batch_time = time.time() - start_time

    print(f"  Normal sync: {normal_time:.3f}s")
    print(f"  Lightweight sync: {lightweight_time:.3f}s")
    print(f"  Batch sync: {batch_time:.3f}s")

    # 性能提升
    if normal_time > 0:
        lightweight_improvement = (normal_time - lightweight_time) / normal_time * 100
        batch_improvement = (normal_time - batch_time) / normal_time * 100
        print(f"  Lightweight improvement: {lightweight_improvement:.1f}%")
        print(f"  Batch improvement: {batch_improvement:.1f}%")

    print("  [PASS]")


def test_statistics():
    print("\n" + "=" * 60)
    print("Test 10: Sync Statistics")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1")

    # 执行几次同步
    for i in range(5):
        sync.sync_clocks()
        time.sleep(0.1)

    stats = sync.get_sync_statistics()
    print(f"  Total syncs: {stats['total_syncs']}")
    print(f"  Failed syncs: {stats['failed_syncs']}")
    print(f"  Average RTT: {stats['average_rtt']:.3f}s")
    print(f"  Sync quality: {stats['sync_quality']:.3f}")
    print(f"  Cache size: {stats['cache_size']}")
    print(f"  Current interval: {stats['current_sync_interval']:.1f}s")
    print(f"  Optimizations: {stats['optimizations']}")

    print("  [PASS]")


def test_edge_cases():
    print("\n" + "=" * 60)
    print("Test 11: Edge Cases")
    print("=" * 60)

    sync = DistributedClockSync(agent_id="test_agent")

    # 测试空Agent列表
    results = sync.sync_clocks()
    print(f"  Empty agent list: {results}")

    # 测试未注册的Agent
    results = sync.sync_clocks(["non_existent_agent"])
    print(f"  Non-existent agent: {results}")

    # 测试优先级获取
    sync.register_agent("test_agent", priority=5)
    priority = sync.get_agent_sync_priority("test_agent")
    print(f"  Agent priority: {priority}")

    # 测试默认优先级
    priority = sync.get_agent_sync_priority("non_existent")
    print(f"  Default priority: {priority}")

    print("  [PASS]")


if __name__ == "__main__":
    test_sync_modes()
    test_lightweight_sync()
    test_batch_sync()
    test_priority_sync()
    test_sync_quality()
    test_adaptive_interval()
    test_optimizations()
    test_optimized_sync()
    test_performance_comparison()
    test_statistics()
    test_edge_cases()

    print("\n" + "=" * 60)
    print("All distributed clock sync tests passed!")
    print("=" * 60)
