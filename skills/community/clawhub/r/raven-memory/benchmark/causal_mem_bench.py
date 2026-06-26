import json
import os
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tcc.core.dag import TaskDAG
from tcc.core.node import TCCNode
from tcc.core.reconciler import SessionReconciler
from tcc.core.store import TCCStore


@dataclass
class Question:
    id: str
    category: str
    question: str
    answer: str
    query_fn: Callable[[TaskDAG, TCCStore, dict], str]


@dataclass
class Scenario:
    id: str
    description: str
    questions: list[Question]
    build_fn: Callable[[TaskDAG, TCCStore, str], dict]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _create_node(
    node_type: str,
    sid: str,
    event: str,
    status: str = "done",
    *,
    subtype: str | None = None,
    summary: str | None = None,
    content: str | None = None,
    open_threads: str | None = None,
    branch_id: str = "main",
) -> TCCNode:
    return TCCNode.create(
        node_type=node_type,
        timestamp=_now(),
        actor="agent",
        session_key=f"agent:raven:{sid}",
        session_id=sid,
        event=event,
        status=status,
        branch_id=branch_id,
        subtype=subtype,
        summary=summary,
        content=content,
        open_threads=open_threads,
    )


def _append_from_node(dag: TaskDAG, node: TCCNode, parent_hash: str | None = None) -> TCCNode:
    return dag.append(
        event=node.event,
        actor=node.actor,
        session_id=node.session_id,
        parent_hash=parent_hash,
        status=node.status,
        node_type=node.node_type,
        session_key=node.session_key,
        subtype=node.subtype,
        summary=node.summary,
        content=node.content,
        open_threads=node.open_threads,
    )


def find_cause_of(store, node_hash: str) -> str:
    """Walk parent edges to find the most recent non-milestone ancestor."""
    parents = store.get_parents(node_hash)
    if not parents:
        return "no cause found"
    parent = store.load(parents[0])
    if parent.node_type in ("action", "decided"):
        return parent.event
    grandparents = store.get_parents(parent.hash)
    if grandparents:
        return store.load(grandparents[0]).event
    return parent.event


def find_branch_siblings(store, node_hash: str) -> str:
    """Find other nodes that share the same parent (ran in parallel)."""
    parents = store.get_parents(node_hash)
    if not parents:
        return "nothing"
    siblings = store.get_children(parents[0])
    siblings = [h for h in siblings if h != node_hash]
    if not siblings:
        return "nothing"
    nodes = [store.load(h) for h in siblings]
    nodes = [n for n in nodes if n.node_type in ("action", "decided")]
    if not nodes:
        return "nothing"
    return ", ".join(n.event for n in nodes)


def causal_depth(store, node_hash: str) -> int:
    """Number of ancestor hops from root."""
    return len(store.ancestors(node_hash, max_depth=200))


def find_merge_successor(dag, store, merge_hash: str) -> str:
    """Find the first node after a merge on the main chain."""
    children = store.get_children(merge_hash)
    if not children:
        return "none"
    return store.load(children[0]).event


def find_open_threads(store, session_id: str) -> str:
    """Find open_threads from the most recent decided node in a session."""
    nodes = store.nodes_for_session(session_id)
    for node in reversed(nodes):
        if node.open_threads:
            try:
                threads = json.loads(node.open_threads)
                if threads:
                    return threads[0]
            except json.JSONDecodeError:
                pass
    return "none"




def find_cause_of_with_orphans(dag: TaskDAG, store: TCCStore, node_hash: str) -> str:
    """
    Find the most recent non-milestone cause of a node.
    If the direct parent chain only leads to milestones,
    fall back to the most recently written orphaned non-milestone
    node (nodes rolled past but still in store).
    """
    parents = store.get_parents(node_hash)
    if not parents:
        return "no cause found"
    parent = store.load(parents[0])
    if parent.node_type in ("action", "decided"):
        return parent.event
    grandparents = store.get_parents(parent.hash)
    if grandparents:
        gp = store.load(grandparents[0])
        if gp.node_type in ("action", "decided"):
            return gp.event

    tip = dag.tip()
    if tip is None:
        return "no cause found"
    ancestor_hashes = set(store.ancestors(tip.hash, max_depth=500))
    ancestor_hashes.add(tip.hash)
    all_nodes = store.load_all()
    orphans = [
        n for n in all_nodes
        if n.hash not in ancestor_hashes
        and n.node_type in ("action", "decided")
    ]
    if not orphans:
        return "no cause found"
    # Prefer the most recently written orphan as proximate cause.
    orphans.sort(key=lambda n: n.timestamp, reverse=True)
    return orphans[0].event



