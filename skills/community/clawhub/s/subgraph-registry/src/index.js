#!/usr/bin/env node

/**
 * Subgraph Registry MCP Server
 *
 * Exposes the classified subgraph registry as MCP tools that agents can call
 * to discover and select the right subgraph before querying The Graph.
 *
 * Tools:
 *   - search_subgraphs: Filter by domain, network, protocol type, entity, keyword
 *   - recommend_subgraph: Natural language goal -> best subgraphs
 *   - get_subgraph_detail: Full classification detail for a specific subgraph
 *   - list_registry_stats: Available domains, networks, protocol types
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";
import express from "express";
import { fileURLToPath, pathToFileURL } from "url";
import { basename, dirname, join } from "path";
import { existsSync, mkdirSync, readFileSync, unlinkSync, writeFileSync } from "fs";
import { get as httpsGet } from "https";
import { createHash } from "crypto";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DATA_DIR = join(__dirname, "..", "data");
const DB_PATH = join(DATA_DIR, "registry.db");
const OPENAPI_JSON_PATH = join(DATA_DIR, "openapi.json");
// Bundled with the npm package so runtime semantic search has zero
// network dependency. Same model fastembed uses at crawl time
// (Xenova/all-MiniLM-L6-v2) — vectors are bitwise-comparable.
const EMBEDDING_MODEL_DIR = join(DATA_DIR, "models", "all-MiniLM-L6-v2");
const GITHUB_DB_URL =
  "https://github.com/PaulieB14/subgraph-registry/raw/main/python/data/registry.db";

// SHA-256 of the registry.db shipped with this npm version. Any download or
// pre-bundled copy that doesn't match this hash is rejected — protects users
// against a compromised GitHub repo or man-in-the-middle on the download.
//
// HOW TO UPDATE WHEN REBUILDING THE REGISTRY:
//   1. Run the crawler to rebuild python/data/registry.db
//   2. shasum -a 256 python/data/registry.db
//   3. Paste the new hash here and bump package.json version
//   4. Update SKILL.md "Verifying the registry" section
const EXPECTED_DB_SHA256 =
  "e141528f7708553bb10db438d29ac438b673cc0fe99bdc4b1685af2e3f10a3cb";
// Skip-verification escape hatch (set to "1" only if you're rebuilding the DB
// locally and know what you're doing — never set in agent-runtime defaults).
const SKIP_VERIFY = process.env.SUBGRAPH_REGISTRY_SKIP_VERIFY === "1";

// ── x402 gateway constants ─────────────────────────────────
// The Graph's public x402 gateway (live since 2026-05-08) lets agents pay
// per-query in USDC on Base without any API key. POST GraphQL to query_url_x402
// and the gateway returns HTTP 402 with a payment manifest; an x402 client
// (e.g. @graphprotocol/client-x402, x402-fetch) signs the EIP-3009 USDC
// transfer and retries automatically.
const X402_GATEWAY_BASE = "https://gateway.thegraph.com/api/x402";
const X402_PRICING = {
  amount_usd: 0.01,
  asset: "USDC",
  asset_contract: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
  chain: "base",
  network: "eip155:8453",
  pay_to: "0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB", // Graph x402 gateway
  scheme: "exact",
  asset_transfer_method: "eip3009",
};

function buildQueryEndpoints(subgraphId) {
  return {
    query_url: `https://gateway.thegraph.com/api/[api-key]/subgraphs/id/${subgraphId}`,
    query_url_x402: `${X402_GATEWAY_BASE}/subgraphs/id/${subgraphId}`,
    pricing: X402_PRICING,
  };
}

// ── Download DB from GitHub if missing ─────────────────────

function sha256OfFile(path) {
  const h = createHash("sha256");
  h.update(readFileSync(path));
  return h.digest("hex");
}

function verifyDbOrThrow(path) {
  if (SKIP_VERIFY) {
    console.error(
      "SUBGRAPH_REGISTRY_SKIP_VERIFY=1 — skipping registry.db hash check."
    );
    return;
  }
  const actual = sha256OfFile(path);
  if (actual !== EXPECTED_DB_SHA256) {
    // Refuse to load a registry that doesn't match the known-good hash.
    // Delete the file so the next run gets a fresh download attempt instead
    // of caching a poisoned copy.
    try { unlinkSync(path); } catch (_) {}
    throw new Error(
      `registry.db SHA-256 mismatch.\n` +
        `  expected: ${EXPECTED_DB_SHA256}\n` +
        `  actual:   ${actual}\n` +
        `The downloaded registry does not match the version pinned to this ` +
        `npm package. Refusing to load. If you intentionally rebuilt the DB ` +
        `locally, set SUBGRAPH_REGISTRY_SKIP_VERIFY=1 to bypass.`
    );
  }
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const follow = (u) => {
      httpsGet(u, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          follow(res.headers.location);
          return;
        }
        if (res.statusCode !== 200) {
          reject(new Error(`Download failed: HTTP ${res.statusCode}`));
          return;
        }
        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          writeFileSync(dest, Buffer.concat(chunks));
          resolve();
        });
        res.on("error", reject);
      }).on("error", reject);
    };
    follow(url);
  });
}

async function ensureDb() {
  if (existsSync(DB_PATH)) {
    verifyDbOrThrow(DB_PATH);
    return;
  }
  mkdirSync(DATA_DIR, { recursive: true });
  console.error("Registry not found locally. Downloading from GitHub...");
  await downloadFile(GITHUB_DB_URL, DB_PATH);
  console.error("Downloaded registry.db — verifying SHA-256...");
  verifyDbOrThrow(DB_PATH);
  console.error("Registry verified OK.");
}

// ── Database ───────────────────────────────────────────────

let db;

function getDb() {
  if (!db) {
    db = new Database(DB_PATH, { readonly: true });
  }
  return db;
}

// ── Tool Implementations ───────────────────────────────────

function searchSubgraphs({
  query = "",
  domain = "",
  network = "",
  protocol_type = "",
  entity = "",
  min_reliability = 0,
  include_unserved = false,
  limit = 20,
} = {}) {
  const conditions = [];
  const params = [];

  // Default: hide deployments with 0 active indexer allocations — these
  // return "subgraph not found: no allocations" even though the ID is valid.
  if (!include_unserved) {
    conditions.push("active_allocation_count > 0");
  }

  if (domain) {
    conditions.push("domain = ?");
    params.push(domain);
  }
  if (network) {
    conditions.push("network = ?");
    params.push(network);
  }
  if (protocol_type) {
    conditions.push("protocol_type = ?");
    params.push(protocol_type);
  }
  if (entity) {
    conditions.push('canonical_entities LIKE ?');
    params.push(`%"${entity}"%`);
  }
  if (min_reliability > 0) {
    conditions.push("reliability_score >= ?");
    params.push(min_reliability);
  }
  if (query) {
    const words = query.trim().split(/\s+/).filter((w) => w.length > 2).slice(0, 5);
    if (words.length) {
      const wordConds = words.map(() => "(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)");
      words.forEach((w) => params.push(`%${w}%`, `%${w}%`, `%${w}%`));
      conditions.push(`(${wordConds.join(" OR ")})`);
    } else {
      conditions.push("(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)");
      params.push(`%${query}%`, `%${query}%`, `%${query}%`);
    }
  }

  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";
  // Over-fetch to allow dedup by IPFS hash (same deployment, different subgraph IDs)
  const fetchLimit = limit * 3;
  const sql = `
    SELECT id, display_name, description, auto_description, domain, protocol_type, network,
           reliability_score, ipfs_hash, entity_count, canonical_entities,
           powered_by_substreams, active_allocation_count
    FROM subgraphs
    ${where}
    ORDER BY reliability_score DESC
    LIMIT ?
  `;
  params.push(fetchLimit);

  const rows = getDb().prepare(sql).all(...params);
  // Dedup by IPFS hash — keep highest reliability per deployment
  const seenIpfs = new Set();
  const results = [];
  for (const r of rows) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    results.push({
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
      ipfs_hash: r.ipfs_hash,
      entity_count: r.entity_count,
      canonical_entities: JSON.parse(r.canonical_entities),
      powered_by_substreams: Boolean(r.powered_by_substreams),
      active_allocation_count: r.active_allocation_count || 0,
      ...buildQueryEndpoints(r.id),
    });
    if (results.length >= limit) break;
  }

  return {
    total: results.length,
    subgraphs: results,
    query_instructions: "Two ways to query: (a) RECOMMENDED — POST GraphQL to query_url_x402 and pay $0.01 USDC on Base per query via x402 (no API key required; gateway returns HTTP 402 with a payment manifest, use an x402 client like @graphprotocol/client-x402 to sign and retry). (b) LEGACY — replace [api-key] in query_url with a Graph API key from https://thegraph.com/studio/apikeys/. Call get_subgraph_detail first for the schema.",
  };
}

function recommendSubgraph({ goal, chain = "" }) {
  const goalLower = goal.toLowerCase();

  const domainMap = {
    defi: ["defi", "swap", "trade", "lend", "borrow", "yield", "stake", "liquidity", "pool", "token"],
    nfts: ["nft", "collectible", "art", "marketplace"],
    dao: ["governance", "vote", "proposal", "dao"],
    identity: ["ens", "domain", "name", "identity"],
    infrastructure: ["indexer", "graph", "oracle"],
    social: ["social", "profile", "post", "lens"],
    gaming: ["game", "player", "quest"],
  };
  const typeMap = {
    dex: ["dex", "swap", "trade", "exchange", "amm", "uniswap", "sushi"],
    lending: ["lend", "borrow", "loan", "collateral", "aave", "compound"],
    bridge: ["bridge", "cross-chain"],
    staking: ["stake", "validator", "delegation"],
    options: ["option", "call", "put", "strike"],
    perpetuals: ["perp", "perpetual", "leverage", "margin"],
    governance: ["governance", "vote", "proposal"],
    "name-service": ["ens", "name service", "domain name"],
    "nft-marketplace": ["nft market", "opensea", "blur"],
  };

  const domains = Object.entries(domainMap)
    .filter(([, kws]) => kws.some((k) => goalLower.includes(k)))
    .map(([d]) => d);
  const ptypes = Object.entries(typeMap)
    .filter(([, kws]) => kws.some((k) => goalLower.includes(k)))
    .map(([t]) => t);

  const conditions = ["active_allocation_count > 0"];
  const params = [];

  if (chain) {
    conditions.push("network = ?");
    params.push(chain);
  }
  if (domains.length) {
    conditions.push(`domain IN (${domains.map(() => "?").join(",")})`);
    params.push(...domains);
  }
  if (ptypes.length) {
    conditions.push(`protocol_type IN (${ptypes.map(() => "?").join(",")})`);
    params.push(...ptypes);
  }

  if (!domains.length && !ptypes.length) {
    const words = goalLower.split(/\s+/).filter((w) => w.length > 2).slice(0, 5);
    if (words.length) {
      const textConds = words.map(() => "(display_name LIKE ? OR description LIKE ?)");
      words.forEach((w) => params.push(`%${w}%`, `%${w}%`));
      conditions.push(`(${textConds.join(" OR ")})`);
    }
  }

  const where = `WHERE ${conditions.join(" AND ")}`;
  const sql = `
    SELECT id, display_name, description, auto_description, domain, protocol_type, network,
           reliability_score, ipfs_hash, canonical_entities, active_allocation_count
    FROM subgraphs
    ${where}
    ORDER BY reliability_score DESC
    LIMIT 15
  `;

  const rows = getDb().prepare(sql).all(...params);
  // De-dup first so we batch the stability lookup over the trimmed set.
  const seenIpfs = new Set();
  const keep = [];
  for (const r of rows) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    keep.push(r);
    if (keep.length >= 5) break;
  }
  // Batch the schema-stability lookup into ONE SELECT instead of N+1.
  // Falls back to {} if the schema_history table doesn't exist (pre-
  // feature DB snapshot).
  const stabMap = getSchemaStabilityBatch(keep.map((r) => r.id));
  const recommendations = keep.map((r) => {
    const stab = stabMap[r.id] || {
      schema_changed_at: null,
      schema_stable_days: null,
    };
    return {
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
      ipfs_hash: r.ipfs_hash,
      canonical_entities: JSON.parse(r.canonical_entities),
      active_allocation_count: r.active_allocation_count || 0,
      schema_changed_at: stab.schema_changed_at,
      schema_stable_days: stab.schema_stable_days,
      ...buildQueryEndpoints(r.id),
    };
  });

  return {
    goal,
    chain_filter: chain || null,
    inferred_domain: domains.length ? domains : null,
    inferred_protocol_type: ptypes.length ? ptypes : null,
    total_matches: recommendations.length,
    recommendations,
  };
}

function getSubgraphDetail({ subgraph_id }) {
  const row = getDb()
    .prepare("SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?")
    .get(subgraph_id, subgraph_id);

  if (!row) return { error: `Subgraph '${subgraph_id}' not found` };

  const result = { ...row };
  result.canonical_entities = JSON.parse(result.canonical_entities);
  result.categories = JSON.parse(result.categories);
  if (result.all_entities) result.all_entities = JSON.parse(result.all_entities);
  // Contract addresses extracted from the manifest — list of
  // {kind, name, address, network, startBlock}. Null on subgraphs we
  // haven't crawled with manifest support yet, or substreams-powered ones.
  if (result.contract_addresses) {
    try { result.contract_addresses = JSON.parse(result.contract_addresses); }
    catch { /* leave as string if not valid JSON */ }
  }
  if (!result.description && result.auto_description) {
    result.description = result.auto_description;
  }
  const endpoints = buildQueryEndpoints(result.id);
  result.query_url = endpoints.query_url;
  result.query_url_x402 = endpoints.query_url_x402;
  result.pricing = endpoints.pricing;

  // Schema-evolution fields. Surfaces how long the schema has been
  // stable (schema_stable_days) and the unix timestamp of the last
  // detected fingerprint change. Helps agents prefer mature subgraphs.
  const stab = getSchemaStabilityFor(result.id);
  result.schema_changed_at = stab.schema_changed_at;
  result.schema_stable_days = stab.schema_stable_days;
  // Don't leak the embedding blob to MCP callers — it's 1.5 KB of
  // float32 bytes that's only useful for cosine math inside the server.
  delete result.embedding;

  // Per-subgraph starter query generated by the crawler from this subgraph's
  // parsed schema. Falls back to the legacy generic example when the column
  // is empty (pre-feature DBs).
  const FALLBACK_EXAMPLE =
    "{ pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) { id token0 { symbol } token1 { symbol } totalValueLockedUSD } }";
  const exampleQuery = result.example_query || FALLBACK_EXAMPLE;

  result.query_instructions = {
    recommended: "x402",
    x402: {
      url: endpoints.query_url_x402,
      payment: endpoints.pricing,
      flow: "POST GraphQL to url. Gateway returns HTTP 402 with a base64 payment-required header containing the payment manifest. Sign $0.01 USDC on Base with an x402 client and retry. No API key, no signup.",
      client_libraries: ["@graphprotocol/client-x402", "x402-fetch"],
      example_query: exampleQuery,
    },
    api_key_legacy: {
      url: endpoints.query_url,
      flow: "Get an API key from https://thegraph.com/studio/apikeys/, replace [api-key] in the url, then POST GraphQL.",
    },
    schema_hint: result.example_query
      ? "example_query above was generated from this subgraph's actual schema. Adapt the entity name + field selection as needed."
      : "Use the all_entities field above to see what entities and fields are available to query.",
  };
  return result;
}


