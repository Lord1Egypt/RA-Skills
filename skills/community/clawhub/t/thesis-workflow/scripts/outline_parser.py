#!/usr/bin/env python3
"""
outline_parser.py - 目录解析器 v1.0
基于 v1.2 算法(3样本验证),支持固定规则 + AI兜底 + 手动输入三层解析
"""

import re
import os
import docx
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any, Callable
from collections import Counter
from state_manager_v2 import outline_load

# ============================================================
# 固定规则层(v1.2 通用正则,已在3样本验证)
# ============================================================

# 一级章节:第X章 或 第[中文]章(空格容忍0或多个)
CH1_PATTERN = re.compile(r'^\s*第(\d+|[一二三四五六七八九十]+)章\s*(.+)$')

# 二级章节:X.Y(空格容忍0或多个)
CH2_PATTERN = re.compile(r'^\s*(\d+)\.(\d+)\s*(\S.*)$')

# 三级章节:X.Y.Z(空格容忍0或多个)
CH3_PATTERN = re.compile(r'^\s*(\d+)\.(\d+)\.(\d+)\s*(\S.*)$')

# 大纲锚点(起始/终止)
OUTLINE_START_ANCHORS = ["论文大纲", "目录", "目  录", "目 录"]
OUTLINE_END_ANCHOR = "参考文献"

# 中文数字转换
CHINESE_TO_INT = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
}

# 手动输入示例
MANUAL_INPUT_TEMPLATE = """
## 目录结构示例(请按此格式输入)

第1章 绪论
1.1 研究背景
1.1.1 行业背景
1.1.2 研究意义
1.2 研究内容
第2章 理论基础与文献综述
2.1 战略管理理论
2.1.1 企业战略概念
2.1.2 竞争战略理论
2.2 文献综述

(提示:
- 一级标题用"第X章"
- 二级用"X.Y"
- 三级用"X.Y.Z"
- 不要加#号或markdown格式)
"""


def to_int(s: str) -> int:
    """将字符串数字转为int"""
    if s.isdigit():
        return int(s)
    return CHINESE_TO_INT.get(s, 0)


def extract_text_from_docx(docx_path: str) -> List[Tuple[int, str, str]]:
    """
    从 docx 文件读取段落列表
    返回: [(段落索引, 样式名, 文本), ...]
    """
    try:
        doc = docx.Document(docx_path)
        return [(i, p.style.name, p.text) for i, p in enumerate(doc.paragraphs)]
    except Exception:
        # docx 损坏时回退到 XML 直接解析
        import zipfile
        try:
            with zipfile.ZipFile(docx_path, 'r') as z:
                with z.open('word/document.xml') as f:
                    xml_content = f.read().decode('utf-8')
        except Exception:
            return []

        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        root = ET.fromstring(xml_content)
        paragraphs = root.findall('.//w:p', ns)
        result = []
        for i, p in enumerate(paragraphs):
            se = p.find('.//w:pStyle', ns)
            style = se.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if se is not None else 'Normal'
            text = ''.join(x.text or '' for x in p.findall('.//w:t', ns))
            result.append((i, style, text))
        return result


def extract_outline_from_text(text: str) -> Tuple[List[Dict], List[Dict]]:
    """
    从纯文本(粘贴的开题报告内容)中解析目录
    返回: (nodes_list, issues_list)
    """
    lines = text.strip().split('\n')
    return _parse_outline_lines(lines)


def extract_outline_from_docx(docx_path: str) -> Tuple[List[Dict], List[Dict]]:
    """
    从 docx 文件解析目录
    返回: (nodes_list, issues_list)
    """
    paragraphs = extract_text_from_docx(docx_path)

    # 定位大纲区
    start_idx = end_idx = None
    for i, (_, _, t) in enumerate(paragraphs):
        ts = t.strip()
        if start_idx is None and ts in OUTLINE_START_ANCHORS:
            start_idx = i
        elif start_idx is not None and ts == OUTLINE_END_ANCHOR:
            end_idx = i
            break

    if end_idx is None:
        end_idx = len(paragraphs)

    if start_idx is None:
        return [], [{"type": "no_anchor", "message": "未找到大纲锚点(论文大纲/目录)"}]

    # 解析章节
    lines = [p[2].strip() for p in paragraphs[start_idx + 1:end_idx]]
    return _parse_outline_lines(lines)


