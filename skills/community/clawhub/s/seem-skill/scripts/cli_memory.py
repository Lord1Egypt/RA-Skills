#!/usr/bin/env python3
"""
CLI for SEEM Skill - one-shot atomic operations.

Usage examples:
    python scripts/cli_memory.py store --text "Lena asked about dogs"
    python scripts/cli_memory.py store --speaker "Alice" --text "Lena asked about dogs"
    python scripts/cli_memory.py store --dialogue-id "D1:1" --speaker "Lena" --text "Asked about dogs"
    python scripts/cli_memory.py store --text "Showed image" --image-path "dog.jpg"
    python scripts/cli_memory.py recall --query "What did Lena ask?" --strategy hybrid
    python scripts/cli_memory.py stats
    python scripts/cli_memory.py clear --yes

Each invocation performs one operation and exits.
"""
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

# Add parent directory to path so we can import SEEM as a package
script_dir = os.path.dirname(os.path.abspath(__file__))
skill_root = os.path.abspath(os.path.join(script_dir, ".."))
skills_dir = os.path.abspath(os.path.join(skill_root, ".."))
if skills_dir not in sys.path:
    sys.path.insert(0, skills_dir)

from SEEM import SEEMSkill, SEEMConfig, RetrieveStrategy, RecallMode

# Default paths
DEFAULT_DATA_DIR = os.path.join(skill_root, "data")
DEFAULT_CONFIG = os.path.join(skill_root, "config", "config.py")


