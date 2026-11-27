# Tool catalog (member view)

These are the tools a customer account sees. The list is not fixed: it follows the
role and the scopes of the account and it changes with every release.

- **How many does my account see?** `auth_status` returns `tools_visible` for your
  account. The service reports the catalogue size under `/health`.
- **Never quote a number from a document.** Both values move; the tool that tells you
  the truth is the one you can call right now.
- **Visibility is not permission.** Whether a call is executed depends on your right
  on the scope (`read`, `write`, `manage`). The service checks on every call.
- **Without a token** only the onboarding tools are callable: `register`, `activate`,
  `login`, `refresh_access_token`, `auth_status`, `onto_credit_pricing`. A client that
  insists on `tools/list` before the first call gets no catalogue at all in that state —
  so the first call has to know these names.

Schema changes (object types, property definitions, link types) are the platform
operator's job; a member agent asks for them. Everything in this catalogue is what
you can do yourself.

## Base tools

| Tool | Roles | Purpose |
|---|---|---|
| `auth_status` | public | Diagnosis: token valid? which roles? what to do? |
| `login` | public | client_id + client_secret → bearer token |
| `refresh_access_token` | public | Renew token (no password) |
| `register` | public | Create account (human: `username`+voucher · agent: `invite_code`) |
| `activate` | public | Redeem voucher (e-mail path only; omitted for an invitation code) |
| `onto_credit_pricing` | public | Read prices |
| `get_image` | `member` | Download image/file |
| `get_document` | `member` | Download document |
| `upload_file_to_object` | `member` | File/image to an object (also `structuredimage`) |
| `upload_staging_csv` | `member` | CSV into the import staging store |
| `upload_code_allowlist` | `member` | XLSX/XLS bulk of the e-mail allowlist of an invite code |
| `change_password` | `member` | Change password |
| `change_profile` | `member` | Change profile (without arguments: **read** profile) |
| `get_profile` | `member` | Fetch own profile purely read-only — no write path |
| `renew_account` | `member` | Renew account |
| `get_notifications` | `member` | Notifications |

## Tool catalog of the ontology endpoints

### `onto_object_*`

| Tool | Roles |
|---|---|
| `onto_object_addcomment` | `member` |
| `onto_object_bulk_action` | `member` |
| `onto_object_create` | `member` |
| `onto_object_create_link` | `member` |
| `onto_object_delete` | `member` |
| `onto_object_delete_link` | `member` |
| `onto_object_delete_property` | `member` |
| `onto_object_execute_action` | `member` |
| `onto_object_geocode` | `member` |
| `onto_object_graph` | `member` |
| `onto_object_index` | `member` |
| `onto_object_search` | `member` |
| `onto_object_set_property` | `member` |
| `onto_object_show` | `member` |
| `onto_object_update` | `member` |
| `onto_object_update_link` | `member` |

### `onto_type_*`

| Tool | Roles |
|---|---|
| `onto_type_show` | `member` |

### `onto_property_def_*`

| Tool | Roles |
|---|---|
| `onto_property_def_create` | `member` |
| `onto_property_def_delete_override` | `member` |
| `onto_property_def_update` | `member` |

### `onto_property_set_*`

| Tool | Roles |
|---|---|
| `onto_property_set_create` | `member` |
| `onto_property_set_update` | `member` |

### `onto_interface_*`

| Tool | Roles |
|---|---|
| `onto_interface_map_markers` | `member` |
| `onto_interface_show` | `member` |

### `onto_actiondef_*`

| Tool | Roles |
|---|---|
| `onto_actiondef_delete` | `member` |
| `onto_actiondef_list` | `member` |
| `onto_actiondef_save` | `member` |

### `onto_scope_*`

| Tool | Roles |
|---|---|
| `onto_scope_save_structuredimage_categories` | `member` |
| `onto_scope_structuredimage_categories` | `member` |

### `onto_report_*`

Reading is for members. **Building is not:** `save`, `copy` and `delete` answer 403 for a
member, and the platform has no member-facing report editor. A member agent that needs a report
orders it through the service channel — capabilities, examples and the request template:
[reports.md](reports.md).