def _parse_outline_lines(lines: List[str]) -> Tuple[List[Dict], List[Dict]]:
    """
    核心解析逻辑(通用规则)
    返回: (nodes_list, issues_list)
    """
    tree = []
    issues = []

    current_ch1 = None
    current_ch2 = None

    for raw_line in lines:
        # strip 段首段尾空格,处理段首空格
        text = raw_line.strip()
        if not text:
            continue

        m3 = CH3_PATTERN.match(text)
        m2 = CH2_PATTERN.match(text)
        m1 = CH1_PATTERN.match(text)

        if m3:
            # 三级章节
            num = f"{m3.group(1)}.{m3.group(2)}.{m3.group(3)}"
            ch3 = {
                "level": 3,
                "num": num,
                "title": m3.group(4),
                "children": []
            }
            if current_ch2:
                current_ch2["children_ids"].append(num)
                current_ch2["children"].append(ch3)
            else:
                issues.append({
                    "type": "orphan_ch3",
                    "num": num,
                    "title": m3.group(4),
                    "message": f"三级章节 {num} 缺少父级二级章节"
                })
        elif m2:
            # 二级章节
            num = f"{m2.group(1)}.{m2.group(2)}"
            ch2 = {
                "level": 2,
                "num": num,
                "title": m2.group(3),
                "children_ids": [],
                "children": []
            }
            if current_ch1:
                current_ch1["children_ids"].append(num)
                current_ch2 = ch2
                current_ch1["children"].append(ch2)
            else:
                issues.append({
                    "type": "orphan_ch2",
                    "num": num,
                    "title": m2.group(3),
                    "message": f"二级章节 {num} 缺少父级章节"
                })
        elif m1:
            # 一级章节
            ch1_num = to_int(m1.group(1))
            ch1 = {
                "level": 1,
                "num": ch1_num,
                "title": m1.group(2),
                "children_ids": [],
                "children": []
            }
            current_ch1 = ch1
            current_ch2 = None
            tree.append(ch1)

    # 编号唯一性 + 连续性校验(v1.2 新增)
    issues.extend(_validate_numbering(tree))

    return tree, issues


def _validate_numbering(tree: List[Dict]) -> List[Dict]:
    """编号唯一性 + 连续性校验"""
    issues = []

    for ch1 in tree:
        # 一级编号唯一性
        # (tree本身已保证)

        l2_nums = [c["num"] for c in ch1["children"]]
        l2_dupes = [n for n, cnt in Counter(l2_nums).items() if cnt > 1]
        for n in l2_dupes:
            issues.append({
                "type": "L2_duplicate",
                "path": n,
                "chapter": ch1["title"],
                "message": f"二级编号 {n} 在 {ch1['title']} 中重复"
            })

        for ch2 in ch1["children"]:
            l3_nums = [c["num"] for c in ch2["children"]]

            # 三级编号唯一性
            l3_dupes = [n for n, cnt in Counter(l3_nums).items() if cnt > 1]
            for n in l3_dupes:
                issues.append({
                    "type": "L3_duplicate",
                    "path": n,
                    "chapter": ch2["title"],
                    "message": f"三级编号 {n} 在 {ch2['title']} 中重复"
                })

            # 三级编号连续性
            expected = 1
            for ch3 in ch2["children"]:
                actual = int(ch3["num"].split('.')[-1])
                if actual != expected:
                    issues.append({
                        "type": "L3_not_continuous",
                        "actual": ch3["num"],
                        "expected": f"{ch2['num']}.{expected}",
                        "title": ch3["title"],
                        "message": f"三级编号 {ch3['num']} 不连续,期望 {ch2['num']}.{expected}"
                    })
                expected = actual + 1

    return issues


