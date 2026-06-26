# Tool Reference

Read this when you need the full flag/parameter detail and output formats for the three ML engineering scripts.

## Tools (quick commands)

### Model Deployment Pipeline

```bash
python scripts/model_deployment_pipeline.py --model model.pkl --target staging
```

Generates deployment artifacts: Dockerfile, Kubernetes manifests, health checks.

### RAG System Builder

```bash
python scripts/rag_system_builder.py --config rag_config.yaml --analyze
```

Scaffolds RAG pipeline with vector store integration and retrieval logic.

### ML Monitoring Suite

```bash
python scripts/ml_monitoring_suite.py --config monitoring.yaml --deploy
```

Sets up drift detection, alerting, and performance dashboards.

---

## model_deployment_pipeline.py

**Purpose:** Generates deployment artifacts for productionizing ML models, including Dockerfiles, Kubernetes manifests, and health check configurations.

**Usage:**

```bash
python scripts/model_deployment_pipeline.py --input <path> --output <path> [--config <file>] [--verbose]
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input path (model artifact or directory) |
| `--output` | `-o` | Yes | Output path for generated deployment artifacts |
| `--config` | `-c` | No | Configuration file for deployment settings |
| `--verbose` | `-v` | No | Enable debug-level logging output |

**Example:**

```bash
python scripts/model_deployment_pipeline.py -i ./models/classifier.pkl -o ./deploy/
```

**Output Formats:** JSON to stdout containing `status`, `start_time`, `end_time`, and `processed_items`. Logs progress to stderr.

---

## rag_system_builder.py

**Purpose:** Scaffolds a RAG pipeline with vector store integration, retrieval logic, and ingestion configuration.

**Usage:**

```bash
python scripts/rag_system_builder.py --input <path> --output <path> [--config <file>] [--verbose]
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input path (document corpus or configuration directory) |
| `--output` | `-o` | Yes | Output path for generated RAG pipeline artifacts |
| `--config` | `-c` | No | Configuration file for RAG settings (vector DB, chunking, embedding) |
| `--verbose` | `-v` | No | Enable debug-level logging output |

**Example:**

```bash
python scripts/rag_system_builder.py -i ./documents/ -o ./rag-pipeline/ -c rag_config.yaml
```

**Output Formats:** JSON to stdout containing `status`, `start_time`, `end_time`, and `processed_items`. Logs progress to stderr.

---

## ml_monitoring_suite.py

**Purpose:** Sets up drift detection, performance alerting, and monitoring dashboards for production ML models.

**Usage:**

```bash
python scripts/ml_monitoring_suite.py --input <path> --output <path> [--config <file>] [--verbose]
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input path (model metrics, reference data, or monitoring config) |
| `--output` | `-o` | Yes | Output path for generated monitoring configuration and dashboards |
| `--config` | `-c` | No | Configuration file for monitoring thresholds and alert rules |
| `--verbose` | `-v` | No | Enable debug-level logging output |

**Example:**

```bash
python scripts/ml_monitoring_suite.py -i ./model-metrics/ -o ./monitoring/ -c monitoring.yaml -v
```

**Output Formats:** JSON to stdout containing `status`, `start_time`, `end_time`, and `processed_items`. Logs progress to stderr.
