# The CLI, the SDKs and the OpenAPI document

The packages offer the same operations under the same names. Use one when it's installed or the project already depends on it. Plain HTTP with curl works everywhere.

## The `rumoro` CLI

Install it with `npm install -g @rumoro-dev/cli`, or run it without installing as `npx @rumoro-dev/cli --help`. Check whether it's available with `command -v rumoro`.

- Every endpoint is a `noun:verb` command, such as `rumoro mentions:search --relevant true --intent buy_intent --limit 20` or `rumoro keywords:create --term "basil" --kind brand`. Each rule file names the command for each endpoint.
- It reads `RUMORO_API_KEY`, or the key that `rumoro auth:login` saved in `~/.rumoro/config.json`.
- It prints JSON, compact when piped and indented in a terminal, and writes errors to stderr.
- `rumoro mentions:watch` streams new mentions as they arrive, one JSON object per line, so `| jq -r '.post.url'` works.

[Source](https://github.com/rumoro-dev/cli) · [Docs](https://docs.rumoro.dev/cli)

## TypeScript SDK

Install it with `npm install @rumoro-dev/sdk`. Each endpoint is a function, generated from the OpenAPI document.

```ts
import { createRumoro } from '@rumoro-dev/sdk';
const rumoro = createRumoro({ apiKey: process.env.RUMORO_API_KEY! });
const { data, error } = await rumoro.searchMentions({ query: { relevant: true, limit: 25 } });
```

[Source](https://github.com/rumoro-dev/sdk) · [Docs](https://docs.rumoro.dev/sdks/typescript)

## Python SDK

Install it with `pip install rumoro`. It has a sync client (`Rumoro`) and an async one (`AsyncRumoro`).

```python
from rumoro import Rumoro
rumoro = Rumoro(api_key="ref_...")
for mention in rumoro.mentions.search(relevant=True, limit=25).data:
    print(mention.classification.relevance, mention.post.url)
```

[Source](https://github.com/rumoro-dev/sdk-python) · [Docs](https://docs.rumoro.dev/sdks/python)

## The OpenAPI document

`https://api.rumoro.dev/v1/openapi.json` lists every operation, parameter, field and error code. The SDKs, the CLI and the rule files in this skill are generated from it.
