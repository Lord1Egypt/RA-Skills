#!/usr/bin/env python3
"""
TurboQuant Memory Integration Script

Quantize embeddings in SQLite-based memory systems for compressed storage
and accelerated vector search.

Usage:
    python memory_quantize.py --db /path/to/memory.db --bits 4 --benchmark
    python memory_quantize.py --db /path/to/memory.db --bits 4 --migrate
"""

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

# Import from same directory
sys.path.insert(0, str(Path(__file__).parent))
from turboquant import TurboQuantProd, pack_indices, unpack_indices


def detect_vec0_tables(conn: sqlite3.Connection) -> dict:
    """Auto-detect OpenClaw vec0 tables."""
    # Look for tables using vec0 extension
    cursor = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND sql LIKE '%USING vec0%'
    """)
    
    vec0_tables = [row[0] for row in cursor.fetchall()]
    
    if not vec0_tables:
        return None
    
    # Use first vec0 table found
    table_name = vec0_tables[0]
    
    # Check if it has 'embedding' column and get dimension
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    cols = {row[1]: row[2] for row in cursor.fetchall()}
    
    if 'embedding' not in cols:
        return None
    
    # Detect dimension from first row
    cursor = conn.execute(f"SELECT embedding FROM {table_name} WHERE embedding IS NOT NULL LIMIT 1")
    row = cursor.fetchone()
    if row and row[0]:
        vec = np.frombuffer(row[0], dtype=np.float32)
        return {
            "table": table_name,
            "emb_col": "embedding", 
            "id_col": "rowid",  # vec0 tables use rowid
            "dim": len(vec),
            "is_vec0": True
        }
    
    return None


class OpenClawVecReader:
    """Efficient reader for OpenClaw vec0 embedding tables."""
    
    def __init__(self, conn: sqlite3.Connection, table_name: str, embedding_col: str = "embedding"):
        self.conn = conn
        self.table_name = table_name
        self.embedding_col = embedding_col
        
        # Detect dimension
        self.dim = self._detect_dimension()
        if self.dim is None:
            raise ValueError(f"Could not detect dimension from {table_name}.{embedding_col}")
    
    def _detect_dimension(self) -> int:
        """Detect embedding dimension from first row."""
        cursor = self.conn.execute(
            f"SELECT {self.embedding_col} FROM {self.table_name} "
            f"WHERE {self.embedding_col} IS NOT NULL LIMIT 1"
        )
        row = cursor.fetchone()
        if row and row[0]:
            vec = np.frombuffer(row[0], dtype=np.float32)
            return len(vec)
        return None
    
    def read_batch(self, offset: int = 0, limit: int = 1000) -> List[Dict]:
        """Read batch of embeddings with metadata."""
        cursor = self.conn.execute(
            f"SELECT rowid, {self.embedding_col} FROM {self.table_name} "
            f"WHERE {self.embedding_col} IS NOT NULL "
            f"LIMIT {limit} OFFSET {offset}"
        )
        
        batch = []
        for row in cursor:
            vec = np.frombuffer(row[1], dtype=np.float32)
            if len(vec) == self.dim:
                batch.append({
                    "id": str(row[0]),
                    "embedding": vec
                })
        
        return batch
    
    def count_embeddings(self) -> int:
        """Count total embeddings."""
        cursor = self.conn.execute(
            f"SELECT COUNT(*) FROM {self.table_name} "
            f"WHERE {self.embedding_col} IS NOT NULL"
        )
        return cursor.fetchone()[0]


def detect_embedding_schema(conn: sqlite3.Connection) -> dict:
    """Auto-detect embedding column and dimension from a SQLite database."""
    # Common table/column patterns for memory systems
    candidates = [
        ("memories", "embedding", "id", "text", "is_deleted = 0"),
        ("memories", "embedding", "id", "content", "1=1"),
        ("embeddings", "vector", "id", "text", "1=1"),
        ("documents", "embedding", "id", "content", "1=1"),
    ]
    
    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    
    for table, emb_col, id_col, text_col, where in candidates:
        if table not in tables:
            continue
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if emb_col not in cols:
            continue
        
        # Check if text column exists, fallback to first text-like column
        actual_text_col = text_col if text_col in cols else None
        if actual_text_col is None:
            for c in cols:
                if c not in (id_col, emb_col, 'hash', 'metadata', 'created_at', 'updated_at'):
                    actual_text_col = c
                    break
        
        # Detect dimension from first row
        row = conn.execute(
            f"SELECT {emb_col} FROM {table} WHERE {emb_col} IS NOT NULL AND {where} LIMIT 1"
        ).fetchone()
        if row and row[0]:
            vec = np.frombuffer(row[0], dtype=np.float32)
            return {
                "table": table, "emb_col": emb_col, "id_col": id_col,
                "text_col": actual_text_col, "where": where,
                "dim": len(vec)
            }
    
    return None


def load_embeddings(conn: sqlite3.Connection, schema: dict) -> list:
    """Load all embeddings from database."""
    text_select = f", {schema['text_col']}" if schema['text_col'] else ""
    query = (
        f"SELECT {schema['id_col']}, {schema['emb_col']}{text_select} "
        f"FROM {schema['table']} "
        f"WHERE {schema['emb_col']} IS NOT NULL AND {schema['where']}"
    )
    rows = conn.execute(query).fetchall()
    
    results = []
    for row in rows:
        vec = np.frombuffer(row[1], dtype=np.float32)
        text = row[2] if len(row) > 2 else ""
        results.append({"id": row[0], "embedding": vec, "text": str(text)[:200]})
    
    return results


def create_quantized_table(conn: sqlite3.Connection):
    """Create table for quantized embeddings with fp16 scales."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS quantized_embeddings (
            memory_id TEXT PRIMARY KEY,
            norm REAL NOT NULL,
            scale REAL NOT NULL,
            mse_indices BLOB NOT NULL,
            qjl_signs BLOB NOT NULL,
            residual_norm REAL NOT NULL,
            bits INTEGER NOT NULL,
            dim INTEGER NOT NULL,
            seed_rot INTEGER NOT NULL DEFAULT 42,
            seed_qjl INTEGER NOT NULL DEFAULT 137,
            sketch_dim INTEGER NOT NULL DEFAULT 256
        );
        CREATE INDEX IF NOT EXISTS idx_qe_memory_id ON quantized_embeddings(memory_id);
    """)


def migrate(db_path: str, bits: int = 4, seed_rot: int = 42, seed_qjl: int = 137, sketch_dim: int = 256):
    """Quantize all embeddings and store in quantized_embeddings table."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Try vec0 tables first, then fallback to generic detection
    schema = detect_vec0_tables(conn)
    if not schema:
        schema = detect_embedding_schema(conn)
    
    if not schema:
        print("❌ Could not detect embedding schema in database")
        conn.close()
        return False
    
    print(f"📋 Detected: table={schema['table']}, dim={schema['dim']}")
    if schema.get('is_vec0'):
        print("📋 Using vec0 table format")
    
    # Use batch processing for large datasets
    if schema.get('is_vec0'):
        reader = OpenClawVecReader(conn, schema['table'], schema['emb_col'])
        total_count = reader.count_embeddings()
        print(f"📦 Total embeddings: {total_count}")
        
        # Initialize quantizer
        quantizer = TurboQuantProd(dim=reader.dim, bits=bits, seed_rot=seed_rot, seed_qjl=seed_qjl, sketch_dim=sketch_dim)
        
        # Create table
        create_quantized_table(conn)
        
        # Process in batches
        batch_size = 1000
        mse_bits = bits - 1
        t0 = time.time()
        total_processed = 0
        
        for offset in range(0, total_count, batch_size):
            batch = reader.read_batch(offset, batch_size)
            if not batch:
                break
            
            for item in batch:
                qdata = quantizer.quantize(item['embedding'])
                packed_mse = pack_indices(qdata['mse_indices'], mse_bits)
                packed_qjl = pack_indices(qdata['qjl_signs'], 1)
                
                conn.execute(
                    "INSERT OR REPLACE INTO quantized_embeddings "
                    "(memory_id, norm, scale, mse_indices, qjl_signs, residual_norm, bits, dim, seed_rot, seed_qjl, sketch_dim) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (item['id'], qdata['norm'], qdata['scale'], packed_mse, packed_qjl,
                     qdata['residual_norm'], bits, reader.dim, seed_rot, seed_qjl, sketch_dim)
                )
                total_processed += 1
            
            if total_processed % 1000 == 0:
                print(f"  Quantized {total_processed}/{total_count}...")
                conn.commit()  # Commit periodically
        
        conn.commit()
        count = total_processed
        
        # Size comparison  
        original_size = total_count * reader.dim * 4  # float32
    
    else:
        # Legacy processing for non-vec0 tables
        data = load_embeddings(conn, schema)
        print(f"📦 Loaded {len(data)} embeddings")
        
        if not data:
            conn.close()
            return False
        
        # Initialize quantizer
        dim = schema['dim']
        quantizer = TurboQuantProd(dim=dim, bits=bits, seed_rot=seed_rot, seed_qjl=seed_qjl, sketch_dim=sketch_dim)
        mse_bits = bits - 1
        
        # Create table
        create_quantized_table(conn)
        
        # Quantize and store
        t0 = time.time()
        count = 0
        for item in data:
            qdata = quantizer.quantize(item['embedding'])
            packed_mse = pack_indices(qdata['mse_indices'], mse_bits)
            packed_qjl = pack_indices(qdata['qjl_signs'], 1)
            
            conn.execute(
                "INSERT OR REPLACE INTO quantized_embeddings "
                "(memory_id, norm, scale, mse_indices, qjl_signs, residual_norm, bits, dim, seed_rot, seed_qjl, sketch_dim) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (item['id'], qdata['norm'], qdata['scale'], packed_mse, packed_qjl,
                 qdata['residual_norm'], bits, dim, seed_rot, seed_qjl, sketch_dim)
            )
            count += 1
            if count % 100 == 0:
                print(f"  Quantized {count}/{len(data)}...")
        
        conn.commit()
        original_size = sum(len(item['embedding']) * 4 for item in data)
    
    elapsed = time.time() - t0
    
    compressed_size = conn.execute(
        "SELECT SUM(LENGTH(mse_indices) + LENGTH(qjl_signs) + 20) FROM quantized_embeddings"
    ).fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Migration complete!")
    print(f"   Vectors: {count}")
    print(f"   Time: {elapsed:.1f}s ({elapsed/count*1000:.0f}ms/vec)")
    print(f"   Original: {original_size/1024:.0f} KB")
    print(f"   Compressed: {compressed_size/1024:.0f} KB")
    print(f"   Ratio: {original_size/compressed_size:.1f}x")
    
    return True


