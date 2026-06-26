#!/usr/bin/env python3
"""
测试用例生成工具 - generate_testcases.py

根据需求文档自动生成测试用例，支持多种测试设计方法
"""

import sys
import re
import json
from pathlib import Path
from docx import Document
from typing import List, Dict, Any, Tuple
from datetime import datetime


class TestCaseGenerator:
    """测试用例生成器"""

    def __init__(self, doc_path):
        """
        初始化测试用例生成器

        Args:
            doc_path: Word 文档路径
        """
        self.doc_path = Path(doc_path)
        self.doc = None
        self.content = ""
        self.test_cases = []
        self.tc_counter = 1

    def load_document(self):
        """加载 Word 文档"""
        try:
            self.doc = Document(self.doc_path)
            print(f"成功加载文档: {self.doc_path}")
            return True
        except Exception as e:
            print(f"文档加载失败: {e}")
            return False

    def extract_content(self):
        """提取文档内容"""
        if not self.doc:
            return

        content_parts = []
        for para in self.doc.paragraphs:
            if para.text.strip():
                content_parts.append(para.text)

        self.content = "\n".join(content_parts)
        print(f"提取文本内容: {len(self.content)} 字符")

    def add_test_case(self, module: str, title: str, preconditions: str,
                      steps: str, priority: str, expected_result: str, method: str = ""):
        """
        添加测试用例

        Args:
            module: 测试模块
            title: 用例标题
            preconditions: 前置条件
            steps: 测试步骤
            priority: 优先级
            expected_result: 预期结果
            method: 测试方法
        """
        self.test_cases.append({
            "id": f"TC{self.tc_counter:03d}",
            "module": module,
            "title": title,
            "preconditions": preconditions,
            "steps": steps,
            "priority": priority,
            "expected_result": expected_result,
            "method": method
        })
        self.tc_counter += 1

    def extract_features_from_text(self) -> List[Dict[str, Any]]:
        """
        从文本中提取功能特性

        Returns:
            List[Dict]: 功能特性列表
        """
        features = []

        # 提取标题和功能模块
        lines = self.content.split('\n')
        current_module = "全局"

        for line in lines:
            line = line.strip()

            # 识别标题（可能是模块名）
            if line.startswith('##') or line.startswith('# '):
                module_name = line.lstrip('# ')
                if module_name and len(module_name) < 20:  # 假设模块名不超过20个字
                    current_module = module_name

            # 识别功能描述
            feature_keywords = ["功能", "模块", "支持", "显示", "验证", "测试", "实现"]
            if any(keyword in line for keyword in feature_keywords) and len(line) > 10:
                features.append({
                    "module": current_module,
                    "description": line
                })

        print(f"提取到 {len(features)} 个功能特性")
        return features

    def generate_positive_test_cases(self, features: List[Dict[str, Any]]):
        """
        生成正向测试用例（基于功能特性）

        Args:
            features: 功能特性列表
        """
        print("\n生成正向测试用例...")

        for feature in features[:20]:  # 限制数量
            module = feature["module"]
            desc = feature["description"]

            # 提取关键词
            action = ""
            if "验证" in desc:
                action = "验证"
            elif "测试" in desc:
                action = "测试"
            elif "显示" in desc:
                action = "验证显示"
            elif "支持" in desc:
                action = "验证支持"
            else:
                action = "测试"

            title = f"{action}{module}功能正常"
            preconditions = f"1. 系统已部署\n2. {module}模块已配置"
            steps = f"1. 进入{module}模块\n2. 执行相关操作\n3. 观察结果"
            expected = f"1. {module}功能正常工作\n2. 无错误提示\n3. 界面显示正常"

            self.add_test_case(module, title, preconditions, steps, "高", expected, "正向测试")

    def generate_boundary_test_cases(self, features: List[Dict[str, Any]]):
        """
        生成边界值测试用例

        Args:
            features: 功能特性列表
        """
        print("\n生成边界值测试用例...")

        # 提取数字和限制
        numbers = re.findall(r'(\d+)\s*(个|条|次|秒|分钟|小时|天)', self.content)

        # 去重并限制数量，转换为列表后切片
        unique_numbers = list(set(numbers))[:5]
        for i, (num, unit) in enumerate(unique_numbers):
            num = int(num)
            module = "边界值测试"

            # 最小值测试
            title = f"验证{unit}数为{max(0, num-1)}时的边界"
            preconditions = f"1. 系统已部署\n2. 可配置{unit}数"
            steps = f"1. 设置{unit}数为{max(0, num-1)}\n2. 执行操作\n3. 观察结果"
            expected = f"1. 系统正常处理\n2. 无错误提示\n3. 功能正常"
            self.add_test_case(module, title, preconditions, steps, "高", expected, "边界值测试")

            # 最大值+1测试
            title = f"验证{unit}数为{num+1}时的边界"
            steps = f"1. 设置{unit}数为{num+1}\n2. 执行操作\n3. 观察结果"
            expected = f"1. 系统正确处理或提示上限\n2. 无崩溃\n3. 有明确提示信息"
            self.add_test_case(module, title, preconditions, steps, "中", expected, "边界值测试")

    def generate_exception_test_cases(self, features: List[Dict[str, Any]]):
        """
        生成异常测试用例（错误推测法）

        Args:
            features: 功能特性列表
        """
        print("\n生成异常测试用例...")

        # 常见异常场景
        exception_scenarios = [
            ("网络异常", "验证网络断开时的系统表现", "断网", "系统有明确的网络错误提示，无崩溃"),
            ("权限异常", "验证权限不足时的系统表现", "移除权限", "系统提示权限不足，引导用户授权"),
            ("数据异常", "验证数据为空时的系统表现", "清空数据", "显示空状态提示，无崩溃"),
            ("输入异常", "验证特殊字符输入的处理", "输入特殊字符<>'\"", "正确处理或过滤，无XSS风险"),
            ("并发异常", "验证多用户并发操作", "模拟并发请求", "系统正确处理并发，无数据错乱"),
            ("超时异常", "验证请求超时的处理", "模拟超时场景", "系统提示超时，支持重试"),
            ("存储异常", "验证存储空间不足时的处理", "模拟存储已满", "系统提示存储不足，引导清理"),
        ]

        for module, title, step_add, expected in exception_scenarios:
            preconditions = "1. 系统已部署\n2. 测试环境已准备"
            steps = f"1. {step_add}\n2. 执行相关操作\n3. 观察系统反应"
            self.add_test_case(module, title, preconditions, steps, "中", expected, "错误推测")

    def generate_scene_test_cases(self, features: List[Dict[str, Any]]):
        """
        生成场景测试用例（场景法）

        Args:
            features: 功能特性列表
        """
        print("\n生成场景测试用例...")

        # 基本流程场景
        scenarios = [
            ("登录流程", "验证完整登录流程",
             "1. 用户账号已创建",
             "1. 打开应用\n2. 输入账号密码\n3. 点击登录\n4. 完成验证",
             "登录成功，进入主页"),
            ("核心功能流程", "验证核心功能完整流程",
             "1. 已登录系统\n2. 有操作权限",
             "1. 进入核心功能模块\n2. 执行完整操作流程\n3. 完成业务流程",
             "流程顺畅，功能正常，数据正确"),
            ("退出流程", "验证安全退出流程",
             "1. 已登录系统",
             "1. 点击退出\n2. 确认退出\n3. 观察退出过程",
             "安全退出，数据保存，跳转登录页"),
        ]

        for module, title, preconditions, steps, expected in scenarios:
            self.add_test_case(module, title, preconditions, steps, "高", f"1. {expected}", "场景法")

    def generate_ui_test_cases(self, features: List[Dict[str, Any]]):
        """
        生成UI测试用例

        Args:
            features: 功能特性列表
        """
        print("\n生成UI测试用例...")

        # 提取界面相关的特性
        ui_keywords = ["界面", "页面", "按钮", "菜单", "图标", "显示"]

        for feature in features[:10]:  # 限制数量
            desc = feature["description"]
            if any(keyword in desc for keyword in ui_keywords):
                module = "UI测试"
                title = f"验证{desc[:30]}的正确显示"
                preconditions = "1. 系统已部署\n2. 设备已准备"
                steps = f"1. 查看相关界面\n2. 检查{desc[:20]}\n3. 验证显示效果"
                expected = "1. 显示清晰无错位\n2. 样式符合设计\n3. 无兼容性问题"

                self.add_test_case(module, title, preconditions, steps, "中", expected, "UI测试")

    def generate_compatibility_test_cases(self):
        """生成兼容性测试用例"""
        print("\n生成兼容性测试用例...")

        compatibility_scenarios = [
            ("兼容性", "验证不同浏览器兼容性",
             "1. 准备多种浏览器",
             "1. 在Chrome测试\n2. 在Firefox测试\n3. 在Safari测试",
             "所有浏览器功能正常"),
            ("兼容性", "验证不同分辨率适配",
             "1. 准备不同分辨率设备",
             "1. 测试高分辨率\n2. 测试标准分辨率\n3. 测试低分辨率",
             "界面自适应正常，无错位"),
            ("兼容性", "验证不同系统版本兼容性",
             "1. 准备不同系统版本",
             "1. 在高版本系统测试\n2. 在标准版本测试\n3. 在低版本测试",
             "所有版本功能正常"),
        ]

        for module, title, preconditions, steps, expected in compatibility_scenarios:
            self.add_test_case(module, title, preconditions, steps, "中", f"1. {expected}", "兼容性测试")

    def generate_performance_test_cases(self):
        """生成性能测试用例"""
        print("\n生成性能测试用例...")

        performance_scenarios = [
            ("性能", "验证页面加载性能",
             "1. 系统已部署",
             "1. 清除缓存\n2. 访问主要页面\n3. 记录加载时间",
             "页面加载时间在可接受范围内（<3秒）"),
            ("性能", "验证并发用户性能",
             "1. 准备性能测试环境",
             "1. 模拟并发用户\n2. 执行关键操作\n3. 监控系统性能",
             "系统支持预期并发数，无性能瓶颈"),
            ("性能", "验证大数据量性能",
             "1. 准备大数据量环境",
             "1. 加载大数据列表\n2. 执行查询操作\n3. 记录响应时间",
             "大数据量下响应时间可接受"),
        ]

        for module, title, preconditions, steps, expected in performance_scenarios:
            self.add_test_case(module, title, preconditions, steps, "低", f"1. {expected}", "性能测试")

    def generate_test_cases(self):
        """生成所有测试用例"""
        if not self.load_document():
            return False

        self.extract_content()

        # 提取功能特性
        features = self.extract_features_from_text()

        # 按不同方法生成测试用例
        self.generate_positive_test_cases(features)
        self.generate_boundary_test_cases(features)
        self.generate_exception_test_cases(features)
        self.generate_scene_test_cases(features)
        self.generate_ui_test_cases(features)
        self.generate_compatibility_test_cases()
        self.generate_performance_test_cases()

        print(f"\n总计生成测试用例: {len(self.test_cases)} 个")
        return True

    def save_to_markdown(self, output_path=None):
        """
        保存测试用例到Markdown文件

        Args:
            output_path: 输出文件路径，默认为文档同级目录

        Returns:
            str: 输出文件路径
        """
        if output_path is None:
            output_path = self.doc_path.parent / f"{self.doc_path.stem}_testcases.md"

        with open(output_path, 'w', encoding='utf-8') as f:
            # 写入标题
            f.write(f"# 测试用例\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"基于需求文档: {self.doc_path.name}\n\n")
            f.write(f"总用例数: {len(self.test_cases)}\n\n")
            f.write("---\n\n")

            # 按模块分组
            modules = {}
            for tc in self.test_cases:
                module = tc["module"]
                if module not in modules:
                    modules[module] = []
                modules[module].append(tc)

            # 写入各模块的测试用例
            for module, cases in modules.items():
                f.write(f"## {module}\n\n")

                for tc in cases:
                    f.write(f"### {tc['id']}: {tc['title']}\n\n")
                    f.write(f"**测试方法**: {tc.get('method', '')}\n\n")
                    f.write(f"**优先级**: {tc['priority']}\n\n")
                    f.write(f"**前置条件**:\n```\n{tc['preconditions']}\n```\n\n")
                    f.write(f"**测试步骤**:\n```\n{tc['steps']}\n```\n\n")
                    f.write(f"**预期结果**:\n```\n{tc['expected_result']}\n```\n\n")
                    f.write("---\n\n")

        print(f"测试用例已保存到Markdown: {output_path}")
        return str(output_path)

    def save_to_json(self, output_path=None):
        """
        保存测试用例到JSON文件

        Args:
            output_path: 输出文件路径，默认为文档同级目录

        Returns:
            str: 输出文件路径
        """
        if output_path is None:
            output_path = self.doc_path.parent / f"{self.doc_path.stem}_testcases.json"

        data = {
            "generated_at": datetime.now().isoformat(),
            "source_document": str(self.doc_path),
            "total_cases": len(self.test_cases),
            "test_cases": self.test_cases
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"测试用例已保存到JSON: {output_path}")
        return str(output_path)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="测试用例生成工具 - 根据需求文档自动生成测试用例",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_testcases.py demand/需求文档.docx
  python generate_testcases.py demand/需求文档.docx --output testcases.md
        """
    )

    parser.add_argument("doc_file", help="需求文档路径（Word格式）")
    parser.add_argument("--output", help="输出文件路径（可选）")

    args = parser.parse_args()

    # 创建生成器
    generator = TestCaseGenerator(args.doc_file)

    # 生成测试用例
    if generator.generate_test_cases():
        # 保存到Markdown
        md_path = generator.save_to_markdown(args.output)
        # 同时保存JSON
        json_path = generator.save_to_json()

        print(f"\n生成完成！")
        print(f"Markdown文件: {md_path}")
        print(f"JSON文件: {json_path}")
    else:
        print("\n生成失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
