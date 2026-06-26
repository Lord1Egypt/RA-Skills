#!/usr/bin/env python3
"""
冷区盲化补丁 - 确保 archive_basement 不进入热区索引与查询主路
版本：v1.0
日期：2026-04-09
"""

import json
from pathlib import Path

ROOT = Path('/Users/zhouyi0415126.com/ai_matrix/vault/01_core')


def is_cold_zone_path(path: str) -> bool:
    """判断路径是否属于冷区（archive_basement）"""
    return "archive_basement" in path


def filter_cold_zone_from_manifest(manifest_path: Path) -> None:
    """从 manifest 文件中过滤掉冷区路径"""
    if not manifest_path.exists():
        return
    
    filtered = []
    removed = []
    
    for line in manifest_path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        
        try:
            item = json.loads(line)
            if is_cold_zone_path(item.get('path', '')):
                removed.append(item['path'])
                continue
            filtered.append(line)
        except json.JSONDecodeError:
            continue
    
    if removed:
        # 创建备份
        backup_path = manifest_path.with_suffix('.jsonl.backup')
        manifest_path.rename(backup_path)
        
        # 写入过滤后的内容
        manifest_path.write_text('\n'.join(filtered) + '\n', encoding='utf-8')
        
        print(f"[COLD_ZONE_FILTER] 从 {manifest_path.name} 中移除了 {len(removed)} 个冷区文件")
        for path in removed[:5]:  # 只显示前5个
            print(f"  - {path}")
        if len(removed) > 5:
            print(f"  ... 还有 {len(removed) - 5} 个文件")
    else:
        print(f"[COLD_ZONE_FILTER] {manifest_path.name} 中未发现冷区文件")


def validate_index_vectors(index_path: Path) -> bool:
    """验证向量索引中是否包含冷区路径"""
    if not index_path.exists():
        return True
    
    cold_count = 0
    total_count = 0
    
    for line in index_path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        
        try:
            item = json.loads(line)
            total_count += 1
            if is_cold_zone_path(item.get('path', '')):
                cold_count += 1
        except json.JSONDecodeError:
            continue
    
    if cold_count > 0:
        print(f"[COLD_ZONE_VALIDATION] 警告：{index_path.name} 中包含 {cold_count}/{total_count} 个冷区文件")
        return False
    else:
        print(f"[COLD_ZONE_VALIDATION] 通过：{index_path.name} 中未发现冷区文件")
        return True


def patch_build_scripts():
    """为构建脚本生成补丁代码片段"""
    patches = {
        'build_index.py': '''
# === 冷区盲化补丁开始 ===
def should_index(path: str) -> bool:
    """判断路径是否应该被索引"""
    return "archive_basement" not in path

# 在读取 manifest 后添加过滤
filtered_items = []
for item in items:
    if should_index(item["path"]):
        filtered_items.append(item)
    else:
        print(f"跳过冷区文件: {item['path']}")
items = filtered_items
# === 冷区盲化补丁结束 ===
''',
        
        'build_index_bge.py': '''
# === 冷区盲化补丁开始 ===
def should_index(path: str) -> bool:
    """判断路径是否应该被索引"""
    return "archive_basement" not in path

# 在读取 manifest 后添加过滤
filtered_items = []
for item in items:
    if should_index(item["path"]):
        filtered_items.append(item)
    else:
        print(f"跳过冷区文件: {item['path']}")
items = filtered_items
# === 冷区盲化补丁结束 ===
''',
        
        'query_bge.py': '''
# === 冷区盲化补丁开始 ===
def is_cold_zone_path(path: str) -> bool:
    """判断路径是否属于冷区"""
    return "archive_basement" in path

# 在返回结果前添加过滤
rows = [r for r in rows if not is_cold_zone_path(r["path"])]
# === 冷区盲化补丁结束 ===
''',
        
        'graph_router.py': '''
# === 冷区盲化补丁开始 ===
def is_cold_zone_path(path: str) -> bool:
    """判断路径是否属于冷区"""
    return "archive_basement" in path

# 在构建图邻居时添加过滤
links = [l for l in links if not is_cold_zone_path(l)]
# === 冷区盲化补丁结束 ===
'''
    }
    
    return patches


def main():
    """主函数：执行冷区盲化检查与修复"""
    print("=" * 60)
    print("冷区盲化补丁检查 - Memory Palace v3.0")
    print("=" * 60)
    
    # 1. 检查并过滤 manifest 文件
    manifest_path = ROOT / 'memory/palace/watchdog/index/watchdog_manifest_v1_2026-04-08.jsonl'
    print(f"\n[1] 检查 manifest 文件: {manifest_path.name}")
    filter_cold_zone_from_manifest(manifest_path)
    
    # 2. 验证向量索引文件
    index_path = ROOT / 'memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl'
    print(f"\n[2] 验证向量索引文件: {index_path.name}")
    validate_index_vectors(index_path)
    
    # 3. 生成补丁代码
    print(f"\n[3] 生成脚本补丁代码")
    patches = patch_build_scripts()
    
    for script_name, patch_code in patches.items():
        script_path = ROOT / 'scripts/watchdog' / script_name
        if script_path.exists():
            print(f"  - {script_name}: 需要添加 {len(patch_code.splitlines())} 行补丁代码")
        else:
            print(f"  - {script_name}: 文件不存在")
    
    # 4. 输出补丁应用指南
    print(f"\n[4] 补丁应用指南")
    print("=" * 40)
    print("手动应用步骤：")
    print("1. 备份原始脚本文件")
    print("2. 根据上面的补丁代码，在相应位置添加过滤逻辑")
    print("3. 重新构建索引：python scripts/watchdog/build_index_bge.py")
    print("4. 验证查询结果：python scripts/watchdog/query_bge.py '测试查询'")
    print("\n自动应用（未来版本）：")
    print("将 cold_zone_blinding_patch.py 集成到构建流程中")
    
    print(f"\n[COLD_ZONE_PATCH_COMPLETE] 冷区盲化补丁检查完成")


if __name__ == '__main__':
    main()