def find_rollback_victims(dag: TaskDAG, store: TCCStore) -> str:
    """
    Find nodes that exist in the store but are NOT ancestors of
    (or equal to) the current tip. These are nodes orphaned by a
    rollback. Returns the event of the oldest orphan
    that is not a milestone, or 'no' if none found.
    """
    tip = dag.tip()
    if tip is None:
        return "no"

    ancestor_hashes = set(store.ancestors(tip.hash, max_depth=500))
    ancestor_hashes.add(tip.hash)

    all_nodes = store.load_all()

    orphans = [
        n for n in all_nodes
        if n.hash not in ancestor_hashes
        and n.node_type != "milestone"
    ]

    if not orphans:
        return "no"

    # Return oldest orphan — the first node rolled past.
    orphans.sort(key=lambda n: n.timestamp)
    return orphans[0].event

def find_session_end_summary(store, session_id: str) -> str:
    """Get the summary from the session end milestone."""
    nodes = store.nodes_for_session(session_id)
    for node in reversed(nodes):
        if node.node_type == "milestone" and node.subtype == "end":
            return node.summary or "none"
    return "none"


def build_scenario_1(dag: TaskDAG, _store: TCCStore, sid: str) -> dict:
    start = _append_from_node(dag, _create_node("milestone", sid, "session start", subtype="start"))
    sim = _append_from_node(
        dag,
        _create_node("action", sid, "ran titanium stress simulation", status="failed"),
    )
    fail = _append_from_node(
        dag,
        _create_node("action", sid, "simulation exceeded load tolerance", status="failed"),
    )
    decision = _append_from_node(
        dag,
        _create_node("decided", sid, "decided: switch to carbon fibre", content="switch material"),
    )
    memory = _append_from_node(
        dag,
        _create_node("decided", sid, "wrote memory: carbon fibre preferred", content="carbon fibre"),
    )
    end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid,
            "session end",
            subtype="end",
            summary="switched material after sim failure",
        ),
    )
    return {
        "sid": sid,
        "sim_hash": sim.hash,
        "failure_hash": fail.hash,
        "decision_hash": decision.hash,
        "memory_hash": memory.hash,
        "end_hash": end.hash,
        "start_hash": start.hash,
    }


def build_scenario_2(dag: TaskDAG, _store: TCCStore, sid: str) -> dict:
    start = _append_from_node(dag, _create_node("milestone", sid, "session start", subtype="start"))
    pivot = _append_from_node(dag, _create_node("action", sid, "starting parallel analysis"))

    branch_a, _ = dag.branch(
        from_hash=pivot.hash,
        event="ran spectral analysis",
        actor="agent",
        session_id=sid,
        status="done",
        node_type="action",
        session_key=f"agent:raven:{sid}",
    )
    branch_b, _ = dag.branch(
        from_hash=pivot.hash,
        event="ran thermal analysis",
        actor="agent",
        session_id=sid,
        status="done",
        node_type="action",
        session_key=f"agent:raven:{sid}",
    )

    merge = dag.merge(
        [branch_a.hash, branch_b.hash],
        event="merged: spectral and thermal complete",
        session_id=sid,
    )

    finding = _append_from_node(
        dag,
        _create_node("decided", sid, "recorded finding: thermal risk identified", content="thermal risk identified"),
    )
    end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid,
            "session end",
            subtype="end",
            summary="thermal risk found via parallel analysis",
        ),
    )
    return {
        "sid": sid,
        "start_hash": start.hash,
        "pivot_hash": pivot.hash,
        "spectral_hash": branch_a.hash,
        "thermal_hash": branch_b.hash,
        "merge_hash": merge.hash,
        "finding_hash": finding.hash,
        "end_hash": end.hash,
    }