def build_outline_tree(tree: List[Dict], paper_title: str = None) -> Dict[str, Any]:
    """
    将嵌套树结构转为标准目录树JSON(含metadata和nodes_flatten)
    """
    nodes_flatten = []
    total_l1 = len(tree)
    total_l2 = sum(len(c["children"]) for c in tree)
    total_l3 = sum(len(c2["children"]) for c in tree for c2 in c["children"])

    def node_id(ch1_idx, ch2=None, ch3=None):
        if ch3:
            return ch3["num"]
        if ch2:
            return ch2["num"]
        return f"ch{ch1_idx + 1}"

    # 扁平化 + 构建兄弟关系
    # 分层追踪：每层独立管理 prev，不跨层级污染
    prev_ch1_id = None
    for i, ch1 in enumerate(tree):
        nid = f"ch{i + 1}"
        nodes_flatten.append({
            "id": nid,
            "level": 1,
            "num": ch1["num"],
            "title": ch1["title"],
            "parent_id": None,
            "children_ids": ch1["children_ids"],
            "prev_sibling_id": prev_ch1_id,
            "next_sibling_id": None,
            "writing_status": "pending",
            "key_conclusion": None,
            "word_count": None
        })
        if prev_ch1_id:
            # 更新前一 ch1 的 next_sibling_id
            for n in reversed(nodes_flatten[:-1]):
                if n["id"] == prev_ch1_id:
                    n["next_sibling_id"] = nid
                    break
        prev_ch1_id = nid

        prev_l2_id = None
        for j, ch2 in enumerate(ch1["children"]):
            nid2 = ch2["num"]
            nodes_flatten.append({
                "id": nid2,
                "level": 2,
                "num": ch2["num"],
                "title": ch2["title"],
                "parent_id": f"ch{i + 1}",
                "children_ids": ch2["children_ids"],
                "prev_sibling_id": prev_l2_id,
                "next_sibling_id": None,
                "writing_status": "pending",
                "key_conclusion": None,
                "word_count": None
            })
            if prev_l2_id:
                for n in reversed(nodes_flatten[:-1]):
                    if n["id"] == prev_l2_id:
                        n["next_sibling_id"] = nid2
                        break
            prev_l2_id = nid2

            prev_l3_id = None
            for k, ch3 in enumerate(ch2["children"]):
                nid3 = ch3["num"]
                nodes_flatten.append({
                    "id": nid3,
                    "level": 3,
                    "num": ch3["num"],
                    "title": ch3["title"],
                    "parent_id": nid2,
                    "children_ids": [],
                    "prev_sibling_id": prev_l3_id,
                    "next_sibling_id": None,
                    "writing_status": "pending",
                    "key_conclusion": None,
                    "word_count": None
                })
                if prev_l3_id:
                    for n in reversed(nodes_flatten[:-1]):
                        if n["id"] == prev_l3_id:
                            n["next_sibling_id"] = nid3
                            break
                prev_l3_id = nid3

    return {
        "outline_tree": {
            "metadata": {
                "paper_title": paper_title,
                "total_l1": total_l1,
                "total_l2": total_l2,
                "total_l3": total_l3,
                "total_nodes": len(nodes_flatten),
                "created_at": None
            },
            "nodes": nodes_flatten
        }
    }


def outline_parse(text_or_docx: str, paper_title: str = None) -> Dict[str, Any]:
    """
    主入口:解析目录(文本或docx路径)
    返回标准目录树JSON

    解析失败返回: {"ok": False, "error": "...", "suggestion": "..."}
    """
    # 判断输入类型
    is_file = text_or_docx.strip().endswith('.docx') or \
              (len(text_or_docx) < 200 and text_or_docx.startswith('/'))

    if is_file:
        tree, issues = extract_outline_from_docx(text_or_docx)
    else:
        tree, issues = extract_outline_from_text(text_or_docx)

    if not tree:
        return {
            "ok": False,
            "error": "未解析到任何章节",
            "suggestion": MANUAL_INPUT_TEMPLATE
        }

    outline = build_outline_tree(tree, paper_title)

    return {
        "ok": True,
        "outline": outline,
        "issues": issues,
        "summary": {
            "l1": outline["outline_tree"]["metadata"]["total_l1"],
            "l2": outline["outline_tree"]["metadata"]["total_l2"],
            "l3": outline["outline_tree"]["metadata"]["total_l3"],
            "total": outline["outline_tree"]["metadata"]["total_nodes"]
        }
    }


