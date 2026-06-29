#!/usr/bin/env python3
"""
orchestrator_v2.py - 论文写作流程编排器 v1.0

驱动完整流程:
  Phase 1: 目录解析(一次性,确认后锁定)
  Phase 2: 逐节点写作(串行,评审驱动)
  Phase 3: 整合输出

支持断点续跑:
  状态持久化到 state 文件,中断后可从上次位置继续

用法:
  result = orchestrate(paper_name, phase, llm_func=my_llm)
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from pathlib import Path
_script_dir = Path(__file__).parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from context_builder import build_prompt_package_text, build_prompt_package
from node_writer import write_node_with_llm, extract_key_conclusion
from reviewer import review_node
from state_manager_v2 import (
    outline_load, outline_save, outline_update_status, outline_get_node, outline_get_context,
    WORKSPACE, _get_paper_dir, _get_outline_nodes
)
from outline_parser import (
    insert_chapter_summary_nodes,
    get_chapter_summary_id,
    get_chapter_id_from_summary,
    extract_proposal_content,
    extract_content_hints,
    save_content_hints_to_outline,
    outline_parse,
)

from gatekeeper_integration import (
    notify_gatekeeper,
    gk_enabled,
    write_user_decision,
    clear_pending,
)


# ============================================================
# Gatekeeper 辅助
# ============================================================

def _gk_notify(paper_name: str, event: str, phase: str, node_id: str = "",
               details: dict = None, blocking: bool = False) -> dict:
    """
    Orchestrator → Gatekeeper 的统一通知入口。

    - GK 未启用时:直接返回 {"ok": True, "gk_disabled": True}
    - blocking=True:等待用户决策(通过 _gk_user_decision.json)
    """
    if not gk_enabled(paper_name):
        return {"ok": True, "gk_disabled": True}
    return notify_gatekeeper(
        paper_name=paper_name,
        event=event,
        phase=phase,
        node_id=node_id,
        details=details or {},
        blocking=blocking,
    )


def enable_gatekeeper(paper_name: str, gk_session: str = "") -> Dict[str, Any]:
    """
    启用 Gatekeeper(在 OpenClaw agent spawn GK session 后调用)。

    在 _orchestrate_state.json 中设置 gk_enabled=true。
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}
    state["gk_enabled"] = True
    state["gk_session"] = gk_session
    state["gk_started_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save_orchestrate_state(paper_name, state)
    return {"ok": True, "message": f"Gatekeeper 已启用(session={gk_session})"}


def disable_gatekeeper(paper_name: str) -> Dict[str, Any]:
    """禁用 Gatekeeper(流程结束后调用)"""
    state = load_orchestrate_state(paper_name)
    if state:
        state["gk_enabled"] = False
        save_orchestrate_state(paper_name, state)
    # 清理协作文件
    clear_pending(paper_name)
    return {"ok": True, "message": "Gatekeeper 已停用"}


# ============================================================
# 公共辅助:论文内容组装
# ============================================================

def _assemble_full_content(paper_name: str, state: Dict = None) -> str:
    """
    组装完整论文内容:遍历 completed/failed 节点,按大纲顺序拼接为 Markdown。

    供 Phase 3 / 3.5 / 4 / 5 复用,消除重复逻辑。

    参数:
        paper_name: 论文标识
        state: 可选,传入已有的 orchestrate_state(避免重复加载)

    返回:
        完整论文 Markdown 字符串(## 标题 + 正文,节点间空行分隔)
    """
    if state is None:
        state = load_orchestrate_state(paper_name)
    if not state:
        return ""

    outline_state = outline_load(paper_name)
    if not outline_state:
        return ""

    nodes = _get_outline_nodes(outline_state)
    completed_ids = set(state.get("completed_nodes", []))
    failed_ids = set(state.get("failed_nodes", []))

    sections = []
    for node in nodes:
        if node["id"] in completed_ids or node["id"] in failed_ids:
            node_data = outline_get_node(paper_name, node["id"])
            # 排除 reviewing 状态节点(未通过评审的内容不进最终论文)
            if node_data and node_data.get("writing_status") == "reviewing":
                continue
            content = node_data.get("content", "") if node_data else ""
            if content:
                title = node.get("title", node["id"])
                sections.append(f"## {title}\n\n{content}")

    return "\n\n".join(sections)


# ============================================================
# Phase 1: 目录解析
# ============================================================


# ============================================================
# 状态管理(Orchestrate state 函数已迁移至 state_manager_v2.py,修复 B-2)
# ============================================================

# 直接从 state_manager_v2 导入(避免重复定义和循环依赖)
from state_manager_v2 import (
    _get_orchestrate_state_path,
    load_orchestrate_state,
    save_orchestrate_state,
    init_orchestrate_state,
    update_progress,
)


# ============================================================
# Phase 1: 目录解析
# ============================================================

def orchestrate_phase1(paper_name: str, docx_path: str = None,
                     outline_text: str = None) -> Dict[str, Any]:
    """
    Phase 1: 目录解析

    输入:docx 文件路径 或 目录文本
    返回:解析后的目录树,等待用户确认
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        state = init_orchestrate_state(paper_name)

    # 如果已确认,不管当前是哪个 phase,都返回 confirmed
    if state.get("phase1_confirmed"):
        return {
            "ok": True,
            "phase": "phase1",
            "confirmed": True,
            "message": "目录已确认,无需重复操作"
        }

    if state["phase"] not in ("phase1",):
        return {
            "ok": False,
            "error": f"当前阶段为 {state['phase']},不是 phase1"
        }

    return {
        "ok": True,
        "phase": "phase1",
        "confirmed": False,
        "message": "请确认目录结构,确认后进入 Phase 2"
    }


def orchestrate_phase1_1(
    paper_name: str,
    input_type: str,
    input_data: str,
    llm_func: Callable[[str], str] = None,
    docx_path: str = None
) -> Dict[str, Any]:
    """
    Phase 1.1: 解析入口(修订 Step 11 - 拍板决策"1.先上传 2.后面才能解析")

    拍板要点:
      - 拍板 #1 强制:Phase 1.1 必走(未传任何输入报错)
      - 拍板 #2 方案 A:合并 phase1_0_upload + phase1_1_parse 为一个 action
      - 拍板 #3 不要 auto:用户必须明确选 docx 或 text
      - 拍板 #4 解析失败只能 3 选项:重新输入 docx / 重新输入 text / 取消

    参数:
      paper_name: 论文名
      input_type: "docx" | "text" (拍板 #3 禁用 auto)
      input_data: docx_path 或 outline_text(取决于 input_type)
      llm_func: LLM 调用函数(可选,AI 兑底匹配标题)
      docx_path: 保留与 input_data 重复(兼容调用方习惯)

    返回:
      成功:{
        ok: True,
        action: "review_outline",
        input_type: "docx" | "text",
        outline: {...},
        issues: [...],
        message: "目录已解析,请确认"
      }
      失败:{
        ok: False,
        action: "input_required",   # 拍板 #4 强制走3选项
        error: "...",
        issues: [...],
        retry_options: {"1": "重新上传 docx", "2": "手动录入目录文本", "3": "取消"}
      }
    """
    # 拍板 #1 强制:未传任何输入报错
    if input_type not in ("docx", "text"):
        return {
            "ok": False,
            "error": f"拍板 #3 禁用 auto,input_type 必须是 'docx' 或 'text',实际: {input_type}",
            "action": "input_required",
            "retry_options": {
                "1": "重新上传 docx(input_type=docx)",
                "2": "手动录入目录文本(input_type=text)",
                "3": "取消"
            }
        }

    if not input_data:
        return {
            "ok": False,
            "error": "input_data 不能为空",
            "action": "input_required",
            "retry_options": {
                "1": "重新上传 docx",
                "2": "手动录入目录文本",
                "3": "取消"
            }
        }

    # 拍板 #3 不要 auto:用户必须明确选 docx 或 text
    # docx_path 参数与 input_data 重复时,以 input_data 为准
    if input_type == "docx":
        docx_path_to_use = docx_path or input_data
        if not os.path.exists(docx_path_to_use):
            return {
                "ok": False,
                "error": f"docx 文件不存在: {docx_path_to_use}",
                "action": "input_required",
                "retry_options": {
                    "1": "重新上传 docx",
                    "2": "手动录入目录文本",
                    "3": "取消"
                }
            }
        result = outline_parse(docx_path_to_use)
    else:  # text
        result = outline_parse(input_data)

    if not result.get("ok"):
        # 解析失败 → 拍板 #4 走 3 选项
        return {
            "ok": False,
            "action": "input_required",
            "error": result.get("error", "解析失败"),
            "issues": result.get("issues", []),
            "suggestion": result.get("suggestion", ""),
            "retry_options": {
                "1": "重新上传 docx(input_type=docx)",
                "2": "手动录入目录文本(input_type=text)",
                "3": "取消"
            }
        }

    outline = result["outline"]

    # 增强项1:在每个 L1 章节末尾插入虚拟摘要节点
    outline = insert_chapter_summary_nodes(outline)

    # 持久化 outline_state(包含虚拟节点)
    outline_save(paper_name, outline)

    # 初始化 orchestrate_state
    init_orchestrate_state(paper_name)

    # 保存 docx_path 到 state(拍板方案 A:state 只存路径,每次重读)
    state = load_orchestrate_state(paper_name)
    if input_type == "docx":
        state["phase1_3_docx_path"] = docx_path_to_use
        state["phase1_3_input_type"] = "docx"
    else:
        state["phase1_3_docx_path"] = None  # text 输入无 docx
        state["phase1_3_input_type"] = "text"
    state["phase1_3_status"] = "pending"
    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "action": "review_outline",
        "input_type": input_type,
        "input_data_preview": input_data[:100] if isinstance(input_data, str) else str(input_data)[:100],
        "outline": outline,
        "issues": result.get("issues", []),
        "summary": result.get("summary", {}),
        "message": f"目录已解析(input_type={input_type}),请确认后进入 Phase 1.2"
    }


def confirm_phase1(paper_name: str) -> Dict[str, Any]:
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if state.get("phase1_confirmed"):
        return {"ok": True, "message": "目录已确认"}

    state["phase1_confirmed"] = True
    # 拍板 #1 强制 + #2 方案 B 枚举字段:
    # 大纲确认(Phase 1.2)后推进到 phase1_2，归因确认(Phase 1.3)后才进 phase2
    state["phase1_3_status"] = "pending"   # 初始 pending,需用户提交 docx
    state["phase"] = "phase1_2"            # 大纲确认后进入 phase1_2，等归因确认

    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase1_2",
        "phase1_3_status": "pending",
        "message": "目录已确认(Phase 1.2 完成)，请核对下方归因分析(Phase 1.3)"
    }


# ============================================================
# Phase 1.3: 开题报告归因(Step 11)
# ============================================================

def orchestrate_phase1_3(
    paper_name: str,
    docx_path: str = None,
    llm_func: Callable[[str], str] = None
) -> Dict[str, Any]:
    """
    Phase 1.3: 开题报告归因(增强项4 content_hint 接入链路)

    流程:
      1. 检查 phase1_confirmed == True
      2. 检查 docx_path 存在且可读
      3. 调用 extract_proposal_content() 提取并归因开题报告内容
      4. 调用 extract_content_hints() 提炼每个节点的 content_hint
      5. save_content_hints_to_outline() 写入 state
      6. 设置 phase1_3_status = "submitted",保存归因详情

    拍板 #3 时机 A:submit 时一次性写入 state(持久化)。
    拍板 #5 细粒度:返回每个节点的归因详情(content_hint + matched paragraphs + confidence)。

    返回:
      {
        ok: True,
        phase1_3_status: "submitted",
        docx_path: str,
        summary: {matched, orphan, ai_heading_matched, ai_classified, total_paragraphs},
        node_details: {
          "1.1": {"content_hint": "...", "matched_paragraphs": [...], "confidence": ...},
          ...
        },
        orphan_segments: [...],
        message: str
      }
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if not state.get("phase1_confirmed"):
        return {"ok": False, "error": "Phase 1 目录未确认"}

    if state.get("phase1_3_status") not in ("pending", "submitted"):
        return {"ok": False, "error": f"Phase 1.3 状态异常: {state.get('phase1_3_status')}"}

    # 修订 11.9:优先从 state 读 docx_path(推荐方案 A:每次重读,state 只存路径)
    if not docx_path:
        docx_path = state.get("phase1_3_docx_path")
    if not docx_path:
        return {"ok": False, "error": "未指定 docx_path,且 state 中无存档。请先调用 phase1_1_init 提交 docx。"}

    if not os.path.exists(docx_path):
        return {
            "ok": False,
            "error": f"开题报告文件不存在: {docx_path}",
            "action": "input_required",
            "retry_options": {
                "1": "重新上传 docx(不同文件)",
                "2": "切换到手动录入目录文本",
                "3": "取消"
            }
        }

    # 1. 读取目录树
    outline_state = outline_load(paper_name)
    if not outline_state:
        return {"ok": False, "error": "目录树未初始化"}
    outline_tree = outline_state["outline"]

    # 2. extract_proposal_content 提取并归因(细粒度)
    proposal_result = extract_proposal_content(
        docx_path, outline_tree, llm_func=llm_func
    )
    if not proposal_result.get("ok"):
        return {
            "ok": False,
            "error": proposal_result.get("error", "开题报告提取失败")
        }

    # 3. extract_content_hints 提炼
    content_hints = extract_content_hints(
        docx_path, outline_tree, llm_func=llm_func
    )

    # 4. save_content_hints_to_outline 写入 state
    save_result = save_content_hints_to_outline(paper_name, content_hints)

    # 5. 组装细粒度 node_details(拍板 #5)
    # 修复 P1-2:重命名 matched_count → matched_paragraphs_total,matched_paragraphs → matched_paragraphs_preview
    # 避免 matched_count=49 与 matched_paragraphs=list[3] 的数量不一致误解
    nodes = _get_outline_nodes(outline_state)
    node_id_set = {n["id"] for n in nodes}
    node_details = {}
    for node_id in node_id_set:
        node = next((n for n in nodes if n["id"] == node_id), None)
        node_segments = proposal_result.get("node_segments", {}).get(node_id, [])
        node_details[node_id] = {
            "title": node.get("title", "") if node else "",
            "level": node.get("level", 0) if node else 0,
            "content_hint": content_hints.get(node_id, ""),
            "matched_paragraphs_total": len(node_segments),  # 总段数
            "matched_paragraphs_preview": node_segments[:3],  # 前3段预览
            # 保留旧字段名(向后兼容 v2.0.1 调用方)
            "matched_count": len(node_segments),
            "matched_paragraphs": node_segments[:3],
            "has_hint": bool(content_hints.get(node_id))
        }

    # 6. 更新 state
    state["phase1_3_status"] = "submitted"
    state["phase1_3_docx_path"] = docx_path
    state["phase1_3_submitted_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    state["phase1_3_result"] = {
        "summary": {
            "total_paragraphs": proposal_result.get("total_paragraphs", 0),
            "matched_paragraphs": proposal_result.get("matched_paragraphs", 0),
            "ai_heading_matched": proposal_result.get("ai_heading_matched", 0),
            "ai_classified": proposal_result.get("ai_classified", 0),
            "orphan_segments": len(proposal_result.get("orphan_segments", [])),
            "undecided_segments": len(proposal_result.get("undecided_segments", [])),
            "hints_written": save_result.get("written", 0),
            "hints_skipped": save_result.get("skipped", 0),
        },
        "node_details": node_details,
    }
    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase1_3_status": "submitted",
        "docx_path": docx_path,
        "summary": state["phase1_3_result"]["summary"],
        "node_details": node_details,
        "orphan_segments": proposal_result.get("orphan_segments", []),
        "message": f"开题报告归因完成:{state['phase1_3_result']['summary']}"
    }


def update_node_content_hint(
    paper_name: str,
    node_id: str,
    new_hint: str
) -> Dict[str, Any]:
    """
    用户在 Phase 1.3 查看归因详情后,可手动调整单个节点的 content_hint。
    拍板 #4:允许用户覆盖。

    只能在 phase1_3_status in (submitted, confirmed) 时调用。
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    p13_status = state.get("phase1_3_status")
    if p13_status not in ("submitted", "confirmed"):
        return {"ok": False, "error": f"Phase 1.3 状态为 {p13_status},不能修改 content_hint"}

    if not new_hint or not new_hint.strip():
        return {"ok": False, "error": "new_hint 不能为空"}

    outline_update_status(paper_name, node_id, "pending", content_hint=new_hint.strip())

    # 同步更新 phase1_3_result.node_details 中的 content_hint
    if state.get("phase1_3_result") and state["phase1_3_result"].get("node_details"):
        nd = state["phase1_3_result"]["node_details"]
        if node_id in nd:
            nd[node_id]["content_hint"] = new_hint.strip()
            nd[node_id]["has_hint"] = True
            nd[node_id]["user_modified"] = True
            save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "node_id": node_id,
        "content_hint": new_hint.strip(),
        "message": f"节点 {node_id} content_hint 已更新"
    }


def confirm_phase1_3(paper_name: str) -> Dict[str, Any]:
    """
    用户确认 Phase 1.3 归因后调用。
    phase1_3_status = "confirmed",phase = "phase2"。
    拍板 #1 强制:必须确认才能进 Phase 2。
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if state.get("phase1_3_status") == "confirmed":
        return {"ok": True, "message": "Phase 1.3 已确认"}

    if state.get("phase1_3_status") != "submitted":
        return {"ok": False, "error": f"Phase 1.3 状态为 {state.get('phase1_3_status')},未提交"}

    state["phase1_3_status"] = "confirmed"
    state["phase1_3_confirmed_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    state["phase"] = "phase2"

    # 获取目录树（含节点层级结构）
    outline_state = outline_load(paper_name)
    if not outline_state:
        return {"ok": False, "error": "目录树未初始化"}
    nodes = _get_outline_nodes(outline_state)
    first_node = nodes[0] if nodes else None
    state["current_node_id"] = first_node["id"] if first_node else None

    # 构建含归因信息的完整章节树（拍板标准：用户流转 Phase2 前必须能 check 所有节点）
    node_details = state.get("phase1_3_result", {}).get("node_details", {})
    chapter_tree = {}    # {level1_id: {title, sections: {level2_id: {...}}, subsections: {level3_id: {...}}}}
    l2_to_l1 = {}  # 快速查找：level-2 node 所属的 level-1 node id
    for n in _get_outline_nodes(outline_state):
        nid = n["id"]
        nd = node_details.get(nid, {})
        level = n.get("level", 1)
        info = {
            "title": n.get("title", ""),
            "level": level,
            "content_hint": nd.get("content_hint", ""),
            "has_hint": nd.get("has_hint", False),
            "matched_paragraphs_preview": nd.get("matched_paragraphs_preview", []),
        }
        if level == 1:
            chapter_tree[nid] = {"title": info["title"], "sections": {}, "subsections": {}, **info}
        elif level == 2:
            parent = n.get("parent_id")
            if parent and parent in chapter_tree:
                chapter_tree[parent]["sections"][nid] = {"title": info["title"], **info}
                l2_to_l1[nid] = parent
        elif level == 3:
            parent = n.get("parent_id")
            l1_parent = l2_to_l1.get(parent) if parent else None
            if l1_parent and l1_parent in chapter_tree:
                chapter_tree[l1_parent]["subsections"][nid] = {"title": info["title"], **info}

    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase2",
        "phase1_3_status": "confirmed",
        "current_node_id": first_node["id"] if first_node else None,
        "node_details": node_details,
        "chapter_tree": chapter_tree,  # 含归因信息的完整章节树
        "summary": state.get("phase1_3_result", {}).get("summary", {}),
        "message": f"Phase 1.3 已确认,进入 Phase 2。"
               f"请核对下方章节树中每章/节/小节的 content_hint 是否与开题报告一致。"
    }


def skip_phase1_3(paper_name: str, reason: str = None, operator: str = None) -> Dict[str, Any]:
    """
    跳过 Phase 1.3(保留代码路径,拍板 #1 默认禁用)。

    ⚠️ 拍板 #1「强制」:默认不允许跳过。
    本函数仅用于调试或开发场景,必须显式提供 reason 和 operator 才能调用。

    v2.0.6 P0-1 修复:双层保护
      - 入口层(orchestrate())已拦截 phase1_3_skip action
      - 函数层强制检查 reason / operator + 生产环境 env guard

    参数:
      paper_name: 论文名
      reason: 跳过原因(必填,audit log)
      operator: 操作人/agent 标识(必填,audit log)

    返回:
      成功:{"ok": True, "audit_log": "..."}
      失败:{"ok": False, "error": "..."}
    """
    # v2.0.6 P0-1 修复:双层保护第一层 - 生产环境 env guard
    if os.environ.get("MBA_THESIS_PRODUCTION") == "1":
        return {
            "ok": False,
            "error": "拍板 #1 强制:MBA_THESIS_PRODUCTION=1 模式下禁止跳过 Phase 1.3",
            "hint": "取消环境变量或使用调试模式"
        }

    # v2.0.6 P0-1 修复:双层保护第二层 - 必填 reason + operator
    if not reason or not reason.strip():
        return {
            "ok": False,
            "error": "跳过 Phase 1.3 必须提供 reason 参数(audit 必填)"
        }
    if not operator or not operator.strip():
        return {
            "ok": False,
            "error": "跳过 Phase 1.3 必须提供 operator 参数(audit 必填)"
        }

    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    # v2.0.6 P0-1 修复:audit log
    audit_entry = {
        "action": "phase1_3_skip",
        "paper_name": paper_name,
        "reason": reason,
        "operator": operator,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }
    if "audit_log" not in state:
        state["audit_log"] = []
    state["audit_log"].append(audit_entry)

    state["phase1_3_status"] = "skipped"
    state["phase"] = "phase2"

    outline_state = outline_load(paper_name)
    nodes = _get_outline_nodes(outline_state)
    first_node = nodes[0] if nodes else None
    state["current_node_id"] = first_node["id"] if first_node else None

    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase2",
        "phase1_3_status": "skipped",
        "current_node_id": state["current_node_id"],
        "message": "Phase 1.3 已跳过,进入 Phase 2(注意:content_hint 全部为空)"
    }


