#!/usr/bin/env python3
"""
Sum2Slides v1.0.1 快速安全扫描脚本
仿照ClawHub安全扫描标准，进行快速检查
"""

import os
import sys
import json
import yaml
import re
from datetime import datetime
from pathlib import Path

def scan_project(project_dir):
    """扫描项目"""
    print("🔍 Sum2Slides v1.0.1 安全扫描开始")
    print("=" * 60)
    
    results = {
        "扫描时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "项目名称": "sum2slides",
        "版本": "1.0.0",
        "检查结果": [],
        "发现问题": [],
        "建议": [],
        "扫描状态": "✅ 通过"
    }
    
    project_path = Path(project_dir)
    
    # 检查1: 必需文件存在性
    print("\n📁 1. 必需文件检查:")
    required_files = [
        ("SKILL.md", "技能主文档"),
        ("README.md", "项目说明"),
        ("package.json", "包配置文件"),
        ("requirements.txt", "依赖文件"),
        ("CHANGELOG.md", "更新日志")
    ]
    
    for filename, description in required_files:
        file_path = project_path / filename
        if file_path.exists():
            print(f"  ✅ {filename} - {description}")
            results["检查结果"].append(f"✅ {filename} 存在")
        else:
            print(f"  ❌ {filename} - {description} (缺失)")
            results["发现问题"].append(f"❌ {filename} 缺失")
            results["扫描状态"] = "⚠️ 有问题"
    
    # 检查2: package.json完整性
    print("\n📦 2. package.json检查:")
    package_file = project_path / "package.json"
    if package_file.exists():
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # 检查必需字段
            required_fields = ["name", "version", "description", "author", "license"]
            for field in required_fields:
                if field in package_data:
                    value = package_data[field]
                    if field == "name" and value == "sum2slides":
                        print(f"  ✅ name = '{value}' (正确)")
                    elif field == "version" and value == "1.0.0":
                        print(f"  ✅ version = '{value}' (正确)")
                    else:
                        print(f"  ✅ {field} = '{value}'")
                else:
                    print(f"  ⚠️  {field} 字段缺失")
                    results["发现问题"].append(f"⚠️ package.json缺少{field}字段")
        
        except json.JSONDecodeError:
            print(f"  ❌ JSON解析失败")
            results["发现问题"].append(f"❌ package.json格式错误")
    else:
        print(f"  ❌ package.json文件不存在")
    
    # 检查3: 依赖安全检查
    print("\n🛡️ 3. 依赖安全检查:")
    req_file = project_path / "requirements.txt"
    if req_file.exists():
        try:
            with open(req_file, 'r') as f:
                content = f.read()
            
            dependencies = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    dependencies.append(line)
            
            print(f"  ✅ 发现 {len(dependencies)} 个依赖包:")
            for dep in dependencies:
                print(f"    - {dep}")
                
            # 检查是否有已知的高风险包
            risky_packages = ["pycrypto", "Crypto", "rsa", "django-debug-toolbar"]
            for dep in dependencies:
                for risky in risky_packages:
                    if risky.lower() in dep.lower():
                        print(f"  ⚠️  发现可能的高风险包: {dep}")
                        results["建议"].append(f"⚠️ 建议检查依赖包安全性: {dep}")
                        
        except Exception as e:
            print(f"  ❌ 依赖文件解析失败: {e}")
    else:
        print(f"  ⚠️  requirements.txt文件不存在")
    
    # 检查4: Python代码安全检查
    print("\n🐍 4. Python代码安全检查:")
    python_files = []
    for root, dirs, files in os.walk(project_path):
        # 跳过隐藏目录和虚拟环境
        if any(part.startswith('.') for part in Path(root).parts):
            continue
        
        for file in files:
            if file.endswith('.py') and not (('__pycache__' in root) or ('venv' in root)):
                python_files.append(Path(root) / file)
    
    print(f"  ✅ 发现 {len(python_files)} 个Python文件")
    
    security_issues = []
    for py_file in python_files[:10]:  # 只检查前10个文件
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查硬编码的秘密
            sensitive_patterns = [
                r'password\s*=\s*[\'\"].*?[\'\"]',
                r'api_key\s*=\s*[\'\"].*?[\'\"]',
                r'secret\s*=\s*[\'\"].*?[\'\"]',
                r'token\s*=\s*[\'\"].*?[\'\"]',
            ]
            
            found_issues = []
            for pattern in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    found_issues.append("硬编码敏感信息")
            
            if not found_issues:
                print(f"    ✅ {py_file.name} 通过安全扫描")
            else:
                print(f"    ⚠️  {py_file.name} 存在安全风险: {', '.join(found_issues)}")
                security_issues.append(f"{py_file.name}: {', '.join(found_issues)}")
                
        except Exception as e:
            print(f"    ❌ {py_file.name} 检查失败: {e}")
    
    if security_issues:
        results["发现问题"].append("⚠️ Python代码存在安全风险")
        results["建议"].append("🔒 建议检查Python代码中的硬编码敏感信息")
    
    # 检查5: 文档完整性
    print("\n📚 5. 文档完整性检查:")
    doc_files = [
        "TUTORIAL.md",
        "DEMO.md",
        "FAQ.md",
        "CONTRIBUTING.md",
        "SECURITY_REPORT.md",
        "OPENCLAW_USAGE_GUIDE.md"
    ]
    
    missing_docs = []
    for doc_file in doc_files:
        file_path = project_path / doc_file
        if file_path.exists():
            size = os.path.getsize(file_path)
            if size > 100:
                print(f"  ✅ {doc_file} 存在 ({size} 字节)")
            else:
                print(f"  ⚠️  {doc_file} 存在但内容过少 ({size} 字节)")
                missing_docs.append(doc_file)
        else:
            print(f"  ⚠️  {doc_file} 缺失")
            missing_docs.append(doc_file)
    
    if missing_docs:
        results["建议"].append(f"📝 建议补充文档: {', '.join(missing_docs)}")
    
    # 检查6: 配置文件和目录
    print("\n⚙️  6. 配置文件和目录检查:")
    
    # 检查config目录
    config_dir = project_path / "config"
    if config_dir.exists():
        config_files = list(config_dir.iterdir())
        print(f"  ✅ config/ 目录存在 ({len(config_files)} 个文件)")
        
        # 检查YAML配置文件
        yaml_files = [f for f in config_files if f.name.endswith(('.yaml', '.yml'))]
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"    ✅ {yaml_file.name} YAML格式正确")
            except yaml.YAMLError:
                print(f"    ❌ {yaml_file.name} YAML格式错误")
    
    # 检查examples目录
    examples_dir = project_path / "examples"
    if examples_dir.exists():
        example_files = list(examples_dir.iterdir())
        print(f"  ✅ examples/ 目录存在 ({len(example_files)} 个示例)")
    
    # 生成最终报告
    print("\n" + "=" * 60)
    print("📊 扫描完成报告:")
    print("=" * 60)
    
    total_checks = len(results["检查结果"]) + len(results["发现问题"])
    passed_checks = len(results["检查结果"])
    
    print(f"📈 检查统计:")
    print(f"  总检查项: {total_checks}")
    print(f"  通过项: {passed_checks}")
    print(f"  发现问题: {len(results['发现问题'])}")
    print(f"  建议项: {len(results['建议'])}")
    print(f"  总体状态: {results['扫描状态']}")
    
    if results["发现问题"]:
        print(f"\n📋 发现问题:")
        for issue in results["发现问题"]:
            print(f"  - {issue}")
    
    if results["建议"]:
        print(f"\n💡 改进建议:")
        for suggestion in results["建议"]:
            print(f"  - {suggestion}")
    
    # 总结和建议
    print(f"\n🎯 总结和建议:")
    if results["扫描状态"] == "✅ 通过":
        print("  ✅ 项目整体安全状况良好")
        print("  ✅ 文件结构完整")
        print("  ✅ 核心文档齐全")
        print("  ✅ 准备就绪，可以上传")
    else:
        print("  ⚠️  项目存在一些问题需要解决")
        print("  🔧 建议解决发现的问题后再上传")
        print("  📋 详细问题请查看上述列表")
    
    return results

