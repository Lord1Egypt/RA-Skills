# Reusable traveler profile and local artifact storage

Read this reference when the user wants the agent to remember travel information, use a saved profile, or save a plan outside the current conversation.

## Consent and precedence

Explain the exact local location and fields before the first save. For a first-time user or a user with no valid profile, use the local profile HTML and require its explicit local-storage consent checkbox before saving. Do not silently create a profile. If the user declines, do not persist a profile. A current instruction always wins over a stored value. Confirm a profile summary before using it for a consequential recommendation.

Use only stable, travel-relevant fields: nationality, residence country and residence-status category, response/spoken languages, city/country and preferred departure airports, usual currency, travel style, accessibility and dietary preferences, visited places, wish list, explicit exclusions, and optional digital-travel preferences (normal map/booking apps, services to avoid, Google-service access, and non-sensitive booking-access notes). Never store passport numbers or images, payment/account credentials, exact addresses, local identity numbers, or private account data.

## Decision precedence

Use the current-trip form to decide what is applicable now; use the profile only to avoid re-entering stable defaults.

| Information | Rule |
| --- | --- |
| Current dates, party, budget, destination scope, travel geography, transport modes, climate and stay needs | Current-trip value is authoritative. Do not replace it from the profile. |
| Home city/country, airports, usual currency, pace, stable interests, accessibility, avoid-list, service preferences | Prefill only when the current-trip field is blank. The traveler can overwrite it. |
| Nationality, residence country, residence-status category | Use whenever the trip may leave the country of residence; omit when the traveller stays home. The status category is what makes the visa answer computable — store the category only, never a document number, image, or expiry date. |
| Profile exclusions and revisit settings | Apply as hard filters/diversity rules unless the current trip explicitly overrides them. |
| Dietary/religious food needs and `never_recommend` places | Carried into the current-trip intake as prefilled values, so they arrive as structured trip data rather than only living in the profile file. A hard rule that depends on someone remembering to open a second file is not a hard rule. |
| Maps, booking platforms and local transport operators | Select by the actual destination/route market and normal declared access; profile apps are a preference, not a mandate. |

Never infer how far a traveller wants to go from nationality, residence, language, currency, or a saved map app: that is the scope question's job. Use nationality and residence status only for the separate question of what entry a given destination requires. If a current-trip scope and named destination conflict, ask a short clarification before ranking.

## Place history semantics

| Profile list | Recommendation effect |
| --- | --- |
| `excluded_places` with `never_recommend` | Hard filter unless the user explicitly overrides it. |
| `excluded_places` with `avoid_for_now` | Strong preference; surface only if constraints make it necessary. |
| `visited_places` with `revisit_interest: no` | Avoid repeat recommendations. |
| Other visited places | Use to diversify, but do not assume a repeat is unwanted. |
| `wish_list` | Raise priority only when feasible; never bypass entry, budget, or dates. |

Keep reasons concise. Do not infer a sensitive reason for an exclusion. Ask whether a country-level exclusion also applies to transit stops when it matters.

## Workspace procedure

Use a user-selected local folder. The default implementation uses `Travel Buddy` directly inside the user’s home folder with:

- `profiles/` — opt-in reusable traveler profiles;
- `plans/` — researched plan JSON, including sources and assumptions;
- `html/` — final browse-only itinerary pages.

Run `python scripts/travel_workspace.py init` to create folders. Run `python scripts/travel_workspace.py create-profile <profile-id> --consent` only after opt-in. Fill the profile using the template, then run `python scripts/travel_workspace.py validate-profile <profile.json>` before relying on it. Do not overwrite an existing profile; update only the exact profile file the user names.

When exactly one valid profile exists the workflow reuses it without asking. Summarize what was loaded and confirm it before the trip form; `python scripts/start_intake_workflow.py --edit-profile` reopens the profile form preloaded with the saved values and then continues to the trip form.

### Guided form intake

