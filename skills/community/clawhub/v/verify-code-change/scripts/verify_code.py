#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码变更验证器
运行应用或测试命令，验证代码变更是否破坏现有功能
"""

import sys
import asyncio
import argparse
import subprocess
from typing import Optional


async def verify_code_change(
    test_command: str,
    expected_behavior: Optional[str] = None,
    timeout: int = 60
) -> bool:
    """
    验证代码变更

    Args:
        test_command: 测试命令
        expected_behavior: 预期行为描述
        timeout: 超时时间（秒）

    Returns:
        是否验证通过
    """
    print(f"✓ 执行测试命令: {test_command}")
    print(f"✓ 超时时间: {timeout} 秒")
    if expected_behavior:
        print(f"✓ 预期行为: {expected_behavior}")
    print()

    try:
        # 执行测试命令
        process = await asyncio.create_subprocess_exec(
            *test_command.split(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd='.'  # 在当前目录执行
        )

        # 等待结果
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            # 超时，终止进程
            try:
                process.kill()
                await process.wait()
            except Exception:
                pass

            print("✗ 验证失败: 测试超时")
            print(f"  命令: {test_command}")
            print(f"  超时: {timeout} 秒")
            print("\n建议:")
            print("  1. 增加超时时间（--timeout 参数）")
            print("  2. 检查测试命令是否正确")
            print("  3. 确认测试环境是否正常")
            return False

        # 解码输出
        stdout_text = stdout.decode('utf-8', errors='ignore')
        stderr_text = stderr.decode('utf-8', errors='ignore')

        # 检查返回码
        if process.returncode == 0:
            print("✓ 验证通过: 测试成功")
            print()
            if stdout_text.strip():
                print("=== 标准输出 ===")
                print(stdout_text)
            if stderr_text.strip():
                print("=== 错误输出 ===")
                print(stderr_text)
            return True
        else:
            print("✗ 验证失败: 测试未通过")
            print(f"  返回码: {process.returncode}")
            print()
            if stdout_text.strip():
                print("=== 标准输出 ===")
                print(stdout_text)
            if stderr_text.strip():
                print("=== 错误输出 ===")
                print(stderr_text)

            # 分析常见错误
            stderr_lower = stderr_text.lower()
            if 'error' in stderr_lower or 'fail' in stderr_lower:
                print("\n可能的错误原因:")
                if 'import' in stderr_lower or 'module' in stderr_lower:
                    print("  - 缺少依赖包")
                if 'syntax' in stderr_lower or 'parse' in stderr_lower:
                    print("  - 语法错误")
                if 'test' in stderr_lower:
                    print("  - 测试失败，检查代码逻辑")
                if 'timeout' in stderr_lower:
                    print("  - 测试超时，考虑增加超时时间")

            return False

    except FileNotFoundError:
        print(f"✗ 验证失败: 命令不存在")
        print(f"  命令: {test_command.split()[0]}")
        print("\n建议:")
        print("  1. 检查命令是否拼写正确")
        print("  2. 确认命令是否在 PATH 中")
        print("  3. 尝试使用完整路径")
        return False
    except PermissionError:
        print(f"✗ 验证失败: 权限不足")
        print(f"  命令: {test_command}")
        print("\n建议:")
        print("  1. 检查文件/目录权限")
        print("  2. 尝试使用 sudo (Linux/macOS)")
        print("  3. 以管理员身份运行 (Windows)")
        return False
    except Exception as e:
        print(f"✗ 验证失败: 执行错误")
        print(f"  错误: {type(e).__name__}: {e}")
        print(f"  命令: {test_command}")
        print()
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='代码变更验证器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --test-command "npm test"
  %(prog)s --test-command "python -m pytest" --timeout 120
  %(prog)s --test-command "cargo test" --expected-behavior "所有测试通过"
        """
    )
    parser.add_argument('--test-command', '-c', required=True,
                       help='测试命令（如 npm test, python -m pytest）')
    parser.add_argument('--expected-behavior', '-e',
                       help='预期行为描述')
    parser.add_argument('--timeout', '-t', type=int, default=60,
                       help='超时时间（秒，默认: 60）')

    args = parser.parse_args()

    # 执行验证
    success = asyncio.run(verify_code_change(
        test_command=args.test_command,
        expected_behavior=args.expected_behavior,
        timeout=args.timeout
    ))

    # 返回码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
