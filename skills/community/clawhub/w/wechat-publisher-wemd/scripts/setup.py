#!/usr/bin/env python3
"""
setup.py

首次使用时自动初始化 WeMD 渲染引擎：
1. npm install 安装 render.js 的依赖
2. git clone WeMD → 编译 packages/core → 复制到 core-dist → 清理
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WEMD_DIR = Path(__file__).resolve().parent.parent / "vendor" / "wemd"
NODE_MODULES = WEMD_DIR / "node_modules"
CORE_DIST = WEMD_DIR / "core-dist"
LOCK_FILE = WEMD_DIR / ".installed"

WEMD_REPO = "https://github.com/tenngoxars/WeMD.git"


def is_installed() -> bool:
    return LOCK_FILE.is_file() and NODE_MODULES.is_dir() and CORE_DIST.is_dir()


def _check_cmd(cmd: str) -> bool:
    try:
        r = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def _patch_markdown_it() -> None:
    mi_pkg = NODE_MODULES / "markdown-it" / "package.json"
    if not mi_pkg.is_file():
        return
    try:
        pkg = json.loads(mi_pkg.read_text())
        if "exports" in pkg and "./lib/*" not in pkg["exports"]:
            pkg["exports"]["./lib/*"] = "./lib/*.js"
            mi_pkg.write_text(json.dumps(pkg, indent=2))
    except Exception:
        pass

    token_dir = NODE_MODULES / "markdown-it" / "lib"
    token_file = token_dir / "token.js"
    if not token_file.is_file():
        token_dir.mkdir(exist_ok=True)
        token_file.write_text(
            'class Token {\n'
            '  constructor(type,tag,nesting){this.type=type||"";this.tag=tag||"";this.nesting=nesting||0;\n'
            '    this.attrs=null;this.map=null;this.level=0;this.children=null;\n'
            '    this.content="";this.markup="";this.info="";this.meta=null;this.block=false;this.hidden=false;}\n'
            '  attrIndex(n){if(!this.attrs)return -1;for(let i=0;i<this.attrs.length;i++)if(this.attrs[i][0]===n)return i;return -1;}\n'
            '  attrPush(d){if(this.attrs)this.attrs.push(d);else this.attrs=[d];}\n'
            '  attrSet(n,v){const i=this.attrIndex(n);if(i<0)this.attrPush([n,v]);else this.attrs[i]=[n,v];}\n'
            '  attrGet(n){const i=this.attrIndex(n);return i>=0?this.attrs[i][1]:null;}\n'
            '  attrJoin(n,v){const i=this.attrIndex(n);if(i<0)this.attrPush([n,v]);else this.attrs[i][1]+=" "+v;}\n'
            '}\n'
            'module.exports=Token;\n'
        )


def _install_npm() -> str | None:
    if NODE_MODULES.is_dir():
        return None
    r = subprocess.run(
        ["npm", "install", "--omit=dev", "--no-audit", "--no-fund"],
        cwd=str(WEMD_DIR), capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0:
        return f"npm install failed: {r.stderr.strip()[:300]}"
    _patch_markdown_it()
    return None


def _build_core() -> str | None:
    if CORE_DIST.is_dir() and any(CORE_DIST.iterdir()):
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        r = subprocess.run(
            ["git", "clone", "--depth", "1", WEMD_REPO, str(tmp / "WeMD")],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            return f"git clone failed: {r.stderr.strip()[:300]}"

        core_dir = tmp / "WeMD" / "packages" / "core"
        r = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund"],
            cwd=str(core_dir), capture_output=True, text=True, timeout=120,
        )
        if r.returncode != 0:
            return f"core npm install failed: {r.stderr.strip()[:300]}"

        r = subprocess.run(
            ["npx", "--yes", "typescript", "--build"],
            cwd=str(core_dir), capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            tsc_bin = core_dir / "node_modules" / ".bin" / "tsc"
            r = subprocess.run(
                [str(tsc_bin)] if tsc_bin.is_file() else ["npx", "tsc"],
                cwd=str(core_dir), capture_output=True, text=True, timeout=60,
            )
        if r.returncode != 0:
            return f"core tsc failed: {r.stderr.strip()[:300]}"

        dist_src = core_dir / "dist"
        if not dist_src.is_dir():
            return "core build produced no dist/ directory"

        if CORE_DIST.exists():
            shutil.rmtree(CORE_DIST)
        shutil.copytree(dist_src, CORE_DIST)

    return None


def install() -> dict:
    if is_installed():
        return {"ok": True, "status": "already_installed"}

    for cmd in ["node", "npm", "git"]:
        if not _check_cmd(cmd):
            return {"ok": False, "message": f"{cmd} not found. Please install Node.js (v18+) and git."}

    err = _install_npm()
    if err:
        return {"ok": False, "message": err}

    err = _build_core()
    if err:
        return {"ok": False, "message": err}

    LOCK_FILE.write_text("installed")
    return {"ok": True, "status": "installed"}


def ensure_installed():
    if is_installed():
        return
    result = install()
    if not result["ok"]:
        raise RuntimeError(f"WeMD setup failed: {result['message']}")


def main() -> int:
    result = install()
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
