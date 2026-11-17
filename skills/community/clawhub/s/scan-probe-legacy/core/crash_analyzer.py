# -*- coding: utf-8 -*-
"""F8: 报错修复

分析MC崩溃报告(crash report)和日志文件(latest.log)，
自动识别错误模式，给出中文诊断和修复建议。

使用方式:
    from core.crash_analyzer import run
    import argparse
    args = argparse.Namespace(crash_log="crash-xxx.txt", launcher="pcl2", mc_version="1.21.1")
    result = run(args)
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import ReportGenerator

logger = get_logger("crash_analyzer")

# === 日志文件最大读取行数 ===
MAX_LOG_LINES = 5000

# === 崩溃报告关键段落正则 ===
CRASH_SECTION_PATTERNS = {
    "description": re.compile(r"^--+ *Description *--+", re.IGNORECASE),
    "system_details": re.compile(r"^--+ *System Details *--+", re.IGNORECASE),
    "mod_list": re.compile(r"^--+ *Loaded Modules? *--+", re.IGNORECASE),
    "stacktrace": re.compile(r"^--+ *Stack trace *--+", re.IGNORECASE),
    "head": re.compile(r"^--+ *Head *--+", re.IGNORECASE),
    "affected_level": re.compile(r"^--+ *Affected level *--+", re.IGNORECASE),
}


def _read_log_file(file_path: Path) -> str:
    """读取日志文件内容（自动处理编码）"""
    encodings = ["utf-8", "gbk", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                lines = f.readlines()
                # 限制行数
                if len(lines) > MAX_LOG_LINES:
                    logger.warning(
                        f"日志文件过大({len(lines)}行)，仅读取最后{MAX_LOG_LINES}行"
                    )
                    lines = lines[-MAX_LOG_LINES:]
                return "".join(lines)
        except UnicodeDecodeError:
            continue
    # 最后尝试忽略错误
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _detect_file_type(content: str, filename: str) -> str:
    """判断文件类型: crash_report / latest_log / other"""
    lower_name = filename.lower()

    if "crash" in lower_name and (lower_name.endswith(".txt") or lower_name.endswith(".log")):
        return "crash_report"

    if "latest" in lower_name and lower_name.endswith(".log"):
        return "latest_log"

    # 通过内容判断
    if "---- Minecraft Crash Report ----" in content:
        return "crash_report"

    if "Stopping!" in content and "Starting minecraft" in content:
        return "latest_log"

    # 检查是否包含Java异常
    if re.search(r"(Exception|Error|Caused by|at \w+\.\w+)", content):
        return "latest_log"

    return "other"


def _extract_crash_info(content: str) -> Dict[str, Any]:
    """从崩溃报告中提取关键信息（含模组版本）"""
    info = {
        "description": "",
        "game_version": "",
        "loader": "",
        "mod_count": 0,
        "mods": [],
        "mod_versions": {},  # mod_id -> version字符串
        "stacktrace": "",
        "head_section": "",
    }

    # 提取描述
    desc_match = re.search(
        r"Description:\s*(.+?)(?=----|\Z)", content, re.DOTALL
    )
    if desc_match:
        info["description"] = desc_match.group(1).strip()[:500]

    # 提取游戏版本
    version_match = re.search(
        r"Minecraft Version[:\s]+([\d.]+)", content
    )
    if version_match:
        info["game_version"] = version_match.group(1)

    # 提取加载器
    if "NeoForge" in content or "neoforge" in content:
        info["loader"] = "neoforge"
    elif "Fabric" in content:
        info["loader"] = "fabric"
    elif "Forge" in content:
        info["loader"] = "forge"
    elif "Quilt" in content:
        info["loader"] = "quilt"

    # 提取模组列表（含版本）
    mod_section_match = re.search(
        r"(?:Loaded Modules?|Mod List)[:\s]*(.+?)(?=----|\Z)",
        content,
        re.DOTALL,
    )
    if mod_section_match:
        mod_text = mod_section_match.group(1)
        mods = []
        mod_versions = {}

        # 格式1: "create 6.0.10" 或 "  create\t6.0.10"
        for line in mod_text.split("\n"):
            line = line.strip().lstrip("·-*• \t")
            if not line:
                continue
            # 匹配 "name version" 格式
            m = re.match(
                r"^([\w\-]+)[\s\t]+([A-Za-z]?[\d][\w\.\-+]+)",
                line
            )
            if m:
                mod_id = m.group(1)
                version = m.group(2)
                mods.append(mod_id)
                mod_versions[mod_id] = version
                continue
            # 格式2: "create:6.0.10"
            m2 = re.match(
                r"^([\w\-]+):[\s]*([A-Za-z]?[\d][\w\.\-+]+)",
                line
            )
            if m2:
                mod_id = m2.group(1)
                version = m2.group(2)
                mods.append(mod_id)
                mod_versions[mod_id] = version
                continue
            # 格式3: 只有mod名
            m3 = re.match(r"^([\w\-]+)$", line)
            if m3:
                mod_id = m3.group(1)
                mods.append(mod_id)

        # 如果上面没匹配到，用旧正则兜底
        if not mods:
            mods = re.findall(r"(\w[\w-]+):(?:\w+)", mod_text)

        info["mods"] = [m for m in mods[:100] if m]
        info["mod_count"] = len(info["mods"])
        info["mod_versions"] = mod_versions

    # 提取堆栈跟踪
    stack_match = re.search(
        r"(?:Stack trace|Caused by)[:\s]*(.+?)(?=----|\Z)",
        content,
        re.DOTALL,
    )
    if stack_match:
        info["stacktrace"] = stack_match.group(1).strip()[:2000]

    return info


def _match_patterns(content: str, crash_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """匹配崩溃模式（含上下文提取）"""
    patterns = config.get_crash_patterns().get("patterns", [])
    matches = []
    matched_ids = set()

    # 合并搜索范围：全文 + 描述 + 堆栈
    search_text = content
    if crash_info.get("description"):
        search_text += "\n" + crash_info["description"]
    if crash_info.get("stacktrace"):
        search_text += "\n" + crash_info["stacktrace"]

    # 按行分割用于上下文提取
    content_lines = content.split("\n")

    for pattern in patterns:
        if pattern["id"] in matched_ids:
            continue
        try:
            regex = re.compile(pattern["regex"], re.IGNORECASE)
            match = regex.search(search_text)
            if match:
                # 提取匹配行的上下文
                matched_text = match.group(0)
                context_lines = []

                # 找到匹配行号
                for i, line in enumerate(content_lines):
                    if regex.search(line):
                        # 取前后各2行上下文
                        start = max(0, i - 2)
                        end = min(len(content_lines), i + 3)
                        for j in range(start, end):
                            prefix = ">> " if j == i else "   "
                            context_lines.append(f"{prefix}{j+1}: {content_lines[j][:200]}")
                        break  # 只取第一个匹配的上下文

                matches.append({
                    "id": pattern["id"],
                    "name_cn": pattern["name_cn"],
                    "severity": pattern["severity"],
                    "desc_cn": pattern["desc_cn"],
                    "common_causes": pattern.get("common_causes", []),
                    "suggestions": pattern.get("suggestions", []),
                    "matched_regex": pattern["regex"],
                    "matched_text": matched_text[:200],
                    "context": "\n".join(context_lines) if context_lines else "",
                })
                matched_ids.add(pattern["id"])
        except re.error as e:
            logger.warning(f"正则编译失败: {pattern['regex']} - {e}")

    # 按严重程度排序
    severity_order = {"high": 0, "medium": 1, "low": 2}
    matches.sort(key=lambda x: severity_order.get(x["severity"], 3))

    return matches


def _fuzzy_match_mods(content: str, crash_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """模糊匹配堆栈中的模组包名，辅助定位涉事模组"""
    mod_clues = []

    # 从堆栈中提取 com.xxx.yyy 格式的包名
    stacktrace = crash_info.get("stacktrace", "")
    if not stacktrace:
        stacktrace = content

    # 匹配Java包名模式
    pkg_pattern = re.compile(r"(?:at\s+)?((?:com|net|org|io)\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+){1,4})")
    seen = set()

    for m in pkg_pattern.finditer(stacktrace):
        pkg = m.group(1)
        # 提取模组名（通常是第三段或第四段）
        parts = pkg.split(".")
        if len(parts) >= 3:
            mod_name = parts[2] if parts[1] in ("minecraft", "mojang") else parts[1]
            if mod_name not in seen and mod_name not in ("java", "sun", "android", "google"):
                seen.add(mod_name)
                mod_clues.append({
                    "mod_name": mod_name,
                    "package": pkg,
                })

    return mod_clues[:15]


def _normalize_mod_id(mod_id: str) -> str:
    """规范化模组ID（去空格、小写、下划线处理）"""
    return mod_id.strip().lower().replace("-", "_")


def _lookup_mod_version_recommendation(
    mod_id: str,
    mc_version: str,
    loader: str,
    current_version: str = "",
) -> Optional[Dict[str, Any]]:
    """在推荐数据库中查找指定模组的推荐版本

    Args:
        mod_id: 模组ID
        mc_version: MC版本，如"1.21.1"
        loader: 加载器类型
        current_version: 当前安装的版本（用于对比）

    Returns:
        推荐信息字典，无匹配则返回None
    """
    rec_db = config.get_mod_version_recommendations().get("mods", {})

    # 规范化mod_id
    norm_mod = _normalize_mod_id(mod_id)

    # 精确匹配或模糊匹配
    candidate = None
    if mod_id in rec_db:
        candidate = rec_db[mod_id]
    else:
        # 遍历查找规范化后匹配的key
        for key in rec_db:
            if _normalize_mod_id(key) == norm_mod:
                candidate = rec_db[key]
                break
        # 最后尝试子串匹配（如 create_railways 匹配 railways）
        if not candidate:
            for key in rec_db:
                if norm_mod in _normalize_mod_id(key) or _normalize_mod_id(key) in norm_mod:
                    candidate = rec_db[key]
                    break

    if not candidate:
        return None

    name_cn = candidate.get("name_cn", mod_id)

    # 查找MC版本
    mc_info = candidate.get("minecraft_versions", {})
    if mc_version not in mc_info:
        # 尝试找最近的（如1.21匹配1.21.1）
        for key in mc_info:
            if key.startswith(mc_version) or mc_version.startswith(key):
                mc_version = key
                break
        else:
            return {
                "mod_id": mod_id,
                "name_cn": name_cn,
                "mc_version": mc_version,
                "status": "mc_version_not_found",
                "message": f"数据库中无 {mc_version} 版本信息",
            }

    # 查找加载器
    loader_info = mc_info[mc_version].get(loader)
    if not loader_info:
        # 尝试其他加载器作为参考
        other_loader = next(iter(mc_info[mc_version].values()), None)
        if other_loader:
            return {
                "mod_id": mod_id,
                "name_cn": name_cn,
                "mc_version": mc_version,
                "loader": loader,
                "status": "loader_mismatch",
                "message": f"数据库中无 {loader} 加载器信息（有其他加载器版本）",
                "alternate_recommendation": other_loader.get("recommended", ""),
            }
        return {
            "mod_id": mod_id,
            "name_cn": name_cn,
            "mc_version": mc_version,
            "status": "loader_not_found",
            "message": f"数据库中无 {loader} 加载器信息",
        }

    recommended = loader_info.get("recommended", "")
    minimum = loader_info.get("minimum", "")
    notes = loader_info.get("notes", "")
    depends = loader_info.get("depends", {})

    # 判断当前版本状态
    status = "unknown"
    status_reason = ""
    if current_version and recommended:
        if current_version == recommended:
            status = "up_to_date"
            status_reason = "当前已是推荐版本"
        elif minimum and _version_compare(current_version, minimum) < 0:
            status = "outdated"
            status_reason = f"当前版本低于最低要求版本 {minimum}"
        else:
            status = "recommend_update"
            status_reason = f"推荐升级到 {recommended}"

    return {
        "mod_id": mod_id,
        "name_cn": name_cn,
        "mc_version": mc_version,
        "loader": loader,
        "current_version": current_version,
        "recommended_version": recommended,
        "minimum_version": minimum,
        "status": status,
        "status_reason": status_reason,
        "notes": notes,
        "depends": depends,
    }


def _version_compare(v1: str, v2: str) -> int:
    """比较两个版本字符串，返回 -1/0/1

    规则：按数字分段比较，非数字部分权重较低
    """
    def normalize(v: str) -> List:
        v = v.strip().lstrip("vV")
        # 处理带加号的版本，如 "0.6.6+0.6.0" -> 取前面部分
        if "+" in v:
            v = v.split("+")[0]
        parts = re.split(r"[\.\-]", v)
        result = []
        for p in parts:
            if p.isdigit():
                result.append((0, int(p)))  # 0表示数字段
            else:
                result.append((1, p.lower()))  # 1表示非数字段
        return result

    parts1 = normalize(v1)
    parts2 = normalize(v2)
    max_len = max(len(parts1), len(parts2))
    for i in range(max_len):
        if i >= len(parts1):
            return -1
        if i >= len(parts2):
            return 1
        t1, v1_part = parts1[i]
        t2, v2_part = parts2[i]
        if t1 != t2:
            return -1 if t1 < t2 else 1
        if isinstance(v1_part, int) and isinstance(v2_part, int):
            if v1_part < v2_part:
                return -1
            if v1_part > v2_part:
                return 1
        else:
            cmp_res = (v1_part > v2_part) - (v1_part < v2_part)
            if cmp_res != 0:
                return cmp_res
    return 0


def _analyze_version_recommendations(
    crash_info: Dict[str, Any],
    offline_mode: bool = False,
) -> List[Dict[str, Any]]:
    """对崩溃中涉及的所有模组进行版本分析推荐

    策略：
    1. 优先查本地数据库（快速、离线可用）
    2. 本地未命中时，联网查询 Modrinth API（全生态覆盖）
    3. 联网失败或禁用时，仅返回本地结果

    Args:
        crash_info: 已提取的崩溃信息（含mod_versions等）
        offline_mode: 是否禁用联网查询（仅使用本地数据库）

    Returns:
        版本推荐列表，按严重程度排序（需更新的在前面）
    """
    mc_version = crash_info.get("game_version", "")
    loader = crash_info.get("loader", "neoforge")
    mod_versions = crash_info.get("mod_versions", {})
    mods_list = crash_info.get("mods", [])

    if not mc_version:
        return []

    recommendations = []
    seen_ids = set()
    status_priority = {
        "outdated": 0,
        "recommend_update": 1,
        "loader_mismatch": 2,
        "online_outdated": 2,   # 联网查到的版本过旧
        "online_found": 3,      # 联网查到，状态待用户确认
        "online_not_found": 4,  # 联网未找到
        "unknown": 5,
        "mc_version_not_found": 5,
        "loader_not_found": 5,
        "up_to_date": 6,
        "online_up_to_date": 6,  # 联网查到，当前就是最新
    }

    # 分析有版本号的模组
    for mod_id, current_ver in mod_versions.items():
        rec = _lookup_mod_version_recommendation(
            mod_id, mc_version, loader, current_ver
        )
        if rec:
            rec["source"] = "local"
            recommendations.append(rec)
            seen_ids.add(mod_id)
        elif not offline_mode:
            # 本地没查到，尝试联网
            online_rec = _online_lookup(
                mod_id, mc_version, loader, current_ver
            )
            if online_rec:
                recommendations.append(online_rec)
                seen_ids.add(mod_id)

    # 分析有mod名但无版本号的
    for mod_id in mods_list:
        if mod_id in seen_ids:
            continue
        rec = _lookup_mod_version_recommendation(mod_id, mc_version, loader)
        if rec:
            rec["source"] = "local"
            recommendations.append(rec)
            seen_ids.add(mod_id)
        elif not offline_mode:
            online_rec = _online_lookup(mod_id, mc_version, loader)
            if online_rec:
                recommendations.append(online_rec)
                seen_ids.add(mod_id)

    # 按优先级排序
    recommendations.sort(
        key=lambda r: status_priority.get(r.get("status", "unknown"), 3)
    )

    return recommendations


def _online_lookup(
    mod_id: str,
    mc_version: str,
    loader: str,
    current_version: str = "",
) -> Optional[Dict[str, Any]]:
    """通过 Modrinth 联网查询模组版本推荐

    Args:
        mod_id: 模组 ID
        mc_version: MC 版本
        loader: 加载器
        current_version: 当前版本（可选）

    Returns:
        统一格式的推荐字典，或 None
    """
    try:
        from core.modrinth_client import get_latest_recommended_version
    except ImportError:
        logger.warning("modrinth_client 模块不可用，跳过联网查询")
        return None

    try:
        online_result = get_latest_recommended_version(
            mod_id, mc_version, loader
        )
    except Exception as e:
        logger.debug(f"联网查询异常({mod_id}): {e}")
        return None

    if not online_result or online_result.get("status") == "not_found":
        # 联网也没找到，返回一个“未知”占位
        return {
            "mod_id": mod_id,
            "name_cn": mod_id,
            "current_version": current_version,
            "recommended_version": "",
            "status": "online_not_found",
            "status_reason": f"本地数据库和 Modrinth 均未找到该模组的 {mc_version}/{loader} 版本信息",
            "source": "online",
            "project_title": "",
            "download_url": "",
            "notes": "建议检查模组 ID 是否正确，或手动到 Modrinth/CurseForge 查找",
            "online_result": online_result,
        }

    # 联网查到了，构造统一格式
    rec_ver = online_result.get("recommended_version", "")
    current_ver_clean = current_version or ""

    if current_ver_clean and rec_ver:
        cmp = _version_compare(current_ver_clean, rec_ver)
        if cmp == 0:
            status = "online_up_to_date"
            reason = "当前已是 Modrinth 上推荐的最新 release 版本"
        elif cmp < 0:
            status = "online_outdated"
            reason = f"当前版本低于 Modrinth 推荐版本 {rec_ver}"
        else:
            status = "online_found"
            reason = f"当前版本高于 Modrinth 推荐版本，可能是非正式版或版本号差异"
    else:
        status = "online_found"
        reason = "来自 Modrinth 实时查询"

    return {
        "mod_id": mod_id,
        "name_cn": online_result.get("project_title", mod_id),
        "current_version": current_ver_clean,
        "recommended_version": rec_ver,
        "status": status,
        "status_reason": reason,
        "loader": loader,
        "mc_version": mc_version,
        "source": "online",
        "project_id": online_result.get("project_id", ""),
        "project_title": online_result.get("project_title", ""),
        "download_url": online_result.get("download_url", ""),
        "download_filename": online_result.get("download_filename", ""),
        "download_size": online_result.get("download_size", 0),
        "game_versions": online_result.get("game_versions", []),
        "loaders": online_result.get("loaders", []),
        "online_matches": online_result.get("matches", []),
        "notes": online_result.get("note", ""),
        "depends": {},
    }


def _extract_error_lines(content: str) -> List[Dict[str, str]]:
    """提取关键错误行"""
    error_lines = []

    for i, line in enumerate(content.split("\n"), 1):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # 匹配关键错误模式
        if re.search(
            r"(Exception|Error|Caused by|FATAL|SEVERE|MixinApplyError|"
            r"Failed to|Cannot|Unable to|Missing|Duplicate|OutOfMemory)",
            line_stripped,
            re.IGNORECASE,
        ):
            error_lines.append({
                "line_num": i,
                "content": line_stripped[:300],
            })

    return error_lines[:30]  # 最多30条


def _detect_involved_mods(content: str, known_mods: List[str]) -> List[str]:
    """检测涉及的模组"""
    involved = []
    for mod in known_mods:
        if mod and mod in content:
            involved.append(mod)
    return involved


def _generate_html_report(
    file_path: str,
    file_type: str,
    crash_info: Dict[str, Any],
    matched_patterns: List[Dict[str, Any]],
    error_lines: List[Dict[str, str]],
    involved_mods: List[str],
    mod_clues: List[Dict[str, Any]],
    version_recommendations: List[Dict[str, Any]],
    timestamp: str,
) -> str:
    """生成崩溃分析HTML报告"""
    rg = ReportGenerator("报错修复")

    # === 概览卡片 ===
    severity_count = {"high": 0, "medium": 0, "low": 0}
    for p in matched_patterns:
        severity_count[p["severity"]] = severity_count.get(p["severity"], 0) + 1

    total_patterns = len(config.get_crash_patterns().get("patterns", []))

    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{file_type}</div>
        <div class='oc-label'>文件类型</div>
      </div>
      <div class='overview-card critical'>
        <div class='oc-num'>{severity_count['high']}</div>
        <div class='oc-label'>高危问题</div>
      </div>
      <div class='overview-card warning'>
        <div class='oc-num'>{severity_count['medium']}</div>
        <div class='oc-label'>中危问题</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{severity_count['low']}</div>
        <div class='oc-label'>低危问题</div>
      </div>
    </div>
    """

    # === 基本信息 ===
    info_rows = ""
    if crash_info.get("game_version"):
        info_rows += f"<tr><td>游戏版本</td><td>{crash_info['game_version']}</td></tr>"
    if crash_info.get("loader"):
        info_rows += f"<tr><td>加载器</td><td>{crash_info['loader']}</td></tr>"
    info_rows += f"<tr><td>模组数量</td><td>{crash_info.get('mod_count', 0)}</td></tr>"
    if crash_info.get("description"):
        info_rows += (
            f"<tr><td>崩溃描述</td><td>{crash_info['description'][:200]}</td></tr>"
        )

    info_html = f"""
    <div class='callout'>
      <div class='callout-title'>基本信息</div>
      <table class='data-table'>
        <thead><tr><th>项目</th><th>值</th></tr></thead>
        <tbody>{info_rows}</tbody>
      </table>
    </div>
    """

    # === 诊断结果（含上下文） ===
    diagnosis_html = ""
    if matched_patterns:
        diag_rows = ""
        severity_classes = {"high": "high", "medium": "medium", "low": "low"}
        for i, p in enumerate(matched_patterns, 1):
            cls = severity_classes.get(p["severity"], "low")
            causes_html = "".join(f"<li>{c}</li>" for c in p.get("common_causes", []))
            suggestions_html = "".join(f"<li>{s}</li>" for s in p.get("suggestions", []))

            # 上下文展示
            context_html = ""
            if p.get("context"):
                context_html = f"""
                <h4>匹配上下文</h4>
                <pre class='code-block'>{p['context']}</pre>
                """

            # 匹配文本
            matched_text_html = ""
            if p.get("matched_text"):
                matched_text_html = f"<p><strong>匹配片段:</strong> <code>{p['matched_text']}</code></p>"

            diag_rows += f"""
            <tr>
              <td>{i}</td>
              <td><span class='badge badge-{cls}'>{p['severity'].upper()}</span></td>
              <td><strong>{p['name_cn']}</strong></td>
              <td>{p['desc_cn']}</td>
            </tr>
            <tr>
              <td colspan="4">
                <details>
                  <summary>详细建议</summary>
                  {matched_text_html}
                  <h4>常见原因</h4>
                  <ul>{causes_html}</ul>
                  <h4>修复建议</h4>
                  <ul>{suggestions_html}</ul>
                  {context_html}
                </details>
              </td>
            </tr>
            """
        diagnosis_html = f"""
        <div class='callout critical'>
          <div class='callout-title'>诊断结果 - 检测到 {len(matched_patterns)} 个问题（共 {total_patterns} 种模式）</div>
          <table class='data-table'>
            <thead>
              <tr><th>#</th><th>严重度</th><th>问题</th><th>描述</th></tr>
            </thead>
            <tbody>{diag_rows}</tbody>
          </table>
        </div>
        """
    else:
        diagnosis_html = """
        <div class='callout green'>
          <div class='callout-title'>未匹配到已知错误模式</div>
          <p>当前日志内容未匹配到内置的崩溃模式库。</p>
          <p>建议：将日志中的关键错误行搜索社区（如MCBBS、GitHub Issues）获取帮助。</p>
        </div>
        """

    # === 关键错误行 ===
    errors_html = ""
    if error_lines:
        error_rows = ""
        for e in error_lines[:15]:
            error_rows += f"""
            <tr>
              <td>{e['line_num']}</td>
              <td><code>{e['content']}</code></td>
            </tr>
            """
        errors_html = f"""
        <div class='callout warning'>
          <div class='callout-title'>关键错误行</div>
          <table class='data-table'>
            <thead><tr><th>行号</th><th>内容</th></tr></thead>
            <tbody>{error_rows}</tbody>
          </table>
        </div>
        """

    # === 涉及模组 ===
    mods_html = ""
    if involved_mods:
        mod_items = "".join(f"<li><code>{m}</code></li>" for m in involved_mods)
        mods_html = f"""
        <div class='callout'>
          <div class='callout-title'>涉及模组（从模组列表提取）</div>
          <ul>{mod_items}</ul>
        </div>
        """

    # === 堆栈模组线索 ===
    clues_html = ""
    if mod_clues:
        clue_rows = ""
        for c in mod_clues:
            clue_rows += f"""
            <tr>
              <td><strong>{c['mod_name']}</strong></td>
              <td><code>{c['package']}</code></td>
            </tr>
            """
        clues_html = f"""
        <div class='callout'>
          <div class='callout-title'>堆栈模组线索（从堆栈包名推断）</div>
          <p>以下模组在崩溃堆栈中被发现，可能是问题来源：</p>
          <table class='data-table'>
            <thead><tr><th>模组名</th><th>Java包路径</th></tr></thead>
            <tbody>{clue_rows}</tbody>
          </table>
        </div>
        """

    # === 模组版本推荐 ===
    version_html = ""
    if version_recommendations:
        # 统计
        need_update = sum(
            1 for r in version_recommendations
            if r.get("status") in ("outdated", "online_outdated", "recommend_update", "online_found")
        )
        up_to_date = sum(
            1 for r in version_recommendations
            if r.get("status") in ("up_to_date", "online_up_to_date")
        )
        issues_count = sum(
            1 for r in version_recommendations
            if r.get("status") in ("loader_mismatch", "mc_version_not_found", "loader_not_found", "online_not_found")
        )
        local_count = sum(1 for r in version_recommendations if r.get("source") == "local")
        online_count = sum(1 for r in version_recommendations if r.get("source") == "online")

        version_rows = ""
        status_badge = {
            "outdated": ("badge high", "低于最低要求"),
            "online_outdated": ("badge high", "联网-需升级"),
            "recommend_update": ("badge medium", "推荐升级"),
            "online_found": ("badge medium", "联网-建议升级"),
            "loader_mismatch": ("badge medium", "加载器不匹配"),
            "loader_not_found": ("badge medium", "无该加载器数据"),
            "mc_version_not_found": ("badge", "无该版本数据"),
            "online_not_found": ("badge", "联网-未找到"),
            "up_to_date": ("badge low", "已是最新"),
            "online_up_to_date": ("badge low", "联网-已是最新"),
            "unknown": ("badge", "未知"),
        }
        for r in version_recommendations:
            s = r.get("status", "unknown")
            cls, label = status_badge.get(s, ("badge", s))
            current = r.get("current_version", "未检测") or "未检测"
            recommended = r.get("recommended_version", "—")
            notes = r.get("notes", "")
            depends = r.get("depends", {})
            source = r.get("source", "unknown")
            
            # 来源标识
            source_html = ""
            if source == "online":
                source_html = "<small style='color:#0099ff'>[联网]</small>"
            elif source == "local":
                source_html = "<small style='color:#44cc88'>[本地]</small>"
            
            # 下载链接
            download_html = ""
            if r.get("download_url"):
                download_html = f"<br/><a href='{r['download_url'][:120]}' style='color:#0066cc; font-size:11px'>⬇ 下载 {r.get('download_filename', '')}</a>"
            
            depends_html = ""
            if depends:
                dep_items = "、".join(f"{k} {v}" for k, v in depends.items())
                depends_html = f"<br/><small style='color:#888'>依赖: {dep_items}</small>"

            version_rows += f"""
            <tr>
              <td><strong>{r.get('name_cn', r['mod_id'])}</strong> {source_html}<br/><small style='color:#888'>{r['mod_id']}</small></td>
              <td><code>{current}</code></td>
              <td><code>{recommended}</code>{download_html}</td>
              <td><span class='badge {cls}'>{label}</span><br/><small style='color:#888'>{r.get('status_reason', '')}</small></td>
              <td>
                {notes if notes else '—'}
                {depends_html}
              </td>
            </tr>
            """

        version_html = f"""
        <div class='callout critical'>
          <div class='callout-title'>
            模组版本智能推荐（检测 {len(version_recommendations)} 个模组）
            <span style='margin-left:16px; font-weight:normal; font-size:13px;'>
              <span style='color:#ff5555'>需更新: {need_update}</span> ｜
              <span style='color:#ffaa00'>注意: {issues_count}</span> ｜
              <span style='color:#44cc88'>已最新: {up_to_date}</span> ｜
              <span style='color:#0099ff'>联网: {online_count}</span> ｜
              <span style='color:#44cc88'>本地: {local_count}</span>
            </span>
          </div>
          <table class='data-table'>
            <thead>
              <tr>
                <th>模组</th>
                <th>当前版本</th>
                <th>推荐版本</th>
                <th>状态</th>
                <th>说明/依赖</th>
              </tr>
            </thead>
            <tbody>{version_rows}</tbody>
          </table>
          <div style='margin-top:12px; padding:10px; background:#f8f9fa; border-radius:6px; font-size:13px;'>
            <strong>💡 使用说明：</strong>
            版本推荐结合了内置本地数据库和 Modrinth 实时联网查询。
            <span style='color:#0099ff'>[联网]</span> 标签表示来自 Modrinth API 实时查询（全生态覆盖）；
            <span style='color:#44cc88'>[本地]</span> 标签表示来自内置数据库（机械动力等热门模组的快速离线匹配）。
            状态为「低于最低要求」或「联网-需升级」的模组必须升级。
          </div>
        </div>
        """

    body_html = f"""
    <h2>分析概览</h2>
    {overview_html}

    <h2>基本信息</h2>
    {info_html}

    <h2>诊断结果</h2>
    {diagnosis_html}

    <h2>模组版本智能推荐</h2>
    {version_html}

    <h2>关键错误行</h2>
    {errors_html}

    <h2>涉及模组</h2>
    {mods_html}

    <h2>堆栈线索</h2>
    {clues_html}

    <div class='callout'>
      <div class='callout-title'>技术说明</div>
      <p>本报告基于内置崩溃模式库进行正则匹配分析，共包含 {total_patterns} 种常见MC崩溃模式。</p>
      <p>支持识别：Mixin失败、依赖缺失、Java版本、内存溢出、渲染错误、光影冲突、网络协议、注册表冲突、存档损坏、世界生成、机械动力专项等。</p>
      <p>每个匹配结果包含上下文行，方便快速定位问题位置。</p>
    </div>
    """

    return rg.render_full_html("报错修复分析", body_html, timestamp)