def load_config() -> SEEMConfig:
    """Load configuration from environment variables (preferred) or config.py fallback.
    
    Environment variables (OpenClaw injects these automatically):
    - LLM_API_KEY (required)
    - LLM_MODEL (default: qwen3.5-plus)
    - LLM_BASE_URL (default: https://api.xiaomimimo.com/v1)
    - MM_ENCODER_API_KEY (required)
    - MM_ENCODER_MODEL (default: Qwen/Qwen3-Embedding-8B)
    - MM_ENCODER_BASE_URL (default: https://api.siliconflow.cn/v1/embeddings)
    """
    # Check required environment variables
    llm_api_key = os.getenv("LLM_API_KEY")
    mm_encoder_api_key = os.getenv("MM_ENCODER_API_KEY")
    
    if not llm_api_key or not mm_encoder_api_key:
        # Fallback: try to load from config.py
        try:
            # Add skill_root to path for config import
            if skill_root not in sys.path:
                sys.path.insert(0, skill_root)
            import config as skill_config
            
            # Support both dict-style (LLM_CONFIG) and flat-style (LLM_API_KEY) configs
            if hasattr(skill_config, 'LLM_CONFIG'):
                llm_cfg = skill_config.LLM_CONFIG
                emb_cfg = skill_config.EMBEDDING_CONFIG
                defaults = getattr(skill_config, 'SEEM_DEFAULT_CONFIG', {})
                return SEEMConfig(
                    llm_api_key=llm_cfg.get("api_key", ""),
                    llm_model=llm_cfg.get("model", "mimo-v2-flash"),
                    llm_base_url=llm_cfg.get("base_url"),
                    mm_encoder_api_key=emb_cfg.get("api_key", ""),
                    mm_encoder_model=emb_cfg.get("model", "Qwen/Qwen3-Embedding-8B"),
                    mm_encoder_base_url=emb_cfg.get("base_url"),
                    retrieve_strategy=RetrieveStrategy(defaults.get("retrieve_strategy", "hybrid_rrf")),
                    top_k_candidates=defaults.get("top_k_candidates", 3),
                    top_k_chunks=defaults.get("top_k_chunks", 3),
                    backfill_chunks=defaults.get("backfill_chunks", 5),
                    rrf_rank_constant=defaults.get("rrf_rank_constant", 30),
                    enable_cache=defaults.get("enable_cache", True),
                    cache_max_size=defaults.get("cache_max_size", 1000),
                    cache_ttl_seconds=defaults.get("cache_ttl_seconds", 300),
                    enable_integration=defaults.get("enable_integration", True),
                    enable_fact_graph=defaults.get("enable_fact_graph", True),
                    entity_similarity_threshold=defaults.get("entity_similarity_threshold", 0.9)
                )
            else:
                return SEEMConfig(
                    llm_api_key=skill_config.LLM_API_KEY,
                    llm_model=getattr(skill_config, 'LLM_MODEL', 'qwen3.5-plus'),
                    llm_base_url=getattr(skill_config, 'LLM_BASE_URL', 'https://api.xiaomimimo.com/v1'),
                    mm_encoder_api_key=skill_config.MM_ENCODER_API_KEY,
                    mm_encoder_model=getattr(skill_config, 'MM_ENCODER_MODEL', 'Qwen/Qwen3-Embedding-8B'),
                    mm_encoder_base_url=getattr(skill_config, 'MM_ENCODER_BASE_URL', 'https://api.siliconflow.cn/v1/embeddings'),
                    retrieve_strategy=RetrieveStrategy(getattr(skill_config, 'RETRIEVE_STRATEGY', 'hybrid_rrf')),
                    top_k_candidates=getattr(skill_config, 'TOP_K_CANDIDATES', 3),
                    rrf_rank_constant=getattr(skill_config, 'RRF_RANK_CONSTANT', 30),
                    top_k_chunks=getattr(skill_config, 'TOP_K_CHUNKS', 3),
                    backfill_chunks=getattr(skill_config, 'BACKFILL_CHUNKS', 5),
                    enable_cache=getattr(skill_config, 'ENABLE_CACHE', True),
                    cache_max_size=getattr(skill_config, 'CACHE_MAX_SIZE', 1000),
                    cache_ttl_seconds=getattr(skill_config, 'CACHE_TTL_SECONDS', 300),
                    enable_integration=getattr(skill_config, 'ENABLE_INTEGRATION', True),
                    enable_fact_graph=getattr(skill_config, 'ENABLE_FACT_GRAPH', True),
                    entity_similarity_threshold=getattr(skill_config, 'ENTITY_SIMILARITY_THRESHOLD', 0.9)
                )
        except Exception as e:
            print(f"Error loading config: {e}")
            print("\n⚠️  API keys not found. Please set environment variables:")
            print("   export LLM_API_KEY='your-key'")
            print("   export MM_ENCODER_API_KEY='your-key'")
            print("\nOr create config/config.py from config/config.py.example")
            sys.exit(1)
    
    # Load from environment variables (OpenClaw mode)
    return SEEMConfig(
        llm_api_key=llm_api_key,
        llm_model=os.getenv("LLM_MODEL", "qwen3.5-plus"),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.xiaomimimo.com/v1"),
        mm_encoder_api_key=mm_encoder_api_key,
        mm_encoder_model=os.getenv("MM_ENCODER_MODEL", "Qwen/Qwen3-Embedding-8B"),
        mm_encoder_base_url=os.getenv("MM_ENCODER_BASE_URL", "https://api.siliconflow.cn/v1/embeddings"),
        retrieve_strategy=RetrieveStrategy(os.getenv("RETRIEVE_STRATEGY", "hybrid_rrf")),
        top_k_candidates=int(os.getenv("TOP_K_CANDIDATES", "3")),
        rrf_rank_constant=int(os.getenv("RRF_RANK_CONSTANT", "30")),
        top_k_chunks=int(os.getenv("TOP_K_CHUNKS", "3")),
        backfill_chunks=int(os.getenv("BACKFILL_CHUNKS", "5")),
        enable_cache=os.getenv("ENABLE_CACHE", "true").lower() == "true",
        cache_max_size=int(os.getenv("CACHE_MAX_SIZE", "1000")),
        cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "300")),
        enable_integration=os.getenv("ENABLE_INTEGRATION", "true").lower() == "true",
        enable_fact_graph=os.getenv("ENABLE_FACT_GRAPH", "true").lower() == "true",
        entity_similarity_threshold=float(os.getenv("ENTITY_SIMILARITY_THRESHOLD", "0.9"))
    )


def build_skill(config: SEEMConfig) -> SEEMSkill:
    """Build SEEM Skill instance"""
    return SEEMSkill(config)


