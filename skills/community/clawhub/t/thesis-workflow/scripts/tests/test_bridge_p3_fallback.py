#!/usr/bin/env python3
"""
test_bridge_p3_fallback.py - 增强项1 P3 fallback 跨章节桥接 单元测试

覆盖场景：
  1. 同章节前序节点 → P1 命中（不应走 P3）
  2. 父节点有结论 → P2 命中（不应走 P3）
  3. 跨章节首节点 + 上一章节有摘要 → P3 命中（增强项1 核心场景）
  4. 跨章节首节点 + 上一章节摘要未合成 → 返回 None（降级）
  5. 首章节首节点 → 无上游 → 返回 None
  6. outline_get_context 自动附加 prev_chapter_summary 字段
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_builder import generate_bridge
from outline_parser import insert_chapter_summary_nodes
from state_manager_v2 import (
    outline_save,
    outline_load,
    outline_update_status,
    outline_get_context,
)


TEST_PAPER = "test_bridge_p3_paper"


def setup_outline():
    """构造 2 章 × 2 L2 测试 outline，并初始化虚拟摘要节点"""
    nodes = [
        # Chapter 1
        {"id": "ch1", "level": 1, "num": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1", "1.2"], "prev_sibling_id": None, "next_sibling_id": "ch2",
         "writing_status": "completed", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "1.1", "level": 2, "num": "1.1", "title": "研究背景", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "1.2",
         "writing_status": "completed", "key_conclusion": "AI 时代互联网分发面临范式重构",
         "word_count": 1500, "content": "x"},
        {"id": "1.2", "level": 2, "num": "1.2", "title": "研究内容", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": "1.1", "next_sibling_id": None,
         "writing_status": "completed", "key_conclusion": "本文聚焦差异化战略研究",
         "word_count": 1200, "content": "x"},
        # Chapter 2
        {"id": "ch2", "level": 1, "num": 2, "title": "理论基础", "parent_id": None,
         "children_ids": ["2.1", "2.2"], "prev_sibling_id": "ch1", "next_sibling_id": None,
         "writing_status": "completed", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "2.1", "level": 2, "num": "2.1", "title": "竞争战略理论", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "2.2",
         "writing_status": "completed", "key_conclusion": "Porter 三种基本竞争战略",
         "word_count": 1800, "content": "x"},
        {"id": "2.2", "level": 2, "num": "2.2", "title": "文献综述", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": "2.1", "next_sibling_id": None,
         "writing_status": "completed", "key_conclusion": "AI 时代文献聚焦差异化",
         "word_count": 1500, "content": "x"},
    ]

    outline = {"outline_tree": {"metadata": {"paper_title": "测试"}, "nodes": nodes}}
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)
    return outline_with_summary


def cleanup():
    from state_manager_v2 import _get_state_path
    p = _get_state_path(TEST_PAPER)
    if os.path.exists(p):
        os.remove(p)


def test_p1_prev_takes_priority():
    """测试 1：P1 命中 → 不走 P3"""
    print("\n=== 测试 1：P1 前序节点命中 ===")
    setup_outline()

    context = {
        "current_node": {"id": "1.2", "title": "研究内容", "level": 2},
        "prev_node": {"id": "1.1", "title": "研究背景", "level": 2,
                      "key_conclusion": "AI 时代互联网分发面临范式重构"},
        "parent_node": {"id": "ch1", "title": "绪论", "key_conclusion": None},
        "prev_chapter_summary": {  # 即使有 P3 也不应走
            "chapter_id": "ch0",
            "chapter_title": "fake chapter",
            "key_conclusion": "fake summary"
        }
    }

    bridge = generate_bridge(context)
    assert bridge is not None
    assert "1.1" not in bridge and "fake" not in bridge
    assert "研究背景" in bridge, f"P1 应引用前序节点 '研究背景'，实际: {bridge}"
    print(f"   ✅ P1 命中（包含「研究背景」）")
    print(f"   ✅ 未走 P3（无 'fake' 字样）")


def test_p2_parent_takes_priority():
    """测试 2：P2 命中（无 prev） → 不走 P3"""
    print("\n=== 测试 2：P2 父节点命中 ===")
    setup_outline()

    context = {
        "current_node": {"id": "1.1", "title": "研究背景", "level": 2},
        "prev_node": None,
        "parent_node": {"id": "ch1", "title": "绪论",
                        "key_conclusion": "本章提出研究问题"},
        "prev_chapter_summary": None
    }

    bridge = generate_bridge(context)
    assert bridge is not None
    assert "绪论" in bridge and "研究问题" in bridge
    print(f"   ✅ P2 命中（包含「绪论」「研究问题」）")


def test_p3_cross_chapter_fallback():
    """测试 3：P3 命中 — 跨章节首节点 + 上一章节摘要"""
    print("\n=== 测试 3：P3 跨章节桥接（增强项1 核心） ===")
    setup_outline()

    # 模拟章节摘要已合成
    outline_update_status(
        TEST_PAPER, "__ch1_summary__", "completed",
        key_conclusion="本章从 AI 时代背景出发，提出差异化战略研究问题，构建了论文的整体研究框架。",
        word_count=50
    )

    context = {
        "current_node": {"id": "2.1", "title": "竞争战略理论", "level": 2},
        "prev_node": None,         # 跨章节无 prev
        "parent_node": {"id": "ch2", "title": "理论基础",
                        "key_conclusion": None},  # 父节点无 key_conclusion
        "prev_chapter_summary": {
            "chapter_id": "ch1",
            "chapter_title": "绪论",
            "key_conclusion": "本章从 AI 时代背景出发，提出差异化战略研究问题，构建了论文的整体研究框架。"
        }
    }

    bridge = generate_bridge(context)
    assert bridge is not None, "P3 fallback 应返回承接段"
    assert "绪论" in bridge, f"P3 应引用上一章节 '绪论'，实际: {bridge}"
    assert "竞争战略理论" in bridge, f"P3 应包含当前节点标题，实际: {bridge}"
    print(f"   ✅ P3 命中（包含「绪论」+ 当前节点）")
    print(f"   ✅ Bridge: {bridge[:80]}...")


def test_p3_unavailable_returns_none():
    """测试 4：P3 不可用 → 返回 None"""
    print("\n=== 测试 4：上一章节摘要未合成 → 返回 None ===")
    setup_outline()

    # 不设置 __ch1_summary__ 的 key_conclusion
    context = {
        "current_node": {"id": "2.1", "title": "竞争战略理论", "level": 2},
        "prev_node": None,
        "parent_node": {"id": "ch2", "title": "理论基础",
                        "key_conclusion": None},
        "prev_chapter_summary": None  # 摘要未合成
    }

    bridge = generate_bridge(context)
    assert bridge is None, "无上游时应返回 None"
    print(f"   ✅ 无上游 → 返回 None（NodeWriter 自行处理）")


def test_first_chapter_no_prev_summary():
    """测试 5：首章节首节点 → 无上游 → 返回 None"""
    print("\n=== 测试 5：首章节首节点 ===")
    setup_outline()

    context = {
        "current_node": {"id": "1.1", "title": "研究背景", "level": 2},
        "prev_node": None,
        "parent_node": {"id": "ch1", "title": "绪论", "key_conclusion": None},
        "prev_chapter_summary": None  # ch1 是首章节，无上一章节
    }

    bridge = generate_bridge(context)
    assert bridge is None, "首章节首节点应返回 None"
    print(f"   ✅ 首章节首节点 → 返回 None")


def test_outline_get_context_includes_prev_chapter_summary():
    """测试 6：outline_get_context 自动附加 prev_chapter_summary"""
    print("\n=== 测试 6：outline_get_context 自动附加 P3 ===")
    setup_outline()

    # 合成 ch1 摘要
    outline_update_status(
        TEST_PAPER, "__ch1_summary__", "completed",
        key_conclusion="本章系统提出研究问题，奠定全文分析基础。"
    )

    # 获取 2.1 的上下文（应自动附加 ch1 摘要）
    context = outline_get_context(TEST_PAPER, "2.1")
    assert context is not None
    assert "prev_chapter_summary" in context

    prev_summary = context["prev_chapter_summary"]
    assert prev_summary is not None
    assert prev_summary["chapter_id"] == "ch1"
    assert prev_summary["chapter_title"] == "绪论"
    assert "研究问题" in prev_summary["key_conclusion"]
    print(f"   ✅ outline_get_context 自动附加 prev_chapter_summary")
    print(f"   ✅ chapter_id={prev_summary['chapter_id']}, title={prev_summary['chapter_title']}")

    # 首章节首节点（1.1）应没有 prev_chapter_summary
    ctx_first = outline_get_context(TEST_PAPER, "1.1")
    assert ctx_first["prev_chapter_summary"] is None
    print(f"   ✅ 1.1（首章节首节点）：prev_chapter_summary=None")


def main():
    """主测试入口"""
    print("=" * 60)
    print("增强项1 P3 fallback 跨章节桥接 单元测试")
    print("=" * 60)

    try:
        test_p1_prev_takes_priority()
        test_p2_parent_takes_priority()
        test_p3_cross_chapter_fallback()
        test_p3_unavailable_returns_none()
        test_first_chapter_no_prev_summary()
        test_outline_get_context_includes_prev_chapter_summary()

        print("\n" + "=" * 60)
        print("✅ 全部测试通过（6 个测试用例）")
        print("=" * 60)
        cleanup()
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        cleanup()
        return 1
    except Exception as e:
        print(f"\n❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        return 2


if __name__ == "__main__":
    sys.exit(main())
