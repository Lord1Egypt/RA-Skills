/**
 * Subgraph search path — queries facts via GraphQL hash_in.
 *
 * Used when the managed service is active (TOTALRECLAW_SELF_HOSTED is not
 * "true"). Replaces the HTTP POST to /v1/search with a GraphQL query to
 * the subgraph via the relay server.
 *
 * The relay server proxies GraphQL queries to Graph Studio with its own
 * API key at `${relayUrl}/v1/subgraph`. Clients never need a subgraph endpoint.
 *
 * Query cost optimization:
 *   Phase 1: Single query with ALL trapdoors (1 query).
 *   Phase 2: If saturated (1000 results), split into small parallel batches
 *            so rare trapdoor matches aren't drowned by common ones.
 *   Phase 3: Cursor-based pagination for any saturated batch.
 *
 * This minimizes Graph Network query costs (pay-per-query via GRT):
 *   - Small datasets (<1000 matches): 1 query total
 *   - Medium datasets: 1 + N batch queries
 *   - Large datasets: 1 + N batches + pagination queries
 */

import { getSubgraphConfig } from './subgraph-store.js';
import { CONFIG } from './config.js';
import { buildRelayHeaders } from './relay-headers.js';

export interface SubgraphSearchFact {
  id: string;
  encryptedBlob: string;
  encryptedEmbedding: string | null;
  decayScore: string;
  timestamp: string;
  isActive: boolean;
}

/** Batch size for Phase 2 split queries. */
const TRAPDOOR_BATCH_SIZE = CONFIG.trapdoorBatchSize;
/** Graph Studio / Graph Network hard limit on `first` argument. */
const PAGE_SIZE = CONFIG.pageSize;

/**
 * Execute a single GraphQL query against the subgraph endpoint.
 * Returns null on any network or HTTP error (never throws).
 */
async function gqlQuery<T>(
  endpoint: string,
  query: string,
  variables: Record<string, unknown>,
  authKeyHex?: string,
): Promise<T | null> {
  try {
    const overrides: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (authKeyHex) {
      overrides['Authorization'] = `Bearer ${authKeyHex}`;
    }
    const headers = buildRelayHeaders(overrides);
    const response = await fetch(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query, variables }),
    });
    if (!response.ok) {
      const body = await response.text().catch(() => '');
      console.error(`[TotalReclaw] Subgraph query failed: HTTP ${response.status} — ${body.slice(0, 200)}`);
      return null;
    }
    const json = await response.json() as { data?: T; error?: string; errors?: Array<{ message: string }> };
    if (json.error || json.errors) {
      console.error(`[TotalReclaw] Subgraph query error: ${json.error || json.errors?.map(e => e.message).join('; ')}`);
    }
    return json.data ?? null;
  } catch (err) {
    console.error(`[TotalReclaw] Subgraph query exception: ${err instanceof Error ? err.message : String(err)}`);
    return null;
  }
}

/** GraphQL query for blind index lookup. */
const SEARCH_QUERY = `
  query SearchByBlindIndex($trapdoors: [String!]!, $owner: Bytes!, $first: Int!) {
    blindIndexes(
      where: { hash_in: $trapdoors, owner: $owner, fact_: { isActive: true } }
      first: $first
      orderBy: id
      orderDirection: desc
    ) {
      id
      fact {
        id
        encryptedBlob
        encryptedEmbedding
        decayScore
        timestamp
        createdAt
        isActive
        contentFp
        sequenceId
        version
      }
    }
  }
`;

/** Pagination query — cursor-based using id_gt, ascending for deterministic walk. */
const PAGINATE_QUERY = `
  query PaginateBlindIndex($trapdoors: [String!]!, $owner: Bytes!, $first: Int!, $lastId: String!) {
    blindIndexes(
      where: { hash_in: $trapdoors, owner: $owner, id_gt: $lastId, fact_: { isActive: true } }
      first: $first
      orderBy: id
      orderDirection: asc
    ) {
      id
      fact {
        id
        encryptedBlob
        encryptedEmbedding
        timestamp
        createdAt
        decayScore
        isActive
        contentFp
        sequenceId
        version
      }
    }
  }
`;

