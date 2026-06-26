# WhatsApp Cloud API - Error Codes Reference

> **Author:** Bello Sanchez
> **API Version:** v21.0
> **Last Updated:** 2026-02-09

---

## Overview

This document covers the error response format, common error codes, rate limits, quality ratings, messaging tiers, and retry strategies for the WhatsApp Cloud API. Proper error handling is essential for building a reliable messaging system.

---

## Error Response Format

All API errors follow a consistent JSON structure:

```json
{
  "error": {
    "message": "Human-readable error description",
    "type": "OAuthException",
    "code": 100,
    "error_subcode": 2494075,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "Additional context about the error"
    },
    "fbtrace_id": "A1B2C3D4E5F6"
  }
}
```

### Error Fields

| Field            | Type   | Description                                                    |
|------------------|--------|----------------------------------------------------------------|
| `message`        | string | Human-readable description of the error.                       |
| `type`           | string | Error category (e.g., `OAuthException`, `GraphMethodException`). |
| `code`           | number | Primary error code for programmatic handling.                  |
| `error_subcode`  | number | More specific error identifier within the primary code.        |
| `error_data`     | object | Additional context, including `messaging_product` and `details`. |
| `fbtrace_id`     | string | Unique trace ID for Meta support debugging.                    |

> **Tip:** Always log `fbtrace_id` alongside error codes. Meta support requires this ID when investigating issues.

---

## Common Error Codes

### Message Delivery Errors

| Code   | Subcode | Title                           | Cause                                           | Resolution                                    |
|--------|---------|----------------------------------|--------------------------------------------------|-----------------------------------------------|
| 131030 | —       | Recipient not valid WhatsApp user | Phone number is not registered on WhatsApp.     | Validate the number before sending. Remove from contact list if persistent. |
| 131047 | —       | Re-engagement message required   | 24-hour customer service window has expired.    | Send an approved template message to re-open the conversation window. Do NOT retry the original message. |
| 131050 | —       | User stopped marketing messages  | User opted out of marketing-category messages.  | Only send utility or service-category templates. Respect the opt-out — do NOT retry. |
| 131051 | —       | Unsupported message type         | The `type` field value is not recognized.       | Verify the `type` field spelling and that it matches a supported message type. |
| 131056 | —       | Pair rate limit exceeded         | Too many messages sent to the same recipient in a short window. | Wait at least 60 seconds before retrying to the same number. |

### Rate Limit Errors

| Code   | Subcode | Title                 | Cause                                          | Resolution                                       |
|--------|---------|------------------------|-------------------------------------------------|--------------------------------------------------|
| 130429 | —       | Rate limit hit         | Exceeded 80 messages per second per phone number. | Queue messages and implement throttling. Retry with exponential backoff. |

### Template Errors

| Code   | Subcode | Title                             | Cause                                             | Resolution                                       |
|--------|---------|------------------------------------|----------------------------------------------------|--------------------------------------------------|
| 132000 | —       | Template parameter count mismatch  | Number of parameters does not match template placeholders. | Verify parameter count matches the template definition exactly. |
| 132012 | —       | Template not found                 | Template name or language code is incorrect.       | Verify the template name and `language.code` match what is approved in Business Manager. |
| 132015 | —       | Template paused                    | Template paused due to low quality rating.         | Review template quality in Business Manager. Edit and resubmit, or create a new template. |
| 132068 | —       | Flow is in blocked state           | The WhatsApp Flow associated with the template is blocked. | Review and fix the Flow in Business Manager before resending. |

### Registration and Authentication Errors

| Code   | Subcode | Title                       | Cause                                         | Resolution                                        |
|--------|---------|------------------------------|------------------------------------------------|---------------------------------------------------|
| 133010 | —       | Phone number not registered  | Business phone number is not registered for Cloud API. | Complete phone number registration (see PHONE-NUMBERS.md). |
| 100    | —       | Invalid parameter            | A required parameter is missing or malformed.  | Check the request body against the API specification. |
| 190    | —       | Invalid OAuth token          | Access token is expired, revoked, or invalid.  | Refresh the access token. For system user tokens, regenerate in Business Manager. |

---

## Rate Limits

### Cloud API Throughput

| Limit Type               | Value                                   |
|--------------------------|-----------------------------------------|
| Messages per second      | 80 per phone number                     |
| Media uploads per second | Subject to general Graph API rate limits |
| API calls per hour       | Varies by app tier and token type        |

### Template Message Limits

Template message sending is subject to per-number daily limits that depend on the phone number's quality rating and messaging tier.

---

## Quality Rating

Each business phone number has a quality rating that Meta calculates based on user feedback and messaging patterns.

| Rating          | Indicator | Impact                                           |
|-----------------|-----------|--------------------------------------------------|
| High            | GREEN     | Number is performing well. Eligible for tier upgrades. |
| Medium          | YELLOW    | Quality is declining. Current tier is maintained. Watch closely. |
| Low             | RED       | Poor quality. Messaging tier may decrease. Templates may be paused. |

