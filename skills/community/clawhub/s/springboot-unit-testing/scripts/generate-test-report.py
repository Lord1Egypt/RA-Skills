#!/usr/bin/env python3
"""
测试报告生成脚本
生成Spring Boot项目的测试覆盖率和质量报告
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Dict, List, Tuple, Any

class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.report_dir = self.project_root / "test-reports"
        self.report_dir.mkdir(exist_ok=True)
        
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合测试报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "summary": {},
            "coverage": {},
            "test_categories": {},
            "issues": [],
            "recommendations": []
        }
        
        # 收集测试信息
        report["summary"] = self.collect_test_summary()
        report["coverage"] = self.collect_coverage_data()
        report["test_categories"] = self.analyze_test_categories()
        report["issues"] = self.identify_issues()
        report["recommendations"] = self.generate_recommendations()
        
        # 生成报告文件
        self.save_report(report)
        self.generate_html_report(report)
        
        return report
    
    def collect_test_summary(self) -> Dict[str, Any]:
        """收集测试摘要信息"""
        summary = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "test_classes": 0,
            "test_methods": 0,
            "execution_time": 0.0
        }
        
        # 查找Surefire测试报告
        surefire_dir = self.project_root / "target" / "surefire-reports"
        if surefire_dir.exists():
            for xml_file in surefire_dir.glob("*.xml"):
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    summary["total_tests"] += int(root.get("tests", 0))
                    summary["failed_tests"] += int(root.get("failures", 0))
                    summary["skipped_tests"] += int(root.get("skipped", 0))
                    summary["passed_tests"] = summary["total_tests"] - summary["failed_tests"] - summary["skipped_tests"]
                    
                    # 计算执行时间
                    time_attr = root.get("time")
                    if time_attr:
                        summary["execution_time"] += float(time_attr)
                    
                    # 统计测试类和方法
                    for testcase in root.findall(".//testcase"):
                        summary["test_methods"] += 1
                        class_name = testcase.get("classname", "")
                        if class_name and class_name not in self._test_classes:
                            self._test_classes.add(class_name)
                            summary["test_classes"] += 1
                            
                except ET.ParseError:
                    print(f"警告: 无法解析XML文件: {xml_file}")
        
        return summary
    
    def collect_coverage_data(self) -> Dict[str, Any]:
        """收集覆盖率数据"""
        coverage = {
            "line_coverage": 0.0,
            "branch_coverage": 0.0,
            "method_coverage": 0.0,
            "class_coverage": 0.0,
            "instructions_coverage": 0.0,
            "complexity_coverage": 0.0,
            "by_package": {},
            "by_class": {}
        }
        
        # 查找JaCoCo覆盖率报告
        jacoco_xml = self.project_root / "target" / "site" / "jacoco" / "jacoco.xml"
        if jacoco_xml.exists():
            try:
                tree = ET.parse(jacoco_xml)
                root = tree.getroot()
                
                # 收集整体覆盖率
                counter_types = {
                    "LINE": "line_coverage",
                    "BRANCH": "branch_coverage", 
                    "METHOD": "method_coverage",
                    "CLASS": "class_coverage",
                    "INSTRUCTION": "instructions_coverage",
                    "COMPLEXITY": "complexity_coverage"
                }
                
                for counter in root.findall(".//counter"):
                    counter_type = counter.get("type")
                    if counter_type in counter_types:
                        missed = int(counter.get("missed", 0))
                        covered = int(counter.get("covered", 0))
                        total = missed + covered
                        
                        if total > 0:
                            coverage_rate = (covered / total) * 100
                            coverage[counter_types[counter_type]] = round(coverage_rate, 2)
                
                # 按包收集覆盖率
                for package in root.findall(".//package"):
                    package_name = package.get("name", "unknown")
                    package_coverage = {}
                    
                    for counter in package.findall("counter"):
                        counter_type = counter.get("type")
                        missed = int(counter.get("missed", 0))
                        covered = int(counter.get("covered", 0))
                        total = missed + covered
                        
                        if total > 0:
                            coverage_rate = (covered / total) * 100
                            package_coverage[counter_type.lower()] = round(coverage_rate, 2)
                    
                    coverage["by_package"][package_name] = package_coverage
                
                # 按类收集覆盖率（仅限主要业务类）
                for package in root.findall(".//package"):
                    for class_elem in package.findall("class"):
                        class_name = class_elem.get("name", "unknown")
                        if "Test" not in class_name:  # 排除测试类
                            class_coverage = {}
                            
                            for counter in class_elem.findall("counter"):
                                counter_type = counter.get("type")
                                missed = int(counter.get("missed", 0))
                                covered = int(counter.get("covered", 0))
                                total = missed + covered
                                
                                if total > 0:
                                    coverage_rate = (covered / total) * 100
                                    class_coverage[counter_type.lower()] = round(coverage_rate, 2)
                            
                            if class_coverage:
                                coverage["by_class"][class_name] = class_coverage
                                
            except ET.ParseError:
                print(f"警告: 无法解析JaCoCo XML文件: {jacoco_xml}")
        
        return coverage
    
    def analyze_test_categories(self) -> Dict[str, Any]:
        """分析测试类别分布"""
        categories = {
            "unit_tests": {"count": 0, "coverage": 0.0},
            "integration_tests": {"count": 0, "coverage": 0.0},
            "controller_tests": {"count": 0, "coverage": 0.0},
            "service_tests": {"count": 0, "coverage": 0.0},
            "repository_tests": {"count": 0, "coverage": 0.0},
            "exception_tests": {"count": 0, "coverage": 0.0},
            "boundary_tests": {"count": 0, "coverage": 0.0}
        }
        
        # 分析测试文件
        test_dir = self.project_root / "src" / "test"
        if test_dir.exists():
            for test_file in test_dir.rglob("*.java"):
                content = test_file.read_text(encoding="utf-8", errors="ignore")
                
                # 根据文件名和内容分类
                file_name = test_file.name
                
                if "IntegrationTest" in file_name or "IT.java" in file_name:
                    categories["integration_tests"]["count"] += 1
                elif "ControllerTest" in file_name:
                    categories["controller_tests"]["count"] += 1
                elif "ServiceTest" in file_name:
                    categories["service_tests"]["count"] += 1
                elif "RepositoryTest" in file_name or "MapperTest" in file_name:
                    categories["repository_tests"]["count"] += 1
                else:
                    categories["unit_tests"]["count"] += 1
                
                # 根据内容进一步分类
                if "assertThrows" in content or "Exception" in content:
                    categories["exception_tests"]["count"] += 1
                
                if "boundary" in content.lower() or "Boundary" in content:
                    categories["boundary_tests"]["count"] += 1
        
        return categories
    
    def identify_issues(self) -> List[Dict[str, Any]]:
        """识别测试问题"""
        issues = []
        
        # 检查覆盖率阈值
        coverage = self.collect_coverage_data()
        
        thresholds = {
            "line_coverage": 85.0,
            "branch_coverage": 80.0,
            "method_coverage": 90.0,
            "class_coverage": 95.0
        }
        
        for metric, threshold in thresholds.items():
            actual = coverage.get(metric, 0.0)
            if actual < threshold:
                issues.append({
                    "type": "COVERAGE_LOW",
                    "severity": "MEDIUM",
                    "metric": metric,
                    "expected": threshold,
                    "actual": actual,
                    "message": f"{metric.replace('_', ' ').title()} 低于阈值: {actual}% < {threshold}%"
                })
        
        # 检查缺少的测试类别
        categories = self.analyze_test_categories()
        
        required_categories = ["controller_tests", "service_tests", "repository_tests"]
        for category in required_categories:
            if categories[category]["count"] == 0:
                issues.append({
                    "type": "MISSING_TEST_CATEGORY",
                    "severity": "HIGH",
                    "category": category,
                    "message": f"缺少{category.replace('_', ' ').title()}"
                })
        
        # 检查异常和边界测试
        if categories["exception_tests"]["count"] == 0:
            issues.append({
                "type": "MISSING_EXCEPTION_TESTS",
                "severity": "MEDIUM",
                "message": "缺少异常处理测试"
            })
        
        if categories["boundary_tests"]["count"] == 0:
            issues.append({
                "type": "MISSING_BOUNDARY_TESTS",
                "severity": "MEDIUM",
                "message": "缺少边界值测试"
            })
        
        return issues
    
    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """生成改进建议"""
        recommendations = []
        
        # 基于问题生成建议
        issues = self.identify_issues()
        
        for issue in issues:
            if issue["type"] == "COVERAGE_LOW":
                metric = issue["metric"]
                recommendations.append({
                    "type": "IMPROVE_COVERAGE",
                    "priority": "HIGH" if issue["severity"] == "HIGH" else "MEDIUM",
                    "action": f"提高{metric.replace('_', ' ').title()}",
                    "details": f"当前覆盖率: {issue['actual']}%, 目标: {issue['expected']}%"
                })
            
            elif issue["type"] == "MISSING_TEST_CATEGORY":
                category = issue["category"]
                recommendations.append({
                    "type": "ADD_TEST_CATEGORY",
                    "priority": "HIGH",
                    "action": f"添加{category.replace('_', ' ').title()}",
                    "details": "参考测试模板创建对应的测试类"
                })
            
            elif issue["type"] == "MISSING_EXCEPTION_TESTS":
                recommendations.append({
                    "type": "ADD_EXCEPTION_TESTS",
                    "priority": "MEDIUM",
                    "action": "添加异常处理测试",
                    "details": "为每个可能抛出异常的方法添加异常测试"
                })
            
            elif issue["type"] == "MISSING_BOUNDARY_TESTS":
                recommendations.append({
                    "type": "ADD_BOUNDARY_TESTS",
                    "priority": "MEDIUM",
                    "action": "添加边界值测试",
                    "details": "为输入参数、状态转换、数据边界添加测试"
                })
        
        # 通用建议
        recommendations.extend([
            {
                "type": "REVIEW_TEST_NAMING",
                "priority": "LOW",
                "action": "检查测试命名规范",
                "details": "确保测试方法名遵循 Given-When-Then 格式"
            },
            {
                "type": "OPTIMIZE_TEST_SPEED",
                "priority": "MEDIUM",
                "action": "优化测试执行速度",
                "details": "考虑使用@MockBean代替真实依赖，使用内存数据库"
            },
            {
                "type": "ADD_INTEGRATION_TESTS",
                "priority": "MEDIUM",
                "action": "添加集成测试",
                "details": "使用@Testcontainers测试端到端流程"
            }
        ])
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any]) -> None:
        """保存JSON格式报告"""
        report_file = self.report_dir / "test-report.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 测试报告已保存: {report_file}")
    
    def generate_html_report(self, report: Dict[str, Any]) -> None:
        """生成HTML格式报告"""
        html_file = self.report_dir / "test-report.html"
        
        html_content = self._generate_html_content(report)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML报告已生成: {html_file}")
    
    def _generate_html_content(self, report: Dict[str, Any]) -> str:
        """生成HTML内容"""
        summary = report["summary"]
        coverage = report["coverage"]
        categories = report["test_categories"]
        issues = report["issues"]
        recommendations = report["recommendations"]
        
        return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spring Boot测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
        }}
        
        .header .timestamp {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        
        .section {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .section h2 {{
            color: #4a5568;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
            margin-top: 0;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .metric-card {{
            background: #f7fafc;
            border-left: 4px solid #4299e1;
            padding: 1rem;
            border-radius: 5px;
        }}
        
        .metric-card.high {{
            border-left-color: #48bb78;
        }}
        
        .metric-card.medium {{
            border-left-color: #ed8936;
        }}
        
        .metric-card.low {{
            border-left-color: #e53e3e;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .coverage-chart {{
            display: flex;
            align-items: center;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .coverage-item {{
            text-align: center;
        }}
        
        .coverage-value {{
            font-size: 2.5rem;
            font-weight: bold;
        }}
        
        .coverage-label {{
            font-size: 0.9rem;
            color: #718096;
        }}
        
        .issue-list, .recommendation-list {{
            list-style: none;
            padding: 0;
        }}
        
        .issue-item, .recommendation-item {{
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            background: #f7fafc;
            border-left: 4px solid #e53e3e;
        }}
        
        .recommendation-item {{
            border-left-color: #48bb78;
        }}
        
        .issue-severity {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-right: 0.5rem;
        }}
        
        .severity-high {{
            background: #fed7d7;
            color: #c53030;
        }}
        
        .severity-medium {{
            background: #feebc8;
            color: #dd6b20;
        }}
        
        .severity-low {{
            background: #e6fffa;
            color: #234e52;
        }}
        
        .priority-high {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .priority-medium {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        .priority-low {{
            background: #e9d8fd;
            color: #44337a;
        }}
        
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #718096;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #718096;
            font-size: 0.9rem;
            border-top: 1px solid #e2e8f0;
        }}
        
        @media (max-width: 768px) {{
            .metrics-grid, .summary-stats {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Spring Boot测试报告</h1>
        <div class="timestamp">生成时间: {report['timestamp']}</div>
        <div class="timestamp">项目路径: {report['project_root']}</div>
    </div>
    
    <div class="section">
        <h2>📊 测试摘要</h2>
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_tests', 0)}</div>
                <div class="stat-label">总测试数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('passed_tests', 0)}</div>
                <div class="stat-label">通过测试</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('failed_tests', 0)}</div>
                <div class="stat-label">失败测试</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('skipped_tests', 0)}</div>
                <div class="stat-label">跳过测试</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('test_classes', 0)}</div>
                <div class="stat-label">测试类</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('execution_time', 0):.2f}s</div>
                <div class="stat-label">执行时间</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>📈 代码覆盖率</h2>
        <div class="coverage-chart">
            <div class="coverage-item">
                <div class="coverage-value">{coverage.get('line_coverage', 0)}%</div>
                <div class="coverage-label">行覆盖率</div>
            </div>
            <div class="coverage-item">
                <div class="coverage-value">{coverage.get('branch_coverage', 0)}%</div>
                <div class="coverage-label">分支覆盖率</div>
            </div>
            <div class="coverage-item">
                <div class="coverage-value">{coverage.get('method_coverage', 0)}%</div>
                <div class="coverage-label">方法覆盖率</div>
            </div>
            <div class="coverage-item">
                <div class="coverage-value">{coverage.get('class_coverage', 0)}%</div>
                <div class="coverage-label">类覆盖率</div>
            </div>
        </div>
        
        <h3>测试类别分布</h3>
        <div class="metrics-grid">
            <div class="metric-card {'high' if categories.get('unit_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('unit_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">单元测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('integration_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('integration_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">集成测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('controller_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('controller_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">Controller测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('service_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('service_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">Service测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('repository_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('repository_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">Repository测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('exception_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('exception_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">异常测试</div>
            </div>
            <div class="metric-card {'high' if categories.get('boundary_tests', {{}}).get('count', 0) > 0 else 'low'}">
                <div class="metric-value">{categories.get('boundary_tests', {{}}).get('count', 0)}</div>
                <div class="metric-label">边界测试</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>⚠️ 发现问题</h2>
        <ul class="issue-list">
            {self._generate_issues_html(issues)}
        </ul>
    </div>
    
    <div class="section">
        <h2>💡 改进建议</h2>
        <ul class="recommendation-list">
            {self._generate_recommendations_html(recommendations)}
        </ul>
    </div>
    
    <div class="footer">
        <p>报告由Spring Boot测试报告生成器生成</p>
        <p>建议定期运行测试并检查覆盖率，确保代码质量</p>
    </div>
</body>
</html>
"""
    
    def _generate_issues_html(self, issues: List[Dict[str, Any]]) -> str:
        """生成问题HTML"""
        if not issues:
            return '<li class="issue-item">🎉 未发现问题！测试覆盖良好。</li>'
        
        html_parts = []
        for issue in issues:
            severity_class = f"severity-{issue['severity'].lower()}"
            html_parts.append(f"""
                <li class="issue-item">
                    <span class="issue-severity {severity_class}">{issue['severity']}</span>
                    {issue['message']}
                </li>
            """)
        
        return "\n".join(html_parts)
    
    def _generate_recommendations_html(self, recommendations: List[Dict[str, Any]]) -> str:
        """生成建议HTML"""
        if not recommendations:
            return '<li class="recommendation-item">✅ 无需改进建议。</li>'
        
        html_parts = []
        for rec in recommendations:
            priority_class = f"priority-{rec['priority'].lower()}"
            html_parts.append(f"""
                <li class="recommendation-item">
                    <span class="issue-severity {priority_class}">{rec['priority']}</span>
                    <strong>{rec['action']}</strong><br>
                    <small>{rec['details']}</small>
                </li>
            """)
        
        return "\n".join(html_parts)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate-test-report.py <项目根目录>")
        print("示例: python generate-test-report.py /path/to/spring-boot-project")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"错误: 项目目录不存在: {project_root}")
        sys.exit(1)
    
    print(f"🔍 开始分析项目: {project_root}")
    
    try:
        generator = TestReportGenerator(project_root)
        report = generator.generate_comprehensive_report()
        
        print("\n" + "="*60)
        print("📋 测试报告摘要")
        print("="*60)
        
        summary = report["summary"]
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过测试: {summary['passed_tests']}")
        print(f"失败测试: {summary['failed_tests']}")
        print(f"跳过测试: {summary['skipped_tests']}")
        print(f"执行时间: {summary['execution_time']:.2f}秒")
        
        coverage = report["coverage"]
        print(f"\n📊 代码覆盖率:")
        print(f"  行覆盖率: {coverage.get('line_coverage', 0)}%")
        print(f"  分支覆盖率: {coverage.get('branch_coverage', 0)}%")
        print(f"  方法覆盖率: {coverage.get('method_coverage', 0)}%")
        print(f"  类覆盖率: {coverage.get('class_coverage', 0)}%")
        
        issues = report["issues"]
        print(f"\n⚠️  发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"  - {issue['message']}")
        
        recommendations = report["recommendations"]
        print(f"\n💡 生成 {len(recommendations)} 条改进建议")
        
        print(f"\n✅ 报告已生成:")
        print(f"  JSON报告: {os.path.join(generator.report_dir, 'test-report.json')}")
        print(f"  HTML报告: {os.path.join(generator.report_dir, 'test-report.html')}")
        
    except Exception as e:
        print(f"❌ 生成报告时出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()