def validate_manual_input(text: str) -> Dict[str, Any]:
    """
    验证用户手动输入的目录文本
    成功返回: {"ok": True, "outline": {...}}
    失败返回: {"ok": False, "error": "..."}
    """
    if not text or len(text.strip()) < 50:
        return {
            "ok": False,
            "error": "输入内容太少,至少需要包含完整的目录结构"
        }

    tree, issues = extract_outline_from_text(text)

    if not tree:
        error_msg = "未识别到任何章节,请检查格式是否正确"
        if issues:
            error_msg = issues[0].get("message", error_msg)
        return {
            "ok": False,
            "error": error_msg,
            "suggestion": MANUAL_INPUT_TEMPLATE
        }

    # 基本校验
    if len(tree) < 5:
        return {
            "ok": False,
            "error": f"章节数量太少({len(tree)}章),至少需要5章,请检查输入是否完整"
        }

    # 有严重问题(编号重复)但有内容
    critical_issues = [i for i in issues if i.get("type") in ["L2_duplicate"]]
    if critical_issues:
        return {
            "ok": False,
            "error": f"发现编号重复问题:{critical_issues[0]['message']}",
            "suggestion": MANUAL_INPUT_TEMPLATE
        }

    outline = build_outline_tree(tree)
    return {
        "ok": True,
        "outline": outline,
        "issues": issues
    }


# ============================================================
# 开题报告内容提取与归因
# ============================================================

def _llm_match_proposal_headings(
    headings: List[str],
    nodes: List[Dict],
    llm_func: Callable[[str], str]
) -> List[Dict[str, Any]]:
    """
    用 AI 匹配开题报告标题到目录节点（第一层 AI 归因）

    输入：开题报告标题列表 + 目录节点列表
    输出：每个标题的匹配结果

    返回格式：
    [
        {
            "heading": "1.4 研究思路与方法",
            "node_id": "1.3",   # 匹配的节点ID
            "confidence": 0.85,  # 置信度
            "reason": "1.4是1.3的补充，具体内容属于研究思路范畴"
        },
        ...
    ]
    """
    if not headings or not llm_func:
        return []

    # 构建节点上下文
    node_context = []
    for n in nodes:
        indent = "  " * (n.get("level", 1) - 1)
        node_context.append(f"{indent}- [{n['id']}] {n.get('title', '')} (级别 {n.get('level', '')})")

    headings_text = "\n".join([f"[{i}] {h}" for i, h in enumerate(headings)])

    prompt = f"""你是一个学术论文结构分析助手。
你的任务：将开题报告中的每个章节标题，匹配到论文目录的对应节点。

## 论文目录节点
{chr(10).join(node_context)}

## 开题报告标题（需匹配到目录节点）
{headings_text}

## 匹配规则
1. 根据标题语义，找到最匹配的目录节点
2. 标题与目录节点标题可能存在措辞差异（如"1.4 研究思路"→"1.3 研究目的与意义"），根据语义判断
3. 如果某标题在目录中找不到合适的匹配节点，返回 node_id=null（该标题不归入任何节点）
4. 置信度 0-1：高度确定 0.85+，较有把握 0.7-0.85，不确定 0.5-0.7，匹配不上 <0.5

## 输出格式（JSON数组）
[{{"idx": 0, "node_id": "1.3", "confidence": 0.8, "reason": "..."}}, ...]

只输出 JSON 数组，不要有其他内容。"""

    try:
        response = llm_func(prompt)
        import json, re
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception:
        pass

    return [{"idx": i, "node_id": None, "confidence": 0.0, "reason": "LLM调用失败"} for i in range(len(headings))]


def _llm_semantic_classify(
    segments: List[str],
    nodes: List[Dict],
    llm_func: Callable[[str], str]
) -> List[Dict[str, Any]]:
    """
    用 AI 语义识别段落归属（第二层归因）

    输入：未归因的段落列表 + 目录节点列表
    输出：每个段落的分类结果

    返回格式：
    [
        {
            "segment": "段落文本",
            "node_id": "最匹配的节点ID" 或 null（游离）,
            "confidence": 置信度 0-1,
            "reason": "判断理由"
        },
        ...
    ]
    """
    if not segments or not llm_func:
        return []

    # 构建节点上下文
    node_context = []
    for n in nodes:
        node_context.append(f"  - {n['id']}: {n.get('title', '')} (num={n.get('num', '')}, level={n.get('level', '')}")

    segments_text = "\n".join([f"[{i}] {s}" for i, s in enumerate(segments)])

    prompt = f"""你是一个学术论文结构分析助手。你的任务是根据目录节点，判断每个段落属于哪个节点。

## 目录节点
{chr(10).join(node_context)}

## 待分类段落
{segments_text}

## 判断规则
1. 分析每个段落的语义内容，判断它最匹配哪个目录节点
2. 如果段落与某个节点的主题高度相关，归入该节点
3. 如果段落是过渡性文字、背景介绍且无法判断归属，归入 null（游离）
4. 给出每个段落的置信度（0-1）：高度确定 0.9+，较有把握 0.7-0.9，不确定 0.5-0.7，完全无法判断 <0.5

## 输出格式（JSON数组）
[{{"idx": 0, "node_id": "1.1", "confidence": 0.85, "reason": "..."}}, ...]

只输出 JSON，不要有其他内容。"""

    try:
        response = llm_func(prompt)
        import json, re
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception:
        pass

    return [{"idx": i, "node_id": None, "confidence": 0.0, "reason": "LLM调用失败"} for i in range(len(segments))]


