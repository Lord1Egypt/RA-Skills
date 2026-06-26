"""
yaoyao-memory tests
测试套件
"""

import subprocess
import sys
from pathlib import Path

# 测试目录
TESTS_DIR = Path(__file__).parent
SKILL_DIR = TESTS_DIR.parent


def run_test(script_name: str) -> bool:
    """运行单个测试脚本"""
    script_path = SKILL_DIR / "scripts" / script_name
    if not script_path.exists():
        print(f"❌ {script_name} 不存在")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {script_name}")
            return True
        else:
            print(f"❌ {script_name}: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"❌ {script_name}: {e}")
        return False


def test_health_check():
    """测试健康检查"""
    return run_test("health_check.py")


def test_search():
    """测试搜索"""
    return run_test("search.py")


def test_memory_stats():
    """测试统计"""
    return run_test("memory_stats.py")


if __name__ == "__main__":
    print("🧪 yaoyao-memory 测试套件")
    print("=" * 40)
    
    tests = [
        ("健康检查", test_health_check),
        ("搜索", test_search),
        ("统计", test_memory_stats),
    ]
    
    passed = 0
    failed = 0
    
    for name, test in tests:
        print(f"\n测试: {name}")
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 40)
    print(f"结果: {passed} 通过, {failed} 失败")