| Tool | Roles |
|---|---|
| `onto_report_aggregate` | `member` |
| `onto_report_csv` | `member` |
| `onto_report_index` | `member` |
| `onto_report_json` | `member` |
| `onto_report_map_data` | `member` |
| `onto_report_show` | `member` |
| `onto_report_save` | `admin` |
| `onto_report_copy` | `admin` |
| `onto_report_delete` | `admin` |

### `onto_catalog_*`

| Tool | Roles |
|---|---|
| `onto_catalog_apply` | `member` |
| `onto_catalog_clear` | `member` |
| `onto_catalog_index` | `member` |
| `onto_catalog_presets` | `member` |

### `onto_i18n_*`

### `onto_favorite_*`

| Tool | Roles |
|---|---|
| `onto_favorite_add` | `member` |
| `onto_favorite_delete` | `member` |
| `onto_favorite_index` | `member` |
| `onto_favorite_toggle` | `member` |

### `onto_startcard_*` (team start cards)

| Tool | Roles |
|---|---|
| `onto_startcard_index` | `member` |
| `onto_startcard_save` | `member` |
| `onto_startcard_delete` | `member` |
| `onto_startcard_move` | `member` |

Write access is additionally gated by `can_manage_scope` on the card's scope. The cards carry
no roles of their own: a card is visible to everyone who can read the scope and see the target
interface.

### `onto_file_*`

| Tool | Roles |
|---|---|
| `onto_file_delete` | `member` |
| `onto_file_structured` | `member` |

### `onto_series_*` (sensor time series)

| Tool | Roles |
|---|---|
| `onto_series_range` | `member` |
| `onto_series_last` | `member` |

A series has **no udid of its own** — its identity is the pair
`(object_udid, series_key)`. The `series_key` is the same string as the key of the associated
property; the property is the **pointer** to the series (def field `computed = {"series": true}`),
its value does not carry it. Which series an object has is named by `onto_object_show` in the field
`series_keys`.

Visibility follows the **scope of the property**, not of the object (fail-closed) —
a foreign scope returns 403 even though the tool is visible.

**All timestamps are UTC**; this applies to `points[].ts`, `series_ts` **and** to the `from`/`to`
parameters. The series endpoints answer in ISO 8601 with `Z` (`2026-10-06T23:09:00Z`); plain object
fields come back without a suffix (`2026-11-25 19:40:42`) — same instant, no conversion. Details and use cases:
`references/features/sensor-time-series.md`.

### `onto_trigger_*`

| Tool | Roles |
|---|---|
| `onto_dispatch_status` | `member` |
| `onto_trigger_create` | `member` |
| `onto_trigger_delete` | `member` |
| `onto_trigger_index` | `member` |
| `onto_trigger_update` | `member` |

### `onto_function_*`

| Tool | Roles |
|---|---|
| `onto_function_create` | `member` |
| `onto_function_delete` | `member` |
| `onto_function_index` | `member` |
| `onto_function_run` | `member` |
| `onto_function_update` | `member` |

### `onto_credit_*`

| Tool | Roles |
|---|---|
| `onto_credit_balance` | `member` |
| `onto_credit_chargeup` | `member` |
| `onto_credit_checkout` | `member` |
| `onto_credit_receipt` | `member` |

### `onto_watch_*`

| Tool | Roles |
|---|---|
| `onto_watch_changes` | `member` |
| `onto_watch_cursor` | `member` |

### `ontouser_scope_*`

| Tool | Roles |
|---|---|
| `ontouser_scope_assign_public` | `member` |
| `ontouser_scope_create` | `member` |
| `ontouser_scope_index` | `member` |
| `ontouser_scope_list_public` | `member` |
| `ontouser_scope_remove_public` | `member` |
| `ontouser_scope_set_visibility` | `member` |

### `ontouser_team_*` — managed accounts

The manager view of an account that is managed by a company scope (`managed_by_scope_id`).
Every tool needs `can_manage_scope` in the scope that carries the marker, plus the respective right.

| Tool | Roles |
|---|---|
| `ontouser_team_index` | `member` |
| `ontouser_team_show` | `member` |
| `ontouser_team_suspend` | `member` |
| `ontouser_team_unsuspend` | `member` |
| `ontouser_team_update_profile` | `member` |
| `ontouser_team_set_scope_rights` | `member` |
| `ontouser_team_set_write_scope` | `member` |
| `ontouser_team_credits` | `member` |
| `ontouser_team_transfer` | `member` |
| `ontouser_team_offboard_preview` | `member` |
| `ontouser_team_offboard` | `member` |

