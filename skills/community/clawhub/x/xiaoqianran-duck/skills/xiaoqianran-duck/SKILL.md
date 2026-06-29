---
name: xiaoqianran-duck
description: Local analytical data tool powered by DuckDB. Supports importing and querying CSV, TSV, JSON, Parquet, Excel and direct Hugging Face datasets via hf:// protocol with token support. Includes CLI, Node helper, preview server, and Rust backend for Tauri/Electron/Qt apps.
---

# xiaoqianran-duck

Local analytical data tool powered by **DuckDB**.

## Vision

A desktop-first data explorer that combines:

- **Powerful local storage**: Single-file `data.duckdb`
- **Multi-format support**: CSV / TSV / JSON / Parquet / Excel
- **Hugging Face integration**: Direct access via `hf://` (no need to download everything first) + token login for gated datasets
- **Flexible frontends**: Designed to work with Tauri, Electron, or Qt

## Installation & Quick Start

```bash
# Node
npm install xiaoqianran-duck

# CLI
npx xiaoqianran-duck import data.csv
npx xiaoqianran-duck hf hf://datasets/user/ds/data.parquet mytable
npx xiaoqianran-duck query "SELECT * FROM mytable LIMIT 10"
```

See full README.md and examples/.

## Features

- Query remote Hugging Face datasets directly with DuckDB `hf://` protocol
- Import selected data from HF or local files (CSV/TSV/JSON/Parquet/Excel) into `data.duckdb`
- Fast analytical queries (Parquet-first)
- Export to Parquet/CSV/JSON
- Cross-platform desktop app support
- CLI, Node.js helper, simple HTTP preview server, Rust backend prototype

## HF Token Support (for gated datasets)

```bash
export HF_TOKEN=hf_your_token
# or put in .env next to data.duckdb
```

In code:
```js
const helper = new DuckDBHelper('data.duckdb');
await helper.setHFTtoken(process.env.HF_TOKEN);
await helper.importFromHF('hf://datasets/user/private-ds/data.parquet');
```

## Usage Examples

### Import local files

```bash
duck import sales.csv
duck import data.parquet my_sales
duck import report.xlsx
```

In JS:
```js
const DuckDBHelper = require('xiaoqianran-duck');
const helper = new DuckDBHelper('./data.duckdb');
await helper.importFile('./data.csv');
await helper.importFile('./big.parquet', 'big_data');
```

### HF datasets (direct, no full download)

```bash
duck hf hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet
```

Supports @~parquet suffix for optimized Parquet views on HF.

### Queries

```bash
duck query "SELECT city, COUNT(*) as cnt FROM mytable GROUP BY city"
duck query "SELECT * FROM 'data.csv' LIMIT 5"   # direct file query
```

### List / Inspect / Export

```bash
duck tables
duck describe mytable
duck export mytable backup.parquet
```

### Preview Server (web UI)

```bash
node examples/preview-server.js
# Open http://localhost:3000
# Browse tables and run queries in browser
```

## Rust Backend (for Tauri)

See rust-backend/src/main.rs for DuckDB-rs example with HF and local import.

Compile with cargo build (uses bundled DuckDB).

## Architecture

Frontend (Tauri/Electron/Qt) → DuckDB (data.duckdb) → Files (local + hf://)

## License

MIT

See README.md for full details and code.