// ── JSON-LD per-subgraph well-known shape ─────────────────────────────────
// Stable, machine-readable manifest other crawlers and agents can index
// without going through MCP. Served at /.well-known/subgraph/{id}.jsonld and
// /subgraphs/{id}.jsonld (alias, same payload).
const JSONLD_CONTEXT = "https://subgraph-registry.paulieb14.dev/context.jsonld";

function buildJsonLdManifest(row) {
  if (!row) return null;
  const detail = getSubgraphDetail({ subgraph_id: row.id });
  if (detail?.error) return null;
  return {
    "@context": JSONLD_CONTEXT,
    "@type": "SubgraphDeployment",
    "@id": `https://subgraph-registry.paulieb14.dev/subgraphs/${row.id}`,
    id: row.id,
    ipfsHash: row.ipfs_hash,
    name: row.display_name,
    description: row.description || row.auto_description,
    network: row.network,
    classification: {
      domain: row.domain,
      protocolType: row.protocol_type,
      confidence: row.classification_confidence,
    },
    entities: detail.all_entities || [],
    canonicalEntities: detail.canonical_entities || [],
    contracts: detail.contract_addresses || null,
    reliabilityScore: row.reliability_score,
    activeIndexers: row.active_allocation_count,
    queryVolume30d: row.query_volume_30d,
    endpoints: {
      x402: detail.query_url_x402,
      apiKey: detail.query_url,
    },
    exampleQuery: detail.query_instructions?.x402?.example_query || null,
    poweredBySubstreams: !!row.powered_by_substreams,
    pricing: detail.pricing,
  };
}

