# -*- coding: utf-8 -*-
"""F4: Mixin冲突扫描

批量扫描mods文件夹中所有模组的Mixin配置文件，
检测配置层面的重叠注入目标、版本不匹配、基础冲突风险，
自动生成冲突诊断报告与兼容清单。

使用方式:
    from core.mixin_scanner import run
    import argparse
    args = argparse.Namespace(mods_dir="mods", output=None, severity="summary")
    result = run(args)
"""

import sys
import os
import json
import re
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.jar_utils import extract_jar, create_temp_dir, cleanup_temp_dir, read_jar_file
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("mixin_scanner")

# === Mixin版本兼容性映射 ===
LOADER_MIXIN_VERSIONS = {
    "forge": {"min": "0.7", "recommended": "0.8"},
    "neoforge": {"min": "0.8", "recommended": "0.8"},
    "fabric": {"min": "0.4", "recommended": "0.5"},
    "quilt": {"min": "0.4", "recommended": "0.5"},
}

# === Mixin配置文件识别正则 ===
MIXIN_CONFIG_PATTERNS = [
    re.compile(r"^mixins?\..*\.json$", re.IGNORECASE),
    re.compile(r"^assets/.*/mixins?\..*\.json$", re.IGNORECASE),
    re.compile(r"^data/.*/mixins?\..*\.json$", re.IGNORECASE),
]

# === 冲突类型中文描述 ===
CONFLICT_DESC = {
    "overlapping_target": "多个模组同时修改同一个类，可能导致功能异常或崩溃",
    "version_mismatch": "Mixin配置版本与加载器支持的版本不匹配",
    "incompatible_loader": "Mixin配置声明的加载器与当前环境不兼容",
    "abstract_method": "Mixin包含抽象方法实现，可能与其他模组冲突",
    "required_conflict": "多个required=true的Mixin修改同一目标，优先级冲突",
}

# === 冲突建议 ===
CONFLICT_SUGGESTIONS = {
    "overlapping_target": "测试两个模组是否兼容，或寻找替代方案。如崩溃，尝试移除其中一个模组",
    "version_mismatch": "检查加载器版本，升级加载器或寻找兼容版本的模组",
    "incompatible_loader": "确认模组的加载器支持情况，寻找对应加载器的版本",
    "abstract_method": "注意该Mixin的实现细节，可能需要配合其他依赖模组",
    "required_conflict": "两个模组都强制修改同一目标，极可能冲突，建议二选一",
}


def _is_mixin_config(filename: str) -> bool:
    """判断文件是否为Mixin配置文件"""
    basename = os.path.basename(filename)
    for pattern in MIXIN_CONFIG_PATTERNS:
        if pattern.match(basename) or pattern.match(filename):
            return True
    return False