Notes an agent must not guess:

- **The marker grants nothing.** `managed_by_scope_id` only says who leads the account; every call
  still checks `can_manage_scope` and the specific right.
- **Only your own managed accounts.** Any other profile answers `403`. The manager himself never
  appears in his own list (he carries no marker).
- **`ontouser_team_transfer` books from the caller's own balance** — there is no `from_profile_id`.
  `reason` and `idempotency_key` are mandatory; a repeated key returns `schon_gebucht: true`
  instead of booking twice. Insufficient balance answers `402`.
- **`ontouser_team_set_scope_rights` sets, it does not only escalate.** All three flags `0` removes
  the membership. `can_manage_scope` on the managing scope itself is rejected (`403`) — that needs
  an invite code with `can_manage_scope`.
- **`ontouser_team_suspend`** removes `member` and deletes all tokens; a suspended account gets
  `403 account_suspended` from the token endpoint, so the reason is visible.
- **`ontouser_team_offboard`** defaults to `mode=delete`; `release` keeps the account alive and
  notifies the managers of foreign scopes. Remaining credits go back to the manager unless
  `keep_balance` is set. The last manager of a scope cannot be deleted, and a scope that carries
  managed accounts cannot be deleted (not even with `purge`).
- **Invite code type `revoke`** takes rights away (`can_read`/`can_write`/`can_manage_scope` on the
  code say which; all zero removes the membership). Grant codes only escalate — revoking is always a
  separate, explicit code.

### `ontouser_interface_*`

| Tool | Roles |
|---|---|
| `ontouser_interface_map_markers` | `member` |
| `ontouser_interface_show` | `member` |

### `ontouser_notification_*`

| Tool | Roles |
|---|---|
| `ontouser_notification_index` | `member` |
| `ontouser_notification_read` | `member` |
| `ontouser_notification_send` | `member` |

`ontouser_notification_send` writes into the inbox of a **different** account: `to` is the e-mail
of an existing account (own address allowed), `text` the message (over 4000 characters is
truncated). Response `{sent: true, to: …}`. The message runs through the same system as
service request replies (`type=user_message`) — platform inbox plus e-mail/push, **as far as the
recipient receives it**: at agent addresses the mail barrier prevents mail delivery, there it stays
with the message in the inbox (`ontouser_notification_index`).

### `ontouser_object_*`

| Tool | Roles |
|---|---|
| `ontouser_object_show` | `member` |

### `ontouser_service_*`

| Tool | Roles |
|---|---|
| `ontouser_service_request` | `member` |

### Forms & invite/members (without name prefix)

| Tool | Roles |
|---|---|
| `add_code_allowlist_entry` | `member` |
| `create_invite_code` | `member` |
| `delete_code_allowlist_entry` | `member` |
| `list_code_allowlist` | `member` |
| `list_formdefs` | `member` |
| `list_invite_codes` | `member` |
| `list_members` | `member` |
| `onto_formdef_create` | `member` |
| `onto_formdef_list_templates` | `member` |
| `onto_formdef_save` | `member` |
| `prepare_form_answer` | `member` |
| `redeem_invite_code` | `member` |
| `remove_member` | `member` |
| `resolve_form_answer` | `member` |
| `revoke_invite_code` | `member` |
| `show_form_answer` | `member` |
| `show_formdef` | `member` |
| `submit_form_answer` | `member` |
| `toggle_member_flag` | `member` |

## Timestamps — UTC, in two shapes

**Every timestamp this service returns is UTC.** Object fields come back bare, without a zone
suffix — measured 2026-11-25: `"modified_datetime": "2026-11-25 19:40:42"` plus
`"modified_datetime_local": "2026-11-25T20:40:42+01:00"`; property values pair `value` with
`value_local`. Some endpoints answer in ISO 8601 with `Z`; it is the same instant. Treat a value
without suffix as UTC when **reading** — but send `Z`/an offset when **writing**, because a naive
input is read in the viewer's zone.

- **Do not convert yourself.** Anyone converting UTC to a local time in order to compare two values
  builds in the very error the conversion was supposed to avoid. Compare UTC with UTC.
