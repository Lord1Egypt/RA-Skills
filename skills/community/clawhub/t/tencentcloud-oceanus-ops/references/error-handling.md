# Error Handling Matrix

Standard error recovery strategies for TencentCloud Oceanus API errors.

## Error Response Format

TencentCloud API returns errors in this format:
```json
{
  "Response": {
    "Error": {
      "Code": "ErrorCode",
      "Message": "Human-readable error message"
    },
    "RequestId": "xxx-xxx-xxx"
  }
}
```

The CLI wraps this into a standardized envelope:
```json
{
  "success": false,
  "operation": "CreateJob",
  "error": {
    "code": "ErrorCode",
    "message": "Human-readable error message"
  },
  "request_id": "xxx-xxx-xxx"
}
```

## Common Error Codes and Recovery

### Authentication Errors

| Code | Meaning | Recovery |
|------|---------|----------|
| AuthFailure | CAM signature/auth error | Check TENCENTCLOUD_SECRET_ID/SECRET_KEY environment variables |
| AuthFailure.UnauthorizedOperation | Insufficient permissions | Request CAM policy with `oceanus:*` permissions |
| UnsupportedOperation.NoPermissionAccess | Workspace access denied | Verify user has workspace membership |

### Validation Errors

| Code | Meaning | Recovery |
|------|---------|----------|
| InvalidParameter.InvalidName | Job name format invalid | Use alphanumeric, Chinese, `-`, `_`, `.` (max 50 chars) |
| InvalidParameterValue.JobName | Illegal job name | Same as above |
| InvalidParameterValue.JobNameExisted | Duplicate job name | Choose a unique name |
| InvalidParameterValue.ClusterId | Cluster ID invalid/empty | Provide valid cluster-xxxx ID |
| InvalidParameterValue.CuMem | CU memory value invalid | Use 2, 4, 8, or 16 |
| InvalidParameterValue.JobTypeCombineWithClusterType | Type mismatch | Verify JobType + ClusterType compatibility |

### Resource Errors

| Code | Meaning | Recovery |
|------|---------|----------|
| ResourceNotFound.ClusterId | Cluster not found | Verify cluster exists with describe_clusters |
| ResourceUnavailable.Cluster | Cluster not in running state | Wait for cluster to be ready |
| ResourceUnavailable.ClusterGroupStatus | Cluster group status error | Check cluster health |
| ResourceUnavailable.ReqCuMem | Shared cluster CuMem constraint | Shared clusters only allow CuMem=4 |

### Limit Errors

| Code | Meaning | Recovery |
|------|---------|----------|
| LimitExceeded.Job | Job count exceeded | Delete unused jobs or request quota increase |
| LimitExceeded | General quota exceeded | Contact support for quota increase |

### Operation Errors

| Code | Meaning | Recovery |
|------|---------|----------|
| FailedOperation | General operation failure | Retry with correct parameters |
| FailedOperation.DuplicatedJobName | Duplicate job name | Use a unique name |
| FailedOperation.UserNotAuthenticated | User not verified | Complete real-name verification |
| InternalError | Internal server error | Retry after delay |
| InternalError.DB | Database error | Retry after delay |

### Client Errors (CLI-generated)

| Code | Meaning | Recovery |
|------|---------|----------|
| MissingCredentials | Env vars not set | **Stop execution** and guide the user to persist credentials in a shell/OS config file based on their OS (macOS → `~/.zshrc`; Linux bash → `~/.bashrc`; fish → `~/.config/fish/conf.d/*.fish`; Windows → `setx` / `[Environment]::SetEnvironmentVariable(... "User")`). Never ask the user to paste secrets into chat, never echo/print env vars, and never write keys to repo files. See `references/credential-setup.md` for the full per-OS template and the `MissingCredentials` recovery flow. |
| ValidationError | Required parameter missing | Add the missing --parameter |
| SafetyCheckRequired | Mutation without --confirm | Add --confirm flag |
| Cancelled | User cancelled interactively | Re-run with --confirm if intended |
| NetworkError | Cannot reach API endpoint | Check network connectivity |
| HttpError | HTTP error from server | Check status code and retry |

## Retry Strategy

1. **Retryable**: InternalError, InternalError.DB, NetworkError, HttpError (5xx)
2. **Not retryable**: AuthFailure, InvalidParameter*, ResourceNotFound*, LimitExceeded*
3. **Recommended delay**: 1s, 2s, 4s (exponential backoff, max 3 retries)