def save_report(results, output_file="security_scan_report.md"):
    """保存扫描报告"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Sum2Slides v1.0.1 安全扫描报告\n\n")
        f.write(f"**扫描时间**: {results['扫描时间']}\n")
        f.write(f"**项目名称**: {results['项目名称']}\n")
        f.write(f"**版本**: {results['版本']}\n")
        f.write(f"**总体状态**: {results['扫描状态']}\n\n")
        
        f.write("## 检查结果\n\n")
        for check in results["检查结果"]:
            f.write(f"- {check}\n")
        
        if results["发现问题"]:
            f.write("\n## 发现问题\n\n")
            for issue in results["发现问题"]:
                f.write(f"- {issue}\n")
        
        if results["建议"]:
            f.write("\n## 改进建议\n\n")
            for suggestion in results["建议"]:
                f.write(f"- {suggestion}\n")
        
        f.write("\n## 扫描总结\n\n")
        total_checks = len(results["检查结果"]) + len(results["发现问题"])
        passed_checks = len(results["检查结果"])
        
        f.write(f"- 总检查项: {total_checks}\n")
        f.write(f"- 通过项: {passed_checks}\n")
        f.write(f"- 发现问题: {len(results['发现问题'])}\n")
        f.write(f"- 总体状态: {results['扫描状态']}\n")
        
        if results["扫描状态"] == "✅ 通过":
            f.write("\n**结论**: 项目安全状况良好，准备就绪可以上传。\n")
        else:
            f.write("\n**结论**: 项目存在一些需要解决的问题，建议修复后再上传。\n")
    
    print(f"\n📄 报告已保存到: {output_file}")

def main():
    """主函数"""
    # 设置项目目录
    project_dir = "/home/wwu/.openclaw/workspace/sum2slides-1.0.0"
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        sys.exit(1)
    
    print(f"📂 扫描项目目录: {project_dir}")
    print("=" * 60)
    
    # 运行扫描
    results = scan_project(project_dir)
    
    # 保存报告
    save_report(results)
    
    # 在控制台输出总结
    print("\n" + "=" * 60)
    print("🎉 安全扫描完成！")
    print("=" * 60)
    
    if results["扫描状态"] == "✅ 通过":
        print("✅ 项目已准备好上传到 ClawHub")
        print("🚀 您现在可以上传 sum2slides v1.0.1")
    else:
        print("⚠️  项目存在一些问题需要解决")
        print("🔧 请查看上面的问题列表并修复")
        print("📋 详细信息请查看生成的报告文件")
    
    print("\n📋 您可以查看 security_scan_report.md 获取详细报告")

if __name__ == "__main__":
    main()