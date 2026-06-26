#!/usr/bin/env python3
"""
baseline_test.py — Synapse Wiki 基线测试

测试所有核心功能：
1. wiki_init - 初始化 Wiki
2. wiki_ingest - 摄取资料
3. wiki_lint - 健康检查
4. wiki_query - 查询知识
"""

import sys
import os
from pathlib import Path
import subprocess
import shutil

# Colors for output
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'

def log(msg, color=Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")

def run_script(script_path, args):
    """Run a Python script and return result."""
    try:
        result = subprocess.run(
            ['python3', str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

TEST_WIKI = Path('/tmp/synapse-test-wiki')
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'

def cleanup():
    """Clean up test directory."""
    if TEST_WIKI.exists():
        shutil.rmtree(TEST_WIKI, ignore_errors=True)

def test_wiki_init():
    """Test 1: Initialize Wiki."""
    log('\n[Test 1] wiki_init - Initialize Wiki', Colors.BLUE)
    cleanup()

    code, stdout, stderr = run_script(SCRIPT_DIR / 'scaffold.py', [str(TEST_WIKI), '测试知识库'])

    if code == 0 and 'Created' in stdout:
        log('  ✓ PASS: Wiki initialized', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {stderr or stdout}', Colors.RED)
        return False

def test_wiki_ingest():
    """Test 2: Ingest Source."""
    log('\n[Test 2] wiki_ingest - Ingest Source', Colors.BLUE)

    # Create test article
    article_dir = TEST_WIKI / 'raw' / 'articles'
    article_dir.mkdir(parents=True, exist_ok=True)
    article_path = article_dir / 'test.md'
    article_path.write_text('''---
title: 测试文章
---

# 测试文章

这是一篇测试文章。

## 核心思想

测试的核心思想。

## 关键概念

测试的关键概念。
''', encoding='utf-8')

    code, stdout, stderr = run_script(SCRIPT_DIR / 'ingest.py', [str(TEST_WIKI), str(article_path)])

    if code == 0 and 'Created' in stdout:
        log('  ✓ PASS: Source ingested', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {stderr or stdout}', Colors.RED)
        return False

def test_wiki_lint():
    """Test 3: Health Check."""
    log('\n[Test 3] wiki_lint - Health Check', Colors.BLUE)

    code, stdout, stderr = run_script(SCRIPT_DIR / 'lint_wiki.py', [str(TEST_WIKI)])

    # Lint 返回 0=无问题，1=发现问题，两者都是正常运行
    # 关键是有输出表明检查已执行
    if code in [0, 1]:
        if 'Wiki pages' in stdout or 'issues found' in stdout or 'ok' in stdout.lower() or 'Checking' in stdout:
            log('  ✓ PASS: Lint completed', Colors.GREEN)
            return True
        else:
            log(f'  ✗ FAIL: Lint output异常：{stdout[:100]}', Colors.RED)
            return False
    else:
        log(f'  ✗ FAIL: Lint 执行失败：{stderr or stdout}', Colors.RED)
        return False

def test_wiki_query():
    """Test 4: Query Knowledge."""
    log('\n[Test 4] wiki_query - Query Knowledge', Colors.BLUE)

    code, stdout, stderr = run_script(SCRIPT_DIR / 'query.py', [str(TEST_WIKI), '测试'])

    if code == 0 and ('查询' in stdout or '没有找到' in stdout or 'Querying' in stdout):
        log('  ✓ PASS: Query completed', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {stderr or stdout}', Colors.RED)
        return False

def main():
    log('\n' + '=' * 60, Colors.BLUE)
    log('Synapse Wiki Baseline Tests', Colors.BLUE)
    log('=' * 60, Colors.BLUE)

    results = []
    results.append(test_wiki_init())
    results.append(test_wiki_ingest())
    results.append(test_wiki_lint())
    results.append(test_wiki_query())

    cleanup()

    passed = sum(results)
    total = len(results)

    log('\n' + '=' * 60, Colors.BLUE)
    log(f'Results: {passed}/{total} tests passed', Colors.GREEN if passed == total else Colors.RED)
    log('=' * 60 + '\n', Colors.BLUE)

    # Note: Integration tests available in integration_test.py (5 additional tests)
    # Run: python3 tests/integration_test.py

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
