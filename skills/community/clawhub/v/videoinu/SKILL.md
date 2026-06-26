---
name: videoinu
version: "1.0.0"
description: "Videoinu platform skill — manage projects via Graphs (canvases), upload/download files, chat with AI Agents, and run Workflows. Use when: user mentions Videoinu, Graph management, uploading files to Videoinu, agent chat on Videoinu, or running Videoinu workflows."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3"] },
      },
  }
---

# videoinu-skill

> Videoinu platform skill — manage projects via Graphs (canvases), upload/download files, chat with AI Agents, and run Workflows.

## Important: How to Use

**You MUST use the Python scripts provided by this skill to interact with Videoinu. Do NOT use mcporter, MCP, curl, or any other method to call the API directly.**

All scripts are located in the `scripts/` directory of this skill. Tokens are stored in `~/.videoinu/credentials.json` and scripts read them automatically.

Example: to list projects, run `python3 <skill_scripts_dir>/list_graphs.py` — do not construct HTTP requests manually.

## Overview

videoinu-skill provides a set of Python scripts for interacting with the Videoinu platform. It covers the following core capabilities:

1. **Graph Management** — Create, list, and view Graphs (project canvases) along with their ViewNodes / CoreNodes
2. **File Upload/Download** — Upload local files to the platform (creating CoreNodes) or download files from a Graph
3. **Agent Chat** — Create Agent sessions and chat with AI Agents via WebSocket
4. **Workflow Execution** — Run Workflow definitions and query execution status

### Requirements

- **Binary**: `python3` (3.9+)
- **Environment variable**: `VIDEOINU_ACCESS_KEY` (required)
- **Optional environment variable**: `VIDEOINU_API_BASE` (defaults to `https://videoinu.com`)
- **No third-party dependencies**: all scripts use only the Python standard library

### Authentication

All requests use Cookie-based authentication: `Cookie: token=<VIDEOINU_ACCESS_KEY>`

### Obtaining and Saving the Access Key

How to obtain your Access Key:
1. Log in at https://videoinu.com
2. Go to Profile page → click **Copy Access Key**

Saving the Access Key (choose one):

**Option A: Save locally with auth.py (recommended)**
```bash
python3 auth.py save "your-access-key"
# Token saved to ~/.videoinu/credentials.json (owner read/write only)
# All scripts will auto-read it — no environment variable needed
```

**Option B: Environment variable**
```bash
export VIDEOINU_ACCESS_KEY="your-access-key"
```

Token resolution priority: environment variable > `~/.videoinu/credentials.json`

Verify and manage:
```bash
python3 auth.py status   # Show current auth status
python3 auth.py verify   # Verify token validity
python3 auth.py logout   # Remove saved token
```

If the user is not yet logged in, direct them to https://videoinu.com/login to sign up / log in and obtain their key.

**Security warning**: Never hardcode the Access Key into script files. The Access Key is a JWT token containing user identity information — leaking it could lead to account compromise. Use `auth.py save` or environment variables.

---

## Script Reference

| Script | Function | Input | Output |
|--------|----------|-------|--------|
| `auth.py` | Save/verify/manage Access Key | `save`/`status`/`verify`/`logout` | Auth status |
| `list_graphs.py` | List user's Graphs | `--page-size`, `--tag` | Graph list |
| `get_graph.py` | View Graph details (ViewNode + CoreNode) | `GRAPH_ID` | Filtered node info |
| `create_graph.py` | Create a new Graph | `NAME`, `--tag` | Graph ID + URL |
| `upload_file.py` | Upload a file to create a CoreNode | File path | CoreNode ID + URL |
| `download_file.py` | Download files from a Graph | `GRAPH_ID` or `--urls` | Local file paths |
| `create_session.py` | Create an Agent session | `GRAPH_ID`, `--list` | Session ID |
| `agent_chat.py` | Chat with an Agent | `SESSION_ID`, message | Agent reply |
| `run_workflow.py` | Run a Workflow | `DEFINITION_ID`, inputs | Instance ID |
| `query_workflow.py` | Query Workflow status | `INSTANCE_ID`, `--poll` | Execution status |

---

## Core Concepts

### Graph (Canvas / Project)
A Graph is Videoinu's project container. It contains:
- **ViewNode**: A visual node on the canvas with position, labels, and connections
- **CoreNode**: An underlying data node representing an actual asset (image, video, audio, text) or operation (Workflow output)
- **Connection**: A link between ViewNodes representing data flow
- **Group**: A grouping of ViewNodes

Each ViewNode can reference one or more CoreNodes (`core_refs`), with `selected_core_id` indicating the currently selected version.

### CoreNode Types
- `asset`: Asset node
  - `asset_type`: `image` | `video` | `audio` | `text` | `json` | `file`
  - `source_type`: `upload` | `import` | `generated`
  - Has `url` (media file) or `content` (text content)
- `operation`: Operation node (Workflow execution output)
  - `status`: `pending` | `completed` | `failed`

### Agent Sessions
An Agent is an AI assistant bound to a Graph. It communicates via WebSocket in real time.
- One Graph maps to one Agent Project
- One Project can have multiple Sessions
- Agents can invoke Tools to operate on nodes within the Graph

### Workflow
A predefined automation pipeline that accepts inputs (CoreNode references) and produces new CoreNodes.

---

## Typical Workflows

### Scenario 1: Browse User Projects

```bash
# 1. List all Graphs
python3 list_graphs.py

# 2. View details of a specific Graph
python3 get_graph.py GRAPH_ID
```