# ============================================================
# Phase 2: 逐节点写作
# ============================================================

def get_next_writing_node(paper_name: str, state: Dict) -> Optional[str]:
    """
    获取下一个待写作节点
    从 current_node_id 往后找,跳过已完成的
    """
    outline_state = outline_load(paper_name)
    if not outline_state:
        return None

    nodes = _get_outline_nodes(outline_state)
    node_ids = [n["id"] for n in nodes]   

    current = state.get("current_node_id")
    if current is None:
        # 首次,从第一个开始
        return node_ids[0] if node_ids else None

    # 从 current 之后找下一个未完成的（排除 completed + failed）
    try:
        idx = node_ids.index(current)
        failed = set(state.get("failed_nodes", []))
        for i in range(idx + 1, len(node_ids)):
            nid = node_ids[i]
            if nid not in state["completed_nodes"] and nid not in failed:
                return nid
        return None  # 全部完成
    except ValueError:
        return node_ids[0]


def write_single_node(paper_name: str, node_id: str,
                     llm_func: Callable[[str], str],
                     bypass_scarcity: bool = False,
                     reviewer_func: Callable[[str], str] = None,
                     allow_self_review: bool = False) -> Dict[str, Any]:
    """
    执行单个节点的写作 + 评审流程

    参数:
      paper_name: 论文名
      node_id: 节点 ID
      llm_func: LLM 调用函数(写作)
      bypass_scarcity: 是否跳过 Step 1.5 的 info_scarcity 检查(修复 B-1)
        - True: 跳过 scarcity 检查直接写作(用于 apply_user_decision 之后)
        - False: 默认,按原逻辑检查
      reviewer_func: 独立评审函数(v2.0.6 P1-2 新增)
        - None: 默认使用 llm_func(self-review,警告)
        - callable: 独立 LLM 评审函数
      allow_self_review: 是否允许 self-review
        - False: 默认,llm_func == reviewer_func 时警告
        - True: 调试场景可设为 True

    v2.0.6 P1-2 修复:独立 Reviewer
      - 防止生成和评审使用同一个 LLM(自我审核)
      - 默认要求 reviewer_func != llm_func
      - allow_self_review=True 可调试

    返回:
      {
        ok: bool,
        action: "completed" | "pending_review" | "needs_user_input" | "error",
        node_id: str,
        review_result: dict | None,
        error: str
      }
    """
    # v2.0.6 P1-2 修复:独立 Reviewer 警告
    if reviewer_func is None:
        if not allow_self_review:
            import warnings
            warnings.warn(
                f"⚠️ v2.0.6 P1-2: write_single_node({node_id}) 未传 reviewer_func,"
                f"默认 self-review (llm_func 同时用于生成与评审)。"
                f"建议传入独立 reviewer_func 或显式 allow_self_review=True。",
                stacklevel=2
            )
        actual_reviewer = llm_func
    else:
        if reviewer_func is llm_func and not allow_self_review:
            import warnings
            warnings.warn(
                f"⚠️ v2.0.6 P1-2: write_single_node({node_id}) reviewer_func 与 llm_func 是同一对象,"
                f"请传独立 reviewer_func。",
                stacklevel=2
            )
        actual_reviewer = reviewer_func
    # Step 1: 构建 prompt 并写作
    from node_writer import write_node

    write_result = write_node(paper_name, node_id)
    if not write_result["ok"]:
        return {
            "ok": False,
            "action": "error",
            "node_id": node_id,
            "review_result": None,
            "error": write_result.get("error", "写作失败")
        }

    prompt_text = write_result.get("prompt", "")

    # Step 1.5 (增强项4): 写作前信息检查
    # 修复 B-1:bypass_scarcity=True 时跳过检查(Orchestrator 已决策的路径)
    scarcity_check = check_info_scarcity(paper_name, node_id)
    if not bypass_scarcity and scarcity_check.get("action") == "needs_user_input":
        # 贫瘠 → 暂停,返回 needs_user_input
        return {
            "ok": True,
            "action": "needs_user_input",
            "node_id": node_id,
            "scarcity_info": scarcity_check,
            "review_result": None,
            "chapter_summary": None,
            "error": ""
        }

    # Step 2: 调用 LLM 生成内容
    system_prompt = (
        "你是一位专业的 MBA 学术论文写作者。\n"
        "请根据以下写作任务生成内容。\n"
        "生成完成后,请用 <key_conclusion>标签</key_conclusion> 包裹本节的核心结论,"
        "以便程序提取。\n\n"
        "写作要求:\n"
        "1. 内容需符合学术论文规范\n"
        "2. 逻辑清晰,论证充分\n"
        "3. 字数在指定范围内\n"
        "4. 结尾必须包含用 <key_conclusion> 包裹的结论摘要\n"
    )

    full_prompt = f"{system_prompt}\n\n{prompt_text}"

    try:
        response_text = llm_func(full_prompt)
    except Exception as e:
        return {
            "ok": False,
            "action": "error",
            "node_id": node_id,
            "review_result": None,
            "error": f"LLM 调用失败: {str(e)}"
        }

    # Step 3: 解析 response,提取 content 和 key_conclusion
    import re
    from node_writer import extract_key_conclusion_from_response, count_words

    content_clean = re.sub(
        r'<key_conclusion>.*?</key_conclusion>',
        '',
        response_text,
        flags=re.DOTALL
    ).strip()

    key_conclusion = extract_key_conclusion_from_response(response_text)
    word_count = count_words(content_clean)

    # Step 4: 写入 state(先用 reviewing,评审通过后才 completed)
    outline_update_status(
        paper_name, node_id, "reviewing",
        content=content_clean,
        key_conclusion=key_conclusion,
        word_count=word_count
    )

    # Step 4.5: 增强项1 - 触发章节摘要合成(如适用)
    chapter_summary_result = None
    try:
        chapter_id = is_last_child_of_chapter(paper_name, node_id)
        if chapter_id:
            chapter_summary_result = synthesize_chapter_summary(
                paper_name, chapter_id, llm_func
            )
    except Exception as e:
        chapter_summary_result = {
            "ok": False,
            "action": "ask_user",
            "error": f"章节摘要合成异常: {str(e)}"
        }

    # Step 5: 评审
    # review_node() 内部会从磁盘加载节点内容（Step 4 已通过 outline_update_status 写入）
    # 无需在此手动修改内存中的 node 字典

    # 调用评审(注入 mock outline_get_node)
    def mock_llm(prompt: str) -> str:
        return llm_func(prompt)

    review_result = review_node(paper_name, node_id, actual_reviewer)

    # action 规则:
    # high → 自动完成
    # medium/low → 需要用户确认
    quality = review_result.get("quality", "medium")
    if quality == "high":
        outline_update_status(paper_name, node_id, "completed")
        action = "completed"
    else:
        action = "pending_review"

    return {
        "ok": True,
        "action": action,
        "node_id": node_id,
        "review_result": review_result,
        "chapter_summary": chapter_summary_result,
        "error": ""
    }


