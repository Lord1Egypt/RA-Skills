---
name: skill-for-ragflow
description: Operate RAGFlow v0.27.3 deployments through a bundled Node CLI for everyday knowledge-base setup, document ingestion, parsing, retrieval, chat assistants, agents, GraphRAG, connectors, models, embedded website access, system-token listing/creation/deletion, and diagnostics. Use when a request explicitly involves a RAGFlow server, dataset, document pipeline, or RAGFlow agent.
metadata:
  openclaw:
    requires:
      bins:
        - node
      env:
        - RAGFLOW_URL
        - RAGFLOW_API_KEY
    primaryEnv: RAGFLOW_API_KEY
    homepage: https://github.com/LunarCache/ragflow-skill
---

# RAGFlow Skill

Operate common RAGFlow v0.27.3 workflows through `node {baseDir}/scripts/ragflow.js <command> [options]`. Prefer `--json` when parsing or chaining results. Prioritize daily operations over exhaustive API coverage.

This package targets v0.27.3 and accepts only current API parameters. Use `--knn-top-k` for retrieval and `--session` for chat; no deprecated aliases or legacy streaming mode are supported. Treat `-rc`, alpha, beta, and nightly releases as separate targets; GitHub may label a release candidate as `latest`. Check `system-version` before using this skill with a newly upgraded deployment.

## Requirements

- Set `RAGFLOW_URL` and `RAGFLOW_API_KEY` in the process environment.
- Use Node.js to run bundled scripts.
- Run `system-health --json` after first-time setup to verify service reachability and dependencies. Run `system-version --json` to identify the deployment version. Use `list-datasets --page-size 1 --json` to verify API-key authentication.

## Security Notes

- **Administrative scope.** This skill can read and change the configured RAGFlow tenant, configure model-provider credentials, and list/create/delete system tokens used for shared-site embedding. Run these operations only within the user's authorized scope. `embed-code` can create a system token when none exists; token deletion requires explicit destructive confirmation.
- **Environment, network, and files.** Node scripts read `RAGFLOW_URL` and `RAGFLOW_API_KEY`, optional `RAGFLOW_PROVIDER_API_KEY`, and documented RAGFlow retry/diagnostic settings. They send authenticated requests to the configured RAGFlow server; server-side provider/connector actions may contact configured external services. Local reads include selected uploads, JSON/config/key files; downloads write only to a requested output path. These are capability disclosures, not host permission grants. The skill does not inspect SSH, cloud-provider, or unrelated application credentials.

- **Use HTTPS in production.** Production deployments should use `https://` for `RAGFLOW_URL` to protect the API key in transit. Local development (`http://localhost`) is acceptable for testing.
- **Use a dedicated, rotatable API key for automation.** RAGFlow v0.27.3 API keys are tenant-scoped rather than permission-scoped.
- **Protect your API key.** Never share `RAGFLOW_API_KEY` in chat messages or commit it to version control. Use process environment variables supplied by the host.

## Quick Command Reference

| Scenario | Commands |
|----------|----------|
| **Knowledge base setup** | `create-dataset`, `list-datasets`, `get-dataset`, `update-dataset`, `delete-datasets` |
| **Document ingestion** | `upload-documents`, `ingest-documents`, `list-documents`, `get-document`, `update-document`, `delete-documents`, `download-document`, `preview-document`, `metadata-summary`, `update-metadata` |
| **Parsing & chunking** | `start-parsing`, `stop-parsing`, `wait-parsing`, `list-chunks`, `get-chunk`, `add-chunk`, `update-chunk`, `delete-chunks`, `get-document-graph`, `delete-document-graph` |
| **Direct retrieval** | `retrieve` |
| **Chat assistant** | `create-chat`, `list-chats`, `get-chat`, `update-chat`, `patch-chat`, `delete-chats` |
| **Chat sessions** | `create-session`, `list-sessions`, `get-session`, `update-session`, `delete-sessions`, `chat`, `chat-session` |
| **Agent** | `create-agent`, `list-agents`, `get-agent`, `update-agent`, `delete-agents` |
| **Agent Tags** | `list-agent-tags`, `update-agent-tags` |
| **Agent sessions** | `create-agent-session`, `list-agent-sessions`, `delete-agent-sessions`, `agent-chat` |
| **Connector** | `list-connectors`, `create-connector`, `get-connector`, `update-connector`, `delete-connector` |
| **RAPTOR** | `run-raptor`, `trace-raptor` |
| **GraphRAG** | `get-knowledge-graph`, `delete-knowledge-graph`, `run-graphrag`, `trace-graphrag` |
| **Embedded website access** | `list-system-tokens`, `create-system-token`, `delete-system-token`, `embed-code`, `embed-info`, `embed-chat`, `embed-agent-chat` |
| **Model discovery** | `list-models`, `list-added-models`, `list-default-models`, `set-default-model` |
| **Model providers** | `list-providers`, `get-provider`, `add-provider`, `delete-provider`, `list-provider-models`, `list-provider-instances`, `get-provider-instance`, `create-provider-instance`, `delete-provider-instances`, `verify-provider`, `list-instance-models`, `add-instance-model`, `set-model-status` |
| **System** | `system-version`, `system-health`, `get-log-levels`, `set-log-level` |

## Common Workflows

### Full RAG pipeline (upload -> parse -> retrieve)

1. `create-dataset --name "My KB" --chunk-method naive`
2. `upload-documents --dataset <id> --files ./doc1.pdf ./doc2.txt`
3. `start-parsing --dataset <id> --doc-ids <doc_id1> <doc_id2> --confirm-destructive`
4. `wait-parsing --dataset <id> --doc-ids <doc_id1> <doc_id2>`
5. `retrieve --question "What is X?" --datasets <id>`

