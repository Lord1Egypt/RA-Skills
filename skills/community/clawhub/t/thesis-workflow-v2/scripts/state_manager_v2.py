#!/usr/bin/env python3
"""
state_manager_v2.py - 目录树状态管理器 v1.0
管理目录树 + 五态机 + 节点上下文查询
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

WORKSPACE = os.environ.get(
    "THESIS_WORKSPACE",
    os.path.expanduser("~/.openclaw/workspace")
)


# ============================================================
# 嵌套结构兼容层 (P1 修复)
# ============================================================

def _get_outline_nodes(state: Optional[Dict]) -> List[Dict]:
    """
    多版本兼容:从 state 中提取 outline nodes 列表
    支持三种历史嵌套结构:
    A. state["outline"]["outline_tree"]["nodes"]   # 期望结构
    B. state["outline"]["nodes"]                    # 简化结构
    C. state["outline"]["outline"]["outline_tree"]["nodes"]  # 旧版嵌套
    """
    if state is None:
        return []
    o = state.get("outline", {})
    # 优先结构 A
    nodes = o.get("outline_tree", {}).get("nodes")
    if nodes is not None:
        return nodes
    # 结构 B
    nodes = o.get("nodes")
    if nodes is not None:
        return nodes
    # 结构 C(嵌套深度错乱时的兜底)
    nodes = o.get("outline", {}).get("outline_tree", {}).get("nodes")
    if nodes is not None:
        return nodes
    return []


def _set_outline_nodes(state: Dict, nodes: List[Dict]) -> None:
    """
    多版本兼容:将 outline nodes 写回 state
    自动检测现有结构并保持层级一致
    """
    if state is None:
        return
    o = state.get("outline", {})
    if "outline_tree" in o:
        # 结构 A
        o["outline_tree"]["nodes"] = nodes
    elif "nodes" in o:
        # 结构 B
        o["nodes"] = nodes
    elif "outline" in o and isinstance(o.get("outline"), dict) and "outline_tree" in o["outline"]:
        # 结构 C:先压平到结构 A
        o["outline_tree"] = o["outline"]["outline_tree"]
        del o["outline"]
        o["outline_tree"]["nodes"] = nodes
    else:
        # 全新结构:初始化为结构 A
        if "outline" not in state:
            state["outline"] = {}
        state["outline"]["outline_tree"] = {"metadata": {}, "nodes": nodes}


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

    # P1 修复:写盘前压平嵌套结构为标准结构 A(防御性)
    if "outline" in state and isinstance(state["outline"].get("outline"), dict):
        # 检测到嵌套 C 结构 → 压平为 A
        state["outline"]["outline_tree"] = state["outline"]["outline"]["outline_tree"]
        del state["outline"]["outline"]

    # 原子写入:先写临时文件,再 rename
    tmp_path = state_path + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_path)

    return {"ok": True, "path": state_path}


def outline_load(paper_name: str) -> Optional[Dict[str, Any]]:
    """加载目录树状态(带重试)"""
    state_path = _get_state_path(paper_name)
    if not os.path.exists(state_path):
        return None
    for attempt in range(3):
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            if attempt < 2:
                import time
                time.sleep(0.1)
                continue
            return None
    return None


# ============================================================
# 节点状态管理(五态机)
# ============================================================

# pending → writing → reviewing → approved → completed
#               ↓
#            failed → writing(重试)

VALID_STATUSES = {"pending", "writing", "reviewing", "approved", "failed", "completed"}


def outline_update_status(paper_name: str, node_id: str, status: str,
                          retry_count: int = None, key_conclusion: str = None,
                          word_count: int = None,
                          content: str = None,
                          content_hint: str = None,
                          content_backup: str = None,
                          force: bool = False) -> Dict[str, Any]:
    """
    更新节点状态
    支持额外字段更新:content_hint (增强项4 写作前信息检查)

    v2.0.6 P1-1 B-2 修复:幂等检查
      - 默认拒绝覆盖已完成节点的内容(避免混合用法导致状态污染)
      - 设 force=True 可强制覆盖(调试用)
    """
    if status not in VALID_STATUSES:
        return {"ok": False, "error": f"无效状态: {status}"}

    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "error": "目录树未初始化"}

    # 更新节点状态
    nodes = _get_outline_nodes(state)
    node_found = False
    for node in nodes:
        if node["id"] == node_id:
            # v2.0.6 P1-1 B-2 修复:幂等检查
            # 已 completed 的节点,非 force 写入 content 时拒绝(避免覆盖)
            existing_status = node.get("writing_status", "pending")
            if (not force
                and existing_status == "completed"
                and status in ("completed", "writing")
                and content is not None
                and node.get("content")):
                return {
                    "ok": False,
                    "error": f"节点 {node_id} 已 completed,"
                             f"不能覆盖其 content(v2.0.6 B-2 幂等保护)。"
                             f"如需重写请用 force=True(调试用)或调 "
                             f"orchestrate_v2.write_single_node() 重走标准流程。",
                    "current_status": existing_status,
                    "hint": "建议重走 v2.0.4 推荐路径:write_single_node(bypass_scarcity=True)"
                }
            node["writing_status"] = status
            if key_conclusion is not None:
                node["key_conclusion"] = key_conclusion
            if word_count is not None:
                node["word_count"] = word_count
            if content is not None:
                # M3 修复:写入新内容前先备份旧内容
                if content_backup is None and node.get("content"):
                    node["content_backup"] = node["content"]
                node["content"] = content
            if content_hint is not None:
                node["content_hint"] = content_hint
            if content_backup is not None:
                node["content_backup"] = content_backup
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
        # approved 不改变 current_node_id,等 completed 才推进
        pass

    state["updated_at"] = datetime.now().isoformat()

    state_path = _get_state_path(paper_name)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # 修复 B-2:同步 orchestrate state.completed_nodes / failed_nodes
    # 避免外调 outline_update_status 时 orchestrate state 不同步
    sync_orchestrate_state_from_outline(paper_name, node_id, status)

    return {"ok": True, "status": status, "node_id": node_id}


# ============================================================
# 节点上下文查询(用于 ContextBuilder)
# ============================================================

def outline_get_context(paper_name: str, node_id: str) -> Optional[Dict[str, Any]]:
    """
    获取节点的上下文信息(前序节点摘要、后续节点方向等)
    用于 ContextBuilder 生成 prompt 包

    兄弟关系在同一父节点内查找,不依赖 prev_sibling_id/next_sibling_id 字段
    """
    state = outline_load(paper_name)
    if not state:
        return None

    nodes = _get_outline_nodes(state)
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
        # 一级节点:找同级的其他一级节点
        parent_node = None
        sibling_ids = [n["id"] for n in nodes if n.get("level") == 1 and n["id"] != node_id]

    # 同级前序节点(紧前一个)
    prev_node = None
    if node_id in sibling_ids:
        idx = sibling_ids.index(node_id)
        if idx > 0:
            prev_id = sibling_ids[idx - 1]
            prev_node = node_map.get(prev_id)

    # 同级后续节点(紧后一个)
    next_node = None
    if node_id in sibling_ids:
        idx = sibling_ids.index(node_id)
        if idx < len(sibling_ids) - 1:
            next_id = sibling_ids[idx + 1]
            next_node = node_map.get(next_id)

    # 增强项1 P3 fallback:上一章节虚拟摘要节点
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
    增强项1:获取上一章节的虚拟摘要节点(用于跨章节 bridge P3 fallback)。

    返回:
      {
        "chapter_id": "ch1",
        "chapter_title": "绪论",
        "key_conclusion": "本章系统..."  # 200-300 字
      }
      或 None(首章节 / 无虚拟摘要节点 / 不是章节首节点)

    触发条件(Step 12 修订):当前节点是某章节首节点(prev_sibling_id == None)
    """
    if not node or node.get("is_virtual"):
        return None

    # 查本节点所属 L1 章节(递归向上走 L2/L3)
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

    # 仅当当前节点是 L2 章节首节点才查上一章节摘要
    # 必须是直接子节点(parent_id == chapter_id)且是首节点(prev_sibling_id == None)
    # 排除 L3 节点(其 parent 是 L2 不是 L1)
    if node.get("parent_id") != chapter_id:
        return None  # 不是直接属于该章节(L3 节点的 parent 是 L2)
    if node.get("prev_sibling_id") is not None:
        return None  # 不是章节首节点

    # 推算上一章节 ID(ch1 -> chN-1)
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
        return None  # 未合成则不起作用,返回 None

    return {
        "chapter_id": prev_chapter_id,
        "chapter_title": prev_summary_node.get("chapter_title", prev_chapter_id),
        "key_conclusion": summary
    }


