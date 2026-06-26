"""
微信小程序分包分析工具
功能：
  1. 扫描项目文件，统计各模块大小
  2. 生成符合 2MB 限制的分包方案
  3. 输出 app.json 分包配置片段
  4. 输出各包预估大小报告

用法：
  python analyze_subpackages.py <项目目录> [--main-max MB] [--pkg-max MB]
"""

import os
import json
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# 扩展名 → 估算压缩比（实际压缩后 / 源码大小）
EXT_RATIO = {
    '.js': 0.45,
    '.wxml': 0.35,
    '.wxss': 0.35,
    '.json': 0.40,
    '.png': 0.90,
    '.jpg': 0.90,
    '.jpeg': 0.90,
    '.gif': 0.85,
    '.svg': 0.70,
    '.woff': 0.80,
    '.woff2': 0.75,
    '.ttf': 0.80,
    '.eot': 0.85,
    '.mp3': 0.98,
    '.mp4': 0.98,
    '.zip': 0.98,
}

DEFAULT_MAIN_MAX = 2.0   # MB
DEFAULT_PKG_MAX  = 2.0   # MB


@dataclass
class FileEntry:
    path: str
    size: int          # bytes
    est_compressed: int # bytes


@dataclass
class Module:
    name: str
    root: str           # 相对项目根的路径
    files: list[FileEntry] = field(default_factory=list)
    total_raw: int = 0
    total_est: int = 0

    def add_file(self, path: str, size: int):
        ratio = EXT_RATIO.get(Path(path).suffix.lower(), 0.60)
        est   = int(size * ratio)
        self.files.append(FileEntry(path, size, est))
        self.total_raw += size
        self.total_est  += est


def scan_dir(root: str) -> dict[str, int]:
    """扫描目录，返回 {相对路径: 文件大小}"""
    sizes = {}
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                sizes[os.path.relpath(full, root)] = os.path.getsize(full)
            except OSError:
                sizes[os.path.relpath(full, root)] = 0
    return sizes


