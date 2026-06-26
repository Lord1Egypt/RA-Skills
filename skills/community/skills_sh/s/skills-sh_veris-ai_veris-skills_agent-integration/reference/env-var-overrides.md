## Principle

Prefer environment-variable overrides over code changes whenever possible.

Use the current split:

- **Stable non-secret defaults** -> `agent.environment` in `veris.yaml`
- **Secrets and per-environment values** -> `veris env vars set`
- **Local-only convenience** -> root `.env` or shell exports when doing local smoke tests

If the agent already reads a secret directly by name (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.), prefer `veris env vars set` and do not duplicate that key in `veris.yaml`.

## Docker hostnames -> localhost

When the repo currently relies on docker-compose service names, rewrite them to localhost within the Veris container:

| Original | Veris override |
| --- | --- |
| `REDIS_HOST=redis` | `REDIS_HOST=localhost` |
| `REDIS_URL=redis://redis:6379/0` | `REDIS_URL=redis://localhost:6379/0` |
| `DATABASE_URL=postgresql://user:pass@postgres:5432/mydb` | `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/SIMULATION_ID` |
| `ELASTICSEARCH_URL=http://elasticsearch:9200` | `ELASTICSEARCH_URL=http://localhost:9200` |
| `AMQP_URL=amqp://guest:guest@rabbitmq:5672` | `AMQP_URL=amqp://guest:guest@localhost:5672` |
| `KAFKA_BOOTSTRAP_SERVERS=kafka:9092` | `KAFKA_BOOTSTRAP_SERVERS=localhost:9092` |
| `MINIO_ENDPOINT=minio:9000` | `MINIO_ENDPOINT=localhost:9000` |

## Mock-service credentials

### Salesforce

Use:
- `SALESFORCE_DOMAIN=mock-salesforce`
- `SALESFORCE_USERNAME=mock_user@simulation.test`
- `SALESFORCE_CONSUMER_KEY=mock_consumer_key_12345`
- `SALESFORCE_CONSUMER_SECRET=mock_consumer_secret_67890`

### Google Calendar / Drive / Docs

Use:
- `GOOGLE_APPLICATION_CREDENTIALS=/certs/mock-service-account.json`

### Slack

Use:
- `SLACK_BOT_TOKEN=xoxb-mock-token-for-veris-simulation`
- `SLACK_SIGNING_SECRET=mock-signing-secret`

### Postgres

Use:
- `DATABASE_URL=postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/SIMULATION_ID`

### Jira / Confluence

Usually keep the agent’s existing Atlassian base URL and let DNS interception route it:
- `https://mycompany.atlassian.net`

## LLM providers

The LLM proxy handles supported providers automatically.

Usually you only need to set the real provider key with:

```bash
veris env vars set OPENAI_API_KEY=sk-... --secret
```

or:

```bash
veris env vars set ANTHROPIC_API_KEY=sk-ant-... --secret
```

No `services:` entry is needed for the provider itself.

## Optional services

If the repo imports SDKs for observability or optional tooling that are not critical to user-facing behavior, prefer disable flags over code changes when possible:

- `DD_TRACE_ENABLED=false`
- `SENTRY_DSN=""`
- `NEW_RELIC_LICENSE_KEY=""`

If the agent still crashes without the service, then it is not optional and must be mocked, bundled, or kept external.

## `veris env vars set` vs `agent.environment`

Use `agent.environment` for:
- stable local URLs
- non-secret defaults
- values that need `${VAR}` or `${SIMULATION_ID}` expansion

Use `veris env vars set` for:
- secrets
- environment-specific URLs
- values that differ between dev/staging/prod

Platform env vars set with `veris env vars set` take precedence over `agent.environment`.

## Special values in `veris.yaml`

- `${VAR_NAME}` -> expanded from runtime env
- `${SIMULATION_ID}` -> expanded from the simulation context when supported in the value
- `SIMULATION_ID` in database URLs is also commonly used literally

For local runs, a root `.env` file or exported shell variables can still be useful, but do not generate `.env.simulation`.
