#!/usr/bin/env python3
"""
Study Buddy 命令验证测试
"""

import subprocess
import sys
import os
import tempfile

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=5
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def test_help():
    """测试 help 命令"""
    print("=== 测试 help ===")
    # 测试 help 子命令
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py help")
    if success and "Study Buddy" in stdout:
        print("✅ help 子命令正常")
        return True
    else:
        print(f"❌ help 失败: {stderr}")
        return False

def test_data():
    """测试 data 命令"""
    print("\n=== 测试 data ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py data")
    if success and "数据目录" in stdout:
        print("✅ data 正常")
        return True
    else:
        print(f"❌ data 失败: {stderr}")
        return False

def test_today():
    """测试 today 命令"""
    print("\n=== 测试 today ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py today")
    if success and ("今日任务" in stdout or "今日学习" in stdout or "还没有学习档案" in stdout):
        print("✅ today 正常")
        return True
    else:
        print(f"❌ today 失败: {stderr}")
        return False

def test_progress():
    """测试 progress 命令"""
    print("\n=== 测试 progress ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py progress")
    if success and ("学习进度" in stdout or "累计学习" in stdout or "还没有学习档案" in stdout):
        print("✅ progress 正常")
        return True
    else:
        print(f"❌ progress 失败: {stderr}")
        return False

def test_plan():
    """测试 plan 命令"""
    print("\n=== 测试 plan ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py plan")
    if success and ("学习计划" in stdout or "阶段" in stdout or "还没有学习档案" in stdout):
        print("✅ plan 正常")
        return True
    else:
        print(f"❌ plan 失败: {stderr}")
        return False

def test_report():
    """测试 report 命令"""
    print("\n=== 测试 report ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py report")
    if success and ("学习报告" in stdout or "学习概况" in stdout or "还没有学习档案" in stdout):
        print("✅ report 正常")
        return True
    else:
        print(f"❌ report 失败: {stderr}")
        return False

def test_wrong_list():
    """测试 wrong list 命令"""
    print("\n=== 测试 wrong list ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py wrong list")
    if success and ("错题本" in stdout or "错题" in stdout or "还没有学习档案" in stdout):
        print("✅ wrong list 正常")
        return True
    else:
        print(f"❌ wrong list 失败: {stderr}")
        return False

def test_feedback():
    """测试 feedback 命令"""
    print("\n=== 测试 feedback ===")
    success, stdout, stderr = run_command("python3 scripts/study-buddy.py feedback")
    if success and ("学习反馈" in stdout or "学习建议" in stdout or "还没有学习档案" in stdout):
        print("✅ feedback 正常")
        return True
    else:
        print(f"❌ feedback 失败: {stderr}")
        return False

def main():
    print("🧪 Study Buddy 命令验证测试\n")
    
    # 切换到正确目录
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    temp_dir = tempfile.TemporaryDirectory()
    os.environ["STUDY_BUDDY_HOME"] = os.path.join(temp_dir.name, "study-buddy-data")
    
    tests = [
        ("help", test_help),
        ("data", test_data),
        ("today", test_today),
        ("progress", test_progress),
        ("plan", test_plan),
        ("report", test_report),
        ("wrong list", test_wrong_list),
        ("feedback", test_feedback),
    ]
    
    passed = 0
    for name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed}/{len(tests)} 通过")
    
    try:
        if passed == len(tests):
            print("✅ 所有命令正常！")
            return 0
        else:
            print("⚠️  部分命令需要检查")
            return 1
    finally:
        temp_dir.cleanup()

if __name__ == "__main__":
    sys.exit(main())