def extract_proposal_content(
    docx_path: str,
    outline_tree: Dict,
    llm_func: Callable[[str], str] = None,
    confidence_threshold: float = 0.7
) -> Dict[str, Any]:
    """
    从开题报告 docx 中提取正文内容，并归因到目录节点

    归因策略（三层）：
      1. 固定规则层：精确匹配开题报告标题 → 目录节点
      2. AI 标题匹配层：LLM 匹配剩余标题 → 节点（llm_func 提供）
      3. AI 语义层：无法匹配标题的正文段落 → 节点

    参数：
      docx_path: 开题报告 docx 文件路径
      outline_tree: outline_parse() 返回的 outline 对象
      llm_func: LLM 调用函数（标题匹配 + 语义归因）
      confidence_threshold: AI 置信度阈值，默认 0.7

    返回：
      {
        ok: bool,
        node_segments: {node_id: ["段落1", "段落2"]},
        orphan_segments: ["段落1", "段落2"],
        undecided_segments: [("段落", {"candidates": [("node_id", score), ...]})],
        total_paragraphs: int,
        matched_paragraphs: int,  # 固定规则层
        ai_heading_matched: int,  # AI 标题匹配层
        ai_classified: int        # AI 语义层
      }
    """
    import re

    # 获取所有段落
    paragraphs = extract_text_from_docx(docx_path)
    if not paragraphs:
        return {
            "ok": False,
            "error": "无法读取 docx 内容",
            "node_segments": {},
            "orphan_segments": [],
            "undecided_segments": [],
            "total_paragraphs": 0,
            "matched_paragraphs": 0,
            "ai_heading_matched": 0,
            "ai_classified": 0
        }

    # 获取所有节点
    nodes = outline_tree.get("outline_tree", {}).get("nodes", [])
    node_map = {n["id"]: n for n in nodes}

    # 构建 node_id → paragraphs 映射
    node_segments: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    orphan_segments: List[str] = []
    undecided_segments: List[Tuple[str, Dict]] = []

    # 章节标题模式
    heading_patterns = [
        (r'^第([一二三四五六七八九十\d]+)章\s*([^\n]{0,50})$', 'ch'),
        (r'^(\d+(?:\.\d+){1,2})\s+([^\n]{2,50})$', 'num'),
    ]

    # ---- 提取所有标题段落 ----
    proposal_headings: List[str] = []
    heading_info: List[Dict] = []  # {idx, text, num_str, title_text, pat_type}

    for idx, style, text in paragraphs:
        text = text.strip()
        if not text or len(text) < 5:
            continue

        for pat_regex, pat_type in heading_patterns:
            m = re.match(pat_regex, text)
            if m:
                if len(text) > 35:  # 真标题判断
                    continue
                num_str = m.group(1) if m.lastindex >= 1 else ""
                title_text = m.group(2).strip() if m.lastindex >= 2 else ""
                proposal_headings.append(text)
                heading_info.append({
                    "idx": idx,
                    "text": text,
                    "num_str": num_str,
                    "title_text": title_text,
                    "pat_type": pat_type
                })
                break

    # ---- 建立标题 → node_id 映射 ----
    # 第一步：固定规则精确匹配
    heading_to_node: Dict[str, str] = {}  # heading_text → node_id

    for info in heading_info:
        title_text = info["title_text"]
        pat_type = info["pat_type"]
        num_str = info["num_str"]
        heading_text = info["text"]

        for node in nodes:
            node_title = node.get("title", "")
            # 精确匹配标题
            if title_text and title_text == node_title:
                heading_to_node[heading_text] = node["id"]
                break

        # L1 中文数字章节（"第一章" → ch1）
        if heading_text not in heading_to_node and pat_type == 'ch':
            cn_map = {"一":"1","二":"2","三":"3","四":"4","五":"5",
                      "六":"6","七":"7","八":"8","九":"9","十":"10"}
            norm_num = cn_map.get(num_str, num_str)
            for node in nodes:
                if str(node.get("num", "")) == norm_num and node.get("level") == 1:
                    heading_to_node[heading_text] = node["id"]
                    break

    # 第二步：AI 标题匹配（未匹配的标题）
    unmatched_headings = [info for info in heading_info if info["text"] not in heading_to_node]
    ai_heading_matched_count = 0

    if unmatched_headings and llm_func:
        heading_texts = [info["text"] for info in unmatched_headings]
        ai_results = _llm_match_proposal_headings(heading_texts, nodes, llm_func)

        for i, info in enumerate(unmatched_headings):
            if i < len(ai_results):
                result = ai_results[i]
                confidence = result.get("confidence", 0.0)
                node_id = result.get("node_id")

                if confidence >= confidence_threshold and node_id and node_id in node_map:
                    heading_to_node[info["text"]] = node_id
                    ai_heading_matched_count += 1
                elif confidence >= 0.5 and node_id and node_id in node_map:
                    # 中等置信度：记录但不自动归入（正文跟随时特殊处理）
                    heading_to_node[info["text"]] = node_id  # 暂存，后续正文用
                # 低置信度：不归入，正文全部游离

    # ---- 处理正文段落 ----
    current_node_id: Optional[str] = None
    current_paragraphs: List[str] = []
    matched_count = 0
    unclassified: List[Tuple[int, str]] = []

    for idx, style, text in paragraphs:
        text = text.strip()
        if not text or len(text) < 5:
            continue

        # 检测是否为标题
        is_heading = False
        new_node_id: Optional[str] = None

        for pat_regex, pat_type in heading_patterns:
            m = re.match(pat_regex, text)
            if m:
                if len(text) > 35:
                    continue
                is_heading = True
                new_node_id = heading_to_node.get(text)  # 从映射表查找
                break

        if is_heading and new_node_id:
            # 保存上一个节点的内容
            if current_node_id and current_paragraphs:
                node_segments[current_node_id].extend(current_paragraphs)
                matched_count += len(current_paragraphs)

            current_node_id = new_node_id
            current_paragraphs = []
        elif current_node_id:
            current_paragraphs.append(text)
        else:
            unclassified.append((idx, text))

    # 保存最后一个节点
    if current_node_id and current_paragraphs:
        node_segments[current_node_id].extend(current_paragraphs)
        matched_count += len(current_paragraphs)

    # ---- AI 语义归因（未匹配标题的正文段落）----
    ai_classified_count = 0
    if unclassified and llm_func:
        unclassified_texts = [t for _, t in unclassified]
        ai_results = _llm_semantic_classify(unclassified_texts, nodes, llm_func)

        for i, (idx, text) in enumerate(unclassified):
            if i < len(ai_results):
                result = ai_results[i]
                confidence = result.get("confidence", 0.0)
                node_id = result.get("node_id")

                if confidence >= confidence_threshold and node_id and node_id in node_map:
                    node_segments[node_id].append(text)
                    ai_classified_count += 1
                elif confidence >= 0.5 and node_id and node_id in node_map:
                    undecided_segments.append((text, {
                        "candidates": [(node_id, confidence)],
                        "reason": result.get("reason", "")
                    }))
                else:
                    orphan_segments.append(text)
    else:
        for _, text in unclassified:
            orphan_segments.append(text)

    # 统计
    total = len([p for _, _, p in paragraphs if p.strip()])

    return {
        "ok": True,
        "node_segments": node_segments,
        "orphan_segments": orphan_segments,
        "undecided_segments": undecided_segments,
        "total_paragraphs": total,
        "matched_paragraphs": matched_count,
        "ai_heading_matched": ai_heading_matched_count,
        "ai_classified": ai_classified_count
    }


