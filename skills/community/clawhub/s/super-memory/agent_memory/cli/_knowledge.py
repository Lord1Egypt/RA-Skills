"""Knowledge management: entities, topic-summaries, encyclopedia, doc, distill, distill-stats."""

from __future__ import annotations

import json
import os
from argparse import Namespace

from agent_memory.cli._utils import (
    get_memory,
    _HAS_DOCUMENT_PARSER,
    _HAS_SEMANTIC_CHUNKER,
    _HAS_CHUNK_INDEXER,
    _HAS_CHUNK_RETRIEVER,
)

try:
    from agent_memory.cli._utils import DocumentParser
except ImportError:
    DocumentParser = None

try:
    from agent_memory.cli._utils import SemanticChunker
except ImportError:
    SemanticChunker = None

try:
    from agent_memory.cli._utils import ChunkIndexer
except ImportError:
    ChunkIndexer = None

try:
    from agent_memory.cli._utils import ChunkRetriever
except ImportError:
    ChunkRetriever = None


def cmd_entities(args):
    """查看知识实体"""
    mem = get_memory()
    entities = mem.distiller.get_entities(
        entity_type=args.type,
        name_like=args.name,
    )
    if not entities:
        print("📭 暂无知识实体")
    else:
        output = []
        for e in entities:
            attrs = json.loads(e.get("attributes", "{}"))
            output.append({
                "id": e["entity_id"],
                "name": e["name"],
                "type": e["entity_type"],
                "importance": e.get("importance", "medium"),
                "attributes": attrs,
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_topic_summaries(args):
    """查看主题摘要"""
    mem = get_memory()
    summaries = mem.distiller.get_topic_summaries(topic_code=args.topic)
    if not summaries:
        print("📭 暂无主题摘要")
    else:
        output = []
        for s in summaries:
            output.append({
                "id": s["topic_id"],
                "topic": s["topic_code"],
                "summary": s["summary"][:500],
                "source_count": s.get("source_count", 0),
                "importance": s.get("importance", "medium"),
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


# ── 百科全书命令 ──────────────────────────────────────────


def cmd_encyclopedia(args):
    """查看/搜索/导出个人百科"""
    mem = get_memory()

    if args.export:
        path = mem.export_encyclopedia(args.export)
        print(json.dumps({"exported": path}, ensure_ascii=False, indent=2))
    elif args.search:
        results = mem.search_encyclopedia(args.search)
        if not results:
            print("📭 百科全书为空 — 使用 remember 积累知识")
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        entries = mem.get_encyclopedia(category=args.category)
        if not entries:
            print("📭 百科全书为空 — 使用 remember 积累知识")
        else:
            output = []
            for e in entries:
                output.append({
                    "id": e["entry_id"],
                    "title": e["title"],
                    "category": e["category"],
                    "preview": e["content"][:300],
                })
            print(json.dumps(output, ensure_ascii=False, indent=2))

    mem.close()


# ── 文档精读命令 ──────────────────────────────────────────


def cmd_doc(args):
    """文档精读命令"""
    subcmd = args.doc_subcmd

    if subcmd == "upload":
        _cmd_doc_upload(args)
    elif subcmd == "search":
        _cmd_doc_search(args)
    elif subcmd == "list":
        _cmd_doc_list(args)
    elif subcmd == "locate":
        _cmd_doc_locate(args)
    else:
        print("用法: agent-memory doc <upload|search|list|locate> [参数]")


def _cmd_doc_upload(args):
    """上传文档并自动分段索引"""
    if not _HAS_DOCUMENT_PARSER or not _HAS_SEMANTIC_CHUNKER or not _HAS_CHUNK_INDEXER:
        print(json.dumps({"error": "文档精读模块未安装 (document_parser / semantic_chunker / chunk_indexer)"}, ensure_ascii=False))
        return

    file_path = args.file_path
    if not os.path.exists(file_path):
        print(json.dumps({"error": f"文件不存在: {file_path}"}, ensure_ascii=False))
        return

    mem = get_memory()
    try:
        doc_parser = DocumentParser()
        chunker = SemanticChunker()
        indexer = ChunkIndexer(
            store=mem.store,
            encoder=mem.encoder,
            embedding_store=getattr(mem, 'embedding_store', None),
        )

        parsed = doc_parser.parse(file_path)
        doc_title = args.title or parsed.title or os.path.basename(file_path)

        chunk_result = chunker.chunk_document(
            parsed.sections,
            "pending",
            strategy=args.strategy,
        )

        index_result = indexer.index_document(
            chunk_result,
            title=doc_title,
            source_path=file_path,
            source_type=parsed.source_type,
            importance=args.importance,
        )

        output = {
            "doc_id": index_result.doc_id,
            "title": doc_title,
            "source_type": parsed.source_type,
            "total_sections": len(parsed.sections),
            "total_chunks": index_result.total_chunks,
            "indexed_chunks": index_result.indexed_chunks,
            "failed_chunks": index_result.failed_chunks,
            "strategy_used": chunk_result.strategy_used,
        }
        if index_result.errors:
            output["errors"] = index_result.errors[:5]
        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_doc_search(args):
    """检索文档分段"""
    if not _HAS_CHUNK_RETRIEVER:
        print(json.dumps({"error": "文档检索模块未安装 (chunk_retriever)"}, ensure_ascii=False))
        return

    mem = get_memory()
    try:
        retriever = ChunkRetriever(
            store=mem.store,
            embedding_store=getattr(mem, 'embedding_store', None),
        )

        result = retriever.search(
            query=args.query,
            top_k=args.top_k,
            expand_context=args.expand_context,
            doc_id=args.doc_id,
            strategy=args.strategy,
        )

        output = {
            "query": result.query,
            "total_hits": result.total_hits,
            "strategy": result.strategy,
            "context_expanded": result.context_expanded,
            "hits": [
                {
                    "memory_id": h.memory_id,
                    "chunk_id": h.chunk_id,
                    "doc_id": h.doc_id,
                    "chapter": h.chapter,
                    "section": h.section,
                    "page_num": h.page_num,
                    "position": h.position,
                    "content": h.content[:300],
                    "score": round(h.score, 4),
                }
                for h in result.hits
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_doc_list(args):
    """列出文档和分段"""
    if not _HAS_CHUNK_RETRIEVER:
        print(json.dumps({"error": "文档检索模块未安装 (chunk_retriever)"}, ensure_ascii=False))
        return

    mem = get_memory()
    try:
        retriever = ChunkRetriever(store=mem.store)

        if args.doc_id:
            doc_meta = retriever._get_document_meta(args.doc_id)
            if not doc_meta:
                print(f"❌ 文档不存在: {args.doc_id} — 使用 doc list 查看所有文档")
                return

            chunks = retriever.get_document_chunks(args.doc_id)
            output = {
                "doc_id": args.doc_id,
                "title": doc_meta.get("title", ""),
                "source_type": doc_meta.get("source_type", ""),
                "total_chunks": doc_meta.get("total_chunks", 0),
                "total_chars": doc_meta.get("total_chars", 0),
                "chunks": [
                    {
                        "chunk_id": c.chunk_id,
                        "memory_id": c.memory_id,
                        "chapter": c.chapter,
                        "section": c.section,
                        "page_num": c.page_num,
                        "position": c.position,
                        "content_preview": c.content[:200],
                    }
                    for c in chunks
                ],
            }
        else:
            rows = mem.store.conn.execute(
                "SELECT doc_id, title, source_type, total_chunks, total_chars, created_at FROM document_meta ORDER BY created_at DESC"
            ).fetchall()
            output = {
                "total": len(rows),
                "documents": [
                    {
                        "doc_id": r["doc_id"],
                        "title": r["title"],
                        "source_type": r["source_type"],
                        "total_chunks": r["total_chunks"],
                        "total_chars": r["total_chars"],
                        "created_at": r["created_at"],
                    }
                    for r in rows
                ],
            }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_doc_locate(args):
    """精准回溯到原文位置"""
    if not _HAS_CHUNK_RETRIEVER:
        print(json.dumps({"error": "文档检索模块未安装 (chunk_retriever)"}, ensure_ascii=False))
        return

    mem = get_memory()
    try:
        retriever = ChunkRetriever(store=mem.store)

        location = retriever.locate_source(args.memory_id)

        if not location.get("found"):
            print(f"❌ 记忆 {args.memory_id} 未关联文档 — 使用 doc upload 上传文档")
            return

        doc_meta = location.get("document", {})
        print(f"📄 文档: {doc_meta.get('title', 'N/A')} ({location.get('doc_id', '')})")
        print(f"   章节: {location.get('chapter', '') or '无'}")
        print(f"   小节: {location.get('section', '') or '无'}")
        print(f"   页码: {location.get('page_num', 0)}")
        print(f"   位置: 第 {location.get('position', 0)} 段")
        print(f"   字符偏移: {location.get('char_offset', 0)}-{location.get('char_offset', 0) + location.get('char_length', 0)}")

        if not args.json:
            mem_data = mem.store.get_memory(args.memory_id)
            if mem_data:
                content = mem_data.get("content", "")
                print(f"\n📝 原文片段:")
                print(f"   {content[:200]}{'...' if len(content) > 200 else ''}")
        else:
            print(json.dumps(location, ensure_ascii=False, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


# ── 蒸馏命令 ──────────────────────────────────────────────


def cmd_distill(args):
    """执行记忆蒸馏"""
    mem = get_memory()
    result = mem.distill(force=args.force)
    if isinstance(result, dict) and result.get("error"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        distilled_count = result.get("distilled_count", result.get("new_entries", 0))
        if distilled_count:
            print(f"✅ 蒸馏完成：生成了 {distilled_count} 条知识")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


def cmd_distill_stats(args):
    """查看蒸馏系统统计"""
    mem = get_memory()
    stats = mem.get_distill_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    mem.close()