function listRegistryStats() {
  const d = getDb();
  const domains = d
    .prepare("SELECT domain, COUNT(*) as count FROM subgraphs GROUP BY domain ORDER BY count DESC")
    .all();
  const networks = d
    .prepare("SELECT network, COUNT(*) as count FROM subgraphs WHERE network IS NOT NULL GROUP BY network ORDER BY count DESC")
    .all();
  const ptypes = d
    .prepare("SELECT protocol_type, COUNT(*) as count FROM subgraphs GROUP BY protocol_type ORDER BY count DESC")
    .all();
  const total = d.prepare("SELECT COUNT(*) as c FROM subgraphs").get().c;

  return {
    total_subgraphs: total,
    domains: Object.fromEntries(domains.map((r) => [r.domain, r.count])),
    networks: Object.fromEntries(networks.map((r) => [r.network, r.count])),
    protocol_types: Object.fromEntries(ptypes.map((r) => [r.protocol_type, r.count])),
  };
}

// ── Semantic search (vector embeddings) ───────────────────
// At crawl time the Python pipeline computes a 384-dim
// sentence-transformers/all-MiniLM-L6-v2 embedding per subgraph and
// stores it as a little-endian float32 BLOB in the `embedding` column.
// At query time the Node MCP server loads the SAME model architecture
// via @xenova/transformers (quantized INT8 ONNX bundled under
// data/models/) and embeds the query string once, then ranks rows by
// cosine similarity. No PyTorch, no Python sidecar — runtime is pure
// JS + sqlite.
//
// IMPORTANT: vectors are NOT bitwise-identical across runtimes. The JS
// side is INT8-quantized; the Python side is float32. Top-K rankings
// are stable but absolute scores can drift by ~0.01-0.03. The default
// `min_score: 0.3` is calibrated for the quantized JS side. If you
// run cross-runtime cosine comparisons, expect approximate not exact
// agreement.