def extract_content_hints(
    docx_path: str,
    outline_tree: Dict,
    llm_func: Callable[[str], str] = None,
    max_hint_chars: int = 150
) -> Dict[str, str]:
    """
    从开题报告 docx 中提取每个节点的方向提示（content_hint）

    使用 extract_proposal_content() 的结果：
    - 每个节点的 node_segments 就是该节点在开题报告中的内容
    - 取前 1-2 个段落，每段取前 60 字作为提示

    参数：
      docx_path: 开题报告 docx 文件路径
      outline_tree: outline_parse() 返回的 outline 对象
      llm_func: LLM 调用函数（传入 extract_proposal_content）
      max_hint_chars: 每个 hint 的最大字符数，默认 150

    返回：
      {node_id: "方向提示文本", ...}
    """
    # 调用 extract_proposal_content 获取每个节点的内容
    result = extract_proposal_content(docx_path, outline_tree, llm_func=llm_func)
    if not result.get("ok"):
        return {}

    content_hints: Dict[str, str] = {}

    for node_id, segments in result["node_segments"].items():
        if not segments:
            continue

        # 取前 2 个段落作为 hint
        hint_parts = []
        for seg in segments[:2]:
            # 取前 60 字，去除多余空白
            hint = seg.strip()[:60]
            if hint:
                hint_parts.append(hint)

        if hint_parts:
            full_hint = "。".join(hint_parts)
            # 截断到 max_hint_chars
            if len(full_hint) > max_hint_chars:
                full_hint = full_hint[:max_hint_chars] + "..."
            content_hints[node_id] = full_hint

    # 孤儿段落不归入任何节点，但整体孤儿数量可作为参考
    if result.get("orphan_segments"):
        orphan_count = len(result["orphan_segments"])
        # 存入 special key
        content_hints["__orphan_count__"] = str(orphan_count)

    return content_hints


