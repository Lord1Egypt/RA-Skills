#!/usr/bin/env python3
"""
outline_parser.py - 目录解析器 v2.0.7
基于 v1.2 算法(3样本验证),支持固定规则 + AI兜底 + 手动输入三层解析
v2.0.7 新增: 引擎切换 B(MinerU)→A(heuristic) 单向降级
"""

import re
import os
import shutil
import logging
import docx
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any, Callable
from collections import Counter
from state_manager_v2 import outline_load, _get_state_path, _get_outline_nodes, _set_outline_nodes

logger = logging.getLogger(__name__)

# ============================================================
# v2.0.7 引擎切换状态(F4 进程级 + F5 跨 paper 共享)
# ============================================================
_mineru_check_done = False
_mineru_available = False
_fallback_used = False

# ============================================================
# v2.0.9 向量标题匹配（可选依赖，BGE-small-zh）
# ============================================================
try:
    from simple_embedder import TitleMatcher
    _VECTOR_MATCHER_IMPORTED = True
except ImportError:
    _VECTOR_MATCHER_IMPORTED = False
except Exception:
    _VECTOR_MATCHER_IMPORTED = False

def vector_matcher_available() -> bool:
    """惰性检查向量匹配器是否可用。首次调用时加载模型，后续缓存结果。"""
    if not _VECTOR_MATCHER_IMPORTED:
        return False
    try:
        return TitleMatcher.is_available()
    except Exception:
        return False


def reset_fallback_state():
    """重置模块级状态(测试用 + 进程重启模拟)"""
    global _mineru_check_done, _mineru_available, _fallback_used
    _mineru_check_done = False
    _mineru_available = False
    _fallback_used = False


def _is_mineru_available() -> bool:
    """
    检测 mineru-open-api CLI 是否在 PATH(一次性缓存)
    F4=进程级: 只在第一次调用时检测,后续用缓存值
    """
    global _mineru_check_done, _mineru_available
    if not _mineru_check_done:
        _mineru_available = shutil.which("mineru-open-api") is not None
        _mineru_check_done = True
    return _mineru_available


def _log_fallback_to_audit(from_engine: str, to_engine: str, reason: str, docx_path: str):
    """
    记录降级事件到 stdout + state.audit_log(F2=是)
    F1=否: 不弹窗(不调用 warnings.warn)
    """
    from pathlib import Path
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    # 1. stdout 打印(主流程可捕获)
    print(f"[AUDIT {timestamp}] engine_fallback: {from_engine} -> {to_engine}")
    print(f"           reason: {reason[:200]}")
    print(f"           docx: {docx_path}")

    # 2. 尝试写入 state.audit_log(函数内 import,避免循环依赖 + 方便测试 patch)
    try:
        from state_manager_v2 import load_orchestrate_state, save_orchestrate_state

        # 从 docx_path 推断 paper_name
        # 假设路径是 ~/.openclaw/workspace/{paper_name}/xxx.docx
        try:
            path = Path(docx_path).resolve()
            parts = path.parts
            paper_name = None
            if ".openclaw" in parts and "workspace" in parts:
                idx = parts.index("workspace")
                if idx + 1 < len(parts):
                    paper_name = parts[idx + 1]

            if paper_name:
                state = load_orchestrate_state(paper_name)
                if state:
                    if "audit_log" not in state:
                        state["audit_log"] = []
                    state["audit_log"].append({
                        "action": "outline_engine_fallback",
                        "from_engine": from_engine,
                        "to_engine": to_engine,
                        "reason": reason[:500],
                        "docx_path": docx_path,
                        "timestamp": timestamp
                    })
                    save_orchestrate_state(paper_name, state)
        except Exception:
            # 路径解析或 state 读写失败不阻断主流程
            pass
    except Exception:
        # audit 模块 import 失败也不阻断
        pass


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
OUTLINE_START_ANCHORS = ["论文大纲", "目录", "目  录", "目 录", "4.  论文大纲", "4.论文大纲", "4 论文大纲"]
OUTLINE_END_ANCHOR = "参考文献"

