#!/usr/bin/env python3
"""
Python 项目迁移脚本
安全地重构项目结构，支持备份、预览、回滚
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

class ProjectMigrator:
    def __init__(self, project_path: str, dry_run: bool = False):
        self.project = Path(project_path)
        self.dry_run = dry_run
        self.backup_path = None
        self.changes = []
        self.errors = []
    
    def create_backup(self) -> Path:
        """创建项目备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.project.name}.backup.{timestamp}"
        self.backup_path = self.project.parent / backup_name
        
        if self.dry_run:
            print(f"[DRY RUN] 会创建备份：{self.backup_path}")
            return self.backup_path
        
        print(f"📦 创建备份：{self.backup_path}")
        shutil.copytree(self.project, self.backup_path)
        return self.backup_path
    
    def analyze_and_plan(self) -> dict:
        """分析项目并生成迁移计划"""
        plan = {
            "source": str(self.project.absolute()),
            "timestamp": datetime.now().isoformat(),
            "actions": [],
            "warnings": []
        }
        
        # 检查是否需要 src 布局
        src_dir = self.project / "src"
        main_py_files = list(self.project.glob("*.py"))
        
        if main_py_files and not src_dir.exists():
            plan["actions"].append({
                "type": "create_dir",
                "path": str(src_dir),
                "reason": "创建 src/ 目录以符合现代 Python 项目结构"
            })
            
            for py_file in main_py_files:
                if py_file.name not in ["setup.py", "conftest.py"]:
                    target = src_dir / py_file.name
                    plan["actions"].append({
                        "type": "move",
                        "source": str(py_file),
                        "target": str(target),
                        "reason": "移动源代码到 src/"
                    })
        
        # 检查是否需要创建包目录
        init_files = list(self.project.glob("__init__.py"))
        if not init_files and main_py_files:
            package_name = self.project.name.replace("-", "_")
            package_dir = self.project / package_name
            
            if not self.dry_run:
                plan["actions"].append({
                    "type": "create_dir",
                    "path": str(package_dir),
                    "reason": f"创建包目录：{package_name}"
                })
        
        # 检查缺失的配置文件
        config_files = {
            "pyproject.toml": "现代 Python 项目配置",
            ".gitignore": "Git 忽略规则",
            ".pre-commit-config.yaml": "Pre-commit 钩子配置"
        }
        
        for cfg_file, reason in config_files.items():
            if not (self.project / cfg_file).exists():
                plan["actions"].append({
                    "type": "create",
                    "path": str(self.project / cfg_file),
                    "reason": reason
                })
        
        # 检查测试目录
        tests_dir = self.project / "tests"
        if not tests_dir.exists():
            plan["actions"].append({
                "type": "create_dir",
                "path": str(tests_dir),
                "reason": "创建测试目录"
            })
            plan["actions"].append({
                "type": "create",
                "path": str(tests_dir / "__init__.py"),
                "reason": "测试包初始化文件"
            })
            plan["actions"].append({
                "type": "create",
                "path": str(tests_dir / "conftest.py"),
                "reason": "Pytest 配置"
            })
        
        return plan
    
    def execute_plan(self, plan: dict) -> bool:
        """执行迁移计划"""
        print(f"\n🚀 开始执行迁移计划，共 {len(plan['actions'])} 个操作\n")
        
        for i, action in enumerate(plan["actions"], 1):
            action_type = action["type"]
            
            try:
                if action_type == "create_dir":
                    self._create_dir(action["path"])
                
                elif action_type == "move":
                    self._move_file(action["source"], action["target"])
                
                elif action_type == "create":
                    self._create_file(action["path"], action.get("reason", ""))
                
                print(f"  [{i}/{len(plan['actions'])}] ✅ {action['reason']}")
                
            except Exception as e:
                error_msg = f"操作失败：{action['reason']} - {str(e)}"
                self.errors.append(error_msg)
                print(f"  [{i}/{len(plan['actions'])}] ❌ {error_msg}")
                
                # 发生错误时回滚
                if self.backup_path:
                    print(f"\n⚠️  发生错误，开始回滚...")
                    self._rollback()
                    return False
        
        return len(self.errors) == 0
    
    def _create_dir(self, path: str):
        """创建目录"""
        p = Path(path)
        if self.dry_run:
            return
        p.mkdir(parents=True, exist_ok=True)
    
    def _move_file(self, source: str, target: str):
        """移动文件"""
        src = Path(source)
        tgt = Path(target)
        
        if self.dry_run:
            if tgt.exists():
                print(f"  ⚠️  目标已存在：{tgt}")
            return
        
        # 检查目标是否已存在（避免覆盖）
        if tgt.exists():
            raise FileExistsError(f"目标文件已存在：{tgt}")
        
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(tgt))
    
    def _create_file(self, path: str, reason: str):
        """创建文件"""
        p = Path(path)
        
        if self.dry_run:
            return
        
        if p.exists():
            return  # 已存在，跳过
        
        p.parent.mkdir(parents=True, exist_ok=True)
        
        # 根据文件类型生成内容
        content = self._generate_file_content(p, reason)
        p.write_text(content, encoding="utf-8")
    
    def _generate_file_content(self, path: Path, reason: str) -> str:
        """生成文件内容模板"""
        name = path.name
        
        if name == "__init__.py":
            return f'"""{path.parent.name} package"""\n'
        
        elif name == "conftest.py":
            return '"""Pytest configuration"""\n\nimport pytest\n'
        
        elif name == ".gitignore":
            return '''__pycache__/
*.py[cod]
.env
venv/
.pytest_cache/
.coverage
'''
        
        elif name == "pyproject.toml":
            return f'''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{path.parent.name}"
version = "0.1.0"
dependencies = []
'''
        
        elif name == ".pre-commit-config.yaml":
            return '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