def orchestrate_phase2(paper_name: str,
                      llm_func: Optional[Callable[[str], str]] = None) -> Dict[str, Any]:
    """
    Phase 2: 逐节点写作 + 评审

    支持断点续跑:从 current_node_id 继续

    参数:
      paper_name: 论文名
      llm_func: LLM 调用函数(必传)。修复 P1-1:调用时校验,缺则返回友好错误而非 TypeError
    """
    # 修复 P1-1:llm_func 缺则返回友好错误
    if llm_func is None:
        return {
            "ok": False,
            "error": "llm_func 必传:Phase 2 需要调用 LLM 进行写作,请提供 llm_func(prompt) -> str",
            "action": "input_required"
        }

    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在,请先初始化 Phase 1"}

    if not state.get("phase1_confirmed"):
        return {"ok": False, "error": "Phase 1 目录未确认"}

    # Step 11 拍板 #1 强制:Phase 1.3 必须确认才能进 Phase 2
    if state.get("phase1_3_status") != "confirmed":
        return {
            "ok": False,
            "error": f"Phase 1.3 未确认(当前状态: {state.get('phase1_3_status')}),请先提交并确认开题报告归因"
        }

    if state["phase"] not in ("phase2",):
        return {"ok": False, "error": f"当前阶段为 {state['phase']},不是 phase2"}

    # 检查是否有待用户确认的节点
    if state.get("pending_review"):
        pending_node = state["pending_review"][0]
        return {
            "ok": True,
            "action": "wait_for_user",
            "reason": "pending_review",
            "node_id": pending_node,
            "message": f"节点 {pending_node} 需要您确认评审结果"
        }

    # 获取下一个待处理节点
    next_node = get_next_writing_node(paper_name, state)

    if next_node is None:
        # 全部完成
        state["phase"] = "phase3"
        save_orchestrate_state(paper_name, state)
        return {
            "ok": True,
            "action": "phase_complete",
            "phase": "phase3",
            "message": "所有节点写作完成,进入 Phase 3"
        }

    # 执行当前节点
    result = write_single_node(paper_name, next_node, llm_func)

    if not result["ok"]:
        return result

    # 修复 B-1:needs_user_input action 必须单独处理(不进 pending_review)
    if result["action"] == "needs_user_input":
        # HIL 路径:不修改任何 state,直接返回给 Orchestrator 上层决策
        # 调用方需调 apply_user_decision + write_single_node(bypass_scarcity=True) 继续
        return {
            "ok": True,
            "action": "needs_user_input",
            "node_id": next_node,
            "scarcity_info": result.get("scarcity_info", {}),
            "progress": state["progress"],
            "message": f"节点 {next_node} 信息贫瘠,需要用户决策(决策 1=提供 hint, 2=AI 自行生成, 3=跳过)"
        }

    # 更新 state
    state["current_node_id"] = next_node

    quality = result["review_result"].get("quality", "medium")

    if result["action"] == "completed":
        state["completed_nodes"].append(next_node)
        update_progress(state)

        # 继续下一节点
        next_next = get_next_writing_node(paper_name, state)
        return {
            "ok": True,
            "action": "continue",
            "node_id": next_node,
            "quality": quality,
            "review_result": result["review_result"],
            "next_node_id": next_next,
            "progress": state["progress"],
            "message": f"节点 {next_node} 完成(质量:{quality}),进入下一节点 {next_next}"
        }
    else:
        # 需要用户确认(medium/low)
        state["pending_review"].append(next_node)
        update_progress(state)
        save_orchestrate_state(paper_name, state)

        return {
            "ok": True,
            "action": "wait_for_user",
            "reason": "pending_review",
            "node_id": next_node,
            "quality": quality,
            "review_result": result["review_result"],
            "progress": state["progress"],
            "message": f"节点 {next_node} 需要您确认评审结果(质量:{quality})"
        }


