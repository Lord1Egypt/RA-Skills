#!/usr/bin/env python3
"""
warmup.py - 缓存预热脚本

功能：
- 启动时预热常用查询的 embedding 缓存
- 减少首次查询延迟
- 支持定时预热

用法：
    python3 warmup.py              # 预热所有常用查询
    python3 warmup.py --dry-run   # 仅显示将要预热的查询
    python3 warmup.py --list      # 列出常用查询
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 常用查询列表 - 根据用户历史生成
COMMON_QUERIES = [
    # 基础查询
    "配置", "设置", "状态", "规则", "推送",
    "记忆", "用户", "系统", "决策",
    # 操作类
    "搜索", "查询", "查找", "添加", "删除",
    "修改", "编辑", "创建", "开启", "关闭",
    # 信息类
    "是什么", "如何", "怎么", "多少", "几个",
    "最近", "今天", "昨天", "记录", "日志",
    # 性能类
    "性能", "效率", "速度", "延迟", "内存",
    # 管理类
    "备份", "恢复", "导出", "导入", "同步",
    "版本", "更新", "升级", "安装",
    # 工具类
    "命令", "指令", "使用", "帮助",
]


def warmup_cache(dry_run: bool = False, verbose: bool = True) -> dict:
    """预热 embedding 缓存"""
    # 临时启用详细模式（warmup 需要看到进度）
    import memory
    memory._embedding_verbose = verbose
    
    from core.embedding import EmbeddingEngine
    from core.embedding_cache import get_embedding_cache
    
    # 初始化 embedding 引擎
    emb = EmbeddingEngine(
        api_url="https://ai.gitee.com/v1/embeddings",
        api_key="你的API_KEY",  # TODO: 从配置读取
        model="Qwen3-Embedding-8B"
    )
    cache = get_embedding_cache()
    
    stats = {
        "total": len(COMMON_QUERIES),
        "cached": 0,
        "already_cached": 0,
        "failed": 0,
        "total_time_ms": 0,
    }
    
    if dry_run:
        print("=== 预热计划（dry-run）===\n")
        for q in COMMON_QUERIES:
            print(f"  预热: {q}")
        print(f"\n共 {len(COMMON_QUERIES)} 个查询")
        return stats
    
    print("=== 开始预热缓存 ===\n")
    
    for q in COMMON_QUERIES:
        start = time.time()
        try:
            vec = emb.get(q)
            elapsed = (time.time() - start) * 1000
            stats["total_time_ms"] += elapsed
            
            if vec:
                stats["cached"] += 1
                print(f"  ✅ {q}: {elapsed:.1f}ms")
            else:
                stats["failed"] += 1
                print(f"  ❌ {q}: 失败")
        except Exception as e:
            stats["failed"] += 1
            print(f"  ❌ {q}: {e}")
    
    print(f"\n=== 预热完成 ===")
    print(f"总计: {stats['total']} 个查询")
    print(f"成功: {stats['cached']} 个")
    print(f"失败: {stats['failed']} 个")
    print(f"耗时: {stats['total_time_ms']:.1f}ms")
    print(f"\n缓存统计: {emb.get_cache_stats()}")
    
    return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="缓存预热脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅显示计划，不执行")
    parser.add_argument("--list", action="store_true", help="列出常用查询")
    
    args = parser.parse_args()
    
    if args.list:
        print("=== 常用查询列表 ===\n")
        for i, q in enumerate(COMMON_QUERIES, 1):
            print(f"  {i:2d}. {q}")
        print(f"\n共 {len(COMMON_QUERIES)} 个查询")
    else:
        warmup_cache(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
