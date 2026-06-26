#!/usr/bin/env python3
"""
研报搜索 Skill 验证脚本

用于验证 skill 目录结构和必要文件是否完整。

用法:
    python validate.py
    python validate.py /path/to/skill/dir
"""

import os
import py_compile
import sys
from pathlib import Path
from typing import List, Tuple


class SkillValidator:
    """Skill 目录验证器"""

    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def check_file_exists(self, file_path: Path, description: str, required: bool = True) -> bool:
        """检查文件是否存在"""
        if file_path.exists():
            print(f"  ✓ {description} 存在")
            return True
        else:
            msg = f"{description} 缺失: {file_path}"
            if required:
                self.errors.append(msg)
                print(f"  ✗ {msg}")
            else:
                self.warnings.append(msg)
                print(f"  ⚠ {msg}")
            return False

    def check_directory_exists(self, dir_path: Path, description: str, required: bool = True) -> bool:
        """检查目录是否存在"""
        if dir_path.is_dir():
            print(f"  ✓ {description} 存在")
            return True
        else:
            msg = f"{description} 缺失: {dir_path}"
            if required:
                self.errors.append(msg)
                print(f"  ✗ {msg}")
            else:
                self.warnings.append(msg)
                print(f"  ⚠ {msg}")
            return False

    def check_skill_md_format(self, skill_md: Path) -> None:
        """检查 SKILL.md 格式"""
        print("\n检查 SKILL.md 格式...")

        if not skill_md.exists():
            return

        content = skill_md.read_text(encoding="utf-8")

        # 检查必要字段
        required_fields = ["name:", "description:"]
        for field in required_fields:
            if any(line.startswith(field) for line in content.splitlines()):
                print(f"  ✓ 包含 {field} 字段")
            else:
                self.errors.append(f"SKILL.md 缺少 {field} 字段")
                print(f"  ✗ 缺少 {field} 字段")

        # 检查可选字段
        optional_fields = ["argument-hint:"]
        for field in optional_fields:
            if any(line.startswith(field) for line in content.splitlines()):
                print(f"  ✓ 包含 {field} 字段")
            else:
                self.warnings.append(f"SKILL.md 建议添加 {field} 字段")
                print(f"  ⚠ 建议添加 {field} 字段")

    def check_python_syntax(self, file_path: Path) -> None:
        """检查 Python 脚本语法"""
        if not file_path.exists():
            return
        try:
            py_compile.compile(str(file_path), doraise=True)
            print(f"  ✓ {file_path.name} 语法正确")
        except py_compile.PyCompileError as exc:
            self.errors.append(f"{file_path} 存在语法错误: {exc.msg}")
            print(f"  ✗ {file_path.name} 语法错误")

    def validate(self) -> bool:
        """执行完整验证"""
        print(f"\n=== 研报搜索 Skill 验证 ===")
        print(f"目录: {self.skill_dir}\n")

        # 检查必要文件
        print("检查必要文件...")
        self.check_file_exists(self.skill_dir / "SKILL.md", "SKILL.md")
        self.check_file_exists(self.skill_dir / "template.md", "template.md")

        # 检查 examples 目录
        examples_dir = self.skill_dir / "examples"
        if self.check_directory_exists(examples_dir, "examples/ 目录"):
            self.check_file_exists(examples_dir / "sample.md", "examples/sample.md")

        # 检查 scripts 目录
        scripts_dir = self.skill_dir / "scripts"
        if self.check_directory_exists(scripts_dir, "scripts/ 目录"):
            # 检查 Python 脚本
            self.check_file_exists(
                scripts_dir / "fxbaogao_client.py",
                "scripts/fxbaogao_client.py",
                required=True
            )
            self.check_file_exists(
                scripts_dir / "search_reports.py",
                "scripts/search_reports.py",
                required=True
            )
            self.check_file_exists(
                scripts_dir / "get_report_content.py",
                "scripts/get_report_content.py",
                required=True
            )
            self.check_file_exists(
                scripts_dir / "validate.sh",
                "scripts/validate.sh",
                required=False
            )
            self.check_file_exists(
                scripts_dir / "validate.py",
                "scripts/validate.py",
                required=False
            )

            print("\n检查 Python 脚本语法...")
            self.check_python_syntax(scripts_dir / "fxbaogao_client.py")
            self.check_python_syntax(scripts_dir / "search_reports.py")
            self.check_python_syntax(scripts_dir / "get_report_content.py")

        # 检查 SKILL.md 格式
        self.check_skill_md_format(self.skill_dir / "SKILL.md")

        # 输出结果
        print("\n" + "=" * 40)

        if self.errors:
            print(f"验证失败：发现 {len(self.errors)} 个错误")
            for error in self.errors:
                print(f"  ✗ {error}")
            return False

        if self.warnings:
            print(f"验证通过（有 {len(self.warnings)} 个警告）")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
            return True

        print("验证通过")
        return True


def main():
    # 确定验证目录
    if len(sys.argv) > 1:
        skill_dir = Path(sys.argv[1])
    else:
        # 默认为脚本所在目录的上级目录
        skill_dir = Path(__file__).parent.parent

    if not skill_dir.is_dir():
        print(f"错误: 目录不存在: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    validator = SkillValidator(skill_dir)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