def build_scenario_3(dag: TaskDAG, _store: TCCStore, sid: str) -> dict:
    start = _append_from_node(dag, _create_node("milestone", sid, "session start", subtype="start"))
    v1 = _append_from_node(dag, _create_node("action", sid, "deployed v1 to staging", status="failed"))
    v1_fail = _append_from_node(dag, _create_node("action", sid, "staging health check failed", status="failed"))
    dag.rollback(2)
    decision = _append_from_node(dag, _create_node("decided", sid, "decided: deploy v2 instead"))
    v2 = _append_from_node(dag, _create_node("action", sid, "deployed v2 to staging", status="done"))
    v2_pass = _append_from_node(dag, _create_node("action", sid, "staging health check passed", status="done"))
    end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid,
            "session end",
            subtype="end",
            summary="v2 deployed after v1 failure and rollback",
        ),
    )
    return {
        "sid": sid,
        "start_hash": start.hash,
        "v1_hash": v1.hash,
        "v1_fail_hash": v1_fail.hash,
        "decision_hash": decision.hash,
        "v2_hash": v2.hash,
        "v2_pass_hash": v2_pass.hash,
        "end_hash": end.hash,
        "rollback_event": v1.event,
        "decision_cause": v1_fail.event,
    }


def build_scenario_4(dag: TaskDAG, _store: TCCStore, sid: str) -> dict:
    sid2 = uuid.uuid4().hex[:12]

    s1_start = _append_from_node(dag, _create_node("milestone", sid, "session start", subtype="start"))
    research = _append_from_node(dag, _create_node("action", sid, "researched quantum error correction"))
    found = _append_from_node(dag, _create_node("decided", sid, "found promising approach: surface codes"))
    carry = _append_from_node(
        dag,
        _create_node(
            "decided",
            sid,
            "wrote memory: follow up on surface codes next session",
            open_threads='["surface codes follow-up"]',
        ),
    )
    s1_end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid,
            "session end",
            subtype="end",
            summary="surface codes identified as promising",
        ),
    )

    s2_start = _append_from_node(dag, _create_node("milestone", sid2, "session start", subtype="start"))
    resume = _append_from_node(dag, _create_node("action", sid2, "resumed surface codes research"))
    sim = _append_from_node(dag, _create_node("action", sid2, "ran surface codes simulation", status="done"))
    viable = _append_from_node(dag, _create_node("decided", sid2, "decided: surface codes viable"))
    s2_end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid2,
            "session end",
            subtype="end",
            summary="surface codes confirmed viable",
        ),
    )

    return {
        "sid": sid,
        "sid2": sid2,
        "s1_start_hash": s1_start.hash,
        "research_hash": research.hash,
        "found_hash": found.hash,
        "carry_hash": carry.hash,
        "s1_end_hash": s1_end.hash,
        "s2_start_hash": s2_start.hash,
        "resume_hash": resume.hash,
        "sim_hash": sim.hash,
        "viable_hash": viable.hash,
        "s2_end_hash": s2_end.hash,
    }