let _embedderPromise = null;

async function getEmbedder() {
  // Lazy single-load; ~23 MB ONNX. First call latency ~1-2s on cold
  // start, subsequent calls are ~5-20ms per query embed.
  if (!_embedderPromise) {
    _embedderPromise = (async () => {
      // Dynamic import keeps the cold-start cost off the critical
      // path of tools that don't need embeddings (search_subgraphs,
      // get_subgraph_detail, list_registry_stats).
      const { pipeline, env } = await import("@xenova/transformers");
      // Prefer the locally-bundled model so the package works offline
      // and at zero-egress hosting. Falls back to the HF hub if the
      // bundled dir is missing (e.g. running from a git checkout
      // before the model stage step has run).
      if (existsSync(EMBEDDING_MODEL_DIR)) {
        env.localModelPath = join(DATA_DIR, "models");
        env.allowRemoteModels = false;
      }
      const extractor = await pipeline(
        "feature-extraction",
        "all-MiniLM-L6-v2",
        { quantized: true },
      );
      return extractor;
    })();
  }
  return _embedderPromise;
}

async function embedQuery(text) {
  const extractor = await getEmbedder();
  // pooling: "mean" + normalize: true matches sentence-transformers
  // default — identical to what fastembed produces server-side.
  const output = await extractor(text, { pooling: "mean", normalize: true });
  // output.data is a Float32Array of length 384
  return output.data;
}

function blobToFloat32(buf) {
  // SQLite returns the BLOB as a Node Buffer. better-sqlite3's Buffers
  // are views into a pooled slab with NO byteOffset alignment guarantee
  // — and Float32Array requires byteOffset to be a multiple of 4. Wrap-
  // without-copy used to throw `RangeError: start offset of Float32Array
  // should be a multiple of 4` on any row whose blob landed at an odd
  // offset (~7/8 of the time in production). Copy the bytes into a
  // fresh aligned ArrayBuffer instead — the 1.5 KB/row alloc dwarfs the
  // cosine compute that follows anyway.
  const ab = buf.buffer.slice(
    buf.byteOffset,
    buf.byteOffset + buf.byteLength,
  );
  return new Float32Array(ab);
}

