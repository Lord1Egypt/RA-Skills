---
name: sdw-kb
description: any input (code, docs, papers, images) → knowledge graph → clustered communities → HTML + JSON + audit report. Uses graphifyy via uv tool environment. Trigger whenever the user mentions knowledge graphs, graphify, sdw-kb, or wants to turn files/code/docs into a navigable knowledge graph, even if they don't explicitly say "sdw-kb".
trigger: /sdw-kb
---

# /sdw-kb

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

**This skill uses `graphifyy` installed via `uv tool install graphifyy`.** All Python commands must run through the uv tool virtual environment.

## Default Knowledge Base Directory

All knowledge bases are stored under `~/.sdw/knowledge_bases/`. This directory is at the same level as `~/.sdw/skills/` (if it exists). Each knowledge base is a subfolder, and each subfolder always contains a `graphify-out/` directory with the graph outputs.

```
~/.sdw/
├── knowledge_bases/
│   ├── my-project/
│   │   ├── graphify-out/
│   │   │   ├── graph.json
│   │   │   ├── graph.html
│   │   │   ├── GRAPH_REPORT.md
│   │   │   └── cost.json
│   │   ├── .graphify_detect.json   (temp, cleaned up after run)
│   │   └── ... (other temp files)
│   ├── research-papers/
│   │   └── graphify-out/
│   └── codebase-x/
│       └── graphify-out/
```

### Path Resolution Rules

When the user invokes `/sdw-kb`, resolve the **working KB directory** (where `graphify-out/` lives and temp files are written) as follows:

1. **`/sdw-kb <path> --kb <name>`** — Use `<path>` as the input corpus. The KB directory is `~/.sdw/knowledge_bases/<name>/`. Create it if it doesn't exist.
2. **`/sdw-kb <path>`** (no `--kb`) — Use `<path>` as input. Derive the KB name from the last component of the path (e.g., `/home/user/projects/my-app` → KB name `my-app`). KB directory is `~/.sdw/knowledge_bases/my-app/`.
3. **`/sdw-kb --kb <name>`** (no path) — The KB must already exist at `~/.sdw/knowledge_bases/<name>/`. Use it for query/explain/path/cluster-only operations. If the KB doesn't exist, tell the user: "Knowledge base '<name>' not found. Run `/sdw-kb <source-path> --kb <name>` to create it."
4. **`/sdw-kb`** (no path, no --kb) — Use `.` (current directory) as input. Derive KB name from the current directory name.
5. **`/sdw-kb list`** — List all knowledge bases in `~/.sdw/knowledge_bases/`, showing name, node/edge count (from `graph.json`), and last modified date.

**All `graphify-out/` output paths and all temp files (`.graphify_*.json`, etc.) are written inside the KB directory, NOT in the current working directory.** This keeps each KB self-contained. When the skill references `graphify-out/...` or `.graphify_*.json` in the pipeline steps below, always prepend the KB directory path (e.g., `~/.sdw/knowledge_bases/my-project/graphify-out/graph.json`).

At the start of every run, `cd` into the KB directory so that all relative paths resolve correctly, then `cd` back when done.

## Usage

```
/sdw-kb                                             # full pipeline on current directory, KB name = dir name
/sdw-kb <path>                                      # full pipeline, KB name derived from path
/sdw-kb <path> --kb my-project                      # full pipeline, explicit KB name
/sdw-kb --kb my-project query "<question>"           # query an existing KB by name
/sdw-kb list                                        # list all knowledge bases
/sdw-kb <path> --mode deep                          # thorough extraction, richer INFERRED edges
/sdw-kb <path> --update                             # incremental - re-extract only new/changed files
/sdw-kb <path> --directed                            # build directed graph (preserves edge direction: source→target)
/sdw-kb --kb my-project --cluster-only              # rerun clustering on existing KB
/sdw-kb <path> --no-viz                             # skip visualization, just report + JSON
/sdw-kb <path> --svg                                # also export graph.svg (embeds in Notion, GitHub)
/sdw-kb <path> --graphml                            # export graph.graphml (Gephi, yEd)
/sdw-kb <path> --neo4j                              # generate cypher.txt for Neo4j
/sdw-kb <path> --neo4j-push bolt://localhost:7687   # push directly to Neo4j
/sdw-kb <path> --obsidian --obsidian-dir ~/vaults/my-project
/sdw-kb <path> --mcp                                # start MCP stdio server for agent access
/sdw-kb <path> --watch                              # watch folder, auto-rebuild on code changes
/sdw-kb add <url>                                   # fetch URL, save to KB's ./raw, update graph
/sdw-kb add <url> --author "Name"                   # tag who wrote it
/sdw-kb query "<question>"                          # BFS traversal on current-dir KB
/sdw-kb query "<question>" --dfs                    # DFS - trace a specific path
/sdw-kb query "<question>" --budget 1500            # cap answer at N tokens
/sdw-kb path "AuthModule" "Database"                # shortest path between two concepts
/sdw-kb explain "SwinTransformer"                   # plain-language explanation of a node
```

