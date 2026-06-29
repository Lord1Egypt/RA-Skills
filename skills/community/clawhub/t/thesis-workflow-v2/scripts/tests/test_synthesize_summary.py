#!/usr/bin/env python3
"""
test_synthesize_summary.py - 增强项1 章节摘要合成 单元测试

覆盖场景：
  1. is_last_child_of_chapter 边界（首个/中间/末尾节点）
  2. synthesize_chapter_summary 正常流程（LLM 路径）
  3. synthesize_chapter_summary 用户输入路径
  4. synthesize_chapter_summary LLM 失败 → ask_user
  5. synthesize_chapter_summary 空子节点结论
  6. 章节摘要超长截断到 300 字
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outline_parser import (
    insert_chapter_summary_nodes,
    outline_parse,
)
from orchestrator_v2 import (
    is_last_child_of_chapter,
    synthesize_chapter_summary,
)
from state_manager_v2 import (
    outline_save,
    outline_load,
    outline_update_status,
)


TEST_PAPER = "test_synthesize_summary_paper"


def setup_outline():
    """
    构造测试用的 outline_state，2 个 L1 章节 + 各 2 个 L2。
    初始：所有 L2 节点 pending（用于测试边界）。
    写入 ~/.openclaw/workspace/<paper>/_outline_state.json
    """
    import os as _os
    from state_manager_v2 import _get_paper_dir, _get_state_path

    paper_dir = _get_paper_dir(TEST_PAPER)
    state_path = _get_state_path(TEST_PAPER)

    nodes = [
        {"id": "ch1", "level": 1, "num": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1", "1.2"], "prev_sibling_id": None, "next_sibling_id": "ch2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "1.1", "level": 2, "num": "1.1", "title": "研究背景", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "1.2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "1.2", "level": 2, "num": "1.2", "title": "研究内容", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": "1.1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "ch2", "level": 1, "num": 2, "title": "理论基础", "parent_id": None,
         "children_ids": ["2.1", "2.2"], "prev_sibling_id": "ch1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None,
         "content": None},
        {"id": "2.1", "level": 2, "num": "2.1", "title": "竞争战略理论", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "2.2",
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
        {"id": "2.2", "level": 2, "num": "2.2", "title": "文献综述", "parent_id": "ch2",
         "children_ids": [], "prev_sibling_id": "2.1", "next_sibling_id": None,
         "writing_status": "pending", "key_conclusion": None, "word_count": None, "content": None},
    ]

    # 插入虚拟摘要节点
    outline = {
        "outline_tree": {
            "metadata": {"paper_title": "测试", "total_nodes": 6},
            "nodes": nodes,
        }
    }
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)

    return outline_with_summary


def cleanup():
    """清理测试状态"""
    from state_manager_v2 import _get_state_path
    import os as _os
    path = _get_state_path(TEST_PAPER)
    if _os.path.exists(path):
        _os.remove(path)
    paper_dir = _os.path.dirname(path)
    if _os.path.exists(paper_dir) and not _os.listdir(paper_dir):
        _os.rmdir(paper_dir)


def test_is_last_child_of_chapter():
    """测试 1：is_last_child_of_chapter 边界判断"""
    print("\n=== 测试 1：is_last_child_of_chapter 边界 ===")
    setup_outline()

    # 初始状态：所有 L2 都 pending
    # 模拟 1.1 完成
    outline_update_status(TEST_PAPER, "1.1", "completed", key_conclusion="AI 背景")
    r = is_last_child_of_chapter(TEST_PAPER, "1.1")
    assert r is None, f"1.1 写完时（1.2 未完成）应返回 None，实际 {r}"
    print("   ✅ 1.1 写完时（1.2 未完成）：非章节末尾")

    # 模拟 1.2 完成 → ch1 章节全部完成 → 返回 ch1
    outline_update_status(TEST_PAPER, "1.2", "completed", key_conclusion="研究内容")
    r = is_last_child_of_chapter(TEST_PAPER, "1.2")
    assert r == "ch1", f"1.2 写完时（ch1 全完成）应返回 'ch1'，实际 {r}"
    print("   ✅ 1.2 写完时（ch1 章节全完成）：章节末尾 → ch1")

    # 模拟 2.1 完成
    outline_update_status(TEST_PAPER, "2.1", "completed", key_conclusion="Porter")
    r = is_last_child_of_chapter(TEST_PAPER, "2.1")
    assert r is None, f"2.1 写完时（2.2 未完成）应返回 None，实际 {r}"
    print("   ✅ 2.1 写完时（2.2 未完成）：非章节末尾")

    # 模拟 2.2 完成 → ch2 章节全部完成
    outline_update_status(TEST_PAPER, "2.2", "completed", key_conclusion="文献")
    r = is_last_child_of_chapter(TEST_PAPER, "2.2")
    assert r == "ch2", f"2.2 写完时（ch2 全完成）应返回 'ch2'，实际 {r}"
    print("   ✅ 2.2 写完时（ch2 全完成）：章节末尾 → ch2")


def test_synthesize_llm_path():
    """测试 2：synthesize_chapter_summary LLM 路径"""
    print("\n=== 测试 2：synthesize_chapter_summary LLM 路径 ===")
    setup_outline()

    # 模拟 2.1 和 2.2 都完成
    outline_update_status(TEST_PAPER, "2.1", "completed", key_conclusion="Porter 提出三种基本竞争战略：成本领先、差异化、集中化")
    outline_update_status(TEST_PAPER, "2.2", "completed", key_conclusion="近年文献聚焦数字化与 AI 时代的战略选择")

    captured_prompt = {}

    def mock_llm(prompt: str) -> str:
        captured_prompt["text"] = prompt
        return "本章系统梳理了竞争战略理论基础，包括 Porter 的三种基本战略框架，并结合 AI 时代文献综述，论证了差异化战略的适用性。"

    result = synthesize_chapter_summary(TEST_PAPER, "ch2", mock_llm)

    assert result["ok"] is True, f"应成功，实际 {result}"
    assert result["action"] == "completed"
    assert result["source"] == "llm"
    assert result["summary"] is not None
    assert len(result["summary"]) <= 300, f"摘要应 <=300 字，实际 {len(result['summary'])}"
    print(f"   ✅ 摘要合成成功（{len(result['summary'])} 字）")
    print(f"   ✅ source=llm")
    print(f"   ✅ 摘要前 30 字: {result['summary'][:30]}...")

    # 验证写入 state
    state = outline_load(TEST_PAPER)
    summary_node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                         if n["id"] == "__ch2_summary__"), None)
    assert summary_node is not None, "应找到虚拟摘要节点"
    assert summary_node["key_conclusion"] == result["summary"]
    assert summary_node["writing_status"] == "completed"
    print(f"   ✅ 已写入虚拟节点 key_conclusion")


def test_synthesize_user_input_path():
    """测试 3：synthesize_chapter_summary 用户输入路径"""
    print("\n=== 测试 3：用户输入路径 ===")
    setup_outline()

    outline_update_status(TEST_PAPER, "2.1", "completed", key_conclusion="Porter 战略")
    outline_update_status(TEST_PAPER, "2.2", "completed", key_conclusion="AI 文献")

    user_input = "本章从战略理论和文献两个维度为后续环境分析提供方法论支撑。"

    result = synthesize_chapter_summary(
        TEST_PAPER, "ch2",
        llm_func=None,  # 传 None 时不应调用
        user_input=user_input
    )

    assert result["ok"] is True
    assert result["source"] == "user"
    assert result["summary"] == user_input
    print(f"   ✅ 用户输入路径生效（source=user）")


def test_synthesize_llm_failure_ask_user():
    """测试 4：synthesize_chapter_summary LLM 失败 → ask_user"""
    print("\n=== 测试 4：LLM 失败 → ask_user ===")
    setup_outline()

    outline_update_status(TEST_PAPER, "2.1", "completed", key_conclusion="Porter 战略")
    outline_update_status(TEST_PAPER, "2.2", "completed", key_conclusion="AI 文献")

    def failing_llm(prompt: str) -> str:
        raise RuntimeError("模拟 LLM 不可用")

    result = synthesize_chapter_summary(TEST_PAPER, "ch2", failing_llm)

    assert result["ok"] is False, f"应失败，实际 {result}"
    assert result["action"] == "ask_user", f"失败时应 ask_user，实际 {result['action']}"
    assert "child_conclusions" in result, "ask_user 时应附带 child_conclusions"
    assert len(result["child_conclusions"]) == 2
    print(f"   ✅ LLM 失败返回 action=ask_user")
    print(f"   ✅ 附带 {len(result['child_conclusions'])} 个子节点结论供 Orchestrator 展示")

    # 验证失败时未写入 state
    state = outline_load(TEST_PAPER)
    summary_node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                         if n["id"] == "__ch2_summary__"), None)
    assert summary_node["key_conclusion"] is None, "失败时不应写入 key_conclusion"
    print(f"   ✅ 失败时未污染 state")


def test_synthesize_empty_children():
    """测试 5：无子节点结论 → ask_user"""
    print("\n=== 测试 5：无子节点结论 ===")
    setup_outline()

    # 不设置任何子节点 key_conclusion
    result = synthesize_chapter_summary(TEST_PAPER, "ch2", lambda p: "x")

    assert result["ok"] is False
    assert result["action"] == "ask_user"
    assert result.get("child_conclusions") == []
    print(f"   ✅ 无子节点结论 → ask_user")


def test_synthesize_truncate_long():
    """测试 6：超长摘要截断到 300 字"""
    print("\n=== 测试 6：超长摘要截断 ===")
    setup_outline()

    outline_update_status(TEST_PAPER, "2.1", "completed", key_conclusion="Porter")
    outline_update_status(TEST_PAPER, "2.2", "completed", key_conclusion="AI")

    long_text = "本" * 500  # 500 字，超过 300

    def long_llm(prompt: str) -> str:
        return long_text

    result = synthesize_chapter_summary(TEST_PAPER, "ch2", long_llm)

    assert result["ok"] is True
    assert len(result["summary"]) == 300, f"应截断到 300 字，实际 {len(result['summary'])}"
    print(f"   ✅ 500 字 → 截断到 300 字")


def main():
    """主测试入口"""
    print("=" * 60)
    print("增强项1 章节摘要合成 单元测试")
    print("=" * 60)

    try:
        test_is_last_child_of_chapter()
        test_synthesize_llm_path()
        test_synthesize_user_input_path()
        test_synthesize_llm_failure_ask_user()
        test_synthesize_empty_children()
        test_synthesize_truncate_long()

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
