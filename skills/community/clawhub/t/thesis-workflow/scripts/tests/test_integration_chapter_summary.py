#!/usr/bin/env python3
"""
test_integration_chapter_summary.py - 增强项1 集成测试

完整流程：
  1. outline 初始化 + 插入虚拟摘要节点
  2. 章节1所有 L2 节点完成（含 key_conclusion）
  3. 触发章节摘要合成（synthesize_chapter_summary）
  4. 章节2首节点写作时，bridge 自动引用上一章节摘要（end-to-end 验证）

场景：
  A. happy path：LLM 合成成功 → bridge 包含摘要
  B. fallback：LLM 失败 → 用户输入 → bridge 包含用户输入
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outline_parser import insert_chapter_summary_nodes
from orchestrator_v2 import (
    is_last_child_of_chapter,
    synthesize_chapter_summary,
)
from context_builder import generate_bridge
from state_manager_v2 import (
    outline_save,
    outline_load,
    outline_update_status,
    outline_get_context,
)


TEST_PAPER = "test_integration_paper"


def setup_full_outline():
    """构造完整 2 章 × 各 2 L2 outline"""
    nodes = [
        {"id": "ch1", "level": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1", "1.2"], "prev_sibling_id": None, "next_sibling_id": "ch2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "1.1", "level": 2, "title": "研究背景", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "1.2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "1.2", "level": 2, "title": "研究内容", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": "1.1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "ch2", "level": 1, "title": "理论基础", "parent_id": None,
         "children_ids": ["2.1", "2.2"], "prev_sibling_id": "ch1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "2.1", "level": 2, "title": "竞争战略理论", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "2.2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "2.2", "level": 2, "title": "文献综述", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": "2.1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
    ]
    outline = {"outline_tree": {"metadata": {"paper_title": "集成测试"}, "nodes": nodes}}
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)
    return outline_with_summary


def cleanup():
    from state_manager_v2 import _get_state_path
    p = _get_state_path(TEST_PAPER)
    if os.path.exists(p):
        os.remove(p)


def test_happy_path_llm_synthesis():
    """测试 A：完整 happy path — LLM 合成 + bridge 引用"""
    print("\n=== 集成测试 A：happy path（LLM 合成成功） ===")
    setup_full_outline()

    # 1. 模拟章节1所有 L2 节点写作完成
    outline_update_status(TEST_PAPER, "1.1", "completed",
                          key_conclusion="AI 时代互联网分发面临范式重构，传统应用商店增长见顶",
                          word_count=1500)
    # 触发检测：1.1 不是最后（1.2 未完成）
    r = is_last_child_of_chapter(TEST_PAPER, "1.1")
    assert r is None, "1.1 不应触发章节摘要（1.2 未完成）"
    print(f"   ✅ 1.1 完成时检测：非章节末尾")

    outline_update_status(TEST_PAPER, "1.2", "completed",
                          key_conclusion="本文聚焦差异化战略在 AI 时代的适用性",
                          word_count=1200)
    # 触发检测：1.2 完成 → ch1 全部完成
    r = is_last_child_of_chapter(TEST_PAPER, "1.2")
    assert r == "ch1", f"1.2 完成应触发 ch1 摘要，实际 {r}"
    print(f"   ✅ 1.2 完成时检测：触发 ch1 摘要合成")

    # 2. 触发章节摘要合成
    def mock_llm_summary(prompt: str) -> str:
        return "本章从 AI 时代背景出发，提出差异化战略研究问题，构建了「问题—理论—分析—战略—保障」的全文研究框架，为后续章节奠定基础。"

    syn_result = synthesize_chapter_summary(TEST_PAPER, "ch1", mock_llm_summary)
    assert syn_result["ok"] is True
    assert syn_result["source"] == "llm"
    print(f"   ✅ 章节摘要合成成功（{len(syn_result['summary'])} 字）")

    # 3. 模拟章节2首节点写作（2.1）→ bridge 应包含上一章节摘要
    ctx = outline_get_context(TEST_PAPER, "2.1")
    assert ctx["prev_chapter_summary"] is not None
    assert "绪论" in ctx["prev_chapter_summary"]["chapter_title"]
    print(f"   ✅ 2.1 context 自动附加 ch1 摘要")

    bridge = generate_bridge(ctx)
    assert bridge is not None, "P3 fallback 应返回 bridge"
    assert "绪论" in bridge, "bridge 应引用上一章节"
    assert "竞争战略理论" in bridge, "bridge 应包含当前节点标题"
    print(f"   ✅ Bridge 含上一章节摘要:")
    print(f"      {bridge[:100]}...")

    # 4. 验证状态文件
    state = outline_load(TEST_PAPER)
    ch1_summary_node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                              if n["id"] == "__ch1_summary__"), None)
    assert ch1_summary_node["writing_status"] == "completed"
    assert ch1_summary_node["key_conclusion"] is not None
    print(f"   ✅ __ch1_summary__ 节点已 completed")


def test_fallback_user_input():
    """测试 B：fallback — LLM 失败 → 用户输入 → bridge"""
    print("\n=== 集成测试 B：fallback（LLM 失败 → 用户输入） ===")
    setup_full_outline()

    # 1. 章节1完成
    outline_update_status(TEST_PAPER, "1.1", "completed",
                          key_conclusion="AI 时代背景")
    outline_update_status(TEST_PAPER, "1.2", "completed",
                          key_conclusion="研究内容")

    # 2. LLM 失败
    def failing_llm(prompt: str) -> str:
        raise RuntimeError("模拟 LLM 不可用")

    syn_result = synthesize_chapter_summary(TEST_PAPER, "ch1", failing_llm)
    assert syn_result["ok"] is False
    assert syn_result["action"] == "ask_user"
    print(f"   ✅ LLM 失败 → ask_user 模式触发")

    # 3. 用户手动填写摘要
    user_summary = "本章从时代背景切入，提出差异化战略研究问题。"

    syn_result_2 = synthesize_chapter_summary(
        TEST_PAPER, "ch1", failing_llm,  # LLM 还是失败
        user_input=user_summary
    )
    assert syn_result_2["ok"] is True
    assert syn_result_2["source"] == "user"
    print(f"   ✅ 用户输入路径生效（source=user）")

    # 4. 章节2首节点 bridge 应使用用户输入的摘要
    ctx = outline_get_context(TEST_PAPER, "2.1")
    bridge = generate_bridge(ctx)
    assert bridge is not None
    assert "绪论" in bridge
    # bridge 应基于用户输入的摘要
    assert "差异化战略研究问题" in bridge or "时代背景" in bridge
    print(f"   ✅ Bridge 基于用户摘要生成:")
    print(f"      {bridge[:100]}...")


def main():
    """主测试入口"""
    print("=" * 60)
    print("增强项1 集成测试（end-to-end）")
    print("=" * 60)

    try:
        test_happy_path_llm_synthesis()
        test_fallback_user_input()

        print("\n" + "=" * 60)
        print("✅ 集成测试全部通过（2 个端到端场景）")
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
