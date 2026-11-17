# Supported input formats

Accept JSON from Anthropic's Claude Platform endpoints:

- `/v1/organizations/cost_report`: actual costs in decimal-string minor units. Divide USD cents by 100.
- `/v1/organizations/usage_report/messages`: uncached input, cache creation, cache reads, output, model, service tier, context window, and server tool usage.

Analyze both files together. Files may be positional in any order or use `--costs` and `--usage` flags.

Warn instead of crashing when date ranges or workspace IDs do not match. Warn when `has_more` is true because the export is incomplete.

Do not support Claude Enterprise Analytics, Claude Platform on AWS, Amazon Bedrock, Google Vertex AI, screenshots, CSV, or non-Anthropic providers in this MVP.
