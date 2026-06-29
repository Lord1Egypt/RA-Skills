# Sage Router + Codex CLI live demo script

A reproducible demo showing Sage Router routing Codex CLI across local Ollama and cloud providers with automatic fallback. Use this for launch videos, livestreams, and sales calls.

## Prereqs

- Sage Router: `git clone https://github.com/earlvanze/sage-router.git`
- Ollama running locally with at least one model (e.g. `ollama pull qwen2.5-coder:latest`)
- Codex CLI installed
- At least one cloud provider key exported (optional but recommended for the fallback demo)

## Setup (2 minutes)

```bash
cd sage-router
python3 router.py --port 8790 &
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

Confirm the router is healthy and discoverable:

```bash
curl -s http://localhost:8790/health | jq .
curl -s http://localhost:8790/pricing | jq .
```

## Demo 1: local-first routing

Run Codex against the router with a coding task. The router prefers the local coding model and only falls back to cloud if local is unavailable.

```bash
codex --model ollama/qwen2.5-coder:latest "refactor this function to use a context manager"
```

Show the route the router picked:

```bash
tail -n 20 /tmp/sage-router.log   # or your configured log path
```

Point out the `route:` line: model selected, attempts, elapsed, fallback chain.

## Demo 2: automatic failover (the "wow" moment)

Kill the local model mid-session to force fallback:

```bash
ollama stop qwen2.5-coder:latest
```

Re-run the same Codex command. Sage Router detects the local failure and falls over to the next healthy provider in policy, with no mid-stream model handoff and no Codex config change. Show the route event proving the fallback.

## Demo 3: cloud-first, local fallback

Flip policy so a frontier cloud model is preferred and local Ollama is the safety net:

```bash
codex --model openai/gpt-4.1 "add unit tests for the parser"
```

Then throttle/simulate a cloud outage (rate limit, revoke key temporarily) and show the request still completing via local Ollama.

## Demo 4: one endpoint, every tool

Show that the same endpoint works for OpenAI-compatible and Anthropic-compatible tools without changing the router:

```bash
export ANTHROPIC_BASE_URL=http://localhost:8790
export ANTHROPIC_API_KEY=local-router
```

## Closing CTA

- Free local core: https://github.com/earlvanze/sage-router
- Hosted reliability + analytics (paid): https://sagerouter.dev
- Bring your own keys. No model resale. Credentials stay local by default.

## Tips for the presenter

- Keep a second terminal tailing the route log so the audience sees fallback happen live.
- Pre-pull models before the demo to avoid pull latency.
- Have the failover demo queued second; it's the strongest differentiator vs a plain proxy.
