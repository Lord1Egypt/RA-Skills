Share this Distiller integration with operators who want a clean webpage-to-Markdown step for agents.

Recommended message:

```text
Install web-distiller, sign in at https://webdistiller.dev if you need an API key, and start with POST /markdown or the default `web-distiller <url>` command. Upgrade to Starter only if you need POST /distill. POST /extract is temporarily unavailable right now.
```

Suggested environment:

```env
DISTILLER_API_BASE=https://webdistiller.dev
DISTILLER_API_KEY=your-api-key
```

Suggested command:

```bash
web-distiller <url>
```

Notes:

- `--endpoint markdown` is the default and best first step
- `--endpoint distill` is for paid users
- `--format text` is useful for compact prompts
- `--format json` is useful when the caller needs metadata too