### Factors That Affect Quality

- **User blocks**: High block rates lower quality rapidly.
- **User reports**: Spam reports directly impact the rating.
- **Template feedback**: Low engagement or high dismissal rates on templates.
- **Message relevance**: Sending irrelevant content to users.

### How to Improve Quality

1. Only message users who have opted in.
2. Send relevant, timely content.
3. Honor opt-out requests immediately.
4. Use the correct template category (marketing vs. utility vs. authentication).
5. Monitor the quality rating in Business Manager and react to YELLOW before it drops to RED.

---

## Messaging Tiers

Messaging tiers determine how many unique customers a business phone number can message within a rolling 24-hour period.

| Tier   | Unique Customers per 24 Hours |
|--------|-------------------------------|
| Tier 1 | 1,000                         |
| Tier 2 | 10,000                        |
| Tier 3 | 100,000                       |
| Tier 4 | Unlimited                     |

### Tier Upgrade Conditions

A number automatically upgrades to the next tier when ALL of the following are true:

1. Quality rating is **GREEN**.
2. The number has reached its current tier's daily sending limit.
3. The number has been active and sending for at least **7 consecutive days**.

### Tier Downgrade Conditions

A number is downgraded when:

1. Quality rating drops to **RED**.
2. Meta reduces the tier by one level.
3. Further downgrades are possible if quality does not improve.

> **Warning:** A downgrade from Tier 3 to Tier 2 can severely disrupt high-volume messaging. Monitor quality proactively.

---

## Retry Strategy

Not all errors should be retried. The table below defines the correct retry behavior for each error category.

### Retryable Errors

| Error Code | Error Name            | Retry Strategy                                                        |
|------------|-----------------------|-----------------------------------------------------------------------|
| 130429     | Rate limit hit        | Exponential backoff starting at 1 second, doubling up to 60 seconds max. |
| 131056     | Pair rate limit       | Wait at least 60 seconds before retrying to the same recipient.       |
| 5xx        | Server errors         | Retry with exponential backoff, maximum 3 attempts. If still failing, alert operations. |

### Non-Retryable Errors (Do NOT Retry)

| Error Code | Error Name                      | Correct Action                                                      |
|------------|---------------------------------|----------------------------------------------------------------------|
| 131047     | Re-engagement required          | Send an approved template message instead. The original message type cannot be sent outside the 24-hour window. |
| 131050     | User opted out of marketing     | Respect the opt-out. Remove user from marketing campaigns. Only send utility/service messages if applicable. |
| 131030     | Not a WhatsApp user             | Mark the number as invalid. Do not retry.                           |
| 132000     | Parameter count mismatch        | Fix the parameter count in your code. This is a developer error.    |
| 132012     | Template not found              | Verify the template name and language. This is a configuration error. |
| 132015     | Template paused                 | Fix the template quality or create a new template. Do not retry.    |
| 133010     | Number not registered           | Complete phone number registration first.                           |
| 190        | Invalid token                   | Refresh or regenerate the access token. Do not retry with the same token. |

### Recommended Backoff Implementation

```
Attempt 1: Wait 1 second
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds
...
Max wait: 60 seconds
Max attempts: 5 (for rate limits), 3 (for server errors)
```

Add jitter (random 0-500ms) to each wait interval to prevent thundering herd when multiple senders hit the rate limit simultaneously.

---

## Webhook Error Notifications

The API also delivers error notifications via webhooks when messages fail asynchronously (after the API returns a 200 response).

### Webhook Error Payload

```json
{
  "entry": [{
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "statuses": [{
          "id": "wamid.ABC123",
          "status": "failed",
          "timestamp": "1678901234",
          "recipient_id": "18091234567",
          "errors": [{
            "code": 131047,
            "title": "Re-engagement message",
            "message": "More than 24 hours have passed since the customer last replied.",
            "error_data": {
              "details": "Message failed to send because more than 24 hours have passed since the customer last replied to this number."
            }
          }]
        }]
      }
    }]
  }]
}
```

> **Important:** Always implement webhook error handlers in addition to synchronous API error handling. Some delivery failures are only reported asynchronously.

---

## Best Practices

1. **Log every error with `fbtrace_id`.** This is required for Meta support escalation.
2. **Categorize errors as retryable vs. non-retryable** before building retry logic. Retrying non-retryable errors wastes resources and can worsen quality ratings.
3. **Implement a dead-letter queue** for messages that fail after maximum retry attempts.
4. **Monitor rate limit errors (130429) as a capacity signal.** If they occur frequently, you need to distribute load across multiple phone numbers.
5. **Alert on quality rating changes.** A drop from GREEN to YELLOW should trigger an operational review before it reaches RED.
6. **Handle webhook errors separately from API errors.** A successful API response (200) does not guarantee delivery — always process asynchronous status webhooks.
