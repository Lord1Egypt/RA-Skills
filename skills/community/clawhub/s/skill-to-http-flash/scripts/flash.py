#!/usr/bin/env python3
"""
skill-to-http-flash v2.0 CLI

将单个 OpenClaw Skill 编译为独立的 HTTP(S) API 服务。

v2.0：subprocess 直执行模式（不依赖 Gateway / LLM）

Usage:
  python flash.py create   --skill <name>  [--output <dir>] [--skill-dir <path>]
  python flash.py list
  python flash.py remove   --skill <name>  [--delete-files]
  python flash.py recreate --skill <name>  [--yes] [--diff]
  python flash.py cert     --skill <name>  --cert-action info|renew|import
  python flash.py systemd  --skill <name>
  python flash.py jobs-export-sqlite --skill <name>

Standalone（非 OpenClaw 环境）：
  export FLASH_SKILL_DIR=/path/to/skills
  export FLASH_DATA_DIR=/path/to/data
  或：python flash.py create --skill <name> --skill-dir /path --data-dir /path
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from string import Template

# Ensure scripts/ dir is on sys.path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


# ============================================================
# 路径探测（v2.0 三层 fallback）
# ============================================================

def _detect_flash_data_dir(override: str | None = None) -> Path:
    """探测 flash 数据目录。

    优先级：
      1. --data-dir CLI flag
      2. FLASH_DATA_DIR / OPENCLAW_FLASH_DATA_DIR env
      3. <workspace>/.skill-to-http-flash/
      4. ~/.skill-to-http-flash/
    """
    if override:
        return Path(override).expanduser()
    for env_var in ("FLASH_DATA_DIR", "OPENCLAW_FLASH_DATA_DIR"):
        if env := os.environ.get(env_var):
            return Path(env).expanduser()
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / ".skill-to-http-flash"
    return Path.home() / ".skill-to-http-flash"


def _detect_skill_dirs(override: str | None = None) -> list[Path]:
    """探测 skill 搜索目录。

    优先级：
      1. --skill-dir CLI flag（单一目录）
      2. FLASH_SKILL_DIR env
      3. 多 agent runtime 默认目录（OpenClaw / Claude Code / Cursor / 通用 ./skills）
      4. openclaw.json 的 skills.load.extraDirs（若存在）
    """
    if override:
        return [Path(override).expanduser()]
    if env := os.environ.get("FLASH_SKILL_DIR"):
        return [Path(env).expanduser()]
    # 多 agent runtime 兜底：任意 agent 环境开箱即用，无需手设 env
    dirs = [
        Path.home() / ".openclaw" / "workspace" / "skills",  # OpenClaw
        Path.home() / ".claude" / "skills",                   # Claude Code
        Path.home() / ".cursor" / "skills",                   # Cursor
        Path.home() / ".config" / "skills",                   # 通用 XDG
        Path.cwd() / "skills",                                 # 项目本地 ./skills
        Path("/app/skills"),                                  # 容器常见挂载
    ]
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text())
            for extra in cfg.get("skills", {}).get("load", {}).get("extraDirs", []):
                extra_path = Path(extra).expanduser()
                if extra_path.exists() and extra_path not in dirs:
                    dirs.append(extra_path)
    except Exception:
        pass
    return dirs


def _detect_http_root() -> Path:
    """探测 cert/secrets 根目录。"""
    if env := os.environ.get("OPENCLAW_HTTP_ROOT"):
        return Path(env).expanduser()
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / ".http"
    return Path.home() / ".http"


# Lazy-init globals (set in main() after CLI args parsed)
FLASH_DATA_DIR: Path = _detect_flash_data_dir()
SKILL_DIRS: list[Path] = _detect_skill_dirs()
HTTP_ROOT: Path = _detect_http_root()
FLASH_PROJECTS_FILE: Path = FLASH_DATA_DIR / "projects.json"
DEFAULT_OUTPUT_BASE: Path = FLASH_DATA_DIR / "services"

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "server_template.py"
SKILL_MD_MAX_CHARS = 8192


def _refresh_paths(args: argparse.Namespace):
    """根据 CLI flag 覆盖全局路径。"""
    global FLASH_DATA_DIR, SKILL_DIRS, FLASH_PROJECTS_FILE, DEFAULT_OUTPUT_BASE, HTTP_ROOT
    FLASH_DATA_DIR = _detect_flash_data_dir(getattr(args, "data_dir", None))
    SKILL_DIRS = _detect_skill_dirs(getattr(args, "skill_dir", None))
    HTTP_ROOT = _detect_http_root()
    FLASH_PROJECTS_FILE = FLASH_DATA_DIR / "projects.json"
    DEFAULT_OUTPUT_BASE = FLASH_DATA_DIR / "services"
    FLASH_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Skill 查找 / frontmatter
# ============================================================

def _find_skill(name: str) -> Path | None:
    for base_dir in SKILL_DIRS:
        if not base_dir.exists():
            continue
        candidate = base_dir / name
        if candidate.is_dir() and (candidate / "SKILL.md").exists():
            return candidate
        for subdir in base_dir.iterdir():
            if not subdir.is_dir():
                continue
            skill_md = subdir / "SKILL.md"
            if not skill_md.exists():
                continue
            try:
                fm = _parse_frontmatter_flat(skill_md.read_text(encoding="utf-8", errors="replace"))
                if fm.get("name") == name:
                    return subdir
            except Exception:
                pass
    return None


def _parse_frontmatter_flat(content: str) -> dict[str, str]:
    """简易 frontmatter parser（顶层 key:value，支持 YAML `>-` / `>` / `|` 多行字符串折叠）。

    支持：
      single_line: value
      folded: >-              # 折叠多行（空格连接）
        line 1
        line 2
      literal: |              # 保留换行
        line 1
        line 2
    不支持：嵌套对象（如 metadata: {...}）/ 列表
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return {}
    result: dict[str, str] = {}
    lines = m.group(1).split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        if not line or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not key:
            continue

        # 检查是否是多行字符串标记 `>` / `>-` / `|` / `|-` 后跟缩进块
        is_folded = val in (">", ">-")    # 折叠：换行变空格
        is_literal = val in ("|", "|-")    # 保留：换行保留
        if is_folded or is_literal:
            # 收集后续缩进行直到下一个顶层 key 或文件结束
            block_lines: list[str] = []
            while i < len(lines):
                next_line = lines[i]
                # 缩进行（任何空格/tab 缩进）+ 非空行才是 block 内容
                if next_line and (next_line[0] in (" ", "\t")):
                    block_lines.append(next_line.lstrip())
                    i += 1
                elif not next_line.strip():
                    # 空行属于 block（literal 保留为换行，folded 折叠）
                    block_lines.append("")
                    i += 1
                else:
                    break  # 顶层 key 开始
            if is_folded:
                # 折叠：连续非空行用空格连接，空行变换行
                result[key] = " ".join(l for l in block_lines if l).strip()
            else:
                result[key] = "\n".join(block_lines).strip()
            continue

        # 普通单行 value，去引号
        val = val.strip('"').strip("'")
        if val:
            result[key] = val
    return result