def _parse_mixin_config(config_path: Path) -> Optional[Dict[str, Any]]:
    """解析Mixin配置文件"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.debug(f"解析Mixin配置失败: {config_path.name}, 原因: {e}")
        return None


def _extract_mixin_info(config: Dict[str, Any], mod_id: str) -> Dict[str, Any]:
    """从Mixin配置中提取关键信息"""
    info = {
        "mod_id": mod_id,
        "config_file": "",
        "required": config.get("required", False),
        "package": config.get("package", ""),
        "compatibilityLevel": config.get("compatibilityLevel", ""),
        "minVersion": config.get("minVersion", ""),
        "maxVersion": config.get("maxVersion", ""),
        "mixins": [],
        "client": [],
        "server": [],
    }

    for mixin in config.get("mixins", []):
        if isinstance(mixin, dict):
            info["mixins"].append({
                "name": mixin.get("name", ""),
                "desc": mixin.get("desc", ""),
                "target": _parse_desc(mixin.get("desc", "")),
            })
        elif isinstance(mixin, str):
            info["mixins"].append({
                "name": mixin,
                "desc": "",
                "target": "",
            })

    for mixin in config.get("client", []):
        if isinstance(mixin, dict):
            info["client"].append({
                "name": mixin.get("name", ""),
                "desc": mixin.get("desc", ""),
                "target": _parse_desc(mixin.get("desc", "")),
            })
        elif isinstance(mixin, str):
            info["client"].append({"name": mixin, "desc": "", "target": ""})

    for mixin in config.get("server", []):
        if isinstance(mixin, dict):
            info["server"].append({
                "name": mixin.get("name", ""),
                "desc": mixin.get("desc", ""),
                "target": _parse_desc(mixin.get("desc", "")),
            })
        elif isinstance(mixin, str):
            info["server"].append({"name": mixin, "desc": "", "target": ""})

    return info


def _parse_desc(desc: str) -> str:
    """从Mixin desc中提取目标类名

    desc格式: (Lnet/minecraft/world/level/block/entity/AbstractFurnaceBlockEntity;)V
    提取: net.minecraft.world.level.block.entity.AbstractFurnaceBlockEntity
    """
    if not desc:
        return ""

    match = re.search(r"\(L([^;]+);", desc)
    if match:
        return match.group(1).replace("/", ".")
    return ""


def scan_mod_jar(jar_path: Path) -> List[Dict[str, Any]]:
    """扫描单个JAR中的Mixin配置"""
    mixin_configs = []
    mod_id = jar_path.stem

    try:
        tmp_dir = create_temp_dir("mixin_scan")
        try:
            extract_jar(jar_path, tmp_dir)

            for root, dirs, files in os.walk(tmp_dir):
                for filename in files:
                    if _is_mixin_config(filename):
                        config_path = Path(root) / filename
                        config = _parse_mixin_config(config_path)
                        if config:
                            rel_path = str(config_path.relative_to(tmp_dir))
                            info = _extract_mixin_info(config, mod_id)
                            info["config_file"] = rel_path
                            mixin_configs.append(info)
        finally:
            cleanup_temp_dir(tmp_dir)

    except Exception as e:
        logger.warning(f"扫描JAR失败 {jar_path.name}: {e}")

    return mixin_configs


def detect_conflicts(all_configs: List[Dict[str, Any]], loader: str = "forge") -> Dict[str, Any]:
    """检测Mixin冲突"""
    conflicts = []
    warnings = []

    # === 1. 构建目标类索引 ===
    target_index = defaultdict(list)  # target_class -> [config_info]

    for cfg in all_configs:
        for mixin_list in [cfg["mixins"], cfg["client"], cfg["server"]]:
            for mixin in mixin_list:
                target = mixin.get("target", "")
                if target:
                    target_index[target].append({
                        "mod_id": cfg["mod_id"],
                        "mixin_name": mixin["name"],
                        "config_file": cfg["config_file"],
                        "required": cfg["required"],
                    })

    # === 2. 检测重叠注入目标 ===
    for target, entries in target_index.items():
        if len(entries) > 1:
            mods_involved = list(set(e["mod_id"] for e in entries))
            has_required = any(e["required"] for e in entries)

            if has_required and len(mods_involved) > 1:
                conflict_type = "required_conflict"
                severity = "high"
            else:
                conflict_type = "overlapping_target"
                severity = "high" if len(mods_involved) >= 3 else "medium"

            conflicts.append({
                "type": conflict_type,
                "severity": severity,
                "target_class": target,
                "mods_involved": mods_involved,
                "mixin_details": [
                    {"mod_id": e["mod_id"], "mixin": e["mixin_name"], "required": e["required"]}
                    for e in entries
                ],
                "desc_cn": CONFLICT_DESC.get(conflict_type, "未知冲突类型"),
                "suggestion": CONFLICT_SUGGESTIONS.get(conflict_type, "建议人工排查"),
            })

    # === 3. 检测版本兼容性 ===
    loader_info = LOADER_MIXIN_VERSIONS.get(loader, {})
    min_required = loader_info.get("min", "0.7")

    for cfg in all_configs:
        min_ver = cfg.get("minVersion", "")
        if min_ver and _compare_versions(min_ver, min_required) < 0:
            warnings.append({
                "type": "version_mismatch",
                "severity": "low",
                "mod_id": cfg["mod_id"],
                "config_file": cfg["config_file"],
                "minVersion": min_ver,
                "loader_minVersion": min_required,
                "desc_cn": f"模组 {cfg['mod_id']} 的Mixin最低版本 {min_ver} 低于加载器 {loader} 要求的 {min_required}",
                "suggestion": "升级加载器或寻找兼容版本的模组",
            })

    # === 4. 按严重程度排序 ===
    severity_order = {"high": 0, "medium": 1, "low": 2}
    conflicts.sort(key=lambda c: severity_order.get(c["severity"], 3))
    warnings.sort(key=lambda w: severity_order.get(w["severity"], 3))

    return {
        "conflicts": conflicts,
        "warnings": warnings,
        "total_conflicts": len(conflicts),
        "total_warnings": len(warnings),
    }


def _compare_versions(v1: str, v2: str) -> int:
    """比较两个版本号，返回 -1/0/1"""
    try:
        parts1 = [int(x) for x in v1.split(".")]
        parts2 = [int(x) for x in v2.split(".")]
        max_len = max(len(parts1), len(parts2))
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for a, b in zip(parts1, parts2):
            if a < b:
                return -1
            if a > b:
                return 1
        return 0
    except (ValueError, AttributeError):
        return 0


def _generate_html_report(
    scan_summary: Dict[str, Any],
    conflicts_data: Dict[str, Any],
    all_configs: List[Dict[str, Any]],
    severity: str,
    timestamp: str,
) -> str:
    """生成HTML冲突诊断报告"""
    rg = ReportGenerator("Mixin冲突诊断报告")

    # === 概览卡片 ===
    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{scan_summary['total_mods']}</div>
        <div class='oc-label'>扫描模组数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{scan_summary['mods_with_mixins']}</div>
        <div class='oc-label'>含Mixin的模组</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{scan_summary['total_mixin_targets']}</div>
        <div class='oc-label'>Mixin目标总数</div>
      </div>
      <div class='overview-card critical'>
        <div class='oc-num'>{conflicts_data['total_conflicts']}</div>
        <div class='oc-label'>冲突数</div>
      </div>
      <div class='overview-card warning'>
        <div class='oc-num'>{conflicts_data['total_warnings']}</div>
        <div class='oc-label'>警告数</div>
      </div>
    </div>
    """

    # === 冲突详情 ===
    conflicts_html = ""
    if conflicts_data["conflicts"]:
        conflict_rows = ""
        for i, c in enumerate(conflicts_data["conflicts"], 1):
            severity_class = "high" if c["severity"] == "high" else "medium"
            mods_html = ", ".join(c["mods_involved"])
            conflict_rows += f"""
            <tr>
              <td>{i}</td>
              <td><span class='badge badge-{severity_class}'>{c['severity'].upper()}</span></td>
              <td><code>{c['target_class']}</code></td>
              <td>{mods_html}</td>
              <td>{c['desc_cn']}</td>
              <td>{c['suggestion']}</td>
            </tr>
            """
        conflicts_html = f"""
        <div class='callout critical'>
          <div class='callout-title'>⚠️ 检测到 {conflicts_data['total_conflicts']} 个冲突</div>
          <table class='data-table'>
            <thead>
              <tr><th>#</th><th>严重度</th><th>目标类</th><th>涉及模组</th><th>描述</th><th>建议</th></tr>
            </thead>
            <tbody>
              {conflict_rows}
            </tbody>
          </table>
        </div>
        """
    else:
        conflicts_html = """
        <div class='callout ok'>
          <div class='callout-title'>✅ 未检测到Mixin冲突</div>
          <p>当前整合包的Mixin配置无明显重叠注入目标。</p>
        </div>
        """

    # === 警告详情 ===
    warnings_html = ""
    if conflicts_data["warnings"]:
        warning_rows = ""
        for i, w in enumerate(conflicts_data["warnings"], 1):
            warning_rows += f"""
            <tr>
              <td>{i}</td>
              <td><span class='badge badge-{w["severity"]}'>{w['severity'].upper()}</span></td>
              <td>{w['mod_id']}</td>
              <td><code>{w['config_file']}</code></td>
              <td>{w['desc_cn']}</td>
              <td>{w['suggestion']}</td>
            </tr>
            """
        warnings_html = f"""
        <div class='callout warning'>
          <div class='callout-title'>⚠️ {conflicts_data['total_warnings']} 个警告</div>
          <table class='data-table'>
            <thead>
              <tr><th>#</th><th>严重度</th><th>模组</th><th>配置文件</th><th>描述</th><th>建议</th></tr>
            </thead>
            <tbody>
              {warning_rows}
            </tbody>
          </table>
        </div>
        """

    # === 兼容性清单 ===
    compat_items = []
    for cfg in all_configs:
        total_mixins = len(cfg["mixins"]) + len(cfg["client"]) + len(cfg["server"])
        compat_items.append({
            "mod_id": cfg["mod_id"],
            "config_file": cfg["config_file"],
            "required": cfg["required"],
            "compatibilityLevel": cfg["compatibilityLevel"],
            "minVersion": cfg["minVersion"],
            "total_mixins": total_mixins,
        })

    compat_rows = ""
    for item in sorted(compat_items, key=lambda x: x["mod_id"]):
        required_badge = "✅ 是" if item["required"] else "❌ 否"
        compat_rows += f"""
        <tr>
          <td>{item['mod_id']}</td>
          <td><code>{item['config_file']}</code></td>
          <td>{required_badge}</td>
          <td>{item['compatibilityLevel']}</td>
          <td>{item['minVersion']}</td>
          <td>{item['total_mixins']}</td>
        </tr>
        """

    compat_html = f"""
    <div class='callout'>
      <div class='callout-title'>📋 兼容性清单</div>
      <table class='data-table'>
        <thead>
          <tr><th>模组ID</th><th>配置文件</th><th>Required</th><th>兼容级别</th><th>最低版本</th><th>Mixin数</th></tr>
        </thead>
        <tbody>
          {compat_rows}
        </tbody>
      </table>
    </div>
    """

    # === 完整Mixin列表（仅full模式） ===
    full_detail_html = ""
    if severity == "full":
        mixin_detail_rows = ""
        for cfg in all_configs:
            for mixin_list_name, mixin_list in [("mixins", cfg["mixins"]), ("client", cfg["client"]), ("server", cfg["server"])]:
                for mixin in mixin_list:
                    target = mixin.get("target", "") or "(无desc信息)"
                    mixin_detail_rows += f"""
                    <tr>
                      <td>{cfg['mod_id']}</td>
                      <td>{mixin_list_name}</td>
                      <td>{mixin['name']}</td>
                      <td><code>{target}</code></td>
                    </tr>
                    """

        full_detail_html = f"""
        <details class='callout' open>
          <summary>📝 全部Mixin目标列表（共 {len(all_configs)} 个配置）</summary>
          <table class='data-table'>
            <thead>
              <tr><th>模组</th><th>类型</th><th>Mixin名称</th><th>目标类</th></tr>
            </thead>
            <tbody>
              {mixin_detail_rows}
            </tbody>
          </table>
        </details>
        """

    # === 组装HTML ===
    body_html = f"""
    <h2>扫描概览</h2>
    {overview_html}

    <h2>冲突诊断</h2>
    {conflicts_html}

    <h2>警告信息</h2>
    {warnings_html}

    <h2>兼容性分析</h2>
    {compat_html}
    {full_detail_html}

    <div class='callout'>
      <div class='callout-title'>技术说明</div>
      <p>本报告基于Mixin配置文件层面的静态分析，检测配置声明的重叠注入目标。</p>
      <p>部分重叠注入实际运行时可能兼容（如使用不同注入点），本报告仅作为安装前的风险参考。</p>
      <p>如需深度分析（字节码级别），请等待V3版本。</p>
    </div>
    """

    return rg.render_full_html("Mixin冲突扫描报告", body_html, timestamp)


