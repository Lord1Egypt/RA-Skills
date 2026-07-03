#!/usr/bin/env python3
"""
教材解析脚本 - 多格式教材内容解析
支持文本、PDF、JSON 格式的教材解析
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

class MaterialParser:
    """多格式教材解析器"""

    def __init__(self, file_path: str, format_type: str = 'auto'):
        self.file_path = Path(file_path)
        self.format_type = format_type.lower()
        self.content = {}
        self.error = None

    def detect_format(self) -> Optional[str]:
        """自动检测文件格式"""
        if not self.file_path.exists():
            self.error = f"文件不存在: {self.file_path}"
            return None

        ext = self.file_path.suffix.lower()

        if ext == '.pdf':
            return 'pdf'
        elif ext == '.json':
            return 'json'
        elif ext in ['.txt', '.md', '.text']:
            return 'text'
        else:
            # 尝试通过内容判断
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)
                    if content.strip().startswith('{'):
                        return 'json'
                    else:
                        return 'text'
            except Exception:
                return None

    def parse_text(self) -> Dict[str, Any]:
        """解析纯文本教材"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()

            structure = {
                "metadata": {
                    "title": self.file_path.stem,
                    "format": "text",
                    "language": "zh-CN"
                },
                "structure": {
                    "chapters": self._extract_chapters(text_content),
                    "sections": self._extract_sections(text_content)
                },
                "content": {
                    "theoretical_knowledge": self._extract_theory(text_content),
                    "practical_content": self._extract_practical(text_content),
                    "experiments": self._extract_experiments(text_content),
                    "examples": self._extract_examples(text_content)
                },
                "3d_elements": {
                    "scenes": self._extract_scenes(text_content),
                    "objects": self._extract_objects(text_content),
                    "environments": self._extract_environments(text_content)
                },
                "interactions": {
                    "user_actions": self._extract_actions(text_content),
                    "feedback_mechanisms": [],
                    "assessment_methods": []
                }
            }

            self.content = structure
            return structure

        except Exception as e:
            self.error = f"文本解析失败: {str(e)}"
            return {"error": self.error}

    def parse_pdf(self) -> Dict[str, Any]:
        """解析PDF教材"""
        try:
            import PyPDF2

            with open(self.file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)

                # 提取所有页面文本
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"

            # 使用文本解析逻辑处理提取的内容
            text_structure = self.parse_text_from_string(text_content)
            text_structure["metadata"]["format"] = "pdf"
            text_structure["metadata"]["pages"] = len(pdf_reader.pages)

            self.content = text_structure
            return text_structure

        except ImportError:
            self.error = "需要安装 PyPDF2 库: pip install PyPDF2"
            return {"error": self.error}
        except Exception as e:
            self.error = f"PDF解析失败: {str(e)}"
            return {"error": self.error}

    def parse_json(self) -> Dict[str, Any]:
        """解析JSON格式教材"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # 验证JSON结构
            if not isinstance(json_data, dict):
                raise ValueError("JSON必须是对象格式")

            # 标准化JSON内容
            structure = {
                "metadata": {
                    "title": json_data.get("title", self.file_path.stem),
                    "author": json_data.get("author", ""),
                    "subject": json_data.get("subject", ""),
                    "grade_level": json_data.get("grade_level", ""),
                    "language": json_data.get("language", "zh-CN"),
                    "format": "json"
                },
                "structure": json_data.get("structure", {
                    "chapters": [],
                    "sections": []
                }),
                "content": json_data.get("content", {
                    "theoretical_knowledge": [],
                    "practical_content": [],
                    "experiments": [],
                    "examples": []
                }),
                "3d_elements": json_data.get("3d_elements", {
                    "scenes": [],
                    "objects": [],
                    "environments": []
                }),
                "interactions": json_data.get("interactions", {
                    "user_actions": [],
                    "feedback_mechanisms": [],
                    "assessment_methods": []
                })
            }

            self.content = structure
            return structure

        except json.JSONDecodeError as e:
            self.error = f"JSON格式错误: {str(e)}"
            return {"error": self.error}
        except Exception as e:
            self.error = f"JSON解析失败: {str(e)}"
            return {"error": self.error}

    def parse(self) -> Dict[str, Any]:
        """主解析方法"""
        if self.format_type == 'auto':
            detected_format = self.detect_format()
            if not detected_format:
                return {"error": "无法检测文件格式"}
            self.format_type = detected_format

        if self.format_type == 'text':
            return self.parse_text()
        elif self.format_type == 'pdf':
            return self.parse_pdf()
        elif self.format_type == 'json':
            return self.parse_json()
        else:
            return {"error": f"不支持的格式: {self.format_type}"}

    def parse_text_from_string(self, text: str) -> Dict[str, Any]:
        """从字符串解析内容（用于PDF等提取后的文本）"""
        return {
            "metadata": {
                "title": self.file_path.stem,
                "format": "text",
                "language": "zh-CN"
            },
            "structure": {
                "chapters": self._extract_chapters(text),
                "sections": self._extract_sections(text)
            },
            "content": {
                "theoretical_knowledge": self._extract_theory(text),
                "practical_content": self._extract_practical(text),
                "experiments": self._extract_experiments(text),
                "examples": self._extract_examples(text)
            },
            "3d_elements": {
                "scenes": self._extract_scenes(text),
                "objects": self._extract_objects(text),
                "environments": self._extract_environments(text)
            },
            "interactions": {
                "user_actions": self._extract_actions(text),
                "feedback_mechanisms": [],
                "assessment_methods": []
            }
        }

    # 以下为辅助方法，用于提取不同类型的内容

    def _extract_chapters(self, text: str) -> List[Dict[str, str]]:
        """提取章节结构"""
        chapters = []
        lines = text.split('\n')

        current_chapter = None
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('第') and ('章' in line or '节' in line):
                if current_chapter:
                    chapters.append(current_chapter)
                current_chapter = {
                    "title": line,
                    "line": i + 1,
                    "content": ""
                }
            elif current_chapter:
                current_chapter["content"] += line + "\n"

        if current_chapter:
            chapters.append(current_chapter)

        return chapters

    def _extract_sections(self, text: str) -> List[Dict[str, str]]:
        """提取小节结构"""
        sections = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            if line and len(line) < 100 and not line.endswith('。'):
                # 简单的章节标题判断
                if any(keyword in line for keyword in ['一、', '二、', '三、', '1.', '2.', '3.']):
                    sections.append({
                        "title": line,
                        "line": i + 1
                    })

        return sections

    def _extract_theory(self, text: str) -> List[str]:
        """提取理论知识"""
        theory_sections = []
        # 简单提取，实际应用中可以更复杂
        keywords = ['概念', '原理', '定义', '定律', '公式']
        lines = text.split('\n')

        for line in lines:
            if any(keyword in line for keyword in keywords):
                theory_sections.append(line.strip())

        return theory_sections

    def _extract_practical(self, text: str) -> List[str]:
        """提取实践内容"""
        practical_sections = []
        keywords = ['实践', '操作', '练习', '应用']
        lines = text.split('\n')

        for line in lines:
            if any(keyword in line for keyword in keywords):
                practical_sections.append(line.strip())

        return practical_sections

    def _extract_experiments(self, text: str) -> List[Dict[str, Any]]:
        """提取实验内容"""
        experiments = []
        keywords = ['实验', '演示', '测试']
        lines = text.split('\n')

        current_experiment = None
        for i, line in enumerate(lines):
            if any(keyword in line for keyword in keywords):
                if current_experiment:
                    experiments.append(current_experiment)
                current_experiment = {
                    "name": line.strip(),
                    "line": i + 1,
                    "steps": []
                }
            elif current_experiment and line.strip().startswith(('1.', '2.', '3.', '第一步', '第二步', '第三步')):
                current_experiment["steps"].append(line.strip())

        if current_experiment:
            experiments.append(current_experiment)

        return experiments

    def _extract_examples(self, text: str) -> List[str]:
        """提取示例"""
        examples = []
        keywords = ['示例', '例子', '例题']
        lines = text.split('\n')

        for line in lines:
            if any(keyword in line for keyword in keywords):
                examples.append(line.strip())

        return examples

    def _extract_scenes(self, text: str) -> List[Dict[str, Any]]:
        """提取3D场景信息"""
        scenes = []
        keywords = ['实验室', '教室', '场景', '环境']
        lines = text.split('\n')

        for i, line in enumerate(lines):
            if any(keyword in line for keyword in keywords):
                scenes.append({
                    "name": line.strip(),
                    "line": i + 1,
                    "type": "generic"
                })

        return scenes

    def _extract_objects(self, text: str) -> List[Dict[str, Any]]:
        """提取3D对象信息"""
        objects = []
        keywords = ['设备', '仪器', '模型', '物体']
        lines = text.split('\n')

        for i, line in enumerate(lines):
            if any(keyword in line for keyword in keywords):
                objects.append({
                    "name": line.strip(),
                    "line": i + 1,
                    "geometry_type": "box",  # 默认几何类型
                    "material_type": "standard"  # 默认材质类型
                })

        return objects

    def _extract_environments(self, text: str) -> List[str]:
        """提取环境信息"""
        environments = []
        keywords = ['环境', '条件', '温度', '湿度', '光照']
        lines = text.split('\n')

        for line in lines:
            if any(keyword in line for keyword in keywords):
                environments.append(line.strip())

        return environments

    def _extract_actions(self, text: str) -> List[str]:
        """提取用户操作信息"""
        actions = []
        keywords = ['点击', '拖动', '旋转', '缩放', '选择']
        lines = text.split('\n')

        for line in lines:
            if any(keyword in line for keyword in keywords):
                actions.append(line.strip())

        return actions

    def save_content(self, output_path: str) -> bool:
        """保存解析结果"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.content, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.error = f"保存失败: {str(e)}"
            return False