# v2.x.x C 路径: Word 自定义样式（南大 MBA 模板等）
# 这些样式不属于 Word 内置 Heading 1/2/3，但用户用它们写论文标题
# MinerU 不会识别，所以需要 python-docx 直接读
CUSTOM_OUTLINE_STYLES = {
    "l1": ("MBA-章标题", "Heading 1", "Title"),
    "l2": ("MBA-一级节标题", "Heading 2"),
    "l3": ("Heading 3",),
}

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


def _preprocess_paragraphs(paragraphs: List[Tuple[int, str, str]]) -> List[Tuple[int, str, str]]:
    """
    v2.0.7 A 路径: 段落预合并
    合并被 Word/编辑器拆段的章节号。规则:
      - 纯数字 + ".X"    → "N.M"     (如 "1" + ".1 标题")
      - "X.Y" + " 标题"   → "X.Y 标题"  (如 "1.1" + " 标题")
      - "第N章" + "标题"   → "第N章 标题"
      - ".X.Y" + " 标题"   → ".X.Y 标题"
    返回合并后的 paragraphs 列表。
    """
    merged = []
    i = 0
    while i < len(paragraphs):
        idx, style, text = paragraphs[i]
        text = text.strip()

        if not text:
            merged.append((idx, style, text))
            i += 1
            continue

        # 检查是否需要跟下一段合并
        if i + 1 < len(paragraphs):
            next_idx, next_style, next_text = paragraphs[i + 1]
            next_text = next_text.strip()

            # 规则 1: 纯数字 + ".X" 开头(如 "1" + ".1 标题" → "1.1 标题")
            if re.match(r'^\d+$', text) and re.match(r'^\.\d', next_text):
                merged.append((idx, style, f"{text}{next_text}"))
                i += 2
                continue

            # 规则 2: "X.Y" + 后续段(带空格分隔,如 "1.1" + " 标题" → "1.1 标题")
            if re.match(r'^\d+\.\d+$', text) and next_text:
                merged.append((idx, style, f"{text} {next_text}"))
                i += 2
                continue

            # 规则 3: "第N章" + 后续段(中文数字也算,如 "第一章" + "绪论")
            if re.match(r'^第[\d一二三四五六七八九十]+章$', text) and next_text:
                merged.append((idx, style, f"{text} {next_text}"))
                i += 2
                continue

            # 规则 4: ".X.Y" + 后续段(如 ".1.1" + " 标题")
            if re.match(r'^\.\d+\.\d+$', text) and next_text:
                merged.append((idx, style, f"{text}{next_text}"))
                i += 2
                continue

        merged.append((idx, style, text))
        i += 1

    return merged


def extract_outline_from_docx_with_heuristic(docx_path: str) -> Tuple[List[Dict], List[Dict]]:
    """
    v2.0.7 A 路径: python-docx + 启发式预合并
    适用场景: MinerU 不可用 或 已降级。
    """
    paragraphs = extract_text_from_docx(docx_path)
    paragraphs = _preprocess_paragraphs(paragraphs)  # v2.0.7 新增

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


def _strip_markdown_bold(text: str) -> str:
    """
    v2.0.7 新增: 清理 markdown 加粗标记
    MinerU 输出常见格式: "## **第1章 绪论**" → "第1章 绪论"
    同时去除可能的 markdown heading 前缀 "## "、"### " 等
    """
    s = text.strip()
    # 去除 markdown heading 前缀
    s = re.sub(r'^#{1,6}\s*', '', s)
    # 去除加粗标记 **xxx**(保留内容)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    # 去除单星号 *xxx*(如果有)
    s = re.sub(r'\*([^*]+)\*', r'\1', s)
    return s.strip()