def run(args) -> Dict[str, Any]:
    """F4 Mixin冲突扫描主入口

    Args:
        args: argparse.Namespace，需包含:
            - mods_dir: mods文件夹路径
            - output: 输出目录(可选)
            - severity: 报告详细度 summary/full

    Returns:
        统一返回结构字典
    """
    start_time = datetime.now()
    mods_dir = getattr(args, "mods_dir", None)
    output_dir = getattr(args, "output", None) or str(config.OUTPUT_DIR / "reports")
    severity = getattr(args, "severity", "summary")

    if not mods_dir:
        return config.make_result(
            status="error",
            feature="F4",
            input_summary={"mods_dir": None},
            result={"error": "缺少 --mods-dir 参数"},
            errors=["必须指定mods文件夹路径"],
        )

    mods_path = Path(mods_dir)
    if not mods_path.exists():
        return config.make_result(
            status="error",
            feature="F4",
            input_summary={"mods_dir": str(mods_path)},
            result={"error": f"路径不存在: {mods_dir}"},
            errors=[f"mods目录不存在: {mods_dir}"],
        )

    logger.info(f"开始扫描mods目录: {mods_dir}")

    # === 1. 收集所有JAR文件 ===
    jar_files = sorted(mods_path.glob("*.jar"))
    if not jar_files:
        return config.make_result(
            status="success",
            feature="F4",
            input_summary={"mods_dir": str(mods_path), "jar_count": 0},
            result={"scan_summary": {"total_mods": 0, "mods_with_mixins": 0, "total_mixin_targets": 0, "conflicts": 0, "warnings": 0}, "conflicts": [], "compatibility_list": []},
            warnings=["mods目录为空或无JAR文件"],
        )

    # === 2. 确定加载器 ===
    loader = getattr(args, "loader", "forge")
    if not loader:
        loader = "forge"

    # === 3. 扫描每个JAR ===
    all_configs = []
    logger.info(f"发现 {len(jar_files)} 个JAR文件，开始扫描...")

    for jar_path in jar_files:
        logger.debug(f"扫描: {jar_path.name}")
        configs = scan_mod_jar(jar_path)
        if configs:
            all_configs.extend(configs)
            logger.debug(f"  发现 {len(configs)} 个Mixin配置")

    # === 4. 构建扫描摘要 ===
    mods_with_mixins = set(c["mod_id"] for c in all_configs)
    total_targets = sum(
        len(c["mixins"]) + len(c["client"]) + len(c["server"])
        for c in all_configs
    )

    scan_summary = {
        "total_mods": len(jar_files),
        "mods_with_mixins": len(mods_with_mixins),
        "total_mixin_targets": total_targets,
        "total_configs": len(all_configs),
    }

    # === 5. 检测冲突 ===
    conflicts_data = detect_conflicts(all_configs, loader)
    scan_summary["conflicts"] = conflicts_data["total_conflicts"]
    scan_summary["warnings"] = conflicts_data["total_warnings"]

    # === 6. 兼容性清单 ===
    compat_list = []
    for cfg in all_configs:
        total_mixins = len(cfg["mixins"]) + len(cfg["client"]) + len(cfg["server"])
        compat_list.append({
            "mod_id": cfg["mod_id"],
            "config_file": cfg["config_file"],
            "required": cfg["required"],
            "compatibilityLevel": cfg["compatibilityLevel"],
            "minVersion": cfg["minVersion"],
            "total_mixins": total_mixins,
        })

    # === 7. 生成报告 ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    report_name = f"mixin_scan_{timestamp}"
    report_html = _generate_html_report(
        scan_summary, conflicts_data, all_configs, severity, timestamp
    )
    html_path = Path(output_dir) / f"{report_name}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_path = Path(output_dir) / f"{report_name}.json"
    json_data = {
        "scan_summary": scan_summary,
        "conflicts": conflicts_data["conflicts"],
        "warnings": conflicts_data["warnings"],
        "compatibility_list": compat_list,
        "timestamp": timestamp,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    logger.info(
        f"扫描完成: {scan_summary['total_mods']}个模组, "
        f"{scan_summary['mods_with_mixins']}个含Mixin, "
        f"{scan_summary['conflicts']}个冲突, {scan_summary['warnings']}个警告"
    )

    return config.make_result(
        status="success",
        feature="F4",
        input_summary={
            "mods_dir": str(mods_path),
            "jar_count": len(jar_files),
            "loader": loader,
            "severity": severity,
        },
        result={
            "scan_summary": scan_summary,
            "conflicts": conflicts_data["conflicts"],
            "warnings": conflicts_data["warnings"],
            "compatibility_list": compat_list,
        },
        output_files={
            "report": str(html_path),
            "data": str(json_path),
        },
    )
