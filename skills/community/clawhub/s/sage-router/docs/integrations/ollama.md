# Use Sage Router with Ollama and Ollama Cloud

Sage Router supports local Ollama and Ollama Cloud models exposed through your local Ollama runtime.

```bash
ollama serve
ollama list
```

Provider config:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434",
      "models": ["auto-discover"],
      "api": "ollama"
    }
  }
}
```

Sage Router discovers models from `/api/tags`. If your local Ollama runtime exposes `:cloud` models, Sage Router can discover and route to them.

Use `local-first` when you want real local models before cloud routes. Sage Router treats `:cloud` models as cloud-backed even though they are reached through localhost.
