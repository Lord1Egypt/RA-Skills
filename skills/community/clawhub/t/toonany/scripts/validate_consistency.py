#!/usr/bin/env python3
"""Validate cross-file consistency (character names, scene names, style drift)."""

import argparse
import sys
from pathlib import Path

from utils.consistency import ConsistencyChecker
from utils.dependency_tracker import DependencyTracker
from utils.logger import setup_logger


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate project consistency")
    parser.add_argument("--project", "-p", default=".", help="Project directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    project_dir = Path(args.project)
    if not project_dir.exists():
        print(f"项目目录不存在: {project_dir}")
        return 1

    logger = setup_logger("validate_consistency", verbose=args.verbose)

    logger.info("=" * 50)
    logger.info(f"一致性校验: {project_dir.name}")
    logger.info("=" * 50)

    # 1. Cross-file consistency
    logger.info("\n[1/2] 跨文件一致性检查...")
    checker = ConsistencyChecker(project_dir)
    result = checker.run_all()

    all_ok = result["ok"]
    for check_name, check_result in result["checks"].items():
        if check_result["ok"]:
            logger.info(f"  ✓ {check_name}: 通过")
        else:
            logger.warning(f"  ! {check_name}: 发现 {len(check_result['issues'])} 个问题")
            for issue in check_result["issues"]:
                logger.warning(f"    - {issue}")

    # 2. Dependency tracking
    logger.info("\n[2/2] 依赖追踪检查...")
    tracker = DependencyTracker(project_dir)
    stale = tracker.check_stale()

    if stale:
        logger.warning("  发现过期文件:")
        for item in stale:
            logger.warning(f"    - {item['file']}: {item['reason']}")
    else:
        logger.info("  ✓ 所有文件版本正常")

    # Summary
    logger.info("\n" + "=" * 50)
    if all_ok and not stale:
        logger.info("✓ 一致性校验通过！")
    else:
        logger.warning("⚠ 一致性校验完成（发现问题）")
    logger.info("=" * 50)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
