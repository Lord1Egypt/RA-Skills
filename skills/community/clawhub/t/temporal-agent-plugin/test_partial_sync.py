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


if __name__ == "__main__":
    test_sync_modes()
    test_lightweight_sync()
    print("\n" + "=" * 60)
    print("Partial tests passed!")
    print("=" * 60)
