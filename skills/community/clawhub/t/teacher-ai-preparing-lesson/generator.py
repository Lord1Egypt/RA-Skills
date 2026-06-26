#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教学文档生成器 - 完整版
支持生成课件(PPT)、教学设计(Word)、任务单(Word)
需要依赖 docx 和 pptx skills
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Windows 终端编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class TeachingMaterialsTool:
    """教学文档生成工具"""

    def __init__(self, workspace: Optional[str] = None):
        """初始化"""
        if workspace is None:
            workspace = os.getcwd()

        self.workspace = Path(workspace)
        self.teacher_dir = self.workspace / "MyTeacher"
        self.skills_dir = Path.home() / ".workbuddy" / "skills"

    def check_dependencies(self) -> Dict[str, bool]:
        """检查依赖的 skills 是否存在"""
        skills = {
            "docx": (self.skills_dir / "docx").exists(),
            "pptx": (self.skills_dir / "pptx").exists(),
            "dragon-ppt-maker": (self.skills_dir / "dragon-ppt-maker").exists(),
        }
        return skills

    def generate_ppt(self, info: Dict, content: List[Dict]) -> str:
        """
        生成 PPT 课件

        Args:
            info: 课程信息
            content: 幻灯片内容列表，每个元素是一页幻灯片的内容

        Returns:
            生成的 PPT 文件路径
        """
        # 使用 dragon-ppt-maker 生成 PPT
        ppt_maker = self.skills_dir / "dragon-ppt-maker" / "ppt_maker.py"

        if not ppt_maker.exists():
            raise FileNotFoundError("未找到 dragon-ppt-maker skill")

        # 构建输出路径
        folder_name = self._build_folder_name(info)
        output_dir = self.teacher_dir / folder_name
        output_file = output_dir / f"{info['lesson_name']}_课件.pptx"

        # 准备幻灯片数据
        slides_data = self._prepare_slides_data(info, content)

        # 将数据写入临时 JSON 文件
        temp_json = output_dir / "slides_data.json"
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(slides_data, f, ensure_ascii=False, indent=2)

        # 调用 dragon-ppt-maker
        cmd = [
            sys.executable,
            str(ppt_maker),
            "--input", str(temp_json),
            "--output", str(output_file),
            "--theme", "modern"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"PPT 生成失败: {result.stderr}")

        return str(output_file)

    def generate_word(self, info: Dict, doc_type: str, content: Dict) -> str:
        """
        生成 Word 文档

        Args:
            info: 课程信息
            doc_type: 文档类型 (teaching_design/task_sheet)
            content: 文档内容

        Returns:
            生成的 Word 文件路径
        """
        # 使用 docx skill 生成 Word 文档
        # 这里需要实现调用 docx skill 的逻辑
        # 当前版本创建一个 JSON 数据文件，供 AI 助手使用

        folder_name = self._build_folder_name(info)
        output_dir = self.teacher_dir / folder_name

        doc_name = f"{info['lesson_name']}_教学设计.docx" if doc_type == "teaching_design" \
                  else f"{info['lesson_name']}_任务单.docx"
        output_file = output_dir / doc_name

        # 准备文档数据
        doc_data = {
            "info": info,
            "type": doc_type,
            "content": content
        }

        # 写入 JSON 文件
        data_file = output_dir / f"{doc_type}_data.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(doc_data, f, ensure_ascii=False, indent=2)

        print(f"✓ 文档数据已准备: {data_file}")
        print(f"  请使用 AI 助手调用 docx skill 生成 Word 文件")

        return str(data_file)

    def _build_folder_name(self, info: Dict) -> str:
        """构建文件夹名称"""
        return f"{info['grade']}_{info['unit']}_{info['lesson_num']}_{info['lesson_name']}"

    def _prepare_slides_data(self, info: Dict, content: List[Dict]) -> List[Dict]:
        """准备幻灯片数据"""
        slides = []

        # 确定配色方案
        color_scheme = self._get_color_scheme(info.get("subject", "数学"))

        for slide in content:
            slide_data = {
                "title": slide.get("title", ""),
                "content": slide.get("content", ""),
                "image": slide.get("image", ""),
                "layout": slide.get("layout", "title_content"),
                "background": color_scheme["background"],
                "primary_color": color_scheme["primary"],
                "accent_color": color_scheme["accent"]
            }
            slides.append(slide_data)

        return slides

    def _get_color_scheme(self, subject: str) -> Dict:
        """获取配色方案"""
        colors = {
            "语文_古诗词": {
                "primary": "#8B0000",
                "secondary": "#F5F5DC",
                "accent": "#DAA520",
                "background": "#FAF8EF"
            },
            "语文_现代文": {
                "primary": "#2E86AB",
                "secondary": "#A23B72",
                "accent": "#F18F01",
                "background": "#FFFFFF"
            },
            "数学": {
                "primary": "#0D9488",
                "secondary": "#065F46",
                "accent": "#F97316",
                "background": "#FAFAF9"
            },
            "英语": {
                "primary": "#6366F1",
                "secondary": "#8B5CF6",
                "accent": "#EC4899",
                "background": "#F8F9FA"
            }
        }

        if subject.startswith("语文") and "古诗" in subject:
            return colors["语文_古诗词"]
        elif subject.startswith("语文"):
            return colors["语文_现代文"]
        else:
            return colors["数学"]

    def create_course_structure(self, info: Dict) -> str:
        """创建课程文件夹结构"""
        folder_name = self._build_folder_name(info)
        course_dir = self.teacher_dir / folder_name

        # 创建文件夹
        course_dir.mkdir(parents=True, exist_ok=True)

        # 创建子文件夹
        (course_dir / "参考资源").mkdir(exist_ok=True)
        (course_dir / "参考资源" / "images").mkdir(exist_ok=True)

        return str(course_dir)


def print_dependencies_status(dependencies: Dict[str, bool]):
    """打印依赖状态"""
    print("\n依赖检查:")
    print("-" * 40)
    for skill, exists in dependencies.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {skill}")

    missing = [k for k, v in dependencies.items() if not v]
    if missing:
        print(f"\n⚠️  缺少以下 skills: {', '.join(missing)}")
        print("   某些功能可能无法正常使用")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="教学文档生成工具 - 完整版")
    parser.add_argument("--check", action="store_true", help="检查依赖")
    parser.add_argument("--workspace", help="工作空间路径")

    args = parser.parse_args()

    tool = TeachingMaterialsTool(workspace=args.workspace)

    if args.check:
        deps = tool.check_dependencies()
        print_dependencies_status(deps)
    else:
        print("请指定操作: --check")