interface BlindIndexEntry {
  id: string;
  fact: SubgraphSearchFact;
}

interface SearchResponse {
  blindIndexes?: BlindIndexEntry[];
}

/** Collect facts from blind index entries, deduplicating by fact id. */
function collectFacts(
  entries: BlindIndexEntry[],
  allResults: Map<string, SubgraphSearchFact>,
): void {
  for (const entry of entries) {
    if (entry.fact && entry.fact.isActive !== false && !allResults.has(entry.fact.id)) {
      allResults.set(entry.fact.id, entry.fact);
    }
  }
}

/**
 * Paginate a single trapdoor chunk until exhausted or maxCandidates reached.
 */
async function paginateChunk(
  subgraphUrl: string,
  chunk: string[],
  owner: string,
  allResults: Map<string, SubgraphSearchFact>,
  maxCandidates: number,
  authKeyHex?: string,
): Promise<void> {
  let lastId = '';
  while (allResults.size < maxCandidates) {
    const data = await gqlQuery<SearchResponse>(
      subgraphUrl,
      PAGINATE_QUERY,
      { trapdoors: chunk, owner, first: PAGE_SIZE, lastId },
      authKeyHex,
    );
    const entries = data?.blindIndexes ?? [];
    if (entries.length === 0) break;
    collectFacts(entries, allResults);
    if (entries.length < PAGE_SIZE) break;
    lastId = entries[entries.length - 1].id;
  }
}

/**
 * Search the subgraph for facts matching the given trapdoors.
 *
 * Adaptive strategy to minimize query costs:
 *
 *   Phase 1: Single query with ALL trapdoors.
 *     - If not saturated (< PAGE_SIZE results): done. 1 query total.
 *     - If saturated: common trapdoors may be drowning rare ones. Go to Phase 2.
 *
 *   Phase 2: Split trapdoors into small parallel batches (TRAPDOOR_BATCH_SIZE=5).
 *     - Each batch independently gets up to PAGE_SIZE results.
 *     - Rare trapdoor matches get their own budget.
 *
 *   Phase 3: Cursor-based pagination for any saturated batch.
 *     - Only for power users with very large datasets.
 */
export async function searchSubgraph(
  owner: string,
  trapdoors: string[],
  maxCandidates: number,
  authKeyHex?: string,
): Promise<SubgraphSearchFact[]> {
  const config = getSubgraphConfig();
  const subgraphUrl = `${config.relayUrl}/v1/subgraph`;
  const allResults = new Map<string, SubgraphSearchFact>();

  // -----------------------------------------------------------------------
  // Phase 1: Single query with all trapdoors (1 query)
  // -----------------------------------------------------------------------
  const phase1 = await gqlQuery<SearchResponse>(
    subgraphUrl,
    SEARCH_QUERY,
    { trapdoors, owner, first: PAGE_SIZE },
    authKeyHex,
  );

  const phase1Entries = phase1?.blindIndexes ?? [];
  collectFacts(phase1Entries, allResults);

  // Not saturated — we got everything in 1 query. Done.
  if (phase1Entries.length < PAGE_SIZE) {
    return Array.from(allResults.values());
  }

  // -----------------------------------------------------------------------
  // Phase 2: Saturated — split into small batches for better rare-word recall.
  // Common trapdoors were drowning rare ones in the single-query result.
  // -----------------------------------------------------------------------
  const chunks: string[][] = [];
  for (let i = 0; i < trapdoors.length; i += TRAPDOOR_BATCH_SIZE) {
    chunks.push(trapdoors.slice(i, i + TRAPDOOR_BATCH_SIZE));
  }

  const batchResults = await Promise.all(
    chunks.map(async (chunk) => {
      const data = await gqlQuery<SearchResponse>(
        subgraphUrl,
        SEARCH_QUERY,
        { trapdoors: chunk, owner, first: PAGE_SIZE },
        authKeyHex,
      );
      return { chunk, entries: data?.blindIndexes ?? [] };
    }),
  );

  const saturatedChunks: string[][] = [];
  for (const { chunk, entries } of batchResults) {
    collectFacts(entries, allResults);
    if (entries.length >= PAGE_SIZE) {
      saturatedChunks.push(chunk);
    }
  }

  // -----------------------------------------------------------------------
  // Phase 3: Cursor-based pagination for saturated batches (power users).
  // -----------------------------------------------------------------------
  for (const chunk of saturatedChunks) {
    if (allResults.size >= maxCandidates) break;
    await paginateChunk(subgraphUrl, chunk, owner, allResults, maxCandidates, authKeyHex);
  }

  return Array.from(allResults.values());
}

