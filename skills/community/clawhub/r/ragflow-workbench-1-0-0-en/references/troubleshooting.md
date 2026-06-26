# Troubleshooting Guide

This guide documents common issues encountered when running the RAGFlow skill pack, along with investigation strategies and solutions. This document is updated continuously to improve system robustness.

---

## 1. Embedding Error: `input (X tokens) is too large to process`

### Background
After uploading a file and triggering parsing, if a document chunk exceeds the Embedding API service's physical batch size limit (e.g., vLLM/TGI defaults to 512 tokens), the parse task will fail.

**Example error:**
```text
[ERROR]Generate embedding error:Error code: 500 - {'error': {
    'code': 500, 
    'message': 'input (549 tokens) is too large to process. increase the physical batch size (current batch size: 512)', 
    'type': 'server_error'
}}
```

### Investigation Steps
1. **Check knowledge base configuration**: Look at the current `chunk_token_num` (max chunk token count).
   ```bash
   uv run python scripts/datasets.py info <dataset_id> --json
   ```
2. **Confirm API limit**: Identify the Embedding service limit from the error message (e.g., 512 above).

### Solution
Reduce the knowledge base's `chunk_token_num`. Recommended value is **50%~60%** of the Embedding API's physical limit.

**Steps:**
1. Create or edit `_parser_config.json`:
   ```json
   {"chunk_token_num": 256}
   ```
2. Update the configuration using `update_dataset.py`:
   ```bash
   uv run python scripts/update_dataset.py <dataset_id> --parser-config "@_parser_config.json" --json
   ```
3. **Key point**: After modification, you must **delete old documents and re-upload/re-parse** for the new config to take effect.

---

## How to Contribute
If you encounter a new issue and find a solution, please add it to this guide using the following format:
1. **Problem description/background** (include specific error logs)
2. **Investigation steps**
3. **Solution** (prefer script-based commands)