def extract_outline_from_docx_via_mineru(
    docx_path: str,
    language: str = "ch",
    timeout: int = 120
) -> Tuple[List[Dict], List[Dict]]:
    """
    v2.0.7 B 路径: 用 MinerU 解析 docx → md → outline
    优点: 保留文档结构,正确识别 heading(不会拆段)
    缺点: ⚠️ 上传 docx 到 MinerU 云端(隐私风险)
    前置: mineru-open-api CLI 已在 PATH
    """
    import subprocess
    import tempfile
    from pathlib import Path

    if not _is_mineru_available():
        raise RuntimeError(
            "mineru-open-api 未安装。请运行: npm install -g mineru-open-api"
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["mineru-open-api", "flash-extract", docx_path,
             "-o", tmpdir, "--language", language],
            capture_output=True, text=True, timeout=timeout
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"mineru-open-api 失败 (code={result.returncode}): {result.stderr[:500]}"
            )

        # 找生成的 md 文件
        md_files = list(Path(tmpdir).rglob("*.md"))
        if not md_files:
            raise RuntimeError(f"MinerU 没生成 md 文件: {tmpdir}")

        md_text = md_files[0].read_text(encoding="utf-8")
        # 用 markdown heading 解析(天然正确)
        return extract_outline_from_text(md_text)


def extract_outline_from_docx_with_custom_styles(docx_path: str) -> Tuple[List[Dict], List[Dict]]:
    """
    v2.x.x C 路径: 读取 Word 自定义样式 (如 MBA-章标题/MBA-一级节标题)
    适用场景: 用户用 Word 自定义样式（非 Heading 1/2/3）写论文标题（如南大 MBA 模板）
    优势: 不依赖 MinerU（避免隐私问题 + 速度问题），不依赖任何 heading 渲染
    """
    paragraphs = extract_text_from_docx(docx_path)

    # 1. 找大纲区起点：用自定义 L1 样式 + 含"论文大纲"/"目录"的段
    start_idx = None
    for i, (_, style, text) in enumerate(paragraphs):
        ts = text.strip()
        if style in CUSTOM_OUTLINE_STYLES["l1"]:
            for anchor in OUTLINE_START_ANCHORS:
                if anchor in ts or ts.endswith(anchor) or ts.replace(" ", "") == anchor.replace(" ", ""):
                    start_idx = i + 1
                    break
        if start_idx is not None:
            break

    if start_idx is None:
        # 没找到自定义样式锚点 → 回退到 heuristic
        return extract_outline_from_docx_with_heuristic(docx_path)

    # 2. 找大纲区终点：含"参考文献"的段
    end_idx = len(paragraphs)
    for i in range(start_idx, len(paragraphs)):
        _, style, text = paragraphs[i]
        ts = text.strip()
        if "参考文献" in ts and (style in CUSTOM_OUTLINE_STYLES["l1"] or style == "Normal" or style == "Title"):
            end_idx = i
            break

    # 3. 收集大纲区内的章节行（L1 + L2/L3 节点）
    #    关键发现：南大 MBA 模板中，"第1章 绪论" 等 L1 标题是 Normal 样式，
    #    不是 MBA-章标题。所以 L1 需要靠文本模式（"第N章 XXX"）识别。
    outline_lines = []
    for i in range(start_idx, end_idx):
        _, style, text = paragraphs[i]
        ts = text.strip()
        if not ts:
            continue
        # 优先级1: L2/L3 样式（南大 MBA-一级节标题 → L2/L3）
        if style in CUSTOM_OUTLINE_STYLES["l2"] or style in CUSTOM_OUTLINE_STYLES["l3"]:
            outline_lines.append(ts)
            continue
        # 优先级2: L1 标题段——但南大模板中 L1 是 Normal 样式，需靠文本模式识别
        if re.match(r'^第[\d一二三四五六七八九十]+章', ts):
            outline_lines.append(ts)
            continue
        # 优先级3: MBA-章标题（防其他模板用）
        if style in CUSTOM_OUTLINE_STYLES["l1"] and not re.match(r'^第[\d一二三四五六七八九十]+章', ts):
            # 避免被 OUTLINE_START_ANCHORS 错误加进去
            continue

    if not outline_lines:
        return extract_outline_from_docx_with_heuristic(docx_path)

    # 4. 用 _parse_outline_lines 解析
    tree, issues = _parse_outline_lines(outline_lines)

    # 5. L1 节点占位处理：开题报告通常没有"绪论"等章节标题
    #    只有当 title 为空时才用 "第N章" 作占位
    for ch in tree:
        if ch.get("level") == 1:
            if not ch.get("title", "").strip():
                # 占位标题（仅当 title 为空时）
                ch["title"] = f"第{ch['num']}章"
                ch["_needs_llm_title"] = True
            else:
                ch["_needs_llm_title"] = False

    return tree, issues


