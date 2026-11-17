# Frozen regression samples — env governance (open-source edition)

Expected classification (clawhub profile, all must hold). The open-source
`config/env_contracts.json` ships with an **empty** `runtimeInjected` list
(platform-neutral; platform-specific injections belong in downstream forks),
so `fixture_runtime.py` variables are expected to classify as
`ENV_REQUIRED_UNDECLARED` (no runtime contract to exempt them). Once a
downstream fork declares them in `runtimeInjected`, they classify as
`ENV_RUNTIME_INJECTED` and stop warning. Everything else matches the
internal edition.

| fixture | variable | expected code | visible |
|---|---|---|---|
| fixture_optional.py | OPENCLAW_WORKSPACE | ENV_OPTIONAL_OVERRIDE | no |
| fixture_optional.py | SKILL_RELEASE_HUB_BASE | ENV_OPTIONAL_OVERRIDE | no |
| fixture_optional.py | SRP_TIMEOUT | ENV_OPTIONAL_OVERRIDE | no |
| fixture_required.py | API_TOKEN | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_required.py | DB_URL | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_runtime.py | MULTICA_AGENT_ID | ENV_REQUIRED_UNDECLARED (empty contract; RUNTIME_INJECTED once declared) | WARN |
| fixture_runtime.py | MULTICA_TASK_ID | ENV_REQUIRED_UNDECLARED (empty contract; RUNTIME_INJECTED once declared) | WARN |
| fixture_runtime.py | MULTICA_AGENT_NAME | ENV_REQUIRED_UNDECLARED (empty contract; RUNTIME_INJECTED once declared) | WARN |
| fixture_js.js | API_URL | ENV_OPTIONAL_OVERRIDE | no |
| fixture_js.js | API_TOKEN_JS | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_js.js | BRACKET_VAR | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_sh.sh | SRP_OUTPUT_DIR | ENV_OPTIONAL_OVERRIDE | no |
| fixture_sh.sh | MUST_HAVE_VAR | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_sh.sh | PLAIN_VAR | ENV_REQUIRED_UNDECLARED | WARN |
| fixture_comment.py (tests/) | * | (never scanned — test path) | no |

## v1.2 additions — JS env data-flow (declared-unused governance)

| fixture | variable | expected code | visible |
|---|---|---|---|
| fixture_js_dataflow.mjs | MULTICA_PROFILE | ENV_DECLARED_INDIRECT | no (evidence only) |
| fixture_js_dataflow.mjs | USAGE_LOOKBACK_DAYS | ENV_DECLARED_INDIRECT | no (evidence only) |
| fixture_js_dataflow.mjs | USAGE_SNAPSHOT_PATH | ENV_DECLARED_INDIRECT | no (evidence only) |
| fixture_js_dataflow_neg.mjs | (all) | NOT tracked (plain object / non-env parse / non-env call arg) | — |

Contract changes (config/env_contracts.json) MUST re-run this suite + changelog entry.
