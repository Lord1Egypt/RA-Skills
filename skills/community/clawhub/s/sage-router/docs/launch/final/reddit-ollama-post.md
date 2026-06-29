# Reddit r/Ollama launch post

Status: ready after owner approval. Use this as the second Reddit post after
the r/selfhosted launch post because the launch funnel currently shows Reddit
as the strongest external channel and the Ollama route page is live.

## Title

Sage Router — local Ollama + Ollama Cloud routing with provider failover

## Body

I built and open-sourced the model router I run between my agents and Ollama.

Sage Router exposes one OpenAI-compatible endpoint, routes by task/model
capability/provider health/policy, and can fail over between local Ollama,
Ollama Cloud through your authorized local Ollama runtime, and other providers
you configure.

The Ollama-specific use case:

- keep local Ollama first for privacy, latency, or cost;
- overflow to cloud providers when local capacity is not enough;
- fall back to local Ollama when a cloud provider rate-limits or fails;
- keep provider keys and OAuth/subscription paths on your router host by
  default;
- route image/audio/video requests only to models that can actually handle
  those inputs.

30-second local start:

```bash
python3 router.py --port 8790
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

Ollama route overview:
https://sagerouter.dev/ollama-ai-model-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Public model catalog:
https://sagerouter.dev/models?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Quickstart:
https://sagerouter.dev/quickstart?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

Repo:
https://github.com/earlvanze/sage-router?utm_source=reddit&utm_medium=community&utm_campaign=sage-router-launch

How are you handling failover between local Ollama and cloud models today?
Are people mostly keeping that in each app, using Open WebUI, writing a small
gateway, or just accepting provider failures?
