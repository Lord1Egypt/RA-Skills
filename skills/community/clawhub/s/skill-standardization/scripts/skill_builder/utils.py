#!/usr/bin/env python3
"""
工具函数模块 — 从原 skill_builder.py 提取
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# R-12: 外部数据目录变量检测模式（通用化，非框架绑定）
_DATA_VAR_RE = re.compile(
    r'^([A-Za-z_]*?(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Za-z_]*(?:_DIR|_PATH))\s*=\s*(.+)$'
)

# 可选拆分到 references/ 的章节关键词（用于 refactor 拆分判断）
SPLITTABLE_KEYWORDS = {
    "详细教程": ["详细教程", "使用指南", "完整指南", "逐步指南"],
    "示例集合": ["示例", "examples", "用例", "案例"],
    "参考文档": ["参考文档", "API 参考", "命令参考", "参数说明"],
    "常见问题": ["常见问题", "FAQ", "faq", "疑难解答"],
    "版本日志": ["更新日志", "changelog", "版本历史", "变更记录"],
    "架构设计": ["架构", "architecture", "设计", "模块说明"],
}


def _create_backup(skill_dir, operation, workspace="."):
    """创建技能目录的 ZIP 备份（带时间戳）
    
    ZIP 格式避免备份目录被 Skill 扫描器误识别为重复技能。
    支持单文件回退：可用 zipfile.ZipFile 的 extract() 提取指定文件。
    """
    import zipfile
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{skill_dir.name}_bak_{operation}_{ts}.zip"
    backup_path = skill_dir.parent / backup_name
    
    with zipfile.ZipFile(str(backup_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(str(skill_dir)):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "__MACOSX"}]
            rel = os.path.relpath(root, str(skill_dir))
            for f in files:
                if f.endswith((".pyc", ".DS_Store")):
                    continue
                arcname = os.path.join(rel, f) if rel != "." else f
                zf.write(os.path.join(root, f), arcname)
    
    print(f"  [BACKUP] 已创建: {backup_path}")
    return backup_path


def _write_json(path, data):
    """写入 JSON 文件（格式化，UTF-8）"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _check_artifact_paths(skill_dir):
    """检查产出物路径规范性（铁律4）

    返回违规列表
    """
    violations = []
    skill_name = skill_dir.name
    expected_prefix = f"skills/.standardization/{skill_name}/"

    # 检查 SKILL.md 中的路径引用
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        # 查找路径引用
        path_pattern = r'`([^`]*?(?:skills?|scripts?|references?)[^`]*?)`'
        for m in re.finditer(path_pattern, content):
            path_ref = m.group(1)
            # 检查是否符合规范
            if not path_ref.startswith(expected_prefix):
                if "skills/" in path_ref or "scripts/" in path_ref:
                    violations.append(f"路径引用不符合规范：{path_ref} (期望前缀：{expected_prefix})")

    return violations


def _check_external_data_dir(skill_dir, results, workspace="."):
    """检查外部数据目录规范性（R-12）"""
    meta_file = skill_dir / "_meta.json"
    if not meta_file.exists():
        return

    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception:
        return

    # 检查 data_dir 字段
    if "data_dir" not in meta:
        results["warnings"].append("⚠️  _meta.json 缺少 data_dir 字段（R-12）")
        return

    expected_data_dir = f"skills/.standardization/{skill_dir.name}/data/"
    if meta["data_dir"] != expected_data_dir:
        results["warnings"].append(
            f"⚠️  data_dir 不符合规范：{meta['data_dir']} (期望：{expected_data_dir})"
        )

    # 检查脚本中是否有对应的变量声明
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script_file in scripts_dir.iterdir():
            if script_file.suffix in (".py", ".sh", ".bat"):
                content = script_file.read_text(encoding="utf-8", errors="ignore")
                for line in content.splitlines():
                    m = _DATA_VAR_RE.match(line)
                    if m:
                        var_name = m.group(1)
                        var_value = m.group(2).strip().strip("\"'")
                        if var_value != expected_data_dir:
                            results["warnings"].append(
                                f"⚠️  脚本 {script_file.name} 中 {var_name} 值不符合规范：{var_value}"
                            )
