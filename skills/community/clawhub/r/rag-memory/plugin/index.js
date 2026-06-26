import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import https from "node:https";
import http from "node:http";
import { URL } from "node:url";

// ── HTTP helper ────────────────────────────────────────────────────────────────

function post(url, body, extraHeaders = {}) {
  return new Promise((resolve, reject) => {
    const parsed  = new URL(url);
    const lib     = parsed.protocol === "https:" ? https : http;
    const payload = JSON.stringify(body);
    const req     = lib.request(
      {
        hostname: parsed.hostname,
        port:     parsed.port || (parsed.protocol === "https:" ? 443 : 80),
        path:     parsed.pathname + parsed.search,
        method:   "POST",
        headers:  {
          "Content-Type":   "application/json",
          "Content-Length": Buffer.byteLength(payload),
          ...extraHeaders,
        },
      },
      (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => {
          try { resolve(JSON.parse(data)); }
          catch (e) { reject(new Error(`JSON parse failed: ${data.slice(0, 200)}`)); }
        });
      },
    );
    req.on("error", reject);
    req.write(payload);
    req.end();
  });
}

// ── Embed via OpenAI-compatible endpoint ───────────────────────────────────────

async function embed(cfg, text) {
  const headers = {};
  if (cfg.embed_api_key) headers["Authorization"] = `Bearer ${cfg.embed_api_key}`;
  const res = await post(
    `${cfg.embed_base_url}/v1/embeddings`,
    { model: cfg.embed_model, input: [text] },
    headers,
  );
  if (!res.data?.[0]?.embedding) throw new Error("embed: no embedding in response");
  return res.data[0].embedding;
}

// ── Query Qdrant ───────────────────────────────────────────────────────────────

async function searchQdrant(cfg, cols, scope, vector, topK) {
  const headers = {};
  if (cfg.qdrant_api_key) headers["api-key"] = cfg.qdrant_api_key;

  let collections;
  if (scope === "memory") {
    collections = [cols.memory];
  } else if (scope === "docs") {
    collections = [cols.docs];
  } else {
    collections = [cols.memory, cols.docs];
  }

  const allResults = [];
  for (const col of collections) {
    try {
      const res = await post(
        `${cfg.qdrant_url}/collections/${col}/points/search`,
        {
          vector,
          limit:          topK,
          with_payload:   true,
          score_threshold: cfg.score_threshold,
        },
        headers,
      );
      for (const r of (res.result || [])) {
        allResults.push({
          score:  r.score,
          text:   r.payload?.text || "",
          source: r.payload?.source || "unknown",
          file:   r.payload?.file_name || r.payload?.file_path || "",
          date:   r.payload?.log_date || r.payload?.created_at || "",
          tags:   r.payload?.tags || [],
        });
      }
    } catch (e) {
      console.error(`rag-memory: collection ${col} error: ${e.message}`);
    }
  }

  allResults.sort((a, b) => b.score - a.score);
  return allResults.slice(0, topK);
}

// ── Format output ──────────────────────────────────────────────────────────────

function formatResults(results, query, truncateChars = 0) {
  if (!results.length) {
    return `[vector_search] No relevant results found for: "${query}"`;
  }
  const lines = [`[vector_search] Top ${results.length} results for: "${query}"\n`];
  results.forEach((r, i) => {
    const meta = [
      r.source,
      r.file ? `file:${r.file}` : "",
      r.date ? `date:${r.date}` : "",
      `score:${r.score.toFixed(3)}`,
    ].filter(Boolean).join(" | ");
    const text = truncateChars > 0 && r.text.length > truncateChars
      ? r.text.slice(0, truncateChars) + "…"
      : r.text.trim();
    lines.push(`── Result ${i + 1} [${meta}]`);
    lines.push(text);
    lines.push("");
  });
  return lines.join("\n");
}

// ── Plugin entry ───────────────────────────────────────────────────────────────

export default definePluginEntry({
  id:   "rag-memory",
  name: "RAG Memory",
  register(api) {
    const cfg    = api.pluginConfig;
    const prefix = cfg.collection_prefix;
    const cols   = { memory: `${prefix}_memory`, docs: `${prefix}_docs` };

    api.registerTool({
      name:        "vector_search",
      description: "Search agent memory and docs via semantic vector search. Use this instead of loading entire memory files.",
      parameters: {
        type:     "object",
        required: ["query"],
        properties: {
          query: { type: "string", description: "Question or topic to search for" },
          scope: { type: "string", enum: ["memory", "docs", "all"], default: "all" },
          top_k: { type: "integer", default: cfg.top_k, minimum: 1, maximum: 10 },
        },
      },
      async execute(_id, { query, scope = "all", top_k = cfg.top_k }) {
        if (!query?.trim()) return { content: [{ type: "text", text: "vector_search requires a non-empty query" }], isError: true };
        const k = Math.min(Math.max(1, parseInt(top_k, 10)), 10);
        const vector  = await embed(cfg, query.trim());
        const results = await searchQdrant(cfg, cols, scope, vector, k);
        return { content: [{ type: "text", text: formatResults(results, query) }] };
      },
    });

    if (cfg.auto_inject) {
      api.registerHook("before_prompt_build", async (ctx) => {
        const lastUser = [...ctx.messages].reverse().find((m) => m.role === "user");
        if (!lastUser?.content) return {};
        const query = typeof lastUser.content === "string"
          ? lastUser.content
          : lastUser.content.map((b) => b.text ?? "").join(" ");
        if (query.trim().length < (cfg.auto_inject_min_query_len ?? 20)) return {};
        try {
          const vector  = await embed(cfg, query.slice(0, 500));
          const results = await searchQdrant(cfg, cols, "all", vector, cfg.top_k);
          if (!results.length) return {};
          return { prependContext: formatResults(results, query, cfg.auto_inject_max_result_chars ?? 500) };
        } catch {
          return {};
        }
      }, { name: "rag-memory-inject", priority: 100 });
    }
  },
});
