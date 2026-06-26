# Persona Templates API Reference

Templates define a persona once and reuse it to spin up multiple agents instantly. Ideal for multi-tenant SaaS, enterprise rollouts, or A/B testing personas.

## What a Template Can Include

- **System Prompt** — Agent role, tone, and knowledge scope
- **Entry Message** — Greeting when the session starts
- **Exit Message** — Farewell when conversation ends
- **Idle Timeout** — Response when user is inactive
- **Knowledge Base Attachments** — Pre-bound knowledge sources
- **Behavior & Safety Settings** — Guardrails, escalation rules
- **Callback Events & Webhooks** — External workflow triggers

## Create a Template

`POST /v1/ext/template`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/template \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "template_name": "Sales Assistant Template",
    "template_system_prompt": "You are a friendly AI sales assistant that guides users through product selection and answers detailed product questions clearly.",
    "config": {
      "systemPrompt": "Respond in a conversational tone and always ask follow-up questions.",
      "conversationalContext": "sales",
      "maxCallDuration": 300
    },
    "knowledge_base": [
      { "id": "15b12908-309f-4e0f-bcb0-a4e23d45169a", "name": "Product Catalog" }
    ],
    "is_active": true,
    "record": true,
    "callback_url": "",
    "callback_events": []
  }'
```

**Response:**
```json
{ "id": "d65a4f92-44b1-4fe6-b2ac-a1cb66366ddc", "message": "Template created successfully" }
```

## When to Use Templates

- **Faster Deployment** — Clone-ready configs launch agents in seconds
- **Brand Consistency** — Central personality and tone management
- **Scale to Thousands** — Ideal for enterprise multi-location rollouts
- **Easy Experimentation** — Modify templates without rebuilding agents

## Get Template by ID

`GET /v1/ext/template/{id}`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/template/{id} \
  --header 'x-api-key: <api-key>'
```

## List All Templates

`GET /v1/ext/templates`

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/templates \
  --header 'x-api-key: <api-key>'
```

## Update a Template

`PUT /v1/ext/template/{id}`

```bash
curl --request PUT \
  --url https://api.trugen.ai/v1/ext/template/{id} \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "template_name": "Updated Name",
    "template_system_prompt": "Updated system prompt",
    "config": {
      "conversationalContext": "Updated context",
      "maxCallDuration": 300
    },
    "knowledge_base": null,
    "record": true,
    "is_active": true
  }'
```

**Response:** `{ "id": "...", "message": "Template details updated successfully" }`

## Delete a Template

`DELETE /v1/ext/template/{id}`

```bash
curl --request DELETE \
  --url https://api.trugen.ai/v1/ext/template/{id} \
  --header 'x-api-key: <api-key>'
```
