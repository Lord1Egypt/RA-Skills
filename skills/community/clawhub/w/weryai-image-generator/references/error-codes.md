# WeryAI Error Codes

> Last updated: 2026-03-19
> Source: `ApiResultCode.java` (server-side enum)

## API Response Structure

```json
{
  "status": 200,
  "msg": "Success",
  "data": { ... }
}
```

Success: `status` is `200` or `0`. Non-zero/non-200 indicates an error.

## HTTP-Level Errors

| HTTP Status | Code | Description | Action |
|---|---|---|---|
| 400 | `BAD_REQUEST` | Malformed request | Check request format |
| 403 | `INVALID_API_KEY` | API key invalid or IP denied | Verify `WERYAI_API_KEY` |
| 429 | — | Rate limited | Wait and retry |
| 500 | `SERVER_ERR` | Server error | Retry later |

## Business Error Codes (Image Generation Related)

| Code | Name | Description | Action |
|---|---|---|---|
| `1001` | REQUEST_RATE_LIMIT_EXCEEDED | Too many requests | Slow down, retry after a moment |
| `1002` | PARAMETER_ERROR | Invalid parameters | Check prompt, URLs, aspect_ratio, model, image_number |
| `1003` | RESOURCE_NOT_EXISTS | Task/batch not found | Check ID, may have expired |
| `1006` | NOT_MODEL | Model not supported | Use a different model key |
| `1007` | QUEUE_FULL | Service queue full | Wait and retry |
| `1009` | PERMISSION_DENIED | Permission denied | Check account permissions |
| `1010` | DATA_NOT_FOUND | Data not found | Resource may not exist |
| `1011` | INSUFFICIENT_CREDITS | Not enough credits | Run `balance-image.js`, recharge at weryai.com |
| `1014` | UPLOAD_IMG_EXCEED_MAX_LIMIT | Image too large | Use a smaller image |
| `1015` | UPLOAD_IMG_EXCEED_DAILY_LIMIT | Daily upload limit | Wait until tomorrow |
| `1017` | VIP_PERMISSION_DENIED | Requires subscription | Upgrade subscription plan |

## Content Safety Errors

| Code | Name | Description | Action |
|---|---|---|---|
| `2001` | IMG_RECOGNITION_LIMIT | Input image flagged | Use a different reference image |
| `2003` | IMG_TEXT_CHECK_FAILED | Prompt or image flagged | Revise prompt, remove sensitive content |
| `2004` | IMAGE_FORMAT_NOT_SUPPORT | Unsupported image format | Use jpg, png, or webp |

## Workflow Errors

| Code | Name | Description | Action |
|---|---|---|---|
| `6001` | WORKFLOW_SYSTEM_ERROR | Internal workflow error | Retry later |
| `6002` | WORKFLOW_RATE_LIMIT_EXCEEDED | Workflow rate limit | Slow down |
| `6003` | WORKFLOW_CREDIT_DEDUCT_FAILED | Credit deduction failed | Retry |
| `6004` | WORKFLOW_GENERATE_FAILED | Generation failed | Retry with different params |
| `6010` | WORKFLOW_COMMIT_CONCURRENT_TASK_LIMIT_EXCEEDED | Max 20 concurrent tasks | Wait for tasks to complete |
| `6101` | OPEN_API_DAILY_LIMIT_EXCEEDED | Daily API limit exceeded | Wait until tomorrow |

## Task Status Values

WeryAI uses inconsistent status values. The CLI normalizes all variants:

| Normalized | Raw Variants |
|---|---|
| `waiting` | `waiting`, `WAITING`, `PENDING`, `pending` |
| `processing` | `processing`, `PROCESSING` |
| `completed` | `succeed`, `SUCCEED`, `SUCCESS`, `success` |
| `failed` | `failed`, `FAILED` |
| `unknown` | Any other value (logged as warning) |

## Model-Specific Constraints

| Model | Constraint |
|---|---|
| `WERYAI_IMAGE_1_0` | `image_number` is fixed at 4 (auto-corrected) |
| `GROK_IMAGINE_IMAGE` | `aspect_ratio` is fixed at `3:4` (auto-corrected) |
