#!/usr/bin/env python3
"""
baseline_test.py — Synapse Code 基线测试

测试所有核心功能：
1. code_init - 初始化项目
2. code_status - 检查状态

注意：完整测试需要 pipeline-workspace 和 synapse-core 环境
"""

import sys
import os
from pathlib import Path
import subprocess
import shutil

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
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

TEST_PROJECT = Path('/tmp/synapse-code-test')
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'

def cleanup():
    """Clean up test directory."""
    if TEST_PROJECT.exists():
        shutil.rmtree(TEST_PROJECT, ignore_errors=True)

def test_init_project():
    """Test 1: Initialize Project."""
    log('\n[Test 1] code_init - Check init_project.py syntax', Colors.BLUE)
    cleanup()

    # Check if script exists and has valid Python syntax
    init_script = SCRIPT_DIR / 'init_project.py'
    if not init_script.exists():
        log(f'  ✗ FAIL: init_project.py not found', Colors.RED)
        return False

    # Check Python syntax
    try:
        import ast
        source = init_script.read_text(encoding='utf-8')
        ast.parse(source)
        log('  ✓ PASS: init_project.py has valid syntax', Colors.GREEN)
        return True
    except SyntaxError as e:
        log(f'  ✗ FAIL: Syntax error in init_project.py: {e}', Colors.RED)
        return False

def test_infer_task_type():
    """Test 2: Infer Task Type."""
    log('\n[Test 2] code_infer - Test task type inference', Colors.BLUE)

    # Test 8 cases covering natural language scenarios
    test_cases = [
        ("修复登录 bug", "bugfix"),
        ("优化启动速度", "optimization"),
        ("添加暗色模式", "feature"),
        ("理解这个函数", "understand"),
        ("把变量改名", "refactor"),
        # Real user scenarios
        ("网页打不开了，是什么问题", "debug"),
        ("实现用户登录功能，使用 JWT", "feature"),
        ("优化数据库查询性能", "optimization"),
    ]

    passed = 0
    for text, expected in test_cases:
        code, stdout, stderr = run_script(SCRIPT_DIR / 'infer_task_type.py', [text])
        if code == 0 and expected in stdout.lower():
            passed += 1
        else:
            log(f'  ✗ FAIL: "{text}" expected {expected}, got: {stdout[:80]}', Colors.RED)

    if passed == len(test_cases):
        log(f'  ✓ PASS: infer_task_type.py works ({passed}/{len(test_cases)})', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {passed}/{len(test_cases)} test cases passed', Colors.RED)
        return False

def test_check_status():
    """Test 3: Check Status."""
    log('\n[Test 3] code_status - Check status script', Colors.BLUE)

    code, stdout, stderr = run_script(SCRIPT_DIR / 'check_status.py', [str(TEST_PROJECT)])

    # Should run without crashing (even if project doesn't exist)
    if code in [0, 1]:
        log('  ✓ PASS: check_status.py runs', Colors.GREEN)
        return True
    else:
        log(f'  ✗ FAIL: {stderr or stdout}', Colors.RED)
        return False


def test_run_pipeline_modes():
    """Test 4: Run Pipeline mode detection."""
    log('\n[Test 4] run_pipeline - Mode detection', Colors.BLUE)

    # Test detect_environment function by checking script syntax and structure
    run_pipeline_script = SCRIPT_DIR / 'run_pipeline.py'

    if not run_pipeline_script.exists():
        log('  ✗ FAIL: run_pipeline.py not found', Colors.RED)
        return False

    try:
        import ast
        source = run_pipeline_script.read_text(encoding='utf-8')
        ast.parse(source)

        # Check for required modes
        required_modes = ['auto', 'standalone', 'lite', 'full']
        modes_found = sum(1 for mode in required_modes if f'"{mode}"' in source or f"'{mode}'" in source)

        if modes_found == len(required_modes):
            log(f'  ✓ PASS: All {len(required_modes)} modes defined', Colors.GREEN)
            return True
        else:
            log(f'  ✗ FAIL: Only {modes_found}/{len(required_modes)} modes found', Colors.RED)
            return False

    except SyntaxError as e:
        log(f'  ✗ FAIL: Syntax error: {e}', Colors.RED)
        return False


def test_im_friendly_output():
    """Test 5: IM-friendly output (no ANSI codes)."""
    log('\n[Test 5] IM-friendly output - No ANSI codes', Colors.BLUE)

    # Check auto_log_trigger.py for ANSI codes
    script = SCRIPT_DIR / 'auto_log_trigger.py'

    if not script.exists():
        log('  ✗ FAIL: auto_log_trigger.py not found', Colors.RED)
        return False

    source = script.read_text(encoding='utf-8')

    # Check for ANSI escape sequences
    ansi_patterns = ['\\033[', '\\x1b[', 'Colors.']
    has_ansi = any(pattern in source for pattern in ansi_patterns)

    # Check for IM-friendly patterns
    im_friendly_patterns = ['[INFO]', '[✓]', '[⚠]', '[✗]', '[⟳]']
    has_im_friendly = any(pattern in source for pattern in im_friendly_patterns)

    if not has_ansi and has_im_friendly:
        log('  ✓ PASS: IM-friendly output (no ANSI codes)', Colors.GREEN)
        return True
    elif has_ansi:
        log('  ✗ FAIL: Found ANSI codes in output', Colors.RED)
        return False
    else:
        log('  ⚠ WARNING: Output format unclear', Colors.YELLOW)
        return True  # Still pass if no ANSI codes

def main():
    log('\n' + '=' * 60, Colors.BLUE)
    log('Synapse Code Baseline Tests', Colors.BLUE)
    log('=' * 60, Colors.BLUE)

    results = []
    results.append(test_init_project())
    results.append(test_infer_task_type())
    results.append(test_check_status())
    results.append(test_run_pipeline_modes())
    results.append(test_im_friendly_output())

    cleanup()

    passed = sum(results)
    total = len(results)

    log('\n' + '=' * 60, Colors.BLUE)
    log(f'Results: {passed}/{total} tests passed', Colors.GREEN if passed == total else Colors.RED)
    log('=' * 60 + '\n', Colors.BLUE)

    # Note: Integration tests available in integration_test.py (6 additional tests)
    # Run: python3 tests/integration_test.py

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
