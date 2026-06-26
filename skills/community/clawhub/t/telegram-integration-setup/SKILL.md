---
name: telegram-integration
description: Configure and troubleshoot OpenClaw Telegram integrations for new bots, DMs, groups, and topic-enabled supergroups. Use when setting up Telegram routing, onboarding a new bot/group/chat, enforcing allowlists or mention-gating, finding chat IDs/thread IDs, validating account-scoped policy, or diagnosing why Telegram messages are skipped or not replied to.
---

# Telegram Integration

## Overview
Set up Telegram safely and repeatably across machines by following a fixed integration checklist, policy model, and troubleshooting flow.

## Quick Workflow

1. Confirm integration scope: DM only, groups only, or both.
2. Configure account-level Telegram policy first (DM/group policy and allowlist stance).
3. Add chat targets (DM/group) in the correct config scope.
4. For topic-enabled groups, capture both `chat_id` and `message_thread_id` and apply thread rules if needed.
5. Enforce mention-gating and sender allowlists as required.
6. Reload/restart gateway and verify with a real Telegram test message.
7. If no reply, run the troubleshooting section in order.

## Integration Rules

### 1) Use the correct config scope
Always keep policy and targets aligned:
- Global Telegram settings define defaults.
- Account-scoped settings define what each bot account can respond to.
- Group or topic entries are only effective if the active account policy allows them.

If policy is `allowlist`, ensure the target chat is explicitly allowlisted in the same account scope used by the bot.

### 2) Require mention-gating for groups by default
For group chats, prefer `requireMention: true` unless the use-case demands ambient replies.

This reduces accidental triggers and cross-talk in busy groups.

### 3) Topic-enabled groups need thread awareness
For supergroups with topics enabled:
- `chat_id` identifies the group.
- `message_thread_id` identifies the topic thread.

If behavior is thread-specific, configure topic-level routing/policy instead of assuming group-level config is enough.

### 4) Bot permissions in Telegram group
When adding the bot to a topic-enabled group, grant admin rights needed for reliable topic behavior.

Minimum recommended permissions:
- Manage Topics
- Send Messages (and related basic messaging permissions)

Without topic management capability, behavior in topic threads can be inconsistent.

### 5) Multi-account bots
If multiple Telegram bot accounts are configured:
- Verify message routing lands on the intended account.
- Duplicate required allowlist entries per account when policies are account-scoped.
- Avoid assuming global group entries automatically authorize all accounts.

## ID Discovery (No Secrets)

### Get `chat_id`
Use one of:
- Telegram `getUpdates` flow after sending a message that the bot can observe.
- Telegram message-link conversion (`/c/<id>/...` => `-100<id>` for supergroups).

### Get `message_thread_id`
For topic-enabled groups, extract the topic/thread id from update payloads or message link/thread metadata.

## Verification Checklist
After any change, validate in this order:

1. Bot account token resolves and account is active.
2. Target chat is present in the correct account scope.
3. Policy (`allowlist` vs `all`) matches intended behavior.
4. `requireMention` matches your test message format.
5. Sender is permitted by allowFrom rules (global/account/group/topic as used).
6. Gateway reload/restart completed.
7. Fresh Telegram test message confirms end-to-end reply.

## Troubleshooting: "Message received but no bot reply"
Follow in strict order:

1. Check logs for skip reasons (`not-allowed`, missing mention, policy mismatch).
2. Confirm target group is allowlisted under the active Telegram account.
3. Confirm sender allowlist rules include the sender at the effective policy layer.
4. Confirm mention requirement is satisfied in the test message.
5. For topic groups, verify topic/thread id handling and topic permissions.
6. Check for Telegram API polling conflicts (`409 getUpdates conflict`) indicating multiple bot instances polling the same token.
7. Re-test after reload/restart and inspect new logs only (avoid stale conclusions).

## Safe Defaults

- DM policy: allowlist unless open intake is explicitly needed.
- Group policy: allowlist + mention required.
- Narrow sender allowlists at the smallest practical scope.
- Prefer account-scoped group authorization for multi-bot setups.
- Keep one active poller/webhook path per bot token to prevent update conflicts.

## Reuse Pattern for New Machines

When migrating or onboarding a new host:

1. Apply baseline Telegram policy template.
2. Register bot account(s).
3. Add DM/group targets with explicit account scoping.
4. Apply mention and allowFrom constraints.
5. Validate with one DM and one group/topic test.
6. Capture final known-good config snippet for future reuse.
