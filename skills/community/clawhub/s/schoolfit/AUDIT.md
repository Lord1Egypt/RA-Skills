# SchoolFit Audit Boundary

This file documents the security and product boundary for ClawHub review.

## Runtime Access

- The helper calls only `https://schoolfit.hk/api/...` and the session-code page at `https://schoolfit.hk/skill-code`.
- The default base URL is fixed to `https://schoolfit.hk`; custom schemes, embedded user-info, ports, and non-API paths are rejected by the helper.
- The published runtime helper does not read machine-local content, shell configuration, cookies, browser storage, or private project files.
- The skill does not read local databases, Prisma schemas, SQLite files, raw data snapshots, `.env` files, student files, or browser storage.
- The skill does not call `/api/agent/chat` in v1.

## Access Code

- The `sfhk_...` code is a SchoolFit access code for trial API use and low-detail usage telemetry.
- It is not a school account login or student identity.
- Agents should keep the code only in the active one-to-one chat context or pass it with `--skill-code` for the current run.
- The full code must not be written to disk, logs, examples, issue trackers, commits, screenshots, marketplace listings, or final answers.

## Query Transmission

- Live commands with `--q` send the provided school-search preference text to `https://schoolfit.hk/api/...` for that request.
- Agents must tell users this before live queries and ask them to remove student names, HKID, phone numbers, addresses, report-card details, and private document contents.
- `parse-parent-request` is the local-only option for first-pass parsing; it does not call SchoolFit APIs.

## Privacy And Telemetry

- Telemetry records only command, endpoint, traceId, status/error, latency, activation status, skill version, and session-code hash prefix.
- Telemetry does not include the full session access code, raw parent question, student name, HKID, personal phone, address, report-card content, or private documents.
- Obvious HKID, personal phone, email, address, full student name, and document-content inputs are blocked before SchoolFit API calls.

## Read-Oriented Boundary

- SchoolFit returns school information, comparisons, checklists, and reminders.
- It does not operate external school systems or act on behalf of a family.
- Vacancy and admissions data are time-limited leads, not guarantees.
- Application plans are checklists and reminders only; families must complete any official school process themselves.

## Review Notes

- The access code is deliberately scoped and non-student-identifying.
- All remote calls are constrained to the SchoolFit domain and documented API paths.
