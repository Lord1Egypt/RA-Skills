# Supported input formats

Accept local JSON exports from:

- Google Cloud Billing standard or detailed BigQuery export rows. Read `cost`, `currency`, `credits`, `service.description`, `sku.description`, `project.id`, and usage timestamps.
- Gemini or Vertex AI response logs containing `usageMetadata`, including `promptTokenCount`, `candidatesTokenCount`, `cachedContentTokenCount`, `thoughtsTokenCount`, `toolUsePromptTokenCount`, and `totalTokenCount`.

Analyze billing and usage files together. Files may be positional in any order or passed with `--billing` and `--usage`.

Only include a billing row when its service, SKU, model, or description clearly identifies Gemini or a Vertex AI generative model. Never total unrelated Google Cloud charges. Calculate net cost as `cost + credits`, because billing credit amounts are normally negative.

Warn rather than crash when billing and usage date ranges or project IDs do not match. Warn when no Gemini rows are found.

Do not support screenshots, invoices, CSV, Google Workspace Gemini subscriptions, or non-Google providers in this MVP.
