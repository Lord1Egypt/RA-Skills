"""
环境检测与包安装脚本 | Environment check and package installer
运行方式 | Run: C:\\Tools\\anaconda3\\python.exe scripts/check_env.py
"""

import subprocess
import sys
import importlib

from .reader_core import _bilingual

REQUIRED_PACKAGES = {
    "pandas": "pandas",
    "pyreadstat": "pyreadstat",
    "pyreadr": "pyreadr",
    "openpyxl": "openpyxl",
    "scipy": "scipy",
    "h5py": "h5py",
    "pyarrow": "pyarrow",
    "lxml": "lxml",
    "odfpy": "odfpy",
    "html5lib": "html5lib",
    # v1.4 新增
    "jmpio": "jmpio-python",
    "pzfx": "pzfx",
    # v1.9 新增
    "tableauhyperapi": "tableauhyperapi",  # Tableau Hyper .hyper (ships native libhyper binary)
    "dbfread": "dbfread",                  # dBASE / FoxPro .dbf read
    "dbf": "dbf",                          # dBASE / FoxPro .dbf write
    "pyodbc": "pyodbc",                    # MS Access .mdb/.accdb read (needs host Access driver)
}

def check_and_install(auto_install: bool = False):
    """检测依赖包；仅当 auto_install=True 时才安装（默认只检测，避免静默修改 Python 环境）。"""
    missing = []
    installed = []

    for import_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "unknown")
            installed.append(f"  ✅ {import_name} {version}")
        except ImportError:
            missing.append(pip_name)
            installed.append(f"  ❌ {import_name} ({_bilingual('not installed', '未安装')})")

    print(_bilingual("=== Package Status Check ===", "=== 包状态检测 ==="))
    print("\n".join(installed))

    if missing:
        missing_str = ', '.join(missing)
        if auto_install:
            print(f"\n{_bilingual(f'=== Installing missing packages: {missing_str} ===', f'=== 正在安装缺失包: {missing_str} ===')}")
            # 使用 conda 或 pip 安装
            for pkg in missing:
                print(f"\n{_bilingual(f'Installing {pkg}...', f'正在安装 {pkg}...')}")
                try:
                    # 先尝试 conda（更快，二进制包）
                    result = subprocess.run(
                        ["conda", "install", "-y", pkg, "-c", "conda-forge"],
                        capture_output=True, text=True, timeout=300
                    )
                    if result.returncode != 0:
                        # 降级到 pip
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg],
                            capture_output=True, text=True, timeout=300
                        )
                        if result.returncode != 0:
                            print(f"  ❌ {_bilingual(f'{pkg} install failed', f'{pkg} 安装失败')}: {result.stderr[:500]}")
                        else:
                            print(f"  ✅ {pip_name} {_bilingual('installed via pip successfully', '已通过 pip 安装成功')}")
                    else:
                        print(f"  ✅ {pip_name} {_bilingual('installed via conda successfully', '已通过 conda 安装成功')}")
                except Exception as e:
                    print(f"  ❌ {_bilingual(f'{pkg} install error', f'{pkg} 安装异常')}: {str(e)[:200]}")
        else:
            print(f"\n{_bilingual(f'⚠️ Missing packages: {missing_str}', f'⚠️ 缺失包: {missing_str}')}")
            print(_bilingual("By default this only checks; it does not modify the environment. To auto-install, run with --install.",
                            "默认仅检测，不修改环境。如需自动安装，请加 --install 参数运行本脚本。"))
    else:
        print(_bilingual("\n✅ All dependencies are ready", "\n✅ 所有依赖包已就绪"))

if __name__ == "__main__":
    import argparse
    _p = argparse.ArgumentParser(description=_bilingual("statdata-transfer dependency check", "statdata-transfer 依赖检测"))
    _p.add_argument("--install", action="store_true",
                    help=_bilingual("Auto-install missing dependencies (modifies the Python environment)", "自动安装缺失的依赖包（会修改 Python 环境）"))
    _args = _p.parse_args()
    check_and_install(auto_install=_args.install)
