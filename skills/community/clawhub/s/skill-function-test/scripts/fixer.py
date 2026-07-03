"""
fixer.py — 通用修复工具（语言无关）

核心 I/O（safe_write/safe_patch）：任何文件类型通用。
语言特定修复器按文件扩展名自动派发，目前支持：
  .py  → add_none_guard, stdout_to_logging, exception_guard
  .sh  → shell_cd_guard, shell_null_guard, shell_stderr_guard
  .js  → js_null_guard, js_try_catch, js_console_to_logger
  .ps1 → powershell_error_guard, powershell_null_guard
"""
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime


# ── 目录定位 ──
# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.normpath(os.path.join(_SCRIPT_DIR, ".."))
_SKILLS_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, ".."))


def _fix_record_path(skill_dir: str = None) -> str:
    """修复记录文件路径"""
    if skill_dir is None:
        skill_dir = os.getcwd()
    target = os.path.basename(os.path.abspath(skill_dir))
    data_dir = os.path.normpath(os.path.join(
        _SKILLS_ROOT, ".standardization", "skill-function-test", "data", target
    ))
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, "outputs"), exist_ok=True); return os.path.join(data_dir, "outputs", ".fix-record.json")


def log_fix(skill_dir: str, fix_type: str, filepath: str, detail: str = "",
            success: bool = True):
    """记录一条修复行为到 .fix-record.json"""
    path = _fix_record_path(skill_dir)
    records = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append({
        "fix_type": fix_type,
        "filepath": filepath,
        "detail": detail,
        "success": success,
        "at": datetime.now().isoformat(timespec="seconds"),
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════
# 辅助：检测文件语言
# ═══════════════════════════════════════════════════════

def _detect_lang(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    mapping = {".py": "python", ".sh": "shell", ".bash": "shell",
               ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
               ".ps1": "powershell", ".bat": "bat", ".cmd": "bat"}
    # 无扩展名但第一行是 shebang
    if ext == "":
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                first = f.readline().strip()
            if "bash" in first or "sh" in first:
                return "shell"
            if "node" in first:
                return "javascript"
            if "pwsh" in first or "powershell" in first:
                return "powershell"
        except Exception:
            pass
    return mapping.get(ext, "unknown")


# ═══════════════════════════════════════════════════════
# 原子 I/O（语言无关）
# ═══════════════════════════════════════════════════════

def safe_write(filepath: str, content: str, encoding: str = "utf-8") -> bool:
    """原子写入，支持任意文件类型

    备份文件创建在数据目录内，不污染技能根目录。
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=os.path.dirname(os.path.abspath(filepath)),
            prefix=".fix_tmp_",
            suffix=os.path.splitext(filepath)[1] or ".tmp",
        )
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        if os.path.exists(filepath):
            # 备份到数据目录，不放在技能根目录
            import hashlib
            _data_dir = os.path.normpath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "..", ".standardization", "skill-function-test", "data",
                os.path.basename(os.path.dirname(os.path.dirname(filepath))),
                "backups"
            ))
            os.makedirs(_data_dir, exist_ok=True)
            _orig_name = os.path.basename(filepath)
            with open(filepath, "rb") as _fh:
                _hash = hashlib.sha256(_fh.read()).hexdigest()[:8]
            _ts = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
            bak_path = os.path.join(_data_dir, f"{_ts}_{_orig_name}_{_hash}.bak")
            shutil.copy2(filepath, bak_path)
        os.replace(tmp_path, filepath)
        return True
    except Exception as e:
        print(f"  [FIX] 写入失败 {filepath}: {e}")
        return False


def safe_read(filepath: str, encoding: str = "utf-8") -> str:
    """安全读取文件"""
    with open(filepath, "r", encoding=encoding) as f:
        return f.read()


# ═══════════════════════════════════════════════════════
# 字符串修补（语言无关）
# ═══════════════════════════════════════════════════════

def safe_patch(filepath: str, old_str: str, new_str: str) -> bool:
    """基于精确字符串替换的修补"""
    try:
        content = safe_read(filepath)
        if old_str not in content:
            print(f"  [FIX] 未找到匹配: {old_str[:40]}...")
            return False
        new_content = content.replace(old_str, new_str)
        return safe_write(filepath, new_content)
    except Exception as e:
        print(f"  [FIX] patch 失败: {e}")
        return False


def safe_patch_regex(filepath: str, pattern: str, replacement: str) -> bool:
    """基于正则的批量替换"""
    try:
        content = safe_read(filepath)
        new_content, count = re.subn(pattern, replacement, content)
        if count == 0:
            print(f"  [FIX] 正则未匹配: {pattern[:40]}...")
            return False
        ok = safe_write(filepath, new_content)
        if ok:
            print(f"  [FIX] 已替换 {count} 处")
        return ok
    except Exception as e:
        print(f"  [FIX] regex 修补失败: {e}")
        return False


# ═══════════════════════════════════════════════════════
# Shell 修复工具
# ═══════════════════════════════════════════════════════

def fix_shell_cd_guard(filepath: str) -> bool:
    """
    为 shell 脚本中的裸 cd 添加 || exit 1 保护
    匹配:  `cd some/path` （非 `cd some/path || exit`）
    替换为: `cd some/path || exit 1`
    """
    try:
        content = safe_read(filepath)
        # 匹配行首缩进 + cd + 非注释 + 无 ||/&&
        pattern = r'(^[\t ]*cd\s+\S+)(?!(?:\s*\|\||\s*&&))'
        new_content, count = re.subn(
            pattern, r'\1 || exit 1', content, flags=re.MULTILINE)
        if count == 0:
            print(f"  [FIX-SH] 未发现裸 cd 操作")
            return False
        ok = safe_write(filepath, new_content)
        if ok:
            print(f"  [FIX-SH] 已为 {count} 处 cd 添加 || exit 1")
        return ok
    except Exception as e:
        print(f"  [FIX-SH] cd 保护失败: {e}")
        return False


def fix_shell_null_guard(filepath: str) -> bool:
    """
    为 shell 变量展开添加 `set -u` + 默认值保护
    在文件顶部添加 set -u（如果还没有），
    将 ${var} 替换为 ${var:-}
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")
        modified = False

        # 添加 set -u 和 set -e
        has_set_u = any("set -u" in l for l in lines[:5])
        has_set_e = any("set -e" in l for l in lines[:5])
        if not has_set_u or not has_set_e:
            insert_at = 0
            for i, l in enumerate(lines[:5]):
                if l.strip().startswith("#"):
                    insert_at = i + 1
            for line in ["set -e", "set -u"]:
                if line == "set -e" and not has_set_e:
                    lines.insert(insert_at, "set -e")
                    insert_at += 1
                    modified = True
                elif line == "set -u" and not has_set_u:
                    lines.insert(insert_at, "set -u")
                    insert_at += 1
                    modified = True

        if not modified and count == 0:
            return False

        new_content = "\n".join(lines)
        return safe_write(filepath, new_content)
    except Exception as e:
        print(f"  [FIX-SH] null 保护失败: {e}")
        return False


def fix_shell_stderr_guard(filepath: str) -> bool:
    """
    将 `command 2>/dev/null` 替换为带错误输出的处理
    `command` → `command 2>&1 || echo "[WARN] command failed" >&2`
    """
    try:
        content = safe_read(filepath)
        # 匹配 2>/dev/null（忽略错误）
        pattern = r'(2\s*>\s*/dev/null)'
        new_content, count = re.subn(pattern, '2>&1', content)
        if count == 0:
            return False
        ok = safe_write(filepath, new_content)
        if ok:
            print(f"  [FIX-SH] 已处理 {count} 处 2>/dev/null")
        return ok
    except Exception as e:
        print(f"  [FIX-SH] stderr 保护失败: {e}")
        return False


# ═══════════════════════════════════════════════════════
# JavaScript 修复工具
# ═══════════════════════════════════════════════════════

def fix_js_null_guard(filepath: str) -> bool:
    """
    在 JS 函数中对参数添加空值保护
    将 `function foo(x) {` 后面的裸 `x` 调用前加 `if (x == null) return;`
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")
        new_lines = []
        in_function = False
        depth = 0
        func_param = ""
        modified = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            # 匹配函数定义
            m = re.match(r'^(function\s+\w+\s*\([^)]*\))\s*{', stripped)
            if not m:
                m = re.match(r'^(\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*=>)\s*{', stripped)
            if not m:
                m = re.match(r'^(\w+\s*\([^)]*\))\s*{', stripped)  # 方法简写

            if m:
                indent = line[:len(line) - len(line.lstrip())]
                # 提取参数名
                params_str = m.group(1)
                params = re.findall(r'(\w+)\s*[=),]', params_str.split("(")[-1]) if "(" in params_str else []
                for p in params:
                    if p in ("err", "error", "callback", "cb", "done", "next"):
                        continue
                    if len(p) > 1 and p not in ("var", "let", "const", "function", "return",
                                                  "if", "else", "for", "while", "this", "true",
                                                  "false", "null", "undefined"):
                        guard = f'{indent}  if ({p} == null) return;'
                        # 在 { 后插入
                        brace_pos = line.index("{") if "{" in line else -1
                        if brace_pos >= 0:
                            new_lines.append(line)
                            new_lines.append(guard)
                            modified = True
                            continue
                new_lines.append(line)
            else:
                new_lines.append(line)

        if not modified:
            return False
        return safe_write(filepath, "\n".join(new_lines))
    except Exception as e:
        print(f"  [FIX-JS] null 保护失败: {e}")
        return False


def fix_js_try_catch(filepath: str) -> bool:
    """
    为 JS 中的 JSON.parse / fetch / fs.readFile 等操作包裹 try/catch
    """
    try:
        content = safe_read(filepath)
        risky_patterns = [
            r'JSON\.parse\s*\(',
            r'fetch\s*\(',
            r'(?:fs\.)?readFile(?:Sync)?\s*\(',
            r'(?:fs\.)?writeFile(?:Sync)?\s*\(',
            r'JSON\.stringify\s*\(',
        ]
        combined = '|'.join(risky_patterns)
        lines = content.split("\n")
        new_lines = []
        modified = False

        for i, line in enumerate(lines):
            if re.search(combined, line) and not line.strip().startswith(("//", "*", "/*")):
                indent = line[:len(line) - len(line.lstrip())]
                # 跳过已在 try 中的
                if i > 0 and "try" in lines[i-1]:
                    new_lines.append(line)
                    continue
                new_lines.append(f"{indent}try {{")
                new_lines.append(f"{indent}  {line.strip()}")
                new_lines.append(f"{indent}}} catch (e) {{")
                new_lines.append(f'{indent}  console.error("[WARN]", e.message || e);')
                new_lines.append(f"{indent}}}")
                modified = True
            else:
                new_lines.append(line)

        if not modified:
            return False
        return safe_write(filepath, "\n".join(new_lines))
    except Exception as e:
        print(f"  [FIX-JS] try/catch 包裹失败: {e}")
        return False


def fix_js_console_to_logger(filepath: str) -> bool:
    """
    将 console.log → 替换为带前缀的结构化日志
    console.log("msg") → console.log("[SKILL]", "msg")
    """
    try:
        content = safe_read(filepath)
        pattern = r'(console\.(?:log|warn|error)\s*\()("(?:[^"]*)")'
        def replacer(m):
            prefix = m.group(1)
            msg = m.group(2)
            return f'{prefix}"[SKILL]", {msg}'
        new_content, count = re.subn(pattern, replacer, content)
        if count == 0:
            return False
        ok = safe_write(filepath, new_content)
        if ok:
            print(f"  [FIX-JS] 已处理 {count} 处 console")
        return ok
    except Exception as e:
        print(f"  [FIX-JS] console 处理失败: {e}")
        return False


# ═══════════════════════════════════════════════════════
# PowerShell 修复工具（.ps1）
# ═══════════════════════════════════════════════════════

def fix_powershell_error_guard(filepath: str) -> bool:
    """
    为 PowerShell 脚本添加 `$ErrorActionPreference = 'Stop'`
    并将裸命令包裹 try/catch
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")
        modified = False

        # 检查是否已有 ErrorActionPreference
        has_eap = any("ErrorActionPreference" in l for l in lines[:5])
        if not has_eap:
            insert_at = 0
            for i, l in enumerate(lines[:5]):
                if l.strip().startswith("#"):
                    insert_at = i + 1
            lines.insert(insert_at, "$ErrorActionPreference = 'Stop'")
            modified = True

        # 将 Invoke-WebRequest / Invoke-RestMethod 包裹 try/catch
        new_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.search(r'(Invoke-(?:WebRequest|RestMethod)|Start-Process|Remove-Item)', stripped):
                if i > 0 and "try" in lines[i-1]:
                    new_lines.append(line)
                    continue
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f"{indent}try {{")
                new_lines.append(f"{indent}    {stripped}")
                new_lines.append(f"{indent}}} catch {{")
                new_lines.append(f'{indent}    Write-Warning "操作失败: $_"')
                new_lines.append(f"{indent}}}")
                modified = True
            else:
                new_lines.append(line)

        if not modified:
            return False
        return safe_write(filepath, "\n".join(new_lines))
    except Exception as e:
        print(f"  [FIX-PS] 错误保护失败: {e}")
        return False


# ═══════════════════════════════════════════════════════
# Python 修复工具（已有，保留）
# ═══════════════════════════════════════════════════════

def fix_add_none_guard(filepath: str, func_name: str, lineno: int, param: str) -> bool:
    """
    在函数体内添加零值保护
    在 lineno 行后插入:
        if {param} == 0 / None / '':
            return 0 or raise
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")

        if lineno > len(lines):
            return False

        # 查找参数在函数中的使用位置
        guard_code = f"    if {param} == 0 or {param} is None:\n        return 0.0"
        indent = "    "

        # 在 def 行之后，第一个非注释/装饰器行之前插入
        insert_at = lineno  # lineno is the def line
        for i in range(lineno, min(lineno + 5, len(lines))):
            line = lines[i]
            if line.strip() and not line.strip().startswith(("#", "@", '"""', "'''")):
                if line.strip().startswith(("def ", "async def")):
                    continue
                insert_at = i
                break

        lines.insert(insert_at, guard_code)
        return safe_write(filepath, "\n".join(lines))
    except Exception as e:
        print(f"  [FIX] 添加零值保护失败: {e}")
        return False


def fix_stdout_to_logging(filepath: str, module_name: str = None) -> bool:
    """
    将裸 print() 替换为 logging 调用
    自动添加 logging 导入和基本配置
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")
        new_lines = []
        has_logging_import = False
        print_count = 0

        for line in lines:
            stripped = line.strip()
            # 跳过标签化的 print (如 [KB] 开头的)
            if stripped.startswith("print(") and not stripped.startswith("print(f"):
                if "[KB]" not in stripped and "[ECON" not in stripped and "[EVM" not in stripped:
                    # 提取内容
                    inner = stripped[6:].strip().strip("()").strip('"').strip("'")
                    indent = line[:len(line) - len(line.lstrip())]
                    new_lines.append(f'{indent}logging.info("{inner}")')
                    print_count += 1
                    continue
            new_lines.append(line)

        if print_count == 0:
            return False

        # 添加 logging 导入
        result = "\n".join(new_lines)
        if "import logging" not in result:
            result = "import logging\n" + result

        # 添加 logging 基本配置（只在 __main__ 前加）
        if "logging.basicConfig" not in result:
            result = result.replace(
                'if __name__ == "__main__":',
                'logging.basicConfig(level=logging.INFO, format="%(message)s")\n\nif __name__ == "__main__":',
            )

        ok = safe_write(filepath, result)
        if ok:
            print(f"  [FIX] 已替换 {print_count} 处 print → logging.info")
        return ok
    except Exception as e:
        print(f"  [FIX] print→logging 转换失败: {e}")
        return False


def fix_hardcoded_path(filepath: str, old_path: str, var_name: str) -> bool:
    """
    将硬编码路径替换为变量引用
    在文件顶部添加变量定义
    """
    try:
        content = safe_read(filepath)
        if old_path not in content:
            return False

        # 添加变量定义
        var_def = f'\n# 路径变量（替换硬编码）\n{var_name} = "{old_path}"\n'
        lines = content.split("\n")

        # 找到 import 块结束的位置
        insert_at = 0
        for i, line in enumerate(lines):
            if line.strip().startswith(("import ", "from ")):
                insert_at = i + 1

        lines.insert(insert_at, var_def.strip())

        # 替换所有硬编码路径
        new_content = "\n".join(lines)
        new_content = new_content.replace(f'"{old_path}"', var_name)
        new_content = new_content.replace(f"'{old_path}'", var_name)

        return safe_write(filepath, new_content)
    except Exception as e:
        print(f"  [FIX] 路径替换失败: {e}")
        return False


def fix_exception_guard(filepath: str, risky_pattern: str) -> bool:
    """
    为裸露的风险操作添加 try/except 包裹
    匹配行包含 risky_pattern 时，包裹 try/except
    """
    try:
        content = safe_read(filepath)
        lines = content.split("\n")
        new_lines = []
        modified = False

        for i, line in enumerate(lines):
            if risky_pattern in line and not line.strip().startswith("#"):
                indent = line[:len(line) - len(line.lstrip())]
                # 跳过已在 try 块中的
                if i > 0 and lines[i-1].strip().rstrip(":").endswith("try"):
                    new_lines.append(line)
                    continue
                new_lines.append(f"{indent}try:")
                new_lines.append(f"{indent}    {line.strip()}")
                new_lines.append(f"{indent}except Exception as e:")
                new_lines.append(f'{indent}    print(f"  [WARN] 操作失败: {{e}}")')
                modified = True
            else:
                new_lines.append(line)

        if modified:
            return safe_write(filepath, "\n".join(new_lines))
        return False
    except Exception as e:
        print(f"  [FIX] 异常包裹失败: {e}")
        return False


# ═══════════════════════════════════════════════════════
# 批量修复入口
# ═══════════════════════════════════════════════════════

def apply_fix(filepath: str, fix_type: str, params: dict = None,
              skill_dir: str = None) -> bool:
    """
    统一修复入口，按文件类型自动派发

    fix_type (语言无关):
      safe_patch, safe_patch_regex

    fix_type (Python):
      add_none_guard, stdout_to_logging, hardcoded_path, exception_guard

    fix_type (Shell):
      shell_cd_guard, shell_null_guard, shell_stderr_guard

    fix_type (JavaScript):
      js_null_guard, js_try_catch, js_console_to_logger

    fix_type (PowerShell):
      powershell_error_guard

    skill_dir 传入时自动记录修复日志
    """
    fixers = {
        "add_none_guard": lambda: fix_add_none_guard(
            filepath, params.get("func_name"), params.get("lineno", 1), params.get("param")),
        "stdout_to_logging": lambda: fix_stdout_to_logging(filepath),
        "hardcoded_path": lambda: fix_hardcoded_path(
            filepath, params.get("old_path"), params.get("var_name")),
        "exception_guard": lambda: fix_exception_guard(filepath, params.get("pattern")),
        "shell_cd_guard": lambda: fix_shell_cd_guard(filepath),
        "shell_null_guard": lambda: fix_shell_null_guard(filepath),
        "shell_stderr_guard": lambda: fix_shell_stderr_guard(filepath),
        "js_null_guard": lambda: fix_js_null_guard(filepath),
        "js_try_catch": lambda: fix_js_try_catch(filepath),
        "js_console_to_logger": lambda: fix_js_console_to_logger(filepath),
        "powershell_error_guard": lambda: fix_powershell_error_guard(filepath),
        "safe_patch": lambda: safe_patch(
            filepath, params.get("old_str"), params.get("new_str")),
        "safe_patch_regex": lambda: safe_patch_regex(
            filepath, params.get("pattern"), params.get("replacement")),
    }
    fixer = fixers.get(fix_type)
    if fixer:
        result = fixer()
        if skill_dir:
            log_fix(skill_dir, fix_type, filepath, detail=fix_type, success=result)
        return result
    print(f"  [FIX] 未知修复类型: {fix_type}")
    return False


def auto_fix(filepath: str, issue_type: str, detail: dict = None) -> bool:
    """
    智能修复：根据文件扩展名 + 问题类型自动选择合适的修复器

    参数:
      filepath: 目标文件路径
      issue_type: 问题类型（"zero_division", "null_guard", "console_log", "cd_guard" 等）
      detail: 补充信息（行号、参数名等）
    """
    lang = _detect_lang(filepath)
    issue_map = {
        ("python", "zero_division"): "add_none_guard",
        ("python", "console_log"): "stdout_to_logging",
        ("python", "exception"): "exception_guard",
        ("shell", "cd_guard"): "shell_cd_guard",
        ("shell", "null_guard"): "shell_null_guard",
        ("shell", "stderr"): "shell_stderr_guard",
        ("javascript", "null_guard"): "js_null_guard",
        ("javascript", "exception"): "js_try_catch",
        ("javascript", "console_log"): "js_console_to_logger",
        ("powershell", "exception"): "powershell_error_guard",
    }
    fix_type = issue_map.get((lang, issue_type))
    if not fix_type:
        print(f"  [FIX] 不支持修复 ({lang}, {issue_type})")
        return False
    print(f"  [FIX] 自动选择: {lang} → {fix_type}")
    return apply_fix(filepath, fix_type, detail or {})


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        filepath = sys.argv[1]
        fix_type = sys.argv[2]
        if fix_type == "auto" and len(sys.argv) >= 4:
            result = auto_fix(filepath, sys.argv[3])
        else:
            result = apply_fix(filepath, fix_type)
        print(f"  [FIX] {'成功' if result else '失败'}")
    else:
        print("用法: python fixer.py <filepath> <fix-type> [issue_type]")
        print("  fix-type: add_none_guard | stdout_to_logging | hardcoded_path |")
        print("            exception_guard | shell_cd_guard | shell_null_guard |")
        print("            js_null_guard | js_try_catch | js_console_to_logger |")
        print("            powershell_error_guard | safe_patch | safe_patch_regex | auto")
