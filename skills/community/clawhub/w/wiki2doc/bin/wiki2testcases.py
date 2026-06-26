#!/usr/bin/env python3
"""
完整的自动化工作流 - wiki2testcases.py

将Wiki页面转换为测试用例Excel文件的完整流程:
1. 从Wiki提取内容生成Word文档
2. 分析需求检测问题
3. 生成测试用例（Markdown格式）
4. 转换为Excel格式
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


class WorkflowOrchestrator:
    """工作流编排器"""

    def __init__(self, wiki_url):
        """
        初始化工作流编排器

        Args:
            wiki_url: Wiki页面URL
        """
        self.wiki_url = wiki_url
        self.base_dir = Path(__file__).parent.parent  # wiki2doc目录
        self.bin_dir = Path(__file__).parent
        self.demand_dir = self.base_dir / "demand"
        self.demand_dir.mkdir(exist_ok=True)

        # 步骤输出文件
        self.doc_file = None
        self.analysis_report = None
        self.testcase_md = None
        self.testcase_excel = None

    def log(self, message, level="INFO"):
        """
        打印日志

        Args:
            message: 日志消息
            level: 日志级别
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def step1_extract_from_wiki(self):
        """
        步骤1: 从Wiki提取内容并生成Word文档

        Returns:
            bool: 是否成功
        """
        self.log("\n" + "="*60)
        self.log("步骤1: 从Wiki提取内容并生成Word文档")
        self.log("="*60)

        try:
            # 调用wiki2doc.py
            wiki2doc_script = self.bin_dir / "wiki2doc.py"
            if not wiki2doc_script.exists():
                self.log(f"找不到wiki2doc.py脚本: {wiki2doc_script}", "ERROR")
                return False

            cmd = [sys.executable, str(wiki2doc_script), self.wiki_url]
            self.log(f"执行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, cwd=str(self.base_dir), capture_output=True, text=True)

            if result.returncode != 0:
                self.log(f"Wiki提取失败: {result.stderr}", "ERROR")
                return False

            # 查找生成的Word文档
            doc_files = list(self.demand_dir.glob("*.docx"))
            if doc_files:
                # 按修改时间排序，取最新的
                self.doc_file = max(doc_files, key=lambda p: p.stat().st_mtime)
                self.log(f"[OK] 成功生成Word文档: {self.doc_file}")
                return True
            else:
                self.log("未找到生成的Word文档", "ERROR")
                return False

        except Exception as e:
            self.log(f"步骤1执行失败: {e}", "ERROR")
            return False

    def step2_analyze_requirements(self):
        """
        步骤2: 分析需求文档

        Returns:
            bool: 是否成功
        """
        self.log("\n" + "="*60)
        self.log("步骤2: 分析需求文档")
        self.log("="*60)

        if not self.doc_file or not self.doc_file.exists():
            self.log("Word文档不存在，跳过此步骤", "WARNING")
            return True  # 不阻止后续步骤

        try:
            # 调用analyze_requirements.py
            analyze_script = self.bin_dir / "analyze" / "analyze_requirements.py"
            if not analyze_script.exists():
                self.log(f"找不到分析脚本: {analyze_script}", "ERROR")
                return False

            cmd = [sys.executable, str(analyze_script), str(self.doc_file)]
            self.log(f"执行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, cwd=str(self.base_dir), capture_output=True, text=True)

            if result.returncode != 0:
                self.log(f"需求分析失败: {result.stderr}", "ERROR")
                return False

            # 查找生成的分析报告
            report_files = list(self.demand_dir.glob("*_analysis_report.txt"))
            if report_files:
                self.analysis_report = max(report_files, key=lambda p: p.stat().st_mtime)
                self.log(f"[OK] 成功生成分析报告: {self.analysis_report}")
                return True
            else:
                self.log("未找到分析报告", "WARNING")
                return True  # 不阻止后续步骤

        except Exception as e:
            self.log(f"步骤2执行失败: {e}", "ERROR")
            return False

    def step3_generate_test_cases(self):
        """
        步骤3: 生成测试用例

        Returns:
            bool: 是否成功
        """
        self.log("\n" + "="*60)
        self.log("步骤3: 生成测试用例")
        self.log("="*60)

        if not self.doc_file or not self.doc_file.exists():
            self.log("Word文档不存在，无法生成测试用例", "ERROR")
            return False

        try:
            # 调用generate_testcases.py
            generate_script = self.bin_dir / "generate" / "generate_testcases.py"
            if not generate_script.exists():
                self.log(f"找不到生成脚本: {generate_script}", "ERROR")
                return False

            cmd = [sys.executable, str(generate_script), str(self.doc_file)]
            self.log(f"执行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, cwd=str(self.base_dir), capture_output=True, text=True)

            if result.returncode != 0:
                self.log(f"测试用例生成失败: {result.stderr}", "ERROR")
                return False

            # 查找生成的Markdown文件
            md_files = list(self.demand_dir.glob("*_testcases.md"))
            if md_files:
                self.testcase_md = max(md_files, key=lambda p: p.stat().st_mtime)
                self.log(f"[OK] 成功生成测试用例Markdown: {self.testcase_md}")
                return True
            else:
                self.log("未找到测试用例Markdown文件", "ERROR")
                return False

        except Exception as e:
            self.log(f"步骤3执行失败: {e}", "ERROR")
            return False

    def step4_convert_to_excel(self):
        """
        步骤4: 转换为Excel格式

        Returns:
            bool: 是否成功
        """
        self.log("\n" + "="*60)
        self.log("步骤4: 转换为Excel格式")
        self.log("="*60)

        if not self.testcase_md or not self.testcase_md.exists():
            self.log("测试用例Markdown文件不存在", "ERROR")
            return False

        try:
            # 调用md2excel.py
            convert_script = self.bin_dir / "convert" / "md2excel.py"
            if not convert_script.exists():
                self.log(f"找不到转换脚本: {convert_script}", "ERROR")
                return False

            cmd = [sys.executable, str(convert_script), str(self.testcase_md)]
            self.log(f"执行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, cwd=str(self.base_dir), capture_output=True, text=True)

            if result.returncode != 0:
                self.log(f"Excel转换失败: {result.stderr}", "ERROR")
                return False

            # 查找生成的Excel文件
            excel_files = list(self.demand_dir.glob("*_testcases.xlsx"))
            if excel_files:
                self.testcase_excel = max(excel_files, key=lambda p: p.stat().st_mtime)
                self.log(f"[OK] 成功生成Excel文件: {self.testcase_excel}")
                return True
            else:
                # 可能是md同名xlsx
                excel_files = list(self.demand_dir.glob("*.xlsx"))
                if excel_files:
                    self.testcase_excel = max(excel_files, key=lambda p: p.stat().st_mtime)
                    self.log(f"[OK] 成功生成Excel文件: {self.testcase_excel}")
                    return True
                else:
                    self.log("未找到Excel文件", "ERROR")
                    return False

        except Exception as e:
            self.log(f"步骤4执行失败: {e}", "ERROR")
            return False

    def run(self):
        """
        运行完整工作流

        Returns:
            bool: 是否成功
        """
        self.log("开始执行完整工作流...")
        self.log(f"Wiki URL: {self.wiki_url}")
        self.log(f"工作目录: {self.base_dir}")

        # 执行各个步骤
        steps = [
            ("步骤1: Wiki提取", self.step1_extract_from_wiki),
            ("步骤2: 需求分析", self.step2_analyze_requirements),
            ("步骤3: 测试用例生成", self.step3_generate_test_cases),
            ("步骤4: Excel转换", self.step4_convert_to_excel)
        ]

        for step_name, step_func in steps:
            if not step_func():
                self.log(f"{step_name} 失败，工作流终止", "ERROR")
                return False

        # 打印总结
        self.log("\n" + "="*60)
        self.log("工作流执行完成！")
        self.log("="*60)

        if self.doc_file:
            self.log(f"[OK] Word文档: {self.doc_file}")
        if self.analysis_report:
            self.log(f"[OK] 分析报告: {self.analysis_report}")
        if self.testcase_md:
            self.log(f"[OK] 测试用例MD: {self.testcase_md}")
        if self.testcase_excel:
            self.log(f"[OK] 测试用例Excel: {self.testcase_excel}")

        self.log(f"\n所有文件保存在: {self.demand_dir}")

        return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Wiki到测试用例的完整自动化工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
完整工作流:
  1. 从Wiki提取内容生成Word文档
  2. 分析需求检测遗漏点、矛盾点
  3. 生成测试用例（Markdown格式）
  4. 转换为Excel格式

示例:
  python wiki2testcases.py http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
        """
    )

    parser.add_argument("wiki_url", help="Wiki页面URL")

    args = parser.parse_args()

    # 创建工作流编排器
    orchestrator = WorkflowOrchestrator(args.wiki_url)

    # 运行工作流
    if orchestrator.run():
        print("\n[OK] 工作流执行成功！")
        sys.exit(0)
    else:
        print("\n[FAILED] 工作流执行失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