def _load_projects() -> dict:
    if FLASH_PROJECTS_FILE.exists():
        try:
            return json.loads(FLASH_PROJECTS_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_projects(projects: dict):
    FLASH_PROJECTS_FILE.write_text(json.dumps(projects, ensure_ascii=False, indent=2))


def _yesno(prompt: str, default: bool = True) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    try:
        answer = input(prompt + suffix).strip().lower()
    except EOFError:
        return default
    if not answer:
        return default
    return answer in ("y", "yes")


# ============================================================
# Template rendering
# ============================================================

def _render_server(
    skill_name: str,
    skill_description: str,
    skill_md: str,
    skill_dir: str,
    entry_rel: str,
    interpreter: str,
    input_schema: dict,
    port: int,
    timeout: int,
    tls_enabled: bool = False,
) -> str:
    tpl = TEMPLATE_PATH.read_text()
    if len(skill_md) > SKILL_MD_MAX_CHARS:
        skill_md = skill_md[:SKILL_MD_MAX_CHARS] + "\n\n[... SKILL.md truncated at generation time ...]"
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tmpl = Template(tpl)
    return tmpl.substitute(
        skill_name=repr(skill_name),
        skill_description=repr(skill_description),
        skill_dir=repr(skill_dir),
        entry_rel=repr(entry_rel),
        interpreter=repr(interpreter),
        port=str(port),
        timeout=str(timeout),
        tls_enabled=str(bool(tls_enabled)),
        skill_md_embedded=repr(skill_md),
        input_schema_json=json.dumps(input_schema, ensure_ascii=False),
        generated_at=repr(generated_at),
    )


# ============================================================
# Interactive param confirmation
# ============================================================

def _interactive_confirm_params(
    skill_name: str,
    schema: dict,
    entry_rel: str,
    interpreter: str,
) -> tuple[dict, int, int, bool]:
    print(f"\n📋 Entry: {entry_rel} (interpreter: {interpreter})")
    print(f"📋 Extracted parameters for '{skill_name}':")
    print(f"   {json.dumps(schema, ensure_ascii=False, indent=2)}")
    print()

    if not _yesno("Does this look correct?", default=True):
        print("\n→ You can edit params.json in the output directory then run:")
        print(f"  python flash.py recreate --skill {skill_name}")
        print()

    import socket as _sock

    def _port_free(p: int) -> bool:
        try:
            _s = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
            _s.setsockopt(_sock.SOL_SOCKET, _sock.SO_REUSEADDR, 0)
            _s.bind(('0.0.0.0', p))
            _s.close()
            return True
        except OSError:
            return False

    # 找出 7780-7800 范围内首个空闲端口作为默认推荐
    DEFAULT_PORT = 7780
    suggested_port = DEFAULT_PORT
    if not _port_free(DEFAULT_PORT):
        for p in range(DEFAULT_PORT + 1, DEFAULT_PORT + 21):
            if _port_free(p):
                suggested_port = p
                print(f"   ℹ️  Port {DEFAULT_PORT} is in use, suggesting next free port {suggested_port}.")
                break
        else:
            suggested_port = DEFAULT_PORT  # 范围内都没空，让用户自己挑

    while True:
        try:
            port_str = input(f"Port [{suggested_port}]: ").strip()
        except EOFError:
            port_str = ""
        if not port_str:
            port = suggested_port
        else:
            try:
                port = int(port_str)
                if not (1 <= port <= 65535):
                    print(f"   ❌ Invalid port '{port_str}'")
                    continue
            except ValueError:
                print(f"   ❌ Invalid port '{port_str}'")
                continue
        if _port_free(port):
            break
        print(f"   ❌ Port {port} is already in use. Try another or press Enter to use {suggested_port}.")

    while True:
        try:
            timeout_str = input("Default subprocess timeout in seconds [60]: ").strip()
        except EOFError:
            timeout_str = ""
        if not timeout_str:
            timeout = 60
            break
        try:
            timeout = int(timeout_str)
            if timeout < 1:
                raise ValueError
            break
        except ValueError:
            print(f"   ❌ Invalid timeout '{timeout_str}'")

    print()
    print("TLS / HTTPS:")
    print("  - Default: HTTP (zero-friction, caller just uses curl)")
    print("  - HTTPS: self-signed cert auto-generated (caller needs -k or trust store import)")
    try:
        tls_ans = input("Enable HTTPS? [y/N]: ").strip().lower()
    except EOFError:
        tls_ans = ""
    tls_enabled = tls_ans in ("y", "yes")

    return schema, port, timeout, tls_enabled


# ============================================================
# Commands
# ============================================================

def cmd_create(args):
    skill_name = args.skill
    skill_dir = _find_skill(skill_name)

    if not skill_dir:
        print(f"❌ Skill '{skill_name}' not found in:")
        for d in SKILL_DIRS:
            print(f"   {d}")
        print("\nHint: set --skill-dir <path> or FLASH_SKILL_DIR env var.")
        sys.exit(1)

    # 强制绝对路径：server.py 启动时 cwd 不是 flash.py 的工作目录，
    # 相对路径会解析错（standalone 模式 + 一般场景都需要绝对路径）。
    skill_dir = skill_dir.resolve()

    skill_md_path = skill_dir / "SKILL.md"
    skill_md = skill_md_path.read_text(encoding="utf-8", errors="replace")
    fm = _parse_frontmatter_flat(skill_md)
    description = fm.get("description", skill_name)

    # Resolve entry (v2.0)
    from params_generator import resolve_entry, extract_params, FALLBACK_SCHEMA
    try:
        entry_abs, entry_rel, interpreter = resolve_entry(skill_dir, skill_name, skill_md)
    except FileNotFoundError as e:
        print(f"❌ Entry resolution failed:\n")
        print(str(e))
        sys.exit(1)

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_BASE / f"{skill_name}-api"
    output_dir = output_dir.expanduser().resolve()

    if (output_dir / "server.py").exists():
        print(f"⚠️  Output directory already has a server.py: {output_dir}")
        if not _yesno("Overwrite existing project?", default=False):
            print("Aborted.")
            sys.exit(0)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔍 Skill: {skill_name}")
    print(f"   Source: {skill_dir}")
    print(f"   Entry : {entry_rel} → {entry_abs}")
    print(f"   Output: {output_dir}")
    print()

    try:
        schema = extract_params(skill_name, skill_md)
    except Exception as e:
        print(f"⚠️  Params extraction failed: {e}, using fallback")
        import copy
        schema = copy.deepcopy(FALLBACK_SCHEMA)

    confirmed_schema, port, timeout, tls_enabled = _interactive_confirm_params(
        skill_name, schema, entry_rel, interpreter
    )

    print(f"\n🔨 Generating server code...")
    server_code = _render_server(
        skill_name=skill_name,
        skill_description=description,
        skill_md=skill_md,
        skill_dir=str(skill_dir),
        entry_rel=entry_rel,
        interpreter=interpreter,
        input_schema=confirmed_schema,
        port=port,
        timeout=timeout,
        tls_enabled=tls_enabled,
    )

    server_path = output_dir / "server.py"
    server_path.write_text(server_code)
    os.chmod(server_path, 0o755)
    print(f"   ✅ {server_path}")

    params_path = output_dir / "params.json"
    params_path.write_text(json.dumps(confirmed_schema, ensure_ascii=False, indent=2))
    print(f"   ✅ {params_path}")

    req_path = output_dir / "requirements.txt"
    req_path.write_text("fastapi\nuvicorn[standard]\ncryptography\npydantic\njsonschema\n")
    print(f"   ✅ {req_path}")

    _write_start_script(output_dir, skill_name)
    _write_stop_script(output_dir, skill_name)
    _write_restart_script(output_dir, skill_name)
    _write_readme(output_dir, skill_name, description, port, timeout,
                  confirmed_schema, tls_enabled, entry_rel, interpreter)

    projects = _load_projects()
    projects[skill_name] = {
        "output_dir": str(output_dir),
        "skill_dir": str(skill_dir),
        "entry_rel": entry_rel,
        "interpreter": interpreter,
        "port": port,
        "timeout": timeout,
        "tls_enabled": tls_enabled,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skill_md_mtime": skill_md_path.stat().st_mtime,
        "flash_version": "2.0.0",
    }
    _save_projects(projects)

    _proto = "https" if tls_enabled else "http"
    print()
    print("=" * 56)
    print("  ✨  Project generated successfully (flash v2.0)")
    print("=" * 56)
    print(f"  Directory: {output_dir}")
    print(f"  Entry    : {entry_rel}")
    print(f"  Mode     : {'HTTPS' if tls_enabled else 'HTTP（默认零门槛）'}")
    print(f"  URL      : {_proto}://localhost:{port}")
    print(f"  Quick start:")
    print(f"    cd {output_dir} && pip install -r requirements.txt")
    print(f"    python3 server.py start")
    print("=" * 56)
    print()


def cmd_list(args):
    projects = _load_projects()
    if not projects:
        print("No flash projects found.")
        print("\nAvailable skills for flashing:")
        _list_available_skills()
        return

    print(f"\n📦 Flash projects ({len(projects)}):\n")
    print(f"  {'SKILL':<24} {'PORT':<8} {'ENTRY':<24} {'CREATED':<20} {'STATUS':<10}")
    print(f"  {'-'*24} {'-'*8} {'-'*24} {'-'*20} {'-'*10}")
    for name, proj in sorted(projects.items()):
        port = proj.get("port", "-")
        entry = proj.get("entry_rel", "-")[:24]
        created = proj.get("created_at", "-")
        pid_file = FLASH_DATA_DIR / f"{name}.pid"
        status = "stopped"
        if pid_file.exists():
            try:
                info = json.loads(pid_file.read_text())
                pid = info.get("pid", 0)
                os.kill(pid, 0)
                status = "running"
            except (OSError, ValueError, json.JSONDecodeError):
                status = "stale"
        print(f"  {name:<24} {str(port):<8} {entry:<24} {created:<20} {status:<10}")
    print()


def cmd_remove(args):
    skill_name = args.skill
    projects = _load_projects()

    if skill_name not in projects:
        print(f"❌ No flash project for '{skill_name}'")
        return

    proj = projects[skill_name]
    output_dir = Path(proj["output_dir"])

    pid_file = FLASH_DATA_DIR / f"{skill_name}.pid"
    if pid_file.exists():
        import signal
        try:
            info = json.loads(pid_file.read_text())
            pid = info.get("pid", 0)
            if pid:
                os.kill(pid, signal.SIGTERM)
                print(f"  🛑 Stopped running process (PID {pid})")
        except Exception:
            pass
        pid_file.unlink(missing_ok=True)

    if args.delete_files and output_dir.exists():
        import shutil
        print(f"  ⚠️  About to permanently delete: {output_dir}")
        if not _yesno("  Confirm delete?", default=False):
            print("  Deletion cancelled. No changes made.")
            return
        shutil.rmtree(output_dir)
        print(f"  🗑️  Deleted {output_dir}")
    else:
        print(f"  📁 Project files kept at {output_dir}")
        print(f"     Use --delete-files to remove them.")

    del projects[skill_name]
    _save_projects(projects)
    print(f"✅ Removed flash project '{skill_name}'")


def cmd_recreate(args):
    skill_name = args.skill
    projects = _load_projects()

    if skill_name not in projects:
        print(f"❌ No flash project for '{skill_name}'. Use 'create' first.")
        sys.exit(1)

    proj = projects[skill_name]
    output_dir = Path(proj["output_dir"])

    params_path = output_dir / "params.json"
    existing_schema = None
    if params_path.exists():
        try:
            existing_schema = json.loads(params_path.read_text())
        except Exception:
            pass

    skill_dir = Path(proj["skill_dir"])
    if not skill_dir.exists():
        skill_dir = _find_skill(skill_name)
        if not skill_dir:
            print(f"❌ Skill directory not found: {proj['skill_dir']}")
            sys.exit(1)
    # 强制绝对路径（同 cmd_create）
    skill_dir = skill_dir.resolve()
    proj["skill_dir"] = str(skill_dir)

    skill_md_path = skill_dir / "SKILL.md"
    skill_md = skill_md_path.read_text(encoding="utf-8", errors="replace")
    fm = _parse_frontmatter_flat(skill_md)
    description = fm.get("description", skill_name)

    from params_generator import resolve_entry, extract_params
    try:
        entry_abs, entry_rel, interpreter = resolve_entry(skill_dir, skill_name, skill_md)
    except FileNotFoundError as e:
        print(f"❌ Entry resolution failed:\n{e}")
        sys.exit(1)

    try:
        new_schema = extract_params(skill_name, skill_md)
    except Exception as e:
        print(f"⚠️  Params extraction failed: {e}, using existing schema")
        new_schema = existing_schema if existing_schema is not None else _get_fallback_schema()

    if existing_schema:
        old_props = set(existing_schema.get("properties", {}).keys())
        new_props = set(new_schema.get("properties", {}).keys())
        added = new_props - old_props
        removed = old_props - new_props
        if added or removed:
            print("\n📊 Schema changes detected:")
            if added:
                print(f"   + Added: {', '.join(added)}")
            if removed:
                print(f"   - Removed: {', '.join(removed)}")
            print()
        else:
            print("\n📊 No schema changes detected.")
        # Also check entry change
        if proj.get("entry_rel") != entry_rel:
            print(f"⚠️  Entry changed: {proj.get('entry_rel')} → {entry_rel}")
    else:
        print("\n📊 No existing params.json. New schema:")
        print(f"   {json.dumps(new_schema, ensure_ascii=False, indent=2)}")

    if args.diff:
        print("🔍 Diff-only mode. No changes made.")
        return

    print(f"\n🔄 Recreating '{skill_name}' at {output_dir}")
    port = proj.get("port", 7780)
    timeout = proj.get("timeout", 60)
    tls_enabled = proj.get("tls_enabled", False)
    if getattr(args, "tls_enabled", False):
        tls_enabled = True
    elif getattr(args, "no_tls", False):
        tls_enabled = False

    if not args.yes:
        if not _yesno("\nProceed with regeneration?", default=True):
            print("Cancelled.")
            return

    server_code = _render_server(
        skill_name=skill_name,
        skill_description=description,
        skill_md=skill_md,
        skill_dir=str(skill_dir),
        entry_rel=entry_rel,
        interpreter=interpreter,
        input_schema=new_schema,
        port=port,
        timeout=timeout,
        tls_enabled=tls_enabled,
    )

    server_path = output_dir / "server.py"
    server_path.write_text(server_code)
    os.chmod(server_path, 0o755)
    print(f"   ✅ {server_path} regenerated")

    params_path.write_text(json.dumps(new_schema, ensure_ascii=False, indent=2))
    print(f"   ✅ {params_path} updated")

    proj["skill_md_mtime"] = skill_md_path.stat().st_mtime
    proj["tls_enabled"] = tls_enabled
    proj["entry_rel"] = entry_rel
    proj["interpreter"] = interpreter
    proj["flash_version"] = "2.0.0"
    _save_projects(projects)

    pid_file = FLASH_DATA_DIR / f"{skill_name}.pid"
    if pid_file.exists():
        try:
            info = json.loads(pid_file.read_text())
            pid = info.get("pid", 0)
            os.kill(pid, 0)
            print(f"\n⚠️  Service is running (PID {pid}). Restart to apply:")
            print(f"   python {output_dir}/server.py stop && python {output_dir}/server.py start")
        except OSError:
            pass


def _get_fallback_schema() -> dict:
    from params_generator import FALLBACK_SCHEMA
    import copy
    return copy.deepcopy(FALLBACK_SCHEMA)


def _list_available_skills():
    for base_dir in SKILL_DIRS:
        if not base_dir.exists():
            continue
        for subdir in sorted(base_dir.iterdir()):
            if not subdir.is_dir():
                continue
            skill_md = subdir / "SKILL.md"
            if skill_md.exists():
                try:
                    fm = _parse_frontmatter_flat(skill_md.read_text(encoding="utf-8", errors="replace"))
                    name = fm.get("name", subdir.name)
                    desc = fm.get("description", "")[:60]
                    print(f"   {name:<30} {desc}")
                except Exception:
                    pass


# ============================================================
# Script generators
# ============================================================

def _write_start_script(output_dir: Path, skill_name: str):
    data_dir = str(FLASH_DATA_DIR)
    script = f"""#!/bin/bash
# Start {skill_name} API server (flash v2.0)
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
DATA_DIR="${{FLASH_DATA_DIR:-${{OPENCLAW_FLASH_DATA_DIR:-{data_dir}}}}}"
mkdir -p "$DATA_DIR/logs"

PID_FILE="$DATA_DIR/{skill_name}.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(python3 -c "import json; print(json.load(open('$PID_FILE')).get('pid',0))" 2>/dev/null)
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "❌ {skill_name} API already running (PID $PID)"
        exit 1
    fi
    rm -f "$PID_FILE"
fi

echo "Starting {skill_name} API..."
nohup python3 server.py start > "$DATA_DIR/logs/{skill_name}.log" 2>&1 &

for i in $(seq 1 10); do
    sleep 1
    if [ -f "$PID_FILE" ]; then
        PID=$(python3 -c "import json; print(json.load(open('$PID_FILE')).get('pid',0))" 2>/dev/null)
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            PORT=$(python3 -c "import json; print(json.load(open('$PID_FILE')).get('port',0))" 2>/dev/null)
            echo "✅ {skill_name} API started (PID $PID, port $PORT)"
            exit 0
        fi
    fi
done
echo "❌ Failed to start (timeout 10s)"
echo "   Check logs: $DATA_DIR/logs/{skill_name}.log"
exit 1
"""
    path = output_dir / "start.sh"
    path.write_text(script)
    os.chmod(path, 0o755)


def _write_stop_script(output_dir: Path, skill_name: str):
    script = f"""#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 server.py stop
"""
    path = output_dir / "stop.sh"
    path.write_text(script)
    os.chmod(path, 0o755)


def _write_restart_script(output_dir: Path, skill_name: str):
    script = f"""#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
bash stop.sh
sleep 1
bash start.sh
"""
    path = output_dir / "restart.sh"
    path.write_text(script)
    os.chmod(path, 0o755)


def _write_readme(
    output_dir: Path,
    skill_name: str,
    description: str,
    port: int,
    timeout: int,
    schema: dict,
    tls_enabled: bool,
    entry_rel: str,
    interpreter: str,
):
    proto = "https" if tls_enabled else "http"
    curl_flag = "-k " if tls_enabled else ""
    tls_note = (
        "- HTTPS with self-signed certificate (use `-k` with curl)\n"
        if tls_enabled else
        f"- HTTP mode (zero-friction); switch to HTTPS:\n"
        f"    `python3 flash.py recreate --skill {skill_name} --tls-enabled`\n"
    )

    readme = f"""# {skill_name} API (flash v2.0)

{description}

> Auto-generated by skill-to-http-flash v2.0 (subprocess direct execution)

## Architecture

```
POST /run  →  subprocess.run(["{interpreter}", "{entry_rel}", --foo value, ...])
            →  envelope {{ success / exit_code / elapsed_ms / data|output / stderr / truncated }}
```

不依赖 OpenClaw Gateway / LLM。秒级冷启，100% 复现。

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API guide page |
| GET | `/health` | Probe entry file + interpreter |
| GET | `/schema` | Parameter schema |
| POST | `/run` | Sync execute (default {timeout}s timeout, 512KB truncation) |
| POST | `/run/async` | Async execute (no truncation) |
| GET | `/jobs/{{job_id}}` | Poll async job |

## Quick Start

```bash
pip install -r requirements.txt
python3 server.py start
```

Access: `{proto}://localhost:{port}/docs`

## Sync Call

```bash
curl {curl_flag}-X POST {proto}://localhost:{port}/run \\
  -H "Content-Type: application/json" \\
  -d '{{"timeout_seconds": {timeout}}}'
```

Response envelope:
```json
{{
  "success": true,
  "exit_code": 0,
  "elapsed_ms": 240,
  "data": <json> | null,
  "output": <string> | null,
  "stderr": "<only if !success>",
  "truncated": false
}}
```

## Input Schema

```json
{json.dumps(schema, ensure_ascii=False, indent=2)}
```

## Param → CLI mapping rules

- `{{"foo": "x"}}` → `--foo x`
- `{{"foo_bar": 10}}` → `--foo-bar 10`
- `{{"verbose": true}}` → `--verbose`
- `{{"verbose": false}}` → (omitted)
- `{{"tags": ["a","b"]}}` → `--tags a --tags b`
- `{{"meta": {{"k":"v"}}}}` → `--meta '{{"k":"v"}}'`

Field names MUST match `[a-z][a-z0-9_]*` (security).

## Notes

- Default timeout: {timeout}s
{tls_note}- Async jobs: 1-hour memory TTL + JSONL persistence (`{FLASH_DATA_DIR}/jobs/{skill_name}.jsonl`)
- API Key auth (optional): `FLASH_API_KEY=<secret> python3 server.py start`
  Then: `curl {curl_flag}-H "X-API-Key: <secret>" {proto}://localhost:{port}/run ...`
- Runtime TLS toggle: `FLASH_TLS_ENABLED=1 python3 server.py start`
- Standalone (non-OpenClaw): set `FLASH_SKILL_DIR=/path/to/skills` env var
- To regenerate after skill upgrade: `python flash.py recreate --skill {skill_name}`
"""
    path = output_dir / "README.md"
    path.write_text(readme)


# ============================================================
# JSONL → SQLite export
# ============================================================

def cmd_jobs_export_sqlite(args):
    import sqlite3
    skill_name = args.skill
    jobs_dir = FLASH_DATA_DIR / "jobs"
    sources = sorted(jobs_dir.glob(f"{skill_name}.jsonl*"))
    if not sources:
        print(f"❌ No JSONL job files found for skill '{skill_name}' in {jobs_dir}")
        sys.exit(1)

    out_path = Path(args.output).expanduser() if args.output else jobs_dir / f"{skill_name}.db"
    print(f"📦 Exporting {len(sources)} JSONL file(s) → {out_path}")

    conn = sqlite3.connect(str(out_path))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            skill TEXT,
            status TEXT,
            created_at REAL,
            elapsed_ms INTEGER,
            result TEXT,
            error TEXT,
            error_type TEXT,
            raw_json TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_created ON jobs(created_at)")

    inserted = skipped = 0
    for src in sources:
        with src.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    skipped += 1
                    continue
                cur.execute("""
                    INSERT OR REPLACE INTO jobs
                    (job_id, skill, status, created_at, elapsed_ms,
                     result, error, error_type, raw_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rec.get("job_id"),
                    rec.get("skill"),
                    rec.get("status"),
                    rec.get("created_at"),
                    rec.get("elapsed_ms"),
                    json.dumps(rec.get("result"), ensure_ascii=False) if rec.get("result") is not None else None,
                    rec.get("error"),
                    rec.get("error_type"),
                    json.dumps(rec, ensure_ascii=False),
                ))
                inserted += 1
    conn.commit()
    cur.execute("SELECT COUNT(*), SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END), SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) FROM jobs")
    total, completed, failed = cur.fetchone()
    conn.close()

    print(f"✅ Exported {inserted} records ({skipped} malformed skipped)")
    print(f"   Total in DB: {total} (completed: {completed}, failed: {failed})")
    print(f"   Output: {out_path}")


# ============================================================
# Cert 管理（独立实现，不依赖 skill-to-http）
# ============================================================

def cmd_cert(args):
    """Manage TLS cert (uses bundled _cert.py)."""
    skill_name = args.skill
    projects = _load_projects()
    if skill_name not in projects:
        print(f"❌ No flash project for '{skill_name}'. Use 'create' first.")
        sys.exit(1)

    cert_dir = HTTP_ROOT / "certs" / f"flash-{skill_name}"
    cert_path = cert_dir / "server.crt"
    key_path = cert_dir / "server.key"
    cert_dir.mkdir(parents=True, exist_ok=True)

    import subprocess as _sp
    sub_action = args.cert_action or "info"

    if sub_action == "info":
        if not cert_path.exists():
            print(f"❌ Cert not found: {cert_path}")
            print(f"   Generate: python3 flash.py cert --skill {skill_name} --cert-action renew")
            return
        out = _sp.check_output(
            ["openssl", "x509", "-in", str(cert_path), "-noout",
             "-subject", "-enddate", "-ext", "subjectAltName"],
            text=True,
        )
        print(f"📋 Cert info for flash-{skill_name}:")
        print(f"   Path: {cert_path}")
        print(out)
        return

    if sub_action == "renew":
        try:
            from _cert import generate_self_signed_cert
        except ImportError as e:
            raise RuntimeError(f"_cert module missing (broken installation): {e}") from e
        generate_self_signed_cert(cert_path, key_path, common_name=f"flash-{skill_name}")
        print(f"✅ Cert generated for flash-{skill_name}")
        print(f"   Cert: {cert_path}")
        print(f"   Key : {key_path}")
        return

    if sub_action == "import":
        if not args.cert_src or not args.key_src:
            print("❌ import 需要 --cert-src <path> --key-src <path>")
            sys.exit(1)
        import shutil as _shutil
        _shutil.copy2(args.cert_src, cert_path)
        _shutil.copy2(args.key_src, key_path)
        os.chmod(key_path, 0o600)
        print(f"✅ Imported cert to {cert_path}")
        return


# ============================================================
# Systemd
# ============================================================

def cmd_systemd(args):
    skill_name = args.skill
    projects = _load_projects()
    if skill_name not in projects:
        print(f"❌ No flash project for '{skill_name}'. Use 'create' first.")
        sys.exit(1)

    proj = projects[skill_name]
    output_dir = proj["output_dir"]
    port = proj.get("port", 7780)
    user = os.environ.get("USER", "node")
    restart_sec = args.restart_sec

    if args.user:
        unit_path = f"~/.config/systemd/user/{skill_name}-api.service"
    else:
        unit_path = f"/etc/systemd/system/{skill_name}-api.service"

    unit = f"""[Unit]
Description={skill_name} API (skill-to-http-flash v2.0)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={user}
Group={user}
WorkingDirectory={output_dir}
ExecStart=/usr/bin/env python3 {output_dir}/server.py start
KillSignal=SIGTERM
TimeoutStopSec=15
PIDFile={FLASH_DATA_DIR}/{skill_name}.pid
Environment=FLASH_DATA_DIR={FLASH_DATA_DIR}
Environment=OPENCLAW_HTTP_ROOT={HTTP_ROOT}
Restart=always
RestartSec={restart_sec}
StandardOutput=journal
StandardError=journal
SyslogIdentifier={skill_name}-api

NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy={'default.target' if args.user else 'multi-user.target'}
"""

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(unit)
        print(f"✅ Systemd unit written to: {output_path}")
    else:
        print(unit)

    print()
    print("─" * 56)
    if args.user:
        print(f"  systemctl --user daemon-reload")
        print(f"  systemctl --user enable {skill_name}-api")
        print(f"  systemctl --user start {skill_name}-api")
        print(f"  loginctl enable-linger {user}  # 保持登出后存活")
    else:
        print(f"  sudo systemctl daemon-reload")
        print(f"  sudo systemctl enable {skill_name}-api")
        print(f"  sudo systemctl start {skill_name}-api")
    print("─" * 56)


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="skill-to-http-flash v2.0: Compile a Skill into a standalone HTTP(S) API (subprocess direct execution)",
    )
    # Global flags (standalone friendly)
    parser.add_argument("--skill-dir", help="Override skill search dir (else FLASH_SKILL_DIR / OpenClaw default)")
    parser.add_argument("--data-dir", help="Override flash data dir (else FLASH_DATA_DIR / workspace default)")

    sub = parser.add_subparsers(dest="command", help="Commands")

    p_create = sub.add_parser("create", help="Create a new flash project")
    p_create.add_argument("--skill", required=True, help="Skill name")
    p_create.add_argument("--output", help="Output directory")

    sub.add_parser("list", help="List all flash projects")

    p_remove = sub.add_parser("remove", help="Remove a flash project")
    p_remove.add_argument("--skill", required=True)
    p_remove.add_argument("--delete-files", action="store_true")

    p_recreate = sub.add_parser("recreate", help="Recreate a flash project")
    p_recreate.add_argument("--skill", required=True)
    p_recreate.add_argument("--yes", "-y", action="store_true")
    p_recreate.add_argument("--diff", action="store_true")
    p_recreate.add_argument("--tls-enabled", action="store_true")
    p_recreate.add_argument("--no-tls", action="store_true")

    p_systemd = sub.add_parser("systemd", help="Generate systemd unit file")
    p_systemd.add_argument("--skill", required=True)
    p_systemd.add_argument("--output")
    p_systemd.add_argument("--user", action="store_true")
    p_systemd.add_argument("--restart-sec", type=int, default=5)

    p_export = sub.add_parser("jobs-export-sqlite",
                              help="Export async job history (JSONL) to SQLite")
    p_export.add_argument("--skill", required=True)
    p_export.add_argument("--output")

    p_cert = sub.add_parser("cert", help="Manage TLS cert")
    p_cert.add_argument("--skill", required=True)
    p_cert.add_argument("--cert-action", choices=["info", "renew", "import"], default="info")
    p_cert.add_argument("--cert-src")
    p_cert.add_argument("--key-src")

    args = parser.parse_args()
    _refresh_paths(args)

    if args.command == "create":
        cmd_create(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "recreate":
        cmd_recreate(args)
    elif args.command == "systemd":
        cmd_systemd(args)
    elif args.command == "jobs-export-sqlite":
        cmd_jobs_export_sqlite(args)
    elif args.command == "cert":
        cmd_cert(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
