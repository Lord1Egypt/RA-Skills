#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求文档批量检查工具（AI 驱动版）
默认使用 LLM 进行智能检查，规则检查仅作为 fallback
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# 导入解析器
sys.path.insert(0, str(Path(__file__).parent))
from parse_requirement import RequirementParser

# 导入 LLM 检查器
try:
    from check_with_llm import check_with_llm, get_llm_config

    llm_config = get_llm_config()
    USE_LLM_CHECKER = llm_config is not None

    if USE_LLM_CHECKER:
        print(f"\n✅ AI 驱动模式：已加载 LLM 配置")
        print(f"   Source: {llm_config.get('source', 'unknown')}")
        print(f"   Base URL: {llm_config['base_url']}")
        print(f"   Model: {llm_config.get('model', 'glm-5')}")
except ImportError as e:
    print(f"⚠️  LLM 检查器不可用：{e}")
    USE_LLM_CHECKER = False

# 导入 LLM GWT 生成器
try:
    from generate_gwt_with_llm import generate_gwt_with_llm, call_llm_for_gwt
    USE_GWT_LLM = True
except ImportError as e:
    print(f"⚠️  LLM GWT 生成器不可用：{e}")
    USE_GWT_LLM = False


class BatchRequirementChecker:
    """批量需求检查器（AI 驱动）"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.parser = RequirementParser()

        self.stats = {
            "total_files": 0,
            "success_count": 0,
            "warning_count": 0,
            "issue_count": 0,
            "start_time": None,
            "end_time": None,
        }

        self.results = []

    def scan_directory(self, input_dir: str, recursive: bool = True) -> List[Path]:
        """扫描目录中的所有需求文件"""
        input_path = Path(input_dir)

        if not input_path.exists():
            raise FileNotFoundError(f"目录不存在：{input_dir}")

        files = []
        if recursive:
            for ext in [".docx", ".md", ".txt", ".pdf"]:
                files.extend(input_path.rglob(f"*{ext}"))
        else:
            for ext in [".docx", ".md", ".txt", ".pdf"]:
                files.extend(input_path.glob(f"*{ext}"))

        files = [
            f
            for f in files
            if not f.name.startswith(".") and not f.name.startswith("~")
        ]
        return sorted(files)

    def check_file(self, file_path: Path) -> Dict:
        """检查单个文件（AI 驱动）"""
        try:
            # 解析文件获取内容
            parse_result = self.parser.parse(str(file_path))

            if not parse_result["success"]:
                return {
                    "success": False,
                    "file": str(file_path),
                    "error": parse_result.get("error", "解析失败"),
                }

            content = parse_result["content"]

            # AI 驱动检查（优先使用 LLM）
            if USE_LLM_CHECKER:
                print(f"  🤖 AI 智能检查中...")
                llm_result = check_with_llm(content, str(file_path))

                # LLM 返回的结果直接作为检查结果
                pre_check = {
                    "summary": llm_result.get("summary", {}),
                    "warnings": llm_result.get("warnings", []),
                    "passed": llm_result.get("passed", []),
                    "gwt_analysis": llm_result.get("gwt_acceptance", {}),
                    "source": "llm",
                }
            else:
                print(f"  ⚠️  LLM 不可用，跳过 AI 检查")
                pre_check = {
                    "summary": {},
                    "warnings": [],
                    "passed": [],
                    "gwt_analysis": {},
                    "source": "rules",
                }

            # 统计信息
            summary = pre_check.get("summary", {})

            self.stats["success_count"] += 1
            if summary.get("warning_count", 0) > 0:
                self.stats["warning_count"] += 1
            if summary.get("issue_count", 0) > 0:
                self.stats["issue_count"] += 1

            return {
                "success": True,
                "file": str(file_path),
                "result": {"parse_result": parse_result, "pre_check": pre_check},
                "content": content,
            }

        except Exception as e:
            return {"success": False, "file": str(file_path), "error": str(e)}

    def generate_individual_report(self, file_result: Dict) -> str:
        """生成单个文件的检查报告"""
        if not file_result["success"]:
            return f"""# ❌ 检查失败：{file_result["file"]}

**错误**: {file_result.get("error", "未知错误")}