def _try_cli_integration(skill: SEEMSkill, new_memory_id: str, config: SEEMConfig):
    """CLI one-shot integration: judge new memory against existing candidates.
    
    Since CLI creates a fresh SEEMSkill per invocation, the pending buffer is
    always empty.  This function manually runs the batch judge with the
    newly-stored memory as the sole pending item, using dense retrieval to
    find candidate memories for potential merging.
    """
    if new_memory_id not in skill.memories:
        return
    new_memory = skill.memories[new_memory_id]
    new_embedding = skill.memory_embeddings.get(new_memory_id)
    if new_embedding is None:
        return
    
    # Retrieve candidates via dense similarity
    candidate_ids = skill._dense_retrieve(new_embedding, top_k=config.top_k_candidates)
    candidate_ids = [cid for cid in candidate_ids if cid != new_memory_id and cid in skill.memories]
    if not candidate_ids:
        return
    
    # Build pending list and candidate map for batch judge
    pending = [(new_memory_id, new_memory)]
    candidate_map = {new_memory_id: candidate_ids}
    
    merge_groups = skill._batch_judge(pending, candidate_map)
    
    for group in merge_groups:
        members = group.get("members", [])
        if len(members) < 2:
            continue
        chunk_check = group.get("chunk_count_check", {})
        if chunk_check.get("exceeds_limit", False):
            continue
        coherence = group.get("coherence_level", "WEAK")
        if coherence not in ("STRONG", "MODERATE"):
            continue
        integrated_summary = group.get("integrated_summary", "")
        integrated_events = group.get("integrated_events", [])
        if not integrated_summary or not integrated_events:
            continue
        
        skill._merge_group(
            member_ids=members,
            integrated_summary=integrated_summary,
            integrated_events=integrated_events,
        )
        skill.stats["integration_count"] += 1
        skill.save_to_disk()
        print(f"  ✓ Integrated with: {[m[:8] for m in members if m != new_memory_id]}")
        return  # Only one merge per CLI invocation


# ==================== Store Commands ====================

def cmd_store(args):
    """Store a conversation turn"""
    config = load_config()
    skill = build_skill(config)
    
    # Build observation
    observation = {
        "text": args.text,
        "timestamp": args.timestamp or datetime.now().isoformat()
    }
    
    # Add dialogue_id if provided (auto-generated if not)
    if args.dialogue_id:
        observation["dialogue_id"] = args.dialogue_id
    
    # Add speaker if provided (defaults to "User" in skill)
    if args.speaker:
        observation["speaker"] = args.speaker
    
    # Add image if provided
    if args.image_path:
        observation["image"] = {
            "path": args.image_path,
            "img_id": args.image_id or f"img_{len(observation.get('dialogue_id', 'auto'))}",
            "caption": args.image_caption or ""
        }
    
    # Store
    try:
        memory_id = skill.store(observation)
        
        # CLI runs as one-shot process — pending state is lost between calls.
        # Force immediate integration by manually triggering the batch judge
        # with the just-stored memory against all existing memories.
        if config.enable_integration and len(skill.memories) > 1:
            try:
                _try_cli_integration(skill, memory_id, config)
            except Exception as ie:
                print(f"  [integration skipped: {ie}]")
        
        print(f"✓ Stored memory: {memory_id}")
        print(f"  Dialogue ID: {observation.get('dialogue_id', 'auto-generated')}")
        if observation.get("speaker"):
            print(f"  Speaker: {observation['speaker']}")
        if observation.get("timestamp"):
            print(f"  Timestamp: {observation['timestamp']}")
        if observation.get("image"):
            print(f"  Image: {observation['image']['img_id']}")
    except Exception as e:
        print(f"✗ Store failed: {e}")
        sys.exit(1)


# ==================== Recall Commands ====================

def cmd_recall(args):
    """Recall memories and facts"""
    config = load_config()
    
    # Override strategy if specified
    if args.strategy:
        config.retrieve_strategy = RetrieveStrategy(args.strategy)
    
    skill = build_skill(config)
    
    # Build query
    query = {"text": args.query}
    if args.image_path:
        query["image"] = {
            "path": args.image_path,
            "img_id": "query_img"
        }
    
    # Recall
    try:
        result = skill.recall(query, top_k=args.top_k, top_k_facts=args.top_k_facts,
                               mode=RecallMode(args.mode))
        memories = result["memories"]
        facts = result["facts"]
        
        # Print memory results
        print(f"--- Recall Results ({len(memories)} memories) ---\n")
        for i, mem in enumerate(memories, 1):
            print(f"[{i}] Dialogue ID: {mem['dialogue_id']}")
            print(f"    Text: {mem['text'][:300]}...")
            if mem.get('image'):
                print(f"    Image: {mem['image'].get('img_id', 'N/A')}")
            if mem.get('has_multimodal'):
                print(f"    [Multimodal]")
            print()
        
        # Print fact results
        if facts:
            print(f"--- Related Facts ({len(facts)} triples) ---\n")
            for i, fact in enumerate(facts, 1):
                score_str = f"{fact['score']:.3f}"
                time_str = f" @ {fact['time']}" if fact.get("time") else ""
                print(f"  {i}. ({score_str}) {fact['subject']} —[{fact['predicate']}]→ {fact['object']}{time_str}")
            print()
        
        print("--- End ---")
    except Exception as e:
        print(f"✗ Recall failed: {e}")
        sys.exit(1)