Use `python scripts/start_intake_workflow.py --assistant auto` for the normal first-trip entry point. It checks the local `profiles/` directory: if there is no valid profile, it starts the one-time profile form; if there is exactly one valid profile, it proceeds directly to the current-trip form and pre-fills stable values; if there are multiple profiles, require `--profile PROFILE_ID`. Both forms speak Chinese or English and carry a switch; `--language zh|en` sets the language they open in, otherwise the saved profile's preferred output language decides, otherwise Chinese, and a first-time traveller's trip form follows the profile they have just saved. Stored values never change with the display language. The profile form itself is served by `python scripts/serve_profile_intake.py`, a temporary HTTP server bound only to `127.0.0.1`, with examples and inline privacy guidance. The browser submits JSON directly to the local process. On a first-trip save, the current-trip service is started before the profile service closes; its local URL is returned to the browser, which changes to the current-trip form in the same tab. The terminal also prints that URL as a fallback.

The form has no third-party scripts, remote requests, login, payment, or download/move/upload step. It may collect a non-sensitive note such as “avoid channels requiring a local phone”, but never card details, account context, or identity numbers. After the current-trip form submits, it emits `TRAVEL BUDDY NEXT STEP:` followed by the next action its work mode implies — `TRIP_CONSTRUCTION` when the destination scope is `fixed`, otherwise `DESTINATION_DISCOVERY` — together with the trip input, optional profile, and local workflow-event paths, and hands off to `scripts/run_destination_discovery.py`. It does not guess or resume a “last” conversation. Under `auto` the runner **always stands down** and prints the saved intake path for the assistant already working in this workspace to continue from. Two earlier versions tried to decide when a second assistant was safe to start — by recognising assistant names, then by a tty test — and each let one start beside the assistant already working, which is what produced two conflicting plans in a measured run; opencode, Cursor and Cline set none of the recognised variables and allocate a full pty, so the tty test saw a human. Continuation is therefore opt-in: `--assistant codex` or `--assistant claude` (or `TRAVEL_BUDDY_ASSISTANT=codex|claude`) starts the selected CLI in a new task, shows its output in the current terminal, saves a result plus run log under `plans/`, and records the child's PID and a copy-pasteable stop command in `plans/destination-discovery-*.pid.json` — the earlier version printed the PID nowhere durable, so a user who wanted to stop it could not. `--assistant none` disables continuation explicitly. If a profile name already exists, do not overwrite it unless the user explicitly approves starting the server with `--overwrite`.

### First-trip form intake

When no current-trip intake is available, use `python scripts/start_intake_workflow.py` rather than starting the trip form directly. A saved personal profile does not replace this per-trip form. Its companion HTML form collects departure point, dates/duration, party, budget, destination scope, experience preferences, per-traveler entry eligibility, transport tolerance, and climate constraints. It is also loopback-only and saves one `trip-profile.json`-compatible intake plus a `next-action-*.json` event under `plans/`; it does not create another reusable personal profile. The event carries the derived `work_mode` and a matching `next_action` — `trip_construction` for an already-fixed destination, otherwise `destination_discovery` — and must be acted on immediately.

After validating a final plan, run
`python scripts/save_trip_deliverables.py <plan.json> --verification <report.json>`. The
verification argument is not optional: without it, or without an explicit `--unverified`, the script
refuses to save at all — structure gates cannot tell you whether a fare, an opening time or an entry
rule is true, so a plan that never faced the parallel-verify stage does not get to look finished.
`--unverified` saves anyway, records `verification_status: unverified` in the plan and prints a
localized "not fact-checked" banner above everything on the page, because a gap recorded only in
JSON warns whoever opens the JSON, and that is never the person standing at an airline counter.
It saves paired JSON and HTML using a date/title filename and refuses to overwrite unless
`--overwrite` is deliberately supplied. Use a user-selected `--workspace` when the default location is not appropriate.

On an explicit forget/delete request, show the resolved profile path and delete only that profile. Never remove the entire workspace or other trips to satisfy a profile deletion request.