def run(args) -> Dict[str, Any]:
    """F8 报错修复主入口

    Args:
        args: argparse.Namespace，需包含:
            - crash_log: crash report或latest.log文件路径
            - launcher: 启动器类型(可选)
            - mc_version: MC版本(可选)
            - output: 输出目录(可选)
            - offline: 是否禁用联网查询(可选，默认False)

    Returns:
        统一返回结构字典
    """
    crash_log = getattr(args, "crash_log", None)
    output_dir = getattr(args, "output", None) or str(config.OUTPUT_DIR / "reports")
    offline_mode = getattr(args, "offline", False)

    if not crash_log:
        return config.make_result(
            status="error",
            feature="F8",
            input_summary={"crash_log": None},
            result={"error": "缺少 --crash-log 参数"},
            errors=["必须指定crash report或latest.log文件路径"],
        )

    log_path = Path(crash_log)
    if not log_path.exists():
        return config.make_result(
            status="error",
            feature="F8",
            input_summary={"crash_log": str(log_path)},
            result={"error": f"文件不存在: {crash_log}"},
            errors=[f"日志文件不存在: {crash_log}"],
        )

    logger.info(f"开始分析日志: {log_path.name}")

    # === 1. 读取文件 ===
    content = _read_log_file(log_path)

    # === 2. 检测文件类型 ===
    file_type = _detect_file_type(content, log_path.name)
    logger.info(f"文件类型: {file_type}")

    # === 3. 提取崩溃信息 ===
    crash_info = _extract_crash_info(content) if file_type == "crash_report" else {
        "description": "",
        "game_version": "",
        "loader": "",
        "mod_count": 0,
        "mods": [],
        "mod_versions": {},
        "stacktrace": "",
        "head_section": "",
    }

    # 若crash_report提取失败，尝试从latest.log推断MC版本和加载器
    if not crash_info.get("game_version"):
        m = re.search(r"minecraft version[\s:]+([\d.]+)", content, re.IGNORECASE)
        if m:
            crash_info["game_version"] = m.group(1)
    if not crash_info.get("loader"):
        if re.search(r"NeoForge|neoforge", content, re.IGNORECASE):
            crash_info["loader"] = "neoforge"
        elif re.search(r"Fabric|fabric", content, re.IGNORECASE):
            crash_info["loader"] = "fabric"
        elif re.search(r"Forge|forge", content, re.IGNORECASE):
            crash_info["loader"] = "forge"
    # 从latest.log提取已加载模组和版本
    if not crash_info.get("mod_versions") or len(crash_info.get("mod_versions", {})) == 0:
        for line in content.split("\n"):
            m = re.search(
                r"Loading mod[\s:]+([\w\-]+)[\s:]+([A-Za-z]?[\d][\w\.\-+]+)",
                line, re.IGNORECASE
            )
            if m:
                crash_info["mods"].append(m.group(1))
                crash_info["mod_versions"][m.group(1)] = m.group(2)
        if crash_info.get("mod_versions"):
            crash_info["mod_count"] = len(crash_info["mods"])

    # === 4. 匹配错误模式 ===
    matched_patterns = _match_patterns(content, crash_info)
    logger.info(f"匹配到 {len(matched_patterns)} 个错误模式")

    # === 5. 提取关键错误行 ===
    error_lines = _extract_error_lines(content)

    # === 6. 检测涉及的模组 ===
    involved_mods = _detect_involved_mods(content, crash_info.get("mods", []))

    # === 6.5 堆栈模组线索 ===
    mod_clues = _fuzzy_match_mods(content, crash_info)
    if mod_clues:
        logger.info(f"从堆栈中提取到 {len(mod_clues)} 个模组线索")

    # === 6.6 版本推荐分析 ===
    version_recommendations = _analyze_version_recommendations(
        crash_info, offline_mode=offline_mode
    )
    if version_recommendations:
        outdated = sum(
            1 for r in version_recommendations
            if r.get("status") in ("outdated", "online_outdated")
        )
        recommend_update = sum(
            1 for r in version_recommendations
            if r.get("status") in ("recommend_update", "online_found")
        )
        local_count = sum(
            1 for r in version_recommendations if r.get("source") == "local"
        )
        online_count = sum(
            1 for r in version_recommendations if r.get("source") == "online"
        )
        online_not_found = sum(
            1 for r in version_recommendations
            if r.get("status") == "online_not_found"
        )
        logger.info(
            f"版本推荐: 检测{len(version_recommendations)}个模组, "
            f"需更新{outdated}, 推荐升级{recommend_update}, "
            f"本地{local_count}, 联网{online_count}, 联网未找到{online_not_found}"
        )

    # === 7. 生成报告 ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    report_html = _generate_html_report(
        str(log_path), file_type, crash_info,
        matched_patterns, error_lines, involved_mods,
        mod_clues, version_recommendations, timestamp,
    )
    html_path = Path(output_dir) / f"crash_analysis_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_data = {
        "file_path": str(log_path),
        "file_type": file_type,
        "crash_info": crash_info,
        "matched_patterns": matched_patterns,
        "error_lines": error_lines,
        "involved_mods": involved_mods,
        "mod_clues": mod_clues,
        "version_recommendations": version_recommendations,
        "timestamp": timestamp,
    }
    json_path = Path(output_dir) / f"crash_analysis_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # === 8. 生成修复建议汇总 ===
    all_suggestions = []
    for p in matched_patterns:
        for s in p.get("suggestions", []):
            all_suggestions.append({"problem": p["name_cn"], "suggestion": s})

    # 版本相关的修复建议
    version_suggestions = []
    for r in version_recommendations:
        status = r.get("status", "")
        name_cn = r.get("name_cn", r["mod_id"])
        cur_ver = r.get("current_version", "?")
        rec_ver = r.get("recommended_version", "?")
        reason = r.get("status_reason", "")

        if status in ("outdated", "online_outdated"):
            prefix = "【必须升级】" if status == "outdated" else "【联网检测-需升级】"
            dl_hint = ""
            if r.get("download_url"):
                dl_hint = f"，下载链接: {r['download_url'][:80]}..."
            version_suggestions.append(
                f"{prefix}{name_cn}: 当前{cur_ver} → 推荐{rec_ver}（{reason}）{dl_hint}"
            )
        elif status in ("recommend_update", "online_found"):
            prefix = "【推荐升级】" if status == "recommend_update" else "【联网检测-建议更新】"
            dl_hint = ""
            if r.get("download_url"):
                dl_hint = f"，下载链接: {r['download_url'][:80]}..."
            version_suggestions.append(
                f"{prefix}{name_cn}: 当前{cur_ver} → 推荐{rec_ver}（{reason}）{dl_hint}"
            )
        elif status == "loader_mismatch":
            version_suggestions.append(
                f"【加载器不匹配】{name_cn}: {reason}"
            )
        elif status == "online_not_found":
            version_suggestions.append(
                f"【未找到版本】{name_cn}: {reason}"
            )
    all_suggestions.extend(
        [{"problem": "模组版本问题", "suggestion": s} for s in version_suggestions]
    )

    # 概要统计
    outdated = sum(
        1 for r in version_recommendations
        if r.get("status") in ("outdated", "online_outdated")
    )
    recommend_update = sum(
        1 for r in version_recommendations
        if r.get("status") in ("recommend_update", "online_found")
    )
    up_to_date = sum(
        1 for r in version_recommendations
        if r.get("status") in ("up_to_date", "online_up_to_date")
    )
    online_count = sum(
        1 for r in version_recommendations if r.get("source") == "online"
    )
    online_not_found = sum(
        1 for r in version_recommendations
        if r.get("status") == "online_not_found"
    )

    logger.info(
        f"分析完成: {len(matched_patterns)}个问题, {len(error_lines)}个错误行, "
        f"{len(mod_clues)}个模组线索, {len(version_recommendations)}个版本推荐 "
        f"(必须升级{outdated}, 推荐升级{recommend_update}, 已最新{up_to_date}, "
        f"联网查询{online_count}, 联网未找到{online_not_found})"
    )

    return config.make_result(
        status="success",
        feature="F8",
        input_summary={
            "crash_log": str(log_path),
            "file_type": file_type,
        },
        result={
            "file_type": file_type,
            "crash_info": crash_info,
            "matched_patterns": matched_patterns,
            "error_lines_count": len(error_lines),
            "involved_mods": involved_mods,
            "mod_clues": mod_clues,
            "version_recommendations": version_recommendations,
            "version_summary": {
                "total_checked": len(version_recommendations),
                "outdated": outdated,
                "recommend_update": recommend_update,
                "up_to_date": up_to_date,
                "loader_issues": sum(
                    1 for r in version_recommendations
                    if r.get("status") in ("loader_mismatch", "loader_not_found")
                ),
                "local_count": sum(
                    1 for r in version_recommendations if r.get("source") == "local"
                ),
                "online_count": online_count,
                "online_not_found": online_not_found,
                "offline_mode": offline_mode,
            },
            "fix_suggestions": all_suggestions,
        },
        output_files={
            "report": str(html_path),
            "data": str(json_path),
        },
    )
