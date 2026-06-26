# Specialization: ML / AI System

Apply this guidance on top of the base SOP for AI/ML platforms, model serving, algorithm pipelines, and LLM applications.

## Phase 3 — ML System Layer Pattern

Typical 4-layer pattern for ML systems:

| Layer | Responsibility |
|-------|---------------|
| **Serving / Application** | API gateway, user interface, request routing |
| **Orchestration** | Experiment tracking, pipeline scheduling, task queue |
| **Execution / Compute** | Model training workers, inference servers, GPU scheduling |
| **Storage / Registry** | Model registry, feature store, dataset store, artifact store |

## Phase 5 — Critical Flows for ML Systems

Always document these flows (in addition to general business flows):

1. **Model training flow**: data ingestion → preprocessing → training → evaluation → registration
2. **Inference / serving flow**: request → preprocessing → model forward pass → postprocessing → response
3. **Model promotion flow**: experiment → staging validation → production promotion → rollback
4. **Data pipeline flow**: source → ingestion → validation → feature engineering → storage

## Phase 6 — Storage Selection for ML

| Data type | Storage choice | Notes |
|-----------|---------------|-------|
| Model weights / artifacts | Object storage (MinIO, S3) | Versioned, immutable |
| Experiment metadata | Relational DB or MLflow tracking | Query by params, metrics |
| Features (batch) | Data warehouse / Parquet on object storage | |
| Features (online) | Redis / DynamoDB | Low-latency lookup |
| Training datasets | Object storage + metadata DB | Large files, never copy |
| Inference logs | Time-series DB or object storage | Monitoring, drift detection |

## Phase 7 — ML-Specific Decision Points

| Decision | Consideration |
|----------|--------------|
| Online vs batch inference | Latency SLA < 100ms → online; throughput-first → batch |
| GPU scheduling | Dynamic memory allocation vs fixed slot reservation |
| Model isolation | Shared process (fast) vs Docker container per model (safe, isolated) |
| Framework | PyTorch for research flexibility; ONNX for cross-platform serving |
| Feature store | Only add if serving features to multiple models; otherwise compute inline |
| Experiment tracking | MLflow (self-hosted) vs Weights & Biases (cloud) vs custom |

## Phase 8 — ML Inference API Standards

Standard inference endpoint pattern:

```
POST /api/v1/predict
{
  "model_id": "string",
  "inputs": { ... }       // model-specific input schema
}
→ 200 {
  "prediction": { ... },  // model-specific output schema
  "model_version": "1.0",
  "latency_ms": 42
}
```

Health endpoint must report resource status:
```
GET /health
→ { "status": "ok", "gpu_memory_free_mb": 8192, "model_loaded": true }
```

## Phase 9 — Deployment Patterns for ML

| Pattern | When to use |
|---------|------------|
| Single host, Docker Compose | Private deployment, single GPU workstation, offline |
| Model server (Triton, TorchServe) | Multiple models, batching, dynamic batching |
| Kubernetes + GPU node pool | Multi-tenant, auto-scaling, multiple GPU types |
| Serverless inference | CPU-only, short bursts, cold start acceptable |

## Phase 10 — ML-Specific NFR

- **Model drift monitoring**: log inputs/outputs; schedule periodic drift detection
- **GPU memory management**: always report free memory in `/health`; schedule tasks against available memory not fixed slots
- **Reproducibility**: pin all library versions; store random seeds with experiment metadata
- **Data lineage**: record which dataset version produced which model version
- **Fairness / bias**: define evaluation metrics beyond accuracy for safety-critical systems
- **Inference latency SLA**: define P50 / P95 / P99 latency targets separately
