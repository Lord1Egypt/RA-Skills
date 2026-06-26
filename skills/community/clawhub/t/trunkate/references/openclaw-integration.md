# OpenClaw & Trunkate API Integration Spec

## 1. Request Flow

1. **Interceptor**: The `PreRequest` event triggers `pre_request.py`.
2. **Logic Gate**: `activator.py` evaluates `OPENCLAW_CURRENT_TOKENS` vs `OPENCLAW_TOKEN_LIMIT`.
3. **Execution**: If the threshold (default 0.8) is met, the system issues a POST request to the `/optimize` endpoint.
4. **State Injection**: On success, the script emits `OPENCLAW_ACTION:SET_HISTORY` to update the agent's memory.

## 2. API Endpoint Specification

- **URL**: `https://api.trunkate.ai/optimize` (Configurable via `TRUNKATE_API_URL`).
- **Method**: `POST`.
- **Auth**: `Authorization: Bearer <TRUNKATE_API_KEY>`.
- **Payload Schema**:

  | Field | Type | Description |
  | :--- | :--- | :--- |
  | `text` | string | The full prompt or history text to optimize. |
  | `task` | string? | Optional intent hint (e.g., "Summarize logs"). |
  | `budget` | int? | Target token budget (API default: 2048). |
  | `model` | string | Target LLM (Default: "gpt-4o"). |

## 3. Response Schema

The backend returns an `OptimizeResponse` object:

- `optimized_text`: The semantically compressed output.
- `original_tokens` / `optimized_tokens`: Comparison metrics.
- `reduction_percent`: The efficiency gain of the call.
- `soft_limit_enforced`: Boolean indicating if the budget was strictly met.

## 4. Operational Environment Variables

| Variable | Default | Source |
| :--- | :--- | :--- |
| `TRUNKATE_API_KEY` | REQUIRED | Firestore `api_keys_v2`. |
| `TRUNKATE_THRESHOLD` | `0.8` | Activator Logic Gate. |
| `TRUNKATE_AUTO_BUDGET` | `2000` | Target for `/optimize` call. |

## 5. Service Resilience (Bypass Protocol)

In the event of a service-level failure, Trunkate AI follows a "Silent Bypass" to prevent session lock:

- **429 Rate Limit**: If `api key budget exceeded` or `account rate limit exceeded` is returned, the system skips optimization and proceeds with the raw history.
- **5xx/Timeout**: If the API, Redis, or Firestore is unreachable, the `error-detector.py` issues a bypass alert and yields to the unoptimized context.
- **Zero-Latency Fail-Safe**: Infrastructure-level errors never block the agent; the unoptimized prompt is always the fallback.