### Scenario 2: Create a New Project and Upload Files

```bash
# 1. Create a new Graph (auto-tagged with free-mode so it appears in the UI)
python3 create_graph.py "My New Project"
# → returns graph_id

# 2. Upload a reference file
python3 upload_file.py /path/to/reference.png
# → returns core_node_id, file_url

# 3. Verify the Graph
python3 get_graph.py GRAPH_ID
```

### Scenario 3: Chat with an Agent

```bash
# 1. Create a session
python3 create_session.py GRAPH_ID
# → returns session_id

# 2. Send a message
python3 agent_chat.py SESSION_ID "Analyze the structure of this project"

# 3. Send a message with a file reference
python3 agent_chat.py SESSION_ID "Check this image {{@core_node:CORE_NODE_ID:image.png}}"

# 4. List existing sessions
python3 create_session.py GRAPH_ID --list
```

### Scenario 4: Upload a File and Have the Agent Process It

```bash
# 1. Upload the file
python3 upload_file.py /path/to/video.mp4
# → core_node_id = "abc123"

# 2. Create a session (if you don't have one yet)
python3 create_session.py GRAPH_ID
# → session_id = "sess456"

# 3. Ask the Agent to process the file
python3 agent_chat.py sess456 "Please edit this video {{@core_node:abc123:video.mp4}}" --auto-approve
```

### Scenario 5: Run a Workflow

```bash
# 1. List available Workflow definitions
python3 run_workflow.py --list

# 2. Run within an existing Graph
python3 run_workflow.py DEF_ID --graph-id GRAPH_ID \
  --inputs '{"input_image": {"type": "core_node_refs", "core_node_ids": ["NODE_ID"]}}'
# → returns instance_id

# 3. Poll execution status until complete
python3 query_workflow.py INSTANCE_ID --poll
```

### Scenario 6: Download Generated Results from a Graph

```bash
# Download all images from the Graph
python3 download_file.py GRAPH_ID --type image --output-dir ./results

# Download all videos
python3 download_file.py GRAPH_ID --type video

# Download specific URLs directly
python3 download_file.py --urls "https://..." "https://..." --output-dir ./output
```

---

## Agent Reference Format

You can reference nodes in a Graph within messages sent to the Agent:

```
{{@core_node:CORE_NODE_ID:display_name}}
{{@view_node:VIEW_NODE_ID:display_name}}
```

Example:
```
Please analyze this image {{@core_node:a1b2c3d4:sunset.png}}
```

The Agent will fetch the corresponding CoreNode content based on the reference.

---

## Output Format

All scripts output JSON to stdout and errors to stderr.

**Success**:
```json
{
  "graphs": [...],
  "has_more": false
}
```

**Error**:
```json
{
  "error": "VIDEOINU_ACCESS_KEY is not set. Run: export VIDEOINU_ACCESS_KEY=\"your-access-key\""
}
```

---

## Core Principles

1. **Faithfully convey user intent**: Pass the user's request to the Agent as-is — do not embellish, translate, or rewrite the prompt
2. **Look before you leap**: Use `get_graph.py` to understand the current state of a Graph before performing operations
3. **Reference, don't describe**: When referring to existing files, use `{{@core_node:ID:name}}` references instead of text descriptions
4. **Upload first**: If the user provides a local file, upload it with `upload_file.py` first, then reference it in messages
5. **Poll responsibly**: Both Workflow and Agent responses have timeout limits — do not poll indefinitely

---

## API Endpoint Reference

All HTTP endpoints are based on `VIDEOINU_API_BASE` (defaults to `https://videoinu.com`).

### Go Backend (`/api/backend/`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/graph/list` | List Graphs |
| POST | `/graph` | Create a Graph |
| GET | `/graph/:id` | Get Graph details |
| DELETE | `/graph/:id` | Delete a Graph |
| POST | `/core_nodes/upload/presign` | Get a pre-signed upload URL |
| POST | `/core_nodes` | Create CoreNodes (batch) |
| GET | `/core_nodes/assets_v2` | List asset CoreNodes |
| POST | `/wf/instance/run_in_graph` | Run a Workflow in a Graph |
| POST | `/wf/instance/run_create_graph` | Run a Workflow and create a Graph |
| GET | `/wf/instance/:id/status_sse` | Workflow status SSE |
| GET | `/wf/definition/list` | List Workflow definitions |

### Agent Service (`/api/agent/`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/by-graph/:graphId` | Get Agent Project by Graph ID |
| POST | `/projects/` | Create an Agent Project |
| GET | `/sessions/by-project/:projectId` | List sessions for a Project |
| POST | `/sessions/` | Create a session |
| DELETE | `/sessions/:sessionId` | Delete a session |
| WS | `/sessions/:sessionId/stream` | WebSocket Agent session stream |

### WebSocket Message Format (JSON-RPC 2.0)

**Send prompt**:
```json
{"jsonrpc": "2.0", "method": "prompt", "id": "uuid", "params": {"user_input": "message"}}
```

**Heartbeat**:
```json
{"jsonrpc": "2.0", "method": "heartbeat", "id": "hb-uuid", "params": {"heartbeat_id": "uuid"}}
```

**Approve tool call**:
```json
{"jsonrpc": "2.0", "id": "rpc-id-from-request", "result": {"request_id": "req-id", "response": "approve"}}
```

**Received event types**: `TurnBegin`, `ContentPart`, `ToolCall`, `ToolCallPart`, `ToolResult`, `ApprovalRequest`, `StatusUpdate`, `SessionNotice`, `ReplayComplete`
