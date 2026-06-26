# Runtime Env Var Template

Use this template when deciding what belongs in `agent.environment` versus `veris env vars set`.

## Preferred split

### 1. Stable non-secret defaults -> `agent.environment`

Examples:

```yaml
agent:
  environment:
    LOG_LEVEL: info
    DATABASE_URL: postgresql://postgres:postgres@localhost:5432/SIMULATION_ID
    SALESFORCE_DOMAIN: mock-salesforce
```

### 2. Secrets and per-environment values -> `veris env vars set`

Examples:

```bash
veris env vars set OPENAI_API_KEY=sk-... --secret
veris env vars set ANTHROPIC_API_KEY=sk-ant-... --secret
veris env vars set SALESFORCE_CONSUMER_KEY=... --secret
veris env vars set SALESFORCE_CONSUMER_SECRET=... --secret
veris env vars set LOG_LEVEL=debug
```

### 3. Optional local-only convenience -> root `.env`

For local smoke tests or `veris run local`, it can still be useful to mirror values in a root `.env` file or export them in the shell. This is optional and should not replace the platform env-var flow.

## Common categories

### LLM provider keys

Usually set with:

```bash
veris env vars set OPENAI_API_KEY=sk-... --secret
```

Do not generate a `.env.simulation` file for this.

### Mock credentials

If the mock expects stable fake credentials, those are often fine in `agent.environment`.

Examples:
- `SALESFORCE_DOMAIN=mock-salesforce`
- `SLACK_BOT_TOKEN=xoxb-mock-token-for-veris-simulation`

### External endpoints

If the user keeps a dependency external, prefer:

```bash
veris env vars set PINECONE_API_KEY=... --secret
veris env vars set PINECONE_ENVIRONMENT=us-east-1
veris env vars set KAFKA_BOOTSTRAP_SERVERS=broker.example.com:9092
```

## Rule of thumb

- If the value is safe to commit and stable across environments, it can live in `agent.environment`
- If the value is sensitive or environment-specific, use `veris env vars set`
- If the app already reads a secret directly by name, do not duplicate it in `veris.yaml`
