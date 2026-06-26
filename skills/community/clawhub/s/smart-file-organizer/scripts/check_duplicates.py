#!/usr/bin/env python3
"""
重复文件检查工具
使用 MD5 算法检测目录中的重复文件
"""

import os
import hashlib
import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def calculate_md5(filepath, chunk_size=8192):
    """计算文件的 MD5 哈希值"""
    md5 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    except (OSError, IOError) as e:
        print(f"警告: 无法读取文件 {filepath}: {e}", file=sys.stderr)
        return None


def find_duplicates(target_dir):
    """查找目标目录中的重复文件"""
    target_path = Path(target_dir)

    if not target_path.exists():
        return {"error": f"目录不存在: {target_dir}"}

    if not target_path.is_dir():
        return {"error": f"路径不是目录: {target_dir}"}

    # MD5 -> 文件列表映射
    md5_map = defaultdict(list)

    # 遍历所有文件
    for root, dirs, files in os.walk(target_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            # 跳过隐藏文件
            if filename.startswith('.'):
                continue

            filepath = Path(root) / filename

            # 只处理文件，跳过符号链接
            if filepath.is_file() and not filepath.is_symlink():
                md5 = calculate_md5(filepath)
                if md5:
                    # 计算相对路径
                    rel_path = filepath.relative_to(target_path)
                    # 获取文件修改时间
                    mtime = os.path.getmtime(filepath)
                    md5_map[md5].append({
                        "path": str(rel_path),
                        "mtime": mtime,
                        "size": filepath.stat().st_size
                    })

    # 筛选出重复文件
    duplicates = {
        md5: files
        for md5, files in md5_map.items()
        if len(files) > 1
    }

    return {
        "total_files": sum(len(files) for files in md5_map.values()),
        "unique_files": len(md5_map),
        "duplicate_groups": len(duplicates),
        "duplicates": duplicates
    }


def format_report(data, target_dir):
    """格式化报告为易读文本"""
    if "error" in data:
        return f"❌ 错误: {data['error']}"

    lines = []
    lines.append("🔍 重复文件检查报告")
    lines.append("=" * 60)
    lines.append(f"📂 目标目录: {target_dir}")
    lines.append(f"📄 总文件数: {data['total_files']}")
    lines.append(f"✅ 唯一文件: {data['unique_files']}")
    lines.append(f"🔄 重复组数: {data['duplicate_groups']}")
    lines.append("")

    if data['duplicate_groups'] == 0:
        lines.append("✨ 未发现重复文件！")
        return "\n".join(lines)

    lines.append("⚠️  发现以下重复文件：")
    lines.append("")

    for md5, files in data['duplicates'].items():
        lines.append(f"MD5: {md5[:16]}...")
        lines.append(f"  大小: {files[0]['size']:,} 字节")

        # 按修改时间排序（最早的在前）
        sorted_files = sorted(files, key=lambda x: x['mtime'])

        for i, file_info in enumerate(sorted_files):
            mtime_str = datetime.fromtimestamp(file_info['mtime']).strftime('%Y-%m-%d %H:%M:%S')
            prefix = "  ✅ 保留" if i == 0 else "  🗑️  重复"
            lines.append(f"{prefix}: {file_info['path']}")
            lines.append(f"       时间: {mtime_str}")

        lines.append("")

    return "\n".join(lines)


def delete_duplicates(data, target_dir, dry_run=False):
    """删除重复文件（保留每组最早创建的文件）"""
    if "error" in data or data['duplicate_groups'] == 0:
        return {"deleted": 0, "freed_space": 0}

    deleted_count = 0
    freed_space = 0

    for md5, files in data['duplicates'].items():
        # 按修改时间排序（最早的在前）
        sorted_files = sorted(files, key=lambda x: x['mtime'])

        # 删除除第一个外的所有文件
        for file_info in sorted_files[1:]:
            filepath = Path(target_dir) / file_info['path']

            if not dry_run:
                try:
                    filepath.unlink()
                    deleted_count += 1
                    freed_space += file_info['size']
                except OSError as e:
                    print(f"警告: 无法删除 {filepath}: {e}", file=sys.stderr)
            else:
                deleted_count += 1
                freed_space += file_info['size']

    return {
        "deleted": deleted_count,
        "freed_space": freed_space
    }


def main():
    if len(sys.argv) < 2:
        print("用法: check_duplicates.py <目标目录> [--json] [--delete] [--dry-run]", file=sys.stderr)
        sys.exit(1)

    target_dir = sys.argv[1]
    output_json = "--json" in sys.argv
    delete_mode = "--delete" in sys.argv
    dry_run = "--dry-run" in sys.argv

    # 查找重复文件
    result = find_duplicates(target_dir)

    # 输出结果
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result, target_dir))

    # 删除模式
    if delete_mode or dry_run:
        delete_result = delete_duplicates(result, target_dir, dry_run=dry_run)

        if not output_json:
            mode = "模拟删除" if dry_run else "已删除"
            print(f"\n🗑️  {mode_result}:")
            print(f"  文件数: {delete_result['deleted']}")
            print(f"  释放空间: {delete_result['freed_space']:,} 字节")
        else:
            print(json.dumps(delete_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
