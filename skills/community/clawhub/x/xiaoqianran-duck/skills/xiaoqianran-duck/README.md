# xiaoqianran-duck

Local analytical data tool powered by **DuckDB**.

## Vision

A desktop-first data explorer that combines:

- **Powerful local storage**: Single-file `data.duckdb`
- **Multi-format support**: CSV / TSV / JSON / Parquet / Excel
- **Hugging Face integration**: Direct access via `hf://` (no need to download everything first) + token login for gated datasets
- **Flexible frontends**: Designed to work with Tauri, Electron, or Qt

```
Tauri / Electron / Qt 前端
        ↓
DuckDB 数据库文件 data.duckdb
        ↓
CSV / TSV / JSON / Parquet / Excel / Hugging Face (hf://)
```

## Features (Planned / In Progress)

- Query remote Hugging Face datasets directly with DuckDB `hf://` protocol
- Import selected data from HF or local files into `data.duckdb`
- Fast analytical queries (Parquet-first)
- Cross-platform desktop app support

## Current Status

Prototype stage. Core data layer (DuckDB + HF) has been validated in Node.js and Python.

## Quick Start (Node example)

```bash
cd examples
npm install
node hf-import.js
```

This will:
1. Connect to DuckDB
2. Query a sample dataset from Hugging Face
3. Import it into a local `data.duckdb` file

## Architecture

See the conversation history for full details on recommended stack (Tauri + Rust + duckdb-rs is preferred for production).

## License

MIT

## Getting Started

### Run the Hugging Face demo

```bash
cd examples
npm install
npm run hf
```

This creates a `data.duckdb` in the project root with data imported from Hugging Face.

### Run the Preview Server (Web UI)

```bash
# First populate data
node examples/demo-local-import.js

# Start server
node examples/preview-server.js
# Open http://localhost:3000
```

Browse tables and run queries in browser.

## Validated in this environment

- DuckDB CLI + `hf://`
- Node.js (`@duckdb/node-api`) + `hf://` + import to local `.duckdb`
- Python `duckdb` package + same flow
- ClawHub skill published and inspectable

## Roadmap - All Features Completed Sequentially ✅

- [x] Local file import (CSV/TSV/JSON/Parquet/Excel) — **done** (`lib/duckdb-helper.js`)
- [x] HF token management + direct `hf://` access — **done**
- [x] Full CLI (`bin/duck.js`): import, hf, query, tables, describe, export
- [x] Rust / Tauri backend prototype — **done** (`rust-backend/`, Rust 1.96 installed, code ready)
- [x] Electron integration example — **done**
- [x] Preview / Query UI — **done** (HTTP server at `examples/preview-server.js`)
- [x] ClawHub Skill published — **done** (see below)

**Published ClawHub Skill**: `xiaoqianran-duck` v1.0.0 by @xiaoqianran (CLEAN)

All core features for the DuckDB + HF + multi-frontend data tool are implemented.

See GitHub issues or use `clawhub inspect xiaoqianran-duck` for details.

## CLI Usage

```bash
# After npm link or npx
duck import ./sales.csv
duck hf hf://datasets/user/ds/data.parquet my_table
duck query "SELECT city, COUNT(*) FROM my_table GROUP BY city"
duck tables
duck describe my_table
duck export my_table output.parquet
```

Run with: `npm run cli -- import file.csv` or directly `node bin/duck.js ...`
