# OpenAPI custom tools

Resolve `<PYTHON>` to an available Python 3 interpreter and `<SKILL_DIR>` to this Skill's absolute directory. Wrapped POSIX examples show argument grouping; adapt continuation characters to the current shell.

## Preference order

1. Standard SDK metadata read (`getToolProviders`) when available.
2. Standard `smartbi` CLI operations discovered through `list`/`describe`.
3. Source-confirmed internal SmartBI internal APIs when the standard surface is missing.
4. Browser/HAR evidence only to confirm an uncovered contract; never replay credentials from a HAR.

## Internal contracts

The following internal routes are source-confirmed under `/smartbi/smartbix/api/dataagent/tools`:

| Action | Method and path | Notes |
| --- | --- | --- |
| Parse without saving | `POST /parse?type=OPENAPI` | Request body is the OpenAPI text |
| List | `POST /list` | Read-only metadata |
| Get by name | `GET /getByName?name=...` | Returns definition and tools |
| Execute | `POST /execute` | Remote tool side effects depend on the OpenAPI operation |
| Create | `POST /create` | Write; no automatic retry |
| Update | `POST /update` | Recreates all Tool IDs |
| Delete | `POST /delete?id=...` | Destructive; not automated by this skill |

Use the included read/parse commands:

```bash
<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  provider-list --output <PROVIDERS_JSON>

<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  provider-get --name '<PROVIDER_NAME>' --output <PROVIDER_JSON>

<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  provider-parse --openapi-file <OPENAPI_YAML> --output <PARSED_JSON>
```

Provider writes are intentionally not automated by the bundled script. When a write is authorized, save the current Provider definition, parse the candidate first, call create/update exactly once, read it back, obtain the new Tool IDs, rebind affected Agent nodes, and run a fresh conversation.

## Reliable OpenAPI subset

- OpenAPI 3 with exactly one `servers` entry;
- operations limited to `GET`, `POST`, `PUT`, and `DELETE`;
- each operation has `operationId` and an explicit `200` response;
- request body uses a simple inline object where possible;
- one content type, preferably `application/json`;
- top-level flat parameters for workflow-node compatibility;
- no dependence on `default` response, `2XX` wildcard, or deep `$ref` chains.

Current SmartBI versions may emit request-body parameter metadata with `name` but no stable `id`. A Provider saving successfully therefore does not prove ReAct can pass parameters. Use a workflow node with explicit named inputs until a real read-back and conversation test proves parameter IDs are valid.

Updating a Provider deletes and recreates all of its Tool records. Any Agent node bound by Tool ID may become stale even if the Provider ID and name remain unchanged.

## Server-side safety

For read-only planning, validation, or governance tools, enforce non-execution on the remote server. Do not depend on prompts, an OpenAPI `default: false`, or the LLM to keep an execution switch disabled. Test false values as emitted by the actual SmartBI UI; some builds serialize a checkbox as `"[false]"`.
