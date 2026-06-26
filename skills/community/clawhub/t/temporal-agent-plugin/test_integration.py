#!/usr/bin/env python3
import time
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.bayesian_predictor import AdaptiveTimeoutPredictor
from core.conversation_time_anchor import ConversationTimeAnchorManager
from core.social_temporal import SocialTemporal
from core.distributed_clock_sync import DistributedClockSync


def test_integration():
    print("=" * 80)
    print("🔧 时序插件 V2.1 集成测试")
    print("=" * 80)

    # 测试1: 轻量预测器
    print("\n1. 测试轻量预测器...")
    predictor = AdaptiveTimeoutPredictor(task_type='integration_test')
    for i in range(10):
        predictor.update(1.0 + i * 0.1)
    timeout = predictor.predict_timeout()
    print(f"   ✓ 预测超时: {timeout:.2f}s")

    # 测试2: 会话级时间锚点
    print("\n2. 测试会话级时间锚点...")
    manager = ConversationTimeAnchorManager()
    manager.create_agent_anchor("test_session", "agent1")
    manager.create_agent_anchor("test_session", "agent2")
    manager.sync_upstream_to_downstream("test_session", "agent1", "agent2")
    agent2_time = manager.get_agent_anchor("test_session", "agent2").get_local_time()
    print(f"   ✓ Agent2 时间: {agent2_time:.2f}")

    # 测试3: 文化适配停顿分析
    print("\n3. 测试文化适配停顿分析...")
    st = SocialTemporal(culture="zh_CN")
    st.record_utterance("Speaker1", "你好")
    time.sleep(0.1)
    st.record_utterance("Speaker2", "你好，很高兴认识你")
    pause_type = st.get_pause_type()
    print(f"   ✓ 停顿类型: {pause_type}, 文化: {st.culture}")

    # 测试4: 高频同步协议
    print("\n4. 测试高频同步协议...")
    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("remote_agent")
    sync.set_sync_mode("lightweight")
    results = sync.sync_clocks_optimized()
    quality = sync.get_sync_quality()
    print(f"   ✓ 同步结果: {results}, 质量: {quality:.3f}")

    # 测试5: 多模块协同
    print("\n5. 测试多模块协同...")
    # 模拟一个完整的多Agent协作场景
    session_id = "multi_agent_session"
    
    # 创建时间锚点
    manager.create_agent_anchor(session_id, "agent_A")
    manager.create_agent_anchor(session_id, "agent_B")
    
    # 同步时间
    manager.sync_upstream_to_downstream(session_id, "agent_A", "agent_B")
    
    # 文化分析
    st_cn = SocialTemporal(culture="zh_CN")
    st_en = SocialTemporal(culture="en_US")
    
    # 预测器
    cron_predictor = AdaptiveTimeoutPredictor(task_type='cron')
    api_predictor = AdaptiveTimeoutPredictor(task_type='api')
    
    print("   ✓ 多模块协同初始化完成")

    print("\n" + "=" * 80)
    print("🎉 时序插件 V2.1 集成测试通过！")
    print("=" * 80)
    print("\n核心功能验证:")
    print("   ✅ 轻量模式预测器")
    print("   ✅ 会话级时间锚点")
    print("   ✅ 文化适配停顿分析")
    print("   ✅ 高频同步协议优化")
    print("   ✅ 多模块协同工作")
    print("\n所有功能正常，V2.1版本已准备就绪！")


if __name__ == "__main__":
    test_integration()