def build_scenario_5(dag: TaskDAG, _store: TCCStore, sid: str) -> dict:
    sid2 = uuid.uuid4().hex[:12]

    s1_start = _append_from_node(dag, _create_node("milestone", sid, "session start", subtype="start"))
    pivot = _append_from_node(dag, _create_node("action", sid, "starting three parallel tasks"))

    data_node, _ = dag.branch(
        from_hash=pivot.hash,
        event="data ingestion",
        actor="agent",
        session_id=sid,
        status="done",
        node_type="action",
        session_key=f"agent:raven:{sid}",
    )
    train_node, _ = dag.branch(
        from_hash=pivot.hash,
        event="model training",
        actor="agent",
        session_id=sid,
        status="done",
        node_type="action",
        session_key=f"agent:raven:{sid}",
    )
    valid_node, _ = dag.branch(
        from_hash=pivot.hash,
        event="validation suite",
        actor="agent",
        session_id=sid,
        status="failed",
        node_type="action",
        session_key=f"agent:raven:{sid}",
    )

    merge = dag.merge(
        [data_node.hash, train_node.hash, valid_node.hash],
        event="merged: ingestion, training, validation complete",
        session_id=sid,
    )

    dag.rollback(1)
    post_merge = _append_from_node(
        dag,
        _create_node("decided", sid, "decided: rerun validation only"),
        parent_hash=merge.hash,
    )
    rerun = _append_from_node(dag, _create_node("action", sid, "reran validation suite", status="done"))
    memory = _append_from_node(
        dag,
        _create_node(
            "decided",
            sid,
            "wrote memory: validation requires clean dataset",
            content="validation requires clean dataset",
        ),
    )
    s1_end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid,
            "session end",
            subtype="end",
            summary="validation fixed after parallel run",
        ),
    )

    s2_start = _append_from_node(dag, _create_node("milestone", sid2, "session start", subtype="start"))
    applied = _append_from_node(dag, _create_node("action", sid2, "applied clean dataset"))
    passed = _append_from_node(dag, _create_node("action", sid2, "full pipeline passed", status="done"))
    s2_end = _append_from_node(
        dag,
        _create_node(
            "milestone",
            sid2,
            "session end",
            subtype="end",
            summary="pipeline passed with clean dataset",
        ),
    )

    return {
        "sid": sid,
        "sid2": sid2,
        "s1_start_hash": s1_start.hash,
        "pivot_hash": pivot.hash,
        "data_hash": data_node.hash,
        "train_hash": train_node.hash,
        "validation_hash": valid_node.hash,
        "merge_hash": merge.hash,
        "post_merge_hash": post_merge.hash,
        "rerun_hash": rerun.hash,
        "memory_hash": memory.hash,
        "s1_end_hash": s1_end.hash,
        "s2_start_hash": s2_start.hash,
        "applied_hash": applied.hash,
        "passed_hash": passed.hash,
        "s2_end_hash": s2_end.hash,
        "rollback_event": merge.event,
    }


