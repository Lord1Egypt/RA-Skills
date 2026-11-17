# Datasets, documents, parsing and chunks (v0.27.3)

[API overview](API.md)

## Dataset

```javascript
// List datasets (supports pagination: page, page_size, id, name)
const datasets = await client.listDatasets({ page: 1, page_size: 10 });

// Get a single dataset by ID (enriched with total_size and connectors)
const dataset = await client.getDataset("<dataset_id>");
// Returns: { id: "...", name: "...", total_size: 1024, connectors: [...], ... }

// Create a dataset
const dataset = await client.createDataset({
  name: "Tech Docs",
  chunk_method: "naive",
});

// Update a dataset
await client.updateDataset("<dataset_id>", { name: "New Name" });

// Delete datasets by IDs
await destructiveClient.deleteDatasets(["<id1>", "<id2>"]);
```

## Document

```javascript
// Upload documents
await client.uploadDocuments("<dataset_id>", ["./report.pdf", "./notes.txt"]);

// Override display names when paths are temporary/task IDs
await client.uploadDocuments("<dataset_id>", [
  { path: "./tmp/task-output", name: "report.pdf" },
]);

// List documents (supports page, page_size, id, name, orderby, desc, keywords, suffix, types, run, metadata, metadata_condition, return_empty_metadata)
const docs = await client.listDocuments("<dataset_id>");

// Get a single document by ID
const doc = await client.getDocument("<dataset_id>", "<doc_id>");

// Update a document
await client.updateDocument("<dataset_id>", "<doc_id>", {
  name: "Renamed",
  parser_config: { pages: [[1, 2]] },
  chunk_method: "knowledge_graph",
  enabled: 1,
  meta_fields: { author: "Alice" },
});

// Delete documents by IDs
await destructiveClient.deleteDocuments("<dataset_id>", ["<doc_id1>", "<doc_id2>"]);
```

RAGFlow v0.27.3 defines document updates as `PATCH /api/v1/datasets/{dataset_id}/documents/{document_id}`. `updateDocument()` sends that request directly.

You can also filter documents by metadata:

```javascript
const docs = await client.listDocuments("<dataset_id>", {
  metadata_condition: JSON.stringify({
    logic: "and",
    conditions: [{ name: "status", comparison_operator: "=", value: "published" }],
  }),
});
```

You can also summarize metadata across documents:

```javascript
const summary = await client.metadataSummary("<dataset_id>", ["<doc_id1>", "<doc_id2>"]);
// Returns: { summary: [...] }
```

## Document Download

```javascript
// Download via dataset
const doc = await client.downloadDocument(datasetId, documentId);

// Download by document ID
const doc = await client.downloadDocumentById(documentId);

// Preview a document inline (v0.27.3)
const preview = await client.previewDocument(documentId);
```

Downloads/previews are normalized from binary HTTP responses into `{ content, encoding: "base64", name, content_type, size }`. Decode with `Buffer.from(doc.content, "base64")`; `content` is not plain text or a remote URL. JSON API errors and HTTP failures still reject the request.

## Parsing

```javascript
// Start parsing (returns immediately)
await destructiveClient.startParsing("<dataset_id>", ["<doc_id1>"]);

// Stop parsing
await destructiveClient.stopParsing("<dataset_id>", ["<doc_id1>"]);

// Start ingestion without purging existing tasks/chunks
await client.ingestDocuments(["<doc_id1>"], { run: "1" });

// After authorizing a purge, rerun with the dedicated destructive client
await destructiveClient.ingestDocuments(["<doc_id1>"], { run: "1", delete: true });

// Cancel ingestion for ingestion-pipeline datasets
await client.ingestDocuments(["<doc_id1>"], { run: "2" });

// Wait for parsing to complete (polls until DONE or FAIL)
// Documents stuck in CANCEL keep polling until timeout.
const results = await client.waitForParsing("<dataset_id>", ["<doc_id1>"], {
  interval: 3000,   // poll interval in ms (default: 3000)
  maxWait: 120000,  // max wait in ms (default: 120000)
});
```

## Chunk

```javascript
// List chunks (supports pagination: page, page_size, keywords)
const chunks = await client.listChunks("<dataset_id>", "<doc_id>");

// Exact chunk lookup by ID
const chunk = await client.getChunk("<dataset_id>", "<doc_id>", "<chunk_id>");

// Add a chunk
await client.addChunk("<dataset_id>", "<doc_id>", {
  content: "Custom chunk text",
  important_keywords: ["keyword1", "keyword2"],
});

// Update a chunk
await client.updateChunk("<dataset_id>", "<doc_id>", "<chunk_id>", {
  content: "Updated content",
  important_keywords: ["new_keyword"],
});

// Delete chunks by IDs
await destructiveClient.deleteChunks("<dataset_id>", "<doc_id>", ["<chunk_id1>"]);

// Inspect or delete the document structure graph
const graph = await client.getDocumentStructureGraph("<dataset_id>", "<doc_id>");
await destructiveClient.deleteDocumentStructureGraph("<dataset_id>", "<doc_id>");
```

`updateChunk()` also accepts `available` (0/1 or boolean), `image_base64`, and `image_update_mode` (`append`, `replace`, `remove`). Append/replace require image data; remove must omit it. `listChunks()` supports `chunk_ids` (comma-separated IDs) and `available` (`"true"`/`"false"`); it returns `{ total, chunks, doc }`.

Both `startParsing()` and `stopParsing()` clear the selected documents' existing chunks on the server and require the dedicated destructive client. Starting parsing clears old tasks as well.

`updateChunk()` uses `PATCH /api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}`. `ingestDocuments()` is for ingestion-pipeline datasets; use `startParsing()`/`stopParsing()` for the built-in chunking pipeline.

`deleteChunks()` retries the transient `rm_chunk deleted chunks 0, expect N` response only after `getChunk()` confirms the target chunk still exists. This distinguishes document-store refresh delay from a genuinely missing chunk. Override with:

```javascript
await destructiveClient.deleteChunks("<dataset_id>", "<doc_id>", ["<chunk_id1>"], {
  maxRetries: 0,
  retryDelay: 1000,
});
```

When the CLI is run with `--json`, `delete-chunks` wraps the server result with diagnostic fields that pipelines can consume directly:

```json
{
  "result": {},
  "requested_chunk_ids": ["<chunk_id1>"],
  "existing_chunk_ids": ["<chunk_id1>"],
  "missing_chunk_ids": [],
  "visibility_checked": true,
  "retry_count": 1,
  "retries": [
    {
      "attempt": 0,
      "next_attempt": 2,
      "max_retries": 3,
      "existing_chunk_ids": ["<chunk_id1>"],
      "missing_chunk_ids": []
    }
  ]
}
```

On a final delete visibility failure, the CLI exits non-zero and emits JSON with `error`, `requested_chunk_ids`, `existing_chunk_ids`, `missing_chunk_ids`, `retry_count`, `retries`, and `delete_chunk_diagnostics`.

All CLI command failures in `--json` mode use the same top-level error envelope:

```json
{
  "error": {
    "message": "API Error: Unauthorized",
    "raw_message": "Unauthorized",
    "code": 401,
    "status": 401,
    "command": "list-models"
  }
}
```

Command-specific diagnostics, such as delete chunk visibility checks, are added as extra top-level fields alongside `error`.

