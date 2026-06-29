#!/usr/bin/env python3
"""
test_info_scarcity.py - 增强项4 写作前信息检查 单元测试

覆盖场景：
  1. save_content_hints_to_outline：写入 + 跳过特殊 key + 跳过不存在节点
  2. check_info_scarcity 标准 A：3 项全空 → needs_user_input
  3. check_info_scarcity 部分缺失：1 项缺失 → 仍 needs_user_input
  4. check_info_scarcity 全部齐备：3 项都有 → proceed
  5. apply_user_decision 决策 1：用户提供 hint → 写入节点
  6. apply_user_decision 决策 2：AI 自行生成 → 不写入
  7. apply_user_decision 决策 3：跳过 → 标记 failed
  8. 集成：完整闭环（save hint → check 通过 → proceed）
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outline_parser import (
    insert_chapter_summary_nodes,
    save_content_hints_to_outline,
    extract_content_hints,
)
from state_manager_v2 import (
    outline_save,
    outline_load,
    outline_update_status,
    _get_state_path,
)
from context_builder import build_prompt_package, build_prompt_package_text
from orchestrator_v2 import check_info_scarcity, apply_user_decision


TEST_PAPER = "test_info_scarcity_paper"


def cleanup():
    p = _get_state_path(TEST_PAPER)
    if os.path.exists(p):
        os.remove(p)


def setup_outline():
    """构造 2 章 × 2 L2 测试 outline"""
    nodes = [
        {"id": "ch1", "level": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1", "1.2"], "writing_status": "pending"},
        {"id": "1.1", "level": 2, "title": "研究背景", "parent_id": "ch1",
         "children_ids": [], "writing_status": "pending"},
        {"id": "1.2", "level": 2, "title": "研究内容", "parent_id": "ch1",
         "children_ids": [], "writing_status": "pending"},
        {"id": "ch2", "level": 1, "title": "理论基础", "parent_id": None,
         "children_ids": ["2.1"], "writing_status": "pending"},
        {"id": "2.1", "level": 2, "title": "竞争战略理论", "parent_id": "ch2",
         "children_ids": [], "writing_status": "pending"},
    ]
    outline = {"outline_tree": {"metadata": {"paper_title": "test"}, "nodes": nodes}}
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)


# ============================================================
# 测试 1-4: save_content_hints_to_outline
# ============================================================

def test_save_content_hints_basic():
    """测试 1：save_content_hints_to_outline 基本写入"""
    print("\n=== 测试 1：save_content_hints_to_outline 基本写入 ===")
    setup_outline()

    hints = {
        "1.1": "AI 时代互联网分发面临范式重构",
        "1.2": "本文聚焦差异化战略研究",
        "__orphan_count__": "5",  # 应跳过
        "non_existent_node": "应跳过",  # 应跳过
    }
    r = save_content_hints_to_outline(TEST_PAPER, hints)

    assert r["ok"] is True
    assert r["written"] == 2
    assert r["skipped"] == 2

    state = outline_load(TEST_PAPER)
    node_11 = next((n for n in state["outline"]["outline_tree"]["nodes"]
                    if n["id"] == "1.1"), None)
    node_12 = next((n for n in state["outline"]["outline_tree"]["nodes"]
                    if n["id"] == "1.2"), None)
    assert node_11["content_hint"] == "AI 时代互联网分发面临范式重构"
    assert node_12["content_hint"] == "本文聚焦差异化战略研究"
    print(f"   ✅ written={r['written']}, skipped={r['skipped']}")


# ============================================================
# 测试 2-4: check_info_scarcity（标准 A）
# ============================================================

def test_scarcity_all_empty():
    """测试 2：3 项全空 → needs_user_input（3 项全 missing）"""
    print("\n=== 测试 2：3 项全空 → needs_user_input ===")
    setup_outline()

    r = check_info_scarcity(TEST_PAPER, "1.1")

    assert r["ok"] is True
    assert r["action"] == "needs_user_input"
    assert set(r["missing_sources"]) == {"content_hint", "user_hints", "bridge"}
    assert "1" in r["prompt_options"]
    assert "2" in r["prompt_options"]
    assert "3" in r["prompt_options"]
    print(f"   ✅ action=needs_user_input, missing={r['missing_sources']}")
    print(f"   ✅ prompt_options: {list(r['prompt_options'].keys())}")


def test_scarcity_one_missing():
    """测试 3：部分缺失（标准 A：任一为空就暂停）"""
    print("\n=== 测试 3：部分缺失 → needs_user_input（标准 A） ===")
    setup_outline()

    # 只给 content_hint，user_hints 和 bridge 仍空
    outline_update_status(TEST_PAPER, "1.1", "pending",
                          content_hint="用户填的提示")

    r = check_info_scarcity(TEST_PAPER, "1.1")

    assert r["action"] == "needs_user_input"
    assert "user_hints" in r["missing_sources"]
    assert "bridge" in r["missing_sources"]
    assert "content_hint" not in r["missing_sources"]
    print(f"   ✅ missing={r['missing_sources']}")


def test_scarcity_all_present():
    """测试 4：3 项齐备 → proceed"""
    print("\n=== 测试 4：3 项齐备 → proceed ===")
    setup_outline()

    # 准备：1.1 + 1.2 完成 → ch1 摘要合成 → prev_chapter_summary 齐
    outline_update_status(TEST_PAPER, "1.1", "completed",
                          key_conclusion="AI 时代背景")
    outline_update_status(TEST_PAPER, "1.2", "completed",
                          key_conclusion="研究内容")
    outline_update_status(TEST_PAPER, "__ch1_summary__", "completed",
                          key_conclusion="本章从背景出发，提出差异化战略问题。",
                          word_count=50)

    # 2.1 加 content_hint
    outline_update_status(TEST_PAPER, "2.1", "pending",
                          content_hint="竞争战略理论核心是 Porter 三种基本战略")
    # 加 chapter_hints（user_hints）
    state = outline_load(TEST_PAPER)
    state["chapter_hints"] = {"2.1": ["波特竞争战略理论", "差异化"]}
    state_path = _get_state_path(TEST_PAPER)
    import json
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    r = check_info_scarcity(TEST_PAPER, "2.1")

    assert r["action"] == "proceed"
    assert r["missing_sources"] == []
    assert r["current_info"]["bridge_source"] == "chapter_summary"
    print(f"   ✅ action=proceed（content_hint + bridge=chapter_summary + user_hints 齐备）")


# ============================================================
# 测试 5-7: apply_user_decision（3 个决策路径）
# ============================================================

def test_decision_1_user_provides_hint():
    """测试 5：决策 1 — 用户提供 content_hint"""
    print("\n=== 测试 5：决策 1（用户提供 hint） ===")
    setup_outline()

    r = apply_user_decision(TEST_PAPER, "1.1", "1", user_hint="用户手写提示")

    assert r["ok"] is True
    assert r["action"] == "proceed"
    assert r["decision"] == "1"

    state = outline_load(TEST_PAPER)
    node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                 if n["id"] == "1.1"), None)
    assert node["content_hint"] == "用户手写提示"
    print(f"   ✅ 决策 1 生效：content_hint 已写入节点")


def test_decision_2_ai_self_generate():
    """测试 6：决策 2 — AI 自行生成"""
    print("\n=== 测试 6：决策 2（AI 自行生成） ===")
    setup_outline()

    r = apply_user_decision(TEST_PAPER, "1.1", "2")

    assert r["ok"] is True
    assert r["action"] == "proceed"
    assert r["decision"] == "2"

    state = outline_load(TEST_PAPER)
    node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                 if n["id"] == "1.1"), None)
    # 不应写入 content_hint（仍为 None 或无字段）
    assert not node.get("content_hint"), f"决策 2 不应写入 hint，实际: {node.get('content_hint')}"
    print(f"   ✅ 决策 2 生效：不写入 hint，继续写作")


def test_decision_3_skip_node():
    """测试 7：决策 3 — 跳过该节点"""
    print("\n=== 测试 7：决策 3（跳过节点） ===")
    setup_outline()

    r = apply_user_decision(TEST_PAPER, "1.1", "3")

    assert r["ok"] is True
    assert r["action"] == "skipped"
    assert r["decision"] == "3"

    state = outline_load(TEST_PAPER)
    node = next((n for n in state["outline"]["outline_tree"]["nodes"]
                 if n["id"] == "1.1"), None)
    assert node["writing_status"] == "failed"
    print(f"   ✅ 决策 3 生效：节点标记为 failed")


# ============================================================
# 测试 8: 集成闭环
# ============================================================

def test_integration_full_loop():
    """测试 8：完整闭环 — save hint → check 通过 → build prompt"""
    print("\n=== 测试 8：完整闭环（end-to-end） ===")
    setup_outline()

    # 1. 开题报告 → 提取 hints → 写入 state
    save_content_hints_to_outline(TEST_PAPER, {
        "1.1": "AI 时代互联网分发面临范式重构",
        "2.1": "理论部分对应 Porter 战略"
    })

    # 2. 1.1：缺 user_hints + bridge（首章节首节点）
    r1 = check_info_scarcity(TEST_PAPER, "1.1")
    print(f"   Step 1: check 1.1 → action={r1['action']}, missing={r1['missing_sources']}")
    assert r1["action"] == "needs_user_input"

    # 3. 用户决策 1：手动补充 user_hints
    state = outline_load(TEST_PAPER)
    state["chapter_hints"] = {
        "1.1": ["AI 时代背景", "互联网分发演进"],
        "2.1": ["波特竞争战略理论"]
    }
    state_path = _get_state_path(TEST_PAPER)
    import json
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # 4. 再 check 1.1：user_hints 已有，但 bridge 仍缺（首章节）
    r2 = check_info_scarcity(TEST_PAPER, "1.1")
    print(f"   Step 2: 加 user_hints → missing={r2['missing_sources']}")
    assert "user_hints" not in r2["missing_sources"]

    # 5. 用户决策 2 (AI 自行生成)：允许 1.1 不补 bridge 直接写
    r_apply = apply_user_decision(TEST_PAPER, "1.1", "2")
    assert r_apply["action"] == "proceed"
    print(f"   Step 3: 用户决策 2 (AI 自行生成) → proceed")

    # 6. 1.1 完成 → 写 key_conclusion + 1.2 完成 → 触发 ch1 摘要合成
    outline_update_status(TEST_PAPER, "1.1", "completed",
                          content_hint="AI 时代互联网分发面临范式重构",
                          key_conclusion="AI 时代互联网分发面临范式重构")
    outline_update_status(TEST_PAPER, "1.2", "completed",
                          key_conclusion="本文聚焦差异化战略研究")
    outline_update_status(TEST_PAPER, "__ch1_summary__", "completed",
                          key_conclusion="本章从背景出发提出差异化研究问题。",
                          word_count=30)

    # 7. 2.1 应 proceed（content_hint + bridge=chapter_summary 都齐）
    r3 = check_info_scarcity(TEST_PAPER, "2.1")
    print(f"   Step 4: check 2.1 → action={r3['action']}, missing={r3['missing_sources']}")
    assert r3["action"] == "proceed"

    # 8. build prompt 应包含 content_hint
    pkg = build_prompt_package(TEST_PAPER, "2.1")
    assert pkg["content_hint"] == "理论部分对应 Porter 战略"
    text = build_prompt_package_text(pkg)
    assert "## 开题报告方向参考" in text
    assert "Porter 战略" in text
    print(f"   ✅ 闭环完成：content_hint 写入 → check → build prompt 含 hint")


def main():
    """主测试入口"""
    print("=" * 60)
    print("增强项4 写作前信息检查 单元测试")
    print("=" * 60)

    try:
        test_save_content_hints_basic()
        test_scarcity_all_empty()
        test_scarcity_one_missing()
        test_scarcity_all_present()
        test_decision_1_user_provides_hint()
        test_decision_2_ai_self_generate()
        test_decision_3_skip_node()
        test_integration_full_loop()

        print("\n" + "=" * 60)
        print("✅ 全部测试通过（8 个测试用例）")
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
