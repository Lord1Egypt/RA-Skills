# Vidau API Error Codes and User Messages

When the script or API returns a non-200 response, use `code` or `message` to give the user a clear explanation. Below are common errors and suggested user messages.

| Code / Keyword | Meaning | Suggested user message |
|----------------|---------|-------------------------|
| `CreditInsufficient` | Insufficient credits | Insufficient credits. Please top up in the Vidau console and try again. |
| `TaskPromptPolicyViolation` | Prompt violates content policy | Your prompt may violate content policy. Please revise and try again. |
| `ImageDownloadFailure` | Image download failed | The image URL(s) could not be downloaded. Ensure they are publicly accessible. |
| `VIDAU_API_KEY` not set | API Key not configured | Register at https://www.superaiglobal.com/ to get an API key, then configure it in OpenClaw skills.entries.vidau or set env VIDAU_API_KEY. |
| HTTP 401 | Authentication failed | Invalid or expired API Key. Check your key in the Vidau console. |
| HTTP 429 | Too many requests | Too many requests. Please try again later. |
| Other 4xx/5xx | Server error | The API returned an error. Try again later or check the docs / contact support. |

Agents should relay the API `message` to the user first, then add the short message above if needed.
