# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-10-14

### Fixed

- **A quiet Vercel poll no longer sends its notes to the chat.** OpenClaw stays
  silent only when a cron command prints exactly `NO_REPLY`; anything on stderr
  is delivered with it. A poll that found errors below the threshold therefore
  sent `stdout: NO_REPLY / stderr: note: ...` with no project named, eleven
  times in two days on one install. `watch`, `vercel-watch` and `digest` now
  append a successful run's notes to `web-observer.log` beside the state file;
  a failed run still writes them to stderr.

### Changed

- **Error alerts list distinct errors.** An alert names the project and its
  domain, then each distinct error once with its count, routes, status,
  whether it was an HTTP failure or only logged an error line, and a sample
  request id.
  With `includeMessages` on, errors are grouped by message and quoted.
- **Opted-in messages are redacted.** Only the first line is sent, capped at
  200 characters, with common secret shapes replaced by `[redacted]`.

## [0.2.0] - 2026-10-14

### Added

- **The Vercel and GA4 modules watch more than one site.** `vercel.projects`
  takes a list of projects in place of `vercel.project`, and `ga4.properties` a
  list of properties in place of `ga4.property`; the singular forms still work.
  Each Vercel project is polled with its own query and keeps its own alert
  state, so one site's errors neither raise nor clear another's alert. The GA4
  digest gets one section per property, and a failing property no longer holds
  back the rest. Uptime already took one watch per URL.

### Changed

- **Vercel state is kept per project.** A state file written by 0.1.1 is read
  back and handed to the first configured project, so upgrading neither repeats
  an alert nor forgets an outstanding one.
- **`vercel-watch` saves its state even when it exits 2.** With several
  projects, a configuration problem on one must not stop another's alert from
  being remembered as sent.

## [0.1.1] - 2026-09-23

### Security

- **A Vercel error alert no longer quotes request paths.** An error with no
  recorded route was grouped under its concrete path, which whoever made the
  request chooses, so anybody could put text of their choice into the chat.
  Such errors are now counted as `(unrouted)`.
- **A redirect from https to http is no longer followed.** The allowlist
  compares hosts only, so a downgrade on the same host was followed and any
  configured header, such as an authorization token, was sent in the clear.
  It now fails the check with `redirect-off-allowlist`.
- **Configured headers are sent only to the watch's own host.** The allowlist
  is shared by every watch, so a redirect to another watch's host used to
  carry the first watch's headers with it.

### Changed

- **SKILL.md declares what it reads from `openclaw.json`.** A new section names
  the exact keys the Vercel and GA4 modules read, when, and why, so a reviewer
  need not find them in the code. It is prose rather than `requires.config`,
  which OpenClaw treats as an eligibility gate that would hold back an
  uptime-only install.
- **The `security_level: L1` frontmatter field is gone.** Neither ClawHub nor
  OpenClaw defines it, so it was a trust label nothing verified.

### Fixed

- **A watch whose interval equals the tick is no longer checked at half its
  rate.** The next due time was stamped when a check finished, so it landed a
  fraction of a second after the next round arrived, that round found the watch
  not due, and the check fell to the round after. The default configuration has
  both set to five minutes, so a five-minute watch was checked every ten, and an
  outage took up to twenty minutes to report instead of ten. A round now takes a
  watch that comes due within half a tick, so each due time is served by the
  nearer round.

## [0.1.0] - 2026-08-19

First release. Three things a website owner asks, answered from one command
line, with the first of them implemented here and the other two delegated.

### Added

- **Uptime watching.** A list of URLs, each with its own interval, checked by a
  single scheduled job that runs only what is due. One alert when a site goes
  down, one when it recovers, and silence in between. Status, body-substring and
  regular-expression expectations, so a 200 that renders an error page still
  fails. Typed failure reasons: `timeout`, `dns`, `connection-refused`, `tls`,
  `status-mismatch`, `body-mismatch`, `redirect-off-allowlist`, `network`.
- **Two independent blip guards.** `attempts` retries within one round, seconds
  apart, which catches a dropped packet. `failureThreshold` counts consecutive
  failed rounds, minutes apart, which catches a flaky minute.
- **A Vercel bridge.** Ad hoc traffic, speed and error-log questions, plus a
  scheduled poll that alerts on new errors and a performance budget check on
  Core Web Vitals. Errors are deduplicated across overlapping windows by request
  id, and the poll window widens to cover a missed cycle.
- **A GA4 bridge.** Ad hoc traffic questions and a scheduled digest.
- `check`, for verifying a configuration immediately without consuming the one
  alert a real outage is entitled to.
- `doctor`, which names one next step at a time, and `doctor --json` for an
  agent walking somebody through setup.
- `schedule`, which prints the `openclaw cron add` commands a configuration
  needs, and creates them with `--apply`.
- `--dry-run` on every command that would send a request or an alert.
- A systemd unit and timer, as a fallback for installs running with OpenClaw's
  cron disabled.

### Notes on how this works, all verified against a live OpenClaw 2026.7.1-2

- **Alerts travel over OpenClaw's own mechanism, and this skill holds no bot
  token.** A cron job with a `command` payload delivers the command's stdout to
  the configured chat channel, and the exact token `NO_REPLY` suppresses that
  delivery. So an alert is a scheduled command printing text, and silence is the
  same command printing `NO_REPLY`.
- **A scheduled run exits 0 even when it alerts**, because a non-zero exit would
  additionally fire OpenClaw's own cron failure notification and report one
  outage twice.
- **A cron command payload runs with the Gateway's environment**, which carries
  none of a skill's configured variables. Web Observer therefore reads the
  delegated skills' credentials from `openclaw.json` and passes them into those
  skills' own subprocess environment, rather than asking for them to be
  configured twice.
- **Vercel request logs must not be queried with an end in the past.** A window
  ending more than about an hour ago is answered `HTTP 400
  ExceedsBillingLimitError`; with the end left at now, every `--since` succeeds.
  The poller therefore never specifies an end.
- **An empty error log is not evidence of a healthy site**, because runtime logs
  are retained for one hour on Hobby. That is said in the alert rather than
  smoothed over.

### Security

- **Only user-configured hosts are contacted, enforced in code.** The allowlist
  is derived from the configured watch URLs by one function with no other input
  and no flag that extends it, and the host is re-checked before every request
  including every redirect hop. A redirect off the allowlist fails the check
  naming the host and is never followed. Redirects are not followed at all by
  default.
- Only `GET`, `HEAD` and `OPTIONS` are ever issued.
- **Raw Vercel log text is never forwarded into an alert unless the user opts
  in**, and that is enforced at the bridge rather than in the formatter: with
  `includeMessages` off, the message, the log lines and the raw row are not
  copied out of the bridge at all. The underlying skill scrubs only its own
  Vercel token from log content, so anything an application printed, including
  secrets and customer data, would otherwise arrive verbatim.
- A response body is measured, never quoted into an alert, and at most 1 MiB of
  it is read.
- Credentials travel only in a subprocess environment, never on a command line,
  never in output, never to a file.
- `requires.env` is empty, so uptime watching, which needs no credential, is
  never held in "needs setup" for one.

### Known limitations

- The Vercel error watch needs `openclaw-vercel-insights` 1.1.0, which currently
  lives on its `logs-surface` branch. An older copy is detected and reported by
  version and location, with the install command; traffic and speed keep
  working. See the TODO in README.md and in `src/bridge/vercel.ts`.
- There is no history: this tool alerts on change and does not keep a record of
  past outages beyond the current state.
- Retention figures for plans other than Hobby are taken from Vercel's
  documentation rather than measured.