def outline_get_next_node(paper_name: str) -> Optional[Dict[str, Any]]:
    """
    获取下一个待写节点
    返回节点信息或None(全部完成)
    """
    state = outline_load(paper_name)
    if not state:
        return None

    nodes = _get_outline_nodes(state)
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
    for node in _get_outline_nodes(state):
        if node["id"] == node_id:
            return node
    return None


def outline_get_all_nodes(paper_name: str) -> List[Dict[str, Any]]:
    """获取所有节点"""
    state = outline_load(paper_name)
    if not state:
        return []
    return _get_outline_nodes(state)


def outline_progress(paper_name: str) -> Dict[str, Any]:
    """
    获取当前写作进度摘要
    """
    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "error": "目录树未初始化"}

    nodes = _get_outline_nodes(state)
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
    """删除目录树状态(清理用)"""
    state_path = _get_state_path(paper_name)
    if os.path.exists(state_path):
        os.remove(state_path)
        return {"ok": True}
    return {"ok": False, "error": "状态文件不存在"}


# ============================================================
# Orchestrate 状态管理(迁移自 orchestrator_v2.py,修复 B-2)
# ============================================================

def _get_orchestrate_state_path(paper_name: str) -> str:
    """获取编排状态文件路径"""
    return os.path.join(_get_paper_dir(paper_name), "_orchestrate_state.json")


