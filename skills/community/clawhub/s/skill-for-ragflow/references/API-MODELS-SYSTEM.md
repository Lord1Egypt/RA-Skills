# Model providers and server configuration (v0.27.3)

[API overview](API.md)

## LLM Models

```javascript
// List available models (v0.27.3 flat tenant model catalog)
const models = await client.listModels({ type: "chat" });
// GET /api/v1/models -> [{ name, model_type, provider_name, model_id, ... }]
// Client returns the server catalog array; CLI list-models groups it as { groups, total }.
```

RAGFlow v0.27.3 exposes model discovery at `/api/v1/models` (replacing the legacy `/v1/llm/my_llms`, which was removed in v0.27.0). Authentication uses `RAGFLOW_API_KEY`. There is no legacy endpoint fallback; `listModelsLegacy()` has been removed.

Use `identifier` from CLI `list-models`, including `<model>@<instance>@<provider>` for a named instance. For the default instance, use model names plus provider suffixes when creating resources, for example `qwen-turbo@Tongyi-Qianwen` for `llm_id` and `text-embedding-v4@Tongyi-Qianwen` for `embedding_model`. Some deployments return numeric `id` fields; those are server row IDs and should not be sent as `llm_id`.

## Tenant Models (v0.27.3)

These methods use the `/api/v1/models` routes and authenticate with `RAGFLOW_API_KEY`.

```javascript
// List the tenant's added models, optionally filtered by type
const added = await client.listAddedModels({ type: "chat" });
// GET /api/v1/models?type=chat -> [{ name, model_type, provider_name, ... }]

// List the tenant's default models
const defaults = await client.listDefaultModels();
// GET /api/v1/models/default -> { default_models: [...] }

// Set (or clear) the default model for a type
await client.setDefaultModel({
  model_type: "chat",          // required: chat | embedding | rerank | asr | vision | tts | ocr
  model_provider: "OpenAI",    // omit provider/instance/name to clear the default
  model_instance: "default",
  model_name: "gpt-4o",
});
// PATCH /api/v1/models/default
```

## Model Providers (v0.27.3)

RAGFlow v0.27.3 provides provider/instance/model management under `/api/v1/providers`. All methods authenticate
with `RAGFLOW_API_KEY`. Path segments are URL-encoded, so model identifiers containing `@` or `/` are handled
automatically.

In v0.27.3, each provider instance supports `PUT` and `GET` on `/instances/{instance_id_or_name}` for updating a
single instance's credentials; the CLI uses `GET /instances` to list and `POST /instances` to create.

```javascript
// List configured providers, or system-available providers with { available: true }
await client.listProviders({ available: true });        // GET /api/v1/providers?available=true
await client.getProvider("OpenAI");                      // GET /api/v1/providers/OpenAI
await client.addProvider("OpenAI");                      // PUT /api/v1/providers { provider_name }
// Removing a configured provider requires separately authorized scope.
await destructiveClient.deleteProvider(providerName);

// Discover a provider's models (some providers fetch a live list from the remote API)
await client.listProviderModels("OpenAI", { api_key: "sk-...", base_url: "" });

// Instances hold a set of credentials (multiple API keys per provider are supported)
await client.listProviderInstances("OpenAI");
await client.getProviderInstance("OpenAI", "default");
await client.createProviderInstance("OpenAI", {
  instance_name: "default",    // required
  api_key: "sk-...",           // required
  base_url: "",
  region: "",
  model_info: [],
});                                                       // POST /api/v1/providers/OpenAI/instances
await destructiveClient.deleteProviderInstances("OpenAI", ["default"]);

// Test a provider connection / API key without persisting an instance
await client.verifyProvider("OpenAI", { api_key: "sk-...", base_url: "", region: "default" });

// Manage the models on an instance
await client.listInstanceModels("OpenAI", "default", { supported: true });
await client.addInstanceModel("OpenAI", "default", {
  model_name: "gpt-4o",        // required
  model_type: "chat",          // required
  max_tokens: 8192,
  extra: {},
});
await client.setInstanceModelStatus("OpenAI", "default", "gpt-4o", "enable"); // PATCH .../models/<name>
```

Treat `api_key` values as sensitive: pass them in, but do not echo them back to the user.

## System

```javascript
// Get the server version
const version = await client.getSystemVersion();

// Check service health
const health = await client.getSystemHealth();

// Inspect and update log levels
const levels = await client.getLogLevels();
await client.setLogLevel("ragflow", "DEBUG");
```

`getSystemHealth()` handles RAGFlow's raw health JSON rather than the usual `{ code, data }` envelope. The health route checks reachability and server dependencies; use `validateConnection()` or an authenticated resource command to verify the API key.

## Utility

```javascript
// Validate connection to RAGFlow server
const ok = await client.validateConnection();
// Returns: true | false
```

## Configuration

Set the following environment variables to configure the API client:
```bash
export RAGFLOW_URL=https://your-ragflow-instance.com
export RAGFLOW_API_KEY=ragflow-xxxxx
```

`RAGFLOW_URL` should be the server root, for example `http://127.0.0.1:9380`. Bare hosts such as `localhost:9380` are normalized to `http://localhost:9380`. The client adds `/api/v1` for REST endpoints, including model discovery.

### Security Best Practices

- **Production: Use HTTPS.** Set `RAGFLOW_URL=https://...` for production deployments to protect the API key in transit.
- **Dedicated keys.** Use a dedicated, rotatable automation key; RAGFlow API keys are tenant-scoped rather than permission-scoped.
- **Protect secrets.** Never commit `RAGFLOW_API_KEY` to version control. Use process environment variables supplied by the host.

Provider instance names must match `[0-9A-Za-z_-]+`. Connector `refresh_freq`, `prune_freq`, and `timeout_secs` must be integers; invalid values fail locally before HTTP.
