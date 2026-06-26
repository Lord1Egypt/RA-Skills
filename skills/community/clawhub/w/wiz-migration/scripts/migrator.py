#!/usr/bin/env python3
"""
为知笔记附件迁移模块
"""

import os
import shutil
from pathlib import Path
from typing import Dict


def run_attachment_migration(source_dir, target_dir, script_path=None):
    """
    运行附件迁移
    
    Args:
        source_dir: 源数据目录（包含 _Attachments）
        target_dir: 目标目录
        script_path: 可选的批处理脚本路径
        
    Returns:
        dict: 迁移结果统计
    """
    source = Path(source_dir).resolve()
    target = Path(target_dir).resolve()
    
    if not source.exists():
        raise FileNotFoundError(f"源目录不存在: {source}")
    
    # 创建目标根目录
    target.mkdir(parents=True, exist_ok=True)
    
    stats = {
        "copied": 0,
        "skipped": 0,
        "failed": 0,
        "total_size": 0
    }
    
    print(f"正在扫描附件目录...")
    
    # 方法1: 使用批处理脚本（Windows）
    if script_path and os.name == 'nt' and Path(script_path).exists():
        return _run_batch_script(script_path, source_dir, target_dir)
    
    # 方法2: Python 实现跨平台版本
    return _copy_attachments_python(source, target, stats)


def _run_batch_script(script_path, source_dir, target_dir):
    """
    运行 Windows 批处理脚本
    
    注意：这会启动一个新进程，不是在 Python 中复制
    """
    import subprocess
    
    # 修改脚本中的路径
    script_content = Path(script_path).read_text(encoding='utf-8')
    
    # 替换路径
    script_content = script_content.replace(
        'set "SOURCE_DIR=C:\\Users\\Administrator\\Documents\\My Knowledge"',
        f'set "SOURCE_DIR={source_dir}"'
    )
    script_content = script_content.replace(
        'set "TARGET_DIR=G:\\Data\\knowledge\\wiz"',
        f'set "TARGET_DIR={target_dir}"'
    )
    
    # 写入临时脚本
    temp_script = Path("temp_copy_attachments.bat")
    temp_script.write_text(script_content, encoding='utf-8')
    
    try:
        print("正在运行批处理脚本...")
        result = subprocess.run(
            [str(temp_script)],
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"错误输出: {result.stderr}")
        
        # 解析结果（批处理脚本里的统计比较困难，简单返回）
        return {
            "copied": 0,  # 无法精确获取
            "skipped": 0,
            "failed": 0,
            "via_batch": True
        }
    finally:
        if temp_script.exists():
            temp_script.unlink()


def _copy_attachments_python(source: Path, target: Path, stats: Dict):
    """
    Python 实现附件复制
    
    查找并复制所有 _Attachments 目录
    """
    print(f"源目录: {source}")
    print(f"目标目录: {target}")
    print()
    
    # 查找所有 _Attachments 目录
    attachments_dirs = []
    
    # 递归查找
    for root, dirs, files in os.walk(source):
        for d in dirs:
            if d == "_Attachments" or d.endswith("_files"):
                attachments_dirs.append(Path(root) / d)
    
    if not attachments_dirs:
        print("⚠️  未找到 _Attachments 或 _files 目录")
        print("请确认:")
        print("  1. 源目录是否正确")
        print("  2. 是否为导出的 Wiz 数据")
        return stats
    
    print(f"找到 {len(attachments_dirs)} 个附件目录\n")
    
    total = len(attachments_dirs)
    
    for idx, attach_dir in enumerate(attachments_dirs, 1):
        try:
            # 计算相对路径
            rel_path = attach_dir.relative_to(source)
            dest_path = target / rel_path
            
            print(f"[{idx}/{total}] 处理: {rel_path}")
            
            if dest_path.exists():
                # 已存在，统计文件数量
                existing_files = list(dest_path.rglob("*"))
                existing_file_count = sum(1 for f in existing_files if f.is_file())
                print(f"  ⏭️  已存在，跳过 ({existing_file_count} 个文件)")
                stats["skipped"] += existing_file_count
                continue
            
            # 复制目录
            shutil.copytree(attach_dir, dest_path)
            
            # 统计文件数量
            copied_files = list(dest_path.rglob("*"))
            file_count = sum(1 for f in copied_files if f.is_file())
            
            stats["copied"] += file_count
            print(f"  ✅ 复制完成 ({file_count} 个文件)")
            
        except Exception as e:
            print(f"  ❌ 复制失败: {e}")
            stats["failed"] += 1
    
    print()
    print("=" * 60)
    print("统计结果:")
    print(f"  处理目录数: {total}")
    print(f"  ✅ 新复制文件: {stats['copied']}")
    print(f"  ⏭️  已存在跳过: {stats['skipped']}")
    print(f"  ❌ 失败目录: {stats['failed']}")
    print("=" * 60)
    
    return stats


def find_attachments(source_dir):
    """
    查找所有附件目录（供外部调用）
    
    Returns:
        list: 附件目录路径列表
    """
    source = Path(source_dir)
    attachments = []
    
    for root, dirs, files in os.walk(source):
        for d in dirs:
            if d == "_Attachments" or d.endswith("_files"):
                attachments.append(Path(root) / d)
    
    return attachments


def copy_attachments_batch(source_dir, target_dir):
    """
    批量复制附件（简化接口）
    
    Returns:
        dict: 统计信息
    """
    stats = {"copied": 0, "skipped": 0, "failed": 0}
    return run_attachment_migration(source_dir, target_dir, stats)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]
        result = run_attachment_migration(source, target)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("使用方法:")
        print("  python migrator.py <源目录> <目标目录>")
        print("\n示例:")
        print('  python migrator.py "C:\\Users\\Admin\\Documents\\My Knowledge" "G:\\Data\\wiz"')
