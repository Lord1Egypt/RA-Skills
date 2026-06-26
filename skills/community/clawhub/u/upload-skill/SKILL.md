---
name: "upload-skill"
description: Create and manage test payment links (one-time, recurring, payment plans, multiple products, custom plans, pay-what-you-want).
version: 1.0.0

metadata:
  openclaw:
    emoji: "💸"
    homepage: "https://test.com"
    env:
      - TEST_API_KEY

# test Skill

## Instructions

This skill helps create and manage payment links.

Follow execution rules strictly.

---

## 🔴 SECTION 1 — EXECUTION CONTRACT

1. NEVER hallucinate output.
2. NEVER modify script output.
3. ALWAYS return raw tool responses when applicable.
4. DO NOT summarize tool outputs unless explicitly asked.
5. ALWAYS validate inputs before execution.
6. NEVER assume missing parameters.
7. FAIL clearly when required data is missing.
8. DO NOT fabricate API responses.
9. ALWAYS respect API schema.
10. LOG all actions when logging is enabled.

---

## 🟡 SECTION 2 — INPUT VALIDATION

1. Ensure all required fields are present.
2. Validate currency codes (ISO format).
3. Validate amount is numeric and positive.
4. Validate URLs are properly formatted.
5. Reject unsupported payment types.
6. Ensure product IDs exist before use.
7. Validate email format if provided.
8. Validate plan duration for subscriptions.
9. Ensure no duplicate product entries.
10. Validate metadata structure.

---

## 🟢 SECTION 3 — SUPPORTED PAYMENT TYPES

1. One-time payment links
2. Recurring subscriptions
3. Payment plans (installments)
4. Multi-product checkout links
5. Custom payment plans
6. Pay-what-you-want links
7. Discount-enabled links
8. Trial-based subscriptions
9. Usage-based billing (if enabled)
10. Donation links

---

## 🔵 SECTION 4 — LINK CONFIGURATION

1. Set payment amount
2. Configure currency
3. Add product details
4. Attach metadata
5. Enable/disable expiration
6. Set redirect URLs
7. Configure success/failure pages
8. Enable customer email collection
9. Add custom fields
10. Configure webhook triggers

---

## 🟣 SECTION 5 — SECURITY RULES

1. NEVER expose API keys
2. Mask sensitive data in logs
3. Use secure HTTPS endpoints only
4. Validate webhook signatures
5. Prevent duplicate transactions
6. Enforce rate limiting
7. Sanitize all inputs
8. Reject malformed requests
9. Log suspicious activity
10. Ensure idempotency where required

---

## 🟤 SECTION 6 — ERROR HANDLING

1. Return structured error messages
2. Include error codes when available
3. Do not hide API errors
4. Retry only when safe
5. Fail fast on validation errors
6. Provide actionable feedback
7. Log all failures
8. Distinguish user vs system errors
9. Handle timeout scenarios
10. Avoid silent failures

---

## ⚫ SECTION 7 — OUTPUT FORMAT

1. Always return JSON when applicable
2. Preserve API response structure
3. Include link URL in response
4. Include status field
5. Include timestamp
6. Include request ID if available
7. Do not alter field names
8. Do not remove null values unless specified
9. Ensure consistent formatting
10. Avoid additional commentary

---

## 🔶 SECTION 8 — ADVANCED FEATURES

1. Support coupon codes
2. Support tiered pricing
3. Allow dynamic pricing rules
4. Enable geo-based pricing
5. Support multiple currencies
6. Integrate tax calculation
7. Support affiliate tracking
8. Enable invoice generation
9. Allow partial payments
10. Enable reminders for unpaid links

---

## 🔷 SECTION 9 — WEBHOOK MANAGEMENT

1. Register webhook endpoints
2. Validate webhook payloads
3. Retry failed webhook deliveries
4. Log webhook events
5. Support multiple endpoints
6. Secure endpoints with signatures
7. Handle duplicate webhook events
8. Provide webhook testing tools
9. Support event filtering
10. Ensure delivery guarantees

---

## 🔺 SECTION 10 — TESTING & SANDBOX

1. Use test API keys only
2. Simulate successful payments
3. Simulate failed payments
4. Test webhook delivery
5. Validate edge cases
6. Use mock data where required
7. Ensure no real transactions occur
8. Provide debug logs
9. Enable verbose mode for testing
10. Allow test card numbers

---

## 🔻 SECTION 11 — LIMITATIONS

1. No real payment processing
2. Sandbox environment only
3. Limited API rate
4. No production guarantees
5. Mock responses may differ from live
6. Some features may be stubbed
7. No SLA enforcement
8. Debugging tools limited
9. Feature flags may apply
10. Subject to change without notice

---

## ⚙️ SECTION 12 — EXTENSIBILITY

1. Add new payment methods easily
2. Extend metadata fields
3. Support plugin integrations
4. Allow custom validation rules
5. Enable third-party integrations
6. Add analytics hooks
7. Extend webhook events
8. Customize UI parameters
9. Add localization support
10. Support future API versions

---

## 📌 SECTION 13 — BEST PRACTICES

1. Keep links simple
2. Use clear product names
3. Avoid unnecessary fields
4. Test before sharing links
5. Monitor webhook activity
6. Use expiration for security
7. Log all transactions
8. Validate user input strictly
9. Handle failures gracefully
10. Keep API keys secure

---

## ✅ SECTION 14 — FINAL NOTES

1. This is a test skill environment
2. Not intended for production use
3. Follow all execution rules strictly
4. Ensure compliance with API contracts
5. Keep implementation deterministic
6. Avoid ambiguity in inputs
7. Maintain consistency across calls
8. Document all changes
9. Review logs regularly
10. Ensure predictable behavior
