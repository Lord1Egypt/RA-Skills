#!/usr/bin/env python3
"""
输出验证器 — 自动验证 skill 输出质量，真正读取项目文件做验证

用法:
  python output_validator.py validate <skill> [project_path]
  python output_validator.py validate-all [project_path]
  python output_validator.py auto-fix <skill> [project_path]
  python output_validator.py load-design <DESIGN.md>
  python output_validator.py report
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 尝试导入 PyYAML
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class OutputValidator:
    """自动验证 skill 输出质量"""

    # 多语言章节名映射（中英文对照）
    SECTION_ALIASES = {
        "overview": ["overview", "概述", "概览", "简介"],
        "implementation": ["implementation", "实现", "实现方案", "实施方案"],
        "testing": ["testing", "测试", "测试策略", "测试方案"],
        "deployment": ["deployment", "部署", "部署方案"],
        "architecture": ["architecture", "架构", "系统架构"],
        "requirements": ["requirements", "需求", "功能需求"],
        "design": ["design", "设计", "详细设计"],
        "api": ["api", "接口", "api接口", "api文档"],
        "security": ["security", "安全", "安全设计"],
        "performance": ["performance", "性能", "性能优化"],
    }

    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.orchestration_dir = self.project_path / ".orchestration"
        self.design_path = None
        self.validation_rules = {}
        self.results = {}

    def load_from_design(self, design_path):
        """从 DESIGN.md 加载验证规则"""
        self.design_path = Path(design_path).resolve()
        if not self.design_path.exists():
            print(f"错误: DESIGN.md 不存在: {design_path}", file=sys.stderr)
            return False

        content = self.design_path.read_text(encoding="utf-8")

        # 提取质量验证章节
        val_match = re.search(
            r'##\s+(?:质量验证|[Vv]alidation)\s*\n(.*?)(?=\n##|\Z)',
            content, re.DOTALL
        )
        if not val_match:
            print("DESIGN.md 中未找到质量验证配置")
            return False

        val_text = val_match.group(1).strip()
        # 去掉可能的 ```yaml 代码块包裹
        val_text = re.sub(r'```ya?ml\s*\n?', '', val_text)
        val_text = re.sub(r'\n?```', '', val_text)

        if HAS_YAML:
            try:
                data = yaml.safe_load(val_text)
                if isinstance(data, dict):
                    # 可能包在 validation 键下
                    if "validation" in data:
                        self.validation_rules = data["validation"]
                    else:
                        self.validation_rules = data
                    print(f"从 DESIGN.md 加载了 {len(self.validation_rules)} 个验证规则")
                    return True
            except yaml.YAMLError:
                pass

        # 简单解析
        self.validation_rules = self._simple_yaml_parse(val_text)
        print(f"从 DESIGN.md 加载了 {len(self.validation_rules)} 个验证规则(简单解析)")
        return True

    def add_rule(self, skill_name, rules):
        """手动添加验证规则"""
        self.validation_rules[skill_name] = rules

    def validate(self, skill_name):
        """验证单个 skill 的输出"""
        rules = self.validation_rules.get(skill_name, {})
        if not rules:
            return {"valid": True, "errors": [], "warnings": [], "fixable": False}

        errors = []
        warnings = []
        fixable = False

        # 获取 skill 的输出内容
        output = self._get_output_for_skill(skill_name)

        # 1. 必需章节检查
        required_sections = rules.get("required_sections", [])
        if required_sections and output:
            for section in required_sections:
                if not self._has_section(output, section):
                    errors.append(f"缺少必需章节: {section}")
                    fixable = True

        # 2. 格式验证
        fmt = rules.get("format", "")
        if fmt and output:
            if fmt == "markdown" and not self._is_valid_markdown(output):
                warnings.append("输出可能不是有效的 Markdown 格式")
            elif fmt == "json":
                try:
                    json.loads(output)
                except (json.JSONDecodeError, TypeError):
                    errors.append("输出不是有效的 JSON 格式")
            elif fmt == "yaml" and HAS_YAML:
                try:
                    yaml.safe_load(output)
                except Exception:
                    errors.append("输出不是有效的 YAML 格式")

        # 3. 长度验证
        max_length = rules.get("max_length", 0)
        min_length = rules.get("min_length", 0)
        if output:
            output_len = len(output)
            if max_length and output_len > max_length:
                errors.append(f"输出长度 {output_len} 超过最大限制 {max_length}")
            if min_length and output_len < min_length:
                warnings.append(f"输出长度 {output_len} 低于最小建议 {min_length}")

        # 4. 文件存在性检查
        expected_outputs = rules.get("expected_outputs", [])
        if expected_outputs:
            for output_path in expected_outputs:
                full_path = self.project_path / output_path.rstrip("/")
                if output_path.endswith("/"):
                    # 目录
                    if not full_path.is_dir():
                        errors.append(f"期望的输出目录不存在: {output_path}")
                        fixable = True
                else:
                    # 文件
                    if not full_path.exists():
                        errors.append(f"期望的输出文件不存在: {output_path}")
                        fixable = True

        # 5. 测试覆盖率估算
        test_coverage = rules.get("test_coverage", 0)
        if test_coverage:
            estimated = self._estimate_test_coverage()
            if estimated < test_coverage:
                warnings.append(
                    f"测试覆盖率估算 ~{estimated}%，低于期望 {test_coverage}%"
                )

        # 6. 安全检查
        check_severity = rules.get("check_severity", "")
        if check_severity and output:
            security_issues = self._check_security(output, check_severity)
            for issue in security_issues:
                errors.append(f"安全问题: {issue}")

        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "fixable": fixable,
        }
        self.results[skill_name] = result
        return result

    def validate_all(self):
        """验证所有已注册规则的 skill"""
        all_results = {}
        for skill_name in self.validation_rules:
            all_results[skill_name] = self.validate(skill_name)
        return all_results

    def auto_fix(self, skill_name):
        """自动修复可修复的问题"""
        rules = self.validation_rules.get(skill_name, {})
        if not rules:
            print(f"没有 {skill_name} 的验证规则")
            return False

        fixed = []

        # 修复缺失章节
        required_sections = rules.get("required_sections", [])
        output = self._get_output_for_skill(skill_name)

        if required_sections and output:
            for section in required_sections:
                if not self._has_section(output, section):
                    # 在文件末尾添加占位符章节
                    placeholder = self._create_section_placeholder(section)
                    self._append_to_output(skill_name, placeholder)
                    fixed.append(f"添加缺失章节: {section}")

        # 修复缺失文件/目录
        expected_outputs = rules.get("expected_outputs", [])
        for output_path in expected_outputs:
            full_path = self.project_path / output_path.rstrip("/")
            if output_path.endswith("/"):
                if not full_path.is_dir():
                    full_path.mkdir(parents=True, exist_ok=True)
                    # 创建 .gitkeep
                    (full_path / ".gitkeep").touch()
                    fixed.append(f"创建缺失目录: {output_path}")
            else:
                if not full_path.exists():
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(f"# {skill_name} 输出\n\n待填写...\n", encoding="utf-8")
                    fixed.append(f"创建缺失文件: {output_path}")

        if fixed:
            print(f"自动修复了 {len(fixed)} 个问题:")
            for f in fixed:
                print(f"  - {f}")
            return True
        else:
            print("没有可自动修复的问题")
            return False

    def get_report(self):
        """生成验证报告"""
        if not self.results:
            return "暂无验证结果，请先运行 validate 或 validate-all"

        lines = []
        lines.append("=" * 50)
        lines.append(" Skill 输出验证报告")
        lines.append("=" * 50)
        lines.append(f" 项目: {self.project_path.name}")
        lines.append(f" 时间: {datetime.now().isoformat()}")
        lines.append("-" * 50)

        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r["valid"])
        failed = total - passed

        lines.append(f" 总计: {total} 个 skill，{passed} 通过，{failed} 未通过")
        lines.append("")

        for skill_name, result in self.results.items():
            mark = "PASS" if result["valid"] else "FAIL"
            lines.append(f" [{mark}] {skill_name}")

            for err in result.get("errors", []):
                lines.append(f"   ERROR: {err}")
            for warn in result.get("warnings", []):
                lines.append(f"   WARN:  {warn}")

            if result.get("fixable"):
                lines.append(f"   (可自动修复)")

        lines.append("")
        lines.append("=" * 50)
        return "\n".join(lines)

    # ============================================================
    # 内部方法
    # ============================================================

    def _get_output_for_skill(self, skill_name):
        """真正读取项目文件获取 skill 的输出内容"""
        rules = self.validation_rules.get(skill_name, {})
        expected = rules.get("expected_outputs", [])

        # 收集所有输出文件的内容
        contents = []
        for output_path in expected:
            full_path = self.project_path / output_path.rstrip("/")
            if output_path.endswith("/"):
                # 目录：读取其中所有 .md 和 .py 文件
                if full_path.is_dir():
                    for f in sorted(full_path.rglob("*")):
                        if f.is_file() and f.suffix in (".md", ".py", ".txt", ".json"):
                            try:
                                content = f.read_text(encoding="utf-8")
                                contents.append(f"--- {f.relative_to(self.project_path)} ---\n{content}")
                            except (OSError, UnicodeDecodeError):
                                pass
            else:
                # 单个文件
                if full_path.exists() and full_path.is_file():
                    try:
                        content = full_path.read_text(encoding="utf-8")
                        contents.append(content)
                    except (OSError, UnicodeDecodeError):
                        pass

        # 如果没有从 expected_outputs 读到内容，尝试从 context 获取输出文件信息
        if not contents:
            context_file = self.orchestration_dir / "context.json"
            if context_file.exists():
                try:
                    ctx = json.loads(context_file.read_text(encoding="utf-8"))
                    ctx_data = ctx.get("data", {})
                    # 查找 skill 对应的输出
                    for key, value in ctx_data.items():
                        if skill_name in key and isinstance(value, str):
                            contents.append(value)
                except (json.JSONDecodeError, OSError):
                    pass

        return "\n\n".join(contents) if contents else ""

    def _has_section(self, content, section_name):
        """检查内容中是否包含指定章节（支持中英文别名）"""
        # 获取所有可能的章节名
        names = [section_name]
        for key, aliases in self.SECTION_ALIASES.items():
            if section_name.lower() in aliases or section_name.lower() == key:
                names = aliases
                break

        # 检查 markdown 标题
        for name in names:
            pattern = re.compile(
                rf'^#+\s*{re.escape(name)}',
                re.IGNORECASE | re.MULTILINE
            )
            if pattern.search(content):
                return True

        return False

    def _is_valid_markdown(self, content):
        """简单检查是否是有效 Markdown"""
        # 至少包含一个标题或列表标记
        return bool(re.search(r'^#+\s|\n#+\s|^\s*[-*]\s', content, re.MULTILINE))

    def _estimate_test_coverage(self):
        """基于 tests/ 和 src/ 文件比例估算测试覆盖率"""
        tests_dir = self.project_path / "tests"
        src_dir = self.project_path / "src"

        if not tests_dir.exists() or not src_dir.exists():
            return 0

        test_files = list(tests_dir.rglob("*.py"))
        src_files = list(src_dir.rglob("*.py"))

        if not src_files:
            return 100

        # 粗略估算：有测试文件的模块比例
        tested_modules = set()
        for tf in test_files:
            # test_foo.py -> foo.py
            module_name = tf.name.replace("test_", "").replace(".py", "")
            tested_modules.add(module_name)

        total_modules = set()
        for sf in src_files:
            total_modules.add(sf.stem)

        if not total_modules:
            return 0

        covered = len(tested_modules & total_modules)
        return min(100, int((covered / len(total_modules)) * 100))

    def _check_security(self, content, severity):
        """简单的安全检查"""
        issues = []

        # 检查硬编码密码
        if re.search(r'(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{4,}', content, re.IGNORECASE):
            issues.append("可能包含硬编码密码")

        # 检查硬编码密钥
        if re.search(r'(api_key|secret_key|access_key)\s*[:=]\s*["\'][^"\']{8,}', content, re.IGNORECASE):
            issues.append("可能包含硬编码 API 密钥")

        # 检查 SQL 注入风险
        if re.search(r'(SELECT|INSERT|UPDATE|DELETE).*\+\s*(request|params|input)', content, re.IGNORECASE):
            issues.append("可能存在 SQL 注入风险")

        return issues

    def _create_section_placeholder(self, section_name):
        """为缺失章节创建占位符"""
        return f"\n\n## {section_name.title()}\n\n> TODO: 此章节待填写\n"

    def _append_to_output(self, skill_name, content):
        """向 skill 的主要输出文件追加内容"""
        rules = self.validation_rules.get(skill_name, {})
        expected = rules.get("expected_outputs", [])

        for output_path in expected:
            if not output_path.endswith("/"):
                full_path = self.project_path / output_path
                if full_path.exists() and full_path.suffix == ".md":
                    with open(full_path, "a", encoding="utf-8") as f:
                        f.write(content)
                    return

        # 如果没找到特定文件，尝试 IMPLEMENTATION.md 或 requirements.md
        for candidate in ["IMPLEMENTATION.md", "requirements.md"]:
            full_path = self.project_path / candidate
            if full_path.exists():
                with open(full_path, "a", encoding="utf-8") as f:
                    f.write(content)
                return

    def _simple_yaml_parse(self, text):
        """简单 YAML 解析器"""
        result = {}
        current_skill = None

        for line in text.strip().split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # 一级缩进（2空格）= skill 名
            if line.startswith("  ") and not line.startswith("    "):
                if ":" in stripped:
                    k, v = stripped.split(":", 1)
                    current_skill = k.strip()
                    v = v.strip()
                    if not current_skill in result:
                        result[current_skill] = {}
                    if v and v not in ("", "null", "~"):
                        try:
                            result[current_skill][k.strip()] = json.loads(v)
                        except (json.JSONDecodeError, ValueError):
                            result[current_skill][k.strip()] = v
            elif not line.startswith(" "):
                if ":" in stripped:
                    k, v = stripped.split(":", 1)
                    key = k.strip()
                    v = v.strip()
                    if v and v not in ("", "null", "~"):
                        try:
                            result[key] = json.loads(v)
                        except (json.JSONDecodeError, ValueError):
                            result[key] = v
                    else:
                        result[key] = {}

        return result


def main():
    args = sys.argv[1:]
    if not args:
        _print_usage()
        return

    command = args[0]
    project_path = os.getcwd()

    if command == "validate":
        if len(args) < 2:
            print("错误: 用法: validate <skill_name> [project_path]", file=sys.stderr)
            sys.exit(1)
        skill_name = args[1]
        if len(args) > 2:
            project_path = args[2]
        validator = OutputValidator(project_path)
        # 尝试从项目目录的 DESIGN.md 自动加载规则
        design = Path(project_path) / "DESIGN.md"
        if design.exists():
            validator.load_from_design(str(design))
        result = validator.validate(skill_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["warnings"]:
            print("\n警告:")
            for w in result["warnings"]:
                print(f"  - {w}")

    elif command == "validate-all":
        if len(args) > 1:
            project_path = args[1]
        validator = OutputValidator(project_path)
        design = Path(project_path) / "DESIGN.md"
        if design.exists():
            validator.load_from_design(str(design))
        results = validator.validate_all()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print()
        print(validator.get_report())

    elif command == "auto-fix":
        if len(args) < 2:
            print("错误: 用法: auto-fix <skill_name> [project_path]", file=sys.stderr)
            sys.exit(1)
        skill_name = args[1]
        if len(args) > 2:
            project_path = args[2]
        validator = OutputValidator(project_path)
        design = Path(project_path) / "DESIGN.md"
        if design.exists():
            validator.load_from_design(str(design))
        validator.auto_fix(skill_name)

    elif command == "load-design":
        if len(args) < 2:
            print("错误: 用法: load-design <DESIGN.md>", file=sys.stderr)
            sys.exit(1)
        validator = OutputValidator(os.getcwd())
        validator.load_from_design(args[1])
        print(f"加载了 {len(validator.validation_rules)} 个验证规则:")
        for skill, rules in validator.validation_rules.items():
            print(f"  {skill}: {list(rules.keys())}")

    elif command == "report":
        validator = OutputValidator(project_path)
        print(validator.get_report())

    else:
        _print_usage()


def _print_usage():
    print("用法:")
    print("  python output_validator.py validate <skill_name> [project_path]")
    print("  python output_validator.py validate-all [project_path]")
    print("  python output_validator.py auto-fix <skill_name> [project_path]")
    print("  python output_validator.py load-design <DESIGN.md>")
    print("  python output_validator.py report")


if __name__ == "__main__":
    main()
