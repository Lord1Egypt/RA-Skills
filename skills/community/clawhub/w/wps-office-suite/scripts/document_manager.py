# 文档管理脚本 v2.0
import argparse
import json
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta


def open_document(path: str) -> dict:
    """打开文档"""
    try:
        path = Path(path).resolve()
        if not path.exists():
            return {"success": False, "error": f"文件不存在: {path}"}

        if sys.platform == "win32":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])

        return {"success": True, "path": str(path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_document(path: str, output_dir: str = None) -> dict:
    """保存/备份文档"""
    try:
        path = Path(path).resolve()
        if not path.exists():
            return {"success": False, "error": f"文件不存在: {path}"}

        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / path.name
        else:
            desktop = Path.home() / "Desktop"
            backup_dir = desktop / "WPS_Backup"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = backup_dir / f"{path.stem}_{timestamp}{path.suffix}"

        shutil.copy2(str(path), str(output_path))
        return {"success": True, "path": str(output_path)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_recent_documents(limit: int = 10) -> dict:
    """获取最近文档"""
    try:
        home = Path.home()
        search_dirs = [
            home / "Desktop",
            home / "Documents",
        ]

        d_drive = Path("D:/文档")
        if d_drive.exists():
            search_dirs.append(d_drive)

        valid_extensions = {'.docx', '.xlsx', '.pptx', '.pdf'}
        recent_files = []
        cutoff = datetime.now() - timedelta(days=30)

        for d in search_dirs:
            if not d.exists():
                continue
            for f in d.glob("*"):
                if f.is_file() and f.suffix.lower() in valid_extensions:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if mtime > cutoff:
                        recent_files.append({
                            "name": f.name,
                            "path": str(f),
                            "modified": mtime.isoformat(),
                            "size": f.stat().st_size,
                            "source_dir": str(d)
                        })

        recent_files.sort(key=lambda x: x["modified"], reverse=True)
        return {"success": True, "files": recent_files[:limit], "total_found": len(recent_files)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_document_info(path: str) -> dict:
    """获取文档信息"""
    try:
        path = Path(path).resolve()
        if not path.exists():
            return {"success": False, "error": f"文件不存在: {path}"}

        stat = path.stat()
        size = stat.st_size
        size_human = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.2f} MB"

        return {
            "success": True,
            "name": path.name,
            "path": str(path),
            "size": size,
            "size_human": size_human,
            "suffix": path.suffix.lower(),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="文档管理 v2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    p_open = sub.add_parser("open")
    p_open.add_argument("--path", required=True)

    p_save = sub.add_parser("save")
    p_save.add_argument("--path", required=True)
    p_save.add_argument("--output-dir", default=None)

    p_recent = sub.add_parser("recent")
    p_recent.add_argument("--limit", type=int, default=10)

    p_info = sub.add_parser("info")
    p_info.add_argument("--path", required=True)

    args = parser.parse_args()

    try:
        if args.command == "open":
            result = open_document(args.path)
        elif args.command == "save":
            result = save_document(args.path, args.output_dir)
        elif args.command == "recent":
            result = get_recent_documents(args.limit)
        elif args.command == "info":
            result = get_document_info(args.path)
        else:
            result = {"error": f"未知命令: {args.command}"}

        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
