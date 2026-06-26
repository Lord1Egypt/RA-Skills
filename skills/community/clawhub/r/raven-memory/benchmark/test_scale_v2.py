"""
Raven Scale Test v2 — 500 nodes, WAL, concurrent multi-agent writes

Tests:
1.  Write 500 nodes via save_nodes_batch() — timing
2.  recent(20) at scale
3.  CTE ancestor traversal at depth
4.  path_between root → tip
5.  Semantic search across 500 nodes
6.  Branch/merge at scale
7.  Rollback at depth
8.  Session resume with full history
9.  nodes_for_session query
10. Concurrent multi-agent writes (10 agents, 50 nodes each = 500 nodes)
11. WAL mode confirmed
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
from datetime import datetime, timezone

from tcc.core.dag import TaskDAG
from tcc.core.node import TCCNode
from tcc.core.reconciler import SessionReconciler
from tcc.core.store import TCCStore


def elapsed(start: float) -> str:
    ms = (time.time() - start) * 1000
    return f"{ms:.1f}ms"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    print("=" * 60)
    print("Raven Scale Test v2 — 500 nodes + concurrent agents")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "raven_scale.db")
        store = TCCStore(db_path)
        dag = TaskDAG(store)
        reconciler = SessionReconciler()

        # ── Test 11: WAL mode confirmed ──────────────────────────────────
        print("\n=== Test 11: WAL mode ===")
        row = store._conn.execute("PRAGMA journal_mode").fetchone()
        wal_mode = row[0] if row else "unknown"
        print(f"  journal_mode: {wal_mode}")
        assert wal_mode == "wal", f"Expected WAL, got {wal_mode}"
        sync = store._conn.execute("PRAGMA synchronous").fetchone()
        print(f"  synchronous: {sync[0]} (1=NORMAL)")
        print("[PASS] WAL mode enabled")

        # ── Test 1: Batch write 500 nodes ────────────────────────────────
        print("\n=== Test 1: Batch write 500 nodes ===")
        ctx = reconciler.start_session(dag)
        sid = ctx["session_id"]

        event_templates = [
            ("ran unit tests", "tool", "action", "pytest", "all 42 tests passed"),
            ("user updated budget cap to $8000", "user", "decided", None, None),
            ("deployed to staging", "agent", "action", "deploy.sh", "exit 0"),
            ("session checkpoint", "system", "milestone", None, None),
            ("read config file", "agent", "action", "read_file", "loaded 14 settings"),
            ("wrote memory: prefers concise answers", "agent", "decided", None, None),
            ("ran smoke tests on staging", "tool", "action", "smoke_runner", "3/3 passed"),
            ("user confirmed go-ahead for prod", "user", "decided", None, None),
        ]

        # Build 500 nodes as a batch
        items: list[tuple[TCCNode, list[str]]] = []
        prev_hash = dag.tip().hash if dag.tip() else None

        t_build = time.time()
        for i in range(500):
            tmpl = event_templates[i % len(event_templates)]
            event_text, actor, node_type, tool_name, result_summary = tmpl
            node = TCCNode.create(
                node_type=node_type,
                timestamp=now(),
                event=f"{event_text} #{i}",
                actor=actor,
                session_key=f"agent:raven:{sid}",
                session_id=sid,
                status="done",
                branch_id="main",
                tool_name=tool_name,
                result_summary=result_summary,
                open_threads=json.dumps(["task alpha", "task beta"]) if i % 50 == 0 else None,
            )
            parent_hashes = [prev_hash] if prev_hash else []
            items.append((node, parent_hashes))
            prev_hash = node.hash

        build_time = elapsed(t_build)

        t_write = time.time()
        store.save_nodes_batch(items)
        write_time = elapsed(t_write)

        # Update dag _index and _parents after batch write
        for node, parent_hashes in items:
            dag._index[node.hash] = node
            dag._parents[node.hash] = parent_hashes

        # Advance tip to last node
        last_node = items[-1][0]
        dag._tip_hash = last_node.hash
        store.set_meta("tip_hash", last_node.hash)

        total_nodes = len(store.load_all())
        print(f"  Built 500 nodes in {build_time}")
        print(f"  Batch wrote 500 nodes in {write_time}")
        print(f"  Total nodes in store: {total_nodes}")
        assert total_nodes >= 500
        print(f"[PASS] 500 nodes batch written — {write_time}")

        # ── Test 2: recent(20) at scale ──────────────────────────────────
        print("\n=== Test 2: recent(20) at scale ===")
        t_recent = time.time()
        recent = dag.recent(20)
        recent_time = elapsed(t_recent)
        assert len(recent) == 20
        assert recent[0].timestamp >= recent[-1].timestamp
        print(f"  recent(20) in {recent_time}")
        print(f"[PASS] recent() correct — {recent_time}")

        # ── Test 3: CTE ancestor traversal ──────────────────────────────
        print("\n=== Test 3: CTE ancestor traversal ===")
        tip = dag.tip()
        t_anc = time.time()
        ancestors_100 = store.ancestors(tip.hash, max_depth=100)
        anc_100_time = elapsed(t_anc)

        t_anc2 = time.time()
        ancestors_500 = store.ancestors(tip.hash, max_depth=500)
        anc_500_time = elapsed(t_anc2)

        print(f"  ancestors(100): {len(ancestors_100)} nodes in {anc_100_time}")
        print(f"  ancestors(500): {len(ancestors_500)} nodes in {anc_500_time}")
        assert len(ancestors_100) > 0
        assert len(ancestors_500) >= len(ancestors_100)
        print(f"[PASS] CTE traversal — {anc_500_time}")

        # ── Test 4: path_between root → tip ─────────────────────────────
        print("\n=== Test 4: path_between root → tip ===")
        root_hash = store.get_meta("root_hash")
        if root_hash:
            t_path = time.time()
            path = store.path_between(root_hash, tip.hash)
            path_time = elapsed(t_path)
            print(f"  path length: {len(path)} hops in {path_time}")
            assert path[0] == root_hash
            assert path[-1] == tip.hash
            print(f"[PASS] path_between — {path_time}")
        else:
            print("[SKIP] root_hash not in meta")

        # ── Test 5: Semantic search ──────────────────────────────────────
        print("\n=== Test 5: Semantic search at scale ===")
        if store.is_vec_enabled:
            t_embed = time.time()
            n_embedded = store.embed_all(show_progress=False, batch_size=64)
            embed_time = elapsed(t_embed)
            print(f"  Embedded {n_embedded} nodes in {embed_time}")

            queries = [
                "budget cap updated",
                "staging deployment",
                "smoke tests passed",
                "user confirmed production",
            ]
            for q in queries:
                t_s = time.time()
                results = store.search(q, n=5)
                print(f"  search('{q}'): {len(results)} results in {elapsed(t_s)}")
                assert len(results) > 0
            print("[PASS] semantic search at scale")
        else:
            print("[SKIP] sqlite-vec not enabled")

        # ── Test 6: Branch/merge at scale ───────────────────────────────
        print("\n=== Test 6: Branch/merge at scale (10 branches) ===")
        base = dag.tip().hash
        branch_hashes = []
        t_branch = time.time()
        for i in range(10):
            node, _ = dag.branch(
                from_hash=base,
                event=f"parallel task {i}",
                actor="agent",
                session_id=sid,
                status="running",
            )
            dag.update_status(node.hash, "done")
            branch_hashes.append(node.hash)
        branch_time = elapsed(t_branch)

        t_merge = time.time()
        merge = dag.merge(branch_hashes, event="merged 10 parallel tasks", session_id=sid)
        merge_time = elapsed(t_merge)

        assert merge.subtype == "merge"
        assert len(dag._parents[merge.hash]) >= 2
        print(f"  10 branches created+closed in {branch_time}")
        print(f"  Merged in {merge_time}")
        print(f"[PASS] branch/merge at scale")

        # ── Test 7: Rollback at depth ────────────────────────────────────
        print("\n=== Test 7: Rollback at depth (50 hops) ===")
        tip_before = dag.tip().hash
        t_rb = time.time()
        rolled = dag.rollback(50)
        rb_time = elapsed(t_rb)
        assert rolled.hash != tip_before
        assert dag.tip().hash == rolled.hash
        print(f"  rollback(50) in {rb_time}")
        print(f"  Landed on: {rolled.event}")
        print(f"[PASS] rollback at depth — {rb_time}")

        # ── Test 8: Session resume ───────────────────────────────────────
        print("\n=== Test 8: Session resume with full history ===")
        reconciler.end_session(dag, sid, notes="scale test session complete")

        t_reload = time.time()
        store2 = TCCStore(db_path)
        dag2 = TaskDAG(store2)
        reload_time = elapsed(t_reload)

        t_resume = time.time()
        ctx2 = SessionReconciler().start_session(
            dag2,
            search_query="staging deployment",
            n_recent=10,
        )
        resume_time = elapsed(t_resume)

        assert ctx2["is_fresh"] is False
        assert len(ctx2["summary"]) > 0
        print(f"  Reload {total_nodes}+ nodes in {reload_time}")
        print(f"  Session resume in {resume_time}")
        print(f"  Summary preview: {ctx2['summary'][:80]}...")
        print(f"[PASS] session resume — {reload_time} reload, {resume_time} resume")

        # ── Test 9: nodes_for_session ────────────────────────────────────
        print("\n=== Test 9: nodes_for_session ===")
        t_sq = time.time()
        session_nodes = store2.nodes_for_session(sid)
        sq_time = elapsed(t_sq)
        assert len(session_nodes) > 0
        print(f"  {len(session_nodes)} nodes in {sq_time}")
        print(f"[PASS] nodes_for_session — {sq_time}")

        # ── Test 10: Concurrent multi-agent writes ───────────────────────
        print("\n=== Test 10: Concurrent multi-agent writes ===")
        print("  10 agents × 50 nodes each = 500 nodes")

        store_ma = TCCStore(db_path)
        dag_ma = TaskDAG(store_ma)
        ctx_ma = SessionReconciler().start_session(dag_ma)
        sid_ma = ctx_ma["session_id"]
        fork = dag_ma.tip().hash

        errors: list[str] = []
        written_hashes: list[str] = []
        lock = threading.Lock()

        def agent_write(agent_id: int) -> None:
            # Each agent gets its own store connection
            agent_store = TCCStore(db_path)
            agent_dag = TaskDAG(agent_store)

            parent = fork
            batch: list[tuple[TCCNode, list[str]]] = []

            for i in range(50):
                try:
                    node = TCCNode.create(
                        node_type="action",
                        timestamp=now(),
                        event=f"agent_{agent_id} task {i}",
                        actor="agent",
                        session_key=f"agent:raven:{sid_ma}",
                        session_id=sid_ma,
                        status="done",
                        branch_id=f"agent_{agent_id}",
                        tool_name="agent_tool",
                        result_summary=f"agent {agent_id} result {i}",
                    )
                    batch.append((node, [parent]))
                    parent = node.hash
                except Exception as exc:
                    with lock:
                        errors.append(f"agent_{agent_id} build {i}: {exc}")
                    return

            try:
                agent_store.save_nodes_batch(batch)
                with lock:
                    written_hashes.extend(n.hash for n, _ in batch)
            except Exception as exc:
                with lock:
                    errors.append(f"agent_{agent_id} batch write: {exc}")

        t_concurrent = time.time()
        threads = [threading.Thread(target=agent_write, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        concurrent_time = elapsed(t_concurrent)

        assert len(errors) == 0, f"Concurrent write errors: {errors}"
        assert len(written_hashes) == 500, f"Expected 500, got {len(written_hashes)}"
        assert len(set(written_hashes)) == 500, "Duplicate hashes detected"

        # Verify all nodes readable
        verify_store = TCCStore(db_path)
        missing = []
        for h in written_hashes[:50]:  # spot check 50
            try:
                verify_store.load(h)
            except Exception:
                missing.append(h)
        assert len(missing) == 0, f"{len(missing)} nodes missing after concurrent write"

        print(f"  500 nodes written by 10 concurrent agents in {concurrent_time}")
        print(f"  Errors: {len(errors)}")
        print(f"  Unique hashes: {len(set(written_hashes))}")
        print(f"  Spot check (50 nodes): all readable")
        print(f"[PASS] concurrent multi-agent writes — {concurrent_time}")

        # ── Summary ──────────────────────────────────────────────────────
        final_count = len(verify_store.load_all())
        print("\n" + "=" * 60)
        print("ALL SCALE TESTS PASSED")
        print("=" * 60)
        print(f"\nFinal node count : {final_count}")
        print(f"WAL mode         : {wal_mode}")
        print(f"sqlite-vec       : {'enabled' if store.is_vec_enabled else 'disabled'}")
        print(f"\nKey timings:")
        print(f"  Batch write 500 : {write_time}")
        print(f"  recent(20)      : {recent_time}")
        print(f"  CTE 500 deep    : {anc_500_time}")
        print(f"  Store reload    : {reload_time}")
        print(f"  Session resume  : {resume_time}")
        print(f"  10-agent conc.  : {concurrent_time}")


if __name__ == "__main__":
    main()