def parse_app_json(root: str) -> dict:
    """读取 app.json，返回 dict"""
    path = os.path.join(root, 'app.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_app_js(root: str) -> str:
    """读取 app.js 内容"""
    path = os.path.join(root, 'app.js')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return ''


def extract_requires(content: str) -> list[str]:
    """从 JS 内容中提取 require/import 的相对路径"""
    patterns = [
        r"require\s*\(\s*['\"]([^'\"]+)['\"]",       # require('path')
        r"import\s+.*\s+from\s+['\"]([^'\"]+)['\"]", # import x from 'path'
    ]
    results = []
    for pat in patterns:
        results.extend(re.findall(pat, content))
    return results


def build_dep_graph(root: str) -> dict[str, set[str]]:
    """构建页面依赖图 {页面路径: {依赖的模块路径}}"""
    pages_dir = os.path.join(root, 'pages')
    components_dir = os.path.join(root, 'components')
    subpackages_dir = os.path.join(root, 'subpackages')

    deps = {}

    def scan_js(dir_root: str, base: str = ''):
        if not os.path.isdir(dir_root):
            return
        for dirpath, _, filenames in os.walk(dir_root):
            for fn in filenames:
                if fn.endswith('.js'):
                    full = os.path.join(dirpath, fn)
                    rel  = os.path.relpath(full, dir_root)
                    with open(full, encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    reqs = extract_requires(content)
                    # 过滤非相对路径
                    local_reqs = {r for r in reqs if not r.startswith('/') and not r.startswith('http')}
                    deps[os.path.join(base, rel)] = local_reqs

    scan_js(pages_dir, 'pages')
    scan_js(components_dir, 'components')
    if os.path.isdir(subpackages_dir):
        for pkg in os.listdir(subpackages_dir):
            pkg_path = os.path.join(subpackages_dir, pkg)
            if os.path.isdir(pkg_path):
                scan_js(pkg_path, f'subpackages/{pkg}')

    return deps


def group_pages_by_size(files: dict[str, int], pkg_max_mb: float) -> list[list[str]]:
    """
    贪心算法：将页面按预估大小分组，每组不超过 pkg_max_mb
    返回 [[页面路径列表], ...]
    """
    # 先把所有非 page 的文件算进主包（或按需分配）
    page_files = {}
    other_files = {}
    for rel, size in files.items():
        if '/pages/' in rel:
            page_files[rel] = size
        else:
            other_files[rel] = size

    # 把 pages 按顶层文件夹分组（每个文件夹 = 一个潜在包）
    pkg_groups: dict[str, dict[str, int]] = {}
    for rel, size in page_files.items():
        parts = rel.split(os.sep)
        if len(parts) >= 2:
            pkg_key = parts[1]  # pages/xxx/index.js → xxx
        else:
            pkg_key = '_misc'
        pkg_groups.setdefault(pkg_key, {})[rel] = size

    # 合并超大的包
    pkg_max_bytes = int(pkg_max_mb * 1024 * 1024)
    results = []
    current = {}
    current_size = 0

    for pkg_name in sorted(pkg_groups.keys()):
        group = pkg_groups[pkg_name]
        group_size = sum(group.values())
        est_group = sum(int(s * 0.5) for s in group.values())

        if current_size + est_group <= pkg_max_bytes:
            current.update(group)
            current_size += est_group
        else:
            if current:
                results.append(current)
            current = dict(group)
            current_size = est_group

    if current:
        results.append(current)

    return results


def estimate_page_size(page_root: str, page_dir: str) -> int:
    """估算单个页面的总大小（raw bytes）"""
    total = 0
    page_path = os.path.join(page_root, page_dir)
    if not os.path.isdir(page_path):
        return 0
    for dirpath, _, filenames in os.walk(page_path):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                total += os.path.getsize(full)
            except OSError:
                pass
    return total


def generate_subpackage_config(
    app_root: str,
    pkg_groups: list[dict[str, int]],
    main_max_mb: float,
    pkg_max_mb: float,
) -> tuple[list[dict], list[dict]]:
    """
    生成 app.json 的 subpackages 配置
    返回 (main_pages, subpackages_configs)
    """
    pages = []
    subpackages = []

    existing_pages = []
    app_json = parse_app_json(app_root)
    if 'pages' in app_json:
        existing_pages = app_json['pages']

    # 统计主包已有页面
    main_page_dirs = set()
    for p in existing_pages:
        parts = p.split('/')
        if len(parts) >= 2:
            main_page_dirs.add(parts[1])

    main_size = 0
    main_size += len(read_app_js(app_root).encode('utf-8'))
    app_json_bytes = os.path.getsize(os.path.join(app_root, 'app.json'))
    main_size += app_json_bytes
    app_wxss = os.path.join(app_root, 'app.wxss')
    if os.path.exists(app_wxss):
        main_size += os.path.getsize(app_wxss)
    app_json_content = json.dumps(app_json, ensure_ascii=False)

    # 收集所有 pages 目录下的文件夹
    pages_root = os.path.join(app_root, 'pages')
    all_page_dirs = []
    if os.path.isdir(pages_root):
        for name in os.listdir(pages_root):
            full = os.path.join(pages_root, name)
            if os.path.isdir(full):
                all_page_dirs.append(name)

    main_max_bytes = int(main_max_mb * 1024 * 1024)
    pkg_max_bytes  = int(pkg_max_mb  * 1024 * 1024)

    # 第一个组放主包（如果主包未超限）
    main_pages = []
    sub_pages_by_pkg: dict[int, list[str]] = {}

    for idx, group in enumerate(pkg_groups):
        if idx == 0 and main_size < main_max_bytes * 0.7:
            # 尝试放主包
            for rel in group:
                parts = rel.split(os.sep)
                if len(parts) >= 2:
                    page_dir = parts[1]
                    page_path = parts[1] + '/' + '/'.join(parts[2:]).rsplit('.', 1)[0]
                    main_pages.append(page_path)
                    main_size += group[rel]
        else:
            # 放分包
            sub_pages_by_pkg.setdefault(idx, [])
            for rel in sorted(group.keys()):
                parts = rel.split(os.sep)
                if len(parts) >= 2:
                    page_path = '/'.join(parts[1:]).rsplit('.', 1)[0]
                    sub_pages_by_pkg[idx].append(page_path)

    # 构建分包配置
    pkg_counter = 0
    for idx, pages_list in sub_pages_by_pkg.items():
        if not pages_list:
            continue
        root_name = f'subpackages/pkg{pkg_counter}'
        subpackages.append({
            'root': root_name,
            'pages': sorted(pages_list)
        })
        pkg_counter += 1

    return main_pages, subpackages


def bytes_to_mb(b: int) -> float:
    return b / 1024 / 1024


def main():
    parser = argparse.ArgumentParser(description='微信小程序分包分析工具')
    parser.add_argument('project_dir', help='小程序项目根目录（包含 app.json）')
    parser.add_argument('--main-max', type=float, default=DEFAULT_MAIN_MAX,
                        help=f'主包大小上限（MB），默认 {DEFAULT_MAIN_MAX}')
    parser.add_argument('--pkg-max', type=float, default=DEFAULT_PKG_MAX,
                        help=f'单个分包大小上限（MB），默认 {DEFAULT_PKG_MAX}')
    parser.add_argument('--output', '-o', default=None,
                        help='输出报告文件路径（JSON），默认打印到 stdout')
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f'错误：目录不存在: {project_dir}', file=sys.stderr)
        sys.exit(1)

    # 找到小程序根目录（向上找 app.json）
    app_root = project_dir
    while app_root and not (app_root / 'app.json').exists():
        if app_root.parent == app_root:
            break
        app_root = app_root.parent

    if not (app_root / 'app.json').exists():
        print(f'错误：在 {project_dir} 及上级目录中未找到 app.json', file=sys.stderr)
        sys.exit(1)

    print(f'📁 小程序根目录: {app_root}')

    # 扫描所有文件
    all_files = scan_dir(app_root)
    total_raw = sum(all_files.values())
    total_est = sum(
        int(s * EXT_RATIO.get(Path(p).suffix.lower(), 0.60))
        for p, s in all_files.items()
    )

    print(f'📊 文件总数: {len(all_files)}')
    print(f'   原始大小: {bytes_to_mb(total_raw):.2f} MB')
    print(f'   预估压缩后: {bytes_to_mb(total_est):.2f} MB')
    print()

    # 分析 app.js 和 app.json 大小（固定在主包）
    fixed_main_size = 0
    for fn in ['app.js', 'app.json', 'app.wxss']:
        fp = app_root / fn
        if fp.exists():
            sz = fp.stat().st_size
            fixed_main_size += sz
            print(f'  [主包固定] {fn}: {bytes_to_mb(sz)*1024:.1f} KB')

    print()
    print(f'  主包固定部分合计: {bytes_to_mb(fixed_main_size)*1024:.1f} KB')
    print()

    # 提取 pages 目录下的所有页面
    pages_root = app_root / 'pages'
    subpackages_root = app_root / 'subpackages'
    page_modules: dict[str, dict[str, int]] = {}
    other_files: dict[str, int] = {}

    for rel, size in all_files.items():
        parts = Path(rel).parts
        if len(parts) >= 2 and parts[0] == 'pages':
            page_group = parts[1]
            page_modules.setdefault(page_group, {})[rel] = size
        elif str(rel).startswith('subpackages'):
            # 分包已有结构，放 other
            other_files[rel] = size
        else:
            other_files[rel] = size

    pkg_max_bytes = int(args.pkg_max * 1024 * 1024)
    main_max_bytes = int(args.main_max * 1024 * 1024)

    # 贪心分配
    main_pages = {}
    subpackage_groups: list[dict[str, int]] = []
    current_sub = {}

    # 先排序列出页面
    sorted_groups = sorted(page_modules.items(), key=lambda x: -sum(x[1].values()))

    available_main = main_max_bytes - fixed_main_size
    current_main_size = 0

    for page_name, files in sorted_groups:
        page_raw = sum(files.values())
        page_est = sum(int(s * 0.5) for s in files.values())

        if current_main_size + page_est <= available_main * 0.85:
            main_pages.update(files)
            current_main_size += page_est
        else:
            # 检查是否需要新开一个分包
            sub_est = sum(int(s * 0.5) for s in files.values())
            current_sub_est = sum(int(s * 0.5) for s in current_sub.values())

            if current_sub_est + sub_est <= pkg_max_bytes:
                current_sub.update(files)
            else:
                if current_sub:
                    subpackage_groups.append(current_sub)
                current_sub = dict(files)

    if current_sub:
        subpackage_groups.append(current_sub)

    # 输出报告
    print('=' * 60)
    print('📦 分包方案')
    print('=' * 60)

    # 主包
    main_total = fixed_main_size + sum(main_pages.values())
    main_est   = int(main_total * 0.50)
    status_icon = '✅' if main_est <= main_max_bytes else '❌'
    print(f'\n🏠 主包（{status_icon}）')
    print(f'   原始大小: {bytes_to_mb(main_total):.2f} MB')
    print(f'   预估压缩后: {bytes_to_mb(main_est):.2f} MB / {args.main_max} MB')
    print(f'   包含页面: {len(main_pages)} 个文件')
    if main_est > main_max_bytes:
        print('   ⚠️ 主包超过限制！需将更多页面移至分包')

    # 分包
    pkg_configs = []
    for idx, group in enumerate(subpackage_groups):
        pkg_raw = sum(group.values())
        pkg_est = int(pkg_raw * 0.5)
        pkg_root = f'subpackages/pkg{idx}'
        status_icon = '✅' if pkg_est <= main_max_bytes else '❌'
        print(f'\n📦 分包 {idx + 1} - {pkg_root}（{status_icon}）')
        print(f'   原始大小: {bytes_to_mb(pkg_raw):.2f} MB')
        print(f'   预估压缩后: {bytes_to_mb(pkg_est):.2f} MB / {args.pkg_max} MB')
        print(f'   页面目录: {sorted(set(Path(f).parts[1] for f in group.keys() if len(Path(f).parts) >= 2))}')

        pages_list = []
        for rel in sorted(group.keys()):
            p = Path(rel)
            if len(p.parts) >= 3 and p.parts[0] == 'pages':
                page_path = '/'.join(p.parts[1:]).rsplit('.', 1)[0]
                pages_list.append(page_path)

        pkg_configs.append({
            'root': pkg_root,
            'pages': sorted(set(pages_list))
        })

    # 统计
    total_est = main_est + sum(int(sum(g.values()) * 0.5) for g in subpackage_groups)
    print()
    print('=' * 60)
    print(f'📈 汇总')
    print(f'   主包: {bytes_to_mb(main_est):.2f} MB')
    for idx, g in enumerate(subpackage_groups):
        print(f'   分包{idx+1}: {bytes_to_mb(int(sum(g.values())*0.5)):.2f} MB')
    print(f'   合计: {bytes_to_mb(total_est):.2f} MB')

    # 生成 app.json 片段
    print()
    print('=' * 60)
    print('📝 app.json subpackages 配置片段:')
    print('=' * 60)
    config = {
        'main_pages': [f"pages/{Path(f).parts[1]}/{'/'.join(Path(f).parts[2:]).rsplit('.',1)[0]}"
                       for f in sorted(main_pages.keys())],
        'subpackages': pkg_configs
    }
    print(json.dumps(config, ensure_ascii=False, indent=2))

    if args.output:
        report = {
            'project': str(app_root),
            'summary': {
                'total_raw_mb': round(bytes_to_mb(total_raw), 2),
                'total_est_mb': round(bytes_to_mb(total_est), 2),
                'main_est_mb': round(bytes_to_mb(main_est), 2),
                'package_count': len(subpackage_groups),
            },
            'main_package': {
                'files': list(main_pages.keys()),
                'raw_bytes': main_total,
                'est_bytes': main_est,
            },
            'subpackages': [
                {
                    'root': pkg['root'],
                    'pages': pkg['pages'],
                    'raw_bytes': sum(subpackage_groups[i].values()),
                    'est_bytes': int(sum(subpackage_groups[i].values()) * 0.5),
                }
                for i, pkg in enumerate(pkg_configs)
            ]
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f'\n报告已保存至: {args.output}')


if __name__ == '__main__':
    main()
