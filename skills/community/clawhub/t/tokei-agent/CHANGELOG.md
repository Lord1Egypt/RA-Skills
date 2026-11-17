# Changelog

All notable changes to `tokei-agent`. Dates are the npm publish times.

This file was seeded on 2026-08-02, after 0.3.2 shipped, by reconstructing the
history from `npm view tokei-agent time` and the commits that touched `cli/`.
Entries before 0.3.3 are therefore summaries written after the fact; entries
from 0.3.3 on are written as part of the release.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This package is pre-1.0: minor versions may carry breaking changes, though none
has so far.

## [Unreleased]

## [0.3.8] — 2026-10-23

### Changed

- Internal: MCP tools and CLI commands now come from one registry,
  `src/tool-manifest.json`, with request mapping in `src/tool-dispatch.ts`.
  Command arguments, output, exit codes, help text and the MCP tool list are
  unchanged.

- `engines.node` is now `>=22.12`. Node 22.0–22.11 printed an `ExperimentalWarning`
  about JSON modules on stderr on every run, because the CLI now imports
  `tool-manifest.json`. Output and MCP traffic were unaffected.

### Fixed

- A command named after a built-in object property (`tokei-agent toString`,
  `constructor`, `__proto__`) crashed with an `internal_error` and exit 1. It is
  now an unknown-command usage error, exit 2.

## [0.3.7] — 2026-10-18

### Changed

- **`media:upload` cap is 4 MB, down from 5 MB.** The CLI refuses a file over
  4 MB (or under 100 bytes) before sending it, with exit code `2` and a
  `usage_error`. The cap covers video as well as images. The 50/day media cap now
  counts uploads that pass validation. A rejected file uses no quota.
- **`pages:unpublish` hides the page.** Visitors to a draft page's URL see "This
  promotion isn't open right now" and cannot join. Only the signed-in owner still
  sees it. `--help`, the `pages_unpublish` tool description, `SKILL.md` and
  `README.md` no longer say a draft "still renders publicly".
- `SKILL.md` counts 28 writable `actions:catalog` types, up from 26. The two new
  ones are `tokei_cross_promote` and `app_download`. The CLI reads the catalog
  live, so no code changed.
- Hero image URLs for `pages_update` are described as `media.tokei.io` or
  `res.cloudinary.com` URLs, replacing the retired Supabase storage wording.
- Changing an `entry_methods` row's target keeps entrants' credit while the row
  keeps its `id`. Omit the `id` to make a new action. The `pages_update` tool
  description and `SKILL.md` say so.

### Fixed

- `SKILL.md` and `README.md` describe the one-POST `media:upload` that 0.3.6
  introduced. The 0.3.6 package still documents the retired two-step signed
  ticket.
- `SKILL.md` lists three zero-count templates (`secret-codes`, `survey-system`,
  `collect-email-list`), not two. A `secret-codes` clone forces its secret-code
  input **off**.
- `SKILL.md` names the deployment prerequisites that apply today (`linkedin_oidc`
  for `linkedin_share` and `linkedin_post`, Steam login for the three `steam_*`
  types) and no longer asks agents to warn about X/Twitter OAuth.
- Stale comments in `cli/src/index.ts`, `cli/src/media.ts` and
  `cli/bin/tokei-agent.mjs` that still described the two-step media flow.

## [0.3.6] — 2026-09-04

This entry was written on 2026-09-22. The release skipped the changelog step, so
the 0.3.6 tarball on npm carries no entry for itself.

### Fixed

- **`media:upload` works again.** Tokei moved media storage to
  `https://media.tokei.io/`, and `POST /api/v1/media` now answers `410 GONE` to
  the two-step signed-ticket request that 0.3.5 and earlier send. The CLI command
  and the `media_upload` MCP tool now send the file as one `multipart/form-data`
  POST. Caps are unchanged: 5 MB per file, video included, and no
  `application/pdf`. Anyone on 0.3.5 or older gets a 410 from `media:upload` until
  they upgrade.

### Changed

- `media:upload` returns a `public_url` on `https://media.tokei.io/` instead of a
  `…supabase.co/storage/…` URL. The `pages_update` media fields accept Tokei
  media, Supabase storage and Cloudinary URLs.
- `entry_methods` rows accept an optional `id` (`[A-Za-z0-9_-]`, 1–64 chars) for
  stable per-row identity. Two rows with the same `id` in one array are a 422.
- Up to 5 `entry_methods` rows may share one `actionType` for `twitter_follow`,
  `instagram_follow` and `facebook_visit_page`. Every other type is capped at 1,
  and exceeding a cap is a 422. `--help`, the `pages_update` tool description
  and `SKILL.md` document both rules.
- `SKILL.md` counts 26 writable `actions:catalog` types, up from 25.

## [0.3.5] — 2026-08-28

### Fixed