function cosineSim(a, b) {
  // Assumes vectors are already L2-normalized (they are: the embedder
  // is called with normalize:true and fastembed normalizes by default).
  // For normalized vectors, cosine sim == dot product.
  let dot = 0;
  const n = Math.min(a.length, b.length);
  for (let i = 0; i < n; i++) dot += a[i] * b[i];
  return dot;
}

async function semanticSearchSubgraphs({
  query,
  limit = 10,
  min_score = 0.3,
  include_unserved = false,
  domain = "",
  network = "",
  protocol_type = "",
  min_reliability = 0,
}) {
  if (!query || typeof query !== "string") {
    return { error: "query is required and must be a string" };
  }
  // Clamp limit — the inputSchema declares maximum:50 but MCP clients
  // don't validate by default. Without the clamp, `limit: 10000` just
  // sorts more results pointlessly.
  limit = Math.max(1, Math.min(Number(limit) || 10, 50));
  if (typeof min_score !== "number" || isNaN(min_score)) min_score = 0.3;

  const qvec = await embedQuery(query);

  // SQL pre-filter shaves ~14k → <1k rows for narrow queries (e.g.
  // "lending positions on Arbitrum"). Cosine math runs only on the
  // post-filter set.
  const conditions = ["embedding IS NOT NULL"];
  const params = [];
  if (!include_unserved) {
    conditions.push("active_allocation_count > 0");
  }
  if (domain) {
    conditions.push("domain = ?");
    params.push(domain);
  }
  if (network) {
    conditions.push("network = ?");
    params.push(network);
  }
  if (protocol_type) {
    conditions.push("protocol_type = ?");
    params.push(protocol_type);
  }
  if (typeof min_reliability === "number" && min_reliability > 0) {
    conditions.push("reliability_score >= ?");
    params.push(min_reliability);
  }
  const where = `WHERE ${conditions.join(" AND ")}`;
  const rows = getDb()
    .prepare(
      `SELECT id, display_name, description, auto_description, domain,
              protocol_type, network, reliability_score, ipfs_hash,
              entity_count, canonical_entities, powered_by_substreams,
              active_allocation_count, embedding
       FROM subgraphs
       ${where}`,
    )
    .all(...params);

  // Score every row. With ~14k subgraphs × 384 floats this is ~5ms on
  // a modern x64 box — cheap enough to do linearly per request.
  const scored = [];
  const seenIpfs = new Set();
  for (const r of rows) {
    const vec = blobToFloat32(r.embedding);
    const score = cosineSim(qvec, vec);
    if (score < min_score) continue;
    scored.push({ row: r, score });
  }
  scored.sort((a, b) => b.score - a.score);

  const results = [];
  for (const { row: r, score } of scored) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    results.push({
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
      ipfs_hash: r.ipfs_hash,
      entity_count: r.entity_count,
      canonical_entities: JSON.parse(r.canonical_entities),
      powered_by_substreams: Boolean(r.powered_by_substreams),
      active_allocation_count: r.active_allocation_count || 0,
      semantic_score: Number(score.toFixed(4)),
      ...buildQueryEndpoints(r.id),
    });
    if (results.length >= limit) break;
  }

  return {
    query,
    total: results.length,
    model: "sentence-transformers/all-MiniLM-L6-v2",
    subgraphs: results,
    query_instructions:
      "Each result includes query_url_x402 (pay $0.01 USDC on Base, no API key) and a legacy query_url. semantic_score is cosine similarity in [0,1]; values >0.5 are typically strong matches.",
  };
}

// ── Schema evolution ──────────────────────────────────────
// schema_history is append-only: one row per fingerprint change for a
// given subgraph_id. Read at query time to surface "how long has this
// schema been stable?" so agents can prefer subgraphs whose contract
// of data is mature.

function getSchemaChanges({ subgraph_id, since_timestamp = 0 }) {
  if (!subgraph_id || typeof subgraph_id !== "string") {
    return { error: "subgraph_id is required and must be a string" };
  }
  // Coerce since_timestamp to a non-negative integer. SQLite has loose
  // typing so passing a string like "2024-01-01" used to silently match
  // nothing; passing NaN matched everything. Validate at the boundary.
  let since = Number(since_timestamp);
  if (!Number.isFinite(since) || since < 0) since = 0;
  since = Math.floor(since);

  // Always return the same key set so agents can pattern-match against
  // a stable shape even when the schema_history table is missing.
  const now = Math.floor(Date.now() / 1000);
  const baseShape = {
    subgraph_id,
    total_changes: 0,
    last_changed_at: null,
    stable_days: null,
    changed_within_24h: false,
    changed_within_7d: false,
    changes: [],
  };

  let rows;
  try {
    rows = getDb()
      .prepare(
        `SELECT fingerprint, prev_fingerprint, detected_at, ipfs_hash
         FROM schema_history
         WHERE subgraph_id = ? AND detected_at >= ?
         ORDER BY detected_at DESC`,
      )
      .all(subgraph_id, since);
  } catch (err) {
    // schema_history table doesn't exist yet (pre-feature DB snapshot).
    return {
      ...baseShape,
      note: "schema_history table not present in this registry.db — feature ships in v0.7+.",
    };
  }

  const last_changed_at = rows.length > 0 ? rows[0].detected_at : null;
  const stable_days =
    last_changed_at !== null
      ? Math.round(((now - last_changed_at) / 86400) * 10) / 10
      : null;

  return {
    subgraph_id,
    total_changes: rows.length,
    last_changed_at,
    stable_days,
    changed_within_24h:
      last_changed_at !== null && now - last_changed_at < 86400,
    changed_within_7d:
      last_changed_at !== null && now - last_changed_at < 86400 * 7,
    changes: rows.map((r) => ({
      fingerprint: r.fingerprint,
      prev_fingerprint: r.prev_fingerprint,
      detected_at: r.detected_at,
      ipfs_hash: r.ipfs_hash,
    })),
  };
}

