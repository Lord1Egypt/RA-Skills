"""
inspector.py — 技能功能蓝皮书扫描器

对目标技能执行全量结构扫描，输出结构化的 BlueBook 数据。
扫描内容：
- 文件清单（按类型分组：Python/MD/shell/JSON/其他）
- AST 函数签名（Python 文件的 def/class 名称和参数）
- 引用链路（MD 中引用的脚本、函数、文件）
- 安全数据（敏感操作：文件删除、网络请求、subprocess）
- 模块依赖关系（import 关系图）
- 约束提取（从 SKILL.md 提取"必须/禁止/铁律/应/不得"等约束关键词）

S4 阶段A：约束提取由 extract_constraints() 函数完成，
产出结构化约束清单供 S4 引擎使用。
"""
import ast
import json
import os
import re
import subprocess
import sys
from typing import Optional

# 流程钩子
_HOOKS_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hooks.py"
))
def _hook_check(skill_dir, step):
    r = subprocess.run([sys.executable, _HOOKS_SCRIPT, "check", skill_dir, step],
                        capture_output=True, text=True, encoding="utf-8")
    if r.stdout and r.stdout.strip(): print(r.stdout)
    if r.returncode != 0: sys.exit(r.returncode)
def _hook_done(skill_dir, step):
    subprocess.run([sys.executable, _HOOKS_SCRIPT, "done", skill_dir, step],
                    capture_output=True, encoding="utf-8")

# 时间线输出
_TIMELINE_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "timeline.py"
))
def _tl(skill_dir: str, *args):
    """调用 timeline.py 记录 marker"""
    try:
        subprocess.run(
            [sys.executable, _TIMELINE_SCRIPT, "mark", skill_dir] + list(args),
            capture_output=True, timeout=10,
        )
    except Exception:
        pass

# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"


class BlueBook:
    """蓝皮书数据结构"""
    def __init__(self):
        self.skill_name: str = ""
        self.version: str = ""
        self.description: str = ""
        self.file_manifest: dict = {
            "python": [],
            "markdown": [],
            "shell": [],
            "json": [],
            "other": [],
        }
        self.functions: list[dict] = []       # {file, name, type, params, lineno}
        self.classes: list[dict] = []          # {file, name, methods, lineno}
        self.reference_links: list[dict] = []  # {source, target, type}
        self.sensitive_ops: list[dict] = []    # {file, lineno, operation, type}
        self.import_chain: dict = {}           # {file: [imported_modules]}
        self.cli_scripts: list[dict] = []       # {path, name, has_main, supports: {flag:bool}}
        self.total_size_bytes: int = 0
        self.file_count: int = 0

    def to_dict(self) -> dict:
        return {
            "skill_name": self.skill_name,
            "version": self.version,
            "description": self.description,
            "file_manifest": self.file_manifest,
            "functions": self.functions,
            "classes": self.classes,
            "reference_links": self.reference_links,
            "sensitive_ops": self.sensitive_ops,
            "import_chain": self.import_chain,
            "cli_scripts": self.cli_scripts,
            "total_size_bytes": self.total_size_bytes,
            "file_count": self.file_count,
        }


class ConstraintItem:
    """从 SKILL.md 中提取的单条约束"""
    def __init__(self, cid: str, text: str, lineno: int,
                 strength: str, has_script: bool = False,
                 script_path: str = ""):
        self.cid = cid          # C-01, C-02...
        self.text = text        # 约束原文
        self.lineno = lineno    # 在 SKILL.md 中的行号
        self.strength = strength  # 必须/禁止/铁律/应/不得/建议/推荐
        self.has_script = has_script   # 是否有对应脚本支撑
        self.script_path = script_path  # 脚本路径（如果有）
        self.category = ""      # LLM 推理后填写: 脚本强制 / MD软约束
        self.noise_tolerance = ""  # LLM 推理后填写: 高/中/低
        self.design_note = ""   # LLM 推理后填写的噪音设计说明

    def to_dict(self) -> dict:
        return {
            "cid": self.cid,
            "text": self.text,
            "lineno": self.lineno,
            "strength": self.strength,
            "has_script": self.has_script,
            "script_path": self.script_path,
            "category": self.category,
            "noise_tolerance": self.noise_tolerance,
            "design_note": self.design_note,
        }


# ═══════════════════════════════════════════════════════
# 文件扫描
# ═══════════════════════════════════════════════════════

