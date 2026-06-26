#!/usr/bin/env python3
"""
需求分析工具 - analyze_requirements.py

分析 .docx 中的需求内容，检测遗漏点、矛盾点和不明确之处
"""

import sys
import re
import json
from pathlib import Path
from docx import Document
from typing import List, Dict, Tuple, Any


class RequirementAnalyzer:
    """需求分析器"""

    def __init__(self, doc_path):
        """
        初始化需求分析器

        Args:
            doc_path: Word 文档路径
        """
        self.doc_path = Path(doc_path)
        self.doc = None
        self.requirements = []
        self.issues = {
            "missing_points": [],    # 遗漏点
            "contradictory_points": [],  # 矛盾点
            "unclear_points": [],    # 不明确点
            "incomplete_points": []  # 不完整点
        }

    def load_document(self):
        """加载 Word 文档"""
        try:
            self.doc = Document(self.doc_path)
            print(f"成功加载文档: {self.doc_path}")
            return True
        except Exception as e:
            print(f"文档加载失败: {e}")
            return False

    def extract_text_content(self):
        """
        提取文档中的文本内容

        Returns:
            str: 文档的完整文本内容
        """
        if not self.doc:
            return ""

        full_text = []
        for para in self.doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)

        return "\n".join(full_text)

    def analyze_missing_points(self, text: str) -> List[Dict[str, Any]]:
        """
        分析需求中的遗漏点

        Args:
            text: 需求文本内容

        Returns:
            List[Dict]: 遗漏点列表
        """
        missing_points = []
        lines = text.split('\n')

        # 检查每个段落是否有功能描述但没有测试要点
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # 检查功能描述
            if any(keyword in line for keyword in ["功能", "模块", "菜单", "按钮"]):
                # 查找前后10行是否有测试相关内容
                start_idx = max(0, i - 5)
                end_idx = min(len(lines), i + 10)
                context_lines = lines[start_idx:end_idx]
                context_text = '\n'.join(context_lines)

                if not any(keyword in context_text for keyword in ["测试", "验证", "检查", "步骤"]):
                    missing_points.append({
                        "type": "功能缺少测试",
                        "description": "该功能描述缺少相应的测试要点或验证步骤",
                        "severity": "high",
                        "suggestion": "建议为该功能添加具体的测试要点和验证方法",
                        "location": f"第{i+1}行附近",
                        "context": line,
                        "surrounding_text": context_text
                    })

            # 检查数据字段
            if any(keyword in line for keyword in ["字段", "输入框", "输入", "数据项"]):
                # 查找前后5行是否有校验说明
                start_idx = max(0, i - 3)
                end_idx = min(len(lines), i + 5)
                context_lines = lines[start_idx:end_idx]
                context_text = '\n'.join(context_lines)

                if not any(keyword in context_text for keyword in ["校验", "验证", "格式", "限制", "长度", "类型"]):
                    missing_points.append({
                        "type": "数据缺少校验",
                        "description": "该数据字段缺少格式校验或限制说明",
                        "severity": "medium",
                        "suggestion": "建议添加数据格式、长度限制、类型等校验规则",
                        "location": f"第{i+1}行",
                        "context": line,
                        "surrounding_text": context_text
                    })

            # 检查界面元素
            if any(keyword in line for keyword in ["按钮", "菜单", "图标", "图片"]):
                start_idx = max(0, i - 3)
                end_idx = min(len(lines), i + 5)
                context_lines = lines[start_idx:end_idx]
                context_text = '\n'.join(context_lines)

                if not any(keyword in context_text for keyword in ["样式", "颜色", "大小", "位置", "尺寸", "宽度", "高度"]):
                    missing_points.append({
                        "type": "UI缺少具体说明",
                        "description": "该界面元素缺少具体的样式或尺寸说明",
                        "severity": "medium",
                        "suggestion": "建议添加界面元素的具体规格（大小、颜色、位置等）",
                        "location": f"第{i+1}行",
                        "context": line,
                        "surrounding_text": context_text
                    })

            # 检查异常情况
            if any(keyword in line for keyword in ["异常", "错误", "失败", "网络异常", "权限不足"]):
                start_idx = max(0, i - 2)
                end_idx = min(len(lines), i + 5)
                context_lines = lines[start_idx:end_idx]
                context_text = '\n'.join(context_lines)

                if not any(keyword in context_text for keyword in ["提示", "处理", "跳转", "容错", "重试"]):
                    missing_points.append({
                        "type": "缺少异常处理说明",
                        "description": "该异常情况缺少具体的处理方式或提示信息",
                        "severity": "high",
                        "suggestion": "建议添加异常处理逻辑、错误提示信息和恢复方案",
                        "location": f"第{i+1}行",
                        "context": line,
                        "surrounding_text": context_text
                    })

        return missing_points

    def analyze_contradictory_points(self, text: str) -> List[Dict[str, Any]]:
        """
        分析需求中的矛盾点

        Args:
            text: 需求文本内容

        Returns:
            List[Dict]: 矛盾点列表
        """
        contradictory_points = []
        lines = text.split('\n')

        # 提取数字和单位
        number_patterns = []
        patterns = [
            (r'(\d+)\s*个\s*菜单', "菜单数量"),
            (r'(\d+)\s*px|(\d+)\s*像素', "尺寸"),
            (r'(\d+)\s*秒|(\d+)\s*分钟', "时间"),
            (r'(\d+)\s*KB|(\d+)\s*KB|(\d+)\s*MB', "数据量"),
        ]

        for pattern, category in patterns:
            for i, line in enumerate(lines):
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        num = next((m for m in match if m.isdigit()), None)
                    else:
                        num = match

                    if num:
                        number_patterns.append({
                            "category": category,
                            "value": num,
                            "context": line,
                            "line_number": i + 1
                        })

        # 检查同一类别是否有不同数值
        categories = {}
        for item in number_patterns:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)

        for cat, items in categories.items():
            if len(items) > 1:
                values = [item["value"] for item in items]
                if len(set(values)) > 1:
                    # 收集所有矛盾的上下文
                    contexts = []
                    for item in items:
                        contexts.append(f"第{item['line_number']}行: {item['context']}")

                    contradictory_points.append({
                        "type": "数值矛盾",
                        "description": f"关于{cat}的描述存在不同数值: {values}",
                        "severity": "high",
                        "suggestion": "请确认正确的{cat}数值",
                        "location": "多个位置",
                        "conflicting_contexts": contexts
                    })

        # 检查相互矛盾的描述
        矛盾对 = [
            ("必须", "可选", "强制性矛盾"),
            ("固定", "可变", "性质矛盾"),
            ("自动", "手动", "操作方式矛盾"),
            ("开启", "关闭", "状态矛盾")
        ]

        for word1, word2, issue_type in 矛盾对:
            for i, line in enumerate(lines):
                if word1 in line and word2 in line:
                    contradictory_points.append({
                        "type": issue_type,
                        "description": f"在该描述中同时出现了'{word1}'和'{word2}'，可能存在逻辑矛盾",
                        "severity": "medium",
                        "suggestion": "请确认正确的操作逻辑，或者说明两者的适用场景",
                        "location": f"第{i+1}行",
                        "context": line
                    })

        return contradictory_points

    def analyze_unclear_points(self, text: str) -> List[Dict[str, Any]]:
        """
        分析需求中的不明确点

        Args:
            text: 需求文本内容

        Returns:
            List[Dict]: 不明确点列表
        """
        unclear_points = []
        lines = text.split('\n')

        # 检查模糊描述词
        vague_terms = {
            "适当": "没有具体的参数范围或数值",
            "合理": "缺少具体的评判标准和具体值",
            "优化": "缺少具体的优化目标和可衡量指标",
            "改善": "没有明确的改善方向和量化指标",
            "尽快": "缺少具体的时间要求",
            "等": "列表不完整，缺少其他项",
            "等等": "说明不充分",
            "包括但不限于": "边界不明确"
        }

        for i, line in enumerate(lines):
            for term, issue in vague_terms.items():
                if term in line:
                    unclear_points.append({
                        "type": "模糊描述",
                        "description": f"使用模糊词汇'{term}'，{issue}",
                        "severity": "medium",
                        "suggestion": f"建议将'{term}'替换为具体的数值、范围或标准",
                        "location": f"第{i+1}行",
                        "context": line
                    })

            # 检查是否有缩写但无全称
            common_abbreviations = ["UI", "UX", "API", "DB", "URL", "HTTP", "HTTPS"]
            for abbrev in common_abbreviations:
                if abbrev in line:
                    # 简单检查是否有全称说明
                    if abbrev not in ["UI", "UX", "API"]:  # 这些是常见缩写，不提示
                        # 检查同一行或前后行是否有说明
                        start_idx = max(0, i - 1)
                        end_idx = min(len(lines), i + 2)
                        context_lines = lines[start_idx:end_idx]
                        context_text = '\n'.join(context_lines)

                        if f"（{abbrev}）" not in context_text and f"({abbrev})" not in context_text:
                            unclear_points.append({
                                "type": "缩写不明确",
                                "description": f"使用了缩写'{abbrev}'但没有全称说明",
                                "severity": "low",
                                "suggestion": "建议提供缩写的全称或技术标准",
                                "location": f"第{i+1}行",
                                "context": line
                            })

        return unclear_points

    def analyze_incomplete_points(self, text: str) -> List[Dict[str, Any]]:
        """
        分析需求中的不完整点

        Args:
            text: 需求文本内容

        Returns:
            List[Dict]: 不完整点列表
        """
        incomplete_points = []

        # 检查是否有列表但是数量不符合
        list_content = re.findall(r'\d+[.、)\]]\s*[^0-9]', text)
        if list_content:
            if len(list_content) > 8:
                incomplete_points.append({
                    "type": "列表过长",
                    "description": f"发现{len(list_content)}列表项，可能需要分类整理",
                    "severity": "low",
                    "suggestion": "建议将长列表按照功能或类型进行分组"
                })

        # 检查是否有未完成的句子
        incomplete_sentences = re.findall(r'[。！？，、,][^。！？\n]{0,5}$', text, re.MULTILINE)
        if incomplete_sentences:
            incomplete_points.append({
                "type": "句子不完整",
                "description": "发现可能未完成的句子，内容可能不完整",
                "severity": "medium",
                "suggestion": "建议检查是否有遗漏的内容描述"
            })

        return incomplete_points

    def analyze(self):
        """执行完整的需求分析"""
        if not self.load_document():
            return False

        # 提取文本内容
        text = self.extract_text_content()
        print(f"文档文本长度: {len(text)} 字符")

        # 执行各类分析
        print("\n开始分析需求...")

        self.issues["missing_points"] = self.analyze_missing_points(text)
        print(f"发现遗漏点: {len(self.issues['missing_points'])} 个")

        self.issues["contradictory_points"] = self.analyze_contradictory_points(text)
        print(f"发现矛盾点: {len(self.issues['contradictory_points'])} 个")

        self.issues["unclear_points"] = self.analyze_unclear_points(text)
        print(f"发现不明确点: {len(self.issues['unclear_points'])} 个")

        self.issues["incomplete_points"] = self.analyze_incomplete_points(text)
        print(f"发现不完整点: {len(self.issues['incomplete_points'])} 个")

        return True

    def generate_report(self, output_path=None):
        """
        生成分析报告

        Args:
            output_path: 报告输出路径，默认为文档同级目录下的JSON文件

        Returns:
            str: 报告文件路径
        """
        if output_path is None:
            output_path = self.doc_path.parent / f"{self.doc_path.stem}_analysis_report.json"

        report = {
            "document": str(self.doc_path),
            "analyzed_at": __import__('datetime').datetime.now().isoformat(),
            "summary": {
                "missing_points": len(self.issues["missing_points"]),
                "contradictory_points": len(self.issues["contradictory_points"]),
                "unclear_points": len(self.issues["unclear_points"]),
                "incomplete_points": len(self.issues["incomplete_points"])
            },
            "issues": self.issues
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n分析报告已保存到: {output_path}")

        # 生成人类可读的报告
        report_file = self.doc_path.parent / f"{self.doc_path.stem}_analysis_report.txt"
        self._generate_human_readable_report(report_file)

        return str(report_file)

    def _generate_human_readable_report(self, output_path):
        """生成人类可读的报告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("需求分析报告\n")
            f.write("="*70 + "\n\n")

            f.write(f"分析文件: {self.doc_path}\n")
            f.write(f"分析时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # 遗漏点
            if self.issues["missing_points"]:
                f.write("【遗漏点】\n")
                f.write("-"*70 + "\n\n")
                for i, issue in enumerate(self.issues["missing_points"], 1):
                    f.write(f"{i}. {issue['type']} (严重程度: {issue['severity']})\n")
                    f.write(f"   位置: {issue.get('location', '未知')}\n")
                    f.write(f"   问题描述: {issue['description']}\n")

                    # 显示需求原文
                    if "context" in issue:
                        f.write(f"   需求原文: {issue['context']}\n")

                    # 显示上下文
                    if "surrounding_text" in issue and issue['surrounding_text']:
                        f.write(f"   上下文: {issue['surrounding_text'][:200]}...\n")

                    f.write(f"   改进建议: {issue['suggestion']}\n")
                    f.write(f"\n")
            else:
                f.write("【遗漏点】[OK] 暂无明显遗漏点\n\n")

            # 矛盾点
            if self.issues["contradictory_points"]:
                f.write("【矛盾点】\n")
                f.write("-"*70 + "\n\n")
                for i, issue in enumerate(self.issues["contradictory_points"], 1):
                    f.write(f"{i}. {issue['type']} (严重程度: {issue['severity']})\n")
                    f.write(f"   位置: {issue.get('location', '多个位置')}\n")
                    f.write(f"   问题描述: {issue['description']}\n")

                    # 显示需求原文
                    if "context" in issue:
                        f.write(f"   需求原文: {issue['context']}\n")

                    # 显示矛盾的上下文
                    if "conflicting_contexts" in issue:
                        f.write(f"   矛盾的具体位置:\n")
                        for ctx in issue['conflicting_contexts']:
                            f.write(f"     - {ctx}\n")

                    f.write(f"   改进建议: {issue['suggestion']}\n")
                    f.write(f"\n")
            else:
                f.write("【矛盾点】[OK] 暂无明显矛盾点\n\n")

            # 不明确点
            if self.issues["unclear_points"]:
                f.write("【不明确点】\n")
                f.write("-"*70 + "\n\n")
                for i, issue in enumerate(self.issues["unclear_points"], 1):
                    f.write(f"{i}. {issue['type']} (严重程度: {issue['severity']})\n")
                    f.write(f"   位置: {issue.get('location', '未知')}\n")
                    f.write(f"   问题描述: {issue['description']}\n")

                    # 显示需求原文
                    if "context" in issue:
                        f.write(f"   需求原文: {issue['context']}\n")

                    f.write(f"   改进建议: {issue['suggestion']}\n")
                    f.write(f"\n")
            else:
                f.write("【不明确点】[OK] 暂无明显不明确点\n\n")

            # 不完整点
            if self.issues["incomplete_points"]:
                f.write("【不完整点】\n")
                f.write("-"*70 + "\n\n")
                for i, issue in enumerate(self.issues["incomplete_points"], 1):
                    f.write(f"{i}. {issue['type']} (严重程度: {issue['severity']})\n")
                    f.write(f"   位置: {issue.get('location', '未知')}\n")
                    f.write(f"   问题描述: {issue['description']}\n")

                    # 显示需求原文
                    if "context" in issue:
                        f.write(f"   需求原文: {issue['context']}\n")

                    f.write(f"   改进建议: {issue['suggestion']}\n")
                    f.write(f"\n")
            else:
                f.write("【不完整点】[OK] 暂无明显不完整点\n\n")

            f.write("="*70 + "\n")
            f.write(f"分析完成 | 总问题数: {sum([len(v) for v in self.issues.values()])}\n")
            f.write(f"  - 遗漏点: {len(self.issues['missing_points'])}\n")
            f.write(f"  - 矛盾点: {len(self.issues['contradictory_points'])}\n")
            f.write(f"  - 不明确点: {len(self.issues['unclear_points'])}\n")
            f.write(f"  - 不完整点: {len(self.issues['incomplete_points'])}\n")
            f.write("="*70 + "\n")

        print(f"人类可读报告已保存到: {output_path}")

    def get_issues(self):
        """获取分析结果"""
        return self.issues


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="需求分析工具 - 分析Word文档中的遗漏点、矛盾点和不明确点",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python analyze_requirements.py demand/需求文档.docx
  python analyze_requirements.py demand/需求文档.docx --output custom_report.json
        """
    )

    parser.add_argument("doc_file", help="Word文档路径")
    parser.add_argument("--output", help="输出报告路径（可选）")

    args = parser.parse_args()

    # 创建分析器
    analyzer = RequirementAnalyzer(args.doc_file)

    # 执行分析
    if analyzer.analyze():
        # 生成报告
        report_path = analyzer.generate_report(args.output)
        print(f"\n分析完成！")
        print(f"报告文件: {report_path}")
    else:
        print("\n分析失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()