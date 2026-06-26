#!/usr/bin/env python3
"""Validate project structure and required fields. Cross-platform replacement for bash scripts."""

import argparse
import json
import sys
from pathlib import Path

from utils.logger import setup_logger


REQUIRED_PROJECT_FIELDS = ["name", "type", "artStyle", "videoRatio"]
REQUIRED_MODEL_FIELDS = ["provider", "model"]


def check_project_json(project_dir: Path) -> tuple[bool, list[str]]:
    """Check project.json existence and required fields."""
    errors = []
    project_json = project_dir / "project.json"

    if not project_json.exists():
        errors.append("project.json 不存在")
        return False, errors

    try:
        with open(project_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"project.json 格式错误: {e}")
        return False, errors

    for field in REQUIRED_PROJECT_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"project.json 缺少字段: {field}")

    # Check models config
    models = data.get("models", {})
    for model_type in ["text", "image", "video"]:
        model_config = models.get(model_type)
        if not model_config:
            errors.append(f"models.{model_type} 未配置")
        else:
            for field in REQUIRED_MODEL_FIELDS:
                if field not in model_config or not model_config[field]:
                    errors.append(f"models.{model_type}.{field} 未配置")

    return len(errors) == 0, errors


def check_directory_structure(project_dir: Path) -> tuple[bool, list[str], list[str]]:
    """Check required directories exist."""
    errors = []
    warnings = []

    required_dirs = ["outline", "assets", "script", "storyboard"]
    optional_dirs = ["video", "audio", "subtitle", "final"]

    for d in required_dirs:
        dir_path = project_dir / d
        if not dir_path.exists():
            errors.append(f"必需目录不存在: {d}/")

    for d in optional_dirs:
        dir_path = project_dir / d
        if not dir_path.exists():
            warnings.append(f"可选目录不存在: {d}/")

    return len(errors) == 0, errors, warnings


def check_storyline(project_dir: Path) -> tuple[bool, list[str]]:
    """Check storyline.md structure."""
    errors = []
    storyline = project_dir / "storyline.md"

    if not storyline.exists():
        errors.append("storyline.md 不存在")
        return False, errors

    content = storyline.read_text(encoding="utf-8")
    required_sections = ["主题", "主线剧情", "主要人物关系", "情感基调"]

    for section in required_sections:
        if section not in content:
            errors.append(f"storyline.md 缺少章节: {section}")

    return len(errors) == 0, errors


def check_outlines(project_dir: Path) -> tuple[bool, list[str], list[str]]:
    """Check outline files."""
    errors = []
    warnings = []

    outline_dir = project_dir / "outline"
    if not outline_dir.exists():
        errors.append("outline/ 目录不存在")
        return False, errors, warnings

    outline_files = sorted(outline_dir.glob("outline-*.md"))
    if not outline_files:
        warnings.append("未找到大纲文件")
        return True, errors, warnings

    required_sections = ["标题", "核心矛盾", "剧情主干", "剧情节点"]

    for f in outline_files:
        content = f.read_text(encoding="utf-8")
        for section in required_sections:
            if section not in content:
                errors.append(f"{f.name} 缺少章节: {section}")

    return len(errors) == 0, errors, warnings


def check_assets(project_dir: Path) -> tuple[bool, list[str], list[str]]:
    """Check asset files."""
    errors = []
    warnings = []

    assets_dir = project_dir / "assets"
    if not assets_dir.exists():
        errors.append("assets/ 目录不存在")
        return False, errors, warnings

    for name in ["characters", "props", "scenes"]:
        md_path = assets_dir / f"{name}.md"
        if not md_path.exists():
            warnings.append(f"assets/{name}.md 不存在")

    data_json = assets_dir / "data.json"
    if not data_json.exists():
        warnings.append("assets/data.json 不存在（资产未提取）")

    return len(errors) == 0, errors, warnings


def validate_project(project_dir: Path, logger) -> tuple[int, int]:
    """Run all validation checks.

    Returns:
        Tuple of (error_count, warning_count).
    """
    total_errors = 0
    total_warnings = 0

    logger.info("=" * 50)
    logger.info(f"验证项目: {project_dir.name}")
    logger.info("=" * 50)

    # 1. Project config
    logger.info("\n[1/5] 检查项目配置...")
    ok, errors = check_project_json(project_dir)
    if ok:
        logger.info("  ✓ project.json 有效")
    else:
        for e in errors:
            logger.error(f"  ✗ {e}")
            total_errors += 1

    # 2. Directory structure
    logger.info("\n[2/5] 检查目录结构...")
    ok, errors, warnings = check_directory_structure(project_dir)
    if ok:
        logger.info("  ✓ 必需目录完整")
    else:
        for e in errors:
            logger.error(f"  ✗ {e}")
            total_errors += 1
    for w in warnings:
        logger.warning(f"  ! {w}")
        total_warnings += 1

    # 3. Storyline
    logger.info("\n[3/5] 检查故事线...")
    ok, errors = check_storyline(project_dir)
    if ok:
        logger.info("  ✓ storyline.md 结构完整")
    else:
        for e in errors:
            logger.warning(f"  ! {e}")
            total_warnings += 1

    # 4. Outlines
    logger.info("\n[4/5] 检查大纲...")
    ok, errors, warnings = check_outlines(project_dir)
    if ok:
        logger.info("  ✓ 大纲检查通过")
    else:
        for e in errors:
            logger.error(f"  ✗ {e}")
            total_errors += 1
    for w in warnings:
        logger.warning(f"  ! {w}")
        total_warnings += 1

    # 5. Assets
    logger.info("\n[5/5] 检查资产...")
    ok, errors, warnings = check_assets(project_dir)
    if ok:
        logger.info("  ✓ 资产检查通过")
    else:
        for e in errors:
            logger.error(f"  ✗ {e}")
            total_errors += 1
    for w in warnings:
        logger.warning(f"  ! {w}")
        total_warnings += 1

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("验证结果")
    logger.info("=" * 50)
    logger.info(f"错误: {total_errors}")
    logger.info(f"警告: {total_warnings}")

    if total_errors == 0 and total_warnings == 0:
        logger.info("\n✓ 项目验证通过！")
    elif total_errors == 0:
        logger.info("\n⚠ 项目验证通过（有警告）")
    else:
        logger.error("\n✗ 项目验证失败")

    logger.info("=" * 50)

    return total_errors, total_warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Toonany project structure")
    parser.add_argument("--project", "-p", default=".", help="Project directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    project_dir = Path(args.project)
    if not project_dir.exists():
        print(f"项目目录不存在: {project_dir}")
        return 1

    logger = setup_logger("validate_project", verbose=args.verbose)
    errors, warnings = validate_project(project_dir, logger)

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