def save_content_hints_to_outline(paper_name: str, content_hints: Dict[str, str]) -> Dict[str, Any]:
    """
    将 extract_content_hints() 返回的 {node_id: hint_text} 写入 outline_state。
    增强项4 写作前信息检查：content_hint 持久化到 outline_state 节点字段。

    逻辑：
      - 对每个节点的 content_hint 字段写入（如果已有则覆盖）
      - __orphan_count__ 等特殊 key 跳过（不入节点）
      - 返回写入统计

    参数：
      paper_name: 论文名
      content_hints: {node_id: hint_text}

    返回：
      {
        ok: bool,
        written: int,        # 实际写入节点数
        skipped: int,        # 跳过的特殊 key 数
        error: str
      }
    """
    state = outline_load(paper_name)
    if not state:
        return {"ok": False, "written": 0, "skipped": 0, "error": "目录树未初始化"}

    nodes = state["outline"]["outline_tree"]["nodes"]
    node_ids = {n["id"] for n in nodes}

    written = 0
    skipped = 0

    for key, hint in content_hints.items():
        # 跳过特殊 key（如 __orphan_count__）
        if key.startswith("__"):
            skipped += 1
            continue
        # 节点不存在时跳过
        if key not in node_ids:
            skipped += 1
            continue
        # 写入节点 content_hint
        for n in nodes:
            if n["id"] == key:
                n["content_hint"] = hint
                written += 1
                break

    state["outline"]["outline_tree"]["nodes"] = nodes
    state["updated_at"] = datetime.now().isoformat()

    state_path = os.path.join(
        os.path.expanduser("~/.openclaw/workspace"),
        paper_name,
        "_outline_state.json"
    )
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    return {
        "ok": True,
        "written": written,
        "skipped": skipped,
        "error": ""
    }


# ============================================================
# 章节摘要节点插入（增强项1 — 跨父节点 Bridge）
# ============================================================

