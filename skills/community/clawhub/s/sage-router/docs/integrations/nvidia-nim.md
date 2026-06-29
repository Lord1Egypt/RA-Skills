# Use Sage Router with NVIDIA NIM / NVIDIA Cloud

Sage Router can route to NVIDIA-backed inference endpoints using your own NVIDIA API key.

```bash
export NVIDIA_API_KEY=nvapi-...
```

Provider config:

```json
{
  "providers": {
    "nvidia": {
      "baseUrl": "https://integrate.api.nvidia.com/v1",
      "apiKey": "${NVIDIA_API_KEY}",
      "models": ["auto-discover"],
      "api": "openai-completions"
    }
  }
}
```

Recommended chain: local model for low-risk tasks, NVIDIA NIM for GPU-backed hosted inference, Anthropic/OpenAI/Gemini fallback for provider diversity.
