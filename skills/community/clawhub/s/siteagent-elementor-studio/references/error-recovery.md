# When a write fails — errors, governance & self-correction

The fork surfaces structured errors designed for an agent to **recover from without
guessing**. Read the error, don't just report it. This file covers three families:
schema-in-error self-correction, governance (approval + rollback), and the numeric range
hints that keep values valid in the first place.

---

## 1. Schema-in-error — correct and retry in ONE round trip

The fork embeds the fix inside the error message, so you rarely need a second discovery
call. The MCP adapter drops `WP_Error` *data*, so the fork puts the recoverable detail in
the **message** — read it there.

### Wrong widget name → `invalid_widget_type` / `widget_not_found`

`add-widget` with an unknown type, and `get-widget-schema` for an unknown type, return an
error whose message carries the **nearest valid widget names inline**:

> `Widget type "headng" not found. Did you mean: heading, …?`

**Recovery:** parse the `Did you mean:` list, pick the intended name, retry with it. Don't
make a separate `list-widgets` call — the suggestions are already there (ranked exact →
substring → smallest edit distance). REST callers also get `data.suggestions` +
`data.schema_hint`.

### Bad atomic settings → `save_rejected`

When an Elementor 4 **atomic** widget rejects settings (`add-atomic-widget`,
`update-atomic-widget`, and the `add-atomic-*` helpers), the error carries the target
atomic type's **compact prop schema inline** — each prop as `{ type, enum? }` distilled
from Elementor's own `get_props_schema()`. e.g. an `e-heading` rejection tells you
`tag: {type:string, enum:[h1…h6]}`, `title: {type:html}`, `link: {type:link}`.

**Recovery:** read the inline prop schema, correct the offending settings to the right
`$$type`/enum, and re-send once. No `get-widget-schema` round trip needed.

### Non-atomic target → `not_atomic`

`apply-global-class`, `add-interaction`, and the other atomic-only writes reject a
non-atomic element with `not_atomic` and embed the element's **compact settings schema**
(`type`, `setting_keys`, `has_classes`). That tells you the element isn't atomic, so a
Global Class / Interaction can't bind to it — pick an atomic element instead, or convert
the section (see `v3-to-v4-conversion.md`).

### Invalid Global Class props → `invalid_styles`

`create-global-class` / `update-global-class` reject an unknown/mistyped style prop with
`invalid_styles`, embedding `rejected_props`, `type_mismatches`, and `allowed_props`.

**Recovery:** drop/rename the rejected props (or fix the type) and retry. Remember
`background-color` and flex `gap` are intentionally *not* accepted here — use `background`
and the structured layout, or set them via the dedicated atomic helpers.

---

## 2. Governance — approval grants & auto-rollback (opt-in)

**Only present when the [SiteAgent worker](https://github.com/Digitizers/SiteAgent)
(`digitizer-site-worker`) is installed** alongside the plugin. On a plain install none of
this fires and writes behave normally. All of it is **opt-in** — a bare SiteAgent install
does not gate Elementor writes until an operator turns it on.

Governance wraps page-data writes with **capture-before-write** snapshots plus two
optional gates. The error codes you may hit:

| Error code | What happened | What to tell the user / do |
|---|---|---|
| `governance_grant_required` | Grant enforcement is on, but the write carried no `X-Aura-Approval-Grant`. **The tool never ran.** | The write needs approval. The **gateway must mint a grant** bound to this tool + params; you can't self-fix it. Ask the user to approve, then the request is retried *with* the grant. |
| `governance_grant_invalid` | A grant was presented but rejected (bad signature, wrong tool/params/site binding, expired, or reused nonce). **The tool never ran.** | Same — a *fresh valid* grant is needed. Don't retry the same grant. |
| `governance_render_failed` | The write succeeded at the data layer but the page came back **broken** (HTTP 5xx or white screen), so it was **reverted to the pre-write snapshot**. | The page is safe (unchanged). **Do not blindly re-send the identical write** — it broke the page. Investigate the settings that caused it (often a bad value), fix, then try again. |
| `governance_rollback_failed` | A write failed (or render-reverted) **and the rollback itself failed** — the page may be **partially written**. | **Stop. Do not retry.** Surface this to the user with the snapshot id from the message; it must be restored manually. This is the one governance error you never auto-recover from. |
| `governance_snapshot_failed` | Governance couldn't snapshot before writing, so it **refused the write** (fail-closed — no blind mutation without a rollback point). | The page is unchanged. Report the reason; the write can be retried once the snapshot path works. |

Key facts that shape your response:

- **Grants are opt-in and gateway-minted.** Enforcement is OFF by default even when a
  SiteAgent gateway key exists. When on, a grant binds to the **exposed MCP tool name**
  (`/` → `-`, e.g. `elementor-mcp-update-element`) + exact params. An agent cannot forge
  one — approval is a human/gateway step.
- **Dry-run previews are exempt.** A preview-capable tool (one whose schema has an `apply`
  flag — the SEO/a11y generators) invoked with `apply` falsy writes nothing and needs no
  grant. Reach for a preview first when you just want to *show* a proposed change.
- **The render check is edits-only and fail-safe.** It reverts only when a
  *confirmed-healthy* page turns broken after the write. Transient/inconclusive probes
  never revert a good write, and create-style writes aren't render-checked.
- **Retry semantics summary:** `grant_*` → needs approval, not a code fix; `render_failed`
  → fix the content before retrying (the write was undone); `rollback_failed` → do not
  retry, escalate to the user with the snapshot id.

---

## 3. Numeric range hints — send valid values the first time

`get-widget-schema` now carries a control's own numeric bounds into the JSON Schema, so
you can pick a valid value without a second lookup:

- **`number` controls** emit `minimum` / `maximum` / `multipleOf` (from the control's
  `min` / `max` / `step` — unit-free, so unambiguous). A zero/omitted step is not emitted.
- **`slider` controls** expose a `unit` **enum** (the units the control offers) and, when
  the control offers exactly **one** unit, a `size` `minimum` / `maximum` from that unit's
  range. A multi-unit slider (bounds differ per unit, e.g. `px` 0–1000 vs `%` 0–100)
  leaves `size` unconstrained on purpose — don't assume a bound it didn't give you.

**Use them:** before setting a numeric/slider control on anything non-trivial, read the
schema and clamp your value to `[minimum, maximum]`, honor `multipleOf`, and pick a `unit`
from the enum. This avoids the value being silently clamped/dropped by Elementor.

> The fork's schema is also **richer than the bare `get_controls()` path** — it enables
> style/group controls *outside the editor* (`Performance::set_use_style_controls`), so
> typography/color/shadow controls appear in the schema even over the WP-CLI/stdio bridge.
> Trust `get-widget-schema` as the ground truth for a widget's real controls.
