#!/usr/bin/env python3
"""
test_chapter_summary.py - 增强项1 章节摘要节点 单元测试

覆盖场景：
  1. 单章节插入（一个 L1 + 两个 L2）
  2. 多章节插入（两个 L1 + 各两个 L2）
  3. L3 节点纳入 synthesizes
  4. 幂等性（重复调用不重复插入）
  5. 边界：空 outline / 缺失字段不崩溃
  6. 辅助函数 get_chapter_summary_id / get_chapter_id_from_summary
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outline_parser import (
    insert_chapter_summary_nodes,
    get_chapter_summary_id,
    get_chapter_id_from_summary,
)


def make_node(node_id, level, title, parent_id=None, children_ids=None,
              writing_status="pending", key_conclusion=None):
    """构造测试用节点"""
    return {
        "id": node_id,
        "level": level,
        "num": node_id,
        "title": title,
        "parent_id": parent_id,
        "children_ids": children_ids or [],
        "prev_sibling_id": None,
        "next_sibling_id": None,
        "writing_status": writing_status,
        "key_conclusion": key_conclusion,
        "word_count": None,
    }


def test_single_chapter():
    """测试 1：单章节（1 个 L1 + 2 个 L2）"""
    print("\n=== 测试 1：单章节插入 ===")
    outline = {
        "outline_tree": {
            "metadata": {"paper_title": "测试", "total_nodes": 3},
            "nodes": [
                make_node("ch1", 1, "绪论", children_ids=["1.1", "1.2"]),
                make_node("1.1", 2, "研究背景", parent_id="ch1"),
                make_node("1.2", 2, "研究内容", parent_id="ch1"),
            ]
        }
    }

    result = insert_chapter_summary_nodes(outline)
    nodes = result["outline_tree"]["nodes"]

    assert len(nodes) == 4, f"期望 4 节点（3+1），实际 {len(nodes)}"
    summary_nodes = [n for n in nodes if n.get("is_virtual")]
    assert len(summary_nodes) == 1, f"应有 1 个虚拟节点，实际 {len(summary_nodes)}"

    summary = summary_nodes[0]
    assert summary["id"] == "__ch1_summary__", f"id 应为 __ch1_summary__，实际 {summary['id']}"
    assert summary["type"] == "chapter_summary"
    assert summary["chapter_id"] == "ch1"
    assert summary["chapter_title"] == "绪论"
    assert summary["synthesizes"] == ["1.1", "1.2"], \
        f"synthesizes 应为 ['1.1', '1.2']，实际 {summary['synthesizes']}"
    assert summary["key_conclusion"] is None, "key_conclusion 初始应为 None"
    assert summary["writing_status"] == "pending"

    # 虚拟节点应位于章节末尾
    assert nodes[-1]["id"] == "__ch1_summary__", "摘要节点应位于章节末尾"

    print(f"   ✅ 节点数: {len(nodes)}（3 → 4）")
    print(f"   ✅ 虚拟节点 ID: {summary['id']}")
    print(f"   ✅ synthesizes: {summary['synthesizes']}")


def test_multi_chapter():
    """测试 2：多章节（2 个 L1 + 各 2 个 L2）"""
    print("\n=== 测试 2：多章节插入 ===")
    outline = {
        "outline_tree": {
            "metadata": {"paper_title": "测试", "total_nodes": 6},
            "nodes": [
                make_node("ch1", 1, "绪论", children_ids=["1.1", "1.2"]),
                make_node("1.1", 2, "研究背景", parent_id="ch1"),
                make_node("1.2", 2, "研究内容", parent_id="ch1"),
                make_node("ch2", 1, "理论基础", children_ids=["2.1", "2.2"]),
                make_node("2.1", 2, "竞争战略理论", parent_id="ch2"),
                make_node("2.2", 2, "文献综述", parent_id="ch2"),
            ]
        }
    }

    result = insert_chapter_summary_nodes(outline)
    nodes = result["outline_tree"]["nodes"]

    assert len(nodes) == 8, f"期望 8 节点（6+2），实际 {len(nodes)}"
    summary_nodes = [n for n in nodes if n.get("is_virtual")]
    assert len(summary_nodes) == 2, f"应有 2 个虚拟节点，实际 {len(summary_nodes)}"

    # 顺序应为 ch1, 1.1, 1.2, __ch1_summary__, ch2, 2.1, 2.2, __ch2_summary__
    expected_order = ["ch1", "1.1", "1.2", "__ch1_summary__",
                      "ch2", "2.1", "2.2", "__ch2_summary__"]
    actual_order = [n["id"] for n in nodes]
    assert actual_order == expected_order, \
        f"顺序错误\n  期望: {expected_order}\n  实际: {actual_order}"

    # 第一个摘要节点 synthesizes 应为 ['1.1', '1.2']
    s1 = summary_nodes[0]
    assert s1["synthesizes"] == ["1.1", "1.2"], \
        f"第一个摘要 synthesizes 错误: {s1['synthesizes']}"
    assert s1["chapter_id"] == "ch1"

    # 第二个摘要节点 synthesizes 应为 ['2.1', '2.2']
    s2 = summary_nodes[1]
    assert s2["synthesizes"] == ["2.1", "2.2"], \
        f"第二个摘要 synthesizes 错误: {s2['synthesizes']}"
    assert s2["chapter_id"] == "ch2"

    # metadata 更新
    meta = result["outline_tree"]["metadata"]
    assert meta["total_nodes"] == 8
    assert meta["virtual_nodes"] == 2
    assert meta["real_nodes"] == 6

    print(f"   ✅ 节点顺序: {actual_order}")
    print(f"   ✅ virtual_nodes: {meta['virtual_nodes']}, real_nodes: {meta['real_nodes']}")


def test_l3_in_synthesizes():
    """测试 3：L3 节点纳入 synthesizes"""
    print("\n=== 测试 3：L3 节点纳入 synthesizes ===")
    outline = {
        "outline_tree": {
            "metadata": {"paper_title": "测试"},
            "nodes": [
                make_node("ch1", 1, "绪论", children_ids=["1.1"]),
                make_node("1.1", 2, "研究背景", children_ids=["1.1.1", "1.1.2"]),
                make_node("1.1.1", 3, "行业背景", parent_id="1.1"),
                make_node("1.1.2", 3, "研究意义", parent_id="1.1"),
            ]
        }
    }

    result = insert_chapter_summary_nodes(outline)
    summary = [n for n in result["outline_tree"]["nodes"] if n.get("is_virtual")][0]

    # synthesizes 应包含 1.1 (L2) 和 1.1.1, 1.1.2 (L3)
    expected = ["1.1", "1.1.1", "1.1.2"]
    assert summary["synthesizes"] == expected, \
        f"synthesizes 应为 {expected}，实际 {summary['synthesizes']}"

    print(f"   ✅ synthesizes: {summary['synthesizes']}")


def test_idempotency():
    """测试 4：幂等性（重复调用不重复插入）"""
    print("\n=== 测试 4：幂等性 ===")
    outline = {
        "outline_tree": {
            "metadata": {"paper_title": "测试"},
            "nodes": [
                make_node("ch1", 1, "绪论", children_ids=["1.1"]),
                make_node("1.1", 2, "研究背景", parent_id="ch1"),
            ]
        }
    }

    # 第一次插入
    r1 = insert_chapter_summary_nodes(outline)
    n1 = len(r1["outline_tree"]["nodes"])
    v1 = r1["outline_tree"]["metadata"]["virtual_nodes"]

    # 第二次插入（应该幂等）
    r2 = insert_chapter_summary_nodes(r1)
    n2 = len(r2["outline_tree"]["nodes"])
    v2 = r2["outline_tree"]["metadata"]["virtual_nodes"]

    # 第三次插入
    r3 = insert_chapter_summary_nodes(r2)
    n3 = len(r3["outline_tree"]["nodes"])
    v3 = r3["outline_tree"]["metadata"]["virtual_nodes"]

    assert n1 == n2 == n3, f"幂等失败：{n1}, {n2}, {n3}"
    assert v1 == v2 == v3 == 1, f"虚拟节点数异常：{v1}, {v2}, {v3}"

    print(f"   ✅ 第一次: {n1} 节点 / {v1} 虚拟")
    print(f"   ✅ 第二次: {n2} 节点 / {v2} 虚拟（不变）")
    print(f"   ✅ 第三次: {n3} 节点 / {v3} 虚拟（不变）")


def test_edge_cases():
    """测试 5：边界条件"""
    print("\n=== 测试 5：边界条件 ===")

    # 空 outline
    empty1 = insert_chapter_summary_nodes({})
    assert empty1 == {}, "空字典应原样返回"
    print("   ✅ 空字典不崩溃")

    # 空 nodes
    empty2 = insert_chapter_summary_nodes({"outline_tree": {"nodes": []}})
    assert empty2["outline_tree"]["nodes"] == [], "空 nodes 应原样返回"
    print("   ✅ 空 nodes 不崩溃")

    # 缺少 metadata
    no_meta = {
        "outline_tree": {
            "nodes": [
                make_node("ch1", 1, "绪论"),
                make_node("1.1", 2, "研究背景", parent_id="ch1"),
            ]
        }
    }
    r = insert_chapter_summary_nodes(no_meta)
    assert r["outline_tree"]["metadata"]["virtual_nodes"] == 1
    print("   ✅ 缺失 metadata 自动补全")


def test_helper_functions():
    """测试 6：辅助函数"""
    print("\n=== 测试 6：辅助函数 ===")

    # get_chapter_summary_id
    assert get_chapter_summary_id("ch1") == "__ch1_summary__"
    assert get_chapter_summary_id("ch99") == "__ch99_summary__"
    assert get_chapter_summary_id("3") == "__ch3_summary__"
    print("   ✅ get_chapter_summary_id")

    # get_chapter_id_from_summary
    assert get_chapter_id_from_summary("__ch1_summary__") == "ch1"
    assert get_chapter_id_from_summary("__ch99_summary__") == "ch99"
    # 非法输入
    assert get_chapter_id_from_summary("invalid") is None
    assert get_chapter_id_from_summary("__ch1__summary__") is None  # 格式不对
    assert get_chapter_id_from_summary("") is None
    assert get_chapter_id_from_summary(None) is None
    print("   ✅ get_chapter_id_from_summary（含边界）")


def main():
    """主测试入口"""
    print("=" * 60)
    print("增强项1 章节摘要节点 单元测试")
    print("=" * 60)

    try:
        test_single_chapter()
        test_multi_chapter()
        test_l3_in_synthesizes()
        test_idempotency()
        test_edge_cases()
        test_helper_functions()

        print("\n" + "=" * 60)
        print("✅ 全部测试通过（6 个测试用例）")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