## What sdw-kb is for

sdw-kb is built around Andrej Karpathy's /raw folder workflow: drop anything into a folder - papers, tweets, screenshots, code, notes - and get a structured knowledge graph that shows you what you didn't know was connected.

Three things it does that your AI assistant alone cannot:
1. **Persistent graph** - relationships are stored in `graphify-out/graph.json` and survive across sessions. Ask questions weeks later without re-reading everything.
2. **Honest audit trail** - every edge is tagged EXTRACTED, INFERRED, or AMBIGUOUS. You know what was found vs invented.
3. **Cross-document surprise** - community detection finds connections between concepts in different files that you would never think to ask about directly.

Use it for:
- A codebase you're new to (understand architecture before touching anything)
- A reading list (papers + tweets + notes → one navigable graph)
- A research corpus (citation graph + concept graph in one)
- Your personal /raw folder (drop everything in, let it grow, query it)

## What You Must Do When Invoked

Follow these steps in order. Do not skip steps.

### Step 0 - Resolve KB directory

First, determine the KB name and working directory according to the Path Resolution Rules above.

```powershell
$KB_BASE = "$HOME/.sdw/knowledge_bases"
New-Item -ItemType Directory -Force -Path $KB_BASE | Out-Null

# Determine KB_NAME based on user input:
# - If --kb <name> was given: $KB_NAME = "<name>"
# - If <path> was given but no --kb: $KB_NAME = (Split-Path -Leaf "<path>")
# - If neither: $KB_NAME = (Split-Path -Leaf (Get-Location))
$KB_DIR = "$KB_BASE/$KB_NAME"
New-Item -ItemType Directory -Force -Path $KB_DIR | Out-Null
New-Item -ItemType Directory -Force -Path "$KB_DIR/graphify-out" | Out-Null
```

For **`/sdw-kb list`**, enumerate all subdirectories under `$KB_BASE` and for each, read `graphify-out/graph.json` to show node/edge count:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json, os
from pathlib import Path
from datetime import datetime

kb_base = Path.home() / '.sdw' / 'knowledge_bases'
if not kb_base.exists():
    print('No knowledge bases found. Run /sdw-kb <path> to create one.')
    raise SystemExit(0)

kbs = sorted([d for d in kb_base.iterdir() if d.is_dir()])
if not kbs:
    print('No knowledge bases found. Run /sdw-kb <path> to create one.')
    raise SystemExit(0)