# ==================== Management Commands ====================

def cmd_stats(args):
    """View statistics"""
    config = load_config()
    skill = build_skill(config)
    
    stats = skill.get_stats()
    
    print("--- SEEM Skill Stats ---")
    print(f"Total stored: {stats['total_stored']}")
    print(f"Total recalled: {stats['total_recalled']}")
    print(f"Integration count: {stats['integration_count']}")
    print(f"LLM calls: {stats['llm_calls']}")
    print(f"Memory count: {stats['memory_count']}")
    print(f"Chunk count: {stats['chunk_count']}")
    print(f"Entity count: {stats['entity_count']}")
    print("--- End ---")


def cmd_clear(args):
    """Clear all memories"""
    if not args.yes:
        print("⚠️  WARNING: This will delete all memories!")
        print("Use --yes to confirm")
        sys.exit(1)
    
    config = load_config()
    skill = build_skill(config)
    
    skill.reset()
    print("✓ All memories cleared")


def cmd_info(args):
    """Show skill information"""
    print("--- SEEM Skill Information ---")
    print("Name: seem-skill")
    print("Version: 1.0.0")
    print("Description: Structured Episodic & Entity Memory")
    print()
    print("Features:")
    print("  - Episodic memory extraction (LLM)")
    print("  - Dynamic memory integration")
    print("  - Multimodal support (images)")
    print("  - Hybrid retrieval (DPR + RRF)")
    print("  - Entity linking")
    print("  - LRU cache")
    print()
    print("Retrieval Strategies:")
    print("  - DPR: Dense retrieval (~300ms)")
    print("  - Hybrid RRF: Dense + Sparse (~400ms)")
    print("  - PPR: Personalized PageRank over knowledge graph (~500ms)")
    print("--- End ---")


def cmd_display(args):
    """Display memories in human-readable format"""
    config = load_config()
    skill = build_skill(config)
    
    # Display memories
    try:
        output = skill.display_memories(
            dialogue_id=args.dialogue_id,
            format_type=args.format
        )
        print(output)
    except Exception as e:
        print(f"✗ Display failed: {e}")
        sys.exit(1)


