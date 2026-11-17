# Runtime Status And Errors

Use this reference for authentication, environment selection, pagination, timeout, retry, cache, partial success, and normalized errors.

## Runtime Request Rules

- Skill calls only `scripts/invoke.sh`, which calls `yeelight-home invoke --stdin`.
- Region, endpoint, credential store, pagination, timeout, and cache policy are Runtime concerns.
- The model must not set endpoint URLs, headers, operation names, retry counts, cache TTLs, or network policy.
- Reads may be paginated by Runtime. The user-facing answer should summarize the returned result, not page mechanics.
- Do not blindly retry writes. If Runtime reports uncertainty, explain `partial` or `blocked` as returned.
- Runtime owns long-lived topology caching for rooms, devices, groups, scenes, and automations. Direct control and state/scene execution use the cache automatically to resolve "which entity" and refresh once on cache miss.
- Topology cache is not live state. When the user asks for current power, brightness, online status, or other real-time values, use `state.query` or the relevant live read intent; do not answer current state from cached topology fields.
- Runtime owns the selected current home in the active profile. When `lighting.design.import` creates a new home, Runtime returns `selectedHouseId` and updates the active profile; later house-scoped calls should rely on that context unless the user names another home.
- Diagnosis and detail questions may benefit from cached target resolution, but the answer must come from Runtime's live read evidence in the response, not from cached entity summary fields alone.
- Runtime stores topology cache and local memory in profile/region/house scoped local shards internally. Do not add account, region, or home lookup turns only to choose cache or memory files.
- After successful or partial house-scoped writes, Runtime refreshes or invalidates topology cache from its write-after-read verification path. Do not issue a separate `entity.list` only to warm or refresh cache.
- For fast user experience, ordinary control should go directly to the final Runtime intent with target words and room qualifiers. Runtime will use cached topology and return `clarification_required` only when the target is genuinely missing or ambiguous.
- `operation.batch.configure` is the low-friction path for one user request with multiple allowlisted add/update/configure steps. Runtime executes the allowlisted batch directly and may return `partial` if a later step fails.
- Do not put account-scoped `home.create` inside `operation.batch.configure`; create/select the home first, then batch the house-scoped configuration steps against that home.
- Do not create/select a home before a full new-home lighting design import. Use `lighting.design.import` with no `houseId`; it creates and selects the home in one Runtime call.

## Status Handling

| Runtime status | Skill behavior |
| --- | --- |
| `success` | State the actual result. |
| `partial` | State what succeeded, what did not, and any returned safe next step. |
| `clarification_required` | Ask exactly the smallest returned clarification question. |
| `auth_required` | Tell the user to run the local QR login command; if QR is unavailable, tell them to import an already authorized token in their own terminal with `auth token set --stdin`; do not request secrets. |
| `blocked` | Explain the returned reason and safe alternative. |
| `not_supported` | Explain the unsupported capability without attempting unsupported fallback. |
| `error` | Report the redacted message and avoid guessing cause or success. |

## Structured Clarification

- If Runtime clarification contains `payloadShape`, `examples`, or `nextStep`, treat those fields as the machine-readable call contract.
- Use that contract to repair the next SkillRequest when the missing information can be derived from current context or from a Runtime read such as `scene.detail.get` or `automation.detail.get`.
- Do not tell the user that the payload shape is unknown when Runtime has returned `payloadShape` or `editablePayload`.
- Ask the user only when the contract still lacks a business choice that cannot be inferred, such as which scene action to edit among multiple plausible actions.
- For complex JSON writes such as scene, automation, lighting design import, operation batch, favorite batch, home sort, room batch, panel event, or knob configuration, do not guess nested field names. If the first request is rejected, rebuild from Runtime's returned `payloadShape`, `examples`, `nextStep`, or detail `editablePayload`, then send one corrected Runtime request.
- `acceptedFields` alone is not enough for nested writes. When nested action, condition, room, item, button-event, or operation fields are involved, inspect Runtime's nested `payloadShape` or detail `updateShape` before answering the user. If Runtime failed to include nested shape for a supported complex write, report that as a Runtime contract problem instead of guessing the complete JSON.
- If the shape is unclear before a write, call local-only `intent.explain`; in its parameters object, set the `intent` field to the target Runtime intent. In `invoke --stdin` responses, use `result.intentExplanation.payloadGuide`, `result.intentExplanation.requestSchema.examples`, and `result.intentExplanation.acceptedFields` as the objective contract. This does not require cloud access and should be faster than repeated failed writes.
- For read-modify-write flows, `scene.detail.get` and `automation.detail.get` `editablePayload` are the source payloads. Preserve them, apply the minimal intended edit, and resend a complete update payload.

## Dry-Run Preview

- Use `options.dryRun=true` or wrapper/CLI `--dry-run` only when a no-write preview is useful before user confirmation.
- Dry-run preview is not a stored operation. It exists only to help the caller explain the planned Runtime request before resending without dry-run.
- After the user agrees, resend the same Runtime request without dry-run. Keep the user's original wording and targets stable.
- If Runtime reports `profile_mismatch`, `region_mismatch`, missing house context, or validation errors, ask the smallest clarification or regenerate the Runtime request in the current context.

## Runtime Missing

- If `scripts/invoke.sh` returns `error.code=runtime_missing`, the local `yeelight-home` CLI is not available to the Skill.
- Tell the user to install `yeelight-home` from the public `yeelight/yeelight-home` release or a currently available package manager. Currently available guidance names are GitHub Releases, Homebrew, Scoop, Debian package, and npm; Winget can be mentioned only after its registry shows the package is published.
- If the user already installed the CLI in a non-PATH location, tell them to set `YEELIGHT_HOME_BIN` to the absolute executable path.
- After installation, ask the user to run `yeelight-home auth status --json`; if not logged in, use `yeelight-home auth login --qr`. If QR is unavailable, use `printf '%s' "$YEELIGHT_TOKEN" | yeelight-home auth token set --stdin --region <region>` in the user's own terminal for explicit local token import outside chat.
- Do not suggest bypass commands, internal requests, keys, or external services as a workaround.

## Error Rules

- Missing credentials are handled locally with the Runtime login flow.
- Ambiguous or unknown targets should become one clarification question, not guessed IDs.
- Business failures must stay redacted; do not expose full low-level envelopes, identifiers, or token-like values.
- App-only, LAN-only, BLE-only, QR, pairing, or credential-sensitive flows must become Runtime guidance or blocks.
- Write verification mismatch is a partial outcome until Runtime returns a definitive state.
- `not_supported` with `error.code=unsupported_intent` means the requested intent is not executable in the public Runtime catalog. Use a supported catalog intent or `intent.explain`; do not retry guessed intent names.
