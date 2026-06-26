# Bug: Format Errors Incorrectly Cooldown Auth Profiles as Billing Errors

**Date:** 2026-04-12
**Author:** CC Mini (lesa-work-02)
**Severity:** Critical (cascading outage: single format error disables all models)
**Upstream:** OpenClaw (should be filed as issue on openclaw/openclaw)

## Summary

When the Anthropic API rejects a request with a format error (e.g., `messages.101: tool_use ids were found without tool_result blocks`), OpenClaw's auth-state system marks the auth profile with `disabledReason: "billing"` and puts it in cooldown. This is wrong. Format errors are payload errors, not profile/billing errors. The profile itself is fine.

## Impact

The incorrect billing classification cascades:

1. First Anthropic model fails with format error → profile cooldown set
2. Second Anthropic model (fallback) tries the same profile → skipped because "Provider anthropic has billing issue (skipping all models)"
3. ALL Anthropic models become unusable even though the auth profile has valid credentials and billing

On Apr 11, this turned a single corrupt message (messages.101) into a total outage across all 3 fallback models:
- anthropic/claude-sonnet-4-6: format error → cooldown
- xai/grok-4.20: 429 rate limit (separate issue)
- anthropic/claude-haiku-4-5: SKIPPED because "Provider anthropic has billing issue" (cascade from sonnet's format error)

## Expected Behavior

Format errors (400 `invalid_request_error`) should be classified as `reason: "format"` in the failover system, NOT as `reason: "billing"`. They should NOT disable the auth profile or cooldown the provider. The specific request should fail, not all future requests to the same provider.

## Actual Behavior (from gateway.err.log)

```
[agent] auth profile failure state updated: profile=sha256:ae51d6f852f6 provider=anthropic reason=format window=cooldown
[model-fallback] decision=skip_candidate candidate=anthropic/claude-haiku-4-5 reason=billing detail=Provider anthropic has billing issue (skipping all models)
```

The profile is set to `reason=format` but the skip cascade uses `reason=billing`. Something in the failure propagation converts format errors to billing classifications.

## Location in Source

- `src/agents/pi-embedded-runner/model.ts`: throws "Unknown model" errors that cascade
- Auth-state management: `~/.openclaw/agents/main/agent/auth-state.json`
- Failover logic: likely in `src/agents/failover-error.ts` or `pi-embedded-helpers.ts`

## Workaround

Clear billing flags manually:
```bash
perl -i -pe 's/"disabledReason":\s*"billing"/"disabledReason": null/g' ~/.openclaw/agents/main/agent/auth-state.json
openclaw gateway restart
```

This was done 3 times on Apr 11 during the outage.

## Fix

In OpenClaw's failover classification logic: format errors (HTTP 400, `invalid_request_error`) should NOT set `disabledReason: "billing"` on the auth profile. They should be classified as transient request-level errors that don't affect the profile's availability for subsequent requests.
