# Retrieval, metadata, connectors and indexing (v0.27.3)

[API overview](API.md)

## Retrieval

```javascript
const results = await client.retrieve({
  question: "What is deep learning?",
  dataset_ids: ["<dataset_id>"],
  similarity_threshold: 0.3,
  page_size: 5,
  knn_top_k: 1024,
  knn_num_candidates: 2048,
  rerank_candidates_count: 64,
  highlight: true,
  include_knowledge_compilation: false,
  vector_similarity_weight: 0.7,
  keyword: true,
  use_kg: false,
  rerank_id: "<rerank_model_id>",
});
```

`retrieve()` forwards the payload unchanged. Prefer `knn_top_k` over the deprecated `top_k`; `knn_num_candidates` must be at least `knn_top_k`. Set `rerank_candidates_count >= page * page_size` (defaults: 64, 1, 30). `document_ids` and `metadata_condition` filters intersect. `include_knowledge_compilation: false` excludes compiled chunks. The response is `{ chunks, total, doc_aggs }`.

## Metadata

```javascript
// Batch-update or delete metadata for selected documents.
await client.updateMetadata("<dataset_id>", {
  selector: { document_ids: ["<doc_id>"] },
  updates: [{ key: "status", value: "reviewed" }],
});
```

## Connector

Connectors are tenant-scoped (not dataset-scoped). The client calls the tenant-level routes.

```javascript
// List connectors (tenant scope)
const connectors = await client.listConnectors();

// Create connector
const connector = await client.createConnector({
  name: "Documentation sitemap",
  source: "sitemap",
  config: { sitemap_url: "https://example.com/sitemap.xml" }
});

// Get, update, delete connector
const conn = await client.getConnector(connectorId);
await client.updateConnector(connectorId, { refresh_freq: 10 });
await destructiveClient.deleteConnector(connectorId);
```

## RAPTOR

```javascript
// Start RAPTOR processing
const task = await client.runRaptor(datasetId);

// Check progress
const progress = await client.traceRaptor(datasetId);
```

## GraphRAG

```javascript
const graph = await client.getKnowledgeGraph(datasetId);
await client.runGraphRag(datasetId);
const progress = await client.traceGraphRag(datasetId);
await destructiveClient.deleteKnowledgeGraph(datasetId);
```