- **MCP tool calls no longer forward undeclared arguments.** `callTool` built the
  request body as `{ ...fixedBody, ...args }` and validated only that *required*
  arguments were present, so any extra field a caller invented rode through to the
  API. Because `PATCH /api/v1/contests/{id}` replaces `prizes` wholesale, a call of
  `pages_publish { contest_id, prizes: [] }` **wiped the page's prize list** — under
  a tool annotated `destructiveHint: false`. Arguments are now allowlisted against
  the tool's own `inputSchema.properties` before the merge; undeclared fields are
  dropped, and the tool result now names the ones it ignored rather than
  discarding them in silence. Declared arguments still win over `fixedBody`.

  One documented field was caught by this and is declared as part of the same
  release: `entries_create` accepted `marketing_consent`
  (`docs/using-custom-apis.md`) without advertising it, so the allowlist would
  have dropped it. See Added below.
- **`entries_create` was silently discarding `marketing_consent`.** The v1 route
  accepts it and the field gates whether an entrant is ever synced to the
  creator's connected email provider, so an import of consented entrants would
  have returned 201 on every row and synced none of them.

### Added

- `entries_create` declares `marketing_consent`. Set it to `true` only when the
  participant genuinely gave marketing consent elsewhere; it records the consent
  and its timestamp, and is what enables the email-provider sync.

### Changed

- `pages_update`'s description now states that `status` is not settable there and
  points at `pages_publish` / `pages_unpublish`. `status` stays undeclared on
  purpose — `pages_publish` enforces a future-`end_date` check that a raw
  `status: "active"` would bypass.
- `webhooks_delete` now declares `idempotentHint: true`, and its description states
  that the subscription's queued and historical `webhook_deliveries` rows are
  deleted with it (`ON DELETE CASCADE`), so past delivery attempts are not
  retrievable afterwards.
- The MCP server instructions and the `pages_unpublish` description are reworded
  from instructing the agent ("slow down", "Tell your user this…") to describing
  what the API does. No behavioural change.

## [0.3.4] — 2026-08-21

### Added

- `pages:update --template simple` — the Custom template: bare structural
  markup the creator styles entirely via `--custom-css`, rather than a fixed
  layout.
- `pages:update --custom-css <css>` — creator CSS for the Custom template,
  applied on both the hosted page and the widget embed via `--tokei-*` custom
  properties and `.tokei-simple-*` class hooks. Max 20 KB; server-sanitised,
  with unsafe constructs rejected by a 422 naming the reason.
- `--card-width` gains `xl` and `max-w-7xl`, in both the CLI flag and the
  `pages_update` MCP tool's schema.
- `entry_methods` — the page's action buttons — is now settable through
  `pages:update --data` and the `pages_update` MCP tool, alongside `prizes`
  and `reward_thresholds`. Replaces the whole list wholesale: an action row
  (`actionType`, `label`, `points?`, `config?`, `requireVerification?`) or a
  custom-link row (`label`, `points?`, `link`, `actionsRequired?`) with no
  `actionType`.

## [0.3.3] — 2026-08-03

### Added

- `events:catalog` (+ `--type`) and the `events_catalog` MCP tool — every
  webhook event Tokei can send, with its payload schema, description and emit
  sites, fetched from the API rather than bundled so the CLI can never drift
  from the platform. **21 commands, 21 MCP tools.**
- `winners:list <contestId>` and the `winners_list` MCP tool — read-only
  selection-run history with the winners of each run. Unpaginated, capped at the
  100 most recent runs. Selecting winners stays a human action in the dashboard;
  the CLI can only read the result.
- **All five webhook events are now subscribable**, not just `entry.created`:
  `contest.ended`, `winner.selected`, `daily_bonus.claimed` and
  `referral.converted` now fire on the live platform and are accepted by
  `webhooks:create --events`. Previously they were catalogued but rejected with
  a 422.
- **Installable as a Claude Code plugin** — a fifth distribution channel
  alongside npm, skills.sh, ClawHub and the MCP registry:

  ```
  /plugin marketplace add gilesdawe/tokei-agent
  /plugin install tokei-agent@tokei
  ```

  The skill then loads automatically as `tokei-agent:tokei-agent`, with no
  `npx skills add` step. Adds `.claude-plugin/plugin.json` and
  `.claude-plugin/marketplace.json` to the repo. Not included in the npm
  tarball — plugin users install from GitHub.
- The ANSI wordmark now renders above `--help` at an interactive terminal.
  Previously `--help` returned before the terminal UI was created, so the first
  command most people run was undecorated. Suppressed — byte for byte — for
  pipes, redirects, CI, `TERM=dumb`, `TOKEI_OUTPUT=json` and terminals narrower
  than 60 columns, so parsed output is unchanged.
- `SKILL.md` gains a fourth hard rule: get explicit human approval before any
  action that emails people or changes anything public, with the read-only
  commands listed as exempt.

### Fixed

- The `webhooks_create` MCP tool advertised `entry.created` as the only valid
  value for `events`, in both its JSON-schema `enum` and its description. MCP
  clients read that schema as the contract, so an agent had no way to subscribe
  to the four events this release activates. The CLI's own `webhooks:create` was
  never affected.