def handle_review_decision(paper_name: str, node_id: str,
                          decision: str) -> Dict[str, Any]:
    """
    处理用户对评审结果的决策

    decision: "continue" | "rewrite" | "skip"
      - continue: 接受当前版本,继续下一节点
      - rewrite: 要求重新生成
      - skip: 跳过该节点
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if node_id not in state.get("pending_review", []):
        return {"ok": False, "error": f"节点 {node_id} 不在待确认列表中"}

    if decision == "continue":
        # 接受当前版本:同步 outline state(reviewing → completed)
        outline_update_status(paper_name, node_id, "completed", force=True)
        state = load_orchestrate_state(paper_name)  # 重新加载
        state["pending_review"].remove(node_id)
        if node_id not in state["completed_nodes"]:
            state["completed_nodes"].append(node_id)
        update_progress(state)

    elif decision == "skip":
        # 跳过
        state["pending_review"].remove(node_id)
        state["failed_nodes"].append(node_id)
        update_progress(state)

    elif decision == "rewrite":
        # 打回重写(从 pending 中移除,不加入 completed,下次会重新生成)
        state["pending_review"].remove(node_id)
        # 重置 outline writing_status 为 pending（清除 reviewing 状态）
        outline_update_status(paper_name, node_id, "pending")
        # 不加入 completed_nodes,下次会重新生成

    save_orchestrate_state(paper_name, state)

    # 获取下一节点
    next_node = get_next_writing_node(paper_name, state)

    return {
        "ok": True,
        "decision": decision,
        "next_node_id": next_node,
        "progress": state["progress"],
        "message": f"已处理节点 {node_id} 的决策 ({decision}),下一节点:{next_node}"
    }


# ============================================================
# Phase 3: 整合 + 修改 + 输出
# ============================================================

def orchestrate_phase3(paper_name: str) -> Dict[str, Any]:
    """
    Phase 3: 整合所有节点内容,生成完整论文
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if state["phase"] != "phase3":
        return {"ok": False, "error": f"当前阶段为 {state['phase']},不是 phase3"}

    # 加载所有节点内容
    outline_state = outline_load(paper_name)
    nodes = _get_outline_nodes(outline_state)   

    completed_ids = set(state["completed_nodes"])

    full_content = _assemble_full_content(paper_name, state)

    # 标记为待用户确认状态
    state["phase3_status"] = "awaiting_review"
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase3",
        "sub_status": "awaiting_review",
        "content": full_content,
        "word_count": len(full_content),
        "completed_count": len(state["completed_nodes"]),
        "failed_count": len(state.get("failed_nodes", [])),
        "message": "论文已整合,请预览并提出修改意见"
    }


def handle_phase3_feedback(paper_name: str,
                          feedback: List[Dict[str, str]],
                          llm_func: Callable[[str], str] = None) -> Dict[str, Any]:
    """
    Phase 3: 处理用户修改意见

    feedback 格式:
    [
        {"node_id": "1.1", "instruction": "补充行业数据支撑"},
        {"node_id": "2.1", "instruction": "逻辑不够清晰,重新组织"}
    ]

    返回:修改后的完整论文内容
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if state["phase"] != "phase3":
        return {"ok": False, "error": f"当前阶段为 {state['phase']},不是 phase3"}

    if not feedback:
        return {"ok": False, "error": "feedback 为空"}

    if not llm_func:
        return {"ok": False, "error": "修改需要提供 llm_func"}

    modified_count = 0
    for item in feedback:
        node_id = item.get("node_id")
        instruction = item.get("instruction", "")

        if not node_id:
            continue

        # 获取当前节点内容
        node = outline_get_node(paper_name, node_id)
        if not node:
            continue

        current_content = node.get("content", "")

        # 调用 LLM 修改
        prompt = f"""节点:{node.get('title', node_id)}

当前内容:
---
{current_content}
---

修改要求:{instruction}

请根据修改要求,生成修改后的完整内容。"""

        try:
            new_content = llm_func(prompt)
            # 去掉可能的 key_conclusion 标签
            import re
            new_content = re.sub(r'<key_conclusion>.*?</key_conclusion>', '', new_content, flags=re.DOTALL).strip()

            # 写入 state
            outline_update_status(paper_name, node_id, "completed", content=new_content, force=True)
            modified_count += 1
        except Exception as e:
            import warnings
            warnings.warn(f"Phase 3 修改节点 {node_id} 异常: {e}")

    # 重新整合
    result = orchestrate_phase3(paper_name)
    result["modified_count"] = modified_count
    result["message"] = f"已完成 {modified_count} 处修改,请再次预览"

    return result


def confirm_phase3_and_export(paper_name: str) -> Dict[str, Any]:
    """
    Phase 3: 用户确认整合结果,输出 Word
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    if state["phase"] != "phase3":
        return {"ok": False, "error": f"当前阶段为 {state['phase']},不是 phase3"}

    full_content = _assemble_full_content(paper_name, state)

    # 保存最终内容(统一路径:WORKSPACE/paper_name/final.md)
    output_dir = _get_paper_dir(paper_name)
    output_path = os.path.join(output_dir, f"{paper_name}_final.md")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return {
        "ok": True,
        "phase": "phase3",
        "sub_status": "exported",
        "output_path": output_path,
        "word_count": len(full_content),
        "message": f"论文已导出至 {output_path},请使用 md2docx_strict.py 转换为 Word"
    }


# ============================================================
# Phase 3.5:深度学术评审
# ============================================================


# ============================================================
# 辅助函数:基于大纲拆分论文正文
# ============================================================

def _build_chapter_pattern(node_title: str) -> str:
    """
    根据大纲节点标题构造定位正则。

    "第1章 研究背景与意义"
      → r'^#+\s*第1章[^\n]*研究背景[^\n]*'m

    规则:
      - 强制保留:章节号(第1-7章)
      - 强制匹配:章节号后前8个非标点字符(核心关键词)
      - 可选:剩余文字(允许正文标题略有不同)
    """
    # 提取章节号
    num_match = re.search(r'第[1-7]章', node_title)
    if not num_match:
        return r'^#+\s*第[1-7]章'
    chapter_num = num_match.group()

    # 提取章节号后的文字,取前8个非标点字符作为关键词
    after_num = node_title[len(chapter_num):].strip()
    keywords = re.sub(r'[^\w\u4e00-\u9fff]', '', after_num)[:8]

    if keywords:
        return rf'^#+\s*{re.escape(chapter_num)}[^\n]*{re.escape(keywords)}[^\n]*'
    else:
        # 退化:只有章节号
        return rf'^#+\s*{re.escape(chapter_num)}'