def benchmark(db_path: str, bits: int = 4, n_queries: int = 30, sketch_dim: int = 256):
    """Benchmark quantized search accuracy against brute-force."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Try vec0 tables first
    schema = detect_vec0_tables(conn)
    if not schema:
        schema = detect_embedding_schema(conn)
    
    if not schema:
        print("❌ Could not detect embedding schema")
        conn.close()
        return
    
    # Load embeddings with size limit for benchmarking
    max_vectors = 5000  # Limit for performance
    
    if schema.get('is_vec0'):
        reader = OpenClawVecReader(conn, schema['table'], schema['emb_col'])
        total_count = reader.count_embeddings()
        limit = min(max_vectors, total_count)
        
        embeddings = []
        data = []
        for offset in range(0, limit, 1000):
            batch = reader.read_batch(offset, min(1000, limit - offset))
            for item in batch:
                embeddings.append(item['embedding'])
                data.append(item)
            if len(embeddings) >= limit:
                break
        
        dim = reader.dim
    else:
        data = load_embeddings(conn, schema)
        data = data[:max_vectors]  # Limit size
        embeddings = [d['embedding'] for d in data]
        dim = schema['dim']
    
    conn.close()
    
    print(f"📋 {len(data)} vectors, dim={dim}, bits={bits}")
    
    quantizer = TurboQuantProd(dim=dim, bits=bits, sketch_dim=sketch_dim)
    
    # Quantize all
    t0 = time.time()
    quantized_db = [quantizer.quantize(e) for e in embeddings]
    qt = time.time() - t0
    print(f"⏱️  Quantized in {qt:.1f}s")
    
    # Compression stats
    original_bytes = sum(len(e) * 4 for e in embeddings)
    compressed_bytes = 0
    for q in quantized_db:
        compressed_bytes += 12 + len(pack_indices(q['mse_indices'], bits-1)) + \
                           len(pack_indices(q['qjl_signs'], 1)) + 8  # norm + scale + residual_norm
    print(f"📦 Compression: {original_bytes/1024:.0f} KB → {compressed_bytes/1024:.0f} KB ({original_bytes/compressed_bytes:.1f}x)")
    
    # Search benchmark
    np.random.seed(42)
    n_queries = min(n_queries, len(data))
    test_indices = np.random.choice(len(data), n_queries, replace=False)
    
    recall_1 = recall_5 = recall_10 = 0
    t0 = time.time()
    
    for qi in test_indices:
        query = embeddings[qi]
        qnorm = np.linalg.norm(query)
        
        # True ranking by cosine similarity
        true_scores = []
        for i, e in enumerate(embeddings):
            if i == qi:
                continue
            cos = np.dot(query, e) / (qnorm * np.linalg.norm(e))
            true_scores.append((i, cos))
        true_scores.sort(key=lambda x: x[1], reverse=True)
        
        true_top1 = true_scores[0][0]
        true_top5 = set(s[0] for s in true_scores[:5])
        true_top10 = set(s[0] for s in true_scores[:10])
        
        # Quantized search
        results = quantizer.search(query, quantized_db, top_k=11)
        results = [(i, s) for i, s in results if i != qi][:10]
        
        est_top1 = results[0][0]
        est_top5 = set(r[0] for r in results[:5])
        est_top10 = set(r[0] for r in results)
        
        if est_top1 == true_top1:
            recall_1 += 1
        recall_5 += len(est_top5 & true_top5) / 5
        recall_10 += len(est_top10 & true_top10) / 10
    
    search_time = time.time() - t0
    
    print(f"\n🔍 Search Benchmark ({n_queries} queries)")
    print(f"   Time: {search_time:.1f}s ({search_time/n_queries*1000:.0f}ms/query)")
    print(f"   Top-1  Recall: {recall_1/n_queries:.0%}")
    print(f"   Top-5  Recall: {recall_5/n_queries:.0%}")
    print(f"   Top-10 Recall: {recall_10/n_queries:.0%}")
    
    # Example search
    qi = test_indices[0]
    print(f"\n📝 Example: \"{data[qi]['text'][:80]}\"")
    results = quantizer.search(embeddings[qi], quantized_db, top_k=4)
    results = [(i, s) for i, s in results if i != qi][:3]
    for rank, (i, score) in enumerate(results, 1):
        print(f"   {rank}. [{score:.4f}] \"{data[i]['text'][:80]}\"")


def main():
    parser = argparse.ArgumentParser(description="TurboQuant Memory Integration")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--bits", type=int, default=4, help="Bits per coordinate (default: 4)")
    parser.add_argument("--migrate", action="store_true", help="Quantize and store in new table")
    parser.add_argument("--benchmark", action="store_true", help="Run search accuracy benchmark")
    parser.add_argument("--queries", type=int, default=30, help="Number of benchmark queries")
    
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"❌ Database not found: {args.db}")
        sys.exit(1)
    
    if args.benchmark:
        benchmark(args.db, args.bits, args.queries)
    elif args.migrate:
        migrate(args.db, args.bits)
    else:
        print("Specify --benchmark or --migrate")
        parser.print_help()


if __name__ == "__main__":
    main()
