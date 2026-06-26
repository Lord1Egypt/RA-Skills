#!/usr/bin/env python3
"""
SpringBoot 项目结构分析工具
扫描项目目录，识别结构问题，生成分析报告
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict

# 标准包结构定义
STANDARD_PACKAGES = {
    'controller': '控制器层（REST API）',
    'service': '业务层接口',
    'service.impl': '业务层实现',
    'dao': '数据访问层（Mapper）',
    'entity': '数据库实体',
    'dto': '数据传输对象',
    'vo': '视图对象',
    'config': '配置类',
    'util': '工具类',
    'common': '公共类',
    'exception': '异常处理',
    'interceptor': '拦截器',
    'aspect': '切面',
}

# 类名后缀与标准位置的映射
CLASS_PATTERNS = {
    'Controller': 'controller',
    'ServiceImpl': 'service.impl',
    'Service': 'service',
    'Mapper': 'dao',
    'DAO': 'dao',
    'Repository': 'dao',
    'DTO': 'dto',
    'VO': 'vo',
    'BO': 'dto',
    'PO': 'entity',
    'DO': 'entity',
    'Entity': 'entity',
    'Config': 'config',
    'Configuration': 'config',
    'Util': 'util',
    'Utils': 'util',
    'Helper': 'util',
    'Exception': 'exception',
    'Interceptor': 'interceptor',
    'Aspect': 'aspect',
}

# MyBatis 相关文件
MYBATIS_PATTERNS = ['.xml', 'Mapper']

# 配置文件
CONFIG_FILES = [
    'application.yml', 'application.yaml', 'application.properties',
    'application-dev.yml', 'application-prod.yml', 'application-test.yml',
    'mybatis-config.xml', 'logback.xml', 'log4j2.xml'
]


def find_java_files(project_path):
    """查找所有 Java 文件"""
    java_files = []
    for root, dirs, files in os.walk(project_path):
        # 跳过 target 和 .git 目录
        dirs[:] = [d for d in dirs if d not in ['target', '.git', 'node_modules', '.idea']]
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    return java_files


def find_resource_files(project_path):
    """查找资源文件"""
    resource_files = []
    resources_path = os.path.join(project_path, 'src', 'main', 'resources')
    if os.path.exists(resources_path):
        for root, dirs, files in os.walk(resources_path):
            for file in files:
                resource_files.append(os.path.join(root, file))
    return resource_files


def analyze_class_location(file_path, project_path):
    """分析类文件的位置是否规范"""
    file_name = os.path.basename(file_path)
    class_name = file_name.replace('.java', '')
    relative_path = os.path.relpath(file_path, project_path)
    
    # 确定当前所在包
    parts = relative_path.split(os.sep)
    if 'java' in parts:
        java_idx = parts.index('java')
        current_package = '.'.join(parts[java_idx+1:-1])
    else:
        current_package = ''
    
    # 根据类名后缀判断应该在哪里
    expected_package = None
    for suffix, pkg in CLASS_PATTERNS.items():
        if class_name.endswith(suffix):
            expected_package = pkg
            break
    
    # 如果没有后缀匹配，根据内容猜测
    if not expected_package:
        expected_package = guess_type_from_content(file_path)
    
    return {
        'file': relative_path,
        'class_name': class_name,
        'current_package': current_package,
        'expected_package': expected_package,
        'is_correct_location': current_package.endswith(expected_package) if expected_package else True
    }


def guess_type_from_content(file_path):
    """根据文件内容猜测类类型"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '@RestController' in content or '@Controller' in content:
            return 'controller'
        elif '@Service' in content:
            return 'service'
        elif '@Mapper' in content or 'extends BaseMapper' in content:
            return 'dao'
        elif '@Entity' in content or '@Table' in content:
            return 'entity'
        elif '@Configuration' in content or '@ConfigurationProperties' in content:
            return 'config'
        elif 'class' in content and 'Util' in content:
            return 'util'
    except:
        pass
    return None