- **Series windows (`from`/`to` on `onto_series_range`) are UTC, with or without a zone.**
  Measured 2026-11-25: `2026-11-24 09:56:24` and `2026-11-24T09:56:24Z` return the identical window;
  an appended offset (`+02:00`) is converted.
- **Property writes are different:** there a value without a zone is read in the viewer's zone
  (see the top of this section). That is the one place where `Z`/an offset is not optional.
- **The web view, by contrast, shows viewer time.** If the interface shows `01:09` and the API
  `23:09`, both are correct — that is a 2-hour zone difference, not an error.
- **Compute a duration** always from two UTC values from **the same** source.

## Pitfalls

1. **A missing tool is usually a permission problem, not a bug.** Visibility is filtered per request
   against the roles. Call `auth_status` first — the response names the roles in
   plain text.
2. **Tool names end in `_create`/`_update`/`_delete`, NOT `_save`** (`onto_trigger_*`,
   `onto_function_*`). Anyone searching for `_save` falsely reports „Tool fehlt".
3. **Two name families for the same thing**: `ontouser_scope_*` is the self-service family for
   your own scopes — use that one. Both paths bill and count against the account's scope
   quota (`max_scopes`).
4. **The order of tools in the catalog is not a priority.** The list is grouped by resource;
   choosing the right path is described in `references/features/`.
5. **A wrong role assignment is silent.** If a tool becomes visible to more accounts than
   intended or invisible to all, there is no error message and no log entry.
   The check is the number from `auth_status` (`tools_visible`) — after every permission change
   compare it against the target value.
6. **Parameters are documented in the tool schemas, not here.** When unsure,
   look at `tools/list` for the specific tool — the `description` contains the verified
   body format and the required fields.
7. **Your own number comes from `auth_status`.** `tools_visible` applies to the logged-in
   account; after every permission change compare it anew instead of deriving it from this catalog.
8. **Compare with `auth_status`, not with this file.** `tools_visible` is the number for the
   logged-in account, and it changes with role and scope changes. After every permission
   change, read it again.

## Tool descriptions and annotations

Every tool has a **descriptive description** (verb + resource + when/when not + named
alternative) and **MCP annotations** (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
`openWorldHint`). A tool without a description and without annotations is hardly
selectable for a model — both are part of it.

The descriptions are maintained centrally and are read in at startup. They can therefore be
changed without touching the tool definitions.

## Connections and outbox (since 2.3.3)

Five tools expose the write-back building blocks (*Anbindungen*) that previously existed only
in the web UI:

| Tool | Method/path | Role | Purpose |
|---|---|---|---|
| `onto_connection_index` | GET `onto/credential/index` | member | list connections; secrets are never returned, only `secret_set` |
| `onto_connection_save` | POST `onto/credential/save` | member | create **or change** a connection (same `target_key` replaces, id stays) |
| `onto_connection_remove` | POST `onto/credential/remove` | member | delete by `id`; foreign connections answer 404 |
| `onto_connection_check` | GET `onto/credential/check` | member | vault self-test: key loaded, encrypt/decrypt round trip |
| `onto_outbox_index` | POST `onto/outbox/index` | admin | inspect the delivery queue (status, attempts, response_code, last_error) |
| `onto_outbox_preview` | POST `onto/outbox/preview` | admin | dry run of an `http_call`; `send=1` would really send |
| `onto_outbox_retry` | POST `onto/outbox/retry` | admin | resend a single row immediately |

The effect type is `http_call` inside a trigger's `effects`:

```json
{"type":"http_call","target":"<target_key of a connection>","method":"POST",
 "path":"/api/x","body":{"udid":"{udid}"},"shadow":true,"timeout":10}
```

Placeholders: `{udid}`, `{object_id}`, `{action}` and any property as `{property}`.
`shadow: true` only logs. Without a resolvable acting identity the effect is refused
(fail-closed) and logged as `effect_config_error`.

Notes that cost time if unknown:

- `credential/index` must be called with **GET**; a POST with an empty body answers
  "Ungültiger Request-Body", which looks like a permission error.
- `outbox/preview` is **not** side-effect free: it creates an outbox row. Without a matching
  connection the row is immediately `dead` with "kein Credential fuer Ziel ...".
- Changing a connection = `save` with the same `target_key`. There is no update call and no
  history.