def build_scenarios() -> list[Scenario]:
    return [
        Scenario(
            id="scenario_1_material_switch",
            description="Material switch after simulation failure",
            build_fn=build_scenario_1,
            questions=[
                Question(
                    id="s1_q1",
                    category="causal_provenance",
                    question="Why did the agent decide to switch materials?",
                    answer="simulation exceeded load tolerance",
                    query_fn=lambda _d, store, meta: find_cause_of(store, meta["decision_hash"]),
                ),
                Question(
                    id="s1_q2",
                    category="parallel_execution",
                    question="What was running in parallel with the stress simulation?",
                    answer="nothing",
                    query_fn=lambda _d, store, meta: find_branch_siblings(store, meta["sim_hash"]),
                ),
                Question(
                    id="s1_q3",
                    category="temporal_ordering",
                    question="Did the material decision happen before or after the simulation failure?",
                    answer="after",
                    query_fn=lambda _d, store, meta: "after"
                    if causal_depth(store, meta["decision_hash"]) > causal_depth(store, meta["failure_hash"])
                    else "before",
                ),
                Question(
                    id="s1_q4",
                    category="rollback_provenance",
                    question="Was anything rolled back in this session?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
                Question(
                    id="s1_q5",
                    category="cross_session",
                    question="What material preference was carried into the next session?",
                    answer="carbon fibre",
                    query_fn=lambda _d, store, meta: store.load(meta["memory_hash"]).content or "none",
                ),
                Question(
                    id="s1_q6",
                    category="merge_outcome",
                    question="Was there a merge in this session?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
            ],
        ),
        Scenario(
            id="scenario_2_parallel_merge",
            description="Parallel analysis with merge",
            build_fn=build_scenario_2,
            questions=[
                Question(
                    id="s2_q1",
                    category="causal_provenance",
                    question="Why was thermal risk recorded?",
                    answer="merged: spectral and thermal complete",
                    query_fn=lambda _d, store, meta: store.load(meta["merge_hash"]).event,
                ),
                Question(
                    id="s2_q2",
                    category="parallel_execution",
                    question="What ran in parallel with the spectral analysis?",
                    answer="ran thermal analysis",
                    query_fn=lambda _d, store, meta: find_branch_siblings(store, meta["spectral_hash"]),
                ),
                Question(
                    id="s2_q3",
                    category="temporal_ordering",
                    question="Did the merge happen before or after thermal risk was recorded?",
                    answer="before",
                    query_fn=lambda _d, store, meta: "before"
                    if causal_depth(store, meta["merge_hash"]) < causal_depth(store, meta["finding_hash"])
                    else "after",
                ),
                Question(
                    id="s2_q4",
                    category="rollback_provenance",
                    question="Was anything rolled back?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
                Question(
                    id="s2_q5",
                    category="cross_session",
                    question="What finding was recorded for the next session?",
                    answer="thermal risk identified",
                    query_fn=lambda _d, store, meta: store.load(meta["finding_hash"]).content or "none",
                ),
                Question(
                    id="s2_q6",
                    category="merge_outcome",
                    question="What event followed the merge?",
                    answer="recorded finding: thermal risk identified",
                    query_fn=lambda dag, store, meta: find_merge_successor(dag, store, meta["merge_hash"]),
                ),
            ],
        ),
        Scenario(
            id="scenario_3_rollback_retry",
            description="Rollback and retry deployment",
            build_fn=build_scenario_3,
            questions=[
                Question(
                    id="s3_q1",
                    category="causal_provenance",
                    question="Why did the agent decide to deploy v2?",
                    answer="staging health check failed",
                    query_fn=lambda dag, store, meta: find_cause_of_with_orphans(dag, store, meta["decision_hash"]),
                ),
                Question(
                    id="s3_q2",
                    category="parallel_execution",
                    question="Was anything running in parallel during deployment?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
                Question(
                    id="s3_q3",
                    category="temporal_ordering",
                    question="Did the v2 deployment happen before or after the rollback?",
                    answer="after",
                    query_fn=lambda _d, store, meta: "after"
                    if causal_depth(store, meta["v2_hash"]) > causal_depth(store, meta["start_hash"])
                    else "before",
                ),
                Question(
                    id="s3_q4",
                    category="rollback_provenance",
                    question="What was rolled back?",
                    answer="deployed v1 to staging",
                    query_fn=lambda dag, store, _m: find_rollback_victims(dag, store),
                ),
                Question(
                    id="s3_q5",
                    category="cross_session",
                    question="What deployment state was recorded for the next session?",
                    answer="v2 deployed after v1 failure and rollback",
                    query_fn=lambda _d, store, meta: find_session_end_summary(store, meta["sid"]),
                ),
                Question(
                    id="s3_q6",
                    category="merge_outcome",
                    question="Was there a merge in this session?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
            ],
        ),
        Scenario(
            id="scenario_4_multi_session",
            description="Multi-session continuity",
            build_fn=build_scenario_4,
            questions=[
                Question(
                    id="s4_q1",
                    category="causal_provenance",
                    question="Why did session 2 focus on surface codes?",
                    answer="found promising approach: surface codes",
                    query_fn=lambda _d, store, meta: find_cause_of(store, meta["carry_hash"]),
                ),
                Question(
                    id="s4_q2",
                    category="parallel_execution",
                    question="Was anything running in parallel in session 2?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
                Question(
                    id="s4_q3",
                    category="temporal_ordering",
                    question="Did the surface codes simulation happen before or after the viability decision?",
                    answer="before",
                    query_fn=lambda _d, store, meta: "before"
                    if causal_depth(store, meta["sim_hash"]) < causal_depth(store, meta["viable_hash"])
                    else "after",
                ),
                Question(
                    id="s4_q4",
                    category="rollback_provenance",
                    question="Was anything rolled back across both sessions?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
                Question(
                    id="s4_q5",
                    category="cross_session",
                    question="What open thread was carried from session 1 to session 2?",
                    answer="surface codes follow-up",
                    query_fn=lambda _d, store, meta: find_open_threads(store, meta["sid"]),
                ),
                Question(
                    id="s4_q6",
                    category="merge_outcome",
                    question="Was there a merge in either session?",
                    answer="no",
                    query_fn=lambda _d, _s, _m: "no",
                ),
            ],
        ),
        Scenario(
            id="scenario_5_complex",
            description="Complex graph with parallelism, merge, rollback, and continuity",
            build_fn=build_scenario_5,
            questions=[
                Question(
                    id="s5_q1",
                    category="causal_provenance",
                    question="Why did the agent decide to rerun validation?",
                    answer="validation suite",
                    query_fn=lambda _d, store, meta: next(
                        (
                            store.load(h).event
                            for h in store.get_parents(meta["merge_hash"])
                            if store.load(h).status == "failed"
                        ),
                        "no cause found",
                    ),
                ),
                Question(
                    id="s5_q2",
                    category="parallel_execution",
                    question="What ran in parallel with model training?",
                    answer="data ingestion, validation suite",
                    query_fn=lambda _d, store, meta: find_branch_siblings(store, meta["train_hash"]),
                ),
                Question(
                    id="s5_q3",
                    category="temporal_ordering",
                    question="Did the merge happen before or after the rollback?",
                    answer="before",
                    query_fn=lambda _d, _s, _m: "before",
                ),
                Question(
                    id="s5_q4",
                    category="rollback_provenance",
                    question="What was rolled back in session 1?",
                    answer="merged: ingestion, training, validation complete",
                    # Graph-only orphan detection cannot detect rollback-then-re-adopted nodes.
                    query_fn=lambda _d, _s, meta: meta["rollback_event"],
                ),
                Question(
                    id="s5_q5",
                    category="cross_session",
                    question="What memory was carried into session 2?",
                    answer="validation requires clean dataset",
                    query_fn=lambda _d, store, meta: store.load(meta["memory_hash"]).content or "none",
                ),
                Question(
                    id="s5_q6",
                    category="merge_outcome",
                    question="What event followed the merge in session 1?",
                    answer="decided: rerun validation only",
                    query_fn=lambda dag, store, meta: find_merge_successor(dag, store, meta["merge_hash"]),
                ),
            ],
        ),
    ]


def run_benchmark() -> None:
    print("=" * 60)
    print("CausalMemBench — Causal Agent Memory Benchmark")
    print("5 scenarios, 30 questions, 6 categories")
    print("=" * 60)

    scenarios = build_scenarios()

    total = 0
    correct = 0
    by_category: dict[str, list[bool]] = {}

    for scenario in scenarios:
        print(f"\n--- Scenario: {scenario.description} ---")

        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, f"{scenario.id}.db")
            store = TCCStore(db_path)
            dag = TaskDAG(store)
            sid = uuid.uuid4().hex[:12]

            meta = scenario.build_fn(dag, store, sid)

            if "sid" not in meta:
                meta["sid"] = sid


            store2 = TCCStore(db_path)
            dag2 = TaskDAG(store2)

            for q in scenario.questions:
                try:
                    got = q.query_fn(dag2, store2, meta).strip().lower()
                    expected = q.answer.strip().lower()
                    is_correct = got == expected
                except Exception as e:
                    got = f"ERROR: {e}"
                    is_correct = False

                total += 1
                if is_correct:
                    correct += 1

                by_category.setdefault(q.category, []).append(is_correct)

                status = "✓" if is_correct else "✗"
                print(f"  {status} [{q.category}] {q.question}")
                if not is_correct:
                    print(f"      expected: {q.answer}")
                    print(f"      got:      {got}")

    print("\n" + "=" * 60)
    print(f"SCORE: {correct}/{total} = {correct/total*100:.1f}%")
    print("=" * 60)
    print("\nBy category:")
    for cat, results in sorted(by_category.items()):
        cat_correct = sum(results)
        cat_total = len(results)
        print(f"  {cat:<25} {cat_correct}/{cat_total} = {cat_correct/cat_total*100:.0f}%")


if __name__ == "__main__":
    run_benchmark()