print(f'Knowledge bases ({len(kbs)}):')
print(f'  {\"Name\":<30} {\"Nodes\":>8} {\"Edges\":>8} {\"Last Modified\":>20}')
print(f'  {\"-\"*30} {\"-\"*8} {\"-\"*8} {\"-\"*20}')
for kb in kbs:
    graph_file = kb / 'graphify-out' / 'graph.json'
    if graph_file.exists():
        data = json.loads(graph_file.read_text())
        nodes = len(data.get('nodes', []))
        links = len(data.get('links', []))
        mtime = datetime.fromtimestamp(graph_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        print(f'  {kb.name:<30} {nodes:>8} {links:>8} {mtime:>20}')
    else:
        print(f'  {kb.name:<30} {\"(empty)\":>8} {\"\":>8} {\"\":>20}')
"
```

If the user ran `/sdw-kb list`, stop here. Otherwise proceed.

**All subsequent steps use `$KB_DIR` as the working directory.** Every reference to `graphify-out/` becomes `$KB_DIR/graphify-out/`, and every temp file (`.graphify_*.json`) is written to `$KB_DIR/`. Concretely, in every code block below:
- Replace `.graphify_detect.json` with `$KB_DIR/.graphify_detect.json`
- Replace `.graphify_ast.json` with `$KB_DIR/.graphify_ast.json`
- Replace `.graphify_semantic.json` with `$KB_DIR/.graphify_semantic.json`
- Replace `.graphify_extract.json` with `$KB_DIR/.graphify_extract.json`
- Replace `.graphify_analysis.json` with `$KB_DIR/.graphify_analysis.json`
- Replace `.graphify_labels.json` with `$KB_DIR/.graphify_labels.json`
- Replace `.graphify_cached.json` with `$KB_DIR/.graphify_cached.json`
- Replace `.graphify_uncached.txt` with `$KB_DIR/.graphify_uncached.txt`
- Replace `.graphify_semantic_new.json` with `$KB_DIR/.graphify_semantic_new.json`
- Replace `.graphify_incremental.json` with `$KB_DIR/.graphify_incremental.json`
- Replace `graphify-out/` with `$KB_DIR/graphify-out/`
- Replace `New-Item -ItemType Directory -Force -Path graphify-out` with using `$KB_DIR/graphify-out` (already created in Step 0)

The simplest approach: `cd` into `$KB_DIR` before running the pipeline, and `cd` back to the original directory when done. This way all relative paths resolve naturally inside the KB directory.

### UV Python Helper

All Python commands in this skill MUST use the Python interpreter from the uv tool virtual environment. Define this helper at the start:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
```

Every `python -c` command below should be replaced with `& $UV_PYTHON -c`. This ensures graphify modules are always importable.

### Step 1 - Ensure graphifyy is installed via uv

```powershell
# Set up the Python path from uv tool environment
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"

# Check if graphifyy is installed via uv
if (-not (Test-Path $UV_PYTHON)) {
    Write-Host "graphifyy not found in uv tools. Installing..."
    uv tool install graphifyy
    $UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
}

# Verify import works
& $UV_PYTHON -c "import graphify; print(f'graphify {graphify.__version__} ready (via uv)')"
```

If the import succeeds, print the version and move straight to Step 2. If uv is not installed, stop and tell the user:
> "This skill requires `uv`. Install it first: https://docs.astral.sh/uv/getting-started/installation/"

### Step 2 - Detect files

The INPUT_PATH is the source corpus path the user provided (or `.` if none). Temp files and outputs go into `$KB_DIR`.

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from graphify.detect import detect
from pathlib import Path
result = detect(Path('INPUT_PATH'))
print(json.dumps(result))
" > "$KB_DIR/.graphify_detect.json"
```

Replace INPUT_PATH with the actual path the user provided. Do NOT cat or print the JSON - read it silently and present a clean summary instead:

```
Corpus: X files · ~Y words
  code:     N files (.py .ts .go ...)
  docs:     N files (.md .txt ...)
  papers:   N files (.pdf ...)
  images:   N files
  video:    N files (.mp4 .mp3 ...)
```

Omit any category with 0 files from the summary.

Then act on it:
- If `total_files` is 0: stop with "No supported files found in [path]."
- If `skipped_sensitive` is non-empty: mention file count skipped, not the file names.
- If `total_words` > 2,000,000 OR `total_files` > 200: show the warning and the top 5 subdirectories by file count, then ask which subfolder to run on. Wait for the user's answer before proceeding.
- Otherwise: proceed directly to Step 2.5 if video files were detected, or Step 3 if not.

### Step 2.5 - Transcribe video / audio files (only if video files detected)

Skip this step entirely if `detect` returned zero `video` files.

Video and audio files cannot be read directly. Transcribe them to text first, then treat the transcripts as doc files in Step 3.

**Strategy:** Read the god nodes from the detect output or analysis file. You are already a language model - write a one-sentence domain hint yourself from those labels. Then pass it to Whisper as the initial prompt. No separate API call needed.

**However**, if the corpus has *only* video files and no other docs/code, use the generic fallback prompt: `"Use proper punctuation and paragraph breaks."`

**Step 1 - Write the Whisper prompt yourself.**

Read the top god node labels from detect output or analysis, then compose a short domain hint sentence.

Set it as `$env:GRAPHIFY_WHISPER_PROMPT` before running the transcription command.

**Step 2 - Transcribe (PowerShell):**

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json, os
from pathlib import Path
from graphify.transcribe import transcribe_all

detect = json.loads(Path('graphify-out/.graphify_detect.json').read_text())
video_files = detect.get('files', {}).get('video', [])
prompt = os.environ.get('GRAPHIFY_WHISPER_PROMPT', 'Use proper punctuation and paragraph breaks.')

transcript_paths = transcribe_all(video_files, initial_prompt=prompt)
print(json.dumps(transcript_paths))
" | Out-File -FilePath graphify-out\.graphify_transcripts.json -Encoding utf8
```

After transcription:
- Read the transcript paths from `graphify-out\.graphify_transcripts.json`
- Add them to the docs list before dispatching semantic subagents in Step 3B
- Print how many transcripts were created: `Transcribed N video file(s) -> treating as docs`
- If transcription fails for a file, print a warning and continue with the rest

**Whisper model:** Default is `base`. If the user passed `--whisper-model <name>`, set `$env:GRAPHIFY_WHISPER_MODEL = "<name>"` before running the command above.

### Step 3 - Extract entities and relationships

**Before starting:** note whether `--mode deep` was given. You must pass `DEEP_MODE=true` to every subagent in Step B2 if it was. Track this from the original invocation - do not lose it.

This step has two parts: **structural extraction** (deterministic, free) and **semantic extraction** (your AI model, costs tokens).

**Run Part A (AST) and Part B (semantic) in parallel. Dispatch all semantic subagents AND start AST extraction in the same message. Both can run simultaneously since they operate on different file types. Merge results in Part C as before.**

#### Part A - Structural extraction for code files

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.extract import collect_files, extract
from pathlib import Path
import json

code_files = []
detect = json.loads(Path('.graphify_detect.json').read_text())
for f in detect.get('files', {}).get('code', []):
    code_files.extend(collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])

