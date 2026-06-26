# Synology DSM API Error Codes

## Universal Error Codes (All APIs)

| Code | Name | Description | Suggested Action |
|------|------|-------------|-----------------|
| 100 | Unknown error | Unspecified server error | Retry once, then investigate |
| 101 | Bad request | Malformed or invalid parameters | Check parameter names and values |
| 102 | No such API | API name not found | Verify package is installed; use SYNO.API.Info to check |
| 103 | No such method | Method doesn't exist for this API | Check API docs for available methods |
| 104 | Version not supported | Requested version too high/low | Query SYNO.API.Info for supported version range |
| 105 | No permission | Insufficient user privileges | Check user/group permissions in DSM |
| 106 | Session timeout | Session expired (~15 min inactivity) | Re-authenticate and retry |
| 107 | Session interrupted | Session forcibly closed | Re-authenticate and retry |
| 108 | Missing required parameters | Required param not provided | Check required parameters in docs |
| 109 | Invalid parameter | Parameter value out of range/format | Validate input values |
| 114 | Missing upload file | File upload expected but not provided | Include file in multipart form |
| 117 | Request too large | Request body exceeds limit | Reduce payload or chunk uploads |
| 118 | Temporary unavailable | Service restarting or busy | Wait and retry |
| 119 | Invalid JSON | Request body is not valid JSON | Fix JSON formatting |
| 150 | IP blocked | Too many failed attempts | Wait for block to expire |

## Authentication Error Codes (SYNO.API.Auth)

| Code | Description | Suggested Action |
|------|-------------|-----------------|
| 400 | Incorrect password | Verify credentials |
| 401 | Account disabled | Contact NAS admin |
| 402 | Permission denied | User lacks API access |
| 403 | 2FA code required | Include `otp_code` parameter |
| 404 | 2FA authentication failed | Check OTP code |
| 406 | Enforce 2FA for auth | Account requires 2FA; provide OTP |
| 407 | Blocked IP after failed attempts | Wait or whitelist IP |
| 408 | Expired password | Change password in DSM |
| 409 | Password must be changed | Change password before login |
| 410 | Unauthorized IP | IP not in allowed list |

## FileStation Error Codes (SYNO.FileStation.*)

| Code | Description |
|------|-------------|
| 400 | Invalid parameter of file operation |
| 401 | Unknown error of file operation |
| 402 | System too busy |
| 403 | User not authorized for this file operation |
| 404 | Invalid group |
| 405 | Invalid user |
| 406 | Cannot access that path |
| 407 | Permission denied on this operation |
| 408 | Disk quota exceeded |
| 409 | Connection type not allowed |
| 410 | File/folder path too long |
| 411 | File/folder already exists |
| 412 | File/folder name too long |
| 414 | Path does not exist |
| 415 | File not allowed in this shared folder |
| 416 | Item in use or locked |
| 417 | File extension policy violation |
| 418 | Folder limit exceeded |
| 419 | Cannot create subfolder in this path |

## DownloadStation Error Codes (SYNO.DownloadStation.*)

| Code | Description |
|------|-------------|
| 400 | File upload failed |
| 401 | Max number of tasks reached |
| 402 | Destination denied |
| 403 | Destination does not exist |
| 404 | Invalid task ID |
| 405 | Invalid task action |
| 406 | No default destination |

## How to Read Error Responses

Every API response with an error has this format:

```json
{
  "success": false,
  "error": {
    "code": 106,
    "errors": []
  }
}
```

Check `success` first. If `false`, look up `error.code` in the tables above. The `errors` array may contain additional details for batch operations.
