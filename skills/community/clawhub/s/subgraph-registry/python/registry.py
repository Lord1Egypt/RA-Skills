"""
Registry Builder

End-to-end pipeline:
1. Crawls the Graph Network subgraph
2. Classifies all subgraphs
3. Builds indices and summary stats
4. Outputs the agent-friendly JSON registry
5. Optionally writes to SQLite for fast lookups
"""

import asyncio
import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path

from crawler import full_crawl
from classifier import classify_all, Classification

try:
    # Optional at module-import time so test/import paths that don't
    # need embeddings (e.g. test.yml's smoke-import step) don't pay
    # the fastembed install cost during CI.
    import embedder  # type: ignore
except Exception:  # pragma: no cover
    embedder = None  # type: ignore

DATA_DIR = Path(__file__).parent / "data"
REGISTRY_FILE = DATA_DIR / "registry.json"
SYNC_STATE_FILE = DATA_DIR / "sync-state.json"
SQLITE_FILE = DATA_DIR / "registry.db"


def load_sync_state() -> dict:
    try:
        return json.loads(SYNC_STATE_FILE.read_text())
    except FileNotFoundError:
        return {"last_sync_timestamp": 0, "total_classified": 0}


def save_sync_state(state: dict):
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2))


def build_summary(classified: list[Classification]) -> dict:
    by_domain: dict[str, int] = {}
    by_network: dict[str, int] = {}
    by_protocol_type: dict[str, int] = {}
    families: dict[str, dict] = {}

    for sg in classified:
        by_domain[sg.domain] = by_domain.get(sg.domain, 0) + 1
        if sg.network:
            by_network[sg.network] = by_network.get(sg.network, 0) + 1
        by_protocol_type[sg.protocol_type] = by_protocol_type.get(sg.protocol_type, 0) + 1

        if sg.schema_family:
            fp = sg.schema_family["fingerprint"]
            if fp not in families:
                families[fp] = {
                    "fingerprint": fp,
                    "member_count": sg.schema_family["members"],
                    "representative_name": sg.display_name,
                    "domain": sg.domain,
                    "protocol_type": sg.protocol_type,
                }

    return {
        "total_subgraphs": len(classified),
        "by_domain": dict(sorted(by_domain.items(), key=lambda x: x[1], reverse=True)),
        "by_network": dict(sorted(by_network.items(), key=lambda x: x[1], reverse=True)),
        "by_protocol_type": dict(sorted(by_protocol_type.items(), key=lambda x: x[1], reverse=True)),
        "schema_family_count": len(families),
        "top_schema_families": sorted(families.values(), key=lambda x: x["member_count"], reverse=True)[:20],
    }


def build_indices(classified: list[Classification]) -> dict:
    by_domain: dict[str, list] = {}
    by_network: dict[str, list] = {}
    by_entity: dict[str, list] = {}

    for sg in classified:
        entry = {
            "id": sg.id,
            "name": sg.display_name,
            "network": sg.network,
            "protocol_type": sg.protocol_type,
            "reliability_score": sg.reliability_score,
            "ipfs_hash": sg.ipfs_hash,
        }

        by_domain.setdefault(sg.domain, []).append(entry)

        if sg.network:
            by_network.setdefault(sg.network, []).append({**entry, "domain": sg.domain})

        for ce in sg.canonical_entities:
            by_entity.setdefault(ce["canonical_type"], []).append({
                **entry,
                "entity_name": ce["name"],
                "domain": sg.domain,
            })

    # Sort all lists by reliability
    for lst in by_domain.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)
    for lst in by_network.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)
    for lst in by_entity.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)

    return {"by_domain": by_domain, "by_network": by_network, "by_entity": by_entity}


