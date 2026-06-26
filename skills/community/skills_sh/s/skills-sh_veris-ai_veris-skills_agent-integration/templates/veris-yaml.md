# `veris.yaml` Annotated Examples

Use these as starting points when generating the final `.veris/veris.yaml`.

## Example 1: HTTP agent with Postgres and Salesforce

```yaml
version: "1.0"

services:
  - name: postgres
    config:
      POSTGRES_PASSWORD: postgres
      SCHEMA_PATH: /agent/db/schema.sql
  - name: salesforce
    dns_aliases:
      - login.salesforce.com
      - test.salesforce.com
      - mock-salesforce.salesforce.com

actor:
  channels:
    - type: http
      url: http://localhost:8080/api/chat
      method: POST
      request:
        message_field: message
        session_field: session_id
      response:
        type: json
        message_field: response

agent:
  code_path: /agent
  entry_point: python -m app.main
  port: 8080
  environment:
    DATABASE_URL: postgresql://postgres:postgres@localhost:5432/SIMULATION_ID
    SALESFORCE_DOMAIN: mock-salesforce
    LOG_LEVEL: info
```

If you use `SCHEMA_PATH: /agent/db/schema.sql`, make sure `.veris/Dockerfile.sandbox` also copies `db/` into `/agent/db/`.

## Example 2: One-shot function agent

```yaml
version: "1.0"

services:
  - name: elastic
    dns_aliases:
      - siem-cluster.es.us-east-1.elastic-cloud.com

actor:
  config:
    MAX_TURNS: "1"
  channels:
    - type: function
      callable: app.handlers:handle_message

agent:
  code_path: /agent
  environment:
    ES_URL: https://siem-cluster.es.us-east-1.elastic-cloud.com
    ES_INDEX: siem-events
```

Notes:
- No `entry_point`
- No `port`
- `MAX_TURNS: "1"` because the callable is one-shot/stateless

## Example 3: Email-driven support agent

```yaml
version: "1.0"

services:
  - name: salesforce
    dns_aliases:
      - login.salesforce.com
      - test.salesforce.com

actor:
  channels:
    - type: email
      agent_inbox: support@email.test
      poll_interval: 15

agent:
  code_path: /agent
  entry_point: uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port 8080
  port: 8080
  environment:
    SALESFORCE_DOMAIN: mock-salesforce
```

## Example 4: Multi-process app with bundled Redis

```yaml
version: "1.0"

services:
  - name: atlassian/jira
    dns_aliases:
      - api.atlassian.com
      - mycompany.atlassian.net

actor:
  channels:
    - type: http
      url: http://localhost:8080/chat

agent:
  code_path: /agent
  entry_point: bash start.sh
  port: 8080
  environment:
    REDIS_URL: redis://localhost:6379/0
    JIRA_BASE_URL: https://mycompany.atlassian.net
```

## Example 5: Voice agent over `voice_ws`

```yaml
version: "1.0"

actor:
  channels:
    - type: voice_ws
      url: ws://localhost:8080/voice
      language: en-US
      wait_for_callee_first: true

agent:
  code_path: /agent
  entry_point: uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port 8080
  port: 8080
  environment:
    LOG_LEVEL: info
```

The agent's framework must speak PCM16/24 kHz/mono over a bare binary WebSocket. If the framework's native transport doesn't match that (e.g., LiveKit Agents, anything WebRTC-only), use `entry_point: bash start.sh` instead and bundle a transport bridge — see [reference/voice-channels.md](../reference/voice-channels.md) and [Pattern 9](../reference/infrastructure-patterns.md#pattern-9-transport-bridge).

## Generation rules

- Use `actor.channels`, not `persona.modality`
- Use `agent_inbox`, not `email_address`
- Use canonical service names (`salesforce`, `google/calendar`, `oracle/fscm`, etc.)
- Only add `actor.config.MAX_TURNS` when the interaction model requires it
- Do not add `RESPONSE_INTERVAL`, `POLL_INTERVAL`, or `REFLECTION_INTERVAL` unless the user explicitly asks for advanced harness tuning
- Omit `agent.entry_point` and `agent.port` for function channels
- Keep secrets out of `veris.yaml`
