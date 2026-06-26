#!/usr/bin/env python3
"""QuantClaw Skill preflight：定位引擎 + 校验依赖 + JSON输出（零外部依赖，跨平台）"""
import json, sys, os, io, importlib.util
from pathlib import Path
from collections import deque
from contextlib import redirect_stdout, redirect_stderr

PKGS = ["qgdata", "filelock", "vnpy_portfoliostrategy"] #必需pip包
EPKGS = [("vnpy_qmt", "vnpy_xt")] #(pip源码目录名, 实际import名)
MARKER = Path("backtests") / "pipeline_orchestrator.py" #引擎标识文件
MAX_D = 4 #BFS最大扫描深度
QGDATA_URL = "https://quantgo.ai/data" #Token获取地址
SKIP = frozenset({".git", "__pycache__", "node_modules", "venv", ".venv", #通用
    "Windows", "$Recycle.Bin", "System Volume Information", "Program Files", "Program Files (x86)", "ProgramData"}) #Win系统目录

def _bases(): #跨平台搜索根
    if sys.platform == "win32":
        return [Path(f"{d}:/") for d in "CDEFG" if Path(f"{d}:/").exists()]
    return [p for p in [Path("/opt"), Path.home()] if p.exists()]

def find_engine(): #优先级：环境变量 → 受限BFS
    for k in ("QUANTCLAW_ROOT", "QMT_PROJECT_ROOT"):
        v = os.environ.get(k, "")
        if v and (Path(v) / MARKER).exists(): return str(Path(v).resolve()), "env"
    q = deque((b, 0) for b in _bases())
    while q:
        cur, depth = q.popleft()
        if (cur / MARKER).exists(): return str(cur.resolve()), "scan"
        if depth < MAX_D:
            try: q.extend((c, depth + 1) for c in sorted(cur.iterdir()) if c.is_dir() and c.name not in SKIP and not c.name.startswith('.'))
            except (PermissionError, OSError): pass
    return None, None

def chk(name): #检查单个包（静默import，防止第三方包污染stdout）
    if not importlib.util.find_spec(name): return False, None
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            m = __import__(name)
        return True, str(getattr(m, "__version__", getattr(m, "VERSION", "?")))
    except Exception: return True, "?"

def main():
    root, src = find_engine()
    deps, blockers, pip_miss, edit_cmds = {}, [], [], []
    for p in PKGS: #必需包
        ok, v = chk(p); deps[p] = {"installed": ok, "version": v}
        if not ok: blockers.append(f"{p} 未安装"); pip_miss.append(p)
    for src_dir, imp_name in EPKGS: #editable包（pip目录名≠import名）
        ok, v = chk(imp_name); has_src = bool(root) and (Path(root) / src_dir).is_dir()
        deps[src_dir] = {"installed": ok, "version": v, "source_exists": has_src}
        if not ok:
            blockers.append(f"{src_dir} 未安装" + (f"（源码在 {Path(root) / src_dir}）" if has_src else ""))
            if has_src: edit_cmds.append(f'"{sys.executable}" -m pip install -e "{Path(root) / src_dir}"')
            else: pip_miss.append(src_dir)
    if not root: blockers.insert(0, "引擎未找到：未发现包含 backtests/pipeline_orchestrator.py 的目录")
    fix = ([f'"{sys.executable}" -m pip install {" ".join(pip_miss)}'] if pip_miss else []) + edit_cmds
    hints = [] #非阻塞提示（不影响ready状态）
    _SHARED_PREFIX = "Mj9mN2xP" #引擎内置共享试用Token前缀（qg_constants.QGDATA_SHARED_TOKEN）
    token = os.environ.get("QGDATA_TOKEN", "")
    env_files = [Path(root or "") / ".env", Path.home() / ".openclaw" / ".env"] #.env文件回退读取
    if not token:
        for ef in env_files:
            try:
                for line in ef.read_text(encoding="utf-8").splitlines():
                    if line.strip().startswith("QGDATA_TOKEN") and "=" in line:
                        token = line.split("=", 1)[1].strip().strip("'\"")
                        if token: break
            except (OSError, UnicodeDecodeError): pass
    if not token: hints.append(f"QGDATA_TOKEN 未配置，回测时将回退到内置共享试用Token（每日有限额度）。获取个人Token: {QGDATA_URL}")
    elif token.startswith(_SHARED_PREFIX): hints.append(f"当前使用的是内置共享试用Token（每日有限额度），Portfolio等大数据量策略可能触发频率限制。获取个人Token: {QGDATA_URL}")
    elif len(token) < 20: hints.append(f"QGDATA_TOKEN 长度异常（{len(token)}字符），请确认是否完整。获取/重置: {QGDATA_URL}")
    ready = bool(root) and not blockers
    ec = 0 if ready else (1 if not root else 2) #0=就绪 1=引擎未找到 2=依赖缺失
    print(json.dumps({"engine_root": root, "engine_found": bool(root), "engine_source": src,
        "python_bin": sys.executable, "deps": deps, "ready": ready, "blockers": blockers, "hints": hints, "fix_cmd": fix,
        "doctor_cmd": f'"{sys.executable}" "{Path(root) / MARKER}" config-doctor' if root else None
    }, ensure_ascii=False, indent=2))
    sys.exit(ec)

if __name__ == "__main__": main()
