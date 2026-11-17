"""
Domain-Knowledge Toolkit CLI
命令行入口：query / stats / extract
整合检索引擎（阶段三）
"""

import argparse
import sys
import json
from pathlib import Path

# 添加项目根目录到 path
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from storage.knowledge_store import KnowledgeStore
from retrieval.index_manager import IndexManager
from retrieval.query_engine import QueryEngine
from retrieval.formatter import ResultFormatter
from extractors.doc_extractor import DocExtractor
from extractors.code_extractor import CodeExtractor
from extractors.table_extractor import TableExtractor
from extractors.manual_extractor import ManualExtractor
from utils.id_generator import generate_entity_id, generate_relation_id


def cmd_query(args):
    """查询领域知识（使用查询引擎）"""
    engine = QueryEngine(str(SKILL_DIR))
    formatter = ResultFormatter()

    results = engine.query(
        input_text=args.input,
        top_k=args.top_k,
        entity_type_filter=args.type if hasattr(args, 'type') and args.type else None,
        tag_filter=args.tag.split(',') if hasattr(args, 'tag') and args.tag else None
    )

    output = formatter.format_results(results, query_text=args.input)
    print(output)


def cmd_stats(args):
    """知识库统计"""
    store = KnowledgeStore(str(SKILL_DIR / "storage"))
    index = IndexManager(str(SKILL_DIR / "storage"))
    formatter = ResultFormatter()

    store_stats = store.get_stats()
    index_stats = index.get_stats()

    output = formatter.format_stats(store_stats, index_stats)
    print(output)


def cmd_extract(args):
    """从文档提取知识"""
    file_path = args.file
    extract_type = args.type

    # 选择提取器
    extractor_map = {
        'doc': DocExtractor,
        'code': CodeExtractor,
        'table': TableExtractor,
        'manual': ManualExtractor
    }

    extractor_cls = extractor_map.get(extract_type)
    if not extractor_cls:
        print(f"不支持的提取类型: {extract_type}")
        return

    extractor = extractor_cls()

    if extract_type == 'manual':
        # 手动录入模式
        results = extractor.extract(file_path)
    else:
        results = extractor.extract(file_path)

    if not results:
        print(f"未从 {file_path} 提取到任何实体。")
        return

    # 写入知识库
    store = KnowledgeStore(str(SKILL_DIR / "storage"))
    added_count = 0

    for r in results:
        entity_type = r['entity_type']
        entity = r['entity']
        provenance = r['provenance']
        tags = r['tags']

        # 生成幂等 ID
        entity_id = generate_entity_id(entity_type, entity, provenance.get('source_path', ''))
        added = store.add_entity(entity_id, entity_type, entity, provenance, tags)
        if added:
            added_count += 1
            print(f"  + [{entity_type}] {entity.get('name', entity.get('model', entity.get('title', '?')))}")
            print(f"    ID: {entity_id[:16]}...")
        else:
            print(f"  = [{entity_type}] 已存在，跳过")

    print(f"\n提取完成: {len(results)} 个实体，新增 {added_count} 个")


def cmd_ingest(args):
    """批量导入（提取 + 写入 + 重建索引）"""
    file_path = args.file
    extract_type = args.type

    # 提取
    extractor_map = {
        'doc': DocExtractor,
        'code': CodeExtractor,
        'table': TableExtractor
    }
    extractor_cls = extractor_map.get(extract_type)
    if not extractor_cls:
        print(f"不支持的提取类型: {extract_type}")
        return

    extractor = extractor_cls()
    results = extractor.extract(file_path)

    if not results:
        print(f"未从 {file_path} 提取到任何实体。")
        return

    # 写入
    store = KnowledgeStore(str(SKILL_DIR / "storage"))
    added = 0
    for r in results:
        entity_id = generate_entity_id(r['entity_type'], r['entity'],
                                        r['provenance'].get('source_path', ''))
        if store.add_entity(entity_id, r['entity_type'], r['entity'], r['provenance'], r['tags']):
            added += 1

    print(f"导入完成: {added}/{len(results)} 个新实体")
    print("索引将在下次查询时自动重建。")


def main():
    parser = argparse.ArgumentParser(description="Domain-Knowledge Toolkit")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # query 命令
    query_parser = subparsers.add_parser('query', help='查询领域知识')
    query_parser.add_argument('input', type=str, help='用户输入的任务描述')
    query_parser.add_argument('--top-k', type=int, default=10, help='返回最大知识条数')
    query_parser.add_argument('--type', type=str, default=None, help='实体类型过滤')
    query_parser.add_argument('--tag', type=str, default=None, help='标签过滤 (逗号分隔)')

    # stats 命令
    subparsers.add_parser('stats', help='知识库统计')

    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='从文档提取知识')
    extract_parser.add_argument('--file', type=str, required=True, help='源文件路径')
    extract_parser.add_argument('--type', type=str,
                                choices=['doc', 'code', 'table', 'manual'],
                                required=True, help='提取器类型')

    # ingest 命令
    ingest_parser = subparsers.add_parser('ingest', help='批量导入知识')
    ingest_parser.add_argument('--file', type=str, required=True, help='源文件路径')
    ingest_parser.add_argument('--type', type=str,
                                choices=['doc', 'code', 'table'],
                                required=True, help='提取器类型')

    args = parser.parse_args()

    if args.command == 'query':
        cmd_query(args)
    elif args.command == 'stats':
        cmd_stats(args)
    elif args.command == 'extract':
        cmd_extract(args)
    elif args.command == 'ingest':
        cmd_ingest(args)


if __name__ == "__main__":
    main()