'''
        
        return f'# {reason}\n'
    
    def _rollback(self):
        """回滚到备份"""
        if not self.backup_path or not self.backup_path.exists():
            print("⚠️  没有可用的备份，无法回滚")
            return
        
        print(f"🔄 从备份恢复：{self.backup_path}")
        
        # 删除当前项目
        if not self.dry_run and self.project.exists():
            shutil.rmtree(self.project)
        
        # 恢复备份
        if not self.dry_run:
            shutil.move(str(self.backup_path), str(self.project))
            print("✅ 回滚完成")


def print_plan(plan: dict):
    """打印迁移计划"""
    print("\n📋 迁移计划预览\n")
    print(f"项目：{plan['source']}")
    print(f"时间：{plan['timestamp']}\n")
    
    if not plan["actions"]:
        print("✅ 无需迁移，项目结构已经符合最佳实践\n")
        return
    
    print(f"将要执行 {len(plan['actions'])} 个操作:\n")
    
    for i, action in enumerate(plan["actions"], 1):
        action_type = action["type"]
        icon = {"create_dir": "📁", "move": "🔄", "create": "📄"}.get(action_type, "•")
        print(f"  {i}. {icon} [{action_type}] {action['reason']}")
        if "source" in action:
            print(f"      {action['source']}")
            print(f"      → {action['target']}")
        else:
            print(f"      {action['path']}")
    
    print()


def main():
    if len(sys.argv) < 2:
        print("用法：python migrate_project.py <项目路径> [--dry-run] [--plan <输出文件>]")
        print("\n选项:")
        print("  --dry-run     预览模式，不实际修改文件")
        print("  --plan FILE   将计划保存为 JSON 文件")
        print("\n⚠️  警告：此脚本会修改项目结构，建议先备份！")
        sys.exit(1)
    
    project_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    plan_output = None
    
    for i, arg in enumerate(sys.argv):
        if arg == "--plan" and i + 1 < len(sys.argv):
            plan_output = sys.argv[i + 1]
    
    migrator = ProjectMigrator(project_path, dry_run)
    
    # 分析并生成计划
    plan = migrator.analyze_and_plan()
    
    # 打印计划
    print_plan(plan)
    
    # 保存计划（可选）
    if plan_output:
        Path(plan_output).write_text(json.dumps(plan, indent=2, ensure_ascii=False))
        print(f"📄 计划已保存到：{plan_output}\n")
    
    # 预览模式退出
    if dry_run:
        print("✅ 预览模式完成，未执行任何修改")
        print("\n确认执行迁移请运行（不带 --dry-run）:")
        print(f"  python migrate_project.py {project_path}")
        return
    
    # 询问确认
    if not plan["actions"]:
        return
    
    print("⚠️  此操作将修改项目文件，建议先备份！")
    confirm = input("确认执行？输入 'yes' / '确认' / 'y' 继续：").strip().lower()
    
    # 支持中英文确认
    if confirm not in ["yes", "y", "确认", "是"]:
        print("❌ 已取消")
        return
    
    # 创建备份
    migrator.create_backup()
    
    # 执行迁移
    success = migrator.execute_plan(plan)
    
    if success:
        print("\n🎉 迁移完成！")
    else:
        print("\n❌ 迁移失败，已回滚到备份")
        sys.exit(1)


if __name__ == "__main__":
    main()
