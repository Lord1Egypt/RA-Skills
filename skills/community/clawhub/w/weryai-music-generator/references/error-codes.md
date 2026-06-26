# Error Codes

These are the main WeryAI and CLI-side errors you are likely to encounter when using the `weryai-music-generator` skill package.

## CLI-side Errors

| Code | Meaning |
| --- | --- |
| `VALIDATION` | The local CLI rejected the request before submission |
| `NO_API_KEY` | `WERYAI_API_KEY` was not set before running the script |
| `TIMEOUT` | The HTTP request or polling window exceeded the configured timeout |
| `NETWORK_ERROR` | The request failed before the API returned a usable JSON response |
| `TASK_FAILED` | The task reached a failed terminal state |
| `PROTOCOL` | The API returned success but no usable task ID |

## Common WeryAI API Errors

| Code | Meaning |
| --- | --- |
| `1001` | Request rate limit exceeded |
| `1002` | Parameter error |
| `1003` | Resource not found |
| `1007` | Queue full |
| `1011` | Insufficient credits |
| `2003` | Content flagged by safety system |
| `6001` | Workflow system error |
| `6003` | Credit deduction failed |
| `6004` | Generation failed |
| `6010` | Concurrent task limit reached |
| `6101` | Daily request limit exceeded |

## Troubleshooting Hints

- If you get `VALIDATION`, compare the request against [api-music.md](api-music.md).
- If you get `NO_API_KEY`, set `WERYAI_API_KEY` before running the script.
- If you get HTTP `403`, verify `WERYAI_API_KEY` and API access policy.
- If you get `1011`, recharge credits before retrying.
- If you get `TASK_FAILED`, inspect the returned `msg` from the task status response.
- If polling returns `TIMEOUT`, increase `WERYAI_POLL_TIMEOUT_MS` or check the task later with `status`.