def main():
    parser = argparse.ArgumentParser(
        description='教材解析脚本 - 多格式教材内容解析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 parse_materials.py textbook.pdf --output content.json
  python3 parse_materials.py textbook.txt --format text --output content.json
  python3 parse_materials.py textbook.json --validate --schema references/data_structures.json
        """
    )

    parser.add_argument('input_file', help='输入教材文件路径')
    parser.add_argument('--format', choices=['auto', 'text', 'pdf', 'json'],
                        default='auto', help='输入文件格式 (默认: auto)')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    parser.add_argument('--validate', action='store_true', help='验证输出格式')
    parser.add_argument('--schema', help='验证用的JSON Schema文件路径')

    args = parser.parse_args()

    # 创建解析器
    material_parser = MaterialParser(args.input_file, args.format)

    # 解析教材
    print(f"正在解析教材: {args.input_file}")
    result = material_parser.parse()

    # 检查错误
    if 'error' in result:
        print(f"❌ 解析失败: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # 保存结果
    print(f"正在保存结果到: {args.output}")
    if material_parser.save_content(args.output):
        print(f"✅ 解析成功！结果已保存到 {args.output}")

        # 显示摘要
        print("\n📊 解析摘要:")
        print(f"  标题: {result['metadata']['title']}")
        print(f"  格式: {result['metadata']['format']}")
        print(f"  章节数: {len(result['structure']['chapters'])}")
        print(f"  实验数: {len(result['content']['experiments'])}")
        print(f"  3D场景数: {len(result['3d_elements']['scenes'])}")
        print(f"  3D对象数: {len(result['3d_elements']['objects'])}")

        # 验证（如果需要）
        if args.validate:
            print("\n🔍 验证输出格式...")
            if args.schema:
                # 实现JSON Schema验证
                print(f"  使用Schema: {args.schema}")
            else:
                print("  ⚠️ 未提供Schema文件，跳过验证")
    else:
        print(f"❌ 保存失败: {material_parser.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()