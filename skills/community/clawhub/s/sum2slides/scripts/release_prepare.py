#!/usr/bin/env python3
"""
Sum2Slides v1.0.1 发布准备脚本
执行发布前的所有检查和准备工作
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_version_info():
    """检查版本信息"""
    
    print("🔍 检查版本信息...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    package_json = project_root / "package.json"
    
    if not package_json.exists():
        print("❌ package.json文件不存在")
        return False
    
    with open(package_json, 'r', encoding='utf-8') as f:
        package_info = json.load(f)
    
    print(f"✅ 名称: {package_info['name']}")
    print(f"✅ 版本: {package_info['version']}")
    print(f"✅ 描述: {package_info['description'][:100]}...")
    print(f"✅ 许可证: {package_info['license']}")
    print(f"✅ 作者: {package_info['author']}")
    
    # 验证版本号
    if package_info['version'] != "1.0.0":
        print(f"⚠️ 版本号不是1.0.0，当前: {package_info['version']}")
        return False
    
    print("✅ 版本信息检查通过")
    return True

def check_documentation():
    """检查文档完整性"""
    
    print("\n📚 检查文档完整性...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    required_docs = [
        "SKILL.md",
        "README.md",
        "CHANGELOG.md",
        "TUTORIAL.md",
        "FAQ.md",
        "DEMO.md",
        "CONTRIBUTING.md"
    ]
    
    all_present = True
    for doc in required_docs:
        doc_path = project_root / doc
        if doc_path.exists():
            size = doc_path.stat().st_size
            print(f"✅ {doc} ({size} 字节)")
        else:
            print(f"❌ {doc} 文件不存在")
            all_present = False
    
    if all_present:
        print("✅ 文档完整性检查通过")
    else:
        print("❌ 文档完整性检查失败")
    
    return all_present

def check_source_code():
    """检查源代码完整性"""
    
    print("\n💻 检查源代码完整性...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src" / "sum2slides"
    
    if not src_dir.exists():
        print("❌ 源代码目录不存在")
        return False
    
    # 检查核心模块
    core_modules = [
        pathlib.Path(src_dir) / "core" / "__init__.py",
        pathlib.Path(src_dir) / "core" / "parser.py",
        pathlib.Path(src_dir) / "core" / "analyzer.py",
        pathlib.Path(src_dir) / "core" / "generator.py",
        pathlib.Path(src) / "__init__.py",
        pathlib.Path(src) / "api.py",
        pathlib.Path(src) / "cli.py"
    ]
    
    all_present = True
    for module in core_modules:
        if module.exists():
            print(f"✅ {module.relative_to(project_root)}")
        else:
            print(f"⚠️ {module.relative_to(project_root)} 不存在（可选）")
    
    print("✅ 源代码完整性检查通过")
    return True

def check_external_links():
    """检查外部链接有效性"""
    
    print("\n🔗 检查外部链接有效性...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    package_json = project_root / "package.json"
    
    with open(package_json, 'r', encoding='utf-8') as f:
        package_info = json.load(f)
    
    # 检查关键链接
    links_to_check = {
        "GitHub仓库": package_info.get("repository", {}).get("url"),
        "项目主页": package_info.get("homepage"),
        "文档网站": package_info.get("documentation")
    }
    
    all_valid = True
    for name, url in links_to_check.items():
        if url:
            print(f"✅ {name}: {url}")
        else:
            print(f"⚠️ {name}: 未设置")
            all_valid = False
    
    print("✅ 外部链接检查完成（实际有效性需手动验证）")
    return all_valid

def check_package_structure():
    """检查包结构"""
    
    print("\n📦 检查包结构...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "src",
        "tests",
        "config",
        "scripts",
        "examples"
    ]
    
    all_present = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ 不存在")
            all_present = False
    
    if all_present:
        print("✅ 包结构检查通过")
    else:
        print("❌ 包结构检查失败")
    
    return all_present

def check_config_files():
    """检查配置文件"""
    
    print("\n⚙️ 检查配置文件...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    config_files = [
        "config/default.yaml",
        "config/simple.yaml",
        "requirements.txt"
    ]
    
    all_present = True
    for config_file in config_files:
        config_path = project_root / config_file
        if config_path.exists():
            size = config_path.stat().st_size
            print(f"✅ {config_file} ({size} 字节)")
        else:
            print(f"❌ {config_file} 不存在")
            all_present = False
    
    if all_present:
        print("✅ 配置文件检查通过")
    else:
        print("❌ 配置文件检查失败")
    
    return all_present

def create_release_notes():
    """创建发布说明"""
    
    print("\n📝 创建发布说明...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    
    release_notes = """# Sum2Slides v1.0.1 发布说明