def extract_outline_from_docx(docx_path: str) -> Tuple[List[Dict], List[Dict]]:
    """
    从 docx 文件解析目录
    v2.x.x 统一入口: 根据模块级状态决策调用哪个路径。
    解析路径顺序: C (自定义样式) → B (MinerU) → A (heuristic)
    v2.x.x 新增 C 路径: 修复 MinerU 不识别 Word 自定义样式的问题
    """
    global _fallback_used

    # 情况 1: 优先尝试 C 路径 (自定义样式)
    try:
        tree, issues = extract_outline_from_docx_with_custom_styles(docx_path)
        if tree and len(tree) >= 5:
            return tree, issues
    except Exception as e:
        # C 路径失败，继续尝试其他路径
        pass

    # 情况 2: MinerU 不可用 → 直接 A
    if not _is_mineru_available():
        return extract_outline_from_docx_with_heuristic(docx_path)

    # 情况 3: 已降级过 → 直接 A(不回环)
    if _fallback_used:
        return extract_outline_from_docx_with_heuristic(docx_path)

    # 情况 4: 尝试 MinerU(B 路径)
    try:
        return extract_outline_from_docx_via_mineru(docx_path)

    except KeyboardInterrupt:
        raise

    except Exception as e:
        _fallback_used = True
        _log_fallback_to_audit(
            from_engine="mineru",
            to_engine="heuristic",
            reason=str(e),
            docx_path=docx_path
        )
        return extract_outline_from_docx_with_heuristic(docx_path)


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
        # 中文数字章节号 + 顿号 + 标题（如：一、 研究背景与研究问题）
        (r'^[一二三四五六七八九十\d]+[、\.]\s*([^\n]{2,50})$', 'cn_num'),
        # 带括号的中文数字（如：（一）  研究背景）
        (r'^\（([一二三四五六七八九十\d]+)\）\s*([^\n]{2,50})$', 'cn_paren'),
        # 半角数字编号（如：1.  宏观与技术背景）
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

        # 中文数字编号 + 顿号/点号（如：一、 研究背景，或 1. 宏观与技术背景）
        # → 尝试用 title_text 模糊匹配 node title
        if heading_text not in heading_to_node and pat_type in ('cn_num', 'cn_paren'):
            for node in nodes:
                node_title = node.get("title", "")
                if title_text and (title_text in node_title or node_title in title_text):
                    heading_to_node[heading_text] = node["id"]
                    break

        # 数字编号（1. 宏观与技术背景）→ 直接匹配 node num
        if heading_text not in heading_to_node and pat_type == 'num':
            for node in nodes:
                if str(node.get("num", "")) == num_str:
                    heading_to_node[heading_text] = node["id"]
                    break

    # 第二步：AI 标题匹配（未匹配的标题）
    unmatched_headings = [info for info in heading_info if info["text"] not in heading_to_node]
    ai_heading_matched_count = 0

    if unmatched_headings:
        # ── 2a: 向量标题匹配（确定性 + 毫秒级，v2.0.9 新增）────
        if vector_matcher_available():
            heading_texts = [info["text"] for info in unmatched_headings]
            try:
                matches = TitleMatcher.match_headings(
                    heading_texts, nodes, threshold=0.75
                )
                for node_id, heading_text, score in matches:
                    if node_id in node_map:
                        heading_to_node[heading_text] = node_id
                        ai_heading_matched_count += 1
                        logger.info(
                            "向量匹配: %s → [%s] (score=%.3f)",
                            heading_text, node_id, score,
                        )
            except Exception as e:
                import logging
                _logger = logging.getLogger(__name__)
                _logger.warning(
                    "[TitleMatcher] 向量匹配降级: heading_count=%d, error=%s",
                    len(unmatched_headings), str(e)
                )
                # 继续走到 LLM 兜底逻辑

        # ── 2b: LLM 标题匹配（向量未匹配或无向量依赖时兜底）────
        still_unmatched = [
            info for info in unmatched_headings
            if info["text"] not in heading_to_node
        ]
        if still_unmatched and llm_func:
            heading_texts = [info["text"] for info in still_unmatched]
            ai_results = _llm_match_proposal_headings(heading_texts, nodes, llm_func)

            for i, info in enumerate(still_unmatched):
                if i < len(ai_results):
                    result = ai_results[i]
                    confidence = result.get("confidence", 0.0)
                    node_id = result.get("node_id")

                    if confidence >= confidence_threshold and node_id and node_id in node_map:
                        heading_to_node[info["text"]] = node_id
                        ai_heading_matched_count += 1
                    elif confidence >= 0.5 and node_id and node_id in node_map:
                        # 中等置信度：暂存，后续正文跟随用
                        heading_to_node[info["text"]] = node_id

    # ---- 处理正文段落 ----
    # 修复 P0-1：未匹配标题前的段落默认归到第一个 L1 章节，避免 79 段全 unclassified
    # 找到第一个 L1 节点作为 fallback
    first_l1_id: Optional[str] = None
    for node in nodes:
        if node.get("level") == 1 and not node.get("is_virtual"):
            first_l1_id = node["id"]
            break

    current_node_id: Optional[str] = first_l1_id  # 修复 P0-1：默认归到 ch1
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



