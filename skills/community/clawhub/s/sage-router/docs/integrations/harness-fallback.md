# Use Sage Router for harness fallback

Sage Router is designed for agent harnesses and developer tools that need policy-based fallback across the user’s own authorized provider access.

Example provider mix:

```json
{
  "providers": {
    "ollama": { "baseUrl": "http://localhost:11434", "models": ["auto-discover"], "api": "ollama" },
    "openai": { "baseUrl": "https://api.openai.com/v1", "apiKey": "${OPENAI_API_KEY}", "models": ["auto-discover"], "api": "openai-completions" },
    "anthropic": { "baseUrl": "https://api.anthropic.com", "apiKey": "${ANTHROPIC_API_KEY}", "models": ["auto-discover"], "api": "anthropic-messages" },
    "nvidia": { "baseUrl": "https://integrate.api.nvidia.com/v1", "apiKey": "${NVIDIA_API_KEY}", "models": ["auto-discover"], "api": "openai-completions" }
  }
}
```

Recommended modes: `fast`, `balanced`, `best`, and `local-first`.