def _split_by_chapter(
    content: str,
    outline_nodes: List[Dict]
) -> Dict[str, Dict]:
    """
    基于大纲 level-1 节点拆分论文内容。

    参数:
      content:        完整论文 Markdown 字符串
      outline_nodes:  outline_tree["nodes"] 列表

    返回:
      {
        "ch1": {
          "node_id":     "ch1",
          "chapter_num": "第1章",
          "title":       "第1章 研究背景与意义",
          "content":      "## 1.1 研究背景\n...",
          "matched":      True,     # 是否成功在正文中定位
          "start_char":   0,
          "end_char":     1523,
        },
        ...
      }
    """
    import warnings

    # Step 1:提取 level-1 节点,按 original_index 排序
    level1_nodes = [
        n for n in outline_nodes if n.get("level") == 1
    ]
    level1_nodes.sort(key=lambda x: x.get("original_index", 0))

    if not level1_nodes:
        # 退化:无可用大纲节点,回退到硬编码正则
        warnings.warn("[_split_by_chapter] 无 level-1 节点,回退到硬编码正则拆分")
        pattern = r'^(#\s*第[1-7]章[^\n]*)(?=\n#+[^\n]|$)'
        matches = list(re.finditer(pattern, content, re.MULTILINE))
        chapters = {}
        for i, match in enumerate(matches):
            ch_num_match = re.match(r'#\s*(第[1-7]章)', match.group(1).strip())
            if not ch_num_match:
                continue
            chapter_id = ch_num_match.group(1)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            chapter_content = content[start:end].strip()
            chapters[chapter_id] = {
                "node_id": chapter_id, "chapter_num": chapter_id,
                "title": match.group(1).strip(), "content": chapter_content,
                "matched": True, "start_char": match.start(), "end_char": end
            }
        return chapters

    # Step 2:构造每章在正文中的起止位置
    result: Dict[str, Dict] = {}

    for idx, node in enumerate(level1_nodes):
        node_id = node["id"]
        title = node.get("title", "")

        # 构造本章正则
        pattern_str = _build_chapter_pattern(title)
        pattern = re.compile(pattern_str, re.MULTILINE)
        match = pattern.search(content)

        if match:
            start_char = match.start()
            # 找下一章的位置作为终点
            end_char = None
            for next_idx in range(idx + 1, len(level1_nodes)):
                next_title = level1_nodes[next_idx].get("title", "")
                next_pattern = re.compile(_build_chapter_pattern(next_title), re.MULTILINE)
                next_match = next_pattern.search(content, start_char + 1)
                if next_match:
                    end_char = next_match.start()
                    break
            if end_char is None:
                end_char = len(content)

            # 内容 = 标题行之后到 end_char 之前
            raw_content = content[match.end():end_char].strip()
            # 重组:保留标题行 + 内容
            chapter_content = f"{match.group().strip()}\n\n{raw_content}" if raw_content else match.group().strip()

            result[node_id] = {
                "node_id": node_id,
                "chapter_num": re.search(r'第[1-7]章', title).group() if re.search(r'第[1-7]章', title) else "",
                "title": title,
                "content": chapter_content,
                "matched": True,
                "start_char": start_char,
                "end_char": end_char,
            }
        else:
            # 未匹配到:用前后章节位置推算,打印 warning
            warnings.warn(
                f"[_split_by_chapter] 节点 \"{node_id}\" 在正文中未找到标题行:{title}"
            )
            # 尝试估算位置
            prev_end = result[level1_nodes[idx - 1]["id"]]["end_char"] if idx > 0 and level1_nodes[idx - 1]["id"] in result else 0
            next_start = None
            for next_idx in range(idx + 1, len(level1_nodes)):
                next_title = level1_nodes[next_idx].get("title", "")
                next_pattern = re.compile(_build_chapter_pattern(next_title), re.MULTILINE)
                next_match = next_pattern.search(content, prev_end + 1)
                if next_match:
                    next_start = next_match.start()
                    break
            next_start = next_start or len(content)

            result[node_id] = {
                "node_id": node_id,
                "chapter_num": re.search(r'第[1-7]章', title).group() if re.search(r'第[1-7]章', title) else "",
                "title": title,
                "content": "",
                "matched": False,
                "start_char": prev_end,
                "end_char": next_start,
            }

    return result


def _parse_review_json(response: str) -> Dict[str, Any]:
    """从 LLM 响应中解析 JSON 评审结果"""
    import re
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    return {"p0": [], "p1": [], "p2": [], "summary": "解析失败,请重试"}


def _normalize_issue_text(text: str) -> str:
    """归一化问题文本用于去重:移除标点/空格/大小写"""
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', '', text)
    return text.lower()


def _get_p0_signature(p0_list: List[Dict]) -> set:
    """获取 P0 问题签名(node_id + 归一化文本前50字符)"""
    signatures = set()
    for item in p0_list:
        node_id = item.get("node_id", "")
        issue_text = _normalize_issue_text(item.get("issue", ""))[:50]
        signatures.add(f"{node_id}:{issue_text}")
    return signatures


# 对 Phase 3 整合版做二次审查,输出 P0/P1/P2 分级问题清单
# ============================================================

def orchestrate_phase3_5(paper_name: str,
                         llm_func: Optional[Callable[[str], str]] = None) -> Dict[str, Any]:
    """
    Phase 3.5:深度学术评审(固定节点,不可跳过)

    输入:Phase 3 整合版论文
    输出:P0/P1/P2 分级问题清单

    后续:有 P0 → 自动进入修订 → 回到 Phase 3.5 重审
          无 P0 → 进入 Phase 4
          连续 2 轮无新 P0 → 通过
          超 3 轮 → HIL 暂停
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    # 获取 Phase 3 整合版内容
    outline_state = outline_load(paper_name)
    if not outline_state:
        return {"ok": False, "error": "目录树未初始化"}
    full_content = _assemble_full_content(paper_name, state)
    if not full_content:
        return {"ok": False, "error": "目录树未初始化或无已完成节点"}

    # _split_by_chapter 需要 nodes 参数，从 outline 加载
    outline_state = outline_load(paper_name)
    nodes = _get_outline_nodes(outline_state) if outline_state else []   


    # 逐章深度评审(修复 8000 字截断 Bug)
    if llm_func:
        all_p0, all_p1, all_p2 = [], [], []
        chapter_summaries = []

        # M5 修复:预构建章节 key_conclusion 摘要,供跨章评审使用
        chapter_conclusions = {}
        for node in nodes:
            if node.get("writing_status") == "completed":
                ch_id = node["id"]
                kc = node.get("key_conclusion", "")
                if kc:
                    chapter_conclusions[ch_id] = kc

        chapters = _split_by_chapter(full_content, nodes)
        for node_id, chapter_info in chapters.items():
            chapter_text = chapter_info["content"]

            # M5 修复:构建前后章上下文
            sorted_ids = list(chapters.keys())
            idx_map = {nid: i for i, nid in enumerate(sorted_ids)}
            idx = idx_map.get(node_id, -1)
            ctx_lines = []
            if idx > 0:
                prev_id = sorted_ids[idx - 1]
                prev_kc = chapter_conclusions.get(prev_id, "")
                if prev_kc:
                    ctx_lines.append(f"【前一章核心结论】\n{prev_kc}")
            if idx >= 0 and idx < len(sorted_ids) - 1:
                next_title = chapters[sorted_ids[idx + 1]]["title"]
                ctx_lines.append(f"【下一章标题】\n{next_title}")
            context_block = ("\n\n".join(ctx_lines) + "\n\n") if ctx_lines else ""

            chapter_prompt = f"""你是一位学术论文评审专家。请对以下论文的第 {node_id} 进行深度学术评审。

评审维度:
1. 理论框架是否完整、逻辑一致
2. 论证链是否严密,有无跳跃或断层
3. 数据/引用支撑是否充分
4. 结论是否与前面的分析一致对应
5. 章节之间逻辑衔接是否顺畅
6. 学术规范(引用格式、术语一致性)
{context_block}
请按以下分级输出问题清单:
- P0(阻塞性):必须修复的问题(论证错误、数据明显偏差、逻辑断裂)
- P1(重要):建议修复(引用不充分、表述不清晰、结构可优化)
- P2(轻微):可选项(格式微调、措辞润色)

章节内容:
---
{chapter_text}
---

