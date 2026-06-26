# ARK Responses API Notes

Use this file when you need to adjust request fields, response parsing, or publishing metadata for `volcengine-ark-web-search`.

## Current Runtime Contract

- Endpoint: `https://ark.cn-beijing.volces.com/api/v3/responses`
- Auth: `Authorization: Bearer $ARK_API_KEY`
- Content type: `application/json`
- Tool enabled by this skill: `web_search`

Request shape used by the bundled script:

```json
{
  "model": "doubao-seed-1-6-250615",
  "stream": false,
  "tools": [
    {
      "type": "web_search",
      "max_keyword": 2
    }
  ],
  "input": [
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "System prompt here"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "User query here"
        }
      ]
    }
  ]
}
```

Compatibility behavior in the script:

- If `search_context_size` is supplied and ARK responds with HTTP `400` indicating that field is unsupported, the script drops the field and retries automatically.
- Transient HTTP failures and network errors can be retried with `--retries` and `--retry-delay`.
- `--timeout` applies per attempt, not across the whole run.
- Default markdown output is script-controlled and normalized into title, summary, and sources.

## Why The Script Uses Standard Library HTTP

- No extra dependency is required beyond `python3`.
- The bundle is easier to install and publish on ClawHub.
- The script remains usable on systems where `volcenginesdkarkruntime` is not installed.

## Model Drift

Volcengine model ids change over time. Do not assume a single hard-coded model remains the best choice.

Current skill behavior:

- default model: `doubao-seed-1-6-250615`
- override path: `--model ...` or `ARK_MODEL=...`

Reason:

- The user-supplied example used `doubao-seed-1-6-250615`.
- Official Volcengine examples have also shown newer dated variants, so the skill should remain override-friendly.

## Tool Naming Drift

Volcengine documentation has shown both `web_search` and `web_search_preview` in public examples at different times.

Current skill behavior:

- default tool name: `web_search`

If your target environment requires a different tool id, update both:

1. `scripts/ark_web_search.py`
2. `SKILL.md`

## Response Parsing Strategy

The Responses API is OpenAI-like but can evolve. The script therefore uses tolerant parsing:

- Prefer top-level `output_text` when present.
- Otherwise scan `output[].content[]` for `text` or `output_text`.
- In streaming mode, collect SSE deltas first and attach the final response object if provided.
- Collect source links by recursively scanning for `url` or `href` fields.

If Volcengine changes the event schema, fix `find_stream_delta()` and `extract_output_text()` first.

## Known Compatibility Issue

Some ARK environments accept:

- `max_keyword`
- `timeout`

but reject:

- `search_context_size`

Current skill behavior:

- keep `--search-context-size` available because some environments may support it
- if the current environment rejects it, automatically retry once without it

## Output Contract

For the default `markdown` format, the script aims to produce:

1. `# <query as title>`
2. `## 摘要`
3. concise answer body
4. `## 来源`
5. parsed source links when available

The default system prompt explicitly asks the model not to emit its own title or sources section, which reduces layout drift.

## ClawHub Publishing Notes

This skill is publish-ready as a text bundle:

- required file: `SKILL.md`
- optional supporting files: `scripts/ark_web_search.py`, this reference file, `agents/openai.yaml`

Frontmatter metadata is aligned with the runtime:

- required env: `ARK_API_KEY`
- required local runtime: `python3`

## Official References

- Responses object docs: `https://www.volcengine.com/docs/82379/1783703?lang=zh`
- Responses streaming article: `https://developer.volcengine.com/articles/7563963410168569894`
- Web search article: `https://developer.volcengine.com/articles/7565184101091639338`
- Web search API reference: `https://www.volcengine.com/docs/82379/1958524?lang=zh`
- Common online inference docs: `https://www.volcengine.com/docs/82379/2121998?lang=zh`
