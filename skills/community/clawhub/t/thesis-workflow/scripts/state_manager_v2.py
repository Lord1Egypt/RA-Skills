#!/usr/bin/env python3
"""
state_manager_v2.py - 目录树状态管理器 v1.0
管理目录树 + 五态机 + 节点上下文查询
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")


def _get_paper_dir(paper_name: str) -> str:
    """获取论文状态目录"""
    paper_dir = os.path.join(WORKSPACE, paper_name)
    os.makedirs(paper_dir, exist_ok=True)
    return paper_dir


def _get_state_path(paper_name: str) -> str:
    return os.path.join(_get_paper_dir(paper_name), "_outline_state.json")


# ============================================================
# 目录树写入
# ============================================================

def outline_save(paper_name: str, outline: Dict[str, Any]) -> Dict[str, Any]:
    """
    保存目录树到状态文件
    """
    state_path = _get_state_path(paper_name)
    
    state = {
        "paper_name": paper_name,
        "outline": outline,
        "writing_progress": {
            "current_node_id": None,
            "completed_node_ids": [],
            "failed_node_ids": [],
            "retry_count": {}
        },
        "updated_at": datetime.now().isoformat()
    }
    
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    return {"ok": True, "path": state_path}


def outline_load(paper_name: str) -> Optional[Dict[str, Any]]:
    """加载目录树状态"""
    state_path = _get_state_path(paper_name)
    if not os.path.exists(state_path):
        return None
    with open(state_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ============================================================
# 节点状态管理（五态机）
# ============================================================

# pending → writing → reviewing → approved → completed
#               ↓
#            failed → writing（重试）

VALID_STATUSES = {"pending", "writing", "reviewing", "approved", "failed", "completed"}


def outline_update_status(paper_name: str, node_id: str, status: str,
                          retry_count: int = None, key_conclusion: str = None,
                          word_count: int = None,
                          content: str = None,
                          content_hint: str = None) -> Dict[str, Any]:
    """
    更新节点状态
    支持额外字段更新：content_hint (增强项4 写作前信息检查)
    """
    if status not in VALID_STATUSES:
        return {"ok": False, "error": f"无效状态: {status}"}

    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "error": "目录树未初始化"}

    # 更新节点状态
    nodes = state["outline"]["outline_tree"]["nodes"]
    node_found = False
    for node in nodes:
        if node["id"] == node_id:
            node["writing_status"] = status
            if key_conclusion is not None:
                node["key_conclusion"] = key_conclusion
            if word_count is not None:
                node["word_count"] = word_count
            if content is not None:
                node["content"] = content
            if content_hint is not None:
                node["content_hint"] = content_hint
            node_found = True
            break
    
    if not node_found:
        return {"ok": False, "error": f"节点不存在: {node_id}"}
    
    # 更新进度
    progress = state["writing_progress"]
    
    if status == "writing":
        progress["current_node_id"] = node_id
        if node_id in progress["failed_node_ids"]:
            progress["failed_node_ids"].remove(node_id)
    elif status == "completed":
        progress["completed_node_ids"].append(node_id)
        if node_id == progress["current_node_id"]:
            progress["current_node_id"] = None
    elif status == "failed":
        progress["failed_node_ids"].append(node_id)
        if node_id in progress["completed_node_ids"]:
            progress["completed_node_ids"].remove(node_id)
        if retry_count is not None:
            progress["retry_count"][node_id] = retry_count
    elif status == "approved":
        # approved 不改变 current_node_id，等 completed 才推进
        pass
    
    state["updated_at"] = datetime.now().isoformat()
    
    state_path = _get_state_path(paper_name)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    return {"ok": True, "status": status, "node_id": node_id}


# ============================================================
# 节点上下文查询（用于 ContextBuilder）
# ============================================================

def outline_get_context(paper_name: str, node_id: str) -> Optional[Dict[str, Any]]:
    """
    获取节点的上下文信息（前序节点摘要、后续节点方向等）
    用于 ContextBuilder 生成 prompt 包
    
    兄弟关系在同一父节点内查找，不依赖 prev_sibling_id/next_sibling_id 字段
    """
    state = outline_load(paper_name)
    if not state:
        return None
    
    nodes = state["outline"]["outline_tree"]["nodes"]
    node_map = {n["id"]: n for n in nodes}
    
    node = node_map.get(node_id)
    if not node:
        return None
    
    parent_id = node.get("parent_id")
    level = node.get("level")
    
    # 获取同父节点的兄弟节点列表
    if parent_id:
        parent_node = node_map.get(parent_id)
        sibling_ids = parent_node.get("children_ids", []) if parent_node else []
    else:
        # 一级节点：找同级的其他一级节点
        parent_node = None
        sibling_ids = [n["id"] for n in nodes if n.get("level") == 1 and n["id"] != node_id]
    
    # 同级前序节点（紧前一个）
    prev_node = None
    if node_id in sibling_ids:
        idx = sibling_ids.index(node_id)
        if idx > 0:
            prev_id = sibling_ids[idx - 1]
            prev_node = node_map.get(prev_id)
    
    # 同级后续节点（紧后一个）
    next_node = None
    if node_id in sibling_ids:
        idx = sibling_ids.index(node_id)
        if idx < len(sibling_ids) - 1:
            next_id = sibling_ids[idx + 1]
            next_node = node_map.get(next_id)

    # 增强项1 P3 fallback：上一章节虚拟摘要节点
    prev_chapter_summary = _get_prev_chapter_summary(node, nodes, node_map)

    context = {
        "current_node": node,
        "prev_node": {
            "id": prev_node["id"],
            "title": prev_node["title"],
            "level": prev_node["level"],
            "key_conclusion": prev_node.get("key_conclusion")
        } if prev_node else None,
        "parent_node": {
            "id": parent_node["id"],
            "title": parent_node["title"],
            "key_conclusion": parent_node.get("key_conclusion")
        } if parent_node else None,
        "next_node": {
            "id": next_node["id"],
            "title": next_node["title"],
            "level": next_node["level"]
        } if next_node else None,
        "parent_conclusion": parent_node.get("key_conclusion") if parent_node else None,
        "prev_sibling_conclusion": prev_node.get("key_conclusion") if prev_node else None,
        "next_node_title": next_node["title"] if next_node else None,
        "prev_chapter_summary": prev_chapter_summary
    }

    return context


def _get_prev_chapter_summary(node: Dict, nodes: List[Dict], node_map: Dict) -> Optional[Dict]:
    """
    增强项1：获取上一章节的虚拟摘要节点（用于跨章节 bridge P3 fallback）。

    返回：
      {
        "chapter_id": "ch1",
        "chapter_title": "绪论",
        "key_conclusion": "本章系统..."  # 200-300 字
      }
      或 None（首章节 / 无虚拟摘要节点 / 不是章节首节点）

    触发条件（Step 12 修订）：当前节点是某章节首节点（prev_sibling_id == None）
    """
    if not node or node.get("is_virtual"):
        return None

    # 查本节点所属 L1 章节（递归向上走 L2/L3）
    chapter_id = None
    cur = node
    while cur and cur.get("level", 0) > 1:
        parent_id = cur.get("parent_id")
        if not parent_id:
            return None
        cur = node_map.get(parent_id)
        if not cur:
            return None
        if cur.get("level") == 1 and not cur.get("is_virtual"):
            chapter_id = cur["id"]
            break

    if not chapter_id or not chapter_id.startswith("ch"):
        return None

    # 仅当当前节点是章节首节点（prev_sibling_id == None）才查上一章节摘要
    if node.get("prev_sibling_id") is not None:
        return None

    # 推算上一章节 ID（ch1 -> chN-1）
    try:
        ch_num = int(chapter_id[2:])
    except ValueError:
        return None

    if ch_num <= 1:
        return None  # 首章节无前一章节

    prev_chapter_id = f"ch{ch_num - 1}"
    prev_summary_id = f"__ch{ch_num - 1}_summary__"

    prev_summary_node = node_map.get(prev_summary_id)
    if not prev_summary_node:
        return None

    summary = prev_summary_node.get("key_conclusion")
    if not summary:
        return None  # 未合成则不起作用，返回 None

    return {
        "chapter_id": prev_chapter_id,
        "chapter_title": prev_summary_node.get("chapter_title", prev_chapter_id),
        "key_conclusion": summary
    }


def outline_get_next_node(paper_name: str) -> Optional[Dict[str, Any]]:
    """
    获取下一个待写节点
    返回节点信息或None（全部完成）
    """
    state = outline_load(paper_name)
    if not state:
        return None
    
    nodes = state["outline"]["outline_tree"]["nodes"]
    progress = state["writing_progress"]
    completed = set(progress["completed_node_ids"])
    
    # 按顺序找第一个 pending 或 failed（可重试）的节点
    for node in nodes:
        if node["id"] in completed:
            continue
        status = node.get("writing_status", "pending")
        retry_count = progress["retry_count"].get(node["id"], 0)
        
        if status == "pending" or (status == "failed" and retry_count < 3):
            return node
    
    return None


def outline_get_node(paper_name: str, node_id: str) -> Optional[Dict[str, Any]]:
    """根据ID获取单个节点"""
    state = outline_load(paper_name)
    if not state:
        return None
    for node in state["outline"]["outline_tree"]["nodes"]:
        if node["id"] == node_id:
            return node
    return None


def outline_get_all_nodes(paper_name: str) -> List[Dict[str, Any]]:
    """获取所有节点"""
    state = outline_load(paper_name)
    if not state:
        return []
    return state["outline"]["outline_tree"]["nodes"]


def outline_progress(paper_name: str) -> Dict[str, Any]:
    """
    获取当前写作进度摘要
    """
    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "error": "目录树未初始化"}
    
    nodes = state["outline"]["outline_tree"]["nodes"]
    progress = state["writing_progress"]
    
    total = len(nodes)
    completed = len(progress["completed_node_ids"])
    failed = len(progress["failed_node_ids"])
    
    return {
        "ok": True,
        "total": total,
        "completed": completed,
        "failed": failed,
        "in_progress": progress["current_node_id"],
        "percent": round(completed / total * 100, 1) if total > 0 else 0,
        "remaining": total - completed - failed
    }


def outline_delete(paper_name: str) -> Dict[str, Any]:
    """删除目录树状态（清理用）"""
    state_path = _get_state_path(paper_name)
    if os.path.exists(state_path):
        os.remove(state_path)
        return {"ok": True}
    return {"ok": False, "error": "状态文件不存在"}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 state_manager_v2.py load <论文名>")
        print("  python3 state_manager_v2.py progress <论文名>")
        print("  python3 state_manager_v2.py next <论文名>")
        sys.exit(1)
    
    action = sys.argv[1]
    paper_name = sys.argv[2]
    
    if action == "load":
        state = outline_load(paper_name)
        if state:
            print(json.dumps(state, ensure_ascii=False, indent=2))
        else:
            print(f"未找到论文: {paper_name}")
    
    elif action == "progress":
        result = outline_progress(paper_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif action == "next":
        node = outline_get_next_node(paper_name)
        if node:
            print(json.dumps(node, ensure_ascii=False, indent=2))
        else:
            print("全部节点已完成")
    
    elif action == "delete":
        print(outline_delete(paper_name))
