# TokenLab OpenAI-Compatible Migration Skill

This skill helps coding agents migrate OpenAI-compatible apps, SDKs, examples, and environment variables to TokenLab.

Install:

```bash
npx skills add https://github.com/hedging8563/tokenlab-skills --skill tokenlab-openai-compatible-migration -y
```

Use it when you want an agent to:

- Replace OpenAI/OpenRouter-compatible base URLs with TokenLab.
- Keep existing OpenAI SDK code with minimal changes.
- Decide when to keep `/v1/chat/completions` and when to use Responses, Anthropic Messages, or Gemini native routes.
- Add model discovery and error recovery instead of hardcoded stale model IDs.
