# Troubleshooting

Read error.kind, code, submission_id, task_id, request_id, state_file, and account_action. Explain impact/next step without keys, complete requests, stacks, or upload credentials.

| Signal | Action |
| --- | --- |
| input/configuration, exit 2 | Correct local inputs/configuration |
| authentication_required / HTTP/business 401 | Follow [authentication](authentication.md), then continue the original stage |
| 403 | Check IP allowlists, permissions, ownership |
| 1000 | Correct specific parameter/media issues while preserving intent |
| 1001 / Invalid taskType | Check environment availability; do not try invented types |
| 1006 / HTTP 429 | Reduce frequency; back off GET, do not automatically repeat POST |
| 1007 | Use the pricing/credit-pack link in account_action and preserve successful work through [account continuation](account-continuation.md) |
| 1008 | Check the specific quota; do not promise that buying credits resolves it |
| 1200 | Verify ID/environment; missing tasks do not authorize replacements |
| HTTP 200, business code not 200 | Business failure even with data |
| POST timeout/disconnect/500 | May be accepted. Retain submission_id/journal and resume. Without task_id, investigate the original operation rather than changing IDs to resubmit |
| cannot_resume without task_id | Keep the original directory. submission_id locates a local journal, not an undocumented server recovery endpoint |
| journal, exit 4 | Journal persistence failed after a request. Preserve returned submission_id, task_id, request_id, and path. Use status/wait directly for an available task_id; a file error does not mean nothing was submitted |
| Same submission_id / state conflicts with another request | Preserve the original journal. Use a new ID only for an intentionally new operation, never overwrite to bypass deduplication |
| FAILED | Report available cause/IDs; do not claim a refund |
| INSUFFICIENT_POINTS | Terminal failure: stop polling, retain record, resolve balance |
| COMPLETED without result / unknown status | Preserve ID and investigate through GET/support |

Subtitle removal can damage scene details. Compare source/output; retain the original and ID when quality fails. Do not automatically incur another charge.

Example: "The task is still processing. I saved its ID so we can continue checking." For uncertainty: "I saved the request record and will verify acceptance before creating another task."

[Recovery](task-lifecycle.md) · [Capabilities](capability-discovery.md)
