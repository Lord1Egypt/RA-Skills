#!/usr/bin/env python3
"""
时间同步验证脚本

简单测试时间锚点的时间同步功能，验证时间不对齐问题是否已解决。
"""

import time
from src.core.time_anchor import TimeAnchorInjector

def test_time_synchronization():
    """测试时间同步功能"""
    print("=== 时间同步验证 ===")
    
    injector = TimeAnchorInjector()
    
    # 创建会话
    session_id = "test_session"
    injector.create_session(session_id)
    
    # 测试初始时间
    initial_time = injector.get_current_timestamp(session_id)
    print(f"初始时间: {initial_time}")
    
    # 模拟时间偏移
    reference_time = time.time() + 10.0  # 人为设置时间偏移10秒
    print(f"参考时间: {reference_time}")
    
    # 执行时间同步
    injector.sync_time(session_id, reference_time)
    
    # 验证同步后的时间
    synced_time = injector.get_current_timestamp(session_id)
    print(f"同步后时间: {synced_time}")
    
    # 计算同步误差
    sync_error = abs(synced_time - reference_time)
    print(f"同步误差: {sync_error:.6f}秒")
    
    # 测试时间漂移检测
    drift = injector.get_time_drift(session_id)
    print(f"时间漂移: {drift:.6f}秒")
    print(f"漂移过大: {injector.is_time_drift_excessive(session_id)}")
    
    # 测试时间锚点注入
    prompt = "What time is it now?"
    injected = injector.inject_time_anchor(prompt, session_id=session_id)
    print("\n时间锚点注入:")
    print(injected)
    
    # 清理会话
    injector.remove_session(session_id)
    
    return sync_error < 0.1

def test_session_isolation():
    """测试会话隔离功能"""
    print("\n=== 会话隔离验证 ===")
    
    injector = TimeAnchorInjector()
    
    # 创建两个会话
    session1 = "session_1"
    session2 = "session_2"
    
    injector.create_session(session1)
    injector.create_session(session2)
    
    # 为会话1设置时间偏移
    reference_time1 = time.time() + 5.0
    injector.sync_time(session1, reference_time1)
    
    # 获取两个会话的时间
    time1 = injector.get_current_timestamp(session1)
    time2 = injector.get_current_timestamp(session2)
    
    print(f"会话1时间: {time1}")
    print(f"会话2时间: {time2}")
    print(f"时间差: {abs(time1 - time2):.6f}秒")
    
    # 验证会话隔离
    session_isolated = abs(time1 - time2) > 4.0
    print(f"会话隔离成功: {session_isolated}")
    
    # 清理会话
    injector.clear_all_sessions()
    
    return session_isolated

def test_time_anchor_headers():
    """测试时间锚点头部注入"""
    print("\n=== 时间锚点头部验证 ===")
    
    injector = TimeAnchorInjector()
    
    # 测试时间锚点注入
    prompt = "Hello, what's the current time?"
    injected = injector.inject_time_anchor(prompt)
    
    print("原始提示词:")
    print(prompt)
    print("\n注入时间锚点后:")
    print(injected)
    
    # 验证时间锚点头部存在
    has_header = "[时间锚点]" in injected
    has_time = "当前时间：" in injected
    has_timezone = "时区：" in injected
    
    print(f"\n验证结果:")
    print(f"包含时间锚点头部: {has_header}")
    print(f"包含当前时间: {has_time}")
    print(f"包含时区: {has_timezone}")
    
    return has_header and has_time and has_timezone

if __name__ == "__main__":
    print("时间同步验证脚本")
    print("=" * 50)
    
    # 运行测试
    test1_passed = test_time_synchronization()
    test2_passed = test_session_isolation()
    test3_passed = test_time_anchor_headers()
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"时间同步测试: {'通过' if test1_passed else '失败'}")
    print(f"会话隔离测试: {'通过' if test2_passed else '失败'}")
    print(f"时间锚点注入测试: {'通过' if test3_passed else '失败'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 所有测试通过！时间不对齐问题已解决。")
    else:
        print("\n❌ 部分测试失败，需要进一步优化。")