def extract_code_name_from_docx(
    docx_path: str,
    llm_func: Callable[[str], str] = None
) -> Dict[str, Any]:
    """
    从开题报告 docx 文件名中提取去标识公司名（如 "A公司"）。

    LLM 直接读文件名，根据论文标题上下文推断出论文用哪个字母代指目标公司。

    参数：
      docx_path: 开题报告 docx 文件路径
      llm_func: LLM 调用函数

    返回：
      {"ok": bool, "code_name": str, "confidence": float}
    """
    import re as re_module
    basename = os.path.basename(docx_path)

    # 兜底：正则直接从文件名提取
    m = re_module.search(r'([A-E])公司', basename)
    if m:
        code_name = m.group(0)  # "A公司"

        # LLM 二次确认（仅在有 llm_func 时）
        if llm_func:
            prompt = f"""以下是一篇MBA论文的文件名，请找出其中用字母代指目标公司的部分（如"A公司"、"B公司"）。

文件名：{basename}

请直接回答：论文中用哪个字母代指目标公司？只回答字母，如"A公司"。"""
            try:
                response = llm_func(prompt).strip()
                confirm_m = re_module.search(r'[A-E]公司', response)
                if confirm_m:
                    code_name = confirm_m.group(0)
                    return {"ok": True, "code_name": code_name, "confidence": 0.95}
            except Exception:
                pass

        return {"ok": True, "code_name": code_name, "confidence": 0.8}

    # 完全兜底：从路径各层级搜索
    for part in basename.split('/'):
        m2 = re_module.search(r'([A-E])公司', part)
        if m2:
            return {"ok": True, "code_name": m2.group(0), "confidence": 0.7}

    return {"ok": False, "code_name": None, "confidence": 0.0}


