# -*- coding: utf-8 -*-
"""
dt_discover.py - 自动检索 UE 项目和 DataTable JSON 文件
扫描用户工作区和常见路径，找到 .uproject 文件和 DataTable 相关的 JSON 文件

用法：
  python dt_discover.py                          # 自动扫描工作区和常见路径
  python dt_discover.py --root <search_dir>      # 指定搜索根目录
  python dt_discover.py --table <table_name>     # 按表名搜索 JSON 文件
  python dt_discover.py --depth <n>              # 指定搜索深度 (默认 5)
  python dt_discover.py --project <project_name> # 按项目名过滤
"""

import argparse
import json
import os
import sys
import glob
import time


def find_uproject_files(search_roots, max_depth=5):
    """在指定目录中递归搜索 .uproject 文件"""
    projects = []
    visited = set()

    for root_dir in search_roots:
        if not os.path.isdir(root_dir):
            continue
        root_dir = os.path.abspath(root_dir)
        if root_dir in visited:
            continue
        visited.add(root_dir)

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # 深度限制
            depth = dirpath.replace(root_dir, "").count(os.sep)
            if depth >= max_depth:
                dirnames.clear()
                continue

            # 跳过常见的无关目录
            skip_dirs = {'.git', '.svn', 'node_modules', '__pycache__', '.workbuddy',
                         'Binaries', 'Intermediate', 'DerivedDataCache', 'Saved'}
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            for f in filenames:
                if f.endswith('.uproject'):
                    project_path = os.path.join(dirpath, f)
                    project_name = os.path.splitext(f)[0]
                    projects.append({
                        "name": project_name,
                        "uproject": project_path,
                        "root": dirpath,
                    })

    return projects


def find_datatable_jsons(project_root, table_name=None):
    """在 UE 项目中搜索 DataTable 相关的 JSON 文件"""
    results = []
    content_dir = os.path.join(project_root, "Content")

    if not os.path.isdir(content_dir):
        return results

    # 搜索所有 JSON 文件
    for dirpath, dirnames, filenames in os.walk(content_dir):
        # 跳过无关目录
        skip_dirs = {'Intermediate', 'DerivedDataCache', 'Saved', '__pycache__'}
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for f in filenames:
            if not f.endswith('.json'):
                continue

            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, project_root)
            file_name_lower = f.lower()

            # 如果指定了表名，进行匹配
            if table_name:
                table_name_lower = table_name.lower()
                # 匹配文件名（模糊）
                if table_name_lower not in file_name_lower:
                    continue

            # 尝试读取 JSON 判断是否为 DataTable 格式（数组且元素含 Name 字段）
            info = _inspect_json(full_path)
            if info:
                results.append({
                    "file": full_path,
                    "rel_path": rel_path,
                    "file_name": f,
                    **info,
                })

    return results


def find_datatable_jsons_by_content(project_root, table_name):
    """通过文件内容搜索 — 当文件名不匹配时，在 JSON 内容中查找表名关键字"""
    results = []
    content_dir = os.path.join(project_root, "Content")

    if not os.path.isdir(content_dir):
        return results

    table_name_lower = table_name.lower()

    for dirpath, dirnames, filenames in os.walk(content_dir):
        skip_dirs = {'Intermediate', 'DerivedDataCache', 'Saved', '__pycache__'}
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for f in filenames:
            if not f.endswith('.json'):
                continue

            full_path = os.path.join(dirpath, f)

            # 先快速检查文件内容中是否包含表名关键字
            try:
                with open(full_path, 'rb') as fh:
                    raw_head = fh.read(4096)  # 只读前 4KB 做快速判断
                # 尝试多种编码
                for enc in ['utf-8', 'utf-16-le', 'utf-16-be']:
                    try:
                        head_text = raw_head.decode(enc).lower()
                        if table_name_lower in head_text:
                            info = _inspect_json(full_path)
                            if info:
                                rel_path = os.path.relpath(full_path, project_root)
                                results.append({
                                    "file": full_path,
                                    "rel_path": rel_path,
                                    "file_name": f,
                                    **info,
                                })
                            break
                    except (UnicodeDecodeError, UnicodeError):
                        continue
            except (IOError, OSError):
                continue

    return results


def _inspect_json(json_path):
    """快速检测 JSON 文件是否为 DataTable 格式，返回摘要信息"""
    try:
        with open(json_path, "rb") as f:
            raw = f.read()

        # 编码检测
        if raw[:2] == b'\xff\xfe':
            text = raw.decode("utf-16-le")
            if text and text[0] == '\ufeff':
                text = text[1:]
            encoding = "utf-16-le"
        elif raw[:2] == b'\xfe\xff':
            text = raw.decode("utf-16-be")
            if text and text[0] == '\ufeff':
                text = text[1:]
            encoding = "utf-16-be"
        elif raw[:3] == b'\xef\xbb\xbf':
            text = raw[3:].decode("utf-8")
            encoding = "utf-8-bom"
        else:
            text = raw.decode("utf-8")
            encoding = "utf-8"

        data = json.loads(text)

        # DataTable JSON 通常是一个数组，每个元素含 "Name" 字段
        if isinstance(data, list) and len(data) > 0:
            first = data[0]
            if isinstance(first, dict) and "Name" in first:
                # 收集一些摘要信息
                fields = sorted(first.keys())
                sample_names = [str(s.get("Name", "")) for s in data[:5]]
                return {
                    "encoding": encoding,
                    "row_count": len(data),
                    "fields": fields,
                    "sample_ids": sample_names,
                    "is_datatable": True,
                }

        return None

    except (json.JSONDecodeError, UnicodeDecodeError, IOError, OSError):
        return None