def analyze_mybatis_files(resource_files):
    """分析 MyBatis 相关文件"""
    mapper_xml_files = []
    for file_path in resource_files:
        file_name = os.path.basename(file_path)
        if file_name.endswith('Mapper.xml'):
            relative_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(file_path)))
            mapper_xml_files.append(relative_path)
    return mapper_xml_files


def check_config_files(resource_files):
    """检查配置文件"""
    found_configs = []
    missing_configs = []
    
    resource_dir = os.path.dirname(resource_files[0]) if resource_files else ''
    existing_files = [os.path.basename(f) for f in resource_files]
    
    for config in CONFIG_FILES:
        if config in existing_files:
            found_configs.append(config)
        else:
            missing_configs.append(config)
    
    return found_configs, missing_configs


def generate_report(project_path, analysis_result):
    """生成分析报告"""
    report = []
    report.append("=" * 60)
    report.append("SpringBoot 项目结构分析报告")
    report.append("=" * 60)
    report.append(f"项目路径: {project_path}")
    report.append("")
    
    # 统计信息
    report.append("【统计信息】")
    report.append(f"Java 文件总数: {len(analysis_result['java_files'])}")
    report.append(f"MyBatis XML 文件: {len(analysis_result['mybatis_files'])}")
    report.append(f"配置文件: {len(analysis_result['found_configs'])}")
    report.append("")
    
    # 位置不规范的类
    misplaced_classes = [c for c in analysis_result['class_analysis'] if not c['is_correct_location']]
    if misplaced_classes:
        report.append("【位置不规范的类】")
        for cls in misplaced_classes:
            report.append(f"  - {cls['class_name']}")
            report.append(f"    当前: {cls['current_package']}")
            report.append(f"    建议: {cls['expected_package']}")
        report.append("")
    
    # 缺失的标准包
    existing_packages = set(c['current_package'].split('.')[-1] for c in analysis_result['class_analysis'] if c['current_package'])
    missing_packages = set(STANDARD_PACKAGES.keys()) - existing_packages
    if missing_packages:
        report.append("【缺失的标准包】")
        for pkg in sorted(missing_packages):
            report.append(f"  - {pkg}: {STANDARD_PACKAGES[pkg]}")
        report.append("")
    
    # 配置文件检查
    report.append("【配置文件状态】")
    report.append(f"  已存在: {', '.join(analysis_result['found_configs']) if analysis_result['found_configs'] else '无'}")
    
    important_missing = [c for c in analysis_result['missing_configs'] if 'application' in c]
    if important_missing:
        report.append(f"  缺失重要配置: {', '.join(important_missing)}")
    report.append("")
    
    # 建议
    report.append("【重构建议】")
    if misplaced_classes:
        report.append("1. 将位置不规范的类移动到对应的标准包中")
    if missing_packages:
        report.append(f"2. 创建缺失的标准包: {', '.join(sorted(missing_packages))}")
    if important_missing:
        report.append("3. 补充缺失的配置文件")
    report.append("")
    
    return '\n'.join(report)


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_project.py <项目路径>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"错误: 路径不存在 {project_path}")
        sys.exit(1)
    
    print(f"正在分析项目: {project_path}")
    print("-" * 60)
    
    # 分析
    java_files = find_java_files(project_path)
    resource_files = find_resource_files(project_path)
    
    class_analysis = [analyze_class_location(f, project_path) for f in java_files]
    mybatis_files = analyze_mybatis_files(resource_files)
    found_configs, missing_configs = check_config_files(resource_files)
    
    analysis_result = {
        'java_files': java_files,
        'class_analysis': class_analysis,
        'mybatis_files': mybatis_files,
        'found_configs': found_configs,
        'missing_configs': missing_configs
    }
    
    # 生成报告
    report = generate_report(project_path, analysis_result)
    print(report)
    
    # 保存 JSON 报告
    report_file = os.path.join(project_path, 'project-analysis-report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存: {report_file}")


if __name__ == '__main__':
    main()
