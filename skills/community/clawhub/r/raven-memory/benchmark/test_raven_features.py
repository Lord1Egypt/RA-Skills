from __future__ import annotations

import os
import tempfile

from tcc.core.dag import TaskDAG
from tcc.core.reconciler import SessionReconciler
from tcc.core.store import TCCStore


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "raven_features.db")
        store = TCCStore(db_path)
        dag = TaskDAG(store)
        reconciler = SessionReconciler()

        # Fresh DAG initializes correctly
        assert dag.tip() is None
        print("[PASS] fresh DAG initializes")

        # Session start + append advances tip
        session_ctx = reconciler.start_session(dag)
        sid = session_ctx["session_id"]
        start_tip = dag.tip()
        assert start_tip is not None
        assert start_tip.node_type == "milestone"
        assert start_tip.subtype == "start"
        print("[PASS] start_session creates milestone start node")

        appended = dag.append(event="implemented parser", actor="agent", session_id=sid)
        assert dag.tip() is not None and dag.tip().hash == appended.hash
        assert appended.status == "done"
        print("[PASS] append adds node and advances tip")

        # node_parents table tracking
        parents = store.get_parents(appended.hash)
        assert isinstance(parents, list)
        assert len(parents) == 1
        print(f"[PASS] node_parents: {len(parents)} parents")

        # branch_from_tip writes no node
        count_before_branch = len(store.load_all())
        branch_id = dag.branch_from_tip(session_id=sid)
        count_after_branch = len(store.load_all())
        assert isinstance(branch_id, str)
        assert branch_id in dag._branches
        assert count_before_branch == count_after_branch
        print(f"[PASS] branch_from_tip: {branch_id}")

        # branch() creates running node
        parent_hash = dag.tip().hash
        branch_node, branch_bid = dag.branch(
            from_hash=parent_hash,
            event="parallel branch task",
            actor="agent",
            session_id=sid,
            status="running",
        )
        assert branch_node.status == "running"
        assert dag._parents[branch_node.hash] == [parent_hash]
        assert branch_bid in dag._branches
        print("[PASS] branch creates running branch node")

        # public merge()
        node_a, _ = dag.branch(from_hash=dag.tip().hash, event="task A", actor="agent", session_id=sid)
        node_b, _ = dag.branch(from_hash=dag.tip().hash, event="task B", actor="agent", session_id=sid)
        dag.update_status(node_a.hash, "done")
        dag.update_status(node_b.hash, "done")
        merge = dag.merge([node_a.hash, node_b.hash], session_id=sid)
        assert merge.node_type == "milestone"
        assert merge.subtype == "merge"
        assert len(dag._parents[merge.hash]) >= 2
        print(f"[PASS] public merge: {merge.event}")

        # auto-merge when all branches done/failed
        base = dag.tip().hash
        auto_a, _ = dag.branch(from_hash=base, event="auto A", actor="agent", session_id=sid, status="running")
        auto_b, _ = dag.branch(from_hash=base, event="auto B", actor="agent", session_id=sid, status="running")
        tip_before_done = dag.tip().hash
        dag.update_status(auto_a.hash, "failed")
        assert dag.tip().hash == tip_before_done
        dag.update_status(auto_b.hash, "done")
        auto_merge_tip = dag.tip()
        assert auto_merge_tip is not None
        assert auto_merge_tip.node_type == "milestone"
        assert auto_merge_tip.subtype == "merge"
        print("[PASS] auto-merge fires on done/failed branches")

        # recent() most-recent-first and ancestor checks
        recent = dag.recent(5)
        assert len(recent) > 0
        assert recent[0].timestamp >= recent[-1].timestamp
        assert dag.is_ancestor_of_tip(recent[-1].hash) is True
        print("[PASS] recent ordering + is_ancestor_of_tip")

        # since(session_id)
        session_nodes = dag.since(sid)
        assert len(session_nodes) > 0
        assert all(node.session_id == sid for node in session_nodes)
        print("[PASS] since(session_id) returns correct nodes")

        # rollback moves tip and clears stale branches
        rollback_from = dag.tip().hash
        stale_branch_node, stale_bid = dag.branch(
            from_hash=rollback_from,
            event="stale branch",
            actor="agent",
            session_id=sid,
            status="running",
        )
        _ = stale_branch_node
        dag.append(event="main progress", actor="agent", session_id=sid)
        rolled = dag.rollback(1)
        assert dag.tip() is not None and dag.tip().hash == rolled.hash
        assert stale_bid not in dag._branches
        print("[PASS] rollback moves tip and clears stale branches")

        # Reconciler note/event APIs on new schema
        note_node = reconciler.record_note(dag, sid, "Need to revisit constraints")
        assert note_node.node_type == "decided"
        assert note_node.trigger == "explicit"

        event_node = reconciler.record_event(
            dag=dag,
            session_id=sid,
            event="ran smoke tests",
            actor="tool",
            result_summary="all green",
            tool_name="pytest",
        )
        assert event_node.result_summary == "all green"
        assert event_node.tool_name == "pytest"
        print("[PASS] reconciler record_note/record_event new signatures")

        # End session + persistence
        end = reconciler.end_session(dag, sid, notes="session complete")
        assert end is not None
        assert end.subtype == "end"
        assert end.summary == "session complete"

        store_reloaded = TCCStore(db_path)
        dag_reloaded = TaskDAG(store_reloaded)
        assert dag_reloaded.tip() is not None
        assert len(dag_reloaded.recent(20)) > 0
        print("[PASS] persistence across store reload")

        # CTE traversal + path
        tip = dag_reloaded.tip()
        assert tip is not None
        ancestors = store_reloaded.ancestors(tip.hash, max_depth=50)
        assert len(ancestors) > 0
        print(f"[PASS] ancestors CTE: {len(ancestors)} ancestors found")

        root_hash = store_reloaded.get_meta("root_hash")
        if root_hash:
            path_hashes = store_reloaded.path_between(root_hash, tip.hash)
            assert path_hashes[0] == root_hash
            assert path_hashes[-1] == tip.hash
            print("[PASS] path_between returns valid root->tip path")

        # Session 2 resumes session 1 history
        reconciler2 = SessionReconciler()
        ctx2 = reconciler2.start_session(dag_reloaded, search_query="smoke")
        assert ctx2["is_fresh"] is False
        assert isinstance(ctx2["summary"], str) and len(ctx2["summary"]) > 0
        print("[PASS] session 2 resumes session 1 context")


if __name__ == "__main__":
    main()