**检查时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        result = file_result["result"]
        parse_result = result.get("parse_result", {})
        pre_check = result.get("pre_check", {})

        metadata = parse_result.get("metadata", {})
        summary = pre_check.get("summary", {})
        gwt_analysis = pre_check.get("gwt_analysis", {})
        warnings = pre_check.get("warnings", [])
        passed = pre_check.get("passed", [])

        # 计算评分和结论
        score_result = self.calculate_score_and_conclusion(pre_check)

        report = []
        report.append("# 📋 需求规范检查报告（AI 驱动）")
        report.append("")
        report.append(f"**文件**: {metadata.get('source', file_result['file'])}")
        report.append(f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(
            f"**检查方式**: {'🤖 LLM 智能检查' if pre_check.get('source') == 'llm' else '📋 规则检查'}"
        )
        report.append("")

        # 评分和结论（友好版）
        report.append("## 🎯 检查结论")
        report.append("")

        conclusion = score_result["conclusion"]
        score = score_result["score"]

        report.append(f"**结论**: {conclusion}")
        report.append("")

        report.append(f"**说明**: {score_result['reason']}")
        report.append("")

        # 概览
        report.append("## 📊 检查概览")
        report.append("")
        report.append("*以下为检查情况概览，具体建议请查看下方详细内容*")
        report.append("")
        report.append(f"- **符合规范的检查项**: {len(passed)}")
        report.append(f"- **可能需要完善的地方**: {len(warnings)}")
        report.append(f"- **建议再确认一下的地方**: {summary.get('issue_count', 0)}")
        has_gwt = gwt_analysis.get("auto_generated", [])
        report.append(
            f"- **验收标准**: {'✅ 已生成参考标准' if has_gwt else '⚠️ 可补充验收标准'}"
        )
        report.append("")

        # GWT 验收标准
        report.append("## 📋 GWT 验收标准检查")
        report.append("")
        if gwt_analysis.get("has_gwt"):
            report.append("✅ 文档已包含 GWT 格式的验收标准")
        elif has_gwt:
            report.append("⚠️ 文档缺少 GWT 格式的验收标准")
            report.append("")
            report.append("**已自动生成的验收标准**:")
            report.append("")

            # 打印具体的 GWT 场景
            for i, gwt in enumerate(has_gwt, 1):
                report.append(f"### 验收场景 {i}: {gwt.get('category', '验证')}")
                report.append(f"- **Given**（给定）: {gwt.get('given', '')}")
                report.append(f"- **When**（当）: {gwt.get('when', '')}")
                report.append(f"- **Then**（那么）: {gwt.get('then', '')}")
                if gwt.get("reason"):
                    report.append(f"- **理由**: {gwt.get('reason', '')}")
                report.append("")

            # 专家点评
            if gwt_analysis.get("expert_comment"):
                report.append("**专家点评**:")
                report.append(gwt_analysis.get("expert_comment", ""))
                report.append("")
        else:
            report.append("⚠️ 文档缺少 GWT 格式的验收标准")
            report.append("")
            report.append("建议补充的验收标准:")
            report.append("")
            report.append("无")
        report.append("")

        # 通过项
        if passed:
            report.append("## ✅ 通过检查")
            report.append("")
            for item in passed:
                report.append(f"- {item}")
            report.append("")

        # 详细问题（温柔话术）
        if warnings:
            report.append("## 💡 可能需要关注的地方")
            report.append("")
            report.append("*以下建议供参考，你可以根据实际需求情况选择采纳*")
            report.append("")
            for i, warning in enumerate(warnings, 1):
                # 兼容 LLM 格式和规则检查格式
                rule_name = warning.get("rule", warning.get("dimension", "未知维度"))
                report.append(f"### {i}. 【{rule_name}】")
                report.append("")

                # 温柔的问题说明
                issue_text = warning.get("issue", "")
                if issue_text:
                    if "未" in issue_text or "缺少" in issue_text or "不" in issue_text:
                        # 把否定句改成建议句
                        issue_text = (
                            issue_text.replace("未", "如果能")
                            .replace("缺少", "可以考虑增加")
                            .replace("不明确", "可以更明确")
                        )
                        report.append(f"**可能需要注意**:")
                        report.append(f"{issue_text}")
                    else:
                        report.append(f"**问题说明**:")
                        report.append(f"{issue_text}")

                # 原文引用（支持多种字段名）
                evidence = warning.get("evidence", []) or warning.get("quote", [])
                if evidence:
                    report.append("")
                    report.append("**原文引用**:")
                    for e in evidence[:3]:
                        report.append(f"- {e}")

                # 温柔的建议
                suggestion = warning.get("suggestion", "")
                if suggestion:
                    report.append("")
                    if "必须" in suggestion or "建议" in suggestion:
                        # 软化语气
                        suggestion = suggestion.replace("必须", "建议").replace(
                            "应该", "可以"
                        )
                    report.append(f"**优化建议**:")
                    report.append(f"{suggestion}")
                    report.append("")
                    report.append("*注：如果当前需求不需要这些内容，可以忽略此建议*")

                report.append("")

        return "\n".join(report)

    def generate_gwt_batch(self) -> None:
        """批量生成 GWT 验收标准（LLM 驱动）"""
        if not USE_GWT_LLM:
            print("  ⚠️  LLM GWT 生成器不可用，跳过 GWT 生成")
            return

        print("  🧪 正在生成 GWT 验收标准...")

        for result in self.results:
            if not result["success"]:
                continue

            parse_result = result["result"].get("parse_result", {})
            pre_check = result["result"].get("pre_check", {})
            content = result.get("content", "")
            filename = result["file"]

            # 如果文档已有 GWT，跳过生成
            gwt_analysis = pre_check.get("gwt_analysis", {})
            if gwt_analysis.get("has_gwt"):
                print(f"    ✅ {Path(filename).name}: 文档已有 GWT，跳过生成")
                continue

            # 调用 LLM 生成 GWT
            gwt_result = call_llm_for_gwt(content, filename)

            if gwt_result.get("success"):
                auto_generated = gwt_result.get("auto_generated", [])
                pre_check["gwt_analysis"]["auto_generated"] = auto_generated
                pre_check["gwt_analysis"]["expert_comment"] = gwt_result.get(
                    "expert_comment", ""
                )
                pre_check["gwt_analysis"]["source"] = "llm_generated"
                print(
                    f"    ✅ {Path(filename).name}: 生成 {len(auto_generated)} 个验收场景"
                )
            else:
                error_msg = gwt_result.get("error", "未知错误")
                print(f"    ⚠️  {Path(filename).name}: GWT 生成失败 - {error_msg}")

    def calculate_score_and_conclusion(self, pre_check: Dict) -> Dict:
        """计算评分和结论（友好版，支持优先级分级）"""
        summary = pre_check.get("summary", {})
        gwt_analysis = pre_check.get("gwt_analysis", {})
        suggestions = pre_check.get("suggestions", pre_check.get("warnings", []))

        # 支持 LLM 返回的字段名
        compliance_rate = summary.get("compliance_rate", 100)
        suggestion_count = summary.get("suggestion_count", len(suggestions))

        # 按优先级统计建议数量
        core_suggestions = [s for s in suggestions if s.get("priority") == "core"]
        improve_suggestions = [s for s in suggestions if s.get("priority") == "improve"]
        optimize_suggestions = [
            s for s in suggestions if s.get("priority") == "optimize"
        ]

        core_count = len(core_suggestions)
        improve_count = len(improve_suggestions)
        optimize_count = len(optimize_suggestions)

        # 计算评分（基于优先级）
        score = compliance_rate

        # 核心建议扣分较多（影响理解）
        score -= core_count * 15

        # 完善建议扣分适中
        score -= improve_count * 10

        # 优化建议扣分较少
        score -= optimize_count * 5

        # GWT缺失扣分
        if not gwt_analysis.get("auto_generated"):
            score -= 10

        # 确保分数在0-100之间
        score = max(0, min(100, score))
        score = round(score, 1)

        # 友好版结论（帮助性话术）
        if score >= 85 and core_count == 0:
            conclusion = "🌟 质量优秀"
            reason = "文档质量很好，内容完整清晰，可以帮助团队快速理解需求"
        elif score >= 70 and core_count <= 1:
            conclusion = "✅ 通过"
            reason = f"整体不错，有{improve_count + optimize_count}项可以优化，能帮助团队更好理解需求"
        elif score >= 50:
            conclusion = "💡 建议自检"
            reason = f"有{core_count}项核心建议、{improve_count}项完善建议，建议补充后会更清晰"
        else:
            conclusion = "🔧 建议完善"
            reason = f"有{core_count}项核心建议需要补充，完善后可以帮助团队更好实施"

        return {
            "score": score,
            "conclusion": conclusion,
            "reason": reason,
            "core_count": core_count,
            "improve_count": improve_count,
            "optimize_count": optimize_count,
        }

    def generate_summary_report(self) -> str:
        """生成汇总报告"""
        report = []
        report.append("# 📊 需求文档批量检查汇总报告（AI 驱动）")
        report.append("")
        report.append(
            f"**检查时间**: {self.stats['start_time']} - {self.stats['end_time']}"
        )
        report.append("")

        # 计算总体评分
        total_score = 0
        pass_count = 0
        partial_pass_count = 0
        reject_count = 0

        for result in self.results:
            if result["success"]:
                pre_check = result["result"].get("pre_check", {})
                score_result = self.calculate_score_and_conclusion(pre_check)
                total_score += score_result["score"]

                if score_result["conclusion"] == "通过":
                    pass_count += 1
                elif score_result["conclusion"] == "部分通过":
                    partial_pass_count += 1
                else:
                    reject_count += 1

        avg_score = (
            round(total_score / self.stats["success_count"], 1)
            if self.stats["success_count"] > 0
            else 0
        )

        # 总体结论（友好版）
        if reject_count > 0:
            overall_conclusion = f"🔧 有{reject_count}个文档需要改进，建议优先完善"
        elif partial_pass_count > self.stats["success_count"] * 0.5:
            overall_conclusion = f"💡 超过半数文档建议自检，可以统一确认一下"
        elif pass_count > self.stats["success_count"] * 0.8:
            overall_conclusion = f"✅ 整体质量良好，大部分文档可以直接评审"
        else:
            overall_conclusion = f"🌟 整体质量优秀，可以进入评审阶段"

        # 统计信息
        report.append("## 📈 统计信息")
        report.append("")
        report.append(f"- **总文件数**: {self.stats['total_files']}")
        report.append(f"- **检查成功**: {self.stats['success_count']}")
        report.append(f"- **存在警告**: {self.stats['warning_count']}")
        report.append(f"- **存在问题**: {self.stats['issue_count']}")
        report.append("")

        # 总体评分
        report.append("## 🎯 总体评分")
        report.append("")
        report.append(f"**平均评分**: **{avg_score}/100**")
        report.append("")
        report.append(f"**通过**: {pass_count} 个 ✅")
        report.append(f"**部分通过**: {partial_pass_count} 个 ⚠️")
        report.append(f"**打回**: {reject_count} 个 ❌")
        report.append("")
        report.append(f"**总体结论**: {overall_conclusion}")
        report.append("")

        # 文件列表
        report.append("## 📁 文件检查详情")
        report.append("")
        report.append("| 文件名 | 评分 | 结论 | 合规率 | 警告 | 问题 | GWT | 报告 |")
        report.append("|--------|------|------|--------|------|------|-----|------|")

        for result in self.results:
            filename = Path(result["file"]).name

            if result["success"]:
                pre_check = result["result"].get("pre_check", {})
                summary = pre_check.get("summary", {})
                score_result = self.calculate_score_and_conclusion(pre_check)

                score = score_result["score"]
                conclusion = score_result["conclusion"]

                # 友好版结论图标
                if "优秀" in conclusion:
                    conclusion_icon = "🌟"
                elif "通过" in conclusion:
                    conclusion_icon = "✅"
                elif "自检" in conclusion:
                    conclusion_icon = "💡"
                else:
                    conclusion_icon = "🔧"

                compliance = summary.get("compliance_rate", 100)
                warnings = len(pre_check.get("warnings", []))
                issues = summary.get("issue_count", 0)
                has_gwt = (
                    "✅"
                    if pre_check.get("gwt_analysis", {}).get("auto_generated")
                    else "❌"
                )

                report_name = f"{Path(result['file']).stem}_report.md"
                report_link = f"[查看](./{report_name})"

                report.append(
                    f"| {filename} | {score} | {conclusion_icon} {conclusion} | {compliance}% | {warnings} | {issues} | {has_gwt} | {report_link} |"
                )
            else:
                report.append(
                    f"| {filename} | N/A | ❌ 失败 | N/A | N/A | N/A | N/A | ❌ 失败 |"
                )

        report.append("")

        return "\n".join(report)

    def run(
        self, input_dir: str, recursive: bool = True, generate_summary: bool = False
    ) -> None:
        """执行批量检查（AI 驱动）

        Args:
            input_dir: 输入目录
            recursive: 是否递归扫描子目录
            generate_summary: 是否生成汇总报告（默认 False）
        """
        print(f"🔍 开始扫描目录：{input_dir}")
        print()

        self.stats["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 扫描文件
        files = self.scan_directory(input_dir, recursive)
        self.stats["total_files"] = len(files)

        print(f"📁 找到 {len(files)} 个需求文件")
        print()

        # 逐个检查（AI 驱动）
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 检查：{file_path.name}")

            result = self.check_file(file_path)
            self.results.append(result)

            if result["success"]:
                pre_check = result["result"].get("pre_check", {})
                summary = pre_check.get("summary", {})
                print(
                    f"  ✅ 检查完成 - 合规率：{summary.get('compliance_rate', 100)}%, 警告：{len(pre_check.get('warnings', []))}个"
                )
            else:
                print(f"  ❌ 检查失败：{result.get('error', '未知错误')}")

        # 批量生成 GWT 验收标准
        print()
        self.generate_gwt_batch()

        # 记录结束时间
        self.stats["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print()
        print("📝 生成报告...")

        # 生成 individual 报告
        for result in self.results:
            if result["success"]:
                report_md = self.generate_individual_report(result)
                report_path = self.output_dir / f"{Path(result['file']).stem}_report.md"
                report_path.write_text(report_md, encoding="utf-8")
                print(f"  ✅ 生成报告：{report_path.name}")

        # 生成汇总报告（可选）
        if generate_summary:
            summary_md = self.generate_summary_report()
            summary_path = self.output_dir / "00_汇总报告.md"
            summary_path.write_text(summary_md, encoding="utf-8")
            print(f"  ✅ 生成汇总报告：{summary_path.name}")
        else:
            print(f"  ℹ️  跳过汇总报告（如需生成请使用 --summary 参数）")

        # 生成 JSON 结果
        json_data = {"stats": self.stats, "results": []}

        for result in self.results:
            json_result = {"file": result["file"], "success": result["success"]}

            if result["success"]:
                pre_check = result["result"].get("pre_check", {})
                json_result["summary"] = pre_check.get("summary", {})
                json_result["warnings"] = pre_check.get("warnings", [])
                json_result["passed"] = pre_check.get("passed", [])
                json_result["gwt"] = pre_check.get("gwt_analysis", {})
                score_result = self.calculate_score_and_conclusion(pre_check)
                json_result["score"] = score_result["score"]
                json_result["conclusion"] = score_result["conclusion"]
            else:
                json_result["error"] = result.get("error", "")

            json_data["results"].append(json_result)

        json_path = self.output_dir / "检查结果.json"
        json_path.write_text(
            json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  ✅ 生成 JSON 结果：{json_path.name}")

        print()
        print("=" * 60)
        print("✅ 批量检查完成！")
        print("=" * 60)
        print()
        print(f"📊 统计信息:")
        print(f"  - 总文件数：{self.stats['total_files']}")
        print(f"  - 检查成功：{self.stats['success_count']}")
        print(f"  - 存在警告：{self.stats['warning_count']}")
        print(f"  - 存在问题：{self.stats['issue_count']}")
        print()
        print(f"📁 报告目录：{self.output_dir}")
        print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="需求文档批量检查工具（AI 驱动版）")
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=None,
        help="输入目录（包含需求文件的目录，可选，默认从 config.json 读取）",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="报告输出目录（可选，默认从 config.json 读取）",
    )
    parser.add_argument("--no-recursive", action="store_true", help="不递归扫描子目录")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="生成汇总报告（默认不生成，仅在需要时生成）",
    )

    args = parser.parse_args()

    # 加载配置
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        input_dir = args.input_dir or config.get("directories", {}).get("input")
        output_dir = args.output_dir or config.get("directories", {}).get("output")
    else:
        input_dir = args.input_dir
        output_dir = args.output_dir or "./requirement_reports"

    if not input_dir:
        print("❌ 错误：未指定输入目录")
        print()
        print("用法:")
        print("  1. 命令行指定：python3 batch_check_ai.py /path/to/input/")
        print("  2. 配置文件：编辑 config.json 中的 directories.input")
        print()
        parser.print_help()
        sys.exit(1)

    if not output_dir:
        output_dir = "./requirement_reports"

    # 创建批量检查器
    batch_checker = BatchRequirementChecker(output_dir)

    # 执行批量检查
    batch_checker.run(
        input_dir, recursive=not args.no_recursive, generate_summary=args.summary
    )


if __name__ == "__main__":
    main()