def load_orchestrate_state(paper_name: str) -> Optional[Dict[str, Any]]:
    """加载编排状态(带重试)"""
    path = _get_orchestrate_state_path(paper_name)
    if not os.path.exists(path):
        return None
    for attempt in range(3):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            if attempt < 2:
                import time
                time.sleep(0.1)
                continue
            return None
    return None


def save_orchestrate_state(paper_name: str, state: Dict[str, Any]) -> bool:
    """保存编排状态(原子写入)"""
    path = _get_orchestrate_state_path(paper_name)
    try:
        state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        # 原子写入:先写临时文件,再 rename
        tmp_path = path + ".tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
        return True
    except Exception:
        return False


def init_orchestrate_state(paper_name: str) -> Dict[str, Any]:
    """初始化编排状态"""
    outline_state = outline_load(paper_name)
    if not outline_state:
        raise ValueError(f"论文 {paper_name} 的目录树未初始化")

    nodes = _get_outline_nodes(outline_state)
    total = len(nodes)

    state = {
        "paper_name": paper_name,
        "phase": "phase1_1",   # phase1_1=初始化，phase1_2=大纲确认，phase1_3=归因确认
        "current_node_id": None,
        "completed_nodes": [],
        "pending_review": [],     # 待用户确认(medium/low)
        "failed_nodes": [],       # 用户选择跳过的节点
        "phase1_confirmed": False,
        "phase1_3_status": "pending",   # 增强项4/Step 11: pending|submitted|confirmed|skipped
        "phase1_3_docx_path": None,     # 上传的开题报告路径
        "phase1_3_result": None,        # 归因详细结果(细粒度)
        "phase1_3_submitted_at": None,  # submit 时间戳
        "phase1_3_confirmed_at": None,  # confirm 时间戳
        "progress": {
            "total": total,
            "completed": 0,
            "pending": 0,
            "failed": 0
        },
        "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }
    save_orchestrate_state(paper_name, state)
    return state


def update_progress(state: Dict[str, Any]) -> Dict[str, Any]:
    """更新进度统计"""
    total = state["progress"]["total"]
    completed = len(state["completed_nodes"])
    pending = len(state["pending_review"])
    failed = len(state["failed_nodes"])

    state["progress"] = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "failed": failed
    }
    return state


def sync_orchestrate_state_from_outline(paper_name: str, node_id: str, status: str) -> None:
    """修复 B-2:同步 orchestrate state 的 completed_nodes / failed_nodes 列表

    当 outline_update_status() 被调用且状态是 completed/failed 时,
    同步更新 orchestrate state 的列表,避免混合用法下已完成节点被重复处理。

    仅同步 completed / failed,其他状态(writing / pending / approved)不动。
    如果 orchestrate state 文件不存在(未初始化),则跳过。
    """
    try:
        orchestrate_state = load_orchestrate_state(paper_name)
        if not orchestrate_state:
            return  # orchestrate state 未初始化,跳过

        completed = orchestrate_state.setdefault("completed_nodes", [])
        failed = orchestrate_state.setdefault("failed_nodes", [])

        if status == "completed":
            if node_id not in completed:
                completed.append(node_id)
            # 从 failed 移除(如果之前 failed 过)
            if node_id in failed:
                failed.remove(node_id)
        elif status == "failed":
            if node_id not in failed:
                failed.append(node_id)
            # 从 completed 移除(如果之前 completed 过)
            if node_id in completed:
                completed.remove(node_id)
        # 其他状态(writing / pending / approved)暂不同步

        # 同时刷新 progress 计数(避免列表与计数不同步)
        update_progress(orchestrate_state)

        save_orchestrate_state(paper_name, orchestrate_state)
    except Exception as e:
        # 同步失败不影响主流程(outline state 已写入)，但记录警告
        import warnings
        warnings.warn(f"sync_orchestrate_state_from_outline 同步失败（节点 {node_id}, 状态 {status}）: {e}，"
                      f"orchestrate_state 可能与 outline_state 不一致，建议检查")


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
