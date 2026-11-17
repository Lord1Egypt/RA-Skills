#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrator.py — 技能数据目录迁移助手 v1.1.0

扫描旧数据目录，迁移到新数据目录（skills/.standardization/<skill>/），
并自动更新代码中的路径引用。
"""

import os
import json
import re
import shutil
from pathlib import Path


class SkillMigrator:
    """技能数据迁移器"""

    def __init__(self, console=None):
        self.console = console

    def migrate(self, args):
        """执行数据目录迁移"""
        skill_dir = Path(args.skill_dir).resolve()
        dry_run = getattr(args, "dry_run", False)
        force = getattr(args, "force", False)

        if not skill_dir.exists():
            print(f"❌ 技能目录不存在: {skill_dir}")
            return False

        skill_name = skill_dir.name

        # 1. 检测当前数据目录
        current_data_dir = self._detect_current_data_dir(skill_dir)
        if not current_data_dir:
            print(f"ℹ️  未找到需要迁移的数据目录")
            return True

        # 2. 计算目标数据目录
        target_data_dir = self._compute_target_data_dir(skill_dir)
        target_data_dir.mkdir(parents=True, exist_ok=True)

        print(f"  源数据目录: {current_data_dir}")
        print(f"  目标数据目录: {target_data_dir}")

        if dry_run:
            # dry-run 模式：只显示计划
            self._dry_run(current_data_dir, target_data_dir, skill_dir)
            return True

        # 3. 执行迁移
        try:
            self._execute_migration(current_data_dir, target_data_dir, skill_dir, force)
            print(f"✅ 数据迁移完成！")
            return True
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            return False

    def _detect_current_data_dir(self, skill_dir):
        """自动检测当前数据目录（三种方法）"""
        import re

        # 方法1: 从脚本中的 get_*_home() 函数检测
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            for py_file in sorted(scripts_dir.glob("*.py")):
                content = py_file.read_text(encoding="utf-8", errors="replace")
                lines = content.split("\n")
                in_get_home = False
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    # 检测进入 get_*_home 函数
                    if re.match(r'\s*def get_\w+_home\(', stripped):
                        in_get_home = True
                    # 在 get_*_home 函数内，提取 default = Path.home() / ... 路径
                    if in_get_home and re.match(r'\s*default\s*=\s*Path\.home\(', stripped):
                        # 提取所有字符串字面量
                        string_literals = re.findall(r'["\']([^"\']*)["\']', stripped)
                        if string_literals:
                            detected_path = Path.home()
                            for part in string_literals:
                                if part:  # 跳过空字符串
                                    detected_path = detected_path / part
                            if detected_path.exists():
                                print(f"    ✓ 从 {py_file.name} 检测到数据目录: {detected_path}")
                                return detected_path
                    # 退出函数检测：遇到 return 或下一个 def
                    if in_get_home and stripped.startswith("return "):
                        in_get_home = False
                    if in_get_home and re.match(r'\s*def ', stripped) and not stripped.startswith("def get_"):
                        in_get_home = False

        # 方法2: 从 _meta.json 检测
        meta_file = skill_dir / "_meta.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                data_dir = meta.get("data_dir")
                if data_dir:
                    # 相对于 skills 目录解析
                    skills_dir = self._find_skills_dir(skill_dir)
                    candidate = Path(os.path.join(skills_dir, data_dir))
                    if candidate.exists():
                        print(f"    ✓ 从 _meta.json 检测到数据目录: {candidate}")
                        return candidate
            except Exception:
                pass

        # 方法3: 常见默认路径
        common_paths = [
            Path.home() / ".workbuddy" / skill_dir.name,
            skill_dir / "data",
        ]
        for p in common_paths:
            if p.exists():
                print(f"    ✓ 从常见路径检测到数据目录: {p}")
                return p

        return None

    def _compute_target_data_dir(self, skill_dir):
        """计算目标数据目录"""
        skills_dir = self._find_skills_dir(skill_dir)
        skill_name = skill_dir.name
        return skills_dir / ".standardization" / skill_name

    def _find_skills_dir(self, skill_dir):
        """向上查找 skills 目录"""
        p = skill_dir.resolve()
        for _ in range(5):
            if p.name == "skills" and p.is_dir():
                return p
            parent = p.parent
            if parent == p:
                break
            p = parent
        # 如果找不到，使用父目录
        return skill_dir.parent

    def _dry_run(self, src, dst, skill_dir):
        """显示迁移计划"""
        print(f"\n=== MIGRATE-DATA DRY-RUN ===")
        print(f"将要执行的操作：")
        print(f"  1. 迁移数据: {src} → {dst}")
        print(f"  2. 更新脚本路径引用")
        print(f"  3. 更新 _meta.json data_dir 字段")

        # 显示将要迁移的文件
        if src.exists():
            files = list(src.rglob("*"))
            files = [f for f in files if f.is_file()]
            print(f"\n将要迁移 {len(files)} 个文件：")
            for f in files[:10]:
                rel = f.relative_to(src)
                print(f"    {rel}")
            if len(files) > 10:
                print(f"    ... 和其他 {len(files) - 10} 个文件")

    def _execute_migration(self, src, dst, skill_dir, force):
        """执行实际迁移"""
        # 1. 迁移数据文件
        if src.exists() and src != dst:
            if dst.exists() and not force:
                print(f"⚠️  目标目录已存在，使用 --force 覆盖")
                return
            print(f"  📦 迁移数据文件...")
            shutil.copytree(str(src), str(dst), dirs_exist_ok=True)
            print(f"    ✅ 已迁移: {src} → {dst}")

        # 2. 更新脚本路径引用（支持 Path() 拼接和字符串字面量）
        self._update_path_references(skill_dir, src, dst)

        # 3. 更新 _meta.json
        self._update_meta_json(skill_dir, dst)

    def _update_path_references(self, skill_dir, old_path, new_path):
        """更新脚本中的路径引用（支持 Path() 拼接和字符串字面量）"""
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists():
            return

        # 情况A：旧路径是字符串字面量（简单替换）
        old_str = str(old_path)
        new_str = str(new_path)

        # 情况B：旧路径是 Path.home() / "a" / "b" 拼接形式
        # 此时需要重写整行（而不仅是字符串替换）
        old_path_parts = None
        if "Path.home()" in old_str or old_str == str(old_path):
            # 尝试解析旧路径的组件
            old_path_parts = self._parse_path_parts(old_str)

        print(f"  🔍 更新路径引用...")
        updated = 0
        for py_file in sorted(scripts_dir.glob("*.py")):
            content = py_file.read_text(encoding="utf-8", errors="replace")
            original_content = content

            # 策略1：简单字符串替换（适用于字符串字面量）
            if old_str in content:
                content = content.replace(old_str, new_str)
                if content != original_content:
                    py_file.write_text(content, encoding="utf-8")
                    print(f"    ✅ 字符串替换: {py_file.name}")
                    updated += 1
                    continue

            # 策略2：Path() 拼接重写（适用于 get_*_home() 函数）
            if old_path_parts:
                lines = content.split("\n")
                new_lines = []
                in_get_home = False
                modified = False

                for i, line in enumerate(lines):
                    # 检测进入 get_*_home 函数
                    if re.match(r'\s*def get_\w+_home\(', line):
                        in_get_home = True
                        new_lines.append(line)
                        continue

                    # 在 get_*_home 函数内，重写 default = 行
                    if in_get_home and re.match(r'\s*default\s*=\s*Path\.home\(', line):
                        # 重写为标准路径
                        skill_name = skill_dir.name
                        indent = line[:len(line) - len(line.lstrip())]
                        new_line = indent + "default = Path.home() / \".workbuddy\" / \"skills\" / \".standardization\" / \"" + skill_name + "\""
                        new_lines.append(new_line)
                        modified = True
                        updated += 1
                        print(f"    ✅ Path() 拼接重写: {py_file.name}")
                        continue

                    # 退出函数检测
                    if in_get_home and line.strip().startswith("return "):
                        in_get_home = False

                    new_lines.append(line)

                if modified:
                    py_file.write_text("\n".join(new_lines), encoding="utf-8")

        if updated == 0:
            print(f"    ℹ️  未找到需要更新的引用")
        else:
            print(f"    ✅ 共更新 {updated} 个文件")

    def _parse_path_parts(self, path_str):
        """解析路径字符串，提取组件列表（用于 Path() 拼接）"""
        # 尝试匹配 Path.home() / "a" / "b" 模式
        parts = re.findall(r'["\']([^"\']*)["\']', path_str)
        # 过滤空字符串
        parts = [p for p in parts if p]
        return parts if parts else None

    def _update_meta_json(self, skill_dir, new_data_dir):
        """更新 _meta.json 中的 data_dir 字段"""
        meta_file = skill_dir / "_meta.json"
        if not meta_file.exists():
            return

        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            return

        # 计算相对于 skills 目录的路径
        skills_dir = self._find_skills_dir(skill_dir)
        try:
            rel_path = new_data_dir.relative_to(skills_dir)
        except ValueError:
            rel_path = str(new_data_dir)

        meta["data_dir"] = str(rel_path)
        meta_file.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print(f"  ✅ 更新 _meta.json: data_dir = {rel_path}")

    def _scan_hardcoded_paths(self, skill_dir):
        """扫描脚本中的硬编码路径（用于审计）"""
        issues = []
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists():
            return issues

        for py_file in sorted(scripts_dir.glob("*.py")):
            content = py_file.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")
            for i, line in enumerate(lines):
                # 检测 Path.home() 拼接路径
                if "Path.home()" in line and ".workbuddy" in line:
                    issues.append({
                        "file": str(py_file.relative_to(skill_dir)),
                        "line": i + 1,
                        "content": line.strip(),
                    })

        return issues