以 JSON 格式输出:
{{
  "p0": [{{"node_id": "{node_id}", "issue": "...", "severity": "p0"}}],
  "p1": [...],
  "p2": [...],
  "summary": "本章评价(50字以内)"
}}
只输出 JSON。"""

            try:
                response = llm_func(chapter_prompt)
                chapter_result = _parse_review_json(response)
                all_p0.extend(chapter_result.get("p0", []))
                all_p1.extend(chapter_result.get("p1", []))
                all_p2.extend(chapter_result.get("p2", []))
                if chapter_result.get("summary"):
                    chapter_summaries.append(f"{node_id}:{chapter_result['summary']}")
            except Exception as e:
                import warnings
                warnings.warn(f"Phase 3.5 评审章节 {node_id} 异常: {e}")
                chapter_summaries.append(f"{node_id}:评审异常 - {e}")

        review_result = {
            "p0": all_p0,
            "p1": all_p1,
            "p2": all_p2,
            "summary": "; ".join(chapter_summaries) if chapter_summaries else "逐章评审完成"
        }
    else:
        review_result = {"p0": [], "p1": [], "p2": [], "summary": "未提供 llm_func,跳过深度评审"}

    # 更新状态
    p0_count = len(review_result.get("p0", []))
    p1_count = len(review_result.get("p1", []))
    p2_count = len(review_result.get("p2", []))
    review_round = state.get("phase3_5_round", 0) + 1

    state["phase"] = "phase3.5"
    state["phase3_5_round"] = review_round
    state["phase3_5_result"] = review_result
    state["phase3_5_status"] = "pending_review"

    # 连续2轮无新P0检测(修复 P1-7:改用 node_id + 归一化文本签名)
    prev_p0_sigs = _get_p0_signature(
        state.get("phase3_5_prev_result", {}).get("p0", [])
    )
    curr_p0_sigs = _get_p0_signature(review_result.get("p0", []))
    new_p0 = curr_p0_sigs - prev_p0_sigs

    if p0_count == 0:
        # 无 P0 → 连续 clean 递增
        state["phase3_5_consecutive_clean"] = state.get("phase3_5_consecutive_clean", 0) + 1
        # 连续 2 轮无 P0 才通过
        if state["phase3_5_consecutive_clean"] >= 2:
            state["phase3_5_status"] = "passed"
        else:
            state["phase3_5_status"] = "pending_review"
    elif not new_p0:
        # 有 P0 但无新增(旧 P0 未修复)→ 不递增 clean,也不重置
        state["phase3_5_status"] = "pending_review"
    else:
        # 有新 P0 → 重置 clean
        state["phase3_5_consecutive_clean"] = 0
        state["phase3_5_status"] = "pending_review"

    # 记录本次结果供下次对比
    state["phase3_5_prev_result"] = review_result

    # HIL #7:超 3 轮未收敛
    needs_hil = review_round > 3 and p0_count > 0

    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase3.5",
        "review_round": review_round,
        "p0": review_result.get("p0", []),
        "p1": review_result.get("p1", []),
        "p2": review_result.get("p2", []),
        "p0_count": p0_count,
        "p1_count": p1_count,
        "p2_count": p2_count,
        "new_p0_count": len(new_p0),
        "consecutive_clean": state.get("phase3_5_consecutive_clean", 0),
        "summary": review_result.get("summary", ""),
        "needs_hil": needs_hil,
        "status": state["phase3_5_status"],
        "message": f"深度评审第 {review_round} 轮:P0={p0_count}, P1={p1_count}, P2={p2_count}" + \
                   (",已达到通过标准" if state["phase3_5_status"] == "passed" else "") + \
                   (",超过3轮未收敛,需要您决策" if needs_hil else ""),
    }


def auto_fix_p0_issues(paper_name: str,
                       llm_func: Callable[[str], str]) -> Dict[str, Any]:
    """
    Phase 3.5 → Phase 4 自动衔接:修复 P0 问题

    读取 phase3_5_result 中的 P0 问题,逐个调用 LLM 修复。
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    review_result = state.get("phase3_5_result", {})
    p0_issues = review_result.get("p0", [])

    if not p0_issues:
        return {"ok": True, "fixed": 0, "message": "无 P0 问题需要修复"}

    fixed = 0
    for issue in p0_issues:
        node_id = issue.get("node_id", "")
        issue_text = issue.get("issue", "")
        if not node_id or not issue_text:
            continue

        node = outline_get_node(paper_name, node_id)
        if not node:
            continue

        current_content = node.get("content", "")
        if not current_content:
            continue

        prompt = f"""请修复以下问题:
节点:{node.get('title', node_id)}
问题:{issue_text}

当前内容:
---
{current_content}
---

请输出修复后的完整内容。
"""

        try:
            new_content = llm_func(prompt)
            import re
            new_content = re.sub(r'<key_conclusion>.*?</key_conclusion>', '', new_content, flags=re.DOTALL).strip()

            # M3 修复:字数校验,修复后不应大幅缩水
            old_len = len(current_content)
            new_len = len(new_content)
            if old_len > 0 and new_len < old_len * 0.5:
                import warnings
                warnings.warn(
                    f"Phase 4 修复跳过:节点 {node_id} 修复后字数 {new_len} < 原字数 {old_len} 的 50%,"
                    f"疑似修复失败,保留原内容"
                )
                continue

            # M3 修复:写入新内容(outline_update_status 会自动备份旧 content)
            outline_update_status(paper_name, node_id, "completed", content=new_content, force=True)
            fixed += 1
        except Exception as e:
            import warnings
            warnings.warn(f"Phase 4 修复节点 {node_id} 异常: {e}")

    return {
        "ok": True,
        "fixed": fixed,
        "total": len(p0_issues),
        "message": f"已修复 {fixed}/{len(p0_issues)} 个 P0 问题"
    }


# ============================================================
# Phase 4:整合 + 终审
# ============================================================

def orchestrate_phase4(paper_name: str,
                       llm_func: Optional[Callable[[str], str]] = None) -> Dict[str, Any]:
    """
    Phase 4:整合 P0/P1 修复 + 终审

    流程:
      1. 自动修复 P0 问题
      2. 建议修复 P1 问题(询问用户)
      3. 重新整合论文
      4. 输出最终版
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    review_result = state.get("phase3_5_result", {})
    p0 = review_result.get("p0", [])
    p1 = review_result.get("p1", [])

    # HIL #8:Phase 4 开始前检查 Phase 3.5 是否已通过
    phase3_5_status = state.get("phase3_5_status", "")
    if phase3_5_status != "passed":
        p0_count = len(p0)
        p1_count = len(p1)
        print(f"\n⚠️ HIL #8: Phase 3.5 尚未通过,是否继续 Phase 4?")
        print(f"  当前 P0={p0_count}, P1={p1_count}")

        # 通过 Gatekeeper 通知用户,等决策(blocking)
        gk_result = _gk_notify(
            paper_name=paper_name,
            event="hils_blocked",
            phase="phase4",
            node_id="",
            details={"hil": "hil8", "p0": p0_count, "p1": p1_count},
            blocking=True,
        )

        if not gk_result.get("gk_disabled"):
            # Gatekeeper 模式:看用户决策
            if gk_result.get("blocked"):
                return {
                    "ok": False,
                    "blocked": "hil8_timeout",
                    "p0": p0_count,
                    "p1": p1_count,
                    "message": "HIL #8:Gatekeeper 决策超时(30分钟),Phase 4 已暂停"
                }
            decision = gk_result.get("decision", "")
            if decision not in ("proceed", "fix"):
                return {
                    "ok": False,
                    "blocked": "hil8_phase3_5_not_passed",
                    "gk_decision": decision,
                    "p0": p0_count,
                    "p1": p1_count,
                    "message": f"HIL #8:用户选择「{decision}」,Phase 4 已暂停"
                }
            # decision == proceed 或 fix → 继续
        else:
            # 回退 CLI 交互
            if not sys.stdin.isatty():
                return {
                    "ok": False,
                    "blocked": "hil8_phase3_5_not_passed",
                    "p0": p0_count,
                    "p1": p1_count,
                    "message": f"HIL #8:Phase 3.5 未通过(P0={p0_count}, P1={p1_count}),需人工确认后继续"
                }
            user_input = input("  继续执行 Phase 4?(y/N): ").strip().lower()
            if user_input != 'y':
                return {
                    "ok": False,
                    "blocked": "hil8_phase3_5_not_passed",
                    "p0": p0_count,
                    "p1": p1_count,
                    "message": f"HIL #8:Phase 3.5 未通过(当前 P0={p0_count}, P1={p1_count}),已暂停"
                }

    # 自动修复 P0
    fix_result = {"fixed_p0": 0, "fixed_p1": 0}
    if p0 and llm_func:
        from context_builder import build_prompt_package, build_prompt_package_text
        fixed = 0
        for issue in p0:
            node_id = issue.get("node_id", "")
            issue_text = issue.get("issue", "")
            if not node_id or not issue_text:
                continue
            node = outline_get_node(paper_name, node_id)
            if not node or not node.get("content"):
                continue
            prompt = f"""修复节点「{node.get('title', node_id)}」的以下问题:
{issue_text}

当前内容:
---
{node['content']}
---

