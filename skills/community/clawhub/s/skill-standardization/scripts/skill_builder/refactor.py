"""
refactor.py — 对非标 skill 进行整体改造（标准化）

正确逻辑：
- 技能安装目录：skills/<skill-name>/（不搬迁）
- 数据/产出物路径：应指向 skills/.standardization/<skill-name>/
- refactor 只整理技能内部文件结构，不搬迁整个目录

v2.30.0: 增加 --fix-code 参数，支持阶段3.5代码引用重写
"""

import sys
import os
import json
import shutil

import tempfile
from pathlib import Path

from scripts.cleanup_manager import start_session, end_session


class Refactor:
    def __init__(self, console=None):
        self.console = console

    def refactor(self, args):
        """对非标 skill 进行整体改造"""
        # 兼容文件路径和目录路径
        input_path = Path(args.skill_dir)
        if input_path.is_file():
            skill_dir = input_path.parent
        else:
            skill_dir = input_path

        if not skill_dir.exists():
            print(f"[X] Skill 目录不存在: {skill_dir}")
            sys.exit(1)

        # 1. dry-run 模式：只输出计划，不创建备份
        if args.dry_run:
            self._dry_run(skill_dir)
            return

        # 2. 备份（除非 --no-backup）
        backup_dir = None
        if not args.no_backup:
            backup_dir = _create_backup(skill_dir, "refactor", args.workspace)
            print(f"[file] 备份已创建: {backup_dir}")

        # ★ cleanup session: 开始追踪临时/备份文件
        _cm_manifest = start_session(str(skill_dir), "refactor")

        # ★ 步骤2.5: inspect — 读取技能全貌（备份后、改造前）
        try:
            from ..skill_inspector import inspect_skill
            print(f"\n{'='*50}")
            print("  Skill 结构扫描 — 了解全貌后再改造")
            print(f"{'='*50}")
            print(inspect_skill(str(skill_dir)))
            print()
        except ImportError:
            print("[!] skill_inspector 未找到，跳过结构扫描")

        # 3. 执行迁移（整理技能内部文件结构）
        migration_plan = self._build_migration_plan(skill_dir)

        print(f"\n=== refactor 执行计划 ===")
        print(f"Source: {skill_dir}")
        if backup_dir:
            print(f"Backup: {backup_dir}")

        # 4. 执行文件移动
        self._execute_migration(skill_dir, migration_plan)

        # 3.5 代码引用重写（--fix-code）
        if getattr(args, "fix_code", False):
            fixed = self._fix_code_references(skill_dir)
            print(f"  [fix] 代码引用重写: 修正了 {fixed} 处路径")

        # 5. 验证总字节一致性
        self._verify_migration(skill_dir, backup_dir, migration_plan)

        # 权限扫描 + 写入 permissions.md + 注入授权要求章节
        report = self._run_permission_checker(skill_dir)
        self._inject_auth_section(skill_dir, report)

        # ★ 新增：版本号 bump + 进度管理
        self._bump_version(skill_dir, "patch", {})
        self._audit_and_update_progress(skill_dir, mode="refactor")

        # ★ cleanup session: 结束追踪并清理临时/备份文件
        _cm_report = end_session()
        print(f"  清理: 删除 {_cm_report['deleted']} 个临时文件（跳过 {_cm_report['skipped']}）")
        if _cm_report["errors"]:
            for e in _cm_report["errors"]:
                print(f"    ⚠️ {e}")

        print(f"\n[OK] refactor 完成！")
        print(f"   备份位置: {backup_dir}")
        print(f"   迁移文件: {len(migration_plan)} 个")

        # ═══════════════════════════════════════════════════
        # [强制钩子] 版本号三端一致验证
        # ═══════════════════════════════════════════════════
        print(f"\n{'='*55}")
        print(f"  ⚠️ 执行完成后，请验证以下三项版本号一致：")
        print(f"  1. SKILL.md frontmatter version")
        print(f"  2. _meta.json version")
        print(f"  3. references/changelog.md 最新条目版本")
        print(f"  → 运行 audit --verify 确认三端一致")
        print(f"{'='*55}")

    def _dry_run(self, skill_dir):
        """输出迁移计划但不执行"""
        print(f"=== refactor DRY-RUN plan ===")
        print(f"Source: {skill_dir}")
        print(f"Backup: {skill_dir}_bak_refactor_YYYYMMDD_HHMMSS (将创建）")

        migration_plan = self._build_migration_plan(skill_dir)

        print(f"\nMigration plan ({len(migration_plan)} files):")
        for rule_id, src, dst, size in migration_plan:
            print(f"  {rule_id} {Path(src).name:20s} → {dst:30s} ({size // 1024}KB)")

        print(f"\nExcluded:")
        print(f"  __pycache__/        (M-05: always excluded)")
        print(f"\nTotal size: {sum(s for _, _, _, s in migration_plan) // 1024}KB")
        print(f"Verification will check ±1% tolerance")

    def _build_migration_plan(self, skill_dir):
        """构建迁移计划 — 处理文件和子目录"""
        plan = []
        excluded_dirs = {"__pycache__", "node_modules", ".git", "venv", ".venv"}
        # 已知标准目录（不迁移整个目录，但会扫描其下文件）
        known_std_dirs = {"scripts", "references", "assets"}

        for item in skill_dir.iterdir():
            if item.name in {"SKILL.md", "_meta.json", "scripts", "references"}:
                continue  # 标准文件/目录，跳过
            if item.name.startswith(".") and item.name != ".gitignore":
                continue  # 隐藏文件，跳过
            if item.is_dir() and item.name in excluded_dirs:
                continue  # 排除目录

            if item.is_file():
                # 判断迁移目标
                ext = item.suffix.lower()
                size = item.stat().st_size

                if ext in (".py", ".sh", ".bat", ".ps1"):
                    dst = skill_dir / "scripts" / item.name
                    rule_id = "M-01"
                elif ext == ".md" and size > 50 * 1024:  # > 50KB
                    dst = skill_dir / "references" / item.name
                    rule_id = "M-02"
                elif ext in (".json", ".yaml", ".toml") and item.name != "_meta.json":
                    dst = skill_dir / "scripts" / item.name
                    rule_id = "M-03"
                else:
                    continue  # 不迁移

                if dst.exists():
                    print(f"[!]  目标已存在，跳过: {dst}")
                    continue

                plan.append((rule_id, item, dst, size))

            elif item.is_dir():
                # 处理子目录：递归收集文件，判断是否需要迁移
                for sub_item in item.rglob("*"):
                    if not sub_item.is_file():
                        continue
                    # 跳过已知标准目录里的文件（已在正确位置）
                    if item.name in known_std_dirs:
                        continue
                    # 跳过排除目录里的文件
                    if any(part in excluded_dirs for part in sub_item.parts):
                        continue

                    ext = sub_item.suffix.lower()
                    size = sub_item.stat().st_size

                    # 判断目标位置：保持原目录结构
                    rel_path = sub_item.relative_to(skill_dir)
                    dst = skill_dir / rel_path
                    rule_id = "M-04"  # 数据文件迁移

                    if dst.exists():
                        continue  # 目标已存在，跳过

                    plan.append((rule_id, sub_item, dst, size))

        return plan

    def _execute_migration(self, skill_dir, plan):
        """执行迁移计划"""
        # 确保目标目录存在
        (skill_dir / "scripts").mkdir(exist_ok=True)
        (skill_dir / "references").mkdir(exist_ok=True)

        for rule_id, src, dst, size in plan:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.move(str(src), str(dst))
                print(f"  {rule_id} {Path(src).name} → {dst}")

    def _verify_migration(self, skill_dir, backup_dir, plan):
        """验证迁移前后总字节一致"""
        if not backup_dir:
            return
        orig_size = sum(p.stat().st_size for p in backup_dir.rglob("*") if p.is_file())
        new_size = sum(p.stat().st_size for p in skill_dir.rglob("*") if p.is_file())
        diff = abs(orig_size - new_size)
        if diff > orig_size * 0.01:  # >1% 差异
            print(f"[!]  警告：迁移前后大小差异 {diff} bytes ({diff / orig_size:.1%})")
        else:
            print(f"[OK] 验证通过：大小差异 <1% ({diff} bytes)")

    def _fix_code_references(self, skill_dir):
        """
        阶段3.5：代码引用重写
        扫描 scripts/*.py 中的硬编码数据目录路径，自动替换为
        skills/.standardization/<skill>/ 规范路径。
        只处理 get_*_home() 函数中的 default 赋值。
        """
        import re
        skill_name = skill_dir.name
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.is_dir():
            return 0

        # 正确路径模板（赋值语句右侧）
        correct_suffix = '".workbuddy" / "skills" / ".standardization" / "' + skill_name + '"'

        fixed_count = 0

        for py_file in sorted(scripts_dir.glob("*.py")):
            content = py_file.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")
            new_lines = []
            in_get_home = False
            modified = False

            for idx, line in enumerate(lines):
                # 检测进入 get_*_home 函数
                if re.match(r"\s*def get_\w+_home\(", line):
                    in_get_home = True
                    new_lines.append(line)
                    continue

                # 在 get_*_home 函数内，处理 default = 行
                if in_get_home and re.match(r"\s*default\s*=\s*Path\.home\(", line):
                    # 检查当前路径是否合规（包含 .standardization）
                    rest = "\n".join(lines[idx:])
                    if ".standardization" not in rest or skill_name not in rest:
                        # 不合规，需要修复
                        indent = line[:len(line) - len(line.lstrip())]
                        new_line = indent + "default = Path.home() / " + correct_suffix
                        new_lines.append(new_line)
                        modified = True
                        fixed_count += 1
                        continue

                # 退出函数检测：遇到 return 或下一个 def
                if in_get_home and line.strip().startswith("return "):
                    in_get_home = False

                new_lines.append(line)

            if modified:
                py_file.write_text("\n".join(new_lines), encoding="utf-8")
                print(f"    [OK] 修正 {py_file.name}: default 路径 → skills/.standardization/{skill_name}/")

        return fixed_count

    def _run_permission_checker(self, skill_dir):
        """运行 permission_checker.py 扫描权限"""
        checker = Path(__file__).parent.parent / "scripts" / "permission_checker.py"
        if not checker.exists():
            print(f"[!] permission_checker.py 不存在: {checker}")
            return None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                out = f.name
            result = subprocess.run(
                [sys.executable, str(checker), str(skill_dir), "--output", out],
                capture_output=True, text=True, timeout=30
            )
            if os.path.exists(out):
                with open(out, "r", encoding="utf-8") as f:
                    report = json.load(f)
                os.unlink(out)
                # 自动写入权限说明到 references/permissions.md
                self._write_permission_md(skill_dir, report)
                return report
            return None
        except Exception as e:
            print(f"[!] 运行 permission_checker.py 失败: {e}")
            return None

    def _write_permission_md(self, skill_dir, report):
        """将权限扫描报告自动写入 references/permissions.md（详细格式）"""
        from pathlib import Path as Path2
        import json as json2

        skill_dir = Path(skill_dir)
        pm = skill_dir / "references" / "permissions.md"
        issues = report.get("issues", [])
        risk_level = report.get("risk_level", "unknown")

        if not issues:
            print("[💡] 权限扫描无风险项，跳过 permissions.md 写入")
            return

        lines = []
        lines.append("# 基于skill-standardization渐进式披露规范的权限说明\n")
        lines.append(f"权限扫描风险等级：**{risk_level}**\n")
        lines.append("## 权限总览\n")
        lines.append(f"共 {len(issues)} 项权限风险，按类别分组如下：\n")

        # 按类别分组（使用 type 字段）
        categories = {}
        for iss in issues:
            cat = iss.get("type", "other")
            categories.setdefault(cat, []).append(iss)

        # 类型中文映射
        type_cn = {
            "sensitive_access": "敏感信息访问",
            "critical_write": "关键位置写入",
            "network_access": "网络访问",
            "file_delete": "文件删除",
            "subprocess_call": "子进程调用",
            "missing_declaration": "缺少声明",
        }
        cat_desc = {
            "sensitive_access": "读取内存文件、凭证、Token 等敏感数据",
            "critical_write": "向系统关键目录或 skills/ 安装目录写入文件",
            "network_access": "通过 HTTP/HTTPS 向外发送请求或接收数据",
            "file_delete": "删除文件或目录（可能不可逆）",
            "subprocess_call": "调用系统命令或其他可执行文件",
            "missing_declaration": "SKILL.md frontmatter 未声明对应权限字段",
        }

        for cat, items in categories.items():
            cat_name = type_cn.get(cat, cat)
            cat_action = cat_desc.get(cat, "未知权限作用")
            lines.append(f"### {cat_name}（{len(items)} 项）")
            lines.append(f"> **权限作用**：{cat_action}")
            lines.append("")
            lines.append("| # | 文件 | 行号 | 匹配内容 | 风险等级 | 授权方式 | 说明 |")
            lines.append("|---|------|------|----------|----------|----------|------|")
            for i, iss in enumerate(items, 1):
                sev = iss.get("severity", "?")
                sev_cn = {"HIGH": "[ERROR] 高", "MEDIUM": "[WARN] 中", "LOW": "[OK] 低", "ERROR": "[ERROR] 高"}.get(sev, sev)
                file = iss.get("file", "")
                line = iss.get("line", "")
                match = iss.get("match", iss.get("pattern", ""))[:50]
                method = iss.get("authorization_method", "immediate")
                method_cn = {"immediate": "即时授权", "unified": "统一授权", "silent": "静默"}.get(method, method)
                reason = iss.get("reason", "")
                desc = iss.get("description", "")
                lines.append(f"| {i} | `{file}` | {line} | `{match}` | {sev_cn} | {method_cn} | {desc} |")
            lines.append("")

        lines.append("## 授权方式说明\n")
        lines.append("- **即时授权**：每次执行前需获得用户批准")
        lines.append("- **统一授权**：首次执行前获得用户批准，后续不再询问")
        lines.append("- **静默授权**：无需用户交互，自动执行并记录")
        lines.append("")
        lines.append("## 详细风险列表\n")
        for i, iss in enumerate(issues, 1):
            sev = iss.get("severity", "?")
            sev_cn = {"HIGH": "高", "MEDIUM": "中", "LOW": "低", "ERROR": "高"}.get(sev, sev)
            desc = iss.get("description", "")
            file = iss.get("file", "")
            line = iss.get("line", "")
            reason = iss.get("reason", "")
            lines.append(f"{i}. **[{sev_cn}] {desc}**")
            lines.append(f"   - 位置：`{file}` 第 {line} 行")
            if reason:
                lines.append(f"   - 原因：{reason}")
            lines.append("")

        pm.parent.mkdir(parents=True, exist_ok=True)
        new_content = "\n".join(lines)
        # 文件已存在且不含 skill-standardization 头部时，保留原有内容在下方
        if pm.exists():
            existing = pm.read_text(encoding="utf-8")
            if "基于skill-standardization渐进式披露规范的权限说明" not in existing:
                new_content = new_content + "\n\n---\n\n" + existing
        pm.write_text(new_content, encoding="utf-8")
        print(f"[[OK]] 权限扫描结果已自动写入 {pm}")

    def _inject_auth_section(self, skill_dir, report):
        """
        根据权限检查报告，为 SKILL.md 注入「## 授权要求」章节。

        授权方式直接读取 report 中每项的 authorization_method 字段
        （由 permission_checker.py 的 suggest_authorization_methods() 生成，
         已根据技能工作性质（自动化/交互式）智能判断）。
        """
        if not report:
            return
        issues = report.get("issues", [])
        if not issues:
            return

        skill_md = Path(skill_dir) / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text(encoding="utf-8")

        # 已存在则跳过
        if "## 授权要求" in content:
            print("[*] SKILL.md 已包含「授权要求」章节，跳过注入")
            return

        # 按 authorization_method 分组（来自 suggest_authorization_methods() 的智能判断）
        groups = {"immediate": [], "unified": [], "silent": []}
        for iss in issues:
            method = iss.get("authorization_method", "immediate")
            if method not in groups:
                groups[method] = []
            groups[method].append(iss)

        # 构建章节内容
        auth_section = ["\n", "\n", "## 授权要求\n", "\n"]
        for method, items in groups.items():
            if not items:
                continue
            if method == "immediate":
                auth_section.append("### 立即授权（操作前询问）\n")
            elif method == "unified":
                auth_section.append("### 统一授权（首次确认，后续信任）\n")
            elif method == "silent":
                auth_section.append("### 静默授权（无需询问）\n")
            for iss in items:
                auth_section.append(f"- `{iss.get('file', '')}:{iss.get('line', '')}` — {iss.get('operation', '')} → **{iss.get('suggested_auth', '')}**\n")
            auth_section.append("\n")

        # 注入到 SKILL.md 末尾
        skill_md.write_text(content + "".join(auth_section), encoding="utf-8")
        print(f"[*] 已注入「授权要求」章节（{sum(len(v) for v in groups.values())} 项操作）")

    # ── 版本号 bump ────────────────────────────────────────────────────────

    def _bump_version(self, skill_dir, bump_type, results):
        """自动升级版本号（SemVer）"""
        from pathlib import Path as Path2
        import re, json as json2

        skill_md = Path(skill_dir) / "SKILL.md"
        meta_file = Path(skill_dir) / "_meta.json"
        if not skill_md.exists():
            print("[!] SKILL.md 不存在，无法升级版本号")
            return

        # 读取当前版本
        content = skill_md.read_text(encoding="utf-8")
        m = re.search(r"^version:\s*([\d\.]+)", content, re.MULTILINE)
        if not m:
            print("[!] SKILL.md frontmatter 中未找到 version 字段")
            return

        old_ver = m.group(1)
        parts = list(map(int, old_ver.split(".")))
        while len(parts) < 3:
            parts.append(0)

        # 升级
        bt = (bump_type or "patch").lower()
        if bt == "major":
            parts[0] += 1
            parts[1] = 0
            parts[2] = 0
        elif bt == "minor":
            parts[1] += 1
            parts[2] = 0
        else:  # patch
            parts[2] += 1

        new_ver = ".".join(map(str, parts))

        # 写入 SKILL.md
        new_content = content[:m.start(1)] + new_ver + content[m.end(1):]
        skill_md.write_text(new_content, encoding="utf-8")

        # 写入 _meta.json
        if meta_file.exists():
            try:
                meta = json2.loads(meta_file.read_text(encoding="utf-8"))
                meta["version"] = new_ver
                meta_file.write_text(
                    json2.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8"
                )
            except Exception as e:
                print(f"[!] 更新 _meta.json 版本号失败: {e}")

        print(f"[[OK]] 版本号升级: {old_ver} → {new_ver} ({bt})")

    # ── 审计 + 进度管理 ────────────────────────────────────────────────────

    def _audit_and_update_progress(self, skill_dir, mode="refactor"):
        """审计 skill 并更新 .progress.md"""
        import subprocess, json as json2
        from pathlib import Path as Path2

        skill_dir = Path(skill_dir).resolve()
        progress_file = skill_dir / ".progress.md"

        # 1. 创建 .progress.md
        from skill_audit.progress_manager import create_progress
        create_progress(str(skill_dir), mode)

        # 2. 运行审计（通过 subprocess 调用 python -m skill_audit）
        try:
            result = subprocess.run(
                ["python", "-m", "skill_audit", "audit", str(skill_dir), "--json"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                print(f"[!] 审计失败: {result.stderr}")
                return
            audit_result = json2.loads(result.stdout)
        except Exception as e:
            print(f"[!] 审计执行失败: {e}")
            return

        # 3. 更新 .progress.md
        from skill_audit.progress_manager import update_progress_from_audit, finalize_progress
        update_progress_from_audit(str(skill_dir), audit_result)
        finalize_progress(str(skill_dir), audit_result)

        # 4. 打印报告
        from skill_audit import format_report
        print(format_report(audit_result, verbose=True))


def _create_backup(skill_dir, operation, workspace):
    """创建技能目录的 ZIP 备份（带时间戳）"""
    import zipfile
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{skill_dir.name}_bak_{operation}_{ts}.zip"
    backup_path = skill_dir.parent / backup_name

    with zipfile.ZipFile(str(backup_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(str(skill_dir)):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "__MACOSX"}]
            rel = os.path.relpath(root, str(skill_dir))
            for f in files:
                if f.endswith((".pyc", ".DS_Store")):
                    continue
                arcname = os.path.join(rel, f) if rel != "." else f
                zf.write(os.path.join(root, f), arcname)

    print(f"  [BACKUP] 已创建: {backup_path}")
    return backup_path
