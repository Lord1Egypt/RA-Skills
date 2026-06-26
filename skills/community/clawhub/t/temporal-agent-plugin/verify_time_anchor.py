#!/usr/bin/env python3
"""
时间锚点验证脚本

测试时间锚点的时间同步和会话管理功能，验证时间不对齐问题是否已解决。
"""

import time
from src.core.time_anchor import TimeAnchorInjector

def test_time_anchor_basic():
    """测试基本时间锚点功能"""
    print("=== 测试基本时间锚点功能 ===")
    
    injector = TimeAnchorInjector()
    
    # 测试时间上下文
    time_context = injector.get_time_context()
    print(f"当前时间: {time_context['current_time']}")
    print(f"日期: {time_context['current_date']}")
    print(f"时间: {time_context['current_time_only']}")
    print(f"星期: {time_context['day_of_week_chinese']}")
    print(f"时区: {time_context['timezone']}")
    print()

def test_session_management():
    """测试会话管理功能"""
    print("=== 测试会话管理功能 ===")
    
    injector = TimeAnchorInjector()
    
    # 创建会话
    session1 = injector.create_session("test_session_1")
    session2 = injector.create_session("test_session_2")
    
    print(f"创建会话1: {session1.session_id}")
    print(f"创建会话2: {session2.session_id}")
    
    # 获取会话上下文
    context1 = injector.get_session_context("test_session_1")
    context2 = injector.get_session_context("test_session_2")
    
    print(f"会话1存在: {context1 is not None}")
    print(f"会话2存在: {context2 is not None}")
    
    # 测试会话时间
    time1 = injector.get_current_timestamp("test_session_1")
    time2 = injector.get_current_timestamp("test_session_2")
    
    print(f"会话1时间戳: {time1}")
    print(f"会话2时间戳: {time2}")
    print(f"时间差: {abs(time1 - time2):.6f}秒")
    
    # 测试时间同步
    reference_time = time.time() + 5.0  # 模拟时间偏移
    injector.sync_time("test_session_1", reference_time)
    
    synced_time = injector.get_current_timestamp("test_session_1")
    print(f"同步后会话1时间: {synced_time}")
    print(f"与参考时间的误差: {abs(synced_time - reference_time):.6f}秒")
    
    # 测试时间漂移检测
    drift = injector.get_time_drift("test_session_1")
    print(f"时间漂移: {drift:.6f}秒")
    print(f"漂移过大: {injector.is_time_drift_excessive('test_session_1')}")
    
    # 清理会话
    injector.remove_session("test_session_1")
    injector.remove_session("test_session_2")
    
    print(f"会话1清理后存在: {injector.get_session_context('test_session_1') is not None}")
    print(f"会话2清理后存在: {injector.get_session_context('test_session_2') is not None}")
    print()

def test_time_anchor_injection():
    """测试时间锚点注入功能"""
    print("=== 测试时间锚点注入功能 ===")
    
    injector = TimeAnchorInjector()
    
    # 创建会话
    injector.create_session("test_session")
    
    # 测试时间锚点注入
    prompt = "Hello, what time is it?"
    injected = injector.inject_time_anchor(prompt, session_id="test_session")
    
    print("原始提示词:")
    print(f"{prompt}")
    print("\n注入时间锚点后:")
    print(f"{injected}")
    print()

def test_time_sync_accuracy():
    """测试时间同步精度"""
    print("=== 测试时间同步精度 ===")
    
    injector = TimeAnchorInjector()
    injector.create_session("sync_test")
    
    # 多次同步测试
    for i in range(3):
        reference_time = time.time() + (i + 1) * 2
        injector.sync_time("sync_test", reference_time)
        synced_time = injector.get_current_timestamp("sync_test")
        error = abs(synced_time - reference_time)
        
        print(f"同步 {i+1}: 参考时间={reference_time:.6f}, 同步后={synced_time:.6f}, 误差={error:.6f}秒")
        
        # 等待一小段时间
        time.sleep(0.1)
    
    print()

def test_multiple_sessions():
    """测试多会话管理"""
    print("=== 测试多会话管理 ===")
    
    injector = TimeAnchorInjector()
    
    # 创建多个会话
    session_ids = [f"session_{i}" for i in range(5)]
    for session_id in session_ids:
        injector.create_session(session_id)
    
    # 获取所有会话
    sessions = injector.get_all_sessions()
    print(f"创建了 {len(sessions)} 个会话")
    
    # 测试每个会话的时间
    for session in sessions:
        session_time = injector.get_current_timestamp(session.session_id)
        print(f"{session.session_id}: {session_time:.6f}")
    
    # 清理所有会话
    injector.clear_all_sessions()
    remaining_sessions = injector.get_all_sessions()
    print(f"清理后剩余会话数: {len(remaining_sessions)}")
    print()

if __name__ == "__main__":
    print("时间锚点验证脚本")
    print("=" * 50)
    
    test_time_anchor_basic()
    test_session_management()
    test_time_anchor_injection()
    test_time_sync_accuracy()
    test_multiple_sessions()
    
    print("=" * 50)
    print("验证完成！")