function getSchemaStabilityFor(id) {
  // Light-weight helper used by get_subgraph_detail to enrich a single
  // row with schema-stability fields. Falls back to nulls if the
  // schema_history table doesn't exist (older DB snapshots). For
  // recommend_subgraph, use getSchemaStabilityBatch instead — it
  // collapses N queries into one.
  try {
    const r = getDb()
      .prepare(
        "SELECT MAX(detected_at) AS schema_changed_at " +
          "FROM schema_history WHERE subgraph_id = ?",
      )
      .get(id);
    if (!r || r.schema_changed_at == null) {
      return { schema_changed_at: null, schema_stable_days: null };
    }
    const now = Math.floor(Date.now() / 1000);
    const days = Math.round(((now - r.schema_changed_at) / 86400) * 10) / 10;
    return { schema_changed_at: r.schema_changed_at, schema_stable_days: days };
  } catch (_) {
    return { schema_changed_at: null, schema_stable_days: null };
  }
}

function getSchemaStabilityBatch(ids) {
  // Single GROUP BY query for up to ~5-50 subgraph IDs. Returns a map
  // { [id]: { schema_changed_at, schema_stable_days } }. Empty map on
  // missing table or empty input.
  if (!Array.isArray(ids) || ids.length === 0) return {};
  try {
    const placeholders = ids.map(() => "?").join(",");
    const rows = getDb()
      .prepare(
        `SELECT subgraph_id, MAX(detected_at) AS schema_changed_at
         FROM schema_history
         WHERE subgraph_id IN (${placeholders})
         GROUP BY subgraph_id`,
      )
      .all(...ids);
    const now = Math.floor(Date.now() / 1000);
    const out = {};
    for (const r of rows) {
      if (r.schema_changed_at == null) {
        out[r.subgraph_id] = {
          schema_changed_at: null,
          schema_stable_days: null,
        };
        continue;
      }
      out[r.subgraph_id] = {
        schema_changed_at: r.schema_changed_at,
        schema_stable_days:
          Math.round(((now - r.schema_changed_at) / 86400) * 10) / 10,
      };
    }
    return out;
  } catch (_) {
    return {};
  }
}

// ── MCP Server ─────────────────────────────────────────────

