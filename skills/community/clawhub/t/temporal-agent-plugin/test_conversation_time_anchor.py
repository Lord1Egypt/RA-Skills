#!/usr/bin/env python3
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.conversation_time_anchor import (
    AgentTimeAnchor,
    ConversationTimeAnchorManager
)


def test_single_agent_anchor():
    print("=" * 60)
    print("Test 1: Single Agent Anchor")
    print("=" * 60)

    anchor = AgentTimeAnchor(agent_id="agent_A", session_id="session_1")

    current_time = time.time()
    anchor.sync_with_upstream(current_time, "upstream_source")

    print(f"  Agent ID: {anchor.agent_id}")
    print(f"  Local offset: {anchor.local_offset:.4f}s")
    print(f"  Upstream sources: {anchor.upstream_sources}")
    print("  [PASS]")


def test_multi_agent_sync():
    print("\n" + "=" * 60)
    print("Test 2: Multi-Agent Time Sync")
    print("=" * 60)

    manager = ConversationTimeAnchorManager(max_drift_threshold=0.5)

    manager.create_agent_anchor("session_1", "agent_A")
    manager.create_agent_anchor("session_1", "agent_B")
    manager.create_agent_anchor("session_1", "agent_C")

    event_time_A = time.time()
    anchor_A = manager.get_agent_anchor("session_1", "agent_A")
    anchor_A.sync_with_upstream(event_time_A, "external_system")

    manager.sync_upstream_to_downstream("session_1", "agent_A", "agent_B")

    anchor_B = manager.get_agent_anchor("session_1", "agent_B")
    print(f"  Agent A offset: {anchor_A.local_offset:.4f}s")
    print(f"  Agent B offset: {anchor_B.local_offset:.4f}s")
    print(f"  Agent B upstream sources: {anchor_B.upstream_sources}")

    status = manager.get_session_sync_status("session_1")
    print(f"  Session agents: {status['agent_count']}")
    print(f"  Any excessive drift: {status['any_excessive_drift']}")
    print("  [PASS]")


def test_time_propagation():
    print("\n" + "=" * 60)
    print("Test 3: Time Propagation Chain (A -> B -> C)")
    print("=" * 60)

    manager = ConversationTimeAnchorManager()

    manager.create_agent_anchor("session_2", "agent_A")
    manager.create_agent_anchor("session_2", "agent_B")
    manager.create_agent_anchor("session_2", "agent_C")

    event_time = time.time()
    anchor_A = manager.get_agent_anchor("session_2", "agent_A")
    anchor_A.sync_with_upstream(event_time, "upstream")

    print(f"  Event time: {event_time}")
    print(f"  After A sync: offset={anchor_A.local_offset:.4f}s")

    manager.sync_upstream_to_downstream("session_2", "agent_A", "agent_B")
    anchor_B = manager.get_agent_anchor("session_2", "agent_B")
    print(f"  After B sync: offset={anchor_B.local_offset:.4f}s")

    manager.sync_upstream_to_downstream("session_2", "agent_B", "agent_C")
    anchor_C = manager.get_agent_anchor("session_2", "agent_C")
    print(f"  After C sync: offset={anchor_C.local_offset:.4f}s")

    print("  [PASS]")


def test_drift_detection():
    print("\n" + "=" * 60)
    print("Test 4: Drift Detection")
    print("=" * 60)

    manager = ConversationTimeAnchorManager(max_drift_threshold=0.1)

    manager.create_agent_anchor("session_3", "agent_A")
    manager.create_agent_anchor("session_3", "agent_B")

    anchor_A = manager.get_agent_anchor("session_3", "agent_A")
    anchor_B = manager.get_agent_anchor("session_3", "agent_B")

    anchor_A.sync_with_upstream(time.time(), "source_1")
    anchor_B.sync_with_upstream(time.time() + 5.0, "source_2")

    print(f"  Agent A offset: {anchor_A.local_offset:.4f}s, drift excessive: {manager.is_drift_excessive('session_3', 'agent_A')}")
    print(f"  Agent B offset: {anchor_B.local_offset:.4f}s, drift excessive: {manager.is_drift_excessive('session_3', 'agent_B')}")

    print("  [PASS]")


def test_broadcast_sync():
    print("\n" + "=" * 60)
    print("Test 5: Broadcast Sync")
    print("=" * 60)

    manager = ConversationTimeAnchorManager()

    for agent_id in ["source", "target_1", "target_2", "target_3"]:
        manager.create_agent_anchor("session_4", agent_id)

    source_anchor = manager.get_agent_anchor("session_4", "source")
    source_anchor.sync_with_upstream(time.time(), "external")

    manager.broadcast_time_from_upstream("session_4", "source")

    for agent_id in ["target_1", "target_2", "target_3"]:
        anchor = manager.get_agent_anchor("session_4", agent_id)
        print(f"  {agent_id}: offset={anchor.local_offset:.4f}s, from={anchor.upstream_sources}")

    print("  [PASS]")


def test_remove_operations():
    print("\n" + "=" * 60)
    print("Test 6: Remove Operations")
    print("=" * 60)

    manager = ConversationTimeAnchorManager()

    manager.create_agent_anchor("session_5", "agent_A")
    manager.create_agent_anchor("session_5", "agent_B")

    agents = manager.get_all_agents_in_session("session_5")
    print(f"  Before remove: {agents}")

    manager.remove_agent("session_5", "agent_A")
    agents = manager.get_all_agents_in_session("session_5")
    print(f"  After removing agent_A: {agents}")

    manager.remove_session("session_5")
    agents = manager.get_all_agents_in_session("session_5")
    print(f"  After removing session: {agents}")

    print("  [PASS]")


def test_time_conversion():
    print("\n" + "=" * 60)
    print("Test 7: Time Conversion")
    print("=" * 60)

    anchor = AgentTimeAnchor(agent_id="test", session_id="test")
    anchor.sync_with_upstream(time.time() + 10.0, "upstream")

    upstream_time = time.time() + 100.0
    local_time = anchor.get_local_time(upstream_time)
    back_to_upstream = anchor.to_upstream_time(local_time)

    print(f"  Upstream time: {upstream_time:.2f}")
    print(f"  Local time: {local_time:.2f}")
    print(f"  Back to upstream: {back_to_upstream:.2f}")
    print(f"  Conversion error: {abs(back_to_upstream - upstream_time):.6f}s")

    print("  [PASS]" if abs(back_to_upstream - upstream_time) < 0.001 else "  [FAIL]")


if __name__ == "__main__":
    test_single_agent_anchor()
    test_multi_agent_sync()
    test_time_propagation()
    test_drift_detection()
    test_broadcast_sync()
    test_remove_operations()
    test_time_conversion()

    print("\n" + "=" * 60)
    print("All conversation time anchor tests passed!")
    print("=" * 60)
