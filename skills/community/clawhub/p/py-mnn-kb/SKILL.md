---
name: py_mnn_kb
description: >
  Local vector knowledge base with GraphRAG retrieval (vector + BM25 + knowledge graph).
  Use this skill when the user mentions: "查知识库", "加入知识库", "记住这个", "save to KB",
  "add to knowledge base", "query knowledge base", "记录一下", or similar intent to
  store or retrieve private knowledge.
license: MIT
allowed-tools:
  - kb_build
  - kb_note
  - kb_query
  - kb_status
disable: false
---

# py_mnn_kb — MNN Knowledge Base Skill

Local GraphRAG knowledge base backed by SQLite + MNN embeddings.
Fully compatible with Android OfflineAI RAG database format.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp config.example.json config.json
# Edit config.json: set llm_api.api_key, optionally change default_name
```

Key fields in `config.json`:

| Field | Default | Description |
|---|---|---|
| `knowledge_base.default_name` | `default` | KB used when `--kb` is omitted |
| `knowledge_base.storage_dir` | `assets/knowledge_bases` | Where DB files are stored |
| `llm_api.api_key` | *(required for query+LLM)* | OpenAI-compatible API key |
| `graph_ner.custom_dict_path` | `assets/example_terms.json` | Domain terminology for NER |

### 3. First run (auto-downloads embedding model)
```bash
python scripts/py_mnn_kb.py status
```
On first use, `Qwen3-Embedding-0.6B-MNN-int4` (~400 MB) is auto-downloaded into `assets/`.

---

## Tools

### `kb_build` — Build / append knowledge base from files

Indexes a directory of documents. **Runs in background; returns immediately.**
Check progress with `kb_status`.

**Parameters:**
| Name | Type | Required | Description |
|---|---|---|---|
| `dir_path` | string | yes | Directory path to index (recursive) |
| `kb_name` | string | no | KB name (default: value of `default_name` in config.json) |

**Returns:** `{ status, command, kb_name, pid, files, message }`

**Supported formats:** `.txt` `.md` `.pdf` `.docx` `.pptx` `.xlsx` `.csv` `.html` `.json` `.jsonl`

**CLI:**
```bash
python scripts/py_mnn_kb.py build ./my_docs/ --kb my_kb
python scripts/py_mnn_kb.py build ./my_docs/          # uses default KB name
```

**Trigger phrases:** "加入知识库", "索引这个目录", "build KB", "index these files"

---

### `kb_note` — Insert a text note directly into the knowledge base

Embeds and stores a free-form text snippet. **Synchronous. Refused while build is running.**

**Parameters:**
| Name | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | Text content to store |
| `kb_name` | string | no | KB name (default: `default_name`) |
| `title` | string | no | Optional title, stored as source label |

**Returns:** `{ status, kb_name, chunks_added, elapsed_sec }`

**CLI:**
```bash
python scripts/py_mnn_kb.py note "Q1 roadmap: focus on modules A and B" --kb my_kb
python scripts/py_mnn_kb.py note "$(cat meeting.txt)" --kb my_kb --title "Weekly meeting"
```

**Trigger phrases:** "记住这个", "记录一下", "加个笔记", "save this", "remember this"

---

### `kb_query` — Retrieve relevant chunks (RAG retrieval)

Runs vector + BM25 + GraphRAG fusion and returns the top-N context string.
**The agent appends this context to its prompt — no LLM call is made inside this tool.**
**Synchronous. Refused while build is running.**

**Parameters:**
| Name | Type | Required | Description |
|---|---|---|---|
| `prompt` | string | yes | Query question or keywords |
| `kb_name` | string | no | KB name (default: `default_name`) |

**Returns:** Multi-document context string, e.g.:
```
Document1 [ID:42 source:manual.pdf]:
Deployment has three steps...

Document2 [ID:55 source:notes.md]:
...
```

**CLI:**
```bash
python scripts/py_mnn_kb.py query "NAND筛选核心流程" --kb my_kb --no-llm
python scripts/py_mnn_kb.py --output json query "产品路线图" --kb my_kb
```

**Agent usage pattern:**
```
context = kb_query("用户的问题", kb_name="my_kb")
# Then: f"Based on the following context:\n{context}\n\nQuestion: {user_question}"
```

**Trigger phrases:** "查知识库", "查一下", "知识库里有没有", "search KB"

---

### `kb_status` — Check build progress or last build result

**No KB initialization needed. Always returns instantly.**

**Parameters:**
| Name | Type | Required | Description |
|---|---|---|---|
| `kb_name` | string | no | (informational only, does not affect result) |

**Returns:**
- While building: `{ status: "building", progress: 0-100, message }`
- After success:  `{ status: "ok", message, stats: { chunks_added, elapsed_sec, ... } }`
- After failure:  `{ status: "error", error }`
- Not yet run:    `{ status: "idle", message }`

**CLI:**
```bash
python scripts/py_mnn_kb.py status
```

**Trigger phrases:** "构建进度", "build status", "知识库建好了吗"

---

## Workflow Examples

**A · User uploads files → auto-index**
```
User: "把这些文档加入知识库"
Agent → save files to temp dir
      → kb_build(dir_path=tmp_dir, kb_name="my_kb")   # returns immediately
      → "已开始后台构建，用 kb_status 检查进度"
```

**B · User dictates a note → insert**
```
User: "记住：STAR2000 低温写性能提升 8%"
Agent → kb_note(text="STAR2000 低温写性能提升 8%", kb_name="my_kb", title="技术发现")
      → "已保存到知识库 my_kb"
```

**C · User asks a question → KB-assisted answer**
```
User: "NAND 筛选核心流程是什么？"
Agent → context = kb_query("NAND 筛选核心流程", kb_name="my_kb")
      → append context to LLM prompt → generate answer
```

**D · Check if build finished before querying**
```
Agent → st = kb_status()
      → if st["status"] == "building": tell user to wait
      → else: proceed with kb_query(...)
```

---

## Notes

- `kb_build` is **incremental append** — re-running on the same directory adds only new content
- `kb_note` and `kb_query` are **blocked** (return `status: building`) while a build is running
- `--output json` on any CLI command returns machine-parseable JSON on stdout
- KB name `default` is used when `--kb` is omitted; configure `default_name` in `config.json`
