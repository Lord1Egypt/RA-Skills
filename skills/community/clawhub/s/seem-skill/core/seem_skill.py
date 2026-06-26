"""SEEM Skill Core Implementation
Simplified Episodic Embedding Memory for OpenClaw
"""

import json
import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime
import networkx as nx

from .schema import (
    EpisodicMemory, SEEMConfig, RecallResult, RetrieveStrategy, RecallMode, GraphNode, GraphEdge, Fact
)
from .prompts import (
    EPISODIC_EXTRACTION_SYSTEM_PROMPT,
    QUERY_5W1H_SYSTEM_PROMPT,
    FACT_EXTRACTION_SYSTEM_PROMPT,
    format_5w1h_text
)
from .utils import (
    LLMClient, MMEmbedEncoder, BM25Retriever, LRUCache,
    cosine_similarity, batch_cosine_similarity,
    generate_memory_id, format_structured_text
)


class SEEMSkill:
    """
    Simplified SEEM Skill
    Core features: Episodic memory extraction + Dynamic integration + Multimodal retrieval
    """
    
    def __init__(self, config: SEEMConfig):
        """
        Initialize SEEM Skill
        
        Args:
            config: SEEM configuration
        """
        self.config = config
        
        # Initialize LLM client
        self.llm = LLMClient(
            api_key=config.llm_api_key,
            model=config.llm_model,
            base_url=config.llm_base_url
        )
        
        # Initialize multimodal encoder
        self.mm_encoder = MMEmbedEncoder(
            api_key=config.mm_encoder_api_key,
            model=config.mm_encoder_model,
            base_url=config.mm_encoder_base_url
        )
        
        # Core storage
        self.memories: Dict[str, EpisodicMemory] = {}  # memory_id -> EpisodicMemory
        self.memory_embeddings: Dict[str, np.ndarray] = {}  # memory_id -> embedding
        self.chunk_store: Dict[str, Dict[str, Any]] = {}  # chunk_id -> observation
        self.chunk_embeddings: Dict[str, np.ndarray] = {}  # chunk_id -> embedding
        
        # Graph structure storage
        # Graph structure (NetworkX)
        self.nx_graph = nx.DiGraph()  # Unified graph: nodes have 'node_type' + metadata; edges have 'edge_type' + weight + metadata
        self.node_to_memory_ids: Dict[str, Set[str]] = {}  # entity_node_id -> {memory_id}
        self.node_to_chunk_ids: Dict[str, Set[str]] = {}  # entity_node_id -> {chunk_id}
        
        # BM25 corpus (for Hybrid RRF)
        self.bm25_documents: Dict[str, str] = {}  # memory_id -> BM25 document text
        self.chunk_bm25_documents: Dict[str, str] = {}  # chunk_id -> BM25 document text
        self.bm25_retriever: Optional[BM25Retriever] = None
        self.chunk_bm25_retriever: Optional[BM25Retriever] = None
        
        # Entity storage (for entity linking)
        self.entity_embeddings: Dict[str, np.ndarray] = {}  # entity_name -> embedding
        self.entity_map: Dict[str, str] = {}  # surface_form -> canonical_entity_id
        
        # Fact storage (for Fact graph retrieval)
        self.facts: List[Fact] = []  # List of all facts
        self.fact_embeddings: Dict[int, np.ndarray] = {}  # fact_index -> embedding
        self._fact_norm_set: Set[str] = set()  # Normalized (subject,predicate,object) for exact dedup
        self.entity_store_order: List[str] = []  # Entity storage order (for synonymy edge retrieval)
        
        # Cache
        self.cache = LRUCache(
            max_size=config.cache_max_size,
            ttl_seconds=config.cache_ttl_seconds
        ) if config.enable_cache else None

        # ----------------------------------------------------------
        # Deferred Integration State (Strategy C - Batched Window)
        #
        # Instead of running integration (LLM judge + merge) on every
        # single observation, we accumulate observations into a pending
        # queue.  Once `integration_window` observations have been
        # buffered, a single LLM batch-judgment pass decides how to
        # merge them (intra-window + inter-window with existing memories).
        # ----------------------------------------------------------
        self._pending_count: int = 0                 # observations buffered since last flush
        self._pending_memory_ids: List[str] = []     # memory_ids in FIFO order

        # Statistics
        self.stats = {
            "total_stored": 0,
            "total_recalled": 0,
            "integration_count": 0,
            "llm_calls": 0,
            "fact_count": 0,
            "entity_count": 0
        }
        
        # Auto-load persistent data
        if config.enable_cache:  # Use enable_cache as persistence switch
            self.load_from_disk()
    
    def store(self, observation: Dict[str, Any]) -> str:
        """
        Store single conversation turn
        
        Args:
            observation: Conversation turn data
                {
                    "dialogue_id": str (optional, auto-generated if not provided),
                    "speaker": str (optional, default "user"),
                    "text": str,
                    "image": {"path": str, "img_id": str, "caption": str} (optional),
                    "timestamp": str (optional, auto-generated if not provided)
                }
        
        Returns:
            memory_id: Stored memory ID
        """
        # 1. Auto-generate dialogue_id (if not provided)
        import uuid
        chunk_id = observation.get("dialogue_id", f"auto_{uuid.uuid4().hex[:12]}")
        
        # 2. Extract speaker (default "user", lowercase for consistency)
        speaker = observation.get("speaker", "user")
        
        # 3. Auto-generate timestamp (if not provided)
        timestamp = observation.get("timestamp")
        if timestamp is None:
            from datetime import datetime
            timestamp = datetime.now().isoformat()
        
        # 4. Build standardized chunk data
        chunk_data = {
            "dialogue_id": chunk_id,
            "speaker": speaker,
            "text": observation["text"],
            "image": observation.get("image"),
            "timestamp": timestamp,
        }
        
        # 5. Store chunk
        self.chunk_store[chunk_id] = chunk_data
        
        # 2. Episodic memory extraction
        memory = self._extract_episodic_memory(observation, chunk_id)
        
        # 3. Compute multimodal embedding
        embedding = self._compute_memory_embedding(memory, observation)
        
        # 4. Store memory immediately (extraction + embedding always runs per observation)
        #
        # DEFERRED INTEGRATION (Strategy C):
        # We skip per-observation integration and instead buffer memory_ids.
        # When `integration_window` observations have accumulated, a single
        # batch LLM call decides how to merge them all at once.
        # This amortises the expensive LLM-judge cost over w observations.
        memory_id = self._add_memory(memory, embedding)

        # 5. Track pending integration
        if self.config.enable_integration:
            self._pending_count += 1
            self._pending_memory_ids.append(memory_id)

            # Trigger batch integration when the window is full
            if self._pending_count >= self.config.integration_window:
                self._flush_integrations()
        
        # 5. Update statistics
        self.stats["total_stored"] += 1
        
        # Auto-save
        if self.config.enable_cache:
            self.save_to_disk()
        
        return memory_id
    
    def recall(self, query: Dict[str, Any], top_k: Optional[int] = None,
               top_k_facts: Optional[int] = None,
               mode: RecallMode = RecallMode.LITE) -> Dict[str, Any]:
        """
        Retrieve relevant memories and facts

        Args:
            query: Query data {"text": str, "image": {...} (optional)}
            top_k: Number of chunks to retrieve (default uses config.top_k_chunks)
            top_k_facts: Number of fact triples to retrieve (default uses config.top_k_facts)
            mode: Recall mode controlling what is returned as context
                - LITE:  Facts + episodic memory (summary+events). No raw chunks.
                - PRO:   Facts + episodic memory + top_k raw chunks. No backfill.
                - MAX:   Facts + episodic memory + top_k raw chunks + backfill (up to 2×top_k).

        Returns:
            {"memories": [...], "facts": [...]}
        """
        # Auto-flush
        if self._pending_count > 0:
            self._flush_integrations()

        # Encode query
        query_text = query.get("text", "")
        if self.cache:
            cache_key = f"query_embedding:{hash(query_text)}"
            query_embedding = self.cache.get(cache_key)
            if query_embedding is None:
                query_embedding = self.mm_encoder.encode_text(query_text)
                self.cache.put(cache_key, query_embedding)
        else:
            query_embedding = self.mm_encoder.encode_text(query_text)

        # Retrieve top_k chunks by strategy
        top_k = top_k or self.config.top_k_chunks
        if self.config.retrieve_strategy == RetrieveStrategy.HYBRID_RRF:
            retrieved_chunks = self._retrieve_chunks_hybrid_rrf(query, top_k, query_embedding)
        elif self.config.retrieve_strategy == RetrieveStrategy.PPR:
            retrieved_chunks = self._retrieve_chunks_ppr(query, top_k, query_embedding)
        else:
            retrieved_chunks = self._retrieve_chunks_dpr(query, top_k, query_embedding)

        # Build recall results based on mode
        memory_results = self._build_recall_results(retrieved_chunks, top_k, mode)

        # Retrieve facts
        top_k_facts = top_k_facts if top_k_facts is not None else self.config.top_k_facts
        fact_results = self._retrieve_top_facts(query_embedding, top_k=top_k_facts)

        # Update statistics
        self.stats["total_recalled"] += 1

        # Auto-save
        if self.config.enable_cache:
            self.save_to_disk()

        return {
            "memories": memory_results,
            "facts": fact_results,
        }
    
    def reset(self):
        """Reset all state"""
        self.memories.clear()
        self.memory_embeddings.clear()
        self.chunk_store.clear()
        self.chunk_embeddings.clear()
        self.nx_graph.clear()
        self.node_to_memory_ids.clear()
        self.node_to_chunk_ids.clear()
        self.bm25_documents.clear()
        self.chunk_bm25_documents.clear()
        self.bm25_retriever = None
        self.entity_embeddings.clear()
        self.entity_map.clear()
        self.facts.clear()
        self.fact_embeddings.clear()
        self._fact_norm_set.clear()
        self.entity_store_order.clear()
        # Clear pending integration state
        self._pending_count = 0
        self._pending_memory_ids = []
        if self.cache:
            self.cache.clear()
        self.stats = {
            "total_stored": 0,
            "total_recalled": 0,
            "integration_count": 0,
            "llm_calls": 0,
            "fact_count": 0,
            "entity_count": 0
        }
        
        # Clean persistent data
        if self.config.enable_cache:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            if os.path.exists(data_dir):
                import shutil
                shutil.rmtree(data_dir)
                os.makedirs(data_dir, exist_ok=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            **self.stats,
            "memory_count": len(self.memories),
            "chunk_count": len(self.chunk_store),
            "entity_count": len(self.entity_embeddings),
            "fact_count": len(self.facts)
        }
    
    def display_memories(self, dialogue_id: Optional[str] = None, format_type: str = "readable") -> str:
        """
        Display memories in human-readable format with entity summaries and time-sorted events.
        
        Args:
            dialogue_id: Optional dialogue ID to filter memories (if None, display all)
            format_type: Output format - "readable" (human-readable) or "structured" (detailed)
        
        Returns:
            Formatted string representation of memories
        """
        if not self.memories:
            return "No memories stored yet."
        
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("SEEM Episodic Memory Display")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        # Collect memories to display
        memories_to_display = []
        for memory in self.memories.values():
            if dialogue_id:
                for chunk_id in memory.chunk_ids:
                    chunk_data = self.chunk_store.get(chunk_id, {})
                    if chunk_data.get("dialogue_id") == dialogue_id:
                        memories_to_display.append(memory)
                        break
            else:
                memories_to_display.append(memory)
        
        if not memories_to_display:
            if dialogue_id:
                return f"No memories found for dialogue ID: {dialogue_id}"
            else:
                return "No memories to display."
        
        # Sort: timed events first (by earliest event time), then untimed (by memory timestamp)
        def _sort_key(memory):
            times = [e.get("time") for e in memory.events if e.get("time")]
            if times:
                return (0, min(times))
            return (1, memory.timestamp.isoformat() if memory.timestamp else "")
        
        memories_to_display.sort(key=_sort_key)
        
        for idx, memory in enumerate(memories_to_display, 1):
            # Gather all entities
            all_entities = []
            for event in memory.events:
                for p in event.get("participants", []):
                    if p not in all_entities:
                        all_entities.append(p)
            
            # Time span
            all_times = sorted([e["time"] for e in memory.events if e.get("time")])
            if len(all_times) >= 2 and all_times[0] != all_times[-1]:
                time_span = f"{all_times[0]} → {all_times[-1]}"
            elif all_times:
                time_span = all_times[0]
            else:
                time_span = "—"
            
            # Header
            output_lines.append(f"[Memory {idx}] ID: {memory.memory_id}")
            output_lines.append("-" * 80)
            output_lines.append(f"  🕐 {time_span}    👤 {', '.join(all_entities) if all_entities else '—'}")
            output_lines.append("")
            
            # Summary
            output_lines.append("  🧠 Episodic Summary:")
            output_lines.append(f"    {memory.summary}")
            output_lines.append("")
            
            # Events (sorted: timed first)
            if memory.events:
                sorted_events = sorted(memory.events, key=lambda e: (e.get("time") is None, e.get("time") or ""))
                output_lines.append(f"  📋 Events ({len(memory.events)}):")
                for event_idx, event in enumerate(sorted_events, 1):
                    time_badge = f"⏱ {event['time']}" if event.get("time") else "⏱ —"
                    output_lines.append(f"    Event {event_idx}  [{time_badge}]")
                    if event.get("participants"):
                        output_lines.append(f"      👤 {', '.join(event['participants'])}")
                    if event.get("action"):
                        for action in event["action"]:
                            output_lines.append(f"      🎯 {action}")
                    if event.get("location"):
                        output_lines.append(f"      📍 {event['location']}")
                    if event.get("reason"):
                        output_lines.append(f"      ❓ {event['reason']}")
                    if event.get("method"):
                        output_lines.append(f"      🔧 {event['method']}")
                    output_lines.append("")
            
            # Related facts
            chunk_set = set(memory.chunk_ids)
            related_facts = [f for f in self.facts if f.chunk_id in chunk_set]
            if related_facts:
                output_lines.append(f"  🔗 Facts ({len(related_facts)}):")
                for fact in related_facts[:10]:
                    time_str = f" @ {fact.time}" if fact.time else ""
                    output_lines.append(f"    {fact.subject} —[{fact.predicate}]→ {fact.obj}{time_str}")
                if len(related_facts) > 10:
                    output_lines.append(f"    ... and {len(related_facts) - 10} more")
                output_lines.append("")

            # All original utterances
            if memory.chunk_ids:
                output_lines.append(f"  💬 Original Utterances ({len(memory.chunk_ids)}):")
                for chunk_id in memory.chunk_ids:
                    chunk_data = self.chunk_store.get(chunk_id, {})
                    speaker = chunk_data.get("speaker", "?")
                    text = chunk_data.get("text", "")
                    ts = chunk_data.get("timestamp", "")
                    ts_short = ts[:10] if ts else ""
                    preview = text[:80] + ("…" if len(text) > 80 else "")
                    output_lines.append(f"    [{ts_short}] <{speaker}> {preview}")
                output_lines.append("")
            
            # Images
            if memory.image_ids:
                output_lines.append(f"  🖼️  Images: {', '.join(memory.image_ids)}")
                output_lines.append("")
            
            output_lines.append("")
        
        # Global summary
        total_events = sum(len(m.events) for m in self.memories.values())
        all_entities_global = set()
        for m in self.memories.values():
            for e in m.events:
                all_entities_global.update(e.get("participants", []))
        timed_events = sum(1 for m in self.memories.values() for e in m.events if e.get("time"))
        
        output_lines.append("=" * 80)
        output_lines.append(f"Total: {len(memories_to_display)} memories | {total_events} events | {len(all_entities_global)} entities | {len(self.facts)} facts")
        output_lines.append(f"Time coverage: {timed_events}/{total_events} events have timestamps | {len(self.chunk_store)} raw observations")
        output_lines.append("=" * 80)
        
        return "\n".join(output_lines)
    
    # ========== Internal Methods ==========
    
    def _extract_episodic_memory(self, observation: Dict[str, Any], chunk_id: str) -> EpisodicMemory:
        """
        Extract episodic memory from observation (single LLM call)
        
        Args:
            observation: Conversation turn data (with speaker field)
            chunk_id: Chunk ID
            
        Returns:
            EpisodicMemory object
        """
        # Build Prompt
        speaker = observation.get("speaker", "User")
        text = observation.get("text", "")
        image_caption = observation.get("image", {}).get("caption", "") if observation.get("image") else ""
        
        # Build input text (with speaker information)
        input_text = f"[{speaker}]: {text}"
        if image_caption:
            input_text += f"\n[Image: {image_caption}]"
        
        # Include conversation timestamp for relative time resolution
        timestamp = observation.get("timestamp", datetime.now().isoformat())
        user_prompt = f"Conversation timestamp: {timestamp}\n\nExtract episodic memory from the following conversation turn:\n\n{input_text}"
        
        # LLM call
        try:
            result = self.llm.generate(
                system_prompt=EPISODIC_EXTRACTION_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
            self.stats["llm_calls"] += 1
            
            # Parse JSON
            data = json.loads(result)
            
            # Validate events: ensure action count ≤ MAX_ACTIONS_PER_EVENT
            validated_events = self._validate_events(data.get("events", []))
            
            memory = EpisodicMemory(
                memory_id=generate_memory_id(),
                chunk_ids=[chunk_id],
                summary=data["summary"],
                events=validated_events,
                image_ids=[observation["image"]["img_id"]] if observation.get("image") else [],
                timestamp=datetime.now()
            )
        except Exception as e:
            # Fallback: Use text summary
            print(f"Warning: Episodic extraction failed, using fallback: {str(e)}")
            memory = EpisodicMemory(
                memory_id=generate_memory_id(),
                chunk_ids=[chunk_id],
                summary=text[:self.config.fallback_summary_length],
                events=[],
                image_ids=[observation["image"]["img_id"]] if observation.get("image") else [],
                timestamp=datetime.now()
            )
        
        return memory
    
    def _compute_memory_embedding(self, memory: EpisodicMemory, observation: Dict[str, Any]) -> np.ndarray:
        """Calculate multimodal fusion embedding"""
        # Format structured text
        text = format_structured_text(memory.summary, memory.events)
        
        # Multimodal encoding
        image_path = observation.get("image", {}).get("path") if observation.get("image") else None
        
        if self.cache:
            # Check cache
            cache_key = f"embedding:{hash(text + str(image_path))}"
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        # Calculate embedding
        if image_path:
            embedding = self.mm_encoder.encode_multimodal(text=text, image_path=image_path)
        else:
            embedding = self.mm_encoder.encode_text(text=text)
        
        # Cache
        if self.cache:
            self.cache.put(cache_key, embedding)
        
        return embedding
    
    # Constraint constants
    MAX_CHUNKS_PER_MEMORY = 10  # Maximum chunks per memory
    MAX_ACTIONS_PER_EVENT = 5   # Maximum actions per event

    # ================================================================
    # Batch Integration (Strategy C)
    # ================================================================
    # A single LLM call judges ALL pending memories at once, deciding
    # merge groups that may span:
    #   - intra-window:  pending ↔ pending  (internal integration)
    #   - inter-window:  pending ↔ existing  (external integration)
    # ================================================================

    def flush(self):
        """Public API: force-flush all pending integrations immediately.

        Call this before any external operation (recall, save, shutdown)
        that expects a fully-consistent memory graph.
        """
        if self._pending_count > 0:
            self._flush_integrations()

    def _reset_pending(self):
        """Clear the pending integration buffer after a flush."""
        self._pending_count = 0
        self._pending_memory_ids = []

    def _flush_integrations(self):
        """Execute batched integration for all pending memories (Strategy C).

        Workflow
        --------
        1. Collect the w pending memory_ids that still exist in self.memories
           (some may have been deleted by a prior manual flush).
        2. For each pending memory, run dense_retrieve against the FULL
           self.memories pool — this naturally includes:
             - older (pre-window) memories  → external integration candidates
             - other pending memories       → internal integration candidates
        3. Send ALL pending memories + their candidates to the LLM in ONE
           batch call.  The LLM returns a partition of merge groups.
        4. Execute each merge group that has ≥2 members.

        Complexity
        ----------
        - Dense retrieval: w × O(N) cosine similarities  (vector ops, cheap)
        - LLM calls:       1 batch call                  (vs w sequential calls)
        """
        # ---- Step 1: Collect surviving pending memories ----
        pending = []
        for mid in self._pending_memory_ids:
            if mid in self.memories:
                pending.append((mid, self.memories[mid]))

        if not pending:
            self._reset_pending()
            return

        # ---- Step 2: Candidate retrieval for each pending memory ----
        # Dense retrieve runs against self.memories, which already contains
        # ALL pending memories (they were added via _add_memory during store).
        # So candidates naturally include both intra-window and inter-window memories.
        candidate_map: Dict[str, List[str]] = {}
        for mid, memory in pending:
            embedding = self.memory_embeddings.get(mid)
            if embedding is None:
                continue
            candidate_ids = self._dense_retrieve(embedding, top_k=self.config.top_k_candidates)
            # Exclude self; keep only valid existing memories
            candidate_ids = [cid for cid in candidate_ids if cid != mid and cid in self.memories]
            candidate_map[mid] = candidate_ids

        # ---- Step 3: Single LLM batch judgment ----
        merge_groups = self._batch_judge(pending, candidate_map)

        # ---- Step 4: Execute merge groups ----
        merged_ids: Set[str] = set()
        for group in merge_groups:
            members = group.get("members", [])
            if len(members) < 2:
                # Singleton — nothing to merge
                continue

            chunk_check = group.get("chunk_count_check", {})
            if chunk_check.get("exceeds_limit", False):
                print(f"[flush] Merge group {members} exceeds chunk limit, skipping")
                continue

            coherence = group.get("coherence_level", "WEAK")
            if coherence not in ("STRONG", "MODERATE"):
                continue

            integrated_summary = group.get("integrated_summary", "")
            integrated_events = group.get("integrated_events", [])

            if not integrated_summary or not integrated_events:
                # LLM returned empty merge output — skip
                continue

            self._merge_group(
                member_ids=members,
                integrated_summary=integrated_summary,
                integrated_events=integrated_events,
            )
            merged_ids.update(members)

        # ---- Done: reset pending buffer ----
        self._reset_pending()

    def _batch_judge(
        self,
        pending: List[Tuple[str, "EpisodicMemory"]],
        candidate_map: Dict[str, List[str]],
    ) -> List[Dict[str, Any]]:
        """Single LLM call that judges ALL pending memories at once.

        Args:
            pending:        [(pending_id, EpisodicMemory), ...]  pending_id = original memory_id
            candidate_map:  {pending_id → [candidate_memory_ids]}

        Returns:
            List of merge-group dicts as returned by the LLM.
            Each dict has: members, coherence_level, chunk_count_check,
                           integrated_summary, integrated_events.
        """
        from .prompts import BATCH_JUDGE_INTEGRATE_SYSTEM_PROMPT

        # ---- Build compact prompt input ----
        # Pending memories use synthetic labels (p1, p2, …) so the LLM
        # can refer to them concisely.  We maintain a mapping back to
        # real memory_ids.
        label_to_id: Dict[str, str] = {}   # "p1" → real memory_id
        id_to_label: Dict[str, str] = {}   # real memory_id → "p1"

        sections: List[str] = []

        # --- Pending section ---
        sections.append("=== PENDING MEMORIES (window of new observations) ===\n")
        for idx, (mid, mem) in enumerate(pending, 1):
            label = f"p{idx}"
            label_to_id[label] = mid
            id_to_label[mid] = label

            obs_list = self._get_all_observations_for_memory(mem)
            formatted = self._format_memory_for_judge(mem, obs_list)
            sections.append(f"PENDING [pending_id={label}, real_id={mid}]:\n{formatted}\n")

        # --- Candidate section ---
        # Deduplicate: a candidate may appear for multiple pending memories
        seen_candidates: Set[str] = set()
        all_candidates: List[Tuple[str, "EpisodicMemory"]] = []

        for mid, cand_ids in candidate_map.items():
            for cid in cand_ids:
                if cid not in seen_candidates and cid in self.memories:
                    seen_candidates.add(cid)
                    all_candidates.append((cid, self.memories[cid]))

        if all_candidates:
            sections.append("=== EXISTING CANDIDATE MEMORIES ===\n")
            for cid, mem in all_candidates:
                obs_list = self._get_all_observations_for_memory(mem)
                formatted = self._format_memory_for_judge(mem, obs_list)
                sections.append(f"CANDIDATE [memory_id={cid}]:\n{formatted}\n")

        user_prompt = "\n".join(sections)

        # ---- LLM call ----
        try:
            result_text = self.llm.generate(
                system_prompt=BATCH_JUDGE_INTEGRATE_SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )
            self.stats["llm_calls"] += 1

            raw_groups = json.loads(result_text).get("merge_groups", [])

            # ---- Post-processing: resolve labels → real IDs ----
            resolved_groups: List[Dict[str, Any]] = []
            for grp in raw_groups:
                members = grp.get("members", [])
                real_members: List[str] = []
                for m in members:
                    if m in label_to_id:
                        real_members.append(label_to_id[m])
                    elif m in self.memories:
                        # LLM used the real memory_id directly (candidate)
                        real_members.append(m)
                    else:
                        print(f"[batch_judge] Warning: unknown member ID '{m}', skipping")

                if real_members:
                    grp["members"] = real_members
                    resolved_groups.append(grp)

            return resolved_groups

        except Exception as e:
            print(f"[batch_judge] Warning: batch judgment failed: {e}")
            # Fallback: treat each pending memory as a singleton (no merge)
            return [{"members": [mid], "coherence_level": "WEAK",
                     "chunk_count_check": {}, "integrated_summary": "",
                     "integrated_events": []}
                    for mid, _ in pending]

    def _merge_group(
        self,
        member_ids: List[str],
        integrated_summary: str,
        integrated_events: List[Dict[str, Any]],
    ):
        """Merge a group of memories into a single new memory.

        Args:
            member_ids:          Real memory_ids to merge (both pending and candidate).
            integrated_summary:  LLM-produced merged summary.
            integrated_events:   LLM-produced merged events.

        Side effects:
            - Creates a new EpisodicMemory with a fresh memory_id.
            - Deletes all member memories from self.memories / embeddings / BM25.
            - The new memory inherits all chunk_ids from members.
            - Rebuilds BM25 index and graph links.
        """
        # Validate that all member_ids exist
        valid_ids = [mid for mid in member_ids if mid in self.memories]
        if len(valid_ids) < 2:
            # Nothing to merge (members were already deleted by a prior merge)
            return

        # ---- Aggregate chunk_ids and image_ids ----
        all_chunk_ids: List[str] = []
        all_image_ids: List[str] = []
        for mid in valid_ids:
            mem = self.memories[mid]
            all_chunk_ids.extend(mem.chunk_ids)
            all_image_ids.extend(mem.image_ids)

        # Deduplicate while preserving order
        all_chunk_ids = list(dict.fromkeys(all_chunk_ids))
        all_image_ids = list(dict.fromkeys(all_image_ids))

        # Safety: enforce chunk limit
        if len(all_chunk_ids) > self.MAX_CHUNKS_PER_MEMORY:
            print(f"[merge_group] Warning: truncating {len(all_chunk_ids)} chunks → {self.MAX_CHUNKS_PER_MEMORY}")
            all_chunk_ids = all_chunk_ids[:self.MAX_CHUNKS_PER_MEMORY]

        # Validate events
        integrated_events = self._validate_events(integrated_events)

        # ---- Build new merged memory ----
        new_memory = EpisodicMemory(
            memory_id=generate_memory_id(),
            chunk_ids=all_chunk_ids,
            summary=integrated_summary,
            events=integrated_events,
            image_ids=all_image_ids,
            timestamp=datetime.now(),
        )

        # ---- Compute merged embedding ----
        # Use the first member's original observation for multimodal embedding
        first_chunk_id = all_chunk_ids[0] if all_chunk_ids else None
        first_obs = self.chunk_store.get(first_chunk_id, {}) if first_chunk_id else {}
        merged_embedding = self._compute_memory_embedding(new_memory, first_obs)

        # ---- Delete old member memories ----
        self._delete_memories(valid_ids)

        # ---- Insert new merged memory ----
        self._add_memory(new_memory, merged_embedding)
        self.stats["integration_count"] += 1

    def _validate_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate and fix events to ensure action count ≤ MAX_ACTIONS_PER_EVENT
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Validated/fixed events list
        """
        if not events:
            return events
        
        validated_events = []
        for event in events:
            actions = event.get("action", [])
            
            if len(actions) <= self.MAX_ACTIONS_PER_EVENT:
                validated_events.append(event)
            else:
                # Split event into multiple events
                for i in range(0, len(actions), self.MAX_ACTIONS_PER_EVENT):
                    action_chunk = actions[i:i + self.MAX_ACTIONS_PER_EVENT]
                    split_event = {
                        "participants": event.get("participants", []),
                        "action": action_chunk,
                        "time": event.get("time"),
                        "location": event.get("location"),
                        "reason": event.get("reason"),
                        "method": event.get("method")
                    }
                    validated_events.append(split_event)
        
        return validated_events
    
    def _get_all_observations_for_memory(self, memory: EpisodicMemory) -> List[Dict[str, Any]]:
        """Get all observations associated with a memory"""
        observations = []
        for chunk_id in memory.chunk_ids:
            if chunk_id in self.chunk_store:
                observations.append(self.chunk_store[chunk_id])
        return observations
    
    def _format_memory_for_judge(self, memory: EpisodicMemory, observations: List[Dict[str, Any]]) -> str:
        """Format memory for Judge with ALL observations"""
        lines = [
            f"- Summary: {memory.summary}",
            f"- Events: {json.dumps(memory.events, ensure_ascii=False)}",
            f"- Chunk Count: {len(memory.chunk_ids)}",
            f"- All Associated Original Observations ({len(observations)} total):"
        ]
        
        for i, obs in enumerate(observations, 1):
            obs_text = obs.get("text", obs.get("content", ""))
            speaker = obs.get("speaker", "unknown")
            timestamp = obs.get("timestamp", "")
            
            # Format each observation with metadata
            lines.append(f"  [Obs {i}] (Speaker: {speaker}, Time: {timestamp})")
            lines.append(f"    {obs_text[:300]}")  # Show first 300 chars
            lines.append("")
        
        return "\n".join(lines)
    
    def _merge_memories(self, new_memory: EpisodicMemory, integrated_ids: List[str],
                       integrated_summary: str, integrated_events: List[Dict[str, Any]]) -> EpisodicMemory:
        """
        Merge memories with safety checks and intelligent chunk selection
        
        IMPORTANT: All original observations are preserved in chunk_store.
        This method only manages chunk_id references.
        """
        # Merge chunk_ids (preserves all observations)
        all_chunk_ids = list(new_memory.chunk_ids)
        for mid in integrated_ids:
            if mid in self.memories:
                all_chunk_ids.extend(self.memories[mid].chunk_ids)
        all_chunk_ids = list(dict.fromkeys(all_chunk_ids))  # Remove duplicates
        
        # Safety check: Enforce chunk limit (truncate if necessary)
        if len(all_chunk_ids) > self.MAX_CHUNKS_PER_MEMORY:
            # Intelligent truncation: prioritize recent/diverse chunks
            # Keep new memory's chunks + most relevant from candidates
            retained_chunks = all_chunk_ids[:self.MAX_CHUNKS_PER_MEMORY]
            print(f"Warning: Chunk list truncated from {len(all_chunk_ids)} to {self.MAX_CHUNKS_PER_MEMORY}")
            print(f"  Retained chunks: {retained_chunks}")
            print(f"  Note: Truncated chunks remain in chunk_store but are not linked to this memory")
            all_chunk_ids = retained_chunks
        
        # Merge image_ids
        all_image_ids = list(new_memory.image_ids)
        for mid in integrated_ids:
            if mid in self.memories:
                all_image_ids.extend(self.memories[mid].image_ids)
        all_image_ids = list(dict.fromkeys(all_image_ids))
        
        # Final validation on events
        validated_events = self._validate_events(integrated_events)
        
        return EpisodicMemory(
            memory_id=generate_memory_id(),
            chunk_ids=all_chunk_ids,
            summary=integrated_summary,
            events=validated_events,
            image_ids=all_image_ids,
            timestamp=datetime.now()
        )
    
    def _add_memory(self, memory: EpisodicMemory, embedding: np.ndarray) -> str:
        """Add memory to storage"""
        self.memories[memory.memory_id] = memory
        self.memory_embeddings[memory.memory_id] = embedding
        
        # Get corresponding observation
        chunk_id = memory.chunk_ids[0] if memory.chunk_ids else None
        observation = self.chunk_store.get(chunk_id, {}) if chunk_id else {}
        
        # Calculate chunk embedding
        if chunk_id and observation:
            chunk_text = observation.get("text", observation.get("content", ""))
            chunk_image = observation.get("image", {}).get("path") if observation.get("image") else None
            if chunk_image:
                chunk_embedding = self.mm_encoder.encode_multimodal(text=chunk_text, image_path=chunk_image)
            else:
                chunk_embedding = self.mm_encoder.encode_text(chunk_text)
            self.chunk_embeddings[chunk_id] = chunk_embedding
        
        # Build BM25 document
        bm25_text = self._build_bm25_document(memory)
        self.bm25_documents[memory.memory_id] = bm25_text
        
        # Build Chunk BM25 document
        if chunk_id and observation:
            chunk_text = observation.get("text", observation.get("content", ""))
            # Extract 5W1H from events for chunk BM25
            chunk_5w1h = self._extract_chunk_5w1h(memory.events)
            chunk_bm25_text = f"Content: {chunk_text}\n{chunk_5w1h}"
            self.chunk_bm25_documents[chunk_id] = chunk_bm25_text
        
        # Update BM25 corpus
        bm25_text = self._build_bm25_document(memory)
        self.bm25_documents[memory.memory_id] = bm25_text
        self._rebuild_bm25()
        
        # Build graph links
        self._build_graph_links(memory, observation)
        
        # Fact graph construction (if enabled)
        if self.config.enable_fact_graph:
            self._build_fact_graph(memory, chunk_id)
        
        # Entity linking
        self._link_entities(memory.events)
        
        return memory.memory_id
    
    def _delete_memories(self, memory_ids: List[str]):
        """Delete memories"""
        for mid in memory_ids:
            memory = None
            if mid in self.memories:
                # Get memory before deletion
                memory = self.memories[mid]
                # Delete related chunk embeddings
                for chunk_id in memory.chunk_ids:
                    if chunk_id in self.chunk_embeddings:
                        del self.chunk_embeddings[chunk_id]
                
                del self.memories[mid]
            if mid in self.memory_embeddings:
                del self.memory_embeddings[mid]
            if mid in self.bm25_documents:
                del self.bm25_documents[mid]
            
            # Delete related chunk BM25 documents (use saved memory reference)
            if memory:
                for chunk_id in memory.chunk_ids:
                    if chunk_id in self.chunk_bm25_documents:
                        del self.chunk_bm25_documents[chunk_id]
            
            # Clean memory-to-entity indices
            nodes_to_clean = []
            for node_id, memory_set in self.node_to_memory_ids.items():
                if mid in memory_set:
                    memory_set.discard(mid)
                    if not memory_set:
                        nodes_to_clean.append(node_id)
            
            for node_id in nodes_to_clean:
                if node_id in self.node_to_memory_ids:
                    del self.node_to_memory_ids[node_id]
        
        # Rebuild BM25
        self._rebuild_bm25()
    
    def _dense_retrieve(self, query_embedding: np.ndarray, top_k: int) -> List[str]:
        """Dense retrieve Top-K memories"""
        if not self.memory_embeddings:
            return []
        
        # Batch calculate cosine similarity
        memory_ids = list(self.memory_embeddings.keys())
        embeddings = np.stack([self.memory_embeddings[mid] for mid in memory_ids])
        scores = batch_cosine_similarity(query_embedding, embeddings)
        
        # Get Top-K indices
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = [memory_ids[i] for i in top_indices if scores[i] > 0]
        
        return results
    
    def _build_recall_results(self, retrieved_chunks: List[Tuple[str, float]],
                              top_k: int, mode: RecallMode) -> List[Dict[str, Any]]:
        """Build recall results based on mode.

        Args:
            retrieved_chunks: [(chunk_id, score), ...] sorted by relevance, top_k items
            top_k: retrieval parameter
            mode: LITE / PRO / MAX

        Returns:
            List of result dicts.
        """
        # Map chunks to memories
        chunk_to_memory: Dict[str, Any] = {}
        for chunk_id, _ in retrieved_chunks:
            for mid, memory in self.memories.items():
                if chunk_id in memory.chunk_ids:
                    chunk_to_memory[chunk_id] = memory
                    break

        # LITE: no raw chunks, only structured memory
        if mode == RecallMode.LITE:
            # Return one result per unique memory (no raw chunk text)
            seen_mids = set()
            results = []
            for chunk_id, score in retrieved_chunks:
                mem = chunk_to_memory.get(chunk_id)
                if not mem or mem.memory_id in seen_mids:
                    continue
                seen_mids.add(mem.memory_id)
                structured_text = format_structured_text(mem.summary, mem.events)
                results.append({
                    "text": f"[Structured Memory]\n{structured_text}",
                    "image": None,
                    "dialogue_id": chunk_id,
                    "has_multimodal": False,
                })
            return results

        # PRO: top_k chunks, no backfill
        if mode == RecallMode.PRO:
            all_chunk_ids = [cid for cid, _ in retrieved_chunks]

        # MAX: top_k chunks + backfill (up to 2×top_k)
        else:  # mode == RecallMode.MAX
            all_chunk_ids = [cid for cid, _ in retrieved_chunks]
            seen_chunks = set(all_chunk_ids)
            associated_mids = {chunk_to_memory[cid].memory_id
                               for cid in all_chunk_ids if cid in chunk_to_memory}
            max_total = top_k * 2
            for mid in associated_mids:
                if mid not in self.memories:
                    continue
                for cid in self.memories[mid].chunk_ids:
                    if cid not in seen_chunks and cid in self.chunk_store:
                        all_chunk_ids.append(cid)
                        seen_chunks.add(cid)
                    if len(all_chunk_ids) >= max_total:
                        break
                if len(all_chunk_ids) >= max_total:
                    break

        # Build results (PRO or MAX)
        results = []
        for chunk_id in all_chunk_ids:
            if chunk_id not in self.chunk_store:
                continue
            chunk_data = self.chunk_store[chunk_id]
            mem = chunk_to_memory.get(chunk_id)
            # Lazy lookup for backfilled chunks
            if not mem:
                for mid, memory in self.memories.items():
                    if chunk_id in memory.chunk_ids:
                        mem = memory
                        break

            structured_text = format_structured_text(mem.summary, mem.events) if mem else ""
            original_text = chunk_data.get("text", chunk_data.get("content", ""))
            full_text = f"[Structured Memory]\n{structured_text}\n\n[Original Observation]\n{original_text}"

            results.append({
                "text": full_text,
                "image": chunk_data.get("image"),
                "dialogue_id": chunk_data.get("dialogue_id", chunk_id),
                "has_multimodal": bool(chunk_data.get("image")),
            })

        return results

    def _retrieve_top_facts(self, query_embedding: np.ndarray, top_k: int) -> List[Dict[str, Any]]:
        """Retrieve Top-K most relevant fact triples by vector similarity.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of facts to return

        Returns:
            List of dicts: [{"subject": ..., "predicate": ..., "object": ..., "time": ..., "score": ...}, ...]
            sorted by descending similarity score.
        """
        if not self.facts or not self.fact_embeddings:
            return []

        # Build arrays from fact_embeddings (index → embedding)
        fact_indices = list(self.fact_embeddings.keys())
        embeddings = np.stack([self.fact_embeddings[idx] for idx in fact_indices])
        scores = batch_cosine_similarity(query_embedding, embeddings)

        # Sort by score descending, take top_k
        sorted_pairs = sorted(zip(fact_indices, scores), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for idx, score in sorted_pairs:
            if idx < len(self.facts):
                fact = self.facts[idx]
                results.append({
                    "subject": fact.subject,
                    "predicate": fact.predicate,
                    "object": fact.obj,
                    "time": fact.time,
                    "chunk_id": fact.chunk_id,
                    "confidence": fact.confidence,
                    "score": float(score),
                })

        return results

    def _dense_retrieve_chunks(self, query_embedding: np.ndarray, top_k: int) -> List[str]:
        """Dense retrieve Top-K chunks"""
        if not self.chunk_embeddings:
            return []
        
        # Batch calculate cosine similarity
        chunk_ids = list(self.chunk_embeddings.keys())
        embeddings = np.stack([self.chunk_embeddings[cid] for cid in chunk_ids])
        scores = batch_cosine_similarity(query_embedding, embeddings)
        
        # Get Top-K indices
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = [chunk_ids[i] for i in top_indices if scores[i] > 0]
        
        return results
    
    def _retrieve_chunks_dpr(self, query: Dict[str, Any], top_k: int,
                              query_embedding: Optional[np.ndarray] = None) -> List[Tuple[str, float]]:
        """DPR: retrieve top_k chunks by dense similarity. Returns [(chunk_id, score), ...]."""
        if query_embedding is None:
            query_text = query.get("text", "")
            query_embedding = self.mm_encoder.encode_text(query_text)

        chunk_ids = list(self.chunk_embeddings.keys())
        if not chunk_ids:
            return []

        embeddings = np.stack([self.chunk_embeddings[cid] for cid in chunk_ids])
        scores = batch_cosine_similarity(query_embedding, embeddings)
        paired = sorted(zip(chunk_ids, scores), key=lambda x: x[1], reverse=True)
        return [(cid, float(sc)) for cid, sc in paired[:top_k] if sc > 0]

    def _retrieve_chunks_hybrid_rrf(self, query: Dict[str, Any], top_k: int,
                                     query_embedding: Optional[np.ndarray] = None) -> List[Tuple[str, float]]:
        """Hybrid RRF: retrieve top_k chunks by dense+sparse RRF fusion. Returns [(chunk_id, score), ...]."""
        if query_embedding is None:
            query_text = query.get("text", "")
            query_embedding = self.mm_encoder.encode_text(query_text)

        # Dense scores
        dense_scores = {}
        chunk_ids = list(self.chunk_embeddings.keys())
        if chunk_ids:
            embeddings = np.stack([self.chunk_embeddings[cid] for cid in chunk_ids])
            scores = batch_cosine_similarity(query_embedding, embeddings)
            dense_scores = {cid: float(s) for cid, s in zip(chunk_ids, scores)}

        # Sparse scores
        query_5w1h = self._extract_query_5w1h(query)
        sparse_scores = self._compute_chunk_sparse_scores(query_5w1h)

        # RRF fusion
        rrf_scores = self._compute_rrf(dense_scores, sparse_scores, k=self.config.rrf_rank_constant)
        sorted_chunks = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        return [(cid, rrf_scores[cid]) for cid in sorted_chunks[:top_k]]

    def _retrieve_chunks_ppr(self, query: Dict[str, Any], top_k: int,
                              query_embedding: Optional[np.ndarray] = None) -> List[Tuple[str, float]]:
        """PPR: retrieve top_k chunks via Personalized PageRank. Returns [(chunk_id, ppr_score), ...]."""
        if query_embedding is None:
            query_text = query.get("text", "")
            query_embedding = self.mm_encoder.encode_text(query_text)

        G = self.nx_graph
        if G.number_of_nodes() == 0:
            return []

        node_list = list(G.nodes())
        node_to_idx = {n: i for i, n in enumerate(node_list)}
        n_nodes = len(node_list)

        # Step 1: Phrase weights from top facts
        phrase_weights = np.zeros(n_nodes)
        top_k_facts_cfg = min(self.config.top_k_facts, len(self.facts)) if self.facts else 0
        if top_k_facts_cfg > 0:
            retrieved_facts = self._retrieve_top_facts(query_embedding, top_k=top_k_facts_cfg)
            entity_scores: Dict[str, List[float]] = {}
            for fact in retrieved_facts:
                for entity_name in [fact["subject"], fact["object"]]:
                    node_id = f"entity_{entity_name}"
                    if node_id in node_to_idx:
                        entity_scores.setdefault(node_id, []).append(fact["score"])
            for node_id, scores in entity_scores.items():
                phrase_weights[node_to_idx[node_id]] = np.mean(scores)

        # Step 2: Passage weights from dense chunk retrieval
        passage_weights = np.zeros(n_nodes)
        top_k_chunks_cfg = min(getattr(self.config, 'top_k_chunks', 5), len(self.chunk_embeddings)) if self.chunk_embeddings else 0
        if top_k_chunks_cfg > 0:
            dense_chunk_ids = self._dense_retrieve_chunks(query_embedding, top_k=top_k_chunks_cfg)
            if dense_chunk_ids:
                chunk_id_list = list(self.chunk_embeddings.keys())
                chunk_embeddings_arr = np.stack([self.chunk_embeddings[cid] for cid in chunk_id_list])
                all_scores = batch_cosine_similarity(query_embedding, chunk_embeddings_arr)
                score_map = {cid: float(s) for cid, s in zip(chunk_id_list, all_scores)}
                retrieved_scores = [score_map.get(cid, 0.0) for cid in dense_chunk_ids]
                if retrieved_scores:
                    min_s, max_s = min(retrieved_scores), max(retrieved_scores)
                    score_range = max_s - min_s if max_s > min_s else 1.0
                    for cid in dense_chunk_ids:
                        if cid in node_to_idx:
                            passage_weights[node_to_idx[cid]] = (score_map.get(cid, 0.0) - min_s) / score_range

        # Step 3: Combine and normalize
        node_weights = phrase_weights + passage_weights
        if node_weights.sum() <= 0:
            return self._retrieve_chunks_dpr(query, top_k, query_embedding)
        node_weights = node_weights / node_weights.sum()

        # Step 4: Run PPR
        try:
            undirected_G = G.to_undirected()
            pagerank_scores = nx.pagerank(
                undirected_G, alpha=self.config.ppr_damping,
                personalization={n: float(node_weights[node_to_idx[n]]) for n in node_list},
                weight='weight',
            )
        except Exception as e:
            print(f"Warning: PPR failed: {e}, falling back to DPR")
            return self._retrieve_chunks_dpr(query, top_k, query_embedding)

        # Step 5: Extract chunk scores
        chunk_scores = [(nid, sc) for nid, sc in pagerank_scores.items()
                        if G.nodes.get(nid, {}).get("node_type") == "chunk" and nid in self.chunk_store]
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        return chunk_scores[:top_k]

    def _compute_dense_scores(self, query_embedding: np.ndarray) -> Dict[str, float]:
        """Calculate dense scores"""
        memory_ids = list(self.memory_embeddings.keys())
        if not memory_ids:
            return {}
        
        embeddings = np.stack([self.memory_embeddings[mid] for mid in memory_ids])
        scores = batch_cosine_similarity(query_embedding, embeddings)
        
        return {mid: float(score) for mid, score in zip(memory_ids, scores)}
    
    def _compute_chunk_sparse_scores(self, query_5w1h: str) -> Dict[str, float]:
        """Calculate chunk sparse scores (BM25)"""
        if not self.chunk_bm25_retriever:
            return {}
        
        results = self.chunk_bm25_retriever.search(query_5w1h, top_k=len(self.chunk_bm25_documents))
        chunk_ids = list(self.chunk_bm25_documents.keys())
        
        # Map BM25 results to chunk_id
        scores = {}
        for idx, score in results:
            if idx < len(chunk_ids):
                scores[chunk_ids[idx]] = float(score)
        
        return scores
    
    def _compute_sparse_scores(self, query_5w1h: str) -> Dict[str, float]:
        """Calculate sparse scores (BM25)"""
        if not self.bm25_retriever:
            return {}
        
        results = self.bm25_retriever.search(query_5w1h, top_k=len(self.bm25_documents))
        memory_ids = list(self.bm25_documents.keys())
        
        # Map BM25 results to memory_id
        scores = {}
        for idx, score in results:
            if idx < len(memory_ids):
                scores[memory_ids[idx]] = float(score)
        
        return scores
    
    def _compute_rrf(self, dense_scores: Dict[str, float], sparse_scores: Dict[str, float], 
                    k: int = 60) -> Dict[str, float]:
        """RRF fusion"""
        all_memory_ids = set(dense_scores.keys()) | set(sparse_scores.keys())
        
        # Ranking
        dense_ranking = sorted(dense_scores.keys(), key=lambda x: dense_scores[x], reverse=True)
        sparse_ranking = sorted(sparse_scores.keys(), key=lambda x: sparse_scores[x], reverse=True)
        
        # Calculate RRF scores
        rrf_scores = {}
        for mid in all_memory_ids:
            score = 0.0
            if mid in dense_ranking:
                rank1 = dense_ranking.index(mid) + 1
                score += 1.0 / (k + rank1)
            if mid in sparse_ranking:
                rank2 = sparse_ranking.index(mid) + 1
                score += 1.0 / (k + rank2)
            rrf_scores[mid] = score
        
        return rrf_scores
    
    def _extract_query_5w1h(self, query: Dict[str, Any]) -> str:
        """Extract Query 5W1H elements"""
        query_text = query.get("text", "")
        
        try:
            result = self.llm.generate(
                system_prompt=QUERY_5W1H_SYSTEM_PROMPT,
                user_prompt=f"Extract 5W1H from: {query_text}"
            )
            self.stats["llm_calls"] += 1
            
            data = json.loads(result)
            return format_5w1h_text(
                who=data.get("who"),
                what=data.get("what"),
                when=data.get("when"),
                where=data.get("where"),
                why=data.get("why"),
                how=data.get("how")
            )
        except Exception as e:
            print(f"Warning: 5W1H extraction failed: {str(e)}")
            return query_text
    
    def _build_bm25_document(self, memory: EpisodicMemory) -> str:
        """Build BM25 document (5W1H + summary)"""
        # Extract 5W1H from events
        who_list = []
        what_list = []
        when_list = []
        where_list = []
        
        for event in memory.events:
            who_list.extend(event.get("participants", []))
            what_list.extend(event.get("action", []))
            if event.get("time"):
                when_list.append(event["time"])
            if event.get("location"):
                where_list.append(event["location"])
        
        parts = []
        if who_list:
            parts.append(f"Who: {', '.join(who_list)}")
        if what_list:
            parts.append(f"What: {'; '.join(what_list)}")
        if when_list:
            parts.append(f"When: {'; '.join(when_list)}")
        if where_list:
            parts.append(f"Where: {'; '.join(where_list)}")
        
        # Add summary
        bm25_text = f"Summary: {memory.summary}\n" + " | ".join(parts)
        
        return bm25_text
    
    def _rebuild_bm25(self):
        """Rebuild BM25 index"""
        if not self.bm25_documents:
            self.bm25_retriever = None
            return
        
        documents = list(self.bm25_documents.values())
        self.bm25_retriever = BM25Retriever(documents)
        
        # Rebuild Chunk BM25
        self._rebuild_chunk_bm25()
    
    def _link_entities(self, events: List[Dict[str, Any]]):
        """Entity linking (based on embedding similarity)"""
        entities = set()
        for event in events:
            entities.update(event.get("participants", []))
        
        for entity in entities:
            # Calculate embedding
            entity_embedding = self.mm_encoder.encode_text(entity)
            
            # Check if there is already a high-similarity entity
            best_match = None
            best_score = 0.0
            
            for canonical_entity, embedding in self.entity_embeddings.items():
                score = cosine_similarity(entity_embedding, embedding)
                if score > best_score and score >= self.config.entity_similarity_threshold:
                    best_score = score
                    best_match = canonical_entity
            
            if best_match:
                # Link to existing entity
                self.entity_map[entity] = best_match
            else:
                # Create new entity
                self.entity_embeddings[entity] = entity_embedding
    
    def _build_recall_result(self, memory: EpisodicMemory) -> RecallResult:
        """Build recall result"""
        # Get chunk data
        chunk_data = self.chunk_store.get(memory.chunk_ids[0], {}) if memory.chunk_ids else {}
        
        # Assemble text: Structured memory + Original observation
        structured_text = format_structured_text(memory.summary, memory.events)
        original_text = chunk_data.get("text", chunk_data.get("content", ""))
        
        full_text = f"[Structured Memory]\n{structured_text}\n\n[Original Observation]\n{original_text}"
        
        # Image data
        image_data = chunk_data.get("image") if chunk_data else None
        has_multimodal = bool(image_data)
        
        # Dialogue ID
        dialogue_id = chunk_data.get("dialogue_id", memory.chunk_ids[0] if memory.chunk_ids else "")
        
        return RecallResult(
            memory=memory,
            text=full_text,
            image=image_data,
            dialogue_id=dialogue_id,
            has_multimodal=has_multimodal
        )
    
    # ========== Graph Operation Methods ==========
    
    def _add_graph_node(self, node_id: str, node_type: str, metadata: Dict[str, Any] = None):
        """Add graph node to NetworkX DiGraph"""
        if not self.nx_graph.has_node(node_id):
            self.nx_graph.add_node(node_id, node_type=node_type, **(metadata or {}))
        else:
            # Update node_type if not set
            if "node_type" not in self.nx_graph.nodes[node_id]:
                self.nx_graph.nodes[node_id]["node_type"] = node_type
        return node_id
    
    def _add_graph_edge(self, source: str, target: str, edge_type: str, weight: float = 1.0, metadata: Dict[str, Any] = None):
        """Add graph edge to NetworkX DiGraph"""
        self.nx_graph.add_edge(source, target, edge_type=edge_type, weight=weight, **(metadata or {}))
    
    def _get_node_neighbors(self, node_id: str, edge_type: Optional[str] = None) -> List[Tuple[str, Dict[str, Any]]]:
        """Get outgoing neighbors of a node, optionally filtered by edge type.

        Returns:
            List of (neighbor_node_id, edge_attr_dict) tuples.
        """
        if not self.nx_graph.has_node(node_id):
            return []
        results = []
        for _, target, attrs in self.nx_graph.out_edges(node_id, data=True):
            if edge_type is None or attrs.get("edge_type") == edge_type:
                results.append((target, attrs))
        return results
    
    def _build_graph_links(self, memory: EpisodicMemory, observation: Dict[str, Any]):
        """Build graph links: Entity-Chunk"""
        chunk_id = memory.chunk_ids[0] if memory.chunk_ids else None
        if not chunk_id:
            return
        
        # Add Chunk node
        self._add_graph_node(chunk_id, "chunk", {"dialogue_id": observation.get("dialogue_id", chunk_id)})
        
        # Process entities in events
        entities = set()
        for event in memory.events:
            participants = event.get("participants", [])
            entities.update(participants)
        
        for entity in entities:
            # Add Entity node
            entity_node_id = f"entity_{entity}"
            self._add_graph_node(entity_node_id, "entity", {"name": entity})
            
            # Add Entity-Chunk edge
            self._add_graph_edge(entity_node_id, chunk_id, "entity_chunk", weight=1.0)
            
            # Update indices
            if entity_node_id not in self.node_to_chunk_ids:
                self.node_to_chunk_ids[entity_node_id] = set()
            self.node_to_chunk_ids[entity_node_id].add(chunk_id)
            
            if entity_node_id not in self.node_to_memory_ids:
                self.node_to_memory_ids[entity_node_id] = set()
            self.node_to_memory_ids[entity_node_id].add(memory.memory_id)
    
    # ========== Persistence Methods ==========
    
    def save_to_disk(self, data_dir: str = None):
        """Save to disk.

        Note: This method only serializes state.  It does NOT trigger
        integration flush — that responsibility belongs to store()
        (window-full), recall() (consistency), and flush() (explicit).
        Calling flush here would bypass the windowed batching because
        save_to_disk() is invoked after every store().
        """
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        
        os.makedirs(data_dir, exist_ok=True)
        
        # Save memories
        memories_data = {mid: memory.to_dict() for mid, memory in self.memories.items()}
        with open(os.path.join(data_dir, "memories.json"), "w", encoding="utf-8") as f:
            json.dump(memories_data, f, ensure_ascii=False, indent=2)
        
        # Save chunk_store
        with open(os.path.join(data_dir, "chunk_store.json"), "w", encoding="utf-8") as f:
            json.dump(self.chunk_store, f, ensure_ascii=False, indent=2)
        
        # Save graph structure (NetworkX node-link JSON)
        graph_data = nx.node_link_data(self.nx_graph)
        with open(os.path.join(data_dir, "nx_graph.json"), "w", encoding="utf-8") as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        # Save indices
        node_to_memory_ids_data = {k: list(v) for k, v in self.node_to_memory_ids.items()}
        with open(os.path.join(data_dir, "node_to_memory_ids.json"), "w", encoding="utf-8") as f:
            json.dump(node_to_memory_ids_data, f, ensure_ascii=False, indent=2)
        
        node_to_chunk_ids_data = {k: list(v) for k, v in self.node_to_chunk_ids.items()}
        with open(os.path.join(data_dir, "node_to_chunk_ids.json"), "w", encoding="utf-8") as f:
            json.dump(node_to_chunk_ids_data, f, ensure_ascii=False, indent=2)
        
        # Save BM25 documents
        with open(os.path.join(data_dir, "bm25_documents.json"), "w", encoding="utf-8") as f:
            json.dump(self.bm25_documents, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(data_dir, "chunk_bm25_documents.json"), "w", encoding="utf-8") as f:
            json.dump(self.chunk_bm25_documents, f, ensure_ascii=False, indent=2)
        
        # Save entity data
        entity_map_data = self.entity_map
        with open(os.path.join(data_dir, "entity_map.json"), "w", encoding="utf-8") as f:
            json.dump(entity_map_data, f, ensure_ascii=False, indent=2)
        
        # Save facts
        facts_data = [fact.to_dict() for fact in self.facts]
        with open(os.path.join(data_dir, "facts.json"), "w", encoding="utf-8") as f:
            json.dump(facts_data, f, ensure_ascii=False, indent=2)
        
        # Save entity storage order
        with open(os.path.join(data_dir, "entity_store_order.json"), "w", encoding="utf-8") as f:
            json.dump(self.entity_store_order, f, ensure_ascii=False, indent=2)
        
        # Save embeddings (use pickle for numpy arrays)
        with open(os.path.join(data_dir, "memory_embeddings.pkl"), "wb") as f:
            pickle.dump(self.memory_embeddings, f)
        
        with open(os.path.join(data_dir, "chunk_embeddings.pkl"), "wb") as f:
            pickle.dump(self.chunk_embeddings, f)
        
        with open(os.path.join(data_dir, "entity_embeddings.pkl"), "wb") as f:
            pickle.dump(self.entity_embeddings, f)
        
        with open(os.path.join(data_dir, "fact_embeddings.pkl"), "wb") as f:
            pickle.dump(self.fact_embeddings, f)

        # Save normalized fact set
        with open(os.path.join(data_dir, "fact_norm_set.json"), "w", encoding="utf-8") as f:
            json.dump(list(self._fact_norm_set), f)

        # Save statistics
        with open(os.path.join(data_dir, "stats.json"), "w", encoding="utf-8") as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def load_from_disk(self, data_dir: str = None):
        """Load from disk"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        
        if not os.path.exists(data_dir):
            return False
        
        try:
            # Load memories
            memories_path = os.path.join(data_dir, "memories.json")
            if os.path.exists(memories_path):
                with open(memories_path, "r", encoding="utf-8") as f:
                    memories_data = json.load(f)
                self.memories = {mid: EpisodicMemory.from_dict(data) for mid, data in memories_data.items()}
            
            # Load chunk_store
            chunk_store_path = os.path.join(data_dir, "chunk_store.json")
            if os.path.exists(chunk_store_path):
                with open(chunk_store_path, "r", encoding="utf-8") as f:
                    self.chunk_store = json.load(f)
            
            # Load graph structure (NetworkX node-link JSON)
            nx_graph_path = os.path.join(data_dir, "nx_graph.json")
            if os.path.exists(nx_graph_path):
                with open(nx_graph_path, "r", encoding="utf-8") as f:
                    graph_data = json.load(f)
                self.nx_graph = nx.node_link_graph(graph_data, directed=True)
            else:
                # Legacy format fallback: migrate old graph_nodes/graph_edges files
                graph_nodes_path = os.path.join(data_dir, "graph_nodes.json")
                graph_edges_path = os.path.join(data_dir, "graph_edges.json")
                if os.path.exists(graph_nodes_path) and os.path.exists(graph_edges_path):
                    with open(graph_nodes_path, "r", encoding="utf-8") as f:
                        graph_nodes_data = json.load(f)
                    with open(graph_edges_path, "r", encoding="utf-8") as f:
                        graph_edges_data = json.load(f)
                    # Migrate to NetworkX
                    self.nx_graph = nx.DiGraph()
                    for nid, ndata in graph_nodes_data.items():
                        self.nx_graph.add_node(nid, node_type=ndata.get("node_type", "unknown"),
                                               **ndata.get("metadata", {}))
                    for source, edges_list in graph_edges_data.items():
                        for edata in edges_list:
                            self.nx_graph.add_edge(edata["source"], edata["target"],
                                                   edge_type=edata.get("edge_type", "unknown"),
                                                   weight=edata.get("weight", 1.0),
                                                   **edata.get("metadata", {}))
                    print("Migrated legacy graph format to NetworkX")
            
            # Load indices
            node_to_memory_ids_path = os.path.join(data_dir, "node_to_memory_ids.json")
            if os.path.exists(node_to_memory_ids_path):
                with open(node_to_memory_ids_path, "r", encoding="utf-8") as f:
                    node_to_memory_ids_data = json.load(f)
                self.node_to_memory_ids = {k: set(v) for k, v in node_to_memory_ids_data.items()}
            
            node_to_chunk_ids_path = os.path.join(data_dir, "node_to_chunk_ids.json")
            if os.path.exists(node_to_chunk_ids_path):
                with open(node_to_chunk_ids_path, "r", encoding="utf-8") as f:
                    node_to_chunk_ids_data = json.load(f)
                self.node_to_chunk_ids = {k: set(v) for k, v in node_to_chunk_ids_data.items()}
            
            # Load BM25 documents
            bm25_documents_path = os.path.join(data_dir, "bm25_documents.json")
            if os.path.exists(bm25_documents_path):
                with open(bm25_documents_path, "r", encoding="utf-8") as f:
                    self.bm25_documents = json.load(f)
            
            chunk_bm25_documents_path = os.path.join(data_dir, "chunk_bm25_documents.json")
            if os.path.exists(chunk_bm25_documents_path):
                with open(chunk_bm25_documents_path, "r", encoding="utf-8") as f:
                    self.chunk_bm25_documents = json.load(f)
            
            # Load entity data
            entity_map_path = os.path.join(data_dir, "entity_map.json")
            if os.path.exists(entity_map_path):
                with open(entity_map_path, "r", encoding="utf-8") as f:
                    self.entity_map = json.load(f)
            
            # Load facts
            facts_path = os.path.join(data_dir, "facts.json")
            if os.path.exists(facts_path):
                with open(facts_path, "r", encoding="utf-8") as f:
                    facts_data = json.load(f)
                self.facts = [Fact.from_dict(data) for data in facts_data]
            
            # Load entity storage order
            entity_store_order_path = os.path.join(data_dir, "entity_store_order.json")
            if os.path.exists(entity_store_order_path):
                with open(entity_store_order_path, "r", encoding="utf-8") as f:
                    self.entity_store_order = json.load(f)
            
            # Load embeddings
            memory_embeddings_path = os.path.join(data_dir, "memory_embeddings.pkl")
            if os.path.exists(memory_embeddings_path):
                with open(memory_embeddings_path, "rb") as f:
                    self.memory_embeddings = pickle.load(f)
            
            chunk_embeddings_path = os.path.join(data_dir, "chunk_embeddings.pkl")
            if os.path.exists(chunk_embeddings_path):
                with open(chunk_embeddings_path, "rb") as f:
                    self.chunk_embeddings = pickle.load(f)
            
            entity_embeddings_path = os.path.join(data_dir, "entity_embeddings.pkl")
            if os.path.exists(entity_embeddings_path):
                with open(entity_embeddings_path, "rb") as f:
                    self.entity_embeddings = pickle.load(f)
            
            fact_embeddings_path = os.path.join(data_dir, "fact_embeddings.pkl")
            if os.path.exists(fact_embeddings_path):
                with open(fact_embeddings_path, "rb") as f:
                    self.fact_embeddings = pickle.load(f)

            # Load normalized fact set
            fact_norm_set_path = os.path.join(data_dir, "fact_norm_set.json")
            if os.path.exists(fact_norm_set_path):
                with open(fact_norm_set_path, "r", encoding="utf-8") as f:
                    self._fact_norm_set = set(json.load(f))
            else:
                # Rebuild from existing facts (legacy migration)
                for fact in self.facts:
                    norm_key = f"{fact.subject.lower().strip()}|{fact.predicate.lower().strip()}|{fact.obj.lower().strip()}"
                    self._fact_norm_set.add(norm_key)

            # Load statistics
            stats_path = os.path.join(data_dir, "stats.json")
            if os.path.exists(stats_path):
                with open(stats_path, "r", encoding="utf-8") as f:
                    self.stats = json.load(f)
            
            # Rebuild BM25 index
            self._rebuild_bm25()
            
            return True
        except Exception as e:
            print(f"Warning: Failed to load from disk: {e}")
            return False
    
    def _extract_chunk_5w1h(self, events: List[Dict[str, Any]]) -> str:
        """Extract 5W1H from events for chunk BM25"""
        who_list = []
        what_list = []
        when_list = []
        where_list = []
        
        for event in events:
            who_list.extend(event.get("participants", []))
            what_list.extend(event.get("action", []))
            if event.get("time"):
                when_list.append(event["time"])
            if event.get("location"):
                where_list.append(event["location"])
        
        parts = []
        if who_list:
            parts.append(f"Who: {', '.join(who_list)}")
        if what_list:
            parts.append(f"What: {'; '.join(what_list)}")
        if when_list:
            parts.append(f"When: {'; '.join(when_list)}")
        if where_list:
            parts.append(f"Where: {'; '.join(where_list)}")
        
        return " | ".join(parts) if parts else ""
    
    def _rebuild_chunk_bm25(self):
        """Rebuild Chunk BM25 index"""
        if not self.chunk_bm25_documents:
            self.chunk_bm25_retriever = None
            return
        
        documents = list(self.chunk_bm25_documents.values())
        self.chunk_bm25_retriever = BM25Retriever(documents)
    
    # ========== Fact Graph Construction Methods ==========
    
    def _build_fact_graph(self, memory: EpisodicMemory, chunk_id: str):
        """
        Extract facts from observation using LLM and build Fact graph.

        Deduplication: Before inserting a new fact, check cosine similarity
        against existing fact embeddings. If similarity > 0.95, skip fact
        insertion and only link the new chunk to the existing fact's entities.
        """
        chunk_data = self.chunk_store.get(chunk_id, {})
        if not chunk_data:
            return

        observation_text = chunk_data.get("text", "")
        image = chunk_data.get("image")

        # Build complete observation text
        input_text = observation_text
        if image and isinstance(image, dict):
            caption = image.get("caption", "")
            if caption:
                input_text += f"\n[Image: {caption}]"

        # Call LLM to extract facts
        facts = self._extract_facts_with_llm(input_text, chunk_id)

        EMBED_DEDUP_THRESHOLD = 0.93

        def _normalize_triple(s: str, p: str, o: str) -> str:
            """Normalize triple for exact matching: lowercase, strip whitespace."""
            return f"{s.lower().strip()}|{p.lower().strip()}|{o.lower().strip()}"

        for fact in facts:
            # --- Stage 1: Exact match on normalized triple ---
            norm_key = _normalize_triple(fact.subject, fact.predicate, fact.obj)
            is_duplicate = False
            duplicate_existing_idx = -1

            if norm_key in self._fact_norm_set:
                # Find the existing fact with matching normalized triple
                for idx, existing_fact in enumerate(self.facts):
                    if _normalize_triple(existing_fact.subject, existing_fact.predicate, existing_fact.obj) == norm_key:
                        is_duplicate = True
                        duplicate_existing_idx = idx
                        break
            else:
                # --- Stage 2: Embedding similarity check ---
                fact_text = f"{fact.subject} {fact.predicate} {fact.obj}"
                fact_embedding = self.mm_encoder.encode_text(fact_text)

                if self.fact_embeddings:
                    existing_indices = list(self.fact_embeddings.keys())
                    existing_embeddings = np.stack([self.fact_embeddings[idx] for idx in existing_indices])
                    similarities = batch_cosine_similarity(fact_embedding, existing_embeddings)
                    max_sim_idx = int(np.argmax(similarities))
                    max_sim = float(similarities[max_sim_idx])

                    if max_sim >= EMBED_DEDUP_THRESHOLD:
                        is_duplicate = True
                        duplicate_existing_idx = existing_indices[max_sim_idx]

            if is_duplicate:
                # Skip fact insertion — just link chunk to the existing fact's entities
                existing_fact = self.facts[duplicate_existing_idx]
                for entity_name in [existing_fact.subject, existing_fact.obj]:
                    entity_node_id = f"entity_{entity_name}"
                    if self.nx_graph.has_node(entity_node_id):
                        chunk_node_id = f"chunk_{chunk_id}"
                        if self.nx_graph.has_node(chunk_node_id):
                            if not self.nx_graph.has_edge(entity_node_id, chunk_node_id):
                                self._add_graph_edge(entity_node_id, chunk_node_id, "entity_chunk", weight=1.0)
                            if entity_node_id not in self.node_to_chunk_ids:
                                self.node_to_chunk_ids[entity_node_id] = set()
                            self.node_to_chunk_ids[entity_node_id].add(chunk_id)
            else:
                # Insert new fact
                fact_idx = len(self.facts)
                self.facts.append(fact)
                self.fact_embeddings[fact_idx] = fact_embedding
                self._fact_norm_set.add(norm_key)

                # Ensure entity nodes exist
                subject_node_id = self._ensure_entity_node(fact.subject)
                object_node_id = self._ensure_entity_node(fact.obj)

                # Add fact edge (bidirectional)
                if subject_node_id and object_node_id:
                    self._add_graph_edge(
                        subject_node_id, object_node_id, "fact",
                        weight=fact.confidence,
                        metadata={"predicate": fact.predicate, "chunk_id": chunk_id, "time": fact.time}
                    )
                    self._add_graph_edge(
                        object_node_id, subject_node_id, "fact",
                        weight=fact.confidence,
                        metadata={"predicate": fact.predicate, "chunk_id": chunk_id, "time": fact.time}
                    )

                # Add entity-chunk edge
                chunk_node_id = f"chunk_{chunk_id}"
                if self.nx_graph.has_node(chunk_node_id):
                    if subject_node_id:
                        self._add_graph_edge(subject_node_id, chunk_node_id, "entity_chunk", weight=1.0)
                    if object_node_id:
                        self._add_graph_edge(object_node_id, chunk_node_id, "entity_chunk", weight=1.0)

        # Update statistics
        self.stats["fact_count"] = len(self.facts)
        self.stats["entity_count"] = len(self.entity_embeddings)
    
    def _extract_facts_with_llm(self, observation_text: str, chunk_id: str) -> List[Fact]:
        """
        Extract facts from observation using LLM
        
        Args:
            observation_text: Observation text
            chunk_id: Corresponding chunk ID
            
        Returns:
            List of Fact objects
        """
        if not observation_text.strip():
            return []
        
        try:
            # Call LLM to extract facts
            response = self.llm.generate(
                system_prompt=FACT_EXTRACTION_SYSTEM_PROMPT,
                user_prompt=f"Extract facts from the following text:\n\n{observation_text}"
            )
            self.stats["llm_calls"] += 1
            
            # Parse JSON result
            result = json.loads(response)
            fact_tuples = result.get("facts", [])
            
            facts = []
            for fact_tuple in fact_tuples:
                if isinstance(fact_tuple, (list, tuple)) and len(fact_tuple) >= 3:
                    subject = str(fact_tuple[0]).lower().strip()
                    predicate = str(fact_tuple[1]).strip()
                    obj = str(fact_tuple[2]).lower().strip()
                    
                    if subject and predicate and obj:
                        fact = Fact(
                            subject=subject,
                            predicate=predicate,
                            obj=obj,
                            time=None,  # Can be parsed from observation or added later
                            chunk_id=chunk_id,
                            confidence=1.0
                        )
                        facts.append(fact)
            
            return facts
        except Exception as e:
            print(f"Warning: Fact extraction with LLM failed: {str(e)}")
            return []
    
    def _extract_facts_from_events(self, events: List[Dict[str, Any]], chunk_id: str) -> List[Fact]:
        """
        [DEPRECATED] Extract facts from events (no additional LLM call required)
        
        According to SEEM_Adaptation_Design_Document.md design,
        Facts can be directly parsed from participants and actions in events
        """
        facts = []
        
        for event in events:
            participants = event.get("participants", [])
            actions = event.get("action", [])
            time = event.get("time")
            location = event.get("location")
            
            # Generate facts from each participant and action combination
            for participant in participants:
                for action in actions:
                    # Parse action to get predicate and object
                    predicate, obj = self._parse_action(action)
                    
                    if predicate and obj:
                        fact = Fact(
                            subject=participant.lower().strip(),
                            predicate=predicate,
                            obj=obj.lower().strip(),
                            time=time,
                            chunk_id=chunk_id,
                            confidence=1.0
                        )
                        facts.append(fact)
            
            # If location exists, add location-related fact
            if location and participants:
                for participant in participants:
                    fact = Fact(
                        subject=participant.lower().strip(),
                        predicate="located_at",
                        obj=location.lower().strip(),
                        time=time,
                        chunk_id=chunk_id,
                        confidence=0.9
                    )
                    facts.append(fact)
        
        return facts
    
    def _parse_action(self, action: str) -> Tuple[str, str]:
        """
        Parse action string to extract predicate and object
            
        Example: "asked about Scottish Terriers" -> ("asked about", "Scottish Terriers")
        """
        action = action.strip()
        if not action:
            return ("", "")
        
        # Common verb patterns
        patterns = [
            # "verb about X" -> (verb about, X)
            (r"^(\w+\s+about)\s+(.+)$", 2),
            # "verb that X" -> (verb that, X)
            (r"^(\w+\s+that)\s+(.+)$", 2),
            # "verb to X" -> (verb to, X)
            (r"^(\w+\s+to)\s+(.+)$", 2),
            # "verb X" -> (verb, X)
            (r"^(\w+)\s+(.+)$", 2),
        ]
        
        import re
        for pattern, groups in patterns:
            match = re.match(pattern, action, re.IGNORECASE)
            if match:
                predicate = match.group(1).lower().strip()
                obj = match.group(2).strip()
                return (predicate, obj)
        
        # Unable to parse, return the entire action as predicate
        return (action.lower(), "")
    
    def _ensure_entity_node(self, entity_name: str) -> Optional[str]:
        """
        Ensure entity node exists, create if it doesn't exist
        
        Refer to SEEMStore.py's _ensure_entity_node method
        """
        entity_name = entity_name.lower().strip()
        if not entity_name:
            return None
        
        # Find existing node
        node_id = f"entity_{entity_name}"
        if self.nx_graph.has_node(node_id):
            return node_id
        
        # Create new node
        self._add_graph_node(node_id, "entity", {"entity_name": entity_name})
        
        # Calculate entity embedding
        entity_embedding = self.mm_encoder.encode_text(entity_name)
        self.entity_embeddings[entity_name] = entity_embedding
        self.entity_store_order.append(entity_name)
        
        # Add synonymy edge
        self._add_synonymy_edges_for_entity(entity_name, node_id)
        
        return node_id
    
    def _add_synonymy_edges_for_entity(self, entity_name: str, entity_node_id: str):
        """
        Add synonymy edges for new entity
        
        Refer to SEEMStore.py's _add_synonymy_edges_for_entity method
        Use KNN + threshold approach to add synonymy edges
        """
        if len(self.entity_embeddings) <= 1:
            return
        
        top_k = min(self.config.synonymy_edge_topk, len(self.entity_store_order))
        if top_k <= 1:
            return
        
        entity_embedding = self.entity_embeddings.get(entity_name)
        if entity_embedding is None:
            return
        
        # Calculate similarity with all other entities
        similarities = []
        for other_name, other_embedding in self.entity_embeddings.items():
            if other_name == entity_name:
                continue
            sim = cosine_similarity(entity_embedding, other_embedding)
            similarities.append((other_name, sim))
        
        # Sort and select top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        for other_name, score in similarities[:top_k]:
            if score < self.config.synonymy_edge_sim_threshold:
                continue
            
            other_node_id = f"entity_{other_name}"
            if not self.nx_graph.has_node(other_node_id):
                continue
            
            # Add bidirectional synonymy edge
            self._add_graph_edge(entity_node_id, other_node_id, "synonymy", weight=float(score))
            self._add_graph_edge(other_node_id, entity_node_id, "synonymy", weight=float(score))