def write_sqlite(
    classified: list[Classification],
    db_path: Path = SQLITE_FILE,
    incremental: bool = False,
):
    """Write registry to SQLite for fast agent lookups.

    By default this rewrites the DB from scratch. When `incremental=True`,
    the existing DB is preserved and the classified rows are upserted —
    needed because incremental syncs only fetch the deltas, not the full
    corpus.
    """
    # Full rebuild: DROP the subgraphs table but preserve schema_history
    # so the time-series record of schema-fingerprint changes survives
    # across rebuilds. (Previously this was `db_path.unlink()` which
    # wiped history along with everything else.)
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    if not incremental:
        c.execute("DROP TABLE IF EXISTS subgraphs")

    c.execute("""
        CREATE TABLE IF NOT EXISTS subgraphs (
            id TEXT PRIMARY KEY,
            display_name TEXT,
            description TEXT,
            auto_description TEXT,
            website TEXT,
            code_repository TEXT,
            owner TEXT,
            ipfs_hash TEXT,
            network TEXT,
            powered_by_substreams BOOLEAN,
            domain TEXT,
            classification_confidence INTEGER,
            protocol_type TEXT,
            schema_fingerprint TEXT,
            entity_count INTEGER,
            reliability_score REAL,
            signalled_tokens TEXT,
            staked_tokens TEXT,
            query_fees TEXT,
            query_volume_30d INTEGER,
            created_at INTEGER,
            updated_at INTEGER,
            categories TEXT,
            canonical_entities TEXT,
            all_entities TEXT,
            active_allocation_count INTEGER DEFAULT 0,
            contract_addresses TEXT,
            example_query TEXT,
            embedding BLOB
        )
    """)
    # Backfill columns on pre-existing DBs (incremental sync path). Each ALTER
    # is wrapped because SQLite has no "ADD COLUMN IF NOT EXISTS."
    for ddl in (
        "ALTER TABLE subgraphs ADD COLUMN active_allocation_count INTEGER DEFAULT 0",
        "ALTER TABLE subgraphs ADD COLUMN contract_addresses TEXT",
        "ALTER TABLE subgraphs ADD COLUMN example_query TEXT",
        "ALTER TABLE subgraphs ADD COLUMN embedding BLOB",
    ):
        try:
            c.execute(ddl)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Schema-evolution history. Append-only; never truncated. Each row is
    # a single fingerprint change for a subgraph_id (or the bootstrap
    # entry on first sight). Read at query time to answer "how stable is
    # this subgraph's schema?"
    c.execute("""
        CREATE TABLE IF NOT EXISTS schema_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subgraph_id TEXT NOT NULL,
            ipfs_hash TEXT,
            fingerprint TEXT NOT NULL,
            prev_fingerprint TEXT,
            detected_at INTEGER NOT NULL
        )
    """)
    c.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_sg_time "
        "ON schema_history(subgraph_id, detected_at DESC)"
    )
    # Suppress duplicate bootstrap rows (subgraph_id, fingerprint,
    # prev_fingerprint=NULL) — a defensive guard against the full-
    # rebuild bug we fixed by seeding prior_fp from history. If the
    # full-rebuild ever DOES write a NULL prev_fp again, this index
    # turns it into an INSERT OR IGNORE no-op rather than a duplicate.
    c.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uniq_history_bootstrap "
        "ON schema_history(subgraph_id, fingerprint) "
        "WHERE prev_fingerprint IS NULL"
    )
    # TTL prune — anything older than 365 days is irrelevant for
    # "stability_days" computations (anything older just reads as
    # ">1 year stable" anyway) and bloats the npm tarball. Idempotent.
    c.execute(
        "DELETE FROM schema_history WHERE detected_at < ?",
        (int(time.time()) - 365 * 86400,),
    )

    c.execute("CREATE INDEX IF NOT EXISTS idx_domain ON subgraphs(domain)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_network ON subgraphs(network)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_protocol_type ON subgraphs(protocol_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_reliability ON subgraphs(reliability_score DESC)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_fingerprint ON subgraphs(schema_fingerprint)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_allocation ON subgraphs(active_allocation_count)")

    # Snapshot prior fingerprints BEFORE the upsert so we can diff and
    # write to schema_history. On a FULL rebuild the subgraphs table is
    # empty, so we MUST seed prior_fp from schema_history itself —
    # otherwise every subgraph compares against None and inserts a
    # spurious `prev_fingerprint=NULL` row dated `now_unix`, which
    # resets `schema_stable_days` to ~0 for the entire registry the
    # next time someone runs `mode=full`. schema_history is preserved
    # across rebuilds by design (see DROP above), so reading the latest
    # fingerprint per subgraph_id from history gives us the true prior.
    prior_fp: dict[str, str | None] = {}
    try:
        for row in c.execute("SELECT id, schema_fingerprint FROM subgraphs").fetchall():
            prior_fp[row[0]] = row[1]
    except sqlite3.OperationalError:
        pass  # Table was just created and is empty

    # Fall back to schema_history for any subgraph not present in the
    # subgraphs table (the full-rebuild case, or first-time incremental
    # arrivals that were missed by the subgraphs SELECT above). The
    # subgraphs-table lookup takes precedence — it reflects the most
    # recently persisted state.
    try:
        for row in c.execute(
            "SELECT subgraph_id, fingerprint FROM schema_history "
            "WHERE id IN ("
            "  SELECT MAX(id) FROM schema_history GROUP BY subgraph_id"
            ")"
        ).fetchall():
            sg_id, fp = row[0], row[1]
            if sg_id not in prior_fp:
                prior_fp[sg_id] = fp
    except sqlite3.OperationalError:
        pass  # schema_history doesn't exist yet (first run ever)

    # Wrap the write in an explicit transaction so a SIGKILL or OOM
    # mid-batch leaves the file in its pre-write state instead of half-
    # populated. The concurrency group in update-registry.yml prevents
    # concurrent crawls but not crash-mid-write. sqlite3's default
    # isolation_level=DEFERRED auto-opens a transaction on the first
    # DML, so we commit the DDL prelude first and then re-open one
    # explicit transaction covering the entire upsert + history write.
    if conn.in_transaction:
        conn.commit()
    c.execute("BEGIN")
    now_unix = int(time.time())
    history_inserts: list[tuple] = []

    for sg in classified:
        # Diff-and-record: write a history row whenever a subgraph
        # appears with a fingerprint we haven't seen for that ID, OR
        # when the fingerprint changed from the previous run.
        # Skip nulls (schema fetch failed) — recording None would
        # confuse "stability" queries.
        if sg.schema_fingerprint is not None:
            old = prior_fp.get(sg.id)
            if old != sg.schema_fingerprint:
                history_inserts.append((
                    sg.id,
                    sg.ipfs_hash,
                    sg.schema_fingerprint,
                    old,
                    now_unix,
                ))

        c.execute("""
            INSERT OR REPLACE INTO subgraphs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            sg.id, sg.display_name, sg.description, sg.auto_description,
            sg.website, sg.code_repository, sg.owner, sg.ipfs_hash, sg.network,
            sg.powered_by_substreams, sg.domain, sg.classification_confidence,
            sg.protocol_type, sg.schema_fingerprint, sg.entity_count,
            sg.reliability_score, sg.signalled_tokens, sg.staked_tokens,
            sg.query_fees, sg.query_volume_30d, sg.created_at, sg.updated_at,
            json.dumps(sg.self_reported_categories),
            json.dumps([ce["canonical_type"] for ce in sg.canonical_entities]),
            json.dumps(sg.all_entities),
            sg.active_allocation_count,
            json.dumps(sg.contract_addresses) if sg.contract_addresses else None,
            sg.example_query,
            sg.embedding,
        ))

    if history_inserts:
        # INSERT OR IGNORE: the uniq_history_bootstrap partial index
        # makes (subgraph_id, fingerprint) UNIQUE for prev_fingerprint
        # IS NULL rows. A duplicate bootstrap insert (which shouldn't
        # happen anymore, but just in case) becomes a no-op instead
        # of a hard failure that aborts the entire transaction.
        c.executemany(
            "INSERT OR IGNORE INTO schema_history "
            "(subgraph_id, ipfs_hash, fingerprint, prev_fingerprint, detected_at) "
            "VALUES (?, ?, ?, ?, ?)",
            history_inserts,
        )
        print(f"  Schema history: inserted {len(history_inserts)} new fingerprint events")

    conn.commit()
    conn.close()
    print(f"  SQLite written to {db_path} ({db_path.stat().st_size / 1024:.0f} KB)")


async def build_registry(
    max_subgraphs: int | None = None,
    incremental: bool = False,
    write_db: bool = True,
):
    print("╔══════════════════════════════════════════════╗")
    print("║   Subgraph Registry Builder (Python)        ║")
    print("╚══════════════════════════════════════════════╝\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    sync_state = load_sync_state()
    min_updated = sync_state["last_sync_timestamp"] if incremental else 0

    if incremental and min_updated > 0:
        from datetime import datetime, timezone
        print(f"Incremental: fetching updates since {datetime.fromtimestamp(min_updated, tz=timezone.utc).isoformat()}\n")

    # 1. Crawl
    raw_data = await full_crawl(
        min_updated_at=min_updated,
        fetch_schemas_flag=True,
        max_subgraphs=max_subgraphs,
    )

    # 2. Classify
    print("\n=== Classifying ===")
    t0 = time.time()
    # Build query volume map from crawler data
    query_volumes = {}
    for sg in raw_data["subgraphs"]:
        ipfs = sg.get("ipfs_hash")
        vol = sg.get("query_volume_30d", 0)
        if ipfs and vol > 0:
            query_volumes[ipfs] = query_volumes.get(ipfs, 0) + vol
    if query_volumes:
        print(f"  Query volumes available for {len(query_volumes)} deployments")

    classified = classify_all(raw_data["subgraphs"], query_volumes)
    print(f"  Classified {len(classified)} subgraphs in {time.time()-t0:.1f}s")

    # 2b. Deduplicate — keep highest-reliability entry per IPFS hash
    before_count = len(classified)
    seen_ipfs: dict[str, int] = {}
    deduped = []
    for sg in classified:
        ipfs = sg.ipfs_hash
        if not ipfs:
            deduped.append(sg)
            continue
        if ipfs in seen_ipfs:
            existing_idx = seen_ipfs[ipfs]
            if sg.reliability_score > deduped[existing_idx].reliability_score:
                deduped[existing_idx] = sg
        else:
            seen_ipfs[ipfs] = len(deduped)
            deduped.append(sg)
    classified = deduped
    removed = before_count - len(classified)
    if removed > 0:
        print(f"  Deduplicated: removed {removed} duplicate deployments ({before_count} → {len(classified)})")

    # 2c. Compute semantic embeddings for each classified subgraph.
    # Runs in chunked batched passes via fastembed (5-10x faster than
    # per-row). The Node MCP server uses the same MiniLM-L6 model at
    # query time via @xenova/transformers — vectors are CLOSE but not
    # bitwise-identical because the JS side runs the INT8-quantized
    # ONNX while Python runs float32. Top-K rankings are stable;
    # absolute cosine scores may drift by ~0.01-0.03.
    #
    # Lazy reuse: skip re-encoding rows whose source-text inputs are
    # unchanged (same schema_fingerprint + same display_name +
    # description hash + same domain/protocol/network). Saves ~50-100s
    # per full crawl on a GH runner with no quality cost.
    #
    # Per-chunk try/except: if fastembed raises on one batch (rare —
    # usually a malformed string), we preserve the prior embedding for
    # rows in that chunk instead of NULL-ing them out. A broken chunk
    # logs a warning and the pipeline continues.
    if embedder is not None and classified:
        print("\n=== Embedding subgraphs ===")
        t_emb = time.time()

        # Pull existing (id, schema_fingerprint, embedding) rows so we
        # can skip re-encoding unchanged subgraphs.
        existing: dict[str, tuple[str | None, bytes | None]] = {}
        try:
            db_conn = sqlite3.connect(str(SQLITE_FILE))
            for row in db_conn.execute(
                "SELECT id, schema_fingerprint, embedding FROM subgraphs"
            ).fetchall():
                existing[row[0]] = (row[1], row[2])
            db_conn.close()
        except sqlite3.OperationalError:
            pass  # DB doesn't exist yet or column missing — full encode

        # Build (index, text, can_skip) tuples. can_skip=True means
        # we carried over the prior embedding and don't need to encode.
        to_encode_idx: list[int] = []
        to_encode_text: list[str] = []
        skipped = 0
        for idx, c in enumerate(classified):
            text = embedder.build_source_text(
                display_name=c.display_name,
                description=c.description,
                auto_description=c.auto_description,
                canonical_entities=c.canonical_entities,
                all_entities=c.all_entities,
                domain=c.domain,
                protocol_type=c.protocol_type,
                network=c.network,
                contract_addresses=c.contract_addresses,
            )
            prior = existing.get(c.id)
            # Only reuse when fingerprint matches AND embedding is
            # populated — schema_fingerprint is the highest-signal
            # invariant of the embedding inputs.
            if (
                prior is not None
                and prior[1] is not None
                and prior[0] == c.schema_fingerprint
                and c.schema_fingerprint is not None
            ):
                c.embedding = prior[1]
                skipped += 1
                continue
            to_encode_idx.append(idx)
            to_encode_text.append(text)

        # Chunked encode — failures localized to one chunk so a single
        # bad input can't NULL out the entire embedding column.
        CHUNK = 500
        encoded = 0
        for start in range(0, len(to_encode_text), CHUNK):
            chunk_texts = to_encode_text[start : start + CHUNK]
            chunk_idx = to_encode_idx[start : start + CHUNK]
            try:
                blobs = embedder.encode_batch(chunk_texts)
                for ci, blob in zip(chunk_idx, blobs):
                    classified[ci].embedding = blob
                encoded += len(blobs)
            except Exception as e:  # pragma: no cover
                # Preserve whatever embedding was already on the
                # Classification (None for new rows, prior blob for
                # rows we tried to refresh). Don't poison the column.
                print(
                    f"  WARNING: embedding chunk {start//CHUNK} ("
                    f"rows {start}-{start+len(chunk_texts)-1}) failed: {e}; "
                    "preserving prior embeddings for these rows"
                )

        n_with_emb = sum(1 for c in classified if c.embedding)
        print(
            f"  Embedded {encoded} new, reused {skipped} prior; "
            f"{n_with_emb}/{len(classified)} have embeddings in "
            f"{time.time()-t_emb:.1f}s "
            f"(+{n_with_emb * embedder.EMBEDDING_DIM * 4 / 1024 / 1024:.1f} MB)"
        )
    elif embedder is None:
        print("\n=== Embedding subgraphs ===")
        print("  fastembed not installed; skipping embedding pass")

    # 3. Build summary + indices
    print("\n=== Building Indices ===")
    summary = build_summary(classified)
    indices = build_indices(classified)

    print(f"  Domains: {', '.join(summary['by_domain'].keys())}")
    print(f"  Networks: {', '.join(list(summary['by_network'].keys())[:10])}")
    print(f"  Protocol types: {', '.join(summary['by_protocol_type'].keys())}")
    print(f"  Schema families: {summary['schema_family_count']}")
    print(f"  Entity types indexed: {', '.join(indices['by_entity'].keys())}")

    # 4. Assemble registry
    registry = {
        "version": "0.1.0",
        "generated_at": raw_data["crawled_at"],
        "sync_timestamp": raw_data["sync_timestamp"],
        "network_stats": raw_data["network_stats"],
        "summary": summary,
        "indices": indices,
        "subgraphs": [asdict(c) for c in classified],
    }

    # 5. Write outputs
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2, default=str))
    size_mb = REGISTRY_FILE.stat().st_size / 1024 / 1024
    print(f"\n  Registry: {REGISTRY_FILE} ({size_mb:.1f} MB)")

    if write_db:
        write_sqlite(classified, incremental=incremental)

    # Update sync state
    save_sync_state({
        "last_sync_timestamp": raw_data["sync_timestamp"],
        "total_classified": len(classified),
        "last_run_at": raw_data["crawled_at"],
    })

    # Print report
    print("\n╔══════════════════════════════════════════════╗")
    print("║   Registry Summary                          ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Total classified: {len(classified):<24}║")
    print("║                                             ║")
    print("║  By Domain:                                 ║")
    for domain, count in summary["by_domain"].items():
        print(f"║    {domain:<22} {count:>5}            ║")
    print("║                                             ║")
    print("║  Top Networks:                              ║")
    for net, count in list(summary["by_network"].items())[:8]:
        print(f"║    {net:<22} {count:>5}            ║")
    print("║                                             ║")
    print("║  Top Protocol Types:                        ║")
    for pt, count in list(summary["by_protocol_type"].items())[:8]:
        print(f"║    {pt:<22} {count:>5}            ║")
    print("╚══════════════════════════════════════════════╝")

    return registry


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=None, help="Max subgraphs")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--no-db", action="store_true", help="Skip SQLite output")
    args = parser.parse_args()

    asyncio.run(build_registry(
        max_subgraphs=args.max,
        incremental=args.incremental,
        write_db=not args.no_db,
    ))
