#!/usr/bin/env python3
"""
验证项目结构
"""

import os
import sys
from pathlib import Path


def check_directory_structure():
    """检查目录结构"""
    
    base_dir = Path(__file__).parent
    
    required_dirs = [
        base_dir / 'src' / 'sum2slides',
        base_dir / 'tests',
        base_dir / 'docs',
        base_dir / 'examples',
        base_dir / 'config',
        base_dir / 'scripts',
    ]
    
    required_files = [
        base_dir / 'SKILL.md',
        base_dir / 'README.md',
        base_dir / 'pyproject.toml',
        base_dir / 'requirements.txt',
        base_dir / 'requirements-dev.txt',
        base_dir / 'src' / 'sum2slides' / '__init__.py',
        base_dir / 'src' / 'sum2slides' / 'api.py',
        base_dir / 'src' / 'sum2slides' / 'cli.py',
    ]
    
    print("检查目录结构...")
    
    all_ok = True
    
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✓ 目录存在: {dir_path.relative_to(base_dir)}")
        else:
            print(f"✗ 目录缺失: {dir_path.relative_to(base_dir)}")
            all_ok = False
    
    for file_path in required_files:
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✓ 文件存在: {file_path.relative_to(base_dir)} ({size} 字节)")
        else:
            print(f"✗ 文件缺失: {file_path.relative_to(base_dir)}")
            all_ok = False
    
    return all_ok


def check_source_files():
    """检查源代码文件"""
    
    base_dir = Path(__file__).parent
    src_dir = base_dir / 'src' / 'sum2slides'
    
    print("\n检查源代码文件...")
    
    # 统计文件数量和大小
    python_files = list(src_dir.rglob('*.py'))
    
    if not python_files:
        print("✗ 没有找到Python文件")
        return False
    
    print(f"找到 {len(python_files)} 个Python文件:")
    
    total_size = 0
    for file_path in python_files:
        size = file_path.stat().st_size
        total_size += size
        rel_path = file_path.relative_to(base_dir)
        print(f"  {rel_path}: {size} 字节")
    
    print(f"总代码量: {total_size} 字节 ({total_size/1024:.1f} KB)")
    
    # 检查关键模块
    key_modules = [
        'core/parser.py',
        'core/analyzer.py',
        'core/generator.py',
        'core/formatter.py',
        'core/validator.py',
        'exporters/pptx.py',
        'models/document.py',
        'models/slide.py',
        'models/template.py',
    ]
    
    print("\n检查关键模块...")
    all_modules_ok = True
    
    for module in key_modules:
        module_path = src_dir / module
        if module_path.exists():
            size = module_path.stat().st_size
            print(f"✓ {module}: {size} 字节")
        else:
            print(f"✗ {module}: 缺失")
            all_modules_ok = False
    
    return all_modules_ok


def check_documentation():
    """检查文档"""
    
    base_dir = Path(__file__).parent
    
    print("\n检查文档...")
    
    docs = [
        ('SKILL.md', '技能主文档'),
        ('README.md', '项目说明'),
        ('config/default.yaml', '默认配置'),
        ('examples/input/meeting_notes.txt', '会议纪要示例'),
        ('examples/input/research_summary.md', '研究报告示例'),
    ]
    
    all_ok = True
    
    for file_name, description in docs:
        file_path = base_dir / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✓ {description}: {file_name} ({size} 字节)")
        else:
            print(f"✗ {description}: {file_name} 缺失")
            all_ok = False
    
    return all_ok


def check_tests():
    """检查测试文件"""
    
    base_dir = Path(__file__).parent
    tests_dir = base_dir / 'tests'
    
    print("\n检查测试文件...")
    
    if not tests_dir.exists():
        print("✗ 测试目录不存在")
        return False
    
    test_files = list(tests_dir.rglob('test_*.py'))
    
    if not test_files:
        print("✗ 没有找到测试文件")
        return False
    
    print(f"找到 {len(test_files)} 个测试文件:")
    
    for test_file in test_files:
        size = test_file.stat().st_size
        rel_path = test_file.relative_to(base_dir)
        print(f"  {rel_path}: {size} 字节")
    
    return True


def check_scripts():
    """检查脚本文件"""
    
    base_dir = Path(__file__).parent
    scripts_dir = base_dir / 'scripts'
    
    print("\n检查脚本文件...")
    
    if not scripts_dir.exists():
        print("✗ 脚本目录不存在")
        return False
    
    script_files = [
        'setup.py',
        'quick_test.py',
    ]
    
    all_ok = True
    
    for script in script_files:
        script_path = scripts_dir / script
        if script_path.exists():
            size = script_path.stat().st_size
            print(f"✓ {script}: {size} 字节")
        else:
            print(f"✗ {script}: 缺失")
            all_ok = False
    
    return all_ok


def main():
    """主函数"""
    
    print("Sum2Slides v1.0.1 项目结构验证")
    print("="*50)
    
    checks = [
        ("目录结构", check_directory_structure),
        ("源代码", check_source_files),
        ("文档", check_documentation),
        ("测试", check_tests),
        ("脚本", check_scripts),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{check_name}检查...")
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"✗ 检查异常: {e}")
            results.append((check_name, False))
    
    # 显示结果
    print("\n" + "="*50)
    print("验证结果:")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for check_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{check_name:15} {status}")
        if success:
            passed += 1
    
    print("="*50)
    print(f"总计: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("\n✓ 项目结构完整，Sum2Slides v1.0.1 已就绪！")
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行测试: pytest")
        print("3. 安装包: pip install -e .")
        print("4. 使用: sum2slides convert '你的文本' --output test.pptx")
        return 0
    else:
        print(f"\n✗ {total - passed} 项检查失败，需要修复。")
        return 1


if __name__ == '__main__':
    sys.exit(main())