def cmd_view(args):
    """Display memories in compact 5W1H format with rich card layout"""
    config = load_config()
    skill = build_skill(config)
    
    if not skill.memories:
        print("（无记忆）")
        return
    
    # Sort memories: those with timed events first (by earliest time), then untimed
    def _sort_key(item):
        mid, mem = item
        times = [e.get("time") for e in mem.events if e.get("time")]
        if times:
            return (0, min(times))
        return (1, mem.timestamp.isoformat() if mem.timestamp else "")
    
    sorted_memories = sorted(skill.memories.items(), key=_sort_key)
    
    for i, (mid, mem) in enumerate(sorted_memories, 1):
        # Collect all entities across events
        all_entities = []
        for event in mem.events:
            for p in event.get("participants", []):
                if p not in all_entities:
                    all_entities.append(p)
        
        # Count timed vs untimed events
        timed_events = sum(1 for e in mem.events if e.get("time"))
        total_events = len(mem.events)
        
        # Time span display
        all_times = sorted([e["time"] for e in mem.events if e.get("time")])
        if len(all_times) >= 2 and all_times[0] != all_times[-1]:
            time_display = f"{all_times[0]} → {all_times[-1]}"
        elif all_times:
            time_display = all_times[0]
        else:
            time_display = "—"
        
        # Header
        chunks = len(mem.chunk_ids)
        images = len(mem.image_ids)
        chunk_set = set(mem.chunk_ids)
        related_facts = sum(1 for f in skill.facts if f.chunk_id in chunk_set)
        meta_parts = [f"{chunks} chunk{'s' if chunks != 1 else ''}"]
        if images:
            meta_parts.append(f"{images} image{'s' if images != 1 else ''}")
        meta_parts.append(f"{total_events} event{'s' if total_events != 1 else ''}")
        if related_facts:
            meta_parts.append(f"{related_facts} fact{'s' if related_facts != 1 else ''}")
        meta_info = " · ".join(meta_parts)
        
        print(f"┌─ Memory #{i}  [{mid[:12]}…]")
        print(f"│")
        print(f"│  📝 {mem.summary}")
        print(f"│")
        print(f"│  🕐 {time_display}    👤 {', '.join(all_entities) if all_entities else '—'}")
        print(f"│  📊 {meta_info}")
        print(f"│")
        
        # Events: sort timed first, then untimed
        sorted_events = sorted(mem.events, key=lambda e: (e.get("time") is None, e.get("time") or ""))
        
        for j, event in enumerate(sorted_events, 1):
            w = event.get("participants")
            h = event.get("action")
            t = event.get("time")
            r = event.get("location")
            y = event.get("reason")
            m = event.get("method")
            
            # Event header with time badge
            time_badge = f"  ⏱ {t}" if t else "  ⏱ —"
            print(f"│  ┌─ Event {j}{time_badge}")
            
            if w:
                print(f"│  │  👤 {', '.join(w)}")
            if h:
                for action in h:
                    print(f"│  │  🎯 {action}")
            if r:
                print(f"│  │  📍 {r}")
            if y:
                print(f"│  │  ❓ {y}")
            if m:
                print(f"│  │  🔧 {m}")
            
            print(f"│  └{'─' * 46}")
        
        # Original utterances (compact)
        if chunks > 0:
            print(f"│")
            print(f"│  💬 Original utterances:")
            for cid in mem.chunk_ids[:3]:
                chunk_data = skill.chunk_store.get(cid, {})
                speaker = chunk_data.get("speaker", "?")
                text = chunk_data.get("text", "")
                preview = text[:60] + ("…" if len(text) > 60 else "")
                print(f"│    [{speaker}] {preview}")
            if chunks > 3:
                print(f"│    … and {chunks - 3} more")
        
        print(f"└{'─' * 50}")
        print()
    
    # Summary footer
    total_events = sum(len(m.events) for m in skill.memories.values())
    total_entities = set()
    for m in skill.memories.values():
        for e in m.events:
            total_entities.update(e.get("participants", []))
    timed = sum(1 for m in skill.memories.values() for e in m.events if e.get("time"))
    
    print(f"╭{'─' * 48}╮")
    print(f"│  共 {len(skill.memories)} 条记忆 · {total_events} 个事件 · {len(total_entities)} 个实体  │")
    print(f"│  {timed}/{total_events} 事件有时间标注 · {len(skill.chunk_store)} 条原始记录  │")
    print(f"╰{'─' * 48}╯")


def cmd_facts(args):
    """Display all fact triples and graph statistics using NetworkX"""
    import networkx as nx

    config = load_config()
    skill = build_skill(config)

    G = skill.nx_graph

    # Graph statistics
    print(f"{'═' * 60}")
    print(f"  📊 Graph Overview")
    print(f"{'═' * 60}")
    print(f"  Nodes: {G.number_of_nodes()}  |  Edges: {G.number_of_edges()}")

    if G.number_of_nodes() > 0:
        # Node type breakdown
        node_types: dict = {}
        for _, attrs in G.nodes(data=True):
            nt = attrs.get("node_type", "unknown")
            node_types[nt] = node_types.get(nt, 0) + 1
        type_str = "  |  ".join(f"{nt}: {cnt}" for nt, cnt in sorted(node_types.items()))
        print(f"  Types: {type_str}")

        # Edge type breakdown
        edge_types: dict = {}
        for _, _, attrs in G.edges(data=True):
            et = attrs.get("edge_type", "unknown")
            edge_types[et] = edge_types.get(et, 0) + 1
        etype_str = "  |  ".join(f"{et}: {cnt}" for et, cnt in sorted(edge_types.items()))
        print(f"  Edge types: {etype_str}")

        # Connected components (on undirected version)
        undirected = G.to_undirected()
        num_components = nx.number_connected_components(undirected)
        print(f"  Connected components: {num_components}")

        # Top entities by degree
        entity_nodes = [(n, d) for n, d in G.degree() if G.nodes[n].get("node_type") == "entity"]
        if entity_nodes:
            entity_nodes.sort(key=lambda x: x[1], reverse=True)
            top_entities = entity_nodes[:10]
            print(f"  Top entities by degree: {', '.join(f'{n}({d})' for n, d in top_entities)}")
    print()

    # Fact triples
    if not skill.facts:
        print("（无事实三元组）")
        return

    # Optional: filter by entity name
    filter_entity = args.entity.lower().strip() if args.entity else None

    # Group facts by subject for cleaner display
    subject_groups: dict = {}
    for fact in skill.facts:
        if filter_entity and filter_entity not in fact.subject.lower() and filter_entity not in fact.obj.lower():
            continue
        key = fact.subject
        if key not in subject_groups:
            subject_groups[key] = []
        subject_groups[key].append(fact)

    print(f"{'═' * 60}")
    print(f"  🔗 Fact Triples — {len(skill.facts)} total")
    if filter_entity:
        print(f"  Filtered by: {filter_entity}")
    print(f"{'═' * 60}")
    print()

    for subject in sorted(subject_groups.keys()):
        facts_for_subject = subject_groups[subject]
        print(f"  🔹 {subject}")
        for fact in sorted(facts_for_subject, key=lambda f: f.obj):
            time_str = f"  ⏱ {fact.time}" if fact.time else ""
            conf_str = f"  ({fact.confidence:.0%})" if fact.confidence < 1.0 else ""
            print(f"      ──[{fact.predicate}]──▸ {fact.obj}{time_str}{conf_str}")
        print()

    print(f"{'─' * 60}")


