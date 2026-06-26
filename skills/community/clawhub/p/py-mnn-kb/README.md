# py_mnn_kb — MNN Knowledge Base
Local vector knowledge base fully compatible with Android OfflineAI RAG implementation. Can be used as an **OpenClaw Skill** to let AI Agents automatically manage and query private knowledge bases.
---
## Features
- **Cross-platform database compatibility**: `knowledge_graph.db` format is fully compatible with Android. Knowledge bases built on PC can be directly used on mobile devices and vice versa
- **Auto model download**: Automatically downloads `Qwen3-Embedding-0.6B-MNN-int4` from ModelScope on first run, no manual setup required
- **GraphRAG retrieval**: Three-way fusion of vector similarity + BM25 keyword + knowledge graph entity relationships
- **Incremental append**: `build` command only appends new files to existing knowledge base, no rebuild
- **Structured JSON parsing**: Auto-detects Alpaca/CoT/DPO/Conversation training set formats and indexes by entry
---
## Directory Structure
```
py_mnn_kb/
├── scripts/
│   └── py_mnn_kb.py            # Core library + CLI entry
├── assets/
│   ├── knowledge_bases/        # KB storage (auto-created, gitignored)
│   │   └── <kb_name>/
│   │       ├── knowledge_graph.db
│   │       └── metadata.json
│   ├── Qwen3-Embedding-0.6B-MNN-int4/  # Auto-downloaded on first run
│   ├── example_stop.json       # Stopwords list (customizable)
│   └── example_terms.json      # Domain terminology examples
├── config.json             # Your local config (gitignored — copy from example)
├── config.example.json     # Config template committed to git
├── requirements.txt
└── README.md
```
---
## Quick Start
### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
`requirements.txt` packages:
| Package | Purpose | Required |
|---|---|---|
| `MNN>=3.0.0` | MNN Python inference backend (embedding computation) | Required |
| `jieba>=0.42.1` | Chinese word segmentation (NER entity extraction) | Required |
| `psutil>=5.9.0` | Build process monitoring | Required |
| `openai>=1.0.0` | LLM API client (query command LLM generation) | query+LLM |
| `pdfplumber` | PDF parsing | Optional |
| `python-docx` | .docx parsing | Optional |
| `python-pptx` | .pptx parsing | Optional |
| `openpyxl` | .xlsx parsing | Optional |
| `beautifulsoup4` | HTML parsing | Optional |
### 2. Configure
```bash
cp config.example.json config.json
# Edit config.json: set llm_api.api_key (required for query with LLM)
```
### 3. Run
```bash
# Build knowledge base (auto-downloads model on first run)
python scripts/py_mnn_kb.py build ./my_docs/ --kb myproject
# Add note
python scripts/py_mnn_kb.py note "Meeting decision: ..." --kb myproject
# Query (with LLM answer)
python scripts/py_mnn_kb.py query "What is the deployment process?" --kb myproject
# Pure retrieval, no LLM
python scripts/py_mnn_kb.py query "What is the deployment process?" --kb myproject --no-llm
```
---
## CLI Commands
### `build` — Build/Append Knowledge Base
```
python scripts/py_mnn_kb.py build <dir> [--kb <name>] [--config <path>]
```
| Parameter | Description |
|---|---|
| `dir` | Directory to index (recursively scans all supported files) |
| `--kb` | Knowledge base name (default: `default_name` in config.json) |
| `--config` | Config file path (default: config.json in same dir as py_mnn_kb.py) |
**Supported formats**: `.txt` `.md` `.pdf` `.docx` `.pptx` `.xlsx` `.csv` `.html` `.json` `.jsonl`
**Examples**:
```bash
python scripts/py_mnn_kb.py build ../docs/ --kb company_kb
python scripts/py_mnn_kb.py build /tmp/new_files/ --kb company_kb   # Append, no overwrite
```
---
### `note` — Add Text Note
```
python scripts/py_mnn_kb.py note "<text>" [--kb <name>] [--title <title>]
```
| Parameter | Description |
|---|---|
| `text` | Text content to add |
| `--kb` | Knowledge base name |
| `--title` | Optional title, written to metadata |
**Examples**:
```bash
python scripts/py_mnn_kb.py note "Q1 2025 roadmap: focus on modules A and B..." --kb company_kb
python scripts/py_mnn_kb.py note "$(cat meeting_notes.txt)" --kb company_kb --title "Weekly meeting"
```
---
### `query` — RAG Query
```
python scripts/py_mnn_kb.py query "<prompt>" [--kb <name>] [--no-llm] [--output json]
```
| Parameter | Description |
|---|---|
| `prompt` | Query question |
| `--kb` | Knowledge base name |
| `--no-llm` | Only return retrieved document chunks, no LLM call |
| `--output json` | Output full result in JSON format (for Agent parsing) |
**Examples**:
```bash
python scripts/py_mnn_kb.py query "What are the specs of STAR1200?" --kb company_kb
python scripts/py_mnn_kb.py query "DDR sorting principles" --kb company_kb --no-llm
python scripts/py_mnn_kb.py --output json query "Product roadmap" --kb company_kb
```
**JSON output format**:
```json
{
  "status": "ok",
  "command": "query",
  "kb_name": "company_kb",
  "prompt": "Product roadmap",
  "llm_used": true,
  "context": "Document1 [ID:42]:\n...",
  "context_chars": 4800,
  "answer": "Based on the knowledge base...",
  "answer_chars": 512
}
```
---
## Python API (Use as Library)
```python
import sys
sys.path.insert(0, "scripts")
from py_mnn_kb import KnowledgeBase
kb = KnowledgeBase("config.json")  # config.json is at project root
# 1. Build knowledge base
stats = kb.build_kb(files=["doc1.pdf", "manual.docx"], kb_name="myproject")
# → {'status': 'ok', 'kb_name': 'myproject', 'chunks_added': 86, 'elapsed_sec': 45.2}
# 2. Add note
stats = kb.add_note(text="Key finding: ...", kb_name="myproject", title="Meeting notes")
# → {'status': 'ok', 'chunks_added': 1, 'elapsed_sec': 1.2}
# 3. RAG retrieval (returns concatenated context string)
context = kb.query_kb(prompt="What is the deployment process?", kb_name="myproject")
# → "Document1 [ID:42 source:manual.docx]:\nDeployment has three steps..."
```
---
## Use as OpenClaw Skill
### Skill Definition
```python
from py_mnn_kb import KnowledgeBase
from pathlib import Path
kb = KnowledgeBase()
SKILLS = {
    "kb_build": {
        "description": "Build/append vector knowledge base from local directory or files. Supports PDF/Word/PPT/Excel/HTML/TXT/JSON formats. JSON training sets are automatically indexed by structured entries.",
        "function": lambda dir_path, kb_name="default": kb.build_kb(
            files=[str(f) for f in Path(dir_path).rglob("*") if f.is_file()],
            kb_name=kb_name
        ),
        "parameters": {
            "dir_path": "Directory path to index",
            "kb_name": "Knowledge base name (optional, default 'default')"
        }
    },
    "kb_note": {
        "description": "Insert a text snippet (note, summary, chat fragment) directly into knowledge base for immediate retrieval. Suitable for scattered knowledge points from user dictation or paste.",
        "function": lambda text, kb_name="default", title="": kb.add_note(text, kb_name, title=title),
        "parameters": {
            "text": "Text content to store",
            "kb_name": "Knowledge base name (optional)",
            "title": "Title (optional)"
        }
    },
    "kb_query": {
        "description": "Retrieve document chunks most relevant to the question from knowledge base, returns context string. Agent can directly append this context to prompt for LLM to answer.",
        "function": lambda prompt, kb_name="default": kb.query_kb(prompt, kb_name),
        "parameters": {
            "prompt": "Query question or keywords",
            "kb_name": "Knowledge base name (optional)"
        }
    },
    "kb_status": {
        "description": "Check knowledge base build status. Returns build progress if building, last build result if idle, or error if build failed. Does not require KB initialization, instant return.",
        "function": lambda kb_name="default": kb.get_build_status(kb_name),
        "parameters": {
            "kb_name": "Knowledge base name (optional)"
        }
    }
}
```
### Agent Usage Examples
**Scenario A: User uploads file → Auto-index**
```
User: "Add this PDF to knowledge base"
Agent → Save PDF to temp dir → Call kb_build(dir_path=tmp_dir, kb_name="user_kb")
      → Show progress: "Added 32 knowledge chunks to user_kb"
```
**Scenario B: User specifies text → Insert note**
```
User: "Remember this: STAR2000 write performance improved 8% at low temperature"
Agent → Call kb_note(text="...", kb_name="user_kb", title="Tech finding")
      → "Saved to knowledge base user_kb"
```
**Scenario C: User asks question → KB-assisted answer**
```
User: "What is the core NAND screening process?"
Agent → Call kb_query(prompt="NAND screening core process", kb_name="user_kb")
      → Get context → Append to LLM prompt → Generate answer
```
**Scenario D: Summarize webpage/article → Store in KB**
```
User: "Summarize this webpage and save it"
Agent → Crawl webpage → LLM summarizes to knowledge points → Save as temp alpaca JSON
      → Call kb_build(dir_path=tmp_dir, kb_name="user_kb")
```
### OpenClaw Skill Prompt Suggestions
```
You have the following knowledge base tools:
1. kb_build(dir_path, kb_name) - Batch import files from directory to knowledge base
   - Call when user says "add these files to KB", "index this directory"
   - Supported formats: PDF/Word/PPT/Excel/HTML/TXT/JSON
   - Save files to temp directory first, then call this function
   - Returns immediately, build runs in background
2. kb_note(text, kb_name, title) - Insert text snippet directly to knowledge base
   - Call when user says "remember this", "save this text", "add note"
   - Also used for webpage summaries, meeting notes, etc.
3. kb_query(prompt, kb_name) - Retrieve relevant content from knowledge base
   - When user asks questions, call this first to get context, then generate answer
   - Append returned context to your prompt: "Based on: {context}\n\n{question}"
4. kb_status(kb_name) - Check build progress or last build result
   - Call to check if build is still running before calling note/query
   - Returns progress percentage if building, or last build stats if idle
   - Instant return, no KB initialization needed
Notes:
- kb_name defaults to "default", use different names for different projects
- build is incremental append, won't overwrite existing data
- query returns raw context, you're responsible for understanding and generating final answer
- Always check status before note/query if build was recently started
```
---
## config.json Parameters
### `chunking` — Text Chunking
| Parameter | Default | Description |
|---|---|---|
| `chunk_size` | 500 | Chunk size (characters), aligned with Android default |
| `chunk_overlap` | 100 | Adjacent chunk overlap, ensures context continuity |
| `min_chunk_size` | 10 | Minimum chunk size, filters noise fragments |
| `enable_json_dataset_opt` | true | JSON training sets indexed by entry, no re-chunking |
### `retrieval` — Retrieval Parameters
| Parameter | Default | Description |
|---|---|---|
| `search_depth` | 10 | Final number of documents returned |
| `bm25_enabled` | true | Enable BM25 keyword retrieval (RRF fusion with vector) |
| `graph_rag_enabled` | true | Enable knowledge graph entity relationship enhancement |
| `graph_rag_weight_preset` | 1 | Fusion weight: 0=vector_first, 1=balanced, 2=graph_enhanced |
| `graph_rag_vector_expand` | 20 | Vector coarse retrieval count (then graph rerank) |
### `graph_ner` — Entity Recognition
| Parameter | Description |
|---|---|
| `custom_dict_path` | Domain terminology dictionary JSON (improves entity recognition) |
| `stopwords_path` | Stopwords list JSON (filters high-frequency noise words) |
| `enabled` | Whether to enable Graph NER |
---
## Database Format (Fully Compatible with Android)
SQLite table structure:
```
documents      - Text chunks + vectors (BLOB, little-endian float32 × 1024)
entities       - NER entities + frequency stats
entity_edges   - Entity co-occurrence graph (with weights)
chunk_entities - Chunk-entity many-to-many mapping
metadata       - KB metadata (model, dim, chunk params, etc.)
```
Vector serialization fully compatible with Android:
```python
# Python
struct.pack(f"<{len(vec)}f", *vec)
# Java
ByteBuffer.allocate(n*4).order(ByteOrder.LITTLE_ENDIAN).putFloat(v)...