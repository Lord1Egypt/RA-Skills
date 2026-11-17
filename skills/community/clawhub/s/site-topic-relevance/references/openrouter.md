# Explicit OpenRouter CLI usage

The standalone CLI reads the key from the `OPENROUTER_API_KEY` environment variable. Keep keys out of command arguments, prompts, and screenshots. Requires Node.js 22 or later.

```bash
node "$SKILL_DIR/scripts/site-topic-relevance.mjs" analyze "$SITE_URL" \
  --out "$RUN_DIR" --limit 50 --lang en
```

The default route is `openai/gpt-6-luna`. To use another OpenRouter model, pass `--model "provider/model"` and select one that supports strict JSON Schema and the request parameters. The CLI uses only the selected service and model.

The command sends sampled public page text, excerpts, and the assessment schema to `https://openrouter.ai/api/v1/responses`. It sets `store: false`, `provider.require_parameters: true`, and `reasoning.effort: none`. The maximum output is 16,000 tokens. The request times out after 90 seconds, and the crawl and assessment together have a 240-second limit. Failures do not trigger paid retries.

On receipt of the response, the CLI records provider-reported tokens and cost in `private/<run-id>.json` before validating the result. Validation or save failures retain reported usage and mark the run `failed`. Missing usage or cost stays `null`. Divide a nano-USD value by 1e9 to convert it to US dollars.

The shareable HTML, Markdown, and JSON reports can include token counts. Cost, billing details, and the provider response ID stay in the private run file. Directory and file permissions are `0700` and `0600`, respectively, on filesystems that support them. Share the reports separately from the private records. Rendering or reopening a report is local.

The CLI redacts the API key from error messages and omits provider error bodies. For HTTP 429, timeout, or incomplete output, check the private run record and saved corpus before the user decides whether to retry. A saved corpus can be assessed by the current assistant and rendered locally without another crawl or API call.