def _classify_file(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".py":
        return "python"
    if ext == ".md":
        return "markdown"
    if ext in (".sh", ".bat", ".ps1", ".bash"):
        return "shell"
    if ext == ".json":
        return "json"
    return "other"


def scan_files(skill_dir: str) -> dict:
    """扫描技能目录，按类型分类文件"""
    manifest = {"python": [], "markdown": [], "shell": [], "json": [], "other": []}
    total_size = 0
    count = 0

    exclude_dirs = {"__pycache__", ".git", ".dist", "node_modules",
                    ".standardization", "data", ".progress.md"}

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("_bak_") and not d.startswith(".venv")]
        for f in files:
            if f.endswith((".pyc", ".pyd", ".so", ".dll", ".exe")) or f in (".gitkeep", ".DS_Store"):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, skill_dir)
            cat = _classify_file(f)
            manifest[cat].append(rel)
            total_size += os.path.getsize(fpath)
            count += 1

    return manifest, total_size, count


# ═══════════════════════════════════════════════════════
# Python AST 扫描
# ═══════════════════════════════════════════════════════

def _scan_python_ast(filepath: str) -> tuple[list, list, list, list]:
    """扫描单个 Python 文件返回 (functions, classes, imports, sensitive_ops)"""
    functions = []
    classes = []
    imports = []
    sensitive_ops = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception:
        return functions, classes, imports, sensitive_ops

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            params = [arg.arg for arg in node.args.args]
            functions.append({
                "name": node.name,
                "params": params,
                "lineno": node.lineno,
            })
        elif isinstance(node, ast.AsyncFunctionDef):
            params = [arg.arg for arg in node.args.args]
            functions.append({
                "name": node.name,
                "params": params,
                "lineno": node.lineno,
                "async": True,
            })
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(item.name)
            classes.append({
                "name": node.name,
                "methods": methods,
                "lineno": node.lineno,
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}" if module else alias.name)
        elif isinstance(node, ast.Call):
            # 检测敏感操作
            func_name = ""
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                func_name = node.func.id

            if func_name in ("remove", "unlink", "rmtree", "rmdir"):
                sensitive_ops.append({
                    "lineno": node.lineno,
                    "operation": func_name,
                    "type": "file_delete",
                })
            elif func_name in ("system", "popen", "run", "call", "Popen") and \
                    isinstance(node.func, ast.Attribute) and \
                    isinstance(node.func.value, ast.Name) and \
                    node.func.value.id in ("os", "subprocess"):
                sensitive_ops.append({
                    "lineno": node.lineno,
                    "operation": f"{node.func.value.id}.{func_name}",
                    "type": "subprocess",
                })
            elif func_name in ("get", "post", "put", "delete", "request"):
                sensitive_ops.append({
                    "lineno": node.lineno,
                    "operation": func_name,
                    "type": "network",
                })

    return functions, classes, imports, sensitive_ops


# ═══════════════════════════════════════════════════════
# MD 引用扫描
# ═══════════════════════════════════════════════════════

def _scan_md_references(filepath: str) -> list[dict]:
    """从 Markdown 文件中提取引用的脚本/文件"""
    refs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return refs

    # 代码块引用: ```python ... ```
    for m in re.finditer(r'```(\w+)\n(.*?)```', content, re.DOTALL):
        lang = m.group(1)
        code = m.group(2)
        refs.append({
            "source": os.path.basename(filepath),
            "target": f"```{lang} 代码块",
            "type": "code_block",
        })
        # 代码块中的 import/from
        for imp in re.finditer(r'^(?:from\s+(\S+)\s+)?import\s+(\S+)', code, re.MULTILINE):
            refs.append({
                "source": os.path.basename(filepath),
                "target": imp.group(0).strip(),
                "type": "import_ref",
            })

    # 行内引用: `scripts/xxx.py`
    for m in re.finditer(r'`(scripts/[\w/.]+\.\w+)`', content):
        refs.append({
            "source": os.path.basename(filepath),
            "target": m.group(1),
            "type": "file_ref",
        })

    # 引用文件标记: → 详见 `references/xxx.md`
    for m in re.finditer(r'详见\s+`?([\w/.]+\.\w+)`?', content):
        refs.append({
            "source": os.path.basename(filepath),
            "target": m.group(1),
            "type": "ref_link",
        })

    return refs


# ═══════════════════════════════════════════════════════
# S4 阶段A：约束提取
# ═══════════════════════════════════════════════════════

# 约束关键词权重映射
CONSTRAINT_KEYWORDS = {
    "铁律": "铁律",
    "必须": "必须",
    "禁止": "禁止",
    "严禁": "禁止",
    "不得": "禁止",
    "不允许": "禁止",
    "应": "应",
    "不应": "禁止",
    "不要": "禁止",
    "建议": "建议",
    "推荐": "推荐",
    "可以": "建议",
}

# 脚本文件后缀列表（用于检测约束是否关联脚本）
SCRIPT_EXTS = {".py", ".sh", ".bat", ".ps1", ".js"}


def extract_constraints(skill_dir: str) -> list[dict]:
    """
    S4 阶段A：从目标技能的 SKILL.md 提取结构化约束清单。

    扫描 SKILL.md 全文，提取包含约束关键词的行，
    分析其语义强度、是否关联脚本、脚本路径。

    返回:
        list[dict]: 约束清单，每个元素为 ConstraintItem.to_dict()
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return []

    with open(skill_md, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 收集所有脚本文件路径
    all_scripts = set()
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d.startswith(".") or d == "__pycache__"]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SCRIPT_EXTS:
                rel = os.path.relpath(os.path.join(root, f), skill_dir)
                all_scripts.add(rel)

    constraints = []
    cid_counter = 0

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        # 跳过 frontmatter、注释行、空行、表格分隔行
        if not stripped or stripped.startswith("---") or stripped.startswith("#") or \
           stripped.startswith("<!--") or stripped.startswith("|--"):
            continue

        # 检测约束关键词
        found_strength = None
        for kw, strength in CONSTRAINT_KEYWORDS.items():
            if kw in stripped:
                found_strength = strength
                break

        if not found_strength:
            continue

        # 检测是否关联脚本
        has_script = False
        script_path = ""
        for sp in all_scripts:
            if sp in stripped or sp.split("/")[-1] in stripped:
                has_script = True
                script_path = sp
                break

        # 再检查该行后面几行是否有脚本引用
        if not has_script:
            for lookahead in range(1, 4):
                if lineno + lookahead <= len(lines):
                    next_line = lines[lineno + lookahead - 1]
                    for sp in all_scripts:
                        if sp in next_line or sp.split("/")[-1] in next_line:
                            has_script = True
                            script_path = sp
                            break
                    if has_script:
                        break

        cid_counter += 1
        item = ConstraintItem(
            cid=f"C-{cid_counter:02d}",
            text=stripped[:120],
            lineno=lineno,
            strength=found_strength,
            has_script=has_script,
            script_path=script_path,
        )
        constraints.append(item.to_dict())

    return constraints


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def scan(skill_dir: str) -> BlueBook:
    """对目标技能执行完整蓝皮书扫描（含 S4 阶段A 约束提取）"""
    _tl(skill_dir, "blueprint", f"蓝皮书扫描: {os.path.basename(skill_dir)}", "--type", "py_script")
    bb = BlueBook()

    # 读取 _meta.json
    meta_path = os.path.join(skill_dir, "_meta.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            bb.skill_name = meta.get("name", os.path.basename(skill_dir))
            bb.version = meta.get("version", "unknown")
            bb.description = meta.get("description", "")
        except Exception:
            pass
    if not bb.skill_name:
        bb.skill_name = os.path.basename(skill_dir)

    # 文件扫描
    manifest, total_size, count = scan_files(skill_dir)
    bb.file_manifest = manifest
    bb.total_size_bytes = total_size
    bb.file_count = count

    # AST + 引用扫描
    for cat in ("python", "markdown", "shell", "json", "other"):
        for relpath in manifest[cat]:
            abspath = os.path.join(skill_dir, relpath)

            if cat == "python":
                funcs, cls, imps, sensitive = _scan_python_ast(abspath)
                for f in funcs:
                    f["file"] = relpath
                    bb.functions.append(f)
                for c in cls:
                    c["file"] = relpath
                    bb.classes.append(c)
                for imp in imps:
                    bb.import_chain.setdefault(relpath, []).append(imp)
                for s in sensitive:
                    s["file"] = relpath
                    bb.sensitive_ops.append(s)

                # ── CLI 脚本检测 ──
                with open(abspath, "r", encoding="utf-8") as _f:
                    _content = _f.read()
                has_main = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', _content))
                if has_main:
                    supports = {"help": True}
                    for flag in ["--json", "--list", "--show", "--check-only",
                                 "--verify-llm", "--kb-list", "--list-strategies"]:
                        if flag in _content or flag.replace("-", "_") in _content:
                            supports[flag] = True
                    bb.cli_scripts.append({
                        "path": relpath,
                        "name": os.path.basename(relpath).replace(".py", ""),
                        "supports": supports,
                    })

            if cat == "markdown":
                refs = _scan_md_references(abspath)
                bb.reference_links.extend(refs)

            # shell 脚本扫描（文件大小和是否存在）
            if cat == "shell":
                if os.path.getsize(abspath) > 0:
                    bb.functions.append({
                        "file": relpath,
                        "name": os.path.basename(relpath),
                        "params": [],
                        "lineno": 1,
                        "type": "shell_script",
                    })

    _tl(skill_dir, "blueprint", f"蓝皮书扫描完成: {bb.file_count} 文件", "end",
           "--type", "py_script", "--detail", f"{bb.file_count} files, {bb.total_size_bytes} bytes")
    return bb


def print_bluebook(bb: BlueBook) -> str:
    """将蓝皮书格式化为可读文本"""
    lines = []
    lines.append(f"=== 技能蓝皮书: {bb.skill_name} v{bb.version} ===")
    lines.append(f"描述: {bb.description[:80]}...")
    lines.append(f"文件总数: {bb.file_count}（{bb.total_size_bytes} bytes）")
    lines.append("")

    for cat, files in bb.file_manifest.items():
        if files:
            lines.append(f"[{cat.upper()}] {len(files)} 个文件:")
            for f in files:
                lines.append(f"  - {f}")

    lines.append("")
    if bb.functions:
        lines.append(f"[FUNCTIONS] {len(bb.functions)} 个函数:")
        for fn in sorted(bb.functions, key=lambda x: x.get("file", "")):
            p = ", ".join(fn.get("params", []))[:60]
            ftype = fn.get("type", "")
            tag = f" [{ftype}]" if ftype else ""
            lines.append(f"  - {fn['file']}:{fn['lineno']}  {fn['name']}({p}){tag}")

    if bb.classes:
        lines.append("")
        lines.append(f"[CLASSES] {len(bb.classes)} 个类:")
        for c in bb.classes:
            methods = ", ".join(c.get("methods", []))[:60]
            lines.append(f"  - {c['file']}:{c['lineno']}  {c['name']}({methods})")

    if bb.sensitive_ops:
        lines.append("")
        lines.append(f"[SENSITIVE] 检测到 {len(bb.sensitive_ops)} 个敏感操作:")
        for s in bb.sensitive_ops:
            lines.append(f"  - {s['file']}:{s['lineno']}  [{s['type']}] {s['operation']}")

    if bb.import_chain:
        lines.append("")
        lines.append(f"[IMPORTS] import 关系:")
        for f, imps in bb.import_chain.items():
            lines.append(f"  {f} → {', '.join(imps[:5])}")

    if bb.cli_scripts:
        lines.append("")
        lines.append(f"[CLI] {len(bb.cli_scripts)} 个可执行脚本:")
        for s in bb.cli_scripts:
            flags = [k for k, v in s["supports"].items() if v]
            lines.append(f"  - {s['name']} (支持: {', '.join(flags)})")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        target = sys.argv[1]
        if os.path.isdir(target):
            _hook_check(target, "blueprint")
            bb = scan(target)
            print(print_bluebook(bb))
            # 输出 JSON 到数据目录（R-11 合规）
            _SKILLS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            target_name = os.path.basename(os.path.abspath(target))
            data_dir = os.path.join(_SKILLS_ROOT, ".standardization", "skill-function-test", "data", target_name)
            os.makedirs(data_dir, exist_ok=True)
            json_path = os.path.join(data_dir, "outputs", ".function-test_blueprint.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(bb.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"\n蓝皮书 JSON 已保存: {json_path}")

            # S4 阶段A：约束提取
            constraints = extract_constraints(target)
            # 数据目录按 R-12 规范：skills/.standardization/skill-function-test/data/<target_skill>/
            os.makedirs(data_dir, exist_ok=True)
            cpath = os.path.join(data_dir, "outputs", ".constraint-list.json")
            with open(cpath, "w", encoding="utf-8") as f:
                json.dump(constraints, f, ensure_ascii=False, indent=2)
            print(f"约束清单已保存: {cpath} ({len(constraints)} 条)")
            _hook_done(target, "blueprint")
        else:
            print(f"错误: 目录不存在 {target}")
    else:
        print("用法: python inspector.py <skill-dir>")
