#!/usr/bin/env python3
"""
测试脚本 - 验证 skill 安装和配置
"""
import sys
import subprocess
from pathlib import Path


def test_browser_harness():
    """测试 Browser Harness 是否可用"""
    print("测试 1: Browser Harness 可用性...")
    try:
        result = subprocess.run(
            ["browser-harness", "--doctor"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "daemon alive" in result.stdout or "[ok  ] daemon alive" in result.stdout:
            print("  ✅ Browser Harness 正常")
            return True
        else:
            print("  ❌ Browser Harness daemon 未运行")
            print("  提示：运行 browser-harness --setup")
            return False
    except FileNotFoundError:
        print("  ❌ browser-harness 命令未找到")
        print("  提示：检查安装路径")
        return False
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_config_file():
    """测试配置文件是否存在"""
    print("\n测试 2: 配置文件...")
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        print(f"  ✅ 配置文件存在: {config_path}")
        return True
    else:
        print(f"  ❌ 配置文件不存在: {config_path}")
        return False


def test_scripts():
    """测试脚本文件是否存在"""
    print("\n测试 3: 脚本文件...")
    scripts_dir = Path(__file__).parent
    required_scripts = [
        "collect_articles.py",
        "utils.py"
    ]
    
    all_exist = True
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} 不存在")
            all_exist = False
    
    return all_exist


def test_save_dir():
    """测试保存目录是否可写"""
    print("\n测试 4: 保存目录...")
    save_dir = Path.home() / ".openclaw/workspace/knowledge/wechat"
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        test_file = save_dir / ".test"
        test_file.write_text("test")
        test_file.unlink()
        print(f"  ✅ 保存目录可写: {save_dir}")
        return True
    except Exception as e:
        print(f"  ❌ 保存目录不可写: {e}")
        return False


def main():
    print("=== 微信公众号文章采集器 - 安装测试 ===\n")
    
    tests = [
        test_browser_harness,
        test_config_file,
        test_scripts,
        test_save_dir
    ]
    
    results = [test() for test in tests]
    
    print("\n=== 测试结果 ===")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！可以开始使用了。")
        print("\n运行命令：")
        print("  python3 scripts/collect_articles.py")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查上述错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
