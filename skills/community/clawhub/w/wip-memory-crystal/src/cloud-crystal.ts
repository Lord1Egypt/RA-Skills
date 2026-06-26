/// <reference types="@cloudflare/workers-types" />
// cloud-crystal.ts — D1 + Vectorize backend for Memory Crystal Cloud.
//
// DEPRECATED: Demo/onboarding only. Not the production architecture.
// With full LDM tree sync, every node has the complete database locally.
// All search is local. Cloud search is unnecessary.
// See RELAY.md and TECHNICAL.md for the production sync model.
//
// Implements the same search/remember/forget/status interface as the local Crystal,
// but backed by Cloudflare D1 (SQL + FTS5) and Vectorize (vector search).
// Used by the cloud MCP Worker (worker-mcp.ts) for demo/onboarding purposes.

export interface CloudEnv {
  DB: D1Database;
  VECTORIZE: VectorizeIndex;
  OPENAI_API_KEY: string;
}

export interface SearchResult {
  id: number;
  text: string;
  score: number;
  role: string;
  agent_id: string;
  created_at: string;
  source_type: string;
}

export interface Memory {
  id: number;
  text: string;
  category: string;
  status: string;
  created_at: string;
  updated_at: string;
}

// ── Embedding ──

async function embed(text: string, apiKey: string): Promise<number[]> {
  const resp = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'text-embedding-3-small',
      input: text,
      dimensions: 1024,
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Embedding failed: ${resp.status} ${err}`);
  }

  const data = await resp.json() as { data: { embedding: number[] }[] };
  return data.data[0].embedding;
}

// ── CloudCrystal ──

export class CloudCrystal {
  constructor(
    private db: D1Database,
    private vectorize: VectorizeIndex,
    private apiKey: string,
  ) {}

  // Hybrid search: BM25 (FTS5) + vector (Vectorize) + RRF fusion + recency
  async search(userId: string, query: string, limit = 5, agentId?: string): Promise<SearchResult[]> {
    // BM25 search via FTS5
    const agentFilter = agentId ? 'AND c.agent_id = ?' : '';
    const bm25Params: unknown[] = [userId, query];
    if (agentId) bm25Params.push(agentId);

    const bm25Results = await this.db.prepare(`
      SELECT c.id, c.text, c.role, c.agent_id, c.created_at, c.source_type,
             rank AS bm25_score
      FROM chunks_fts f
      JOIN chunks c ON c.id = f.rowid
      WHERE f.text MATCH ? AND c.user_id = ? ${agentFilter}
      ORDER BY rank
      LIMIT ?
    `).bind(query, userId, ...(agentId ? [agentId] : []), limit * 3).all();

    // Vector search via Vectorize
    const queryVec = await embed(query, this.apiKey);
    const vecResults = await this.vectorize.query(queryVec, {
      topK: limit * 3,
      filter: { user_id: userId, ...(agentId ? { agent_id: agentId } : {}) },
      returnMetadata: 'all',
    });

    // RRF fusion (k=60)
    const k = 60;
    const scores = new Map<number, { score: number; data?: any }>();

    // BM25 rankings
    const bm25Rows = (bm25Results.results || []) as any[];
    for (let i = 0; i < bm25Rows.length; i++) {
      const id = bm25Rows[i].id as number;
      const existing = scores.get(id) || { score: 0, data: bm25Rows[i] };
      existing.score += 1 / (k + i + 1);
      scores.set(id, existing);
    }

    // Vector rankings
    for (let i = 0; i < vecResults.matches.length; i++) {
      const match = vecResults.matches[i];
      const id = parseInt(match.id, 10);
      const existing = scores.get(id) || { score: 0 };
      existing.score += 1 / (k + i + 1);
      scores.set(id, existing);
    }

    // Recency boost (same as local Crystal)
    const now = Date.now();
    for (const [id, entry] of scores) {
      if (entry.data?.created_at) {
        const age = now - new Date(entry.data.created_at).getTime();
        const dayAge = age / (1000 * 60 * 60 * 24);
        const recencyBoost = Math.max(0, 1 - dayAge / 90) * 0.15;
        entry.score += recencyBoost;
      }
    }

    // Sort by score, take top N
    const ranked = [...scores.entries()]
      .sort((a, b) => b[1].score - a[1].score)
      .slice(0, limit);

    // Fetch full data for any results we don't have yet
    const needFetch = ranked.filter(([_, v]) => !v.data).map(([id]) => id);
    if (needFetch.length > 0) {
      const placeholders = needFetch.map(() => '?').join(',');
      const rows = await this.db.prepare(
        `SELECT id, text, role, agent_id, created_at, source_type FROM chunks WHERE id IN (${placeholders})`
      ).bind(...needFetch).all();
      const rowMap = new Map((rows.results as any[]).map(r => [r.id, r]));
      for (const [id, entry] of scores) {
        if (!entry.data && rowMap.has(id)) {
          entry.data = rowMap.get(id);
        }
      }
    }

    return ranked.map(([id, entry]) => ({
      id,
      text: entry.data?.text || '',
      score: entry.score,
      role: entry.data?.role || 'unknown',
      agent_id: entry.data?.agent_id || 'unknown',
      created_at: entry.data?.created_at || '',
      source_type: entry.data?.source_type || 'unknown',
    }));
  }

  // Ingest chunks (conversation turns)
  async ingest(userId: string, chunks: Array<{ text: string; role: string; agent_id: string; source_type?: string }>): Promise<number> {
    let ingested = 0;

    for (const chunk of chunks) {
      // Insert into D1
      const result = await this.db.prepare(`
        INSERT INTO chunks (user_id, text, role, agent_id, source_type, token_count)
        VALUES (?, ?, ?, ?, ?, ?)
      `).bind(
        userId,
        chunk.text,
        chunk.role,
        chunk.agent_id,
        chunk.source_type || 'chatgpt',
        Math.ceil(chunk.text.length / 4), // rough token estimate
      ).run();

      const chunkId = result.meta.last_row_id;

      // Embed and upsert to Vectorize
      const vec = await embed(chunk.text, this.apiKey);
      await this.vectorize.upsert([{
        id: String(chunkId),
        values: vec,
        metadata: {
          user_id: userId,
          agent_id: chunk.agent_id,
          role: chunk.role,
          source_type: chunk.source_type || 'chatgpt',
        },
      }]);

      ingested++;
    }

    return ingested;
  }

  // Remember a fact/preference/event
  async remember(userId: string, text: string, category = 'fact'): Promise<number> {
    const result = await this.db.prepare(`
      INSERT INTO memories (user_id, text, category) VALUES (?, ?, ?)
    `).bind(userId, text, category).run();

    return result.meta.last_row_id as number;
  }

  // Forget (deprecate) a memory
  async forget(userId: string, memoryId: number): Promise<boolean> {
    const result = await this.db.prepare(`
      UPDATE memories SET status = 'deprecated', updated_at = datetime('now')
      WHERE id = ? AND user_id = ? AND status = 'active'
    `).bind(memoryId, userId).run();

    return (result.meta.changes || 0) > 0;
  }

  // Status
  async status(userId: string): Promise<{
    chunks: number;
    memories: number;
    agents: string[];
    tier: string;
  }> {
    const chunkCount = await this.db.prepare(
      'SELECT COUNT(*) as count FROM chunks WHERE user_id = ?'
    ).bind(userId).first<{ count: number }>();

    const memoryCount = await this.db.prepare(
      'SELECT COUNT(*) as count FROM memories WHERE user_id = ? AND status = ?'
    ).bind(userId, 'active').first<{ count: number }>();

    const agents = await this.db.prepare(
      'SELECT DISTINCT agent_id FROM chunks WHERE user_id = ?'
    ).bind(userId).all();

    return {
      chunks: chunkCount?.count || 0,
      memories: memoryCount?.count || 0,
      agents: ((agents.results || []) as any[]).map(r => r.agent_id),
      tier: 'convenience', // Tier 2 users only
    };
  }
}