def extract_keywords_from_docx(
    docx_path: str,
    outline_tree: Dict,
    llm_func: Callable[[str], str] = None,
    max_keywords_per_node: int = 5,
    proposal_result: Dict = None
) -> Dict[str, List[str]]:
    """
    从开题报告 docx 内容 + 大纲标题，为每个章节节点生成检索关键词。

    LLM 读取：
    1. 开题报告全文（提取段落）
    2. 该章节的大纲标题（理解上下文）
    3. 该章节对应的开题报告内容

    输出：该章节的检索关键词列表（最多5个）

    数据流：
      Phase 1.3 归因完成 → extract_keywords_from_docx() 生成各节点 keywords
        → 写入 outline_state 各节点
        → Phase 2 context_builder 读取用于检索

    参数：
      docx_path: 开题报告 docx 文件路径
      outline_tree: outline_parse() 返回的 outline 对象
      llm_func: LLM 调用函数
      max_keywords_per_node: 每个节点最多返回关键词数，默认5
      proposal_result: 可选，已有的 extract_proposal_content 结果（避免重复调用）

    返回：
      {node_id: ["keyword1", "keyword2", ...], ...}
    """
    # 1. 获取所有节点
    try:
        nodes = _get_outline_nodes({"outline": outline_tree})
    except Exception:
        nodes = outline_tree.get("nodes", [])

    # 2. 获取每个节点的内容（复用 extract_proposal_content 结果，避免重复 LLM 调用）
    if proposal_result is None:
        result = extract_proposal_content(docx_path, outline_tree, llm_func=llm_func)
    else:
        result = proposal_result
    node_segments = result.get("node_segments", {})

    node_keywords: Dict[str, List[str]] = {}

    # 4. 对每个有内容的节点，LLM 生成关键词
    for node in nodes:
        node_id = node["id"]
        if node_id.startswith("__"):
            continue

        segments = node_segments.get(node_id, [])
        if not segments:
            node_keywords[node_id] = []
            continue

        # 构建上下文：章节标题 + 内容摘要
        node_title = node.get("title", "")
        content_summary = "。".join([s.strip()[:80] for s in segments[:2]])

        # 父章节标题（用于理解上下文）
        parent_title = ""
        parent_id = node.get("parent_id") or node.get("parent")
        if parent_id:
            parent = next((n for n in nodes if n["id"] == parent_id), None)
            if parent:
                parent_title = parent.get("title", "")

        context = f"论文主题：竞争战略研究\n"
        context += f"上级章节：{parent_title}\n" if parent_title else ""
        context += f"本章标题：{node_title}\n"
        context += f"本章内容摘要：{content_summary}"

        prompt = f"""以下是一篇MBA论文中某一章节的信息，请为该章节生成检索关键词。

{context}

要求：
1. 生成该章节在写作时需要检索的背景信息关键词
2. 关键词应该是具体的、可检索的术语（如公司名、行业词、技术词、战略术语）
3. 最多 {max_keywords_per_node} 个，按重要性排序
4. 只返回关键词列表，每行一个，不要解释

示例输出：
vivo
互联网分发
竞争战略
差异化
生态协同"""

        try:
            if llm_func:
                response = llm_func(prompt).strip()
                # 解析关键词（每行一个，去除空白）
                keywords = [k.strip() for k in response.split("\n") if k.strip()]
                keywords = [k for k in keywords if len(k) > 1][:max_keywords_per_node]
                node_keywords[node_id] = keywords
            else:
                node_keywords[node_id] = []
        except Exception:
            node_keywords[node_id] = []

    return node_keywords



