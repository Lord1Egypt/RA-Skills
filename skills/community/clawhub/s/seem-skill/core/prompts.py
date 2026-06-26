"""SEEM Skill Prompt Templates"""

# Episodic Memory Extraction Prompt
EPISODIC_EXTRACTION_SYSTEM_PROMPT = """Extract structured episodic memories from a conversation turn. Output PURE JSON only, no markdown:

{
  "summary": "1-3 sentence active-voice summary",
  "events": [
    {
      "participants": ["entity1", "entity2"],
      "action": ["subject+verb+object"],
      "time": "ISO 8601 or null",
      "location": "place or null",
      "reason": "why or null",
      "method": "how or null"
    }
  ]
}

Rules:

SUMMARY: 1-3 concise active-voice sentences.

EVENTS — each event is one distinct occurrence:

  participants: Involved entities (resolve coreferences).
  action: PURE action statements — subject + verb + object only.
    ⚠️ STRICT SLOT SEPARATION — this is critical:
    - Do NOT put time words in action (no "in 2026", "yesterday", "next quarter")
    - Do NOT put locations in action (no "in South Korea", "at MWC")
    - Do NOT put reasons in action (no "to meet demand", "because of X")
    - Do NOT put methods in action (no "by doubling output", "through open-source")
    action must contain ONLY the WHO did WHAT — nothing else.
    BAD:  "Huawei plans to double production of Ascend chips in 2026"
    GOOD: "Huawei plans to double production of Ascend chips"
    If you find yourself writing "in [place]", "on [date]", "to [purpose]", "by [means]" — stop. That belongs in another slot.

  time: ISO 8601 date. For spans use START only. Frequency ("every week") goes in method, NOT time. Null if absent.
  location: Place name. Null if absent.
  reason: Why it happened (only if clearly stated). Null otherwise.
  method: How it happened (only if clearly stated). Null otherwise.

Other rules:
- For images [Image: ...], extract participants and actions.
- Do not invent details; prefer null.
- Use the same language as the input for all string values."""


# Query 5W1H Extraction Prompt (for Hybrid RRF)
QUERY_5W1H_SYSTEM_PROMPT = """Extract the 5W1H elements from the following query for episodic-memory retrieval. Focus on retrievable event information rather than broad topic labels.

LANGUAGE: Use the same language as the input query for all extracted values. Do NOT translate.

Output STRICT JSON format:
{
  "who": "persons/entities mentioned or null",
  "what": "main action/event or null",
  "when": "time expression or null",
  "where": "location or null",
  "why": "reason or null",
  "how": "method or null"
}

Rules:
- who: People/entities explicitly mentioned or clearly referred to
- what: Main event/action in retrievable form (concise action phrase, not abstract topic)
- when/where/why/how: Fill only if stated or clearly implied; otherwise null
- Resolve coreferences when clear
- Preserve concrete names and time expressions from the query
- For image-related queries, include relevant visual event/entity information
- If uncertain, prefer null over guessing
- Output PURE JSON only, no markdown fences"""

# Format 5W1H Text
def format_5w1h_text(who: str, what: str, when: str, where: str, why: str, how: str) -> str:
    """Format 5W1H elements for retrieval text"""
    parts = []
    if who:
        parts.append(f"Who: {who}")
    if what:
        parts.append(f"What: {what}")
    if when:
        parts.append(f"When: {when}")
    if where:
        parts.append(f"Where: {where}")
    if why:
        parts.append(f"Why: {why}")
    if how:
        parts.append(f"How: {how}")
    
    return " | ".join(parts) if parts else ""


# ============================================================
# Batch Integration Prompt (Strategy C: single LLM call for w pending memories)
# ============================================================

BATCH_JUDGE_INTEGRATE_SYSTEM_PROMPT = """You are a memory integration gatekeeper in BATCH mode. You receive NEW pending memories and EXISTING candidate memories, then decide how to merge them.

Output STRICT JSON (no markdown):
{
  "merge_groups": [
    {
      "members": ["p1", "a1b2c3"],
      "coherence_level": "STRONG",
      "chunk_count_check": {"total": 3, "exceeds_limit": false},
      "integrated_summary": "at most 3 sentences, under 300 chars",
      "integrated_events": [...]
    }
  ]
}

Input format:
- PENDING MEMORIES have pending_id like "p1", "p2".
- CANDIDATE MEMORIES have memory_id like "a1b2c3".

Constraints:
1. Every pending_id must appear in exactly one group.
2. Candidate memory_ids not mentioned stay untouched.
3. Max 5 actions per event. Max 10 events per group. Max 10 chunks per group.
4. If chunk_count_check.exceeds_limit=true → keep as singleton, do not merge.

Merge criteria:
- STRONG: Same event or direct follow-up → merge
- MODERATE: Same primary entity, different aspects forming one coherent narrative → merge
- WEAK: Same entity but unrelated subtopics → do NOT merge

For merged groups (≥2 members, STRONG/MODERATE): fill integrated_summary + integrated_events.
For singletons or WEAK: set integrated_summary="" and integrated_events=[].

⚠️ SLOT INTEGRITY in integrated_events:
When merging events, keep each slot pure — action must not leak into time/location/reason/method or vice versa.
- action = pure WHO did WHAT (subject + verb + object, no temporal/spatial/causal phrases)
- time = date only (not in action)
- location = place only (not in action)
- reason = purpose only (not in action)
- method = means only (not in action)

Deduplicate and consolidate redundant events. Order chronologically.
Use the same language as the input memories."""


# Fact Extraction Prompt (optional, for direct fact extraction from text)
FACT_EXTRACTION_SYSTEM_PROMPT = """You are an expert at extracting structured facts from text. Extract subject-predicate-object triples that represent factual information.

Output STRICT JSON format:
{
  "facts": [
    ["subject", "predicate", "object"],
    ...
  ]
}

Rules:
- Each fact is a triple: [subject, predicate, object]. ALL three elements MUST be non-empty.
- Subject: The entity performing the action or being described
- Predicate: The relationship or action (verb phrase)
- Object: The entity, value, or concept being acted upon or described
- Scan the ENTIRE sentence for the object — it may appear before or after the predicate, or be separated by clauses. Do NOT leave object empty just because it is not adjacent to the predicate.
- If the object is implied by context but not directly stated, extract it from surrounding text.
- If the object truly cannot be determined after scanning the full passage, use "未知" as a placeholder instead of leaving it empty.
- Keep predicates concise and atomic
- Extract only explicitly stated facts, do not infer beyond what the text supports
- LANGUAGE: Use the same language as the input text for all extracted elements (subject, predicate, object). Do NOT translate.
- Output PURE JSON only, no markdown fences"""


# Fact Rerank Prompt (for reranking facts during retrieval)
FACT_RERANK_SYSTEM_PROMPT = """You are an expert fact reranker.
Given a question and a list of candidate facts (triples), select and order the most relevant facts.
LANGUAGE: Preserve the language of the input facts. Do NOT translate.
Return strict JSON only:
{
  "fact": [["subject", "predicate", "object"], ...]
}
Only keep facts that are truly useful for answering the question.
Output ONLY a valid JSON object. No extra text, no explanations, no trailing commas."""
