# Integration Guide: Python Proactive Hooks

To enable automated context optimization and service resilience, register the following scripts within your OpenClaw environment.

## Registration

Add these paths to your `.openclaw/hooks.json` or equivalent agent configuration file:

```json
{
  "hooks": {
    "PreRequest": "python3 hooks/openclaw/pre_request.py",
    "OnError": "python3 scripts/error_detector.py"
  }
}

```

## Environment Variables

| Variable | Requirement | Purpose |
| --- | --- | --- |
| `TRUNKATE_API_KEY` | **REQUIRED** | Authenticates your requests against Firestore `api_keys_v2`. |
| `TRUNKATE_THRESHOLD` | Optional | Usage % (0.1–0.9) to trigger the proactive hook (Default: 0.8). |
| `TRUNKATE_AUTO_BUDGET` | Optional | Target token count for the `/optimize` call (Default: 1000). |
| `TRUNKATE_API_URL` | Optional | Overrides default `https://api.trunkate.ai` for local dev or testing. |
| `TRUNKATE_DEBUG` | Optional | Enable verbose logging of hook execution to `stderr`. |

## Verification

After registration, verify the integration by running a high-context command (e.g., `ls -R` in a large project). The `PreRequest` hook should trigger if your token usage exceeds the threshold, and you should see the `OPENCLAW_ACTION:SET_HISTORY` emission in the agent logs.

---