const TOOLS = [
  {
    name: "search_subgraphs",
    description:
      "Search and filter the classified subgraph registry (15,500+ subgraphs). Filter by domain (defi, nfts, dao, gaming, identity, infrastructure, social, analytics), network (mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche), protocol_type (dex, lending, bridge, staking, options, perpetuals, nft-marketplace, yield-aggregator, governance, name-service), canonical entity type (liquidity_pool, trade, token, position, vault, loan, collateral, liquidation, nft_collection, nft_item, nft_sale, proposal, delegate, domain_name, account, transaction, daily_snapshot, hourly_snapshot), or free-text keyword. Returns subgraphs ranked by reliability score. Each result includes query_url_x402 (POST GraphQL and pay $0.01 USDC on Base per query — no API key needed) and a legacy query_url (Studio API key required).",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: { type: "string", description: "Free-text search across names and descriptions" },
        domain: { type: "string", description: "Filter by domain: defi, nfts, dao, gaming, identity, infrastructure, social, analytics" },
        network: { type: "string", description: "Filter by chain: mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche, etc." },
        protocol_type: { type: "string", description: "Filter by protocol type: dex, lending, bridge, staking, options, perpetuals, etc." },
        entity: { type: "string", description: "Filter by canonical entity: liquidity_pool, trade, token, position, vault, loan, etc." },
        min_reliability: { type: "number", description: "Minimum reliability score (0-1). Higher = more query fees, volume, curation signal, and indexer allocation." },
        limit: { type: "integer", description: "Max results to return (default: 20)", default: 20 },
      },
    },
  },
  {
    name: "recommend_subgraph",
    description:
      "Given a natural-language goal like 'find DEX trades on Arbitrum' or 'get lending liquidation data', returns the best matching subgraphs with reliability scores. Automatically infers domain and protocol type from the goal. Each result includes query_url_x402 (preferred — POST GraphQL, pay $0.01 USDC on Base per query, no API key) and a legacy query_url for Studio-key flows.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        goal: { type: "string", description: "What you want to do, e.g. 'query Uniswap pool data on Base'" },
        chain: { type: "string", description: "Optional chain filter: mainnet, arbitrum-one, base, matic, etc." },
      },
      required: ["goal"],
    },
  },
  {
    name: "get_subgraph_detail",
    description:
      "Get full classification detail for a specific subgraph by its subgraph ID or IPFS hash. Returns domain, protocol type, canonical entities, all entity names with field counts, reliability score, signal data, both query URLs (x402 and legacy), the x402 pricing manifest ($0.01 USDC on Base), and step-by-step instructions for both query paths.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: { type: "string", description: "Subgraph ID or IPFS hash (Qm...)" },
      },
      required: ["subgraph_id"],
    },
  },
  {
    name: "list_registry_stats",
    description:
      "Get an overview of the subgraph registry: total count, available domains, networks, and protocol types with counts. Use this to understand what data is available before searching.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {},
    },
  },
  {
    name: "semantic_search_subgraphs",
    description:
      "Semantic vector search over the subgraph registry. Embeds the query string with sentence-transformers/all-MiniLM-L6-v2 (the same model architecture used at crawl time; the runtime uses an INT8-quantized ONNX build so absolute scores can drift ~0.01-0.03 from the float32 reference but top-K rankings are stable) and ranks subgraphs by cosine similarity against the precomputed 384-dim embedding of each subgraph's description + entities + protocol metadata. Prefer this over search_subgraphs when the goal is fuzzy, paraphrased, or describes a use-case rather than a literal protocol/entity name. Supports the same domain/network/protocol_type/min_reliability pre-filters as search_subgraphs (applied as SQL WHERE before cosine scoring for performance). Returns the same shape as search_subgraphs plus a `semantic_score` in [0,1] (>0.5 is typically a strong match).",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: {
          type: "string",
          description: "Natural-language description of the data the agent wants to query, e.g. 'on-chain options market activity' or 'lending positions near liquidation'",
        },
        limit: {
          type: "integer",
          description: "Max results to return (default 10, max 50)",
          default: 10,
          minimum: 1,
          maximum: 50,
        },
        min_score: {
          type: "number",
          description: "Minimum cosine similarity to include (0-1). Default 0.3.",
          default: 0.3,
        },
        include_unserved: {
          type: "boolean",
          description: "Include subgraphs with 0 active indexer allocations (returns 'no allocations' on query). Default false.",
          default: false,
        },
        domain: {
          type: "string",
          description: "Pre-filter by domain (defi, nfts, dao, gaming, identity, infrastructure, social, analytics)",
        },
        network: {
          type: "string",
          description: "Pre-filter by chain (mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche, etc.)",
        },
        protocol_type: {
          type: "string",
          description: "Pre-filter by protocol type (dex, lending, bridge, staking, options, perpetuals, etc.)",
        },
        min_reliability: {
          type: "number",
          description: "Pre-filter: minimum reliability score (0-1).",
        },
      },
      required: ["query"],
    },
  },
  {
    name: "get_schema_changes",
    description:
      "Return chronological schema-fingerprint changes for a subgraph. Each row is one detected fingerprint change with prev_fingerprint, fingerprint, and detected_at (unix seconds). Use to assess schema stability before depending on a subgraph: a long stable_days value means the schema contract is mature; a recent changed_within_24h means the upstream protocol just shipped a schema update and queries may need to be revisited.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: {
          type: "string",
          description: "Subgraph ID (the same id used by other tools)",
        },
        since_timestamp: {
          type: "integer",
          description: "Only return changes detected at or after this unix timestamp (seconds). Default 0 (full history).",
          default: 0,
        },
      },
      required: ["subgraph_id"],
    },
  },
];

const HANDLERS = {
  search_subgraphs: searchSubgraphs,
  recommend_subgraph: recommendSubgraph,
  get_subgraph_detail: getSubgraphDetail,
  list_registry_stats: listRegistryStats,
  semantic_search_subgraphs: semanticSearchSubgraphs,
  get_schema_changes: getSchemaChanges,
};

function createServer() {
  const server = new Server(
    { name: "subgraph-registry", version: "0.6.0" },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS,
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = HANDLERS[name];
    if (!handler) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: `Unknown tool: ${name}` }) }],
        isError: true,
      };
    }
    try {
      // semantic_search_subgraphs is async (model load + embed); all
      // other handlers are sync but `await` is a no-op on plain values.
      const result = await handler(args || {});
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: err.message }) }],
        isError: true,
      };
    }
  });

  return server;
}

// ── SSE/HTTP Transport (OpenClaw + remote agents) ──────────