def extract_content_hints(
    docx_path: str,
    outline_tree: Dict,
    llm_func: Callable[[str], str] = None,
    max_hint_chars: int = 150,
    proposal_result: Dict = None
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
      proposal_result: 可选，已有的 extract_proposal_content 结果（避免重复调用）

    返回：
      {node_id: "方向提示文本", ...}
    """
    # 复用 extract_proposal_content 结果（避免重复 LLM 调用）
    if proposal_result is None:
        result = extract_proposal_content(docx_path, outline_tree, llm_func=llm_func)
    else:
        result = proposal_result
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

    # v2.x.x 新增: LLM 兜底 — 一次性补全所有空 hint 节点
    # 背景: 之前只取"开题报告匹配段落"前 60 字作 hint，导致 70%+ 节点没 hint。
    #       Phase 2 写作时 LLM 靠"大纲骨架"勉强写，但容易跑题。
    # 修复: 调一次 LLM，输入所有空 hint 节点 (id + title)，输出 hint 字典。
    # v2.x.x P0 hotfix: 从 docx_path 提取 paper_name，传递动态 paper_subject
    _hint_paper_name = ""
    if docx_path:
        from pathlib import Path as _Path
        _docx_path = _Path(docx_path)
        for _parent in _docx_path.parents:
            _parts = _parent.parts
            if ".openclaw" in _parts and "workspace" in _parts:
                _idx = _parts.index("workspace")
                if _idx + 1 < len(_parts):
                    _hint_paper_name = _parts[_idx + 1]
                    break
    if llm_func:
        content_hints = _llm_fill_empty_hints(
            outline_tree=outline_tree,
            content_hints=content_hints,
            llm_func=llm_func,
            max_hint_chars=max_hint_chars,
            paper_name=_hint_paper_name,
        )

    return content_hints


def _llm_fill_empty_hints(
    outline_tree: Dict,
    content_hints: Dict[str, str],
    llm_func: Callable[[str], str],
    max_hint_chars: int = 150,
    paper_name: str = "",
) -> Dict[str, str]:
    """
    v2.x.x 新增: LLM 一次性兜底补全所有空 hint 节点。

    适用场景:
      - 节点在开题报告里没匹配到段落 (orphan) → extract_content_hints() 跳过了它
      - 需为这些"空 hint 节点"生成方向提示，让 Phase 2 写作时 LLM 有上下文约束

    策略:
      - 收集所有空 hint 节点 (id + title)
      - 调一次 LLM，输入节点列表，要求 JSON 数组返回 hint
      - 解析 + 写回 content_hints

    参数:
      outline_tree: outline_parse() 返回的 outline
      content_hints: 已有的 content_hints 字典
      llm_func: LLM 调用函数
      max_hint_chars: 每个 hint 最大字符数，默认 150
      paper_name: 论文项目名（用于提取 paper_subject；兑底使用）

    返回:
      更新后的 content_hints 字典
    """
    if not llm_func:
        return content_hints

    # 1. 收集空 hint 节点
    try:
        nodes = _get_outline_nodes({"outline": outline_tree})
    except Exception:
        return content_hints

    empty_nodes = []
    for n in nodes:
        if n.get("is_virtual"):
            continue
        node_id = n.get("id", "")
        if not node_id:
            continue
        if content_hints.get(node_id, "").strip():
            continue  # 已有 hint，跳过
        empty_nodes.append({
            "id": node_id,
            "level": n.get("level", 0),
            "title": n.get("title", ""),
        })

    if not empty_nodes:
        return content_hints  # 全部有 hint，无需兜底

    # 2. 构造 prompt
    # v2.x.x P0 修复（v2.1.1-beta.10 硬编码 bug）: 论文主题改为动态提取
    # 背景: 之前硬编码"A公司互联网分发业务竞争战略研究..."，导致所有 v2 用户的
    #       _llm_fill_empty_hints 被错误引导为"终端厂商 + AI 大模型"主题
    # 修复: 从 outline_tree.metadata.paper_title 提取，兑底用 paper_name
    paper_subject = ""
    try:
        paper_subject = (
            outline_tree.get("outline_tree", {}).get("metadata", {}).get("paper_title", "")
            or ""
        ).strip()
    except Exception:
        pass
    if not paper_subject:
        # 兑底：从 paper_name 去后缀
        import re as _re_hint
        paper_subject = _re_hint.sub(r'(_v\d+(?:\.\d+)*|_final|_\d{8}_\d{6})+$', '', paper_name or "").strip() or (paper_name or "本研究")
    nodes_text = "\n".join(
        f"- [{n['id']}] L{n['level']} {n['title']}"
        for n in empty_nodes
    )
    prompt = f"""你是一名学术论文写作助手。基于以下论文的节点列表，**一次性**为每个节点生成一段"写作方向提示"（content_hint），用于 Phase 2 写作时的上下文约束。

论文主题：{paper_subject}

要求：
1. 每个 hint 30-80 字
2. 紧扣节点标题与论文主题，给出具体写作方向（理论框架、关键数据、案例、写作侧重点）
3. 用学术、严谨语气，避免空泛话语
4. 用 JSON 数组格式返回，每个元素包含 `id` 和 `hint` 两个字段

节点列表（{len(empty_nodes)} 个）：
{nodes_text}

返回格式（严格 JSON 数组，不要其他文字、代码块标记、注释）：
[
  {{"id": "1.1", "hint": "..."}},
  {{"id": "1.5", "hint": "..."}}
]"""

    # 3. 调 LLM
    try:
        response = llm_func(prompt)
    except Exception as e:
        # LLM 失败不影响主流程，返回原 content_hints
        return content_hints

    if not response or not isinstance(response, str):
        return content_hints

    # 4. 解析 LLM 输出 — 提取 JSON 数组
    import re as _re
    # 匹配第一个 [] 块（贪婪 or 非贪婪都试）
    json_match = _re.search(r'\[.*\]', response, _re.DOTALL)
    if not json_match:
        return content_hints
    try:
        hints_list = json.loads(json_match.group(0))
    except Exception:
        return content_hints

    if not isinstance(hints_list, list):
        return content_hints

    # 5. 写回 content_hints
    filled = 0
    for item in hints_list:
        if not isinstance(item, dict):
            continue
        nid = str(item.get("id", "")).strip()
        hint = str(item.get("hint", "")).strip()
        if not nid or not hint:
            continue
        # 截断到 max_hint_chars
        if len(hint) > max_hint_chars:
            hint = hint[:max_hint_chars] + "..."
        content_hints[nid] = hint
        filled += 1

    return content_hints


def _extract_keywords_from_hint(hint_text: str) -> List[str]:
    """
    备用：从 content_hint 纯文本提取关键词（Phase 1.3 未调用 LLM 时的兜底）。

    不再使用预定义 pattern 库，改为基于文本特征的简单提取：
    - 连续中文字符串（2-10字）
    - 英文词/缩写
    - 数字+单位组合

    注意：关键词正式生成已迁移到 extract_keywords_from_docx()（Phase 1.3 LLM 生成）。
    此函数仅作为兜底使用。

    参数：
      hint_text: 节点对应的 content_hint 文本

    返回：
      List[str]，最多5个
    """
    if not hint_text:
        return []

    import re as re_module
    keywords = []
    seen = set()

    # 提取中文术语（2-10字的连续中文字符串）
    for m in re_module.finditer(r'[\u4e00-\u9fff]{2,10}', hint_text):
        kw = m.group(0)
        if kw not in seen and len(kw) >= 2:
            seen.add(kw)
            keywords.append(kw)

    # 提取英文词/缩写
    for m in re_module.finditer(r'[A-Za-z]{2,}(?:\s+[A-Za-z]{2,})*', hint_text):
        kw = m.group(0).strip()
        if kw and kw.lower() not in seen:
            seen.add(kw.lower())
            keywords.append(kw)

    return list(set(keywords))[:5]


def save_content_hints_to_outline(paper_name: str, content_hints: Dict[str, str]) -> Dict[str, Any]:
    """
    将 extract_content_hints() 返回的 {node_id: hint_text} 写入 outline_state。
    增强项4 写作前信息检查：content_hint 持久化到 outline_state 节点字段。

    P0 修复：使用 _get_state_path() 计算路径，支持 THESIS_WORKSPACE 环境变量
    P1 修复：使用 _get_outline_nodes() / _set_outline_nodes() 处理嵌套兼容

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

    # P1 修复：使用 helper 多版本兼容读取
    nodes = _get_outline_nodes(state)
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
        # 写入节点 content_hint + research_keywords
        for n in nodes:
            if n["id"] == key:
                n["content_hint"] = hint
                # P0 修复：同时提炼并写入 research_keywords（供 Phase 2 多工具检索使用）
                n["research_keywords"] = _extract_keywords_from_hint(hint)
                written += 1
                break

    # P2-1 fix: 初始化所有节点的 content_hint 字段（无 hint 的节点设为空字符串）
    # P0 修复：同时初始化 research_keywords 字段（无关键词的节点设为空列表）
    # 这样 context_builder 读取时能统一用 .get() 判断
    for n in nodes:
        if "content_hint" not in n:
            n["content_hint"] = ""
        if "research_keywords" not in n:
            n["research_keywords"] = []

    # P1 修复：使用 helper 多版本兼容写回
    _set_outline_nodes(state, nodes)
    state["updated_at"] = datetime.now().isoformat()

    # P0 修复：复用 state_manager_v2 的路径计算（支持 THESIS_WORKSPACE）
    state_path = _get_state_path(paper_name)
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