if code_files:
    result = extract(code_files)
    Path('.graphify_ast.json').write_text(json.dumps(result, indent=2))
    print(f'AST: {len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges')
else:
    Path('.graphify_ast.json').write_text(json.dumps({'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}))
    print('No code files - skipping AST extraction')
"
```

#### Part B - Semantic extraction (parallel subagents)

**Fast path:** If detection found zero docs, papers, and images (code-only corpus), skip Part B entirely and go straight to Part C. AST handles code - there is nothing for semantic subagents to do.

**MANDATORY: You MUST use the Agent tool here. Reading files yourself one-by-one is forbidden - it is 5-10x slower. If you do not use the Agent tool you are doing this wrong.**

Before dispatching subagents, print a timing estimate:
- Load `total_words` and file counts from `.graphify_detect.json`
- Estimate agents needed: `ceil(uncached_non_code_files / 22)` (chunk size is 20-25)
- Estimate time: ~45s per agent batch (they run in parallel, so total ≈ 45s × ceil(agents/parallel_limit))
- Print: "Semantic extraction: ~N files → X agents, estimated ~Ys"

**Step B0 - Check extraction cache first**

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from graphify.cache import check_semantic_cache
from pathlib import Path

detect = json.loads(Path('.graphify_detect.json').read_text())
all_files = [f for files in detect['files'].values() for f in files]

cached_nodes, cached_edges, cached_hyperedges, uncached = check_semantic_cache(all_files)

if cached_nodes or cached_edges or cached_hyperedges:
    Path('.graphify_cached.json').write_text(json.dumps({'nodes': cached_nodes, 'edges': cached_edges, 'hyperedges': cached_hyperedges}))
Path('.graphify_uncached.txt').write_text('\n'.join(uncached))
print(f'Cache: {len(all_files)-len(uncached)} files hit, {len(uncached)} files need extraction')
"
```

Only dispatch subagents for files listed in `.graphify_uncached.txt`. If all files are cached, skip to Part C directly.

**Step B1 - Split into chunks**

Load files from `.graphify_uncached.txt`. Split into chunks of 20-25 files each. Each image gets its own chunk (vision needs separate context).

**Step B2 - Dispatch ALL subagents in a single message**

Call the Agent tool multiple times IN THE SAME RESPONSE - one call per chunk. This is the only way they run in parallel. If you make one Agent call, wait, then make another, you are doing it sequentially and defeating the purpose.

Each subagent receives this exact prompt (substitute FILE_LIST, CHUNK_NUM, TOTAL_CHUNKS, and DEEP_MODE):

```
You are a graphify extraction subagent. Read the files listed and extract a knowledge graph fragment.
Output ONLY valid JSON matching the schema below - no explanation, no markdown fences, no preamble.

Files (chunk CHUNK_NUM of TOTAL_CHUNKS):
FILE_LIST

Rules:
- EXTRACTED: relationship explicit in source (import, call, citation, "see §3.2")
- INFERRED: reasonable inference (shared data structure, implied dependency)
- AMBIGUOUS: uncertain - flag for review, do not omit

Code files: focus on semantic edges AST cannot find (call relationships, shared data, arch patterns).
  Do not re-extract imports - AST already has those.
Doc/paper files: extract named concepts, entities, citations. Also extract rationale — sections that explain WHY a decision was made, trade-offs chosen, or design intent. These become nodes with `rationale_for` edges pointing to the concept they explain.
Image files: use vision to understand what the image IS - do not just OCR.
  UI screenshot: layout patterns, design decisions, key elements, purpose.
  Chart: metric, trend/insight, data source.
  Tweet/post: claim as node, author, concepts mentioned.
  Diagram: components and connections.
  Research figure: what it demonstrates, method, result.
  Handwritten/whiteboard: ideas and arrows, mark uncertain readings AMBIGUOUS.

DEEP_MODE (if --mode deep was given): be aggressive with INFERRED edges - indirect deps,
  shared assumptions, latent couplings. Mark uncertain ones AMBIGUOUS instead of omitting.

Semantic similarity: if two concepts in this chunk solve the same problem or represent the same idea without any structural link (no import, no call, no citation), add a `semantically_similar_to` edge marked INFERRED with a confidence_score reflecting how similar they are (0.6-0.95).

Hyperedges: if 3 or more nodes clearly participate together in a shared concept, flow, or pattern that is not captured by pairwise edges alone, add a hyperedge to a top-level `hyperedges` array. Use sparingly — maximum 3 hyperedges per chunk.

confidence_score is REQUIRED on every edge - never omit it, never use 0.5 as a default:
- EXTRACTED edges: confidence_score = 1.0 always
- INFERRED edges: reason about each edge individually. 0.6-0.9 typical range.
- AMBIGUOUS edges: 0.1-0.3

Output exactly this JSON (no other text):
{"nodes":[...],"edges":[...],"hyperedges":[...],"input_tokens":0,"output_tokens":0}
```

**Step B3 - Collect, cache, and merge**

Wait for all subagents. For each result:
- Check that `graphify-out/.graphify_chunk_NN.json` exists on disk
- If the file exists and contains valid JSON with `nodes` and `edges`, include it and save to cache
- If the file is missing, print a warning
- If a subagent failed or returned invalid JSON, print a warning and skip that chunk

Save new results to cache:
```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from graphify.cache import save_semantic_cache
from pathlib import Path

new = json.loads(Path('.graphify_semantic_new.json').read_text()) if Path('.graphify_semantic_new.json').exists() else {'nodes':[],'edges':[],'hyperedges':[]}
saved = save_semantic_cache(new.get('nodes', []), new.get('edges', []), new.get('hyperedges', []))
print(f'Cached {saved} files')
"
```

Merge cached + new results into `.graphify_semantic.json`:
```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from pathlib import Path

cached = json.loads(Path('.graphify_cached.json').read_text()) if Path('.graphify_cached.json').exists() else {'nodes':[],'edges':[],'hyperedges':[]}
new = json.loads(Path('.graphify_semantic_new.json').read_text()) if Path('.graphify_semantic_new.json').exists() else {'nodes':[],'edges':[],'hyperedges':[]}

all_nodes = cached['nodes'] + new.get('nodes', [])
all_edges = cached['edges'] + new.get('edges', [])
all_hyperedges = cached.get('hyperedges', []) + new.get('hyperedges', [])
seen = set()
deduped = []
for n in all_nodes:
    if n['id'] not in seen:
        seen.add(n['id'])
        deduped.append(n)

merged = {
    'nodes': deduped,
    'edges': all_edges,
    'hyperedges': all_hyperedges,
    'input_tokens': new.get('input_tokens', 0),
    'output_tokens': new.get('output_tokens', 0),
}
Path('.graphify_semantic.json').write_text(json.dumps(merged, indent=2))
print(f'Extraction complete - {len(deduped)} nodes, {len(all_edges)} edges ({len(cached[\"nodes\"])} from cache, {len(new.get(\"nodes\",[]))} new)')
"
```
Clean up temp files: `Remove-Item -ErrorAction SilentlyContinue .graphify_cached.json, .graphify_uncached.txt, .graphify_semantic_new.json`

#### Part C - Merge AST + semantic into final extraction

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from pathlib import Path

ast = json.loads(Path('.graphify_ast.json').read_text())
sem = json.loads(Path('.graphify_semantic.json').read_text())

seen = {n['id'] for n in ast['nodes']}
merged_nodes = list(ast['nodes'])
for n in sem['nodes']:
    if n['id'] not in seen:
        merged_nodes.append(n)
        seen.add(n['id'])

merged_edges = ast['edges'] + sem['edges']
merged_hyperedges = sem.get('hyperedges', [])
merged = {
    'nodes': merged_nodes,
    'edges': merged_edges,
    'hyperedges': merged_hyperedges,
    'input_tokens': sem.get('input_tokens', 0),
    'output_tokens': sem.get('output_tokens', 0),
}
Path('.graphify_extract.json').write_text(json.dumps(merged, indent=2))
total = len(merged_nodes)
edges = len(merged_edges)
print(f'Merged: {total} nodes, {edges} edges ({len(ast[\"nodes\"])} AST + {len(sem[\"nodes\"])} semantic)')
"
```

### Step 4 - Build graph, cluster, analyze, generate outputs

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
New-Item -ItemType Directory -Force -Path graphify-out | Out-Null
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
detection  = json.loads(Path('.graphify_detect.json').read_text())

G = build_from_json(extraction)
communities = cluster(G)
cohesion = score_all(G, communities)
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: 'Community ' + str(cid) for cid in communities}
questions = suggest_questions(G, communities, labels)

report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, 'INPUT_PATH', suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report)
to_json(G, communities, 'graphify-out/graph.json')

analysis = {
    'communities': {str(k): v for k, v in communities.items()},
    'cohesion': {str(k): v for k, v in cohesion.items()},
    'gods': gods,
    'surprises': surprises,
    'questions': questions,
}
Path('.graphify_analysis.json').write_text(json.dumps(analysis, indent=2))
if G.number_of_nodes() == 0:
    print('ERROR: Graph is empty - extraction produced no nodes.')
    raise SystemExit(1)
print(f'Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities')
"
```

Replace INPUT_PATH with the actual path.

### Step 5 - Label communities

Read `.graphify_analysis.json`. For each community key, look at its node labels and write a 2-5 word plain-language name.

Then regenerate the report and save the labels:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
detection  = json.loads(Path('.graphify_detect.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}
cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

labels = LABELS_DICT

questions = suggest_questions(G, communities, labels)

report = generate(G, communities, cohesion, labels, analysis['gods'], analysis['surprises'], detection, tokens, 'INPUT_PATH', suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report)
Path('.graphify_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}))
print('Report updated with community labels')
"
```

Replace `LABELS_DICT` with the actual dict and INPUT_PATH with the actual path.

### Step 6 - Generate Obsidian vault (opt-in) + HTML

**Generate HTML always** (unless `--no-viz`). **Obsidian vault only if `--obsidian` was explicitly given.**

If `--obsidian` was given:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.export import to_obsidian, to_canvas
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())
labels_raw = json.loads(Path('.graphify_labels.json').read_text()) if Path('.graphify_labels.json').exists() else {}

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}
cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
labels = {int(k): v for k, v in labels_raw.items()}

obsidian_dir = 'OBSIDIAN_DIR'

n = to_obsidian(G, communities, obsidian_dir, community_labels=labels or None, cohesion=cohesion)
print(f'Obsidian vault: {n} notes in {obsidian_dir}/')

to_canvas(G, communities, f'{obsidian_dir}/graph.canvas', community_labels=labels or None)
print(f'Canvas: {obsidian_dir}/graph.canvas')
"
```

Generate the HTML graph (always, unless `--no-viz`):

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.export import to_html
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())
labels_raw = json.loads(Path('.graphify_labels.json').read_text()) if Path('.graphify_labels.json').exists() else {}

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}
labels = {int(k): v for k, v in labels_raw.items()}

if G.number_of_nodes() > 5000:
    print(f'Graph has {G.number_of_nodes()} nodes - too large for HTML viz.')
else:
    to_html(G, communities, 'graphify-out/graph.html', community_labels=labels or None)
    print('graph.html written - open in any browser')
"
```

### Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag)

**If `--neo4j`**:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.export import to_cypher
from pathlib import Path

G = build_from_json(json.loads(Path('.graphify_extract.json').read_text()))
to_cypher(G, 'graphify-out/cypher.txt')
print('cypher.txt written')
"
```

**If `--neo4j-push <uri>`**:

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.cluster import cluster
from graphify.export import push_to_neo4j
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())
G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}

result = push_to_neo4j(G, uri='NEO4J_URI', user='NEO4J_USER', password='NEO4J_PASSWORD', communities=communities)
print(f'Pushed to Neo4j: {result[\"nodes\"]} nodes, {result[\"edges\"]} edges')
"
```

### Step 7b - SVG export (only if --svg flag)

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.build import build_from_json
from graphify.export import to_svg
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())
labels_raw = json.loads(Path('.graphify_labels.json').read_text()) if Path('.graphify_labels.json').exists() else {}

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}
labels = {int(k): v for k, v in labels_raw.items()}

to_svg(G, communities, 'graphify-out/graph.svg', community_labels=labels or None)
print('graph.svg written')
"
```

### Step 7c - GraphML export (only if --graphml flag)

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from graphify.build import build_from_json
from graphify.export import to_graphml
from pathlib import Path

extraction = json.loads(Path('.graphify_extract.json').read_text())
analysis   = json.loads(Path('.graphify_analysis.json').read_text())

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis['communities'].items()}

to_graphml(G, communities, 'graphify-out/graph.graphml')
print('graph.graphml written')
"
```

### Step 7d - MCP server (only if --mcp flag)

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -m graphify.serve graphify-out/graph.json
```

### Step 8 - Token reduction benchmark (only if total_words > 5000)

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from graphify.benchmark import run_benchmark, print_benchmark
from pathlib import Path

detection = json.loads(Path('.graphify_detect.json').read_text())
result = run_benchmark('graphify-out/graph.json', corpus_words=detection['total_words'])
print_benchmark(result)
"
```

If `total_words <= 5000`, skip silently.

---

### Step 9 - Save manifest, update cost tracker, clean up, and report

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import json
from pathlib import Path
from datetime import datetime, timezone
from graphify.detect import save_manifest

detect = json.loads(Path('.graphify_detect.json').read_text())
save_manifest(detect['files'])

extract = json.loads(Path('.graphify_extract.json').read_text())
input_tok = extract.get('input_tokens', 0)
output_tok = extract.get('output_tokens', 0)

cost_path = Path('graphify-out/cost.json')
if cost_path.exists():
    cost = json.loads(cost_path.read_text())
else:
    cost = {'runs': [], 'total_input_tokens': 0, 'total_output_tokens': 0}

cost['runs'].append({
    'date': datetime.now(timezone.utc).isoformat(),
    'input_tokens': input_tok,
    'output_tokens': output_tok,
    'files': detect.get('total_files', 0),
})
cost['total_input_tokens'] += input_tok
cost['total_output_tokens'] += output_tok
cost_path.write_text(json.dumps(cost, indent=2))

print(f'This run: {input_tok:,} input tokens, {output_tok:,} output tokens')
print(f'All time: {cost[\"total_input_tokens\"]:,} input, {cost[\"total_output_tokens\"]:,} output ({len(cost[\"runs\"])} runs)')
"
Remove-Item -ErrorAction SilentlyContinue .graphify_detect.json, .graphify_extract.json, .graphify_ast.json, .graphify_semantic.json, .graphify_analysis.json, .graphify_labels.json
Remove-Item -ErrorAction SilentlyContinue graphify-out/.needs_update
```

Tell the user:
```
Graph complete. Knowledge base: KB_NAME
Outputs in ~/.sdw/knowledge_bases/KB_NAME/graphify-out/

  graph.html            - interactive graph, open in browser
  GRAPH_REPORT.md       - audit report
  graph.json            - raw graph data
  obsidian/             - Obsidian vault (only if --obsidian was given)

Tip: query this KB anytime with /sdw-kb --kb KB_NAME query "your question"
     or list all KBs with /sdw-kb list
```

Then paste these sections from GRAPH_REPORT.md directly into the chat:
- God Nodes
- Surprising Connections
- Suggested Questions

Then immediately offer to explore. Pick the single most interesting suggested question and ask:

> "The most interesting question this graph can answer: **[question]**. Want me to trace it?"

---

## For --update (incremental re-extraction)

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -c "
import sys, json
from graphify.detect import detect_incremental, save_manifest
from pathlib import Path

result = detect_incremental(Path('INPUT_PATH'))
new_total = result.get('new_total', 0)
print(json.dumps(result, indent=2))
Path('.graphify_incremental.json').write_text(json.dumps(result))
if new_total == 0:
    print('No files changed since last run. Nothing to update.')
    raise SystemExit(0)
print(f'{new_total} new/changed file(s) to re-extract.')
"
```

If new files exist, check whether all changed files are code files. If code-only: skip semantic extraction. Otherwise: run the full pipeline. Then merge into existing graph and run Steps 4-8.

---

## For --cluster-only

Skip Steps 1-3. Load the existing graph from `graphify-out/graph.json` and re-run clustering, then run Steps 5-9.

---

## For /sdw-kb query, /sdw-kb path, /sdw-kb explain, /sdw-kb add

First resolve the KB directory using the same Path Resolution Rules from Step 0. If `--kb <name>` is given, use that KB. Otherwise derive from the current directory name. The graph file is at `$KB_DIR/graphify-out/graph.json`.

All `python -c` commands use `& $UV_PYTHON -c` where `$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"`.

For **query**: BFS (default) or DFS (`--dfs`) traversal on `$KB_DIR/graphify-out/graph.json`.
For **path**: shortest path between two concepts.
For **explain**: plain-language explanation of a single node and its connections.
For **add**: fetch URL, save to `$KB_DIR/raw/`, then auto-run `--update`.

---

## For --watch

```powershell
$UV_PYTHON = "$(uv tool dir)/graphifyy/Scripts/python"
& $UV_PYTHON -m graphify.watch INPUT_PATH --debounce 3
```

---

## For git commit hook

```powershell
graphify hook install    # install
graphify hook uninstall  # remove
graphify hook status     # check
```

---

## For native CLAUDE.md integration

```powershell
graphify claude install
graphify claude uninstall
```

---

## Honesty Rules

- Never invent an edge. If unsure, use AMBIGUOUS.
- Never skip the corpus check warning.
- Always show token cost in the report.
- Never hide cohesion scores behind symbols - show the raw number.
- Never run HTML viz on a graph with more than 5,000 nodes without warning the user.