/**
 * Broadened search: fetch recent active facts by owner without trapdoor filtering.
 * Used as a fallback when trapdoor search returns 0 candidates (e.g., vague queries
 * like "who am I?" where word trapdoors don't overlap with stored fact tokens).
 */
export async function searchSubgraphBroadened(
  owner: string,
  maxCandidates: number,
  authKeyHex?: string,
): Promise<SubgraphSearchFact[]> {
  const config = getSubgraphConfig();
  const subgraphUrl = `${config.relayUrl}/v1/subgraph`;

  const query = `
    query BroadenedSearch($owner: Bytes!, $first: Int!) {
      facts(
        where: { owner: $owner, isActive: true }
        first: $first
        orderBy: timestamp
        orderDirection: desc
      ) {
        id
        encryptedBlob
        encryptedEmbedding
        decayScore
        timestamp
        createdAt
        isActive
        contentFp
        sequenceId
        version
      }
    }
  `;

  const data = await gqlQuery<{ facts?: SubgraphSearchFact[] }>(
    subgraphUrl,
    query,
    { owner, first: Math.min(maxCandidates, 1000) },
    authKeyHex,
  );

  return (data?.facts ?? []).filter(f => f.isActive !== false);
}

/**
 * Fetch a single fact by its client-generated UUID.
 *
 * Used by the pin/unpin tools to retrieve a known fact's encrypted blob and
 * metadata for re-encryption with an updated status. Returns null if the fact
 * is not found, has been tombstoned (isActive=false), or the owner does not
 * match the caller's Smart Account address (defense against stale IDs from
 * another user's recall results).
 */
export async function fetchFactById(
  owner: string,
  factId: string,
  authKeyHex?: string,
): Promise<(SubgraphSearchFact & { owner: string }) | null> {
  const config = getSubgraphConfig();
  const subgraphUrl = `${config.relayUrl}/v1/subgraph`;

  const query = `
    query GetFactById($id: ID!) {
      fact(id: $id) {
        id
        owner
        encryptedBlob
        encryptedEmbedding
        decayScore
        timestamp
        createdAt
        isActive
        contentFp
        sequenceId
        version
      }
    }
  `;

  const data = await gqlQuery<{ fact?: (SubgraphSearchFact & { owner: string }) | null }>(
    subgraphUrl,
    query,
    { id: factId },
    authKeyHex,
  );

  const fact = data?.fact;
  if (!fact) return null;
  if (fact.isActive === false) return null;
  if (typeof fact.owner === 'string' && fact.owner.toLowerCase() !== owner.toLowerCase()) {
    return null;
  }
  return fact;
}

/**
 * Get fact count from the subgraph for dynamic pool sizing.
 * Uses the globalStates entity for a lightweight single-row lookup
 * instead of fetching and counting individual fact IDs.
 */
export async function getSubgraphFactCount(owner: string, authKeyHex?: string): Promise<number> {
  const config = getSubgraphConfig();
  const subgraphUrl = `${config.relayUrl}/v1/subgraph`;

  const query = `
    query FactCount {
      globalStates(first: 1) {
        totalFacts
      }
    }
  `;

  const data = await gqlQuery<{ globalStates?: Array<{ totalFacts: string }> }>(
    subgraphUrl,
    query,
    {},
    authKeyHex,
  );

  if (data?.globalStates && data.globalStates.length > 0) {
    const count = parseInt(data.globalStates[0].totalFacts, 10);
    return isNaN(count) ? 0 : count;
  }

  return 0;
}
