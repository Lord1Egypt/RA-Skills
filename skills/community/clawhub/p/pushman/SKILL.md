---
name: pushman
description: Safely send, inspect, and diagnose personal iPhone notifications through Pushman MCP tools or the installed Pushman CLI. Use when a request names Pushman, asks to notify the user from an agent or terminal workflow, targets Pushman devices, history, usage, login, pairing, authorization, or delivery diagnostics, or needs help configuring the local Pushman MCP server; do not use for implementing generic APNs/FCM push systems or operating unrelated notification services.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - pushman
---

# Pushman

Use Pushman to deliver notifications to the user's own receiving iPhone devices while preserving explicit send intent, credential boundaries, and quota semantics.

## Discover the available surface

1. Prefer connected tools named `pushman_send_notification`, `pushman_list_devices`, `pushman_list_history`, `pushman_get_message`, `pushman_get_usage`, `pushman_get_status`, and `pushman_doctor`. They use the locally configured Pushman CLI credential through `pushman mcp`.
2. If those tools are unavailable, resolve `pushman` from `PATH`. If it is absent, report the prerequisite and point to the [Pushman CLI installation guide](https://github.com/WhiteKiwi/pushman-cli/blob/main/docs/INSTALL.md); do not invent an installation method or credential.
3. Run `pushman version`, then read `pushman help <command>` before composing an unfamiliar or version-sensitive fallback command. This skill requires Pushman 0.1.0 or newer.
4. Do not manually exchange JSON-RPC frames when a client can connect the MCP server or the ordinary CLI can perform the task.

Use MCP for agent workflows because it publishes typed schemas, structured results, and safety annotations. Use the CLI for login, pairing, rename, logout, or when MCP is not connected.

## Classify authorization

- Read-only requests authorize only the narrowest matching status, device, usage, history, message, or doctor operation.
- A direct request to send an exact notification authorizes that one send. Do not add a redundant confirmation when the user already specified the send and its meaningful content.
- A request to draft, preview, configure, inspect, or explain a notification is not authorization to send it. Present the proposed body, title, targets, URL, and update key as applicable, then wait for confirmation.
- A general terminal or task-completion request does not authorize sending unrelated progress notifications. Send only when the user asked to be notified.
- Never broaden one send into repeated sends, additional devices, credential changes, authorization, or account operations.

Read [references/safety.md](references/safety.md) before sending, retrying, authorizing a CLI, revoking a credential, or handling an ambiguous delivery result.

## Send a notification

1. Preserve the user's content and scope. Do not invent a URL, image, target device, group, update key, or additional message text. Minor formatting that the user requested is allowed.
2. If specific devices matter and were not named, use `pushman_list_devices` or `pushman devices` and let the user choose. Omitting devices targets every currently eligible receiver.
3. Prefer `pushman_send_notification`. Provide only requested fields: required `body`, optional `title`, `subtitle`, `url`, `group`, HTTPS `image`, `sound` (`default` or `none`), `key`, `format` (`plain` or `monospace`), and `devices`.
4. For CLI fallback, use `pushman push -` and write the body on stdin so notification content does not enter process arguments or shell history. Pass optional fields as separate flags after consulting installed help. Never interpolate content into shell syntax.
5. Treat success only as server acceptance. Report the returned message ID and target-device count without claiming APNs delivery or that the user opened the notification.

Do not retry a rate-limited, timed-out, interrupted, or otherwise ambiguous send automatically. A retry may create another notification and consume another monthly send. A keyed update is still an accepted send and consumes quota.

## Inspect state and delivery

- Authorization state: use `pushman_get_status`; CLI fallback is `pushman status`.
- Devices: use `pushman_list_devices`; distinguish an eligible receiver from disabled or unavailable notification state.
- Monthly allowance: use `pushman_get_usage`; report used, limit, and reset time without predicting future paid-plan behavior.
- History: use `pushman_list_history` for the retained seven-day list. Use `pushman_get_message` only for a requested message or when its revisions and per-device delivery states are needed.
- Diagnostics: use `pushman_doctor` for credential and hosted-service connectivity. Preserve failed check names and messages without exposing credential material.

History and acceptance are server facts. A delivery state does not prove the user saw or opened a notification. Do not retrieve or repeat message bodies merely to confirm that history exists.

## Authorization and credentials

Read tools require an account CLI credential. `PUSHMAN_TOKEN` is process-scoped and send-only; it does not grant devices, history, usage, status, or doctor access.

- If the CLI is not authorized and read access is needed, offer the two explicit paths. `pushman login` uses Google or Apple in a browser and does not require the iPhone app during authorization. `pushman pair` requires approval in the signed-in iPhone app. Both issue the same account-scoped CLI credential.
- In an interactive terminal, `pushman login` may open the complete verification URL. Use `pushman login --no-browser` for SSH or headless workflows. The user may complete the printed code and URL on another device.
- Run `login` or `pair` only when the current request authorizes that credential change. Never treat displaying a code as approval, submit provider credentials for the user, or expose the device code or resulting bearer credential.
- Never request, display, copy, persist, or inspect the native keyring credential.
- Never place `PUSHMAN_TOKEN` in command arguments, source code, logs, chat, or checked-in MCP configuration.
- `pushman rename` changes the authorized sender nickname and `pushman logout` revokes the credential. Perform either only when explicitly requested; verify with `pushman status` afterward.
- To configure a local stdio client, use the installed client's supported MCP configuration with command `pushman` and arguments `mcp`. Do not expose the server over HTTP, a tunnel, or a public process supervisor.

## Finish with evidence

For a send, report acceptance ID, target count, and any warning or unknown delivery state. For inspection, report the exact queried scope and relevant server facts. For an authorization or credential mutation, verify the resulting status. Do not reproduce notification content, device nicknames, URLs, tokens, or credential values unless the user needs that exact value to complete the current request.