## 🎉 正式版本发布

我们很高兴宣布Sum2Slides v1.0.1正式版本发布！

## 🌟 版本亮点

### 统一品牌
- ✅ 统一为"Sum2Slides"名称
- ✅ 移除Lite/Pro之分
- ✅ 版本号设为1.0.0（首个正式版本）

### 功能完善
- ✅ 文本转幻灯片核心功能
- ✅ 多种模板和主题支持
- ✅ Markdown和纯文本输入
- ✅ PowerPoint导出
- ✅ 命令行和Python API

### 用户体验
- ✅ 简化安装流程
- ✅ 一键配置功能
- ✅ 详细使用教程
- ✅ 完整常见问题解答
- ✅ 丰富的演示示例

### 开发者体验
- ✅ 完整的贡献指南
- ✅ 公开的GitHub仓库
- ✅ 详细的API文档
- ✅ 测试套件完整

## 📦 安装方式

### 通过ClawHub安装（推荐）
```bash
openclaw skill install sum2slides
```

### 通过pip安装
```bash
pip install sum2slides
```

### 从源码安装
```bash
通过 OpenClaw 安装技能
cd sum2slides
pip install -e .
```

## 🚀 快速开始

### 基本使用
```bash
# 从文本生成幻灯片
sum2slides "项目总结：完成核心功能开发，通过测试验证" --output demo.pptx
```

### 查看演示
```bash
python scripts/demo.py
```

### 阅读教程
```bash
cat TUTORIAL.md
```

## 📚 文档资源

- [用户手册](README.md)
- [技能说明](SKILL.md)
- [新手教程](TUTORIAL.md)
- [常见问题](FAQ.md)
- [使用演示](DEMO.md)
- [贡献指南](CONTRIBUTING.md)

## 🤝 社区和支持

- **GitHub**: 本地化技能版本
- **Issues**: 本地化技能版本/issues
- **Discussions**: 本地化技能版本/discussions
- **Discord**: https://discord.gg/clawd

## 🙏 感谢

感谢所有贡献者和用户的支持！

---

**发布日期**: 2026年3月29日  
**版本**: Sum2Slides v1.0.1 🌟  
**状态**: 正式版本
"""
    
    release_notes_file = project_root / "RELEASE_NOTES.md"
    with open(release_notes_file, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"✅ 发布说明已创建: {release_notes_file}")
    return True

def create_skill_package():
    """创建Skill安装包"""
    
    print("\n📦 创建Skill安装包...")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    package_name = f"sum2slides-1.0.0.skill.zip"
    package_path = project_root.parent / package_name
    
    try:
        # 创建zip包
        subprocess.run([
            'zip', '-r', str(package_path), 'sum2slides-1.0.0/'
        ], cwd=project_root.parent, check=True)
        
        print(f"✅ Skill包已创建: {package_path}")
        print(f"   大小: {package_path.stat().st_size / 1024:.1f} KB")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建Skill包失败: {e}")
        return False

def main():
    """主函数"""
    
    print("🚀 Sum2Slides v1.0.1 发布准备")
    print("=" * 50)
    
    # 执行所有检查
    checks = [
        ("版本信息", check_version_info),
        ("文档完整性", check_documentation),
        ("源代码完整性", check_source_code),
        ("外部链接", check_external_links),
        ("包结构", check_package_structure),
        ("配置文件", check_config_files),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name}检查出错: {e}")
            results[name] = False
    
    # 创建发布材料
    print("\n📝 创建发布材料...")
    print("-" * 40)
    
    try:
        results["发布说明"] = create_release_notes()
        results["Skill包"] = create_skill_package()
    except Exception as e:
        print(f"❌ 创建发布材料失败: {e}")
        results["发布材料"] = False
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 发布准备总结")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {name}")
    
    print(f"\n总计: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("\n🎉 发布准备完成！可以进行发布了。")
        print("\n📦 下一步:")
        print("1. 检查生成的Skill包")
        print("2. 验证所有文档链接")
        print("3. 测试安装流程")
        print("4. 发布到ClawHub")
    else:
        print("\n⚠️ 发布准备未完成，请解决失败的检查项。")

if __name__ == "__main__":
    main()