def insert_chapter_summary_nodes(outline: Dict[str, Any]) -> Dict[str, Any]:
    """
    在每个 L1 章节末尾插入虚拟章节摘要节点 __ch{N}_summary__

    设计目的（增强项1 跨父节点 Bridge）：
      - 解决 "2.1 找不到 1.2 key_conclusion" 的 bridge 断裂问题
      - 每个章节末尾自动生成虚拟摘要节点
      - 该节点吸收本章所有 L2/L3 的 key_conclusion
      - 下一章节的 bridge 可引用前一章节的摘要节点（P3 fallback）

    输入: build_outline_tree() 返回的 outline 对象
    输出: 插入了虚拟节点的新 outline 对象（不修改原节点）

    节点结构:
      {
        "id": "__ch{N}_summary__",
        "level": 1,
        "title": "{章节标题} - 本章小结",
        "is_virtual": True,
        "type": "chapter_summary",
        "synthesizes": ["1.1", "1.2", "1.3"],   # 待汇总的子节点 ID
        "chapter_id": "ch1",
        "chapter_title": "绪论",
        "key_conclusion": None,   # 由 synthesize_chapter_summary() 填充
        "writing_status": "pending"
      }

    注意:
      - 虚拟节点不参与 prev/next sibling 关系（仍标记 None）
      - 虚拟节点的 writing_status 始终为 pending（不会被 NodeWriter 写作）
      - 已包含虚拟节点时直接跳过（幂等）
    """
    if not outline or "outline_tree" not in outline:
        return outline

    nodes = outline["outline_tree"].get("nodes", [])
    if not nodes:
        return outline

    # 幂等检查：若已存在虚拟节点，跳过
    if any(n.get("is_virtual") for n in nodes):
        return outline

    # 按 L1 章节分组（保留原始顺序）
    chapters = []  # [{"id": ..., "title": ..., "nodes": [...]}]
    current_ch = None

    for node in nodes:
        if node["level"] == 1 and not node.get("is_virtual"):
            # 新章节开始
            if current_ch is not None:
                chapters.append(current_ch)
            current_ch = {
                "id": node["id"],
                "title": node["title"],
                "nodes": [node]
            }
        elif current_ch is not None:
            current_ch["nodes"].append(node)

    # 收尾最后一章
    if current_ch is not None:
        chapters.append(current_ch)

    # 生成新 nodes 列表：原节点 + 末尾虚拟摘要节点
    new_nodes = []
    for ch in chapters:
        # 添加章节所有原始节点
        new_nodes.extend(ch["nodes"])

        # 获取该章节的子节点 ID（L2/L3）
        child_ids = [
            n["id"] for n in ch["nodes"]
            if n.get("level") in [2, 3] and not n.get("is_virtual")
        ]

        # 章节序号（ch1 -> 1, ch2 -> 2...）
        ch_id_raw = ch["id"]
        if ch_id_raw.startswith("ch"):
            ch_num = ch_id_raw[2:]
        else:
            ch_num = ch_id_raw

        # 虚拟摘要节点
        summary_node = {
            "id": f"__ch{ch_num}_summary__",
            "level": 1,
            "num": None,
            "title": f"{ch['title']} — 本章小结",
            "parent_id": None,
            "children_ids": [],
            "prev_sibling_id": None,
            "next_sibling_id": None,
            "writing_status": "pending",
            "key_conclusion": None,
            "word_count": None,
            "is_virtual": True,
            "type": "chapter_summary",
            "synthesizes": child_ids,
            "chapter_id": ch["id"],
            "chapter_title": ch["title"]
        }
        new_nodes.append(summary_node)

    # 更新 outline
    outline["outline_tree"]["nodes"] = new_nodes
    metadata = outline["outline_tree"].get("metadata", {})
    metadata["total_nodes"] = len(new_nodes)
    metadata["virtual_nodes"] = sum(1 for n in new_nodes if n.get("is_virtual"))
    metadata["real_nodes"] = sum(1 for n in new_nodes if not n.get("is_virtual"))
    outline["outline_tree"]["metadata"] = metadata

    return outline


def get_chapter_summary_id(chapter_id: str) -> str:
    """
    根据 L1 章节 ID 生成虚拟摘要节点 ID
    例如: ch1 -> __ch1_summary__, ch5 -> __ch5_summary__
    """
    if chapter_id.startswith("ch"):
        ch_num = chapter_id[2:]
    else:
        ch_num = chapter_id
    return f"__ch{ch_num}_summary__"


def get_chapter_id_from_summary(summary_node_id: str) -> Optional[str]:
    """
    根据虚拟摘要节点 ID 反查章节 ID
    例如: __ch1_summary__ -> ch1
    """
    if not summary_node_id or not isinstance(summary_node_id, str):
        return None
    if not summary_node_id.startswith("__ch") or not summary_node_id.endswith("_summary__"):
        return None
    middle = summary_node_id[4:-10]  # 去掉前缀 __ch 和后缀 _summary__
    if not middle or not middle.isdigit():
        return None
    return f"ch{middle}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 outline_parser.py <开题报告.docx 或 目录文本>")
        print("")
        print("测试样例:")
        print("  python3 outline_parser.py '/path/to/开题报告.docx'")
        print("  echo '第1章 绪论\\n1.1 研究背景' | python3 outline_parser.py")
        sys.exit(1)

    input_arg = sys.argv[1]
    result = outline_parse(input_arg)

    print(json.dumps(result, ensure_ascii=False, indent=2))