function startHttpTransport(port) {
  const app = express();
  const sessions = new Map();

  app.get("/sse", async (req, res) => {
    const transport = new SSEServerTransport("/messages", res);
    sessions.set(transport.sessionId, transport);

    const server = createServer();

    res.on("close", () => {
      sessions.delete(transport.sessionId);
    });

    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    const sessionId = req.query.sessionId;
    const transport = sessions.get(sessionId);
    if (!transport) {
      res.status(400).json({ error: "Invalid or expired session" });
      return;
    }
    await transport.handlePostMessage(req, res);
  });

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", subgraphs: getDb().prepare("SELECT COUNT(*) as c FROM subgraphs").get().c });
  });

  // ── OpenAPI 3.1 spec (auto-generated at release time) ────────────
  // scripts/gen-openapi.js inventories the TOOLS array + the REST
  // routes below and writes data/openapi.json. We serve the file
  // verbatim so consumers and codegens can hit a stable URL.
  app.get("/.well-known/openapi.json", (_req, res) => {
    if (!existsSync(OPENAPI_JSON_PATH)) {
      res.status(404).json({
        error: "openapi.json not present in this build",
        hint: "Run `node scripts/gen-openapi.js` to generate it.",
      });
      return;
    }
    try {
      const spec = JSON.parse(readFileSync(OPENAPI_JSON_PATH, "utf8"));
      res.type("application/json").json(spec);
    } catch (err) {
      res.status(500).json({ error: "openapi.json parse failed: " + err.message });
    }
  });

  // ── Stable per-subgraph manifest for ecosystem crawlers ───────────────
  // Other tools (E&N tooling, indexer dashboards, agent frameworks) can
  // hit this without needing MCP. JSON-LD so the shape is auto-discoverable.
  const serveManifest = (req, res) => {
    const id = req.params.id;
    const row = getDb()
      .prepare("SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?")
      .get(id, id);
    if (!row) {
      res.status(404).json({ error: `Subgraph '${id}' not found` });
      return;
    }
    const manifest = buildJsonLdManifest(row);
    if (!manifest) {
      res.status(500).json({ error: "Manifest build failed" });
      return;
    }
    res.type("application/ld+json").json(manifest);
  };

  // Canonical .well-known location + a friendlier alias under /subgraphs/
  app.get("/.well-known/subgraph/:id.jsonld", serveManifest);
  app.get("/subgraphs/:id.jsonld", serveManifest);

  // Discovery index so a crawler that doesn't know the ID can find one:
  // returns the top 100 by reliability with their .jsonld URLs.
  app.get("/.well-known/subgraph-index.jsonld", (_req, res) => {
    const rows = getDb()
      .prepare(
        "SELECT id, display_name, network, domain, reliability_score " +
        "FROM subgraphs WHERE active_allocation_count > 0 " +
        "ORDER BY reliability_score DESC LIMIT 100"
      ).all();
    res.type("application/ld+json").json({
      "@context": JSONLD_CONTEXT,
      "@type": "SubgraphIndex",
      generatedAt: new Date().toISOString(),
      count: rows.length,
      subgraphs: rows.map((r) => ({
        "@id": `https://subgraph-registry.paulieb14.dev/subgraphs/${r.id}`,
        id: r.id,
        name: r.display_name,
        network: r.network,
        domain: r.domain,
        reliabilityScore: r.reliability_score,
        manifest: `/.well-known/subgraph/${r.id}.jsonld`,
      })),
    });
  });

  app.listen(port, () => {
    console.error(`SSE transport listening on http://localhost:${port}/sse`);
    console.error(`Well-known manifest at http://localhost:${port}/.well-known/subgraph/{id}.jsonld`);
  });
}

// ── Entry Point ────────────────────────────────────────────

async function main() {
  await ensureDb();

  const subgraphCount = getDb().prepare("SELECT COUNT(*) as c FROM subgraphs").get().c;
  const httpPort = process.env.MCP_HTTP_PORT || (process.argv.includes("--http") ? "3848" : null);
  const httpOnly = process.argv.includes("--http-only");

  // Start SSE/HTTP transport if requested
  if (httpPort || httpOnly) {
    const port = parseInt(httpPort || "3848", 10);
    startHttpTransport(port);
  }

  // Start stdio transport (default, skip if --http-only)
  if (!httpOnly) {
    const server = createServer();
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }

  console.error(`Subgraph Registry MCP server running (${subgraphCount} subgraphs)`);
}

// ── Exports for tooling (OpenAPI generator, tests) ────────
// scripts/gen-openapi.js imports TOOLS + REST_ROUTES at build time.
// Inventory the HTTP routes declaratively here so generator + runtime
// stay in lockstep — drift would silently mis-document the API.
export const REST_ROUTES = [
  {
    method: "get",
    path: "/health",
    summary: "Liveness probe + total subgraph count",
    response: {
      type: "object",
      properties: {
        status: { type: "string", enum: ["ok"] },
        subgraphs: { type: "integer" },
      },
      required: ["status", "subgraphs"],
    },
  },
  {
    method: "get",
    path: "/.well-known/subgraph/{id}.jsonld",
    summary: "JSON-LD manifest for a single subgraph (canonical location)",
    parameters: [
      { name: "id", in: "path", required: true, schema: { type: "string" } },
    ],
    response: { type: "object", description: "JSON-LD SubgraphDeployment manifest" },
  },
  {
    method: "get",
    path: "/subgraphs/{id}.jsonld",
    summary: "JSON-LD manifest alias (same payload as /.well-known/...)",
    parameters: [
      { name: "id", in: "path", required: true, schema: { type: "string" } },
    ],
    response: { type: "object", description: "JSON-LD SubgraphDeployment manifest" },
  },
  {
    method: "get",
    path: "/.well-known/subgraph-index.jsonld",
    summary: "Top-100 subgraphs by reliability with their manifest URLs",
    response: { type: "object", description: "JSON-LD SubgraphIndex" },
  },
  {
    method: "get",
    path: "/.well-known/openapi.json",
    summary: "This OpenAPI spec, self-served for discovery",
    response: { type: "object", description: "OpenAPI 3.1 document" },
  },
];

export { TOOLS };

// Only auto-start when invoked as the entry point — importing the
// module for tooling (scripts/gen-openapi.js, tests) MUST NOT spawn
// the MCP server or open the SQLite file. Use pathToFileURL so the
// comparison works on Windows where process.argv[1] uses backslashes
// while import.meta.url is forward-slashed.
const _isMain =
  process.argv[1] !== undefined &&
  (pathToFileURL(process.argv[1]).href === import.meta.url ||
    basename(process.argv[1]) === "index.js");

if (_isMain) {
  main().catch((err) => {
    console.error("Fatal:", err);
    process.exit(1);
  });
}
