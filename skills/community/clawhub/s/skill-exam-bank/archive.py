"""题库产物归档（可选步骤）：把交付物复制到**使用者自己指定**的归档目录。

用法:
  python archive.py <文件1> [文件2 ...] --to <归档根目录> [--subject "<课程代码><科目名>"]
  python archive.py <文件1> ... --subject "15044马克思主义基本原理"   # 用环境变量指定的归档根

环境变量:
  EXAM_BANK_ARCHIVE_DIR   归档根目录（--to 未给时用它）

行为:
- 归档位置完全由调用方决定：本地文件夹、NAS 挂载盘、网盘同步目录、项目目录均可，本脚本不内置任何固定路径。
- --to 与环境变量都没有时：**跳过归档**，打印提示并以退出码 0 结束（不算失败）。
- 给了 --subject 就在归档根下建同名子目录（如 `15044马克思主义基本原理`），否则直接放根目录。
- 同名文件自动覆盖（覆盖前把旧文件改名 `.bak` 保留一份）。
- 仅用标准库，零依赖，Python 3.6+ 可直接运行。
"""
import argparse
import json
import os
import shutil
import sys


def main():
    ap = argparse.ArgumentParser(description="题库产物归档（归档目录由调用方指定）")
    ap.add_argument("files", nargs="+", help="要归档的文件（xlsx / PDF / .ocr.md / .json / .check.json）")
    ap.add_argument("--to", default=os.environ.get("EXAM_BANK_ARCHIVE_DIR", ""), help="归档根目录")
    ap.add_argument("--subject", default="", help="科目子目录名，如 15044马克思主义基本原理")
    a = ap.parse_args()

    if not a.to:
        print(json.dumps({
            "ok": True, "skipped": True,
            "reason": "未指定归档目录：用 --to <目录> 或设置环境变量 EXAM_BANK_ARCHIVE_DIR",
        }, ensure_ascii=False))
        return 0

    dest = os.path.join(a.to, a.subject) if a.subject else a.to
    os.makedirs(dest, exist_ok=True)

    copied, missing = [], []
    for f in a.files:
        if not os.path.exists(f):
            missing.append(f)
            continue
        target = os.path.join(dest, os.path.basename(f))
        if os.path.exists(target):
            shutil.copy2(target, target + ".bak")
        shutil.copy2(f, target)
        copied.append(os.path.basename(f))

    print(json.dumps({
        "ok": True, "skipped": False, "archive_dir": dest,
        "copied": copied, "missing": missing,
    }, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
