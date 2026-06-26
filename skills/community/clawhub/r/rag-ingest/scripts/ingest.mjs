#!/usr/bin/env node

/**
 * rag-ingest（仅写入模式）
 *
 * 接收 Agent 已解读好的正文，做 chunk → embedding → 写入 Qdrant。
 * 不抓取、不精炼；抓取与解读由 OpenClaw 通过 url-reader / pdf-extract / deep-research 等完成。
 *
 * 环境变量：QDRANT_URL, EMBED_BASE_URL, EMBED_API_KEY, EMBEDDING_MODEL
 *
 * 用法：
 *   rag-ingest --doc-id <id> --topic-tags "主题" --content "正文"
 *   echo "正文" | rag-ingest --doc-id <id> --topic-tags "主题" [--source "https://..."]
 */

import { randomUUID } from "crypto";

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

const argv = process.argv.slice(2);
const getArg = (name, def) => {
  const i = argv.indexOf(`--${name}`);
  if (i === -1 || i + 1 >= argv.length) return def;
  return argv[i + 1];
};

const docId = getArg("doc-id");
const topicTagsRaw = getArg("topic-tags", "");
const source = getArg("source", ""); // 可选，仅作 payload 来源标识
const contentArg = getArg("content");
const collectionName = getArg("collection", "kb_main");

if (!docId || !topicTagsRaw.trim()) {
  console.error("必填：--doc-id 和 --topic-tags。例：--doc-id doc-001 --topic-tags RAG,知识库 [--content \"...\"] 或 --source - 从 stdin 读");
  process.exit(1);
}

function readStdin() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => chunks.push(chunk));
    process.stdin.on("end", () => resolve(chunks.join("")));
    process.stdin.on("error", reject);
  });
}

function smartChunk(text, minChars = 400, maxChars = 1000, overlap = 200) {
  const chunks = [];
  const len = text.length;
  let start = 0;

  const findBreak = (from, to) => {
    const segment = text.slice(from, to);
    let idx = segment.lastIndexOf("\n\n");
    if (idx !== -1 && from + idx >= minChars) return from + idx + 2;
    idx = segment.lastIndexOf("\n");
    if (idx !== -1 && from + idx >= minChars) return from + idx + 1;
    for (const p of ["。", "！", "？", ".", "!", "?"]) {
      idx = segment.lastIndexOf(p);
      if (idx !== -1 && from + idx >= minChars) return from + idx + 1;
    }
    idx = segment.lastIndexOf(" ");
    if (idx !== -1 && from + idx >= minChars) return from + idx + 1;
    return to;
  };

  while (start < len) {
    const maxEnd = Math.min(len, start + maxChars);
    const end = findBreak(start, maxEnd);
    const chunk = text.slice(start, end).trim();
    if (chunk) chunks.push(chunk);
    if (end >= len) break;
    start = Math.max(end - overlap, 0);
  }
  return chunks;
}

async function embed(texts) {
  const resp = await fetch(`${EMBED_BASE_URL}/embeddings`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${EMBED_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model: EMBEDDING_MODEL, input: texts }),
  });
  if (!resp.ok) {
    const t = await resp.text();
    throw new Error(`Embedding 失败: ${resp.status} ${t}`);
  }
  const data = await resp.json();
  return data.data.map((d) => d.embedding);
}

async function qdrantRequest(path, body, method = "POST") {
  const url = `${QDRANT_URL}${path}`;
  const resp = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!resp.ok) {
    const t = await resp.text();
    throw new Error(`Qdrant 请求失败: ${resp.status} ${t}`);
  }
  return resp.json();
}

async function ensureCollection(vectorSize) {
  const resp = await fetch(`${QDRANT_URL}/collections/${collectionName}`);
  if (resp.ok) return;
  await qdrantRequest(`/collections/${collectionName}`, {
    vectors: { size: vectorSize, distance: "Cosine" },
  }, "PUT");
}

async function deleteOldDocPoints() {
  await qdrantRequest(`/collections/${collectionName}/points/delete`, {
    filter: { must: [{ key: "doc_id", match: { value: docId } }] },
  });
}

async function upsertPoints(points) {
  await qdrantRequest(`/collections/${collectionName}/points`, { points }, "PUT");
}

(async () => {
  try {
    if (!QDRANT_URL || !EMBED_API_KEY) {
      console.error("缺少 QDRANT_URL 或 EMBED_API_KEY（或 OPENAI_API_KEY）");
      process.exit(1);
    }

    const rawContent =
      (contentArg != null && String(contentArg).trim() !== "")
        ? String(contentArg).trim()
        : await readStdin();

    if (!rawContent.trim()) {
      console.error("请通过 --content \"...\" 或 stdin 提供非空正文");
      process.exit(1);
    }

    const chunks = smartChunk(rawContent.trim());
    if (!chunks.length) {
      console.error("未生成任何 chunk");
      process.exit(1);
    }

    const vectors = await embed(chunks);
    const dim = vectors[0]?.length;
    if (!dim) throw new Error("Embedding 结果为空");

    await ensureCollection(dim);
    await deleteOldDocPoints();

    const now = new Date().toISOString();
    const tagsArr = topicTagsRaw.split(",").map((t) => t.trim()).filter(Boolean);
    const points = vectors.map((vec, idx) => ({
      id: randomUUID(),
      vector: vec,
      payload: {
        doc_id: docId,
        text_type: "summary",
        chunk_index: idx,
        source: source || null,
        topic_tags: tagsArr,
        text: chunks[idx],
        created_at: now,
        updated_at: now,
      },
    }));

    await upsertPoints(points);
    console.log(`已写入 doc_id=${docId}，collection=${collectionName}，points=${points.length}`);
  } catch (e) {
    console.error("rag-ingest 错误:", e.message || e);
    process.exit(1);
  }
})();
