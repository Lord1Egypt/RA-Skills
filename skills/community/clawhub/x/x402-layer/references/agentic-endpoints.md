# Agentic Endpoint Creation

Deploy your own monetized API endpoints programmatically.

Use this when the user wants to:
- create a paid API
- put an x402 paywall behind a button or action
- reuse one endpoint as the payment source for a custom UI
- top up endpoint credits after launch

## Endpoint
POST https://api.x402layer.cc/agent/endpoints

## Pricing
Create: $1 (4,000 credits included)
Top-up: $1 = 500 credits

## Create Flow
1. POST with endpoint config (name, slug, origin_url, chain)
2. Get 402 challenge
3. Sign with EIP-712
4. Send X-Payment header
5. Receive gateway URL and API key

## Seller-side controls now available in the skill

Agents can now configure the same endpoint-level settings humans use in Studio for direct endpoints:
- best fit audience
- AgentKit benefit mode
- AgentKit discount percent
- AgentKit free-trial uses

Create example:

```bash
python {baseDir}/scripts/create_endpoint.py cataas "CATAAS" https://example.com/cat 0.01 \
  --best-fit agents \
  --agentkit-benefit discount \
  --agentkit-discount-percent 20
```

Update example:

```bash
python {baseDir}/scripts/manage_endpoint.py update cataas \
  --best-fit humans \
  --agentkit-benefit free_trial \
  --agentkit-free-trial-uses 3
```

Audience labels map to:
- `everyone` -> `all`
- `humans` -> `human_only`
- `agents` -> `agent_only`

AgentKit benefit modes mean:
- `off`
- `free`
- `free_trial`
- `discount`

AgentKit benefits are currently valid only for direct endpoints and are evaluated against verified human-backed agent wallets.

The returned gateway URL becomes the public paid endpoint your users or agents call.
That same endpoint can sit behind:
- hosted request pages
- your own frontend button, card, or modal
- another agent workflow

## Top-Up
PUT /agent/endpoints/<slug> with topup_amount

## Check Status
GET /agent/endpoints/<slug> with x-api-key header

## Important Security Rule

When your endpoint origin receives proxied traffic from x402, it must verify:

```http
x-api-key: <YOUR_API_KEY>
```

Reject requests when the key is missing or wrong.

## API Schema

Endpoints can carry an API schema that documents the routes, parameters, and request bodies your origin supports. When set, the schema:
- displays on marketplace listings so consumers know what params to send
- appears in the 402 challenge response so agents can self-discover routes programmatically
- powers the interactive API tester on hosted pay pages
- is returned in `/agent/endpoints` GET responses

### Schema Format

```json
{
  "version": 1,
  "routes": [
    {
      "path": "/",
      "method": "GET",
      "summary": "Get a random cat image",
      "parameters": [
        {
          "name": "tag",
          "in": "query",
          "type": "string",
          "required": false,
          "description": "Filter by tag",
          "example": "cute"
        }
      ],
      "responseExample": "{\"url\": \"https://cataas.com/cat\"}"
    },
    {
      "path": "/says/{text}",
      "method": "GET",
      "summary": "Cat with text overlay",
      "parameters": [
        {
          "name": "text",
          "in": "path",
          "type": "string",
          "required": true,
          "example": "hello"
        }
      ]
    },
    {
      "path": "/analyze",
      "method": "POST",
      "summary": "Analyze an image",
      "parameters": [],
      "requestBody": {
        "contentType": "application/json",
        "fields": [
          {
            "name": "image_url",
            "type": "string",
            "required": true,
            "example": "https://example.com/photo.jpg"
          }
        ]
      }
    }
  ]
}
```

### Attaching Schema at Creation

```bash
# From a JSON file
python {baseDir}/scripts/create_endpoint.py my-api "My API" https://api.example.com 0.01 \
  --schema-file schema.json

# Inline JSON
python {baseDir}/scripts/create_endpoint.py my-api "My API" https://api.example.com 0.01 \
  --schema-json '{"version":1,"routes":[{"path":"/","method":"GET","summary":"Health check","parameters":[]}]}'
```

### Updating Schema

```bash
# Replace schema from file
python {baseDir}/scripts/manage_endpoint.py update my-api --schema-file updated-schema.json

# Clear schema
python {baseDir}/scripts/manage_endpoint.py update my-api --clear-schema
```

### Auto-Detect (Studio Dashboard)

The Studio dashboard can auto-detect schemas from OpenAPI/Swagger specs on your origin. This probes common paths like `/openapi.json`, `/swagger.json`, `/api-docs`, and `/.well-known/openapi`. If found, the spec is converted to x402 schema format and pre-populated in the builder.

### How Agents Discover Schema

When an agent calls an x402 endpoint and receives a 402 challenge, the response includes `api_schema` if one is set. Agents can inspect this to understand available routes before paying:

```python
resp = requests.get("https://api.x402layer.cc/e/my-api")
if resp.status_code == 402:
    challenge = resp.json()
    schema = challenge.get("api_schema")
    if schema:
        for route in schema["routes"]:
            print(f"{route['method']} {route['path']} — {route.get('summary', '')}")
```

Agents can also retrieve schema via the management API:

```python
resp = requests.get(
    "https://api.x402layer.cc/agent/endpoints",
    params={"slug": "my-api"},
    headers={"X-API-Key": api_key},
)
schema = resp.json().get("endpoint", {}).get("api_schema")
```

## When To Create Separate Endpoints

Reuse one endpoint when you just need one paid action.

Create separate endpoints when you need:
- different pricing
- separate analytics/accounting
- different webhook or fulfillment behavior
- different chains or wallet recipients
