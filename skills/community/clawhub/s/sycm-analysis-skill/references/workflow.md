# Workflow Details for sycm-analysis-skill

## Login Verification
- Visit `https://sycm.taobao.com/`. If the response **does not** redirect to `https://sycm.taobao.com/custom/login.htm`, the user is considered logged in.
- If redirected to `login.taobao.com`, prompt the user to complete QR‑code login.
- Use the `Exec` tool to poll the login page every 5 seconds until the redirect no longer occurs.

## Initiate Weekly Report Request
```javascript
async () => {
  const query = encodeURIComponent("查看周报");
  const url = `https://sycm.taobao.com/ucc/next/message/send.json?text=${query}`;
  const r = await fetch(url);
  return await r.json();
}
```
- Extract `conversationCode` and `sendTime` from the JSON response.

## Polling for Report Generation
- Endpoint: `https://sycm.taobao.com/ucc/next/message/getReportResult.json?conversationCode={conversationCode}&sendTime={sendTime}`
- Perform a GET request **every 5 seconds**.
- Stop when `data.content` is non‑empty **or** after **5 minutes** (≈60 attempts). 
- Do **not** use the browser `evaluate` tool for this due to timeout limits; use plain HTTP fetches.

## Result Handling
- Return `data.content` as‑is (Markdown). Preserve all original formatting, charts, and Qianniu links.

## Exception Handling Matrix
| Scenario | Detection | Action |
|---|---|---|
| Not logged in (redirect) | Response redirects to `login.taobao.com` | Prompt user to login via QR code, then poll until authenticated. |
| Not logged in (API error) | API returns error code or malformed JSON | Guide user to open login page, retry every 5 seconds. |
| System busy | Page contains "Too many visitors, queuing" | Inform user to retry later. |
| Timeout | No `data.content` after 5 minutes of polling | Abort and tell user the report generation timed out. |

## Rate Limiting Guidance
- Avoid rapid repeated calls to the same endpoints within a short window to prevent triggering Sycm security controls.
- Implement a minimum 5‑second interval between polling attempts as specified.
