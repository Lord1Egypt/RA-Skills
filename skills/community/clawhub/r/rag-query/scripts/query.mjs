#!/usr/bin/env node

/**
 * rag-query（OpenClaw 知识库检索）
 * 对 Qdrant kb_main 做语义检索，返回 top-k 片段。检索优先：先查知识库再搜索/解读。
 * 环境变量：QDRANT_URL, EMBED_BASE_URL, EMBED_API_KEY, EMBEDDING_MODEL
 * 用法：query.mjs "问题" 或 --query "问题" [--top-k 5] [--topic-tags "tag1,tag2"]
 */

const argv = process.argv.slice(2);
const getArg = (name, def) => {
  const i = argv.indexOf(`--${name}`);
  if (i === -1 || i + 1 >= argv.length) return def;
  return argv[i + 1];
};

let fetchFn = globalThis.fetch;
if (!fetchFn) {
  try {
    const mod = await import("node-fetch");
    fetchFn = mod.default;
  } catch (e) {
    console.error("需要 Node 18+ 或安装 node-fetch");
    process.exit(1);
  }
}
const fetch = fetchFn;

const QDRANT_URL = process.env.QDRANT_URL || "http://127.0.0.1:6333";
const EMBED_BASE_URL =
  process.env.EMBED_BASE_URL || "https://api.vectorengine.ai/v1";
const EMBED_API_KEY =
  process.env.VECTORENGINE_API_KEY ||
  process.env.EMBED_API_KEY ||
  process.env.OPENAI_API_KEY;
const EMBEDDING_MODEL =
  process.env.RAG_INGEST_EMBED_MODEL ||
  process.env.OPENAI_EMBEDDING_MODEL ||
  "text-embedding-3-large";
const COLLECTION_NAME = getArg("collection", "kb_main");

const queryStr =
  getArg("query", null) ?? (argv[0] && !argv[0].startsWith("--") ? argv[0] : null);
const topK = Math.max(1, parseInt(getArg("top-k", "5"), 10) || 5);
const topicTagsArg = getArg("topic-tags", "");

if (!queryStr || !queryStr.trim()) {
  console.error("请提供查询字符串：第一个位置参数或 --query \"...\"");
  process.exit(1);
}

if (!QDRANT_URL || !EMBED_API_KEY) {
  console.error("缺少 QDRANT_URL 或 EMBED_API_KEY（或 OPENAI_API_KEY）");
  process.exit(1);
}

async function embedOne(text) {
  const resp = await fetch(`${EMBED_BASE_URL}/embeddings`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${EMBED_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: EMBEDDING_MODEL,
      input: text,
    }),
  });
  if (!resp.ok) {
    const t = await resp.text();
    throw new Error(`Embedding 失败: ${resp.status} ${t}`);
  }
  const data = await resp.json();
  const vec = data.data?.[0]?.embedding;
  if (!vec || !Array.isArray(vec)) throw new Error("Embedding 返回无向量");
  return vec;
}

async function searchQdrant(vector, limit, filter) {
  const url = `${QDRANT_URL}/collections/${COLLECTION_NAME}/points/search`;
  const body = {
    vector,
    limit,
    with_payload: true,
  };
  if (filter && Object.keys(filter).length) body.filter = filter;
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const t = await resp.text();
    throw new Error(`Qdrant 检索失败: ${resp.status} ${t}`);
  }
  return resp.json();
}

(async () => {
  try {
    const vector = await embedOne(queryStr.trim());
    const topicTags = topicTagsArg
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);
    const filter =
      topicTags.length > 0
        ? { must: [{ key: "topic_tags", match: { any: topicTags } }] }
        : undefined;
    const result = await searchQdrant(vector, topK, filter);
    const points = result.result || [];
    const output = points.map((p) => {
      const pl = p.payload || {};
      return {
        text: pl.text ?? "",
        doc_id: pl.doc_id ?? null,
        source: pl.source ?? null,
        text_type: pl.text_type ?? null,
        topic_tags: pl.topic_tags ?? [],
      };
    });
    console.log(JSON.stringify(output));
  } catch (e) {
    console.error("rag-query 错误:", e.message || e);
    process.exit(1);
  }
})();