### Changed

- This changelog now ships in the tarball. It was added 27 minutes after 0.3.2
  published, so 0.3.3 is the first release to carry it.
- `SKILL.md`'s `templates:list` sample is refreshed against the live 14-template
  menu and marked as an excerpt. It was always illustrative — call the endpoint,
  never hardcode a slug.

## [0.3.2] — 2026-08-02

### Added

- `referrals:top <contestId>` and the `referrals_top` MCP tool — top referrers
  ranked by conversions, plus click/conversion totals. Lists only entrants who
  have actually referred someone. **19 commands, 19 MCP tools.**

### Fixed

- The interactive-output note in `README.md` / `SKILL.md` said "0.3.2+"; the
  feature shipped in 0.3.1.

## [0.3.1] — 2026-08-02

### Added

- `actions:catalog` (+ `--type`) and the matching MCP tool — every entry-action
  type Tokei supports, fetched from the API rather than bundled, so the CLI can
  never drift from the platform.
- Interactive terminal output: the ANSI wordmark on `me`, plus a step line,
  animated spinner and one-line summary elsewhere. Inert unless a real terminal
  is attached — `TOKEI_OUTPUT=json`, `NO_COLOR` and `TOKEI_NO_ANIM=1` all
  control it.

### Fixed

- `--version` now reports the real version. The 0.3.0 tarball was built from a
  tree still labelled 0.2.2 and reported that instead.

## [0.3.0] — 2026-07-26

### Added

- `media:upload <file>` and the `media_upload` MCP tool — two-step signed-ticket
  upload (request a ticket, PUT the bytes), returning a `public_url`.
- Seven media flags on `pages:update`: `--image-video`, `--secondary-image`,
  `--third-image`, `--fourth-image`, `--fifth-image`, `--background-image`,
  `--og-image`.

### Fixed

- Exit-code corruption on Node 24 / Windows: the CLI printed correct JSON and
  then aborted during process exit, so `$LASTEXITCODE` read `-1073740791`
  (`0xC0000409`) on success and failure alike.

### Known issue

- This tarball reports `--version` as `0.2.2`. Fixed in 0.3.1.

## [0.2.2] — 2026-07-25

### Changed

- Documented the exit-code contract: `0` success, `1` API/network error,
  `2` usage error.

## [0.2.1] — 2026-07-22

### Added

- `templates:list` and clone-by-slug (`pages:clone --template <slug>`).
- `pages:publish` / `pages:unpublish` (status draft ⇄ active; publishing
  requires a future `end_date`).
- Appearance flags on `pages:update`: `--template`, `--dark-mode`,
  `--primary-color`, `--card-width`.

## [0.2.0] — 2026-07-20

### Added

- `mcp` — the bundled MCP stdio server, exposing every command as an MCP tool
  for Claude Code, Claude Desktop and other MCP clients.

## [0.1.0] — 2026-07-20

### Added

- Write commands: `pages:clone`, `pages:update`, `entries:create`,
  `webhooks:create`, `webhooks:delete`.
- `SKILL.md` and `README.md`, making the package usable as an agent skill.

## [0.0.1] — 2026-07-20

### Added

- First publish. Read commands (`me`, `pages:list`, `pages:get`, `stats`,
  `leaderboard`, `entries:list`, `surveys:list`, `webhooks:list`), `TOKEI_API_KEY`
  auth, JSON-only stdout with a top-level `rate_limit` object, zero runtime
  dependencies.

[unreleased]: https://github.com/gilesdawe/tokei-agent/compare/v0.3.8...HEAD
[0.3.8]: https://www.npmjs.com/package/tokei-agent/v/0.3.8
[0.3.7]: https://www.npmjs.com/package/tokei-agent/v/0.3.7
[0.3.6]: https://www.npmjs.com/package/tokei-agent/v/0.3.6
[0.3.5]: https://www.npmjs.com/package/tokei-agent/v/0.3.5
[0.3.4]: https://www.npmjs.com/package/tokei-agent/v/0.3.4
[0.3.3]: https://www.npmjs.com/package/tokei-agent/v/0.3.3
[0.3.2]: https://www.npmjs.com/package/tokei-agent/v/0.3.2
[0.3.1]: https://www.npmjs.com/package/tokei-agent/v/0.3.1
[0.3.0]: https://www.npmjs.com/package/tokei-agent/v/0.3.0
[0.2.2]: https://www.npmjs.com/package/tokei-agent/v/0.2.2
[0.2.1]: https://www.npmjs.com/package/tokei-agent/v/0.2.1
[0.2.0]: https://www.npmjs.com/package/tokei-agent/v/0.2.0
[0.1.0]: https://www.npmjs.com/package/tokei-agent/v/0.1.0
[0.0.1]: https://www.npmjs.com/package/tokei-agent/v/0.0.1