# ==================== Main ====================

def main():
    parser = argparse.ArgumentParser(
        description="SEEM Skill CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s store --text "Lena asked about dogs"
  %(prog)s store --speaker "Alice" --text "Lena asked about dogs"
  %(prog)s store --dialogue-id "D1:1" --speaker "Lena" --text "Asked about dogs"
  %(prog)s store --text "Showed image" --image-path "dog.jpg"
  %(prog)s recall --query "What did Lena ask?" --strategy hybrid
  %(prog)s view                           # Compact 5W1H view
  %(prog)s display                        # Detailed display
  %(prog)s display --dialogue-id "D1:1"   # Display specific dialogue
  %(prog)s stats
  %(prog)s clear --yes
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    # Store command
    p_store = subparsers.add_parser("store", help="Store a conversation turn")
    p_store.add_argument("--dialogue-id", help="Dialogue ID (e.g., D1:1, auto-generated if not provided)")
    p_store.add_argument("--speaker", default="user", help="Speaker name (e.g., Alice, Bob, default 'user')")
    p_store.add_argument("--text", required=True, help="Conversation text")
    p_store.add_argument("--timestamp", help="ISO 8601 timestamp (optional)")
    p_store.add_argument("--image-path", help="Image file path (optional)")
    p_store.add_argument("--image-id", help="Image ID (optional)")
    p_store.add_argument("--image-caption", help="Image caption (optional)")
    p_store.set_defaults(func=cmd_store)
    
    # Recall command
    p_recall = subparsers.add_parser("recall", help="Recall memories")
    p_recall.add_argument("--query", required=True, help="Search query")
    p_recall.add_argument("--strategy", choices=["dpr", "hybrid_rrf", "ppr"], help="Retrieval strategy")
    p_recall.add_argument("--mode", choices=["lite", "pro", "max"], default="lite",
                          help="Recall mode: lite (facts+memory), pro (+chunks), max (+backfill)")
    p_recall.add_argument("--top-k", type=int, default=5, help="Number of results")
    p_recall.add_argument("--top-k-facts", type=int, default=5, help="Number of fact triples to retrieve")
    p_recall.add_argument("--image-path", help="Query image path (optional)")
    p_recall.set_defaults(func=cmd_recall)
    
    # Stats command
    p_stats = subparsers.add_parser("stats", help="View statistics")
    p_stats.set_defaults(func=cmd_stats)
    
    # Clear command
    p_clear = subparsers.add_parser("clear", help="Clear all memories")
    p_clear.add_argument("--yes", action="store_true", help="Confirm deletion")
    p_clear.set_defaults(func=cmd_clear)
    
    # Info command
    p_info = subparsers.add_parser("info", help="Show skill information")
    p_info.set_defaults(func=cmd_info)
    
    # Display command
    p_display = subparsers.add_parser("display", help="Display memories in human-readable format")
    p_display.add_argument("--dialogue-id", help="Filter by dialogue ID (optional)")
    p_display.add_argument("--format", choices=["readable", "structured"], default="readable", 
                          help="Output format (default: readable)")
    p_display.set_defaults(func=cmd_display)
    
    # View command (compact 5W1H)
    p_view = subparsers.add_parser("view", help="Display memories in compact 5W1H format")
    p_view.set_defaults(func=cmd_view)

    # Facts command (knowledge graph triples)
    p_facts = subparsers.add_parser("facts", help="Display all fact triples in the knowledge graph")
    p_facts.add_argument("--entity", help="Filter by entity name (optional)")
    p_facts.set_defaults(func=cmd_facts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
