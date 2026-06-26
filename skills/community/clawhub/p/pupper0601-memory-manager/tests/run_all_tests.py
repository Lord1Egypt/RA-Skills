#!/usr/bin/env python3
"""
run_all_tests.py - 运行所有单元测试
"""

import os
import sys
import io

# Windows GBK 环境支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_test_file(filepath):
    """运行单个测试文件"""
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"Running: {os.path.basename(filepath)}")
    print(sep)
    result = os.system(f'python "{filepath}"')
    return result == 0

def main():
    tests_dir = os.path.dirname(__file__)

    test_files = [
        os.path.join(tests_dir, "memory_embed_test.py"),
        os.path.join(tests_dir, "memory_search_test.py"),
        os.path.join(tests_dir, "memory_access_log_test.py"),
    ]

    print("[Rocket] Memory Manager - Unit Test Suite")
    print("=" * 60)

    results = []
    for tf in test_files:
        if os.path.exists(tf):
            results.append(run_test_file(tf))
        else:
            print(f"[Warning] Test file not found: {tf}")

    sep = "=" * 60
    print(f"\n{sep}")
    print("Stats - Final Results")
    print(sep)

    passed = sum(1 for r in results if r)
    total = len(results)

    if passed == total:
        print(f"[OK] All {total} test suites passed!")
        return 0
    else:
        print(f"[FAIL] {passed}/{total} test suites passed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
