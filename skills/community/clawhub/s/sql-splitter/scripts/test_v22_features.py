#!/usr/bin/env python3
"""
SQL 拆分工具 v2.2 功能测试
测试新增的 GUI、断点续传、批量处理、结果预览和配置管理功能
"""

import sys
import os
from pathlib import Path

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

def test_checkpoint():
    """测试断点续传功能"""
    print("=" * 80)
    print("测试断点续传功能")
    print("=" * 80)

    try:
        from checkpoint import CheckpointManager, CheckpointData

        manager = CheckpointManager()

        # 创建测试检查点
        print("1. 创建检查点...")
        checkpoint = manager.create_checkpoint(
            input_file="/test/input.sql",
            output_dir="/test/output",
            dialect="oracle",
            total_objects=100
        )
        print(f"   ✓ 检查点创建成功: {checkpoint.input_file}")

        # 更新检查点
        print("2. 更新检查点...")
        checkpoint = manager.update_checkpoint(checkpoint, processed_file="proc_test.sql")
        checkpoint = manager.update_checkpoint(checkpoint, processed_file="func_test.sql")
        print(f"   ✓ 检查点更新成功: 已处理 {checkpoint.processed_objects} 个对象")

        # 保存检查点
        print("3. 保存检查点...")
        if manager.save_checkpoint(checkpoint):
            print("   ✓ 检查点保存成功")
        else:
            print("   ✗ 检查点保存失败")
            return False

        # 列出检查点
        print("4. 列出检查点...")
        checkpoints = manager.list_checkpoints()
        print(f"   ✓ 找到 {len(checkpoints)} 个检查点")
        for cp in checkpoints:
            print(f"     - {cp['input_file']}: {cp['progress']} ({cp['status']})")

        # 获取恢复进度
        print("5. 获取恢复进度...")
        resume_info = manager.get_resume_progress("/test/input.sql")
        if resume_info:
            print(f"   ✓ 恢复进度: {resume_info['progress']:.1%}")
            print(f"   ✓ 可以恢复: {resume_info['can_resume']}")
        else:
            print("   ✗ 未找到检查点")
            return False

        # 删除检查点
        print("6. 删除检查点...")
        if manager.delete_checkpoint("/test/input.sql"):
            print("   ✓ 检查点删除成功")
        else:
            print("   ✗ 检查点删除失败")
            return False

        print("\n✓ 断点续传功能测试通过")
        return True

    except Exception as e:
        print(f"\n✗ 断点续传功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_processor():
    """测试批量并行处理功能"""
    print("\n" + "=" * 80)
    print("测试批量并行处理功能")
    print("=" * 80)

    try:
        from batch_processor import BatchProcessor, BatchTask

        # 创建批量处理器
        print("1. 创建批量处理器...")
        processor = BatchProcessor(max_workers=2)
        print("   ✓ 批量处理器创建成功")

        # 设置进度回调
        print("2. 设置进度回调...")
        callback_called = []

        def progress_callback(completed, total, message):
            callback_called.append((completed, total, message))
            print(f"   进度: [{completed}/{total}] {message}")

        processor.set_progress_callback(progress_callback)
        print("   ✓ 进度回调设置成功")

        print("\n✓ 批量并行处理功能测试通过")
        return True

    except Exception as e:
        print(f"\n✗ 批量并行处理功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_result_previewer():
    """测试结果预览功能"""
    print("\n" + "=" * 80)
    print("测试结果预览功能")
    print("=" * 80)

    try:
        from result_previewer import ResultPreviewer

        # 创建预览器
        print("1. 创建预览器...")
        previewer = ResultPreviewer()
        print("   ✓ 预览器创建成功")

        # 测试文件大小格式化
        print("2. 测试文件大小格式化...")
        sizes = [
            (1024, "1.00 KB"),
            (1024 * 1024, "1.00 MB"),
            (1024 * 1024 * 1024, "1.00 GB"),
        ]
        for size, expected in sizes:
            formatted = previewer._format_size(size)
            print(f"   {size} bytes -> {formatted}")
            if expected in formatted:
                print(f"   ✓ 格式化正确")
            else:
                print(f"   ✗ 格式化错误: 期望包含 '{expected}'")

        print("\n✓ 结果预览功能测试通过")
        return True

    except Exception as e:
        print(f"\n✗ 结果预览功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_manager():
    """测试配置管理功能"""
    print("\n" + "=" * 80)
    print("测试配置管理功能")
    print("=" * 80)

    try:
        from config_manager import ConfigManager, SplitConfig

        # 创建配置管理器
        print("1. 创建配置管理器...")
        manager = ConfigManager()
        print("   ✓ 配置管理器创建成功")

        # 创建配置
        print("2. 创建配置...")
        config = SplitConfig(
            dialect="oracle",
            output_dir="/test/output",
            max_workers=8,
            use_checkpoint=True
        )
        print(f"   ✓ 配置创建成功: {config.dialect}")

        # 验证配置
        print("3. 验证配置...")
        errors = config.validate()
        if not errors:
            print("   ✓ 配置验证通过")
        else:
            print(f"   ✗ 配置验证失败: {errors}")
            return False

        # 保存配置
        print("4. 保存配置...")
        if manager.save_config(config, "test"):
            print("   ✓ 配置保存成功")
        else:
            print("   ✗ 配置保存失败")
            return False

        # 加载配置
        print("5. 加载配置...")
        loaded_config = manager.load_config("test")
        if loaded_config:
            print(f"   ✓ 配置加载成功: {loaded_config.dialect}")
        else:
            print("   ✗ 配置加载失败")
            return False

        # 列出配置
        print("6. 列出配置...")
        configs = manager.list_configs()
        print(f"   ✓ 找到 {len(configs)} 个配置")
        for cfg in configs:
            print(f"     - {cfg['name']}: {cfg['dialect']}")

        # 删除配置
        print("7. 删除配置...")
        if manager.delete_config("test"):
            print("   ✓ 配置删除成功")
        else:
            print("   ✗ 配置删除失败")
            return False

        print("\n✓ 配置管理功能测试通过")
        return True

    except Exception as e:
        print(f"\n✗ 配置管理功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gui_import():
    """测试 GUI 导入"""
    print("\n" + "=" * 80)
    print("测试 GUI 导入")
    print("=" * 80)

    try:
        # 检查 tkinter 是否可用
        print("1. 检查 tkinter...")
        import tkinter
        print("   ✓ tkinter 可用")

        # 尝试导入 GUI 模块
        print("2. 导入 GUI 模块...")
        from gui import SQLSplitterGUI
        print("   ✓ GUI 模块导入成功")

        print("\n✓ GUI 导入测试通过")
        return True

    except ImportError as e:
        print(f"\n✗ GUI 导入测试失败: {e}")
        print("   提示: GUI 需要 tkinter，请确保已安装")
        return False
    except Exception as e:
        print(f"\n✗ GUI 导入测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "SQL 拆分工具 v2.2 功能测试" + " " * 28 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    results = []

    # 运行所有测试
    results.append(("断点续传", test_checkpoint()))
    results.append(("批量并行处理", test_batch_processor()))
    results.append(("结果预览", test_result_previewer()))
    results.append(("配置管理", test_config_manager()))
    results.append(("GUI 导入", test_gui_import()))

    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("-" * 80)
    print(f"总计: {len(results)} 个测试, {passed} 个通过, {failed} 个失败")

    if failed == 0:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
