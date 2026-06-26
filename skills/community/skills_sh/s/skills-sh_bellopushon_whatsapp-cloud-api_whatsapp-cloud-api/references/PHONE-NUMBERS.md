# WhatsApp Cloud API - Phone Numbers Reference

> **Author:** Bello Sanchez
> **API Version:** v21.0
> **Last Updated:** 2026-02-09

---

## Overview

This document covers phone number formatting, identification fields, registration, and verification for the WhatsApp Cloud API. Correct handling of phone numbers is critical for message delivery, webhook processing, and customer identification.

---

## E.164 Format (Required for Sending)

All phone numbers sent through the API **must** use E.164 international format:

```
+{country_code}{subscriber_number}
```

### Rules

- Must start with `+` followed by the country code.
- No spaces, dashes, parentheses, or other formatting characters.
- Country code is mandatory.

### Examples

| Country              | E.164 Format     | Notes                          |
|----------------------|------------------|--------------------------------|
| Dominican Republic   | +18091234567     | Country code +1, area code 809 |
| United States        | +16505551234     | Country code +1                |
| Mexico (mobile)      | +5215551234567   | Country code +52, prefix 1     |
| Puerto Rico          | +17871234567     | Country code +1, area code 787 |
| Spain                | +34612345678     | Country code +34               |
| Brazil               | +5511912345678   | Country code +55               |

---

## Phone Number Identifiers

The API uses three distinct identifiers for phone numbers. Confusing them is a common source of bugs.

| Field                  | Format             | Example            | Where Used                        |
|------------------------|--------------------|--------------------|-----------------------------------|
| `phone_number_id`      | Numeric string     | `"106540352242922"` | API endpoint paths (sending)     |
| `display_phone_number` | E.164 with `+`     | `"+16505555555"`   | Meta Business Manager display     |
| `wa_id`                | Digits only (no +) | `"18091234567"`    | Webhook payloads, API responses   |

### Key Distinctions

- **`phone_number_id`**: An internal Meta identifier assigned to your business phone number. Used in all API endpoint paths (e.g., `POST /{phone_number_id}/messages`). This is NOT the phone number itself.
- **`display_phone_number`**: The human-readable business phone number as shown in Meta Business Manager. Includes the `+` prefix.
- **`wa_id`**: The canonical WhatsApp identifier for a customer's phone number. Always digits only, never includes `+`. This is what the API returns in webhook contact objects and message responses.

### Normalization Behavior

The API normalizes all input phone numbers to their canonical `wa_id` format:

| Input Sent          | Returned `wa_id`  |
|---------------------|--------------------|
| `+1 (809) 123-4567` | `18091234567`     |
| `+1-809-123-4567`   | `18091234567`     |
| `18091234567`        | `18091234567`     |
| `+18091234567`       | `18091234567`     |

> **Important:** Always store `wa_id` (digits only) as the canonical customer identifier in your database. When comparing phone numbers, strip all formatting and compare digit strings.

---

## Phone Number Registration

A phone number must be registered with the Cloud API before it can send or receive messages.

### Registration Flow

1. **Add the phone number** to your WhatsApp Business Account via Meta Business Suite.
2. **Verify ownership** via SMS or voice call verification code.
3. **Register for Cloud API** messaging through the API or Business Manager.
4. **Retrieve the `phone_number_id`** from the API response or Business Manager settings.

### Registration Endpoint

```
POST https://graph.facebook.com/v21.0/{phone-number-id}/register
```

| Header          | Value                    |
|-----------------|--------------------------|
| `Authorization` | `Bearer {access-token}`  |
| `Content-Type`  | `application/json`       |

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "pin": "123456"
}
```

| Field                | Type   | Required | Description                            |
|----------------------|--------|----------|----------------------------------------|
| `messaging_product`  | string | Yes      | Must be `"whatsapp"`.                  |
| `pin`                | string | Yes      | 6-digit two-step verification PIN.     |

---

## Two-Step Verification

Two-step verification adds a 6-digit PIN requirement to your business number registration, preventing unauthorized re-registration.

### Set or Update PIN

```
POST https://graph.facebook.com/v21.0/{phone-number-id}
```

```json
{
  "pin": "123456"
}
```

### Important Notes

- The PIN is required during number registration and re-registration.
- If you lose the PIN, you must contact Meta support to reset it.
- Two-step verification is strongly recommended for all production numbers.

---

## Retrieving Phone Number Details

### Get a Specific Phone Number

```
GET https://graph.facebook.com/v21.0/{phone-number-id}
```

### Response

```json
{
  "id": "106540352242922",
  "display_phone_number": "+16505555555",
  "verified_name": "My Business",
  "quality_rating": "GREEN",
  "messaging_limit": "TIER_2",
  "platform_type": "CLOUD_API",
  "code_verification_status": "VERIFIED"
}
```

### List All Phone Numbers for a WABA

```
GET https://graph.facebook.com/v21.0/{waba-id}/phone_numbers
```

Returns all phone numbers registered under the WhatsApp Business Account.

---

## Quality Rating and Messaging Limits

Each phone number has a quality rating that affects messaging capacity.

| Quality Rating | Impact                                    |
|----------------|-------------------------------------------|
| GREEN (High)   | Number is performing well. Can tier up.   |
| YELLOW (Medium) | Quality declining. Tier maintained.      |
| RED (Low)       | Poor quality. Tier may decrease.         |

Messaging tier upgrades happen automatically when:
- Quality rating remains GREEN.
- The number reaches the current tier's daily limit.
- The number has been active for at least 7 days.

---

## Best Practices

1. **Always store `wa_id` as the canonical identifier.** Never store formatted numbers as the primary key.
2. **Normalize before comparing.** Strip all non-digit characters and compare digit strings when looking up customers.
3. **Validate E.164 format before sending.** Reject any number that does not match `^\+[1-9]\d{1,14}$`.
4. **Never hardcode `phone_number_id`.** Store it in environment variables or configuration. It changes if you re-register the number.
5. **Monitor quality rating.** A drop to RED can severely limit your messaging capacity and pause your templates.
6. **Use two-step verification.** It prevents unauthorized re-registration of your business number.
