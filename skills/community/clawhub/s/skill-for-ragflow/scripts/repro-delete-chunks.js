#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");
const { createClient } = require("../lib/api.js");

const DEFAULT_RETRIES = 3;
const DEFAULT_RETRY_DELAY_MS = 1000;

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeError(err) {
  return {
    message: err.message,
    code: err.code,
    status: err.status,
  };
}

function chunkListIds(payload) {
  const chunks = Array.isArray(payload) ? payload : payload?.chunks || [];
  return chunks.map((chunk) => chunk.id).filter(Boolean);
}

function chunkIdsFromExactLookup(payload) {
  return chunkListIds(payload);
}

function firstDocumentId(upload) {
  if (Array.isArray(upload)) return upload[0]?.id || "";
  if (Array.isArray(upload?.docs)) return upload.docs[0]?.id || "";
  if (upload?.docs?.id) return upload.docs.id;
  if (upload?.document?.id) return upload.document.id;
  return upload?.id || "";
}

async function main() {
  const client = createClient({ timeout: Number(process.env.RAGFLOW_REPRO_TIMEOUT_MS || 60000) });
  const retries = Number(process.env.RAGFLOW_REPRO_DELETE_RETRIES || DEFAULT_RETRIES);
  const retryDelayMs = Number(process.env.RAGFLOW_REPRO_DELETE_RETRY_DELAY_MS || DEFAULT_RETRY_DELAY_MS);
  const embeddingModel = process.env.RAGFLOW_REPRO_EMBEDDING_MODEL || "text-embedding-v4@Tongyi-Qianwen";
  const marker = `RAGFLOW_DELETE_CHUNK_REPRO_${Date.now()}`;
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "ragflow-delete-chunks-"));
  const filePath = path.join(tempDir, "delete-chunks-repro.md");

  const result = {
    marker,
    config: { embedding_model: embeddingModel, retries, retry_delay_ms: retryDelayMs },
    steps: [],
    attempts: [],
    cleanup: {},
  };

  let datasetId = "";
  let documentId = "";

  try {
    fs.writeFileSync(
      filePath,
      [
        "# RAGFlow delete-chunks repro",
        "",
        `Marker: ${marker}`,
        "This file is created by ragflow-skill to reproduce manual chunk deletion.",
        "",
      ].join("\n"),
      "utf8"
    );

    const datasetPayload = {
      name: `ragflow-delete-chunks-repro-${Date.now()}`,
      chunk_method: "naive",
      permission: "me",
      description: "Temporary dataset for ragflow-skill delete-chunks reproduction",
    };
    if (embeddingModel) datasetPayload.embedding_model = embeddingModel;

    const dataset = await client.createDataset(datasetPayload);
    datasetId = dataset.id;
    result.steps.push({ step: "create-dataset", dataset_id: datasetId });

    const upload = await client.uploadDocuments(datasetId, [filePath]);
    result.steps.push({ step: "upload-response-shape", shape: Array.isArray(upload) ? "array" : Object.keys(upload || {}) });
    documentId = firstDocumentId(upload);
    if (!documentId) throw new Error("Upload did not return a document id");
    result.steps.push({ step: "upload-documents", document_id: documentId });

    await client.startParsing(datasetId, [documentId]);
    const parsed = await client.waitForParsing(datasetId, [documentId], { maxWait: 120000, interval: 3000 });
    result.steps.push({ step: "wait-parsing", documents: parsed.map((doc) => ({ id: doc.id, run: doc.run, chunk_count: doc.chunk_count })) });

    const added = await client.addChunk(datasetId, documentId, {
      content: `Manual chunk for delete reproduction. ${marker}`,
      important_keywords: ["delete", "repro"],
    });
    const chunkId = added?.chunk?.id || added?.id;
    if (!chunkId) throw new Error("addChunk did not return a chunk id");
    result.steps.push({ step: "add-chunk", chunk_id: chunkId });

    const beforeDelete = await client.listChunks(datasetId, documentId);
    result.steps.push({ step: "list-before-delete", chunk_ids: chunkListIds(beforeDelete), contains_added_chunk: chunkListIds(beforeDelete).includes(chunkId) });
    try {
      const exactBeforeDelete = await client.listChunks(datasetId, documentId, { id: chunkId });
      result.steps.push({
        step: "exact-id-before-delete",
        chunk_ids: chunkIdsFromExactLookup(exactBeforeDelete),
        contains_added_chunk: chunkIdsFromExactLookup(exactBeforeDelete).includes(chunkId),
      });
    } catch (err) {
      result.steps.push({ step: "exact-id-before-delete", error: normalizeError(err) });
    }

    for (let attempt = 0; attempt <= retries; attempt++) {
      if (attempt > 0) await delay(retryDelayMs);
      const entry = { attempt, delay_ms: attempt === 0 ? 0 : retryDelayMs };
      try {
        entry.response = await client.deleteChunks(datasetId, documentId, [chunkId], { maxRetries: 0 });
        entry.ok = true;
        result.attempts.push(entry);
        break;
      } catch (err) {
        entry.ok = false;
        entry.error = normalizeError(err);
        if (err.delete_chunk_details) entry.delete_chunk_details = err.delete_chunk_details;
        try {
          const listed = await client.listChunks(datasetId, documentId);
          entry.chunk_ids_after_failure = chunkListIds(listed);
          entry.chunk_still_listed = entry.chunk_ids_after_failure.includes(chunkId);
        } catch (listErr) {
          entry.list_error = normalizeError(listErr);
        }
        result.attempts.push(entry);
      }
    }

    const firstOk = result.attempts[0]?.ok;
    const laterOk = result.attempts.some((attempt, index) => index > 0 && attempt.ok);
    const anyOk = result.attempts.some((attempt) => attempt.ok);
    if (firstOk) {
      result.conclusion = "delete-chunks succeeded immediately; no retry workaround is indicated by this run.";
    } else if (laterOk) {
      result.conclusion = "delete-chunks succeeded only after retry; exact ID lookup and search/delete visibility are temporarily inconsistent after manual chunk insert.";
    } else if (!anyOk) {
      result.conclusion = "delete-chunks failed after retries; this points to a RAGFlow server/doc-store deletion issue rather than a transient CLI timing issue.";
    }
  } catch (err) {
    result.error = normalizeError(err);
  } finally {
    if (datasetId) {
      try {
        result.cleanup.delete_dataset = await client.deleteDatasets([datasetId]);
      } catch (err) {
        result.cleanup.delete_dataset_error = normalizeError(err);
      }
    }
    fs.rmSync(tempDir, { recursive: true, force: true });
  }

  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exitCode = 1;
}

main().catch((err) => {
  console.error(JSON.stringify({ error: normalizeError(err) }, null, 2));
  process.exit(1);
});