### Chat assistant with sessions

1. `create-chat --name "Q&A" --datasets <id> --llm-id qwen-turbo@Tongyi-Qianwen`
2. `create-session --chat <chat_id>`
3. `chat-session --chat <chat_id> --session <session_id> --question "Hello"`

### Agent workflow

1. `create-agent --title "Assistant" --dsl @agent_dsl.json`
2. `create-agent-session --agent <agent_id>`
3. `agent-chat --agent <agent_id> --session <session_id> --question "Hello"`

`agent-chat` streams by default. Use `--stream false` for one final JSON response.

### Connector workflow

1. `create-connector --config @connector.json`
2. `list-connectors`
3. `get-connector --id <id>`

### Model provider workflow (v0.27.3)

1. `list-providers --available` to see configurable providers
2. `add-provider --name <provider>`
3. Set `RAGFLOW_PROVIDER_API_KEY`, then run `create-provider-instance --name <provider> --instance <name>` (credentials live on an instance; a provider can have several)
4. `add-instance-model --name <provider> --instance <name> --model-name <model> --model-type chat`
5. `set-default-model --model-type chat --model-provider <provider> --model-instance <name> --model-name <model>`

Use `verify-provider --name <provider>` with `RAGFLOW_PROVIDER_API_KEY` set, or pass `--api-key-file <path>`, to test a key without persisting an instance.

### Indexing and retrieval

Run `run-raptor --dataset <id>` then `trace-raptor --dataset <id>`, or the equivalent `run-graphrag` / `trace-graphrag` commands. Retrieval uses `--knn-top-k`; when paginating, set `--rerank-candidates-count` to cover `--page × --top-n`. Read the command reference for server defaults and filtering.

### Embedded website access

1. `embed-code --chat <chat_id> --type fullscreen` or `embed-code --agent <agent_id> --type widget`
2. `embed-info --chat <chat_id>` or `embed-info --agent <agent_id>`
3. `embed-chat --chat <chat_id> --question "Hello"` or `embed-agent-chat --agent <agent_id> --question "Hello"`

`embed-chat` automatically creates the embedded chatbot session when `--session` is omitted. RAGFlow's shared-site route only creates a session and returns the prologue on the first no-session request, so the CLI bootstraps `session_id` first and then sends the real question.

## Workflow Decision Guide

The first step in any RAGFlow operation is resolving the target resource ID. After that, choose the right path:

1. **Authoring or debugging a custom agent DSL?** -> Read [references/AGENT_GUIDE.md](references/AGENT_GUIDE.md) - it is a self-contained guide to the current RAGFlow agent DSL schema and includes minimal examples.
2. **Need CLI syntax or option details?** -> Read [references/COMMANDS.md](references/COMMANDS.md) - it's organized by workflow scenario with full option tables.
3. **Editing client code or checking request/response shapes?** -> Read [references/API.md](references/API.md) - it has examples for supported `RagflowClient` workflows.
4. **A command failed?** -> Read [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - common errors with causes and fixes.
5. **Formatting output for the user?** -> Read [references/REFERENCE.md](references/REFERENCE.md) - consistent response templates and status labels.

## Key Constraints

- **Confirm destructive scope.** Verify that the user authorized the exact target before starting/stopping parsing (both clear existing chunks), deletion, metadata removal or dataset-wide metadata changes, or ingestion that purges existing tasks/chunks. Then pass `--confirm-destructive` for that invocation; the CLI otherwise refuses the request. Existing explicit authorization and cleanup of temporary resources from the requested workflow do not require a repeated question. Never add the flag automatically in response to a refusal.
- **Choose the ingestion path first.** For built-in chunking, upload documents, adjust their parser configuration when needed, then run `start-parsing`. For ingestion-pipeline datasets, use `ingest-documents` instead.
- **Preserve source filenames.** When an attachment is stored under a temporary or task-generated path, upload it as `--files <original-name>=<path>` so RAGFlow retains the user-facing name.
- **Resolve complete, stable inputs.** Discover resource IDs with the corresponding `list-*` or `get-*` command, and paginate beyond RAGFlow's 100-item list limit. Use the `identifier` from `list-models` (`<model>@<instance>@<provider>`, or `<model>@<provider>` for the default instance) for `--embedding-model` and `--llm-id`; treat numeric model row IDs as display data only.
- **Preserve session-history intent.** Let `chat-session` append the latest user message by default. Use `--pass-all-history` only when replacing stored history.
- **Protect operational secrets.** Keep `RAGFLOW_API_KEY`, provider keys, system tokens, beta values, and embed URLs containing `auth=` out of user-facing output. Supply provider credentials through `RAGFLOW_PROVIDER_API_KEY` or `--api-key-file`; reveal secret material only when the user explicitly requests copy-paste output.
- **Use the correct public embed origin.** Pass `--origin` when the browser-facing RAGFlow URL differs from `RAGFLOW_URL`. Let the CLI reuse or create a beta token and bootstrap the embedded chat session.
- **Start Agent DSL work from the guide.** Read [references/AGENT_GUIDE.md](references/AGENT_GUIDE.md) before authoring or debugging agents, and adapt its minimal examples instead of reconstructing the canvas schema from memory.

## Output Format

Use raw `--json` internally, then summarize the operational result. Preserve the server's parsing labels (`UNSTART`, `RUNNING`, `CANCEL`, `DONE`, `FAIL`) and similarity scores. Redact API keys, system tokens, beta values, and `auth=` query values unless the user explicitly requests copy-paste secret material. Read [references/REFERENCE.md](references/REFERENCE.md) only when a result needs a domain-specific response template.