输出修复后的完整内容。"""
            try:
                new_c = llm_func(prompt)
                import re
                new_c = re.sub(r'<key_conclusion>.*?</key_conclusion>', '', new_c, flags=re.DOTALL).strip()

                # M3 修复:字数校验
                old_len = len(node.get("content", ""))
                new_len = len(new_c)
                if old_len > 0 and new_len < old_len * 0.5:
                    import warnings
                    warnings.warn(
                        f"Phase 4 修复跳过:节点 {node_id} 修复后字数 {new_len} < 原字数 {old_len} 的 50%,"
                        f"疑似修复失败,保留原内容"
                    )
                    continue

                outline_update_status(paper_name, node_id, "completed", content=new_c, force=True)
                fixed += 1
            except Exception as e:
                import warnings
                warnings.warn(f"Phase 4 修复节点 {node_id} 异常: {e}")
        fix_result["fixed_p0"] = fixed

    # 重新整合论文
    full_content = _assemble_full_content(paper_name, state)

    state["phase"] = "phase4"
    state["phase4_status"] = "completed"
    save_orchestrate_state(paper_name, state)

    return {
        "ok": True,
        "phase": "phase4",
        "fixed_p0": fix_result["fixed_p0"],
        "pending_p1": len(p1),
        "word_count": len(full_content),
        "message": f"Phase 4 整合完成:已修复 {fix_result['fixed_p0']} 个 P0 问题,还有 {len(p1)} 个 P1 建议"
    }


# ============================================================
# Phase 5:终审 + Word 输出
# ============================================================

def orchestrate_phase5(paper_name: str) -> Dict[str, Any]:
    """
    Phase 5:终审 + Word 输出

    流程:
      1. 运行 loop_self_check.py 做 Guardrails 校验
      2. 输出最终 Markdown 文件
      3. 提示用户可运行 md2docx_strict.py 转 Word
    """
    state = load_orchestrate_state(paper_name)
    if not state:
        return {"ok": False, "error": "状态文件不存在"}

    # HIL #9:Word 输出前最终审批
    p0 = len(state.get("phase3_5_result", {}).get("p0", []))
    p1 = len(state.get("phase3_5_result", {}).get("p1", []))
    print(f"\n⚠️ HIL #9: Phase 5 Word 输出前最终审批")
    print(f"  Phase 3.5 结果:P0={p0}, P1={p1}")
    print(f"  即将导出最终版 Markdown 并生成 Word")

    # 通过 Gatekeeper 通知用户,等决策(blocking)
    gk_result = _gk_notify(
        paper_name=paper_name,
        event="export_ready",
        phase="phase5",
        node_id="",
        details={"p0": p0, "p1": p1},
        blocking=True,
    )

    proceed = False
    if not gk_result.get("gk_disabled"):
        if gk_result.get("blocked"):
            return {
                "ok": False,
                "blocked": "hil9_timeout",
                "message": "HIL #9:Gatekeeper 决策超时(30分钟),导出已暂停"
            }
        decision = gk_result.get("decision", "")
        if decision in ("proceed", "fix"):
            proceed = True
        else:
            return {
                "ok": False,
                "blocked": "hil9_word_export_not_confirmed",
                "gk_decision": decision,
                "message": f"HIL #9:用户选择「{decision}」,已取消导出"
            }
    else:
        # 回退 CLI 交互
        if not sys.stdin.isatty():
            return {
                "ok": False,
                "blocked": "hil9_word_export_not_confirmed",
                "message": "HIL #9:Word 导出需人工确认(非交互式环境,已暂停)"
            }
        user_input = input("  确认导出?(y/N): ").strip().lower()
        proceed = (user_input == 'y')
        if not proceed:
            return {
                "ok": False,
                "blocked": "hil9_word_export_not_confirmed",
                "message": "HIL #9:用户取消 Word 导出"
            }

    # 整合最终版
    full_content = _assemble_full_content(paper_name, state)

    # 保存最终 Markdown(统一路径)
    output_dir = _get_paper_dir(paper_name)
    output_path = os.path.join(output_dir, f"{paper_name}_final.md")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    # 运行 Guardrails 校验(必须在 output_path 定义之后)
    guardrails_result = {}
    try:
        import subprocess
        import json as _json
        result = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "loop_self_check.py"), "--file", output_path, "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            guardrails_result = _json.loads(result.stdout) if result.stdout else {"pass": True}
        else:
            guardrails_result = {"pass": False, "error": result.stderr[:200]}
    except Exception as e:
        guardrails_result = {"pass": False, "error": str(e)}

    state["phase"] = "phase5"
    state["phase5_status"] = "exported"
    state["phase5_guardrails"] = guardrails_result
    state["phase5_output_path"] = output_path
    save_orchestrate_state(paper_name, state)

    msg = f"论文已导出至 {output_path}"
    if guardrails_result.get("pass"):
        msg += "(Guardrails 校验通过 ✅)"
    else:
        msg += "(⚠️ Guardrails 校验未通过,请检查后重新导出)"
    msg += "\n如需 Word 文档,请运行:python3 scripts/md2docx_strict.py " + output_path

    return {
        "ok": True,
        "phase": "phase5",
        "guardrails_pass": guardrails_result.get("pass", False),
        "output_path": output_path,
        "word_count": len(full_content),
        "message": msg,
    }


# ============================================================
# 主入口
# ============================================================

def orchestrate(paper_name: str,
               phase: str = None,
               action: str = None,
               llm_func: Callable[[str], str] = None,
               **kwargs) -> Dict[str, Any]:
    """
    统一入口

    phase:
      None / "auto": 根据当前状态自动判断
      "phase1": 目录确认(Phase 1.2 confirm + Phase 1.3 submit/confirm/skip)
      "phase2": 智能写作
      "phase3": 整合 + 修改 + 输出

    action(可选):
      "phase1_1_init": 解析入口(Phase 1.1,修订 Step 11 - input_type=docx|text)
      "phase1_confirm": 锁定目录结构(Phase 1.2)
      "phase1_3_submit": 提交开题报告做归因(Phase 1.3 提交,docx_path 从 state 读)
      "phase1_3_update_hint": 修改节点 content_hint(Phase 1.3 手动调整)
      "phase1_3_confirm": 确认归因,进入 Phase 2(Phase 1.3 确认)
      "phase1_3_skip": 跳过 Phase 1.3(拍板 #1 禁用)
      "phase3_review": 生成论文供用户预览
      "phase3_feedback": 处理用户修改意见
      "phase3_export": 确认并导出 Word

    llm_func: LLM 调用函数,Phase 1.3 submit / phase3_feedback 需要提供

    kwargs: 额外参数(如 docx_path, node_id, new_hint, feedback, decision 等)
    """
    state = load_orchestrate_state(paper_name)

    if phase is None or phase == "auto":
        if not state:
            phase = "phase1"
            # 如果连 state 都没有且用户提供了 input_data,提示先走 phase1_1_init
            if action is None:
                return {
                    "ok": False,
                    "error": "状态文件不存在。请先调用 phase1_1_init 解析开题报告(docx 或 文本)",
                    "next_action": "phase1_1_init"
                }
        elif not state.get("phase1_confirmed"):
            phase = "phase1"
        elif state["phase"] == "phase1_2":
            # Phase 1.2 确认后 → 归因分析（两步：submit → 确认）
            # run_workflow.py 已在 HIL #1 后显式调用 phase1_3_submit + phase1_3_confirm
            # 此处仅处理路由：pending/submitted → phase1_3, confirmed → phase2
            p13_status = state.get("phase1_3_status")
            if p13_status == "confirmed":
                phase = "phase2"
            else:
                # pending / submitted: 由 run_workflow.py 中的显式调用处理
                # orchestrate() 自身不自动推进，保持 phase1_2
                phase = "phase1_2"
        elif state["phase"] == "phase1":
            # 兼容 v2.0.6 前旧状态（phase = "phase1"）
            p13_status = state.get("phase1_3_status")
            if p13_status == "confirmed":
                phase = "phase2"
            elif p13_status == "submitted":
                phase = "phase1"
            else:
                phase = "phase1"
        else:
            phase = state.get("phase", "phase2")

    if phase == "phase1":
        # Step 11 修订 Phase 1.1 入口
        if action == "phase1_1_init":
            input_type = kwargs.get("input_type")
            input_data = kwargs.get("input_data") or kwargs.get("docx_path") or kwargs.get("outline_text")
            docx_path = kwargs.get("docx_path")
            if not input_type:
                return {"ok": False, "error": "phase1_1_init 需要 input_type(docx 或 text)"}
            if not input_data:
                return {"ok": False, "error": "phase1_1_init 需要 input_data(docx_path 或 outline_text)"}
            return orchestrate_phase1_1(paper_name, input_type, input_data, llm_func, docx_path)
        elif action == "phase1_confirm":
            return confirm_phase1(paper_name)
        elif action == "phase1_3_submit":
            # 修订 11.9:docx_path 从 state 读,不再要求传
            docx_path = kwargs.get("docx_path")  # 可选,仅用于覆盖
            return orchestrate_phase1_3(paper_name, docx_path, llm_func)
        elif action == "phase1_3_update_hint":
            node_id = kwargs.get("node_id")
            new_hint = kwargs.get("new_hint")
            if not node_id or new_hint is None:
                return {"ok": False, "error": "phase1_3_update_hint 需要 node_id 和 new_hint"}
            return update_node_content_hint(paper_name, node_id, new_hint)
        elif action == "phase1_3_confirm":
            return confirm_phase1_3(paper_name)
        elif action == "phase1_3_skip":
            # v2.0.6 P0-1 修复:拍板 #1 强制拦截
            # 入口层禁止 phase1_3_skip;如需跳过,必须走 skip_phase1_3() 显式调用并接受审计
            return {
                "ok": False,
                "error": "拍板 #1 强制:Phase 1.3 不允许跳过。"
                         "请先上传开题报告 docx 或手动录入目录文本(phase1_3_submit)。",
                "blocked_action": "phase1_3_skip",
                "required_action": "phase1_3_submit",
                "retry_options": {
                    "1": "上传开题报告 docx(action=phase1_3_submit, docx_path=...)",
                    "2": "手动录入开题报告文本(action=phase1_3_submit, outline_text=...)",
                    "3": "取消"
                }
            }
        else:
            # 默认:Phase 1.2 提示确认
            return orchestrate_phase1(paper_name, **kwargs)

    elif phase == "phase1_2":
        # phase1_2: 大纲已确认，等归因确认
        # 所有 phase1 action 在此分支均合法（submit/confirm/update_hint）
        if action == "phase1_3_submit":
            docx_path = kwargs.get("docx_path")
            return orchestrate_phase1_3(paper_name, docx_path, llm_func)
        elif action == "phase1_3_confirm":
            return confirm_phase1_3(paper_name)
        elif action == "phase1_3_update_hint":
            node_id = kwargs.get("node_id")
            new_hint = kwargs.get("new_hint")
            if not node_id or new_hint is None:
                return {"ok": False, "error": "phase1_3_update_hint 需要 node_id 和 new_hint"}
            return update_node_content_hint(paper_name, node_id, new_hint)
        elif action == "phase1_3_skip":
            return {
                "ok": False,
                "error": "拍板 #1 强制:Phase 1.3 不允许跳过。",
                "blocked_action": "phase1_3_skip",
                "required_action": "phase1_3_submit"
            }
        else:
            return {
                "ok": False,
                "error": f"phase1_2 状态暂只支持 phase1_3_submit/confirm/update_hint，当前 action={action}"
            }

    elif phase == "phase2":
        if not llm_func:
            return {"ok": False, "error": "phase2 需要提供 llm_func"}
        return orchestrate_phase2(paper_name, llm_func)

    elif phase == "phase3":
        if action == "phase3_feedback":
            return handle_phase3_feedback(paper_name, llm_func=llm_func, **kwargs)
        elif action == "phase3_export":
            # 兼容旧调用:Phase 3 → 自动进入 Phase 3.5/4/5
            return orchestrate_phase3_5(paper_name, llm_func)
        else:
            return orchestrate_phase3(paper_name)

    elif phase == "phase3.5":
        if action == "auto_fix":
            if not llm_func:
                return {"ok": False, "error": "auto_fix 需要 llm_func"}
            return auto_fix_p0_issues(paper_name, llm_func)
        elif action == "rerun":
            return orchestrate_phase3_5(paper_name, llm_func)
        else:
            return orchestrate_phase3_5(paper_name, llm_func)

    elif phase == "phase4":
        return orchestrate_phase4(paper_name, llm_func)

    elif phase == "phase5":
        return orchestrate_phase5(paper_name)

    else:
        return {"ok": False, "error": f"未知阶段: {phase}"}


# ============================================================
# 写作前信息检查(增强项4)
# ============================================================

def check_info_scarcity(paper_name: str, node_id: str) -> Dict[str, Any]:
    """
    写作前信息贫瘠检查(增强项4)。

    检查 2 项核心信息源(拍板标准 A):
      1. content_hint:开题报告提取或用户手写,存于 node.content_hint
      2. bridge:prev_sibling_conclusion / parent_conclusion / prev_chapter_summary 任一非空
    注:user_hints(用户自定义分析维度)为可选增强项,不作为强制检查项。

    拍板标准 A:任一为空 → action="needs_user_input",全部非空 → action="proceed"。

    返回:
      {
        ok: True,
        action: "proceed" | "needs_user_input",
        node_id: str,
        node_title: str,
        current_info: {
          content_hint: str,
          has_bridge: bool,
          bridge_source: str | None  # "prev" | "parent" | "chapter_summary"
        },
        missing_sources: ["content_hint", ...],  # 仅 needs_user_input 时填充
        prompt_options: {                        # 仅 needs_user_input 时填充
          "1": "用户提供 content_hint",
          "2": "AI 自行生成",
          "3": "跳过该节点"
        }
      }
    """
    node = outline_get_node(paper_name, node_id)
    if not node:
        return {"ok": False, "action": "proceed", "error": f"节点不存在: {node_id}"}

    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "action": "proceed", "error": "目录树未初始化"}

    # 特例 0:虚拟摘要节点(is_virtual=True)不写作,跳过 info_scarcity
    if node.get("is_virtual"):
        return {
            "ok": True,
            "action": "proceed",
            "node_id": node_id,
            "node_title": node.get("title", ""),
            "current_info": {"is_virtual": True},
            "missing_sources": [],
            "prompt_options": {},
            "note": "虚拟摘要节点,由系统自动合成,不需要人工写作"
        }

    # 1. content_hint
    content_hint = (node.get("content_hint") or "").strip()

    # 2. bridge
    context = outline_get_context(paper_name, node_id)
    has_prev = bool(context.get("prev_sibling_conclusion"))
    has_parent = bool(context.get("parent_conclusion"))
    has_chapter_summary = bool(
        context.get("prev_chapter_summary", {}).get("key_conclusion")
        if context.get("prev_chapter_summary") else False
    )
    has_bridge = has_prev or has_parent or has_chapter_summary
    bridge_source = (
        "prev" if has_prev else
        "parent" if has_parent else
        "chapter_summary" if has_chapter_summary else None
    )

    # 特例 1:首章 L1(无父、无前置 bridge 是不可能的)
    #   - L1 首章节点(level==1, parent_id==None):bridge 允许空
    #   - 其他节点(含章节首 L2):bridge 仍需检查 P3 fallback
    is_first_chapter_l1 = (
        node.get("level") == 1 and node.get("parent_id") is None
    )
    if is_first_chapter_l1:
        # 首章 L1:仅检查 content_hint(bridge 允许空,user_hints 可选)
        missing = []
        if not content_hint:
            missing.append("content_hint")
        # bridge 缺失是首章 L1 的正常状态,不计入 missing
        # user_hints 是可选增强项,不作为强制检查
    else:
        # 标准 A:content_hint 或 bridge 缺失 → needs_user_input
        missing = []
        if not content_hint:
            missing.append("content_hint")
        if not has_bridge:
            missing.append("bridge")

    current_info = {
        "content_hint": content_hint,
        "has_bridge": has_bridge,
        "bridge_source": bridge_source,
        "is_first_chapter_l1": is_first_chapter_l1
    }

    if missing:
        return {
            "ok": True,
            "action": "needs_user_input",
            "node_id": node_id,
            "node_title": node.get("title", ""),
            "current_info": current_info,
            "missing_sources": missing,
            "prompt_options": {
                "1": "用户提供 content_hint(覆盖写入 node.content_hint)",
                "2": "AI 自行生成(不补充,直接调用 LLM)",
                "3": "跳过该节点(记为 failed,后续手动重试)"
            }
        }

    return {
        "ok": True,
        "action": "proceed",
        "node_id": node_id,
        "node_title": node.get("title", ""),
        "current_info": current_info,
        "missing_sources": [],
        "prompt_options": {}
    }


def apply_user_decision(
    paper_name: str,
    node_id: str,
    decision: str,
    user_hint: str = None
) -> Dict[str, Any]:
    """
    处理 Orchestrator 收到的 user decision(贫瘠节点 3 选项)。

    参数:
      paper_name: 论文名
      node_id: 节点 ID
      decision: "1" (提供 hint) | "2" (AI 自行生成) | "3" (跳过)
      user_hint: 用户提供的新 content_hint(仅 decision=="1" 时使用)

    返回:
      {ok: True, action: "proceed" | "skipped" | "error", ...}
    """
    if decision == "1":
        # 用户提供 content_hint → 写入节点 → 继续写作
        if not user_hint or not user_hint.strip():
            return {"ok": False, "error": "decision='1' 必须提供 user_hint"}
        outline_update_status(
            paper_name, node_id, "pending",
            content_hint=user_hint.strip()
        )
        return {"ok": True, "action": "proceed", "decision": "1"}
    elif decision == "2":
        # AI 自行生成:不写入 hint,继续写作
        return {"ok": True, "action": "proceed", "decision": "2"}
    elif decision == "3":
        # 跳过该节点:记为 failed
        outline_update_status(paper_name, node_id, "failed", retry_count=999)
        return {"ok": True, "action": "skipped", "decision": "3"}
    else:
        return {"ok": False, "error": f"无效 decision: {decision},必须是 '1'/'2'/'3'"}


# ============================================================
# 章节摘要合成(增强项1 - 跨父节点 Bridge)
# ============================================================

def is_last_child_of_chapter(paper_name: str, node_id: str) -> Optional[str]:
    """
    判断 node_id 是否是其所属 L1 章节最后一个已完成的 L2/L3 子节点。

    返回:
      - 章节 ID(如 "ch1")如果是最后一个 → 触发摘要合成
      - None 如果不是

    实现:直接读 outline_state,定位章节 synthesizes 列表,检查是否全部 completed。
    """
    state = outline_load(paper_name)
    if not state:
        return None

    nodes = _get_outline_nodes(state)
    node_map = {n["id"]: n for n in nodes}

    target = node_map.get(node_id)
    if not target or target.get("is_virtual"):
        return None

    # 递归查 L1 父章节
    chapter_id = None
    cur = target
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

    if not chapter_id:
        return None

    # 查该章节的虚拟摘要节点
    summary_id = get_chapter_summary_id(chapter_id)
    summary_node = node_map.get(summary_id)
    if not summary_node:
        return None

    synthesizes = summary_node.get("synthesizes", [])
    if not synthesizes:
        return None

    # 检查 synthesizes 列表是否全部 completed
    all_done = True
    for sid in synthesizes:
        s = node_map.get(sid)
        if not s:
            continue
        if s.get("writing_status") != "completed":
            all_done = False
            break

    return chapter_id if all_done else None


def _build_summary_prompt(chapter_title: str, child_conclusions: List[Dict[str, str]],
                         user_input: str = None) -> str:
    """
    构建 LLM 合成章节摘要的 prompt

    参数:
      chapter_title: 章节标题(如"外部环境分析")
      child_conclusions: [{"id": "3.1", "title": "...", "key_conclusion": "..."}, ...]
      user_input: 用户在 Phase 1.3 填的"本章核心问题"(可选补充)
    """
    child_text = "\n".join([
        f"- [{c['id']}] {c['title']}:{c['key_conclusion']}"
        for c in child_conclusions
    ])

    user_supplement = f"\n\n用户补充视角(本章核心问题):\n{user_input}" if user_input else ""

    return f"""你是一位专业的 MBA 学术论文写作者。

任务:将以下章节的子节点关键结论合成为本章摘要。

章节标题:{chapter_title}

子节点关键结论:
{child_text}
{user_supplement}

要求:
1. 提炼本章核心发现与逻辑主线(不要罗列子节点)
2. 为下一章节提供承接基础
3. 字数严格控制在 200-300 字之间,不要超过 300
4. 输出格式:只输出摘要正文,不要任何标题或前缀

摘要正文:"""


def synthesize_chapter_summary(
    paper_name: str,
    chapter_id: str,
    llm_func: Callable[[str], str],
    user_input: str = None
) -> Dict[str, Any]:
    """
    合成章节摘要。

    触发时机(自动):章节最后一个 L2/L3 子节点写作完成时,由 write_single_node() 回调调用。
    失败处理(拍板要求 #3):LLM 失败 → 返回 action="ask_user",由 Orchestrator 询问用户。

    参数:
      paper_name: 论文名
      chapter_id: 章节 ID(如 "ch1")
      llm_func: LLM 调用函数
      user_input: 用户在 Phase 1.3 填的"本章核心问题"(可选)

    返回:
      {
        ok: bool,
        action: "completed" | "ask_user",   # ask_user 时调用方应询问用户
        summary: str | None,                 # 摘要内容(成功时)
        source: "llm" | "user" | None,      # 摘要来源
        error: str,
        chapter_id: str,
        child_conclusions: list              # ask_user 时附带给 Orchestrator
      }
    """
    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "action": "ask_user", "error": "目录树未初始化"}

    nodes = _get_outline_nodes(state)
    node_map = {n["id"]: n for n in nodes}

    summary_id = get_chapter_summary_id(chapter_id)
    summary_node = node_map.get(summary_id)
    if not summary_node:
        return {"ok": False, "action": "ask_user", "error": f"未找到虚拟摘要节点: {summary_id}"}

    # 收集子节点结论
    child_conclusions = []
    for cid in summary_node.get("synthesizes", []):
        c = node_map.get(cid)
        if c and c.get("key_conclusion"):
            child_conclusions.append({
                "id": cid,
                "title": c.get("title", ""),
                "key_conclusion": c["key_conclusion"]
            })

    if not child_conclusions:
        return {
            "ok": False,
            "action": "ask_user",
            "error": "该章节无可用子节点结论",
            "chapter_id": chapter_id,
            "child_conclusions": []
        }

    summary_text = None
    source = None

    # 路径 1:用户提供摘要
    if user_input:
        summary_text = user_input.strip()
        source = "user"

    # 路径 2:LLM 合成
    if not summary_text:
        prompt = _build_summary_prompt(
            chapter_title=summary_node.get("chapter_title", chapter_id),
            child_conclusions=child_conclusions,
            user_input=user_input
        )
        try:
            response_text = llm_func(prompt)
            summary_text = response_text.strip()
            source = "llm"
        except Exception as e:
            # LLM 失败 → 拍板要求 #3:询问用户
            return {
                "ok": False,
                "action": "ask_user",
                "error": f"LLM 调用失败: {str(e)}",
                "chapter_id": chapter_id,
                "chapter_title": summary_node.get("chapter_title", chapter_id),
                "child_conclusions": child_conclusions
            }

    # 路径 3:超长截断到 300 字以内(保底)
    if summary_text and len(summary_text) > 300:
        summary_text = summary_text[:300]

    # 写入虚拟节点
    outline_update_status(
        paper_name, summary_id, "completed",
        key_conclusion=summary_text,
        word_count=len(summary_text) if summary_text else 0
    )

    return {
        "ok": True,
        "action": "completed",
        "summary": summary_text,
        "source": source,
        "error": "",
        "chapter_id": chapter_id,
        "node_id": summary_id
    }