def get_default_search_roots():
    """获取默认的搜索路径"""
    roots = []

    # 1. 当前工作目录
    cwd = os.getcwd()
    roots.append(cwd)

    # 2. 工作区根目录（向上查找 .uproject）
    check_dir = cwd
    for _ in range(10):
        if any(f.endswith('.uproject') for f in os.listdir(check_dir) if os.path.isfile(os.path.join(check_dir, f))):
            roots.append(check_dir)
            break
        parent = os.path.dirname(check_dir)
        if parent == check_dir:
            break
        check_dir = parent

    # 3. 常见的 UE 项目位置（Windows）
    if sys.platform == 'win32':
        home = os.path.expanduser("~")
        common_paths = [
            os.path.join(home, "Documents", "Unreal Projects"),
            os.path.join(home, "Desktop"),
            "D:\\",
            "E:\\",
            "C:\\Users",
        ]
        # 搜索常见的 Perforce/SVN 工作区根目录
        for drive in ['C', 'D', 'E', 'F']:
            drive_root = f"{drive}:\\"
            if os.path.isdir(drive_root):
                # 只扫描驱动器根目录下的第一级目录
                try:
                    for item in os.listdir(drive_root):
                        item_path = os.path.join(drive_root, item)
                        if os.path.isdir(item_path) and not item.startswith(('$', '.')):
                            roots.append(item_path)
                except PermissionError:
                    pass

        roots.extend([p for p in common_paths if os.path.isdir(p)])

    # 4. macOS / Linux
    elif sys.platform == 'darwin':
        home = os.path.expanduser("~")
        roots.extend([
            os.path.join(home, "Documents", "Unreal Projects"),
            os.path.join(home, "Desktop"),
        ])
    else:
        home = os.path.expanduser("~")
        roots.append(home)

    # 去重
    seen = set()
    unique = []
    for r in roots:
        r_abs = os.path.abspath(r)
        if r_abs not in seen:
            seen.add(r_abs)
            unique.append(r_abs)

    return unique


def main():
    parser = argparse.ArgumentParser(description="自动检索 UE 项目和 DataTable JSON 文件")
    parser.add_argument("--root", type=str, action="append", help="搜索根目录 (可多次指定)")
    parser.add_argument("--table", type=str, help="按表名 (JSON 文件名) 搜索")
    parser.add_argument("--depth", type=int, default=5, help="搜索深度 (默认 5)")
    parser.add_argument("--project", type=str, help="按 UE 项目名过滤")
    parser.add_argument("--json-output", action="store_true", help="输出 JSON 格式 (便于脚本解析)")

    args = parser.parse_args()

    search_roots = args.root if args.root else get_default_search_roots()

    print(f"[Discover] 开始搜索 UE 项目...")
    print(f"[Discover] 搜索目录: {len(search_roots)} 个")
    print(f"[Discover] 搜索深度: {args.depth}")
    print()

    start = time.time()

    # Step 1: 查找 UE 项目
    projects = find_uproject_files(search_roots, max_depth=args.depth)

    if args.project:
        projects = [p for p in projects if args.project.lower() in p["name"].lower()]

    elapsed = time.time() - start

    if not projects:
        print("[Discover] 未找到 UE 项目。请使用 --root 指定搜索目录。")
        if args.json_output:
            print(json.dumps({"projects": [], "tables": []}, ensure_ascii=False, indent=2))
        return

    print(f"[Discover] 找到 {len(projects)} 个 UE 项目 ({elapsed:.1f}s):\n")

    for i, proj in enumerate(projects):
        print(f"  [{i + 1}] {proj['name']}")
        print(f"      路径: {proj['root']}")
        print(f"      .uproject: {proj['uproject']}")
        print()

    # Step 2: 在每个项目中搜索 DataTable JSON
    all_tables = []
    for proj in projects:
        tables = find_datatable_jsons(proj["root"], table_name=args.table)

        # 如果按文件名没找到，尝试按内容搜索
        if not tables and args.table:
            tables = find_datatable_jsons_by_content(proj["root"], args.table)

        for t in tables:
            t["project"] = proj["name"]
            t["project_root"] = proj["root"]
        all_tables.extend(tables)

    if all_tables:
        print(f"[Discover] 找到 {len(all_tables)} 个 DataTable JSON 文件:\n")
        for i, t in enumerate(all_tables):
            print(f"  [{i + 1}] {t['file_name']} ({t['row_count']} 行, {t['encoding']})")
            print(f"      项目: {t['project']}")
            print(f"      路径: {t['file']}")
            print(f"      相对路径: {t['rel_path']}")
            print(f"      示例 ID: {', '.join(t['sample_ids'])}")
            print(f"      字段数: {len(t['fields'])}")
            print()
    else:
        print("[Discover] 未找到 DataTable JSON 文件。")
        if args.table:
            print(f"  提示: 未找到与 '{args.table}' 匹配的 JSON 文件。")
            print(f"  请确认表名是否正确，或使用不带 --table 的命令查看所有 JSON 文件。")

    # JSON 输出（便于脚本解析）
    if args.json_output:
        output = {
            "projects": projects,
            "tables": [{
                "file": t["file"],
                "rel_path": t["rel_path"],
                "file_name": t["file_name"],
                "project": t["project"],
                "project_root": t["project_root"],
                "encoding": t["encoding"],
                "row_count": t["row_count"],
                "sample_ids": t["sample_ids"],
                "field_count": len(t["fields"]),
            } for t in all_tables],
        }
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
